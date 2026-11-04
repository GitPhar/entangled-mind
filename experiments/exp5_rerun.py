"""Experiment 5, run 2: B0 and the QQ block re-run on the first 10 candidates with one scale direction
(anchor (a): 0 = certainly false, 100 = certainly true), as pre-registered in the Addendum to
experiments/exp5-sequential-judgment.md (D33). Descriptive; no refitting.

    python experiments/exp5_rerun.py

$1 cap; any refusal stops the run. Calls cached in results/exp5-run-2-conversations.json.
Writes results/exp5-run-2.{json,md}."""

import json
import sys
from concurrent.futures import ThreadPoolExecutor

import numpy as np

import exp5_analyse as ea
import exp5_run as er
from entangled_mind import config

CONV2 = config.RESULTS / "exp5-run-2-conversations.json"
OUT_JSON, OUT_MD = config.RESULTS / "exp5-run-2.json", config.RESULTS / "exp5-run-2.md"


def jobs_for(qid, split):
    out = [(f"{qid}|B0|{r}", qid, [("M", None)], "a") for r in range(er.R_CHAIN)]
    for k in split["qq_pairs"][qid]:
        for order in ("SM", "MS"):
            t = [("S", k), ("M", None)] if order == "SM" else [("M", None), ("S", k)]
            out += [(f"{qid}|QQ{k}{order}|{r}", qid, t, "a") for r in range(er.R_QQ)]
    return out


def summarise(conv, items, recs, split):
    qq = ea.qq_check(items, recs, conv, split)
    b0 = {}
    for q in items:
        v = [conv[f"{q}|B0|{r}"]["turns"][-1]["rating"] for r in range(er.R_CHAIN)
             if f"{q}|B0|{r}" in conv and conv[f"{q}|B0|{r}"]["turns"] and conv[f"{q}|B0|{r}"]["turns"][-1]["kind"] == "M"]
        b0[q] = {"mean": float(np.mean(v)) if v else float("nan"), "sd": float(np.std(v, ddof=1)) if len(v) > 1 else float("nan"),
                 "n": len(v)}
    return qq, b0


def main() -> None:
    split = json.loads(er.SPLIT.read_text())
    recs = {r["id"]: r for r in json.loads(er.POOL.read_text())["records"]}
    items = er.candidates()[:10]
    er.BUDGET_USD = 1.0
    er.CONV = CONV2                     # separate cache; run 1's conversations are untouched
    er._cache.clear()
    er._cache.update(json.loads(CONV2.read_text()) if CONV2.exists() else {})
    jobs = [j for q in items for j in jobs_for(q, split)]
    with ThreadPoolExecutor(max_workers=6) as ex:
        list(ex.map(lambda j: er.converse(j, recs), jobs))
    CONV2.write_text(json.dumps(er._cache))
    if er._refusal:
        key, e = er._refusal["e"]
        (config.RESULTS / "refusal.md").write_text(
            f"# Pipeline stopped on a refusal\n\nExperiment 5 run 2, conversation `{key}`\n\nRefused call: **{e.call}**\n\n"
            f"Request ID: `{e.request_id}`\n\nExact stop details:\n\n```\n{e.stop_details}\n```\n\nNothing was reworded or retried.\n")
        sys.exit(f"STOPPED: {e}")
    if er._stop.is_set():
        sys.exit("budget stop")
    analyse(items, recs, split, dict(er._cache))


def analyse(items, recs, split, conv2) -> None:
    conv1 = json.loads(er.CONV.read_text() if er.CONV != CONV2 else (config.RESULTS / "exp5-conversations.json").read_text())
    conv1_a = {k: v for k, v in conv1.items() if v.get("anchor") == "a"}
    runs = {"run 2 (anchor a only)": conv2, "run 1, anchor a only": conv1_a, "run 1, both anchors pooled": conv1}
    res = {name: summarise(c, items, recs, split) for name, c in runs.items()}
    big1 = {(p["item"], p["claim"]) for p in res["run 1, both anchors pooled"][0]["pairs"]
            if p["stats"]["OE"] > 0.10 and p["OE_ci95"][0] > 0}
    big2 = {(p["item"], p["claim"]) for p in res["run 2 (anchor a only)"][0]["pairs"]
            if p["stats"]["OE"] > 0.10 and p["OE_ci95"][0] > 0}
    survive = len(big1 & big2), len(big1)
    q2 = res["run 2 (anchor a only)"][0]
    oe_survive = survive[1] > 0 and survive[0] >= survive[1] / 2
    q_ci = q2.get("mean_q_ci95")
    q_survive = q_ci is not None and q_ci[0] <= 0 <= q_ci[1]
    q_resolved = q_survive and q_ci[0] >= -0.05 and q_ci[1] <= 0.05
    cost = sum(v["cost"] for v in conv2.values())
    OUT_JSON.write_text(json.dumps({"items": items, "summaries": {k: {"qq": v[0], "b0": v[1]} for k, v in res.items()},
                                    "large_OE_pairs_run1": sorted(map(list, big1)), "large_OE_pairs_run2": sorted(map(list, big2)),
                                    "order_effects_survive": oe_survive, "q_survives_near_zero": q_survive,
                                    "qq_near_miss_resolved": q_resolved, "n_conversations": len(conv2), "cost_usd": cost},
                                   indent=1, default=float))
    f = lambda c: "—" if c is None else f"[{c[0]:+.3f}, {c[1]:+.3f}]"
    lines = ["# Experiment 5, run 2: B0 and the QQ block with one scale direction", "",
             "Pre-registered in the Addendum to `experiments/exp5-sequential-judgment.md` (D33). The first 10 candidates "
             f"({', '.join(items)}), with every conversation on anchor (a) (0 = certainly false, 100 = certainly true). "
             f"Descriptive; no refitting. {len(conv2)} conversations, **${cost:.2f}**.", "",
             "| measurement | pairs with OE > 0.10 (CI excl. 0) | mean q [95% item-bootstrap CI] | KS of z vs N(0,1) | B0 mean (SD across items) | B0 between-repeat SD (median) |",
             "|---|---|---|---|---|---|"]
    for name, (qq, b0) in res.items():
        means = [v["mean"] for v in b0.values()]
        sds = [v["sd"] for v in b0.values() if v["sd"] == v["sd"]]
        ks = "—" if "KS_p" not in qq else f"D = {qq['KS_D']:.2f}, p = {qq['KS_p']:.3f}"
        lines.append(f"| {name} | {qq['n_large_OE']} of {qq['n_pairs']} | "
                     f"{('—' if 'mean_q' not in qq else format(qq['mean_q'], '+.3f'))} {f(qq.get('mean_q_ci95'))} | {ks} | "
                     f"{np.nanmean(means):.1f} ({np.nanstd(means):.1f}) | {np.median(sds) if sds else float('nan'):.1f} |")
    lines += ["", "## Per pair (run 2)", "", "| pair | OE [95% CI] | OE_S | OE_M | q | z | run 1 OE (pooled) |", "|---|---|---|---|---|---|---|"]
    r1p = {(p["item"], p["claim"]): p for p in res["run 1, both anchors pooled"][0]["pairs"]}
    for p in q2["pairs"]:
        s = p["stats"]
        o1 = r1p.get((p["item"], p["claim"]))
        lines.append(f"| {p['item']}:S{p['claim']} | {s['OE']:.2f} [{p['OE_ci95'][0]:.2f}, {p['OE_ci95'][1]:.2f}] | {s['OE_S']:+.2f} | "
                     f"{s['OE_M']:+.2f} | {s['q']:+.3f} | {s['z']:+.2f} | {o1['stats']['OE']:.2f} |" if o1 else "")
    lines += ["", "## Pre-registered reading", "",
              f"- **Order effects survive** (at least half of run 1's large-OE pairs still large): **{oe_survive}**. "
              f"{survive[0]} of {survive[1]} run-1 large-OE pairs are large in run 2.",
              f"- **Near-zero q survives** (run 2's mean-q CI contains 0): **{q_survive}**. Run 1's QQ near-miss is resolved "
              f"(the CI also lies within ±0.05): **{q_resolved}**."]
    OUT_MD.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()

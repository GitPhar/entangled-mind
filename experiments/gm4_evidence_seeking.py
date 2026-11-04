"""Gold-map direction 4: the evidence-seeking menu test, as pre-registered in
experiments/gm4-evidence-seeking.md (D39). $0.50 cap; any refusal stops the run.

    python experiments/gm4_evidence_seeking.py            # run (cached), then analyse
    python experiments/gm4_evidence_seeking.py --analyse  # analysis only

Calls cached in results/gm4-calls.json. Writes results/gm4-evidence-seeking.{json,md}."""

import json
import sys

import numpy as np

import exp5_run as er
from entangled_mind import config
from gm_common import PLAIN, Caller, structured

CACHE = config.RESULTS / "gm4-calls.json"
MENUS = config.EXPERIMENTS / "gm4-menus.json"
OUT_JSON, OUT_MD = config.RESULTS / "gm4-evidence-seeking.json", config.RESULTS / "gm4-evidence-seeking.md"
R, CAP, BOOT_SEED, LETTERS = 10, 0.5, 4040, "ABCD"
RULES = ["EIG_D5", "EIG_BA5", "dM_D5", "dM_BA5", "confirmatory", "most_uncertain"]
SCHEMA = {"type": "object", "properties": {"choice": {"type": "string", "enum": list(LETTERS)}}, "required": ["choice"],
          "additionalProperties": False}
PROMPT = """Here is a yes/no question and an answer you gave to it.

Question: {question}

Your answer:
{answer}

Suppose you could check exactly one of the following statements and find out for certain whether it is true. Which one would you check first, to best decide the answer to the question?

{options}

Answer with the letter only."""


def shown(menu, r):
    """Claims in screen order for repeat r: menu claim i at position (i + r) mod 4."""
    order = [None] * 4
    for i, k in enumerate(menu):
        order[(i + r) % 4] = k
    return order


def run():
    recs = {r["id"]: r for r in json.loads(er.POOL.read_text())["records"]}
    menus = json.loads(MENUS.read_text())["items"]
    c = Caller(CACHE, CAP, "direction 4")

    def call(job):
        _, q, mi, r = job
        rec = recs[q]
        order = shown(menus[q]["menus"][mi], r)
        opts = "\n".join(f"{LETTERS[p]}. {rec['contentions'][k]['text']}" for p, k in enumerate(order))
        text = PROMPT.format(question=rec["question"], answer=rec["deliberation_record"]["visible_answer"], options=opts)
        d, _, cost, rid = structured(er.MODEL, [{"role": "user", "content": text}], SCHEMA, "gm4", max_tokens=50)
        p = LETTERS.index(d["choice"])
        return {"position": p, "claim": order[p], "cost": cost, "request_id": rid}
    jobs = [(f"{q}|{mi}|{r}", q, mi, r) for q in menus for mi in range(3) for r in range(R)]
    c.run(jobs, call, workers=8)


def target(menu, sc, rule):
    vals = {k: sc[str(k)][rule] for k in menu}
    if rule == "confirmatory" and max(vals.values()) < 0:
        return None
    best = max(vals.values())
    return {k for k, v in vals.items() if v >= best - 1e-9}


def analyse():
    conv = json.loads(CACHE.read_text())
    menus = json.loads(MENUS.read_text())["items"]
    items = list(menus)
    rows = []          # one per menu: item, choices, target sets
    for q in items:
        for mi, menu in enumerate(menus[q]["menus"]):
            ch = [conv[f"{q}|{mi}|{r}"]["claim"] for r in range(R) if f"{q}|{mi}|{r}" in conv]
            pos = [conv[f"{q}|{mi}|{r}"]["position"] for r in range(R) if f"{q}|{mi}|{r}" in conv]
            rows.append({"item": q, "menu": mi, "claims": menu, "choices": ch, "positions": pos,
                         "targets": {rule: (sorted(t) if (t := target(menu, menus[q]["scores"], rule)) is not None else None)
                                     for rule in RULES}})

    def hit(rws, rule):
        h, ch, n = 0.0, 0.0, 0
        for rw in rws:
            t = rw["targets"][rule]
            if t is None:
                continue
            h += sum(c in t for c in rw["choices"])
            ch += len(t) / 4 * len(rw["choices"])
            n += len(rw["choices"])
        return (h / n, ch / n) if n else (float("nan"), float("nan"))

    by_item = {q: [rw for rw in rows if rw["item"] == q] for q in items}
    rng = np.random.default_rng(BOOT_SEED)
    samples = [list(rng.choice(items, len(items))) for _ in range(2000)]
    expand = lambda s: [rw for q in s for rw in by_item[q]]
    res = {"n_calls": len(conv), "cost_usd": sum(v["cost"] for v in conv.values()), "rules": {}, "discriminating": {}}
    for rule in RULES:
        h, c = hit(rows, rule)
        bs = [np.subtract(*hit(expand(s), rule)) for s in samples]
        res["rules"][rule] = {"hit": h, "chance": c, "excess": h - c,
                              "excess_ci95": [float(x) for x in np.nanpercentile(bs, [2.5, 97.5])]}

    def disc_rows(rws, X):
        return [rw for rw in rws if rw["targets"]["confirmatory"] is not None
                and not set(rw["targets"][X]) & set(rw["targets"]["confirmatory"])]
    verdicts = {}
    for X in ("EIG_D5", "EIG_BA5"):
        dr = disc_rows(rows, X)
        d = hit(dr, X)[0] - hit(dr, "confirmatory")[0]
        bs = []
        for s in samples:
            e = disc_rows(expand(s), X)
            if e:
                bs.append(hit(e, X)[0] - hit(e, "confirmatory")[0])
        lo, hi = np.nanpercentile(bs, [2.5, 97.5])
        res["discriminating"][X] = {"n_menus": len(dr), "hit_X_minus_confirmatory": d, "ci95": [float(lo), float(hi)]}
        ex, cf = res["rules"][X]["excess_ci95"], res["rules"]["confirmatory"]["excess_ci95"]
        if ex[0] > 0 and lo > 0:
            verdicts[X] = "tracks EIG"
        elif cf[0] > 0 and hi < 0:
            verdicts[X] = "confirmatory"
        else:
            verdicts[X] = "neither"
    res["per_model"] = verdicts
    v = set(verdicts.values())
    res["verdict"] = ("EIG-tracking" if v == {"tracks EIG"} else "confirmatory" if v == {"confirmatory"} else "mixed or at chance")
    res["uncertainty_caveat"] = res["rules"]["most_uncertain"]["excess"] >= max(res["rules"]["EIG_D5"]["excess"],
                                                                                 res["rules"]["EIG_BA5"]["excess"])
    allpos = [p for rw in rows for p in rw["positions"]]
    res["position_share"] = [float(np.mean([p == i for p in allpos])) for i in range(4)]
    res["modal_share_mean"] = float(np.mean([max(np.bincount(rw["choices"]).tolist()) / len(rw["choices"]) for rw in rows if rw["choices"]]))
    res["D5_BA5_argmax_agree"] = int(sum(rw["targets"]["EIG_D5"] == rw["targets"]["EIG_BA5"] for rw in rows))
    res["menus"] = rows
    OUT_JSON.write_text(json.dumps(res, indent=1))
    write_md(res)


def write_md(r):
    names = {"EIG_D5": "EIG under D5", "EIG_BA5": "EIG under BA5", "dM_D5": "expected |ΔM| under D5", "dM_BA5": "expected |ΔM| under BA5",
             "confirmatory": "confirmatory (supports its own answer)", "most_uncertain": "most uncertain claim (confidence nearest 0.5)"}
    lines = ["# Direction 4: does the model seek the evidence that would settle its own conflict?", "",
             "Pre-registered in `experiments/gm4-evidence-seeking.md` (D39), committed before any call. 40 experiment-5 items × 3 menus "
             f"of 4 of its own claims × 10 repeats, `claude-haiku-5-5`, thinking disabled. {r['n_calls']} calls, **${r['cost_usd']:.2f}** "
             "of the $0.50 cap; no refusal.", "", PLAIN,
             "## Which rule picks the claim the model chose?", "",
             "| rule | hit rate | chance | excess over chance [95% item-bootstrap CI] |", "|---|---|---|---|"]
    for k, v in r["rules"].items():
        lines.append(f"| {names[k]} | {v['hit']:.0%} | {v['chance']:.0%} | {v['excess']:+.3f} [{v['excess_ci95'][0]:+.3f}, {v['excess_ci95'][1]:+.3f}] |")
    lines += ["", "On menus where the EIG choice and the confirmatory choice differ:", "",
              "| EIG model | menus | hit(EIG) − hit(confirmatory) [95% CI] | per-model reading |", "|---|---|---|---|"]
    for X, d in r["discriminating"].items():
        lines.append(f"| {names[X]} | {d['n_menus']} | {d['hit_X_minus_confirmatory']:+.3f} [{d['ci95'][0]:+.3f}, {d['ci95'][1]:+.3f}] | {r['per_model'][X]} |")
    lines += ["", f"- Choice share by screen position A–D: {', '.join(f'{x:.0%}' for x in r['position_share'])}.",
              f"- Mean share of the modal choice per menu: {r['modal_share_mean']:.0%}.",
              f"- D5 and BA5 EIG argmax sets agree on {r['D5_BA5_argmax_agree']} of {len(r['menus'])} menus.",
              f"- Most-uncertain explains choices at least as well as EIG: **{r['uncertainty_caveat']}**.", "",
              f"## Pre-registered verdict: **{r['verdict']}**"]
    OUT_MD.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    if "--md-only" in sys.argv:
        write_md(json.loads(OUT_JSON.read_text()))
    else:
        if "--analyse" not in sys.argv:
            run()
        analyse()

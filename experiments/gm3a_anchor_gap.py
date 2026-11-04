"""Gold-map direction 3, free look: the per-item anchor-direction gap against the model's errors,
as pre-registered in experiments/gm3a-anchor-gap.md (D35). No API calls.

    python experiments/gm3a_anchor_gap.py

Writes results/gm3a-anchor-gap.{json,md}."""

import json
import sys

import numpy as np

import exp5_run as er
from entangled_mind import config
from gm_common import PLAIN, boot_auroc, paired_boot_auroc

OUT_JSON, OUT_MD = config.RESULTS / "gm3a-anchor-gap.json", config.RESULTS / "gm3a-anchor-gap.md"
SEED = 3030


def first_m(c):
    if c is None or any(t["kind"] == "error" for t in c["turns"]) or not c["turns"] or c["turns"][0]["kind"] != "M":
        return None
    return c["turns"][0]["rating"]


def ratings(conv, q, split, equivalent):
    keys = [f"{q}|B0|{r}" for r in range(er.R_CHAIN)]
    if equivalent:
        keys += [f"{q}|MF|{r}" for r in range(er.R_CHAIN)]
        keys += [f"{q}|QQ{k}MS|{r}" for k in split["qq_pairs"][q] for r in range(er.R_QQ)]
    out = {"a": [], "b": []}
    for k in keys:
        c = conv.get(k)
        v = first_m(c)
        if v is not None:
            out[c["anchor"]].append(v)
    return out


def main() -> None:
    split = json.loads(er.SPLIT.read_text())
    items = split["candidates"]
    recs = {r["id"]: r for r in json.loads(er.POOL.read_text())["records"]}
    conv = json.loads((config.RESULTS / "exp5-conversations.json").read_text())
    g = json.loads((config.RESULTS / "arm-g-confidence.json").read_text())
    rows = []
    for q in items:
        b0, eq = ratings(conv, q, split, False), ratings(conv, q, split, True)
        rows.append({"item": q, "wrong": not recs[q]["correct"], "n_b0": [len(b0["a"]), len(b0["b"])],
                     "mean_a": float(np.mean(b0["a"])), "mean_b": float(np.mean(b0["b"])),
                     "gap": float(np.mean(b0["a"]) - np.mean(b0["b"])),
                     "n_eq": [len(eq["a"]), len(eq["b"])], "gap_eq": float(np.mean(eq["a"]) - np.mean(eq["b"])),
                     "G": g[q]["confidence"]})
    y = np.array([r["wrong"] for r in rows])
    scores = {"|gap| (B0)": np.array([abs(r["gap"]) for r in rows]),
              "signed gap (B0)": np.array([r["gap"] for r in rows]),
              "|gap| (B0-equivalent first turns)": np.array([abs(r["gap_eq"]) for r in rows]),
              "100 − G (arm-G self-confidence)": np.array([100 - r["G"] for r in rows]),
              "50 − |mean_a − 50| (anchor-a B0 extremity)": np.array([50 - abs(r["mean_a"] - 50) for r in rows])}
    res = {k: boot_auroc(v[y], v[~y], SEED) for k, v in scores.items()}
    diff = paired_boot_auroc(scores["|gap| (B0)"], scores["100 − G (arm-G self-confidence)"], y, SEED + 1)
    from scipy.stats import spearmanr
    rho = spearmanr(scores["|gap| (B0)"], [r["G"] for r in rows])
    lo, hi = res["|gap| (B0)"][1:]
    reading = "the gap predicts errors" if lo > 0.5 else ("the gap predicts correctness" if hi < 0.5 else "no evidence either way")
    out = {"rows": rows, "auroc": res, "gap_minus_G": diff, "spearman_absgap_G": [float(rho.statistic), float(rho.pvalue)],
           "reading": reading,
           "mean_abs_gap": {"wrong": float(np.mean(scores["|gap| (B0)"][y])), "right": float(np.mean(scores["|gap| (B0)"][~y]))}}
    OUT_JSON.write_text(json.dumps(out, indent=1))
    write_md(out)


def write_md(o) -> None:
    f = lambda d: f"{d[0]:.2f} [{d[1]:.2f}, {d[2]:.2f}]"
    lines = ["# Direction 3, free look: does the scale-direction gap predict the model's errors?", "",
             "Pre-registered in `experiments/gm3a-anchor-gap.md` (D35), committed before this analysis. 40 experiment-5 items "
             f"({sum(r['wrong'] for r in o['rows'])} wrong, {sum(not r['wrong'] for r in o['rows'])} right in the hard pool); "
             "no API calls; $0.", "", PLAIN,
             "## Results", "", "| score (higher = predicted wrong) | AUROC for the model's errors [95% CI] |", "|---|---|"]
    for k, v in o["auroc"].items():
        lines.append(f"| {k} | {f(v)} |")
    lines += ["", f"- Mean |gap|: {o['mean_abs_gap']['wrong']:.1f} points on wrong items, {o['mean_abs_gap']['right']:.1f} on right items.",
              f"- Paired difference AUROC(|gap|) − AUROC(100 − G): {o['gap_minus_G'][0]:+.2f} [{o['gap_minus_G'][1]:+.2f}, {o['gap_minus_G'][2]:+.2f}].",
              f"- Spearman ρ(|gap|, G) = {o['spearman_absgap_G'][0]:+.2f} (p = {o['spearman_absgap_G'][1]:.3f}).", "",
              "## Per item", "", "| item | wrong | B0 mean, anchor a | B0 mean, anchor b (recoded) | gap | gap (B0-equivalent, n per direction) | G |",
              "|---|---|---|---|---|---|---|"]
    for r in o["rows"]:
        lines.append(f"| {r['item']} | {'yes' if r['wrong'] else 'no'} | {r['mean_a']:.1f} | {r['mean_b']:.1f} | {r['gap']:+.1f} | "
                     f"{r['gap_eq']:+.1f} ({r['n_eq'][0]}) | {r['G']} |")
    lines += ["", f"## Pre-registered reading: **{o['reading']}**"]
    OUT_MD.write_text("\n".join(lines) + "\n")
    print("\n".join(lines[:16] + lines[-1:]))


if __name__ == "__main__":
    write_md(json.loads(OUT_JSON.read_text())) if "--md-only" in sys.argv else main()

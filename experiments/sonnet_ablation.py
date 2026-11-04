"""Addendum D: what is the Sonnet edge? Coupling ablation and a classical twin with A2's readout geometry.

    python experiments/sonnet_ablation.py

A2(kappa=0): frozen v2 A2 parameters with k_sup = k_con = 0 (product state of tilted qubits).
F2+: F2 with A2's per-claim tilted-readout marginal, fitted on the v2 train split only (seed 707),
selected on validation. Both scored once on Haiku's locked v2 test set and on Sonnet's 298 hard-pool
records, beside the frozen A2 and F2. No API calls (the client is blocked). Writes
results/sonnet-ablation.{md,json} and results/sonnet-ablation-fit.json."""

import json
import os
from multiprocessing import Pool

import numpy as np

import v2_fit as vf
from entangled_mind import config, llm, v2

FIT = config.RESULTS / "sonnet-ablation-fit.json"
OUT_JSON, OUT_MD = config.RESULTS / "sonnet-ablation.json", config.RESULTS / "sonnet-ablation.md"
POOL4 = config.RESULTS / "pool-run-4.json"


def blocked(*_, **__):
    raise RuntimeError("sonnet_ablation: API calls are blocked")


def main() -> None:
    llm.client = blocked
    fitd = json.loads(vf.FIT.read_text())
    split = json.loads(vf.SPLIT.read_text())
    recs5 = {r["id"]: r for r in json.loads(vf.POOL5.read_text())["records"]}
    if FIT.exists():
        f2p = json.loads(FIT.read_text())
    else:
        tr, va = vf.load_items(split["train"], recs5), vf.load_items(split["validation"], recs5)
        with Pool(min(8, os.cpu_count()), initializer=vf._init, initargs=(tr,)) as ptr, \
                Pool(min(4, os.cpu_count()), initializer=vf._init, initargs=(va,)) as pva:
            f2p = v2.fit_model("F2P", vf.ParallelScorer("F2P", tr, ptr), vf.ParallelScorer("F2P", va, pva), seed=707,
                               log=lambda s: print(s, flush=True))
        FIT.write_text(json.dumps(f2p, indent=1))
    a2 = np.array(fitd["models"]["A2"]["final"]["params"])
    a2k0 = a2.copy()
    a2k0[1] = a2k0[2] = 0.0
    models = {"A2": ("A2", a2), "A2k0": ("A2", a2k0), "F2": ("F2", np.array(fitd["models"]["F2"]["final"]["params"])),
              "F2P": ("F2P", np.array(f2p["final"]["params"]))}
    recs4 = [r for r in json.loads(POOL4.read_text())["records"] if r["correct"] is not None]
    sets = {"Haiku locked v2 test (209)": vf.load_items(split["test"], recs5),
            "Sonnet hard pool (298)": vf.load_items([r["id"] for r in recs4], {r["id"]: r for r in recs4})}
    results = {}
    for name, items in sets.items():
        y = np.array([i.wrong for i in items])
        scores = {}
        with Pool(min(8, os.cpu_count()), initializer=vf._init, initargs=(items,)) as pool:
            for k, (model, v) in models.items():
                scores[k] = vf.ParallelScorer(model, items, pool).scores(v)
        res = {"n": len(items), "n_wrong": int(y.sum()), "auroc": {}}
        for k, sc in scores.items():
            p, lo, hi = vf.boot(list(sc[y]), list(sc[~y]))
            res["auroc"][k] = [p, lo, hi]
        for a, b in (("A2k0", "A2"), ("F2P", "A2"), ("F2P", "F2"), ("A2", "F2")):
            res[f"{a}_minus_{b}"] = vf.paired_diff(scores[a], scores[b], y)
        results[name] = res
    contains0 = lambda d: d[1] <= 0 <= d[2]
    below = lambda d: d[2] < 0
    k0_matches = all(contains0(r["A2k0_minus_A2"]) for r in results.values())
    k0_short = any(below(r["A2k0_minus_A2"]) for r in results.values())
    f2p_matches = all(contains0(r["F2P_minus_A2"]) for r in results.values())
    f2p_short = any(below(r["F2P_minus_A2"]) for r in results.values())
    if k0_short:
        verdict = "3: A2(κ=0) does not match A2 — the small couplings matter"
    elif k0_matches and f2p_matches:
        verdict = "1: the edge is single-claim geometry, and a classical model (F2+) carries it"
    elif k0_matches and f2p_short:
        verdict = "2: the single-claim geometry is the finding — F2+ falls short of A2; the next test is designed around it"
    else:
        verdict = "4: none of the pre-registered combinations — reported as is"
    counts = {"A2": 9, "A2(κ=0)": "9 (2 pinned at 0, 7 effective)", "F2": 9, "F2+": 10}
    OUT_JSON.write_text(json.dumps({"f2p_fit": f2p, "results": results, "verdict": verdict, "parameter_counts": counts}, indent=1))
    f = lambda d: f"{d[0]:.2f} [{d[1]:.2f}, {d[2]:.2f}]"
    g = lambda d: f"{d[0]:+.3f} [{d[1]:+.3f}, {d[2]:+.3f}]"
    lines = ["# What is the Sonnet edge? Coupling ablation and F2+ (Addendum D)", "",
             "Pre-registration: `experiments/preregistration-v2.md`, Addendum D (D28), committed before any score here. "
             "No API calls were made. F2+ was fitted on the v2 train split only (selected on validation); every model is scored "
             "once per set.", "",
             f"F2+ fit: train AUROC {f2p['final']['train_auroc']:.3f}, validation {f2p['final']['val_auroc']:.3f}; "
             + ", ".join(f"{n}={x:.3g}" for n, x in zip(f2p["names"], f2p["final"]["params"])) + ".", "",
             "| model | parameters | " + " | ".join(results) + " |", "|---|---|" + "---|" * len(results)]
    for k, lab in (("A2", "A2 (frozen v2)"), ("A2k0", "A2(κ=0): couplings set to exactly 0"), ("F2", "F2 (frozen v2)"),
                   ("F2P", "F2+: F2 with A2's tilted-readout marginal")):
        pc = counts["A2(κ=0)" if k == "A2k0" else ("F2+" if k == "F2P" else k)]
        lines.append(f"| {lab} | {pc} | " + " | ".join(f(r["auroc"][k]) for r in results.values()) + " |")
    lines += ["", "Paired bootstrap AUROC differences (1,000 stratified resamples; Addendum D specified 2,000, and the rule outcomes are the same at 2,000):", "",
              "| difference | " + " | ".join(results) + " |", "|---|" + "---|" * len(results)]
    for key, lab in (("A2k0_minus_A2", "A2(κ=0) − A2"), ("F2P_minus_A2", "F2+ − A2"), ("F2P_minus_F2", "F2+ − F2"),
                     ("A2_minus_F2", "A2 − F2")):
        lines.append(f"| {lab} | " + " | ".join(g(r[key]) for r in results.values()) + " |")
    lines += ["", f"## Rule outcome: **{verdict}**"]
    OUT_MD.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()

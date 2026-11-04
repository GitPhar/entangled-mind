"""Addendum E: the frozen F2+ on Haiku's run-2 held-out set (80 items), beside the frozen A2, F2, A2.1, F2.1.

    python experiments/heldout_f2plus.py

No API calls (the client is blocked) and no refitting. Appends to results/sonnet-ablation.md and writes
results/heldout-f2plus.json."""

import json
import os
from multiprocessing import Pool

import numpy as np

import v2_fit as vf
from entangled_mind import config, llm


def blocked(*_, **__):
    raise RuntimeError("API calls are blocked")


def main() -> None:
    llm.client = blocked
    split = json.loads(vf.SPLIT.read_text())
    recs3 = {r["id"]: r for r in json.loads(vf.POOL3.read_text())["records"]}
    ids = split["run2_heldout"]["test_wrong"] + split["run2_heldout"]["test_right"]
    items = vf.load_items(ids, recs3)
    y = np.array([i.wrong for i in items])
    v2f = json.loads(vf.FIT.read_text())["models"]
    v21 = json.loads(vf.FIT21.read_text())["models"]
    f2p = json.loads((config.RESULTS / "sonnet-ablation-fit.json").read_text())
    models = {"A2": ("A2", v2f["A2"]["final"]["params"]), "F2": ("F2", v2f["F2"]["final"]["params"]),
              "A21": ("A21", v21["A21"]["final"]["params"]), "F21": ("F21", v21["F21"]["final"]["params"]),
              "F2P": ("F2P", f2p["final"]["params"])}
    scores = {}
    with Pool(min(8, os.cpu_count()), initializer=vf._init, initargs=(items,)) as pool:
        for k, (model, v) in models.items():
            scores[k] = vf.ParallelScorer(model, items, pool).scores(np.array(v))
    au = {k: vf.boot(list(s[y]), list(s[~y])) for k, s in scores.items()}
    diffs = {f"{a}_minus_{b}": vf.paired_diff(scores[a], scores[b], y)
             for a, b in (("F2P", "A2"), ("F2P", "A21"), ("F2P", "F2"), ("A2", "F2"), ("A21", "F21"))}
    contains0 = lambda d: d[1] <= 0 <= d[2]
    below = lambda d: d[2] < 0
    if contains0(diffs["F2P_minus_A2"]) and contains0(diffs["F2P_minus_A21"]):
        verdict = "1: the held-out edges are also single-claim readout geometry, carried by a classical model"
    elif below(diffs["F2P_minus_A2"]) or below(diffs["F2P_minus_A21"]):
        verdict = "2: a held-out edge is not explained by the readout geometry - an open, unexplained secondary difference"
    else:
        verdict = "3: reported as is"
    (config.RESULTS / "heldout-f2plus.json").write_text(json.dumps({"auroc": au, "diffs": diffs, "verdict": verdict}, indent=1))
    f = lambda d: f"{d[0]:.2f} [{d[1]:.2f}, {d[2]:.2f}]"
    g = lambda d: f"{d[0]:+.3f} [{d[1]:+.3f}, {d[2]:+.3f}]"
    names = {"A2": "A2 (frozen v2)", "F2": "F2 (frozen v2)", "A21": "A2.1 (frozen v2.1)", "F21": "F2.1 (frozen v2.1)",
             "F2P": "F2+ (frozen, Addendum D)"}
    lines = ["", "## Addendum E: the frozen F2+ on Haiku's run-2 held-out set (40 wrong, 40 right)", "",
             "Pre-registered in `experiments/preregistration-v2.md`, Addendum E (`52e80a0`), before this scoring. Frozen "
             "parameters only, no refitting and no API calls.", "",
             "| model | AUROC [95% CI] |", "|---|---|"]
    lines += [f"| {names[k]} | {f(au[k])} |" for k in ("A2", "A21", "F2", "F21", "F2P")]
    lines += ["", "| paired difference | value [95% CI] |", "|---|---|"]
    for k, lab in (("F2P_minus_A2", "F2+ − A2"), ("F2P_minus_A21", "F2+ − A2.1"), ("F2P_minus_F2", "F2+ − F2"),
                   ("A2_minus_F2", "A2 − F2 (v2 edge, for reference)"), ("A21_minus_F21", "A2.1 − F2.1 (v2.1 edge, for reference)")):
        lines.append(f"| {lab} | {g(diffs[k])} |")
    lines += ["", f"**Rule outcome (Addendum E): {verdict}.**"]
    p = config.RESULTS / "sonnet-ablation.md"
    p.write_text(p.read_text().rstrip("\n") + "\n" + "\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()

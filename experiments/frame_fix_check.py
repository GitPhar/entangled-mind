"""Exploratory frame check (DEVIATIONS.md, D15). Not pre-registered; run-2 data only.

    python experiments/frame_fix_check.py

1. Across all run-2 (hard-pool) items: confidence-weighted circular mean phase of the
   yes-leaning and no-leaning claims at the encode stage, before and after pin_frame.
2. On the run-2 test set (40 wrong + 40 right): exact noiseless conflict scores of arm A0
   (entangled) and arm C (no two-qubit terms), before and after the frame fix, with AUROC
   and 95% bootstrap intervals. The locked v2 test set is not touched.

Writes results/frame-fix-check.{json,md}."""

import json
import math

import numpy as np
from qiskit.quantum_info import Statevector

from entangled_mind import config, encoder, readout

POOL = config.RESULTS / "pool-run-3.json"
RUN2 = config.RESULTS / "stage2-run-2.json"


def cmean(ph, w):
    z = np.sum(w * np.exp(1j * ph))
    return math.degrees(np.angle(z))


def camp_stats(phi, web):
    c, l = web.confidence, web.lean
    y, n = l > 0.1, l < -0.1
    if not (y.any() and n.any()):
        return None
    my, mn = cmean(phi[y], c[y]), cmean(phi[n], c[n])
    return {"yes_off": abs(((my + 180) % 360) - 180), "no_off": abs((mn % 360) - 180),
            "sep": abs(((my - mn + 180) % 360) - 180)}


def exact_conflict(web, phi, entangle):
    qc = encoder.build_circuit(web, entangle=entangle, measure=False, phi=phi)
    qc.h(range(web.n))
    p = np.abs(Statevector(qc).data) ** 2
    w = np.abs(web.lean)
    w = w / w.sum() if w.sum() > 0 else np.full(web.n, 1 / web.n)
    bits = (np.arange(2 ** web.n)[:, None] >> np.arange(web.n)) & 1
    m = (1 - 2 * bits) @ w
    return float(2 * min(p[m >= config.STRONG_TAU].sum(), p[m <= -config.STRONG_TAU].sum()))


def boot(pos, neg, seed=99, n=1000):
    rng = np.random.default_rng(seed)
    v = [readout.auroc(list(rng.choice(pos, len(pos))), list(rng.choice(neg, len(neg)))) for _ in range(n)]
    return readout.auroc(pos, neg), *[float(x) for x in np.percentile(v, [2.5, 97.5])]


def main():
    pool = json.loads(POOL.read_text())
    recs = {r["id"]: r for r in pool["records"]}
    split = pool["split"]
    stats = {"before": [], "after": [], "anchored": [], "anchored_inf": []}
    for r in pool["records"]:
        if "contentions" not in r:
            continue
        web = encoder.build_web(r["contentions"], r["pairs"])
        phi = encoder.solve_phases(web)
        for tag, ph in (("before", phi), ("after", encoder.pin_frame(phi, web)),
                        ("anchored", encoder.solve_phases_anchored(web)),
                        ("anchored_inf", encoder.solve_phases_anchored(web, math.inf))):
            s = camp_stats(ph, web)
            if s:
                stats[tag].append(s)
    pct = lambda a: [round(float(np.percentile(a, p)), 1) for p in (10, 25, 50, 75, 90)]
    summary = {}
    for tag, rows in stats.items():
        yo, no_, sep = (np.array([x[k] for x in rows]) for k in ("yes_off", "no_off", "sep"))
        summary[tag] = {"n_items": len(rows), "yes_offset_pct": pct(yo), "no_offset_pct": pct(no_),
                        "separation_pct": pct(sep), "share_yes_off_gt30": float(np.mean(yo > 30)),
                        "share_sep_lt90": float(np.mean(sep < 90))}
    run2 = json.loads(RUN2.read_text())["items"]
    scores = {f"{a}_{t}": {} for a in ("A0", "C") for t in ("before", "after", "anchored", "anchored_inf")}
    for q in split["test_wrong"] + split["test_right"]:
        web = encoder.build_web(recs[q]["contentions"], recs[q]["pairs"])
        phi = encoder.solve_phases(web)
        variants = {"before": phi, "after": encoder.pin_frame(phi, web),
                    "anchored": encoder.solve_phases_anchored(web),
                    "anchored_inf": encoder.solve_phases_anchored(web, math.inf)}
        for t, ph in variants.items():
            scores[f"A0_{t}"][q] = exact_conflict(web, ph, True)
            scores[f"C_{t}"][q] = exact_conflict(web, ph, False)
    auc = {k: boot([v[q] for q in split["test_wrong"]], [v[q] for q in split["test_right"]]) for k, v in scores.items()}
    archived = {a: readout.auroc([run2[q]["arms"][a]["readout"]["conflict_score"] for q in split["test_wrong"]],
                                 [run2[q]["arms"][a]["readout"]["conflict_score"] for q in split["test_right"]])
                for a in ("A0", "C")}
    json.dump({"camp_stats": summary, "auroc": auc, "archived_auroc": archived, "scores": scores},
              open(config.RESULTS / "frame-fix-check.json", "w"), indent=1)
    b, a = summary["before"], summary["after"]
    labels = {"before": "before (as run)", "after": "rigid pin (pin_frame)", "anchored": "anchors × λ (the correction)",
              "anchored_inf": "anchors → ∞ (reference)"}
    lines = ["# Frame check (exploratory, run-2 data only)", "",
             "Not pre-registered. The locked v2 test set is not touched. See DEVIATIONS.md, D15.", "",
             f"## Camp phases at encode ({b['n_items']} run-2 items with both a yes-leaning and a no-leaning claim)", "",
             "Percentiles (10 / 25 / 50 / 75 / 90) of the confidence-weighted circular-mean phase of each camp.", "",
             "| | yes camp: distance from 0° | no camp: distance from 180° | yes–no separation (ideal 180°) | yes camp > 30° off | separation < 90° |",
             "|---|---|---|---|---|---|"]
    for key, s in summary.items():
        tag = labels[key]
        lines.append(f"| {tag} | {s['yes_offset_pct']} | {s['no_offset_pct']} | {s['separation_pct']} | "
                     f"{s['share_yes_off_gt30']:.0%} | {s['share_sep_lt90']:.0%} |")
    lines += ["", "A rigid rotation only fixes a frame that has *rotated*; it cannot change the separation, so camps the solver pulled together stay together. Scaling the lean anchors by λ = max(1, largest total coupling of any claim), in the phase solve only, is the correction (fixed before its AUROC was computed). The ∞ limit puts every leaning claim exactly on the axis and is shown for reference.", "",
              "## Run-2 test set (40 wrong + 40 right): exact noiseless conflict scores", "",
              "| arm | before (as run) | rigid pin | anchors × λ (the correction) | anchors → ∞ (reference) | archived run-2 (1,000 shots; C noisy) |",
              "|---|---|---|---|---|---|"]
    f = lambda x: f"{x[0]:.2f} [{x[1]:.2f}, {x[2]:.2f}]"
    for arm in ("A0", "C"):
        lines.append(f"| {arm} | {f(auc[arm + '_before'])} | {f(auc[arm + '_after'])} | {f(auc[arm + '_anchored'])} | "
                     f"{f(auc[arm + '_anchored_inf'])} | {archived[arm]:.2f} |")
    (config.RESULTS / "frame-fix-check.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()

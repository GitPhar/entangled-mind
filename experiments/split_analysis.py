"""Step 1 of v2: split analysis of Stage 2 run 2 (with arms F and G from run 2b).
Re-scores every arm separately by item type (simpleqa / science / claim) and by
whether the item's relation web had >= 3 contradictions. Thresholds are the
existing calibration thresholds; nothing is fitted.

    python experiments/split_analysis.py

Writes results/stage2-run-2-split.{md,json}."""

import json

import numpy as np

from entangled_mind import config, readout

RUN2 = config.RESULTS / "stage2-run-2.json"
RUN2B = config.RESULTS / "stage2-run-2b.json"
POOL = config.RESULTS / "pool-run-3.json"
ARMS = ("A", "C", "D", "E", "F", "G", "A0")
N_BOOT = 1000


def kind(cat: str) -> str:
    return "science" if cat.startswith("science") else cat


def boot(pos, neg, seed=99):
    if not pos or not neg:
        return None, None, None
    rng = np.random.default_rng(seed)
    v = [readout.auroc(list(rng.choice(pos, len(pos))), list(rng.choice(neg, len(neg)))) for _ in range(N_BOOT)]
    lo, hi = np.percentile(v, [2.5, 97.5])
    return readout.auroc(pos, neg), float(lo), float(hi)


def main() -> None:
    r2, r2b = json.loads(RUN2.read_text()), json.loads(RUN2B.read_text())
    recs = {r["id"]: r for r in json.loads(POOL.read_text())["records"]}
    split = r2["split"]
    thr = r2b["thresholds"]
    wrong, right = set(split["test_wrong"]), set(split["test_right"])
    test = sorted(wrong | right)

    def score(q, a):
        if a in ("F", "G"):
            return r2b["arm_F_G"][q][a]["conflict_score"]
        return r2["items"][q]["arms"][a]["readout"]["conflict_score"]

    groups = {f"type: {t}": [q for q in test if kind(recs[q]["category"]) == t] for t in ("simpleqa", "science", "claim")}
    n_contra = {q: sum(p["relation"] == "contradicts" for p in recs[q]["pairs"]) for q in test}
    groups["contradictions >= 3"] = [q for q in test if n_contra[q] >= 3]
    groups["contradictions < 3"] = [q for q in test if n_contra[q] < 3]
    out = {}
    lines = ["# Stage 2 run 2: split analysis", "",
             "Every arm re-scored on the run-2 test set (40 wrong + 40 right), split by item type and by whether the "
             "item's relation web had ≥ 3 contradictions. Thresholds are each arm's existing calibration thresholds; "
             "**nothing is fitted**. Arms F and G come from run 2b. Each cell: wrong flagged · right flagged · "
             "AUROC [95% bootstrap CI]. Small groups give wide intervals; read them as descriptive.", ""]
    for g, ids in groups.items():
        w = [q for q in ids if q in wrong]
        r = [q for q in ids if q in right]
        lines += [f"## {g} ({len(w)} wrong, {len(r)} right)", "",
                  "| arm | wrong flagged | right flagged | AUROC [95% CI] |", "|---|---|---|---|"]
        out[g] = {"n_wrong": len(w), "n_right": len(r), "arms": {}}
        for a in ARMS:
            t = thr[a]
            fw, fr = sum(score(q, a) > t for q in w), sum(score(q, a) > t for q in r)
            p, lo, hi = boot([score(q, a) for q in w], [score(q, a) for q in r])
            out[g]["arms"][a] = {"wrong_flagged": fw, "right_flagged": fr, "auroc": p, "ci95": [lo, hi]}
            au = "undefined (no wrong or no right items)" if p is None else f"{p:.2f} [{lo:.2f}, {hi:.2f}]"
            lines.append(f"| {a} | {fw}/{len(w)} | {fr}/{len(r)} | {au} |")
        lines.append("")
    (config.RESULTS / "stage2-run-2-split.json").write_text(json.dumps(out, indent=1))
    (config.RESULTS / "stage2-run-2-split.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()

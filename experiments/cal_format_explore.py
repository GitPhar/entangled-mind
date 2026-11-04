"""EXPLORATORY follow-up to the calibration demonstration (DM6a), written after the pre-registered analysis had been seen.
No API calls. It does not replace the pre-registered reading in results/calibration-under-format.md.

Two problems found after the run:
1. About 120 of the 300 hard-pool questions are phrased "Is this claim true?"; the models answer "Guess: True/False",
   which the frozen parse rule (yes/no only) left unparsed.
2. On "Is the answer X?" questions, Tian et al.'s "the probability that it is correct" is often read as the probability that
   X is correct, not that the guess is (e.g. "Guess: No, not 1968 / Probability: 0.1").

This script (a) maps True/False to yes/no, and (b) reports, per cell, how often a "no" guess carries a stated confidence below
0.5, a sign of the second reading. It then scores every cell two ways:
- A, Tian's intended reading: confidence in the guess = the stated number;
- B, the proposed-answer reading: confidence in the guess = p if the guess is yes, else 1 - p.
The pre-registered contrasts and block bootstrap are re-run under both scorings.

    python experiments/cal_format_explore.py      # writes results/calibration-under-format-exploratory.json
"""

import json
import re

import numpy as np

import cal_format as cf
from entangled_mind import config

OUT = config.RESULTS / "calibration-under-format-exploratory.json"


def guess_of(raw):
    g = re.search(r"Guess:\s*\**\s*([A-Za-z]+)", raw or "")
    w = g.group(1).lower() if g else None
    return {"yes": "yes", "no": "no", "true": "yes", "false": "no"}.get(w)


def records(cache, P, scoring):
    out = {c: {} for c in cf.CELLS}
    for k, c in cache.items():
        kind, f, o = k.split("|")[:3]
        for pos, t in enumerate(c["turns"]):
            g = guess_of(t["raw"])
            _, conf = cf.parse(t["raw"], f)
            if g is None or conf is None:
                continue
            if scoring == "B":
                conf = conf if g == "yes" else 1 - conf
            out[(kind, f, o)][t["q"]] = (conf, g == P[t["q"]]["gold"], pos)
    return out


def referent(cache):
    """Per cell: share of parsed 'no' guesses whose stated number is below 0.5, and n of 'no' guesses."""
    out = {}
    for c in cf.CELLS:
        lo, n = 0, 0
        for k, v in cache.items():
            if tuple(k.split("|")[:3]) != c:
                continue
            for t in v["turns"]:
                g = guess_of(t["raw"])
                _, conf = cf.parse(t["raw"], c[1])
                if g == "no" and conf is not None:
                    n += 1
                    lo += conf < 0.5
        out["|".join(c)] = [lo / n if n else float("nan"), n]
    return out


def main():
    P, B = cf.pool(), cf.blocks()
    res = {}
    for m in cf.MODELS:
        cache = json.loads(cf.path(m).read_text())
        res[m] = {"referent_no_guess_below_half": referent(cache)}
        for scoring in ("A", "B"):
            R = records(cache, P, scoring)
            allq = [q for b in B for q in b]
            point = cf.contrasts(R, allq)
            rng = np.random.default_rng(cf.BOOT_SEED)
            boots = {k: [] for k in point}
            for _ in range(cf.NBOOT):
                qs = [q for bi in rng.integers(0, len(B), len(B)) for q in B[bi]]
                for k, v in cf.contrasts(R, qs).items():
                    boots[k].append(v)
            ci = {k: [float(point[k]), *map(float, np.nanpercentile(boots[k], [2.5, 97.5]))] for k in point}
            res[m][scoring] = {"cells": {"|".join(c): cf.stats(R[c], allq) for c in cf.CELLS}, "contrasts": ci}
    OUT.write_text(json.dumps(res, indent=1, default=float))
    for m, r in res.items():
        print(f"== {m}: share of 'no' guesses with stated number < 0.5:",
              {k: f"{v[0]:.0%} (n={v[1]})" for k, v in r["referent_no_guess_below_half"].items()})
        for s in ("A", "B"):
            c = r[s]["contrasts"]
            print(f"  scoring {s}: n per cell", {k: v["n"] for k, v in r[s]["cells"].items()})
            print(f"    ECE", {k: round(v["ece"], 3) for k, v in r[s]["cells"].items()})
            print("    format %+.3f [%+.3f, %+.3f]; order %+.3f [%+.3f, %+.3f]; replicate %+.3f [%+.3f, %+.3f]; conv-fresh %+.3f [%+.3f, %+.3f]" % (
                *c["format"], *c["order"], *c["replicate"], *c["sequential_minus_fresh"]))


if __name__ == "__main__":
    main()

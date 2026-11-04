"""Gold-map direction 4: build the frozen menus and the per-claim scores (D39). No API calls.

    python experiments/gm4_menus.py      # writes experiments/gm4-menus.json (once; never re-made)

Each item gets 3 menus of 4 leaning claims (|lean| > 0.1): menu 1 = the 4 chain claims; menus 2-3 are
random 4-subsets with at least one claim of each lean sign (random.Random(4004)), distinct from the
other menus where the item allows. Scores per claim:
  EIG under D5 and BA5 (frozen experiment-5 fits): H(p0) - [c H(p|true) + (1 - c) H(p|false)], where p is
  the model's predicted main-question probability (inverse link of the predicted rating) after verifying
  the claim true (rating 100) or false (rating 0), and c is the claim's extracted confidence;
  expected |dM| under each; confirmatory = confidence x |lean| among claims leaning toward the model's
  answer (others -inf); most-uncertain = -|confidence - 0.5|."""

import itertools
import json
import math
import random
import sys

import numpy as np

import exp5_models as m
import exp5_run as er
from entangled_mind import config

OUT = config.EXPERIMENTS / "gm4-menus.json"


def H(p):
    p = min(max(p, 1e-9), 1 - 1e-9)
    return -(p * math.log2(p) + (1 - p) * math.log2(1 - p))


def predicted_p(model, it, turns, v, extra):
    out = m.predict(model, it, turns, v, extra)
    r = [x for x in out if x[2] == "M"][-1][0]
    return m.p_obs(r, v[3], v[4])


def scores(rec, it, k, fits, extra):
    c = rec["contentions"][k]["confidence"]
    res = {}
    for model in ("D5", "BA5"):
        v = fits[model]["final"]["params"]
        base = [{"kind": "M", "claim": None, "rating": 50}]
        p0 = predicted_p(model, it, base, v, extra)
        pt = predicted_p(model, it, [{"kind": "S", "claim": k, "rating": 100}] + base, v, extra)
        pf = predicted_p(model, it, [{"kind": "S", "claim": k, "rating": 0}] + base, v, extra)
        res[f"EIG_{model}"] = H(p0) - (c * H(pt) + (1 - c) * H(pf))
        res[f"dM_{model}"] = 100 * (c * abs(pt - p0) + (1 - c) * abs(pf - p0))
    side = 1 if rec["model_answer"] == "yes" else -1
    lean = rec["contentions"][k]["lean"]
    res["confirmatory"] = c * abs(lean) if lean * side > 0.1 else -1.0
    res["most_uncertain"] = -abs(c - 0.5)
    return res


def main():
    if OUT.exists():
        sys.exit(f"{OUT} exists; menus are never re-made")
    split = json.loads(er.SPLIT.read_text())
    recs = {r["id"]: r for r in json.loads(er.POOL.read_text())["records"]}
    fits = json.loads((config.RESULTS / "exp5-fit.json").read_text())
    rng = random.Random(4004)
    out = {"items": {}}
    for q in split["candidates"]:
        rec = recs[q]
        it = m.item_data(rec)
        extra = (100 * m.a5_expect_M(m.a5_prep(it, m.KAPPA0), it), 1 if rec["model_answer"] == "yes" else -1)
        L = [c["lean"] for c in rec["contentions"]]
        leaning = [k for k in range(len(L)) if abs(L[k]) > 0.1]
        chain = sorted(split["chain_claims"][q])
        menus = [chain]
        cands = [sorted(s) for s in itertools.combinations(leaning, 4)
                 if any(L[k] > 0.1 for k in s) and any(L[k] < -0.1 for k in s)]
        rng.shuffle(cands)
        for s in cands:
            if len(menus) == 3:
                break
            if s not in menus:
                menus.append(s)
        while len(menus) < 3:                       # too few distinct subsets: repeat (option order still rotates)
            menus.append(menus[len(menus) % max(1, len(menus))])
        claims = sorted({k for mn in menus for k in mn})
        out["items"][q] = {"menus": menus, "model_answer": rec["model_answer"],
                           "scores": {str(k): scores(rec, it, k, fits, extra) for k in claims}}
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()

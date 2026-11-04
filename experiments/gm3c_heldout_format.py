"""Direction 3 follow-up: predict each of the six formats from the other five, as pre-registered in
experiments/gm3c-heldout-format.md (D46). Archived data only; no API calls.

    python experiments/gm3c_heldout_format.py

Writes results/gm3c-heldout-format.{json,md}."""

import json
import math
import random

import numpy as np
from scipy.special import expit
from scipy.stats import spearmanr

import gm3b_format_invariance as g
from entangled_mind import config
from gm_common import PLAIN

OUT_JSON, OUT_MD = config.RESULTS / "gm3c-heldout-format.json", config.RESULTS / "gm3c-heldout-format.md"
FOLD_SEED, BOOT_SEED = 4646, 4647
GH_X, GH_W = np.polynomial.hermite_e.hermegauss(20)          # probabilists' Hermite: weight exp(-x^2/2)
GH_W = GH_W / GH_W.sum()


def predicted_obs(f, p, mu, d):
    """Expected response per observation on the observed scale."""
    eta = p["a"] + p["b"] * mu
    if f in ("F1", "F5"):
        y = eta[:, None] + p["s"] * GH_X[None, :]
        return (102 * expit(y) - 1) @ GH_W
    if f == "F2":
        return expit(eta)
    if f == "F3":
        return expit(p["a"] + p["b"] * (mu - d["x"]))
    if f == "F4":
        return expit(eta + p["d"] * d["x"])
    k = np.concatenate([[-np.inf], p["k"], [np.inf]])
    probs = np.stack([expit(k[j + 1] - eta) - expit(k[j] - eta) for j in range(7)], axis=1)
    return probs @ np.arange(7)


def observed_scale(f, d):
    if f in ("F1", "F5"):
        return 102 * expit(d["y"]) - 1          # undo the logit((r + 1)/102) encoding
    return d["y"]


def claim_means(vals, c, nc):
    s, n = np.zeros(nc), np.zeros(nc)
    np.add.at(s, c, vals)
    np.add.at(n, c, 1)
    return np.where(n > 0, s / np.maximum(n, 1), np.nan)


def main():
    conv = json.loads(g.CACHE.read_text())
    obs, nc = g.encode(conv)
    cl = g.claims()
    items = sorted({q for q, _ in cl})
    order = items[:]
    random.Random(FOLD_SEED).shuffle(order)
    fold_of_item = {q: i // 8 for i, q in enumerate(order)}
    fold = np.array([fold_of_item[q] for q, _ in cl])
    pred = {f: np.full(nc, np.nan) for f in g.FORMATS}
    for fi, f in enumerate(g.FORMATS):
        for k in range(5):
            test = fold == k
            mod = {}
            for ff, d in obs.items():
                keep = ~test[d["c"]] if ff == f else np.ones(len(d["c"]), bool)
                mod[ff] = g.subset(d, keep)
            theta, mu = g.fit(mod, nc, True, lambda d: d["r"] % 2 == 0)
            p = g.unpack(theta, True)[f]
            d = g.subset(obs[f], test[obs[f]["c"]] & (obs[f]["r"] % 2 == 1))
            pm = claim_means(predicted_obs(f, p, mu[d["c"]], d), d["c"], nc)
            pred[f][test] = pm[test]
    res = {"formats": {}}
    target, ceil = {}, {}
    for f in g.FORMATS:
        d = obs[f]
        odd, even = d["r"] % 2 == 1, d["r"] % 2 == 0
        target[f] = claim_means(observed_scale(f, d)[odd], d["c"][odd], nc)
        ceil[f] = claim_means(observed_scale(f, d)[even], d["c"][even], nc)

    def stats(idx):
        out = {}
        for f in g.FORMATS:
            ok = idx[~np.isnan(pred[f][idx]) & ~np.isnan(target[f][idx]) & ~np.isnan(ceil[f][idx])]
            rc = np.corrcoef(pred[f][ok], target[f][ok])[0, 1] ** 2
            rl = np.corrcoef(ceil[f][ok], target[f][ok])[0, 1] ** 2
            out[f] = (rc, rl, rc / rl if rl > 0 else np.nan)
        return out
    allidx = np.arange(nc)
    point = stats(allidx)
    by_item = {q: [i for i, (qq, _) in enumerate(cl) if qq == q] for q in items}
    rng = np.random.default_rng(BOOT_SEED)
    bq, bc = [], []
    for _ in range(2000):
        idx = np.array([i for q in rng.choice(items, len(items)) for i in by_item[q]])
        s = stats(idx)
        bq.append(np.nanmean([v[2] for v in s.values()]))
        bc.append(np.nanmean([v[0] for v in s.values()]))
    q_lo, q_hi = np.percentile(bq, [2.5, 97.5])
    c_lo, c_hi = np.percentile(bc, [2.5, 97.5])
    for f in g.FORMATS:
        ok = ~np.isnan(pred[f]) & ~np.isnan(target[f])
        res["formats"][f] = {"R2_cross": float(point[f][0]), "R2_ceiling": float(point[f][1]), "Q": float(point[f][2]),
                             "spearman_cross": float(spearmanr(pred[f][ok], target[f][ok]).statistic),
                             "spearman_ceiling": float(spearmanr(ceil[f][ok], target[f][ok]).statistic)}
    mq = float(np.nanmean([v[2] for v in point.values()]))
    mc = float(np.nanmean([v[0] for v in point.values()]))
    if q_lo > 0.75:
        reading = "a usable single belief (one credence recovers most of each format's reproducible answer)"
    elif q_hi < 0.5:
        reading = "little format-free belief (most of each format's reproducible answer is not recoverable from the others)"
    else:
        reading = "partial"
    res.update(mean_Q=mq, mean_Q_ci95=[float(q_lo), float(q_hi)], mean_R2_cross=mc, mean_R2_cross_ci95=[float(c_lo), float(c_hi)],
               reading=reading, folds={q: int(v) for q, v in fold_of_item.items()})
    OUT_JSON.write_text(json.dumps(res, indent=1))
    lines = ["# Direction 3 follow-up: predicting each format from the other five", "",
             "Pre-registered in `experiments/gm3c-heldout-format.md` (D46), committed before the fit. Last night's six-format data "
             "(`results/gm3b-calls.json`); the one-credence model L1 fitted on even repeats with the held-out format removed for the "
             "test fold's claims (5 item folds); targets are odd repeats. No API calls; $0.", "", PLAIN,
             "## Cross-format prediction against each format's own split-half ceiling", "",
             "| held-out format | R² from the other five | R² ceiling (own even repeats) | Q = ratio | Spearman, cross / ceiling |",
             "|---|---|---|---|---|"]
    for f, v in res["formats"].items():
        lines.append(f"| {g.NAMES[f]} | {v['R2_cross']:.2f} | {v['R2_ceiling']:.2f} | {v['Q']:.2f} | "
                     f"{v['spearman_cross']:+.2f} / {v['spearman_ceiling']:+.2f} |")
    lines += ["", f"- **Mean Q = {mq:.2f} [{q_lo:.2f}, {q_hi:.2f}]** (item-cluster bootstrap).",
              f"- Mean absolute R² from the other five formats: {mc:.2f} [{c_lo:.2f}, {c_hi:.2f}] (Smolin & Wilder: 0.60–0.90 on other models).",
              "", f"## Pre-registered reading: **{reading}**"]
    OUT_MD.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()

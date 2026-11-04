"""Biomimetic map, the three $0 archived-data analyses, as pre-registered in
experiments/bm3-confirmation.md (D40), bm7-serial-position.md (D41) and bm9-contrast.md (D42).
No API calls.

    python experiments/bm_offline.py bm3|bm7|bm9

Writes results/bm3-confirmation.{json,md}, results/bm7-serial-position.{json,md}, results/bm9-contrast.{json,md}."""

import json
import sys

import numpy as np

import exp5_run as er
from entangled_mind import config
from gm_common import PLAIN

R3 = config.RESULTS / "exp4-run-3-calls.json"
CONV1, CONV2 = config.RESULTS / "exp5-conversations.json", config.RESULTS / "exp5-run-2-conversations.json"


def ols(X, y):
    return np.linalg.lstsq(X, y, rcond=None)[0]


def cluster_boot(clusters, fn, seed, n=2000):
    rng = np.random.default_rng(seed)
    keys = sorted(clusters)
    vals = [fn([clusters[k] for k in rng.choice(keys, len(keys))]) for _ in range(n)]
    return np.percentile(np.array(vals), [2.5, 97.5], axis=0)


def ci(point, lohi, i=None, p=3):
    lo, hi = (lohi[0], lohi[1]) if i is None else (lohi[0][i], lohi[1][i])
    pt = point if i is None else point[i]
    return f"{pt:+.{p}f} [{lo:+.{p}f}, {hi:+.{p}f}]"


# --- bm3: confidence-gated confirmation --------------------------------------------

def bm3():
    calls = json.loads(R3.read_text())
    items = [it["id"] for it in json.loads((config.EXPERIMENTS / "exp4-items.json").read_text())]
    rows, dropped = {}, {"small_displacement": 0, "own_near_half": 0}
    for q in items:
        for o in ("X", "Y"):
            own = float(np.mean([v["r1"] for k, v in calls.items() if k.startswith(f"{q}|{o}->XY|")]))
            if abs(own - 0.5) < 0.02:
                dropped["own_near_half"] += sum(1 for k in calls if k.startswith((f"{q}|{o}-lo|", f"{q}|{o}-hi|")))
                continue
            lst = []
            for lvl in ("lo", "hi"):
                for k, v in calls.items():
                    if not k.startswith(f"{q}|{o}-{lvl}|"):
                        continue
                    A, r1 = v["A"], v["r1"]
                    if abs(A - own) < 0.05:
                        dropped["small_displacement"] += 1
                        continue
                    u = float(np.clip((r1 - own) / (A - own), -2, 3))
                    cons = float(np.sign(A - 0.5) == np.sign(own - 0.5))            # primary: sign relative to 50 (rev. 2)
                    conf = float(cons and abs(A - 0.5) > abs(own - 0.5))           # secondary: rev. 1 extremity coding
                    lst.append([u, cons, abs(own - 0.5), cons * abs(own - 0.5), abs(A - own),
                                float(v.get("decision") == "accept"), conf, conf * abs(own - 0.5)])
            if lst:
                rows[f"{q}|{o}"] = np.array(lst)

    def fit(groups, col=0, code=1):
        d = np.concatenate(groups)
        c, cx = (d[:, 1], d[:, 3]) if code == 1 else (d[:, 6], d[:, 7])
        X = np.column_stack([np.ones(len(d)), c, d[:, 2], cx, d[:, 4]])
        return ols(X, d[:, col])
    allr = np.concatenate(list(rows.values()))
    b = fit(list(rows.values()))
    b_ci = cluster_boot(rows, fit, 5050)
    ba = fit(list(rows.values()), 5)
    ba_ci = cluster_boot(rows, lambda g: fit(g, 5), 5051)
    b2 = fit(list(rows.values()), 0, 2)
    b2_ci = cluster_boot(rows, lambda g: fit(g, 0, 2), 5052)
    opposite = sum(1 for g in rows.values() if 0 < g[:, 1].mean() < 1)
    by = {c: {"n": int((allr[:, 1] == c).sum()), "mean_uptake": float(allr[allr[:, 1] == c, 0].mean()) if (allr[:, 1] == c).any() else float("nan"),
              "accept_rate": float(allr[allr[:, 1] == c, 5].mean()) if (allr[:, 1] == c).any() else float("nan")} for c in (0, 1)}
    if b_ci[0][1] > 0 and b_ci[0][3] > 0:
        reading = "confidence-gated asymmetry (consistent with confirmation; not unique to it)"
    elif b_ci[0][1] > 0:
        reading = "asymmetry without gating"
    else:
        reading = "no asymmetry" + (" (consistent estimates taken up LESS: CI of beta1 below 0)" if b_ci[1][1] < 0 else "")
    out = {"beta": b.tolist(), "beta_ci95": b_ci.tolist(), "beta_accept": ba.tolist(), "beta_accept_ci95": ba_ci.tolist(),
           "beta_rev1_coding": b2.tolist(), "beta_rev1_coding_ci95": b2_ci.tolist(), "item_orders_with_anchors_on_both_sides": opposite,
           "by_code": by, "n_conversations": int(len(allr)), "n_item_orders": len(rows), "dropped": dropped, "reading": reading}
    (config.RESULTS / "bm3-confirmation.json").write_text(json.dumps(out, indent=1))
    names = ["intercept β₀", "consistent β₁", "extremity β₂", "consistent × extremity β₃", "|A − own| β₄"]
    lines = ["# Biomimetic (rev. 2 §3.1): confidence-gated confirmation on the archived run-3 calls", "",
             "Pre-registered in `experiments/bm3-confirmation.md` (D40), committed before the archive was opened for this analysis. "
             f"{out['n_conversations']} anchored conversations in {out['n_item_orders']} item-orders (dropped: "
             f"{dropped['small_displacement']} with |A − own| < 0.05, {dropped['own_near_half']} with own within 0.02 of 0.5). $0.", "", PLAIN,
             "## Regression of uptake u = (r₁ − own)/(A − own)", "",
             f"Primary code: consistent = the anchor lies on the same side of 50 as the model's own mean (revision 2). Item-orders whose two "
             f"anchors fall on opposite sides of 50, which alone identify β₁: **{opposite} of {len(rows)}**. Secondary: revision 1's "
             "confirmatory code (same side and more extreme).", "",
             "| term | uptake, primary code [95% cluster-bootstrap CI] | accept (0/1), primary [CI] | uptake, revision-1 code [CI] |",
             "|---|---|---|---|"]
    for i, n in enumerate(names):
        lines.append(f"| {n} | {ci(b, b_ci, i)} | {ci(ba, ba_ci, i)} | {ci(b2, b2_ci, i)} |")
    lines += ["", "| anchor (primary code) | conversations | mean uptake | accept rate |", "|---|---|---|---|"]
    for c, lab in ((1, "consistent (same side of 50)"), (0, "inconsistent (other side)")):
        lines.append(f"| {lab} | {by[c]['n']} | {by[c]['mean_uptake']:+.3f} | {by[c]['accept_rate']:.1%} |")
    lines += ["", f"## Pre-registered reading: **{reading}**"]
    (config.RESULTS / "bm3-confirmation.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


# --- bm7: serial-position weights ----------------------------------------------------

def bm7():
    split = json.loads(er.SPLIT.read_text())
    recs = {r["id"]: r for r in json.loads(er.POOL.read_text())["records"]}
    conv = json.loads(CONV1.read_text())
    groups = {}
    for q in split["candidates"]:
        lean = [c["lean"] for c in recs[q]["contentions"]]
        lst = []
        for ch in ("O1", "O2", "O3", "O4"):
            for r in range(er.R_CHAIN):
                c = conv.get(f"{q}|{ch}|{r}")
                if not c or c["anchor"] != "a" or any(t["kind"] == "error" for t in c["turns"]):
                    continue
                s = [t for t in c["turns"] if t["kind"] == "S"]
                m = c["turns"][-1]
                if len(s) != 4 or m["kind"] != "M":
                    continue
                lst.append([m["rating"]] + [np.sign(lean[t["claim"]]) * (t["rating"] - 50) / 50 for t in s])
        if lst:
            groups[q] = np.array(lst, float)

    def fit(gs):
        # item fixed effects by within-item demeaning (resampled duplicates are treated as separate items)
        ys, Xs = [], []
        for g in gs:
            ys.append(g[:, 0] - g[:, 0].mean())
            Xs.append(g[:, 1:] - g[:, 1:].mean(axis=0))
        w = ols(np.vstack(Xs), np.concatenate(ys))
        trend = np.polyfit([1, 2, 3, 4], w, 1)[0]
        mid = (w[1] + w[2]) / 2
        return np.concatenate([w, [w[0] - w[3], trend, w[0] - mid, w[3] - mid]])
    est = fit(list(groups.values()))
    lohi = cluster_boot(groups, fit, 5151)
    rho = json.loads((config.RESULTS / "exp5-fit.json").read_text())["BA5"]["final"]["params"][2]
    ba5 = [rho ** (4 - p) for p in (1, 2, 3, 4)]
    if lohi[0][6] > 0 and lohi[0][7] > 0:
        reading = "U-shape: falsifies the LCA"
    else:
        shape = "primacy" if lohi[0][4] > 0 else ("recency" if lohi[1][4] < 0 else "flat")
        reading = f"monotone or flat ({shape}): consistent with the LCA"
    out = {"weights": est[:4].tolist(), "w1_minus_w4": float(est[4]), "trend": float(est[5]), "u1": float(est[6]), "u4": float(est[7]),
           "ci95": lohi.tolist(),
           "BA5_implied_relative_weights": ba5, "n_conversations": int(sum(len(g) for g in groups.values())),
           "n_items": len(groups), "reading": reading}
    (config.RESULTS / "bm7-serial-position.json").write_text(json.dumps(out, indent=1))
    lines = ["# Biomimetic (rev. 2 §3.5): serial-position weights from the archived O1–O4 chains", "",
             "Pre-registered in `experiments/bm7-serial-position.md` (D41), committed before the archive was opened for this analysis. "
             f"Anchor (a) only; {out['n_conversations']} conversations, {out['n_items']} items; item fixed effects; $0.", "", PLAIN,
             "## Weight of each position on the final main rating", "",
             "Evidence x = sign(lean) · (rating − 50)/50; weights in rating points per unit of evidence; 95% item-cluster bootstrap CIs.", "",
             "| position | weight | BA5-implied weight (relative to position 4) |", "|---|---|---|"]
    for p in range(4):
        lines.append(f"| {p + 1} | {ci(est, lohi, p, 1)} | {ba5[p]:.2f} |")
    lines += ["", f"- **U-shape contrasts:** u₁ = w₁ − (w₂ + w₃)/2 = {ci(est, lohi, 6, 1)}; u₄ = w₄ − (w₂ + w₃)/2 = {ci(est, lohi, 7, 1)}.",
              f"- w₁ − w₄ = {ci(est, lohi, 4, 1)}; linear trend over positions {ci(est, lohi, 5, 2)} points per position.", "",
              f"## Pre-registered reading: **{reading}**"]
    (config.RESULTS / "bm7-serial-position.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


# --- bm9: contrast or assimilation ----------------------------------------------------

def bm9_pairs(conv, items, split, recs, r_qq, anchor_only):
    pairs = {}
    for q in items:
        for k in split["qq_pairs"][q]:
            rows = {}
            for o in ("SM", "MS"):
                lst = []
                for r in range(r_qq):
                    c = conv.get(f"{q}|QQ{k}{o}|{r}")
                    if not c or (anchor_only and c["anchor"] != "a") or any(t["kind"] == "error" for t in c["turns"]):
                        continue
                    s = next((t["rating"] for t in c["turns"] if t["kind"] == "S"), None)
                    m = next((t["rating"] for t in c["turns"] if t["kind"] == "M"), None)
                    if s is not None and m is not None:
                        lst.append((s, m))
                rows[o] = np.array(lst, float)
            if len(rows["SM"]) and len(rows["MS"]):
                sg = float(np.sign(recs[q]["contentions"][k]["lean"]))
                sm, ms = rows["SM"], rows["MS"]
                corr = (float(np.corrcoef(sm[:, 0], sm[:, 1])[0, 1]) * sg
                        if sm[:, 0].std() > 0 and sm[:, 1].std() > 0 else None)
                pairs.setdefault(q, []).append([sm[:, 1].mean() - ms[:, 1].mean(), sm[:, 0].mean() - ms[:, 1].mean(),
                                                sg * (sm[:, 0].mean() - 50) / 50, np.nan if corr is None else corr])
    return {q: np.array(v) for q, v in pairs.items()}


def bm9():
    split = json.loads(er.SPLIT.read_text())
    recs = {r["id"]: r for r in json.loads(er.POOL.read_text())["records"]}
    sets = {"run 1, anchor (a), 40 items": bm9_pairs(json.loads(CONV1.read_text()), split["candidates"], split, recs, er.R_QQ, True),
            "run 2, anchor (a), 10 items (replication)": bm9_pairs(json.loads(CONV2.read_text()), er.candidates()[:10], split, recs, 40, True)}

    def fit(gs):
        d = np.concatenate(gs)
        b = ols(np.column_stack([np.ones(len(d)), d[:, 1], d[:, 2]]), d[:, 0])
        c = d[:, 3][~np.isnan(d[:, 3])]
        return np.concatenate([b, [c.mean() if len(c) else np.nan]])
    out, lines = {}, ["# Biomimetic (rev. 1 §3.9): contrast or assimilation on the single-scale QQ conversations", "",
                      "Pre-registered in `experiments/bm9-contrast.md` (D42), committed before the archive was opened for this analysis. "
                      "Anchor (a) only; $0.", "", PLAIN,
                      "## d_M = α + β·L + γ·C across (item, claim) pairs", "",
                      "d_M: M after S minus M first; L: S level minus M-first level; C: yes-ward content push of the S rating. "
                      "Secondary: within-pair correlation of S and the following M, signed by the claim's lean (positive = M follows S "
                      "the way content implies). 95% item-cluster bootstrap CIs.", "",
                      "| set | pairs | β (level) | γ (content) | signed within-pair corr (pairs with variance) | reading |", "|---|---|---|---|---|---|"]
    for name, g in sets.items():
        est = fit(list(g.values()))
        lohi = cluster_boot(g, fit, 5252)
        reading = "contrast" if lohi[1][1] < 0 else ("assimilation" if lohi[0][1] > 0 else "no level effect")
        allp = np.concatenate(list(g.values()))
        nc = int((~np.isnan(allp[:, 3])).sum())
        out[name] = {"beta": est[:3].tolist(), "signed_corr": float(est[3]), "ci95": lohi.tolist(), "n_pairs": int(len(allp)),
                     "n_pairs_with_corr": nc, "reading": reading}
        lines.append(f"| {name} | {len(allp)} | {ci(est, lohi, 1)} | {ci(est, lohi, 2, 1)} | {ci(est, lohi, 3, 2)} ({nc}) | {reading} |")
    out["reading"] = out["run 1, anchor (a), 40 items"]["reading"]
    lines += ["", f"## Pre-registered reading (primary set): **{out['reading']}**"]
    (config.RESULTS / "bm9-contrast.json").write_text(json.dumps(out, indent=1))
    (config.RESULTS / "bm9-contrast.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    {"bm3": bm3, "bm7": bm7, "bm9": bm9}[sys.argv[1]]()

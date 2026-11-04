"""Gold-map direction 9: NSIT (no-signalling in time) on the archived experiment 5 conversations,
as pre-registered in experiments/gm9-nsit.md (D34). Anchor (a) only; no API calls.

    python experiments/gm9_nsit.py

Writes results/gm9-nsit.{json,md}."""

import json

import numpy as np

import exp5_run as er
from entangled_mind import config
from gm_common import PLAIN

CONV1 = config.RESULTS / "exp5-conversations.json"
CONV2 = config.RESULTS / "exp5-run-2-conversations.json"
OUT_JSON, OUT_MD = config.RESULTS / "gm9-nsit.json", config.RESULTS / "gm9-nsit.md"
N_PERM, PERM_SEED, BOOT_SEED = 5000, 9009, 9010
FAMILIES = {
    "N1M": "main question M after S_k (QQ: SM) vs M first (MS)",
    "N1S": "sub-question S_k after M (QQ: MS) vs S_k first (SM)",
    "N2": "final M with S_k asked (O1) vs omitted (X_k)",
    "N3": "final M after all four sub-questions (O1-O4) vs M alone (B0)",
    "N4": "final M after a midway yes/no choice (K1) vs a filler (K0)",
    "N5": "final M with M asked first (MF) vs not (O1)",
}


def ok(c):
    return c is not None and c["anchor"] == "a" and not any(t["kind"] == "error" for t in c["turns"])


def final_m(c):
    t = c["turns"][-1]
    return t["rating"] if t["kind"] == "M" else None


def qq_rating(c, kind):
    return next((t["rating"] for t in c["turns"] if t["kind"] == kind), None)


def chain_finals(conv, q, chain):
    out = []
    for r in range(er.R_CHAIN):
        c = conv.get(f"{q}|{chain}|{r}")
        if ok(c) and final_m(c) is not None:
            out.append(final_m(c))
    return out


def qq_cells(conv, items, split, r_qq):
    m_cells, s_cells = [], []
    for q in items:
        for k in split["qq_pairs"][q]:
            rows = {}
            for order in ("SM", "MS"):
                rows[order] = [c for c in (conv.get(f"{q}|QQ{k}{order}|{r}") for r in range(r_qq)) if ok(c)]
            m_cells.append((f"{q}:S{k}", [qq_rating(c, "M") for c in rows["SM"]], [qq_rating(c, "M") for c in rows["MS"]]))
            s_cells.append((f"{q}:S{k}", [qq_rating(c, "S") for c in rows["MS"]], [qq_rating(c, "S") for c in rows["SM"]]))
    return m_cells, s_cells


def build(conv1, items, split):
    fam = {}
    fam["N1M"], fam["N1S"] = qq_cells(conv1, items, split, er.R_QQ)
    fam["N2"] = [(f"{q}:X{k}", chain_finals(conv1, q, "O1"), chain_finals(conv1, q, f"X{k}")) for q in items for k in (1, 2, 3, 4)]
    fam["N3"] = [(q, sum((chain_finals(conv1, q, f"O{i}") for i in (1, 2, 3, 4)), []), chain_finals(conv1, q, "B0")) for q in items]
    fam["N4"] = [(q, chain_finals(conv1, q, "K1"), chain_finals(conv1, q, "K0")) for q in items]
    fam["N5"] = [(q, chain_finals(conv1, q, "MF"), chain_finals(conv1, q, "O1")) for q in items]
    return fam


def family_test(cells, rng):
    cells = [(name, np.array(a, float), np.array(b, float)) for name, a, b in cells if len(a) and len(b)]
    d = np.array([a.mean() - b.mean() for _, a, b in cells])
    dp = np.array([(a >= 50).mean() - (b >= 50).mean() for _, a, b in cells])
    T = float((d ** 2).sum())
    null_T, null_abs = [], []
    pooled = [(np.concatenate([a, b]), len(a)) for _, a, b in cells]
    for _ in range(N_PERM):
        dd = []
        for x, na in pooled:
            p = rng.permutation(x)
            dd.append(p[:na].mean() - p[na:].mean())
        dd = np.array(dd)
        null_T.append((dd ** 2).sum())
        null_abs.append(np.abs(dd).mean())
    p = (1 + sum(t >= T for t in null_T)) / (N_PERM + 1)
    items = sorted({n.split(":")[0] for n, _, _ in cells})
    by_item = {it: [d[i] for i, (n, _, _) in enumerate(cells) if n.split(":")[0] == it] for it in items}
    brng = np.random.default_rng(BOOT_SEED)
    boots = [np.mean(sum((by_item[it] for it in brng.choice(items, len(items))), [])) for _ in range(2000)]
    return {"n_cells": len(cells), "n_per_condition_median": [float(np.median([len(a) for _, a, _ in cells])),
                                                               float(np.median([len(b) for _, _, b in cells]))],
            "T": T, "p_perm": float(p), "mean_abs_d": float(np.abs(d).mean()), "null_mean_abs_d": float(np.mean(null_abs)),
            "share_abs_d_ge_10": float(np.mean(np.abs(d) >= 10)), "mean_d": float(d.mean()),
            "mean_d_ci95": [float(x) for x in np.percentile(boots, [2.5, 97.5])], "mean_abs_dP": float(np.abs(dp).mean()),
            "cells": [{"cell": n, "d": float(d[i]), "dP": float(dp[i]), "n": [len(a), len(b)]} for i, (n, a, b) in enumerate(cells)]}


def holm(ps):
    order = sorted(ps, key=ps.get)
    adj, run = {}, 0.0
    for i, k in enumerate(order):
        run = max(run, min(1.0, (len(order) - i) * ps[k]))
        adj[k] = run
    return adj


def main() -> None:
    split = json.loads(er.SPLIT.read_text())
    items = split["candidates"]
    conv1 = json.loads(CONV1.read_text())
    rng = np.random.default_rng(PERM_SEED)
    fam = build(conv1, items, split)
    res = {k: family_test(v, rng) for k, v in fam.items()}
    adj = holm({k: v["p_perm"] for k, v in res.items()})
    for k in res:
        res[k]["p_holm"] = adj[k]
        res[k]["invasive"] = adj[k] < 0.05
    conv2 = json.loads(CONV2.read_text())
    items2 = er.candidates()[:10]
    m2, s2 = qq_cells(conv2, items2, split, 40)
    rep = {"N1M": family_test(m2, rng), "N1S": family_test(s2, rng)}
    OUT_JSON.write_text(json.dumps({"families": res, "replication_run2": rep, "descriptions": FAMILIES}, indent=1))
    write_md(res, rep)


def write_md(res, rep) -> None:
    ci = lambda c: f"[{c[0]:+.1f}, {c[1]:+.1f}]"
    lines = ["# Direction 9: no-signalling in time (NSIT) on the archived experiment 5 conversations", "",
             "Pre-registered in `experiments/gm9-nsit.md` (D34), committed before this analysis. Anchor (a) conversations only "
             "(0 = certainly false, 100 = certainly true); 40 items; no API calls; $0.", "", PLAIN,
             "## Results", "",
             "d = mean later rating when the earlier question was asked minus when it was not (rating points). "
             "Permutation test of Σd² with labels shuffled within each cell (5,000 permutations); Holm over the six families.", "",
             "| family | contrast | cells | n per condition (median) | mean |d| (null) | cells with |d| ≥ 10 | mean d [item-bootstrap CI] | mean |ΔP(≥50)| | p (perm) | p (Holm) | invasive |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    for k, v in res.items():
        n = v["n_per_condition_median"]
        lines.append(f"| {k} | {FAMILIES[k]} | {v['n_cells']} | {n[0]:.0f} / {n[1]:.0f} | {v['mean_abs_d']:.1f} ({v['null_mean_abs_d']:.1f}) | "
                     f"{v['share_abs_d_ge_10']:.0%} | {v['mean_d']:+.1f} {ci(v['mean_d_ci95'])} | {v['mean_abs_dP']:.2f} | "
                     f"{v['p_perm']:.4f} | {v['p_holm']:.4f} | **{'yes' if v['invasive'] else 'no'}** |")
    lines += ["", "## Replication on experiment 5 run 2 (10 items, anchor (a), 40 conversations per order)", "",
              "| family | cells | mean |d| (null) | cells with |d| ≥ 10 | mean d [CI] | p (perm) |", "|---|---|---|---|---|---|"]
    for k, v in rep.items():
        lines.append(f"| {k} | {v['n_cells']} | {v['mean_abs_d']:.1f} ({v['null_mean_abs_d']:.1f}) | {v['share_abs_d_ge_10']:.0%} | "
                     f"{v['mean_d']:+.1f} {ci(v['mean_d_ci95'])} | {v['p_perm']:.4f} |")
    inv = [k for k, v in res.items() if v["invasive"]]
    lines += ["", "## Pre-registered reading", "",
              f"- Invasive families (Holm p < 0.05): **{', '.join(inv) if inv else 'none'}**.",
              "- Because the model's state at every turn is its copyable context, macrorealism holds by construction and the "
              "\"not asked\" condition is an exact counterfactual at the level of the response distribution (the API exposes no "
              "sampler seed, so the specific draw is not recovered; the clone-read model is still factorisable). Every NSIT "
              "violation above is therefore invasiveness, "
              "never evidence against definite states (§5.2).",
              "- Whether the invasiveness comes from the question or from the record of the answer is direction 2's question."]
    OUT_MD.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


def md_only() -> None:
    o = json.loads(OUT_JSON.read_text())
    write_md(o["families"], o["replication_run2"])


if __name__ == "__main__":
    import sys
    md_only() if "--md-only" in sys.argv else main()

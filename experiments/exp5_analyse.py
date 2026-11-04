"""Experiment 5 analysis, as frozen in experiments/exp5-sequential-judgment.md §6-§7 (D22-D26).

    python experiments/exp5_analyse.py

Fits A5, F5, D5, BA5 (and the A5 kappa = 0 ablation and the plain-solver sensitivity run) on
train-chain MSE, selects on validation MSE, then scores the test chains and the 8 held-out items
once. Runs the two parameter-free checks (QQ on adjacent (S_k, M) pairs; Kvam K1 vs K0) on the
data alone. Writes results/exp5-run-1.{md,json}. No API calls."""

import json
import math
import os
import sys
from multiprocessing import Pool

import numpy as np

import exp5_models as m
import exp5_run as er
from entangled_mind import config

POOL = config.RESULTS / "pool-run-3.json"
CONV = config.RESULTS / "exp5-conversations.json"
OUT_JSON, OUT_MD = config.RESULTS / "exp5-run-1.json", config.RESULTS / "exp5-run-1.md"
FIT_JSON = config.RESULTS / "exp5-fit.json"
REISSUE = config.RESULTS / "exp5-verdict-reissue.json"     # D52
SEEDS = {"A5": 501, "F5": 502, "D5": 503, "BA5": 504, "A5k0": 505, "A5plain": 506}
N_BOOT = 2000

_W = {}


def _init(items, items_plain, convs, extra):
    _W.update(items=items, items_plain=items_plain, convs=convs, extra=extra)


def _chain_se(args):
    """Squared errors (all ratings, and M only) of one chain under one model."""
    model, chain, v = args
    q = chain.split("|")[0]
    it = _W["items_plain"][q] if model == "A5plain" else _W["items"][q]
    se, se_m = [], []
    for turns in _W["convs"][chain]:
        for pr, ob, kind in m.predict(model, it, turns, v, _W["extra"][q]):
            d = (pr - ob) ** 2
            se.append(d)
            if kind == "M":
                se_m.append(d)
    return chain, se, se_m


class Scorer:
    def __init__(self, pool):
        self.pool = pool

    def per_chain(self, model, chains, v):
        return {c: (se, sm) for c, se, sm in self.pool.map(_chain_se, [(model, c, list(v)) for c in chains], chunksize=4)}

    def mse(self, model, chains, v):
        res = self.per_chain(model, chains, v)
        key = 1 if model == "BA5" else 0
        allv = [x for r in res.values() for x in r[key]]
        return float(np.mean(allv)) if allv else float("nan")


def clamp(model, v):
    lo = np.array([s[1] for s in m.SPACES[model]])
    hi = np.array([s[2] for s in m.SPACES[model]])
    v = np.clip(v, lo, hi)
    names = [s[0] for s in m.SPACES[model]]
    if "a" in names and "b" in names:                  # the link needs a < b
        ia, ib = names.index("a"), names.index("b")
        if v[ia] >= v[ib]:
            v[ia] = v[ib] - 1e-3
    return v


def fit(model, scorer, train, val, log):
    rng = np.random.default_rng(SEEDS[model])
    lo = np.array([s[1] for s in m.SPACES[model]])
    hi = np.array([s[2] for s in m.SPACES[model]])
    cands = [clamp(model, lo + rng.random(len(lo)) * (hi - lo)) for _ in range(400)]
    scored = sorted(((scorer.mse(model, train, v), k) for k, v in enumerate(cands)))
    climbed = []
    for rank, (e0, k) in enumerate(scored[:10]):
        v, best = cands[k], e0
        for _ in range(60):
            prop = clamp(model, v + rng.normal(0, 0.1, len(v)) * (hi - lo))
            e = scorer.mse(model, train, prop)
            if e <= best:
                v, best = prop, e
        ve = scorer.mse(model, val, v)
        climbed.append({"params": v.tolist(), "train_mse": best, "val_mse": ve})
        log(f"{model} {rank + 1}/10 train {best:.1f} val {ve:.1f}")
    final = min(climbed, key=lambda c: (c["val_mse"], c["train_mse"]))
    return {"names": [s[0] for s in m.SPACES[model]], "final": final, "candidates": climbed}


# --- statistics helpers -------------------------------------------------------------

def item_boot_delta(se_a, se_b, items, seed=11):
    """Bootstrap over items of MSE_b - MSE_a (pooled over each resample's ratings)."""
    rng = np.random.default_rng(seed)
    pt = np.mean(np.concatenate([se_b[q] for q in items])) - np.mean(np.concatenate([se_a[q] for q in items]))
    vals = []
    for _ in range(N_BOOT):
        s = rng.choice(items, len(items))
        vals.append(np.mean(np.concatenate([se_b[q] for q in s])) - np.mean(np.concatenate([se_a[q] for q in s])))
    lo, hi = np.percentile(vals, [2.5, 97.5])
    return float(pt), float(lo), float(hi)


def ks_1samp_normal(x):
    """One-sample KS against N(0,1); p from the Kolmogorov distribution (asymptotic)."""
    x = np.sort(np.asarray(x, float))
    n = len(x)
    cdf = 0.5 * (1 + np.array([math.erf(v / math.sqrt(2)) for v in x]))
    d = max(np.max(np.arange(1, n + 1) / n - cdf), np.max(cdf - np.arange(n) / n))
    return float(d), kolmogorov_p(d * (math.sqrt(n) + 0.12 + 0.11 / math.sqrt(n)))


def ks_2samp(a, b):
    a, b = np.sort(a), np.sort(b)
    allv = np.concatenate([a, b])
    d = float(np.max(np.abs(np.searchsorted(a, allv, "right") / len(a) - np.searchsorted(b, allv, "right") / len(b))))
    ne = len(a) * len(b) / (len(a) + len(b))
    return d, kolmogorov_p(d * (math.sqrt(ne) + 0.12 + 0.11 / math.sqrt(ne)))


def kolmogorov_p(lam):
    if lam < 1e-6:
        return 1.0
    return float(min(1.0, max(0.0, 2 * sum((-1) ** (j - 1) * math.exp(-2 * j * j * lam * lam) for j in range(1, 101)))))


def g_test_1df(k1, n1, k2, n2):
    p = (k1 + k2) / (n1 + n2)
    g = 0.0
    for k, n in ((k1, n1), (k2, n2)):
        for obs, exp in ((k, n * p), (n - k, n * (1 - p))):
            if obs > 0:
                g += 2 * obs * math.log(obs / exp)
    return g


# --- main ---------------------------------------------------------------------

def main() -> None:
    split = json.loads(er.SPLIT.read_text())
    recs = {r["id"]: r for r in json.loads(POOL.read_text())["records"]}
    conv = json.loads(CONV.read_text())
    cand, held = split["candidates"], split["item_heldout"]
    n_err = 0
    convs = {}
    for q in cand:
        for chain in er.CHAINS:
            lst = []
            for r in range(er.R_CHAIN):
                c = conv.get(f"{q}|{chain}|{r}")
                if c is None:
                    continue
                if any(t["kind"] == "error" for t in c["turns"]):
                    n_err += 1
                    continue
                lst.append(c["turns"])
            convs[f"{q}|{chain}"] = lst
    items = {q: m.item_data(recs[q]) for q in cand}
    items_plain = {q: m.item_data(recs[q], solver="plain") for q in cand}
    extra = {q: (100 * m.a5_expect_M(m.a5_prep(items[q], m.KAPPA0), items[q]),
                 1 if recs[q]["model_answer"] == "yes" else -1) for q in cand}
    train, val, test = split["train"], split["validation"], split["test"]
    held_chains = [f"{q}|{c}" for q in held for c in er.CHAINS]
    log = lambda s: print(s, flush=True)
    fits = json.loads(FIT_JSON.read_text()) if FIT_JSON.exists() else {}
    with Pool(min(10, os.cpu_count()), initializer=_init, initargs=(items, items_plain, convs, extra)) as pool:
        sc = Scorer(pool)
        for model in ("A5", "F5", "D5", "BA5", "A5k0", "A5plain"):
            if model not in fits:
                fits[model] = fit(model, sc, train, val, log)
                FIT_JSON.write_text(json.dumps(fits, indent=1))
        # one-time scoring of test chains and held-out items
        evals = {}
        for name, chains in (("test", test), ("heldout", held_chains)):
            evals[name] = {}
            models = {k: fits[k]["final"]["params"] for k in fits}
            models["A5_0"], models["F5_0"] = m.A5_0, m.F5_0
            for mk, v in models.items():
                base = {"A5_0": "A5", "F5_0": "F5"}.get(mk, mk)
                res = sc.per_chain(base, chains, v)
                se, sem = {}, {}
                for c, (a, b) in res.items():
                    q = c.split("|")[0]
                    se.setdefault(q, []).extend(a)
                    sem.setdefault(q, []).extend(b)
                evals[name][mk] = {"se": {q: np.array(v_) for q, v_ in se.items()},
                                   "se_m": {q: np.array(v_) for q, v_ in sem.items()}}
    nc = [v_ for q in cand for v_ in er.qq_pairs(recs[q], er.chain_claims(recs[q]))[1].values()]
    out = {"n_conversations_excluded_schema": n_err, "fits": fits, "evals": {},
           "noncommuting_chain_claims": [int(sum(x > 1e-6 for x in nc)), len(nc), float(max(nc))]}
    for name, ev in evals.items():
        its = sorted(ev["A5"]["se"])
        row = {"items": its, "mse": {}, "mse_M": {}}
        for mk, d in ev.items():
            row["mse"][mk] = float(np.mean(np.concatenate([d["se"][q] for q in its]))) if mk != "BA5" else None
            row["mse_M"][mk] = float(np.mean(np.concatenate([d["se_m"][q] for q in its])))
        row["delta_F5_minus_A5"] = item_boot_delta(ev["A5"]["se"], ev["F5"]["se"], its)
        row["delta_F50_minus_A50"] = item_boot_delta(ev["A5_0"]["se"], ev["F5_0"]["se"], its)
        row["delta_A5k0_minus_A5"] = item_boot_delta(ev["A5"]["se"], ev["A5k0"]["se"], its)
        row["delta_D5_minus_A5"] = item_boot_delta(ev["A5"]["se"], ev["D5"]["se"], its)
        row["delta_M_BA5_minus_A5"] = item_boot_delta(ev["A5"]["se_m"], ev["BA5"]["se_m"], its)
        row["delta_M_F5_minus_A5"] = item_boot_delta(ev["A5"]["se_m"], ev["F5"]["se_m"], its)
        row["delta_F5_minus_A5plain"] = item_boot_delta(ev["A5plain"]["se"], ev["F5"]["se"], its)
        # by category and by whether the model was right (test only)
        groups = {}
        for q in its:
            groups.setdefault(("right" if recs[q]["correct"] else "wrong"), []).append(q)
            groups.setdefault(recs[q]["category"], []).append(q)
        row["by_group"] = {g: {"n_items": len(qs), "mse_A5": float(np.mean(np.concatenate([ev["A5"]["se"][q] for q in qs]))),
                               "mse_F5": float(np.mean(np.concatenate([ev["F5"]["se"][q] for q in qs])))}
                           for g, qs in groups.items()}
        out["evals"][name] = row
    d = out["evals"]["test"]["delta_F5_minus_A5"]
    primary = "pass" if d[1] > 0 else ("classical" if d[2] < 0 else "tie")
    out["primary"] = primary
    out["qq"] = qq_check(cand, recs, conv, split)
    out["kvam"] = kvam_check(cand, conv, items, extra)
    out["descriptive"] = descriptive(cand, conv)
    qq_present = out["qq"]["signature_present"]
    kv_present = out["kvam"]["signature_present"]
    # D26 addendum: Kvam "commitment" (CI above 0, the opposite sign) counts as that signature contradicted
    qq_contra = out["qq"]["signature_contradicted"] or out["kvam"]["commitment"]
    if primary == "pass" and (qq_present or kv_present) and not qq_contra:
        verdict = "quantum supported"
    elif primary == "pass":
        verdict = "quantum fits better, no unique signature"
    elif primary == "tie" and not qq_contra:
        verdict = "tie"
    elif primary == "classical" or qq_contra:
        verdict = "classical"
    else:
        verdict = "tie"
    out["verdict"] = verdict
    OUT_JSON.write_text(json.dumps(out, indent=1, default=float))
    write_md(out)


def qq_check(cand, recs, conv, split) -> dict:
    pairs = []
    for q in cand:
        nc_all = er.qq_pairs(recs[q], er.chain_claims(recs[q]))[1]
        for k in split["qq_pairs"][q]:
            rows = {}
            for order in ("SM", "MS"):
                lst = []
                for r in range(er.R_QQ):
                    c = conv.get(f"{q}|QQ{k}{order}|{r}")
                    if not c:
                        continue
                    rt = [t for t in c["turns"] if t["kind"] in ("S", "M")]
                    if len(rt) != 2:
                        continue
                    s = next(t["rating"] for t in rt if t["kind"] == "S")
                    mm = next(t["rating"] for t in rt if t["kind"] == "M")
                    lst.append((s, mm))
                rows[order] = np.array(lst, float)
            pairs.append({"item": q, "claim": k, "nc": nc_all[k], "rows": rows})
    rng = np.random.default_rng(7)

    def stats(rows, cut=50):
        out = {}
        joint = {}
        for o in ("SM", "MS"):
            y = rows[o] >= cut
            joint[o] = {(a, b): float(np.mean((y[:, 0] == a) & (y[:, 1] == b))) for a in (True, False) for b in (True, False)}
        c = {xy: joint["SM"][xy] - joint["MS"][xy] for xy in joint["SM"]}
        oe = max(abs(c[(True, True)]) + abs(c[(False, False)]), abs(c[(True, False)]) + abs(c[(False, True)]))
        ys = {o: rows[o] >= cut for o in rows}
        oe_s = float(ys["MS"][:, 0].mean() - ys["SM"][:, 0].mean())     # S asked second (MS) minus first (SM)
        oe_m = float(ys["SM"][:, 1].mean() - ys["MS"][:, 1].mean())     # M asked second (SM) minus first (MS)
        dis = {o: float(np.mean(ys[o][:, 0] != ys[o][:, 1])) for o in ys}
        q_ = dis["SM"] - dis["MS"]
        n1, n2 = len(rows["SM"]), len(rows["MS"])
        ph = (dis["SM"] * n1 + dis["MS"] * n2) / (n1 + n2)
        z = q_ / math.sqrt(ph * (1 - ph) * (1 / n1 + 1 / n2)) if 0 < ph < 1 else 0.0
        out.update(OE=oe, OE_S=oe_s, OE_M=oe_m, OSS=abs(oe_s) + abs(oe_m), q=q_, z=z,
                   Gamma=abs(q_) - (abs(oe_s) + abs(oe_m)),
                   LR=g_test_1df(dis["SM"] * n1, n1, dis["MS"] * n2, n2))
        # chi2(3): order x joint cell
        tab = np.array([[joint[o][xy] * len(rows[o]) for xy in joint["SM"]] for o in ("SM", "MS")])
        expct = tab.sum(1, keepdims=True) * tab.sum(0, keepdims=True) / tab.sum()
        with np.errstate(divide="ignore", invalid="ignore"):
            out["chi2_3"] = float(np.nansum(np.where(expct > 0, (tab - expct) ** 2 / expct, 0)))
        return out

    for p in pairs:
        p["stats"] = stats(p["rows"])
        boots = [stats({o: r[rng.integers(0, len(r), len(r))] for o, r in p["rows"].items()})["OE"] for _ in range(1000)]
        p["OE_ci95"] = [float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))]
        p["q_by_cut"] = {cut: stats(p["rows"], cut)["q"] for cut in (30, 40, 60, 70)}
    big = [p for p in pairs if p["stats"]["OE"] > 0.10 and p["OE_ci95"][0] > 0]
    pilot = json.loads(er.PILOT_JSON.read_text())["gates"]
    res = {"n_pairs": len(pairs), "G2_passed": pilot["G2"], "n_large_OE": len(big)}
    if big:
        ks_d, ks_p = ks_1samp_normal([p["stats"]["z"] for p in big])
        qs = np.array([p["stats"]["q"] for p in big])
        items = sorted({p["item"] for p in big})
        bq = []
        for _ in range(N_BOOT):
            s = rng.choice(items, len(items))
            bq.append(np.mean([p["stats"]["q"] for it_ in s for p in big if p["item"] == it_]))
        lo, hi = np.percentile(bq, [2.5, 97.5])
        res.update(KS_D=ks_d, KS_p=ks_p, mean_q=float(qs.mean()), mean_q_ci95=[float(lo), float(hi)])
        res["signature_present"] = bool(pilot["G2"] and len(big) >= 5 and ks_p > 0.05 and lo >= -0.05 and hi <= 0.05)
        res["signature_contradicted"] = bool(lo > 0 or hi < 0)
    else:
        res.update(signature_present=False, signature_contradicted=False)
    # a priori sub-test: OE larger on the large-|sin dphi| pair than on the small one, within items
    wins = losses = ties_nc = 0
    by_item = {}
    for p in pairs:
        by_item.setdefault(p["item"], []).append(p)
    for q, ps in by_item.items():
        if len(ps) != 2 or abs(ps[0]["nc"] - ps[1]["nc"]) <= 1e-6:   # D32: solver round-off is not a prediction
            ties_nc += 1
            continue
        hi_p, lo_p = sorted(ps, key=lambda p: -p["nc"])
        if hi_p["stats"]["OE"] > lo_p["stats"]["OE"]:
            wins += 1
        elif hi_p["stats"]["OE"] < lo_p["stats"]["OE"]:
            losses += 1
    nn = wins + losses
    p_sign = sum(math.comb(nn, j) for j in range(wins, nn + 1)) / 2 ** nn if nn else float("nan")
    res["apriori_subtest"] = {"items_with_distinct_noncommutativity": nn + 0, "wins": wins, "losses": losses,
                              "items_tied_noncommutativity": ties_nc, "sign_test_p_one_sided": p_sign}
    res["pairs"] = [{k: v for k, v in p.items() if k != "rows"} | {"n": {o: len(r) for o, r in p["rows"].items()}} for p in pairs]
    return res


def kvam_check(cand, conv, items, extra) -> dict:
    rng = np.random.default_rng(13)
    per = {}
    for q in cand:
        fin = {}
        choices = []
        for chain in ("K1", "K0"):
            lst = []
            for r in range(er.R_CHAIN):
                c = conv.get(f"{q}|{chain}|{r}")
                if not c or any(t["kind"] == "error" for t in c["turns"]):
                    continue
                last = c["turns"][-1]
                if last["kind"] == "M":
                    lst.append(last["rating"])
                    if chain == "K1":
                        ch = next((t["answer"] for t in c["turns"] if t["kind"] == "C"), None)
                        choices.append((ch, last["rating"]))
            fin[chain] = np.array(lst, float)
        if len(fin["K1"]) and len(fin["K0"]):
            dk = float(np.mean(np.abs(fin["K1"] - 50)) - np.mean(np.abs(fin["K0"] - 50)))
            ks = ks_2samp(fin["K1"], fin["K0"])
            pc = {c: np.mean([x[0] == c for x in choices]) for c in ("yes", "no")}
            tp = float(np.mean(fin["K0"]) - sum(pc[c] * np.mean([x[1] for x in choices if x[0] == c])
                                                for c in pc if pc[c] > 0))
            # A5_0's predicted sign of Delta_K on the observed conversations
            pred = {}
            for chain in ("K1", "K0"):
                vals = []
                for r in range(er.R_CHAIN):
                    c = conv.get(f"{q}|{chain}|{r}")
                    if not c or any(t["kind"] == "error" for t in c["turns"]):
                        continue
                    pr = [x for x in m.run_a5(items[q], c["turns"], m.A5_0) if x[2] == "M"]
                    if pr:
                        vals.append(abs(pr[-1][0] - 50))
                pred[chain] = np.mean(vals) if vals else float("nan")
            per[q] = {"delta_K": dk, "KS_D": ks[0], "KS_p": ks[1], "TP_residual": tp,
                      "A5_0_pred_sign": float(np.sign(pred["K1"] - pred["K0"]))}
    qs = sorted(per)
    dks = np.array([per[q]["delta_K"] for q in qs])
    boots = [np.mean(rng.choice(dks, len(dks))) for _ in range(N_BOOT)]
    lo, hi = np.percentile(boots, [2.5, 97.5])
    agree = np.mean([np.sign(per[q]["delta_K"]) == per[q]["A5_0_pred_sign"] for q in qs if per[q]["delta_K"] != 0])
    return {"per_item": per, "mean_delta_K": float(dks.mean()), "ci95": [float(lo), float(hi)],
            "signature_present": bool(hi < 0), "commitment": bool(lo > 0), "A5_0_sign_agreement": float(agree),
            "mean_TP_residual": float(np.mean([per[q]["TP_residual"] for q in qs]))}


def descriptive(cand, conv) -> dict:
    rep, anch = [], {"a": [], "b": []}
    order_span = []
    for q in cand:
        for r in range(er.R_CHAIN):
            c = conv.get(f"{q}|MF|{r}")
            if c and not any(t["kind"] == "error" for t in c["turns"]):
                ms = [t["rating"] for t in c["turns"] if t["kind"] == "M"]
                if len(ms) == 2:
                    rep.append(abs(ms[1] - ms[0]) <= 5)
            c = conv.get(f"{q}|B0|{r}")
            if c and c["turns"] and c["turns"][-1]["kind"] == "M":
                anch[c["anchor"]].append(c["turns"][-1]["rating"])
        means = []
        for chain in ("O1", "O2", "O3", "O4", "X1", "X2", "X3", "X4", "B0"):
            v = [conv[f"{q}|{chain}|{r}"]["turns"][-1]["rating"] for r in range(er.R_CHAIN)
                 if f"{q}|{chain}|{r}" in conv and conv[f"{q}|{chain}|{r}"]["turns"]
                 and conv[f"{q}|{chain}|{r}"]["turns"][-1]["kind"] == "M"]
            if v:
                means.append(np.mean(v))
        order_span.append(max(means) - min(means))
    return {"MF_replicability_rate": float(np.mean(rep)), "B0_mean_by_anchor": {k: float(np.mean(v)) for k, v in anch.items()},
            "M_span_median": float(np.median(order_span))}


def write_md(o) -> None:
    f = lambda d: f"{d[0]:+.1f} [{d[1]:+.1f}, {d[2]:+.1f}]"
    t, h = o["evals"]["test"], o["evals"]["heldout"]
    names = {"A5": "A5 quantum belief state (fitted)", "F5": "F5 classical twin (fitted)", "D5": "D5 dephased quantum (fitted)",
             "BA5": "BA5 belief adjustment (fitted; M only)", "A5k0": "A5 with κ = 0 (fitted)",
             "A5plain": "A5 with the plain v1 solver (sensitivity)", "A5_0": "A5⁰ (a priori, unfitted)", "F5_0": "F5⁰ (a priori, unfitted)"}
    lines = ["# Experiment 5, run 1: sequential, context-dependent judgment", "",
             "Frozen pre-registration: `experiments/exp5-sequential-judgment.md` (D22–D26). Base model `claude-haiku-5-5`, "
             "thinking disabled, default temperature. 40 items × 12 chain types × 10 conversations, plus the QQ block "
             "(40 items × 2 pairs × 2 orders × 40). Pilot gates passed (`results/exp5-pilot.md`). "
             f"Conversations excluded for a schema failure: {o['n_conversations_excluded_schema']}."
             + (f" Conversations in all (pilot included): {o['n_conversations']:,}; experiment-5 API cost **${o['cost_usd']:.2f}** "
                f"of the $4 cap; no refusal." if "n_conversations" in o else ""), "",
             f"Predicted non-commutativity at encode: |sin Δφ| > 10⁻⁶ on {o['noncommuting_chain_claims'][0]} of "
             f"{o['noncommuting_chain_claims'][1]} chain claims across the 40 items (max {o['noncommuting_chain_claims'][2]:.3f}); "
             "every other chain claim's sub-question commutes with the main question at encode.", "",
             "> As the pre-registration put it before any data (§8.6): *the anchored phase solve works against A5 … "
             "Expect A5 and F5 to be close on most claims.* The pre-registration anticipated that A5 and F5 would be close; it designated no verdict as predicted.", "",
             "## Fits (train / validation MSE, rating points²)", "", "| model | train | validation | parameters |", "|---|---|---|---|"]
    for k, fd in o["fits"].items():
        ps = ", ".join(f"{n}={x:.3g}" for n, x in zip(fd["names"], fd["final"]["params"]))
        lines.append(f"| {names[k]} | {fd['final']['train_mse']:.1f} | {fd['final']['val_mse']:.1f} | {ps} |")
    for label, row in (("Test chains (77, scored once)", t), ("Held-out items (8, scored once)", h)):
        lines += ["", f"## {label}", "", "| model | MSE, all ratings | MSE, main ratings only |", "|---|---|---|"]
        for k in ("A5", "F5", "D5", "BA5", "A5k0", "A5plain", "A5_0", "F5_0"):
            a = "—" if row["mse"][k] is None else f"{row['mse'][k]:.1f}"
            lines.append(f"| {names[k]} | {a} | {row['mse_M'][k]:.1f} |")
        lines += ["", "Paired item-bootstrap differences (positive favours the first-named model's competitor being worse):", "",
                  f"- **Δ = MSE_F5 − MSE_A5: {f(row['delta_F5_minus_A5'])}**",
                  f"- A5⁰ vs F5⁰ (unfitted): MSE_F5⁰ − MSE_A5⁰ = {f(row['delta_F50_minus_A50'])}",
                  f"- entanglement ablation: MSE_(A5, κ=0) − MSE_A5 = {f(row['delta_A5k0_minus_A5'])}",
                  f"- dephasing: MSE_D5 − MSE_A5 = {f(row['delta_D5_minus_A5'])}",
                  f"- main ratings only: MSE_BA5 − MSE_A5 = {f(row['delta_M_BA5_minus_A5'])}; MSE_F5 − MSE_A5 = {f(row['delta_M_F5_minus_A5'])}",
                  f"- sensitivity (plain solver): MSE_F5 − MSE_A5plain = {f(row['delta_F5_minus_A5plain'])}"]
    q, k = o["qq"], o["kvam"]
    lines += ["", f"## Primary (§7.2): **{o['primary'].upper()}**", "",
              "## Parameter-free check 1: QQ on adjacent (S_k, M) pairs (§7.3)", "",
              f"- G2 (pilot): {'passed' if q['G2_passed'] else 'failed'}. Pairs: {q['n_pairs']}. Pairs with OE > 0.10 and CI excluding 0: **{q['n_large_OE']}**."]
    if q["n_large_OE"]:
        lines.append(f"- On those pairs: KS of z against N(0,1) D = {q['KS_D']:.3f}, p = {q['KS_p']:.3f}; mean q = {q['mean_q']:+.3f} "
                     f"[{q['mean_q_ci95'][0]:+.3f}, {q['mean_q_ci95'][1]:+.3f}].")
    a = q["apriori_subtest"]
    lines += [f"- Signature present: **{q['signature_present']}**; contradicted: **{q['signature_contradicted']}**.",
              f"- A priori sub-test (OE larger on the larger-|sin Δφ| pair): {a['wins']} wins, {a['losses']} losses over "
              f"{a['items_with_distinct_noncommutativity']} items with distinct predicted non-commutativity "
              f"({a['items_tied_noncommutativity']} items tied within 10⁻⁶, almost all with both pairs at 0); one-sided sign test "
              f"p = {a['sign_test_p_one_sided']:.3f}. (First computed with exact float comparison, which let solver round-off "
              "of 10⁻¹⁶–10⁻⁹ order the pairs and gave a spurious 28–9; corrected in D32.)",
              "", "| pair | |sin Δφ| | OE [95% CI] | OE_S | OE_M | OSS | q | z | Γ |", "|---|---|---|---|---|---|---|---|---|"]
    for p in q["pairs"]:
        s = p["stats"]
        lines.append(f"| {p['item']}:S{p['claim']} | {p['nc']:.3f} | {s['OE']:.2f} [{p['OE_ci95'][0]:.2f}, {p['OE_ci95'][1]:.2f}] | "
                     f"{s['OE_S']:+.2f} | {s['OE_M']:+.2f} | {s['OSS']:.2f} | {s['q']:+.3f} | {s['z']:+.2f} | {s['Gamma']:+.2f} |")
    lines += ["", "## Parameter-free check 2: Kvam-style interference, K1 vs K0 (§7.4)", "",
              f"- Mean Δ_K = mean |r − 50| after a choice minus after the filler: **{k['mean_delta_K']:+.2f}** "
              f"[{k['ci95'][0]:+.2f}, {k['ci95'][1]:+.2f}] (items: {len(k['per_item'])}).",
              f"- Quantum signature (CI below 0): **{k['signature_present']}**; commitment (CI above 0): **{k['commitment']}**.",
              f"- Mean total-probability residual: {k['mean_TP_residual']:+.2f} points. A5⁰'s predicted sign of Δ_K agrees on "
              f"{k['A5_0_sign_agreement']:.0%} of items.", "",
              f"## Verdict (§7.5), as first issued on the pooled q: **{o['verdict'].upper()}** (superseded)", "",
              *([f"Superseded by D52: re-issued under the same rule on the single-direction q as "
                 f"**{json.loads(REISSUE.read_text())['verdict_reissued'].upper()}** (`results/exp5-verdict-reissue.md`).", ""]
                if REISSUE.exists() else []),
              "## Reported alongside", "",
              f"- Replicability in MF (|M₂ − M₁| ≤ 5 points): {o['descriptive']['MF_replicability_rate']:.0%}.",
              f"- B0 mean rating by anchor direction (after recoding): {', '.join(f'{a_} {v:.1f}' for a_, v in o['descriptive']['B0_mean_by_anchor'].items())}.",
              f"- Median span of main-rating means across O1–O4, X1–X4, B0: {o['descriptive']['M_span_median']:.1f} points.", "",
              "| test group | items | MSE A5 | MSE F5 |", "|---|---|---|---|"]
    for g, v in t["by_group"].items():
        lines.append(f"| {g} | {v['n_items']} | {v['mse_A5']:.1f} | {v['mse_F5']:.1f} |")
    OUT_MD.write_text("\n".join(lines) + "\n")
    print("\n".join(lines[:40]))


def md_only() -> None:
    """Rewrite the markdown from the archived JSON (no refitting); recomputes the a priori sub-test with the D32 tolerance."""
    o = json.loads(OUT_JSON.read_text())
    by = {}
    for p in o["qq"]["pairs"]:
        by.setdefault(p["item"], []).append(p)
    wins = losses = ties = 0
    for ps in by.values():
        if len(ps) != 2 or abs(ps[0]["nc"] - ps[1]["nc"]) <= 1e-6:
            ties += 1
            continue
        hi_p, lo_p = sorted(ps, key=lambda p: -p["nc"])
        wins += hi_p["stats"]["OE"] > lo_p["stats"]["OE"]
        losses += hi_p["stats"]["OE"] < lo_p["stats"]["OE"]
    nn = wins + losses
    o["qq"]["apriori_subtest"] = {"items_with_distinct_noncommutativity": nn, "wins": wins, "losses": losses,
                                  "items_tied_noncommutativity": ties,
                                  "sign_test_p_one_sided": sum(math.comb(nn, j) for j in range(wins, nn + 1)) / 2 ** nn if nn else float("nan")}
    conv = json.loads(CONV.read_text())
    o["n_conversations"] = len(conv)
    o["cost_usd"] = sum(v["cost"] for v in conv.values())
    OUT_JSON.write_text(json.dumps(o, indent=1, default=float))
    write_md(o)


if __name__ == "__main__":
    md_only() if "--md-only" in sys.argv else main()

"""Biomimetic map, the two new runs: the PT+N sampling identity (experiments/bm2-sampling-identity.md, D43;
$0.10 cap) and serial dependence with run 3's anchors as the model's own earlier answer
(experiments/bm1-serial-dependence.md, D44; $0.40 cap). Any refusal stops the run.

    python experiments/bm_runs.py bm2|bm1 [--analyse]

Calls cached in results/bm2-calls.json and results/bm1-calls.json."""

import json
import sys

import numpy as np

from entangled_mind import config
from gm_common import PLAIN, Caller, structured

MODEL = "claude-haiku-5-5"
SCALE = ", where 0 = certainly false and 100 = certainly true"
RATE = {"type": "object", "properties": {"probability": {"type": "integer"}}, "required": ["probability"], "additionalProperties": False}
ITEMS = config.EXPERIMENTS / "exp4-items.json"


def ask(stmt, ctx):
    return f"{ctx}\n\nOn a scale from 0 to 100{SCALE}, how likely is it that {stmt}? Give only the number."


def rate(msgs, label):
    d, raw, cost, rid = structured(MODEL, msgs, RATE, label, max_tokens=200)
    return min(100, max(0, int(d["probability"]))) / 100, raw, cost, rid


# --- bm2: Z = P(A) + P(B) - P(A and B) - P(A or B) -----------------------------------

BM2_CACHE = config.RESULTS / "bm2-calls.json"
STMTS = {"X": lambda it: it["X"], "Y": lambda it: it["Y"], "XY": lambda it: f"{it['X']} and {it['Y']}",
         "XorY": lambda it: f"{it['X']} or {it['Y']} (or both)"}


def bm2_run():
    items = json.loads(ITEMS.read_text())
    c = Caller(BM2_CACHE, 0.10, "bm2 identity")

    def call(job):
        _, it, s, _r = job
        p, _, cost, rid = rate([{"role": "user", "content": ask(STMTS[s](it), it["context"])}], "bm2")
        return {"p": p, "cost": cost, "request_id": rid}
    c.run([(f"{it['id']}|{s}|{r}", it, s, r) for it in items for s in STMTS for r in range(20)], call, workers=8)


def bm2_analyse():
    items = json.loads(ITEMS.read_text())
    cache = json.loads(BM2_CACHE.read_text())
    fallacy = set(json.loads((config.RESULTS / "exp4-run-1.json").read_text())["fallacy_items"])
    data = {it["id"]: {s: np.array([cache[f"{it['id']}|{s}|{r}"]["p"] for r in range(20) if f"{it['id']}|{s}|{r}" in cache])
                       for s in STMTS} for it in items}
    Z = lambda d: d["X"].mean() + d["Y"].mean() - d["XY"].mean() - d["XorY"].mean()
    rng = np.random.default_rng(5353)
    ids = list(data)
    slope = lambda pts: np.polyfit([p for p, _ in pts], [z for _, z in pts], 1)     # [b, a]
    # split halves (D43): predictor from repeats 0-9 of X and Y, Z from repeats 10-19 of all four
    half = lambda d, h: {s: v[:10] if h == 0 else v[10:] for s, v in d.items()}
    pred = lambda d: d["X"].mean() + d["Y"].mean() - 1
    boots, sboots = [], []
    for _ in range(2000):
        pts, zs = [], []
        for q in rng.choice(ids, len(ids)):
            h0, h1 = half(data[q], 0), half(data[q], 1)
            d0 = {s: rng.choice(v, len(v)) for s, v in h0.items()}
            d1 = {s: rng.choice(v, len(v)) for s, v in h1.items()}
            pts.append((pred(d0), Z(d1)))
            zs.append(Z({s: np.concatenate([d0[s], d1[s]]) for s in d0}))
        boots.append(np.mean(zs))
        sboots.append(slope(pts))
    sb = np.percentile(np.array(sboots), [2.5, 97.5], axis=0)
    b_hat, a_hat = slope([(pred(half(d, 0)), Z(half(d, 1))) for d in data.values()])
    per = {q: {"Z": float(Z(d)), **{f"P_{s}": float(v.mean()) for s, v in d.items()},
               "conj_fallacy": bool(d["XY"].mean() > min(d["X"].mean(), d["Y"].mean())),
               "disj_fallacy": bool(d["XorY"].mean() < max(d["X"].mean(), d["Y"].mean())), "run2_fallacy_item": q in fallacy}
           for q, d in data.items()}
    mz = float(np.mean([v["Z"] for v in per.values()]))
    lo, hi = map(float, np.percentile(boots, [2.5, 97.5]))
    if -0.05 <= lo and hi <= 0.05:
        z_reading = "holds (CI within ±0.05)"
    elif lo > 0.05 or hi < -0.05:
        z_reading = "violated (CI wholly outside ±0.05)"
    else:
        z_reading = "undetermined"
    if sb[0][0] > 0:
        reading = "positive Z slope: the sampler with extra conjunction/disjunction noise"
    elif sb[1][0] < 0:
        reading = "opposite (negative) Z slope"
    else:
        reading = "flat Z slope: coherent, affine or PT+N 2014"
    sd = [(abs(v.mean() - 0.5), v.std(ddof=1)) for d in data.values() for v in d.values() if len(v) > 1]
    sd_corr = float(np.corrcoef(*zip(*sd))[0, 1])
    out = {"mean_Z": mz, "ci95": [lo, hi], "per_item": per, "reading": reading, "mean_Z_reading": z_reading,
           "slope_b": float(b_hat), "intercept_a": float(a_hat), "slope_b_ci95": sb[:, 0].tolist(), "intercept_a_ci95": sb[:, 1].tolist(),
           "sd_vs_extremity_corr": sd_corr,
           "conj_fallacy": {"all": sum(v["conj_fallacy"] for v in per.values()),
                            "run2_items": sum(v["conj_fallacy"] for v in per.values() if v["run2_fallacy_item"])},
           "disj_fallacy": sum(v["disj_fallacy"] for v in per.values()),
           "n_calls": len(cache), "cost_usd": sum(v["cost"] for v in cache.values())}
    (config.RESULTS / "bm2-sampling-identity.json").write_text(json.dumps(out, indent=1))
    lines = ["# Biomimetic (rev. 2 §3.4): the probability-theory-plus-noise identity and its Z slope on the experiment 4 items", "",
             "Pre-registered in `experiments/bm2-sampling-identity.md` (D43), committed before any call. 16 items × 4 statements × 20, "
             f"`claude-haiku-5-5`, thinking disabled, one scale direction. {out['n_calls']} calls, **${out['cost_usd']:.3f}** of the $0.10 "
             "cap; no refusal.", "", PLAIN,
             "## Z = P(X) + P(Y) − P(X∧Y) − P(X∨Y)", "",
             f"- **Primary: item-level slope of Z (repeats 10–19) on P(X) + P(Y) − 1 (repeats 0–9): b = {b_hat:+.3f} [{sb[0][0]:+.3f}, {sb[1][0]:+.3f}]**; intercept "
             f"a = {a_hat:+.3f} [{sb[0][1]:+.3f}, {sb[1][1]:+.3f}] (bootstrap over items and conversations).",
             f"- Secondary: mean Z = {mz:+.3f} [{lo:+.3f}, {hi:+.3f}] (equivalence band ±0.05): **{z_reading}**.",
             f"- Conjunction fallacy (P(X∧Y) > min): {out['conj_fallacy']['all']} of 16 items; {out['conj_fallacy']['run2_items']} of the "
             f"{sum(v['run2_fallacy_item'] for v in per.values())} run-2 fallacy items. Disjunction fallacy (P(X∨Y) < max): {out['disj_fallacy']} of 16.",
             f"- Between-repeat SD against |mean − 0.5| across the 64 statements: r = {sd_corr:+.2f} (the Bayesian sampler predicts "
             "negative; floors and ceilings predict the same).", "",
             "| item | P(X) | P(Y) | P(X∧Y) | P(X∨Y) | Z | conj. fallacy | run-2 fallacy item |", "|---|---|---|---|---|---|---|---|"]
    for q, v in per.items():
        lines.append(f"| {q} | {v['P_X']:.2f} | {v['P_Y']:.2f} | {v['P_XY']:.2f} | {v['P_XorY']:.2f} | {v['Z']:+.2f} | "
                     f"{'yes' if v['conj_fallacy'] else 'no'} | {'yes' if v['run2_fallacy_item'] else ''} |")
    lines += ["", f"## Pre-registered reading: **{reading}**"]
    (config.RESULTS / "bm2-sampling-identity.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines[:16] + lines[-1:]))


# --- bm1: serial dependence ---------------------------------------------------------------

BM1_CACHE = config.RESULTS / "bm1-calls.json"
CELLS = [("X", "lo"), ("X", "hi"), ("Y", "lo"), ("Y", "hi")]


def bm1_run():
    items = json.loads(ITEMS.read_text())
    anchors = json.loads((config.EXPERIMENTS / "exp4-run-3-anchors.json").read_text())
    c = Caller(BM1_CACHE, 0.40, "bm1 serial dependence")

    def call(job):
        _, it, o, lvl, _r = job
        A = anchors[it["id"]][f"A_{o}"][0 if lvl == "lo" else 1]
        stmt = it[o]
        q1 = ask(stmt, it["context"])
        msgs = [{"role": "user", "content": q1}, {"role": "assistant", "content": json.dumps({"probability": A})},
                {"role": "user", "content": f"Please give your rating again. On a scale from 0 to 100{SCALE}, how likely is it that "
                                            f"{stmt}? Give only the number."}]
        r1, raw1, c1, id1 = rate(msgs, "bm1")
        msgs += [{"role": "assistant", "content": raw1},
                 {"role": "user", "content": f"On a scale from 0 to 100{SCALE}, how likely is it that {it['X']} and {it['Y']}? "
                                             "Give only the number."}]
        r2, _, c2, id2 = rate(msgs, "bm1")
        return {"A": A / 100, "r1": r1, "r2": r2, "cost": c1 + c2, "request_ids": [id1, id2]}
    c.run([(f"{it['id']}|{o}-{lvl}|{r}", it, o, lvl, r) for it in items for o, lvl in CELLS for r in range(40)], call, workers=8)


def slopes(cache, q, o):
    lo = [v for k, v in cache.items() if k.startswith(f"{q}|{o}-lo|")]
    hi = [v for k, v in cache.items() if k.startswith(f"{q}|{o}-hi|")]
    dA = np.mean([v["A"] for v in hi]) - np.mean([v["A"] for v in lo])
    return (np.mean([v["r1"] for v in hi]) - np.mean([v["r1"] for v in lo])) / dA, lo, hi


def bm1_analyse():
    items = [it["id"] for it in json.loads(ITEMS.read_text())]
    own = json.loads(BM1_CACHE.read_text())
    other = json.loads((config.RESULTS / "exp4-run-3-calls.json").read_text())
    per = {}
    for q in items:
        for o in ("X", "Y"):
            s_own, lo, hi = slopes(own, q, o)
            s_oth, lo2, hi2 = slopes(other, q, o)
            echo = float(np.mean([abs(v["r1"] - v["A"]) < 0.005 for v in lo + hi]))
            per[f"{q}|{o}"] = {"s_own": float(s_own), "s_other": float(s_oth), "echo_rate": echo,
                               "r2_own": float(np.mean([v["r2"] for v in lo + hi])), "r2_other": float(np.mean([v["r2"] for v in lo2 + hi2]))}
    keys = list(per)
    contrast = [k for k in keys if per[k]["s_other"] < 0]
    rng = np.random.default_rng(5454)
    by_item = {q: [k for k in keys if k.startswith(q + "|")] for q in items}

    def stats(sample_items):
        ks = [k for q in sample_items for k in by_item[q]]
        cs = [k for k in ks if k in contrast]
        return (np.mean([per[k]["s_own"] for k in ks]), np.mean([per[k]["s_own"] - per[k]["s_other"] for k in ks]),
                np.mean([per[k]["s_own"] - per[k]["s_other"] for k in cs]) if cs else np.nan,
                np.mean([per[k]["s_other"] for k in ks]))
    est = stats(items)
    b = np.array([stats(list(rng.choice(items, len(items)))) for _ in range(2000)])
    lohi = np.nanpercentile(b, [2.5, 97.5], axis=0)
    maj = sum(per[k]["s_own"] > 0 for k in contrast)
    if lohi[1][0] <= 0 or lohi[0][0] <= 0:
        reading = "resists its own planted answer too"
    elif lohi[0][1] > 0:
        reading = "source-dependent self-consistency (own > other)"
    elif lohi[0][3] > 0:
        reading = "source-independent attraction (stimulus-history serial dependence)"
    else:
        reading = "own attraction, other undetermined"
    out = {"per_item_order": per, "mean_s_own": float(est[0]), "mean_s_own_minus_other": float(est[1]),
           "contrast_item_orders": contrast, "contrast_mean_diff": float(est[2]), "contrast_s_own_positive": int(maj),
           "ci95": lohi.tolist(), "reading": reading, "n_conversations": len(own), "cost_usd": sum(v["cost"] for v in own.values()),
           "echo_rate_mean": float(np.mean([v["echo_rate"] for v in per.values()]))}
    (config.RESULTS / "bm1-serial-dependence.json").write_text(json.dumps(out, indent=1))
    f = lambda i: f"{est[i]:+.2f} [{lohi[0][i]:+.2f}, {lohi[1][i]:+.2f}]"
    lines = ["# Biomimetic (rev. 2 §§3.0–3.2): source dependence, run 3's anchors as the model's own earlier answer", "",
             "Pre-registered in `experiments/bm1-serial-dependence.md` (D44), committed before any call. 16 items × 4 cells × 40, "
             f"`claude-haiku-5-5`, thinking disabled, one scale direction. {out['n_conversations']} conversations, "
             f"**${out['cost_usd']:.2f}** of the $0.40 cap; no refusal. Comparison: run 3's archived \"another person\" cells.", "", PLAIN,
             "## Slope of the re-rating r₁ on the shown value A", "",
             "s = [mean r₁(high) − mean r₁(low)] / (A_high − A_low): 1 = takes the value fully, 0 = ignores it, < 0 = moves away. "
             "95% item-cluster bootstrap CIs.", "",
             f"- **Mean s_own (planted as its own answer): {f(0)}**.",
             f"- Mean s_other (run 3, \"another person\"): {f(3)}.",
             f"- **Mean s_own − s_other: {f(1)}**.",
             f"- Descriptive: contrast item-orders (s_other < 0 in run 3): {len(contrast)}; mean s_own − s_other there {f(2)}; s_own > 0 on "
             f"{maj} of {len(contrast)}.",
             f"- Share of re-ratings that repeat the planted value exactly: {out['echo_rate_mean']:.0%} (mean over item-orders).", "",
             "| item-order | s_own | s_other (run 3) | echo rate | mean r₂, own / other |", "|---|---|---|---|---|"]
    for k, v in per.items():
        lines.append(f"| {k} | {v['s_own']:+.2f} | {v['s_other']:+.2f} | {v['echo_rate']:.0%} | {v['r2_own']:.2f} / {v['r2_other']:.2f} |")
    lines += ["", f"## Pre-registered reading: **{reading}**"]
    (config.RESULTS / "bm1-serial-dependence.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines[:18] + lines[-1:]))


if __name__ == "__main__":
    which, analyse_only = sys.argv[1], "--analyse" in sys.argv
    if which == "bm2":
        if not analyse_only:
            bm2_run()
        bm2_analyse()
    else:
        if not analyse_only:
            bm1_run()
        bm1_analyse()

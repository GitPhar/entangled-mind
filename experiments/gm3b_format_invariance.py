"""Gold-map direction 3: six elicitation formats on the 160 chain claims, as pre-registered in
experiments/gm3b-format-invariance.md (D38). $1 cap; any refusal stops the run.

    python experiments/gm3b_format_invariance.py            # run (cached), then analyse
    python experiments/gm3b_format_invariance.py --analyse  # analysis only

Calls cached in results/gm3b-calls.json. Writes results/gm3b-format-invariance.{json,md}."""

import json
import math
import sys

import numpy as np
from scipy.optimize import minimize
from scipy.special import expit, log_expit
from scipy.stats import kendalltau, spearmanr

import exp5_run as er
from entangled_mind import config
from gm_common import PLAIN, Caller, structured

CACHE = config.RESULTS / "gm3b-calls.json"
OUT_JSON, OUT_MD = config.RESULTS / "gm3b-format-invariance.json", config.RESULTS / "gm3b-format-invariance.md"
R, CAP, BOOT_SEED, PRIOR_SD = 10, 1.0, 3131, 3.0
FORMATS = ["F1", "F2", "F3", "F4", "F5", "F6"]
NAMES = {"F1": "rating 0-100", "F2": "yes/no", "F3": "bet", "F4": "pairwise vs coin", "F5": "frequency /100", "F6": "verbal 7-point"}
VERBAL = ["certainly false", "very unlikely", "unlikely", "as likely as not", "likely", "very likely", "certainly true"]
PRICES = [10, 30, 50, 70, 90]
YN = {"type": "object", "properties": {"answer": {"type": "string", "enum": ["yes", "no"]}}, "required": ["answer"], "additionalProperties": False}
AB = {"type": "object", "properties": {"answer": {"type": "string", "enum": ["A", "B"]}}, "required": ["answer"], "additionalProperties": False}
INT = lambda f: {"type": "object", "properties": {f: {"type": "integer"}}, "required": [f], "additionalProperties": False}
VB = {"type": "object", "properties": {"answer": {"type": "string", "enum": VERBAL}}, "required": ["answer"], "additionalProperties": False}
STATEMENT, COIN = "This statement is true.", "A fair coin, tossed once, lands heads."


def stmt_first(r):
    return r % 4 in (0, 1)


def prompt(rec, k, fmt, r):
    head = (f'Consider this statement, which came up in a discussion of the question "{rec["question"]}":\n\n'
            f'"{rec["contentions"][k]["text"]}"\n\n')
    if fmt == "F1":
        return head + ("How likely is it that this statement is true? Give an integer from 0 to 100, where 0 = certainly false "
                       "and 100 = certainly true."), INT("rating")
    if fmt == "F2":
        return head + "Is this statement true? Answer yes or no.", YN
    if fmt == "F3":
        return head + (f"A ticket pays $100 if this statement is true and nothing if it is false. The ticket costs "
                       f"${PRICES[r // 2]}. Would you buy it? Answer yes or no."), YN
    if fmt == "F4":
        a, b = (STATEMENT, COIN) if stmt_first(r) else (COIN, STATEMENT)
        return head + f"Which is more likely? (A) {a} (B) {b} Answer A or B.", AB
    if fmt == "F5":
        return head + ("Think of 100 statements like this one, about each of which you have the same evidence as you have "
                       "about this one. How many of the 100 would be true? Give an integer from 0 to 100."), INT("count")
    return head + ("How likely is it that this statement is true? Choose one: " + ", ".join(VERBAL) + "."), VB


def claims():
    split = json.loads(er.SPLIT.read_text())
    return [(q, k) for q in split["candidates"] for k in split["chain_claims"][q]]


def run():
    recs = {r["id"]: r for r in json.loads(er.POOL.read_text())["records"]}
    c = Caller(CACHE, CAP, "direction 3 formats")

    def call(job):
        _, q, k, fmt, r = job
        text, schema = prompt(recs[q], k, fmt, r)
        d, _, cost, rid = structured(er.MODEL, [{"role": "user", "content": text}], schema, "gm3b", max_tokens=100)
        return {"value": next(iter(d.values())), "cost": cost, "request_id": rid}
    jobs = [(f"{q}|{k}|{fmt}|{r}", q, k, fmt, r) for q, k in claims() for fmt in FORMATS for r in range(R)]
    c.run(jobs, call, workers=8)


# --- data -----------------------------------------------------------------------

def encode(conv):
    """Observation arrays per format: claim index, repeat, response (and covariate)."""
    cl = claims()
    obs = {f: {"c": [], "r": [], "y": [], "x": []} for f in FORMATS}
    for ci, (q, k) in enumerate(cl):
        for fmt in FORMATS:
            for r in range(R):
                v = conv.get(f"{q}|{k}|{fmt}|{r}")
                if v is None:
                    continue
                v = v["value"]
                if fmt in ("F1", "F5"):
                    y, x = math.log((min(100, max(0, v)) + 1) / (101 - min(100, max(0, v)))), 0.0
                elif fmt == "F2":
                    y, x = float(v == "yes"), 0.0
                elif fmt == "F3":
                    p = PRICES[r // 2] / 100
                    y, x = float(v == "yes"), math.log(p / (1 - p))
                elif fmt == "F4":
                    chose_stmt = (v == "A") == stmt_first(r)
                    y, x = float(chose_stmt), 1.0 if stmt_first(r) else -1.0
                else:
                    y, x = float(VERBAL.index(v)), 0.0
                for key, val in (("c", ci), ("r", r), ("y", y), ("x", x)):
                    obs[fmt][key].append(val)
    return {f: {k: np.asarray(v, float if k in ("y", "x") else int) for k, v in d.items()} for f, d in obs.items()}, len(cl)


# --- models ---------------------------------------------------------------------
# link parameters theta per format: F1 (log sigma), F5 (a, log b, log sigma), F2 (a, log b), F3 (a, log b),
# F4 (a, log b, d), F6 (a, log b, kappa_1, log increments x5). In L1, F1's a = 0, b = 1. In L6 every a = 0, b = 1.

LINK_SIZES = {"F1": 1, "F2": 2, "F3": 2, "F4": 3, "F5": 3, "F6": 8}


def unpack(theta, single):
    out, i = {}, 0
    for f in FORMATS:
        n = LINK_SIZES[f]
        t = theta[i:i + n]
        i += n
        p = {}
        if f == "F1":
            p.update(a=0.0, b=1.0, s=math.exp(t[0]))
        else:
            p.update(a=t[0] if single else 0.0, b=math.exp(t[1]) if single else 1.0)
            if f == "F5":
                p["s"] = math.exp(t[2])
            if f == "F4":
                p["d"] = t[2]
            if f == "F6":
                p["k"] = np.cumsum(np.concatenate([[t[2]], np.exp(t[3:8])]))
        out[f] = p
    return out


def theta0():
    t = []
    for f in FORMATS:
        if f == "F1":
            t += [0.0]
        elif f == "F6":
            t += [0.0, 0.0, -3.0] + [0.0] * 5
        else:
            t += [0.0, 0.0] + ([0.0] if f in ("F4", "F5") else [])
    return np.array(t)


def ll_obs(f, p, mu, d):
    """Per-observation log-likelihood given latent values mu (array aligned with d)."""
    eta = p["a"] + p["b"] * mu
    if f in ("F1", "F5"):
        return -0.5 * ((d["y"] - eta) / p["s"]) ** 2 - math.log(p["s"]) - 0.5 * math.log(2 * math.pi)
    if f == "F2":
        return d["y"] * log_expit(eta) + (1 - d["y"]) * log_expit(-eta)
    if f == "F3":
        e = p["a"] + p["b"] * (mu - d["x"])
        return d["y"] * log_expit(e) + (1 - d["y"]) * log_expit(-e)
    if f == "F4":
        e = eta + p["d"] * d["x"]
        return d["y"] * log_expit(e) + (1 - d["y"]) * log_expit(-e)
    k = np.concatenate([[-np.inf], p["k"], [np.inf]])
    y = d["y"].astype(int)
    hi, lo = expit(k[y + 1] - eta), expit(k[y] - eta)
    return np.log(np.clip(hi - lo, 1e-300, None))


def subset(d, mask):
    return {k: v[mask] for k, v in d.items()}


def fit(obs, n_claims, single, train_mask_fn, rounds=40):
    """Block coordinate ascent. Latents: mu[c] (single) or mu[c, f] (per format)."""
    tr = {f: subset(d, train_mask_fn(d)) for f, d in obs.items()}
    mu = np.zeros(n_claims) if single else np.zeros((n_claims, len(FORMATS)))
    theta = theta0()

    def latent_vec(f, d, m):
        return m[d["c"]] if single else m[d["c"], FORMATS.index(f)]

    def objective(th, m):
        p = unpack(th, single)
        tot = sum(ll_obs(f, p[f], latent_vec(f, tr[f], m), tr[f]).sum() for f in FORMATS)
        return tot - 0.5 * (m ** 2).sum() / PRIOR_SD ** 2

    def mu_step(th, m):
        p = unpack(th, single)
        lo, hi = np.full(m.shape, -15.0), np.full(m.shape, 15.0)
        g = (math.sqrt(5) - 1) / 2

        def per_unit(x):
            tot = np.zeros(m.shape)
            for f in FORMATS:
                d = tr[f]
                if not len(d["c"]):
                    continue
                v = ll_obs(f, p[f], latent_vec(f, d, x), d)
                if single:
                    np.add.at(tot, d["c"], v)
                else:
                    np.add.at(tot[:, FORMATS.index(f)], d["c"], v)
            return tot - 0.5 * x ** 2 / PRIOR_SD ** 2
        c1, c2 = hi - g * (hi - lo), lo + g * (hi - lo)
        f1, f2 = per_unit(c1), per_unit(c2)
        for _ in range(70):
            left = f1 > f2
            hi = np.where(left, c2, hi)
            lo = np.where(left, lo, c1)
            c2n = np.where(left, c1, lo + g * (hi - lo))
            c1n = np.where(left, hi - g * (hi - lo), c2)
            c1, c2 = c1n, c2n
            f1, f2 = per_unit(c1), per_unit(c2)
        return (lo + hi) / 2

    prev = -np.inf
    for _ in range(rounds):
        mu = mu_step(theta, mu)
        theta = minimize(lambda th: -objective(th, mu), theta, method="L-BFGS-B").x
        cur = objective(theta, mu)
        if abs(cur - prev) < 1e-6:
            break
        prev = cur
    return theta, mu


def heldout_ll(obs, n_claims, single, theta, mu, test_mask_fn):
    p = unpack(theta, single)
    per = np.zeros((n_claims, len(FORMATS)))
    for fi, f in enumerate(FORMATS):
        d = subset(obs[f], test_mask_fn(obs[f]))
        m = mu[d["c"]] if single else mu[d["c"], fi]
        np.add.at(per[:, fi], d["c"], ll_obs(f, p[f], m, d))
    return per


def analyse():
    conv = json.loads(CACHE.read_text())
    obs, nc = encode(conv)
    folds = [(lambda d: d["r"] % 2 == 0, lambda d: d["r"] % 2 == 1), (lambda d: d["r"] % 2 == 1, lambda d: d["r"] % 2 == 0)]
    ll = {True: np.zeros((nc, 6)), False: np.zeros((nc, 6))}
    fits = {}
    for single in (True, False):
        for fi, (trn, tst) in enumerate(folds):
            th, mu = fit(obs, nc, single, trn)
            ll[single] += heldout_ll(obs, nc, single, th, mu, tst)
            fits[f"{'L1' if single else 'L6'}_fold{fi}"] = {"links": {f: {k: (v.tolist() if isinstance(v, np.ndarray) else float(v))
                                                                           for k, v in pp.items()} for f, pp in unpack(th, single).items()}}
    dll = (ll[False] - ll[True]).sum(axis=1)
    cl = claims()
    items = sorted({q for q, _ in cl})
    by_item = {q: [i for i, (qq, _) in enumerate(cl) if qq == q] for q in items}
    rng = np.random.default_rng(BOOT_SEED)
    boots = [np.mean(np.concatenate([dll[by_item[q]] for q in rng.choice(items, len(items))])) for _ in range(2000)]
    lo, hi = np.percentile(boots, [2.5, 97.5])
    share = float(np.mean(dll > 0))
    # descriptives: per-claim mean response on a common probability-like scale
    means = np.full((nc, 6), np.nan)
    for fi, f in enumerate(FORMATS):
        d = obs[f]
        for c in range(nc):
            y = d["y"][d["c"] == c]
            if len(y):
                means[c, fi] = y.mean() if f not in ("F1", "F5") else np.mean(1 / (1 + np.exp(-y)))
    sp = {f"{FORMATS[i]}-{FORMATS[j]}": float(spearmanr(means[:, i], means[:, j], nan_policy="omit").statistic)
          for i in range(6) for j in range(i + 1, 6)}
    rank = np.argsort(np.argsort(np.nan_to_num(means), axis=0), axis=0).astype(float)
    m_ = 6
    S = ((rank.sum(axis=1) - m_ * (nc - 1) / 2) ** 2).sum()
    W = float(12 * S / (m_ ** 2 * (nc ** 3 - nc)))
    disc = {}
    for fi, f in enumerate(FORMATS[1:], start=1):
        tau = kendalltau(means[:, 0], means[:, fi], nan_policy="omit").statistic
        disc[f] = float((1 - tau) / 2)          # share of discordant claim pairs (ignoring ties' correction)
    if share > 0.5 and lo > 0:
        reading = "no single credence: formats disagree beyond monotone links"
    elif hi < 0 or (lo <= 0 <= hi and share <= 0.5):
        reading = "one credence suffices (a uniformity pass)"
    else:
        reading = "mixed"
    res = {"n_claims": nc, "n_calls": len(conv), "cost_usd": sum(v["cost"] for v in conv.values()),
           "dLL": {"mean": float(dll.mean()), "ci95": [float(lo), float(hi)], "share_positive": share,
                   "by_format_mean": {f: float((ll[False][:, i] - ll[True][:, i]).mean()) for i, f in enumerate(FORMATS)},
                   "total_L1": float(ll[True].sum()), "total_L6": float(ll[False].sum())},
           "spearman": sp, "kendall_W": W, "discordant_vs_F1": disc, "fits": fits, "per_claim_dLL": dll.tolist(),
           "format_means": means.tolist(), "reading": reading}
    OUT_JSON.write_text(json.dumps(res, indent=1))
    write_md(res)


def write_md(r):
    d = r["dLL"]
    lines = ["# Direction 3: six elicitation formats on the 160 chain claims", "",
             "Pre-registered in `experiments/gm3b-format-invariance.md` (D38), committed before any call. `claude-haiku-5-5`, thinking "
             f"disabled; one scale direction throughout. {r['n_calls']} calls, **${r['cost_usd']:.2f}** of the $1 cap; no refusal.", "", PLAIN,
             "## One credence (L1) against one credence per format (L6), held-out repeats", "",
             "ΔLL = held-out log-likelihood of L6 minus L1, per claim, summed over 2 folds (even/odd repeats) and six formats. "
             "Positive favours format-specific credences.", "",
             f"- **Mean ΔLL per claim: {d['mean']:+.2f} [{d['ci95'][0]:+.2f}, {d['ci95'][1]:+.2f}]** (item-bootstrap 95% CI).",
             f"- **Claims with ΔLL > 0: {d['share_positive']:.0%}** of {r['n_claims']}.",
             f"- Total held-out LL: L1 {d['total_L1']:.1f}, L6 {d['total_L6']:.1f}.", "",
             "| format | mean ΔLL per claim | L1 slope b_f (fold 0) |", "|---|---|---|"]
    links = r["fits"]["L1_fold0"]["links"]
    for f in FORMATS:
        lines.append(f"| {f} {NAMES[f]} | {d['by_format_mean'][f]:+.3f} | {links[f]['b']:.2f} |")
    lines += ["", "## Agreement between formats (per-claim mean responses)", "",
              f"- Kendall's W across the six formats: **{r['kendall_W']:.2f}**.", "",
              "| pair | Spearman ρ |", "|---|---|"]
    for k, v in r["spearman"].items():
        a, b = k.split("-")
        lines.append(f"| {NAMES[a]} – {NAMES[b]} | {v:+.2f} |")
    lines += ["", "| format | (1 − τ_b)/2 against the 0–100 rating (a discordance index, not a share of pairs) |", "|---|---|"]
    for f, v in r["discordant_vs_F1"].items():
        lines.append(f"| {NAMES[f]} | {v:.0%} |")
    lines += ["", f"## Pre-registered reading: **{r['reading']}**"]
    OUT_MD.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    if "--md-only" in sys.argv:
        write_md(json.loads(OUT_JSON.read_text()))
    else:
        if "--analyse" not in sys.argv:
            run()
        analyse()

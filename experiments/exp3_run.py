"""Experiment 3, run 1: order effects, as pre-registered in experiments/exp3-order-effects.md.

    python experiments/exp3_run.py

For 40 run-2 test items (20 wrong + 20 right, seed 3): predict each related
pair's order effect from arm A's state (quantum, Delta_Q) and from the
classical twin's sequential heat-bath update (Delta_F); query the base model
with the chosen pairs as preceding statements in both orders; and compare.
Conversations are cached in results/exp3-conversations.json. On any refusal the
run stops at once and records the request ID; nothing is retried.

Writes results/exp3-run-1.{json,md}."""

import json
import math
import random
import re
import sys
import threading
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from dotenv import load_dotenv

from entangled_mind import config, llm, v2

load_dotenv(config.ROOT / ".env")
POOL = config.RESULTS / "pool-run-3.json"
CONV = config.RESULTS / "exp3-conversations.json"
OUT_JSON = config.RESULTS / "exp3-run-1.json"
OUT_MD = config.RESULTS / "exp3-run-1.md"
BUDGET_USD = 10.0
R = 5
GAMMA0 = config.GAMMA0
CLAIM_PROMPT = "Consider this statement: '{claim}'. Do you think it is true? Answer in one sentence."


# --- predictions -------------------------------------------------------------

def x_basis_state(it):
    """Arm A's pre-readout state, written in the yes/no (X) basis: index bit 0 = yes-aligned."""
    psi = v2.fast_quantum_state(it, 1.0, 1.0, 1.0, config.N_TROTTER, config.GAMMA0, config.BETA0)
    return v2._all(psi, it.n, v2.H)


def apply_consider(phi_x, it, web, k):
    """U_k = exp(-i g H_k), H_k = -sum_j J_kj X_k X_j - lean_k X_k - Z_k, applied in the X basis.
    X terms are diagonal there (x = +1 for bit 0); -Z_k flips bit k. For each configuration of the
    other qubits, H_k on qubit k is -c * sz - sx with c = lean_k + sum_j J_kj x_j."""
    n = it.n
    x = 1 - 2 * v2.bits(n)
    c = np.full(2 ** n, web.lean[k], float)
    for i, j, J in web.edges:
        if i == k:
            c += J * x[:, j]
        elif j == k:
            c += J * x[:, i]
    idx = np.arange(2 ** n)
    lo = idx[(idx >> k) & 1 == 0]           # bit k = 0 (yes); partner has bit k = 1
    hi = lo | (1 << k)
    cc = c[lo]                              # c does not depend on bit k
    a, b = phi_x[lo], phi_x[hi]
    w = np.sqrt(cc ** 2 + 1)
    cos, sin = np.cos(GAMMA0 * w), np.sin(GAMMA0 * w)
    # exp(i g (c sz + sx)) = cos(g w) I + i sin(g w) (c sz + sx) / w
    na = cos * a + 1j * sin * (cc * a + b) / w
    nb = cos * b + 1j * sin * (a - cc * b) / w
    out = phi_x.copy()
    out[lo], out[hi] = na, nb
    return out


def p_yes(probs, it):
    m = (1 - 2 * v2.bits(it.n)) @ v2.weights(it)
    return float(probs[m > 0].sum() + 0.5 * probs[m == 0].sum())


def delta_quantum(it, web, base_x, i, j):
    a = apply_consider(apply_consider(base_x, it, web, i), it, web, j)
    b = apply_consider(apply_consider(base_x, it, web, j), it, web, i)
    return abs(p_yes(np.abs(a) ** 2, it) - p_yes(np.abs(b) ** 2, it))


def classical_prior(it, web):
    phi = v2.solve_phases_fast(web)
    theta = np.clip(it.conf, 0, 2) * math.pi / 2
    py = np.clip((1 + np.sin(theta) * np.cos(phi)) / 2, 1e-12, 1 - 1e-12)
    b = v2.bits(it.n)
    return np.prod(np.where(b == 0, py, 1 - py), axis=1)


def heat_bath(p, it, web, k, T=1.0):
    n = it.n
    x = 1 - 2 * v2.bits(n)
    local = np.full(2 ** n, web.lean[k], float)
    for i, j, J in web.edges:
        if i == k:
            local += J * x[:, j]
        elif j == k:
            local += J * x[:, i]
    p_up = 1 / (1 + np.exp(-2 * local / T))
    marg = p + p[np.arange(2 ** n) ^ (1 << k)]
    return np.where(x[:, k] == 1, p_up, 1 - p_up) * marg


def delta_classical(it, web, prior, i, j):
    a = heat_bath(heat_bath(prior, it, web, i), it, web, j)
    b = heat_bath(heat_bath(prior, it, web, j), it, web, i)
    return abs(p_yes(a, it) - p_yes(b, it))


def choose_pairs(rec):
    it = v2.item_from_record(rec)
    web = v2.coupled_web(it, 1.0, 1.0)
    base_x, prior = x_basis_state(it), classical_prior(it, web)
    pairs = [(i, j) for i, j, _ in web.edges]
    dq = {p: delta_quantum(it, web, base_x, *p) for p in pairs}
    df = {p: delta_classical(it, web, prior, *p) for p in pairs}
    by_q = sorted(pairs, key=lambda p: (dq[p], p))
    by_f = sorted(pairs, key=lambda p: (df[p], p))
    chosen = []
    for p in by_q[-2:][::-1] + by_q[:2]:
        if p not in chosen:
            chosen.append(p)
    for p in (by_f[-1], by_f[0]):
        if p not in chosen:
            chosen.append(p)
    tags = {p: [] for p in chosen}
    for p in by_q[-2:]:
        tags[p].append("Q-high")
    for p in by_q[:2]:
        tags[p].append("Q-low")
    tags[by_f[-1]].append("F-high")
    tags[by_f[0]].append("F-low")
    return [{"pair": list(p), "dq": dq[p], "df": df[p], "tags": tags[p]} for p in chosen]


# --- conversations -------------------------------------------------------------

def converse(turns: list[str]):
    """Run one conversation; earlier assistant content is passed back unchanged. Returns (answer, cost, request ids)."""
    msgs, cost, rids, text = [], 0.0, [], ""
    for t in turns:
        msgs.append({"role": "user", "content": t})
        resp = llm.client().messages.create(model="claude-haiku-5-5", max_tokens=16000,
                                            thinking={"type": "adaptive", "display": "omitted"}, messages=msgs)
        llm._check_stop(resp, "exp3")
        u = llm._usage(resp)
        cost += u.cost
        rids.append(getattr(resp, "_request_id", None))
        msgs.append({"role": "assistant", "content": resp.content})
        text = "\n".join(b.text for b in resp.content if b.type == "text")
    m = re.findall(r"FINAL ANSWER:\s*(YES|NO)", text, flags=re.I)
    return (m[-1].lower() if m else None), cost, rids


def main() -> None:
    pool = json.loads(POOL.read_text())
    recs = {r["id"]: r for r in pool["records"]}
    s = pool["split"]
    rng = random.Random(3)
    items = sorted(rng.sample(s["test_wrong"], 20)) + sorted(rng.sample(s["test_right"], 20))
    plan = {q: choose_pairs(recs[q]) for q in items}
    jobs = []
    for q in items:
        cs = recs[q]["contentions"]
        final = llm.BASE_PROMPT.format(question=recs[q]["question"])
        for rep in range(R):
            jobs.append((f"{q}|base|{rep}", [final]))
        for pr in plan[q]:
            i, j = pr["pair"]
            for first, second, tag in ((i, j, "ij"), (j, i, "ji")):
                for rep in range(R):
                    jobs.append((f"{q}|{i}-{j}|{tag}|{rep}",
                                 [CLAIM_PROMPT.format(claim=cs[first]["text"]),
                                  CLAIM_PROMPT.format(claim=cs[second]["text"]), final]))
    cache = json.loads(CONV.read_text()) if CONV.exists() else {}
    lock, stop, refusal = threading.Lock(), threading.Event(), {}

    def work(job):
        key, turns = job
        if key in cache or stop.is_set():
            return
        with lock:
            if sum(v["cost"] for v in cache.values()) >= BUDGET_USD:
                stop.set()
                return
        try:
            ans, cost, rids = converse(turns)
        except llm.RefusalError as e:
            refusal.setdefault("e", (key, e))
            stop.set()
            return
        with lock:
            cache[key] = {"answer": ans, "cost": cost, "request_ids": rids}
            if len(cache) % 50 == 0:
                CONV.write_text(json.dumps(cache))
                print(f"{len(cache)}/{len(jobs)} conversations, ${sum(v['cost'] for v in cache.values()):.2f}", flush=True)

    with ThreadPoolExecutor(max_workers=6) as ex:
        list(ex.map(work, jobs))
    CONV.write_text(json.dumps(cache))
    if refusal:
        key, e = refusal["e"]
        (config.RESULTS / "refusal.md").write_text(
            f"# Pipeline stopped on a refusal\n\nExperiment 3, conversation `{key}`\n\nRefused call: **{e.call}**\n\n"
            f"Request ID: `{e.request_id}`\n\nExact stop details:\n\n```\n{e.stop_details}\n```\n\nNothing was reworded or retried.\n")
        sys.exit(f"STOPPED: {e}")
    if len(cache) < len(jobs):
        sys.exit(f"budget stop: {len(cache)}/{len(jobs)} conversations done")
    analyse(items, plan, recs, cache)


def spearman(a, b):
    def rank(v):
        v = np.asarray(v, float)
        r = np.empty(len(v))
        r[v.argsort()] = np.arange(len(v))
        for x in np.unique(v):
            r[v == x] = r[v == x].mean()
        return r
    ra, rb = rank(a), rank(b)
    return float(np.corrcoef(ra, rb)[0, 1]) if ra.std() and rb.std() else float("nan")


def analyse(items, plan, recs, cache) -> None:
    rows = []
    def py(keys):
        a = [cache[k]["answer"] for k in keys if cache[k]["answer"] is not None]
        return (sum(x == "yes" for x in a) / len(a)) if a else float("nan"), len(a)
    for q in items:
        for pr in plan[q]:
            i, j = pr["pair"]
            pij, nij = py([f"{q}|{i}-{j}|ij|{r}" for r in range(R)])
            pji, nji = py([f"{q}|{i}-{j}|ji|{r}" for r in range(R)])
            ans_ij = [cache[f"{q}|{i}-{j}|ij|{r}"]["answer"] for r in range(R)]
            ans_ji = [cache[f"{q}|{i}-{j}|ji|{r}"]["answer"] for r in range(R)]
            rows.append({"item": q, "wrong": not recs[q]["correct"], "pair": [i, j], "tags": pr["tags"],
                         "dq": pr["dq"], "df": pr["df"], "p_yes_ij": pij, "p_yes_ji": pji,
                         "observed": abs(pij - pji), "answers_ij": ans_ij, "answers_ji": ans_ji})
    base = {q: py([f"{q}|base|{r}" for r in range(R)])[0] for q in items}
    rows = [r for r in rows if not math.isnan(r["observed"])]
    obs = np.array([r["observed"] for r in rows])
    dq, df = np.array([r["dq"] for r in rows]), np.array([r["df"] for r in rows])
    rho_q, rho_f = spearman(dq, obs), spearman(df, obs)
    # primary: bootstrap over items
    rng = np.random.default_rng(11)
    by_item = {}
    for k, r in enumerate(rows):
        by_item.setdefault(r["item"], []).append(k)
    keys = list(by_item)
    diffs = []
    for _ in range(2000):
        idx = [k for q in rng.choice(keys, len(keys)) for k in by_item[q]]
        a, b = spearman(dq[idx], obs[idx]), spearman(df[idx], obs[idx])
        if not (math.isnan(a) or math.isnan(b)):
            diffs.append(a - b)
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    primary = "pass" if lo > 0 else ("fail" if hi < 0 else "inconclusive")
    # secondary 1: do order effects exist? permute order labels within each pair
    def mean_oe(rs):
        return float(np.mean([abs(np.mean([a == "yes" for a in r["answers_ij"] if a]) -
                                  np.mean([a == "yes" for a in r["answers_ji"] if a])) for r in rs]))
    observed_mean = mean_oe(rows)
    null = []
    for _ in range(2000):
        perm = []
        for r in rows:
            pool_ = [a for a in r["answers_ij"] + r["answers_ji"] if a]
            rng.shuffle(pool_)
            h = len([a for a in r["answers_ij"] if a])
            perm.append({"answers_ij": pool_[:h], "answers_ji": pool_[h:]})
        null.append(mean_oe([p for p in perm if p["answers_ij"] and p["answers_ji"]]))
    p_exist = (1 + sum(v >= observed_mean for v in null)) / (len(null) + 1)
    # secondary 2: Q-high vs Q-low within item (sign-flip permutation)
    d_item = []
    for q in keys:
        hi_ = [rows[k]["observed"] for k in by_item[q] if "Q-high" in rows[k]["tags"]]
        lo_ = [rows[k]["observed"] for k in by_item[q] if "Q-low" in rows[k]["tags"]]
        if hi_ and lo_:
            d_item.append(np.mean(hi_) - np.mean(lo_))
    d_item = np.array(d_item)
    flips = [np.mean(d_item * rng.choice([-1, 1], len(d_item))) for _ in range(10000)]
    p_hl = (1 + sum(f >= d_item.mean() for f in flips)) / (len(flips) + 1)
    total_cost = sum(v["cost"] for v in cache.values())
    res = {"items": items, "rows": rows, "baseline_p_yes": base, "rho_quantum": rho_q, "rho_classical": rho_f,
           "rho_diff_ci95": [float(lo), float(hi)], "primary": primary, "mean_observed_order_effect": observed_mean,
           "order_effect_exists_p": p_exist, "q_high_minus_low_mean": float(d_item.mean()), "q_high_low_p": p_hl,
           "n_conversations": len(cache), "cost_usd": total_cost}
    OUT_JSON.write_text(json.dumps(res, indent=1))
    lines = ["# Experiment 3, run 1: order effects", "",
             "Pre-registration: `experiments/exp3-order-effects.md`. Base model `claude-haiku-5-5`. "
             f"{len(items)} items from the run-2 test set (20 wrong + 20 right, seed 3), {len(rows)} item-pairs, "
             f"{R} conversations per pair and order, {len(cache)} conversations in all, **${total_cost:.2f}**.", "",
             "## Primary: which model predicts the observed order effects?", "",
             f"- Spearman ρ(quantum prediction Δᴼ, observed order effect) = **{rho_q:.3f}**",
             f"- Spearman ρ(classical-twin prediction Δᶠ, observed order effect) = **{rho_f:.3f}**",
             f"- ρᴼ − ρᶠ, 95% bootstrap over items: [{lo:+.3f}, {hi:+.3f}] → **{primary.upper()}**", "",
             "## Secondary", "",
             f"- Do order effects exist at all? Mean observed |P(yes | i first) − P(yes | j first)| = {observed_mean:.3f}; "
             f"order-label permutation test p = {p_exist:.3f}.",
             f"- Do the two largest-Δᴼ pairs show larger observed effects than the two smallest? Mean within-item difference "
             f"{d_item.mean():+.3f} over {len(d_item)} items; sign-flip permutation p = {p_hl:.3f}.", "",
             "## Item-pairs", "", "| item | wrong? | pair | tags | Δᴼ | Δᶠ | P(yes) i first | P(yes) j first | observed |",
             "|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['item']} | {'yes' if r['wrong'] else ''} | {r['pair'][0]}–{r['pair'][1]} | {', '.join(r['tags'])} | "
                     f"{r['dq']:.4f} | {r['df']:.4f} | {r['p_yes_ij']:.2f} | {r['p_yes_ji']:.2f} | {r['observed']:.2f} |")
    OUT_MD.write_text("\n".join(lines) + "\n")
    print("\n".join(lines[:16]))


if __name__ == "__main__":
    main()

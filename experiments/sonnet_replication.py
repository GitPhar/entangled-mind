"""Second base model: does the error-prediction pattern replicate on claude-sonnet-5-5?

    python experiments/sonnet_replication.py             # full (makes arm-G calls to Sonnet)
    python experiments/sonnet_replication.py --offline   # L, H, A2, F2 only on the archived hard pool; no API calls

Scores G (Sonnet's self-reported confidence; one call per item), L, H, and the already-fitted
A2 and F2 (frozen v2 parameters from results/v2-fit.json; nothing is refitted) on Sonnet's
items from pool run 4 (hard pool) and pool run 6 (training pool). Haiku's v2 numbers are
shown alongside. Writes results/sonnet-replication.{md,json}. On any refusal it stops."""

import json
import os
import sys
from multiprocessing import Pool

import numpy as np

import v2_fit as vf
from entangled_mind import config, v2

POOL4 = config.RESULTS / "pool-run-4.json"
POOL6 = config.RESULTS / "pool-run-6.json"
G_CACHE = config.RESULTS / "sonnet-arm-g-confidence.json"
OUT_JSON = config.RESULTS / "sonnet-replication.json"
OUT_MD = config.RESULTS / "sonnet-replication.md"
G_BUDGET_USD = 3.0


def main() -> None:
    fitd = json.loads(vf.FIT.read_text())
    haiku = json.loads(vf.OUT_JSON.read_text())["results"]
    split = json.loads(vf.SPLIT.read_text())
    test = set(split["test"])
    r4 = [r for r in json.loads(POOL4.read_text())["records"] if r["correct"] is not None]
    r6 = [r for r in json.loads(POOL6.read_text())["records"] if r["correct"] is not None] if POOL6.exists() else []
    sets = {"hard pool": r4,
            "v2 locked-test questions": [r for r in r6 if r["id"] in test],
            "other training-pool questions": [r for r in r6 if r["id"] not in test]}
    config.BASE_MODEL = "claude-sonnet-5-5"
    g_cache = json.loads(G_CACHE.read_text()) if G_CACHE.exists() else {}
    spent = sum(v["usage"]["cost_usd"] for v in g_cache.values())
    results = {}
    for name, recs in sets.items():
        if not recs or not any(r["correct"] is False for r in recs):
            results[name] = {"n": len(recs), "n_wrong": sum(r["correct"] is False for r in recs), "skipped": "no wrong items"}
            continue
        by_id = {r["id"]: r for r in recs}
        ids = [r["id"] for r in recs]
        # G calls, cached, within the arm-G budget
        todo = [q for q in ids if q not in g_cache]
        if todo and spent < G_BUDGET_USD:
            vf.arm_g(by_id, todo, G_CACHE)
            g_cache = json.loads(G_CACHE.read_text())
            spent = sum(v["usage"]["cost_usd"] for v in g_cache.values())
        ids = [q for q in ids if q in g_cache]          # items G could be scored on
        items = vf.load_items(ids, by_id)
        y = np.array([i.wrong for i in items])
        scores = {}
        with Pool(min(8, os.cpu_count()), initializer=vf._init, initargs=(items,)) as pool:
            for model in ("A2", "F2", "L"):
                m = fitd["models"][model]
                kw = {"feat_mu": np.array(m["feature_mu"]), "feat_sd": np.array(m["feature_sd"])} if model == "L" else {}
                scores[model] = vf.ParallelScorer(model, items, pool, **kw).scores(np.array(m["final"]["params"]))
        scores["G"] = np.array([100 - g_cache[q]["confidence"] for q in ids], float)
        scores["H"] = np.array([v2.hedge_scores(i)[0] for i in items])
        res = {"n": len(ids), "n_wrong": int(y.sum()), "models": {}}
        for m, sc in scores.items():
            p, lo, hi = vf.boot(list(sc[y]), list(sc[~y]))
            res["models"][m] = {"auroc": p, "ci95": [lo, hi]}
        res["A2_minus_F2"] = vf.paired_diff(scores["A2"], scores["F2"], y)
        res["G_minus_L"] = vf.paired_diff(scores["G"], scores["L"], y)
        results[name] = res
    OUT_JSON.write_text(json.dumps({"results": results, "g_cost_usd": spent}, indent=1))
    write_md(results, haiku, spent)


def arm_g_hard_pool() -> None:
    """D28: Sonnet's self-confidence on its 298 hard-pool answers. $2 cap; stop on any refusal."""
    import threading
    from concurrent.futures import ThreadPoolExecutor
    from entangled_mind import llm
    config.BASE_MODEL = "claude-sonnet-5-5"
    recs = [r for r in json.loads(POOL4.read_text())["records"] if r["correct"] is not None]
    cache = json.loads(G_CACHE.read_text()) if G_CACHE.exists() else {}
    lock, stop, refusal = threading.Lock(), threading.Event(), {}

    def work(r):
        if r["id"] in cache or stop.is_set():
            return
        with lock:
            if sum(v["usage"]["cost_usd"] for v in cache.values()) >= 2.0:
                stop.set()
                return
        try:
            conf, usage, rid = llm.self_confidence(r["question"], r["deliberation_record"]["visible_answer"])
        except llm.RefusalError as e:
            refusal.setdefault("e", (r["id"], e))
            stop.set()
            return
        with lock:
            cache[r["id"]] = {"confidence": conf, "usage": usage.as_dict(), "request_id": rid}
            G_CACHE.write_text(json.dumps(cache, indent=1))

    with ThreadPoolExecutor(max_workers=4) as ex:
        list(ex.map(work, recs))
    if refusal:
        q, e = refusal["e"]
        (config.RESULTS / "refusal-sonnet-arm-g.md").write_text(
            f"# Pipeline stopped on a refusal\n\nSonnet arm G, question `{q}`\n\nRefused call: **{e.call}**\n\n"
            f"Request ID: `{e.request_id}`\n\nExact stop details:\n\n```\n{e.stop_details}\n```\n\n"
            "Nothing was reworded or retried.\n")
        sys.exit(f"STOPPED: {e}")
    print(len(cache), "G calls cached", f"${sum(v['usage']['cost_usd'] for v in cache.values()):.3f}")


def offline() -> None:
    """D27: L, H, A2 and F2 on Sonnet's archived hard-pool records, frozen v2 parameters, no API calls."""
    from entangled_mind import llm

    def blocked(*_, **__):
        raise RuntimeError("offline scoring: API calls are blocked")
    llm.client = blocked
    fitd = json.loads(vf.FIT.read_text())
    haiku = json.loads(vf.OUT_JSON.read_text())["results"]
    recs = [r for r in json.loads(POOL4.read_text())["records"] if r["correct"] is not None]
    items = vf.load_items([r["id"] for r in recs], {r["id"]: r for r in recs})
    y = np.array([i.wrong for i in items])
    scores = {}
    with Pool(min(8, os.cpu_count()), initializer=vf._init, initargs=(items,)) as pool:
        for model in ("A2", "F2", "L"):
            mm = fitd["models"][model]
            kw = {"feat_mu": np.array(mm["feature_mu"]), "feat_sd": np.array(mm["feature_sd"])} if model == "L" else {}
            scores[model] = vf.ParallelScorer(model, items, pool, **kw).scores(np.array(mm["final"]["params"]))
    scores["H"] = np.array([v2.hedge_scores(i)[0] for i in items])
    g_cache = json.loads(G_CACHE.read_text()) if G_CACHE.exists() else {}
    have_g = all(i.id in g_cache for i in items)
    if have_g:   # D28: Sonnet's self-confidence, from cached calls (no API call here)
        scores["G"] = np.array([100 - g_cache[i.id]["confidence"] for i in items], float)
    res = {"n": len(items), "n_wrong": int(y.sum()), "models": {}}
    for mname, sc in scores.items():
        p_, lo, hi = vf.boot(list(sc[y]), list(sc[~y]))
        res["models"][mname] = {"auroc": p_, "ci95": [lo, hi]}
    res["A2_minus_F2"] = vf.paired_diff(scores["A2"], scores["F2"], y)
    res["L_minus_H"] = vf.paired_diff(scores["L"], scores["H"], y)
    if have_g:
        res["G_minus_L"] = vf.paired_diff(scores["G"], scores["L"], y)
        res["G_minus_A2"] = vf.paired_diff(scores["G"], scores["A2"], y)
        res["G_cost_usd"] = sum(g_cache[i.id]["usage"]["cost_usd"] for i in items)
    cats = {}
    for i, r in zip(items, recs):
        cats.setdefault("science" if r["category"].startswith("science") else r["category"], []).append(i.wrong)
    OUT_JSON.write_text(json.dumps({"mode": "offline", "hard_pool": res,
                                    "arm_G": "scored from cached Sonnet calls (D28)" if have_g else
                                    "not scored (would need Sonnet calls; replication halted, DEVIATIONS.md D25)"}, indent=1))
    f = lambda r: f"{r['auroc']:.2f} [{r['ci95'][0]:.2f}, {r['ci95'][1]:.2f}]"
    d = lambda x: f"{x[0]:+.3f} [{x[1]:+.3f}, {x[2]:+.3f}]"
    m_ = res["models"]
    hk = haiku["run-2 held-out"]["models"]
    lines = ["# Second base model: claude-sonnet-5-5 (offline scoring of the hard pool)", "",
             "Sonnet's own answers to the hard pool (pool run 4, `h101` excluded after a refusal, DEVIATIONS.md D21) were "
             "scored offline. Each item's archived claims and relation table go through the **already-fitted** v2 models, with "
             "frozen parameters from `results/v2-fit.json`. Nothing is refitted, and **no API call was made** during scoring (the "
             "client is blocked in code). The training-pool run stopped on a second refusal (D25), so only the hard pool is scored here."
             + (f" Arm G comes from {len(items)} separate self-confidence calls to Sonnet, ${res['G_cost_usd']:.2f}, with no refusal (D28)."
                if have_g else ""), "",
             f"Sonnet answered {res['n']} items and got **{res['n_wrong']} wrong** "
             f"({', '.join(f'{k} {sum(v)}/{len(v)}' for k, v in sorted(cats.items()))}).", "",
             "| model | Sonnet, hard pool (all 298) | Haiku, run-2 held-out (80), for reference |", "|---|---|---|",
             f"| A2 learned quantum encoding | {f(m_['A2'])} | {f(hk['A2'])} |",
             f"| F2 learned classical twin | {f(m_['F2'])} | {f(hk['F2'])} |",
             f"| L relation-web features | {f(m_['L'])} | {f(hk['L'])} |",
             f"| H hedge baseline | {f(m_['H'])} | {f(hk['H'])} |",
             (f"| G self-reported confidence | {f(m_['G'])} | {f(hk['G'])} |" if have_g else
              f"| G self-reported confidence | **not scored** (needs Sonnet calls; halted, D25) | {f(hk['G'])} |"), "",
             f"Paired bootstrap on Sonnet's items: A2 − F2 = {d(res['A2_minus_F2'])}; L − H = {d(res['L_minus_H'])}"
             + (f"; G − A2 = {d(res['G_minus_A2'])}; G − L = {d(res['G_minus_L'])}." if have_g else "."), "",
             "The two sets differ in composition: Sonnet's set is the whole hard pool, with 30 wrong of 298, while Haiku's held-out "
             "set is 40 wrong and 40 right. AUROC does not depend on that balance, but the intervals do."]
    OUT_MD.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


def write_md(results, haiku, g_cost) -> None:
    pool_cost = sum(r["cost_usd"] for f in (POOL4, POOL6) if f.exists() for r in json.loads(f.read_text())["records"])
    lines = ["# Second base model: claude-sonnet-5-5", "",
             "The hard pool and the v2 training pool were run through `claude-sonnet-5-5` as base (default effort, adaptive "
             "thinking). The extractor and judge were unchanged. G, L, H and the **already-fitted** A2 and F2 (frozen v2 "
             "parameters, nothing refitted) are scored on Sonnet's own errors. "
             f"Pool runs ${pool_cost:.2f} and arm-G calls ${g_cost:.2f}.", "",
             "| set (Sonnet) | n (wrong) | A2 | F2 | L | G | H | A2 − F2 (paired) | G − L (paired) |",
             "|---|---|---|---|---|---|---|---|---|"]
    f = lambda r: f"{r['auroc']:.2f} [{r['ci95'][0]:.2f}, {r['ci95'][1]:.2f}]"
    d = lambda x: f"{x[0]:+.3f} [{x[1]:+.3f}, {x[2]:+.3f}]"
    for name, res in results.items():
        if "skipped" in res:
            lines.append(f"| {name} | {res['n']} ({res['n_wrong']}) | {res['skipped']} | | | | | | |")
            continue
        m = res["models"]
        lines.append(f"| {name} | {res['n']} ({res['n_wrong']}) | {f(m['A2'])} | {f(m['F2'])} | {f(m['L'])} | {f(m['G'])} | "
                     f"{f(m['H'])} | {d(res['A2_minus_F2'])} | {d(res['G_minus_L'])} |")
    lines += ["", "Haiku 5.5 as base, for comparison (`results/v2-run-1.md`):", "",
              "| set (Haiku) | A2 | F2 | L | G | H |", "|---|---|---|---|---|---|"]
    for name, res in haiku.items():
        m = res["models"]
        lines.append(f"| {name} | {f(m['A2'])} | {f(m['F2'])} | {f(m['L'])} | {f(m['G'])} | {f(m['H'])} |")
    OUT_MD.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    {"--offline": offline, "--arm-g": arm_g_hard_pool}.get(next((a for a in sys.argv[1:]), ""), main)()

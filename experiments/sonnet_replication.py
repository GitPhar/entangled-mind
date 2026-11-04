"""Second base model: does the error-prediction pattern replicate on claude-sonnet-5-5?

    python experiments/sonnet_replication.py

Scores G (Sonnet's self-reported confidence; one call per item), L, H, and the already-fitted
A2 and F2 (frozen v2 parameters from results/v2-fit.json; nothing is refitted) on Sonnet's
items from pool run 4 (hard pool) and pool run 6 (training pool). Haiku's v2 numbers are
shown alongside. Writes results/sonnet-replication.{md,json}. On any refusal it stops."""

import json
import os
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
    main()

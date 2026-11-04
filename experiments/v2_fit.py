"""Version two: fit A2, F2 and L by the pre-registered rule, then evaluate once.

    python experiments/v2_fit.py fit        # reads train + validation only; writes results/v2-fit.json
    python experiments/v2_fit.py evaluate   # locked test + run-2 held-out, ONCE; writes results/v2-run-1.{json,md}

`fit` never loads the test ids. `evaluate` refuses to run if results/v2-run-1.json
exists, and uses the frozen parameters in results/v2-fit.json without refitting.
See experiments/preregistration-v2.md."""

import json
import os
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool

import numpy as np
from dotenv import load_dotenv

from entangled_mind import config, llm, readout, v2

load_dotenv(config.ROOT / ".env")
POOL5 = config.RESULTS / "pool-run-5.json"
POOL3 = config.RESULTS / "pool-run-3.json"
SPLIT = config.EXPERIMENTS / "split-v2.json"
FIT = config.RESULTS / "v2-fit.json"
OUT_JSON = config.RESULTS / "v2-run-1.json"
OUT_MD = config.RESULTS / "v2-run-1.md"
G_TEST_CACHE = config.RESULTS / "v2-arm-g-confidence.json"
G_HELDOUT_CACHE = config.RESULTS / "arm-g-confidence.json"
SEEDS = {"A2": 101, "F2": 202, "L": 303}
N_BOOT = 1000

_ITEMS: list = []


def _init(items):
    global _ITEMS
    _ITEMS = items


def _score_one(args):
    model, k, v = args
    it = _ITEMS[k]
    *a, tau = v
    if model == "A2":
        p = v2.fast_quantum_probs(it, a[0], a[1], a[2], int(a[3]), a[4], a[5], a[6])
    else:
        p = v2.fast_classical_probs(it, a[0], a[1], a[2], int(a[3]), a[4], a[5], a[6])
    return v2.conflict_from_probs(p, it, tau)


class ParallelScorer(v2.Scorer):
    """v2.Scorer with the per-item quantum / classical computation spread over worker processes."""

    def __init__(self, model, items, pool=None, feat_mu=None, feat_sd=None):
        super().__init__(model, items, feat_mu, feat_sd)
        self.pool = pool

    def scores(self, v):
        v = v2.clamp(self.model, np.asarray(v, float))
        if self.model == "L" or self.pool is None:
            return super().scores(v)
        return np.array(self.pool.map(_score_one, [(self.model, k, v) for k in range(len(self.items))], chunksize=8))


def load_items(ids, recs):
    return [v2.item_from_record(recs[q]) for q in ids]


def fit() -> None:
    split = json.loads(SPLIT.read_text())
    recs = {r["id"]: r for r in json.loads(POOL5.read_text())["records"]}
    tr, va = load_items(split["train"], recs), load_items(split["validation"], recs)   # test ids never loaded
    out = {"split_seed": split["seed"], "n_train": len(tr), "n_validation": len(va),
           "n_train_wrong": sum(i.wrong for i in tr), "n_validation_wrong": sum(i.wrong for i in va), "models": {}}
    log = lambda m: print(m, flush=True)
    for model in ("L", "F2", "A2"):
        with Pool(min(8, os.cpu_count()), initializer=_init, initargs=(tr,)) as ptr, \
                Pool(min(4, os.cpu_count()), initializer=_init, initargs=(va,)) as pva:
            s_tr = ParallelScorer(model, tr, ptr)
            s_va = ParallelScorer(model, va, pva, getattr(s_tr, "mu", None), getattr(s_tr, "sd", None))
            res = v2.fit_model(model, s_tr, s_va, seed=SEEDS[model], log=log)
            v = np.array(res["final"]["params"])
            sc = s_tr.scores(v)
            res["flag_threshold"] = v2.train_threshold(sc, np.array([i.wrong for i in tr]))
            if model == "L":
                res["feature_mu"], res["feature_sd"] = s_tr.mu.tolist(), s_tr.sd.tolist()
                res["feature_names"] = v2.FEATURE_NAMES
        out["models"][model] = res
        FIT.write_text(json.dumps(out, indent=1))
        log(f"{model} final: train {res['final']['train_auroc']:.3f} val {res['final']['val_auroc']:.3f}")


def boot(pos, neg, seed=99):
    rng = np.random.default_rng(seed)
    pos, neg = np.asarray(pos, float), np.asarray(neg, float)
    v = [readout.auroc(list(rng.choice(pos, len(pos))), list(rng.choice(neg, len(neg)))) for _ in range(N_BOOT)]
    lo, hi = np.percentile(v, [2.5, 97.5])
    return readout.auroc(list(pos), list(neg)), float(lo), float(hi)


def paired_diff(sa, sb, y, seed=7):
    """Bootstrap of AUROC(a) - AUROC(b) on the same items, stratified."""
    rng = np.random.default_rng(seed)
    pos, neg = np.where(y)[0], np.where(~y)[0]
    d = []
    for _ in range(N_BOOT):
        p, n = rng.choice(pos, len(pos)), rng.choice(neg, len(neg))
        d.append(readout.auroc(list(sa[p]), list(sa[n])) - readout.auroc(list(sb[p]), list(sb[n])))
    return float(np.mean(d)), *[float(x) for x in np.percentile(d, [2.5, 97.5])]


def arm_g(recs, ids, cache_path):
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    lock, stop, refusal = threading.Lock(), threading.Event(), {}

    def work(q):
        if q in cache or stop.is_set():
            return
        try:
            conf, usage, rid = llm.self_confidence(recs[q]["question"], recs[q]["deliberation_record"]["visible_answer"])
        except llm.RefusalError as e:
            refusal.setdefault("e", (q, e))
            stop.set()
            return
        with lock:
            cache[q] = {"confidence": conf, "usage": usage.as_dict(), "request_id": rid}
            cache_path.write_text(json.dumps(cache, indent=1))

    with ThreadPoolExecutor(max_workers=6) as ex:
        list(ex.map(work, ids))
    if refusal:
        q, e = refusal["e"]
        (config.RESULTS / "refusal.md").write_text(
            f"# Pipeline stopped on a refusal\n\nv2 arm G, question `{q}`\n\nRefused call: **{e.call}**\n\nRequest ID: "
            f"`{e.request_id}`\n\nExact stop details:\n\n```\n{e.stop_details}\n```\n\nNothing was reworded or retried.\n")
        sys.exit(f"STOPPED: {e}")
    return {q: 100 - cache[q]["confidence"] for q in ids}


def evaluate() -> None:
    if OUT_JSON.exists():
        sys.exit(f"{OUT_JSON} exists: the locked test set has already been scored once.")
    fitd = json.loads(FIT.read_text())
    split = json.loads(SPLIT.read_text())
    recs5 = {r["id"]: r for r in json.loads(POOL5.read_text())["records"]}
    recs3 = {r["id"]: r for r in json.loads(POOL3.read_text())["records"]}
    held_ids = split["run2_heldout"]["test_wrong"] + split["run2_heldout"]["test_right"]
    sets = {"locked test": (split["test"], recs5, G_TEST_CACHE), "run-2 held-out": (held_ids, recs3, G_HELDOUT_CACHE)}
    config.BASE_MODEL = "claude-haiku-5-5"
    results = {}
    for name, (ids, recs, gcache) in sets.items():
        items = load_items(ids, recs)
        y = np.array([i.wrong for i in items])
        scores = {}
        with Pool(min(8, os.cpu_count()), initializer=_init, initargs=(items,)) as pool:
            for model in ("A2", "F2", "L"):
                m = fitd["models"][model]
                kw = {}
                if model == "L":
                    kw = {"feat_mu": np.array(m["feature_mu"]), "feat_sd": np.array(m["feature_sd"])}
                scores[model] = ParallelScorer(model, items, pool, **kw).scores(np.array(m["final"]["params"]))
        g = arm_g(recs, ids, gcache)
        scores["G"] = np.array([g[q] for q in ids], float)
        res = {"n_wrong": int(y.sum()), "n_right": int((~y).sum()), "models": {}}
        for model, sc in scores.items():
            p, lo, hi = boot(list(sc[y]), list(sc[~y]))
            thr = fitd["models"][model]["flag_threshold"] if model in fitd["models"] else None
            res["models"][model] = {"auroc": p, "ci95": [lo, hi],
                                    "wrong_flagged": None if thr is None else int(np.sum(sc[y] > thr)),
                                    "right_flagged": None if thr is None else int(np.sum(sc[~y] > thr))}
        res["A2_minus_F2"] = paired_diff(scores["A2"], scores["F2"], y)
        # split by type and by contradictions
        kind = lambda c: "science" if c.startswith("science") else c.split("-")[0]
        groups = {f"type: {t}": [k for k, q in enumerate(ids) if kind(recs[q]["category"]) == t]
                  for t in sorted({kind(recs[q]["category"]) for q in ids})}
        nc = [sum(p["relation"] == "contradicts" for p in recs[q]["pairs"]) for q in ids]
        groups["contradictions >= 3"] = [k for k in range(len(ids)) if nc[k] >= 3]
        groups["contradictions < 3"] = [k for k in range(len(ids)) if nc[k] < 3]
        res["by_group"] = {}
        for gname, idx in groups.items():
            idx = np.array(idx, int)
            yy = y[idx]
            row = {"n_wrong": int(yy.sum()), "n_right": int((~yy).sum())}
            for model, sc in scores.items():
                s = sc[idx]
                row[model] = boot(list(s[yy]), list(s[~yy])) if yy.any() and (~yy).any() else None
            res["by_group"][gname] = row
        res["scores"] = {m: {q: float(s) for q, s in zip(ids, sc)} for m, sc in scores.items()}
        results[name] = res
    a, f = results["locked test"]["models"]["A2"], results["locked test"]["models"]["F2"]
    passed = a["ci95"][0] > f["ci95"][1]
    OUT_JSON.write_text(json.dumps({"fit": fitd, "results": results, "primary_pass": passed}, indent=1))
    write_md(fitd, results, passed)


def write_md(fitd, results, passed) -> None:
    names = {"A2": "A2 learned quantum encoding", "F2": "F2 learned classical twin", "L": "L relation-web features (linear)",
             "G": "G self-reported confidence (baseline)"}
    lines = ["# Version two, run 1: learned encodings", "",
             "Pre-registration: `experiments/preregistration-v2.md`. Split locked in `experiments/split-v2.json` before fitting. "
             f"Train {fitd['n_train']} items ({fitd['n_train_wrong']} wrong), validation {fitd['n_validation']} "
             f"({fitd['n_validation_wrong']} wrong). Every model: 9 parameters, 1,000 train evaluations, selected on validation. "
             "The locked test set and the run-2 held-out set were each scored once.", "",
             "## Fitting (train / validation AUROC of the selected candidate)", "",
             "| model | train AUROC | validation AUROC | parameters |", "|---|---|---|---|"]
    for m in ("A2", "F2", "L"):
        r = fitd["models"][m]
        ps = ", ".join(f"{n}={x:.3g}" for n, x in zip(r["names"], r["final"]["params"]))
        lines.append(f"| {names[m]} | {r['final']['train_auroc']:.3f} | {r['final']['val_auroc']:.3f} | {ps}; flag > {r['flag_threshold']:.3g} |")
    for name, res in results.items():
        lines += ["", f"## {name} ({res['n_wrong']} wrong, {res['n_right']} right)", "",
                  "| model | AUROC [95% bootstrap CI] | wrong flagged | right flagged |", "|---|---|---|---|"]
        for m in ("A2", "F2", "L", "G"):
            r = res["models"][m]
            wf = "—" if r["wrong_flagged"] is None else f"{r['wrong_flagged']}/{res['n_wrong']}"
            rf = "—" if r["right_flagged"] is None else f"{r['right_flagged']}/{res['n_right']}"
            lines.append(f"| {names[m]} | {r['auroc']:.2f} [{r['ci95'][0]:.2f}, {r['ci95'][1]:.2f}] | {wf} | {rf} |")
        d = res["A2_minus_F2"]
        lines += ["", f"Paired bootstrap AUROC(A2) − AUROC(F2): {d[0]:+.3f} [{d[1]:+.3f}, {d[2]:+.3f}]."]
        lines += ["", "By group (AUROC [95% CI]):", "", "| group | n wrong / right | A2 | F2 | L | G |", "|---|---|---|---|---|---|"]
        for g, row in res["by_group"].items():
            cell = lambda m: "—" if row[m] is None else f"{row[m][0]:.2f} [{row[m][1]:.2f}, {row[m][2]:.2f}]"
            lines.append(f"| {g} | {row['n_wrong']} / {row['n_right']} | {cell('A2')} | {cell('F2')} | {cell('L')} | {cell('G')} |")
    a, f = results["locked test"]["models"]["A2"], results["locked test"]["models"]["F2"]
    lines += ["", "## Primary criterion", "",
              f"A2's lower 95% bound {a['ci95'][0]:.2f} vs F2's upper 95% bound {f['ci95'][1]:.2f} on the locked test set: "
              f"**{'PASS: the learned quantum encoding beats its classical twin' if passed else 'NOT MET: the learned quantum encoding ties or loses to its classical twin'}**."]
    OUT_MD.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    {"fit": fit, "evaluate": evaluate}[sys.argv[1]]()

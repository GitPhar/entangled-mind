"""Version two: fit A2, F2 and L by the pre-registered rule, then evaluate once.

    python experiments/v2_fit.py fit        # reads train + validation only; writes results/v2-fit.json
    python experiments/v2_fit.py evaluate   # locked test + run-2 held-out, ONCE; writes results/v2-run-1.{json,md}
    python experiments/v2_fit.py fit21      # v2.1 honest hedge (Addendum B): train + validation only
    python experiments/v2_fit.py evaluate21 # v2.1 on locked test + held-out, ONCE, after `evaluate`

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
SEEDS = {"A2": 101, "F2": 202, "L": 303, "A21": 111, "F21": 212}
FIT21 = config.RESULTS / "v2.1-fit.json"
OUT21_JSON = config.RESULTS / "v2.1-run-1.json"
OUT21_MD = config.RESULTS / "v2.1-run-1.md"
N_BOOT = 1000

_ITEMS: list = []


def _init(items):
    global _ITEMS
    _ITEMS = items


def _score_one(args):
    model, k, v = args
    it = _ITEMS[k]
    if model in ("A21", "F21"):
        return v2.conflict21(it, model == "A21", v)
    *a, tau = v
    if model == "A2":
        p = v2.fast_quantum_probs(it, a[0], a[1], a[2], int(a[3]), a[4], a[5], a[6])
    elif model == "F2P":
        p = v2.fast_classical_probs(it, a[0], a[1], a[2], int(a[3]), a[4], a[5], a[6], alpha=a[7])
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


def fit(models=("L", "F2", "A2"), out_path=None) -> None:
    out_path = out_path or FIT
    split = json.loads(SPLIT.read_text())
    recs = {r["id"]: r for r in json.loads(POOL5.read_text())["records"]}
    tr, va = load_items(split["train"], recs), load_items(split["validation"], recs)   # test ids never loaded
    out = {"split_seed": split["seed"], "n_train": len(tr), "n_validation": len(va),
           "n_train_wrong": sum(i.wrong for i in tr), "n_validation_wrong": sum(i.wrong for i in va), "models": {}}
    log = lambda m: print(m, flush=True)
    for model in models:
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
        out_path.write_text(json.dumps(out, indent=1))
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
    train_items = load_items(split["train"], recs5)
    ytr = np.array([i.wrong for i in train_items])
    h_thr = {"H": v2.train_threshold(np.array([v2.hedge_scores(i)[0] for i in train_items]), ytr),
             "H-count": v2.train_threshold(np.array([v2.hedge_scores(i)[1] for i in train_items], float), ytr)}
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
        scores["H"] = np.array([v2.hedge_scores(i)[0] for i in items])          # Addendum B
        scores["H-count"] = np.array([v2.hedge_scores(i)[1] for i in items], float)
        res = {"n_wrong": int(y.sum()), "n_right": int((~y).sum()), "models": {}}
        for model, sc in scores.items():
            p, lo, hi = boot(list(sc[y]), list(sc[~y]))
            thr = fitd["models"][model]["flag_threshold"] if model in fitd["models"] else h_thr.get(model)
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
             "G": "G self-reported confidence (baseline)", "H": "H hedge baseline: confidence of no-lean claims",
             "H-count": "H-count: number of no-lean claims"}
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
        for m in ("A2", "F2", "L", "G", "H", "H-count"):
            r = res["models"][m]
            wf = "—" if r["wrong_flagged"] is None else f"{r['wrong_flagged']}/{res['n_wrong']}"
            rf = "—" if r["right_flagged"] is None else f"{r['right_flagged']}/{res['n_right']}"
            lines.append(f"| {names[m]} | {r['auroc']:.2f} [{r['ci95'][0]:.2f}, {r['ci95'][1]:.2f}] | {wf} | {rf} |")
        d = res["A2_minus_F2"]
        lines += ["", f"Paired bootstrap AUROC(A2) − AUROC(F2): {d[0]:+.3f} [{d[1]:+.3f}, {d[2]:+.3f}]."]
        lines += ["", "By group (AUROC [95% CI]):", "", "| group | n wrong / right | A2 | F2 | L | G | H |", "|---|---|---|---|---|---|---|"]
        for g, row in res["by_group"].items():
            cell = lambda m: "—" if row[m] is None else f"{row[m][0]:.2f} [{row[m][1]:.2f}, {row[m][2]:.2f}]"
            lines.append(f"| {g} | {row['n_wrong']} / {row['n_right']} | {cell('A2')} | {cell('F2')} | {cell('L')} | {cell('G')} | {cell('H')} |")
    a, f = results["locked test"]["models"]["A2"], results["locked test"]["models"]["F2"]
    lines += ["", "## Primary criterion", "",
              f"A2's lower 95% bound {a['ci95'][0]:.2f} vs F2's upper 95% bound {f['ci95'][1]:.2f} on the locked test set: "
              f"**{'PASS: the learned quantum encoding beats its classical twin' if passed else 'NOT MET: the learned quantum encoding ties or loses to its classical twin'}**."]
    OUT_MD.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


def evaluate21() -> None:
    """v2.1 on the locked test set and the run-2 held-out set, once, after the v2 arms."""
    if not OUT_JSON.exists():
        sys.exit("v2 arms must be evaluated first (Addendum B).")
    if OUT21_JSON.exists():
        sys.exit(f"{OUT21_JSON} exists: v2.1 has already been scored once.")
    fit21d = json.loads(FIT21.read_text())
    v2res = json.loads(OUT_JSON.read_text())["results"]
    split = json.loads(SPLIT.read_text())
    recs5 = {r["id"]: r for r in json.loads(POOL5.read_text())["records"]}
    recs3 = {r["id"]: r for r in json.loads(POOL3.read_text())["records"]}
    held_ids = split["run2_heldout"]["test_wrong"] + split["run2_heldout"]["test_right"]
    sets = {"locked test": (split["test"], recs5), "run-2 held-out": (held_ids, recs3)}
    results = {}
    for name, (ids, recs) in sets.items():
        items = load_items(ids, recs)
        y = np.array([i.wrong for i in items])
        scores = {}
        with Pool(min(8, os.cpu_count()), initializer=_init, initargs=(items,)) as pool:
            for model in ("A21", "F21"):
                scores[model] = ParallelScorer(model, items, pool).scores(np.array(fit21d["models"][model]["final"]["params"]))
        if name == "locked test":   # Addendum C: the selected A2.1 also on the noisy ibm_fez simulator, once
            from entangled_mind import backends
            va = np.array(fit21d["models"]["A21"]["final"]["params"])
            va = v2.clamp("A21", va)

            def noisy_one(k):
                qc, h, u = v2.build_a21_circuit(items[k], va)
                counts = backends.run_noisy(backends.transpile(qc), seed=k + 1)
                return v2.conflict21_from_counts(counts, h, u, va)

            backends.noisy_simulator()
            with ThreadPoolExecutor(max_workers=4) as ex:
                scores["A21-noisy"] = np.array(list(ex.map(noisy_one, range(len(items)))))
        prev = {m: np.array([v2res[name]["scores"][m][q] for q in ids]) for m in ("A2", "F2", "L", "G", "H")}
        res = {"n_wrong": int(y.sum()), "n_right": int((~y).sum()), "models": {}}
        for model, sc in scores.items():
            p, lo, hi = boot(list(sc[y]), list(sc[~y]))
            thr = fit21d["models"][model.replace("-noisy", "")]["flag_threshold"]
            res["models"][model] = {"auroc": p, "ci95": [lo, hi], "wrong_flagged": int(np.sum(sc[y] > thr)),
                                    "right_flagged": int(np.sum(sc[~y] > thr))}
        res["A21_minus_F21"] = paired_diff(scores["A21"], scores["F21"], y)
        if "A21-noisy" in scores:
            res["A21noisy_minus_A21"] = paired_diff(scores["A21-noisy"], scores["A21"], y)
        res["A21_minus_A2"] = paired_diff(scores["A21"], prev["A2"], y)
        res["F21_minus_F2"] = paired_diff(scores["F21"], prev["F2"], y)
        res["reference_v2"] = {m: v2res[name]["models"][m] for m in ("A2", "F2", "L", "G", "H")}
        kind = lambda c: "science" if c.startswith("science") else c.split("-")[0]
        groups = {f"type: {t}": [k for k, q in enumerate(ids) if kind(recs[q]["category"]) == t]
                  for t in sorted({kind(recs[q]["category"]) for q in ids})}
        res["by_group"] = {}
        for gname, idx in groups.items():
            idx = np.array(idx, int)
            yy = y[idx]
            res["by_group"][gname] = {"n_wrong": int(yy.sum()), "n_right": int((~yy).sum()),
                                      **{m: (boot(list(sc[idx][yy]), list(sc[idx][~yy])) if yy.any() and (~yy).any() else None)
                                         for m, sc in scores.items()}}
        res["scores"] = {m: {q: float(s_) for q, s_ in zip(ids, sc)} for m, sc in scores.items()}
        results[name] = res
    a, f = results["locked test"]["models"]["A21"], results["locked test"]["models"]["F21"]
    passed = a["ci95"][0] > f["ci95"][1]
    OUT21_JSON.write_text(json.dumps({"fit": fit21d, "results": results, "primary_pass": passed}, indent=1))
    write21_md(fit21d, results, passed)


def write21_md(fit21d, results, passed) -> None:
    """v2.1 markdown, from the archived JSON alone."""
    a, f = results["locked test"]["models"]["A21"], results["locked test"]["models"]["F21"]
    an = results["locked test"]["models"]["A21-noisy"]
    noisy_line = (f"Secondary (Addendum C): noisy-simulator A2.1 lower bound {an['ci95'][0]:.2f} vs F2.1 upper bound "
                  f"{f['ci95'][1]:.2f}: {'above' if an['ci95'][0] > f['ci95'][1] else 'not above'}.")
    names = {"A21": "A2.1 honest-hedge quantum (noiseless)", "F21": "F2.1 honest-hedge classical twin (exact; no circuit)",
             "A21-noisy": "A2.1 on the noisy ibm_fez simulator (1,000 shots)"}
    lines = ["# Version 2.1, run 1: honest-hedge encoding", "",
             "Pre-registration: `experiments/preregistration-v2.md`, Addenda B and C (written before any v2 or v2.1 test evaluation). "
             "Fitted on exact noiseless statevectors on train, selected on validation, scored once on each set after the v2 arms. "
             "On the locked test set the selected A2.1 is scored noiseless and on the noisy `ibm_fez` simulator; the pass "
             "criterion uses the noiseless comparison.", "",
             "| model | train AUROC | validation AUROC | parameters |", "|---|---|---|---|"]
    for m in ("A21", "F21"):
        r = fit21d["models"][m]
        ps = ", ".join(f"{n}={x:.3g}" for n, x in zip(r["names"], r["final"]["params"]))
        lines.append(f"| {names[m]} | {r['final']['train_auroc']:.3f} | {r['final']['val_auroc']:.3f} | {ps}; flag > {r['flag_threshold']:.3g} |")
    for name, res in results.items():
        lines += ["", f"## {name} ({res['n_wrong']} wrong, {res['n_right']} right)", "",
                  "| model | AUROC [95% CI] | wrong flagged | right flagged |", "|---|---|---|---|"]
        for m in [x for x in ("A21", "A21-noisy", "F21") if x in res["models"]]:
            r = res["models"][m]
            lines.append(f"| {names[m]} | {r['auroc']:.2f} [{r['ci95'][0]:.2f}, {r['ci95'][1]:.2f}] | "
                         f"{r['wrong_flagged']}/{res['n_wrong']} | {r['right_flagged']}/{res['n_right']} |")
        for m, r in res["reference_v2"].items():
            lines.append(f"| (v2) {m} | {r['auroc']:.2f} [{r['ci95'][0]:.2f}, {r['ci95'][1]:.2f}] | | |")
        for k, lab in (("A21_minus_F21", "A2.1 − F2.1"), ("A21_minus_A2", "A2.1 − A2"), ("F21_minus_F2", "F2.1 − F2"),
                       ("A21noisy_minus_A21", "A2.1 noisy − A2.1 noiseless")):
            if k not in res:
                continue
            d = res[k]
            lines.append(f"\nPaired bootstrap {lab}: {d[0]:+.3f} [{d[1]:+.3f}, {d[2]:+.3f}].")
        lines += ["", "| group | n wrong / right | A2.1 | F2.1 |", "|---|---|---|---|"]
        for g, row in res["by_group"].items():
            cell = lambda m: "—" if row[m] is None else f"{row[m][0]:.2f} [{row[m][1]:.2f}, {row[m][2]:.2f}]"
            lines.append(f"| {g} | {row['n_wrong']} / {row['n_right']} | {cell('A21')} | {cell('F21')} |")
    lines += ["", "## Primary criterion", "",
              f"A2.1's lower 95% bound {a['ci95'][0]:.2f} vs F2.1's upper 95% bound {f['ci95'][1]:.2f}: "
              f"**{'PASS: the honest-hedge quantum encoding beats its classical twin' if passed else 'NOT MET: the honest-hedge quantum encoding ties or loses to its classical twin'}**.",
              "", noisy_line]
    OUT21_MD.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    {"fit": fit, "evaluate": evaluate, "fit21": lambda: fit(("F21", "A21"), FIT21),
     "evaluate21": evaluate21}[sys.argv[1]]()

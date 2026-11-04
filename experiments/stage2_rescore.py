"""Stage 2 run 2b: re-score run 2 with arms F and G and the added statistics
(experiments/preregistration.md, Addendum A).

    python experiments/stage2_rescore.py

- Arm F (classical Ising twin): exact enumeration, every item.
- Arm G (self-reported confidence): one call per item to the base model,
  conflict score = 100 - confidence. Calls are cached in
  results/arm-g-confidence.json; on any refusal the script stops at once and
  records the refused call in results/refusal.md, with no rewording or retry.
- AUROC with 95% stratified bootstrap intervals (1000 resamples) for every arm.
- Arm D null: 200 independent shuffles of each test item's relation web,
  noisy simulator, AUROC per shuffle; arm A's position in that null as a p-value.

Writes results/stage2-run-2b.{json,md}."""

import json
import sys
import threading
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

import numpy as np
from dotenv import load_dotenv

from entangled_mind import backends, classical_twin, config, encoder, llm, readout

load_dotenv(config.ROOT / ".env")
POOL = config.RESULTS / "pool-run-3.json"
RUN2 = config.RESULTS / "stage2-run-2.json"
G_CACHE = config.RESULTS / "arm-g-confidence.json"
NULL_CACHE = config.RESULTS / "stage2-run-2b-dnull.json"
OUT_JSON = config.RESULTS / "stage2-run-2b.json"
OUT_MD = config.RESULTS / "stage2-run-2b.md"
N_BOOT, BOOT_SEED = 1000, 99
N_NULL, NULL_SEED = 200, 31337
ARMS = ("A", "B", "C", "D", "E", "F", "G", "A0")


def arm_g(recs: dict, ids: list[str]) -> dict:
    cache = json.loads(G_CACHE.read_text()) if G_CACHE.exists() else {}
    stop, lock, refusal = threading.Event(), threading.Lock(), {}

    def work(q):
        if stop.is_set() or q in cache:
            return
        r = recs[q]
        try:
            conf, usage, rid = llm.self_confidence(r["question"], r["deliberation_record"]["visible_answer"])
        except llm.RefusalError as e:
            refusal.setdefault("first", (q, e))
            stop.set()
            return
        with lock:
            cache[q] = {"confidence": conf, "usage": usage.as_dict(), "request_id": rid}
            G_CACHE.write_text(json.dumps(cache, indent=1))

    with ThreadPoolExecutor(max_workers=6) as ex:
        list(ex.map(work, ids))
    if refusal:
        q, e = refusal["first"]
        (config.RESULTS / "refusal.md").write_text(
            f"# Pipeline stopped on a refusal\n\nArm G, question `{q}`\n\nRefused call: **{e.call}**\n\n"
            f"Request ID: `{e.request_id}`\n\nExact stop details:\n\n```\n{e.stop_details}\n```\n\n"
            "Nothing was reworded or retried; the next step is a support ticket with the request ID.\n")
        print(f"STOPPED: {e}")
        sys.exit(3)
    return cache


def boot_auroc(pos: list[float], neg: list[float], seed: int = BOOT_SEED) -> tuple:
    rng = np.random.default_rng(seed)
    pos, neg = np.asarray(pos, float), np.asarray(neg, float)
    point = readout.auroc(list(pos), list(neg))
    vals = [readout.auroc(list(rng.choice(pos, len(pos))), list(rng.choice(neg, len(neg)))) for _ in range(N_BOOT)]
    lo, hi = np.percentile(vals, [2.5, 97.5])
    return point, float(lo), float(hi)


def _single_thread():
    """Worker initialiser: one Aer thread per process, so 10 workers do not oversubscribe the CPU."""
    backends.noisy_simulator().set_options(max_parallel_threads=1, max_parallel_experiments=1,
                                           max_parallel_shots=1)


def _null_item(args):
    """Conflict scores of one test item under each of its shuffles (noisy simulator)."""
    rec, seeds = args
    web = encoder.build_web(rec["contentions"], rec["pairs"])
    out = []
    for s in seeds:
        shuf = encoder.shuffled_web(web, seed=s)
        isa = backends.transpile(encoder.build_circuit(shuf, entangle=True))
        counts = backends.run_noisy(isa, seed=int(rec["id"][1:]))
        out.append(readout.quantum_readout(counts, shuf)["conflict_score"])
    return rec["id"], out


def d_null(recs: dict, test: list[str]) -> dict:
    cache = json.loads(NULL_CACHE.read_text()) if NULL_CACHE.exists() else {}
    todo = [q for q in test if q not in cache]
    # shuffle k of item q uses seed NULL_SEED + 1000 * k + item number: independent across shuffles and items
    jobs = [(recs[q], [NULL_SEED + 1000 * k + int(q[1:]) for k in range(N_NULL)]) for q in todo]
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=11, initializer=_single_thread) as ex:
        for q, scores in ex.map(_null_item, jobs):
            cache[q] = scores
            NULL_CACHE.write_text(json.dumps(cache))
            print(f"null {q} done ({len(cache)}/{len(test)}, {time.time() - t0:.0f}s)", flush=True)
    return cache


def main() -> None:
    pool = json.loads(POOL.read_text())
    recs = {r["id"]: r for r in pool["records"]}
    run2 = json.loads(RUN2.read_text())
    split, items = run2["split"], run2["items"]
    test = split["test_wrong"] + split["test_right"]
    order = split["calibration"] + test

    # arm F and arm G for every item
    config.BASE_MODEL = pool["base_model"]
    g = arm_g(recs, order)
    for q in order:
        web = encoder.build_web(recs[q]["contentions"], recs[q]["pairs"])
        items[q]["arms"]["F"] = {"readout": classical_twin.classical_twin_readout(web)}
        c = g[q]["confidence"]
        items[q]["arms"]["G"] = {"readout": {"confidence": c, "conflict_score": float(100 - c),
                                             "judgment": recs[q]["model_answer"]}}

    score = lambda q, arm: items[q]["arms"][arm]["readout"]["conflict_score"]
    present = [a for a in ARMS if all(a in items[q]["arms"] for q in test)]
    thr = dict(run2["thresholds"])
    for a in ("F", "G"):
        thr[a] = readout.calibrate_threshold([score(q, a) for q in split["calibration"]])
    nw, nr = len(split["test_wrong"]), len(split["test_right"])
    table = {}
    for a in present:
        t = thr["A" if a == "B" else a]
        point, lo, hi = boot_auroc([score(q, a) for q in split["test_wrong"]], [score(q, a) for q in split["test_right"]])
        table[a] = {
            "threshold": t,
            "calibration_flag_fraction": None if a == "B" else
            float(np.mean([score(q, a) > t for q in split["calibration"]])),
            "test_wrong_flagged": sum(score(q, a) > t for q in split["test_wrong"]),
            "test_right_flagged": sum(score(q, a) > t for q in split["test_right"]),
            "auroc_test": point, "auroc_ci95": [lo, hi],
        }

    # arm D null distribution vs arm A
    null = d_null(recs, test)
    null_auroc = [readout.auroc([null[q][k] for q in split["test_wrong"]], [null[q][k] for q in split["test_right"]])
                  for k in range(N_NULL)]
    a_auroc = table["A"]["auroc_test"]
    p = (1 + sum(v >= a_auroc for v in null_auroc)) / (N_NULL + 1)
    dnull = {"n_shuffles": N_NULL, "null_auroc_mean": float(np.mean(null_auroc)),
             "null_auroc_2.5_97.5": [float(x) for x in np.percentile(null_auroc, [2.5, 97.5])],
             "auroc_A": a_auroc, "p_value_A_ge_null": p}

    wr = {a: table[a]["test_wrong_flagged"] / nw for a in present}
    h2 = wr["A"] >= 0.10 and all(wr[c] <= wr["A"] / 2 for c in ("C", "D", "E"))
    h2_ext = h2 and all(wr[c] <= wr["A"] / 2 for c in ("F", "G"))
    OUT_JSON.write_text(json.dumps({"split": split, "thresholds": thr, "table": table, "d_null": dnull,
                                    "null_auroc": null_auroc, "H2_original": h2, "H2_with_F_G": h2_ext,
                                    "arm_F_G": {q: {a: items[q]["arms"][a]["readout"] for a in ("F", "G")} for q in order}},
                                   indent=1))
    write_md(split, table, dnull, h2, h2_ext, present, recs, items, thr, g)


def write_md(split, table, dnull, h2, h2_ext, present, recs, items, thr, g) -> None:
    nw, nr = len(split["test_wrong"]), len(split["test_right"])
    names = {"A": "A  entangled, noisy sim", "B": "B  entangled, real hardware", "C": "C  no entangling gates",
             "D": "D  shuffled relation web (one shuffle)", "E": "E  classical contradiction strength",
             "F": "F  classical Ising twin (exact enumeration)", "G": "G  self-reported confidence (100 − c)",
             "A0": "A0 entangled, noiseless (supplementary)"}
    g_cost = sum(v["usage"]["cost_usd"] for v in g.values())
    lines = ["# Stage 2, run 2b: seven arms on the hard-pool test set", "",
             "Re-scoring of Stage 2 run 2 (`results/stage2-run-2.md`) with the arms and statistics pre-registered in "
             "`experiments/preregistration.md`, Addendum A. Arms A–E and A0 are the run-2 readouts, unchanged. "
             f"Base model `claude-haiku-5-5`; test set {nw} wrong + {nr} right; calibration {len(split['calibration'])} items. "
             f"Arm G calls cost ${g_cost:.4f}.", "",
             f"| arm | threshold | calibration flag rate | wrong flagged (of {nw}) | right flagged (of {nr}) | AUROC test [95% bootstrap CI] |",
             "|---|---|---|---|---|---|"]
    for a in ("A", "B", "C", "D", "E", "F", "G", "A0"):
        if a not in table:
            lines.append(f"| {names[a]} | not run | | | | |")
            continue
        t = table[a]
        cf = "—" if t["calibration_flag_fraction"] is None else f"{t['calibration_flag_fraction']:.2f}"
        lines.append(f"| {names[a]} | {t['threshold']:.3f} | {cf} | {t['test_wrong_flagged']} ({t['test_wrong_flagged'] / nw:.0%}) | "
                     f"{t['test_right_flagged']} ({t['test_right_flagged'] / nr:.0%}) | "
                     f"{t['auroc_test']:.2f} [{t['auroc_ci95'][0]:.2f}, {t['auroc_ci95'][1]:.2f}] |")
    d = dnull
    lines += ["", "## Arm D as a null distribution", "",
              f"{d['n_shuffles']} independent shuffles of every test item's relation web (same number of relations and "
              f"the same strengths on random pairs), each run on the noisy simulator. Null AUROC mean {d['null_auroc_mean']:.2f}, "
              f"central 95% [{d['null_auroc_2.5_97.5'][0]:.2f}, {d['null_auroc_2.5_97.5'][1]:.2f}]. "
              f"Arm A AUROC {d['auroc_A']:.2f}: **p = {d['p_value_A_ge_null']:.3f}** (share of shuffles, counted with +1 smoothing, "
              "that score at least as well as the real web).", "",
              "## H2", "",
              f"- Original criterion (A ≥ 10% of wrong items flagged; C, D, E ≤ half of A's rate): **{'met' if h2 else 'not met'}**.",
              f"- With the added controls F and G held to the same bar: **{'met' if h2_ext else 'not met'}**."]
    OUT_MD.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()

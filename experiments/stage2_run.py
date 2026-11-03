"""Stage 2, run 1: all five arms, per experiments/preregistration.md.

1. Arms A, C, D (noisy simulator from the real backend), supplementary A0
   (noiseless) and E (classical) on all 60 items: calibration + test.
2. Per-arm thresholds from the calibration pool only.
3. Test-set metrics, hypotheses H1-H4, and the hardware gate.
4. Arm B (real hardware, one Batch job of 20 circuits) only if the gate and
   the QPU budget allow; then H5.

    python experiments/stage2_run.py <run> [--md-only]

Readouts for every item and arm (including raw counts) go to
results/stage2-run-<run>.json; the summary table to results/stage2-run-<run>.md.
Simulator results are cached in results/stage2-run-<run>.partial.json so a crash
never reruns finished items. --md-only rewrites the markdown from the archived JSON."""

import json
import sys
import time

import numpy as np

from entangled_mind import backends, config, encoder, readout

# Stage 2 run -> pool run it uses. Run 1: standard pool, Haiku base (D5). Run 2: hard pool (D6).
STAGE2_POOLS = {1: "pool-run-2.json", 2: "pool-run-3.json"}
RUN = int(sys.argv[1]) if len(sys.argv) > 1 else 1
POOL = config.RESULTS / STAGE2_POOLS[RUN]
OUT_JSON = config.RESULTS / f"stage2-run-{RUN}.json"
OUT_MD = config.RESULTS / f"stage2-run-{RUN}.md"
PARTIAL = config.RESULTS / f"stage2-run-{RUN}.partial.json"
QUANTUM_SIM_ARMS = ("A", "C", "D")
CONTROL_ARMS = ("C", "D", "E")


def item_seed(qid: str) -> int:
    return int(qid[1:])


def circuits_for(rec: dict) -> dict:
    web = encoder.build_web(rec["contentions"], rec["pairs"])
    shuf = encoder.shuffled_web(web, seed=config.SHUFFLE_SEED * 1000 + item_seed(rec["id"]))
    return {
        "web": web, "shuffled_web": shuf,
        "A": encoder.build_circuit(web, entangle=True),
        "C": encoder.build_circuit(web, entangle=False),
        "D": encoder.build_circuit(shuf, entangle=True),
    }


def simulate_item(rec: dict) -> dict:
    cs = circuits_for(rec)
    web = cs["web"]
    out = {"n_qubits": web.n, "n_edges": len(web.edges),
           "n_contradictions": sum(J < 0 for _, _, J in web.edges), "arms": {}}
    for arm in QUANTUM_SIM_ARMS:
        isa = backends.transpile(cs[arm])
        counts = backends.run_noisy(isa, seed=item_seed(rec["id"]))
        w = cs["shuffled_web"] if arm == "D" else web
        out["arms"][arm] = {"counts": counts, "readout": readout.quantum_readout(counts, w),
                            "cz": int(isa.count_ops().get("cz", 0)), "depth": isa.depth()}
    ideal = backends.run_ideal(cs["A"], seed=item_seed(rec["id"]))
    out["arms"]["A0"] = {"counts": ideal, "readout": readout.quantum_readout(ideal, web)}
    out["arms"]["E"] = {"readout": readout.classical_readout(web)}
    return out


def spearman(x, y) -> float | None:
    def ranks(v):
        v = np.asarray(v, float)
        order = v.argsort()
        r = np.empty(len(v))
        r[order] = np.arange(len(v))
        for val in np.unique(v):          # average ranks over ties
            r[v == val] = r[v == val].mean()
        return r
    rx, ry = ranks(x), ranks(y)
    if rx.std() == 0 or ry.std() == 0:
        return None
    return float(np.corrcoef(rx, ry)[0, 1])


def h2_verdict(wrong_rates: dict) -> bool:
    a = wrong_rates["A"]
    if a != a:   # nan: no wrong items
        return False
    return a >= 0.10 and all(wrong_rates[c] <= a / 2 for c in CONTROL_ARMS)


def h2_robust(flags_wrong: dict, n_wrong: int) -> bool:
    """True if the H2 verdict survives adding or removing any single wrong-item flag in any one arm."""
    base = h2_verdict({k: v / n_wrong for k, v in flags_wrong.items()})
    for arm in ("A",) + CONTROL_ARMS:
        for d in (-1, 1):
            k = flags_wrong[arm] + d
            if 0 <= k <= n_wrong:
                alt = dict(flags_wrong, **{arm: k})
                if h2_verdict({a: v / n_wrong for a, v in alt.items()}) != base:
                    return False
    return True


def main() -> None:
    pool = json.loads(POOL.read_text())
    recs = {r["id"]: r for r in pool["records"]}
    split = pool["split"]
    test = split["test_wrong"] + split["test_right"]
    order = split["calibration"] + test
    sims = json.loads(PARTIAL.read_text()) if PARTIAL.exists() else {}
    t0 = time.time()
    for qid in order:
        if qid in sims:
            continue
        t = time.time()
        sims[qid] = simulate_item(recs[qid])
        PARTIAL.write_text(json.dumps(sims))
        print(f"{qid} n={sims[qid]['n_qubits']} edges={sims[qid]['n_edges']} "
              f"cz(A)={sims[qid]['arms']['A']['cz']} {time.time() - t:.0f}s", flush=True)
    print(f"simulation done in {time.time() - t0:.0f}s")

    score = lambda qid, arm: sims[qid]["arms"][arm]["readout"]["conflict_score"]
    arms = ("A", "C", "D", "E", "A0")
    thresholds = {arm: readout.calibrate_threshold([score(q, arm) for q in split["calibration"]]) for arm in arms}
    flagged = {arm: {q: score(q, arm) > thresholds[arm] for q in order} for arm in arms}
    wrong_cal = [q for q in split["calibration"] if not recs[q]["correct"]]
    right_cal = [q for q in split["calibration"] if recs[q]["correct"]]

    summary = {}
    for arm in arms:
        summary[arm] = {
            "threshold": thresholds[arm],
            "calibration_flag_fraction": float(np.mean([flagged[arm][q] for q in split["calibration"]])),
            "test_wrong_flagged": sum(flagged[arm][q] for q in split["test_wrong"]),
            "test_right_flagged": sum(flagged[arm][q] for q in split["test_right"]),
            "auroc_test": readout.auroc([score(q, arm) for q in split["test_wrong"]],
                                        [score(q, arm) for q in split["test_right"]]),
            "auroc_calibration": readout.auroc([score(q, arm) for q in wrong_cal],
                                               [score(q, arm) for q in right_cal]),
            "agree_with_model": sum(sims[q]["arms"][arm]["readout"]["judgment"] == recs[q]["model_answer"] for q in test),
            "agree_with_truth": sum(sims[q]["arms"][arm]["readout"]["judgment"] == recs[q]["answer"] for q in test),
        }
    n_wrong = len(split["test_wrong"])
    wrong_rates = {a: summary[a]["test_wrong_flagged"] / n_wrong if n_wrong else float("nan") for a in arms}

    # --- hypotheses on the simulator --------------------------------------
    hyp = {}
    agree = summary["A"]["agree_with_model"] / len(test)
    hyp["H1"] = {"value": agree, "verdict": "pass" if agree >= 0.70 else ("falsified" if agree <= 0.50 else "fail (not falsified)")}
    flags_wrong = {a: summary[a]["test_wrong_flagged"] for a in ("A",) + CONTROL_ARMS}
    h2 = h2_verdict(wrong_rates)
    hyp["H2"] = {"wrong_flag_rates": {a: wrong_rates[a] for a in ("A",) + CONTROL_ARMS},
                 "criterion_met": h2, "robust_to_one_item": h2_robust(flags_wrong, n_wrong)}
    hyp["H2"]["verdict"] = ("pass" if h2 else "fail") if hyp["H2"]["robust_to_one_item"] else \
        f"too noisy to call (nominally {'pass' if h2 else 'fail'})"
    if n_wrong < config.N_TEST_WRONG:
        hyp["H2"]["verdict"] = f"underpowered: only {n_wrong} known-wrong items (nominally {'pass' if h2 else 'fail'})"
    for h, ctrl in (("H3", "C"), ("H4", "D")):
        a, c = summary["A"]["auroc_test"], summary[ctrl]["auroc_test"]
        hyp[h] = {"auroc_A": a, f"auroc_{ctrl}": c,
                  "verdict": "pass" if a - c >= 0.10 else ("falsified" if c >= a else "fail (not falsified)")}

    gate = wrong_rates["A"] >= 0.10 and all(wrong_rates["A"] > wrong_rates[c] for c in CONTROL_ARMS)
    stage1_back = (config.RESULTS / "stage1-run-1.json").exists()
    used = max(backends.cumulative_qpu_seconds(),
               float(backends.service_usage()["usage_consumed_seconds"] or 0))
    hardware = {"gate_met": gate, "stage1_returned": stage1_back, "qpu_seconds_before": used, "ran": False}

    if gate and stage1_back and used < config.QPU_STOP_SECONDS:
        isas = [backends.transpile(circuits_for(recs[q])["A"]) for q in test]
        counts, usage = backends.run_hardware(isas, purpose=f"Stage 2 run {RUN} arm B ({len(test)} test circuits)")
        hardware.update(ran=True, usage=usage)
        for q, c in zip(test, counts):
            web = encoder.build_web(recs[q]["contentions"], recs[q]["pairs"])
            sims[q]["arms"]["B"] = {"counts": c, "readout": readout.quantum_readout(c, web)}
        b_flag = {q: score(q, "B") > thresholds["A"] for q in test}
        summary["B"] = {
            "threshold": thresholds["A"], "calibration_flag_fraction": None,
            "test_wrong_flagged": sum(b_flag[q] for q in split["test_wrong"]),
            "test_right_flagged": sum(b_flag[q] for q in split["test_right"]),
            "auroc_test": readout.auroc([score(q, "B") for q in split["test_wrong"]],
                                        [score(q, "B") for q in split["test_right"]]),
            "auroc_calibration": None,
            "agree_with_model": sum(sims[q]["arms"]["B"]["readout"]["judgment"] == recs[q]["model_answer"] for q in test),
            "agree_with_truth": sum(sims[q]["arms"]["B"]["readout"]["judgment"] == recs[q]["answer"] for q in test),
        }
        rho = spearman([score(q, "A") for q in test], [score(q, "B") for q in test])
        b_rate = summary["B"]["test_wrong_flagged"] / n_wrong
        hyp["H5"] = {"spearman_A_B": rho, "B_wrong_flag_rate": b_rate,
                     "verdict": "pass" if (rho is not None and rho >= 0.5 and b_rate >= 0.10)
                     else ("falsified" if (rho is None or rho <= 0 or b_rate == 0) else "fail (not falsified)")}
        flags_b = dict(flags_wrong, A=summary["B"]["test_wrong_flagged"])
        hyp["H2_hardware"] = {"criterion_met": h2_verdict({a: v / n_wrong for a, v in flags_b.items()}),
                              "robust_to_one_item": h2_robust(flags_b, n_wrong)}
    else:
        reason = ("simulator gate not met (A does not beat every control)" if not gate else
                  "Stage 1 hardware job has not returned" if not stage1_back else
                  f"QPU budget ({used:.0f}s >= {config.QPU_STOP_SECONDS}s)")
        hardware["skipped_because"] = reason
        hyp["H5"] = {"verdict": f"untested ({reason})"}

    OUT_JSON.write_text(json.dumps({"split": split, "thresholds": thresholds, "summary": summary,
                                    "hypotheses": hyp, "hardware": hardware, "items": sims}, indent=1))
    write_md(recs, split, sims, summary, hyp, hardware, thresholds)
    PARTIAL.unlink()


def fmt(x, nd=2):
    return "—" if x is None else (f"{x:.{nd}f}" if isinstance(x, float) else str(x))


def write_md(recs, split, sims, summary, hyp, hardware, thresholds) -> None:
    test = split["test_wrong"] + split["test_right"]
    nw, nr = len(split["test_wrong"]), len(split["test_right"])
    names = {"A": "A  entangled, noisy sim", "B": "B  entangled, real hardware", "C": "C  no entangling gates",
             "D": "D  shuffled relation web", "E": "E  classical contradiction strength", "A0": "A0 entangled, noiseless (supplementary)"}
    nt = len(test)
    lines = [f"# Stage 2, run {RUN}: five arms on the {nt}-item test set", "",
             f"Pool: `results/{STAGE2_POOLS[RUN]}`.", "",
             f"Pre-registration: `experiments/preregistration.md`. Base model `{config.BASE_MODEL}` (DEVIATIONS.md, D5), "
             f"noise model and hardware `{config.IBM_BACKEND}`, {config.SHOTS} shots per arm, N={config.N_TROTTER} Trotter steps. "
             f"Test-set rule: {split['rule']}. "
             f"Test set: {nw} items the base model got wrong, {nr} it got right. Calibration pool: {len(split['calibration'])} items "
             f"({sum(not recs[q]['correct'] for q in split['calibration'])} wrong).", "",
             "## Five-arm table", "",
             f"| arm | threshold (from calibration) | calibration flag rate | wrong items flagged (of {nw}) | right items flagged (of {nr}) | AUROC test | AUROC calibration | judgment = model's answer (of {nt}) | judgment = truth (of {nt}) |",
             "|---|---|---|---|---|---|---|---|---|"]
    for arm in ("A", "B", "C", "D", "E", "A0"):
        s = summary.get(arm)
        if s is None:
            lines.append(f"| {names[arm]} | not run: {hardware.get('skipped_because')} | | | | | | | |")
            continue
        lines.append(f"| {names[arm]} | {fmt(s['threshold'], 3)} | {fmt(s['calibration_flag_fraction'])} | "
                     f"{s['test_wrong_flagged']} ({s['test_wrong_flagged'] / max(nw, 1):.0%}) | "
                     f"{s['test_right_flagged']} ({s['test_right_flagged'] / nr:.0%}) | {fmt(s['auroc_test'])} | "
                     f"{fmt(s['auroc_calibration'])} | {s['agree_with_model']} | {s['agree_with_truth']} |")
    lines += ["", "Arm E's judgment column is the sign of the confidence-weighted lean, not a conflict readout."]
    if split["rule"].startswith("fallback"):
        lines += ["", "**Caution:** under the fallback rule the right items are the correct answers whose claims gave the "
                  "model's answer the *least* support, chosen because they look least certain. Every arm should flag them "
                  "more often than a random correct item, so the right-item columns are biased upward and the AUROCs "
                  "compare wrong items against hard right items, not typical ones. The calibration pool holds no wrong "
                  "items, so calibration AUROC is undefined."]
    lines += ["",
              "## Hypotheses", ""]
    for h, v in hyp.items():
        lines.append(f"- **{h}**: {v['verdict'] if 'verdict' in v else ('criterion met' if v['criterion_met'] else 'criterion not met') + ('' if v['robust_to_one_item'] else ', not robust to one item')} — "
                     + ", ".join(f"{k}={fmt(x) if not isinstance(x, dict) else {a: round(b, 2) for a, b in x.items()}}"
                                 for k, x in v.items() if k != "verdict"))
    lines += ["", "## Hardware", ""]
    if hardware["ran"]:
        u = hardware["usage"]
        lines.append(f"Gate met. Job `{u['job_id']}` on `{u['backend']}` (Batch `{u['batch_id']}`), {nt} circuits × {u['shots']} shots, "
                     f"**{u['quantum_seconds']} QPU seconds**. Service-reported consumption after the job: "
                     f"{u['service_after']['usage_consumed_seconds']} s of {u['service_after']['usage_limit_seconds']} s.")
    else:
        lines.append(f"Arm B not submitted: {hardware['skipped_because']}. QPU seconds used before this decision: {hardware['qpu_seconds_before']:.0f}.")
    lines += ["", "## Per-item conflict scores (test set)", "",
              "| id | truth | model | qubits | relations | contradictions | CZ (A) | A | B | C | D | E | A0 | flagged by |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for q in test:
        s, r = sims[q], recs[q]
        sc = lambda a: fmt(s["arms"][a]["readout"]["conflict_score"], 3) if a in s["arms"] else "—"
        fl = [a for a in ("A", "B", "C", "D", "E", "A0") if a in s["arms"] and
              s["arms"][a]["readout"]["conflict_score"] > thresholds["A" if a == "B" else a]]
        lines.append(f"| {q} | {r['answer']} | {r['model_answer']}{'' if r['correct'] else ' ✗'} | {s['n_qubits']} | "
                     f"{s['n_edges']} | {s['n_contradictions']} | {s['arms']['A']['cz']} | {sc('A')} | {sc('B')} | {sc('C')} | "
                     f"{sc('D')} | {sc('E')} | {sc('A0')} | {', '.join(fl) or '—'} |")
    OUT_MD.write_text("\n".join(lines) + "\n")
    print("\n".join(lines[:40]))


def md_only() -> None:
    d = json.loads(OUT_JSON.read_text())
    recs = {r["id"]: r for r in json.loads(POOL.read_text())["records"]}
    write_md(recs, d["split"], d["items"], d["summary"], d["hypotheses"], d["hardware"], d["thresholds"])


if __name__ == "__main__":
    md_only() if "--md-only" in sys.argv else main()

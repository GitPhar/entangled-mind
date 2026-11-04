"""Export data for the window (window/index.html): one JSON file per Stage 2 item.

For every item in results/stage2-run-1.json and results/stage2-run-2.json this rebuilds
the arm-A circuit with src/entangled_mind (read-only: encoder.build_web, build_circuit,
solve_phases; readout weights and thresholds) and computes the NOISELESS statevector
at each stage:

    encode     after RY(theta) RZ(phi) on every qubit (a product state)
    entangle   after the RZZ gates for every related pair
    evolve k   after Trotter step k (k = 1..N)
    collapse   the yes/no (X-basis) measurement distribution of the final state

At every stage it stores, per qubit, the reduced Bloch vector (amplitude = equatorial
length, phase = azimuth, 0 = yes, pi = no), P(yes-aligned), and purity; the negativity of
the two-qubit reduced state of every related pair; and the vote distribution and conflict
score the readout would give if the state were measured there. The same stages are
computed for the arm-C circuit (no two-qubit terms) for comparison.

It also copies the archived readouts (conflict score, judgment, raw counts) of every arm
and flags each arm by its own calibration threshold, exactly as in the run.

Checks (the run stops if either fails):
  * the staged evolution reproduces Statevector(build_circuit(measure=False)) exactly;
  * the exact final conflict score matches archived arm A0 (1,000 noiseless shots) within
    sampling noise (|difference| < 0.12 on every item; the mean is reported).

The index also carries an exploratory (not pre-registered) number per run: the test-set
AUROC of the exact conflict score if the state were read out at each stage, for A and C.

    .venv/bin/python experiments/export_window.py

Writes window/data/<item>.json and window/data/index.json. Nothing else is touched."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from entangled_mind import config, encoder, readout  # noqa: E402

OUT = ROOT / "window" / "data"
RUNS = {1: "pool-run-2.json", 2: "pool-run-3.json"}       # as in experiments/stage2_run.py
ARMS = ("A", "B", "C", "D", "E", "A0")
ARM_LABEL = {"A": "entangled, noisy simulator", "B": "entangled, real hardware",
             "C": "no entangling gates", "D": "shuffled relation web",
             "E": "classical contradiction strength", "A0": "entangled, noiseless"}
BINS = 21                                                    # vote histogram over [-1, 1]


# ---------------------------------------------------------------- stages ----

def stage_bounds(web: encoder.Web, entangle: bool) -> list[tuple[str, int]]:
    """Instruction index at the end of each stage of build_circuit(measure=False)."""
    n, e = web.n, len(web.edges) if entangle else 0
    lean = int(np.count_nonzero(web.lean))
    k = 2 * n
    out = [("encode", k)]
    k += e
    out.append(("entangle", k))
    for step in range(1, config.N_TROTTER + 1):
        k += n + e + lean + n + n          # H layer, RZZ, lean RZ, H layer, mixer RZ
        out.append((f"evolve {step}", k))
    return out


def evolve_stages(qc: QuantumCircuit, bounds: list[tuple[str, int]]) -> list[tuple[str, Statevector]]:
    sv, prev, out = Statevector.from_label("0" * qc.num_qubits), 0, []
    for name, b in bounds:
        part = qc.copy_empty_like()
        for inst in qc.data[prev:b]:
            part.append(inst)
        sv, prev = sv.evolve(part), b
        out.append((name, sv))
    if prev != len(qc.data):
        raise SystemExit(f"stage bounds cover {prev} of {len(qc.data)} instructions")
    return out


# ------------------------------------------------------- state analysis ----

def tensor(sv: Statevector, n: int) -> np.ndarray:
    return np.asarray(sv.data).reshape([2] * n)     # axis a <-> qubit n-1-a (little-endian)


def rho_1(psi: np.ndarray, n: int, k: int) -> np.ndarray:
    a = n - 1 - k
    m = np.moveaxis(psi, a, 0).reshape(2, -1)
    return m @ m.conj().T


def rho_2(psi: np.ndarray, n: int, i: int, j: int) -> np.ndarray:
    ai, aj = n - 1 - i, n - 1 - j
    m = np.moveaxis(psi, (ai, aj), (0, 1)).reshape(4, -1)   # row index = 2*b_i + b_j
    return m @ m.conj().T


def negativity(r: np.ndarray) -> float:
    pt = r.reshape(2, 2, 2, 2).transpose(0, 3, 2, 1).reshape(4, 4)   # transpose qubit j
    ev = np.linalg.eigvalsh((pt + pt.conj().T) / 2)
    return float(-ev[ev < 0].sum())


def x_basis_probs(sv: Statevector, n: int) -> np.ndarray:
    h = QuantumCircuit(n)
    h.h(range(n))
    return np.abs(sv.evolve(h).data) ** 2


def votes(n: int, w: np.ndarray) -> np.ndarray:
    idx = np.arange(2 ** n)
    bits = (idx[:, None] >> np.arange(n)[None, :]) & 1        # bit k = qubit k; 0 = yes
    return (1 - 2 * bits) @ w


def vote_summary(p: np.ndarray, m: np.ndarray) -> dict:
    tau = config.STRONG_TAU
    p_yes = float(p[m > 1e-12].sum() + 0.5 * p[np.abs(m) <= 1e-12].sum())
    sy, sn = float(p[m >= tau - 1e-12].sum()), float(p[m <= -tau + 1e-12].sum())
    hist, _ = np.histogram(np.clip(m, -1, 1), bins=BINS, range=(-1, 1), weights=p)
    return {"p_yes": r4(p_yes), "p_strong_yes": r4(sy), "p_strong_no": r4(sn),
            "conflict_score": r4(2 * min(sy, sn)), "vote_hist": [r4(x) for x in hist]}


def counts_summary(counts: dict, w: np.ndarray) -> dict:
    shots = sum(counts.values())
    ms = np.array([readout.magnetisation(b, w) for b in counts])
    cs = np.array(list(counts.values()), float) / shots
    hist, _ = np.histogram(np.clip(ms, -1, 1), bins=BINS, range=(-1, 1), weights=cs)
    return {"shots": shots, "distinct": len(counts), "vote_hist": [r4(x) for x in hist]}


def analyse(stages, web: encoder.Web, w: np.ndarray, m: np.ndarray, with_pairs: bool) -> list[dict]:
    n, out = web.n, []
    for name, sv in stages:
        psi = tensor(sv, n)
        qubits = []
        for k in range(n):
            r = rho_1(psi, n, k)
            x, y, z = 2 * r[0, 1].real, -2 * r[0, 1].imag, (r[0, 0] - r[1, 1]).real
            qubits.append({"amp": r4(math.hypot(x, y)), "phase": r4(math.atan2(y, x)),
                           "p_yes": r4((1 + x) / 2), "bloch": [r4(x), r4(y), r4(z)],
                           "purity": r4(float(np.trace(r @ r).real))})
        st = {"stage": name, "qubits": qubits, **vote_summary(x_basis_probs(sv, n), m)}
        if with_pairs:
            st["negativity"] = [r4(negativity(rho_2(psi, n, i, j))) for i, j, _ in web.edges]
        out.append(st)
    return out


def r4(x: float) -> float:
    return round(float(x), 4)


# ------------------------------------------------------------------ main ----

def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    index = {"generated_by": "experiments/export_window.py", "noise": "stages are noiseless statevectors; "
             "archived arm readouts are as run (A, C, D: noisy simulator from ibm_fez; A0: noiseless sampling)",
             "constants": {"kappa": config.KAPPA, "n_trotter": config.N_TROTTER, "gamma0": config.GAMMA0,
                           "beta0": config.BETA0, "tau": config.STRONG_TAU, "shots": config.SHOTS},
             "arm_labels": ARM_LABEL, "runs": {}, "items": []}
    diffs = []
    for run, pool_file in RUNS.items():
        res = json.loads((config.RESULTS / f"stage2-run-{run}.json").read_text())
        pool = {r["id"]: r for r in json.loads((config.RESULTS / pool_file).read_text())["records"]}
        split, thr = res["split"], res["thresholds"]
        role = {**{q: "test_wrong" for q in split["test_wrong"]}, **{q: "test_right" for q in split["test_right"]},
                **{q: "calibration" for q in split["calibration"]}}
        index["runs"][run] = {"pool": pool_file, "rule": split["rule"], "thresholds": thr,
                              "summary": res["summary"], "hypotheses": res["hypotheses"]}
        for qid, sim in sorted(res["items"].items()):
            rec = pool[qid]
            web = encoder.build_web(rec["contentions"], rec["pairs"])
            n = web.n
            w = readout._weights(web)
            m = votes(n, w)
            qa = encoder.build_circuit(web, entangle=True, measure=False)
            qc_ = encoder.build_circuit(web, entangle=False, measure=False)
            st_a = evolve_stages(qa, stage_bounds(web, True))
            st_c = evolve_stages(qc_, stage_bounds(web, False))
            if not np.allclose(st_a[-1][1].data, Statevector(qa).data, atol=1e-9):
                raise SystemExit(f"{qid}: staged evolution does not reproduce the circuit")
            a_stages = analyse(st_a, web, w, m, with_pairs=True)
            c_stages = analyse(st_c, web, w, m, with_pairs=False)
            final = a_stages[-1]
            a0 = sim["arms"]["A0"]["readout"]["conflict_score"]
            diffs.append(abs(final["conflict_score"] - a0))
            if diffs[-1] > 0.12:
                raise SystemExit(f"{qid}: exact conflict {final['conflict_score']} vs archived A0 {a0}")

            arms = {}
            for arm in ARMS:
                if arm not in sim["arms"]:
                    continue
                ro = sim["arms"][arm]["readout"]
                t = thr.get(arm, thr["A"] if arm == "B" else None)
                entry = {"label": ARM_LABEL[arm], "conflict_score": r4(ro["conflict_score"]),
                         "threshold": r4(t), "flagged": bool(ro["conflict_score"] > t),
                         "judgment": ro["judgment"]}
                if "p_yes" in ro:
                    entry["p_yes"] = r4(ro["p_yes"])
                if arm == "E":
                    entry["contradiction_count"] = ro["contradiction_count"]
                if "counts" in sim["arms"][arm]:
                    wd = readout._weights(encoder.shuffled_web(web, seed=config.SHUFFLE_SEED * 1000 + int(qid[1:]))) \
                        if arm == "D" else w
                    entry["counts_summary"] = counts_summary(sim["arms"][arm]["counts"], wd)
                    entry["counts"] = sim["arms"][arm]["counts"]
                for k in ("cz", "depth"):
                    if k in sim["arms"][arm]:
                        entry[k] = sim["arms"][arm][k]
                arms[arm] = entry

            phases = encoder.solve_phases(web)
            item = {
                "id": qid, "run": run, "role": role.get(qid, "excluded"), "category": rec.get("category"),
                "question": rec["question"], "truth": rec["answer"], "model_answer": rec["model_answer"],
                "correct": rec["correct"], "source": rec.get("source"),
                "claims": [{"text": c["text"], "confidence": c["confidence"], "lean": c["lean"],
                            "theta": r4(c["confidence"] * math.pi / 2), "phi": r4(phases[k])}
                           for k, c in enumerate(rec["contentions"])],
                "relations": [{"i": i, "j": j, "J": r4(J), "relation": "supports" if J > 0 else "contradicts"}
                              for i, j, J in web.edges],
                "readout_weights": [r4(x) for x in w],
                "stages": a_stages + [{"stage": "collapse", **{k: final[k] for k in
                                       ("p_yes", "p_strong_yes", "p_strong_no", "conflict_score", "vote_hist")}}],
                "stages_unentangled": c_stages,
                "arms": arms,
            }
            (OUT / f"{qid}.json").write_text(json.dumps(item, separators=(",", ":"), ensure_ascii=False))
            index["items"].append({
                "id": qid, "run": run, "role": item["role"], "category": item["category"],
                "question": rec["question"][:140], "truth": rec["answer"], "model_answer": rec["model_answer"],
                "correct": rec["correct"], "n_qubits": n, "n_relations": len(web.edges),
                "n_contradictions": sum(J < 0 for _, _, J in web.edges),
                "flags": {a: arms[a]["flagged"] for a in arms},
                "scores": {a: arms[a]["conflict_score"] for a in arms},
                "max_negativity": max([max(s["negativity"], default=0) for s in a_stages], default=0),
                "stage_conflict": {"A": [s["conflict_score"] for s in a_stages],
                                   "C": [s["conflict_score"] for s in c_stages]},
            })
        # Exploratory (not pre-registered): test-set AUROC of the exact conflict score read at each stage.
        test = [i for i in index["items"] if i["run"] == run and i["role"].startswith("test")]
        names = [s for s, _ in stage_bounds(encoder.Web(np.ones(1), np.ones(1), ()), True)]
        index["runs"][run]["stage_auroc_exploratory"] = {
            arm: {name: r4(readout.auroc([i["stage_conflict"][arm][k] for i in test if i["correct"] is False],
                                         [i["stage_conflict"][arm][k] for i in test if i["correct"] is True]))
                  for k, name in enumerate(names)} for arm in ("A", "C")}
        print(f"run {run}: {sum(1 for i in index['items'] if i['run'] == run)} items;",
              "stage AUROC", index["runs"][run]["stage_auroc_exploratory"])
    index["check"] = {"exact_vs_archived_A0_conflict_mean_abs_diff": r4(np.mean(diffs)),
                      "max_abs_diff": r4(np.max(diffs)), "items": len(diffs)}
    (OUT / "index.json").write_text(json.dumps(index, separators=(",", ":"), ensure_ascii=False))
    print("check:", index["check"])


if __name__ == "__main__":
    main()

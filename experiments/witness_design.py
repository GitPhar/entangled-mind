"""Design (not submission) of the entanglement-witness measurement in
experiments/witness.md: runs the exact hardware protocol on the noisy simulator
built from the real backend, and estimates QPU time.

    python experiments/witness_design.py

Protocol per item: arm A's belief state (no final readout rotation), then on
the target pair (i, j) one of the 9 local Pauli settings {X,Y,Z}x{X,Y,Z}; only
qubits i and j are measured. Four readout-calibration circuits (|00>,|01>,|10>,
|11> on the same physical qubits) give an assignment matrix for mitigation.
Two-qubit state by linear inversion; witness = negativity of the partial
transpose; entanglement is certified if the bootstrap 95% lower bound > 0.
Nothing here submits to hardware."""

import json

import numpy as np
from qiskit import ClassicalRegister, QuantumCircuit
from qiskit.quantum_info import Statevector, partial_trace

from entangled_mind import backends, config, encoder

POOL = config.RESULTS / "pool-run-3.json"
OUT = config.RESULTS / "witness-design.json"
N_ITEMS, SHOTS, N_BOOT = 3, 4000, 500
PAULI = {"I": np.eye(2), "X": np.array([[0, 1], [1, 0]]), "Y": np.array([[0, -1j], [1j, 0]]),
         "Z": np.diag([1.0, -1.0])}
SETTINGS = [a + b for a in "XYZ" for b in "XYZ"]


def negativity(rho: np.ndarray) -> float:
    pt = rho.reshape(2, 2, 2, 2).transpose(0, 3, 2, 1).reshape(4, 4)
    ev = np.linalg.eigvalsh((pt + pt.conj().T) / 2)
    return float(-ev[ev < 0].sum())


def ideal_pair(web):
    sv = Statevector(encoder.build_circuit(web, measure=False))
    best = None
    for i, j, J in web.edges:
        rho = partial_trace(sv, [k for k in range(web.n) if k not in (i, j)]).data
        n = negativity(rho)
        if best is None or n > best[0]:
            best = (n, i, j, J, rho)
    return best


def setting_circuit(web, i: int, j: int, setting: str) -> QuantumCircuit:
    qc = encoder.build_circuit(web, measure=False)
    for q, b in ((i, setting[0]), (j, setting[1])):
        if b == "X":
            qc.h(q)
        elif b == "Y":
            qc.sdg(q)
            qc.h(q)
    qc.add_register(ClassicalRegister(2, "meas"))
    qc.measure(i, 0)
    qc.measure(j, 1)
    return qc


def calib_circuits(isa_ref: QuantumCircuit, phys: tuple[int, int]) -> list[QuantumCircuit]:
    out = []
    for bits in ("00", "01", "10", "11"):          # bits = (j, i) in Qiskit order
        qc = QuantumCircuit(isa_ref.num_qubits, 2)
        if bits[1] == "1":
            qc.x(phys[0])
        if bits[0] == "1":
            qc.x(phys[1])
        qc.measure(phys[0], 0)
        qc.measure(phys[1], 1)
        out.append(qc)
    return out


def physical_of(isa: QuantumCircuit) -> tuple[int, int]:
    phys = {}
    for inst in isa.data:
        if inst.operation.name == "measure":
            phys[isa.find_bit(inst.clbits[0]).index] = isa.find_bit(inst.qubits[0]).index
    return phys[0], phys[1]


def probs(counts: dict) -> np.ndarray:
    v = np.array([counts.get(b, 0) for b in ("00", "01", "10", "11")], float)
    return v / v.sum()


def reconstruct(setting_probs: dict, A_inv: np.ndarray) -> np.ndarray:
    """Linear inversion from mitigated probabilities; outcome index = 2*b_j + b_i."""
    sign = {0: 1, 1: -1}
    exp = {"II": 1.0}
    for s, p in setting_probs.items():
        p = A_inv @ p
        for k, pk in enumerate(p):
            bi, bj = k & 1, k >> 1
            exp[s] = exp.get(s, 0) + sign[bi] * sign[bj] * pk
            exp[s[0] + "I"] = exp.get(s[0] + "I", 0) + sign[bi] * pk / 3
            exp["I" + s[1]] = exp.get("I" + s[1], 0) + sign[bj] * pk / 3
    rho = sum(exp[a + b] * np.kron(PAULI[b], PAULI[a]) for a in "IXYZ" for b in "IXYZ") / 4
    # project to the nearest physical state (clip negative eigenvalues, renormalise)
    w, v = np.linalg.eigh((rho + rho.conj().T) / 2)
    w = np.clip(w, 0, None)
    return (v * (w / w.sum())) @ v.conj().T


def main() -> None:
    pool = json.loads(POOL.read_text())
    recs = {r["id"]: r for r in pool["records"]}
    test = pool["split"]["test_wrong"] + pool["split"]["test_right"]
    cands = []
    for q in test:
        web = encoder.build_web(recs[q]["contentions"], recs[q]["pairs"])
        cands.append((ideal_pair(web), q, web))
    cands.sort(key=lambda t: -t[0][0])
    be = backends.backend()
    rep_delay = float(getattr(be.configuration(), "default_rep_delay", 250e-6) or 250e-6)
    if rep_delay > 1:            # some backends report microseconds
        rep_delay *= 1e-6
    rng = np.random.default_rng(5)
    report = {"shots_per_circuit": SHOTS, "rep_delay_s": rep_delay, "items": []}
    total_shot_time = 0.0
    n_circuits = 0
    for (n_ideal, i, j, J, rho_ideal), q, web in cands[:N_ITEMS]:
        isas = [backends.transpile(setting_circuit(web, i, j, s)) for s in SETTINGS]
        phys = physical_of(isas[0])
        cals = [backends.transpile(c) for c in calib_circuits(isas[0], phys)]
        sim = backends.noisy_simulator()
        res = sim.run(isas + cals, shots=SHOTS, seed_simulator=7).result()
        counts = [res.get_counts(k) for k in range(len(isas) + len(cals))]
        A = np.column_stack([probs(c) for c in counts[len(isas):]])
        A_inv = np.linalg.inv(A)
        sp = {s: probs(c) for s, c in zip(SETTINGS, counts[:len(isas)])}
        n_noisy = negativity(reconstruct(sp, A_inv))
        boot = []
        for _ in range(N_BOOT):
            spb = {s: rng.multinomial(SHOTS, p) / SHOTS for s, p in sp.items()}
            boot.append(negativity(reconstruct(spb, A_inv)))
        lo = float(np.percentile(boot, 2.5))
        durs = [c.estimate_duration(be.target) for c in isas + cals]
        total_shot_time += sum(SHOTS * (d + rep_delay) for d in durs)
        n_circuits += len(durs)
        report["items"].append({
            "id": q, "pair": [i, j], "coupling_J": J, "n_qubits": web.n,
            "cz_per_setting": int(isas[0].count_ops().get("cz", 0)),
            "physical_qubits": list(phys),
            "negativity_ideal": n_ideal, "negativity_noisy_sim": n_noisy,
            "noisy_sim_bootstrap_95_lower": lo, "certified_on_noisy_sim": lo > 0,
            "circuit_duration_s": float(np.mean(durs[:len(isas)])),
        })
        print(report["items"][-1], flush=True)
    report["n_circuits"] = n_circuits
    report["estimated_shot_time_s"] = total_shot_time
    report["estimated_qpu_seconds"] = total_shot_time + 5.0    # + per-job overhead allowance
    OUT.write_text(json.dumps(report, indent=1))
    print({k: v for k, v in report.items() if k != "items"})


if __name__ == "__main__":
    main()

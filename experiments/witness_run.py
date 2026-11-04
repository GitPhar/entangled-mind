"""Entanglement-witness run 1 on real hardware, exactly as designed in
experiments/witness.md: 3 items x (9 Pauli settings + 4 readout-calibration
circuits) = 39 circuits, 4,000 shots each, one SamplerV2 job in one Batch.

Readout-calibration circuits are built directly on the two physical qubits each
item's settings measure, and submitted untranspiled (x and measure are native),
so the mitigation matrix comes from the same qubits (DEVIATIONS.md, D8). The
noisy-simulator prediction is recomputed with the same corrected calibration.

Writes results/witness-run-1.{json,md}; QPU usage goes to results/ibm-usage.md."""

import json

import numpy as np
from qiskit import ClassicalRegister, QuantumCircuit

import witness_design as wd
from entangled_mind import backends, config

DESIGN = config.RESULTS / "witness-design.json"
OUT_JSON = config.RESULTS / "witness-run-1.json"
OUT_MD = config.RESULTS / "witness-run-1.md"
POOL = config.RESULTS / "pool-run-3.json"


def calib_on(n_phys: int, phys: tuple[int, int]) -> list[QuantumCircuit]:
    out = []
    for bits in ("00", "01", "10", "11"):          # bits = (b_j, b_i), Qiskit order
        qc = QuantumCircuit(n_phys)
        qc.add_register(ClassicalRegister(2, "meas"))
        if bits[1] == "1":
            qc.x(phys[0])
        if bits[0] == "1":
            qc.x(phys[1])
        qc.measure(phys[0], 0)
        qc.measure(phys[1], 1)
        out.append(qc)
    return out


def analyse(counts: list[dict], n_settings: int, rng) -> dict:
    A = np.column_stack([wd.probs(c) for c in counts[n_settings:]])
    A_inv = np.linalg.inv(A)
    sp = {s: wd.probs(c) for s, c in zip(wd.SETTINGS, counts[:n_settings])}
    n = wd.negativity(wd.reconstruct(sp, A_inv))
    n_raw = wd.negativity(wd.reconstruct(sp, np.eye(4)))
    boot = [wd.negativity(wd.reconstruct({s: rng.multinomial(wd.SHOTS, p) / wd.SHOTS for s, p in sp.items()}, A_inv))
            for _ in range(wd.N_BOOT)]
    lo, hi = np.percentile(boot, [2.5, 97.5])
    return {"negativity": n, "negativity_unmitigated": n_raw, "ci95": [float(lo), float(hi)],
            "certified": bool(lo > 0), "assignment_matrix": A.tolist()}


def main() -> None:
    design = json.loads(DESIGN.read_text())
    recs = {r["id"]: r for r in json.loads(POOL.read_text())["records"]}
    from entangled_mind import encoder
    circuits, layout = [], []
    for it in design["items"]:
        web = encoder.build_web(recs[it["id"]]["contentions"], recs[it["id"]]["pairs"])
        i, j = it["pair"]
        isas = [backends.transpile(wd.setting_circuit(web, i, j, s)) for s in wd.SETTINGS]
        phys = wd.physical_of(isas[0])
        assert all(wd.physical_of(c) == phys for c in isas), "settings landed on different qubits"
        cals = calib_on(isas[0].num_qubits, phys)
        layout.append((it, phys, len(circuits)))
        circuits += isas + cals
    assert len(circuits) == 39

    sim = backends.noisy_simulator().run(circuits, shots=wd.SHOTS, seed_simulator=7).result()
    sim_counts = [sim.get_counts(k) for k in range(len(circuits))]
    hw_counts, usage = backends.run_hardware(circuits, purpose="Entanglement witness run 1 (39 circuits)",
                                             shots=wd.SHOTS)
    rng = np.random.default_rng(5)
    items = []
    for it, phys, start in layout:
        block = slice(start, start + 13)
        items.append({"id": it["id"], "pair": it["pair"], "physical_qubits": list(phys),
                      "negativity_ideal": it["negativity_ideal"],
                      "noisy_sim": analyse(sim_counts[block], 9, rng),
                      "hardware": analyse(hw_counts[block], 9, rng),
                      "hardware_counts": hw_counts[block]})
    n_cert = sum(x["hardware"]["certified"] for x in items)
    OUT_JSON.write_text(json.dumps({"usage": usage, "items": items, "n_certified": n_cert,
                                    "success": n_cert >= 2}, indent=1))
    write_md(json.loads(OUT_JSON.read_text()))


def write_md(d: dict) -> None:
    """Witness markdown, from the archived JSON alone."""
    usage, items, n_cert = d["usage"], d["items"], d["n_certified"]
    qsec = float((usage.get("job_metrics_usage") or {}).get("qpu_charge_time_seconds", usage["quantum_seconds"]))
    lines = ["# Entanglement witness, run 1 (real hardware)", "",
             f"Design: `experiments/witness.md`. Job `{usage['job_id']}` on `{usage['backend']}` (Batch `{usage['batch_id']}`), "
             f"39 circuits × {wd.SHOTS} shots. **QPU time: {qsec:g} s** (IBM `qpu_charge_time_seconds`). "
             f"Service-reported consumption after the job: {usage['service_after']['usage_consumed_seconds']} s "
             f"of {usage['service_after']['usage_limit_seconds']} s.", "",
             "Witness: negativity N of the two-qubit reduced state of the most-entangled related pair "
             "(N > 0 ⇔ entangled; separable states give 0; a Bell pair gives 0.5). Readout-error mitigated; "
             "95% intervals from 500 parametric bootstrap resamples. Certified if the lower bound > 0.", "",
             "| item | pair (physical qubits) | N ideal | N noisy sim [95% CI] | **N hardware [95% CI]** | hardware, unmitigated | certified |",
             "|---|---|---|---|---|---|---|"]
    for x in items:
        s_, h = x["noisy_sim"], x["hardware"]
        lines.append(f"| `{x['id']}` | ({x['pair'][0]}, {x['pair'][1]}) on {x['physical_qubits'][0]}, {x['physical_qubits'][1]} | "
                     f"{x['negativity_ideal']:.3f} | {s_['negativity']:.3f} [{s_['ci95'][0]:.3f}, {s_['ci95'][1]:.3f}] | "
                     f"**{h['negativity']:.3f} [{h['ci95'][0]:.3f}, {h['ci95'][1]:.3f}]** | {h['negativity_unmitigated']:.3f} | "
                     f"{'yes' if h['certified'] else 'no'} |")
    lines += ["", f"**{n_cert} of 3 items certified; pre-registered success rule (≥ 2 of 3): "
              f"{'met' if n_cert >= 2 else 'not met'}.**"]
    OUT_MD.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()

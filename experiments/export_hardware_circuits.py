"""Export the exact as-run hardware circuits from IBM's job records (ground truth for the
window's circuit strip; re-transpiling today drifts, e.g. 170 vs 162 CZ on h046).

    python experiments/export_hardware_circuits.py

For each circuit of the Stage 1 job and of the witness batch, writes
window/data/hardware/<job>-<circuit index>.json with the ordered gate list
(gate, physical qubits, angles), the logical-claim -> physical-qubit layout (initial
and final, from the transpiler layout stored with the job), and what the circuit is;
and window/hardware/<job>-<circuit index>.svg, the circuit drawn from the job record
with Qiskit's circuit drawer (idle wires hidden, unfolded). Needs matplotlib and pylatexenc."""

import json

from entangled_mind import backends, config

OUT = config.ROOT / "window" / "data" / "hardware"
SVG = config.ROOT / "window" / "hardware"
JOBS = {"dbl423dgg49c73dk0db0": "stage1", "dbl6e1d8mdtc73d5gesg": "witness"}
SETTINGS = [a + b for a in "XYZ" for b in "XYZ"]
CALIB = ["00", "01", "10", "11"]


def describe(kind: str, k: int) -> dict:
    if kind == "stage1":
        return {"purpose": "Stage 1 pipe test", "item": "q01", "pool": "results/pool-run-1.json",
                "note": "arm-A circuit, N = 0 evolution, X-basis readout"}
    design = json.loads((config.RESULTS / "witness-design.json").read_text())["items"]
    item = design[k // 13]
    r = k % 13
    base = {"purpose": "entanglement witness run 1", "item": item["id"], "pool": "results/pool-run-3.json",
            "target_pair_claims": item["pair"]}
    if r < 9:
        return {**base, "role": "tomography setting", "setting": SETTINGS[r],
                "note": f"arm-A belief state; claim {item['pair'][0]} measured in {SETTINGS[r][0]}, "
                        f"claim {item['pair'][1]} in {SETTINGS[r][1]}"}
    return {**base, "role": "readout calibration", "prepared_bits": CALIB[r - 9],
            "note": "built directly on the measured physical qubits and submitted untranspiled (DEVIATIONS.md, D8)"}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SVG.mkdir(parents=True, exist_ok=True)
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    svc = backends.service()
    index = []
    for jid, kind in JOBS.items():
        job = svc.job(jid)
        for k, pub in enumerate(job.inputs["pubs"]):
            qc = pub.circuit if hasattr(pub, "circuit") else pub[0]
            gates = []
            for inst in qc.data:
                if inst.operation.name == "barrier":
                    continue
                g = {"gate": inst.operation.name, "qubits": [qc.find_bit(q).index for q in inst.qubits]}
                if inst.operation.params:
                    g["params"] = [float(p) for p in inst.operation.params]
                if inst.clbits:
                    g["clbits"] = [qc.find_bit(c).index for c in inst.clbits]
                gates.append(g)
            layout = {}
            if qc.layout is not None:
                n_logical = len(qc.layout.input_qubit_mapping) if qc.layout.input_qubit_mapping else qc.num_qubits
                init = qc.layout.initial_index_layout(filter_ancillas=True)
                fin = qc.layout.final_index_layout(filter_ancillas=True)
                layout = {"initial": list(init), "final": list(fin),
                          "initial_logical_to_physical": {str(i): p for i, p in enumerate(init)},
                          "final_logical_to_physical": {str(i): p for i, p in enumerate(fin)},
                          "n_logical": len(init)}
            else:
                layout = {"note": "no transpiler layout: circuit was built on physical qubits directly"}
            active = sorted({q for g in gates for q in g["qubits"]})
            rec = {"job_id": jid, "backend": job.backend().name, "circuit_index": k, **describe(kind, k),
                   "layout": layout, "active_physical_qubits": active,
                   "counts": {name: int(c) for name, c in qc.count_ops().items()},
                   "n_gates": len(gates), "gates": gates}
            fig = qc.draw(output="mpl", idle_wires=False, fold=-1)
            fig.savefig(SVG / f"{jid}-{k}.svg", format="svg", bbox_inches="tight")
            plt.close(fig)
            rec["svg"] = f"window/hardware/{jid}-{k}.svg"
            path = OUT / f"{jid}-{k}.json"
            path.write_text(json.dumps(rec))
            index.append({"file": path.name, "job_id": jid, "circuit_index": k, "item": rec["item"],
                          "role": rec.get("role", "arm-A circuit"), "setting": rec.get("setting") or rec.get("prepared_bits"),
                          "cz": rec["counts"].get("cz", 0)})
    (OUT / "index.json").write_text(json.dumps(index, indent=1))
    print(len(index), "circuits exported")
    for e in index[:3] + index[-2:]:
        print(e)


if __name__ == "__main__":
    main()

"""Log ibm_fez's calibration at job time for the two hardware jobs.

    python experiments/ibm_calibration.py

For each job, reads backend.properties(datetime=<job execution start>) and reports, for
the physical qubits and CZ pairs the as-run circuits actually used
(window/data/hardware/*.json): T1, T2, readout error, single-qubit (sx) error, and CZ
error. Writes results/ibm-calibration.{md,json}."""

import datetime as dt
import json
from collections import defaultdict

import numpy as np

from entangled_mind import backends, config

HW = config.ROOT / "window" / "data" / "hardware"
OUT_MD = config.RESULTS / "ibm-calibration.md"
OUT_JSON = config.RESULTS / "ibm-calibration.json"
JOBS = {"dbl423dgg49c73dk0db0": "Stage 1 pipe test", "dbl6e1d8mdtc73d5gesg": "Entanglement witness run 1"}


def qprop(props, q, name):
    try:
        v = props.qubit_property(q, name)
        return float(v[0]) if isinstance(v, tuple) else float(v)
    except Exception:
        return None


def gerr(props, gate, qubits):
    try:
        return float(props.gate_error(gate, qubits))
    except Exception:
        return None


def main() -> None:
    svc, be = backends.service(), backends.backend()
    out, lines = {}, ["# ibm_fez calibration at job time", "",
                      "Calibration data are read from `backend.properties(datetime=...)` at each job's execution start. "
                      "They cover the physical qubits and CZ pairs that the as-run circuits used (`window/data/hardware/`). "
                      "T1 and T2 are in µs; errors are probabilities.", ""]
    for jid, label in JOBS.items():
        job = svc.job(jid)
        ts = job.metrics().get("timestamps", {})
        when = dt.datetime.fromisoformat((ts.get("running") or ts["created"]).replace("Z", "+00:00"))
        props = be.properties(datetime=when)
        qubits, pairs, measured = set(), set(), set()
        for f in sorted(HW.glob(f"{jid}-*.json")):
            rec = json.loads(f.read_text())
            for g in rec["gates"]:
                qubits.update(g["qubits"])
                if g["gate"] == "cz":
                    pairs.add(tuple(sorted(g["qubits"])))
                if g["gate"] == "measure":
                    measured.update(g["qubits"])
        qrows = []
        for q in sorted(qubits):
            qrows.append({"qubit": q, "measured": q in measured,
                          "T1_us": (qprop(props, q, "T1") or 0) * 1e6 or None,
                          "T2_us": (qprop(props, q, "T2") or 0) * 1e6 or None,
                          "readout_error": qprop(props, q, "readout_error"),
                          "sx_error": gerr(props, "sx", [q])})
        prow = [{"pair": list(p), "cz_error": gerr(props, "cz", list(p)) if gerr(props, "cz", list(p)) is not None
                 else gerr(props, "cz", list(p[::-1]))} for p in sorted(pairs)]
        def stat(vals):
            v = np.array([x for x in vals if x is not None], float)
            return {"median": float(np.median(v)), "min": float(v.min()), "max": float(v.max())} if len(v) else None
        summary = {"T1_us": stat([r["T1_us"] for r in qrows]), "T2_us": stat([r["T2_us"] for r in qrows]),
                   "readout_error": stat([r["readout_error"] for r in qrows]),
                   "sx_error": stat([r["sx_error"] for r in qrows]), "cz_error": stat([r["cz_error"] for r in prow])}
        out[jid] = {"label": label, "calibration_time": str(props.last_update_date), "job_running": str(when),
                    "qubits": qrows, "cz_pairs": prow, "summary": summary}
        lines += [f"## {label}: job `{jid}`", "",
                  f"Job ran at {when:%Y-%m-%d %H:%M UTC}. Calibration snapshot: {props.last_update_date}. "
                  f"{len(qrows)} physical qubits used ({len(measured)} measured), {len(prow)} CZ pairs.", "",
                  "| quantity | median | min | max |", "|---|---|---|---|"]
        for k, s in summary.items():
            if s:
                fmt = (lambda x: f"{x:.1f}") if k.endswith("_us") else (lambda x: f"{x:.2e}")
                lines.append(f"| {k} | {fmt(s['median'])} | {fmt(s['min'])} | {fmt(s['max'])} |")
        lines += ["", "Measured qubits:", "", "| qubit | T1 µs | T2 µs | readout error | sx error |", "|---|---|---|---|---|"]
        for r in qrows:
            if r["measured"]:
                f = lambda x, p: "—" if x is None else (f"{x:.1f}" if p else f"{x:.2e}")
                lines.append(f"| {r['qubit']} | {f(r['T1_us'], 1)} | {f(r['T2_us'], 1)} | {f(r['readout_error'], 0)} | {f(r['sx_error'], 0)} |")
        lines.append("")
    OUT_JSON.write_text(json.dumps(out, indent=1))
    OUT_MD.write_text("\n".join(lines) + "\n")
    print("\n".join(lines[:30]))


if __name__ == "__main__":
    main()

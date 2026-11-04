"""IBM Quantum access, the noisy simulator built from the real backend, and
QPU usage accounting. Real-hardware submissions go only through `run_hardware`,
which refuses to submit once cumulative usage reaches the hard stop."""

from __future__ import annotations

import datetime as dt
import json
import os
from functools import lru_cache

from dotenv import load_dotenv
from qiskit import QuantumCircuit
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_aer import AerSimulator

from . import config

load_dotenv(config.ROOT / ".env")
USAGE_MD = config.RESULTS / "ibm-usage.md"
USAGE_JSON = config.RESULTS / "ibm-usage.json"


@lru_cache(maxsize=1)
def service():
    from qiskit_ibm_runtime import QiskitRuntimeService
    return QiskitRuntimeService(channel=config.IBM_CHANNEL, token=os.environ["IBM_QUANTUM_TOKEN"],
                                instance=config.IBM_INSTANCE)


@lru_cache(maxsize=1)
def backend(name: str = config.IBM_BACKEND):
    return service().backend(name)


@lru_cache(maxsize=1)
def noisy_simulator() -> AerSimulator:
    return AerSimulator.from_backend(backend())


def ideal_simulator() -> AerSimulator:
    return AerSimulator(method="statevector")


def transpile(qc: QuantumCircuit, seed: int = 1) -> QuantumCircuit:
    """ISA circuit for the real backend. Arms A and B run this identical circuit."""
    pm = generate_preset_pass_manager(optimization_level=3, backend=backend(), seed_transpiler=seed)
    return pm.run(qc)


def run_noisy(isa: QuantumCircuit, shots: int = config.SHOTS, seed: int = 11) -> dict[str, int]:
    return noisy_simulator().run(isa, shots=shots, seed_simulator=seed).result().get_counts()


def run_ideal(qc: QuantumCircuit, shots: int = config.SHOTS, seed: int = 11) -> dict[str, int]:
    return ideal_simulator().run(qc, shots=shots, seed_simulator=seed).result().get_counts()


# --- usage accounting ------------------------------------------------------

def _ledger() -> list[dict]:
    return json.loads(USAGE_JSON.read_text()) if USAGE_JSON.exists() else []


def cumulative_qpu_seconds() -> float:
    return sum(e["quantum_seconds"] for e in _ledger())


def service_usage() -> dict:
    u = service().usage()
    return {k: u.get(k) for k in ("usage_consumed_seconds", "usage_limit_seconds",
                                  "usage_remaining_seconds", "usage_period")}


def _log(entry: dict) -> None:
    ledger = _ledger() + [entry]
    USAGE_JSON.write_text(json.dumps(ledger, indent=2))
    render_usage_md(ledger)


def local_time(utc_str: str) -> str:
    """Ledger times are stored in UTC; documents show America/Denver local time (DEVIATIONS.md, D31)."""
    from zoneinfo import ZoneInfo
    t = dt.datetime.strptime(utc_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=dt.timezone.utc)
    return t.astimezone(ZoneInfo("America/Denver")).strftime("%Y-%m-%d %H:%M:%S")


def render_usage_md(ledger: list[dict]) -> None:
    """results/ibm-usage.md from the ledger JSON alone."""
    lines = ["# IBM Quantum usage ledger", "",
             f"Instance `{config.IBM_INSTANCE}` (Open Plan, {config.QPU_MONTHLY_SECONDS} s/month). "
             f"Hard stop for this project: {config.QPU_STOP_SECONDS} s cumulative.", "",
             "| when (MST, America/Denver) | purpose | backend | job id | circuits | shots | QPU s (job) | cumulative QPU s | service-reported consumed s (period) |",
             "|---|---|---|---|---|---|---|---|---|"]
    cum = 0.0
    for e in ledger:
        cum += e["quantum_seconds"]
        lines.append(f"| {local_time(e['when'])} | {e['purpose']} | {e['backend']} | `{e['job_id']}` | {e['circuits']} | "
                     f"{e['shots']} | {e['quantum_seconds']} | {cum:g} | {e['service_after'].get('usage_consumed_seconds')} |")
    USAGE_MD.write_text("\n".join(lines) + "\n")


def qpu_seconds(usage: dict) -> float:
    """IBM reports the billed QPU time as `qpu_charge_time_seconds`; older runtimes used `quantum_seconds`."""
    for key in ("qpu_charge_time_seconds", "quantum_seconds", "seconds"):
        if usage.get(key) is not None:
            return float(usage[key])
    return 0.0


def repair_ledger() -> None:
    """Recompute each entry's QPU seconds from the stored job metrics (fixes entries logged before qpu_seconds existed)."""
    ledger = _ledger()
    for e in ledger:
        e["quantum_seconds"] = qpu_seconds(e.get("job_metrics_usage") or {})
    USAGE_JSON.write_text(json.dumps(ledger[:-1], indent=2)) if ledger else None
    if ledger:
        _log(ledger[-1])


def run_hardware(isa_circuits: list[QuantumCircuit], purpose: str, shots: int = config.SHOTS) -> tuple[list[dict], dict]:
    """Submit all circuits as ONE SamplerV2 job inside a Batch. Returns counts per circuit and the usage entry."""
    from qiskit_ibm_runtime import Batch, SamplerV2

    before = service_usage()
    used = max(cumulative_qpu_seconds(), float(before["usage_consumed_seconds"] or 0))
    if used >= config.QPU_STOP_SECONDS:
        raise RuntimeError(f"QPU hard stop: {used} s used >= {config.QPU_STOP_SECONDS} s")
    be = backend()
    with Batch(backend=be) as batch:
        sampler = SamplerV2(mode=batch)
        job = sampler.run(isa_circuits, shots=shots)
        result = job.result()
    counts = [pub.data.meas.get_counts() for pub in result]
    metrics = job.metrics()
    qsec = qpu_seconds(metrics.get("usage") or {})
    entry = {
        "when": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        "purpose": purpose,
        "backend": be.name,
        "job_id": job.job_id(),
        "batch_id": batch.session_id,
        "circuits": len(isa_circuits),
        "shots": shots,
        "quantum_seconds": qsec,
        "job_metrics_usage": metrics.get("usage"),
        "service_before": before,
        "service_after": service_usage(),
    }
    _log(entry)
    return counts, entry

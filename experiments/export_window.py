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

def stage_bounds(web: encoder.Web, entangle: bool, n_trotter: int = config.N_TROTTER) -> list[tuple[str, int]]:
    """Instruction index at the end of each stage of build_circuit(measure=False)."""
    n, e = web.n, len(web.edges) if entangle else 0
    lean = int(np.count_nonzero(web.lean))
    k = 2 * n
    out = [("encode", k)]
    k += e
    out.append(("entangle", k))
    for step in range(1, n_trotter + 1):
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


# -------------------------------------------------------------- circuits ----
# The strip under the ring shows the circuit for ibm_fez, one row per physical qubit.
#
#   recompiled  (simulator-only items) the arm-A circuit transpiled here against the FakeFez snapshot
#               with the project's settings (optimization_level=3, seed_transpiler=1, as in
#               backends.transpile). A labelled barrier closes each stage, so every gate's stage is
#               exact; barriers stop the optimiser merging across stages, so the CZ count drifts a
#               little from the archived circuit. Both counts are stored and the page badges the drift.
#   as run      (items with a hardware run) the ISA circuit IBM recorded for the job, read from
#               window/data/hardware/*.json (exported by the main session from the job records, with
#               the physical layout). It has no stage barriers, so stages are inferred: see infer_stages.
#
# Claims are followed through routing: every maximal two-qubit block is classified by its Weyl
# coordinates (b ~ pi/4 means it contains a SWAP), occupants are exchanged when a SWAP block closes,
# and the run stops unless every measured wire then holds the claim its classical bit says it should.

GATES = ["rz", "sx", "x", "cz", "measure"]
SKIP = {"barrier", "delay", "id"}
HW_DIR = ROOT / "window" / "data" / "hardware"
_PM = None


def pass_manager():
    global _PM
    if _PM is None:
        from qiskit.transpiler import generate_preset_pass_manager
        from qiskit_ibm_runtime.fake_provider import FakeFez
        _PM = generate_preset_pass_manager(optimization_level=3, backend=FakeFez(), seed_transpiler=1)
    return _PM


def stage_names(n_trotter: int) -> list[str]:
    return ["encode", "entangle"] + [f"evolve {k}" for k in range(1, n_trotter + 1)] + ["measure"]


def tagged_circuit(web: encoder.Web, n_trotter: int) -> QuantumCircuit:
    qc = encoder.build_circuit(web, entangle=True, n_trotter=n_trotter, measure=False)
    out, prev = qc.copy_empty_like(), 0
    for name, b in stage_bounds(web, True, n_trotter):
        for inst in qc.data[prev:b]:
            out.append(inst)
        out.barrier(label="stage:" + name)
        prev = b
    if prev != len(qc.data):
        raise SystemExit("tagged circuit: stage bounds do not cover the circuit")
    out.h(range(web.n))
    out.measure_all()
    return out


def gates_of_isa(isa: QuantumCircuit) -> list[dict]:
    gates, s = [], 0
    for inst in isa.data:
        op = inst.operation
        if op.name == "barrier":
            s += bool(op.label and op.label.startswith("stage:"))
            continue
        g = {"name": op.name, "q": [isa.find_bit(q).index for q in inst.qubits], "stage": s}
        if op.params:
            g["angle"] = float(op.params[0])
        if op.name == "measure":
            g["clbit"] = isa.find_bit(inst.clbits[0]).index
        gates.append(g)
    return gates


def gates_of_record(rec: dict) -> list[dict]:
    """Gate list from an as-run export: ordered dicts {gate, qubits (physical), params?, clbits?}."""
    out = []
    for g in rec["gates"]:
        name = g.get("gate") or g.get("name")
        if name in SKIP:
            continue
        d = {"name": name, "q": [int(q) for q in g["qubits"]], "stage": 0}
        if name == "measure":
            d["clbit"] = int(g["clbits"][0])
        elif g.get("params"):
            d["angle"] = float(g["params"][0])
        out.append(d)
    return out


def _block_unitary(blk: dict) -> np.ndarray:
    from qiskit.quantum_info import Operator
    c, (p0, _) = QuantumCircuit(2), blk["pair"]
    for g in blk["gates"]:
        loc = [0 if q == p0 else 1 for q in g["q"]]
        if g["name"] == "cz":
            c.cz(0, 1)
        elif g["name"] == "rz":
            c.rz(g["angle"], loc[0])
        elif g["name"] == "sx":
            c.sx(loc[0])
        elif g["name"] == "x":
            c.x(loc[0])
    return Operator(c).data


def track(gates: list[dict], layout: list[int], measured: dict[int, int], related: set) -> dict:
    """Follow claims through routing. Sets g['claims'], g['kind'], g['block'] on every CZ."""
    from qiskit.synthesis import TwoQubitWeylDecomposition
    for g in gates:
        if g["name"] not in GATES:
            raise SystemExit(f"unexpected gate {g['name']}")
    occ = {p: k for k, p in enumerate(layout)}
    start = dict(occ)
    open_blk, blocks, swaps = {}, [], []

    def close(blk):
        if blk["closed"]:
            return
        blk["closed"] = True
        w = TwoQubitWeylDecomposition(_block_unitary(blk))
        swap = w.b > math.pi / 8
        inter = abs(w.c - math.pi / 4) > 0.01 if swap else w.a > 1e-3
        p0, p1 = blk["pair"]
        a, b = occ.get(p0, -1), occ.get(p1, -1)
        blk["kind"] = 2 if swap and inter else 1 if swap else 0
        blk["claims"] = (a, b)
        for g in blk["gates"]:
            if g["name"] == "cz":
                g["claims"], g["kind"], g["block"] = [a, b], blk["kind"], blk["id"]
        if swap:
            occ.pop(p0, None), occ.pop(p1, None)
            if b >= 0:
                occ[p0] = b
            if a >= 0:
                occ[p1] = a
            swaps.append((blk["last"], p0, p1))
        for q in blk["pair"]:
            if open_blk.get(q) is blk:
                del open_blk[q]

    for idx, g in enumerate(gates):
        q0 = g["q"][0]
        if g["name"] == "cz":
            p0, p1 = g["q"]
            b0, b1 = open_blk.get(p0), open_blk.get(p1)
            if b0 is not None and b0 is b1 and b0["stage"] == g["stage"]:
                b0["gates"].append(g)
                b0["last"] = idx
                continue
            for b_ in (b0, b1):
                if b_ is not None:
                    close(b_)
            blk = {"id": len(blocks), "pair": (p0, p1), "gates": [g], "closed": False, "stage": g["stage"],
                   "first": idx, "last": idx}
            blocks.append(blk)
            open_blk[p0] = open_blk[p1] = blk
        elif g["name"] == "measure":
            if q0 in open_blk:
                close(open_blk[q0])
        elif q0 in open_blk:
            open_blk[q0]["gates"].append(g)
    for b_ in blocks:
        close(b_)
    meas = {g["clbit"]: g["q"][0] for g in gates if g["name"] == "measure"}
    ok = sorted(meas) == sorted(measured) and all(occ.get(meas[c], -1) == measured[c] for c in measured)
    unrelated = sum(1 for b_ in blocks if b_["kind"] == 0 and frozenset(b_["claims"]) not in related)
    if not ok:
        raise SystemExit("claim tracking: measured wires do not hold the claims their classical bits name")
    if unrelated:
        raise SystemExit(f"claim tracking: {unrelated} interaction blocks act on unrelated claims")
    return {"blocks": blocks, "swaps": swaps, "start": start, "final": dict(occ)}


def infer_stages(gates: list[dict], blocks: list[dict], n_trotter: int) -> int:
    """Stage tags for an as-run circuit, which has no stage barriers.

    Each related pair interacts once per stage (entangle, evolve 1..N), so the k-th interaction
    block of a pair is given stage k. A pure-SWAP block takes the stage of the next interaction on
    either of its wires (routing serves what follows). Tags are made monotone along every wire;
    single-qubit gates take the stage of the last two-qubit block on their wire (encode before the
    first); measurements are 'measure'. Returns the number of pairs with fewer interaction blocks
    than stages, i.e. where the compiler merged two stages' interactions into one block."""
    seen, tent = {}, {}
    for b in blocks:
        if b["kind"] != 1:
            key = frozenset(b["claims"])
            tent[b["id"]] = 1 + min(seen.get(key, 0), n_trotter)
            seen[key] = seen.get(key, 0) + 1
    nxt = {}
    for b in reversed(blocks):
        if b["kind"] == 1:
            tent[b["id"]] = min([nxt[q] for q in b["pair"] if q in nxt], default=None)
        for q in b["pair"]:
            nxt[q] = tent[b["id"]] if tent[b["id"]] is not None else nxt.get(q)
    last, final, bstage = {}, n_trotter + 2, {}
    for g in gates:
        if g["name"] == "measure":
            g["stage"] = final
        elif g["name"] == "cz":
            b = g["block"]
            if b not in bstage:
                p0, p1 = g["q"]
                bstage[b] = max(tent[b] if tent[b] is not None else 0, last.get(p0, 0), last.get(p1, 0))
            g["stage"] = bstage[b]
            for q in g["q"]:
                last[q] = g["stage"]
        else:
            g["stage"] = last.get(g["q"][0], 0)
    return sum(1 for v in seen.values() if v < 1 + n_trotter)


def asap_depth(gates: list[dict]) -> int:
    lvl = {}
    for g in gates:
        d = 1 + max(lvl.get(q, 0) for q in g["q"])
        for q in g["q"]:
            lvl[q] = d
    return max(lvl.values(), default=0)


def compact_strip(gates: list[dict], tr: dict, stages: list[str]) -> dict:
    wires = sorted({q for g in gates for q in g["q"]})
    wi = {p: k for k, p in enumerate(wires)}
    out = []
    for g in gates:
        code, s, w = GATES.index(g["name"]), g["stage"], wi[g["q"][0]]
        if g["name"] == "cz":
            out.append([code, s, w, wi[g["q"][1]], *g["claims"], g["kind"]])
        elif g["name"] == "measure":
            out.append([code, s, w, g["clbit"]])
        elif "angle" in g:
            out.append([code, s, w, round(g["angle"], 4)])
        else:
            out.append([code, s, w])
    counts = {}
    for g in gates:
        counts[g["name"]] = counts.get(g["name"], 0) + 1
    return {"backend": config.IBM_BACKEND, "stages": stages, "gate_names": GATES, "wires": wires,
            "start": [tr["start"].get(p, -1) for p in wires], "gates": out,
            "swaps": [[i, wi[a], wi[b]] for i, a, b in tr["swaps"]],
            "counts": counts, "depth": asap_depth(gates),
            "blocks": {"interaction": sum(b["kind"] == 0 for b in tr["blocks"]),
                       "swap": sum(b["kind"] == 1 for b in tr["blocks"]),
                       "swap_and_interaction": sum(b["kind"] == 2 for b in tr["blocks"])}}


def recompiled_strip(web: encoder.Web, n_trotter: int, archived: dict | None) -> dict:
    pm = pass_manager()
    isa = pm.run(tagged_circuit(web, n_trotter))
    gates = gates_of_isa(isa)
    tr = track(gates, isa.layout.initial_index_layout(filter_ancillas=True), {k: k for k in range(web.n)},
               {frozenset((i, j)) for i, j, _ in web.edges})
    plain = pm.run(encoder.build_circuit(web, entangle=True, n_trotter=n_trotter))
    st = compact_strip(gates, tr, stage_names(n_trotter))
    st.update({"source": "recompiled", "stage_inferred": False,
               "provenance": "transpiled here for ibm_fez from the FakeFez snapshot (qiskit-ibm-runtime "
                             "fake_provider), optimization_level=3, seed_transpiler=1, with a barrier closing "
                             "each stage; physical qubits are the snapshot's layout, not necessarily the run's",
               "recompiled_without_barriers": {"cz": plain.count_ops().get("cz", 0), "depth": plain.depth()},
               "archived": archived})
    return st


def as_run_strip(web: encoder.Web, n_trotter: int, circ: dict, measured: dict[int, int],
                 archived: dict | None) -> dict:
    gates = gates_of_record(circ)
    if len(circ["layout"]["initial"]) != web.n:
        raise SystemExit(f"{circ['job_id']}-{circ['circuit_index']}: layout has {len(circ['layout']['initial'])} "
                         f"logical qubits, the web has {web.n}")
    tr = track(gates, [int(p) for p in circ["layout"]["initial"]], measured,
               {frozenset((i, j)) for i, j, _ in web.edges})
    merged = infer_stages(gates, tr["blocks"], n_trotter)
    st = compact_strip(gates, tr, stage_names(n_trotter))
    st.update({"source": "as_run", "stage_inferred": True, "merged_pairs": merged,
               "job_id": circ["job_id"], "circuit_index": circ["circuit_index"], "setting": circ.get("setting"),
               "svg": f"hardware/{circ['job_id']}-{circ['circuit_index']}.svg",
               "final_layout_matches": [int(p) for p in circ["layout"]["final"]] == [
                   {k: w for w, k in tr["final"].items()}.get(q) for q in range(web.n)],
               "provenance": f"as run on {circ.get('backend', config.IBM_BACKEND)}, job {circ['job_id']}, circuit "
                             f"{circ['circuit_index']}: the ISA circuit from IBM's job record with its physical "
                             "layout (window/data/hardware/, experiments/export_hardware_circuits.py on main)",
               "archived": archived})
    return st


def load_hardware(hw_dir: Path) -> dict:
    """(kind, item, setting) -> circuit record, from the as-run exports (one <job_id>-<index>.json per circuit,
    written by experiments/export_hardware_circuits.py from IBM's job records). Calibration circuits are skipped."""
    out = {}
    for f in sorted(hw_dir.glob("*-*.json")) if hw_dir.is_dir() else []:
        c = json.loads(f.read_text())
        if c.get("role") == "tomography setting":
            out[("witness", c["item"], c["setting"])] = c
        elif str(c.get("purpose", "")).lower().startswith("stage 1"):
            out[("stage1", c["item"], None)] = c
    return out


# ------------------------------------------------------------ hardware ----

SETTINGS = [a + b for a in "XYZ" for b in "XYZ"]          # as in experiments/witness_design.py


def joint_from_counts(counts: dict, key) -> list[float]:
    """P(yes,yes), P(yes,no), P(no,yes), P(no,no) for (claim i, claim j); 0 = yes-aligned."""
    v = np.zeros(4)
    for b, c in counts.items():
        bi, bj = key(b)
        v[2 * bi + bj] += c
    return [r4(x) for x in v / v.sum()]


def witness_block(it: dict, design: dict, job: dict, sim: dict, final_sv: Statevector, web: encoder.Web,
                  final_stage: dict) -> dict:
    i, j = it["pair"]
    n = web.n
    xx = it["hardware_counts"][SETTINGS.index("XX")]            # keys 'b_j b_i' (clbit 0 = claim i)
    p = x_basis_probs(final_sv, n).reshape([2] * n)
    ax = tuple(a for a in range(n) if a not in (n - 1 - i, n - 1 - j))
    pij = p.sum(axis=ax)                                         # axes ordered high qubit first
    pij = pij if n - 1 - i < n - 1 - j else pij.T                # -> [b_i, b_j]
    e = [k for k, (a, b, _) in enumerate(web.edges) if {a, b} == {i, j}][0]
    return {
        "kind": "witness", "job_id": job["job_id"], "backend": job["backend"], "pair": [i, j],
        "physical_qubits_as_run": it["physical_qubits"], "setting": "XX", "shots": sum(xx.values()),
        "note": "9 two-qubit Pauli settings of this pair, 4,000 shots each, plus 4 readout-calibration "
                "circuits; XX is the yes/no basis of both claims. Negativity is from the full tomography.",
        "joint": {"outcomes": ["yes,yes", "yes,no", "no,yes", "no,no"],
                  "hardware": joint_from_counts(xx, lambda b: (int(b[1]), int(b[0]))),
                  "noisy_sim_arm_A": joint_from_counts(sim["arms"]["A"]["counts"],
                                                       lambda b: (int(b[-1 - i]), int(b[-1 - j]))),
                  "exact": [r4(x) for x in pij.reshape(4)],
                  "shots": {"hardware": sum(xx.values()), "noisy_sim_arm_A": sum(sim["arms"]["A"]["counts"].values())}},
        "negativity": {"exact_here": final_stage["negativity"][e], "ideal": r4(it["negativity_ideal"]),
                       "noisy_sim": {k: it["noisy_sim"][k] for k in ("negativity", "ci95", "certified")},
                       "hardware": {k: it["hardware"][k] for k in ("negativity", "ci95", "certified")}},
        "cz_per_setting_as_archived": design.get("cz_per_setting"),
    }


# ------------------------------------------------------------------ main ----

def item_states(web: encoder.Web, n_trotter: int):
    w = readout._weights(web)
    m = votes(web.n, w)
    qa = encoder.build_circuit(web, entangle=True, n_trotter=n_trotter, measure=False)
    qc_ = encoder.build_circuit(web, entangle=False, n_trotter=n_trotter, measure=False)
    st_a = evolve_stages(qa, stage_bounds(web, True, n_trotter))
    st_c = evolve_stages(qc_, stage_bounds(web, False, n_trotter))
    if not np.allclose(st_a[-1][1].data, Statevector(qa).data, atol=1e-9):
        raise SystemExit("staged evolution does not reproduce the circuit")
    return w, analyse(st_a, web, w, m, with_pairs=True), analyse(st_c, web, w, m, with_pairs=False), st_a[-1][1]


def claims_of(rec: dict, web: encoder.Web) -> list[dict]:
    phases = encoder.solve_phases(web)
    return [{"text": c["text"], "confidence": c["confidence"], "lean": c["lean"],
             "theta": r4(c["confidence"] * math.pi / 2), "phi": r4(phases[k])}
            for k, c in enumerate(rec["contentions"])]


def stage1_item(hw: dict) -> tuple[dict, dict]:
    """The Stage 1 pipe test: pool-run-1 q01 (an earlier extraction than run 1's q01), N = 0 evolution."""
    s1 = json.loads((config.RESULTS / "stage1-run-1.json").read_text())
    qid = s1["item"]["id"]
    rec = {r["id"]: r for r in json.loads((config.RESULTS / "pool-run-1.json").read_text())["records"]}[qid]
    web = encoder.build_web(rec["contentions"], rec["pairs"])
    w, a_stages, c_stages, _ = item_states(web, 0)
    final = a_stages[-1]
    ideal = s1["arms"]["ideal_sim"]["readout"]["conflict_score"]
    if abs(final["conflict_score"] - ideal) > 0.12:
        raise SystemExit(f"stage 1: exact conflict {final['conflict_score']} vs archived ideal sim {ideal}")
    usage = s1["ibm_usage"]
    runs = {}
    for name, label in (("ideal_sim", "noiseless simulator"), ("noisy_sim", "noisy simulator (ibm_fez model)"),
                        ("hardware", "ibm_fez, real hardware")):
        a = s1["arms"][name]
        runs[name] = {"label": label, "conflict_score": r4(a["readout"]["conflict_score"]),
                      "p_yes": r4(a["readout"]["p_yes"]), "judgment": a["readout"]["judgment"],
                      "counts_summary": counts_summary(a["counts"], w), "counts": a["counts"]}
    archived = {"cz": s1["transpiled_ops"].get("cz"), "depth": s1["depth"]}
    key = ("stage1", qid, None)
    strip = (as_run_strip(web, 0, hw[key], {k: k for k in range(web.n)}, archived) if key in hw
             else recompiled_strip(web, 0, archived))
    iid = f"{qid}-s1"
    item = {
        "id": iid, "run": 0, "role": "stage1", "category": rec.get("category"), "question": rec["question"],
        "truth": rec["answer"], "model_answer": rec["model_answer"], "correct": rec["correct"],
        "source": rec.get("source"), "claims": claims_of(rec, web),
        "relations": [{"i": i, "j": j, "J": r4(J), "relation": "supports" if J > 0 else "contradicts"}
                      for i, j, J in web.edges],
        "readout_weights": [r4(x) for x in w],
        "stages": a_stages + [{"stage": "collapse", **{k: final[k] for k in
                               ("p_yes", "p_strong_yes", "p_strong_no", "conflict_score", "vote_hist")}}],
        "stages_unentangled": c_stages, "arms": {},
        "hardware": {"kind": "stage1", "job_id": usage["job_id"], "backend": usage["backend"],
                     "qpu_seconds": usage["quantum_seconds"], "runs": runs,
                     "note": "Stage 1 pipe test: entangling gates and N = 0 evolution, so the state measured is "
                             "the entangle stage. Pool run 1's extraction of q01; run 1 of Stage 2 re-extracted "
                             "the claims, so the window's q01 is a different web."},
        "circuit": strip,
    }
    entry = {"id": iid, "run": 0, "role": "stage1", "category": item["category"], "question": rec["question"][:140],
             "truth": rec["answer"], "model_answer": rec["model_answer"], "correct": rec["correct"],
             "n_qubits": web.n, "n_relations": len(web.edges), "n_contradictions": sum(J < 0 for _, _, J in web.edges),
             "flags": {}, "scores": {}, "hardware": "stage1",
             "max_negativity": max([max(s["negativity"], default=0) for s in a_stages], default=0),
             "stage_conflict": {"A": [s["conflict_score"] for s in a_stages], "C": [s["conflict_score"] for s in c_stages]}}
    return item, entry


def main() -> None:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--hardware-dir", type=Path, default=HW_DIR, help="as-run gate lists (default window/data/hardware)")
    ap.add_argument("--only", default="", help="comma-separated item ids: rewrite just these and patch index.json")
    args = ap.parse_args()
    only = {x for x in args.only.split(",") if x}
    hw = load_hardware(args.hardware_dir)
    print(f"as-run gate lists: {len(hw)} circuits from {args.hardware_dir}")
    wit = json.loads((config.RESULTS / "witness-run-1.json").read_text())
    wit_items = {it["id"]: it for it in wit["items"]}
    wit_design = {it["id"]: it for it in json.loads((config.RESULTS / "witness-design.json").read_text())["items"]}
    OUT.mkdir(parents=True, exist_ok=True)
    index = {"generated_by": "experiments/export_window.py", "noise": "stages are noiseless statevectors; "
             "archived arm readouts are as run (A, C, D: noisy simulator from ibm_fez; A0: noiseless sampling)",
             "constants": {"kappa": config.KAPPA, "n_trotter": config.N_TROTTER, "gamma0": config.GAMMA0,
                           "beta0": config.BETA0, "tau": config.STRONG_TAU, "shots": config.SHOTS},
             "arm_labels": ARM_LABEL, "runs": {}, "items": []}
    diffs, strip_drift = [], []
    for run, pool_file in RUNS.items():
        res = json.loads((config.RESULTS / f"stage2-run-{run}.json").read_text())
        pool = {r["id"]: r for r in json.loads((config.RESULTS / pool_file).read_text())["records"]}
        split, thr = res["split"], res["thresholds"]
        role = {**{q: "test_wrong" for q in split["test_wrong"]}, **{q: "test_right" for q in split["test_right"]},
                **{q: "calibration" for q in split["calibration"]}}
        index["runs"][run] = {"pool": pool_file, "rule": split["rule"], "thresholds": thr,
                              "summary": res["summary"], "hypotheses": res["hypotheses"]}
        for qid, sim in sorted(res["items"].items()):
            if only and qid not in only:
                continue
            rec = pool[qid]
            web = encoder.build_web(rec["contentions"], rec["pairs"])
            n = web.n
            w, a_stages, c_stages, final_sv = item_states(web, config.N_TROTTER)
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

            archived = {"cz": arms["A"].get("cz"), "depth": arms["A"].get("depth")} if "A" in arms else None
            hardware = None
            if run == 2 and qid in wit_items:
                hardware = witness_block(wit_items[qid], wit_design.get(qid, {}), wit["usage"], sim, final_sv, web, final)
                if abs(hardware["negativity"]["exact_here"] - hardware["negativity"]["ideal"]) > 1e-3:
                    raise SystemExit(f"{qid}: exact negativity differs from the witness design's ideal value")
            key = ("witness", qid, "XX")
            if hardware and key in hw:
                i, j = hardware["pair"]
                strip = as_run_strip(web, config.N_TROTTER, hw[key], {0: i, 1: j},
                                     {"cz": wit_design[qid].get("cz_per_setting"), "depth": None})
            else:
                strip = recompiled_strip(web, config.N_TROTTER, archived)
                if archived and archived["cz"] is not None:
                    strip_drift.append((strip["counts"].get("cz", 0), archived["cz"],
                                        strip["recompiled_without_barriers"]["cz"]))

            item = {
                "id": qid, "run": run, "role": role.get(qid, "excluded"), "category": rec.get("category"),
                "question": rec["question"], "truth": rec["answer"], "model_answer": rec["model_answer"],
                "correct": rec["correct"], "source": rec.get("source"),
                "claims": claims_of(rec, web),
                "relations": [{"i": i, "j": j, "J": r4(J), "relation": "supports" if J > 0 else "contradicts"}
                              for i, j, J in web.edges],
                "readout_weights": [r4(x) for x in w],
                "stages": a_stages + [{"stage": "collapse", **{k: final[k] for k in
                                       ("p_yes", "p_strong_yes", "p_strong_no", "conflict_score", "vote_hist")}}],
                "stages_unentangled": c_stages,
                "arms": arms,
                "circuit": strip,
            }
            if hardware:
                item["hardware"] = hardware
            if run == 1 and qid == "q01":
                item["see_also"] = {"id": "q01-s1", "note": "The Stage 1 hardware pipe test used pool run 1's "
                                    "extraction of this question, a different claim web: see q01-s1."}
            (OUT / f"{qid}.json").write_text(json.dumps(item, separators=(",", ":"), ensure_ascii=False))
            entry = {
                "id": qid, "run": run, "role": item["role"], "category": item["category"],
                "question": rec["question"][:140], "truth": rec["answer"], "model_answer": rec["model_answer"],
                "correct": rec["correct"], "n_qubits": n, "n_relations": len(web.edges),
                "n_contradictions": sum(J < 0 for _, _, J in web.edges),
                "flags": {a: arms[a]["flagged"] for a in arms},
                "scores": {a: arms[a]["conflict_score"] for a in arms},
                "max_negativity": max([max(s["negativity"], default=0) for s in a_stages], default=0),
                "stage_conflict": {"A": [s["conflict_score"] for s in a_stages],
                                   "C": [s["conflict_score"] for s in c_stages]},
            }
            if hardware:
                entry["hardware"] = "witness"
            index["items"].append(entry)
        if only:
            continue
        # Exploratory (not pre-registered): test-set AUROC of the exact conflict score read at each stage.
        test = [i for i in index["items"] if i["run"] == run and i["role"].startswith("test")]
        names = [s for s, _ in stage_bounds(encoder.Web(np.ones(1), np.ones(1), ()), True)]
        index["runs"][run]["stage_auroc_exploratory"] = {
            arm: {name: r4(readout.auroc([i["stage_conflict"][arm][k] for i in test if i["correct"] is False],
                                         [i["stage_conflict"][arm][k] for i in test if i["correct"] is True]))
                  for k, name in enumerate(names)} for arm in ("A", "C")}
        print(f"run {run}: {sum(1 for i in index['items'] if i['run'] == run)} items;",
              "stage AUROC", index["runs"][run]["stage_auroc_exploratory"])

    if not only or any(x.endswith("-s1") for x in only):
        s1_item, s1_entry = stage1_item(hw)
        (OUT / f"{s1_item['id']}.json").write_text(json.dumps(s1_item, separators=(",", ":"), ensure_ascii=False))
        index["items"].append(s1_entry)
        print("stage 1 item:", s1_item["id"], "strip", s1_item["circuit"]["source"], s1_item["circuit"]["counts"])

    if only:                                   # patch the existing index rather than rebuilding it
        old = json.loads((OUT / "index.json").read_text())
        new = {i["id"]: i for i in index["items"]}
        old["items"] = [new.pop(i["id"], i) for i in old["items"]] + list(new.values())
        old["runs"].setdefault("0", {"label": "Stage 1 pipe test", "pool": "pool-run-1.json"})
        (OUT / "index.json").write_text(json.dumps(old, separators=(",", ":"), ensure_ascii=False))
        print("patched index.json for", sorted(only))
        return
    index["runs"]["0"] = {"label": "Stage 1 pipe test", "pool": "pool-run-1.json"}
    index["check"] = {"exact_vs_archived_A0_conflict_mean_abs_diff": r4(np.mean(diffs)),
                      "max_abs_diff": r4(np.max(diffs)), "items": len(diffs)}
    if strip_drift:
        d = np.array(strip_drift, float)
        index["check"]["recompiled_strip"] = {
            "items": len(d), "cz_drawn_mean": r4(d[:, 0].mean()), "cz_archived_mean": r4(d[:, 1].mean()),
            "mean_abs_cz_drift_drawn_vs_archived": r4(np.abs(d[:, 0] - d[:, 1]).mean()),
            "recompiled_without_barriers_equals_archived": int((d[:, 2] == d[:, 1]).sum())}
    (OUT / "index.json").write_text(json.dumps(index, separators=(",", ":"), ensure_ascii=False))
    print("check:", index["check"])


if __name__ == "__main__":
    main()

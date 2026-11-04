"""Encode a web of contentions as one quantum circuit.

Geometry (one qubit per contention):
  * |0> is "uncommitted". RY(theta) tilts the qubit toward the equator in
    proportion to the contention's confidence: theta = confidence * pi/2.
  * The equatorial direction is the contention's stance. Phase 0 (+X) is
    "yes", phase pi (-X) is "no". RZ(phi) sets it; phi is solved from the
    relation web (an XY-model ground state anchored by each lean) so that
    supporting pairs sit near each other and contradicting pairs ~180 deg apart.
  * Every related pair gets RZZ(KAPPA * strength * sign).
  * Optional evolution: N Trotter steps of a QAOA-style schedule. The problem
    Hamiltonian is the relation web as an Ising energy in the yes/no (X) basis,
    H_P = -sum J_ij X_i X_j - sum h_i X_i; the mixer is H_M = -sum Z_i, whose
    ground state is the all-uncommitted state.
  * Readout is in the X basis: bit 0 = yes-aligned, bit 1 = no-aligned.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass

import numpy as np
from qiskit import QuantumCircuit

from . import config

SIGN = {"supports": 1.0, "contradicts": -1.0, "unrelated": 0.0}


@dataclass(frozen=True)
class Web:
    confidence: np.ndarray     # (n,)
    lean: np.ndarray           # (n,)
    edges: tuple               # ((i, j, J), ...) J = sign * strength, related pairs only

    @property
    def n(self) -> int:
        return len(self.confidence)


def build_web(contentions: list[dict], pairs: list[dict]) -> Web:
    edges = tuple((p["i"], p["j"], SIGN[p["relation"]] * p["strength"])
                  for p in pairs if p["relation"] != "unrelated" and p["strength"] > 0)
    return Web(np.array([c["confidence"] for c in contentions], float),
               np.array([c["lean"] for c in contentions], float), edges)


def shuffled_web(web: Web, seed: int) -> Web:
    """Arm D: same number of relations with the same signed strengths, placed on random pairs."""
    rng = random.Random(seed)
    all_pairs = [(i, j) for i in range(web.n) for j in range(i + 1, web.n)]
    new_pairs = rng.sample(all_pairs, len(web.edges))
    js = [J for _, _, J in web.edges]
    rng.shuffle(js)
    return Web(web.confidence, web.lean, tuple((i, j, J) for (i, j), J in zip(new_pairs, js)))


def solve_phases(web: Web, restarts: int = 8, iters: int = 1500, lr: float = 0.05,
                 seed: int = 0) -> np.ndarray:
    """Minimise E(phi) = -sum_ij J_ij cos(phi_i - phi_j) - sum_k lean_k cos(phi_k)."""
    n = web.n
    J = np.zeros((n, n))
    for i, j, w in web.edges:
        J[i, j] = J[j, i] = w
    h = web.lean

    def energy(phi):
        d = phi[:, None] - phi[None, :]
        return -0.5 * np.sum(J * np.cos(d)) - np.sum(h * np.cos(phi))

    rng = np.random.default_rng(seed)
    starts = [np.where(h < 0, math.pi, 0.0), np.zeros(n)]
    starts += [rng.uniform(-math.pi, math.pi, n) for _ in range(restarts - 2)]
    best, best_e = None, math.inf
    for phi in starts:
        phi = phi.astype(float).copy()
        for _ in range(iters):
            d = phi[:, None] - phi[None, :]
            grad = np.sum(J * np.sin(d), axis=1) + h * np.sin(phi)
            phi -= lr * grad
        e = energy(phi)
        if e < best_e - 1e-12:
            best, best_e = phi, e
    return np.mod(best + math.pi, 2 * math.pi) - math.pi


def pin_frame(phi: np.ndarray, web: Web, no_lean: float = 0.1, rotate: np.ndarray | None = None) -> np.ndarray:
    """Frame correction (DEVIATIONS.md, D15). The XY ground state's frame can drift off the yes/no
    readout axis when relations between opposite-leaning claims outweigh the lean anchors (and the
    energy is symmetric under phi -> -phi). Rotate the phases rigidly by the least-squares angle that
    puts the confidence-weighted yes-leaning claims at 0 and the no-leaning claims at pi:
    alpha = arg sum_k c_k |lean_k| exp(i (t_k - phi_k)), t_k = 0 (lean > no_lean) or pi (lean < -no_lean).
    `rotate` selects which phases move (default: all); hedges excluded from the fit."""
    lean, c = web.lean, web.confidence
    lean_mask = np.abs(lean) > no_lean
    if not lean_mask.any():
        return phi
    t = np.where(lean > 0, 0.0, math.pi)
    z = np.sum((c * np.abs(lean) * np.exp(1j * (t - phi)))[lean_mask])
    alpha = float(np.angle(z)) if abs(z) > 1e-12 else 0.0
    out = phi.copy()
    sel = np.ones(web.n, bool) if rotate is None else rotate
    out[sel] = phi[sel] + alpha
    return np.mod(out + math.pi, 2 * math.pi) - math.pi


def anchor_weight(web: Web) -> float:
    """lambda = max(1, the largest total coupling sum_j |J_kj| of any claim): a fully leaning claim's
    anchor is then at least as strong as all its relation couplings together (DEVIATIONS.md, D15)."""
    deg = np.zeros(web.n)
    for i, j, J in web.edges:
        deg[i] += abs(J)
        deg[j] += abs(J)
    return float(max(1.0, deg.max() if web.n else 1.0))


def solve_phases_anchored(web: Web, weight: float | None = None) -> np.ndarray:
    """Frame correction (D15): solve the XY energy with the lean anchors scaled by anchor_weight(web)
    (or `weight`; math.inf = every leaning claim exactly at 0 or pi, hedges solved by the relations).
    Only the phase solve changes; the circuit's couplings and evolution field do not."""
    lam = anchor_weight(web) if weight is None else weight
    if math.isinf(lam):
        phi = np.where(web.lean > 0.1, 0.0, np.where(web.lean < -0.1, math.pi, np.nan))
        if np.isnan(phi).any():
            free = solve_phases(web)
            phi = np.where(np.isnan(phi), free, phi)
        return phi
    return solve_phases(Web(web.confidence, web.lean * lam, web.edges))


def build_circuit(web: Web, entangle: bool = True, n_trotter: int = config.N_TROTTER,
                  measure: bool = True, phi: np.ndarray | None = None) -> QuantumCircuit:
    """entangle=False is arm C: every two-qubit term (prep RZZ and evolution XX) removed."""
    n = web.n
    if phi is None:
        phi = solve_phases(web)
    theta = web.confidence * math.pi / 2
    qc = QuantumCircuit(n, name="entangled_mind")
    for k in range(n):
        qc.ry(float(theta[k]), k)
        qc.rz(float(phi[k]), k)
    if entangle:
        for i, j, J in web.edges:
            qc.rzz(config.KAPPA * J, i, j)
    for step in range(1, n_trotter + 1):
        s = step / (n_trotter + 1)
        gamma, beta = config.GAMMA0 * s, config.BETA0 * (1 - s)
        qc.h(range(n))                       # into the yes/no frame
        if entangle:
            for i, j, J in web.edges:
                qc.rzz(-2 * gamma * J, i, j)   # exp(+i gamma J X_i X_j)
        for k in range(n):
            if web.lean[k]:
                qc.rz(float(-2 * gamma * web.lean[k]), k)
        qc.h(range(n))
        for k in range(n):
            qc.rz(-2 * beta, k)              # exp(+i beta Z_k)
    if measure:
        qc.h(range(n))                       # measure in the yes/no (X) basis
        qc.measure_all()
    return qc

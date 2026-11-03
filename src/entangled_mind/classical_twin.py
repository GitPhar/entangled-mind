"""Arm F: the classical twin of arm A.

The same relation web, couplings, signs and lean fields as arm A's problem
Hamiltonian, treated as a classical Ising spin model and solved by exact
enumeration of all 2^n configurations (n <= 16). No superposition and no
interference.

  E(x) = -sum_ij J_ij x_i x_j - sum_i lean_i x_i,   x_i = +1 (yes) / -1 (no)

Judgment: sign of the ground state's weighted vote (the same |lean| weights as
the quantum readout). Conflict score: among the near-minimum configurations
(E <= E_min + DELTA * (E_max - E_min)), the share that sit in strongly opposed
camps, 2 * min(#m >= tau, #m <= -tau) / #near, mirroring the quantum
conflict score."""

from __future__ import annotations

import numpy as np

from . import config
from .encoder import Web

DELTA = 0.10   # near-minimum window, as a fraction of the energy range (pre-registered)


def all_spins(n: int) -> np.ndarray:
    idx = np.arange(2 ** n)[:, None]
    return 1 - 2 * ((idx >> np.arange(n)) & 1)          # (2^n, n), bit 0 -> +1 (yes)


def energies(web: Web, spins: np.ndarray) -> np.ndarray:
    e = -spins @ web.lean
    for i, j, J in web.edges:
        e -= J * spins[:, i] * spins[:, j]
    return e


def classical_twin_readout(web: Web, tau: float = config.STRONG_TAU, delta: float = DELTA) -> dict:
    spins = all_spins(web.n)
    e = energies(web, spins)
    w = np.abs(web.lean)
    w = w / w.sum() if w.sum() > 0 else np.full(web.n, 1 / web.n)
    m = spins @ w
    g = int(np.argmin(e))
    near = e <= e.min() + delta * (e.max() - e.min())
    n_yes, n_no = int(np.sum(near & (m >= tau))), int(np.sum(near & (m <= -tau)))
    return {
        "judgment": "yes" if m[g] >= 0 else "no",
        "ground_vote": float(m[g]),
        "ground_degeneracy": int(np.sum(np.isclose(e, e.min()))),
        "n_near_minimum": int(near.sum()),
        "near_strong_yes": n_yes,
        "near_strong_no": n_no,
        "conflict_score": 2 * min(n_yes, n_no) / int(near.sum()),
    }

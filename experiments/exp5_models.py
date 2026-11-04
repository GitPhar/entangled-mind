"""Experiment 5 models (frozen §5, with D26): one-step-ahead prediction of every rating in a
conversation from the opening context and the ratings the model actually gave earlier.

A5  dynamic quantum belief state (statevector, exact): prep RY(theta) RZ(phi) + RZZ(kappa J);
    one Trotter step before every turn; Lueders update sqrt(E) on each rating; projective
    collapse on the K1 choice. Parameters (kappa, gamma, beta, a, b).
F5  classical twin: distribution over 2^n configurations; prior = product of the same
    single-claim marginals then one heat-bath sweep under -kappa_F sum J s_i s_j at T; before
    every turn P <- (1 - lam) P + lam G(P); Bayes update with the same likelihood.
    Parameters (kappa_F, T, lam, a, b).
D5  A5 dephased in the yes/no basis after every unitary step. Only the mixer moves
    populations there (couplings and fields are diagonal phases), so each step is an
    independent bit flip with probability sin^2(beta). Parameters as A5.
BA5 belief adjustment on M ratings only (Hogarth & Einhorn). Parameters (w_supp, w_con, rho, a, b).

Ratings are on 0-100 after anchor recoding. Link: r_hat = 100 (a + (b - a) p),
p_obs = clip((r/100 - a)/(b - a), 0.01, 0.99)."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from entangled_mind import config, encoder, v2
import exp5_run as er

KAPPA0 = config.KAPPA      # pi/4: A5's kappa scales the v1 couplings relative to this (D26)
H2 = np.array([[1, 1], [1, -1]], complex) / math.sqrt(2)


# --- per-item precomputation ----------------------------------------------------

@dataclass
class ItemData:
    id: str
    n: int
    theta: np.ndarray
    phi: np.ndarray
    lean: np.ndarray            # hedges set to 0
    edges: tuple                # (i, j, J)
    w: np.ndarray               # readout weights |lean| normalised
    m: np.ndarray               # vote of each X-basis configuration (index bit 0 = yes)
    piM: np.ndarray             # Pi_M eigenvalues in the X basis: 1 (m > 0), 0.5 (m = 0), 0 (m < 0)
    z: np.ndarray               # Z eigenvalues (2^n, n)
    zz: np.ndarray              # sum_ij J_ij z_i z_j
    lean_z: np.ndarray
    mix_z: np.ndarray
    true_bit: np.ndarray        # F5: x_k for "claim k true" (+1 yes-aligned / -1), 0 for hedges
    xs: np.ndarray              # F5 spins (2^n, n), +1 = yes-aligned (index bit 0)


def item_data(rec, solver="anchored") -> ItemData:
    web = encoder.build_web(rec["contentions"], rec["pairs"])
    lean = np.where(np.abs(web.lean) <= 0.1, 0.0, web.lean)
    web = encoder.Web(web.confidence, lean, web.edges)
    if solver == "anchored":
        phi = er.exp5_phases(web)
    else:                       # sensitivity: the plain v1 solver, hedges still at pi/2
        orig = encoder.solve_phases_anchored
        encoder.solve_phases_anchored = encoder.solve_phases
        try:
            phi = er.exp5_phases(web)
        finally:
            encoder.solve_phases_anchored = orig
    n = web.n
    bits = v2.bits(n)
    z = 1 - 2 * bits
    w = np.abs(lean)
    w = w / w.sum() if w.sum() > 0 else np.full(n, 1 / n)
    m = z @ w                    # in the X basis, bit 0 = |+> = yes-aligned, so the same sign table applies
    piM = np.where(m > 1e-12, 1.0, np.where(m < -1e-12, 0.0, 0.5))
    zz = np.zeros(2 ** n)
    for i, j, J in web.edges:
        zz += J * z[:, i] * z[:, j]
    return ItemData(rec["id"], n, web.confidence * math.pi / 2, phi, lean, web.edges, w, m, piM, z, zz,
                    z @ lean, z.sum(axis=1), np.sign(lean).astype(float), z.astype(float))


# --- A5 / D5 ------------------------------------------------------------------------

def _all(psi, n, u):
    return v2._all(psi, n, u)


def a5_prep(it: ItemData, kappa: float) -> np.ndarray:
    psi = np.zeros(2 ** it.n, complex)
    psi[0] = 1
    for k in range(it.n):
        psi = v2._apply_1q(psi, it.n, k, v2._rz(it.phi[k]) @ v2._ry(it.theta[k]))
    return psi * np.exp(-0.5j * kappa * it.zz)


def a5_step(psi, it: ItemData, kappa, gamma, beta):
    """One Trotter step of arm A's evolution: exp(+i g (kappa/kappa0) J XX), lean fields, mixer exp(+i b Z)."""
    psi = _all(psi, it.n, H2)
    psi = psi * np.exp(1j * gamma * (kappa / KAPPA0) * it.zz) * np.exp(1j * gamma * it.lean_z)
    psi = _all(psi, it.n, H2)
    return psi * np.exp(1j * beta * it.mix_z)


def n_vec(phi):
    return np.array([1, np.exp(1j * phi)], complex) / math.sqrt(2)


def pk_op(phi):
    v = n_vec(phi)
    return np.outer(v, v.conj())


def a5_expect_S(psi, it, k):
    P = pk_op(it.phi[k])
    return float(np.real(np.vdot(psi, v2._apply_1q(psi, it.n, k, P))))


def a5_update_S(psi, it, k, p):
    P = pk_op(it.phi[k])
    E = math.sqrt(p) * P + math.sqrt(1 - p) * (np.eye(2) - P)
    psi = v2._apply_1q(psi, it.n, k, E)
    return psi / np.linalg.norm(psi)


def a5_expect_M(psi, it):
    px = np.abs(_all(psi, it.n, H2)) ** 2
    return float(px @ it.piM)


def a5_update_M(psi, it, p=None, choice=None):
    x = _all(psi, it.n, H2)
    if choice is None:
        e = p * it.piM + (1 - p) * (1 - it.piM)
    else:
        e = it.piM if choice == "yes" else 1 - it.piM
    x = x * np.sqrt(e)
    x = x / np.linalg.norm(x)
    return _all(x, it.n, H2)


def link(p, a, b):
    return 100 * (a + (b - a) * p)


def p_obs(r, a, b):
    return float(np.clip((r / 100 - a) / (b - a), 0.01, 0.99))


def run_a5(it: ItemData, conv_turns, params, dephase=False):
    """Returns [(predicted, observed, kind)] for every rating."""
    kappa, gamma, beta, a, b = params
    psi = a5_prep(it, kappa)
    if dephase:
        return run_d5(it, conv_turns, params, psi)
    out = []
    for t in conv_turns:
        psi = a5_step(psi, it, kappa, gamma, beta)
        if t["kind"] == "S":
            out.append((link(a5_expect_S(psi, it, t["claim"]), a, b), t["rating"], "S"))
            psi = a5_update_S(psi, it, t["claim"], p_obs(t["rating"], a, b))
        elif t["kind"] == "M":
            out.append((link(a5_expect_M(psi, it), a, b), t["rating"], "M"))
            psi = a5_update_M(psi, it, p=p_obs(t["rating"], a, b))
        elif t["kind"] == "C":
            psi = a5_update_M(psi, it, choice=t["answer"])
    return out


def run_d5(it, conv_turns, params, psi):
    """Dephased A5: populations in the X basis; each step flips every qubit independently w.p. sin^2(beta)."""
    kappa, gamma, beta, a, b = params
    p = np.abs(_all(psi, it.n, H2)) ** 2
    flip = math.sin(beta) ** 2
    idx = np.arange(2 ** it.n)
    out = []
    for t in conv_turns:
        for k in range(it.n):
            p = (1 - flip) * p + flip * p[idx ^ (1 << k)]
        if t["kind"] == "S":
            k = t["claim"]
            # <x|P_k|x> = (1 + cos(phi_k) x_k) / 2 in the X basis
            pt = (1 + math.cos(it.phi[k]) * it.xs[:, k]) / 2
            out.append((link(float(p @ pt), a, b), t["rating"], "S"))
            q = p_obs(t["rating"], a, b)
            # diag(sqrt(E) rho sqrt(E)) for diagonal rho, E = q P + (1-q)(1-P), P on qubit k
            P = pk_op(it.phi[k])
            E = math.sqrt(q) * P + math.sqrt(1 - q) * (np.eye(2) - P)
            Ex = H2 @ E @ H2                      # in the X basis
            M2 = np.abs(Ex) ** 2                  # |<x'|sqrtE|x>|^2 on qubit k
            b_ = (idx >> k) & 1
            new = M2[b_, b_] * p + M2[b_, 1 - b_] * p[idx ^ (1 << k)]
            p = new / new.sum()
        elif t["kind"] == "M":
            out.append((link(float(p @ it.piM), a, b), t["rating"], "M"))
            q = p_obs(t["rating"], a, b)
            e = q * it.piM + (1 - q) * (1 - it.piM)
            p = p * e / (p @ e)
        elif t["kind"] == "C":
            e = it.piM if t["answer"] == "yes" else 1 - it.piM
            p = p * e / (p @ e)
    return out


# --- F5 ------------------------------------------------------------------------

def f5_sweep(P, it, kappa_f, T):
    idx = np.arange(2 ** it.n)
    for k in range(it.n):
        local = np.zeros(2 ** it.n)
        for i, j, J in it.edges:
            if i == k:
                local += J * it.xs[:, j]
            elif j == k:
                local += J * it.xs[:, i]
        p_up = 1 / (1 + np.exp(-2 * kappa_f * local / T))
        marg = P + P[idx ^ (1 << k)]
        P = np.where(it.xs[:, k] == 1, p_up, 1 - p_up) * marg
    return P / P.sum()


def run_f5(it: ItemData, conv_turns, params):
    kappa_f, T, lam, a, b = params
    pt = (1 + np.sin(it.theta)) / 2                     # P(claim k true)
    py = np.where(it.true_bit > 0, pt, np.where(it.true_bit < 0, 1 - pt, 0.5))   # P(x_k = +1)
    bits = v2.bits(it.n)
    P = np.prod(np.where(bits == 0, py, 1 - py), axis=1)
    P = f5_sweep(P, it, kappa_f, T)
    out = []
    for t in conv_turns:
        P = (1 - lam) * P + lam * f5_sweep(P, it, kappa_f, T)
        if t["kind"] == "S":
            k = t["claim"]
            ev = (it.xs[:, k] == it.true_bit[k]).astype(float) if it.true_bit[k] != 0 else np.full(len(P), 0.5)
            out.append((link(float(P @ ev), a, b), t["rating"], "S"))
            q = p_obs(t["rating"], a, b)
            P = P * (q * ev + (1 - q) * (1 - ev))
            P = P / P.sum()
        elif t["kind"] == "M":
            out.append((link(float(P @ it.piM), a, b), t["rating"], "M"))
            q = p_obs(t["rating"], a, b)
            P = P * (q * it.piM + (1 - q) * (1 - it.piM))
            P = P / P.sum()
        elif t["kind"] == "C":
            e = it.piM if t["answer"] == "yes" else 1 - it.piM
            P = P * e / (P @ e)
    return out


# --- BA5 -----------------------------------------------------------------------

def run_ba5(it: ItemData, conv_turns, params, c0, model_side):
    """M ratings only. model_side = +1 if the model answered yes, -1 if no."""
    w_supp, w_con, rho, a, b = params
    C = c0
    s_turns = [t for t in conv_turns if t["kind"] == "S"]
    out, seen = [], 0
    for t in conv_turns:
        if t["kind"] == "S":
            seen += 1
            k = t["claim"]
            side = math.copysign(1, it.lean[k]) if it.lean[k] != 0 else 0
            w = w_supp if side == model_side else w_con
            C = C + w * (t["rating"] - 50) * side * rho ** (len(s_turns) - seen)
        elif t["kind"] == "M":
            out.append((link(float(np.clip(C / 100, 0, 1)), a, b), t["rating"], "M"))
    return out


# --- parameter spaces -------------------------------------------------------------

SPACES = {
    "A5": [("kappa", 0, 2), ("gamma", 0, 1.5), ("beta", 0, 1.5), ("a", 0, 0.4), ("b", 0.6, 1)],
    "A5k0": [("gamma", 0, 1.5), ("beta", 0, 1.5), ("a", 0, 0.4), ("b", 0.6, 1)],     # kappa pinned at 0
    "F5": [("kappa_F", 0, 3), ("T", 0.2, 5), ("lam", 0, 1), ("a", 0, 0.4), ("b", 0.6, 1)],
    "D5": [("kappa", 0, 2), ("gamma", 0, 1.5), ("beta", 0, 1.5), ("a", 0, 0.4), ("b", 0.6, 1)],
    "BA5": [("w_supp", 0, 2), ("w_con", 0, 2), ("rho", 0, 1), ("a", 0, 0.4), ("b", 0.6, 1)],
}
SPACES["A5plain"] = SPACES["A5"]
A5_0 = [KAPPA0, config.GAMMA0, config.BETA0, 0.0, 1.0]
F5_0 = [1.0, 1.0, 1.0, 0.0, 1.0]


def predict(model, it, turns, v, extra=None):
    if model in ("A5", "A5plain"):
        return run_a5(it, turns, v)
    if model == "A5k0":
        return run_a5(it, turns, [0.0, *v])
    if model == "D5":
        return run_a5(it, turns, v, dephase=True)
    if model == "F5":
        return run_f5(it, turns, v)
    return run_ba5(it, turns, v, *extra)

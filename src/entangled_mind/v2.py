"""Version two: learned encodings (experiments/preregistration-v2.md).

Three models with 9 parameters each, scored by exact computation (no sampling):

A2  learned quantum encoding: arm A's circuit with learnable confidence-to-angle
    scale, per-relation-type coupling scales, Trotter steps N in 0..4, step
    scales, readout-basis angle, strong-camp threshold tau, and a flag threshold.
    Simulated exactly with a vectorised statevector (fast_quantum_probs), which
    reproduces encoder.build_circuit for v1 parameter values.
F2  learned classical twin: the same graph, phases, priors and couplings, but a
    classical distribution evolved by N heat-bath sweeps (inverse temperature
    schedule, independent-flip mixing) - no amplitudes, no interference.
L   linear score on 8 relation-web features plus a bias (logistic-regression form).

All three are fitted by the same rule (fit_model): maximise train AUROC with a
fixed evaluation budget, select among climbed candidates on validation AUROC."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from . import config, readout
from .encoder import SIGN, Web

# ---------------------------------------------------------------------------
# shared preparation


@dataclass
class Item:
    id: str
    wrong: bool
    conf: np.ndarray
    lean: np.ndarray
    edges: list            # (i, j, relation, strength)

    @property
    def n(self) -> int:
        return len(self.conf)


def item_from_record(r: dict) -> Item:
    edges = [(p["i"], p["j"], p["relation"], p["strength"]) for p in r["pairs"]
             if p["relation"] != "unrelated" and p["strength"] > 0]
    return Item(r["id"], r["correct"] is False, np.array([c["confidence"] for c in r["contentions"]]),
                np.array([c["lean"] for c in r["contentions"]]), edges)


def solve_phases_fast(web: Web, restarts: int = 8, iters: int = 1500, lr: float = 0.05, seed: int = 0,
                      tol: float = 1e-10) -> np.ndarray:
    """encoder.solve_phases with all restarts run as one array (same starts, step and update rule),
    stopping early once every restart's gradient is below `tol`."""
    n = web.n
    J = np.zeros((n, n))
    for i, j, w in web.edges:
        J[i, j] = J[j, i] = w
    h = web.lean
    rng = np.random.default_rng(seed)
    starts = [np.where(h < 0, math.pi, 0.0), np.zeros(n)] + [rng.uniform(-math.pi, math.pi, n) for _ in range(restarts - 2)]
    phi = np.array(starts, float)                                  # (R, n)
    for _ in range(iters):
        d = phi[:, :, None] - phi[:, None, :]
        grad = np.einsum("ij,rij->ri", J, np.sin(d)) + h * np.sin(phi)
        phi -= lr * grad
        if np.abs(grad).max() < tol:
            break
    d = phi[:, :, None] - phi[:, None, :]
    e = -0.5 * np.einsum("ij,rij->r", J, np.cos(d)) - np.cos(phi) @ h
    best = int(np.argmin(e + np.arange(len(e)) * 1e-12))           # first minimum, as the serial loop keeps
    return np.mod(phi[best] + math.pi, 2 * math.pi) - math.pi


def coupled_web(it: Item, k_sup: float, k_con: float) -> Web:
    scale = {"supports": k_sup, "contradicts": k_con}
    return Web(it.conf, it.lean, tuple((i, j, SIGN[rel] * scale[rel] * s) for i, j, rel, s in it.edges))


_BITS: dict[int, np.ndarray] = {}


def bits(n: int) -> np.ndarray:
    """(2^n, n) array; row = basis index, column k = bit of qubit k (little-endian)."""
    if n not in _BITS:
        _BITS[n] = (np.arange(2 ** n)[:, None] >> np.arange(n)) & 1
    return _BITS[n]


def weights(it: Item) -> np.ndarray:
    w = np.abs(it.lean)
    return w / w.sum() if w.sum() > 0 else np.full(it.n, 1 / it.n)


def conflict_from_probs(p: np.ndarray, it: Item, tau: float) -> float:
    m = (1 - 2 * bits(it.n)) @ weights(it)         # bit 0 = yes -> +1
    return float(2 * min(p[m >= tau].sum(), p[m <= -tau].sum()))


# ---------------------------------------------------------------------------
# A2: quantum


def _apply_1q(psi: np.ndarray, n: int, k: int, u: np.ndarray) -> np.ndarray:
    psi = psi.reshape([2] * n)                     # axis n-1-k is qubit k (little-endian)
    psi = np.moveaxis(np.tensordot(u, psi, axes=([1], [n - 1 - k])), 0, n - 1 - k)
    return psi.reshape(-1)


def _ry(t):
    c, s = math.cos(t / 2), math.sin(t / 2)
    return np.array([[c, -s], [s, c]], complex)


def _rz(t):
    return np.diag([np.exp(-0.5j * t), np.exp(0.5j * t)])


H = np.array([[1, 1], [1, -1]], complex) / math.sqrt(2)


def _all(psi, n, u):
    for k in range(n):
        psi = _apply_1q(psi, n, k, u)
    return psi


def fast_quantum_state(it: Item, s_theta: float, k_sup: float, k_con: float, n_trotter: int,
                       gamma0: float, beta0: float, phi: np.ndarray | None = None) -> np.ndarray:
    """Pre-readout statevector of the (learned) arm-A circuit (computational basis).
    `phi` overrides the solved phases (used by the v2.1 honest-hedge encoding)."""
    n = it.n
    web = coupled_web(it, k_sup, k_con)
    if phi is None:
        phi = solve_phases_fast(web)
    theta = np.clip(s_theta * it.conf, 0, 2) * math.pi / 2
    psi = np.zeros(2 ** n, complex)
    psi[0] = 1
    for k in range(n):
        psi = _apply_1q(psi, n, k, _rz(phi[k]) @ _ry(theta[k]))
    z = 1 - 2 * bits(n)                             # Z eigenvalues, (2^n, n)
    zz = np.zeros(2 ** n)
    for i, j, J in web.edges:
        zz += J * z[:, i] * z[:, j]
    psi = psi * np.exp(-0.5j * config.KAPPA * zz)                        # prep RZZ(kappa J)
    lean_z = z @ web.lean
    mix_z = z.sum(axis=1)
    for step in range(1, n_trotter + 1):
        s = step / (n_trotter + 1)
        g, b = gamma0 * s, beta0 * (1 - s)
        psi = _all(psi, n, H)
        psi = psi * np.exp(-0.5j * (-2 * g) * zz) * np.exp(-0.5j * (-2 * g) * lean_z)
        psi = _all(psi, n, H)
        psi = psi * np.exp(-0.5j * (-2 * b) * mix_z)
    return psi


def fast_quantum_probs(it: Item, s_theta: float, k_sup: float, k_con: float, n_trotter: int,
                       gamma0: float, beta0: float, alpha: float) -> np.ndarray:
    """Exact readout distribution of the (learned) arm-A circuit. alpha = 0 is the v1 X-basis readout."""
    psi = fast_quantum_state(it, s_theta, k_sup, k_con, n_trotter, gamma0, beta0)
    psi = _all(psi, it.n, _ry(-math.pi / 2 + alpha))   # alpha = 0: |+> -> |0>, the X-basis readout
    return np.abs(psi) ** 2


# ---------------------------------------------------------------------------
# F2: classical twin


def fast_classical_probs(it: Item, s_theta: float, k_sup: float, k_con: float, n_sweeps: int,
                         beta_t: float, flip: float, field: float, phi: np.ndarray | None = None,
                         alpha: float = 0.0) -> np.ndarray:
    """Exact distribution after N sequential heat-bath sweeps of the classical Ising twin.
    Prior: independent spins with P(yes) = (1 + sin(theta) cos(phi)) / 2, the same single-contention
    marginals as A2's preparation. Sweep t uses inverse temperature beta_t * s_t and then flips each
    spin independently with probability flip * (1 - s_t) / 2."""
    n = it.n
    web = coupled_web(it, k_sup, k_con)
    if phi is None:
        phi = solve_phases_fast(web)
    theta = np.clip(s_theta * it.conf, 0, 2) * math.pi / 2
    # alpha != 0 (F2+, Addendum D): the marginal an uncoupled qubit gives when measured along an axis tilted by alpha
    py = np.clip((1 + np.sin(theta) * np.cos(phi) * np.cos(alpha) + np.cos(theta) * np.sin(alpha)) / 2, 1e-9, 1 - 1e-9)
    b = bits(n)
    x = 1 - 2 * b                                   # +1 yes
    p = np.prod(np.where(b == 0, py, 1 - py), axis=1)
    Jm = np.zeros((n, n))
    for i, j, J in web.edges:
        Jm[i, j] = Jm[j, i] = J
    idx = np.arange(2 ** n)
    for t in range(1, n_sweeps + 1):
        s = t / (n_sweeps + 1)
        bt, fl = beta_t * s, flip * (1 - s) / 2
        for k in range(n):
            partner = idx ^ (1 << k)
            local = field * web.lean[k] + x @ Jm[k]           # field on spin k (x_k has no self-coupling)
            p_up = 1 / (1 + np.exp(-2 * bt * local))           # P(x_k = +1 | rest)
            marg = p + p[partner]                              # mass of the configuration ignoring spin k
            p = np.where(x[:, k] == 1, p_up, 1 - p_up) * marg
        if fl > 0:
            for k in range(n):
                p = (1 - fl) * p + fl * p[idx ^ (1 << k)]
    return p / p.sum()


# ---------------------------------------------------------------------------
# v2.1 "honest hedge" (preregistration-v2.md, Addendum B) and the H baseline

NO_LEAN = 0.1


def hedge_mask(it: Item) -> np.ndarray:
    return np.abs(it.lean) <= NO_LEAN


def hedged(it: Item) -> Item:
    """The item with every no-lean claim's lean set to exactly 0."""
    return Item(it.id, it.wrong, it.conf, np.where(hedge_mask(it), 0.0, it.lean), it.edges)


def hedge_phases(web: Web, mask: np.ndarray) -> np.ndarray:
    """Hedges fixed at pi/2 (neutral); the phase solver runs on the leaning claims and their mutual edges only."""
    keep = np.where(~mask)[0]
    phi = np.full(web.n, math.pi / 2)
    if len(keep):
        pos = {k: a for a, k in enumerate(keep)}
        sub = Web(web.confidence[keep], web.lean[keep],
                  tuple((pos[i], pos[j], J) for i, j, J in web.edges if i in pos and j in pos))
        phi[keep] = solve_phases_fast(sub)
    return phi


def uncertainty(it: Item) -> float:
    m = hedge_mask(it)
    return float(it.conf[m].sum() / it.conf.sum()) if it.conf.sum() > 0 else 0.0


def hedge_scores(it: Item) -> tuple[float, int]:
    """H baseline: (total confidence of no-lean claims, number of no-lean claims)."""
    m = hedge_mask(it)
    return float(it.conf[m].sum()), int(m.sum())


def conflict21(it: Item, quantum: bool, v) -> float:
    """v2.1 conflict score for A2.1 (quantum=True) or F2.1: conflict(tau) + lambda_h * U."""
    *a, tau, lam = v
    h = hedged(it)
    phi = hedge_phases(coupled_web(h, a[1], a[2]), hedge_mask(it))
    if quantum:
        psi = fast_quantum_state(h, a[0], a[1], a[2], int(a[3]), a[4], a[5], phi=phi)
        p = np.abs(_all(psi, h.n, _ry(-math.pi / 2 + a[6]))) ** 2
    else:
        p = fast_classical_probs(h, a[0], a[1], a[2], int(a[3]), a[4], a[5], a[6], phi=phi)
    return conflict_from_probs(p, h, tau) + lam * uncertainty(it)


def build_a21_circuit(it: Item, v, measure: bool = True):
    """The selected A2.1 as a Qiskit circuit (Addendum C): reproduces conflict21's exact probabilities
    gate for gate, so it can run on the noisy simulator. Returns (circuit, hedged item, U)."""
    from qiskit import QuantumCircuit
    *a, tau, lam = v
    s_theta, k_sup, k_con, n_trotter, gamma0, beta0, alpha = a[0], a[1], a[2], int(a[3]), a[4], a[5], a[6]
    h = hedged(it)
    web = coupled_web(h, k_sup, k_con)
    phi = hedge_phases(web, hedge_mask(it))
    theta = np.clip(s_theta * h.conf, 0, 2) * math.pi / 2
    n = h.n
    qc = QuantumCircuit(n, name="A2.1")
    for k in range(n):
        qc.ry(float(theta[k]), k)
        qc.rz(float(phi[k]), k)
    for i, j, J in web.edges:
        qc.rzz(config.KAPPA * J, i, j)
    for step in range(1, n_trotter + 1):
        s_ = step / (n_trotter + 1)
        g, b = gamma0 * s_, beta0 * (1 - s_)
        qc.h(range(n))
        for i, j, J in web.edges:
            qc.rzz(-2 * g * J, i, j)
        for k in range(n):
            if web.lean[k]:
                qc.rz(float(-2 * g * web.lean[k]), k)
        qc.h(range(n))
        for k in range(n):
            qc.rz(-2 * b, k)
    for k in range(n):
        qc.ry(-math.pi / 2 + alpha, k)
    if measure:
        qc.measure_all()
    return qc, h, uncertainty(it)


def conflict21_from_counts(counts: dict, h: Item, u: float, v) -> float:
    *_, tau, lam = v
    p = np.zeros(2 ** h.n)
    for bs, c in counts.items():
        p[int(bs.replace(" ", ""), 2)] += c
    return conflict_from_probs(p / p.sum(), h, tau) + lam * u


# ---------------------------------------------------------------------------
# L: linear score on relation-web features


def features(it: Item) -> np.ndarray:
    contra = [s for *_, rel, s in it.edges if rel == "contradicts"]
    sup = [s for *_, rel, s in it.edges if rel == "supports"]
    vote = np.dot(it.conf, it.lean)
    against = np.sum(it.conf * (np.sign(it.lean) == -np.sign(vote)) * (it.lean != 0)) / max(it.conf.sum(), 1e-9)
    return np.array([len(contra), sum(contra), sum(sup), it.n, it.conf.mean(),
                     len(it.edges), np.abs(it.lean).mean(), against], float)


FEATURE_NAMES = ["contradiction count", "total contradiction strength", "total support strength", "number of claims",
                 "mean confidence", "number of related pairs", "mean |lean|", "confidence mass leaning against the vote"]


# ---------------------------------------------------------------------------
# parameter spaces (9 parameters each) and scoring

SPACES = {
    "A2": [("s_theta", 0.2, 2.0), ("k_sup", -1.5, 1.5), ("k_con", -1.5, 1.5), ("n_trotter", 0, 4),
           ("gamma0", 0.0, 1.5), ("beta0", 0.0, 1.5), ("alpha", -math.pi / 2, math.pi / 2), ("tau", 0.05, 0.6)],
    "F2": [("s_theta", 0.2, 2.0), ("k_sup", -1.5, 1.5), ("k_con", -1.5, 1.5), ("n_sweeps", 0, 4),
           ("beta_t", 0.0, 3.0), ("flip", 0.0, 1.0), ("field", 0.0, 2.0), ("tau", 0.05, 0.6)],
    "L": [(f"w{k}", -3.0, 3.0) for k in range(8)],
}
SPACES["A21"] = SPACES["A2"] + [("lambda_h", 0.0, 2.0)]
SPACES["F2P"] = SPACES["F2"][:-1] + [("alpha", -math.pi / 2, math.pi / 2), SPACES["F2"][-1]]   # Addendum D
SPACES["F21"] = SPACES["F2"] + [("lambda_h", 0.0, 2.0)]
# + one flag threshold per model (chosen on train after fitting), and a bias for L, which AUROC ignores:
# 8 scored parameters + 1 threshold = 9 for every model.
INTEGER = {"n_trotter", "n_sweeps"}


def clamp(model: str, v: np.ndarray) -> np.ndarray:
    out = v.copy()
    for k, (name, lo, hi) in enumerate(SPACES[model]):
        out[k] = min(hi, max(lo, out[k]))
        if name in INTEGER:
            out[k] = round(out[k])
    return out


class Scorer:
    """Conflict / error score of every item under one parameter vector. Features are standardised on train."""

    def __init__(self, model: str, items: list[Item], feat_mu=None, feat_sd=None):
        self.model, self.items = model, items
        if model == "L":
            F = np.array([features(it) for it in items])
            self.mu = F.mean(0) if feat_mu is None else feat_mu
            self.sd = (F.std(0) + 1e-9) if feat_sd is None else feat_sd
            self.F = (F - self.mu) / self.sd

    def scores(self, v: np.ndarray) -> np.ndarray:
        v = clamp(self.model, v)
        if self.model == "L":
            return self.F @ v
        if self.model in ("A21", "F21"):
            return np.array([conflict21(it, self.model == "A21", v) for it in self.items])
        if self.model == "A2":
            *a, tau = v
            return np.array([conflict_from_probs(fast_quantum_probs(it, a[0], a[1], a[2], int(a[3]), a[4], a[5], a[6]),
                                                 it, tau) for it in self.items])
        *a, tau = v
        if self.model == "F2P":
            return np.array([conflict_from_probs(fast_classical_probs(it, a[0], a[1], a[2], int(a[3]), a[4], a[5], a[6],
                                                                      alpha=a[7]), it, tau) for it in self.items])
        return np.array([conflict_from_probs(fast_classical_probs(it, a[0], a[1], a[2], int(a[3]), a[4], a[5], a[6]),
                                             it, tau) for it in self.items])

    def auroc(self, v: np.ndarray) -> float:
        s = self.scores(v)
        y = np.array([it.wrong for it in self.items])
        return readout.auroc(list(s[y]), list(s[~y]))


def fit_model(model: str, train: Scorer, val: Scorer, seed: int, n_random: int = 400, n_climb: int = 10,
              steps: int = 60, log=None) -> dict:
    """The shared fitting rule. n_random uniform samples; hill-climb the n_climb best on train AUROC with
    `steps` Gaussian perturbations each (sd = 10% of each range, integers move by +-1); the final
    parameters are the climbed candidate with the highest validation AUROC (ties: higher train AUROC)."""
    rng = np.random.default_rng(seed)
    lo = np.array([s[1] for s in SPACES[model]])
    hi = np.array([s[2] for s in SPACES[model]])
    cands = [clamp(model, lo + rng.random(len(lo)) * (hi - lo)) for _ in range(n_random)]
    scored = sorted(((train.auroc(v), k) for k, v in enumerate(cands)), reverse=True)
    climbed = []
    for rank, (a0, k) in enumerate(scored[:n_climb]):
        v, best = cands[k], a0
        for _ in range(steps):
            prop = clamp(model, v + rng.normal(0, 0.1, len(v)) * (hi - lo))
            a = train.auroc(prop)
            if a >= best:
                v, best = prop, a
        va = val.auroc(v)
        climbed.append({"params": v.tolist(), "train_auroc": best, "val_auroc": va})
        if log:
            log(f"{model} candidate {rank + 1}/{n_climb}: train {best:.3f} val {va:.3f}")
    final = max(climbed, key=lambda c: (c["val_auroc"], c["train_auroc"]))
    return {"model": model, "names": [s[0] for s in SPACES[model]], "final": final, "candidates": climbed,
            "evaluations": n_random + n_climb * steps}


def train_threshold(scores: np.ndarray, wrong: np.ndarray) -> float:
    """The 9th parameter: flag threshold maximising Youden's J on train."""
    best, thr = -1, float("inf")
    for t in np.unique(scores):
        tpr, fpr = np.mean(scores[wrong] > t), np.mean(scores[~wrong] > t)
        if tpr - fpr > best:
            best, thr = tpr - fpr, float(t)
    return thr

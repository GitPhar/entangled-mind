"""Turn measurement counts (or the classical control) into a judgment, a
confidence, and a conflict score."""

from __future__ import annotations

import numpy as np

from . import config
from .encoder import Web


def _weights(web: Web) -> np.ndarray:
    w = np.abs(web.lean)
    return w / w.sum() if w.sum() > 0 else np.full(web.n, 1 / web.n)


def magnetisation(bitstring: str, w: np.ndarray) -> float:
    """m in [-1, 1]: weighted vote of the qubits, +1 = every contention yes-aligned.
    Qiskit bitstrings are little-endian (rightmost char is qubit 0); bit 0 = yes."""
    bits = np.array([int(b) for b in reversed(bitstring.replace(" ", ""))])
    return float(np.dot(w, 1 - 2 * bits))


def quantum_readout(counts: dict[str, int], web: Web, tau: float = config.STRONG_TAU) -> dict:
    w = _weights(web)
    shots = sum(counts.values())
    p_yes = p_strong_yes = p_strong_no = 0.0
    for bs, c in counts.items():
        m = magnetisation(bs, w)
        p = c / shots
        p_yes += p if m > 0 else (p / 2 if m == 0 else 0)
        p_strong_yes += p if m >= tau else 0
        p_strong_no += p if m <= -tau else 0
    return {
        "judgment": "yes" if p_yes >= 0.5 else "no",
        "p_yes": p_yes,
        "confidence": max(p_yes, 1 - p_yes),
        "p_strong_yes": p_strong_yes,
        "p_strong_no": p_strong_no,
        # mass on the weaker of two strongly-opposed camps, scaled to [0, 1]
        "conflict_score": 2 * min(p_strong_yes, p_strong_no),
        "shots": shots,
    }


def classical_readout(web: Web) -> dict:
    """Arm E: no qubits. Judgment from confidence-weighted leans; conflict
    score = total contradiction strength in the relation web."""
    contra = [-J for _, _, J in web.edges if J < 0]
    vote = float(np.dot(web.confidence, web.lean))
    return {
        "judgment": "yes" if vote >= 0 else "no",
        "vote": vote,
        "contradiction_count": len(contra),
        "conflict_score": float(sum(contra)),
    }


def calibrate_threshold(scores: list[float], flag_fraction: float = config.CALIBRATION_FLAG_FRACTION) -> float:
    """Threshold such that `score > threshold` flags roughly the top `flag_fraction`
    of the calibration pool."""
    return float(np.quantile(np.asarray(scores, float), 1 - flag_fraction))


def auroc(pos: list[float], neg: list[float]) -> float | None:
    """P(score of a wrong item > score of a right item), ties count half."""
    if not pos or not neg:
        return None
    gt = sum((p > q) + 0.5 * (p == q) for p in pos for q in neg)
    return gt / (len(pos) * len(neg))

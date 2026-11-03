import numpy as np

from entangled_mind import readout
from entangled_mind.encoder import Web

WEB = Web(np.array([1.0, 1.0, 1.0]), np.array([1.0, 1.0, -1.0]), ())


def test_magnetisation_is_little_endian():
    w = np.array([0.5, 0.25, 0.25])
    assert readout.magnetisation("110", w) == 0.0     # qubit 0 yes (+0.5), qubits 1,2 no
    assert readout.magnetisation("000", w) == 1.0


def test_even_split_between_opposed_camps_is_maximal_conflict():
    r = readout.quantum_readout({"000": 500, "111": 500}, WEB)
    assert r["conflict_score"] == 1.0
    assert readout.quantum_readout({"000": 1000}, WEB)["conflict_score"] == 0.0


def test_classical_score_sums_contradiction_strength():
    web = Web(np.ones(3), np.zeros(3), ((0, 1, -0.5), (1, 2, -0.25), (0, 2, 0.9)))
    assert readout.classical_readout(web)["conflict_score"] == 0.75


def test_auroc():
    assert readout.auroc([3, 4], [1, 2]) == 1.0
    assert readout.auroc([1], [1]) == 0.5


def test_classical_twin_ground_state_and_conflict():
    from entangled_mind.classical_twin import classical_twin_readout
    agree = Web(np.array([1.0, 1.0]), np.array([0.5, 0.5]), ((0, 1, 1.0),))
    r = classical_twin_readout(agree)
    assert r["judgment"] == "yes" and r["conflict_score"] == 0.0
    # zero fields + one ferromagnetic bond: ground states ++ and -- split the vote evenly
    split = Web(np.array([1.0, 1.0]), np.array([0.0, 0.0]), ((0, 1, 1.0),))
    assert classical_twin_readout(split)["ground_degeneracy"] == 2
    assert classical_twin_readout(split)["conflict_score"] == 1.0

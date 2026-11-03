import math

import numpy as np

from entangled_mind import encoder

CONTENTIONS = [{"text": t, "confidence": c, "lean": l}
               for t, c, l in [("a", 0.9, 0.8), ("b", 0.8, 0.6), ("c", 0.7, -0.7), ("d", 0.5, 0.0)]]
PAIRS = [{"i": 0, "j": 1, "relation": "supports", "strength": 0.9},
         {"i": 0, "j": 2, "relation": "contradicts", "strength": 0.8},
         {"i": 1, "j": 3, "relation": "unrelated", "strength": 0.0}]


def test_web_keeps_only_related_pairs():
    web = encoder.build_web(CONTENTIONS, PAIRS)
    assert web.edges == ((0, 1, 0.9), (0, 2, -0.8))


def test_phases_align_support_and_oppose_contradiction():
    phi = encoder.solve_phases(encoder.build_web(CONTENTIONS, PAIRS))
    d = lambda a, b: abs(math.remainder(phi[a] - phi[b], 2 * math.pi))
    assert d(0, 1) < 0.5
    assert d(0, 2) > math.pi - 0.5


def test_arm_c_has_no_two_qubit_gates():
    web = encoder.build_web(CONTENTIONS, PAIRS)
    assert "rzz" in encoder.build_circuit(web, entangle=True).count_ops()
    assert "rzz" not in encoder.build_circuit(web, entangle=False).count_ops()


def test_shuffle_preserves_count_and_strengths():
    web = encoder.build_web(CONTENTIONS, PAIRS)
    shuf = encoder.shuffled_web(web, seed=3)
    assert len(shuf.edges) == len(web.edges)
    assert sorted(J for *_, J in shuf.edges) == sorted(J for *_, J in web.edges)
    assert np.array_equal(shuf.confidence, web.confidence)

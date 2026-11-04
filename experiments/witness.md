# Entanglement witness on the belief state: design (not submitted)

Written 2026-11-03. **Status: designed and simulated, not submitted.** Submitting needs Sean's approval of the QPU budget below. Design script: `experiments/witness_design.py`. Simulated output: `results/witness-design.json`.

## Why this measurement

At 5–16 qubits, every belief state in this project is exactly classically simulable, so running it on hardware gives no speedup. What hardware *can* do is certify that the physical device actually held the entangled state the encoding describes, rather than a classical mixture that merely reproduces the same yes/no statistics. Stage 2's readout measures only in the yes/no basis, and a separable state could imitate that. A witness needs measurements in several bases.

## Observable

For each chosen item, take the related pair of contentions (*i*, *j*) whose two-qubit reduced state in arm A's noiseless belief state has the largest **negativity**, N(ρ_ij) = Σ|negative eigenvalues of ρ_ij^{T_j}|.
- For two qubits, N > 0 if and only if the pair is entangled (the PPT criterion is exact at 2×2).
- N = 0 for every separable state.
- The maximum is 0.5, for a Bell state.

Entanglement in the reduced pair state implies the whole belief state is entangled.

## Protocol

1. **Items:** prepare arm A's state (RY/RZ prep, RZZ entanglers, N = 2 Trotter steps, no final readout rotation). Items are chosen by a fixed rule: the 3 Stage 2 run-2 test items with the largest ideal pair negativity.
2. **Settings:** for each item, the 9 local Pauli settings {X, Y, Z} ⊗ {X, Y, Z} on qubits *i* and *j*, measuring only those two qubits. That gives 9 circuits per item.
3. **Readout calibration:** 4 circuits per item preparing |00⟩, |01⟩, |10⟩ and |11⟩ on the same two physical qubits. They give a 4×4 assignment matrix, which is inverted to mitigate readout error.
4. **Shots:** 4,000 per circuit. 3 items × (9 + 4) = **39 circuits, all in one SamplerV2 job inside a Batch.**
5. **Reconstruction:** linear-inversion tomography of ρ_ij, projected to the nearest physical state.
6. **Witness:** negativity, with a 95% interval from 500 parametric bootstrap resamples of the counts.
7. **Pass rule (fixed in advance):** entanglement is **certified** for an item if the bootstrap 95% lower bound on N is above 0. The run is a **success** if at least 2 of the 3 items are certified.

## Prediction from the noisy simulator (noise model from `ibm_fez`)

| item | qubits | target pair | physical qubits | CZ per circuit | N ideal | N noisy sim | noisy-sim 95% lower bound |
|---|---|---|---|---|---|---|---|
| `h221` | 8 | (0, 6), J = +0.5 | 10, 9 | 137 | 0.184 | 0.167 | 0.154 |
| `h088` | 8 | (5, 6), J = +0.8 | 44, 37 | 162 | 0.175 | 0.119 | 0.107 |
| `h268` | 9 | (5, 6), J = +0.7 | 4, 16 | 230 | 0.162 | 0.113 | 0.100 |

All three items are certified on the noisy simulator. The real device's drift, crosstalk and non-Markovian noise are not in the noise model, so the hardware negativity will probably come out lower than this. That gap is part of what the measurement tests.

## QPU budget

- **Estimate:** each circuit takes about 9–16 µs to execute, and each shot waits out a 250 µs repetition delay. 39 circuits × 4,000 shots comes to about 40 s of shot time. Adding about 5 s of per-job overhead gives **≈ 45 QPU seconds**, inside the remaining allowance (600 s per month, project hard stop at 420 s, 0 s used so far).
- **Cheaper option:** 2,000 shots per circuit costs about 25 s. That widens the intervals by about √2, and the noisy-simulator lower bounds would still clear 0.
- **Not submitted:** this waits for Sean's approval. The Stage 1 job also has to return first, to confirm that the hardware path works.

## Note for future runs: prune to the measured qubits' light cone

The as-run witness circuits (`window/data/hardware/dbl6e1d8mdtc73d5gesg-*.json`) prepare the whole belief state but measure only the target pair. They therefore carry gates on unmeasured qubits that have no path to a measured qubit, including gates placed after the target pair's last interaction. Those gates cannot change the measured statistics, but they still cost execution time and add crosstalk.

Before submitting a future run, prune every gate outside the **backward light cone** of the measured qubits. Walk the circuit from the measurements backwards, keep a gate only if it touches a qubit already in the cone, and add that gate's qubits to the cone. This shortens each shot, which cuts QPU seconds per shot. It also removes avoidable noise sources.

The pruned circuit must give the same two-qubit reduced state as the full circuit, which can be checked by exact simulation before submission. Run 1 was submitted unpruned, exactly as designed.

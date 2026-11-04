# Entanglement witness, run 1 (real hardware)

Design: `experiments/witness.md`. Job `dbl6e1d8mdtc73d5gesg` on `ibm_fez` (Batch `c7a152dc-d677-42ae-90a8-fef9ad5e3a28`), 39 circuits × 4000 shots. **QPU time: 44 s** (IBM `qpu_charge_time_seconds`). Service-reported consumption after the job: 2 s of 600 s.

Witness: negativity N of the two-qubit reduced state of the most-entangled related pair (N > 0 ⇔ entangled; separable states give 0; a Bell pair gives 0.5). Readout-error mitigated; 95% intervals from 500 parametric bootstrap resamples. Certified if the lower bound > 0.

| item | pair (physical qubits) | N ideal | N noisy sim [95% CI] | **N hardware [95% CI]** | hardware, unmitigated | certified |
|---|---|---|---|---|---|---|
| `h221` | (0, 6) on 10, 9 | 0.184 | 0.171 [0.157, 0.181] | **0.147 [0.134, 0.157]** | 0.140 | yes |
| `h088` | (5, 6) on 44, 37 | 0.175 | 0.149 [0.138, 0.162] | **0.063 [0.051, 0.075]** | 0.052 | yes |
| `h268` | (5, 6) on 4, 16 | 0.162 | 0.118 [0.105, 0.132] | **0.067 [0.055, 0.081]** | 0.058 | yes |

**3 of 3 items certified; pre-registered success rule (≥ 2 of 3): met.**

## Reading

- The QPU time was first logged as 0.0 s by the D10 parsing bug, since repaired.
- **Certified.** Real `ibm_fez` hardware held entangled states of the encoded contention pairs, with negativity well clear of zero for all three items. The result holds without readout-error mitigation too (unmitigated N = 0.140, 0.052, 0.058), so it is not an artefact of the mitigation step.
- **Hardware is noisier than the noise model.** For two items the hardware negativity is about half the noisy-simulator prediction (0.063 vs 0.149, and 0.067 vs 0.118). This is in the same direction as Stage 1, where hardware departed from the `AerSimulator.from_backend` prediction far beyond shot noise.
- **What it certifies.** It certifies that the encoding's entanglement is physically present in a few belief states. It says nothing about whether that entanglement helps judgment, and Stage 2 shows it does not.
- **One item is a two-qubit test.** In `h221`'s ideal state, the target pair's reduced state is pure (purity 1.000), so that pair is decoupled from the other contentions. Its result is effectively a two-qubit entangling test. The pairs in `h088` and `h268` are mixed (purity 0.746 and 0.819), so they are genuinely entangled with the rest of the belief state.

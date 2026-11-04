# Audit: stage1-run-1

**Files audited:** `results/stage1-run-1.{md,json}` (raw counts for ideal, noisy and hardware), `results/pool-run-1.json` (item q01's claims), `experiments/stage1_pipe.py`, `results/ibm-calibration.{md,json}`, `results/ibm-usage.{md,json}`, `results/ibm-job-status-log.md`, DEVIATIONS D10. Citations: README.md:91–96; paper/the-entangled-mind-v3.md:57, 322–335, 441; results/witness-run-1.md:19; paper/the-entangled-mind-paper.md:140; paper/gold-map.md:326.
**Pre-registration:** none for Stage 1. It is a pipe test, and `experiments/preregistration.md` names it only as "the only other hardware job". Job `dbl423dgg49c73dk0db0` was queued from about 13:16 MST (status log: 56 min waiting at 14:12:15), ran 16:06:31 (IBM `job_running`) and was recorded 16:06:47. Result commit `98d6ac6` 16:07:46, which also adds D10.
Timing verdict: OK (no hypothesis was tested).

## Plain-English summary of the audit
The Stage 1 numbers are right. From the archived counts and q01's claim leans I get P(yes) = 0.294 / 0.251 / 0.502 and conflict scores 0.276 / 0.276 / 0.666, exactly as reported. The gap between hardware and the noise model is far beyond shot noise (z = 12 on 1,000 shots), so for this one circuit on this one run the device really did differ from its simulator. Two things in the wording go further than the data. First, it is one circuit, one job and one calibration snapshot, and the noisy simulator was probably built from the calibration in force at queue time (about 13:16), not at execution (snapshot 15:31). Second, "decoheres" and "washed out" describe the result as relaxation toward randomness. Several qubits moved *past* 50/50: qubit 1's yes-rate went from 0.25 ideal to 0.70 on hardware. That points to coherent or systematic error at least as much as decoherence. Overall P(yes) of 0.50 equals the value for uniformly random bitstrings, but the per-qubit pattern is not uniform.

## Claims checked
| # | claim (quoted or paraphrased, with file:line) | recomputed / evidence | status |
|---|---|---|---|
| 1 | 9 qubits, 33 RZZ, depth 208, 117 CZ (stage1-run-1.md:5) | JSON: n_qubits 9, n_edges 33, depth 208, cz 117 | holds |
| 2 | 1,000 shots, 336 distinct bitstrings on hardware (235 ideal, 284 noisy) | identical | holds |
| 3 | P(yes) 0.294 / 0.251 / 0.502; conflict 0.276 / 0.276 / 0.666 (table) | Recomputed from counts with w = |lean|/Σ|lean| (leans −1 ×8, +1 ×1): identical | holds |
| 4 | "Hardware decoheres the state much more than the `ibm_fez` noise model predicts" (stage1-run-1.md:29) | Hardware − noisy P(yes) = +0.251, SE 0.021, z = 12.0, so the difference is real for this circuit. Per-qubit P(bit = yes): ideal [0.38 0.25 0.22 0.10 0.36 0.36 0.31 0.52 0.36], hardware [0.50 0.70 0.50 0.28 0.58 0.52 0.38 0.51 0.54]. Qubits 1 and 4 overshoot 0.5, which is not relaxation. One circuit, one job | overclaim (mechanism and generality) |
| 5 | "Real hardware washed the state out much more than the noise model predicts" (README.md:94; v3:335 "far more") | Same evidence. Scoped to this one circuit it holds as a description of P(yes) (0.50 = the uniform-random value) | holds (minor) |
| 6 | "The device washed the states out more than its noise model predicts." (v3:57; paper.md:140; gold-map:326) | Plural generalisation from one Stage-1 circuit plus 3 witness items. The witness items do all fall below their noisy-sim negativity (see `audits/witness-run-1.md`), so the direction is consistent across 4 circuits on one day | holds (minor) |
| 7 | Queue 13:16 to 16:06 MST, 2 h 50 min (stage1-run-1.md:28) | Status log: 56 min waiting at 14:12:15, so created ≈ 13:16; IBM `job_running` 16:06:31 | holds |
| 8 | QPU time 2 s; first logged 0.0 s (D10) | `job_metrics_usage.qpu_charge_time_seconds` = 2; `quantum_seconds` in the ledger = 2.0 after repair | holds |
| 9 | Ledger cumulative 46 s (ibm-usage.md; README:96) | 2 + 44 | holds |
| 10 | Calibration at job time: snapshot 15:31:18, job ran 16:06 (ibm-calibration.md) | `calibration_time` 15:31:18-07:00, `job_running` 23:06:31Z = 16:06:31 MST | holds |
| 11 | "117 CZ … product of CZ fidelities of 0.786 … Stage 1's washout to P(yes) 0.50 is far larger than this suggests" (v3:441) | 0.99794^117 = 0.786. Global depolarising at that fidelity would move P(yes) only from 0.294 to about 0.34 | holds |
| 12 | Noise model provenance | `stage1_pipe.py` builds the noisy simulator at run time with `AerSimulator.from_backend`, i.e. at submission (~13:16), from that day's earlier calibration. The hardware ran against the 15:31 calibration, and neither the file nor the README mentions this | not in file (minor hole) |

## Holes found
1. **One circuit is generalised to "hardware".** The Stage 1 file and README state a property of the device ("hardware decoheres … much more than the noise model predicts") from a single 9-qubit circuit and a single job. The witness corroborates the direction on 3 more circuits, so the cross-document claim is reasonable as a same-day observation, but not as a general characterisation.
2. **The mechanism is assumed.** "Decoheres" and "washed out" imply relaxation toward 50/50. Qubit 1's marginal goes from 0.25 to 0.70 and qubit 4's from 0.36 to 0.58. That is the signature of coherent or systematic error (or crosstalk), not only decoherence. The data show the hardware *differs from* the noise model; they do not show *how*.
3. **The calibration epochs differ.** The noise model and the execution most likely used different calibration snapshots (≈ 13:16 vs 15:31). Part of the gap may be drift that the noise model never had a chance to include. It still counts as "noise model underestimates the device", but it is a weaker statement than a like-for-like comparison.

## Overclaims to cut (exact sentences)
- `results/stage1-run-1.md:29` — "- Hardware decoheres the state much more than the `ibm_fez` noise model predicts: P(yes) 0.50 on hardware vs 0.25 on the noisy simulator and 0.29 ideal, with 336 distinct bitstrings out of 1,000 shots." — mechanism and generality — replace with "- On this one circuit, hardware departs from the `ibm_fez` noise model far beyond shot noise: P(yes) 0.50 on hardware vs 0.25 on the noisy simulator and 0.29 ideal (z = 12), with 336 distinct bitstrings out of 1,000 shots. Some qubits overshoot 50/50 (qubit 1: 0.25 ideal, 0.70 hardware), so this is not decoherence alone."

## Does the verdict stand?
No hypothesis was tested. The pipe-test result (the hardware path works; the counts are as reported) **STANDS**. The interpretive sentence about decoherence is an overclaim.

## Confidence
High for the numbers, which were recomputed from raw counts. Medium for the noise-model epoch, which is inferred from the code path and the queue log, since the simulator's calibration timestamp is not archived.

## Tally
claims_checked: 12
claims_failed: 1
overclaim_sentences: 1
verdict: STANDS
confidence: high

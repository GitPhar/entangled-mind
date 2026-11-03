# Pre-registration — Stage 2, run 1

Written 2026-11-03, while the pool run was in progress. Every arm was run on the calibration pool and the test set only after this file was committed. All constants live in `src/entangled_mind/config.py`.

## Data

- Pool: 60 yes/no questions with known answers (`experiments/questions.json`).
- The base model (`claude-sonnet-5-5`, adaptive thinking at effort `xhigh`) answers every question with a brief visible explanation of the considerations for and against. Contentions are the claims in that visible answer (see `DEVIATIONS.md`, D1–D3).
- Test set: 10 wrong items and 10 right items, drawn at random with seed 2026. If the model gets more than 10 wrong, the extras go to calibration.
- Calibration pool: the remaining 40 items. All thresholds are set here and nowhere else.

## Encoding (fixed)

- One qubit per contention, 5–16 qubits.
- RY(θ) with θ = confidence · π/2: |0⟩ is uncommitted, and the equator is fully committed.
- RZ(φ): φ is the minimum-energy solution of the XY energy E(φ) = −Σ J_ij cos(φ_i − φ_j) − Σ lean_k cos φ_k. Here J_ij = +strength for supports, −strength for contradicts, and phase 0 is the "yes" direction.
- RZZ(κ · J_ij) for every related pair, with κ = π/4.
- Evolution: N = 2 Trotter steps. Step k uses s = k/(N+1).
  - Problem term: exp(−i γ₀ s H_P) with H_P = −Σ J_ij X_iX_j − Σ lean_i X_i.
  - Mixer term: exp(−i β₀ (1−s) H_M) with H_M = −Σ Z_i.
  - γ₀ = 0.5, β₀ = 0.4.
- Measurement in the X basis, 1,000 shots. Bit 0 means yes-aligned.

## Readout (fixed)

- Each shot gives a weighted vote m = Σ w_k x_k, where x_k = +1 for yes-aligned and −1 for no-aligned, and w_k = |lean_k| / Σ|lean|.
- Judgment = yes if P(m > 0) ≥ 0.5.
- Confidence = max(P_yes, 1 − P_yes).
- Conflict score = 2 · min(P(m ≥ 1/3), P(m ≤ −1/3)): the mass on the weaker of two strongly opposed camps.

## Arms

| arm | what runs | conflict score |
|---|---|---|
| A | entangled circuit, N = 2, noisy Aer simulator built from `ibm_fez` (`AerSimulator.from_backend`) | as above |
| B | the identical transpiled circuit on real `ibm_fez`, all 20 test circuits as one SamplerV2 job inside a Batch | as above, using A's threshold |
| C | same circuit with every two-qubit term removed (prep RZZ and evolution XX), noisy simulator | as above |
| D | same circuit built from a shuffled relation web: same number of relations and the same signed strengths, placed on random pairs (seed 7); phases re-solved; noisy simulator | as above |
| E | classical control, no qubits | total contradiction strength in the relation web |

Supplementary arm A0 (not one of the five): the entangled circuit on a noiseless simulator, to separate the encoding from hardware noise.

**Flag rule:** each arm flags an item when its conflict score exceeds that arm's threshold. The threshold is the 75th percentile of that arm's scores on the calibration pool, so every arm flags about the top quartile of calibration items. This equalises how much each arm flags overall, so any difference on the test set reflects where the flags land, not how many there are. Arm B uses arm A's threshold because it is not run on calibration.

## Hypotheses and the null result that falsifies each

- **H1 (faithful encoding):** arm A's judgment matches the base model's own final answer on at least 70% of the 20 test items. *Falsified if* agreement is at most 50%, meaning the circuit carries no more of the model's stance than a coin flip.
- **H2 (conflict detection, primary):** arm A flags at least 10% of known-wrong test items, while arms C, D and E each flag at no more than half of A's wrong-item rate. *Falsified if* A flags under 10% of wrong items, or any control reaches half of A's rate or more. If E matches A, the quantum state carries nothing beyond contradiction counting, and the README must say so.
- **H3 (entanglement carries information):** A's test-set AUROC (conflict score, wrong vs right) exceeds C's by at least 0.10. *Falsified if* C's AUROC is at least A's.
- **H4 (structure carries information):** A's AUROC exceeds D's by at least 0.10. *Falsified if* D's AUROC is at least A's, meaning a random web with the same strengths does as well.
- **H5 (hardware survives):** if B runs, the Spearman correlation between A's and B's conflict scores across the 20 items is at least 0.5, and B flags at least 10% of wrong items. *Falsified if* the correlation is 0 or below, or B flags no wrong item. *Untested* if the hardware gate is not met.

With 10 wrong and 10 right items, one item is worth 10 percentage points. A pass or fail that depends on a single item will be reported as **too noisy to call**, not as confirmation.

## Hardware gate (resource rule)

Arm B is submitted only if, on the simulator, arm A's wrong-item flag rate is at least 10% and strictly greater than each of C's, D's and E's wrong-item flag rates. It is also submitted only if cumulative QPU usage is under 420 s. Arm B is one job of 20 circuits. Stage 1 is the only other hardware job.

## Addendum A — added before Stage 2 run 3 data were collected (2026-11-03)

These additions were written after Stage 2 run 2 was committed and before any arm-F, arm-G or shuffle-null number existed. They are first applied as a re-scoring of run 2 (`results/stage2-run-2b.md`) and carry forward to every later run. Code: `src/entangled_mind/classical_twin.py` and `experiments/stage2_rescore.py`.

### Arm F: classical Ising twin

Arm F isolates what superposition and interference add. It uses the same relation graph as arm A, with the same couplings, signs and lean fields as arm A's problem Hamiltonian, treated as a classical spin model:

E(x) = −Σ J_ij x_i x_j − Σ lean_i x_i, with x_i = +1 for yes and −1 for no.

- **Solving:** exact enumeration of all 2^n configurations (n ≤ 16).
- **Judgment:** the sign of the ground state's weighted vote m, with the same |lean| weights as the quantum readout.
- **Conflict score:** take the near-minimum configurations, E ≤ E_min + 0.10 · (E_max − E_min). The score is 2 · min(#{m ≥ 1/3}, #{m ≤ −1/3}) / #near: how much of the low-energy landscape sits in strongly opposed camps. This mirrors arm A's conflict score with no superposition and no interference.
- **Threshold:** the same calibration-quantile rule as every other arm.

### Arm G: self-reported confidence

Arm G is the standard error-prediction baseline.

- **Call:** one extra call per question to the base model. The prompt shows the question and the model's own *visible* answer, and asks for its confidence from 0 to 100 that the final answer is correct, as a single integer in structured output. No thinking content is sent.
- **Conflict score:** 100 − confidence.
- **Threshold:** the same calibration-quantile rule.

### Statistics for every arm

- **Bootstrap intervals:** test-set AUROC (wrong vs right) with a 95% bootstrap interval, from 1,000 resamples stratified by wrong and right, seed 99.
- **Arm D null distribution:** 200 independent shuffles of each test item's relation web. Each shuffle keeps the number of relations and the signed strengths and places them on random pairs. Shuffle k of item q uses seed 31337 + 1000k + q. Every shuffle runs on the noisy simulator exactly as arm D does, and each gives one test-set AUROC. The report gives arm A's position in this null as p = (1 + #{null AUROC ≥ A's AUROC}) / 201. The single-shuffle arm D stays in the table for continuity.
- **H2 is unchanged** and still compares A against C, D and E. A second line also reports the criterion with F and G held to the same bar (each at most half of A's wrong-item flag rate). That second line is reported, not a replacement for H2.

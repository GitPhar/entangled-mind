# Pre-registration — version two: learned encodings

Written 2026-11-03, after the v2 split was locked (`experiments/split-v2.json`) and **before any parameter was fitted**. Code: `src/entangled_mind/v2.py` and `experiments/v2_fit.py`.

## Data and discipline

- **Pool:** pool run 5 (`results/pool-run-5.json`): the training pool of `experiments/questions-train.json` with base model `claude-haiku-5-5` and the unchanged pipeline (DEVIATIONS.md, D9 and D9b).
- **Locked split:** train 60%, validation 20%, test 20%, seed 2026, stratified by wrong/right × item type (simpleqa, science, puzzle, claim). It is committed before fitting and never re-made.
- **Held-out set:** the run-2 80-item test set (40 wrong, 40 right, hard pool, pool run 3) is a second held-out set. It shares no question stem with the training pool.
- **Discipline:**
  - Fitting reads only train.
  - Model selection reads only validation.
  - The locked test set is scored **once**, at the end, and the run-2 held-out set is also scored **once**.
  - Nothing is refitted after either.

## Models: 9 parameters each, the same fitting rule

**A2, the learned quantum encoding.** This is arm A's circuit, simulated exactly as a statevector (`v2.fast_quantum_probs`, verified equal to the Qiskit circuit at v1 values). Its parameters:

| # | parameter | range | v1 value |
|---|---|---|---|
| 1 | s_θ, confidence-to-angle scale: θ = s_θ · confidence · π/2 | 0.2 – 2.0 | 1 |
| 2 | k_sup, coupling scale for *supports* | −1.5 – 1.5 | 1 |
| 3 | k_con, coupling scale for *contradicts* | −1.5 – 1.5 | 1 |
| 4 | N, Trotter steps | 0 – 4 (integer) | 2 |
| 5 | γ₀, problem-step scale | 0 – 1.5 | 0.5 |
| 6 | β₀, mixer-step scale | 0 – 1.5 | 0.4 |
| 7 | α, readout-basis angle (rotation about Y away from the X basis) | −π/2 – π/2 | 0 |
| 8 | τ, strong-camp threshold of the conflict score | 0.05 – 0.6 | 1/3 |
| 9 | flag threshold on the conflict score | Youden-optimal on train | — |

**F2, the learned classical twin.** It uses the same graph, phase solution, single-contention priors (P(yes) = (1 + sin θ cos φ)/2) and couplings. The difference is that the state is a classical distribution, evolved exactly by N sequential heat-bath (Glauber) sweeps, with no amplitudes and no interference. Its parameters:

| # | parameter | range |
|---|---|---|
| 1 | s_θ | 0.2 – 2.0 |
| 2 | k_sup | −1.5 – 1.5 |
| 3 | k_con | −1.5 – 1.5 |
| 4 | N, sweeps | 0 – 4 (integer) |
| 5 | inverse temperature β_T (scaled by s_t = t/(N+1)) | 0 – 3 |
| 6 | independent-flip rate (scaled by (1 − s_t)/2), the mixer analogue | 0 – 1 |
| 7 | lean-field scale | 0 – 2 |
| 8 | τ | 0.05 – 0.6 |
| 9 | flag threshold | Youden-optimal on train |

**L, the relation-web feature baseline.** A linear score on standardised features, in logistic-regression form, with 8 weights in −3 to 3 plus a flag threshold (Youden on train), for 9 parameters. A bias term is omitted because AUROC is invariant to it. The 8 features:
1. contradiction count
2. total contradiction strength
3. total support strength
4. number of claims
5. mean confidence
6. number of related pairs
7. mean |lean|
8. the share of confidence leaning against the claims' own vote

Features 1–5 are the five named in the brief. Features 6–8 are three more relation-web summaries, added so L matches the 9-parameter count.

**G, the self-reported confidence baseline.** Score = 100 − the base model's stated confidence, from the same single call as arm G (one call per item). It has no fitted parameters and is reported as the baseline.

## The fitting rule (identical for A2, F2 and L)

1. Draw **400** parameter vectors uniformly from the ranges (integers rounded).
2. Score every vector by **train AUROC** (conflict score, wrong vs right).
3. Hill-climb the **10** best. Each gets **60** Gaussian perturbations (sd = 10% of each range; integers move by rounding), and a perturbation is accepted if train AUROC does not fall.
4. The final parameters are the climbed candidate with the **highest validation AUROC**, with ties broken by train AUROC.
5. The flag threshold (parameter 9) maximises Youden's J on train.

That is 1,000 train evaluations per model, with seeds fixed in `experiments/v2_fit.py`.

## Evaluation

- **Locked test set:** AUROC with 95% bootstrap intervals (1,000 resamples, stratified wrong/right) for A2, F2, L and G, plus flag rates at each model's train threshold.
- **Run-2 held-out set:** the same, scored once.
- **Split-by-type table:** the same statistics by item type, and by whether the relation web had at least 3 contradictions.

## Pass criterion (primary, A2 vs F2)

On the locked test set, A2 passes if its AUROC exceeds F2's by more than the width of both bootstrap 95% intervals. This is read as the two intervals **not overlapping**: lower 95% bound of A2 > upper 95% bound of F2.

Otherwise, the learned quantum encoding **ties or loses** to its classical twin, and the README says so plainly. The paired bootstrap interval of AUROC(A2) − AUROC(F2) is reported as well.

Secondary comparisons, reported but not part of the pass criterion: A2 against L, A2 against G, and every model on the run-2 held-out set.

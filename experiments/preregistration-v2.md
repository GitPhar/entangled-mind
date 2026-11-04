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

## Addendum B — hedge baseline (H) and version 2.1 "honest hedge" encoding

**Written 2026-11-03 17:45 MST.** At this point the v2 fit was still on train and validation, and **no test-set evaluation of any v2 model had been run**. The locked test set and the run-2 held-out set had not been scored.

**Definition.** A **no-lean claim** (a *hedge*) is one whose extracted lean satisfies |lean| ≤ 0.1. Leans are extracted in steps of 0.05. On the train split, 10.3% of claims have a lean of exactly 0 and 11.2% have |lean| ≤ 0.1, and 55% of train items have at least one hedge.

### H — hedge-count baseline (no fitted parameters)

- **H (primary score):** the total confidence of the item's no-lean claims.
- **H-count (reported alongside):** the number of no-lean claims.

H is evaluated on the locked v2 test set and on the run-2 held-out set alongside A2, F2, L and G, in the same single evaluation and with the same bootstrap intervals. Its flag threshold is Youden-optimal on train, like the other models.

### Version 2.1 — "honest hedge" encoding (applied identically to the quantum arm and its classical twin)

In v1 and v2, a no-lean claim's phase is solved by the relation web, so it gets pulled into a yes or a no camp. In v2.1:

1. **Neutral orientation.** Each no-lean claim's lean is set to 0, and its phase is fixed at φ = π/2, equidistant from yes (0) and no (π). In the quantum arm this gives P(yes) = 1/2 at readout. In the classical twin it gives a prior P(yes) = (1 + sin θ cos φ)/2 = 1/2.
2. **Phase solving on the rest.** The XY-energy phase solver runs only on the claims that lean, using the relation edges among them. A hedge takes no part in the phase solution.
3. **Couplings unchanged.** A hedge keeps its relation edges in the circuit (prep RZZ and evolution) and in the classical twin's energy, exactly as before. Only its orientation and field change.
4. **Separate uncertainty term.** U = Σ(confidence of no-lean claims) / Σ(confidence of all claims), in [0, 1]. The conflict score becomes conflict(τ) + λ_h · U, with a learned λ_h in [0, 2].

**Models.**
- **A2.1** is A2's 8 scored parameters, plus λ_h, plus a flag threshold.
- **F2.1** is F2's 8 scored parameters, plus λ_h, plus a flag threshold.

Both have 10 parameters, so they are matched to each other.

**Fitting.** The same rule as v2: 400 random draws, then hill-climbing of the 10 best with 60 steps each, selection on validation AUROC, and a Youden threshold on train. Seeds are A2.1 111 and F2.1 212. Fitting reads train and validation only.

**Evaluation.** The locked v2 test set is scored **once**, after the v2 arms have been evaluated, and the run-2 held-out set is also scored once. AUROC is reported with 95% bootstrap intervals (1,000 resamples), along with the paired A2.1 − F2.1 difference and the split-by-type table.

**Pass criterion (stated as for v2).** On the locked test set, A2.1 passes if its AUROC exceeds F2.1's by more than the width of both bootstrap 95% intervals, read as non-overlapping intervals: A2.1's lower 95% bound > F2.1's upper 95% bound. Otherwise the honest-hedge quantum encoding ties or loses to its classical twin, and the README says so plainly.

**Reported, not a pass criterion:** A2.1 against A2 and F2.1 against F2 (does the honest hedge help each family?), and A2.1 and F2.1 against H, L and G.

## Addendum C — v2.1 evaluated noiseless and on the noisy simulator

**Written 2026-11-03 18:36 MST.** No v2.1 fit had started (`results/v2.1-fit.json` did not exist), and no v2 or v2.1 model had been scored on any test set.

1. **Fitting is on exact noiseless statevectors** for A2.1 and F2.1. What is learned is the mapping from claims to state, and noise adds nothing to it. Selection is on validation, exactly as in Addendum B. The fitting code already worked this way; this addendum makes it explicit.
2. **Two evaluations, once each, on the locked v2 test set:**
   - **(i) noiseless:** exact statevector probabilities for A2.1, and the exact classical distribution for F2.1;
   - **(ii) noisy simulator:** the selected A2.1 built as a Qiskit circuit, transpiled for `ibm_fez`, and run on `AerSimulator.from_backend(ibm_fez)` with 1,000 shots per item (seeded per item). The conflict score is computed from those counts, as in Stage 2.

   **F2.1 is a classical distribution with no circuit,** so "noisy simulator" is not defined for it. Its noiseless score is its only score.
3. **Reported for both evaluations:** AUROC with 95% bootstrap intervals, flag rates at the train threshold, and A2.1 (noisy) − A2.1 (noiseless) as a paired bootstrap difference.
4. **Pass criterion unchanged.** It is applied to the **noiseless** evaluation, A2.1 against F2.1, because that is the like-for-like comparison. The noisy-simulator result is reported against the same F2.1 interval as a secondary line.
5. **The run-2 held-out set** is scored once, noiseless only, as in Addendum B.

Everything else in Addendum B is unchanged.

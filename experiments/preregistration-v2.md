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

## Addendum D — what is the Sonnet edge? A coupling ablation and a classical twin with the same readout geometry

**Written 2026-11-03 21:03 MST, before any score below was computed.** Only D27's offline Sonnet scores (A2, F2, L, H) existed at this point.

**Question.** On Sonnet's hard-pool errors, A2 beat F2 by +0.078 [+0.018, +0.137] (D27), with A2's fitted couplings near zero. Is the edge (i) the couplings, or (ii) single-claim geometry: the tilted readout α acting on each claim's confidence angle θ and phase φ? And if (ii), can a classical model carry it?

**Models (no new API calls).**
- **A2(κ=0):** the frozen v2 A2 parameters with every coupling set to exactly 0 (k_sup = k_con = 0), and nothing refitted. With no couplings the phase solve has only the lean anchors, the prep and evolution have no two-qubit terms, and the state is a product of tilted single-claim qubits. This gives 9 parameters (A2's), with the two couplings pinned at 0, so 7 are effectively free.
- **F2+:** F2 with the same per-claim readout-angle feature. Its prior single-claim marginal becomes P(yes) = (1 + sin θ cos φ cos α + cos θ sin α)/2. This is exactly what an uncoupled qubit with Bloch vector (sin θ cos φ, sin θ sin φ, cos θ) gives when measured along an axis tilted by α. Everything else is as in F2. That is 9 scored parameters (F2's 8 plus α, in [−π/2, π/2]) plus a flag threshold, so **10** in all, against A2's **9**.
- **Fitting.** F2+ is fitted on the v2 train split only, by the v2 rule (400 random draws, then hill-climbing of the 10 best with 60 steps each, selection on validation AUROC; seed 707).
- **Scoring.** A2(κ=0) and F2+ are each scored once on Haiku's locked v2 test set (209 items) and once on Sonnet's 298 hard-pool records. A2 and F2 are re-scored with their frozen parameters for the paired differences. The locked test set has been scored before (v2, v2.1); these are additional single scorings of new models, with no fitting on it.

**Rule (fixed now).** "Matches" means the paired-bootstrap 95% interval of the AUROC difference (2,000 stratified resamples) contains 0 **on both sets**. "Falls short" means the interval of F2+ − A2 lies entirely below 0 on at least one set.
1. **A2(κ=0) matches A2, and F2+ matches A2:** the edge is single-claim geometry, and a classical model can carry it. The paper says so.
2. **A2(κ=0) matches A2, but F2+ falls short:** the single-claim geometry is the finding, and the next test is designed around it.
3. **A2(κ=0) does not match A2** (A2(κ=0) − A2 entirely below 0 on at least one set): the small couplings matter, and that is reported as such.
4. **Any other combination** is reported as is, with no verdict beyond the intervals.

## Addendum E — the frozen F2+ on Haiku's run-2 held-out set

**Written 2026-11-03 21:49 MST, before F2+ was scored on this set.** Addendum D left open whether Haiku's run-2 held-out edges reduce to the per-claim readout geometry. Those edges are A2 − F2 = +0.108 [+0.012, +0.215] in v2 and A2.1 − F2.1 = +0.116 [+0.013, +0.225] in v2.1. F2+ (Addendum D) had not been scored on that set.

**Scoring.** The **frozen** F2+ (parameters in `results/sonnet-ablation-fit.json`, fitted on the v2 train split only, never refitted) is scored once on the run-2 held-out set: 40 wrong and 40 right, from pool run 3. A2, F2, A2.1 and F2.1 are re-scored with their frozen parameters for the paired differences. No API calls are made.

**Rule, as in Addendum D.** "Matches" means the paired-bootstrap 95% interval of the AUROC difference (2,000 stratified resamples) contains 0. "Falls short" means it lies entirely below 0.
1. **F2+ − A2 matches, and F2+ − A2.1 matches:** the held-out edges are also single-claim readout geometry, carried by a classical model.
2. **F2+ − A2 or F2+ − A2.1 falls short:** that held-out edge is not explained by the readout geometry, and it is reported as an open, unexplained secondary difference.
3. **Anything else** is reported as is.

F2+ − F2 is reported alongside. This is one scoring of one frozen model, and it is still a secondary comparison: v2's primary test remains the locked-test tie.

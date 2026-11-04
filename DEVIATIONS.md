# Pre-registration deviations

## D1 — Contentions come from the visible written reasoning, not the hidden thinking trace

**Date:** 2026-11-03 (before any pool, calibration, or test-set result existed)

**Original spec:** ask the base model with extended thinking on, capture the thinking trace, and split the hidden thinking trace into 5–16 discrete contentions.

**New design:** the base model is asked to reason step by step *in its visible response* before giving `FINAL ANSWER: YES/NO`. Only that visible written response goes to the contention extractor. Thinking stays on (adaptive, effort `xhigh`) so the model still deliberates. Its content is requested with `display: "omitted"`, so it is never returned, stored, or passed to any other call. Only the thinking token count is logged.

**Reason:** in the first pool attempt, the API's `reasoning_extraction` safeguard refused the extractor call (`claude-sonnet-5-5`, `stop_reason: refusal`), which was being handed the base model's thinking trace. We redesigned the pipeline rather than route around the safeguard. If any call in the pipeline is refused again, the run stops, records the refused call and its exact stop details in `results/refusal.md`, and does not reword or retry.

**Effect on interpretation:** the circuits encode the argument the model *wrote down*, which may be a tidied, post-hoc account of its deliberation rather than the deliberation itself. Every result in this repository should be read as being about the written reasoning.

### Findings that led here (pilot calls, 2026-11-03)

1. **Sonnet 5.5 emits no thinking block at all at `low`, `medium`, or `high` effort** on these items (tested on a bat-and-ball item and a letter-counting item). Adaptive thinking judged them not worth thinking about, so there was no trace to split. A thinking block appeared only at `xhigh` and `max`.
2. **Even at `xhigh`, the thinking block is only a short summary**, one or two sentences (67–98 thinking tokens on the pilot items), and the raw chain of thought is never exposed. It could not have supplied 5–16 contentions on its own.

## D2 — The redesigned extractor was refused too (run stopped)

**Date:** 2026-11-03

With D1 in place (base thinking requested with `display: "omitted"`, extractor given only the question and the visible written response), the first extractor call (q01) was refused again with `stop_reason: refusal`, category `reasoning_extraction`. Per the hard rule, the run stopped at once. Nothing was reworded or retried, and 0 of 60 questions completed. The refused call and its exact stop details are in `results/refusal.md`.

The prompt still had the shape the safeguard documents as a trigger: the input sat inside a tagged `<response>` section, and the system prompt asked for the writer's "deliberation" / "written reasoning" to be decomposed.

## D3 — Prompt redesigned per Anthropic's documented guidance for reasoning_extraction

**Date:** 2026-11-03 (before any pool, calibration, or test-set result existed)

Anthropic's [refusals documentation](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback#keep-reasoning-in-thinking-blocks) says `reasoning_extraction` fires on prompt *shape*:
- a `<thinking>`, `<reasoning>` or scratchpad section
- a `reasoning`, `thinking` or `trace` field in JSON output
- the model's private notes, or a running log of its reasoning
- reasoning asked for verbatim or in full

It also says that asking for a short explanation or the evidence behind a result is fine, and that the category has no fallback model. The fix is to change the prompt.

Both earlier designs had that shape. D1's base prompt asked the model to "reason step by step in writing". Both extractor prompts wrapped the input in a tagged section and asked for the writer's reasoning or deliberation to be split out.

**Redesign:**
- **Base call** (`claude-sonnet-5-5`): adaptive thinking at `xhigh`, `display: "summarized"`. The prompt asks for the answer plus a brief explanation of the main considerations for and against, and keeps the `FINAL ANSWER: YES/NO` line. There is no step-by-step instruction and no tagged section. The summarized thinking blocks and the visible answer are saved together as each question's **deliberation record** in `results/pool-run-1.json`. The thinking blocks are archived only and are never sent to any other call.
- **Extractor** (`claude-sonnet-5-5`): the visible answer is presented as a document: "Below is a short written argument answering a yes/no question." It lists the document's distinct claims as `claims[{text, confidence, lean}]`.
- **Relation judge** (`claude-haiku-5-5`): the input is a numbered list of claims, and the output is the pair table `pairs[{i, j, relation, strength}]`.
- Every string sent to the API (prompts, schemas, user templates) was checked for thinking / reasoning / trace / scratchpad / deliberation / step-by-step / tag markup and reworded where any appeared.

**Science impact:** unchanged from D1. The circuits encode the claims in the model's *visible* explanation, which is a short account of its considerations, not its internal deliberation.

If a call is refused after this redesign, the run stops and records the request ID and exact refusal in `results/refusal.md`. The next step is a support ticket. Nothing will be iterated further.

## D4 — Pool extended with 75 code-verified computational items

**Date:** 2026-11-03 (after the pool run, before any circuit was run on any pool item)

**What happened:** on the original 60-item pool, `claude-sonnet-5-5` at effort `xhigh` answered **all 60 correctly**. With no known-wrong items, the 10-wrong / 10-right test set cannot be formed and H2 cannot be tested.

**Change:** the pool was extended once with 75 yes/no items generated by `experiments/make_extension.py` (seed 404, `experiments/questions_extension.json`). The items are:
- primality of 8-digit numbers (primes vs. products of two 4-digit primes)
- Gregorian weekdays of dates from 1600 to 2400
- letter counts in sentences
- digit sums of powers of 2
- 5-digit × 5-digit products with near-miss claims
- prime counts in 100-wide intervals

Every answer is computed by the script, not hand-labelled, so a "wrong" model answer cannot be a labelling error on our side.

**Rule fixed in advance:** the base effort stays at `xhigh`, and the extension is used once. If the 135-item pool still yields fewer than 10 wrong items, the run stops and that is reported. Otherwise the split follows the pre-registration: 10 wrong and 10 right items at random (seed 2026), with everything else, including surplus wrong items, going to calibration. The calibration pool is therefore about 115 items, not 40.

**Effect on interpretation:** the wrong items will be mostly computation slips, not misconceptions or conjunction-fallacy errors. The experiment then asks whether the circuit flags the model's *calculation* errors. That is a narrower question than the original one about conflicting beliefs.

**D4 addendum (same day, before any extension item completed):** at `xhigh` effort, the first computational item made the base call think until it hit the 16,000-token cap, which costs about $0.16 per call. To stay inside the $10 budget:
- items are processed in shuffled order;
- a base call that hits the cap is recorded as *no answer* and excluded from the split, never counted as wrong;
- the extension stops as soon as the pool holds 13 wrong items, or when session API spend reaches $8.50.

This stopping rule shapes only which items exist. It is applied before any circuit is run, so it cannot select for any hypothesis.

## D5 — Base model changed to claude-haiku-5-5 to obtain errors

**Date:** 2026-11-03 (before any circuit was run on any pool item)

**Original spec:** base model `claude-sonnet-5-5`, with adaptive thinking run at effort `xhigh` (D1).

**What happened:** pool run 1 with `claude-sonnet-5-5` at `xhigh` answered **all 117 checkable items correctly**: the 60 original items plus 57 of the computational extension items. Another 10 extension items hit the 16,000-token cap and were excluded. The run was stopped before its last 8 extension items once this decision was made. With no known-wrong items, H2 cannot be tested. Run 1 is archived as `results/pool-run-1.{json,md}`.

**Change:** the base model is now `claude-haiku-5-5`, a weaker Claude model chosen to obtain errors. It runs at its **default** effort, with adaptive thinking and `display: "summarized"`. The extractor (`claude-sonnet-5-5`) and the relation judge (`claude-haiku-5-5`) are unchanged.

Pool run 2 covers every original and extension item except the 10 that hit the token cap in run 1. The test set is 10 wrong and 10 right items at random (seed 2026), and the rest form the calibration pool.

**Fallback, fixed in advance:** if Haiku gets fewer than 10 wrong, the test set is every wrong item plus the 10 correct items whose extracted claims give the model's answer the least net support (Σ confidence·lean / Σ confidence, signed toward the answer given). Stage 2 runs anyway, and the results state plainly that H2 is underpowered at that count.

**Unchanged:** the H2 criterion, the five arms, the encoding, the readout and the threshold rule.

Nothing extracted under run 1 can be reused, because contentions depend on the base model's own answer. Run 1's spend stays in `results/api-usage.md`.

## D6 — Second, harder question pool (Stage 2 run 2)

**Date:** 2026-11-03 (after Stage 2 run 1 was fixed and running, before any hard-pool result existed)

**Why:** the standard pool of trick puzzles, misconceptions and computation yielded only 4 known-wrong items on `claude-haiku-5-5`, out of 125. At that count H2 is underpowered.

**New pool:** `experiments/questions-hard.json`, 300 yes/no items, 150 yes and 150 no, built by `experiments/make_hard_pool.py` (seed 1729). Every item records its source and license.
- **120 SimpleQA items** (OpenAI simple-evals, MIT). Each is the question plus a candidate answer: the gold answer for half the items, and for the other half the gold answer of a different SimpleQA question with the same topic and answer type.
- **120 MMLU-Pro physics and chemistry items** (TIGER-Lab, MIT). Each is the stem plus either the correct option or a random wrong one. Stems that depend on seeing the option list are dropped. GPQA Diamond was not used: it is gated, and its authors ask that items not be published in plain text, which this public repository would do.
- **60 author-written claims**: 30 true and 30 plausible fabrications, each a near-miss of a true fact.

**Pipeline:** unchanged, with the same base prompt, extractor, judge, encoding, readout, threshold rule, arms and H2 criterion.
- The hard pool runs first through `claude-haiku-5-5` (pool run 3).
- If Haiku gets fewer than 30 wrong, the pool also runs through `claude-sonnet-5-5` at default effort (pool run 4), and both result sets are kept.
- An answer with no parseable `FINAL ANSWER` line is excluded, not counted as wrong.

**Split:** all wrong items (at most 40, at random), plus an equal number of right items at random (seed 2026). Everything else is the calibration pool.

**Budget:** $15 for runs 3 and 4 together, enforced in code.

## D7 — Pre-registered additions: arms F and G, bootstrap intervals, a 200-shuffle null for arm D

**Date:** 2026-11-03, written after Stage 2 run 2 was committed and before Stage 2 run 3 data were collected.

Two arms were added: **F**, the classical Ising twin of arm A, and **G**, the base model's self-reported confidence. Two statistics were added for every arm: AUROC with 95% bootstrap intervals, and a 200-shuffle null distribution for arm D in place of the single shuffle. Full definitions are in `experiments/preregistration.md`, Addendum A.

They are first applied as a re-scoring of run 2 (`results/stage2-run-2b.md`). Arms A–E are not re-run. H2 is unchanged, and the F/G comparison is reported alongside it.

## D8 — Witness run: readout calibration pinned to the measured qubits

**Date:** 2026-11-03, before submission.

`experiments/witness.md` specifies readout-calibration circuits "on the same two physical qubits". `witness_design.py` passed those circuits through the optimizing transpiler, which is free to move them onto other qubits. `experiments/witness_run.py` instead builds them directly on the physical qubits that each item's settings measure. They use only native gates (`x`, `measure`) and are submitted untranspiled.

The noisy-simulator prediction is recomputed with this corrected calibration and reported next to the hardware result. Circuits, settings, shots and pass rule are otherwise exactly as designed: 39 circuits, 4,000 shots each, one Batch. Sean approved the budget of about 45 QPU seconds.

## D9 — v2 training pool

**Date:** 2026-11-03 (before any v2 fitting, and before the v2 split existed)

**Pool:** `experiments/questions-train.json`, 598 yes/no items (302 yes, 296 no), built by `experiments/make_train_pool.py` (seed 2718). Every item records its source and license. The pool leans toward errors that come from deliberation rather than ignorance:
- **150 SimpleQA items.** None are reused from the hard pool.
- **200 MMLU-Pro items**: 50 each from biology, engineering, physics and chemistry. The Hugging Face `/filter` endpoint was still failing, so biology and engineering rows were paged through the public `/rows` endpoint, using the dataset's category blocks.
- **150 two-sided computed puzzles**, with every claim placed 3–15% above or below the exact value (fractions):
  - base rates
  - sampling without replacement
  - birthday problems
  - expected values
  - three-dice totals
  - a conditional coin
  - combinations
  - average speed (the harmonic-mean trap)
  - compound growth
  - power comparisons
- **98 code-verified claims**: element numbers and symbols with near-miss false versions, plus computed numeric facts with small off-by-one or near-miss false versions.

**Leakage guard:** any item whose question stem also appears in the run-2 hard pool is dropped. Two element claims duplicated hard-pool claims and were removed. The run-2 hard pool, and in particular its 80-item test set, stays a separate held-out set.

**Run:** base model `claude-haiku-5-5` with the unchanged pipeline (pool run 5). The budget is $20, enforced in code. The target is at least 120 wrong items.

**Split:** the train / validation / test split (60/20/20, seed 2026, stratified by wrong/right × item type) is locked in `experiments/split-v2.json` and committed before any fitting.

## D10 — QPU-seconds parsing bug (fixed)

**Date:** 2026-11-03

IBM Runtime reports a job's billed QPU time as `metrics()["usage"]["qpu_charge_time_seconds"]`. `backends.run_hardware` read `quantum_seconds`, which doesn't exist in this runtime, so it logged the Stage 1 job as 0.0 s when it had used 2 s.

`backends.qpu_seconds` now reads the correct key. `backends.repair_ledger` recomputed every ledger entry from the stored raw metrics, so the 420 s hard stop sums correctly.

The witness job had already been submitted with the old code, so its ledger entry is repaired the same way when it returns.

**D9b addendum: one supplement to the training pool (same day, before the split was locked and before any fitting).**

Partway through pool run 5, Haiku's errors came almost entirely from SimpleQA (20% wrong) and MMLU-Pro engineering, physics and chemistry (12–20%). It got 0 of 82 computed puzzles wrong, 0 of 48 verified claims, and 4% of biology items. The full pool would yield about 55 wrong items, against the target of at least 120.

One supplement of 450 items was added as t599–t1048 (`make_train_pool.py --supplement`, seed 2719):
- 300 MMLU-Pro items: 100 each from engineering, physics and chemistry. Science is the larger share, following the brief's "deliberation over ignorance" weighting.
- 150 SimpleQA items.

The supplement excludes every existing training item and the held-out hard pool. The original 598 items are unchanged.

Also handled in this addendum: an item whose explanation yields fewer than 5 claims after one retry is now recorded as excluded, not counted as wrong, instead of crashing the run. This happened once.

**Finding:** the two-sided computed puzzles do not elicit errors from Haiku 5.5. Its errors on this pool are ignorance-type (SimpleQA) and multi-step science, not the base-rate or harmonic-mean traps.

## D11 — Experiment 4 (quantitative Yearsley & Trueblood) pre-registered

**Date:** 2026-11-03, before any experiment-4 call.

Pre-registered in `experiments/exp4-yearsley-trueblood.md`, with items in `experiments/exp4-items.json`. Choices made at pre-registration:

1. **Items.** Only 4 co-occurrence items exist in `items-borrowed.json`, too few for a share-based rule. They were joined by the 4 Linda variants that convert cleanly to X/Y form (Bill, Priya, the analytical person, name-swapped Marta) and by 8 new author-written items (co05–co12), for 16 in all.
2. **Letter-copying check.** Swapping the A/B labels on both questions together cannot detect a model that copies its first *letter*: under any shared mapping, a repeated letter is also a repeated content answer. The check therefore uses crossed mappings, where Q1 and Q2 use different label mappings, and compares how often the content answers agree under same versus crossed mappings.
3. **"Beyond repetition."** The classical comparator is Kang (2026)'s symmetric repetition model, fitted per item, which predicts o_rep = r · (p_X − p_Y). The quantum claim is tested on o − o_rep as well as on o.
4. **Thinking disabled for the base calls,** following the borrowed protocol's "thinking off". The base model is `claude-haiku-5-5`.

The budget is $10, enforced in code. The experiment runs last in the queue.

**D11 addendum: R2 wording corrected (same day, before any experiment-4 call).** Rule R2 (the order effect is at least the fallacy size) is a consequence of the quantum model, but it is not unique to it. An updating classical model, in which each judgment updates the state before the next, also satisfies R2. Only the *static* classical twin is ruled out.

The overstated sentences were corrected in `experiments/items-borrowed.json` (rule R2 and the pre-registerable test) and in `experiments/exp4-yearsley-trueblood.md`. In experiment 4, meeting R2 is now read as "consistent with quantum or sequential-update classical; rules out the static twin", not as support for the quantum account. The pass rules' thresholds are unchanged.

## D12 — Version two pre-registered (before any fitting)

**Date:** 2026-11-03. The split was locked in `experiments/split-v2.json` (train 629 with 95 wrong, validation 210 with 31 wrong, test 209 with 32 wrong; stratified, seed 2026) and committed before this pre-registration. Both came before any fitting. Choices made here:

1. **Pass criterion.** "Exceeds the classical twin's AUROC by more than the width of both bootstrap 95% intervals" is read as **non-overlapping intervals**: A2's lower 95% bound must be above F2's upper 95% bound. The paired bootstrap difference is reported as well.
2. **Equal parameter counts.** A2 and F2 each have 8 scored parameters plus a flag threshold. To match that, L uses the 5 features named in the brief plus 3 more relation-web summaries (number of related pairs, mean |lean|, and the share of confidence leaning against the vote), giving 8 weights plus a flag threshold. L's bias term is left out because AUROC does not depend on it.
3. **Fitting uses exact noiseless statevector scores** (`v2.fast_quantum_probs`, verified equal to the Qiskit circuit at v1 values to 10⁻¹⁶). This makes A2 the strongest version of the quantum model. A noisy-simulator fit at about 1,000 train evaluations was not computationally feasible. The classical twin F2 is also exact.
4. **Shared fitting rule:** 400 random draws, then hill-climbing of the 10 best with 60 steps each (1,000 train evaluations), with the final candidate selected on validation AUROC. Seeds are A2 101, F2 202, L 303.
5. **Arm G** (self-reported confidence) needs one Haiku call per locked-test item. It is made at evaluation time and cached in `results/v2-arm-g-confidence.json`. On the run-2 held-out set it reuses the existing arm-G calls.
6. **Phase solver.** `v2.solve_phases_fast` is a vectorised form of `encoder.solve_phases`, with the same starts and update rule plus early stopping. It agrees within 2×10⁻⁶ rad. v1's solver is unchanged.

## D13 — Experiment 3 implementation choices (logged before any experiment-3 result)

**Date:** 2026-11-03

1. **Budget:** $10, as set in Sean's run instruction. This replaces the $4 cap written in the pre-registration. The expected cost of about $2.60 is unchanged.
2. **Secondary test 1 (do order effects exist at all?)** The pre-registration compares order effects with baseline split-halves. It is implemented as a permutation test that shuffles the order labels within each item-pair. This compares the observed |P(yes | i first) − P(yes | j first)| with what run-to-run variability alone produces, using the same 5 + 5 conversations. The 5 single-turn baseline runs per item are still collected and reported.
3. **Secondary test 2 (do the largest-Δᴼ pairs show bigger effects than the smallest?)** The pre-registration says paired Wilcoxon over items. It is implemented as a sign-flip permutation test on the per-item difference, because scipy is not a dependency.
4. **Exact U_k.** In the yes/no (X) basis, H_k's coupling and field terms are diagonal and −Z_k flips qubit k. So U_k = exp(−iγ₀H_k) is applied as exact 2×2 rotations, one for each configuration of the other qubits, with no truncation. This was checked to preserve the norm to 10⁻¹².

## D14 — Pre-registered additions: hedge baseline H and version 2.1 "honest hedge" encoding

**Date:** 2026-11-04 00:45 UTC, before any test-set evaluation of v2 (the v2 fit was still running on train and validation).

These were added at Sean's request, prompted by the exploratory window vignette W4 (`paper/window-vignettes.md`), which notes that the encoding forces hedging claims into a yes or no camp. Full definitions are in `experiments/preregistration-v2.md`, Addendum B.

**Choices made here:**
- A no-lean claim is defined as |lean| ≤ 0.1. This was set from the train split's lean distribution only.
- The H primary score is the total confidence of no-lean claims, with H-count reported alongside.
- In v2.1, hedges are fixed at phase π/2 with lean 0, and are left out of the phase solver while keeping their couplings.
- The uncertainty term is U = confidence share of hedges, with a learned weight λ_h in [0, 2].
- A2.1 and F2.1 each have 10 parameters, matched to each other.
- v2.1 is evaluated on the locked test set once, after the v2 arms.

Because W4 was an exploratory observation on run-2 data, v2.1 is a hypothesis suggested by data from the run-2 hard pool. Its evaluation on the **run-2 held-out set** is therefore not independent of that suggestion. The **locked v2 test set**, which shares no item with run 2, is the clean test.

## D15 — Correction: the phase solver's frame drifts off the yes/no axis (encoding bug, documented and characterised)

**Date:** 2026-11-04. Prompted by Sean's frame check on window item h046. The work is exploratory and uses run-2 data only. It does not touch the locked v2 test set.

**Finding.** Two causes were possible: (a) a display convention error in `export_window.py`, or (b) the encoding itself. It is **not (a)**: the exported encode-stage Bloch azimuth equals the solver's φ exactly, claim for claim. It **is (b)**, in a more specific form than a free rotation.

The XY energy E(φ) = −Σ J_ij cos(φ_i − φ_j) − Σ lean_k cos φ_k is pinned by its lean anchors, so it cannot rotate freely. But the anchors are weak, with weight 1, against the relation couplings. The relation judge marks "supports" between claims that lean opposite ways when one makes the other more plausible. Those couplings pull the yes and no camps toward each other, and the ground state settles at a compromise off the readout axis. The energy is also symmetric under φ → −φ, so the direction of the tilt is arbitrary.

On h046, the yes claims sit at −62° and −71° and the no claims at −137° to −174°. Across the 225 run-2 items that have both camps:
- 20% have the yes camp more than 30° off axis;
- 20% have camps less than 90° apart;
- at least 10% have fully merged camps.

**Fix 1, a rigid frame pin (`encoder.pin_frame`), does not work.** It applies the least-squares rotation putting the yes camp at 0° and the no camp at 180°. A rotation only fixes a frame that has rotated, so it cannot pull merged camps apart. It changed nothing material.

**Fix 2, the correction: stronger anchors (`encoder.solve_phases_anchored`).** In the phase solve only, the lean field is scaled by λ = max(1, the largest total coupling Σⱼ|J_kj| of any claim in the item). This rule was fixed before its AUROC was computed. Effects:
- yes camps more than 30° off axis fall from 20% to 7%;
- the 10th-percentile camp separation rises from 0° to 147°.

The λ → ∞ limit, which puts every leaning claim exactly on the axis, is reported for reference.

**Effect on error detection, exploratory.** Exact noiseless scores on the run-2 test set:

| arm | as run | with the correction | at λ → ∞ |
|---|---|---|---|
| A0 | 0.49 [0.35, 0.62] | 0.47 [0.34, 0.61] | 0.47 [0.33, 0.60] |
| C | 0.68 [0.56, 0.79] | 0.67 [0.55, 0.78] | 0.67 [0.54, 0.78] |

Details are in `results/frame-fix-check.md`. The frame bug is real, but it does not explain the entangled arm's poor error detection.

**Disposition.**
- v1, v2 and every archived result keep the as-run solver, as pre-registered.
- Following Sean's rule ("if the fix matters, it goes into v2.1"), the correction is **not** added to v2.1, because it does not change the AUROCs. v2.1 stays a single change, the honest hedge. The v2.1 fit had not started when this was decided, so the correction could still be folded in, as a correctness fix, by a pre-registered amendment before `fit21`.
- `export_window.py` needs no fix.

## D16 — v2.1 amendment: fit noiseless, evaluate noiseless and on the noisy simulator

**Date:** 2026-11-03 18:36 MST, before any v2.1 fit or any test-set evaluation.

At Sean's instruction (`experiments/preregistration-v2.md`, Addendum C):
- A2.1 and F2.1 are fitted on exact noiseless statevectors and selected on validation.
- The selected models are evaluated once on the locked test set, noiseless, and A2.1 is also evaluated once on the noisy `ibm_fez` simulator (1,000 shots per item).
- F2.1 has no circuit, so it has only the noiseless evaluation.
- The pass criterion is applied to the noiseless comparison, with the noisy result reported alongside.
- Everything else in Addendum B is unchanged.

## D17 — Experiment 4 run 2 (graded form) pre-registered

**Date:** 2026-11-03 19:06 MST, before any run-2 call. Full design: `experiments/exp4-yearsley-trueblood.md`, "Addendum — run 2".

At Sean's request, the order test is re-run on run 1's 7 fallacy items with graded 0–100 ratings in both orders, 20 repeats per cell. Choices made here:
- Temperature is the model default (1.0); no explicit parameter is sent, because the API rejects one for this model.
- The graded analogue of "beyond repetition" is anchoring of the second rating on the first, fitted by regression.
- q_QQ and Γ are dropped, because they are defined only for binary answers. The marginal shifts OE_X, OE_Y and OSS are kept.

## D18 — Second base model (claude-sonnet-5-5): replication set-up

**Date:** 2026-11-03, before any Sonnet replication call.

At Sean's request, the hard pool (pool run 4, already defined in D6) and the training pool (new pool run 6) are run through `claude-sonnet-5-5` as base, at default effort with adaptive thinking. The extractor and judge are unchanged.

G, L, H and the **already-fitted** A2 and F2 are scored on Sonnet's errors, using the frozen v2 parameters in `results/v2-fit.json`. Nothing is refitted.

**Budget.** At about $0.02 per item, both pools (1,348 items) would cost about $27, against Sean's $15 budget. So:
- the pool runs are capped at $12 together and arm G at $3, both enforced in code;
- run 4 (the full hard pool) goes first;
- run 6 processes the locked v2 test questions first, so a budget stop still covers them, then as much of the rest as the budget allows.

What actually ran is reported in `results/sonnet-replication.md`.

## D19 — Experiment 4 run 2: the pre-registered anchoring estimator is near-tautological (logged after results)

**Date:** 2026-11-03, after run 2's results.

The pre-registered "beyond repetition" analogue regresses the second rating on the first across cells X→XY and Y→XY pooled. Because those two cells differ mainly in their first-rating means, the slope r ≈ o / (P(X) − P(Y)), so o − o_rep ≈ 0 regardless of mechanism. The run's verdict, "static classical twin (with anchoring) supported", is reported as pre-registered, but the results file says plainly that it does not show anchoring explains the effect.

An exploratory within-cell slope, using repeat-to-repeat variation only, cannot be estimated reliably either: at the default temperature the rating standard deviation is 0.00–0.05.

**Lesson for experiment 5 and later runs:** estimate anchoring only within cells, or manipulate the first rating directly.

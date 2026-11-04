# Biomimetic map (rev. 1 §3.2, rev. 2 §3.4): the probability-theory-plus-noise identity and its item-level slope on the experiment 4 items (pre-registration)

Written and frozen 2026-11-04 (America/Denver), in its own commit, before any call. DEVIATIONS.md D43. Budget **$0.10**, enforced in code (the estimate is $0.05). Stop on any refusal: the request ID goes to `results/refusal.md`, and nothing is reworded or retried.

## 1. In plain English

One account of human probability judgment says people estimate a probability by recalling a few noisy instances. Its errors, including the conjunction fallacy, come from that noise. Costello & Watts (2014) showed that in one combination the noise cancels: P(A) + P(B) − P(A and B) − P(A or B) should average 0 even when the individual judgments are biased. The versions of the sampling account that produce the fallacies predict something sharper: item by item, the combination should rise with P(A) + P(B) − 1.

We ask the model for all four ratings on the 16 experiment-4 vignettes and check both.

**Revision 2 of the map** (`f824e14`) corrected this test.
- **Z ≡ 0 does not discriminate.** Coherent probability, any shared affine distortion and PT+N 2014 all give it.
- **The fallacy-producing sampler versions predict a slope.** They give E[Z] = 2Δd·(P(X) + P(Y) − 1) (Zhu, Sanborn & Chater 2020, Table D1), so Z follows P(X) + P(Y) − 1 item by item and crosses zero at P(X) + P(Y) = 1.
- **"Parameter-free" is withdrawn.**
- **The primary test is therefore the item-level Z slope.** Mean Z within ±0.05 is secondary.

## 2. Design

- **Items:** the 16 items in `experiments/exp4-items.json`, each with context, X and Y.
- **Model:** `claude-haiku-5-5`, thinking disabled, default temperature, structured output `{"probability": integer}`. Each call is a single turn.
- **Prompt:** run 3's wording, with **one scale direction**:

  > {context}
  >
  > On a scale from 0 to 100, where 0 = certainly false and 100 = certainly true, how likely is it that {statement}? Give only the number.

- **The four statements:**
  - X;
  - Y;
  - "{X} and {Y}";
  - "{X} or {Y} (or both)".
- **Repeats and cost:** R = 20 per statement, so 16 × 4 × 20 = 1,280 calls, about $0.05.

## 3. Statistics

- **Per item:** Z = P̄(X) + P̄(Y) − P̄(X∧Y) − P̄(X∨Y), from the mean ratings on the 0–1 scale.
- **Mean Z** comes with a 2,000-resample bootstrap CI (seed 5353). Each resample draws items, then the conversations within each item.
- **Reported alongside:**
  - the conjunction-fallacy rate, P̄(X∧Y) > min(P̄(X), P̄(Y)), on all items and on run 2's 7 fallacy items (`results/exp4-run-1.json`);
  - the disjunction-fallacy rate, P̄(X∨Y) < max(P̄(X), P̄(Y));
  - per-item Z;
  - the Bayesian sampler's variance pattern: the between-repeat SD against |mean − 0.5|.

- **Primary:** the item-level OLS Z_i = a + b·(P̄(X)_i + P̄(Y)_i − 1), with the same bootstrap (seed 5354) for a and b.
  - **Split halves.** Z contains P(X) + P(Y), so shared repeat noise alone biases b upward. To remove that, the predictor uses repeats 0–9 of X and Y, and Z uses repeats 10–19 of all four statements. A check on random ratings before freezing gave b ≈ +0.95 without the split.
  - **What a positive slope does not show.** It is not unique to the sampler. Any account in which the conjunction and disjunction ratings do not move with P(X) + P(Y) gives one, including independent noise. The sampler's specific claim is a positive slope with **intercept a ≈ 0**, which is reported.
- **Variance shape** (the within-family split): the between-repeat SD peaks mid-scale for the Bayesian sampler and is constant for PT+N 2014.

## 4. Pre-registered reading

**Primary (the slope):**
- **Sampler with extra conjunction/disjunction noise:** the CI of b lies above 0. Also reported: whether the CI of a contains 0.
- **Flat (coherent, affine, or PT+N 2014):** the CI of b contains 0.
- **Opposite slope:** the CI of b lies below 0.

**Secondary (mean Z, equivalence band ±0.05):**
- holds if the CI lies within [−0.05, +0.05];
- violated if it lies wholly outside the band;
- undetermined otherwise.

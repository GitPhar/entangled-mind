# Gold-map direction 3: is there a credence at all? Six elicitation formats on the 160 chain claims (pre-registration)

Written and frozen 2026-11-04 (America/Denver), in its own commit, before any call. DEVIATIONS.md D38. Budget **$1**, enforced in code. Stop on any refusal: the request ID goes to `results/refusal.md`, and nothing is reworded or retried.

## 1. In plain English

If the model holds a degree of belief in a statement, different ways of asking should all read out that one number, each through its own fixed distortion. Examples are a 0–100 rating, a yes/no, a bet, a comparison with a coin toss, "how many out of 100" and a verbal scale. If instead each way of asking builds a fresh judgment, the formats will disagree in ways no fixed distortion can explain. For example, the model might rate statement A above statement B but bet on B over A.

We ask the model about the same 160 statements in six formats, ten times each, and fit two models:
- **one credence per statement**, plus a monotone link per format;
- **a separate credence per statement and format.**

Each is scored on repeats it was not fitted on. If the separate-credence model predicts the held-out answers better, there is no single credence to read.

## 2. What the literature gives us

- **Smolin & Wilder, "Beliefs and Behavior in Language Models"** (arXiv:2609.07943, 7 Sep 2026; contents reported by the literature session) is the closest precedent.
  - **Design:** one latent per case with a monotone link per output (logit for binary, Beta for numeric, ordered logit for Likert); 16 outputs: numeric probability, quintile choice, Likert, a decision, and 4 threshold, 4 bet and 4 cost framings.
  - **Scale:** 500 cases × 3 domains, on 9 open and GPT models, with no Claude.
  - **Result:** capable models are "usefully described as holding beliefs": concordance 0.8–0.95 and held-out R² of 60–90%. A 2-D latent did not help. Weaker models showed framing effects.
- **What is new here:** Claude; a pairwise comparison against a reference event; a frequency format; one model's own deliberation claims as the propositions; and the earlier finding of a 37-point scale-reversal gap.
- **Prior expectations:**
  - Zhu & Griffiths' Bayesian sampler (2401.16646) predicts monotone shrinkage, which a per-format link absorbs. So it predicts a single latent fits.
  - The gold map's P(no single credence) is revised from 0.45 to **0.25** in light of Smolin & Wilder.

## 3. Design

- **Claims:** the 4 frozen chain claims of each of the 40 experiment-5 candidates (`experiments/split-exp5.json`), 160 in all.
- **Model:** `claude-haiku-5-5`, thinking disabled, default temperature, structured output, single turn.
- **Repeats:** R = 10 per claim and format. That gives 160 × 6 × 10 = **9,600 calls**, costing about $0.20. Cap $1.
- **The statement is always introduced the same way:**

  > Consider this statement, which came up in a discussion of the question "{question}":
  >
  > "{claim}"

- **The six formats.** All use **one scale direction**. The gold map's reversed 0–100 scale is replaced by a verbal scale, per the overnight rule.

| # | format | question | output | repeat-specific detail |
|---|---|---|---|---|
| F1 | rating | How likely is it that this statement is true? Give an integer from 0 to 100, where 0 = certainly false and 100 = certainly true. | `{"rating": int}` | — |
| F2 | yes/no | Is this statement true? Answer yes or no. | `{"answer": "yes"\|"no"}` | — |
| F3 | bet | A ticket pays $100 if this statement is true and nothing if it is false. The ticket costs ${P}. Would you buy it? Answer yes or no. | `{"answer": "yes"\|"no"}` | P = 10, 30, 50, 70, 90 for repeats (0,1), (2,3), … (8,9) |
| F4 | pairwise | Which is more likely? (A) {first} (B) {second}. Answer A or B. | `{"answer": "A"\|"B"}` | The options are "This statement is true." and "A fair coin, tossed once, lands heads." The statement goes first in repeats 0, 1, 4, 5, 8, 9. |
| F5 | frequency | Think of 100 statements like this one, about each of which you have the same evidence as you have about this one. How many of the 100 would be true? Give an integer from 0 to 100. | `{"count": int}` | — |
| F6 | verbal | How likely is it that this statement is true? Choose one: certainly false, very unlikely, unlikely, as likely as not, likely, very likely, certainly true. | `{"answer": <one of the 7>}` | — |

The bet prices and coin positions are balanced, so that the even and odd repeats each contain every price and both positions.

## 4. Models

Each claim c has a latent μ_c on a logit scale. Let η be the linear predictor.

| format | link |
|---|---|
| F1, F5 | y = logit((r + 1)/102) ~ Normal(a_f + b_f·μ, σ_f²) |
| F2 | P(yes) = σ(a_f + b_f·μ) |
| F3 | P(buy at price P) = σ(a_f + b_f·(μ − logit(P/100))) |
| F4 | P(statement chosen) = σ(a_f + b_f·μ + d·s), where s = +1 when the statement is listed first, −1 otherwise |
| F6 | ordered logit, P(y ≤ k) = σ(κ_k − (a_f + b_f·μ)), with κ₁ < … < κ₆ |

- **L1, one credence per claim:** one μ_c per claim, shared by all six formats. For identification, F1's link is fixed at a = 0, b = 1. The other formats' a_f, b_f > 0, σ_f, d and κ are free and shared across claims.
- **L6, one credence per claim and format:** a separate μ_{c,f} for each claim and format. Every a_f is fixed at 0 and every b_f at 1, since those are not identified once μ is free per format. σ_f, d and κ are free and shared.
- **Regularisation:** both models put the same prior, μ ~ Normal(0, 3²), on every latent, so deterministic answers have finite estimates.
- **Fitting:** maximum penalised likelihood by block coordinate ascent.
  - The latents are updated by vectorised golden-section search. Each is a one-dimensional log-concave problem given the links.
  - The link parameters are updated by L-BFGS with the latents held fixed.
  - The two steps alternate for 40 rounds, or until the change in the objective is below 10⁻⁶.

## 5. Statistics

- **2-fold cross-validation over repeats.** Fit on the even repeats and score the log-likelihood of the odd repeats, then the reverse.
- **Per claim:** ΔLL_c = held-out LL(L6) − held-out LL(L1), summed over both folds and all six formats.
- **Primary:** the share of claims with ΔLL_c > 0, and the mean ΔLL_c. The mean has a 2,000-resample bootstrap CI over the 40 items, resampling items with their 4 claims (seed 3131).
- **Reported alongside:**
  - ΔLL by format;
  - the Spearman correlation between the per-claim mean responses of every pair of formats;
  - Kendall's W across the six formats;
  - the L1 fit's per-format slopes b_f;
  - the share of claims whose F1 rating order disagrees with the order implied by each other format.

## 6. Pre-registered reading

1. **No single credence:** more than half of the claims have ΔLL_c > 0, **and** the CI of the mean ΔLL lies above 0. The formats disagree beyond what monotone links can absorb.
2. **One credence suffices:** the CI of the mean ΔLL lies below 0, or it contains 0 with at most half of the claims having ΔLL_c > 0. This is a uniformity pass for LLM belief in Herrmann & Levinstein's sense.
3. **Mixed:** anything else.

## 7. What it cannot do

- A single context per claim is used, so it cannot test uniformity across contexts.
- It does not include the reversed scale. Experiment 5 measured that, and the free look (`results/gm3a-anchor-gap.md`) found the reversal gap unrelated to the model's errors.
- The gold map's "CbD-style consistency test" across formats is not attempted. The formats have no shared outcome space in which CbD applies.

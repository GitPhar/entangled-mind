# Biomimetic map (rev. 1 §3.3, rev. 2 §3.1): confidence-gated confirmation on the archived experiment 4 run 3 calls (pre-registration)

Written and frozen 2026-11-04 (America/Denver), in its own commit, **before `results/exp4-run-3-calls.json` was opened for this analysis**. DEVIATIONS.md D40. Cost $0: no API calls.

**What was already known at freezing:** the run-3 summary in `results/exp4-run-3.md` and `paper/record.md`.
- Accept rate: 0% in 15 of 32 item-orders.
- In 6 item-orders, a higher anchor gave a lower first rating.
- The manipulation check passed in both orders on 1 of 16 items.

No per-conversation breakdown by anchor direction relative to the model's lean has been computed or looked at.

## 1. In plain English

In run 3 the model was told "another person estimated the probability is A" and asked to accept or revise. In the brain, confidence acts as a gate: after a confident decision, agreeing evidence is amplified and disagreeing evidence is shut out (Rollwage et al. 2020; Talluri et al. 2018). If the model works that way:
- it should take up an estimate more when the estimate agrees with its own lean, being more extreme on the same side;
- it should take it up less when the estimate disagrees;
- the gap should be largest on statements it is most sure of.

**Revision 2 of the map** (`f824e14`) demoted this test. Two reasons:
- **It is not unique.** Bounded-scale Bayesian updating and state-dependent precision also give asymmetric, confidence-dependent uptake.
- **It is nearly empty under the faithful coding.** Talluri's coding is by sign relative to the reference, 50. An item whose own mean lies more than 30 points from 50 has both anchors on the same side.

Sean's overnight list keeps the test. It is run here with the revision-2 coding as primary and revision 1's extremity coding as secondary, and it is read as a low-power test whose pass would not single out confirmation bias.

## 2. Data and coding

- **Conversations:** `results/exp4-run-3-calls.json`, the anchored cells X-lo, X-hi, Y-lo and Y-hi. That is 16 items × 2 orders × 2 levels × 40 = 2,560 conversations. All are on one scale direction (D33).
- **own:** the statement's own free first-rating mean, from the X→XY or Y→XY cell of the same item, on the 0–1 scale.
- **Uptake** per conversation: u = (r₁ − own) / (A − own). Here r₁ is the model's stated first rating and A the provided value. u = 1 means full acceptance, 0 means the estimate was ignored, and a negative u means the model moved away from it.
  - Conversations with |A − own| < 0.05 are dropped, because u is unstable there.
  - u is winsorised to [−2, 3].
- **Consistent code (primary; revision 2, Talluri):**
  - **1** if A lies on the same side of 0.5 as own;
  - **0** if it lies on the other side.
  - Statements with own within 0.02 of 0.5 are dropped.
- **Confirmatory code (secondary; revision 1):**
  - **1** if A lies on the same side of 0.5 as own and further from 0.5;
  - **0** otherwise.
- **Extremity:** e = |own − 0.5|.

## 3. Statistics

- **Regression:** OLS at the conversation level, u ~ β₀ + β₁·code + β₂·e + β₃·code × e + β₄·|A − own|. It is fitted separately with the primary and the secondary code. The displacement term controls for the clipping at 2 and 98: on extreme items the confirmatory anchor is closer.
- **CIs:** 2,000 cluster-bootstrap resamples over the 32 item-orders (seed 5050).
- **Reported alongside:**
  - mean uptake and accept rate by code;
  - the same regression with accept (0/1) as the outcome.

## 4. Pre-registered reading

These readings use the **primary (sign) code**:
- **Confidence-gated asymmetry:** the CI of β₁ lies above 0 (uptake is higher for consistent estimates), **and** the CI of β₃ lies above 0 (the asymmetry grows with extremity).
- **Asymmetry without gating:** the CI of β₁ lies above 0, and β₃'s does not.
- **No asymmetry:** anything else, including β₁ < 0, which is reported as such.

A pass is consistent with confirmation but does not single it out (revision 2). The number of item-orders whose two anchors fall on opposite sides of 50 is reported, because only those identify β₁.

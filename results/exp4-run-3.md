# Experiment 4, run 3: a manipulated first rating

Frozen pre-registration: `experiments/exp4-run-3.md` with the D33 amendment (one scale direction: 0 = certainly false, 100 = certainly true). Base model `claude-haiku-5-5`, thinking disabled, default temperature. 16 items, 6720 calls, **$0.30**.

Fit per item and order: r₂ = β₀ + β₁·r₁ + β₂·A over the 80 anchored conversations (0–1 scale). Anchoring predicts β₀ ≈ (1 − β₁)·fresh; content-driven updating (quantum or Bayes) predicts β₀ ≈ 0.

| item | order | manipulation (r₁ hi − lo) | accept rate | β₀ [95% CI] | (1 − β₁)·fresh | β₁ | β₂ | r₂ > r₁ | class |
|---|---|---|---|---|---|---|---|---|---|
| co01 * | X first | -0.21 | 0% | +0.025 [+0.004, +0.046] | +0.100 | +0.02 | +0.01 | 0% | not scored (manipulation check failed) |
| co01 * | Y first | -0.11 | 0% | +0.042 [+0.034, +0.049] | +0.098 | +0.04 | -0.05 | 0% | not scored (manipulation check failed) |
| co02 | X first | +0.08 | 100% | +0.105 [+0.019, +0.424] | +0.077 | -0.09 | +0.01 | 0% | not scored (manipulation check failed) |
| co02 | Y first | +0.05 | 50% | +0.004 [+0.002, +0.005] | +0.053 | +0.25 | +0.04 | 0% | not scored (manipulation check failed) |
| co03 | X first | -0.03 | 16% | +2.173 [+2.150, +2.200] | +1.222 | -1.71 | -0.50 | 0% | not scored (manipulation check failed) |
| co03 | Y first | +0.00 | 0% | +0.207 [+0.198, +0.217] | +0.403 | +0.10 | unid. | 0% | not scored (manipulation check failed) |
| co04 | X first | +0.03 | 0% | -0.668 [-1.963, +0.337] | -0.138 | +1.47 | +0.08 | 0% | not scored (manipulation check failed) |
| co04 | Y first | -0.00 | 0% | -0.087 [-0.216, +0.013] | -0.009 | +1.03 | +0.05 | 2% | not scored (manipulation check failed) |
| co-lin06 * | X first | -0.21 | 0% | +0.020 [+0.007, +0.033] | +0.103 | +0.05 | +0.03 | 0% | not scored (manipulation check failed) |
| co-lin06 * | Y first | +0.06 | 18% | +0.009 [+0.004, +0.014] | +0.066 | +0.39 | +0.01 | 0% | not scored (manipulation check failed) |
| co-lin08 * | X first | +0.06 | 0% | +0.037 [+0.015, +0.060] | +0.167 | -0.01 | -0.00 | 0% | not scored (manipulation check failed) |
| co-lin08 * | Y first | +0.06 | 50% | -0.009 [-0.017, -0.003] | -0.003 | +1.02 | -0.06 | 0% | not scored (manipulation check failed) |
| co-lin09 * | X first | +0.01 | 0% | +0.083 [-0.208, +0.337] | +0.336 | +0.43 | -0.03 | 0% | not scored (manipulation check failed) |
| co-lin09 * | Y first | +0.09 | 1% | -0.006 [-0.031, +0.048] | +0.072 | +0.88 | -0.03 | 0% | not scored (manipulation check failed) |
| co-lin10 * | X first | -0.50 | 0% | +0.042 [+0.036, +0.048] | +0.047 | -0.02 | unid. | 0% | not scored (manipulation check failed) |
| co-lin10 * | Y first | -0.03 | 0% | +0.023 [+0.007, +0.028] | +0.039 | +0.14 | -0.00 | 0% | not scored (manipulation check failed) |
| co05 * | X first | +0.23 | 50% | -0.158 [-0.217, +0.010] | +0.165 | +0.43 | -0.12 | 0% | content |
| co05 * | Y first | +0.09 | 50% | +0.008 [+0.006, +0.009] | +0.280 | +0.04 | +0.08 | 0% | not scored (manipulation check failed) |
| co06 * | X first | +0.26 | 19% | +0.060 [+0.036, +0.092] | +0.238 | +0.04 | +0.04 | 0% | undetermined |
| co06 * | Y first | +0.13 | 50% | +0.008 [-0.001, +0.021] | +0.067 | +0.73 | -0.06 | 10% | content |
| co07 | X first | +0.16 | 0% | -0.016 [-1.542, +0.749] | +0.219 | +0.23 | +0.18 | 0% | undetermined |
| co07 | Y first | +0.05 | 0% | -0.105 [-0.122, -0.091] | +0.101 | +0.65 | +0.00 | 0% | not scored (manipulation check failed) |
| co08 | X first | +0.00 | 0% | +0.073 [+0.073, +0.073] | +0.113 | +0.06 | unid. | 0% | not scored (manipulation check failed) |
| co08 | Y first | +0.00 | 0% | +0.117 [+0.117, +0.117] | +0.118 | +0.02 | unid. | 0% | not scored (manipulation check failed) |
| co09 | X first | +0.07 | 0% | +3.245 [+1.573, +4.938] | +0.000 | -3.56 | -0.24 | 0% | not scored (manipulation check failed) |
| co09 | Y first | +0.15 | 50% | +0.005 [-0.002, +0.011] | +0.000 | +0.11 | -0.03 | 0% | undetermined |
| co10 | X first | +0.12 | 6% | +0.036 [+0.025, +0.042] | +0.030 | -0.01 | -0.00 | 0% | anchoring |
| co10 | Y first | +0.03 | 50% | +0.010 [+0.000, +0.013] | +0.032 | -0.05 | +0.05 | 0% | not scored (manipulation check failed) |
| co11 | X first | +0.06 | 4% | +0.039 [-0.001, +0.083] | +0.031 | -0.03 | +0.02 | 0% | not scored (manipulation check failed) |
| co11 | Y first | +0.03 | 50% | +0.003 [-0.009, +0.009] | +0.020 | +0.33 | +0.02 | 0% | not scored (manipulation check failed) |
| co12 | X first | +0.03 | 0% | -0.246 [-0.273, -0.215] | +0.002 | +0.99 | unid. | 0% | not scored (manipulation check failed) |
| co12 | Y first | +0.06 | 0% | +1.169 [+0.478, +1.949] | +0.796 | -2.05 | +0.21 | 0% | not scored (manipulation check failed) |

\* = one of run 2's 7 fallacy items.

## Slope ratio, on items content-driven in both orders

No item was content-driven in both orders.

Replication of run 2's free-rating order effect o (X→XY minus Y→XY): co01 +0.03, co-lin06 +0.10, co-lin08 +0.00, co-lin09 -0.01, co-lin10 +0.02, co05 +0.04, co06 +0.04.

## Verdict, all 16 items: **untestable (fewer than 3 items pass the manipulation check in both orders: 1)**

Verdict, run 2's 7 fallacy items: **untestable (fewer than 3 items pass the manipulation check in both orders: 1)**

## Reading

- **Untestable, by the pre-registered manipulation check.** The design needed the provided first rating to move the model's own first rating r₁ by at least 10 points between the low and high anchors. Only 6 of 32 item-orders passed, and only 1 item (co06) passed in both orders, against the 3 required. The mechanism question (anchoring vs content-driven updating, and rank-one quantum vs Bayes) cannot be answered from these data.
- **The informative outcome the draft anticipated (§6): the model's first ratings resist social anchors.**
  - **It usually rejects the provided estimate.** The accept rate is 0% in 17 of 32 item-orders; the first rating moves toward the provided value by a median of only 9% of the low-to-high gap.
  - **It sometimes reacts against the anchor.** In 5 item-orders, a higher provided estimate produced a reliably *lower* first rating, down to −0.50 on Marta (co-lin10, X first). These reliable reversals all occur on the three Linda-family vignettes, often as a fixed answer (Marta: 35 in 40 of 40 against a provided 98); their mechanism is not identified.
  - **The ceiling held.** The conjunction rating almost never exceeded the first rating (r₂ > r₁ in at most 10% of conversations, and 0% in most item-orders), as both content-driven accounts require.
- **Where r₁ barely moved, the regression estimates are unstable** (for example β₀ = +2.17 or +3.25) and should not be read. Those item-orders are marked not scored.
- **Run 2's order effect only partly replicates under the explicit scale wording.**
  - Bill (co-lin06) replicates at +0.10.
  - Marta (co-lin10) falls from about +0.10 to +0.02, and co05 from +0.07 to +0.04.
  - Stating the scale direction ("0 = certainly false, 100 = certainly true") appears to shrink some of the graded order effects. That itself is a measurement-sensitivity finding.
- **What it would take to test the mechanism:** a manipulation the model does not resist. For example, set the first rating as the model's own earlier answer in the transcript, not as another person's estimate. That is the "planted answers" condition of `paper/gold-map.md` §2, and it needs its own pre-registration.

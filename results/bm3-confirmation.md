# Biomimetic (rev. 2 §3.1): confidence-gated confirmation on the archived run-3 calls

Pre-registered in `experiments/bm3-confirmation.md` (D40), committed before the archive was opened for this analysis. 2080 anchored conversations in 30 item-orders (dropped: 320 with |A − own| < 0.05, 160 with own within 0.02 of 0.5). $0.

## In plain English

**The question.** In run 3 the model was shown "another person estimated the probability is A" and asked to accept or revise. In the brain, confidence gates what evidence gets in: after a confident decision, agreeing evidence is amplified and disagreeing evidence is shut out. Does the model take up an estimate more when it falls on the same side of 50 as its own view?

**What we found.** No, and if anything the reverse.
- **Uptake by side.** On average the model ignored or pushed back on estimates that agreed with its side: mean uptake −0.03. It moved a little toward estimates on the other side: +0.21.
- **After controlling for distance and extremity,** the regression difference is −0.18 [−0.83, +0.28], which is not reliable either way.
- **Acceptance.** Raw accept rates are 9.7% (agreeing) against 11.3%. With covariates the coefficient is −0.29 [−0.79, −0.03], but it rests on one item-order (co05 X; without it −0.18 [−0.48, +0.02]), and it is one of 15 secondary coefficients.
- **The confidence gate,** meaning that the asymmetry grows with how sure the model is, is not shown: +0.70 [−0.81, +2.53].

**What it means.** No confirmation bias toward another person's number was detected (−0.18 [−0.83, +0.28]). The direction, if any, matches Kumaran et al.'s LLMs, which over-weight *opposing* advice.

**Caveats.**
- The test is weak by design: only 13 of 30 item-orders have estimates on both sides of 50.
- Revision 2 of the map notes that a positive result would not have singled out confirmation anyway.

## Regression of uptake u = (r₁ − own)/(A − own)

Primary code: consistent = the anchor lies on the same side of 50 as the model's own mean (revision 2). Item-orders whose two anchors fall on opposite sides of 50, which alone identify β₁: **13 of 30**. Secondary: revision 1's confirmatory code (same side and more extreme).

| term | uptake, primary code [95% cluster-bootstrap CI] | accept (0/1), primary [CI] | uptake, revision-1 code [CI] |
|---|---|---|---|
| intercept β₀ | -0.722 [-1.866, +0.368] | +0.422 [+0.006, +1.022] | -1.302 [-2.286, -0.142] |
| consistent β₁ | -0.179 [-0.832, +0.280] | -0.294 [-0.794, -0.030] | -0.238 [-0.797, +0.219] |
| extremity β₂ | -0.214 [-1.454, +0.865] | -0.399 [-1.827, +0.450] | +0.067 [-0.540, +0.691] |
| consistent × extremity β₃ | +0.698 [-0.812, +2.534] | +0.868 [-0.156, +2.587] | +1.819 [-0.658, +4.172] |
| |A − own| β₄ | +3.031 [-0.171, +6.460] | -0.757 [-2.182, +0.545] | +4.759 [+0.934, +7.762] |

| anchor (primary code) | conversations | mean uptake | accept rate |
|---|---|---|---|
| consistent (same side of 50) | 1560 | -0.031 | 9.7% |
| inconsistent (other side) | 520 | +0.211 | 11.3% |

## Pre-registered reading: **no asymmetry**

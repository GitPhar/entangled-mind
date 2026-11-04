# Biomimetic (rev. 2 §3.4): the probability-theory-plus-noise identity and its Z slope on the experiment 4 items

Pre-registered in `experiments/bm2-sampling-identity.md` (D43), committed before any call. 16 items × 4 statements × 20, `claude-haiku-5-5`, thinking disabled, one scale direction. 1280 calls, **$0.046** of the $0.10 cap; no refusal.

## In plain English

**The question.** One account of human probability judgment says estimates come from a few noisy recalled samples. Its fallacy-producing versions predict a specific pattern: the combination Z = P(A) + P(B) − P(A and B) − P(A or B) should rise item by item with P(A) + P(B) − 1. We asked the model for all four ratings on the 16 experiment-4 vignettes, 20 times each, on one scale.

**What we found.**
- **The conjunction fallacy is there.** The mean rating of "A and B" exceeds the less likely conjunct on 8 of 16 items, but by under 1 point on 4 of them; it is clear on 4 (co05, co06, co-lin08, co01). It shows the disjunction fallacy on 7.
- **Yet no sampler slope is detected in Z.** The slope is +0.02 [−0.17, +0.16], flat by the pre-registered rule.
- **Z sits near zero:** −0.03 [−0.07, +0.00]. That is close to Costello & Watts' human values but not tight enough to pass the ±0.05 band.
- **Repeat-to-repeat spread is largest for mid-scale statements** (r = −0.54). That fits a Bayesian sampler, but floor and ceiling effects predict the same.

**What it means.** The model commits the classic fallacies, yet its four ratings nearly cancel in Costello & Watts' combination, with no item-by-item slope.
- **Coherent probability** cannot produce the fallacies at all, so it is ruled out, along with any shared distortion of coherent values.
- **The later fallacy-producing sampler versions** need the slope, and it isn't there.
- **No pre-registered account fits both facts.** Mean-level fallacies rule out coherent, affine and PT+N 2014 (whose mean is affine); the flat slope disfavours the extra-noise versions.
- **The variance evidence points the other way.** The mid-scale peak in spread favours the Bayesian sampler over PT+N 2014, which predicts constant spread, but floors and ceilings confound that.

The slope test is flat, as pre-registered; the fallacy pattern is not explained by any account in the flat class.

## Z = P(X) + P(Y) − P(X∧Y) − P(X∨Y)

- **Primary: item-level slope of Z (repeats 10–19) on P(X) + P(Y) − 1 (repeats 0–9): b = +0.015 [-0.165, +0.164]**; intercept a = -0.032 [-0.073, +0.019] (bootstrap over items and conversations).
- Secondary: mean Z = -0.034 [-0.071, +0.002] (equivalence band ±0.05): **undetermined**.
- Conjunction fallacy (P(X∧Y) > min): 8 of 16 items; 6 of the 7 run-2 fallacy items. Disjunction fallacy (P(X∨Y) < max): 7 of 16.
- Between-repeat SD against |mean − 0.5| across the 64 statements: r = -0.54 (the Bayesian sampler predicts negative; floors and ceilings predict the same).

| item | P(X) | P(Y) | P(X∧Y) | P(X∨Y) | Z | conj. fallacy | run-2 fallacy item |
|---|---|---|---|---|---|---|---|
| co01 | 0.85 | 0.06 | 0.11 | 0.85 | -0.05 | yes | yes |
| co02 | 0.96 | 0.06 | 0.07 | 0.96 | -0.01 | yes |  |
| co03 | 0.86 | 0.50 | 0.46 | 1.00 | -0.09 | no |  |
| co04 | 0.75 | 0.30 | 0.30 | 0.93 | -0.17 | no |  |
| co-lin06 | 0.90 | 0.11 | 0.11 | 0.90 | -0.01 | yes | yes |
| co-lin08 | 0.55 | 0.05 | 0.16 | 0.47 | -0.04 | yes | yes |
| co-lin09 | 0.71 | 0.58 | 0.59 | 0.71 | -0.01 | yes | yes |
| co-lin10 | 0.85 | 0.05 | 0.04 | 0.85 | +0.01 | no | yes |
| co05 | 0.38 | 0.07 | 0.29 | 0.24 | -0.08 | yes | yes |
| co06 | 0.44 | 0.08 | 0.26 | 0.37 | -0.10 | yes | yes |
| co07 | 0.54 | 0.35 | 0.31 | 0.74 | -0.16 | no |  |
| co08 | 0.80 | 0.15 | 0.12 | 0.83 | -0.00 | no |  |
| co09 | 0.80 | 0.10 | 0.00 | 0.78 | +0.12 | no |  |
| co10 | 0.85 | 0.03 | 0.03 | 0.85 | +0.00 | yes |  |
| co11 | 0.78 | 0.03 | 0.03 | 0.75 | +0.03 | no |  |
| co12 | 0.51 | 0.45 | 0.27 | 0.66 | +0.04 | no |  |

## Pre-registered reading: **flat Z slope: coherent, affine or PT+N 2014**

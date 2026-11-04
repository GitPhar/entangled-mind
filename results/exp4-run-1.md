# Experiment 4, run 1: quantitative Yearsley & Trueblood test

Pre-registration: `experiments/exp4-yearsley-trueblood.md` (with the D11 addendum: meeting R2 is consistent with the quantum model *or* a sequential-update classical model; it rules out only the static twin). Base model `claude-haiku-5-5`, thinking disabled. 5480 calls, **$0.23**.

## Phase 1: ratings (0–1)

| item | P(X) | P(Y) | P(X and Y) | P(Y and X) | fallacy P(X and Y) − P(Y) [95% CI] | double fallacy [95% CI] |
|---|---|---|---|---|---|---|
| co01 | 0.85 | 0.05 | 0.14 | 0.09 | +0.085 [+0.072, +0.095] | -0.715 [-0.728, -0.705] |
| co02 | 0.97 | 0.08 | 0.03 | 0.03 | -0.049 [-0.054, -0.044] | -0.937 [-0.940, -0.934] |
| co03 | 0.85 | 0.50 | 0.37 | 0.36 | -0.128 [-0.148, -0.110] | -0.478 [-0.497, -0.460] |
| co04 | 0.78 | 0.27 | 0.27 | 0.19 | -0.000 [-0.013, +0.015] | -0.510 [-0.523, -0.498] |
| co-lin06 | 0.82 | 0.07 | 0.09 | 0.11 | +0.019 [+0.003, +0.035] | -0.738 [-0.758, -0.716] |
| co-lin08 | 0.57 | 0.04 | 0.12 | 0.20 | +0.084 [+0.060, +0.109] | -0.446 [-0.470, -0.420] |
| co-lin09 | 0.71 | 0.45 | 0.59 | 0.60 | +0.143 [+0.111, +0.176] | -0.117 [-0.137, -0.099] |
| co-lin10 | 0.85 | 0.04 | 0.07 | 0.07 | +0.029 [+0.004, +0.053] | -0.779 [-0.801, -0.754] |
| co05 | 0.51 | 0.04 | 0.33 | 0.13 | +0.287 [+0.267, +0.303] | -0.175 [-0.208, -0.140] |
| co06 | 0.48 | 0.09 | 0.28 | 0.33 | +0.191 [+0.160, +0.222] | -0.200 [-0.238, -0.165] |
| co07 | 0.65 | 0.39 | 0.23 | 0.30 | -0.160 [-0.185, -0.137] | -0.425 [-0.445, -0.405] |
| co08 | 0.80 | 0.15 | 0.12 | 0.12 | -0.030 [-0.030, -0.030] | -0.680 [-0.680, -0.680] |
| co09 | 0.82 | 0.05 | 0.00 | 0.02 | -0.046 [-0.049, -0.042] | -0.816 [-0.828, -0.805] |
| co10 | 0.78 | 0.04 | 0.03 | 0.03 | -0.015 [-0.019, -0.011] | -0.755 [-0.766, -0.743] |
| co11 | 0.79 | 0.03 | 0.03 | 0.03 | -0.001 [-0.002, +0.000] | -0.765 [-0.774, -0.756] |
| co12 | 0.55 | 0.49 | 0.25 | 0.25 | -0.236 [-0.247, -0.225] | -0.297 [-0.303, -0.288] |

**7 of 16 items show a reliable fallacy** (lower bound > 0) and go to phase 2. Reliable double fallacies (R3): **0**.

## Phase 2: committed forced-branch QQ audit (fallacy items)

Every order-effect number is shown with the marginal-shift check next to it: OE_X and OE_Y (each question's yes-rate when asked second minus first), OSS = |OE_X| + |OE_Y|, q_QQ and Γ = |q_QQ| − OSS (Γ ≤ 0: non-contextual under rank-2 Contextuality-by-Default).

| item | o = P(X then Y) − P(Y then X) | binary fallacy f | o − o_rep (beyond repetition) | repeat r | letter-copy ρ | OE_X | OE_Y | OSS | q_QQ | Γ | saturated |
|---|---|---|---|---|---|---|---|---|---|---|---|
| co01 | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | 0.00 | +0.01 | +0.000 | +0.000 | 0.000 | +0.000 | +0.000 | yes |
| co-lin06 | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | 0.00 | +0.04 | +0.670 | +0.000 | 0.670 | -0.670 | +0.000 | yes |
| co-lin08 | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | 0.18 | -0.07 | +0.500 | +0.000 | 0.500 | -0.500 | +0.000 | yes |
| co-lin09 | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | -0.053 [-0.057, -0.041] | 0.24 | +0.00 | -0.220 | +0.000 | 0.220 | +0.220 | +0.000 | yes |
| co-lin10 | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | -0.029 [-0.063, +0.000] | 0.05 | -0.02 | +0.430 | +0.000 | 0.430 | -0.430 | +0.000 | yes |
| co05 | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | 0.00 | +0.00 | +0.000 | +0.000 | 0.000 | +0.000 | +0.000 | yes |
| co06 | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | 0.00 | +0.00 | +0.000 | +0.000 | 0.000 | +0.000 | +0.000 | yes |

## Pre-registered rules

- Scored items (fallacy item, not saturated, no letter copying, binary fallacy reliably > 0): **0**.
- R2, o ≥ f − 0.05: 0 of 0. Order effect beyond repetition reliably > 0: 0 of 0.
- Static twin (o − o_rep interval contains 0): 0 of 0.
- R1, fallacy items with an order effect reliably ≠ 0: 0 of 7.
- R3, reliable double fallacies: 0 of 16.

**Verdict: untestable (0 scored items; reported descriptively).**

## Reading

- **The rating phase shows conjunction fallacies.** 7 of the 16 items have a reliable fallacy, with P(X and Y) rated above P(Y). The largest are the author-written co05 (+0.29) and co06 (+0.19), and Linda (co01) is +0.085. There are **no double fallacies** (R3), which is what the quantum account requires and what Yearsley & Trueblood (2018) found in people.
- **The binary QQ phase is fully saturated, so R2 cannot be tested.** On every fallacy item the model answers "Is it true that <Y>?" with *no* in all 100 first-position samples. The low-probability conjunct is never affirmed when asked as a yes/no question about truth. P(X then Y) is therefore identically 0 in both orders, both o and f are 0, and no item is scored. This is the saturation caveat of Kang (2026) in its strongest form.
- **The order effect lives in the marginals.** On four items, X's yes-rate changes when X is asked second (OE_X = +0.67, +0.50, −0.22, +0.43; OSS = OE). With Y pinned at "no", that effect cannot reach the joint yes-yes probability that R2 is about. Γ = 0 on every item, but only because Y is deterministic (q_QQ = −OE_X), so the Contextuality-by-Default check is uninformative here.
- **This is a measurement problem, not a verdict for either account.** A binary "is it true?" question elicits a truth judgment, not a probability judgment. The fallacy shows up in graded ratings and disappears under yes/no truth questions. A future run would need a graded sequential measure, such as rating P(Y) after committing to X, or sampling at higher temperature, to put dispersion into the joint distribution.

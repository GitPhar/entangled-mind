# Experiment 5, run 1: sequential, context-dependent judgment

Frozen pre-registration: `experiments/exp5-sequential-judgment.md` (D22–D26). Base model `claude-haiku-5-5`, thinking disabled, default temperature. 40 items × 12 chain types × 10 conversations, plus the QQ block (40 items × 2 pairs × 2 orders × 40). Pilot gates passed (`results/exp5-pilot.md`). Conversations excluded for a schema failure: 0. Conversations in all (pilot included): 12,600; experiment-5 API cost **$1.93** of the $4 cap; no refusal.

Predicted non-commutativity at encode: |sin Δφ| > 10⁻⁶ on 12 of 160 chain claims across the 40 items (max 0.424); every other chain claim's sub-question commutes with the main question at encode.

> As the pre-registration put it before any data (§8.6): *the anchored phase solve works against A5 … Expect A5 and F5 to be close on most claims.* The pre-registration anticipated that A5 and F5 would be close; it designated no verdict as predicted.

## Fits (train / validation MSE, rating points²)

| model | train | validation | parameters |
|---|---|---|---|
| A5 quantum belief state (fitted) | 804.0 | 915.8 | kappa=0.293, gamma=1.15, beta=0.142, a=0.262, b=0.734 |
| F5 classical twin (fitted) | 883.5 | 955.3 | kappa_F=2.14, T=4.2, lam=0, a=0.305, b=0.747 |
| D5 dephased quantum (fitted) | 816.9 | 929.5 | kappa=0.649, gamma=0.947, beta=0.121, a=0.194, b=0.795 |
| BA5 belief adjustment (fitted; M only) | 784.4 | 880.8 | w_supp=0.508, w_con=0.219, rho=0.877, a=0.237, b=0.785 |
| A5 with κ = 0 (fitted) | 819.1 | 935.5 | gamma=0.377, beta=0, a=0.293, b=0.702 |
| A5 with the plain v1 solver (sensitivity) | 808.3 | 924.8 | kappa=0.306, gamma=1.05, beta=0.116, a=0.238, b=0.75 |

## Test chains (77, scored once)

| model | MSE, all ratings | MSE, main ratings only |
|---|---|---|
| A5 quantum belief state (fitted) | 984.0 | 872.9 |
| F5 classical twin (fitted) | 1050.9 | 919.5 |
| D5 dephased quantum (fitted) | 987.8 | 851.5 |
| BA5 belief adjustment (fitted; M only) | — | 827.1 |
| A5 with κ = 0 (fitted) | 1008.4 | 896.5 |
| A5 with the plain v1 solver (sensitivity) | 989.6 | 890.3 |
| A5⁰ (a priori, unfitted) | 1088.3 | 920.4 |
| F5⁰ (a priori, unfitted) | 1739.7 | 1706.2 |

Paired item-bootstrap differences (positive favours the first-named model's competitor being worse):

- **Δ = MSE_F5 − MSE_A5: +67.0 [-34.1, +211.5]**
- A5⁰ vs F5⁰ (unfitted): MSE_F5⁰ − MSE_A5⁰ = +651.4 [+414.6, +910.3]
- entanglement ablation: MSE_(A5, κ=0) − MSE_A5 = +24.4 [-8.0, +60.5]
- dephasing: MSE_D5 − MSE_A5 = +3.8 [-21.8, +30.9]
- main ratings only: MSE_BA5 − MSE_A5 = -45.8 [-94.1, +14.1]; MSE_F5 − MSE_A5 = +46.6 [-27.1, +142.2]
- sensitivity (plain solver): MSE_F5 − MSE_A5plain = +61.4 [-46.6, +218.7]

## Held-out items (8, scored once)

| model | MSE, all ratings | MSE, main ratings only |
|---|---|---|
| A5 quantum belief state (fitted) | 779.7 | 645.7 |
| F5 classical twin (fitted) | 987.0 | 731.0 |
| D5 dephased quantum (fitted) | 768.4 | 596.1 |
| BA5 belief adjustment (fitted; M only) | — | 651.7 |
| A5 with κ = 0 (fitted) | 812.9 | 712.4 |
| A5 with the plain v1 solver (sensitivity) | 837.2 | 642.4 |
| A5⁰ (a priori, unfitted) | 922.5 | 691.3 |
| F5⁰ (a priori, unfitted) | 1642.6 | 1324.6 |

Paired item-bootstrap differences (positive favours the first-named model's competitor being worse):

- **Δ = MSE_F5 − MSE_A5: +207.3 [+52.0, +387.5]**
- A5⁰ vs F5⁰ (unfitted): MSE_F5⁰ − MSE_A5⁰ = +720.1 [+510.0, +924.9]
- entanglement ablation: MSE_(A5, κ=0) − MSE_A5 = +33.2 [-23.6, +103.5]
- dephasing: MSE_D5 − MSE_A5 = -11.3 [-61.4, +44.9]
- main ratings only: MSE_BA5 − MSE_A5 = +5.9 [-75.7, +103.6]; MSE_F5 − MSE_A5 = +85.3 [-11.2, +191.0]
- sensitivity (plain solver): MSE_F5 − MSE_A5plain = +149.8 [+29.1, +284.2]

## Primary (§7.2): **TIE**

## Parameter-free check 1: QQ on adjacent (S_k, M) pairs (§7.3)

- G2 (pilot): passed. Pairs: 80. Pairs with OE > 0.10 and CI excluding 0: **60**.
- On those pairs: KS of z against N(0,1) D = 0.385, p = 0.000; mean q = +0.005 [-0.058, +0.065].
- Signature present: **False**; contradicted: **False**.
- A priori sub-test (OE larger on the larger-|sin Δφ| pair): 1 wins, 2 losses over 3 items with distinct predicted non-commutativity (37 items tied within 10⁻⁶, almost all with both pairs at 0); one-sided sign test p = 0.875. (First computed with exact float comparison, which let solver round-off of 10⁻¹⁶–10⁻⁹ order the pairs and gave a spurious 28–9; corrected in D32.)

| pair | |sin Δφ| | OE [95% CI] | OE_S | OE_M | OSS | q | z | Γ |
|---|---|---|---|---|---|---|---|---|
| h190:S2 | 0.000 | 0.12 [0.00, 0.28] | +0.00 | +0.12 | 0.12 | -0.125 | -1.52 | +0.00 |
| h190:S5 | 0.000 | 0.55 [0.28, 0.85] | -0.23 | +0.33 | 0.55 | +0.100 | +1.70 | -0.45 |
| h101:S3 | 0.000 | 0.12 [0.03, 0.23] | +0.00 | -0.12 | 0.12 | +0.125 | +2.31 | +0.00 |
| h101:S2 | 0.000 | 0.12 [0.07, 0.47] | +0.10 | +0.02 | 0.12 | +0.025 | +0.29 | -0.10 |
| h112:S5 | 0.000 | 0.32 [0.13, 0.55] | +0.17 | +0.15 | 0.32 | +0.175 | +1.57 | -0.15 |
| h112:S2 | 0.000 | 0.15 [0.03, 0.58] | +0.07 | -0.07 | 0.15 | -0.050 | -1.43 | -0.10 |
| h191:S2 | 0.000 | 0.45 [0.30, 0.57] | +0.00 | -0.45 | 0.45 | +0.450 | +4.82 | -0.00 |
| h191:S9 | 0.000 | 0.03 [0.02, 0.47] | +0.00 | -0.03 | 0.03 | -0.025 | -0.59 | -0.00 |
| h261:S0 | 0.424 | 0.15 [0.05, 0.28] | +0.00 | -0.15 | 0.15 | +0.150 | +2.55 | -0.00 |
| h261:S6 | 0.000 | 1.05 [0.95, 1.18] | -0.45 | -0.60 | 1.05 | -0.850 | -7.64 | -0.20 |
| h058:S1 | 0.000 | 0.62 [0.43, 0.82] | -0.07 | -0.55 | 0.62 | +0.475 | +4.42 | -0.15 |
| h058:S3 | 0.000 | 0.10 [0.05, 0.30] | -0.05 | -0.05 | 0.10 | +0.100 | +2.05 | -0.00 |
| h221:S5 | 0.000 | 0.60 [0.40, 0.90] | +0.50 | -0.10 | 0.60 | -0.100 | -0.94 | -0.50 |
| h221:S2 | 0.000 | 0.45 [0.12, 0.82] | +0.22 | -0.22 | 0.45 | -0.050 | -0.59 | -0.40 |
| h279:S6 | 0.000 | 1.00 [0.77, 1.23] | +0.53 | -0.47 | 1.00 | -0.050 | -0.45 | -0.95 |
| h279:S3 | 0.000 | 0.00 [0.00, 0.25] | +0.00 | +0.00 | 0.00 | +0.000 | +0.00 | +0.00 |
| h127:S0 | 0.000 | 0.82 [0.45, 1.18] | +0.27 | +0.55 | 0.82 | -0.275 | -3.57 | -0.55 |
| h127:S3 | 0.000 | 0.53 [0.30, 0.78] | +0.22 | -0.30 | 0.52 | +0.075 | +0.70 | -0.45 |
| h238:S3 | 0.000 | 0.07 [0.00, 0.15] | +0.00 | -0.07 | 0.07 | +0.075 | +1.77 | +0.00 |
| h238:S5 | 0.000 | 0.30 [0.15, 0.48] | +0.17 | -0.12 | 0.30 | +0.200 | +2.70 | -0.10 |
| h111:S5 | 0.000 | 0.70 [0.50, 1.02] | +0.10 | -0.60 | 0.70 | -0.300 | -3.10 | -0.40 |
| h111:S1 | 0.000 | 0.03 [0.00, 0.07] | +0.03 | +0.00 | 0.03 | +0.025 | +1.01 | -0.00 |
| h197:S4 | 0.000 | 0.32 [0.23, 0.65] | +0.33 | +0.00 | 0.33 | -0.225 | -2.03 | -0.10 |
| h197:S3 | 0.000 | 0.00 [0.00, 0.50] | +0.00 | +0.00 | 0.00 | +0.000 | +0.00 | +0.00 |
| h293:S3 | 0.000 | 0.15 [0.05, 0.50] | +0.02 | -0.13 | 0.15 | +0.050 | +0.50 | -0.10 |
| h293:S2 | 0.000 | 0.05 [0.03, 0.43] | +0.00 | -0.05 | 0.05 | +0.050 | +0.54 | +0.00 |
| h102:S0 | 0.000 | 0.53 [0.35, 0.70] | -0.05 | -0.47 | 0.53 | -0.475 | -4.83 | -0.05 |
| h102:S5 | 0.000 | 0.65 [0.45, 0.85] | +0.15 | -0.50 | 0.65 | +0.350 | +3.34 | -0.30 |
| h135:S6 | 0.144 | 0.57 [0.30, 0.90] | +0.17 | -0.40 | 0.57 | +0.125 | +1.37 | -0.45 |
| h135:S3 | 0.026 | 0.95 [0.70, 1.20] | +0.57 | -0.38 | 0.95 | -0.300 | -2.81 | -0.65 |
| h152:S0 | 0.000 | 0.68 [0.33, 1.00] | +0.40 | +0.28 | 0.68 | -0.125 | -1.62 | -0.55 |
| h152:S6 | 0.000 | 0.15 [0.03, 0.30] | -0.03 | -0.12 | 0.15 | +0.150 | +1.77 | +0.00 |
| h222:S4 | 0.000 | 0.67 [0.35, 0.98] | +0.32 | -0.35 | 0.67 | +0.025 | +0.25 | -0.65 |
| h222:S1 | 0.000 | 0.57 [0.35, 0.82] | +0.10 | -0.47 | 0.57 | +0.375 | +3.38 | -0.20 |
| h027:S3 | 0.000 | 0.65 [0.40, 0.93] | -0.25 | -0.40 | 0.65 | +0.150 | +1.77 | -0.50 |
| h027:S1 | 0.000 | 0.48 [0.40, 0.82] | -0.20 | -0.28 | 0.47 | -0.475 | -4.83 | +0.00 |
| h115:S3 | 0.000 | 0.90 [0.62, 1.20] | +0.40 | -0.50 | 0.90 | -0.050 | -1.03 | -0.85 |
| h115:S2 | 0.000 | 0.50 [0.25, 0.80] | +0.30 | -0.20 | 0.50 | -0.100 | -0.89 | -0.40 |
| h137:S6 | 0.000 | 0.50 [0.23, 0.80] | +0.17 | -0.33 | 0.50 | +0.150 | +1.36 | -0.35 |
| h137:S5 | 0.000 | 0.38 [0.23, 0.53] | +0.00 | -0.38 | 0.38 | +0.375 | +4.30 | +0.00 |
| h142:S4 | 0.000 | 0.25 [0.05, 0.45] | +0.00 | -0.25 | 0.25 | +0.250 | +2.31 | +0.00 |
| h142:S7 | 0.000 | 0.08 [0.05, 0.50] | -0.02 | -0.05 | 0.07 | -0.025 | -0.59 | -0.05 |
| h214:S4 | 0.000 | 0.18 [0.05, 0.40] | -0.10 | -0.08 | 0.18 | +0.125 | +1.12 | -0.05 |
| h214:S7 | 0.000 | 0.12 [0.05, 0.55] | +0.03 | -0.10 | 0.13 | +0.075 | +1.77 | -0.05 |
| h187:S5 | 0.000 | 0.00 [0.00, 0.23] | +0.00 | +0.00 | 0.00 | +0.000 | +0.00 | +0.00 |
| h187:S8 | 0.000 | 0.25 [0.05, 0.62] | -0.07 | +0.18 | 0.25 | +0.100 | +1.35 | -0.15 |
| h019:S4 | 0.000 | 0.70 [0.40, 1.00] | +0.20 | -0.50 | 0.70 | +0.100 | +1.12 | -0.60 |
| h019:S3 | 0.000 | 1.27 [1.10, 1.45] | +0.80 | -0.47 | 1.27 | -0.525 | -5.07 | -0.75 |
| h173:S0 | 0.000 | 0.72 [0.52, 0.93] | +0.30 | -0.42 | 0.73 | +0.125 | +1.16 | -0.60 |
| h173:S5 | 0.000 | 0.55 [0.35, 0.75] | +0.15 | -0.40 | 0.55 | +0.250 | +2.44 | -0.30 |
| h149:S7 | 0.206 | 0.13 [0.05, 0.40] | +0.10 | -0.03 | 0.12 | -0.025 | -0.23 | -0.10 |
| h149:S2 | 0.012 | 0.12 [0.08, 0.55] | +0.00 | +0.12 | 0.12 | -0.125 | -1.98 | +0.00 |
| h048:S3 | 0.000 | 0.38 [0.20, 0.55] | +0.00 | -0.38 | 0.38 | +0.375 | +3.62 | +0.00 |
| h048:S1 | 0.000 | 0.50 [0.33, 0.68] | +0.00 | +0.50 | 0.50 | -0.500 | -5.16 | +0.00 |
| h291:S2 | 0.000 | 0.68 [0.57, 0.93] | +0.65 | +0.03 | 0.68 | +0.275 | +2.56 | -0.40 |
| h291:S8 | 0.000 | 0.53 [0.35, 0.78] | -0.10 | -0.42 | 0.52 | +0.225 | +2.13 | -0.30 |
| h093:S3 | 0.000 | 0.00 [0.00, 0.00] | +0.00 | +0.00 | 0.00 | +0.000 | +0.00 | +0.00 |
| h093:S7 | 0.000 | 0.00 [0.00, 0.00] | +0.00 | +0.00 | 0.00 | +0.000 | +0.00 | +0.00 |
| h183:S3 | 0.000 | 0.20 [0.07, 0.33] | +0.00 | -0.20 | 0.20 | +0.200 | +2.98 | -0.00 |
| h183:S6 | 0.000 | 0.15 [0.05, 0.28] | +0.00 | -0.15 | 0.15 | +0.150 | +2.55 | +0.00 |
| h237:S2 | 0.000 | 0.12 [0.07, 0.38] | +0.00 | -0.12 | 0.12 | -0.025 | -0.25 | -0.10 |
| h237:S5 | 0.000 | 0.33 [0.18, 0.47] | +0.00 | -0.33 | 0.33 | +0.325 | +3.94 | -0.00 |
| h080:S3 | 0.000 | 0.45 [0.28, 0.62] | -0.45 | +0.00 | 0.45 | -0.450 | -4.51 | -0.00 |
| h080:S1 | 0.000 | 0.00 [0.00, 0.00] | +0.00 | +0.00 | 0.00 | +0.000 | +0.00 | +0.00 |
| h033:S7 | 0.000 | 0.50 [0.35, 0.65] | -0.50 | +0.00 | 0.50 | -0.500 | -5.16 | +0.00 |
| h033:S8 | 0.000 | 0.00 [0.00, 0.00] | +0.00 | +0.00 | 0.00 | +0.000 | +0.00 | +0.00 |
| h090:S4 | 0.000 | 0.30 [0.15, 0.45] | +0.00 | -0.30 | 0.30 | +0.300 | +3.76 | -0.00 |
| h090:S1 | 0.000 | 0.00 [0.00, 0.00] | +0.00 | +0.00 | 0.00 | +0.000 | +0.00 | +0.00 |
| h248:S0 | 0.000 | 0.60 [0.50, 0.77] | -0.07 | -0.33 | 0.40 | -0.600 | -5.86 | +0.20 |
| h248:S3 | 0.000 | 0.40 [0.22, 0.62] | +0.00 | -0.40 | 0.40 | +0.400 | +4.01 | +0.00 |
| h158:S4 | 0.000 | 0.00 [0.00, 0.00] | +0.00 | +0.00 | 0.00 | +0.000 | +0.00 | +0.00 |
| h158:S2 | 0.000 | 0.00 [0.00, 0.00] | +0.00 | +0.00 | 0.00 | +0.000 | +0.00 | +0.00 |
| h126:S6 | 0.000 | 0.00 [0.00, 0.00] | +0.00 | +0.00 | 0.00 | +0.000 | +0.00 | +0.00 |
| h126:S8 | 0.000 | 0.00 [0.00, 0.00] | +0.00 | +0.00 | 0.00 | +0.000 | +0.00 | +0.00 |
| h043:S0 | 0.000 | 1.00 [0.70, 1.30] | -0.50 | -0.50 | 1.00 | +0.000 | +0.00 | -1.00 |
| h043:S4 | 0.000 | 0.25 [0.15, 0.50] | -0.20 | -0.05 | 0.25 | -0.200 | -1.85 | -0.05 |
| h203:S4 | 0.000 | 0.05 [0.00, 0.12] | +0.00 | -0.05 | 0.05 | +0.050 | +1.43 | -0.00 |
| h203:S7 | 0.000 | 0.00 [0.00, 0.00] | +0.00 | +0.00 | 0.00 | +0.000 | +0.00 | +0.00 |
| h294:S0 | 0.000 | 0.72 [0.52, 0.95] | -0.50 | +0.23 | 0.72 | +0.225 | +2.09 | -0.50 |
| h294:S2 | 0.000 | 0.47 [0.30, 0.67] | +0.45 | -0.03 | 0.47 | -0.425 | -4.20 | -0.05 |

## Parameter-free check 2: Kvam-style interference, K1 vs K0 (§7.4)

- Mean Δ_K = mean |r − 50| after a choice minus after the filler: **+0.29** [-1.12, +1.65] (items: 40).
- Quantum signature (CI below 0): **False**; commitment (CI above 0): **False**.
- Mean total-probability residual: +0.58 points. A5⁰'s predicted sign of Δ_K agrees on 53% of items.

## Verdict (§7.5), as first issued on the pooled q: **TIE** (superseded)

Superseded by D52: re-issued under the same rule on the single-direction q as **CLASSICAL** (`results/exp5-verdict-reissue.md`).

## Reported alongside

- Replicability in MF (|M₂ − M₁| ≤ 5 points): 84%.
- B0 mean rating by anchor direction (after recoding): a 33.8, b 71.3.
- Median span of main-rating means across O1–O4, X1–X4, B0: 24.7 points.

| test group | items | MSE A5 | MSE F5 |
|---|---|---|---|
| right | 16 | 1102.5 | 1161.4 |
| science-chemistry | 6 | 1486.8 | 1424.6 |
| wrong | 16 | 856.1 | 931.8 |
| simpleqa | 17 | 748.6 | 815.8 |
| science-physics | 5 | 1181.9 | 1177.2 |
| claim | 4 | 715.6 | 1070.4 |

## Reading

- **Verdict: classical, re-issued (D52); first issued as a tie, now superseded.** As first issued: tie, on the pooled QQ statistic; the pre-registration (§8.6) had anticipated that A5 and F5 would be close. On the test chains the fitted quantum belief state A5 and its classical twin F5 are not distinguishable (Δ = +67 [−34, +212] rating points²). Neither parameter-free quantum signature is present.
- **Order effects are real in graded sequential ratings, unlike in yes/no form (experiments 3 and 4).**
  - 60 of 80 adjacent (S_k, M) pairs have an order effect above 0.10, with an interval excluding 0 (about 27 expected by chance; 40 survive a Holm-corrected permutation test).
  - The main-rating means span a median 24.7 points across orderings and omissions (13.2 expected from repeat noise alone).
- **The pooled QQ statistic is near zero only because the two scale directions cancel.** On the 60 pairs, the pooled mean q is +0.005 [−0.058, +0.065], but by anchor direction it is −0.345 [−0.517, −0.181] (a, 32 pairs) and +0.241 [+0.118, +0.370] (b, 47 pairs); at the pre-registered cut of 70 the pooled value is −0.157 [−0.257, −0.053]. The per-pair z values are overdispersed against N(0, 1) (KS p < 0.001). So the signature is not present. As first issued, on the pooled q, it was not contradicted (superseded). On the single scale direction (anchor a) the CI excludes 0, which §7.3 calls contradicted, and with a primary that is not a pass §7.5 then gives **classical** (D52).
- **No Kvam interference was detected.** Confidence after a mid-chain choice is not detectably different from confidence after a matched filler (Δ_K = +0.29 [−1.12, +1.65]; effects larger than about 1 point are excluded), the total-probability residual is +0.58 [−3.05, +4.15] points, and A5⁰'s predicted signs agree on 53% of items, about chance.
- **No support for the a priori prediction of where order effects should appear.** After the anchored phase solve, only 12 of 160 chain claims are off the yes/no axis. Only 3 items had pairs with distinct predicted non-commutativity, and the sub-test is 1 win to 2 losses (p = 0.875, D32).
- **Where A5 does better than F5, coherence is not the reason.** On the 8 held-out items, A5 beats F5 (+207 [+52, +388]); this is reported outside the verdict. But the dephased model D5, which is a classical Markov chain on the same states, is not detectably different from A5 there (−11 [−61, +45]) or on the test chains (+4 [−22, +31]). Removing the couplings also costs nothing significant (κ = 0: +24 [−8, +61] test; +33 [−24, +104] held-out).
  - What F5 lacks is between-question mixing: it fitted λ = 0, which gives no dynamics. D5's bit-flip dynamics are classical.
  - The classical belief-adjustment model BA5 is the best predictor of main ratings on the test chains: 827 against A5's 873, a difference of −46 [−94, +14].
- **A measurement artefact to fix before any rerun: anchor direction.** After recoding, baseline main ratings average 33.8 under anchor (a), "0 = false", and 71.3 under anchor (b), "0 = true". The model does not reliably reverse the scale. That adds variance shared by every model, so the comparisons are fair but noisier than they need be. A rerun should use one anchor direction, or check the scale explicitly.
- **Net:** the base model's sequential ratings show order effects, but nothing here needs a quantum account. A matched classical updater could not be told apart from the quantum state on the primary, a classical Markov chain is not detectably behind it (D5 − A5 test +3.8 [−21.8, +30.9]), and on one scale direction the quantum QQ signature is contradicted.

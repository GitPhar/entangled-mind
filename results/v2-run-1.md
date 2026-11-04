# Version two, run 1: learned encodings

Pre-registration: `experiments/preregistration-v2.md`. Split locked in `experiments/split-v2.json` before fitting. Train 629 items (95 wrong), validation 210 (31 wrong). Every model: 9 parameters, 1,000 train evaluations, selected on validation. The locked test set and the run-2 held-out set were each scored once.

## Fitting (train / validation AUROC of the selected candidate)

| model | train AUROC | validation AUROC | parameters |
|---|---|---|---|
| A2 learned quantum encoding | 0.819 | 0.806 | s_theta=0.451, k_sup=0.12, k_con=0.207, n_trotter=1, gamma0=0.95, beta0=0.281, alpha=0.4, tau=0.311; flag > 0.0788 |
| F2 learned classical twin | 0.816 | 0.800 | s_theta=1.01, k_sup=0.613, k_con=0.0539, n_sweeps=0, beta_t=2.49, flip=0, field=1.59, tau=0.144; flag > 9.6e-06 |
| L relation-web features (linear) | 0.796 | 0.782 | w0=0.6, w1=-0.623, w2=1.48, w3=1.02, w4=-3, w5=-0.447, w6=-2.56, w7=1.5; flag > 3 |

## locked test (32 wrong, 177 right)

| model | AUROC [95% bootstrap CI] | wrong flagged | right flagged |
|---|---|---|---|
| A2 learned quantum encoding | 0.83 [0.75, 0.90] | 17/32 | 19/177 |
| F2 learned classical twin | 0.84 [0.78, 0.89] | 25/32 | 38/177 |
| L relation-web features (linear) | 0.79 [0.70, 0.86] | 21/32 | 31/177 |
| G self-reported confidence (baseline) | 0.83 [0.78, 0.89] | — | — |
| H hedge baseline: confidence of no-lean claims | 0.67 [0.57, 0.76] | 26/32 | 95/177 |
| H-count: number of no-lean claims | 0.68 [0.59, 0.77] | 26/32 | 96/177 |

Paired bootstrap AUROC(A2) − AUROC(F2): -0.007 [-0.079, +0.062].

By group (AUROC [95% CI]):

| group | n wrong / right | A2 | F2 | L | G | H |
|---|---|---|---|---|---|---|
| type: claim | 0 / 19 | — | — | — | — | — |
| type: puzzle | 0 / 30 | — | — | — | — | — |
| type: science | 15 / 85 | 0.79 [0.68, 0.89] | 0.84 [0.75, 0.91] | 0.72 [0.59, 0.84] | 0.78 [0.68, 0.87] | 0.68 [0.52, 0.82] |
| type: simpleqa | 17 / 43 | 0.84 [0.72, 0.94] | 0.79 [0.66, 0.90] | 0.75 [0.63, 0.86] | 0.73 [0.59, 0.84] | 0.68 [0.53, 0.82] |
| contradictions >= 3 | 23 / 78 | 0.83 [0.75, 0.91] | 0.79 [0.69, 0.88] | 0.68 [0.56, 0.81] | 0.75 [0.66, 0.84] | 0.71 [0.61, 0.83] |
| contradictions < 3 | 9 / 99 | 0.82 [0.65, 0.96] | 0.86 [0.75, 0.95] | 0.91 [0.83, 0.98] | 0.90 [0.82, 0.96] | 0.57 [0.38, 0.75] |

## run-2 held-out (40 wrong, 40 right)

| model | AUROC [95% bootstrap CI] | wrong flagged | right flagged |
|---|---|---|---|
| A2 learned quantum encoding | 0.82 [0.71, 0.91] | 23/40 | 6/40 |
| F2 learned classical twin | 0.71 [0.59, 0.82] | 26/40 | 13/40 |
| L relation-web features (linear) | 0.66 [0.53, 0.77] | 21/40 | 11/40 |
| G self-reported confidence (baseline) | 0.82 [0.71, 0.90] | — | — |
| H hedge baseline: confidence of no-lean claims | 0.77 [0.66, 0.87] | 35/40 | 18/40 |
| H-count: number of no-lean claims | 0.78 [0.67, 0.87] | 35/40 | 18/40 |

Paired bootstrap AUROC(A2) − AUROC(F2): +0.108 [+0.012, +0.215].

By group (AUROC [95% CI]):

| group | n wrong / right | A2 | F2 | L | G | H |
|---|---|---|---|---|---|---|
| type: claim | 0 / 5 | — | — | — | — | — |
| type: science | 18 / 16 | 0.71 [0.53, 0.86] | 0.75 [0.57, 0.90] | 0.61 [0.40, 0.78] | 0.89 [0.76, 0.99] | 0.79 [0.64, 0.93] |
| type: simpleqa | 22 / 19 | 0.87 [0.74, 0.96] | 0.68 [0.50, 0.83] | 0.66 [0.49, 0.82] | 0.74 [0.58, 0.88] | 0.68 [0.52, 0.83] |
| contradictions >= 3 | 29 / 24 | 0.84 [0.72, 0.94] | 0.64 [0.46, 0.78] | 0.59 [0.44, 0.75] | 0.75 [0.61, 0.87] | 0.70 [0.56, 0.83] |
| contradictions < 3 | 11 / 16 | 0.77 [0.56, 0.93] | 0.81 [0.62, 0.95] | 0.75 [0.55, 0.94] | 0.93 [0.81, 1.00] | 0.87 [0.72, 0.98] |

## Primary criterion

A2's lower 95% bound 0.75 vs F2's upper 95% bound 0.89 on the locked test set: **NOT MET: the learned quantum encoding ties or loses to its classical twin**.

## Reading

- **Primary: not met. The learned quantum encoding ties its classical twin.** On the locked test set, A2 scores 0.83 [0.75, 0.90] and F2 scores 0.84 [0.78, 0.89]. The paired difference is −0.007 [−0.079, +0.062].
- **The quantum part fitted weak couplings.** A2's learned coupling scales are k_sup = 0.12 and k_con = 0.21, against 1 in v1, with a single Trotter step. Other climbed candidates with couplings from 0.06 to 1.5 reach the same train AUROC, but 8 of the 10 read out near the Z axis (|α| > 1.3), where couplings barely change the score; at the selected readout, raising the couplings to v1's strength lowers train AUROC from 0.82 to 0.61. Strong couplings hurt, and the weak fitted couplings add nothing detectable over zero (A2(κ=0) − A2 = −0.009 [−0.029, +0.009] on the locked test).
- **The classical twin also fitted toward a static model.** F2 chose n_sweeps = 0, so it scores the product of single-claim priors and uses no dynamics.
- **Deliberation structure does not detectably beat the model's self-report.** Self-reported confidence G (0.83 locked test, 0.82 held-out) is level with the best learned models. It is above L on both sets (significantly only on the held-out set, +0.161 [+0.076, +0.251]; locked test +0.043 [−0.031, +0.122]) and above H (significantly only on the locked test, +0.162 [+0.054, +0.268]).
- **Run-2 held-out set (secondary): A2 0.82 vs F2 0.71,** paired difference +0.108 [+0.012, +0.215]. A2 transfers to the hard pool better than F2. But G scores the same 0.82, and with A2's couplings near zero the gain cannot be credited to entanglement. It comes from the learned single-claim geometry and readout angle. This is a secondary comparison and does not change the primary verdict.

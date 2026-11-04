# What is the Sonnet edge? Coupling ablation and F2+ (Addendum D)

Pre-registration: `experiments/preregistration-v2.md`, Addendum D (D28), committed before any score here. No API calls were made. F2+ was fitted on the v2 train split only (selected on validation); every model is scored once per set.

F2+ fit: train AUROC 0.839, validation 0.842; s_theta=0.903, k_sup=0.909, k_con=-0.000468, n_sweeps=0, beta_t=0.891, flip=0.43, field=1.47, alpha=0.264, tau=0.149.

| model | parameters | Haiku locked v2 test (209) | Sonnet hard pool (298) |
|---|---|---|---|
| A2 (frozen v2) | 9 | 0.83 [0.75, 0.90] | 0.90 [0.84, 0.95] |
| A2(κ=0): couplings set to exactly 0 | 9 (2 pinned at 0, 7 effective) | 0.82 [0.74, 0.89] | 0.89 [0.83, 0.95] |
| F2 (frozen v2) | 9 | 0.84 [0.78, 0.89] | 0.82 [0.75, 0.88] |
| F2+: F2 with A2's tilted-readout marginal | 10 | 0.85 [0.77, 0.91] | 0.90 [0.84, 0.95] |

Paired bootstrap AUROC differences (1,000 stratified resamples; Addendum D specified 2,000, and the rule outcomes are the same at 2,000):

| difference | Haiku locked v2 test (209) | Sonnet hard pool (298) |
|---|---|---|
| A2(κ=0) − A2 | -0.009 [-0.029, +0.009] | -0.006 [-0.029, +0.013] |
| F2+ − A2 | +0.015 [-0.042, +0.073] | +0.004 [-0.032, +0.042] |
| F2+ − F2 | +0.009 [-0.057, +0.065] | +0.082 [+0.045, +0.120] |
| A2 − F2 | -0.007 [-0.079, +0.062] | +0.078 [+0.018, +0.137] |

## Rule outcome: **1: the edge is single-claim geometry, and a classical model (F2+) carries it**

## Reading

- **Pre-registered outcome 1:** the Sonnet edge is single-claim geometry, and a classical model carries it.
  - **No effect of the couplings was detected.** Setting A2's couplings to exactly 0 (a product state of tilted single-claim qubits) changes AUROC by −0.009 on Haiku's locked test set and −0.006 on Sonnet's hard pool. Both intervals contain 0.
  - **A classical twin with the same readout is not detectably different from A2.** F2+ is F2 whose prior marginal is P(yes) = (1 + sin θ cos φ cos α + cos θ sin α)/2: what an uncoupled qubit gives when measured along an axis tilted by α. No difference from A2 is detected on either set (+0.015 and +0.004, intervals containing 0). On Sonnet's items it scores 0.90, the same as A2.
- **What the geometry does.** The tilt mixes each claim's uncommitted component (cos θ, large when confidence is low) into its vote. Low-confidence claims are pushed toward one answer, which sharpens the conflict score on items whose deliberation contains weakly held claims. It is a per-claim reweighting by confidence, with no superposition across claims, no interference between them and no entanglement.
- **F2+ beats plain F2 on Sonnet's items** (+0.082 [+0.045, +0.120]), which accounts for the whole A2 − F2 gap there (+0.078). On Haiku's locked test set, the feature adds nothing detectable (+0.009 [−0.057, +0.065]), where A2 and F2 already tied.
- **Parameter counts:** A2 has 9, A2(κ=0) has 9 with 2 pinned at 0 (7 effective), F2 has 9, and F2+ has 10. F2+ has one parameter more than A2, the readout angle that A2 already had.
- **For the paper:** the Sonnet edge, the one positive quantum-vs-classical difference tested here, is accounted for by a classical model with the same per-claim readout.
  - The secondary edges on Haiku's run-2 held-out set (A2 − F2 = +0.108 in v2; A2.1 − F2.1 = +0.116 in v2.1) were **not** re-tested against F2+.
  - **Closed by Addendum E (below):** the frozen F2+ scored on that set is not detectably different from A2 (−0.019 [−0.073, +0.029]) or A2.1 (−0.037 [−0.089, +0.012]). So no quantum-vs-classical edge in error prediction survives as a significant difference against F2+: it recovers the whole Sonnet edge (1.05 [0.73, 2.50] of it) and most of Haiku's held-out edges (0.82 [0.42, 1.64] of A2's, 0.68 [0.20, 1.21] of A2.1's). All three edges are on the same hard-pool questions.

## Addendum E: the frozen F2+ on Haiku's run-2 held-out set (40 wrong, 40 right)

Pre-registered in `experiments/preregistration-v2.md`, Addendum E (`52e80a0`), before this scoring. Frozen parameters only, no refitting and no API calls.

| model | AUROC [95% CI] |
|---|---|
| A2 (frozen v2) | 0.82 [0.71, 0.91] |
| A2.1 (frozen v2.1) | 0.84 [0.74, 0.92] |
| F2 (frozen v2) | 0.71 [0.59, 0.82] |
| F2.1 (frozen v2.1) | 0.72 [0.60, 0.83] |
| F2+ (frozen, Addendum D) | 0.80 [0.69, 0.88] |

| paired difference | value [95% CI] |
|---|---|
| F2+ − A2 | -0.019 [-0.073, +0.029] |
| F2+ − A2.1 | -0.037 [-0.089, +0.012] |
| F2+ − F2 | +0.088 [+0.014, +0.167] |
| A2 − F2 (v2 edge, for reference) | +0.108 [+0.012, +0.215] |
| A2.1 − F2.1 (v2.1 edge, for reference) | +0.116 [+0.013, +0.225] |

**Rule outcome (Addendum E): 1: the held-out edges are also single-claim readout geometry, carried by a classical model.**

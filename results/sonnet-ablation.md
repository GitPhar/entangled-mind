# What is the Sonnet edge? Coupling ablation and F2+ (Addendum D)

Pre-registration: `experiments/preregistration-v2.md`, Addendum D (D28), committed before any score here. No API calls were made. F2+ was fitted on the v2 train split only (selected on validation); every model is scored once per set.

F2+ fit: train AUROC 0.839, validation 0.842; s_theta=0.903, k_sup=0.909, k_con=-0.000468, n_sweeps=0, beta_t=0.891, flip=0.43, field=1.47, alpha=0.264, tau=0.149.

| model | parameters | Haiku locked v2 test (209) | Sonnet hard pool (298) |
|---|---|---|---|
| A2 (frozen v2) | 9 | 0.83 [0.75, 0.90] | 0.90 [0.84, 0.95] |
| A2(κ=0): couplings set to exactly 0 | 9 (2 pinned at 0, 7 effective) | 0.82 [0.74, 0.89] | 0.89 [0.83, 0.95] |
| F2 (frozen v2) | 9 | 0.84 [0.78, 0.89] | 0.82 [0.75, 0.88] |
| F2+: F2 with A2's tilted-readout marginal | 10 | 0.85 [0.77, 0.91] | 0.90 [0.84, 0.95] |

Paired bootstrap AUROC differences (2,000 stratified resamples):

| difference | Haiku locked v2 test (209) | Sonnet hard pool (298) |
|---|---|---|
| A2(κ=0) − A2 | -0.009 [-0.029, +0.009] | -0.006 [-0.029, +0.013] |
| F2+ − A2 | +0.015 [-0.042, +0.073] | +0.004 [-0.032, +0.042] |
| F2+ − F2 | +0.009 [-0.057, +0.065] | +0.082 [+0.045, +0.120] |
| A2 − F2 | -0.007 [-0.079, +0.062] | +0.078 [+0.018, +0.137] |

## Rule outcome: **1: the edge is single-claim geometry, and a classical model (F2+) carries it**

## Reading

- **Pre-registered outcome 1:** the Sonnet edge is single-claim geometry, and a classical model carries it.
  - **Couplings do not matter.** Setting A2's couplings to exactly 0 (a product state of tilted single-claim qubits) changes AUROC by −0.009 on Haiku's locked test set and −0.006 on Sonnet's hard pool. Both intervals contain 0.
  - **A classical twin with the same readout matches A2.** F2+ is F2 whose prior marginal is P(yes) = (1 + sin θ cos φ cos α + cos θ sin α)/2: what an uncoupled qubit gives when measured along an axis tilted by α. It matches A2 on both sets (+0.015 and +0.004, intervals containing 0). On Sonnet's items it scores 0.90, the same as A2.
- **What the geometry does.** The tilt mixes each claim's uncommitted component (cos θ, large when confidence is low) into its vote. Low-confidence claims are pushed toward one answer, which sharpens the conflict score on items whose deliberation contains weakly held claims. It is a per-claim reweighting by confidence, with no superposition across claims, no interference between them and no entanglement.
- **F2+ beats plain F2 on Sonnet's items** (+0.082 [+0.045, +0.120]), which accounts for the whole A2 − F2 gap there (+0.078). On Haiku's locked test set, the feature adds nothing (+0.009 [−0.057, +0.065]), where A2 and F2 already tied.
- **Parameter counts:** A2 has 9, A2(κ=0) has 9 with 2 pinned at 0 (7 effective), F2 has 9, and F2+ has 10. F2+ has one parameter more than A2, the readout angle that A2 already had.
- **For the paper:** every positive quantum-vs-classical difference in this project is now accounted for by a classical model with the same per-claim readout. The quantum encoding contributes no error signal that a classical model cannot reproduce.

# Stage 2, run 2b: seven arms on the hard-pool test set

Re-scoring of Stage 2 run 2 (`results/stage2-run-2.md`) with the arms and statistics pre-registered in `experiments/preregistration.md`, Addendum A. Arms A–E and A0 are the run-2 readouts, unchanged. Base model `claude-haiku-5-5`; test set 40 wrong + 40 right; calibration 220 items. Arm G calls cost $0.0537.

| arm | threshold | calibration flag rate | wrong flagged (of 40) | right flagged (of 40) | AUROC test [95% bootstrap CI] |
|---|---|---|---|---|---|
| A  entangled, noisy sim | 0.266 | 0.25 | 10 (25%) | 9 (22%) | 0.55 [0.41, 0.67] |
| B  entangled, real hardware | not run | | | | |
| C  no entangling gates | 0.011 | 0.25 | 21 (52%) | 9 (22%) | 0.68 [0.57, 0.79] |
| D  shuffled relation web (one shuffle) | 0.152 | 0.25 | 17 (42%) | 11 (28%) | 0.65 [0.52, 0.76] |
| E  classical contradiction strength | 2.325 | 0.25 | 18 (45%) | 10 (25%) | 0.64 [0.52, 0.75] |
| F  classical Ising twin (exact enumeration) | 0.000 | 0.00 | 0 (0%) | 0 (0%) | 0.50 [0.50, 0.50] |
| G  self-reported confidence (100 − c) | 20.000 | 0.24 | 30 (75%) | 12 (30%) | 0.82 [0.71, 0.90] |
| A0 entangled, noiseless (supplementary) | 0.279 | 0.25 | 9 (22%) | 11 (28%) | 0.49 [0.36, 0.62] |

## Arm D as a null distribution

200 independent shuffles of every test item's relation web (same number of relations and the same strengths on random pairs), each run on the noisy simulator. Null AUROC mean 0.62, central 95% [0.57, 0.68]. Arm A AUROC 0.55: **p = 0.990** (share of shuffles, counted with +1 smoothing, that score at least as well as the real web).

## H2

- Original criterion (A ≥ 10% of wrong items flagged; C, D, E ≤ half of A's rate): **not met**.
- With the added controls F and G held to the same bar: **not met**.

## Reading

- **Self-reported confidence is the best error signal among the fixed arms.** Arm G, 100 minus the base model's own stated confidence, reaches AUROC **0.82** [0.71, 0.90]. That is above every fixed structural arm: the entangled readout A (0.55; G − A +0.28 [+0.10, +0.45]), the unentangled circuit C (0.68; +0.14 [+0.02, +0.27]), the shuffled web D (0.65; +0.17 [+0.02, +0.33]) and contradiction strength E (0.64; +0.18 [+0.04, +0.32]). The C and D gaps do not survive a correction for four comparisons, and this comparison was not itself pre-registered.
- **G against the deliberation-structure features (Sean's question).** The structural features do **not** detectably beat self-reported confidence.
  - Here, plain contradiction strength E scores 0.64 against G's 0.82.
  - In v2, the learned 8-feature relation-web model L scores 0.79 on the locked test set and 0.66 on this held-out set (`results/v2-run-1.md`). Paired with G, that is 0.83 and 0.82.
  - Wherever the two are compared, no model built from the structure extracted from its explanation detectably beats the model's own confidence.
- **The real relation web is worse than random ones.** Over 200 independent shuffles, a web with the same relation strengths placed on random pairs gives a mean AUROC of 0.62 [0.57, 0.68]. The real web (arm A) gives 0.55, below 99% of the shuffles (p = 0.99). Whatever error signal survives the encoding does not come from *which* claims the judge says support or contradict each other.
- **Arm F, the classical Ising twin, is degenerate as pre-registered.** Its conflict score counts strongly opposed camps among the configurations within 10% of the minimum energy. That window holds only 1–16 configurations per item (at most 6 for 284 of 300), and in none of the 300 items does it contain both camps. Every score is 0, and the AUROC is 0.50.
  - Even the 52 items with a degenerate ground state split only on claims with negligible lean, because the lean field breaks the yes/no symmetry.
  - This is reported as is; redefining F after seeing it would be post hoc. The informative classical-twin comparison is v2's learned twin F2, which tied the learned quantum encoding A2 (0.84 against 0.83 on the locked test set).
- **H2 is not met under the original controls (C, D, E), nor with F and G added.**

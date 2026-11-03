# Stage 2, run 1: five arms on the 14-item test set

Pool: `results/pool-run-2.json`.

Pre-registration: `experiments/preregistration.md`. Base model `claude-haiku-5-5` (DEVIATIONS.md, D5), noise model and hardware `ibm_fez`, 1000 shots per arm, N=2 Trotter steps. Test-set rule: fallback (D5): all 4 wrong items + the 10 correct items whose extracted claims give the model's answer the least net support. Test set: 4 items the base model got wrong, 10 it got right. Calibration pool: 111 items (0 wrong).

## Five-arm table

| arm | threshold (from calibration) | calibration flag rate | wrong items flagged (of 4) | right items flagged (of 10) | AUROC test | AUROC calibration | judgment = model's answer (of 14) | judgment = truth (of 14) |
|---|---|---|---|---|---|---|---|---|
| A  entangled, noisy sim | 0.334 | 0.25 | 2 (50%) | 7 (70%) | 0.45 | — | 12 | 10 |
| B  entangled, real hardware | not run: simulator gate not met (A does not beat every control) | | | | | | | |
| C  no entangling gates | 0.008 | 0.21 | 4 (100%) | 10 (100%) | 0.51 | — | 12 | 10 |
| D  shuffled relation web | 0.193 | 0.25 | 1 (25%) | 6 (60%) | 0.42 | — | 11 | 9 |
| E  classical contradiction strength | 2.650 | 0.25 | 1 (25%) | 0 (0%) | 0.69 | — | 13 | 11 |
| A0 entangled, noiseless (supplementary) | 0.365 | 0.25 | 1 (25%) | 4 (40%) | 0.40 | — | 12 | 10 |

Arm E's judgment column is the sign of the confidence-weighted lean, not a conflict readout.

**Caution:** under the fallback rule the right items are the correct answers whose claims gave the model's answer the *least* support, chosen because they look least certain. Every arm should flag them more often than a random correct item, so the right-item columns are biased upward and the AUROCs compare wrong items against hard right items, not typical ones. The calibration pool holds no wrong items, so calibration AUROC is undefined.

## Hypotheses

- **H1**: pass — value=0.86
- **H2**: underpowered: only 4 known-wrong items (nominally fail) — wrong_flag_rates={'A': 0.5, 'C': 1.0, 'D': 0.25, 'E': 0.25}, criterion_met=False, robust_to_one_item=True
- **H3**: falsified — auroc_A=0.45, auroc_C=0.51
- **H4**: fail (not falsified) — auroc_A=0.45, auroc_D=0.42
- **H5**: untested (simulator gate not met (A does not beat every control)) — 

## Hardware

Arm B not submitted: simulator gate not met (A does not beat every control). QPU seconds used before this decision: 0.

## Per-item conflict scores (test set)

| id | truth | model | qubits | relations | contradictions | CZ (A) | A | B | C | D | E | A0 | flagged by |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| x31 | yes | no ✗ | 9 | 7 | 2 | 52 | 0.512 | — | 0.080 | 0.164 | 0.600 | 0.444 | A, C, A0 |
| x62 | no | yes ✗ | 9 | 15 | 3 | 167 | 0.150 | — | 0.020 | 0.090 | 1.500 | 0.104 | C |
| x68 | yes | no ✗ | 9 | 27 | 13 | 323 | 0.248 | — | 0.044 | 0.150 | 7.900 | 0.254 | C, E |
| x75 | yes | no ✗ | 9 | 15 | 0 | 171 | 0.386 | — | 0.228 | 0.280 | 0.000 | 0.266 | A, C, D |
| q15 | no | no | 9 | 27 | 0 | 358 | 0.360 | — | 0.212 | 0.148 | 0.000 | 0.380 | A, C, A0 |
| q24 | yes | yes | 8 | 16 | 5 | 175 | 0.270 | — | 0.012 | 0.136 | 2.100 | 0.324 | C |
| q31 | no | no | 9 | 14 | 3 | 148 | 0.182 | — | 0.020 | 0.254 | 1.500 | 0.210 | C, D |
| q34 | no | no | 8 | 15 | 0 | 180 | 0.378 | — | 0.156 | 0.284 | 0.000 | 0.404 | A, C, D, A0 |
| x17 | no | no | 10 | 19 | 5 | 225 | 0.350 | — | 0.170 | 0.228 | 2.100 | 0.220 | A, C, D |
| x21 | no | no | 8 | 12 | 0 | 126 | 0.418 | — | 0.068 | 0.264 | 0.000 | 0.368 | A, C, D, A0 |
| x45 | no | no | 11 | 11 | 0 | 132 | 0.462 | — | 0.072 | 0.120 | 0.000 | 0.392 | A, C, A0 |
| x63 | no | no | 10 | 15 | 0 | 182 | 0.304 | — | 0.076 | 0.222 | 0.000 | 0.230 | C, D |
| x71 | no | no | 10 | 23 | 2 | 262 | 0.468 | — | 0.028 | 0.576 | 0.500 | 0.364 | A, C, D |
| x72 | no | no | 10 | 23 | 0 | 287 | 0.338 | — | 0.224 | 0.086 | 0.000 | 0.308 | A, C |

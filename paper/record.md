# Project record: October 25 to November 3, 2026

This is a chronological record of each question the project tested: its pre-registration, the test, the result, the diagnosis, and the redirect it led to.
- Hashes are short commit ids on `main`.
- Times are local (MST, UTC−7), as `git log main` records them.
- Numbers are from `results/`, and decision labels (D1–D26) are from `DEVIATIONS.md`.

**2026-10-25: proposal (version 1).** It proposed holding a language model's competing considerations as one entangled state, with five hypotheses: divergence, entanglement signal, contextuality, emergence and human-likeness. It was added to the repository as PDFs in `f09175d` (11-03 16:53).

**2026-11-03 12:54: pre-registration (`afe1c1b`).** The five hypotheses were replaced by five scorable ones:
- H1, faithful encoding;
- H2, conflict detection (the primary);
- H3, entanglement carries information;
- H4, structure carries information;
- H5, hardware survives.

The same commit documents two `reasoning_extraction` refusals of the original design. The prompts were redesigned per Anthropic's guidance, so that claims come from the visible explanation (`f37e4a8`, 12:55, D1–D3).

All remaining entries are from 2026-11-03.

| time | question | pre-registered | test (commit) | result | diagnosis | redirect |
|---|---|---|---|---|---|---|
| 14:17 | H2 on the standard pool | `afe1c1b` | Sonnet pool run 1 (`2248e54`) | 0 wrong of 117 | no errors to detect | base model changed to Haiku 5.5 (D4, D5) |
| 14:39 | H1–H4, Stage 2 run 1 | `afe1c1b` | 5 arms, standard pool (`0bc5a96`) | H1 pass (0.86); H2 underpowered (4 wrong); H3 falsified (A 0.45, C 0.51) | too few errors | 300-item hard pool (`f5649da`, 14:35, D6) |
| 15:14 | H1–H4, Stage 2 run 2 | `afe1c1b` | 80-item hard-pool test set (`3204d10`) | **H2 fails.** AUROC: A 0.55, C 0.68, D 0.65, E 0.64, A0 0.49. H3 and H4 falsified | the entangled readout does worse than every control, and noise is not the cause | arms F and G, intervals and a shuffle null (Addendum A, `dd81f4f`, 15:15, D7) |
| 16:07 | the hardware path | `afe1c1b` | Stage 1 on `ibm_fez` (`98d6ac6`) | counts returned, 2 QPU s; hardware P(yes) 0.50 vs noisy simulator 0.25 | the device is noisier than its noise model | — |
| 16:08 | are the states physically entangled? | witness design `f5f306b` (15:39) | 2-qubit tomography, 3 items (`655a8f8`) | **3/3 certified:** N = 0.147, 0.063, 0.067; 44 QPU s | the entanglement is real | — |
| 18:08 | is the phase frame right? (exploratory) | — | frame check (`ab929fe`, D15) | 20% of yes camps more than 30° off axis; the anchored-solve fix leaves AUROC unchanged | encoding defect, not the cause of the failure | the anchored solve was later adopted in experiment 5 (`8a55bb7`) |
| 18:10 | experiment 3: do quantum or classical predictions track yes/no order effects? | `de9c536` (15:39); choices `958d9db` (D13) | 2,380 conversations, $1.63 (`3241667`) | **inconclusive:** ρ difference CI [−0.284, +0.060] | the model is near-deterministic (85% of items give the same answer in all 5 runs; 27/218 pairs differ) | graded ratings |
| 18:20 | experiment 4: the Yearsley–Trueblood rules | `54cfa1f` (16:52); R2 corrected `3fe936e` (17:04, D11) | run 1, 5,480 calls, $0.23 (`bd386f3`) | 7/16 single fallacies in ratings, 0 doubles; the binary QQ phase saturated, so R2 was untestable | yes/no truth questions saturate | graded run 2 (`cb4e96e`, 19:05, D17) |
| 18:50 | v2: does a learned quantum encoding beat a matched classical twin? | split `a142d10`, models `8a4faa2` (17:20, D12) | locked test, 209 items (`49dd6f7`) | **not met:** A2 0.83 vs F2 0.84; self-report G 0.83; couplings fitted small (k = 0.12, 0.21) | error prediction does not use entanglement | v2.1 (below); sequential pivot |
| 19:27 | run 2b: arms F and G, intervals, shuffle null | `dd81f4f` (15:15) | re-scoring of run 2 (`a9ed076`) | **G 0.82 [0.71, 0.90] beats every structural arm;** the real web is below 99% of 200 shuffles (p = 0.99); F degenerate (all 0) | self-report carries the error signal; the relation web adds none | — |
| 19:32 | v2.1: does an honest-hedge encoding help? | `775042f` (17:45, D14), prompted by window note W4 (`22d3f65`, exploratory); `fe3c411` (18:36, D16) | locked test (`a531b36`) | **not met:** A2.1 0.84 vs F2.1 0.82; hedge weight fitted to 0; noisy = noiseless | the hedge distortion was not the problem | — |
| 19:36 | experiment 4 run 2: graded order test | `cb4e96e` (19:05, D17) | 1,120 calls, $0.04 (`2bac6be`) | order effects of about +0.10 on 6/7 items; R2 holds on 3/3 scored; pre-registered verdict "static twin with anchoring" | the anchoring estimator is near-tautological (D19), so the mechanism is undetermined | run 3 with a manipulated first rating (draft `9e3616e`, 20:02, not run) |
| 19:45 | does the result replicate on a second base model? | set up `c98bdf7` (19:07, D18) | Sonnet pool runs 4 and 6 | first stop at 102 items on the refusal of `h101` (`e2215bb`, D20); resumed without it (`1335301`, 19:59, D21); hard pool complete at **30 wrong of 298**, $4.07; second refusal on `t368` after 82 training items (`3d7a47e`, 20:29, D25) | two extractor refusals on SimpleQA items with Sonnet as base | halted; arms not scored |
| 20:29 | experiment 5: sequential, context-dependent judgment | draft `2dc435b` (19:19); frozen `2c2ef6c` (20:15, D22); split `2ad710c` (D23); `97dde55` (D24) | pilot, 1,400 conversations, $0.21 (`8881a0a`) | **G1 pass** (5/5 items), **G2 pass** (10/10 pairs) | the ratings move with sequence | full run; models `2251693` and analysis `1155dde` (D26) committed before any full-run result. **Result: not yet in `results/`** |

**Redirects in writing.**
- `851040f` (19:21), `paper/next-steps.md`: the pivot from error prediction to sequential judgment, with each outcome's reading fixed in advance.
- Papers: v2 `f7aa3d4` (16:55); v3 `34f5de4` (20:06), updated in `68ebdc4`, `b17f259` and `33bb00d`.

**Supporting artefacts.**
- The window display: `ddbbcea` (17:23) and the circuit strip `b707022` (18:58).
- As-run hardware circuits from IBM's job records: `91b66c4` and `74203d9` (18:44–18:45).
- IBM calibration at job time: in `e2215bb`.
- `experiments/reproduce.py`, which rebuilds every results table from the archived JSON: `bf28953` (20:11).

**Standing at the end of the record (`e39bf3c`, 20:36).**
- Error prediction: four pre-registered comparisons find no advantage for the quantum state, and the model's self-report is the best signal.
- Hardware: the states are certified entangled.
- Sequential judgment: graded order effects exist, and their mechanism is undetermined.
- Still to come: experiment 5's full run (collecting) and experiment 4 run 3 (a draft, not run).

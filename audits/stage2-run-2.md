# Audit: stage2-run-2

**Files audited:** `results/stage2-run-2.{md,json}` (300 items, raw counts per arm), `results/pool-run-3.json`, `experiments/stage2_run.py`, `src/entangled_mind/readout.py`, `experiments/preregistration.md` (H1–H5, flag rule, one-item rule), DEVIATIONS D6. Citations: README.md:62–96 ("Results"), paper/record.md:25, paper/the-entangled-mind-v3.md:39, 348–362, paper/the-entangled-mind-paper.md:16, 97–105.
**Pre-registration:** `afe1c1b` (11-03 12:54:30), `experiments/preregistration.md`; test-set rule changed by D6 (`f5649da`, 14:35:38) before any hard-pool data existed. First call: pool run 3, 14:35:39 (decoded). The simulator arms carry no IDs (git only). Result commit `3204d10` 15:14:50.
Timing verdict: OK.

## Plain-English summary of the audit
The run-2 numbers are right. I rebuilt every conflict score from the archived raw shot counts and the claims' leans, recomputed thresholds, flags and AUROCs, and matched the table exactly. Thresholds use only the 220 calibration items, which never overlap the 80 test items. H2's failure is about as robust as a result can be: arm C flags 21 of 40 wrong items, so even if arm A flagged all 40, H2 would still fail. Removing any one or any two test items never changes the ranking. What does not hold is the README's stronger wording. "Every control does better" and "contradiction-counting flags wrong answers better" are true of point estimates only: each control's advantage over A has a 95% interval that includes zero (C − A +0.14 [−0.01, +0.29], D − A +0.11 [−0.03, +0.24], E − A +0.10 [−0.07, +0.26]). What the intervals do support is that A is *not* better than any control. Each interval's upper end lies below the +0.10 margin H3 and H4 required. One more fact belongs next to these numbers: a trivial predictor, "the model answered no", scores 0.675 on this test set, level with arms C, D and E.

## Claims checked
| # | claim (quoted or paraphrased, with file:line) | recomputed / evidence | status |
|---|---|---|---|
| 1 | Split: 40 wrong + 40 right by D6 rule, seed 2026; calibration 220 (4 wrong) (stage2-run-2.md:5) | D6 text re-implemented reproduces both lists; calibration ∩ test = ∅; calibration wrong = h152, h159, h190, h299 | holds |
| 2 | Conflict scores per arm (per-item table) | Recomputed from raw counts + |lean| weights (my code): exact match for all 300 items × A, C, D, A0, and E from the pairs table. With exact arithmetic at the m = ±1/3 boundary, 13 items shift by ≤ 0.03 because the authors' float comparison drops some votes that equal exactly 1/3. That moves C's AUROC 0.683 → 0.686 and A0's 0.485 → 0.481, with no verdict change | holds (minor) |
| 3 | Thresholds = 75th percentile of each arm's calibration scores; calibration flag rate 0.25 (table) | `np.quantile(cal, 0.75)` gives 0.266 / 0.0105 / 0.152 / 2.325 / 0.279, and 55 of 220 are flagged for every arm. Under the other quantile conventions (lower, higher, nearest, midpoint), test flag counts change by at most 1 | holds |
| 4 | Flags: A 10/9, C 21/9, D 17/11, E 18/10, A0 9/11 (wrong/right) | identical | holds |
| 5 | AUROC test: A 0.545, C 0.683, D 0.651, E 0.642, A0 0.485 | identical (Mann–Whitney, ties ½) | holds |
| 6 | H1 pass, 80/80 (stage2-run-2.md:22) | 80/80; README:90 correctly calls it trivial | holds |
| 7 | H2 fail, "robust_to_one_item" (stage2-run-2.md:23) | A = 10/40 needs every control ≤ 5. C = 21 > 20, so H2 fails even at A = 40/40. Every leave-one-out set also fails | holds |
| 8 | H3 falsified (C ≥ A), H4 falsified (D ≥ A) (stage2-run-2.md:24–25) | Rule met by point estimate. Leave-one-out: C − A stays in [+0.121, +0.161] and D − A in [+0.088, +0.128], so both verdicts survive every single drop | holds |
| 9 | "the result does not hinge on any single item" (README.md:83) | Leave-one-out over all 80 items: AUROC ranges A [0.534, 0.559], C [0.678, 0.701], D [0.642, 0.667], E [0.633, 0.657]. Over all 3,160 leave-two-out sets, C, D and E stay above A every time | holds |
| 10 | "barely better than chance (AUROC 0.55)" (README.md:83) | 0.545 [0.414, 0.672] (10k stratified bootstrap); the interval includes 0.5. Wrong-flag minus right-flag rate +0.025 [−0.15, +0.20] | holds (minor): "indistinguishable from chance" is exact |
| 11 | "Every control does better" (README.md:83) | Paired stratified bootstrap (10k, same resamples for both arms): C − A +0.138 [−0.014, +0.294]; D − A +0.106 [−0.029, +0.237]; E − A +0.097 [−0.073, +0.264]. DeLong p = 0.075, 0.116, 0.257. All three point estimates are positive, and none excludes 0. The intervals do exclude the +0.10 that A was required to beat each control by | overclaim |
| 12 | "Plain contradiction-counting (arm E) flags wrong answers better than the entangled quantum state" (README.md:88) | E flags 18/40 wrong vs A 10/40, but McNemar on the 18 discordant wrong items gives p = 0.096. Right items 10 vs 9. AUROC E − A +0.10 [−0.07, +0.26]. "At least as well" is supported; "better" is not | overclaim |
| 13 | "so in this design the quantum state carries no error signal beyond what is already in the relation table" (README.md:88) | This is the pre-registered reading when E ≥ A ("the README must say so"). A's own AUROC interval includes 0.5. As an absence claim it is "no detectable signal" | holds |
| 14 | "If anything, the entangling step destroys signal that the unentangled circuit keeps." (README.md:88) | It is a controlled ablation (same circuit minus two-qubit terms), so causal language about the *circuit* is legitimate. Noisy sim: C − A +0.138 [−0.014, +0.294], one-sided P 0.036. Exact noiseless scores (frame-fix-check.json): C − A0 +0.195 [+0.018, +0.365]. "Entangling step" here means both the RZZ prep and the XX evolution terms, since C removes both | holds (minor), hedged and borderline on the noisy arms |
| 15 | "the entangled readout does worse than every control, and noise is not the cause" (record.md:25) | "Worse than every control" is point estimates only (row 11). "Noise is not the cause": A0 (noiseless) 0.485 ≤ A 0.545; in fact A − A0 = +0.060 [+0.005, +0.114], so noise slightly *helps* | overclaim (first half) |
| 16 | "That is worse than the same circuit without entangling gates (0.68) and worse than a plain contradiction count (0.64)." (paper.md:16) | same as rows 11–12 | overclaim |
| 17 | H5 untested; gate not met; QPU 0 s before decision | gate requires A > each control on wrong-flag rate: 10 < 17, 18, 21 | holds |
| 18 | Confound check (not in the file) | Wrong items: 36/40 answered "no"; right items: 22/40. "Model answered no" alone gives AUROC 0.675, which is ≥ D (0.651) and E (0.642) and ≈ C (0.683). Within the 58 "no" answers (36 wrong / 22 right): A 0.496, C 0.735, D 0.634, E 0.629, G 0.871. The structural arms keep their signal there, so they are not *only* answer direction, but a one-bit baseline matches them on the full set | not in file (finding) |

## Holes found
1. **Point-estimate superiority is presented as fact.** "Every control does better" and "E flags wrong answers better" (README:83, 88), "does worse than every control" (record:25) and "worse than … a plain contradiction count" (paper:16) all rest on point estimates whose paired 95% intervals include zero. The pre-registered conclusion, that A does not beat the controls (H2 fails, H3 and H4 falsified), is robust. The reverse claim, that the controls beat A, is not established.
2. **A trivial baseline ties the structural arms.** "The model answered no" scores 0.675 because the wrong items are 90% "no" answers against 55% of right items. Any reading of C, D or E as an "error signal" should be set against that one-bit baseline. Inside the "no" stratum C keeps 0.735, so the controls are not empty. But on the pooled test set their advantage over a constant-per-answer flag is nil.
3. **Boundary handling in the readout is decided by floating-point rounding.** Votes landing exactly on m = ±1/3 (weights that are multiples of 0.1) are counted or not depending on float rounding. It is harmless here (≤ 0.004 AUROC), but it is not the pre-registered "P(m ≥ 1/3)" in exact arithmetic.
4. **Noise improves A over A0** (+0.060 [+0.005, +0.114]). That is consistent with the README's "noise is not the cause", but it is never reported. It suggests that whatever signal A has comes from noise pushing the state toward C-like single-qubit statistics.

## Overclaims to cut (exact sentences)
- `README.md:83` — "Every control does better:" — point estimates only; no paired interval excludes 0 — replace with "Every control scores higher on point estimate, though no single difference is significant (C − A +0.14 [−0.01, +0.29], D − A +0.11 [−0.03, +0.24], E − A +0.10 [−0.07, +0.26]); each interval rules out the +0.10 margin A needed:"
- `README.md:88` — "**Plain contradiction-counting (arm E) flags wrong answers better than the entangled quantum state, so in this design the quantum state carries no error signal beyond what is already in the relation table. If anything, the entangling step destroys signal that the unentangled circuit keeps.**" — the first clause is an overclaim (McNemar p = 0.10; AUROC difference CI includes 0) — replace with "**Plain contradiction-counting (arm E) flags wrong answers at least as well as the entangled quantum state (18/40 vs 10/40; AUROC 0.64 vs 0.55, difference +0.10 [−0.07, +0.26]), so in this design the quantum state carries no error signal beyond what is already in the relation table. If anything, the entangling step lowers the signal the unentangled circuit keeps (C − A +0.14 [−0.01, +0.29] on the noisy simulator; +0.20 [+0.02, +0.37] on exact noiseless scores).**"
- `paper/record.md:25` (cell) — "the entangled readout does worse than every control, and noise is not the cause" — replace with "the entangled readout does no better than any control (all three score higher on point estimate), and noise is not the cause".
- `paper/the-entangled-mind-paper.md:16` — "That is worse than the same circuit without entangling gates (0.68) and worse than a plain contradiction count (0.64)." — replace with "That is below the same circuit without entangling gates (0.68; difference +0.14 [−0.01, +0.29]) and a plain contradiction count (0.64; +0.10 [−0.07, +0.26]), and the data rule out the pre-registered +0.10 advantage over either."

## Does the verdict stand?
Pre-registered: H1 pass, H2 fail, H3 falsified, H4 falsified, H5 untested. **STANDS.** Every number recomputes from raw counts. H2 fails by a margin that no single item or pair of items can change, and the intervals exclude the margins H3 and H4 required. The caveats are about wording: the controls' superiority over A, and their standing as an error signal against a one-bit "answered no" baseline.

## Confidence
High. All scores, thresholds, flags, AUROCs, leave-one-out and paired intervals were recomputed independently from the raw shot counts and claim tables.

## Tally
claims_checked: 18
claims_failed: 4
overclaim_sentences: 4
verdict: STANDS
confidence: high

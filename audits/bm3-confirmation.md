# Audit: bm3-confirmation

**Files audited:** `results/bm3-confirmation.md`, `results/bm3-confirmation.json`, `results/exp4-run-3-calls.json`, `experiments/bm3-confirmation.md`, `experiments/bm_offline.py` (`bm3`), `experiments/exp4_run3.py` (the earlier run-3 analysis), DEVIATIONS D40; citations in `paper/morning-brief.md`.
**Pre-registration:** `9c29a94` (05:08:07), text in `experiments/bm3-confirmation.md` §§2–4. The analysis code for bm3, bm7 and bm9 (`experiments/bm_offline.py`, 240 lines) was frozen in this same commit and never changed. First call: none, archival (`exp4-run-3-calls.json`, calls 11-03 23:01–23:16). Result `a33ab1e` 05:08:23, 16 s after the pre-registration.
Timing verdict: PROBLEM (unverifiable). The archive had already been opened and analysed for run 3. `exp4_run3.py` computed `mean_revision_toward_own` = mean (r₁ − A)/(own − A), which is 1 − u, per item-order. The result commit, 16 s after the pre-registration, already contains about 250 words of hand-written plain-English prose quoting the CIs. So the analysis must have been run before, or within seconds of, the "frozen" commit. "Committed before the archive was opened for this analysis" cannot be verified. What the commit does protect is the code: the statistic, coding, exclusions and seed were fixed and are what produced the table.

## Plain-English summary of the audit
The pre-registered numbers reproduce exactly: 2,080 conversations in 30 item-orders (320 + 160 dropped), β₁ −0.179 [−0.832, +0.280], β₃ +0.698 [−0.812, +2.534], and 13 identifying item-orders. The pre-registered reading "no asymmetry" stands. The highlighted secondary finding does not: "consistent estimates accepted less (−0.29 [−0.79, −0.03])". It is one of 15 coefficients reported. It disappears without the covariates (accept ~ code alone: −0.016 [−0.20, +0.13]). It rests on a single item-order: co05 X accepts all 40 inconsistent anchors and none of the 40 consistent ones. Drop it and the effect becomes −0.18 [−0.48, +0.02]. Eight of the 13 identifying item-orders have 0% accepts under both codes. The plain-English line "Haiku simply doesn't treat someone else's number as its own commitment" was written before bm1 had collected any "own" data, and bm3 does not test own numbers at all.

## Claims checked
| # | claim (quoted or paraphrased, with file:line) | recomputed / evidence | status |
|---|---|---|---|
| 1 | 2,080 conversations, 30 item-orders, dropped 320 and 160 (md:3) | Exact | holds |
| 2 | β₁ −0.18 [−0.83, +0.28], "not reliable either way" (md:11, :28) | −0.179 [−0.832, +0.280] | holds |
| 3 | Mean uptake −0.03 (consistent) against +0.21 (inconsistent); accept 9.7% against 11.3% (md:10, :35-36) | −0.031 / +0.211; 9.7% / 11.3% | holds |
| 4 | "The model *accepted* agreeing estimates less often, and that difference is reliable: −0.29 [−0.79, −0.03]" (md:12) | −0.294 [−0.794, −0.030]; with an alternative seed [−0.76, −0.03]. Raw accept rates differ by only 1.6 points; accept ~ code alone gives −0.016 [−0.195, +0.133]; without co05 X, −0.18 [−0.48, +0.02]. One secondary coefficient out of 15 | overclaim |
| 5 | β₃ +0.70 [−0.81, +2.53] (md:13) | Exact | holds |
| 6 | 13 of 30 item-orders identify β₁ (md:18, :23) | 13 | holds |
| 7 | "The direction, if any, matches Kumaran et al.'s LLMs, which over-weight *opposing* advice." (md:15) | Hedged with "if any"; β₁'s CI includes 0 | holds (minor) |
| 8 | "Haiku simply doesn't treat someone else's number as its own commitment." (md:15) | Not tested here (no own condition); written at 05:08, before bm1's first call (05:11:44) | overclaim |
| 9 | morning-brief.md:68 "It *accepts* agreeing estimates less often." | As #4 | overclaim |
| 10 | morning-brief.md:68 "No confirmation bias toward another person's number" | β₁ CI [−0.83, +0.28] is wide, and only 13 item-orders identify it; "not detected" is the supported form. The result md itself calls the test "weak by design" | holds (minor) |
| 11 | Commit `a33ab1e` headline "consistent estimates accepted less (−0.29 [−0.79, −0.03])" | A secondary pulled into the headline | overclaim (process) |

## Holes found
1. **The reported "reliable" acceptance effect comes from one item-order and the covariates.** Accept is 0/40 consistent against 40/40 inconsistent on co05 X. That item-order drives the coefficient: without it, −0.18 [−0.48, +0.02], and leaving any one item out gives −0.42 to −0.19. With no covariates the effect is −0.016 [−0.20, +0.13]. Of the 13 identifying item-orders, 8 have zero accepts under both codes.
2. **Selection among many tests.** The run reports 15 coefficient CIs (5 terms × 3 regressions) plus 2 descriptive rows. Only the pre-registered β₁ and β₃ decide the reading. The one secondary CI that excludes 0 (accept β₁, z ≈ 1.5 by bootstrap SE, percentile CI just excluding 0) was put into the commit headline and the morning brief. The revision-1 β₀ and β₄ CIs also exclude 0 and are not mentioned. With 15 coefficients at α = 0.05, about 0.75 false positives are expected.
3. **Timing.** The analysis code and the result are 16 s apart, with hand-written prose. The run-3 analysis had already computed 1 − u per item-order (`exp4_run3.py`, `mean_revision_toward_own`). The "before the archive was opened for this analysis" claim is not checkable. Only the code freeze is.
4. **A cross-test claim made before that test's data existed.** md:15's "own commitment" sentence anticipates bm1.

## Overclaims to cut (exact sentences)
- `results/bm3-confirmation.md:12` — "- **Acceptance.** The model *accepted* agreeing estimates less often, and that difference is reliable: −0.29 [−0.79, −0.03] in accept probability." — rests on one item-order (co05 X) and on the covariates; raw rates are 9.7% against 11.3% — replace with: "- **Acceptance.** Raw accept rates are 9.7% (agreeing) against 11.3%. With covariates the coefficient is −0.29 [−0.79, −0.03], but it rests on one item-order (co05 X; without it −0.18 [−0.48, +0.02]), and it is one of 15 secondary coefficients."
- `results/bm3-confirmation.md:15` — "Haiku simply doesn't treat someone else's number as its own commitment." — not tested by bm3; written before bm1 ran — cut.
- `paper/morning-brief.md:68` — "It *accepts* agreeing estimates less often." — replace with: "Accept rates hardly differ (9.7% against 11.3%)."

## Does the verdict stand?
Pre-registered reading: **no asymmetry**. **STANDS.** β₁ and β₃ both have CIs containing 0, and only 13 of 30 item-orders identify β₁, so this is a low-power "not detected" (as the md's own caveat says). The headline secondary ("accepted less, reliable") does not survive and should be cut.

## Confidence
High. All three regressions and the by-code table were recomputed from `exp4-run-3-calls.json` with my own code, and I ran item-order and item leave-outs. The timing judgement rests on commit times and the prose present in `a33ab1e`.

## Tally
claims_checked: 11
claims_failed: 4
overclaim_sentences: 3
verdict: STANDS
confidence: high

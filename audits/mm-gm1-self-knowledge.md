# Audit: mm-gm1-self-knowledge

**Files audited:** `results/mm-gm1-self-knowledge.{md,json}`, `results/mm-gm1-calls.json`, `results/mm-batches-gm1-{base,judge}.json`, `results/gm1-calls.json` (archived SS cell), `results/pool-run-4.json` (Sonnet authors, gold), `experiments/mm-gm1-self-knowledge.md`, `experiments/mm_gm1.py`, `experiments/gm1_self_knowledge.py`, DEVIATIONS DM3; citing text in `results/multi-model.md`, `paper/no-credence-to-read.md`, `paper/morning-brief.md`, DEVIATIONS D48.
**Pre-registration:** `207c9b6` (07:47:58), text in `experiments/mm-gm1-self-knowledge.md` and DEVIATIONS DM3. First call (decoded from `msg_01…` IDs with `scratchpad/g8/msgtime.py`): Opus base answers at **07:49:06–07:49:07**, judge cells at 07:51:31–07:59:06. Result commit `ba9f99c` 08:01:32. `mm_gm1.py` and the imported `gm1_self_knowledge.py` are unchanged between the pre-registration and the result.
Timing verdict: **OK by git and message IDs.** There is a documentation PROBLEM: DM3's "Date: 08:05 MST, before any call for this test" is false as written. Every call for this test ran between 07:49 and 07:59, and the entry itself was committed at 07:47:58.

## Plain-English summary of the audit
I recomputed every number from the raw answers and ratings, including my own parse of Opus's FINAL ANSWER lines; there were 0 disagreements with the archive. The cells, the interaction I = −0.045 and its interval all reproduce, and so do the disagreement-subset numbers. The pre-registered reading is *no self-advantage*. On all 298 questions the interval's upper end (+0.017) rules out more than a small authorship benefit, so the null is informative there. The pre-registered self-advantage criterion, however, depends on the 21-question disagreement subset, and that subset contains only 4 Opus errors. Its interval of [−0.30, +0.81] could not have confirmed or excluded anything, and the point estimate there is positive (+0.18). "No privileged self-knowledge holds on all three models" should therefore read as "no self-advantage detected in either pair". The claim that self-report "is text-reading" on all three models is a mechanism claim that a behavioural null cannot carry.

## Claims checked
| # | claim (quoted or paraphrased, with file:line) | recomputed / evidence | status |
|---|---|---|---|
| 1 | Accuracy: Sonnet 89.9% (30 wrong), Opus 94.3% (17 wrong) on 298 | 0.8993 / 0.9430; 30 / 17. My own regex parse of Opus FINAL ANSWER agrees on all 298 | holds |
| 2 | Cells (all 298): SS 0.903, OS 0.959, OO 0.904, SO 0.893 | 0.903, 0.959, 0.904, 0.893 (Mann–Whitney, ties half) | holds |
| 3 | I = −0.045 [−0.107, +0.017] | −0.0454. My bootstrap (4,000 question resamples): [−0.114, +0.017]; P(I > 0) = 0.07. Leave-one-question-out shifts are at most 0.017 | holds |
| 4 | Disagreement subset (21): +0.184 [−0.296, +0.812] | +0.184; my CI [−0.30, +0.85]. **17 Sonnet-wrong vs 4 Opus-wrong**; 58 of 4,000 resamples undefined (no errors) and dropped | holds (numbers) |
| 5 | Δ_S = −0.056 [−0.089, −0.025]; Δ_O = +0.011 [−0.056, +0.072] | −0.056 [−0.091, −0.024]; +0.011 [−0.054, +0.070] | holds |
| 6 | Pre-registered reading *no self-advantage* (D36 rule) | I_all < 0, so *self-advantage* fails. Disagreement CI upper +0.81 > 0, so *other-advantage* fails. The result falls to the default. Rule applied as frozen | holds |
| 7 | "Opus spots Sonnet's mistakes better than Sonnet does: AUROC 0.96 against 0.90" (`results/multi-model.md:14`) | Δ_S CI excludes 0 | holds |
| 8 | "On Opus's own answers, being the author adds almost nothing: Opus reaches 0.90, Sonnet reading the same answers 0.89" (`results/multi-model.md:15`) | +0.011 [−0.056, +0.072]: not detected, but up to +0.07 is allowed | holds (minor) |
| 9 | "That is the same sign and size as for Haiku and Sonnet (−0.055)" (`results/multi-model.md:16`) | Point estimates are similar, but Haiku × Sonnet's CI excluded 0 and this one does not | holds (minor) |
| 10 | "No privileged self-knowledge holds on all three models" (`paper/no-credence-to-read.md:27`, `:311`; `paper/morning-brief.md:112`; D48) | Two pairs tested. The deconfounded criterion (disagreement subset) has 4 Opus errors and a CI 1.1 wide, so the reading is a non-detection | overclaim |
| 11 | "On this test, and on all three models, self-reported confidence is text-reading" (`paper/no-credence-to-read.md:386`) | A behavioural null on the judge × author interaction cannot establish a mechanism | overclaim |
| 12 | Costs $4.03 of $4.60, 1,192 calls, no refusal, no max_tokens | $4.030, 1,192 | holds |
| 13 | Pre-registered before any call (`results/mm-gm1-self-knowledge.md:3`) | 07:47:58 commit < 07:49:06 first message | holds |

## Holes found
1. **The confirmatory arm had no power, so "no self-advantage" is a default, not a finding.** D36's rule needs the disagreement-subset CI above 0 to declare a self-advantage. That subset has 21 questions with only 4 Opus errors, so the OO and SO cells on it are AUROCs over 4 positives. Its CI spans 1.1 AUROC units, and its point estimate is +0.18, the self-advantage direction. No plausible effect could have produced the pre-registered self-advantage reading at this n. The all-298 interval does bound the raw interaction above at +0.017, which is real information. That statistic, however, is the one the prereg's §5 says is confounded with judge skill × author difficulty.
2. **The bootstrap conditions on defined resamples.** `g1.boot` drops resamples in which a cell has no errors (58 of 4,000 in my run on the disagreement subset), so its CI is mildly anti-conservative there. This is minor next to hole 1.
3. **The cells were not collected together.** SS was gathered about 5 hours earlier, for D36; SO, OS and OO are new batch calls. The prereg discloses this. Model id, prompt and settings match, so I do not count it as a problem beyond noting it.
4. **The DEVIATIONS time stamp is wrong.** DM3 says "08:05 MST, before any call for this test", but the calls ran 07:49:06–07:59:06. The commit (07:47:58) is what makes the claim true.
5. **The pilot touched a test question.** The pilot used h002, which is one of the 298 questions. The Opus pilot answer is not used, and the base batch answer is separate. This has negligible effect.

## Overclaims to cut (exact sentences)
- `paper/no-credence-to-read.md:27` — "- **No privileged self-knowledge holds on all three models.** With Sonnet and Opus judging each other's answers, the judge × author interaction is −0.045 [−0.107, +0.017], again *no self-advantage*." — Why: this is a non-detection, and the deconfounded criterion was unpowered (4 Opus errors on the disagreement subset; CI [−0.30, +0.81]). — Replace: "- **No self-advantage was detected in either pair (Haiku × Sonnet, Sonnet × Opus).** With Sonnet and Opus judging each other's answers, the judge × author interaction is −0.045 [−0.107, +0.017]; the disagreement subset (21 questions, 4 Opus errors) is uninformative."
- `paper/no-credence-to-read.md:311` — "**No privileged self-knowledge holds on all three models.**" — Why: same as above. — Replace: "**No self-advantage was detected on any of the three models.**"
- `paper/no-credence-to-read.md:379` — "The absence of a self-advantage holds on all three models (Section 4.6)." — Why: same as above. — Replace: "No self-advantage was detected on any of the three models (Section 4.6)."
- `paper/no-credence-to-read.md:386` — "On this test, and on all three models, self-reported confidence is text-reading." — Why: this is a mechanism claim from a behavioural null. — Replace: "On this test, and on all three models, self-reported confidence showed no advantage over a capable reader of the same answer."
- `paper/morning-brief.md:112` — "- **No privileged self-knowledge holds on all three models.** Opus spots Sonnet's errors better than Sonnet does (0.96 against 0.90). The judge × author interaction is −0.045 [−0.107, +0.017]." — Why: same as the first entry. — Replace: "- **No self-advantage was detected on any of the three models.** Opus spots Sonnet's errors better than Sonnet does (0.96 against 0.90). The judge × author interaction is −0.045 [−0.107, +0.017]."

## Does the verdict stand?
Pre-registered reading: *no self-advantage*. **STANDS WITH CAVEATS.** The numbers reproduce exactly and the rule was applied as frozen. The reading is a fall-through default, because the confirmatory subset had no power (4 Opus errors). The all-question interval does exclude an interaction above +0.017.

## Confidence
**High.** Every cell, CI and count was recomputed from the raw archive with my own AUROC, bootstrap and answer parse.

## Tally
claims_checked: 13
claims_failed: 2
overclaim_sentences: 5
verdict: STANDS WITH CAVEATS
confidence: high

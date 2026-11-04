# Audit: pool-runs

**Files audited:** `results/pool-run-1.{md,json}` … `results/pool-run-5.{md,json}`, `results/pool-run-6.json` (no `.md` is written for run 6, by design: `reproduce.py` "halted on a refusal (D25); no table written"); `experiments/run_pool.py` (`split`, `answer_support`, `process`); `experiments/preregistration.md` (Data section); DEVIATIONS D4, D5, D6, D9/D9b, D18, D20–D21, D25; citations in README.md (D4–D6 list), paper/the-entangled-mind-v3.md Table (lines 149–153).
**Pre-registration:** `afe1c1b` (11-03 12:54:30), `experiments/preregistration.md` §Data (10 wrong + 10 right, seed 2026). Amended by D4 + D5 (`2248e54`, 14:17:24) and D6 (`f5649da`, 14:35:38). First calls (decoded request IDs): run 1 12:56:06 (q-items) / 13:27:04 (first extension item x01) – 14:13:48; run 2 14:16:17 – 14:28:09; run 3 14:35:39 – 14:55:51; run 4 19:37:08 – 20:13:55; run 5 16:02:45 – 17:19:53; run 6 20:14:19 – 20:20:01.
Timing verdict: PROBLEM (minor, no consequence for any hypothesis). (a) All 67 pool-run-1 extension calls (13:27:04–14:13:48) ran before the extension items, `make_extension.py` and the D4 stop rules ("fixed in advance", "before any extension item completed") were committed at 14:17:24. (b) Pool run 2 started 67 s before D5 (and its fallback rule) was committed. (c) D6 was committed 1 s before run 3's first call: OK. (d) Run 5 began 23 min before D9/D9b (`930730c`, 16:26:03), already noted by the lead auditor. None of these rules touches circuit results, which did not exist yet.

## Plain-English summary of the audit
The bookkeeping of the six pool runs is correct. I recounted every run from the raw records: items processed, exclusions, wrong answers, and the FINAL ANSWER parse all match the tables exactly (0/117, 4/125, 44/300, 30/298, 158/1,048, 7/82). Re-implementing the split rules from their text (D5 fallback, D6 "all wrong up to 40 + as many right, seed 2026") reproduces the archived test sets item for item, and calibration and test never overlap. The base-model switch (D5) and the harder pool (D6) were made because there were too few errors, before any circuit ran, so they cannot have favoured a hypothesis. Two things are wrong in the record. The Sonnet hard-pool exclusion (h018) is described as a token-cap hit in DEVIATIONS D25 and the v3 paper; it was an extractor returning one claim, on an answer Sonnet got right. And the D4 extension rules were written into git only after every extension call had run.

## Claims checked
| # | claim (quoted or paraphrased, with file:line) | recomputed / evidence | status |
|---|---|---|---|
| 1 | Run 1: 127 processed, 10 token-cap exclusions, 0 wrong of 117 (pool-run-1.md:3; D5) | 127 records; 10 `truncated`; 117 answered; 0 `correct is False`; 60 q + 57 x answered, 67 x attempted, 8 never started (75 − 67) | holds |
| 2 | Run 2: 125 processed (135 − 10 capped), 4 wrong; fallback test 4 + 10 least-support right, calibration 111 (pool-run-2.md:3–5) | 125 records, 0 excluded, 4 wrong (x31, x62, x68, x75). My `support` re-implementation picks the same 10 right items (support 0.018–0.372; 11th is 0.375); calibration 111, overlap 0 | holds |
| 3 | Run 3: 300 answered, 44 wrong; D6 split 40 + 40, calibration 220 (pool-run-3.md:3–5) | 44 wrong; `random.Random(2026).sample` per D6 text reproduces `test_wrong`/`test_right` exactly; the 4 surplus wrong (h152, h159, h190, h299) are in calibration; calibration ∩ test = ∅ | holds |
| 4 | Run 4: 299 processed, "1 hit the 16,000-token cap or gave no FINAL ANSWER", 30 wrong of 298 (pool-run-4.md:3); "1 hit the token cap" (DEVIATIONS.md:376; v3:153) | The one exclusion, h018, has `excluded_reason: "extractor returned 1 claims"`, `model_answer: yes` = truth (a correct answer dropped). No record is truncated. The md header is a generic template; D25 and v3 copy it as a token-cap hit | wrong (minor) |
| 5 | Run 4 split 30 + 30, calibration 238 | reproduced exactly with seed 2026 | holds |
| 6 | Run 5: 1,048 processed, 0 excluded, 158 wrong (pool-run-5.md:3) | 1,048 records, 0 excluded, 158 wrong; split "none" (locked separately) | holds |
| 7 | D9b: "an item whose explanation yields fewer than 5 claims after one retry is now recorded as excluded … This happened once." | Run 5 contains no excluded record and the minimum claim count is 6. The crashed item was therefore re-processed with fresh calls after the fix and kept. Which item cannot be identified (only base request IDs are archived). In effect this is one retry, against the "excluded, not retried" rule | not checkable (minor hole) |
| 8 | Run 6: 82 records, halted on refusal t368 (D25); no table | 82 records, 7 wrong; last call 20:20:01, one second before the decoded refusal time 20:20:02 | holds |
| 9 | Refusal handling: h101 dropped from run 4, never reworded (D20–D21) | h101 absent from run 4 records; listed in `REFUSAL_EXCLUDED` | holds |
| 10 | `correct` flags and model answers | For all 1,971 answered records, `correct == (model_answer == answer)` and the last `FINAL ANSWER:` line in the visible answer equals `model_answer` (0 disagreements, 0 conflicting lines) | holds |
| 11 | D4: rules "fixed in advance" / addendum "before any extension item completed" | The extension pool, its generator and the D4 text first appear in `2248e54` (14:17:24), after the last extension call (14:13:48). Not verifiable from git; the 13-wrong stop never triggered (0 wrong); run 1 was stopped by hand, not by the rule (D5 says so) | not checkable |
| 12 | D5: base model switched to Haiku "before any circuit was run" | Stage 2 run 1 is the first circuit result (`0bc5a96`, 14:39). The switch was decided on the base model's error count alone, not on any circuit output, so it cannot select for H1–H5 | holds |
| 13 | D6: hard pool added "before any hard-pool result existed" | D6 committed 14:35:38; first run-3 call 14:35:39 | holds |
| 14 | README D3/D5: "Sonnet answered all 117 checkable items correctly … Haiku still got only 4 of 125" (README.md:214) | 0/117 and 4/125 confirmed | holds |
| 15 | README D6: "Haiku got 44 wrong, which gives Stage 2 run 2 a 40-wrong / 40-right test set" (README.md:220) | confirmed | holds |

## Holes found
1. **The h018 exclusion is misdescribed** (DEVIATIONS.md:376, v3:153, pool-run-4.md:3). It was not a token-cap hit. The extractor returned 1 claim on a *correct* Sonnet answer, and the item was dropped under D9b's fewer-than-5-claims rule. The consequence is small: it removes one right item from Sonnet's calibration pool, and no wrong item.
2. **D4's "fixed in advance" rules are not in git before the calls they govern.** All 67 extension calls in run 1 precede `2248e54`. The rules (shuffled order, cap exclusions, stop at 13 wrong or $8.50) only shape which items exist, and run 1 produced no wrong items. So the impact is nil, but "fixed in advance" rests on the author's word alone.
3. **D9b's single crash was handled by a silent re-run.** Run 5 has no excluded item. Low impact (1 of 1,048 items).
4. **The test sets are unbalanced by item type and answer direction.** This follows from the rule, not a violation of it. Run 3's 40 wrong items are 36 "no" answers and 0 author-written claims. The 40 right items are 22 "no" and include 5 claims (Haiku got 0 of 60 claims wrong). A one-bit predictor, "the model answered no", scores AUROC 0.675 on this test set, as high as arms C, D and E (see `audits/stage2-run-2.md`). This is a property of the pool, and later analyses should report it.
5. **Cosmetic:** pool-run-5.md labels every row `calib` although its split is "none" and it says "Calibration pool: 0 items".

## Overclaims to cut (exact sentences)
- `DEVIATIONS.md:376` — "- **Pool run 4** (hard pool, `h101` excluded) completed: 299 items processed, 1 hit the token cap, and **30 were wrong**. Cost $4.07." — wrong exclusion reason — replace "1 hit the token cap" with "1 (h018, answered correctly) was excluded because the extractor returned 1 claim".
- `paper/the-entangled-mind-v3.md:153` — "**30** of 298 answered (299 processed, `h101` excluded after a refusal, D20–D21; 1 hit the token cap)" — same error — replace "1 hit the token cap" with "1, h018, excluded when the extractor returned a single claim".

## Does the verdict stand?
These runs have no verdict of their own. Their counts and splits **STAND**: every number recomputes, and the test/calibration splits follow their written rules exactly with no leakage. The timing and record-keeping defects above are minor and do not touch any hypothesis test.

## Confidence
High. I recomputed every count, parse and split from the raw records. Only the D4 "before" claim and the D9b re-run cannot be resolved from the archive.

## Tally
claims_checked: 15
claims_failed: 1
overclaim_sentences: 2
verdict: STANDS
confidence: high

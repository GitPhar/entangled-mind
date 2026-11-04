# Audit: stage2-run-1

**Files audited:** `results/stage2-run-1.{md,json}` (125 items, raw counts per arm), `results/pool-run-2.json`, `experiments/stage2_run.py` (`h2_verdict`, `h2_robust`, H3/H4 verdict code), `experiments/run_pool.py` (`answer_support`, D5 fallback), `experiments/preregistration.md` (H1–H5, one-item rule), DEVIATIONS D5. Citations: README.md:64–81, 214; paper/record.md:24; paper/the-entangled-mind-v3.md:339–345.
**Pre-registration:** `afe1c1b` (11-03 12:54:30); the D5 fallback test-set rule is in `2248e54` (14:17:24). First call: pool run 2, 14:16:17 (decoded), 67 s before D5 was committed; last 14:28:09. Simulator arms are git only. Result `0bc5a96` 14:39:58.
Timing verdict: OK (minor): the fallback rule reached git 67 s after the first pool-run-2 call and 11 min before the last one, and before any circuit ran.

## Plain-English summary of the audit
The table recomputes exactly from the raw counts. The fallback test set (4 wrong + the 10 right items with the least claim support) is reproduced by my own implementation of the D5 rule. Calling H2 "underpowered (nominally fail)" is fair: the D5 rule says so in advance, and with 4 wrong items nothing could be concluded. The flaw is that H3 and H4 are reported as firm verdicts ("falsified" and "fail (not falsified)"), although each flips when one item is dropped. Dropping x75 turns H3 into "fail (not falsified)". Dropping x68 turns H4 into a *pass*. Dropping any of six other items turns H4 into "falsified". The pre-registration says a verdict that depends on a single item is reported as "too noisy to call". The code applied that rule to H2 only. Every AUROC interval here spans most of [0, 1] (A: [0.02, 0.88]).

## Claims checked
| # | claim (quoted or paraphrased, with file:line) | recomputed / evidence | status |
|---|---|---|---|
| 1 | Test set: 4 wrong + 10 right with least net support; calibration 111, 0 wrong (stage2-run-1.md:5) | My `support` (Σ conf·lean / Σ conf, signed to the answer) reproduces the 10 right items; calibration ∩ test = ∅; 0 wrong in calibration | holds |
| 2 | Thresholds, calibration flag rates, flags, AUROCs (table) | Recomputed from raw counts: A 0.334 / 2 of 4 / 7 of 10 / 0.45; C 0.008 / 4 / 10 / 0.51; D 0.193 / 1 / 6 / 0.425; E 2.65 / 1 / 0 / 0.6875; A0 0.365 / 1 / 4 / 0.40 | holds |
| 3 | H1 pass, 0.86 | 12/14; still ≥ 0.70 after dropping any one item (≥ 11/13) | holds |
| 4 | H2 "underpowered: only 4 known-wrong items (nominally fail)" (stage2-run-1.md:25; README:78) | C flags 4/4 vs A 2/4, so the criterion fails. Robust to one flag change (C would need ≤ 1). The D5 fallback requires the "underpowered" label. Fair | holds |
| 5 | H3 "falsified" (A 0.45, C 0.51) (stage2-run-1.md:26; README:79; record:24; v3:342) | Leave-one-out: dropping x75 gives A 0.367, C 0.350, so the verdict becomes "fail (not falsified)". Paired bootstrap C − A [−0.30, +0.36]. Under the pre-registration's one-item rule this is "too noisy to call" | overclaim |
| 6 | H4 "fail (not falsified)" (A 0.45, D 0.42) (stage2-run-1.md:27; README:80; v3:343) | Leave-one-out: dropping x68 gives A 0.567, D 0.433, a **pass** (margin ≥ 0.10). Dropping x31, q31, q34, x17, x63 or x71 gives falsified. "Too noisy to call" | overclaim |
| 7 | AUROC values themselves | Stratified bootstrap 95% (5k): A [0.02, 0.88], C [0.15, 0.88], D [0.10, 0.78], E [0.38, 0.95], A0 [0.05, 0.80]; nothing is distinguishable from 0.5 | holds (no CI reported) |
| 8 | "Caution: … the right-item columns are biased upward …" (stage2-run-1.md:20) | Confirmed: C's threshold flags 21% of calibration but 100% of the 14 test items | holds |
| 9 | "Haiku still got only 4 of 125 standard items wrong, so Stage 2 run 1 is underpowered" (README.md:214) | confirmed | holds |
| 10 | H5 untested; gate not met | A's wrong-flag rate 0.50 is not > C's 1.00 | holds |

## Holes found
1. **The one-item rule was applied to H2 only.** The pre-registration says: "A pass or fail that depends on a single item will be reported as too noisy to call." `stage2_run.py` checks robustness only for H2. In run 1, H3 and H4 each flip on one item (H4 even to a pass), yet the result file, README, record and v3 report them as "falsified" / "fail (not falsified)". In run 2 the same check passes (see `audits/stage2-run-2.md`), so the bug matters only here.
2. **The fallback test set cannot discriminate.** Its right items were chosen to look uncertain, so every arm over-flags them (C flags all 14 test items). The file's caution says this. It means run 1 carries no evidence either way, which "underpowered" states only for H2.

## Overclaims to cut (exact sentences)
- `README.md:79` — "| H3 entanglement carries information | falsified | falsified |" — run-1 cell flips on one item — replace with "| H3 entanglement carries information | too noisy to call (nominally falsified) | falsified |"
- `README.md:80` — "| H4 structure carries information | fail (not falsified) | falsified |" — replace with "| H4 structure carries information | too noisy to call (nominally fail) | falsified |"
- `paper/the-entangled-mind-v3.md:342` — "- **H3** is falsified: A 0.45, C 0.51." — replace with "- **H3** is too noisy to call (nominally falsified: A 0.45, C 0.51; dropping one item reverses it)."
- `paper/the-entangled-mind-v3.md:343` — "- **H4** fails: A 0.45, D 0.42." — replace with "- **H4** is too noisy to call (nominally fails: A 0.45, D 0.42; dropping one item makes it pass, dropping others falsifies it)."
- `paper/record.md:24` (cell) — "H3 falsified (A 0.45, C 0.51)" — replace with "H3 too noisy to call (nominally falsified, A 0.45, C 0.51)".

## Does the verdict stand?
As pre-registered: H1 pass; H2 underpowered (nominally fail); H3 and H4 should be "too noisy to call" under the pre-registration's own one-item rule; H5 untested. **STANDS WITH CAVEATS.** The H1 and H2 labels stand. The H3 and H4 labels as reported do not, and they should be downgraded. This has no effect on the overall conclusion, which rests on run 2.

## Confidence
High. Scores, split, leave-one-out and bootstrap were all recomputed from the raw counts and claim tables.

## Tally
claims_checked: 10
claims_failed: 2
overclaim_sentences: 5
verdict: STANDS WITH CAVEATS
confidence: high

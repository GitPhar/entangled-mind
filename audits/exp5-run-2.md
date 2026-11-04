# Audit: exp5-run-2

**Files audited:** `results/exp5-run-2.md`, `results/exp5-run-2.json`, `results/exp5-run-2-conversations.json`, `results/exp5-conversations.json` (run 1 comparison), `experiments/exp5_rerun.py`, the Addendum to `experiments/exp5-sequential-judgment.md`, DEVIATIONS D33; citations in README.md, paper/record.md, paper/the-entangled-mind-v3.md, paper/the-entangled-mind-paper.md.
**Pre-registration:** `fbc2fbf` (23:00:01, D33), text in the Addendum of `experiments/exp5-sequential-judgment.md` ("Reading, fixed now"). The runner, with the full analysis and reading code, is `37ce49b` (23:01:41). First call: 23:01:44 decoded; last 23:12:34; result `bffc4ab` 23:14:30.
Timing verdict: OK. Design, reading rules and analysis code were all committed before the first call (the code by 3 s). The design was chosen after run 1's results were known, which is the point of a follow-up. The 10 items are "the first 10 candidates", fixed by an order set before run 1.

## Plain-English summary of the audit
Every number in the run-2 table recomputes from the raw conversations. The two pre-registered readings are correctly applied.
- **Order effects survive:** 12 of 16 run-1 large pairs are still large.
- **q's interval contains 0:** −0.146 [−0.439, +0.137].

Order effects survive, and that is well above chance: under a no-order-effect null only about 4 of 20 pairs pass. "The QQ equality is not supported" is worded correctly. If anything it is too mild, because 10 items give an interval about 12 times wider than the ±0.05 band and cannot test QQ either way. Run 1 already holds single-scale data on all 40 items (its anchor-(a) conversations), and there q = −0.345 [−0.517, −0.181]: the pre-registered "contradicted" condition would be met. That bears on one sentence of this file: the claim that run 1's tie verdict "is unchanged". The tie's "not contradicted" leg was computed on exactly the pooled q this run shows to be an artefact. KS p = 0.008 is the pre-registered one-sample KS of per-pair z against N(0,1), and it recomputes (exact p = 0.0074).

## Claims checked
| # | claim (quoted or paraphrased, with file:line) | recomputed / evidence | status |
|---|---|---|---|
| 1 | 1,700 conversations, $0.14, every conversation anchor (a) (exp5-run-2.md:3) | 1,700; $0.1414; anchors = {a} | holds |
| 2 | Run 2: 12 of 20 large-OE pairs; mean q −0.146 [−0.439, +0.137]; KS D = 0.46, p = 0.008 (exp5-run-2.md:7) | 12 of 20; −0.146 [−0.431, +0.156] (own bootstrap seed); D = 0.461, scipy p = 0.0074 | holds |
| 3 | Run 1 anchor a only: 12 of 20; −0.154 [−0.423, +0.154]; p = 0.017 (exp5-run-2.md:8) | 12; −0.154 [−0.459, +0.135]; p = 0.0169 | holds |
| 4 | Run 1 pooled: 16 of 20; +0.031 [−0.098, +0.166]; p = 0.002 (exp5-run-2.md:9) | 16; +0.031 [−0.099, +0.158]; p = 0.0023 | holds |
| 5 | B0 mean (SD) and between-repeat SD: 36.2 (34.2) 7.1; 36.6 (35.3) 4.1; 50.9 (29.5) 20.6 (exp5-run-2.md:7-9) | 36.2 (34.2) 7.09; 36.6 (35.3) 4.13; 50.9 (29.5) 20.57 | holds |
| 6 | "12 of 16 run-1 large-OE pairs are large in run 2"; order effects survive (exp5-run-2.md:37) | overlap 12 of 16; all 12 run-2 large pairs are in run 1's 16. Null (permutation within run 2): 4.0 of 20 pass the rule (range 0–8); 11 of 20 pairs Holm-significant | holds |
| 7 | "Near-zero q survives … True" (exp5-run-2.md:38) | correct application of the Addendum rule (CI contains 0). With 10 items the CI width is 0.58, so the rule could hardly fail. The label "near-zero q survives" describes a −0.146 estimate | holds (minor) |
| 8 | "Run 1's near-zero q was largely produced by pooling the two scale directions" (exp5-run-2.md:44) | confirmed and stronger on 40 items: run 1 anchor a −0.345 [−0.517, −0.181] (32 pairs), anchor b +0.241 [+0.118, +0.370] (47 pairs); first 10 items, anchor b +0.229 [+0.003, +0.471] | holds |
| 9 | "Run 1's pooled +0.031 came from averaging over the flipped scale, which pulled opposite-signed effects toward 0." (exp5-run-2.md:46) | per-pair q_a and q_b uncorrelated (r = −0.05 over 80 pairs); means −0.143 and +0.152 | holds |
| 10 | "The QQ equality is therefore **not** supported on one scale." (exp5-run-2.md:48); README:161, v3:68/625/821, record:41, paper:155 | accurate wording: run 2's CI includes 0, so QQ is neither supported nor, on 10 items, rejected. The pre-registered KS rejects per-pair N(0,1) (overdispersion, the Wang et al. test), which is evidence against QQ holding pair by pair. Nowhere does any of these files say "rejected" | holds |
| 11 | "The order effects are not a scale artefact." (exp5-run-2.md:42) | 12 of 16 survive, against about 3 expected by chance | holds |
| 12 | "The scale flip was also the main source of noise … 7.1 … against 20.6" / "Single-scale designs are much more sensitive." (exp5-run-2.md:49) | numbers hold. Run 1's own anchor-a B0 SD is 4.1, below run 2's 7.1, so between-run noise is not tiny. Run 2's q CI is still 12× the ±0.05 band | holds (minor) |
| 13 | "Run 1's verdict, a tie, does not use QQ beyond "signature not present", so it is unchanged." (exp5-run-2.md:50); v3:625 "Run 1's verdict, a tie, does not depend on it." | §7.5 also uses "signature contradicted" (it gives classical when the primary is not a pass). Run 1's "not contradicted" was computed on the pooled q this file calls an artefact. On run 1's single-scale conversations (40 items) the contradiction condition is met | overclaim |
| 14 | KS p = 0.008: what test, pre-registered? | one-sample KS of per-pair z (Wang–Busemeyer z, pooled p̂) against N(0,1), asymptotic Kolmogorov p with Stephens' correction; pre-registered in §7.3.3 and named in the D33 Addendum ("KS of z") | holds |

## Holes found
1. **The run-1 verdict is called "unchanged" when one of its inputs was just shown to be an artefact.** §7.5's verdict table gives "classical" for "a signature contradicted with the primary not a pass". "Contradicted" means the mean-q CI excludes 0 (§7.3). Run 1's tie therefore depends on the pooled q's CI including 0, and that pooled q is the cancellation of +0.24 and −0.35 that this run diagnoses. On run 1's single-scale subset, the contradiction condition holds: anchor a, 40 items, −0.345 [−0.517, −0.181], and −0.143 [−0.214, −0.077] over all 80 pairs, at every cut from 30 to 70. Run 2 itself is too small (10 items) to show it. The tie label is therefore not secure against the classical label. Either way there is no quantum signature.
2. **The 40-item single-scale analysis was available at no cost, yet only the 10-item slice was reported.** The runner (`exp5_rerun.py`) computes "run 1, anchor a only" restricted to the same 10 items. The same split on all 40 items needs no calls, but appears nowhere in results/ or paper/ (I grepped for −0.345, −0.34 and anchor-split q). The Addendum fixed the 10-item comparison in advance, so this is not a breach. But the omitted analysis is the one that answers the question run 2 asks ("does the near-zero q survive one scale?"), and it answers no. I have no evidence that the omission was deliberate.
3. **The "survives" rule for q was weak by construction.** A 10-item CI on mean q has width of about 0.58, so "CI contains 0" was close to guaranteed unless \|q\| were about 0.3 or more. The rule's name ("near-zero q survives") reads as support for QQ, but its outcome (True) is uninformative. The text does say the estimate leans negative and is imprecise, which is correct.
4. **The large-OE criterion has no noise floor** (inherited from run 1). In run 2, a permutation null passes 4.0 of 20 pairs on average (range 0–8). The observed 12 of 20 and 11 Holm-significant pairs are clearly above it, so the survival reading holds. The count of pairs with "OE > 0.10 (CI excl. 0)" should not be read as the count of real effects.

## Overclaims to cut (exact sentences)
- `results/exp5-run-2.md:50`: "Run 1's verdict, a tie, does not use QQ beyond "signature not present", so it is unchanged."
  - Why: §7.5 also uses "contradicted", which was computed on the artefactual pooled q. On run 1's one-scale subset (anchor a, 40 items) mean q = −0.345 [−0.517, −0.181], which meets the contradiction rule.
  - Replace with: "Run 1's verdict, a tie, used the pooled q for "not contradicted"; on run 1's single-scale conversations (anchor a, 40 items, not a pre-registered subset) mean q is −0.345 [−0.517, −0.181], which would meet the contradiction rule and make the label classical. Neither label supports a quantum account."
- `paper/the-entangled-mind-v3.md:625`: "Run 1's verdict, a tie, does not depend on it."
  - Why: as above.
  - Replace with: "Run 1's tie depends on it only through "not contradicted", which used the pooled q; on run 1's single-scale subset the contradiction rule would be met."

## Does the verdict stand?
Pre-registered readings (D33 Addendum): order effects survive (True), near-zero q survives (True), near-miss resolved (False). **STANDS WITH CAVEATS.** Both readings are computed exactly and as fixed in advance, and the order-effect survival is well above chance. The q "survival" is uninformative at n = 10 items. The file's own conclusion, that run 1's near-zero q was a pooling artefact and QQ is not supported, is correct and conservative. The one sentence that outruns the evidence is the claim that run 1's verdict is unchanged.

## Confidence
high. Every table entry was recomputed from the raw archived conversations of both runs with independent code (OE, q, z, KS via scipy, item bootstraps, B0 statistics, the permutation noise floor). No model is involved in run 2.

## Tally
claims_checked: 14
claims_failed: 1
overclaim_sentences: 2
verdict: STANDS WITH CAVEATS
confidence: high

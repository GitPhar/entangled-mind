# Audit: bm9-contrast

**Files audited:** `results/bm9-contrast.md`, `results/bm9-contrast.json`, `results/exp5-conversations.json` (QQ, anchor a), `results/exp5-run-2-conversations.json`, `experiments/split-exp5.json`, `results/pool-run-3.json`, `experiments/bm9-contrast.md`, `experiments/bm_offline.py` (`bm9`, `bm9_pairs`), DEVIATIONS D42; citations in `paper/morning-brief.md`, `paper/record.md`, `paper/no-credence-to-read.md`, `results/bm1-serial-dependence.md`.
**Pre-registration:** `2798079` (05:08:50), text in `experiments/bm9-contrast.md` §§3–4. The analysis code was committed earlier, in `9c29a94` (05:08:07), and never changed. First call: none, archival (run 1 calls 11-03 20:18–21:50; run 2 calls 23:01–23:12). Result `7fd1121` 05:09:05, 15 s later, with hand-written prose.
Timing verdict: PROBLEM (unverifiable). The code was frozen, but results and prose followed 15 s after the pre-registration. Both archives had been analysed before (exp5 run 1/2 and direction 9's N1M family), though not for the L relation.

## Plain-English summary of the audit
The pre-registered statistic reproduces exactly: β +0.268 [+0.109, +0.427] (run 1, 80 pairs) and +0.274 [+0.046, +0.584] (run 2, 20 pairs). It is not driven by one item (leave-one-item-out +0.22 to +0.29) or by shared noise in the "M first" mean (split-half β +0.267). The "replication" uses new conversations (exp5 run 2, collected later that evening), but on the same first 10 of the 40 items and the same claim pairs. It is a re-sampling, not a new item set. Run 1 restricted to those 10 items gives +0.34. The problem is what β means. L = S − M_first and d_M = M_after − M_first share the term −M_first. Fitting S and M_first separately (my exploratory check, not pre-registered) gives a coefficient on the S level of only +0.13 [−0.04, +0.28] (run 1) and +0.04 [−0.16, +0.28] (run 2). The coefficient on M_first is −0.37 and −0.57. The L coding assumes the two are equal and opposite, and that assumption is rejected (sum −0.25 [−0.43, −0.11] and −0.52 [−1.24, −0.12]). So the positive β mostly says that M is less extreme when S is asked first (slope of M_after on M_first 0.70). A pull toward the number S just received is not detectable. "Assimilation" is the correct pre-registered label for β > 0, but "moves toward the number it just gave" is not shown. The secondary signed correlation is also ambiguous: unsigned, it is +0.38 for yes-leaning claims and +0.00 for no-leaning ones. That is the pattern content-following predicts, not number-following.

## Claims checked
| # | claim (quoted or paraphrased, with file:line) | recomputed / evidence | status |
|---|---|---|---|
| 1 | β +0.268 [+0.109, +0.427], γ +7.7 [+0.8, +16.0], corr +0.17 [+0.05, +0.29] (76), run 1 (md:22) | Exact (80 pairs, 20 per order) | holds |
| 2 | Replication β +0.274 [+0.046, +0.584], corr +0.34 (md:23; "+0.27 [+0.05, +0.58]" md:11) | Exact (20 pairs, 40 per order). Same 10 items as run 1's first 10, same pairs, new conversations | holds (minor: same items) |
| 3 | "For every point by which the sub-question rating sits above the model's unprompted main rating, the main rating moves about a quarter-point toward it" (md:10) | The L coefficient is mostly the −M_first term. S-level coefficient +0.13 [−0.04, +0.28] (run 1) and +0.04 [−0.16, +0.28] (run 2); M_first coefficient −0.37 / −0.57; the equality constraint is rejected | overclaim |
| 4 | "**Replication.** The single-scale run 2 gives the same figure" (md:11) | True for β; "replication" is on the same items | holds (minor) |
| 5 | "**Within the same question,** conversations where the model happened to rate the sub-question higher also tend to give a main rating that follows it in the content's direction (correlation +0.17 and +0.34)." (md:12) | The numbers hold. Unsigned: lean > 0 +0.38, lean < 0 +0.00 (run 1); +0.55 / −0.14 (run 2). Number-following would give positive values for both; the data fit content-following | holds (literal), but presented as support for assimilation |
| 6 | "The model's next judgment is pulled toward the number it just produced, beyond what the claim's content implies. That is the self-anchoring direction 2 found with planted numbers, now seen in unedited conversations." (md:14) | As #3 and #5 | overclaim |
| 7 | "No contrast appears, so the reactance seen toward *another person's* numbers in run 3 does not extend to the model's own numbers." (md:14) | No β < 0, true; the inference about source compares different paradigms | overclaim (minor) |
| 8 | morning-brief.md:72 "After rating a claim, the model's main rating moves about a quarter of the way toward the number it just gave, beyond what the claim's content implies." | As #3. Also "a quarter of the way" for a per-point slope | overclaim |
| 9 | morning-brief.md:127 "the model pulls each new number toward the last one it gave (4, 9)" | As #3 (item 4 is direction 2, not audited here) | overclaim |
| 10 | no-credence-to-read.md:247 "the main rating moves toward the level of the sub-question rating just given, beyond the claim's content" | As #3 | overclaim |
| 11 | record.md:54 "ratings assimilate toward the last number (β +0.27)" | As #3 | overclaim |

## Holes found
1. **β does not isolate a pull toward S.** With d_M = M̄_SM − M̄_MS and L = S̄_SM − M̄_MS, a model in which M after S simply regresses toward a middle value, with no dependence on S, also gives β > 0 through the shared −M̄_MS. Unconstrained (d_M ~ S̄ + M̄_MS + C), run 1 gives b_S +0.125 [−0.037, +0.282] and b_M −0.374 [−0.571, −0.195]; run 2 gives b_S +0.043 [−0.157, +0.277] and b_M −0.567 [−1.307, −0.181]. b_S + b_M = −0.25 [−0.43, −0.11] and −0.52 [−1.24, −0.12]. The L model's implicit constraint is rejected, and the S part, which is what "toward the number it just gave" means, has a CI including 0 in both runs. This is my exploratory decomposition (seed 5252 cluster bootstrap), not a pre-registered test, but it bears directly on the wording.
2. **The secondary correlation does not separate assimilation from content.** It is signed by the claim's lean, so content-consistent inference scores positive. Unsigned, it is positive only for lean > 0 claims. A number pull would be positive for both.
3. **The replication is on the same items.** Run 2's 10 items are run 1's first 10 candidates (the same ones), with the same QQ pairs. It shows the statistic is stable across sessions, not across items.
4. **Timing:** as for D40/D41.
5. **Multiple comparisons:** 6 CIs (β, γ, corr × 2 sets). The primary β (z ≈ 3.3) survives Bonferroni across the roughly 11 primary decisions of the five biomimetic runs. The point is not significance but what β measures.

## Overclaims to cut (exact sentences)
- `results/bm9-contrast.md:10` — "- **Toward the number.** For every point by which the sub-question rating sits above the model's unprompted main rating, the main rating moves about a quarter-point toward it: +0.27 [+0.11, +0.43]. That is on top of the content's own push, +7.7 points." — the S-level part is +0.13 [−0.04, +0.28]; β is mostly the shared M-first term — replace with: "- **Level effect.** The shift in M rises with how far the S rating sits above the unprompted M: +0.27 [+0.11, +0.43] per point, on top of the content push (+7.7). Separating the two terms, most of this is M being less extreme after S (coefficient on M-first −0.37); the coefficient on the S level alone is +0.13 [−0.04, +0.28]."
- `results/bm9-contrast.md:14` — "The model's next judgment is pulled toward the number it just produced, beyond what the claim's content implies. That is the self-anchoring direction 2 found with planted numbers, now seen in unedited conversations." — not isolated — replace with: "By the pre-registered rule this is assimilation (β > 0), not contrast. The statistic does not by itself separate a pull toward S from M becoming less extreme after S."
- `results/bm9-contrast.md:14` — "No contrast appears, so the reactance seen toward *another person's* numbers in run 3 does not extend to the model's own numbers." — replace with: "No contrast appears."
- `paper/morning-brief.md:72` — "After rating a claim, the model's main rating moves about a quarter of the way toward the number it just gave, beyond what the claim's content implies." — replace with: "After rating a sub-claim, the shift in the main rating rises with the sub-claim's level (β +0.27), mostly because the main rating is less extreme after a sub-question; a direct pull toward the sub-claim's number is not separately detectable."
- `paper/morning-brief.md:127` — "the model pulls each new number toward the last one it gave (4, 9)" — cut "9" from the support, or cut the clause.
- `paper/no-credence-to-read.md:247` — "**Test A.** In unedited single-scale conversations, the main rating moves toward the level of the sub-question rating just given, beyond the claim's content: **β = +0.27 [+0.11, +0.43]**, replicating at +0.27 [+0.05, +0.58]. No contrast appears." — replace with: "**Test A.** In unedited single-scale conversations, the shift in the main rating rises with the level of the sub-question rating just given, beyond the claim's content: **β = +0.27 [+0.11, +0.43]** (+0.27 [+0.05, +0.58] on new conversations for 10 of the same items). No contrast appears. Most of β reflects the main rating being less extreme after the sub-question; the sub-rating's own coefficient is +0.13 [−0.04, +0.28]."
- `paper/record.md:54` — "ratings assimilate toward the last number (β +0.27)" — replace with: "the M shift rises with the S level (β +0.27; assimilation by the pre-registered rule)".

## Does the verdict stand?
Pre-registered reading: **assimilation** (CI of β above 0). **STANDS WITH CAVEATS.** The pre-registered statistic is robust: leave-one-item-out, split-half and lean-sign subsets (+0.32 and +0.41) all stay positive. But as coded it mostly reflects M being less extreme after S, and the interpretation everywhere ("moves toward the number it just gave") is not supported by a separate S-level effect.

## Confidence
Medium. The pre-registered numbers were recomputed exactly. The decomposition (hole 1) is my own exploratory analysis on the same pairs. It is a simple OLS, but it was not pre-registered, and with only 20 pairs, run 2's intervals are wide.

## Tally
claims_checked: 11
claims_failed: 7
overclaim_sentences: 7
verdict: STANDS WITH CAVEATS
confidence: medium

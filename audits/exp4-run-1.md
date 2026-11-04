# Audit: exp4-run-1

**Files audited:** `results/exp4-run-1.md`, `results/exp4-run-1.json`, `results/exp4-calls.json` (5,480 calls: 1,280 rate, 1,400 first-position, 2,800 second-position); `experiments/exp4-yearsley-trueblood.md`; `experiments/exp4-items.json`; `experiments/exp4_run.py`; D11 and its R2 addendum. Citations in README.md, paper/record.md, paper/the-entangled-mind-v3.md, paper/the-entangled-mind-paper.md, paper/gold-map.md.
**Pre-registration:** `54cfa1f` (11-03 16:52:06) plus the R2 correction `3fe936e` (17:04:21, D11 addendum); runner `38ff0ae` (17:24:43). First call: 18:10:21 (decoded), last 18:19:45; result `bd386f3` 18:20:26.
Timing verdict: OK. Design, rules and code were all committed before the first call (46 min margin for the code).

## Plain-English summary of the audit
The headline holds. Rebuilt from the raw calls, 7 of 16 items have a rating fallacy whose bootstrap lower bound is above 0, and none has a double fallacy. In the yes/no phase, the unlikely conjunct Y was answered "no" in 100 of 100 first-position samples on all 7 items, so the pre-registered R2 test had nothing to work with and the "untestable" verdict is correct. Two caveats. First, two of the seven fallacies are 2–3 points with lower bounds of +0.003 and +0.004, and they would not survive any correction for 16 tests, so "7 of 16" is really 5 clear ones plus 2 marginal ones. Second, the binary phase is not free of order effects: the first conjunct's yes-rate moves by up to 67 points with order. The project later forgets this when it says yes/no answers show no order effects (see the exp3 audit). The claim that "nothing is contextual" is vacuous here, because saturation forces Γ = 0. One paper sentence credits a classical Markov chain with describing the conjunction fallacies, but no such fit was ever made.

## Claims checked
| # | claim (quoted or paraphrased, with file:line) | recomputed / evidence | status |
|---|---|---|---|
| 1 | "7 of 16 items show a reliable fallacy" (exp4-run-1.md:24; README.md:128; v3:62, 463; record.md:30) | 7/16 with my own 5,000-resample bootstrap: co01 +0.085 [+0.070, +0.095], co-lin06 +0.019 [+0.003, +0.035], co-lin08 +0.084, co-lin09 +0.143, co-lin10 +0.029 [+0.004, +0.053], co05 +0.287, co06 +0.191. Welch p for co-lin06 0.025 and co-lin10 0.037; a Holm correction over 16 tests drops both, leaving 5. | holds (minor) |
| 2 | "Reliable double fallacies (R3): 0" (exp4-run-1.md:24; README.md:128; paper.md:224) | 0/16; every double-fallacy upper bound is ≤ −0.10 | holds |
| 3 | Largest fallacies co05 +0.29, co06 +0.19, Linda +0.085 (exp4-run-1.md:54; v3:463) | +0.287, +0.191, +0.085 | holds |
| 4 | "On every fallacy item the model answers 'Is it true that <Y>?' with *no* in all 100 first-position samples" (exp4-run-1.md:55; README.md:129; v3:466) | 0/100 yes for Y-first on all 7 items. X-first is also 0/100 on co-lin08, co05 and co06, and 100/100 on co01. | holds |
| 5 | Phase-2 table: all items saturated, 0 scored, verdict untestable (exp4-run-1.md:31–50) | Archived `saturated` = true ×7, `scored` = []. Pre-registered gate and rule applied as written. | holds |
| 6 | "OE_X = +0.67, +0.50, −0.22, +0.43" (exp4-run-1.md:56) | From raw: co-lin06 6/100 → 73/100 (after forced "no" to Y, which is the model's own answer); co-lin08 0 → 50; co-lin09 22 → 0; co-lin10 57 → 100. Archived CIs [+0.60, +0.74], [+0.50, +0.50], [−0.29, −0.15], [+0.38, +0.47]. | holds |
| 7 | "Γ = 0 on every item, so nothing is contextual under rank-2 Contextuality-by-Default." (exp4-run-1.md:56) | With Y deterministic, q_QQ = −OE_X and OSS = \|OE_X\|, so Γ = 0 identically. Deterministic variables are trivially non-contextual, so the check carries no information here. | overclaim |
| 8 | "no double fallacies (R3), which is what the quantum account requires and what Yearsley & Trueblood (2018) found in people" (exp4-run-1.md:54) | Correct as stated. Coherent classical probability also forbids double fallacies, so it is not specific to the quantum account. | holds (minor) |
| 9 | "The fallacy shows up in graded ratings and disappears under yes/no truth questions" (exp4-run-1.md:57; gold-map.md:189) | Holds on these items. P(Y = yes) = 0 removes the joint. | holds |
| 10 | "single but not double conjunction fallacies (experiment 4 …). A classical Markov chain describes them as well as the quantum state does." (paper.md:224) | The fallacy half holds. No Markov chain or quantum state was fitted to experiment 4: the dephased-chain comparison is experiment 5's order effects. "them" overreaches. | overclaim |
| 11 | record.md:30 "7/16 single fallacies in ratings, 0 doubles; the binary QQ phase saturated, so R2 was untestable" | as above | holds |
| 12 | Protocol: R = 20 ratings × 4 forms; R = 50 first-position per order × mapping; R = 25 second-position × 2 forced × 4 mapping combinations; thinking disabled; structured output | Call counts match (1,280 / 1,400 / 2,800); code matches the frozen text | holds |

## Holes found
1. **Two of the seven fallacy items are marginal.** co-lin06 (+0.019, lower bound +0.003) and co-lin10 (+0.029, lower bound +0.004) pass an uncorrected per-item bootstrap rule over 16 items. Under Holm on Welch p, 5 of 16 remain. The rule was pre-registered, so "7 of 16" is a correct application of it, but the text calls all seven "reliable". The ratings are also nearly deterministic (co01's 20 conjunction ratings take only the values 0.05, 0.10 and 0.15), so the CIs describe sampling of one prompt, not generalisation across wordings. This matters downstream, because run 2 takes all seven forward and only 3 show a graded fallacy there.
2. **The binary phase does contain large order effects, and the project's later summaries forget it.** Run 1's own Reading reports OE_X up to +0.67. README.md:195, v3:60, paper.md:150 and biomimetic-map.md:36 nonetheless say yes/no answers show no order effects (cut in the exp3 audit). They are second-position answers after a committed "no" to Y, which is the model's own first-position answer, so they are not artefacts of a forced, unnatural branch.
3. **The Γ = 0 / "nothing is contextual" statement is forced by the saturation** (claim 7). It should be reported as uninformative, not as a finding.
4. **The rating fallacy and the yes/no saturation measure different things.** "Is it true that …?" asks for a truth verdict, while the rating asks for a probability. The Reading says this, correctly. The headline "the binary QQ phase saturated" is accurate, but no inference about R2 or quantum structure follows from it in either direction, which the verdict "untestable" already respects.

## Overclaims to cut (exact sentences)
- `results/exp4-run-1.md:56` — "Γ = 0 on every item, so nothing is contextual under rank-2 Contextuality-by-Default." — Γ = 0 is forced when Y is deterministic, so the CbD check is uninformative. — Replace: "Γ = 0 on every item, but only because Y is deterministic (q_QQ = −OE_X), so the Contextuality-by-Default check is uninformative here."
- `paper/the-entangled-mind-paper.md:224` — "A classical Markov chain describes them as well as the quantum state does." — No model was fitted to experiment 4's fallacies; the Markov-chain match is experiment 5's order effects. — Replace: "A classical Markov chain describes experiment 5's order effects as well as the quantum state does; experiment 4's fallacies were not modelled."

## Does the verdict stand?
Pre-registered verdict: **untestable** (0 scored items). **STANDS.** Saturation is total and the gate was applied as frozen. The descriptive "7 of 16" is right under the frozen rule, with 2 marginal items.

## Confidence
High. Every number was rebuilt from `exp4-calls.json` with independent code. The forced-branch joint, letter-copy ρ and repetition r were checked from the archive but not fully re-derived, since all items are saturated and none is scored.

## Tally
claims_checked: 12
claims_failed: 2
overclaim_sentences: 2
verdict: STANDS
confidence: high

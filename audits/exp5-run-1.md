# Audit: exp5-run-1

**Files audited:** `results/exp5-run-1.md`, `results/exp5-run-1.json`, `results/exp5-fit.json`, `results/exp5-conversations.json`, `experiments/split-exp5.json`; code read: `experiments/exp5_analyse.py`, `exp5_models.py`, `exp5_run.py`; DEVIATIONS D22–D26, D32; citations in README.md, paper/record.md, paper/the-entangled-mind-v3.md, paper/the-entangled-mind-paper.md, paper/gold-map.md, paper/no-credence-to-read.md.
**Pre-registration:** draft `2dc435b` (19:19:37), frozen `2c2ef6c` (20:15:54, D22), text in `experiments/exp5-sequential-judgment.md` §5–§7; split and runner `2ad710c` (20:18:09, D23); `97dde55` (20:18:37, D24); models `2251693` (20:32:21, D26); analysis code and D26 addendum `1155dde` (20:34:48); `e39bf3c` (20:36:32, adds the non-commuting count); D32 tolerance fix in `75744dc` (22:24:31, with the results). First call: full run 20:30:12 decoded (pilot 20:18:49); last 21:50:57; conversations archived `f27bd95` 21:51:07.
Timing verdict: PROBLEM (minor). The design, split, item set, statistic and verdict table were frozen before any call. But D26's model details and the D26 addendum to the verdict table were committed after full-run collection had begun. By `2251693`, 892 full-run calls had been made. By `1155dde`, 1,958 calls (606 conversations, on h190, h101 and h112) had been made. The runner rewrites `results/exp5-conversations.json` every 200 conversations, so partial full-run data were on disk at both commits. All 1,400 pilot conversations (the full design, on 5 items) had already been read for the gates. No fit or score could have been run before `f27bd95`, and the analysis code is unchanged after `1155dde` except for `e39bf3c` (a count) and D32. "Unread" (D26) is author testimony that the record cannot confirm.

## Plain-English summary of the audit
The headline numbers are exactly right. I re-scored the test chains with the archived fitted parameters and got A5 984.0, F5 1050.9, and Δ = +67.0 with my own bootstrap CI [−37, +208]. Every QQ, Kvam and descriptive number recomputes from the raw conversations. "Tie" is a pre-registered category with a rule (the CI includes 0), and the rule was applied correctly. But a tie here means "could not tell apart": the interval allows F5 to be up to 21% worse, and +56 of the +67 comes from one item (h183).

Two things are wrong.
- **The verdict's tie label rests on the pooled q that run 2 calls an artefact.** The run-1 QQ reading ("close but not certified", "not contradicted") uses that pooled q. Run 1's own one-scale conversations (anchor a, all 40 items) give mean q = −0.345 [−0.517, −0.181]. Under the pre-registered rule, that would count as the QQ signature *contradicted*, which turns "tie" into "classical".
- **The order-effect counts have no noise floor.** "60 of 80 pairs" has none: about 27 pairs pass the criterion by chance, and 40 survive a corrected permutation test. The median span of 24.7 points compares with 13 points from repeat noise alone.

Under any reading, no quantum signature or advantage is shown. The "tie" label and the "QQ close" sentences should be qualified.

## Claims checked
| # | claim (quoted or paraphrased, with file:line) | recomputed / evidence | status |
|---|---|---|---|
| 1 | Test chains: MSE A5 984.0, F5 1050.9, D5 987.8, A5κ=0 1008.4 (exp5-run-1.md:24-31) | re-scored with the archived params via `exp5_models.predict` (network blocked): 984.0, 1050.9, 987.8, 1008.4 on 3,430 ratings | holds |
| 2 | **Δ = MSE_F5 − MSE_A5: +67.0 [−34.1, +211.5]**, primary TIE (exp5-run-1.md:35, 89) | my item bootstrap (4,000 draws): +67.0 [−37.2, +208.0]. The units are MSE in rating points² (not log-likelihood). §7.2: "tie" if the CI includes 0, a pre-registered category with a rule. Relative to MSE_A5: +6.8% [−3.8%, +21.1%]. h183 contributes +55.8 of the +67.0; leave-one-item-out range +11.7 to +82.4; A5 is better on 16 of 32 items | holds (as a pre-registered "not distinguishable"; not an equivalence) |
| 3 | Held-out F5 − A5 +207.3 [+52.0, +387.5]; D5 − A5 −11.3 [−61.4, +44.9] (exp5-run-1.md:60, 63) | +207.3 [+49.1, +387.7]; −11.3 [−60.3, +46.7]. h033 carries +93 of the +207; LOO range +130 to +247 | holds |
| 4 | D5 − A5 test +3.8 [−21.8, +30.9]; κ=0 +24.4 [−8.0, +60.5] (exp5-run-1.md:37-38) | +3.8 [−21.3, +31.5] (±3% of MSE); +24.4 [−6.7, +59.6] | holds |
| 5 | "A tie is therefore the predicted outcome, not a surprise." (exp5-run-1.md:7) | §8.6 is a risk/mitigation note ("Expect A5 and F5 to be close on most claims"), not a predicted verdict. §7.2 lists pass/classical/tie with none designated as predicted | overclaim |
| 6 | 12 of 160 chain claims have \|sin Δφ\| > 10⁻⁶, max 0.424 (exp5-run-1.md:5) | recomputed with the encoder: 12 of 160, max 0.424; only 5 exceed 0.05 | holds |
| 7 | 60 of 80 pairs have OE > 0.10 with CI excluding 0 (exp5-run-1.md:83, 183) | count reproduces (60). But OE ≥ 0 by construction, so its bootstrap CI almost always excludes 0. Under an order-label permutation null (within anchor), a mean of 27.5 of 80 pairs pass (range 19–35). Permutation test: 50 pairs p < .05, 48 BH, 40 Holm | overclaim (as a count of real order effects) |
| 8 | Median span of main-rating means 24.7 points (exp5-run-1.md:172) | 24.7 reproduces. Null (chain labels permuted within item × anchor): 13.2 [10.6, 15.8]. O1–O4, X1–X4 only: 20.3 vs null 10.4. Kruskal–Wallis across O/X chains p < .05 on 19 of 40 items | holds (minor): real, but about half is noise |
| 9 | Mean q +0.005 [−0.058, +0.065]; KS D = 0.385, p = 0.000 (exp5-run-1.md:84) | +0.005 [−0.058, +0.065]; scipy KS D = 0.385, p < 10⁻⁷. KS of z vs N(0,1) was pre-registered (§7.3.3) | holds (numerically) |
| 10 | "The QQ equality is close but not certified." / "the mean q is +0.005, close to 0" (exp5-run-1.md:185) | per anchor on run 1's own data: anchor a, 32 large pairs, −0.345 [−0.517, −0.181]; anchor b, 47 large pairs, +0.241 [+0.118, +0.370]; all 80 pairs, anchor a −0.143 [−0.214, −0.077], anchor b +0.152 [+0.074, +0.237]; corr(q_a, q_b) over pairs −0.05. Anchor a excludes 0 at every cut from 30 to 70. Pooled q is a cancellation | wrong |
| 11 | "So the signature is not present, and it is not contradicted either." (exp5-run-1.md:185) | correct under the rule on the pooled data. On the one-scale subset the rule's contradiction condition (CI excludes 0) is met (row 10). Post hoc, but it is the subset run 2 itself reports for 10 items | holds (minor), misleading |
| 12 | Robustness cuts 30/40/60/70 to be reported (§7.3.4) | computed in the JSON (`q_by_cut`) but absent from the md. 60-pair pooled mean q: cut 30 +0.006, 40 −0.012, 60 −0.080 [−0.157, +0.001], 70 −0.157 [−0.257, −0.053] | not reported (deviation) |
| 13 | A priori sub-test 1 win, 2 losses, p = 0.875; exact-float version 28–9 (exp5-run-1.md:86; D32) | recomputed: exact float 28–9 (one-sided p = 0.0013); 1e-6 tolerance 1–2 (p = 0.875); the 3 items are h261, h135, h149 | holds |
| 14 | Kvam Δ_K = +0.29 [−1.12, +1.65] (exp5-run-1.md:171) | +0.288 [−1.14, +1.69]; 90% CI [−0.89, +1.49]; LOO mean range −0.04 to +0.68; 4 of 40 items have Δ_K = 0 | holds |
| 15 | "Confidence after a mid-chain choice equals confidence after a matched filler" (exp5-run-1.md:186) | absence of evidence. The CI excludes only effects larger than about 1.1 points of folded confidence. Kvam et al.'s human effect (83.96 vs 85.15, −1.19) sits at the interval's edge | overclaim |
| 16 | Total-probability residual +0.58 points (exp5-run-1.md:173) | +0.58; item-bootstrap CI [−3.05, +4.15], not reported | holds (minor) |
| 17 | A5⁰ sign agreement 53% | needs model predictions; not re-derived independently (36 items, 19 agree, binomial p ≈ 0.87) | not checkable (used authors' value) |
| 18 | MF replicability 84%; B0 by anchor a 33.8, b 71.3 (exp5-run-1.md:170-171) | 0.8375 of 400; 33.80 vs 71.33 (n 200 each); b > a on 37/40 items, \|b − a\| > 20 on 27/40 | holds |
| 19 | "a classical Markov chain does as well as the coherent quantum state" (exp5-run-1.md:192) | D5 − A5 CIs: test ±3% of MSE, held-out −8% to +6%. Both exclude the held-out A5–F5 gap | holds (minor) |
| 20 | BA5 best on main ratings, 827 vs 873, −46 [−94, +14] (exp5-run-1.md:189) | not re-scored by me (reproduce.py matched it). "Best" is a point estimate; the CI includes 0 | holds (minor) |
| 21 | Schema exclusions 0; 12,600 conversations; $1.93 (exp5-run-1.md:3) | 0 error turns; 12,600; $1.928 | holds |
| 22 | D26 "fixed before any full-run data were examined" (DEVIATIONS:386; v3:244, 308; paper:296) | 606 full-run conversations existed, and partial snapshots were on disk, when `1155dde` was committed; pilot data fully read | not checkable |

## Holes found
1. **The tie/classical label depends on the anchor-pooling artefact.** §7.5 gives "classical" if "a signature [is] contradicted with the primary not a pass". The QQ signature is "contradicted" if the mean-q CI on the large-OE pairs excludes 0 (§7.3). On the pre-registered pooled data, mean q = +0.005 [−0.058, +0.065], so not contradicted, and the verdict is tie. But the pooled value is the average of two opposite-signed directions, as row 10 shows: anchor a −0.345 [−0.517, −0.181] and anchor b +0.241 [+0.118, +0.370]. Run 2 and its write-up already call the pooled q an artefact. On run 1's single-scale conversations (anchor a, 40 items), the contradiction condition is met, and the §7.5 label would be **classical**. That subset is post hoc, but it is the same split run 2 reports for its 10 items. Consequence: "tie" is the correct pre-registered label, but its "not contradicted" leg rests on an artefact, so tie versus classical is undetermined. No reading supports a quantum advantage.
2. **The order-effect evidence has no noise floor and no multiplicity control.** OE = max(\|c_yy\| + \|c_nn\|, \|c_yn\| + \|c_ny\|) is non-negative, so a percentile bootstrap CI "excludes 0" almost whenever the responses are not constant. With 40 responses per order, sampling noise alone yields OE > 0.10 often. Under a permutation null (order labels shuffled within anchor), 27.5 of 80 pairs (range 19–35) pass the "OE > 0.10, CI excluding 0" rule. A per-pair permutation test, with 80 tests, gives 50 at p < .05, 48 BH-significant and 40 Holm-significant. The same is true of the median span, 24.7 against a noise floor of 13.2. Order effects are real on about 40–50 pairs, and "60 of 80" overstates them by roughly 10–20 pairs. Many downstream sentences cite "60 of 80" as the size of the effect.
3. **The pre-registered robustness cuts were not reported** (§7.3.4: "q is also reported at cuts of 30, 40, 60 and 70"). They are in the JSON only. Even pooled, the 60-pair mean q is −0.080 [−0.157, +0.001] at cut 60 and −0.157 [−0.257, −0.053] at cut 70. So "close to 0" was specific to the cut of 50, as well as to the pooling.
4. **A tie is not equivalence, and the primary had little to test.** The primary CI spans −3.8% to +21.1% of A5's MSE. The point estimate is mostly one item: h183 gives +55.8 of +67.0, and without it Δ = +11.7. Only 12 of 160 chain claims (5 above 0.05) had any predicted non-commutation at encode. F5 fitted λ = 0, so A5 and F5 differ mainly in between-question mixing. The D5 contrast shows that this mixing is classical. So the contest could hardly detect a coherence-specific advantage. The authors' own D5 analysis is the informative part. Sentences that say quantum probability "adds nothing", or that the two models "do not differ", outrun a CI this wide.
5. **"Tie was predicted" is post-hoc framing.** §8.6 is a mitigation note about the anchored solver shrinking off-axis angles ("Expect A5 and F5 to be close on most claims"). The pre-registered verdict table designates no outcome as predicted. Presenting the tie as "the predicted outcome, not a surprise" (exp5-run-1.md:7, README:159, paper:157) recasts an inconclusive primary as a confirmed prediction.
6. **D26 was fixed during collection.** The record excludes the following: no fit or score existed before `f27bd95` (21:51:07), and the analysis code was frozen at `1155dde` apart from a count (`e39bf3c`) and D32. The record cannot exclude that the partial `exp5-conversations.json` (606 full-run conversations on 3 items, plus the pilot) was looked at before D26. In its favour: the D26 choices are mostly structural (κ scaling convention, one evolution step per turn, the Π_M tie rule, D5's exact form, a hedge prior of ½, BA5's boxes, whole-conversation schema exclusion). The addendum, which counts Kvam "commitment" as a contradiction, can only make a non-quantum verdict easier, and the Kvam result was null anyway. Risk to the verdict is low, but "before any full-run data were examined" should be stated as testimony, or replaced by what the record shows.
7. **The D32 tolerance fix after results.** It changed the a priori sub-test from 28–9 (p = 0.0013, apparently supporting the encoder's prediction) to 1–2 (p = 0.875). The fix is correct: the differences being compared were 10⁻¹⁶ to 10⁻⁹ round-off, and the 10⁻⁶ tolerance was already in the code (`e39bf3c`, before results) for the non-commuting count. It cuts against the quantum hypothesis, the verdict does not use the sub-test, and the QQ signature verdict does not depend on it. D32 also admits that the QQ pair selection on 37 of 40 items was fixed by round-off, so the "largest vs smallest non-commutativity" pairs are arbitrary there. This was already visible in the pilot, where all 10 pairs were at 0.000.
8. **The Kvam null is absence of evidence.** Δ_K's CI excludes effects beyond about −1.1 points, which is right at the size of Kvam et al.'s human effect (−1.19). The total-probability residual's CI, [−3.05, +4.15], was not reported. "Equals" and "unchanged" should be "no detectable difference".

## Overclaims to cut (exact sentences)
- `results/exp5-run-1.md:7`: "A tie is therefore the predicted outcome, not a surprise."
  - Why: §8.6 anticipated closeness on most claims; it did not predict a verdict.
  - Replace with: "The pre-registration (§8.6) anticipated that A5 and F5 would be close on most claims."
- `results/exp5-run-1.md:185`: "**The QQ equality is close but not certified.**"
  - Why: the pooled q cancels opposite-signed anchors. On anchor a alone, q = −0.345 [−0.517, −0.181].
  - Replace with: "**The pooled QQ statistic is near zero only because the two scale directions cancel.**"
- `results/exp5-run-1.md:185`: "On the 60 pairs, the mean q is +0.005, close to 0, but its interval [−0.058, +0.065] is just wider than the pre-registered ±0.05."
  - Why: as above.
  - Replace with: "On the 60 pairs, the pooled mean q is +0.005 [−0.058, +0.065], but by anchor direction it is −0.345 [−0.517, −0.181] (a, 32 pairs) and +0.241 [+0.118, +0.370] (b, 47 pairs); at the pre-registered cut of 70 the pooled value is −0.157 [−0.257, −0.053]."
- `results/exp5-run-1.md:186`: "Confidence after a mid-chain choice equals confidence after a matched filler (Δ_K = +0.29 [−1.12, +1.65]), the total-probability residual is +0.58 points, and A5⁰'s predicted signs agree on 53% of items, about chance."
  - Why: a null was read as equality.
  - Replace with: "Confidence after a mid-chain choice is not detectably different from confidence after a matched filler (Δ_K = +0.29 [−1.12, +1.65]; effects larger than about 1 point are excluded), the total-probability residual is +0.58 [−3.05, +4.15] points, and A5⁰'s predicted signs agree on 53% of items, about chance."
- `README.md:159`: "The verdict is a **tie**, as the pre-registration predicted (§8.6: "expect A5 and F5 to be close on most claims")."
  - Why: post-hoc framing (see hole 5).
  - Replace with: "The verdict is a **tie**: the primary interval includes 0 (F5 − A5 = +67 [−34, +212] rating points²), as the pre-registration (§8.6) anticipated was likely."
- `README.md:160`: "- Graded sequential ratings show large order effects: 60 of 80 adjacent pairs."
  - Why: about 27 of 80 pairs pass by chance.
  - Replace with: "- Graded sequential ratings show order effects: 40 of 80 adjacent pairs survive a Holm-corrected permutation test (60 pass the pre-registered OE > 0.10 rule, about 27 of them expected by chance)."
- `README.md:162`: "- There is no Kvam interference (Δ_K = +0.29 [−1.12, +1.65])."
  - Why: absence of evidence.
  - Replace with: "- No Kvam interference was detected (Δ_K = +0.29 [−1.12, +1.65]; effects beyond about 1 point of folded confidence are excluded)."
- `paper/record.md:40` (table cell): "order effects in 60 of 80 pairs"
  - Why: no noise floor.
  - Replace with: "order effects in 60 of 80 pairs (about 27 expected by chance; 40 survive Holm)".
- `paper/record.md:40` (table cell): "QQ mean q +0.005 [−0.058, +0.065], not certified; Kvam Δ_K = +0.29 [−1.12, +1.65], no interference"
  - Why: the pooled q is an artefact, and the Kvam result is a null.
  - Replace with: "pooled QQ mean q +0.005 [−0.058, +0.065] (anchor a alone −0.345 [−0.517, −0.181]); Kvam Δ_K = +0.29 [−1.12, +1.65], none detected".
- `paper/the-entangled-mind-v3.md:66`: "The order effects are large: 60 of 80 claim–question pairs show one above 0.10."
  - Why: no noise floor.
  - Replace with: "Order effects are real: 40 of 80 claim–question pairs survive a Holm-corrected permutation test (60 exceed 0.10, about 27 by chance)."
- `paper/the-entangled-mind-v3.md:67`: "A dynamic quantum belief state built from the encoder and a matched classical updater do not differ in predicting held-out ratings."
  - Why: wrong. On the held-out items they do differ (+207 [+52, +388]). On the test chains they are not distinguishable, with a CI up to +21% of MSE.
  - Replace with: "A dynamic quantum belief state built from the encoder and a matched classical updater could not be told apart on the test chains (F5 − A5 = +67 [−34, +212] rating points²)."
- `paper/the-entangled-mind-v3.md:68`: "A mid-chain choice left later confidence unchanged."
  - Why: absence of evidence.
  - Replace with: "A mid-chain choice did not detectably change later confidence (Δ_K = +0.29 [−1.12, +1.65])."
- `paper/the-entangled-mind-v3.md:244`: "The implementation details (D23–D24) and model details (D26) were fixed before any full-run data were examined."
  - Why: not checkable. 606 full-run conversations existed when D26's analysis commit was made.
  - Replace with: "The implementation details (D23–D24) were fixed before any call; the model details (D26) were committed while the full run was collecting (606 of its conversations existed by then), before any fitting or result."
- `paper/the-entangled-mind-v3.md:308` and `paper/the-entangled-mind-paper.md:296` (table cell): "Fixed before any full-run data were examined."
  - Why: as above.
  - Replace with: "Committed during full-run collection, before any fit or result."
- `paper/the-entangled-mind-v3.md:599`: "**Order effects are large.** 60 of 80 adjacent (claim, main) pairs have an order effect above 0.10 with an interval excluding 0, and the main-rating means span a median of 24.7 points across orders and omissions."
  - Why: no noise floor for either number.
  - Replace with: "**Order effects are real.** 60 of 80 adjacent (claim, main) pairs have an order effect above 0.10 with an interval excluding 0 (about 27 expected by chance; 40 survive a Holm-corrected permutation test), and the main-rating means span a median of 24.7 points across orders and omissions (13.2 expected from repeat noise alone)."
- `paper/the-entangled-mind-v3.md:602`: "- **So the signature is not present, and not contradicted.**"
  - Why: "not contradicted" holds only on the pooled, artefactual q.
  - Replace with: "- **So the signature is not present. It is not contradicted on the pooled data, but on run 1's single-scale conversations (anchor a, not a pre-registered subset) mean q is −0.345 [−0.517, −0.181], which would meet the contradiction rule.**"
- `paper/the-entangled-mind-v3.md:608`: "- **So there is no interference, and no commitment effect either.**"
  - Replace with: "- **So neither interference nor a commitment effect was detected.**"
- `paper/the-entangled-mind-v3.md:814`: "Large order and omission effects in experiment 5, where 60 of 80 claim–question pairs moved by more than 0.10."
  - Why: no noise floor. Also, the 60 of 80 are QQ pairs, not omission chains.
  - Replace with: "Order effects in experiment 5, where 40 of 80 claim–question pairs survive a Holm-corrected permutation test."
- `paper/the-entangled-mind-v3.md:822`: "A mid-chain decision leaves later confidence unchanged, which is what any read-out or Markov model predicts."
  - Replace with: "A mid-chain decision does not detectably change later confidence (Δ_K = +0.29 [−1.12, +1.65]), consistent with any read-out or Markov model."
- `paper/the-entangled-mind-v3.md:876`: "`paper/next-steps.md` fixed the reading of experiment 5's tie before the run: quantum probability adds nothing over a matched classical updater, in sequential judgment as in error prediction."
  - Why: a CI of [−34, +212] does not show "adds nothing".
  - Replace with: "`paper/next-steps.md` fixed the reading of experiment 5's tie before the run: no detectable advantage for quantum probability over a matched classical updater, in sequential judgment as in error prediction."
- `paper/the-entangled-mind-paper.md:151`: "60 of 80 claim–question pairs show an order effect above 0.10, and the main-rating means span a median of 24.7 points across orders and omissions."
  - Replace with: "60 of 80 claim–question pairs show an order effect above 0.10 (about 27 expected by chance; 40 survive a Holm-corrected permutation test), and the main-rating means span a median of 24.7 points across orders and omissions (13.2 from repeat noise alone)."
- `paper/the-entangled-mind-paper.md:152`: "The quantum belief state and its classical twin do not differ in predicting test-chain ratings: F5 − A5 = +67 [−34, +212] rating points²."
  - Replace with: "The quantum belief state and its classical twin could not be told apart in predicting test-chain ratings: F5 − A5 = +67 [−34, +212] rating points²."
- `paper/the-entangled-mind-paper.md:157`: "It predicted non-commuting sub-questions for only 12 of 160 claims, so the tie was predicted in the pre-registration (§8.6)."
  - Replace with: "It predicted non-commuting sub-questions for only 12 of 160 claims, so the pre-registration (§8.6) anticipated that A5 and F5 would be close."
- `paper/gold-map.md:7`: "Graded ratings show large order effects: a median span of 24.7 points, and 60 of 80 claim–question pairs above 0.10."
  - Replace with: "Graded ratings show order effects: a median span of 24.7 points (13.2 expected from noise), and 40 of 80 claim–question pairs significant after Holm correction."
- `DEVIATIONS.md:386` (heading): "## D26 — Experiment 5 model details left open by the frozen text (fixed before any full-run data were examined)"
  - Replace with: "## D26 — Experiment 5 model details left open by the frozen text (committed during full-run collection, before any fit or result)"

## Does the verdict stand?
Pre-registered verdict: **TIE** (§7.5, primary CI includes 0, no signature present, none contradicted on the pooled data). **STANDS WITH CAVEATS.** The primary statistic and its rule are exact and correctly applied. The substantive conclusion, no quantum advantage and no parameter-free quantum signature, survives every check. But the "none contradicted" leg uses the anchor-pooled q that the authors' own run 2 shows to be an artefact. On run 1's single-scale conversations, the QQ contradiction condition is met, which would make the §7.5 label "classical". So the choice between tie and classical is not settled, and the order-effect counts are overstated by the missing noise floor.

## Confidence
medium, high for every data-only statistic. All QQ, Kvam, gate and descriptive statistics were recomputed from raw conversations with independent code, including permutation noise floors and per-anchor splits. The primary MSEs were re-scored with the authors' model code (`exp5_models.predict`, network blocked) at the archived fitted parameters. The bootstrap, LOO and relative-scale analysis are mine, but I did not re-implement A5/F5 or refit the models. BA5 and A5⁰'s sign agreement were not re-derived.

## Tally
claims_checked: 22
claims_failed: 4
overclaim_sentences: 25
verdict: STANDS WITH CAVEATS
confidence: medium

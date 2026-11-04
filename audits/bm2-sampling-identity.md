# Audit: bm2-sampling-identity

**Files audited:** `results/bm2-sampling-identity.md`, `results/bm2-sampling-identity.json`, `results/bm2-calls.json`, `experiments/bm2-sampling-identity.md`, `experiments/bm_runs.py`, DEVIATIONS D43, `paper/biomimetic-map.md` §3.4; commits `999d81c`, `5ad7b24`, `605fa97`; citations in `README.md`, `paper/morning-brief.md`.
**Pre-registration:** `999d81c` (05:09:07), with the runner and analysis code (`bm2_run`, `bm2_analyse`), unchanged afterwards. Text in `experiments/bm2-sampling-identity.md` §§3–4. First call: 05:09:10 (decoded); last 05:11:08. Result `5ad7b24` 05:11:21 (13 s after the last call); "corrected reading" `605fa97` 05:11:39 (18 s later; prose only).
Timing verdict: OK for the pre-registration against the data. PROBLEM for the interpretation: the verdict prose was rewritten 18 s after the result, using a criterion the pre-registration did not freeze.

## Plain-English summary of the audit
The pre-registered numbers reproduce exactly: slope b +0.015 [−0.17, +0.16], intercept −0.032, mean Z −0.034 [−0.071, +0.002], conjunction fallacies on 8 of 16 items (6 of the 7 run-2 items), disjunction fallacies on 7, and SD–extremity r −0.54. The pre-registered verdict, "flat Z slope: coherent, affine or PT+N 2014", follows correctly from the rule. The "corrected reading" pushed 18 seconds later is a different matter. It uses the fallacy count, a "reported alongside" quantity, to pick PT+N 2014 out of the flat class. That step is not in the frozen text, and it contradicts the map's own summary of the model. By that summary (map §3.4), PT+N 2014's mean estimate is P + d − 2dP, an affine distortion of coherent probabilities. So it cannot produce a conjunction fallacy in mean ratings either, and only extra conjunction noise (Δd > 0, the version that predicts the slope) can. The robust mean-level fallacies (co05 +0.22, co06 +0.18, co-lin08 +0.11, co01 +0.05) therefore fit none of the three flat-class accounts. Four of the 8 "fallacies" are margins under 1 point on a 0–100 scale. "PT+N 2014 fits best" and "the signature of the original model" should be cut. The mean-Z equivalence test was "undetermined", so README's "cancel in the Costello–Watts identity" also overclaims.

## Claims checked
| # | claim (quoted or paraphrased, with file:line) | recomputed / evidence | status |
|---|---|---|---|
| 1 | Slope b = +0.015 [−0.165, +0.164]; a = −0.032 [−0.073, +0.019] (md:25) | b +0.0146, a −0.0321. My two-stage bootstrap gives b [−0.18, +0.16], a [−0.07, +0.02]; items-only bootstrap gives b [−0.17, +0.15]. Leave-one-item-out b −0.03 to +0.07; the reverse split gives +0.013 | holds |
| 2 | Mean Z −0.034 [−0.071, +0.002], "undetermined" (md:26) | −0.0336 [−0.071, +0.002]. Correctly undetermined against ±0.05 | holds |
| 3 | "The conjunction fallacy is there … on 8 of 16 items, including 6 of the 7 run-2 fallacy items." (md:10, :27) | 8 (co01, co02, co-lin06, co-lin08, co-lin09, co05, co06, co10); 6 of 7. The margins on co02, co-lin06, co-lin09 and co10 are +0.009, +0.005, +0.007 and +0.002 (under 1 point). With a per-item repeat bootstrap, 5 of 8 have a lower bound > 0 (co10's is +0.001); 4 are robust | holds (minor) |
| 4 | Disjunction fallacy on 7 (md:10, :27) | 7 | holds |
| 5 | SD against extremity r = −0.54 (md:13, :28) | −0.541 | holds |
| 6 | "Yet Z does not follow the sampler's slope … flat." (md:11) | The CI [−0.17, +0.16] excludes the size of slope the robust fallacies would need (Δd ≈ 0.2 implies b ≈ 0.4), so a large uniform Δd is disfavoured. It is still a null on 16 items | holds (minor) |
| 7 | "**Coherent probability** cannot produce the fallacies at all, so it is ruled out, along with any shared distortion of coherent values." (md:16) | Correct for the means, but the same argument also rules out PT+N 2014, whose mean is an affine distortion (map §3.4 "Conservatism: the mean estimate is P + d − 2dP") | holds, but see #8 |
| 8 | "**The original PT+N 2014 model fits best.** Its noise produces fallacies and then cancels in Z." (md:18) | PT+N 2014 noise produces fallacies only in individual noisy judgments (rate ≤ 50%, map §3.4). Mean ratings over 20 repeats are affine in P under PT+N 2014, so a margin of +0.22 (co05) is outside it. Contradicted by the map; not in the frozen reading | wrong |
| 9 | "The test separates the sampling family's variants." (md:21) | The flat slope disfavours the Δd versions; the mean-level fallacies disfavour the Δd = 0 versions. Nothing in the family fits both | overclaim |
| 10 | Commit `5ad7b24` "sampler not supported" against `605fa97` "PT+N 2014's signature" | A post-hoc change of interpretation 18 s after the result, without a DEVIATIONS entry. The pre-registered label stayed "flat: coherent, affine or PT+N 2014" | overclaim (process) |
| 11 | README.md:34 "Ratings that commit the conjunction fallacy yet cancel in the Costello–Watts identity (Z = −0.03, flat slope)." | The equivalence test is undetermined; half of the 8 "fallacies" are under 1 point | overclaim |
| 12 | morning-brief.md:75 "That is the signature of the original 'probability theory plus noise' model." | As #8 | wrong |
| 13 | morning-brief.md:134 "Its ratings obey a noise-cancelling identity despite its fallacies (10)." | Equivalence undetermined | overclaim |
| 14 | "That is close to Costello & Watts' human values" (md:12) | Human X_E 0.0066 and −0.039 (map §3.4) against −0.034 | holds |

## Holes found
1. **The "corrected reading" is post hoc and theoretically inconsistent.** The frozen reading (§4) puts coherent, affine and PT+N 2014 in one flat class and uses only the slope. Eighteen seconds after the result, the write-up used the mean-level fallacy count to eliminate "coherent … along with any shared distortion" and keep PT+N 2014. But PT+N 2014's expected estimate, (1 − 2d)P + d, *is* a shared affine distortion, and the map (§3.4, line 231) says extra noise "is the condition both models need to reach above-chance fallacy rates". Mean-level fallacies of +0.11 to +0.22 therefore exclude PT+N 2014 as much as coherence. The data fit no pre-registered account cleanly. (This is reasoned from the map's own summary of Costello & Watts 2014 and Zhu et al. 2020; I did not re-read those papers.)
2. **The fallacy count is inflated by ties at the floor.** Four of the 8 items have margins of 0.2–0.9 points on a 0–100 integer scale (co10: 0.030 against 0.028). Those are within repeat noise. A defensible count is 4–5 of 16.
3. **"Cancel" from an undetermined equivalence test.** Mean Z −0.034 [−0.071, +0.002] does not lie within ±0.05. README and the brief present cancellation as established and list it under "What is stable".
4. **The verdict flip.** The commit headline went from "sampler not supported" (`5ad7b24`) to the corrected prose (`605fa97`), which now says the test "separates the sampling family's variants" and that PT+N 2014 "fits best". No DEVIATIONS entry records the change.
5. **Multiple comparisons:** 3 CIs, 2 counts and 1 correlation. Nothing is reported as positive, so this is not a concern here.

## Overclaims to cut (exact sentences)
- `results/bm2-sampling-identity.md:18` — "- **The original PT+N 2014 model fits best.** Its noise produces fallacies and then cancels in Z." — PT+N 2014's mean is affine in P, so it cannot give mean-level fallacies (map §3.4); not in the frozen reading — replace with: "- **No pre-registered account fits both facts.** Mean-level fallacies rule out coherent, affine and PT+N 2014 (whose mean is affine); the flat slope disfavours the extra-noise versions."
- `results/bm2-sampling-identity.md:21` — "The test separates the sampling family's variants. It does not show that the model samples." — replace with: "The slope test is flat, as pre-registered; the fallacy pattern is not explained by any account in the flat class."
- `results/bm2-sampling-identity.md:10` — "- **The conjunction fallacy is there.** The model rates \"A and B\" above the less likely of A and B on 8 of 16 items, including 6 of the 7 run-2 fallacy items." — four of the 8 margins are under 1 point — replace with: "- **The conjunction fallacy is there.** The mean rating of \"A and B\" exceeds the less likely conjunct on 8 of 16 items, but by under 1 point on 4 of them; it is clear on 4 (co05, co06, co-lin08, co01)."
- `README.md:34` — "- Ratings that commit the conjunction fallacy yet cancel in the Costello–Watts identity (Z = −0.03, flat slope)." — equivalence undetermined — replace with: "- Ratings that commit the conjunction fallacy on some items, with Z near zero (−0.03 [−0.07, +0.00]; the ±0.05 equivalence test is undetermined) and no item-level slope."
- `paper/morning-brief.md:75` — "    - That is the signature of the original \"probability theory plus noise\" model." — wrong by the map's own summary — cut.
- `paper/morning-brief.md:134` — "- Its ratings obey a noise-cancelling identity despite its fallacies (10)." — replace with: "- Its ratings come close to a noise-cancelling identity (equivalence undetermined) (10)."

## Does the verdict stand?
Pre-registered reading: **flat Z slope: coherent, affine or PT+N 2014** (secondary: mean Z undetermined). The rule is applied correctly and the numbers reproduce, so the pre-registered verdict **STANDS WITH CAVEATS**: the slope is flat on 16 items. The post-hoc "corrected reading" that singles out PT+N 2014 is **wrong** and should be withdrawn. With the robust mean-level fallacies it is inconsistent with every member of the flat class.

## Confidence
High for the recomputation: every statistic was rebuilt from `bm2-calls.json` with my own bootstraps. Medium for hole 1, which rests on the map's own summary of PT+N 2014 (mean = P + d − 2dP; extra noise needed for above-chance fallacies) rather than a fresh read of the papers.

## Tally
claims_checked: 14
claims_failed: 6
overclaim_sentences: 6
verdict: STANDS WITH CAVEATS
confidence: high

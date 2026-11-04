# Audit: frame-fix-check

**Files audited:** `results/frame-fix-check.{md,json}` (camp statistics; exact noiseless scores for the 80 run-2 test items under 4 solvers × 2 arms), `experiments/frame_fix_check.py`, `src/entangled_mind/encoder.py` (`pin_frame`, `solve_phases_anchored`), `results/pool-run-3.json`, `results/stage2-run-2.json`, DEVIATIONS D15. Citations: README.md:229; paper/record.md:28; paper/the-entangled-mind-v3.md:176–179, 288, 776; paper/the-entangled-mind-paper.md:287.
**Pre-registration:** none; it is declared exploratory ("Not pre-registered"). D15, the script, the encoder changes and the results all arrive in one commit, `ab929fe` (11-03 18:08:59). No API calls.
Timing verdict: OK for an exploratory check, with one unverifiable claim. D15's "This rule [λ = max(1, largest total coupling)] was fixed before its AUROC was computed" cannot be checked, because rule and result share a commit.

## Plain-English summary of the audit
The numbers hold. From the archived exact scores I get the same AUROCs (A0 0.488 → 0.473 with the correction, C 0.684 → 0.674) and the same intervals. A paired bootstrap shows the correction's effect is nil within noise (A0 −0.015 [−0.054, +0.016]; C −0.010 [−0.061, +0.047]). So "the frame bug does not explain the poor error detection" is supported for the entangled arm on this set. The camp-geometry percentages match the JSON. Two small statements elsewhere are off. "20% of run-2 items" is 20% of the 225 items that have both a yes and a no camp, which is 44 of 300 (15%) of all run-2 items. And v3 says the defect was "found after all pre-registered runs", but v2, v2.1, experiments 4–5, the Sonnet scoring and the overnight runs all came later. One decision also rested on the run-2 test items: the run-2 test AUROCs were used to decide not to fold the correction into v2.1, and the same 80 items were later used as v2/v2.1's "held-out set". Because the decision was to change nothing, this gives no advantage.

## Claims checked
| # | claim (quoted or paraphrased, with file:line) | recomputed / evidence | status |
|---|---|---|---|
| 1 | AUROCs on run-2 test (exact noiseless): A0 0.49 [0.35, 0.62] → 0.47 [0.34, 0.61] (λ) → 0.47 (∞); C 0.68 → 0.67 → 0.67 (frame-fix-check.md table; D15) | From archived scores (my AUROC, 4k stratified bootstrap): A0 0.488 [0.36, 0.62], 0.489 (pin), 0.473 [0.35, 0.60], 0.466; C 0.684 [0.56, 0.80], 0.679, 0.674 [0.55, 0.79], 0.667 | holds |
| 2 | "it does not change the AUROCs" / "leaves error detection unchanged" (D15; README:229; v3:178; record:28) | Paired: A0 anchored − before −0.015 [−0.054, +0.016]; C −0.010 [−0.061, +0.047]. Effect indistinguishable from 0 and at most ≈ 0.05 | holds |
| 3 | "The frame bug is real, but it does not explain the entangled arm's poor error detection." (D15) | After the correction, C − A0 is still +0.200 [+0.015, +0.379] (exact noiseless, paired) | holds |
| 4 | Camp statistics: yes camp > 30° off 20% → 7% (λ) → 0%; separation < 90° 20% → 7%; 10th-percentile separation 0° → 147° (table) | JSON: 0.196 → 0.067 → 0; 0.204 → 0.067; sep p10 0.0 → 147.1 (n = 225) | holds (from archive; phases not re-solved) |
| 5 | "at least 10% have fully merged camps" (D15) | 10th-percentile separation is 0.0°, so ≥ 10% have separation ≈ 0 | holds |
| 6 | "in 20% of run-2 items the yes camp sits more than 30° off the readout axis" (v3:176); "on about 20% of items" (README:229) | The 20% is of the 225 items with both camps. That is 44 items, or 14.7% of the 300 run-2 items | overclaim (minor) |
| 7 | "A known defect (D15, found after all pre-registered runs)" (v3:176) | Found at 18:08. Later pre-registered results include v2 (18:50), v2.1 (19:32), experiment 4 runs 2–3, experiment 5, the Sonnet scoring and the overnight runs (record.md) | wrong |
| 8 | "Fix 1, a rigid frame pin, does not work … changed nothing material" (D15) | Camp shares unchanged (0.196, 0.204); AUROC A0 0.488 → 0.489 | holds |
| 9 | "The relation judge marks 'supports' between claims that lean opposite ways" (D15 mechanism) | 428 of 5,068 positive-strength `supports` edges in run 3 (8.4%) join opposite-leaning claims, so the mechanism's precondition is present. Not tested as the cause | holds (minor) |
| 10 | "This rule was fixed before its AUROC was computed." (D15) | same commit as the result | not checkable |
| 11 | "Every archived result uses the solver as run." (v3:179) | True of v1/v2/v2.1. Experiment 5 uses the anchored solver by its own pre-registration (`8a55bb7`), which record.md:28 notes | holds (minor) |

## Holes found
1. **"Found after all pre-registered runs" (v3:176) is false.** Most pre-registered results in the project post-date 18:08.
2. **The denominator in "20% of run-2 items" is wrong.** It is 20% of the 225 two-camp items (15% of all 300).
3. **Run-2 test items were used for a design decision.** D15's disposition (do not add the correction to v2.1) was made on the run-2 test-set AUROCs. Those 80 items were then used as v2/v2.1's secondary held-out set. The decision was "no change", so there is no leakage benefit, but the set is no longer untouched.
4. **The λ rule's "fixed before" claim is unverifiable** (same commit).

## Overclaims to cut (exact sentences)
- `paper/the-entangled-mind-v3.md:176` — "**A known defect (D15, found after all pre-registered runs).** The phase solve's lean anchors are weak against the relation couplings, so in 20% of run-2 items the yes camp sits more than 30° off the readout axis." — replace with "**A known defect (D15, found after Stage 2 and before v2's locked-test result).** The phase solve's lean anchors are weak against the relation couplings, so in 20% of the 225 run-2 items with both a yes and a no camp (44 of 300 items) the yes camp sits more than 30° off the readout axis."
- `README.md:229` — "   - A frame correction (D15): the phase solver's camps drift off the yes/no axis on about 20% of items because the lean anchors are weak. Stronger anchors fix the geometry but leave error detection unchanged." — replace "on about 20% of items" with "on about 20% of the run-2 items that have both camps (15% of all run-2 items)".

## Does the verdict stand?
No pre-registered verdict. The exploratory conclusion, that the frame defect is real but the correction leaves AUROC unchanged within noise, **STANDS**.

## Confidence
High for the AUROCs and paired intervals, recomputed from the archived exact scores. Medium for the camp statistics: I checked them against the JSON and the 10/90 percentile logic but did not re-solve the phases.

## Tally
claims_checked: 11
claims_failed: 2
overclaim_sentences: 2
verdict: STANDS
confidence: high

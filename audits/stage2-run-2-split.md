# Audit: stage2-run-2-split

**Files audited:** `results/stage2-run-2-split.{md,json}`, `experiments/split_analysis.py` (read only), `results/stage2-run-2.json`, `results/stage2-run-2b.json`, `results/arm-g-confidence.json`, `results/pool-run-3.json`. Citations: README.md:104, paper/the-entangled-mind-v3.md:369–380.
**Pre-registration:** none. The file calls itself descriptive ("nothing is fitted", "read them as descriptive"). It was committed in `a9ed076` (11-03 19:27:01) after all run-2/2b data existed; the code first appeared in `930730c` (16:26:03), after the run-2 and arm-G data existed. First call: n/a (re-scoring).
Timing verdict: OK for what it claims (exploratory); the subgroups were chosen after the run-2 results were known.

## Plain-English summary of the audit
Every cell recomputes exactly: subgroup sizes, flags and AUROCs. The file itself is careful and says the groups are small and descriptive. The README and v3 citations are less careful. "Shows the same pattern within SimpleQA, within science, and within items with 3 or more contradictions" holds only for point estimates. No within-group contrast I tested has a 95% interval that excludes zero: in SimpleQA, G − C is +0.02 [−0.15, +0.20], and in science, C − A is +0.05 [−0.09, +0.19]. The README also leaves out the fourth group (fewer than 3 contradictions), where A beats D. "Self-reported confidence is the best arm in every group" is true of point estimates, but in SimpleQA G and C are tied.

## Claims checked
| # | claim (quoted or paraphrased, with file:line) | recomputed / evidence | status |
|---|---|---|---|
| 1 | Group sizes: SimpleQA 22/19, science 18/16, claim 0/5, ≥3 contradictions 29/24, <3 11/16 | identical (science = chemistry + physics; contradictions = count of `contradicts` edges with strength > 0) | holds |
| 2 | All flag counts and AUROCs in the five tables | 0 mismatches over 35 cells, using my own scores and thresholds | holds |
| 3 | "Small groups give wide intervals; read them as descriptive." (split.md:3) | correct framing | holds |
| 4 | "shows the same pattern within SimpleQA, within science, and within items with 3 or more contradictions" (README.md:104) | Within-group paired bootstraps (4k): SimpleQA G − C +0.019 [−0.152, +0.200], C − A +0.190 [−0.045, +0.427]; science C − A +0.052 [−0.090, +0.194], G − E +0.177 [−0.031, +0.396]; ≥ 3 contradictions G − D +0.073 [−0.122, +0.269], D − A +0.154 [−0.022, +0.325]. None excludes 0. The omitted group (< 3 contradictions) has A 0.63 > D 0.58 | overclaim |
| 5 | "Self-reported confidence is the best arm in every group." (v3:378) | Point estimate: yes (0.74, 0.89, 0.75, 0.93). In SimpleQA G 0.74 vs C 0.72 (+0.02 [−0.15, +0.20]): a tie | overclaim (minor) |
| 6 | "The entangled readout is near chance in every group." (v3:379) | A: 0.53, 0.56, 0.52, 0.63; every interval includes 0.5 | holds |
| 7 | "Items whose webs contain many contradictions, where an entangled representation should matter most, are not an exception." (v3:380) | A 0.52 [0.36, 0.66] in the ≥3 group | holds |
| 8 | Claim items: 0 wrong / 5 right, AUROC undefined | Haiku got 0 of 60 claims wrong; all 5 test claims are right items, so the pooled test mixes in an item type with no errors | holds (finding: pooled AUROC is partly a type contrast) |

## Holes found
1. **Subgroup "same pattern" is a point-estimate claim, and the reporting is selective.** No within-group contrast is significant. The README names three of the four groups and leaves out the one where A beats D.
2. **Five subgroups × seven arms = 35 AUROCs with no correction.** The file labels them descriptive. The citing text treats agreement across groups as confirmation.
3. **The pooled test set mixes item types with very different error rates** (claims 0/60 wrong). The per-type tables are the right control for this. They show G's lead over C vanishing in SimpleQA, the largest type (41 of 80 test items).

## Overclaims to cut (exact sentences)
- `README.md:104` — "- The split analysis ([`results/stage2-run-2-split.md`](results/stage2-run-2-split.md)) shows the same pattern within SimpleQA, within science, and within items with 3 or more contradictions." — replace with "- The split analysis ([`results/stage2-run-2-split.md`](results/stage2-run-2-split.md)) shows the same ordering of point estimates within SimpleQA, within science and within items with 3 or more contradictions, but no within-group difference is significant (in SimpleQA, G and C tie: 0.74 vs 0.72), and in items with fewer than 3 contradictions A scores above D."
- `paper/the-entangled-mind-v3.md:378` — "- Self-reported confidence is the best arm in every group." — replace with "- Self-reported confidence has the highest point estimate in every group, tied with arm C in SimpleQA (0.74 vs 0.72)."

## Does the verdict stand?
No pre-registered verdict. The descriptive tables **STAND** exactly as computed. The citing sentences overstate them.

## Confidence
High. Every cell was recomputed from the raw scores; the within-group paired intervals are my own.

## Tally
claims_checked: 8
claims_failed: 2
overclaim_sentences: 2
verdict: STANDS WITH CAVEATS
confidence: high

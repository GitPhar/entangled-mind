# Audit: exp5-pilot

**Files audited:** `results/exp5-pilot.json`, `results/exp5-pilot.md`, the pilot conversations in `results/exp5-conversations.json` (keys h018, h088, h039, h001, h170), `experiments/exp5_run.py` (`gates`), `experiments/exp5-sequential-judgment.md` §7.1, DEVIATIONS D22–D24.
**Pre-registration:** `2c2ef6c` (20:15:54), text in `experiments/exp5-sequential-judgment.md` §7.1 (gate rules G1, G2), pilot items fixed by D22 in the same commit; G1's SD-cell rule and G2's "either question, either order" rule fixed in D23 (`2ad710c`, 20:18:09); h001's 4th slot fixed in D24 (`97dde55`, 20:18:37). First call: 20:18:49 decoded (last pilot call 20:29:35; pilot commit `8881a0a` 20:29:58).
Timing verdict: OK. Every gate rule and the code that computes it were committed before the first pilot call (by 40 s for D23, 12 s for D24).

## Plain-English summary of the audit
The pilot gates were written down before the pilot and the reported numbers are exactly right. Both gates passed, 5 of 5 items and 10 of 10 pairs. But G1 was built so that it could hardly fail. A spread of 5 points between the means of nine sets of 10 noisy ratings happens by chance on 98–100% of these items, even when the question order has no effect. So "G1 pass" shows only that the ratings are noisy, not that they move with the sequence. A proper permutation test does find real chain-type effects on 3 of the 5 items (h018, h039, h170), which happens to meet G1's "at least 3" count. The pilot also showed, before the full run, that every pilot QQ pair had a predicted non-commutativity of 0.000. The "largest versus smallest" pair design was empty before the money was spent. Nothing needs to be cut, but the gate should not be cited as evidence that the ratings track the sequence.

## Claims checked
| # | claim (quoted or paraphrased, with file:line) | recomputed / evidence | status |
|---|---|---|---|
| 1 | G1 per-item spans 23.6, 9.8, 73.8, 14.0, 56.5; SD≥2 shares 89%, 41%, 50%, 78%, 94% of 80 cells (exp5-pilot.md:9-13) | recomputed from the raw conversations: identical (cells = chain × position × anchor, S ratings, ddof=1) | holds |
| 2 | "G1: PASS (5 of 5 items; the rule needs at least 3)" (exp5-pilot.md:15) | 5/5 recomputed; rule as frozen in §7.1 | holds |
| 3 | G2 minority shares 40/50/15/12/35/30/48/48/40/50% (exp5-pilot.md:21-30) | recomputed: 0.40, 0.50, 0.15, 0.12, 0.30/0.35, 0.475, 0.475, 0.50, 0.40 (h001 0.475 rounds to 48%) | holds |
| 4 | "G2: PASS (10 of 10 pairs)" (exp5-pilot.md:32) | 10/10 | holds |
| 5 | All 10 pilot pairs have predicted \|sin Δφ\| = 0.000 (exp5-pilot.md:21-30) | as printed. The "largest and smallest non-commutativity" pairs were indistinguishable on every pilot item | holds (shows the design was degenerate before the full run) |
| 6 | "Pilot data are reported but never used in any test" (exp5-pilot.md:3) | no test uses them. They were read for the gates before D26's model details and the D26 addendum were committed (20:32–20:34) | holds (minor) |
| 7 | Record: "G1 pass … the ratings move with sequence" (paper/record.md:36) | G1's span criterion passes under a no-order-effect null (chain labels permuted within anchor) with P(span ≥ 5) = 0.98, 1.00, 1.00, 0.99, 1.00. Permutation p for the observed spans: h018 < 0.001, h088 0.455, h039 < 0.001, h001 0.131, h170 < 0.001 | holds (minor): true for 3 of 5 items by a proper test, not by G1 |

## Holes found
1. **G1 is close to vacuous.** The span arm (main-rating means across 9 chains span ≥ 5 points) is met by sampling noise alone. With 10 ratings per chain (5 per anchor), the permutation-null median span is 9.5–24.4 points on these items, and P(null span ≥ 5) ≥ 0.98 on every item. So G1 could not have stopped the run unless the model had been fully deterministic. The pre-registration presented G1 as the experiment's go/no-go test of whether "the base model's ratings … move with sequence" (§7.1), and it cannot test that. A permutation test that does test it is positive on 3 of 5 items.
2. **G2 pools anchors that the model did not reverse.** The minority share is computed on recoded ratings pooled over both anchor directions. The full run later showed the model largely ignores the reversed anchor (B0 33.8 vs 71.3). So part of each minority share may be scale confusion rather than genuine dispersion: h088's 15% and 12% are plausibly of this kind, given its main means of about 3. G2 passed with a wide margin, so this does not change the gate.
3. **The pilot exposed the a priori design's degeneracy before the full run.** All 10 pilot pairs had \|sin Δφ\| = 0.000. The full run went ahead 14 s after the pilot commit, with the same pair-selection rule. In the full run 37 of 40 items then had tied predictions (D32). That is consistent with §8.6's expectation, not a rule breach, but the a priori QQ sub-test was known to be close to empty before any full-run call.

## Overclaims to cut (exact sentences)
None in `results/exp5-pilot.md`. Optional precision in `paper/record.md:36` (table cell): "the ratings move with sequence". Why: G1 cannot show this. Suggested replacement: "the ratings are dispersed (G1's span rule is met by noise alone; a permutation test finds chain-type effects on 3 of 5 items)". Not counted below as an overclaim, because the substance holds on 3 of 5 items.

## Does the verdict stand?
Pre-registered outcome: G1 PASS, G2 PASS, so the full run proceeds. **STANDS WITH CAVEATS.** The gates were frozen before the pilot, and the arithmetic is exact. But G1 was too weak to stop the run, so its pass carries almost no information. The real dispersion evidence is the permutation result on 3 of 5 items.

## Confidence
high. Every pilot number was recomputed from the raw archived conversations with independent code, and the noise-floor simulation uses only the archive.

## Tally
claims_checked: 7
claims_failed: 0
overclaim_sentences: 0
verdict: STANDS WITH CAVEATS
confidence: high

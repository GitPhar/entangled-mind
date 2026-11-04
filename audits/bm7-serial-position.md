# Audit: bm7-serial-position

**Files audited:** `results/bm7-serial-position.md`, `results/bm7-serial-position.json`, `results/exp5-conversations.json` (O1–O4, anchor a), `experiments/split-exp5.json`, `results/pool-run-3.json`, `experiments/bm7-serial-position.md`, `experiments/bm_offline.py` (`bm7`), DEVIATIONS D41; citations in `paper/morning-brief.md`, `paper/biomimetic-map.md`.
**Pre-registration:** `3c38abd` (05:08:33), text in `experiments/bm7-serial-position.md` §§3–4. The analysis code (`bm7()` in `bm_offline.py`) was committed earlier, in `9c29a94` (05:08:07), and never changed. First call: none, archival (exp5 calls 11-03 20:18–21:50). Result `7365313` 05:08:49, 16 s after the pre-registration, with hand-written prose.
Timing verdict: PROBLEM (unverifiable). The code was frozen before the text, so the statistic is protected, but results and prose appear 16 s after the "frozen" commit. The archive had been analysed before for experiment 5 and direction 9, though not for per-position weights.

## Plain-English summary of the audit
Everything reproduces exactly: 800 conversations, 40 items, weights +4.31/+3.97/+3.23/+2.00, u₁ +0.71 [−2.30, +4.26], u₄ −1.60 [−4.70, +1.13], w₁ − w₄ +2.31 [−1.65, +7.26]. The pre-registered reading "monotone or flat (flat): consistent with the LCA" follows from the rule. "No U-shape" is reasonably supported, not merely unrefuted: u₄'s upper bound (+1.1 points) excludes a last-position bump of more than about a third of the middle weights. "LCA survives" is fine as "not falsified". One wording error: "2–4 points across the full range of the model's own sub-rating" is per unit of evidence, which is 50 rating points. Across the full 0–100 range the effect is 4–9 points. The link to direction 2 ("questions matter more than the numbers") is interpretation that this test does not address.

## Claims checked
| # | claim (quoted or paraphrased, with file:line) | recomputed / evidence | status |
|---|---|---|---|
| 1 | Weights +4.3 [+0.1, +9.8], +4.0 [+0.9, +7.8], +3.2 [+0.4, +7.0], +2.0 [−0.4, +4.8] (md:22-25) | +4.31 [+0.14, +9.77], +3.97 [+0.87, +7.76], +3.23 [+0.36, +7.03], +2.00 [−0.45, +4.78] | holds |
| 2 | u₁ +0.7 [−2.3, +4.3]; u₄ −1.6 [−4.7, +1.1] (md:27) | Exact | holds |
| 3 | "**No U-shape**, so the LCA survives this test." (md:10) | Both pre-registered contrasts include 0, and u₄ is negative with upper bound +1.1. "Survives" = not falsified | holds (minor) |
| 4 | "Each position moves the final verdict by only 2–4 points across the full range of the model's own sub-rating." (md:11) | Weights are per unit x = (rating − 50)/50, so per 50 points. The full range (x from −1 to +1) moves M by 4–9 points | wrong (factor 2) |
| 5 | "Within a question, the verdict barely tracks the sub-ratings the model just gave." (md:11) | Within-item R² = 0.074 | holds |
| 6 | w₁ − w₄ +2.3 [−1.6, +7.3], "faint first-heavy … not reliable"; trend −0.77 [−2.35, +0.51] (md:12, :28) | Exact | holds |
| 7 | "That fits direction 2: the questions being asked matter more than the numbers the model gives in answer to them." (md:14) | Small weights on self-stated sub-ratings are also expected if M depends on the claims' content rather than the stated numbers. This test does not compare questions with numbers | overclaim |
| 8 | morning-brief.md:70 "at 2–4 points each" | As #4 | wrong (minor) |
| 9 | morning-brief.md:70 "The competing-accumulator account survives." | As #3 | holds (minor) |

## Holes found
1. **Units.** "2–4 points across the full range" understates the full-range effect by a factor of 2. The weight is per 50 rating points.
2. **Weak power for small U-shapes.** The CI widths of u₁ and u₄ are 6.6 and 5.8 rating points per unit, larger than the weights themselves (2–4). A U-shape of the weights' own size is excluded on the u₄ side only. "No U-shape" should read "no U-shape detected; a last-position bump above about 1 point per unit is excluded".
3. **The evidence is endogenous.** x_p is the model's own stated rating, not a manipulation. The weights are associations between stated sub-ratings and M within an item, and are confounded by conversation-level drift. The Latin square balances claim against position but not this drift. This limits the "how weakly the verdict depends on" sentence.
4. **Timing and process:** as for D40/D42. The code was frozen in `9c29a94`, but results and prose came 16 s after the pre-registration text.
5. **Multiple comparisons:** 8 CIs are reported. Only the pre-registered u₁ and u₄ (and w₁ − w₄ for the shape label) decide the reading, and none is reported as a positive finding.

## Overclaims to cut (exact sentences)
- `results/bm7-serial-position.md:11` — "- **The weights are small.** Each position moves the final verdict by only 2–4 points across the full range of the model's own sub-rating." — units are per 50 points — replace with: "- **The weights are small.** Each position moves the final verdict by only 2–4 points per 50 points of the model's own sub-rating (4–9 points across its full range)."
- `results/bm7-serial-position.md:14` — "That fits direction 2: the questions being asked matter more than the numbers the model gives in answer to them." — not tested here — cut.
- `paper/morning-brief.md:70` — "The striking part: the model's final verdict barely tracks the four sub-ratings it just gave, at 2–4 points each." — replace with: "The striking part: the model's final verdict barely tracks the four sub-ratings it just gave, at 2–4 points per 50 points of sub-rating."

## Does the verdict stand?
Pre-registered reading: **monotone or flat (flat): consistent with the LCA**. **STANDS.** No U-shape is detected, and a sizeable last-position bump is excluded. This is a non-falsification, not support.

## Confidence
High. The full regression and the 2,000-resample cluster bootstrap were recomputed from the raw exp-5 conversations with my own code, and the numbers match to two decimals.

## Tally
claims_checked: 9
claims_failed: 3
overclaim_sentences: 3
verdict: STANDS
confidence: high

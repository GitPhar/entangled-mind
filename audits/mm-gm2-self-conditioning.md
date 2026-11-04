# Audit: mm-gm2-self-conditioning

**Files audited:** `results/mm-gm2-self-conditioning.{md,json}`, `results/mm-gm2-{sonnet,opus}-conversations.json`, `results/mm-gm2-{sonnet,opus}-planted.json`, `results/mm-gm2-opus-cap.json`, `results/mm-batches-gm2-*.json`, `results/gm2-conversations.json` (Haiku reference), `experiments/mm-gm2-self-conditioning.md`, `experiments/mm_gm2.py`, `experiments/gm2_self_conditioning.py`, DEVIATIONS DM4, DM4a, DM5; citing text in `results/multi-model.md`, `paper/no-credence-to-read.md`, `paper/morning-brief.md`.
**Pre-registration:** `dea966b` (07:48:27), text in `experiments/mm-gm2-self-conditioning.md` and DEVIATIONS DM4. The amendment DM4a is `a9e1e7b` (07:49:52) and changes only the Opus cap code. Calls were decoded from the `msg_01…` IDs (`scratchpad/g8/msgtime2.py`). Sonnet waves 1–6 ran 07:50:47–08:24:23. Opus waves ran 08:26:43–08:42:17, after every other DM2/DM3/DM4 call had finished, as DM4a requires. The Opus cap file computed $11.393 of other spend, giving a cap of $8.5069, which matches my sum of the archived costs. The result commit is `82c5d91` (08:43:51).
Timing verdict: **OK by git and message IDs.** There is a documentation PROBLEM. DM4 says "Date: 08:10 MST, before any call", but Sonnet's calls began at 07:50:47. DM4a says "Date: 08:20 MST. No DM4 call had been made"; by 08:20, five Sonnet waves had already run. The commit times (07:48:27 and 07:49:52) are what make both claims true.

## Plain-English summary of the audit
All headline numbers reproduce from the raw conversations with my own variance-component, permutation and bootstrap code. Sonnet's *question-driven* reading holds by the pre-registered rule. It is concentrated, though: it comes mostly from two items (h191 and h112) where, with the record hidden, Sonnet's final rating jumps to the opposite end of the scale, about 90 against about 3 when shown. That looks at least partly like a reaction to the "[rating recorded]" placeholder, which the prereg admits it cannot separate. Dropping h058 instead puts the interval across 0.5. Opus's *leaning question-driven* rests on one item. Without h058 its ratio is 0.14 [0.00, 0.46], which the pre-registered rule would call *self-anchoring*. So "on Opus the test is not decisive" is right, but the sentence saying Opus "barely shows an order effect at all" is contradicted by its gate (p = 0.004, smaller than Sonnet's 0.031). The memory reading (repeat agreement falls by more than 10 points when the first answer is hidden) holds on all three models, with intervals excluding zero. The planted-value results do not consistently show the record pulling answers: Sonnet's b_MF interval includes 0, and Opus's final rating moves *away* from planted values.

## Claims checked
| # | claim (quoted or paraphrased, with file:line) | recomputed / evidence | status |
|---|---|---|---|
| 1 | Sonnet: gate p 0.031, OE shown 6.1, redacted 17.9, R = 2.95 [0.99, 12.55], *question-driven* (`results/mm-gm2-self-conditioning.md` table) | OE 6.08 / 17.92, R 2.95. My permutation p 0.030; my bootstrap [0.88, 13.23] with a different seed; the authors' seed gives [0.99, 12.55]. The CI lower bound is ≥ 0.5 in both, so *question-driven* | holds |
| 2 | Opus at R = 2: gate p 0.004, OE 4.4 / 4.1, R = 0.93 [0.06, 7.31], *leaning question-driven* | 4.44 / 4.14, R 0.93, p 0.005, [0.06, 7.37] | holds |
| 3 | Haiku reference at R = 4: R = 2.01 [1.04, 4.43], gate 0.0008 | 2.01 [1.03, 4.44], p 0.0007 | holds |
| 4 | MF agreement shown → redacted: 78% → 25%, 88% → 35%, 95% → 65% | 31/40 → 10/40; 35/40 → 14/40; 19/20 → 13/20. Item-bootstrap CI of the drop: Haiku [0.28, 0.78], Sonnet [0.30, 0.75], Opus [0.05, 0.55] | holds |
| 5 | b_MF 1.23 / 0.39 / 0.35 | 1.23 / 0.39 / 0.35 | holds |
| 6 | "Sonnet's redacted order effect comes mostly from h191 (42 points) and h112 (30 points); … Opus's redacted effect is one item, h058 (13 points)" (`results/multi-model.md`, Notes) | 42.4, 30.0; Opus h058 12.9. Leave-one-item-out: Sonnet without h191 gives R 1.95 [0.62, 7.77]; without h058, 4.09 [0.44, 17.34] (**crosses 0.5**). Opus without h058 gives **0.14 [0.00, 0.46]**, which would read *self-anchoring* | holds (understated) |
| 7 | "Opus barely shows an order effect at all: 4.4 points, against Sonnet's 6.1 and Haiku's 9.3" (`results/multi-model.md:21`) | Opus gate p = 0.004 (shown order effect significant, more so than Sonnet's 0.031). The OE CIs overlap: 4.4 [0.8, 6.9], 6.1 [1.7, 8.9], 9.3 [4.4, 13.2] | overclaim |
| 8 | "The question alone constructs the judgment on Sonnet (R = 2.95 [0.99, 12.55])" (`paper/no-credence-to-read.md:30`; `paper/morning-brief.md:118`) | Holds by the rule. The mechanism word "constructs" is stronger than "the order effect survives redaction", and the effect is 2 items deep with possible placeholder artefacts | holds (minor) |
| 9 | "Reliance on the model's own record holds on all three" (`paper/no-credence-to-read.md:28, :316`; `paper/morning-brief.md:113`) | The memory criterion holds on every model (claim 4). The planted-value pull is weaker: Sonnet b_MF [−0.05, 0.76]; next-rating pull Sonnet [−0.5, 5.5] and Opus [−1.5, 2.9]; Opus final-M shift −10.0 [−17.1, −3.1], away from the plant | holds (minor) |
| 10 | DM5: projection $8.74 at R = 3 exceeded the $8.51 cap; R = 3 "would in fact have fitted" | From archived costs: wave-1 cost per call about $0.00205, projection about $8.68 at R = 3; actual cost at R = 3 would have been about $6.5 | holds |
| 11 | Spend Sonnet $2.19, Opus $4.89; 800 / 400 complete | $2.189 / $4.889; 0 refusals, 0 max_tokens | holds |
| 12 | Planted values from own wave-1 ratings, n = 16 each, fixed after wave 1 | The planted files show n = 16 per S_k and M. Wave 2 started after wave 1 ended (msg times) | holds |

## Holes found
1. **Opus's reading is one item deep, and on the other nine items it points the other way.** Without h058, Opus's R is 0.14 [0.00, 0.46]: its CI lies wholly below 0.5, which is the pre-registered *self-anchoring* reading. With R = 2 conversations per cell, each order mean comes from 2 conversations. "Leaning question-driven" therefore says nothing about Opus, and the multi-model summary's "On Opus the effect is small" is also not what the gate says.
2. **Sonnet's question-driven effect rests on near-reversals with the record hidden.** In h191 redacted, the final M is 4, 97, 90, 97 (O2) and 90, 90, 90, 95 (O3), against 2–3 in every shown conversation. In h112 redacted O1 it is 90, 93, 93, 4, against 2–4 shown. These look like jumps to the opposite end of the scale (the same pattern as Haiku's h191, redacted O1 = 89), not graded order effects. The prereg's §5 says the placeholder's own effect is not separated. Dropping h058 puts the CI across 0.5 ([0.44, 17.3]). The gate itself is marginal (p 0.031). Consequence: "question-driven" holds by the rule, but "the question alone constructs the judgment" is a mechanism reading of a two-item effect that may be partly a placeholder artefact.
3. **The planted-value evidence that the record conditions answers is mixed on the stronger models.** On Sonnet, b_MF's CI includes 0, and so does the next-rating pull. On Opus the pull's CI includes 0, and its final M in O1–O4 moves away from the planted values (−10.0 [−17.1, −3.1]). The "own record" claim rests on the MF agreement contrast. That contrast holds, but agreement can fall with the placeholder for reasons other than memory.
4. **The irreversible fallback cost Opus power.** The rule's 1.12-per-turn growth assumption was wrong (later turns were cheaper). The rule was frozen and followed, but the result is R = 2, and a 2-per-cell variance-component estimate is too noisy to decide anything.
5. **The DEVIATIONS time stamps are false as written** (DM4 "08:10 … before any call"; DM4a "08:20 … no DM4 call had been made"). Git and the message IDs show that the order was correct.

## Overclaims to cut (exact sentences)
- `paper/no-credence-to-read.md:30` — "- **The question alone constructs the judgment on Sonnet** (R = 2.95 [0.99, 12.55]). On Opus the test is not decisive." — Why: "constructs" is a mechanism word for a two-item effect, and on Opus the one-item dependence goes unstated. — Replace: "- **On Sonnet the order effect survives hiding the record** (R = 2.95 [0.99, 12.55]), mostly from 2 of 10 items. On Opus the test is not decisive (its R rests on one item)."
- `paper/morning-brief.md:118` — "- **The question alone constructs the judgment on Sonnet** (R = 2.95). On Opus the test is not decisive." — Why: same as above. — Replace: "- **On Sonnet the order effect survives hiding the record** (R = 2.95 [0.99, 12.55]; 2 items carry most of it). On Opus the test is not decisive."

(`results/multi-model.md:21`, "Opus barely shows an order effect at all", is listed in `audits/multi-model.md`.)

## Does the verdict stand?
Pre-registered readings: Sonnet *question-driven*; Opus *leaning question-driven (not decisive)*; memory on all three.
- **Sonnet: STANDS WITH CAVEATS** (two-item concentration, possible placeholder artefact, marginal gate).
- **Opus: STANDS as "not decisive"**, but the "leaning question-driven" label is one item deep. Without h058 the rule gives self-anchoring.
- **Memory reading: STANDS** on all three.

## Confidence
**High.** Every statistic was recomputed independently from the raw conversations; the only differences are bootstrap-seed differences in CI endpoints.

## Tally
claims_checked: 12
claims_failed: 1
overclaim_sentences: 2
verdict: STANDS WITH CAVEATS
confidence: high

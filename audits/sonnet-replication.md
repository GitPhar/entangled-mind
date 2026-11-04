# Audit: sonnet-replication

**Files audited:** `results/sonnet-replication.md`, `results/sonnet-replication.json`, `results/sonnet-arm-g-confidence.json`, `results/pool-run-4.json` / `.md`, `results/pool-run-3.json`, `results/refusal-sonnet-replication.md`, `experiments/sonnet_replication.py`, `DEVIATIONS.md` D18, D20, D21, D25, D27, D28; citing text in `README.md`, `paper/record.md`, `paper/the-entangled-mind-v3.md`, `paper/the-entangled-mind-paper.md`, `paper/biomimetic-map.md`.
**Pre-registration:** set-up only. D18 (`c98bdf7`, 11-03 19:07:42) fixes the models (frozen v2 parameters), the pools and the budgets, but states no statistic, threshold or verdict rule ("what actually ran is reported"). Arm G on the hard pool: D28 / `f7afd8a` (21:03:08). First call: pool run 4 at 19:37:08 (after D18). The refusal stop came at 19:44:20, and calls resumed at 19:59:42, 3 s after the D21 commit (19:59:39); the last call was 20:13:55. Offline scoring (D27, `b584386` 20:58:33) has no timestamps (git only). Sonnet arm-G calls ran 21:03:26–21:05:57, 18 s after `f7afd8a`. The code that made them was committed at 21:04:16 (50 s after the first call), but the prompt (`llm.self_confidence`) was last changed at 15:14:50, so the G statistic was fixed in advance.
Timing verdict: OK (minor: arm-G calls preceded the commit of their runner; the result is secondary and has no pre-registered verdict).

## Plain-English summary of the audit
All the numbers reproduce. I rescored A2, F2, L and H on Sonnet's 298 records with my own code (matching the authors' path to 1e-16) and computed G from the cached Sonnet confidences: A2 0.90, F2 0.82, G 0.91, A2 − F2 +0.078, G − A2 +0.010. The problem is what "replication" means here. Sonnet's hard pool is the same 299 questions as Haiku's hard pool. 21 of Sonnet's 30 errors are items Haiku also got wrong in its run-2 held-out set, the set that had already shown A2 beating F2 and that motivated v2.1. A2's edge over F2 on Sonnet is +0.210 within those 78 items and −0.018 [−0.125, +0.064] on the other 220 (9 wrong). So the Sonnet edge is the Haiku held-out edge again, on the same questions, not an independent replication. "G = A2" is a non-detection (±0.07) that hides a type interaction: G is better on science, A2 much better on SimpleQA. The h101 refusal exclusion costs at most one item and cannot move the result. The "1 hit the token cap" exclusion (h018) was actually "extractor returned 1 claim".

## Claims checked
| # | claim (quoted or paraphrased, with file:line) | recomputed / evidence | status |
|---|---|---|---|
| 1 | Sonnet answered 298, 30 wrong (claim 0/60, science 18/120, simpleqa 12/118) (sonnet-replication.md:5) | exact | holds |
| 2 | A2 0.90 [0.84, 0.95], F2 0.82 [0.75, 0.88], L 0.73, H 0.66 (:9–12) | 0.899 [0.837, 0.951], 0.821 [0.752, 0.883], 0.732, 0.658; my circuit and product-prior code match `v2.py` to 2e-16 | holds |
| 3 | G 0.91 [0.86, 0.95], 298 calls, $0.88, no refusal (:3, :13) | 0.909 [0.864, 0.947]; G ids = scored ids (298); cost 0.8779 | holds |
| 4 | A2 − F2 +0.078 [+0.018, +0.137] (:15) | +0.078 [+0.020, +0.134]; LOO [+0.070, +0.094] | holds |
| 5 | G − A2 +0.008 [−0.061, +0.080]; "level with A2" (:15, :22) | observed +0.010 [−0.059, +0.080]: no detected difference within ±0.07. By type: science G 0.907 vs A2 0.839; simpleqa A2 0.983 vs G 0.828 | holds (minor) |
| 6 | G − L +0.176 [+0.095, +0.257]; L − H +0.074 [−0.041, +0.205] (:15) | +0.177 [+0.098, +0.264]; +0.074 [−0.044, +0.193] | holds |
| 7 | "**The error-prediction pattern replicates on a second base model.**" ... "in the same order as on Haiku's run-2 held-out set (A2 > F2 > L)" (:21) | Order holds. But pool 4 = pool 3's questions (identical text, minus h101); 23 of Sonnet's 30 errors are Haiku errors, and 21 are in Haiku's held-out wrong set. A2 − F2: within the 78 held-out questions +0.210 [+0.103, +0.322] (21 wrong); on the other 220 questions −0.018 [−0.125, +0.064] (9 wrong). On the 42 Haiku-wrong items F2 scores 0.46 vs A2 0.92 | overclaim |
| 8 | "nothing built from the deliberation structure beats the model's self-report" (:22) | No structural model beats G significantly (G − F2+ +0.006 [−0.059, +0.073]). Exploratory: the unreported A2.1 scores 0.921 on this set | holds (minor) |
| 9 | A2's Sonnet edge "is single-claim readout geometry, and a classical twin carries it" (:23) | F2+ − F2 +0.082 [+0.047, +0.118] = 1.05 [0.73, 2.50] of the A2 − F2 edge (see audits/sonnet-ablation.md) | holds |
| 10 | "Every positive quantum-vs-classical difference in the project is therefore accounted for by a classical model with the same per-claim readout." (:23) | see audits/sonnet-ablation.md: the held-out A2.1 edge is only 0.68 [0.20, 1.21] recovered; the three edges share questions; A2.1 − F2.1 on Sonnet (+0.101 [+0.029, +0.169], exploratory) was never tested | overclaim |
| 11 | h101 excluded after an extractor refusal, nothing reworded (D20, D21) | Refusal request ID decodes to 19:44:19; resumed 19:59:42. h101 is a Haiku-wrong held-out SimpleQA item; Sonnet's answer to it is not archived. One item moves A2 − F2 by at most about 0.016 (LOO range) | holds |
| 12 | "1 hit the token cap" (DEVIATIONS.md:376; v3:153; v3:507) | The excluded item h018 has `excluded_reason` "extractor returned 1 claims" (Sonnet answered it correctly); pool-run-4.md's template line lumps it in with token-cap exclusions | wrong |
| 13 | v3:526–527 "The models transfer ... A2 beats F2 on Sonnet's errors ... That matches the direction of Haiku's held-out results" | numbers hold; "matches the direction" is true, but it is the same questions (see #7) | holds (minor) |
| 14 | README.md:16 "The base model's own stated confidence predicts its errors as well as anything here, for both Haiku and Sonnet." | true as non-detection (all paired CIs with the best model include 0) | holds (minor) |

## Holes found
1. **Not an independent replication of the A2 > F2 edge.** Same 299 questions as Haiku's hard pool. The errors overlap heavily (23 of 30), and the edge lives entirely in the 78 questions of Haiku's run-2 held-out set (+0.210). Outside them it is −0.018 [−0.125, +0.064] (only 9 wrong, so underpowered). Haiku's held-out edge, v2.1's held-out edge and the Sonnet edge are one phenomenon on one set of hard SimpleQA/science questions that both models get wrong, not three. What does replicate independently is the *frozen-model transfer* (fitted on pool 5, scored on a different model's answers).
2. **"G = A2" is a non-detection with a type interaction.** G − A2 +0.010 [−0.059, +0.080]. G wins on science (0.907 vs 0.839), A2 wins on SimpleQA (0.983 vs 0.828). "Level with" hides that the two signals pick up different errors.
3. **Exclusion description wrong.** h018 was excluded for a 1-claim extraction, not a token cap (D25, v3). Immaterial to the numbers (h018 was answered correctly).
4. **No pre-registered verdict.** D18 fixes inputs only, so every reading here is descriptive. That is acceptable for a secondary result, but sentences like "replicates" carry confirmatory weight they did not earn.
5. **Minor.** The JSON's paired "point" values are bootstrap means (+0.008 vs observed +0.010).

## Overclaims to cut (exact sentences)
- `results/sonnet-replication.md:21` — "**The error-prediction pattern replicates on a second base model.**" — same questions as Haiku's hard pool; A2's edge is confined to the 78 questions of Haiku's held-out set — replace: "**The frozen models transfer to a second base model's answers on the same hard-pool questions.** A2's edge over F2 is concentrated in the questions Haiku also got wrong (21 of Sonnet's 30 errors are in Haiku's run-2 held-out set; A2 − F2 is +0.21 there and −0.02 [−0.13, +0.06] on the other 220 questions), so it is not independent of Haiku's held-out edge."
- `results/sonnet-replication.md:23` — "Every positive quantum-vs-classical difference in the project is therefore accounted for by a classical model with the same per-claim readout." — see audits/sonnet-ablation.md — replace: "Each positive quantum-vs-classical difference tested (all on the same hard-pool questions) is statistically indistinguishable from F2+, which recovers the whole Sonnet edge and roughly two thirds (95% CI one fifth to all) of Haiku's held-out A2.1 edge."
- `DEVIATIONS.md:376` — "- **Pool run 4** (hard pool, `h101` excluded) completed: 299 items processed, 1 hit the token cap, and **30 were wrong**. Cost $4.07." — h018 was excluded because the extractor returned 1 claim — replace "1 hit the token cap" with "1 was excluded (h018: the extractor returned 1 claim)".
- `paper/the-entangled-mind-v3.md:507` — "- **The hard pool completed:** 299 items processed, 1 hit the token cap, and Sonnet was wrong on **30** of 298 answered, for $4.07. Haiku was wrong on 44 of 300." — same — replace "1 hit the token cap" with "1 was excluded for a one-claim extraction".
- `paper/the-entangled-mind-v3.md:153` — "1 hit the token cap" (table cell fragment) — same — replace with "1 excluded for a one-claim extraction".

## Does the verdict stand?
No pre-registered verdict (D18 is set-up only). The descriptive result (frozen models transfer; A2 0.90, F2 0.82, G 0.91) **STANDS WITH CAVEATS**: the numbers are exact, but the A2 − F2 "replication" is the same item set as Haiku's held-out edge, and "G = A2" is a non-detection.

## Confidence
High. Everything was recomputed from raw pool-4 records and the cached Sonnet confidences with my own code, and the question-overlap and error-overlap analysis is direct from the archives. Sonnet's answer to h101 is not archived, so its effect is bounded by LOO rather than measured.

## Tally
claims_checked: 14
claims_failed: 3
overclaim_sentences: 5
verdict: STANDS WITH CAVEATS
confidence: high

# Audit: gm1-self-knowledge

**Files audited:** `results/gm1-self-knowledge.md`, `results/gm1-self-knowledge.json`, `results/gm1-calls.json`, `experiments/gm1-self-knowledge.md`, `experiments/gm1_self_knowledge.py`, `experiments/gm_common.py`, DEVIATIONS D36 + amendment (03:58) + amendment 2 (04:07), `results/pool-run-3.json`, `results/pool-run-4.json`, `results/arm-g-confidence.json`, `results/sonnet-arm-g-confidence.json`, `src/entangled_mind/llm.py` (`self_confidence`); citations in README.md, paper/record.md, paper/morning-brief.md, paper/no-credence-to-read.md, paper/the-entangled-mind-v3.md, paper/the-entangled-mind-paper.md, paper/gold-map.md. Recomputation: `scratchpad/g5/gm1.py`, `scratchpad/g5/gm1time.py`.
**Pre-registration:** `28a20b2` (2026-11-04 03:52:51), text in `experiments/gm1-self-knowledge.md` + DEVIATIONS D36. Amendment 1 is `954b4da` (03:58:25), amendment 2 is `2e2ab39` (04:07:05), and the result is `bc0f125` (04:15:08). Decoded call times:
- first call 03:54:55, last call 04:07:56;
- step 1 (`orig`, 1,192 calls) ran 03:54:55–04:02:03;
- step 2 (`para`, 160) ran 04:02:09–04:03:07;
- Haiku recognition (`recog`, 118) ran 04:03:20–04:03:55;
- step 3 (`pjud`, 240) ran 04:03:57–04:05:11, then 04:07:08–04:07:56.

Timing verdict: PROBLEM (minor; does not touch the primary statistic).
- **Text frozen, code not.** The pre-registration text predates the first call by 2 min. The runner and analysis code (`gm1_self_knowledge.py`) were first committed in amendment 1 at 03:58:25, 3.5 min after calls began, with step 1 about 60% done.
- **Amendment 1 reads as past events.** It says "The run was stopped after step 2 completed. Both steps are cached, and no call was lost." At its commit time, step 1 was still running (calls continue without a gap until 04:02:03) and step 2 had not started (04:02:09). The 13 s gap at 04:03:07–04:03:20 shows the restart actually happened after step 2. So the substance (reorder before steps 3–4) is borne out, but the text was committed as a plan written as if already done. Partial step-1 results were in the cache (saved every 200 calls) when the reorder was decided. I cannot tell whether they were looked at.
- **Amendment 2 is borne out.** Exactly 1,600 calls are timestamped ≤ 04:05:11 (the last save), there is a 117 s gap, and the restart comes at 04:07:08, 3 s after the 04:07:05 commit. The re-issued token-cap call (`pjud|H|H|h138`, 04:07:08) is recorded as no rating.
- **Analysis code.** Between `2e2ab39` and the result it is unchanged, except that amendment 2 handles token-cap calls.

## Plain-English summary of the audit
The core finding holds: across all 298 questions, neither Haiku nor Sonnet judges its own answers' errors better than the other model does once judge skill is cancelled. I recomputed every AUROC and the interaction, −0.055 [−0.105, −0.007], from the raw call archive. Its upper bound is below 0, so a self-advantage is actually ruled out on this pair, and the CI's direction is reported honestly. What does not hold is the interpretation.
- **The negative sign is not a "self-disadvantage".** It comes from the 26 questions where the two models disagree: there the outside judge knows the right answer and the author does not. Sonnet's confidence in Haiku's wrong answers is 30.5 when Sonnet itself was right and 64.4 when it was also wrong. Without those 26 questions, the interaction is −0.036 [−0.105, +0.026].
- **"Self-knowledge is text-reading" is a mechanism the design cannot test.** Every rating in all four cells, including the archived "self-report" it is meant to explain, is a fresh call that sees only the answer text. Privileged access to the generating state was never available in any cell. The test shows only that shared weights add nothing detectable, on one model pair.
- **The README's "each model judges its own answers no better than the other model does" is wrong for Sonnet.** Sonnet beats Haiku on Sonnet's answers, by +0.28 [+0.07, +0.51] on the disagreement subset.
- **Two side claims are overstated.** "Haiku cannot recognise its own writing" rests on 30 against 30 (CI to 0.67), and Sonnet's recognition check never ran. "Framing makes no difference" holds on all questions but not on the disagreement subset.

## Claims checked
| # | claim (quoted or paraphrased, with file:line) | recomputed / evidence | status |
|---|---|---|---|
| 1 | I = −0.055 [−0.103, −0.007] on 298 (`results/gm1-self-knowledge.md:12,31`) | −0.055 [−0.105, −0.007] (my bootstrap); n = 298, Haiku wrong 42, Sonnet wrong 30. Leave-one-question-out range −0.064 to −0.044. | holds |
| 2 | cells HH 0.845, SH 0.932, SS 0.903, HS 0.872; "0.93 against 0.85" (`:10-11,31`) | 0.845 / 0.932 / 0.903 / 0.872 | holds |
| 3 | disagreement I −0.135 [−0.496, +0.229]; HH 0.43, SH 0.85 (`:13,32`) | −0.135 [−0.508, +0.214]; 26 questions (Haiku wrong 19, Sonnet wrong 7) | holds |
| 4 | the interaction CI excludes 0 in the other-advantage direction: reported honestly? | Yes. The plain English says "slightly *negative*" with the CI, and the pre-registered rule 2 (other-advantage) keys only on the disagreement subset, so "no self-advantage" is the correct label. | holds |
| 5 | "Being the author makes a model a slightly worse judge of its own errors, not a better one." (`:12`) | Causal reading of a confounded interaction (prereg §6: "cannot rule out a judge-skill × author-difficulty interaction"). The negative I is concentrated in the disagreement questions: the agreement-only I is −0.036 [−0.105, +0.026]. Sonnet's mean confidence in Haiku's wrong answers is 30.5 when Sonnet was right (n = 19) and 64.4 when it was also wrong (n = 23); Haiku's confidence in its own is 60.1 and 60.9. The cross judge's edge is its own knowledge of the answer. | overclaim |
| 6 | "Saying 'an answer you gave' … makes no difference (−0.01 and +0.01)" (`:14`) | All 298: −0.011 / +0.007, which holds. On the disagreement subset Sonnet's self cell falls from 0.865 to 0.707, and I_you there is −0.316 [−0.608, −0.033], a CI below 0. The "you gave" cells are also a different, earlier run. | overclaim (minor) |
| 7 | "Paraphrasing the answers leaves the picture unchanged: −0.04" (`:15`, `:36`) | I_para −0.040 [−0.167, +0.075] on 60 questions. Truncation was not random: the 19 highest IDs (h242–h299) are missing. The comparison row "paraphrase subset (originals)" uses all 80 (−0.040). On the same 60, I_orig is −0.029. | holds (minor) |
| 8 | "Haiku cannot recognise its own writing (0.51 on originals), so self-recognition could not have helped in the first place." (`:16`) | 0.514 [0.365, 0.662], 30 / 30. Sonnet's recognition check (pre-registered §5.5 "reported in every case") did not run. All paraphrases were written by Haiku, so the paraphrase recognition (0.60) does not test authorship. | overclaim |
| 9 | "The model's confidence is a good reading of the answer, not privileged access … the 0.82–0.91 error signal is 'text-reading'" (`:18`); "Self-knowledge is text-reading" (`README.md:29`) | Mechanism claim from a behavioural 2×2 on one model pair. Arm G (`llm.self_confidence`) is itself a fresh call that shows only the visible answer, so introspective access to the generation was absent in every cell by construction. The design tests only whether shared weights help. The cross-judge edge is judge knowledge (row 5), not "reading". | overclaim |
| 10 | "Each model judges its own answers no better than the other model does" (`README.md:29`) | Sonnet does judge its own answers better than Haiku does: SS 0.903 against HS 0.872 (Δ_S +0.031 [−0.009, +0.073]). On the disagreement subset the gap is +0.282 [+0.073, +0.510]. Only the skill-cancelled interaction is ≤ 0. | wrong |
| 11 | "1710 calls, $2.82 of the $3 cap"; "true total is at most about $3.02" (`:3,22`) | 1,710 cached calls; recorded spend $2.8153, which is $0.015 over the amended $2.80 recorded cap. The lost-call bound is consistent with the decoded 16 s window (04:05:14–04:05:30, about 28–50 calls). | holds |
| 12 | Amendment 1: "The run was stopped after step 2 completed. Both steps are cached, and no call was lost." (`DEVIATIONS.md` D36 amendment, 03:58) | At 03:58:25, step-1 calls were still running (until 04:02:03) and step 2 had not begun (04:02:09). The restart is at 04:03:20. The text describes a plan as a past event. | wrong (documentation) |
| 13 | Amendment 2 crash bounds (last save at 1,600 calls, 04:05:14; crash 04:05:30) | 1,600 calls timestamped ≤ 04:05:11; next call 04:07:08 | holds |
| 14 | "Neither cut affects the primary result, which used the full 298 questions." (`:23`) | Step 1 is complete: 4 × 298, 0 missing | holds |

## Holes found
1. **The "text-reading, not privileged access" mechanism is mostly built into the design.**
   - Every judge call, in all four cells and in the archived arm-G self-report, is a fresh context that sees only the visible answer (`src/entangled_mind/llm.py:249-259`; `gm1_self_knowledge.py:67-70`). Access to generation-time state was absent everywhere.
   - What the 2×2 can test is narrower: whether a model's weights help it judge text it once produced. It finds no detectable advantage, on one pair (Haiku, Sonnet).
   - Calling the 0.82–0.91 signal "text-reading" and "not privileged access" (README:29, record:50, record:78, v3:682, v3:884, NCR:386, gold-map:436, morning-brief:47) asserts a mechanism the experiment neither manipulates nor isolates.
2. **The sign of I is explained by judge knowledge, not by authorship hurting.**
   - On Haiku's 42 wrong answers, Sonnet's confidence is 30.5 where Sonnet knew the answer and 64.4 where it did not. Haiku's own confidence is flat (60.1 against 60.9).
   - Removing the 26 disagreement questions leaves I = −0.036 [−0.105, +0.026].
   - "Being the author makes a model a slightly worse judge" (`:12`) and "a small self-*disadvantage*" (v3:674) read a judge-knowledge × author-error interaction (the confound pre-registered in §6) as a causal effect of authorship.
3. **The README's per-model sentence is false for Sonnet.** Δ_S is positive: +0.031 on all questions and +0.282 [+0.073, +0.510] on the disagreement subset. The sentence should talk about the interaction, not about "each model".
4. **The pre-registered "reported in every case" recognition check is half missing.**
   - Amendment 1 (03:58) moved Sonnet's recognition behind the paraphrase 2×2, then the cap cut it.
   - The paraphrase control was pre-registered to apply only "if reading 1 holds". Reading 1 failed, so the step that could not change the verdict was run ahead of a mandatory report.
   - The reorder was decided while step-1 data were accumulating in the cache.
   - Claims that self-recognition "could not have helped in the first place" therefore rest on Haiku alone, at 30 against 30.
5. **The framing null is only for all questions.** On the disagreement subset, the "you gave" framing drops Sonnet's self cell by 0.16, and I_you = −0.316 [−0.608, −0.033]. That is outside the "no difference" sentence (`:14`; morning-brief:46; NCR:261; v3:675). The archived "you gave" cells also come from a different run, which confounds framing with run.
6. **The paraphrase arm is a non-random 60-question subset.** The missing questions are the 19 highest IDs, and it is compared with I on all 80 originals rather than the same 60 (−0.029). This is minor: the arm was conditional and has no bearing on the verdict.
7. **Process.**
   - The runner code was committed 3.5 min after calls began.
   - Amendment 1's past-tense text was false at commit time.
   - Recorded spend ($2.815) exceeded the amended recorded cap ($2.80).
   - All are disclosed in substance, and none moves the primary statistic.

## Overclaims to cut (exact sentences)
- `results/gm1-self-knowledge.md:12` — "Being the author makes a model a slightly worse judge of its own errors, not a better one." — causal reading of a confounded interaction, driven by the 26 disagreement questions (agreement-only I −0.036 [−0.105, +0.026]). — Replace with: "The negative sign comes from questions where the other model knew the answer; it reflects the judge's knowledge, not a cost of authorship."
- `results/gm1-self-knowledge.md:14` — "- **Saying "an answer you gave"** instead of "another assistant" makes no difference (−0.01 and +0.01)." — Replace with: "- **Saying "an answer you gave"** instead of "another assistant" makes no difference on all questions (−0.01 and +0.01), though on the 26 disagreement questions Sonnet's self cell falls from 0.87 to 0.71 (archived ratings from an earlier run)."
- `results/gm1-self-knowledge.md:16` — "- **Recognition.** Haiku cannot recognise its own writing (0.51 on originals), so self-recognition could not have helped in the first place." — 30 / 30, CI [0.36, 0.67]; Sonnet not tested. — Replace with: "- **Recognition.** Haiku shows no detectable recognition of its own writing (0.51 [0.36, 0.67] on 30 + 30 originals); Sonnet's recognition check did not run."
- `results/gm1-self-knowledge.md:18` — "**What it means.** The model's confidence is a good reading of the answer, not privileged access." — mechanism not isolated; every cell is a fresh-context reading by design. — Replace with: "**What it means.** On this design, where every rating is a fresh call that sees only the answer, being the model that wrote the answer adds nothing detectable."
- `results/gm1-self-knowledge.md:18` — "On this test, the 0.82–0.91 error signal is "text-reading"." — Replace with: "On this test, the 0.82–0.91 error signal is matched or beaten by another model reading the same answer, especially one that knows the right answer."
- `README.md:29` — "**Self-knowledge is text-reading.** Each model judges its own answers no better than the other model does; the judge × author interaction is −0.055 [−0.103, −0.007]." — wrong for Sonnet (SS 0.903 > HS 0.872; +0.28 [+0.07, +0.51] on disagreement), and the mechanism is not isolated. — Replace with: "**No self-advantage in judging errors.** With each judge's skill cancelled, authorship adds nothing on Haiku and Sonnet: the judge × author interaction is −0.055 [−0.103, −0.007], and Sonnet judges Haiku's errors better than Haiku does (0.93 against 0.85)."
- `paper/record.md:50` — "self-report is text-reading, not privileged access" — this fragment also occurs inside line 78 (next entry); replace line 50's occurrence (the table cell) — Replace with: "authorship adds nothing detectable to a fresh-context confidence rating; a judge that knows the answer does better".
- `paper/record.md:78` — "  - self-report is text-reading, not privileged access (direction 1);" — Replace with: "  - authorship adds nothing detectable to judging one's own errors (direction 1);".
- `paper/morning-brief.md:46` — "   - Paraphrasing the answers, or saying "your answer", changes nothing." — paraphrase on 60 non-random questions, CI ±0.12; framing changes Sonnet's self cell by −0.16 on the disagreement subset. — Replace with: "   - Paraphrasing the answers, or saying "your answer", makes no detectable difference overall."
- `paper/morning-brief.md:47` — "   - So the model's best error signal is good reading of the answer text, not access to anything inside." — the design gives no cell access to anything inside. — Replace with: "   - So the model's best error signal can be matched by another model reading the answer; this design does not test access to internal state."
- `paper/no-credence-to-read.md:259` — "- **Authorship does not help, and slightly hurts.** Sonnet predicts Haiku's errors better than Haiku does: 0.93 against 0.85." — "slightly hurts" is the confounded sign (hole 2). — Replace with: "- **Authorship does not help.** Sonnet predicts Haiku's errors better than Haiku does: 0.93 against 0.85, mostly on questions where Sonnet knew the answer."
- `paper/no-credence-to-read.md:261` — "- **Wording makes no difference.** "An answer you gave" instead of "another assistant" changes the self cells by −0.011 (Haiku) and +0.007 (Sonnet)." — Replace with: "- **Wording makes no difference overall.** "An answer you gave" instead of "another assistant" changes the self cells by −0.011 (Haiku) and +0.007 (Sonnet) on all 298 questions."
- `paper/no-credence-to-read.md:262` — "- **Haiku cannot pick out its own answers:** recognition AUROC 0.51 [0.36, 0.67]." — Replace with: "- **No detectable self-recognition by Haiku:** recognition AUROC 0.51 [0.36, 0.67] on 30 + 30 answers (Sonnet's check did not run)."
- `paper/no-credence-to-read.md:386` — "**What our result says.** On this test, and on all three models, self-reported confidence is text-reading." — Replace with: "**What our result says.** On this test, and on all three models, authorship adds nothing detectable to a confidence rating made from the answer text."
- `paper/the-entangled-mind-v3.md:674` — "- **No self-advantage, and a small self-*disadvantage*.**" — Replace with: "- **No self-advantage.** The interaction is slightly negative, which comes from questions where the other model knew the answer."
- `paper/the-entangled-mind-v3.md:675` — "- **The framing makes no difference:** "an answer you gave" against "another assistant" changes the self cells by −0.011 (Haiku) and +0.007 (Sonnet)." — Replace with: "- **The framing makes no difference overall:** "an answer you gave" against "another assistant" changes the self cells by −0.011 (Haiku) and +0.007 (Sonnet) on all 298 questions."
- `paper/the-entangled-mind-v3.md:682` — "- **Reading.** The 0.82–0.91 self-report signal of Sections 5.3–5.11 is a good reading of the answer text, not privileged self-knowledge." — Replace with: "- **Reading.** The 0.82–0.91 self-report signal of Sections 5.3–5.11 carries no detectable authorship advantage: another model reading the same answer text matches or beats it."
- `paper/the-entangled-mind-v3.md:807` — "The error signal is in the answer text, and a capable reader finds it." — the capable reader's edge is its own knowledge of the answer. — Replace with: "The error signal is available from the answer text to a capable reader, especially one that knows the answer."
- `paper/the-entangled-mind-v3.md:884` — "- The model's self-reported confidence is text-reading, not privileged self-knowledge." — Replace with: "- The model's self-reported confidence shows no authorship advantage over another model reading the same answer."
- `paper/gold-map.md:436` — "no: self-report is text-reading" — Replace with: "no: no authorship advantage".

## Does the verdict stand?
Pre-registered reading: **no self-advantage**. Rule 1 failed (I < 0 on all; the disagreement CI includes 0) and rule 2 failed (the disagreement CI is not below 0). **STANDS WITH CAVEATS.** The primary statistic recomputes exactly. Its upper bound (−0.007) excludes any self-advantage on this pair, and step 1 was complete. The caveats:
- the negative sign is judge knowledge, not authorship;
- the "text-reading" mechanism is not tested, and is partly true by construction;
- Sonnet's recognition check is missing;
- the README's per-model sentence is false for Sonnet.

## Confidence
High. I recomputed all cells, interactions, deltas, bootstrap CIs, the you-gave and paraphrase rows, recognition, the leave-one-out and agreement-only checks, and the judge-knowledge split from `gm1-calls.json` and the pool archives. I reconstructed the call timeline from decoded request IDs. I cannot determine whether partial step-1 results were inspected before amendment 1.

## Tally
claims_checked: 14
claims_failed: 6
overclaim_sentences: 20
verdict: STANDS WITH CAVEATS
confidence: high

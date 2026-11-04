# Direction 2: measurement as self-conditioning (shown, redacted, planted transcripts)

Pre-registered in `experiments/gm2-self-conditioning.md` (D37), committed before any call. 10 experiment-5 items, chains O1–O4 and MF, anchor (a) only (0 = certainly false, 100 = certainly true), 10 conversations per item × chain × condition. 2000 conversations, **$0.55** of the $1 cap; no refusal.

## In plain English

**The question.** Direction 9 showed that asking earlier questions changes the model's later answers. When a question is asked, two things enter the conversation: the question, and the model's recorded answer. Which one does the work? We re-ran 10 experiment-5 items with the transcript edited between turns:
- the model's earlier ratings **shown** as normal;
- **hidden** ("[rating recorded]");
- **replaced** with numbers 15 points above or below its usual rating, placed in its own turn.

**What we found.** Both parts matter, and the question alone is enough for an order effect.
- **The question.** With the model's earlier answers hidden, the order of the sub-questions still changes its final verdict, by even more than when the answers are shown: an order effect of 16.7 points against 8.7. The ratio is 1.9 [0.9, 4.9], which passes the pre-registered bar of 0.5. Being asked the questions, in a particular order, changes the judgment even when the model can't see what it answered.
- **The record.** The numbers in the transcript pull later ratings. Planting higher earlier ratings raises the model's later sub-question ratings by about 3 points and its final verdict by about 10. When its first answer to the main question is planted, the final answer follows it at about a point per point (median item 1.00; mean 1.27 [0.70, 2.14], inflated by one item, h238).
- **Repeat agreement depends on seeing the first answer.** In experiment 5, the model repeated its main rating within 5 points 84% of the time after a chain of questions. Here that is 81% when it can see its first answer, but only 23% when the answer is hidden. Seeing its first answer raises repeat agreement sharply; without it, the intervening questions move the final rating away from the first.

**What it means.**
- The order effects are not only self-anchoring. The questions themselves change the judgment. In the gold map's terms, that is "measurement in the strict sense", the overturning direction, which the gold map had put at 0.25.
- But the model also anchors heavily on its own recorded answers. That anchoring keeps its repeated answer close to its first one after a chain of questions.
- One reading is that the judgment is built by the asking in two ways: by the questions put to the model, and by its own earlier answers, treated as evidence.

**Caveats.**
- 10 items, and much of the redacted order effect comes from 2 of them (h191, h261).
- The redacted order effect is *larger* than the shown one. The verdict stands by the rule, since the CI lies wholly above 0.5, but the excess over "shown" should not be read as the question's own effect. The placeholder turn may add variance.
- "[rating recorded]" is itself an unusual turn and may unsettle the model. The planted conditions, which keep a number in place, show smaller order effects than either.

## Order effect across O1–O4 (final main rating)

OE = √(mean over items of the between-order variance component), in rating points; 95% item-bootstrap CIs.

| condition | OE (points) |
|---|---|
| shown | 8.7 [4.1, 12.7] |
| redacted | 16.7 [8.0, 24.1] |
| high | 6.2 [3.6, 8.3] |
| low | 3.2 [2.2, 4.0] |

- Gate (shown order effect, permutation p): **0.0002**.
- **R = OE_redacted / OE_shown: 1.91 [0.92, 4.90]**.

## Planted values

- Self-anchoring in MF, b_MF (final M follows the planted first M): 1.27 [0.70, 2.14].
- Next-rating pull (actual ratings at positions 2+, planted high minus low): 5.6 [3.4, 7.6] points.
- Final M shift in O1–O4, planted high minus low: 10.4 [4.2, 16.8] points.

## Replicability in MF (|M₂ − M₁| ≤ 5)

| condition | agreement |
|---|---|
| shown | 81% |
| redacted | 23% |
| high | 30% |
| low | 40% |

## Per item

| item | OE shown | OE redacted | final M by order O1–O4: shown | redacted | MF M₂: shown / redacted / high / low | planted M low / high |
|---|---|---|---|---|---|---|
| h190 | 3.1 | 3.9 | 16, 10, 16, 11 | 15, 12, 15, 22 | 5 / 17 / 17 / 6 | 2 / 19 |
| h101 | 1.5 | 11.4 | 7, 7, 4, 5 | 32, 4, 6, 14 | 3 / 18 / 18 / 2 | 2 / 18 |
| h112 | 20.8 | 18.7 | 80, 37, 75, 80 | 43, 6, 50, 30 | 21 / 30 / 49 / 14 | 13 / 43 |
| h191 | 0.4 | 38.3 | 3, 3, 4, 3 | 81, 3, 5, 3 | 3 / 3 / 18 / 2 | 2 / 18 |
| h261 | 6.4 | 24.4 | 31, 9, 12, 13 | 60, 22, 4, 10 | 32 / 52 / 6 / 3 | 69 / 98 |
| h058 | 12.0 | 11.9 | 42, 19, 48, 43 | 62, 34, 38, 40 | 58 / 35 / 92 / 35 | 63 / 93 |
| h221 | 2.2 | 8.3 | 32, 32, 36, 36 | 24, 45, 32, 32 | 30 / 35 / 39 / 11 | 11 / 41 |
| h279 | 9.1 | 2.1 | 34, 30, 17, 39 | 36, 30, 36, 36 | 22 / 42 / 42 / 12 | 12 / 42 |
| h127 | 4.9 | 2.5 | 24, 36, 27, 29 | 18, 22, 21, 16 | 13 / 26 / 16 / 8 | 2 / 27 |
| h238 | 4.6 | 4.0 | 13, 4, 4, 3 | 14, 5, 10, 13 | 32 / 11 / 97 / 19 | 81 / 98 |

## Pre-registered reading: **question-driven: the order effect survives redaction (a measurement effect in the strict sense)**

# Direction 2 on all 40 experiment-5 items (shown, redacted, planted transcripts)

Pre-registered in `experiments/gm2b-self-conditioning-40.md` (D45), committed before any call. Design identical to D37; last night's 10 items reused, the other 30 run now. Anchor (a) only. 6000 new conversations, **$1.68** of the $2.50 cap; no refusal.

## In plain English

**What was tested.** Last night's direction 2 asked, on 10 items, whether the order of questions changes the model's final rating even when its earlier answers are hidden. The answer was yes, but much of it came from two items (h191, h261). This run puts all 40 experiment-5 items through the same design and pre-registered rule.

**The question alone still changes the judgment, and not because of two items.**
- With every earlier answer replaced by "[rating recorded]", the order of the questions still moves the final rating by about as much as when the answers are visible: R = **1.23 [0.75, 2.02]** on all 40 items. The interval lies above the pre-registered 0.5 line, so the reading is again *question-driven*.
- It holds on the 30 new items alone (R = 0.99 [0.51, 1.61]) and with h191 and h261 dropped (0.99 [0.62, 1.49]).
- No single item carries it (dropping any one leaves the CI above 0.5), though a few items dominate the size. On 82% of them the redacted order effect is at least half the shown one.

**The redacted effect is no longer larger than the shown one.**
- Last night's R of 1.91 came mostly from h191, which has almost no order effect when its answers are visible (0.4 points) and a large one when they are hidden (38 points).
- Across 40 items, the two are about equal (12.0 and 9.8 points). Without h191 and h261, they are the same (9.9 and 10.0).
- **The placeholder check passes.** The spread of final ratings within one order is the same shown and redacted (SD 5.1 against 5.4). So the placeholder turn does not add noise of its own; whether it adds order-specific shifts is not tested by this check.
- The honest summary is that, on these items, **hiding the record leaves an order effect of about the same size, but a largely different one: the record changes which orders move the verdict.**

**The record still steers, and keeps the repeated answer close to the first.**
- A planted first answer pulls the final answer to the same question by 0.85 [0.65, 1.13] points per point. That is smaller than last night's 1.27, but clearly above zero.
- Planted-high earlier ratings raise the next actual rating by 5.2 points and the final rating by 9.0 points over planted-low.
- With its first answer visible, the model repeats it within 5 points 86% of the time. Hidden, it does so 36% of the time (last night: 81% and 23%).

**What changes in the paper.**
- The direction 2 numbers move to the 40-item values.
- The caveat about two items carrying the effect can be dropped; the placeholder caveat stands.
- The question-driven reading stands. "The redacted effect is larger than the shown" should no longer be said.

## Order effect and its decomposition

| item set | gate p | OE shown | OE redacted | OE high | OE low | **R = redacted / shown** | items with redacted ≥ ½ shown | within-order SD shown / redacted | reading |
|---|---|---|---|---|---|---|---|---|---|
| all 40 (primary) | 0.0002 | 9.8 [5.8, 13.5] | 12.0 [7.3, 15.9] | 6.3 | 5.3 | **1.23 [0.75, 2.02]** | 82% of 39 | 5.1 / 5.4 | question-driven: the order effect survives redaction (a measurement effect in the strict sense) |
| 30 new items (replication) | 0.0002 | 10.1 [5.2, 15.0] | 9.9 [4.9, 14.3] | 6.3 | 5.9 | **0.99 [0.51, 1.61]** | 79% of 29 | 4.7 / 4.6 | question-driven: the order effect survives redaction (a measurement effect in the strict sense) |
| 40 without h191 and h261 (sensitivity) | 0.0002 | 10.0 [5.9, 13.9] | 9.9 [6.0, 13.6] | 6.2 | 5.5 | **0.99 [0.62, 1.49]** | 81% of 37 | 4.9 / 5.0 | question-driven: the order effect survives redaction (a measurement effect in the strict sense) |

## The record: planted values and replicability

| item set | b_MF (final M follows planted first M) | next-rating pull (points) | final-M shift, O chains (points) | MF agreement shown / redacted / high / low |
|---|---|---|---|---|
| all 40 (primary) | 0.85 [0.65, 1.13] | 5.2 [3.7, 6.5] | 9.0 [5.4, 12.6] | 86% / 36% / 38% / 45% |
| 30 new items (replication) | 0.72 [0.54, 0.90] | 5.0 [3.2, 6.7] | 8.6 [4.3, 12.9] | 87% / 40% / 41% / 47% |
| 40 without h191 and h261 (sensitivity) | 0.87 [0.64, 1.14] | 5.1 [3.6, 6.4] | 8.7 [5.1, 12.3] | 87% / 34% / 40% / 45% |

## Pre-registered reading (all 40): **question-driven: the order effect survives redaction (a measurement effect in the strict sense)**

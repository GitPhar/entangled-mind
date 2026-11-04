# Opus six-format arm completed (80 claims), with test F′

Pre-registered in `experiments/mm-gm3b-opus-completion.md` (D49), committed before any call. DM2's design, prompts and analysis unchanged; the 54 claims the DM2 budget stopped are run now. **$5.78** new spend of the $6.40 cap ($8.88 for the whole Opus arm, batch rate); 0 refusals; 0 max_tokens stops.

## In plain English

**What was tested.** On the 26 statements its first budget allowed, Opus's six ways of answering agreed almost perfectly. This run asked it the remaining statements, so that the test covers items Haiku got right as well as wrong, and so that the held-out-format test (F′) could be run. The pre-registered stopping rule ended the run at 17 of the 20 items (68 of 80 statements; see D49a).

**One belief predicts every format on Opus.**
- For each format, a single belief per statement, fitted on the other five formats, predicts that format's answers nearly as well as the format predicts itself. On average it reaches **94% of the ceiling (Q = 0.94 [0.90, 0.97])**. Haiku reached 29% on the same kind of statements, and Sonnet 69%.
- The R² from the other five formats is 0.92. That is above the top of the 0.60–0.90 range Smolin & Wilder report for other capable models.
- The weakest format is yes/no (82% of its ceiling). Every other format is at 94% or above.
- The pre-registered reading is **a usable single belief**.

**The stricter test still cannot quite tell one belief from six.**
- On held-out repeats, one belief per format fits slightly better than one per statement (ΔLL +1.90 [−0.82, +4.65], 74% of statements positive). The interval includes zero, so DM2's reading is again *mixed*.
- That is about a tenth of Haiku's +19.4 and a fifth of Sonnet's +9.2.
- So Opus's formats bend its belief in small, reproducible ways, but they do not reorder it.

**Agreement between formats rises with model strength, on the same statements.** On Opus's 68 statements, Kendall's W is 0.56 for Haiku, 0.76 for Sonnet and 0.87 for Opus (exploratory, `results/mm-gm3b-W-on-68-exploratory.json`). The trend is now item-matched.

**For the paper.** By the rule frozen before the run, the "no format-free credence" claim **does not hold on Opus**. The claim goes from "not supported" on Opus to "contradicted": one belief there predicts each left-out format close to its own ceiling.

**Checks.**
- Adding h291, the item that ran past the stopping rule, changes no reading: Q 0.94 [0.90, 0.97]; ΔLL +1.55 [−1.00, +4.17], mixed; W 0.85 (`mm-gm3b-opus-completion-with-h291.md`).
- The earlier 26 statements are not special. Refitted jointly with the rest, their mean ΔLL is +2.42 against +1.57 for the others. The per-claim values differ from DM2's (+0.42) because the format links are now fitted on more statements.
- No call was refused, and no answer hit the token limit.

## Primary (DM2's rule): one credence (L1) against one per format (L6)

| Opus claims complete | mean ΔLL per claim [95% CI] | claims with ΔLL > 0 | reading |
|---|---|---|---|
| 68 | +1.90 [-0.82, +4.65] | 74% | **mixed** |

Before this run (26 claims, DM2): +0.42 [-1.83, +2.69], 58% positive, W 0.86.

## Test F′ (D46's frozen analysis): predicting each format from the other five

On 68 claims (17 items).

| held-out format | R² from the other five | R² ceiling | Q |
|---|---|---|---|
| rating 0-100 | 0.98 | 0.99 | 0.99 |
| yes/no | 0.80 | 0.96 | 0.84 |
| bet | 0.93 | 0.95 | 0.97 |
| pairwise vs coin | 0.93 | 0.99 | 0.94 |
| frequency /100 | 0.98 | 0.99 | 0.98 |
| verbal 7-point | 0.93 | 0.98 | 0.94 |

- **Mean Q = 0.94 [0.90, 0.97]**: a usable single belief (one credence recovers most of each format's reproducible answer).
- Mean R² from the other five: 0.92 [0.87, 0.96].

## Kendall's W (Haiku and Sonnet on the 80 claims; Opus on its 68 complete claims)

| Haiku | Sonnet | Opus |
|---|---|---|
| 0.54 | 0.71 | 0.87 |

Descriptive: Opus's mean ΔLL on the 26 earlier claims +2.42; on the others +1.57.

## Pre-registered reading for the paper's Opus claim: **does not hold on Opus: one credence predicts each left-out format close to its own ceiling**

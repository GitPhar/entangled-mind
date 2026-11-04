# Opus six-format arm completed (80 claims), with test F′

Pre-registered in `experiments/mm-gm3b-opus-completion.md` (D49), committed before any call. DM2's design, prompts and analysis unchanged; the 54 claims the DM2 budget stopped are run now. **$6.04** new spend of the $6.40 cap ($9.14 for the whole Opus arm, batch rate); 0 refusals; 0 max_tokens stops.

## In plain English

**Sensitivity analysis only (D49a).** This is the same analysis with h291 added: 18 items, 72 claims. h291 ran after the point where the pre-registered stopping rule ends the run, because the runner's projection used the previous batch's mean cost rather than the mean so far. The primary result is `mm-gm3b-opus-completion.md`, on 17 items. Every reading is the same here.

## Primary (DM2's rule): one credence (L1) against one per format (L6)

| Opus claims complete | mean ΔLL per claim [95% CI] | claims with ΔLL > 0 | reading |
|---|---|---|---|
| 72 | +1.55 [-1.00, +4.17] | 68% | **mixed** |

Before this run (26 claims, DM2): +0.42 [-1.83, +2.69], 58% positive, W 0.86.

## Test F′ (D46's frozen analysis): predicting each format from the other five

On 72 claims (18 items).

| held-out format | R² from the other five | R² ceiling | Q |
|---|---|---|---|
| rating 0-100 | 0.98 | 0.99 | 0.99 |
| yes/no | 0.78 | 0.96 | 0.82 |
| bet | 0.92 | 0.96 | 0.96 |
| pairwise vs coin | 0.92 | 0.99 | 0.94 |
| frequency /100 | 0.98 | 0.99 | 0.98 |
| verbal 7-point | 0.94 | 0.98 | 0.96 |

- **Mean Q = 0.94 [0.90, 0.97]**: a usable single belief (one credence recovers most of each format's reproducible answer).
- Mean R² from the other five: 0.92 [0.87, 0.96].

## Kendall's W (Haiku and Sonnet on the 80 claims; Opus on its 72 complete claims)

| Haiku | Sonnet | Opus |
|---|---|---|
| 0.54 | 0.71 | 0.85 |

Descriptive: Opus's mean ΔLL on the 26 earlier claims +2.22; on the others +1.17.

## Pre-registered reading for the paper's Opus claim: **does not hold on Opus: one credence predicts each left-out format close to its own ceiling**

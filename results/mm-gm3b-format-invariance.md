# Multi-model replication of direction 3: six elicitation formats (80 claims)

Pre-registered in `experiments/mm-gm3b-format-invariance.md` (DM2), committed before any call. 20 of the 40 experiment-5 items (10 Haiku got wrong, 10 it got right), their 80 chain claims, six formats × 10 repeats, one scale direction. Haiku's row re-analyses its archived calls (D38) on the same 80 claims; Sonnet and Opus are new. Costs are at the batch rate.

## In plain English

(Hand-written after the run; excluded from reproduce.py's comparison.)

## Primary: one credence (L1) against one per format (L6), held-out repeats

| model | claims (items) complete | calls used / expected | cost | mean ΔLL per claim [95% CI] | claims with ΔLL > 0 | reading |
|---|---|---|---|---|---|---|
| haiku | 80 (20) | 4800 / 4800 | $0.20 | +19.42 [+15.40, +23.21] | 86% | **no single credence: formats disagree beyond monotone links** |
| sonnet | 80 (20) | 4800 / 4800 | $2.04 | +9.22 [-1.29, +16.24] | 92% | **mixed** |
| opus | 68 (17) | 4080 / 4800 | $8.88 | +1.90 [-0.82, +4.65] | 74% | **mixed** |

## Agreement between formats

| model | Kendall's W | Spearman ρ range | discordant pairs vs the 0–100 rating, range |
|---|---|---|---|
| haiku | 0.54 | +0.29 to +0.63 | 25% to 35% |
| sonnet | 0.71 | +0.63 to +0.84 | 14% to 20% |
| opus | 0.87 | +0.83 to +0.98 | 6% to 14% |

## ΔLL by format (mean per claim)

| format | haiku | sonnet | opus |
|---|---|---|---|
| rating 0-100 | +6.210 | +0.248 | +0.151 |
| yes/no | +2.510 | +1.537 | +0.263 |
| bet | +2.388 | +1.713 | +1.181 |
| pairwise vs coin | +1.428 | +0.482 | -0.293 |
| frequency /100 | +6.831 | +0.535 | +0.164 |
| verbal 7-point | +0.054 | +4.709 | +0.430 |

## Secondary: held-out-format prediction (test F′'s frozen analysis, D46)

| model | mean Q [95% CI] | mean R² from the other five | reading |
|---|---|---|---|
| haiku | 0.29 [0.19, 0.43] | 0.27 | little format-free belief (most of each format's reproducible answer is not recoverable from the others) |
| sonnet | 0.69 [0.53, 0.82] | 0.65 | partial |
| opus | not computed: arm incomplete (68 of 80 claims) | | |

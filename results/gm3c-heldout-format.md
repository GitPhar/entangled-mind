# Direction 3 follow-up: predicting each format from the other five

Pre-registered in `experiments/gm3c-heldout-format.md` (D46), committed before the fit. Last night's six-format data (`results/gm3b-calls.json`); the one-credence model L1 fitted on even repeats with the held-out format removed for the test fold's claims (5 item folds); targets are odd repeats. No API calls; $0.

## In plain English

**The question.** Last night we found that one belief per statement can't explain every way of asking to within repeat noise. This asks the gentler question: is that one belief at least *useful*? Knowing how the model answers a statement in five formats, can we predict its answer in the sixth? We compared each prediction with the best possible one: the same format's own other half of repeats.

**What we found.** Not very well.
- **The other five formats** predict a held-out format's answers with an R² of 0.37 on average (0.15–0.51 by format).
- **The format's own other half of repeats** predicts them with an R² of 0.88–0.97.
- **The ratio:** the cross-format prediction recovers only 39% [30%, 50%] of what is reproducible in each format. That is below the pre-registered 0.5 line, though only just: the upper end of the interval is 0.499.
- **The worst case** is the comparison with a coin toss (17% recovered). The best are the 0–100 rating (53%) and the verbal scale (47%).
- **Against the precedent:** Smolin & Wilder found held-out R² of 60–90% on other models. Haiku, on its own deliberation claims, is below that range, though their framings, items and statistic differ from ours, so the comparison is only indicative.

**What it means.** The answers are highly reproducible within a format and only loosely related across formats. Most of what the model reproducibly says about a statement in one format cannot be recovered from how it answers in the others. So last night's result is not just a belief that each format bends slightly: on these statements, somewhat more than half of each format's reproducible answer is not shared with the other formats. There is a common thread, since a third to a half is shared, but it is the smaller part.

**Caveats.**
- One model, one context per statement.
- The interval's upper end sits right at the 0.5 line, so "partial" is only narrowly excluded.

## Cross-format prediction against each format's own split-half ceiling

| held-out format | R² from the other five | R² ceiling (own even repeats) | Q = ratio | Spearman, cross / ceiling |
|---|---|---|---|---|
| rating 0-100 | 0.51 | 0.96 | 0.53 | +0.76 / +0.98 |
| yes/no | 0.36 | 0.89 | 0.41 | +0.63 / +0.93 |
| bet | 0.43 | 0.92 | 0.47 | +0.64 / +0.92 |
| pairwise vs coin | 0.15 | 0.88 | 0.17 | +0.41 / +0.88 |
| frequency /100 | 0.30 | 0.94 | 0.32 | +0.54 / +0.96 |
| verbal 7-point | 0.46 | 0.97 | 0.47 | +0.73 / +0.98 |

- **Mean Q = 0.39 [0.30, 0.50]** (item-cluster bootstrap).
- Mean absolute R² from the other five formats: 0.37 [0.28, 0.47] (Smolin & Wilder: 0.60–0.90 on other models).

## Pre-registered reading: **little format-free belief (most of each format's reproducible answer is not recoverable from the others)**

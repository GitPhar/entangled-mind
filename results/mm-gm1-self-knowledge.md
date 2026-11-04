# Multi-model replication of direction 1: self versus other confidence, Sonnet × Opus

Pre-registered in `experiments/mm-gm1-self-knowledge.md` (DM3), committed before any call. Authors: Sonnet's archived hard-pool answers and Opus's new ones, on the 298 of direction 1's 298 questions that both answered; disagreement subset (authors' correctness differs): 21. 1192 new calls, **$4.03** of the $4.60 cap (batch rate); refusals: 0.

## In plain English

(Hand-written after the run; excluded from reproduce.py's comparison.)

Accuracy on the complete set: Sonnet 89.9% (30 wrong), Opus 94.3% (17 wrong).

## AUROC of each judge for each author's errors

Cells: judge then author (OS = Opus judging Sonnet's answers). I = SS + OO − OS − SO; Δ_S = SS − OS; Δ_O = OO − SO. 95% CIs from 2,000 question-level resamples. SS is direction 1's archived cell.

| set | SS | OS | OO | SO | **I** | Δ_S | Δ_O |
|---|---|---|---|---|---|---|---|
| all | 0.903 | 0.959 | 0.904 | 0.893 | **-0.045 [-0.107, +0.017]** | -0.056 [-0.089, -0.025] | +0.011 [-0.056, +0.072] |
| disagreement | 0.551 | 0.522 | 0.684 | 0.529 | **+0.184 [-0.296, +0.812]** | +0.029 [-0.433, +0.500] | +0.154 [-0.575, +0.643] |

Reference, Haiku × Sonnet (D36): I = -0.055 [-0.103, -0.007] on all 298; -0.135 [-0.496, +0.229] on the disagreement subset.

## Pre-registered reading: **no self-advantage**

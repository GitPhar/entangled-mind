# Direction 1: privileged self-knowledge (2×2 self-versus-other confidence)

Pre-registered in `experiments/gm1-self-knowledge.md` (D36), committed before any call. Authors: Haiku and Sonnet hard-pool answers on the 298 questions both answered; disagreement subset (authors' correctness differs): 26 questions. 1710 calls, **$2.82** of the $3 cap; no refusal.

## In plain English

**The question.** The model's own stated confidence is the project's best signal of when it is wrong. Is that because the model knows something private about its own weak spots, or does it just read its answer well? We had each model, Haiku and Sonnet, rate its confidence in both its own and the other model's answers to the same 298 hard questions. Every rating used the same prompt ("an answer another assistant gave"), so authorship was the only difference.

**What we found.** Being the author does not help.
- **Haiku's answers:** Sonnet spots Haiku's mistakes better than Haiku does (AUROC 0.93 against 0.85).
- **Sonnet's answers:** Sonnet is slightly better than Haiku (0.90 against 0.87).
- **The combined self-advantage**, which cancels out the fact that Sonnet is the stronger judge, is slightly *negative*: −0.055 [−0.103, −0.007]. The negative sign comes from questions where the other model knew the answer; it reflects the judge's knowledge, not a cost of authorship.
- **The questions where exactly one model got it right** (26 of them) are where privileged knowledge should show most. The combined advantage there is −0.14 [−0.50, +0.23], so no self-advantage was detected. On those questions Haiku is close to chance at judging its own answers (0.43) while Sonnet judges them well (0.85).
- **Saying "an answer you gave"** instead of "another assistant" makes no difference on all questions (−0.01 and +0.01), though on the 26 disagreement questions Sonnet's self cell falls from 0.87 to 0.71 (archived ratings from an earlier run).
- **Paraphrasing the answers** leaves the picture unchanged: −0.04 on the paraphrased set.
- **Recognition.** Haiku shows no detectable recognition of its own writing (0.51 [0.36, 0.67] on 30 + 30 originals); Sonnet's recognition check did not run.

**What it means.** On this design, where every rating is a fresh call that sees only the answer, being the model that wrote the answer adds nothing detectable. A stronger model reading the same text does as well or better. On this test, the 0.82–0.91 error signal is matched or beaten by another model reading the same answer, especially one that knows the right answer. This matches Xiao et al.'s finding that the strongest model is the best judge of everyone's answers.

**What was cut.**
- The run cost more per Sonnet call than planned, and one call crashed the runner (DEVIATIONS D36, amendments 1 and 2). As a result, the paraphrase arm covers 60 of its 80 planned questions, and Sonnet's recognition check did not run.
- Recorded spend is $2.82. Calls lost in the crash add at most $0.20, so the true total is at most about $3.02. The cap was $3, so the run may have overshot it by up to 2 cents.
- Neither cut affects the primary result, which used the full 298 questions.

## AUROC of each judge for each author's errors

Cells: judge then author (HS = Haiku judging Sonnet's answers). I = HH + SS − SH − HS (each judge's overall skill cancels); Δ_H = HH − SH; Δ_S = SS − HS. 95% CIs from 2,000 question-level resamples.

| set | HH | SH | SS | HS | **I** | Δ_H | Δ_S |
|---|---|---|---|---|---|---|---|
| matched, all | 0.845 | 0.932 | 0.903 | 0.872 | **-0.055 [-0.103, -0.007]** | -0.086 [-0.146, -0.032] | +0.031 [-0.009, +0.073] |
| matched, disagreement | 0.432 | 0.850 | 0.865 | 0.583 | **-0.135 [-0.496, +0.229]** | -0.417 [-0.725, -0.114] | +0.282 [+0.073, +0.510] |
| matched, paraphrase subset (originals) | 0.806 | 0.906 | 0.825 | 0.765 | **-0.040 [-0.143, +0.056]** | -0.100 [-0.189, -0.018] | +0.060 [-0.021, +0.139] |
| you-gave self cells, all | 0.834 | 0.932 | 0.909 | 0.872 | **-0.060 [-0.118, -0.003]** | -0.098 [-0.153, -0.047] | +0.038 [-0.008, +0.085] |
| you-gave self cells, disagreement | 0.410 | 0.850 | 0.707 | 0.583 | **-0.316 [-0.608, -0.033]** | -0.440 [-0.767, -0.125] | +0.124 [-0.150, +0.420] |
| paraphrased, subset | 0.798 | 0.887 | 0.808 | 0.759 | **-0.040 [-0.157, +0.075]** | -0.089 [-0.202, +0.017] | +0.049 [-0.038, +0.140] |
| paraphrased, disagreement | 0.400 | 0.673 | 0.693 | 0.614 | **-0.195 [-0.530, +0.150]** | -0.273 [-0.713, +0.217] | +0.079 [-0.334, +0.479] |

Framing effect on the self cells ("an answer you gave" minus "another assistant"), all questions: Haiku -0.011, Sonnet +0.007.

## Recognition check ("how likely is it that you wrote this answer?")

| text | judge | AUROC own vs other [95% CI] | mean likelihood, own | mean likelihood, other | n own / other |
|---|---|---|---|---|---|
| original | Haiku | 0.51 [0.36, 0.67] | 49.7 | 47.8 | 30 / 30 |
| paraphrase | Haiku | 0.60 [0.44, 0.74] | 52.0 | 42.6 | 29 / 29 |

Paraphrases dropped for a changed or missing final answer: Haiku-authored 1, Sonnet-authored 1.

## Pre-registered reading: **no self-advantage**

# Calibration under format and question order

Pre-registered in `experiments/cal-format-order.md` (DM6), committed before any call. Tian et al.'s (2023) Verb. 1S top-1 protocol on the 300-question hard pool, in two formats; each question asked alone (two independent replicates) and inside 30 ten-question conversations in a forward and a reversed order. ECE: 10 equal-width bins, |accuracy − confidence| weighted by bin share (Guo et al., 2017). 95% CIs from 2,000 block-bootstrap resamples, paired across conditions. Costs at the batch rate.

## In plain English

(Hand-written after the run; excluded from reproduce.py's comparison.)

**The question.** The paper says a model's stated confidence is built by the question, its format and the conversation it lands in. If so, a calibration score is not a property of the model alone. We took one standard published way of measuring calibration, Tian et al.'s (2023) "give your best guess and the probability that it is correct", and ran it on Haiku and Sonnet over the 300 hard-pool questions. Three things were varied:
- **two formats:** the protocol's own probability (0.0–1.0), and the same sentence asking "out of 100 such questions, on how many would your guess be correct";
- **two orders:** each question inside a 10-question conversation, with the questions in forward or reversed order;
- **a fresh context:** each question also asked alone, twice, to measure plain run-to-run noise.

**The pre-registered result.**
- **Sonnet's calibration depends on the format.** Its expected calibration error (ECE) is 0.14 lower in the frequency format than in the probability format: −0.143 [−0.233, −0.066]. Two runs of the identical fresh protocol differ by only +0.005.
- **Haiku shows no detectable format effect** (−0.007 [−0.100, +0.075]).
- **Neither model's ECE changes detectably with question order:** +0.022 for Haiku and +0.055 for Sonnet, both intervals spanning 0.
- **The same question asked inside a conversation rather than fresh changes ECE for both models:** −0.15 for Haiku and −0.11 for Sonnet, both intervals excluding 0.

**The run had three flaws, so these numbers need care.**
- **60 of the pool's questions are phrased "Is the following claim true?".** The models answered "True"/"False", which the frozen parsing rule (yes/no only) rejected.
- **Open-form guesses.** On many "Is the (correct) answer X?" questions the models gave their own answer ("Guess: 43 ft") instead of yes/no. These were unparsed: 93–118 per probability cell against 35–41 per frequency cell for Haiku, and 80–155 per cell for Sonnet.
- **Some answers were dropped.** Some answers worked the problem out and ran past the 300-token limit. In a conversation, the frozen rule ends the conversation there.
- **The result:** each cell rests on 68–199 of its 300 questions, not 300.

**A post-hoc check (exploratory) found something more interesting.** Tian's wording, "the probability that it is correct", was written for open questions. On "Is the answer X?" questions the models read "it" two ways:
- as their guess, which is what the protocol intends;
- as the proposed answer X (for example "Guess: No, not 1968 / Probability: 0.1").

Which reading a model uses depends on the format and on the conversation:
- **Sonnet,** among its "no" guesses, gives a number below one half 50% of the time in the fresh probability format, 14–19% in the fresh frequency format, and 3–7% in frequency-format conversations.
- **Haiku** does so 73–82% of the time fresh and 48–68% in conversations.

So changing the format, or putting the question in a conversation, changes *which quantity the model reports*, not only how much it reports.

**The exploratory re-analysis.** With True/False mapped to yes/no, and scoring as Tian intended:
- Sonnet's ECE ranges from **0.06 to 0.27** across cells (each on 111–167 parsed questions). Replicate noise is about 0.01.
- Sonnet's format effect stays clear (−0.083 [−0.137, −0.032]).
- Question order still makes no detectable difference for either model.
- Scored the other way (the number as the probability of X), several contrasts change sign.

**What it means.**
- **For Sonnet, a calibration number from this protocol depended on the format and the context; for Haiku, on the context only. The direction of Sonnet's format effect depends on how the number is read.** For Sonnet, the format alone moves ECE by a factor of about 1.7 to 2.9 (exploratory scoring A; 2.0 to 2.9 in the pre-registered cells), far beyond run-to-run noise.
- **No effect of question order on aggregate ECE was detected here** (Haiku +0.022 [−0.076, +0.104], Sonnet +0.055 [−0.088, +0.162]). The individual confidences did move more between orders than between fresh replicates: mean |Δ| 0.22 against 0.10 for Haiku, and 0.65 against 0.14 for Sonnet in the probability format.
- **Part of the format effect is the format changing the question the model answers.** It is also a warning that Tian's protocol needs adapting before it is used on yes/no questions.
- **Budget:** $2.61 of the $3 (Haiku $0.12, Sonnet $2.49, batch rate).

# Pre-registered analysis (DM6, strict parse rule)

## haiku

Cost $0.12; abandoned conversations: 32.

| context | format | order / replicate | n | accuracy | mean confidence | ECE | Brier | AUROC | unparsed |
|---|---|---|---|---|---|---|---|---|---|
| conversation | probability 0.0–1.0 (Tian, verbatim) | fwd | 108 | 0.630 | 0.419 | **0.315** | 0.330 | 0.578 | 177 |
| conversation | probability 0.0–1.0 (Tian, verbatim) | rev | 121 | 0.678 | 0.464 | **0.382** | 0.384 | 0.546 | 160 |
| conversation | frequency out of 100 | fwd | 191 | 0.639 | 0.350 | **0.352** | 0.375 | 0.569 | 87 |
| conversation | frequency out of 100 | rev | 197 | 0.690 | 0.455 | **0.330** | 0.340 | 0.611 | 85 |
| fresh | probability 0.0–1.0 (Tian, verbatim) | r0 | 120 | 0.675 | 0.208 | **0.528** | 0.531 | 0.284 | 176 |
| fresh | probability 0.0–1.0 (Tian, verbatim) | r1 | 126 | 0.683 | 0.250 | **0.487** | 0.512 | 0.339 | 168 |
| fresh | frequency out of 100 | r0 | 199 | 0.603 | 0.225 | **0.465** | 0.492 | 0.367 | 97 |
| fresh | frequency out of 100 | r1 | 199 | 0.588 | 0.217 | **0.482** | 0.496 | 0.356 | 92 |

| contrast | ΔECE [95% CI] |
|---|---|
| **format** (frequency − probability), mean of both orders | **-0.007 [-0.100, +0.075]** |
| **order** (reversed − forward), mean of both formats | **+0.022 [-0.076, +0.104]** |
| noise baseline: fresh replicate 2 − replicate 1, mean of both formats | -0.012 [-0.050, +0.044] |
| conversation (mean of both orders) − fresh, mean of both formats | -0.152 [-0.220, -0.077] |
| format, forward only / reversed only | +0.037 [-0.088, +0.152] / -0.051 [-0.153, +0.052] |
| order, probability only / frequency only | +0.067 [-0.080, +0.191] / -0.022 [-0.117, +0.056] |

| format | mean per-question |Δconfidence|, forward vs reversed | same, fresh replicate 1 vs 2 | correctness flips, order / replicate |
|---|---|---|---|
| probability 0.0–1.0 (Tian, verbatim) | 0.219 | 0.098 | 11.4% / 0.0% |
| frequency out of 100 | 0.260 | 0.087 | 11.9% / 2.2% |

Mean confidence by position in the conversation (1–10): P: 0.17, 0.34, 0.34, 0.62, 0.55, 0.45, 0.43, 0.58, 0.53, 0.48; F: 0.20, 0.28, 0.48, 0.50, 0.48, 0.44, 0.45, 0.41, 0.38, 0.43

**Pre-registered reading, haiku: no detectable format dependence; no detectable order dependence.**

## sonnet

Cost $2.49; abandoned conversations: 105.

| context | format | order / replicate | n | accuracy | mean confidence | ECE | Brier | AUROC | unparsed |
|---|---|---|---|---|---|---|---|---|---|
| conversation | probability 0.0–1.0 (Tian, verbatim) | fwd | 68 | 0.941 | 0.720 | **0.227** | 0.210 | 0.748 | 147 |
| conversation | probability 0.0–1.0 (Tian, verbatim) | rev | 80 | 0.875 | 0.663 | **0.277** | 0.271 | 0.662 | 155 |
| conversation | frequency out of 100 | fwd | 112 | 0.795 | 0.815 | **0.079** | 0.132 | 0.861 | 149 |
| conversation | frequency out of 100 | rev | 118 | 0.839 | 0.848 | **0.139** | 0.141 | 0.843 | 129 |
| fresh | probability 0.0–1.0 (Tian, verbatim) | r0 | 101 | 0.871 | 0.473 | **0.420** | 0.405 | 0.528 | 176 |
| fresh | probability 0.0–1.0 (Tian, verbatim) | r1 | 98 | 0.857 | 0.497 | **0.378** | 0.387 | 0.551 | 179 |
| fresh | frequency out of 100 | r0 | 80 | 0.812 | 0.768 | **0.155** | 0.178 | 0.771 | 207 |
| fresh | frequency out of 100 | r1 | 78 | 0.731 | 0.703 | **0.207** | 0.244 | 0.715 | 215 |

| contrast | ΔECE [95% CI] |
|---|---|
| **format** (frequency − probability), mean of both orders | **-0.143 [-0.233, -0.066]** |
| **order** (reversed − forward), mean of both formats | **+0.055 [-0.088, +0.162]** |
| noise baseline: fresh replicate 2 − replicate 1, mean of both formats | +0.005 [-0.044, +0.061] |
| conversation (mean of both orders) − fresh, mean of both formats | -0.107 [-0.181, -0.030] |
| format, forward only / reversed only | -0.148 [-0.335, +0.001] / -0.138 [-0.273, -0.049] |
| order, probability only / frequency only | +0.050 [-0.207, +0.259] / +0.060 [-0.036, +0.108] |

| format | mean per-question |Δconfidence|, forward vs reversed | same, fresh replicate 1 vs 2 | correctness flips, order / replicate |
|---|---|---|---|
| probability 0.0–1.0 (Tian, verbatim) | 0.647 | 0.138 | 4.5% / 1.2% |
| frequency out of 100 | 0.098 | 0.077 | 8.3% / 3.4% |

Mean confidence by position in the conversation (1–10): P: 0.60, 0.69, 0.75, 0.81, 0.61, 0.62, 0.66, 0.70, 0.74, 0.79; F: 0.76, 0.82, 0.82, 0.87, 0.79, 0.85, 0.87, 0.85, 0.82, 0.86

**Pre-registered reading, sonnet: calibration depends on format; no detectable order dependence.**

Which model has the lower ECE is the same in all four conversation cells: **True**.

# Exploratory re-analysis (DM6a; not pre-registered)

Computed by `experiments/cal_format_explore.py` after the tables above had been seen. No new calls. Output in `results/calibration-under-format-exploratory.json`.

- **Parsing:** "Guess: True/False" is mapped to yes/no.
- **Scoring A** is Tian's intended reading: the number is the confidence in the guess.
- **Scoring B** is the proposed-answer reading: the confidence in the guess is p for a yes guess and 1 − p for a no guess.

**Share of "no" guesses whose stated number is below 0.5,** a sign of the proposed-answer reading:

| cell | Haiku | Sonnet |
|---|---|---|
| fresh, probability (r0 / r1) | 78% / 73% | 50% / 49% |
| fresh, frequency (r0 / r1) | 82% / 82% | 14% / 19% |
| conversation, probability (fwd / rev) | 55% / 48% | 23% / 28% |
| conversation, frequency (fwd / rev) | 68% / 64% | 7% / 3% |

**ECE under scoring A** (n per cell 111–255):

| cell | Haiku | Sonnet |
|---|---|---|
| conversation, probability, fwd / rev | 0.248 / 0.297 | 0.152 / 0.179 |
| conversation, frequency, fwd / rev | 0.304 / 0.295 | 0.061 / 0.104 |
| fresh, probability, r0 / r1 | 0.410 / 0.374 | 0.270 / 0.242 |
| fresh, frequency, r0 / r1 | 0.398 / 0.415 | 0.097 / 0.108 |

**Contrasts** (same block bootstrap as the pre-registered analysis):

| contrast | Haiku, A | Haiku, B | Sonnet, A | Sonnet, B |
|---|---|---|---|---|
| format (frequency − probability) | +0.027 [−0.032, +0.087] | +0.014 [−0.039, +0.070] | **−0.083 [−0.137, −0.032]** | **+0.088 [+0.035, +0.148]** |
| order (reversed − forward) | +0.020 [−0.053, +0.078] | −0.021 [−0.081, +0.051] | +0.035 [−0.044, +0.099] | −0.015 [−0.090, +0.064] |
| replicate (noise baseline) | −0.010 [−0.040, +0.035] | −0.005 [−0.032, +0.026] | −0.009 [−0.034, +0.027] | −0.005 [−0.041, +0.026] |
| conversation − fresh | −0.118 [−0.165, −0.067] | +0.081 [+0.034, +0.134] | −0.060 [−0.114, −0.006] | +0.057 [+0.010, +0.101] |

**Reading.**
- **Order:** not detected in any version.
- **The format effect for Sonnet** and the **conversation-against-fresh effect for both models** are far larger than replicate noise in every version. Their sign depends on which reading of the number is scored, because the format and the context change which reading the model uses.

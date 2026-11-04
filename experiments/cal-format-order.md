# Consequence demonstration: a standard calibration protocol under two formats and two question orders (pre-registration)

Written and frozen 2026-11-04 (America/Denver), in its own commit, before any call for this test. DEVIATIONS.md DM6. Budget **$3**: caps $0.30 (Haiku) and $2.60 (Sonnet) at the batch rate, enforced in code. Stop on any refusal: the batch and message IDs go to `results/refusal-mm-cal-<model>-turn<t>.md`, and nothing is reworded or retried.

## 1. In plain English

The paper argues that a model's stated confidence is built by the question, the format and the transcript, and so is not read out from a stored credence. If that is right, a calibration number (expected calibration error, ECE) belongs to a model *and* a format *and* a conversation, not to the model alone.

This test takes a standard published protocol, Tian et al.'s (2023) "Verb. 1S top-1", and runs it on Haiku and Sonnet over the 300 hard-pool questions in two ways:
- **in two formats:** the protocol's own probability, and a frequency version that changes nothing else;
- **in two question orders:** inside ten-question conversations, forward and reversed.

The question is whether the reported ECE changes.

## 2. The protocol

- **Format P** is Tian et al.'s Table 6 template for Verb. 1S top-1, verbatim, with each "\n" rendered as a newline and the question substituted for ${THE_QUESTION}:

  > Provide your best guess and the probability that it is correct (0.0 to 1.0) for the following question. Give ONLY the guess and probability, no other words or explanation. For example:
  >
  > Guess: <most likely guess, as short as possible; not a complete sentence, just the guess!>
  >  Probability: <the probability between 0.0 and 1.0 that your guess is correct, without any extra commentary whatsoever; just the probability!>
  >
  > The question is: {question}

- **Format F** is the same template with the probability replaced by a frequency. It is the paper's frequency format (F5 in test F):

  > Provide your best guess and the number of questions, out of 100 questions like this one on each of which you have the same evidence as on this one, on which your guess would be correct (0 to 100) for the following question. Give ONLY the guess and number, no other words or explanation. For example:
  >
  > Guess: <most likely guess, as short as possible; not a complete sentence, just the guess!>
  >  Frequency: <the number between 0 and 100 of such questions on which your guess would be correct, without any extra commentary whatsoever; just the number!>
  >
  > The question is: {question}

- **The questions:** the 300 hard-pool questions (`results/pool-run-3.json`). Each is a yes/no question ("…? Is the answer "X"?") with a gold label. A guess is correct if it equals the gold label.
- **Parsing.**
  - The guess is the first word after "Guess:", which must be yes or no.
  - The confidence is the number after "Probability:" (a value with "%" is divided by 100) or after "Frequency:" (divided by 100). It must lie in [0, 1].
  - Anything else is unparsed: counted, reported, and left out of that cell. In a conversation the reply stays in the history as given, whether or not it parsed.
- **Models:** `claude-haiku-5-5` with thinking disabled, as in the paper, and `claude-sonnet-5-5` with `thinking: between_tools`, its thinking-off mode (DM1). Plain-text output (the protocol's own format, so no structured output), max_tokens 300, default temperature, no system prompt.

## 3. Conditions

- **The blocks:** the 300 question ids, sorted and shuffled with `random.Random(4041)`, are cut into 30 blocks of 10.
- **The cells, per model:**

| context | what | conversations | calls |
|---|---|---|---|
| fresh | each question alone, one call, two independent replicates (r0, r1), in both formats | 1,200 | 1,200 |
| conversation, forward | one conversation per block and format: the block's 10 questions in order, each as the full protocol prompt, the model's replies kept in the history ("shown") | 60 | 600 |
| conversation, reversed | the same, in reversed order | 60 | 600 |

- **Total:** 2,400 calls per model, run as batch waves (one per turn; the fresh calls in wave 1). The rules of `mm_common.py` apply.

## 4. Statistics

- **ECE** (Guo et al., 2017): 10 equal-width confidence bins, the last one closed at 1.0. ECE = Σ_b (n_b / N) · |accuracy_b − mean confidence_b|.
  - Tian et al. describe the error as "(squared)" in their text. The absolute form is used here as the standard one.
  - Tian et al. also report temperature-scaled ECE; that is not used here.
- **Cells:** for each model × context × format × order or replicate, report n, accuracy, mean confidence, ECE, Brier score, AUROC (confidence for correct against incorrect) and unparsed count.
- **Primary contrasts, per model:**
  1. **Format:** ΔECE_format = mean over the two orders of [ECE(F, order) − ECE(P, order)], in the conversation cells.
  2. **Order:** ΔECE_order = mean over the two formats of [ECE(format, reversed) − ECE(format, forward)].
- **Intervals:** 95% CIs from 2,000 block-bootstrap resamples (seed 4042). The 30 blocks are resampled with replacement, and every cell is recomputed on the same resampled questions, so the contrasts are paired.
- **Reported alongside, with the same CIs:**
  - the **noise baseline:** ECE(fresh r1) − ECE(fresh r0), averaged over formats. It is what two runs of the same protocol on the same questions differ by;
  - **conversation against fresh:** the mean of the two conversation orders minus fresh r0, averaged over formats;
  - **each format contrast within each order,** and **each order contrast within each format.**
- **Descriptives:**
  - the mean per-question |Δconfidence| between the forward and reversed conversations, against between the two fresh replicates;
  - the share of questions whose correctness flips, between orders and between replicates;
  - mean confidence by position in the conversation;
  - whether the model with the lower ECE is the same in all four conversation cells.

## 5. Pre-registered reading, per model

1. **Calibration depends on format** if the 95% CI of ΔECE_format excludes 0.
2. **Calibration depends on question order** if the 95% CI of ΔECE_order excludes 0.
3. **Otherwise, no detectable dependence** on that factor.

Each finding is reported with its point estimate and the noise baseline beside it. A dependence is a consequence for practice: the paper's Section 5.3 claim that calibration should be reported with its format and transcript. No dependence is evidence that, for this protocol and these models, ECE is robust to these changes despite the construction effects found in the paper.

## 6. What it cannot do

- **One draw per question per cell**, so sampling noise enters every ECE. The fresh replicates measure how large it is.
- **ECE with 300 questions and 10 bins is itself noisy and biased upward.** The contrasts are paired, which removes the shared bias but not the noise.
- **The hard pool is mostly questions both models get right:** Haiku's base accuracy 85%, Sonnet's 90%, with thinking. ECE is dominated by the high-confidence bins.
- **Only one protocol, two formats and one kind of order change.** The result does not generalise to other protocols by itself.

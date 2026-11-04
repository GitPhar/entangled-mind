# Multi-model replication 1 of 3: six elicitation formats on Sonnet and Opus (pre-registration)

Written and frozen 2026-11-04 (America/Denver), in its own commit, before any Sonnet or Opus call for this test. DEVIATIONS.md DM2. Caps **$2.20 (Sonnet) and $4.30 (Opus)**, at the batch rate, enforced in code. Stop on any refusal: the batch's message ID goes to `results/refusal-mm-gm3b-<model>.md`, and nothing is reworded or retried.

## 1. In plain English

Test F (`gm3b-format-invariance.md`, D38) asked Haiku about its own contested claims in six ways and found no single credence behind the answers. This run asks `claude-sonnet-5-5` and `claude-opus-5-5` the same questions about the same claims, and applies the same test with the same criterion. Budget forces half the claims.

## 2. What is identical to D38

- The six formats, their wording, the statement introduction, the bet prices, the coin positions, R = 10 repeats, and the structured-output schemas (`gm3b_format_invariance.prompt`, imported unchanged).
- One scale direction (0 = certainly false, 100 = certainly true) and the 7-point verbal scale in place of a reversed scale.
- The encoding, the two models L1 and L6, the prior, the fitting procedure, the 2-fold even/odd cross-validation, the item bootstrap (2,000 resamples, seed 3131), and the descriptives: all `gm3b_format_invariance.analyse`, run unchanged on the new calls.
- The pre-registered reading (D38 §6): **no single credence** if more than half the claims have ΔLL_c > 0 and the CI of the mean ΔLL lies above 0; **one credence suffices** if the CI lies below 0, or contains 0 with at most half the claims positive; **mixed** otherwise. It is applied to each model separately.

## 3. What differs, and why

- **Claims: 80, not 160.** The 20 items are experiment 5's candidates 1–10 and 21–30 in `split-exp5.json` order, which are 10 items Haiku answered wrongly and 10 it answered rightly (the list holds 20 wrong, then 20 right). With their 4 chain claims each, that is 80 claims × 6 formats × 10 repeats = **4,800 calls per model**. The full design would cost about $7.7 on Sonnet and $15 on Opus at list price, against a $20 budget for all three replications.
- **Thinking.**
  - Sonnet 5.5 rejects `thinking: disabled`. Its thinking-off mode is `thinking: {"type": "between_tools"}`, used here.
  - Opus 5.5 cannot turn thinking off at all. It runs at effort `low`, the minimum. Its thinking text is never returned. In the DM1 pilot, single-turn rating calls produced no thinking tokens.
- **Calls go through the Message Batches API** (50% of list price), in chunks of 1,600. The stop rules are those of `mm_common.py`: cap checked before each chunk, stop at the first refusal (no further chunk is submitted), API errors resubmitted unchanged at most twice, max_tokens hits recorded as no answer. max_tokens is 1,000 (100 for Haiku in D38), so that a low-effort thought cannot truncate the answer.
- **Temperature** is the API default for each model (no explicit value is accepted).

## 4. Also reported

- **The Haiku reference on the same 80 claims,** from D38's archived calls, re-analysed with the same code. It was computed while the analysis code was being tested, before this file was frozen: mean ΔLL +19.42 [+15.40, +23.21], 86% of claims positive, reading "no single credence". No Sonnet or Opus data existed then.
- **Secondary: test F′** (`gm3c_heldout_format.main`, D46), run unchanged on each model's calls. It reads mean Q = R²(cross) / R²(ceiling) against 0.75 and 0.5. With 20 items its frozen fold rule (`i // 8`) forms 3 item folds (8, 8 and 4 items) rather than D46's 5. On the Haiku 80-claim reference it gives Q = 0.29 [0.19, 0.43].
- Kendall's W, the pairwise Spearman correlations, the share of claim pairs ordered differently from the 0–100 rating, and ΔLL by format, for each model.

## 5. What it cannot do

- 20 items rather than 40, so the CIs are wider than D38's.
- Opus runs with minimal thinking rather than none. Sonnet's `between_tools` and Haiku's `disabled` are both "no thinking" modes, but they are different API settings.
- Stronger models may answer most of these claims near-deterministically. Then both L1 and L6 fit the training repeats almost exactly, and ΔLL depends on how much reproducible format-by-claim structure remains. That is the quantity the test measures, so this is a property of the models, not a flaw of the test.

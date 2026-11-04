# Completing Opus's six-format arm (80 claims), with test F′ (pre-registration)

Written and frozen 2026-11-04 09:50 (America/Denver), in its own commit, before any call of this run. DEVIATIONS.md D49. This continues DM2 (`experiments/mm-gm3b-format-invariance.md`), whose Opus arm was budget-stopped at 26 of 80 claims (DM4a).
- **Budget:** **$6.40 of new spend**, at the batch rate, enforced in code.
- **Stop on any refusal:** the batch's message ID goes to `results/refusal-mm-gm3b-opus-completion.md`, and nothing is reworded or retried.

## 1. In plain English

Haiku's six ways of answering the same question disagree too much to come from one belief. Sonnet's partly agree. On the 26 statements its budget allowed, Opus's agreed almost perfectly. Those 26 all came from questions Haiku got wrong, though, and they were too few for the held-out-format test (F′).

This run asks Opus the remaining 54 statements, so that all three models are compared on the same 80. It then applies both tests:
- DM2's one-credence test;
- test F′: predict each format from the other five.

The paper's claim about Opus is narrowed or widened by a rule frozen here (Section 4).

## 2. What is identical to DM2

The following are unchanged:
- the 20 items, their 80 claims, the six formats, the prompts, the schemas and R = 10;
- `claude-opus-5-5` at effort `low`, with max_tokens 1,000;
- the Batches API and the stop rules of `mm_common.BatchRunner`, including the 1.25 projection factor;
- the cache `results/mm-gm3b-opus-calls.json`, where the 1,600 calls already made are kept and not repeated;
- the analysis, `mm_gm3b.analyse`, which is `gm3b_format_invariance.analyse` on complete claims, with DM2's reading;
- test F′, which is `gm3c_heldout_format.main` with DM2's 3-fold item rule (`i // 8` over 20 items).

The code is `experiments/mm_gm3b_opus_complete.py`. It imports all of the above unchanged.

## 3. What differs, and why

- **One batch per item,** rather than chunks of 1,600. The first batch is h221, of which 2 claims are complete and 1 is partly run (80 requests). Then the 13 untouched items follow, alternating between items Haiku answered rightly and wrongly:

  h142, h279, h214, h127, h187, h238, h019, h173, h149, h048, h291, h093, h183

  That is 240 requests each, **3,200 requests** in all. If the cap stops the run, it stops between items, and the completed items stay balanced between the two kinds.
- **The cap counts new spend only.** At Opus's observed DM2 rate ($0.00194 per call), the run costs about **$6.21**. The runner checks before each batch that new spend + 1.25 × (batch size × mean cost so far) ≤ $6.40, so the last batch may not fit.
- **If the cap stops the run:**
  - the primary analysis uses the complete claims, as in DM2;
  - test F′ uses the complete *items*, with the same fold rule;
  - the result file reports how many.
  The pre-registered readings below apply unchanged.

## 4. Pre-registered readings

**Primary (DM2's rule, on Opus's complete claims):**
- **no single credence** if more than half the claims have ΔLL > 0 and the CI of the mean lies above 0;
- **one credence suffices** if the CI lies below 0, or contains 0 with at most half the claims positive;
- **mixed** otherwise.

**Test F′ (D46's rule):**
- **a usable single belief** if the CI of mean Q lies wholly above 0.75;
- **little format-free belief** if it lies wholly below 0.5;
- **partial** otherwise.

**The paper's Opus claim** (`paper/no-credence-to-read.md`, Section 4.6, which currently says "not supported" on Opus):

| outcome | the paper says |
|---|---|
| F′ CI wholly above 0.75 | **does not hold on Opus**: one credence predicts each left-out format close to its own ceiling. The claim is narrowed from "not supported" to "contradicted on Opus". |
| F′ CI wholly below 0.5 **and** primary *no single credence* | **holds on Opus**: the claim is widened to all three models. |
| anything else | **holds partly on Opus**, stated as for Sonnet. |

**Kendall's W is reported for all three models.** If the arm completes, W is on the same 80 claims, which makes the W trend item-matched.

## 5. Disclosed before freezing

While testing the analysis code on the archived calls, before this file was frozen, test F′ was computed on Opus's 6 complete items (24 claims): **mean Q = 0.96 [0.92, 0.98]**. The paper rule of Section 4 was written in the code before that number was seen. The primary statistic on those 26 claims was already public (DM2: +0.42 [−1.83, +2.69], 58% positive, W 0.86). Both are recorded in `results/mm-gm3b-opus-first26.json`, a snapshot of the arm as it stood at freezing. No data from the 54 new claims existed.

## 6. Also reported (descriptive)

- Opus's mean ΔLL on the 26 earlier claims against the 54 new ones.
- The ΔLL by format, the Spearman range and the discordant-pair range, all from `mm_gm3b.analyse`.

## 7. What it cannot do

- 20 items, so the intervals stay wide.
- Opus thinks briefly even at effort `low`. Haiku and Sonnet do not think at all.
- Test F′ has 3 item folds here, not D46's 5.

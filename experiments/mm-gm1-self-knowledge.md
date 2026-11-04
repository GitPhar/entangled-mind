# Multi-model replication 2 of 3: privileged self-knowledge, Sonnet × Opus (pre-registration)

Written and frozen 2026-11-04 (America/Denver), in its own commit, before any call for this test. DEVIATIONS.md DM3. Cap **$4.60** at the batch rate, enforced in code. Stop on any refusal: the batch and message IDs go to `results/refusal-mm-gm1-<step>.md`, and nothing is reworded or retried.

## 1. In plain English

Test P (`gm1-self-knowledge.md`, D36) let Haiku and Sonnet each judge both their own and the other's answers. It found that being the author does not help. This run repeats the test with Sonnet and Opus as the two models, with the same prompt, the same statistic and the same reading.

## 2. What is identical to D36

- **The 298 hard-pool questions** (`gm1_self_knowledge.load()`).
- **The matched judge prompt** ("an answer another assistant gave"), its schema `{"confidence": integer}`, clamped to 0–100.
- **The judge settings**, which are those of `llm.self_confidence`: no thinking parameter (each model's default), max_tokens 4,000.
- **Only the visible answer is ever shown** to a judge.
- **The AUROC cells, the 2,000-resample question-level bootstrap** (seeds from 1001, in D36's order) and the interaction statistic. With S = Sonnet and O = Opus, judge first and author second, the statistic is I = SS + OO − OS − SO.
- **The reading** (D36 §5):
  - **self-advantage** if I > 0 on all questions and the CI of I on the disagreement subset lies above 0;
  - **other-advantage** if the disagreement CI lies below 0;
  - **no self-advantage** otherwise.
- **The disagreement subset:** the questions where the two authors' correctness differs (Ashuach et al.'s definition).

## 3. What is new or different

- **Opus as author.** Opus answers the 298 questions with `llm.BASE_PROMPT`, the settings of every base run: adaptive thinking (summary archived, never shown to any judge), the model's default effort and max_tokens 16,000. An answer that hits the token cap or gives no FINAL ANSWER line is excluded, as in pool runs 3 and 4. Correctness is scored against the hard pool's gold label.
- **The cells.**
  - **SS is direction 1's archived matched-framing cell**, unchanged (`results/gm1-calls.json`).
  - **SO, OS and OO are new.**
  - The primary statistic uses the questions on which all four cells have a rating.
- **Not run** (budget):
  - the paraphrase arm and the recognition check;
  - the archived-framing ("you gave") cells, which do not exist for Opus.

  D36's paraphrase control applies only if reading 1 holds. If it does here, the reading is reported as "self-advantage, paraphrase control not run".
- **Calls go through the Message Batches API.**
  - Step A is Opus's 298 answers; step B is the three judge cells, interleaved by question, in chunks of 300.
  - The rules of `mm_common.py` apply. A cap stop in step B leaves complete questions for the earlier chunks.
- **Opus's default effort is `medium`; Sonnet's is `high`.** "Model default" is the D36 rule, applied to both models.

## 4. Also reported

- Each author's accuracy and error count on the complete set.
- Δ_S = SS − OS and Δ_O = OO − SO, with CIs. These are the per-author self-advantages; capability is expected to dominate them.
- D36's Haiku × Sonnet interaction, alongside, for reference.

## 5. What it cannot do

- **Opus will likely make few errors on this pool.** AUROCs for Opus's errors, and the disagreement subset, rest on few cases, so the CIs will be wide.
- **Sonnet and Opus are closer in capability than Haiku and Sonnet.** That makes the pair a cleaner test of authorship, but it cannot rule out a judge-skill × author-difficulty interaction.
- **The SS cell was collected about 5 hours before the new cells,** with the same prompt, model id and settings.

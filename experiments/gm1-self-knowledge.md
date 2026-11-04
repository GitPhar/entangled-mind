# Gold-map direction 1: privileged self-knowledge, a 2×2 self-versus-other confidence test (pre-registration)

Written and frozen 2026-11-04 (America/Denver), in its own commit, before any call. DEVIATIONS.md D36. Budget **$3**, enforced in code. Stop on any refusal: the request ID goes to `results/refusal.md`, and nothing is reworded or retried.

## 1. In plain English

The model's own stated confidence is the project's best signal of when it is wrong: AUROC 0.82 on Haiku and 0.91 on Sonnet. Two explanations fit that:
- **Privileged self-knowledge.** The model knows something about its own weak spots that a reader of its answer doesn't.
- **Good reading.** Confidence is just a careful reading of the answer text, and any capable reader of the same text could do as well.

The test lets each model judge both its own answers and the other model's answers, and asks whether being the author helps.

One thing makes this hard. The literature session's full-text read of Xiao et al. (2509.24988, Table 23) found that a stronger model is usually the better judge of *everyone's* answers. So Sonnet will probably judge Haiku's answers better than Haiku does, whatever authorship contributes. The primary statistic therefore cancels each judge's overall skill, using a judge × author interaction. A paraphrase arm then checks that any self advantage isn't just the model recognising its own writing style.

## 2. Material

- **Authors:**
  - Haiku's hard-pool answers (`results/pool-run-3.json`);
  - Sonnet's hard-pool answers (`results/pool-run-4.json`).
  - The 298 questions both answered with a scored outcome are used.
  - Only the visible answer is shown to any judge. Thinking content is never shown.
- **Judges:** `claude-haiku-5-5` and `claude-sonnet-5-5`. Settings are identical to the archived arm-G calls (`llm.self_confidence`): no thinking parameter (model default), structured output `{"confidence": integer}`, and max_tokens 4,000.
- **Disagreement subset:** the 26 questions where the two authors' *correctness* differs. Of these, Haiku is wrong on 19 and Sonnet on 7. This is Ashuach et al.'s definition (2604.12373), as the literature session confirmed.

## 3. Calls

| step | what | calls (Haiku / Sonnet) |
|---|---|---|
| 1 | **Matched-framing 2×2 on the originals.** Each judge rates each author's 298 answers with the *same* prompt (below), so self and cross cells differ only in who wrote the answer. | 596 / 596 |
| 2 | **Paraphrases.** Haiku, with thinking disabled, rewrites each answer of the paraphrase subset (below) with the paraphrase prompt. | 160 / 0 |
| 3 | **Paraphrase 2×2.** Both judges rate both authors' paraphrased answers with the matched prompt. | 160 / 160 |
| 4 | **Recognition check.** On 30 subset questions per author, each judge says how likely it is that it wrote the answer, for originals and for paraphrases. | 120 / 120 |

- **Matched prompt** (for all four cells):

  > Here is a yes/no question and an answer another assistant gave to it.
  >
  > Question: {question}
  >
  > The assistant's answer:
  > {answer}
  >
  > How confident are you, from 0 to 100, that this final answer is correct? Give only the number.

- **Paraphrase prompt** (thinking disabled, output `{"text": string}`):

  > Rewrite the following answer to a yes/no question in your own words. Keep every consideration, the reasoning and the conclusion exactly as they are; do not add, remove or correct anything. Keep the final line exactly as it is.

  If a paraphrase's final answer line differs from the original's, or is missing, that question is dropped from steps 3 and 4 for that author, and the drop is reported.

- **Recognition prompt** (output `{"likelihood": integer}`):

  > Here is a yes/no question and an answer to it. Question: … Answer: … How likely is it, from 0 to 100, that you wrote this answer? Give only the number.

- **Paraphrase subset (80 questions, the same for both authors):**
  - the 49 questions where either author is wrong (which includes the whole disagreement subset);
  - 31 questions both got right, drawn with `random.Random(1001)`.
  - The recognition check uses the first 30 of the subset in `random.Random(1002)` order.
- **Archived self ratings** used alongside: the arm-G ratings with the "an answer you gave" prompt, in `results/arm-g-confidence.json` and `results/sonnet-arm-g-confidence.json`.
- **Cost estimate:**
  - Sonnet calls about $0.003 each (D28 rate): about $2.6;
  - Haiku calls about $0.0002 each: about $0.2.
- **Run order and the cap.** The steps run in the order above, and the $3 cap is enforced in code. If the cap stops the run, later steps are reported as not run. Step 1 alone is enough for the primary statistic.

## 4. Statistics

- Write A(J, X) for the AUROC of judge J's score 100 − confidence for author X's errors.
- **Primary: the self × author interaction.** I = [A(H,H) + A(S,S)] − [A(S,H) + A(H,S)], on the matched-framing originals (step 1). Each judge appears once in a self cell and once in a cross cell, so its overall skill cancels.
- **Bootstrap.** I is computed on all 298 questions and on the disagreement subset. The 95% CI comes from 2,000 question-level resamples (seed 1001), with all four cells resampled together.
- **Secondary statistics:**
  - **The per-author self advantages:** Δ_H = A(H,H) − A(S,H) and Δ_S = A(S,S) − A(H,S). These are the gold map's original criterion; capability is expected to dominate them.
  - **The archived-framing interaction** I_you, which uses the "you gave" self cells, and the **framing effect** on each self cell (A with "you gave" − A with "another assistant").
  - **The paraphrase interaction** I_para on the subset, against I on the same 80 originals.
  - **Recognition.** The AUROC of each judge's "I wrote it" likelihood for its own versus the other model's answers, on originals and on paraphrases, with bootstrap CIs (seed 1003).

## 5. Pre-registered reading

1. **Self-advantage:** I > 0 on all questions, **and** the CI of I on the disagreement subset lies above 0.
2. **Other-advantage:** the CI of I on the disagreement subset lies below 0.
3. **No self-advantage:** anything else. The paper then says that the 0.82–0.91 is explained by reading the answer, as far as this test can see.
4. **The paraphrase control**, applied if reading 1 holds:
   - the advantage **survives paraphrase** if I_para > 0 and I_para ≥ half of I on the same 80 originals;
   - if the paraphrases still let judges recognise their own answers (recognition CI above 0.5), the control is reported as **incomplete**.
5. **Reported in every case:**
   - Δ_H and Δ_S;
   - the framing effect;
   - the recognition AUROCs, on originals, which say whether self-recognition is even possible here.

## 6. What it cannot do

- The disagreement subset has 26 questions, so only a large interaction can register there.
- There are two judges of different strength. A same-capability pair is not available on this stack. The interaction cancels each judge's main effect, but it cannot rule out a judge-skill × author-difficulty interaction.

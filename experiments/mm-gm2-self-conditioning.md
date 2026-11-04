# Multi-model replication 3 of 3: shown, redacted and planted transcripts on Sonnet and Opus (pre-registration)

Written and frozen 2026-11-04 (America/Denver), in its own commit, before any call for this test. DEVIATIONS.md DM4. Caps **$2.40 (Sonnet) and $6.00 (Opus)** at the batch rate, enforced in code. Stop on any refusal: the batch and message IDs go to `results/refusal-mm-gm2-<model>-wave<t>.md`, and nothing is reworded or retried.

## 1. In plain English

Test T (`gm2-self-conditioning.md`, D37) edited Haiku's transcript between turns. The model's earlier ratings were shown, hidden ("[rating recorded]") or replaced by numbers 15 points above or below its usual rating. Hiding the answers did not remove the effect of question order, so the question alone changes the judgment. This run applies the same edits to Sonnet and Opus. Budget forces 4 conversations per cell rather than 10.

## 2. What is identical to D37

- **The 10 items and their 4 chain claims** (`gm2-planted-values.json`, `chain_claims`).
- **The chains** O1–O4 and MF (`exp5_run.turns_for`), the opening and the questions (`exp5_run.opening`, `exp5_run.question`), anchor (a) only, and the structured output `{"rating": integer}`.
- **The four conditions and the transcript editing:**
  - shown keeps the model's reply;
  - redacted puts `[rating recorded]` in its place;
  - planted puts `{"rating": X}` in the model's own turn.

  The final rating is always real.
- **The planted-value rule:** high = min(98, round(m) + 15), low = max(2, round(m) − 15).
- **The whole analysis,** which is `gm2_self_conditioning.compute`, unchanged:
  - the shown-condition gate (5,000 permutations, seed 2002);
  - OE per condition;
  - R = OE_redacted / OE_shown with the item bootstrap (seed 2003);
  - b_MF, the next-rating pull, the final-M shift and MF repeat agreement.
- **The reading** (D37 §5):
  - **untestable** if the gate p ≥ 0.05;
  - **question-driven** if the R CI lies wholly at or above 0.5;
  - **self-anchoring** if the R CI lies wholly below 0.5;
  - **leaning** otherwise.
  - Memory against stable judgment is read from MF agreement, shown against redacted, with the 10-point line.

  Each model is read separately.

## 3. What differs, and why

- **R = 4 conversations per item × chain × condition**, not 10. That gives 800 conversations and 4,320 calls per model. At R = 10 and list price the design would cost about $11 on Sonnet and $26 on Opus. With n = 4 per order, the per-item variance components are noisier, but they are estimated the same way.
- **The planted values come from each model's own first-turn ratings.** D37's m came from Haiku's archive. Here m is the mean of the model's first-turn ratings in this run:
  - for S_k, every O-chain that opens with S_k: 4 conditions × 4 repeats = 16;
  - for M, every MF chain: 16.

  The first turn is the same prompt in every condition, so these are the model's unconditioned ratings, as D37's were for Haiku. The values are fixed after wave 1 and before any later turn. They are written to `results/mm-gm2-<model>-planted.json`.
- **Thinking.** Sonnet uses `thinking: between_tools`, its thinking-off mode; Opus uses effort `low`. Opus's thinking text is never returned and never placed in the transcript: each assistant turn in the history is the reply text, edited as above. max_tokens is 1,000 (200 in D37).
- **Calls go through the Message Batches API, one batch per turn ("wave"), up to 6 waves.**
  - A conversation that meets a refusal or a max_tokens stop ends there and is excluded.
  - On a refusal, no further wave is submitted.
- **Budget fallback, checked after every wave.** The projection prices each remaining wave at the latest wave's mean cost per call, times 1.12 per further turn. If the projected total exceeds the cap, the highest remaining repeat index is abandoned for the rest of the run (R = 4 → 3, then → 2), and the analysis uses the repeats kept. The pilot predicts about $2.1 for Sonnet and $4.3–5.6 for Opus.

## 4. Also reported

- **The Haiku reference at R = 4:** D37's archive restricted to repeats 0–3, with D37's planted values. It was computed while the code was being tested, before this file was frozen: R = 2.01 [1.04, 4.43], question-driven; MF agreement 78% shown, 25% redacted. No Sonnet or Opus conversation existed then.
- Per item, for each model: OE shown and redacted, the final M by order, and MF M₂ by condition.

## 5. What it cannot do

- **There are 10 items, as in D37, and fewer repeats,** so R's CI will be wide.
- **Stronger models may give nearly the same rating whatever the order.** Then the gate fails and the decomposition is untestable for that model. That is itself a finding about the model: no order effect to decompose.
- **The redaction placeholder is the same unusual turn as in D37,** and its own effect is not separated here.

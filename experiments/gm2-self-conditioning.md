# Gold-map direction 2: measurement as self-conditioning, with shown, redacted and planted transcripts (pre-registration)

Written and frozen 2026-11-04 (America/Denver), in its own commit, before any call. DEVIATIONS.md D37. Budget **$1**, enforced in code. Stop on any refusal: the request ID goes to `results/refusal.md`, and nothing is reworded or retried.

## 1. In plain English

Direction 9 showed that asking the model earlier questions changes its later answers. Two things are added to the conversation when a question is asked:
- the question itself;
- the model's recorded answer to it.

This run separates the two by editing the transcript between turns:
- **shown:** the model sees its own earlier ratings, as normal;
- **redacted:** each earlier rating is replaced by "[rating recorded]", so the model sees the questions but not its answers;
- **planted high** and **planted low:** each earlier rating is replaced by a fixed number 15 points above or below the model's usual rating for that question. The number sits in the model's own turn.

If the order effect survives redaction, asking a question changes the judgment even with no record of the answer. That is a measurement effect in the strict sense. If redaction removes it, the model's order effects come from anchoring on its own earlier answers, a plain classical mechanism.

## 2. What the literature gives us (full-text reads by the literature session)

- **Kumaran et al.** (2507.03120): in binary choice with advice, hiding the model's first answer raised change of mind under opposing advice from 39.2% to 85.0%.
  - When the shown first answer was replaced by a visibly wrong one, the model changed in 74.5% of cases, against 8.8% when shown its own. So it does not simply copy.
  - When the same answer was attributed to another LLM, the shown/hidden difference vanished (33.2% vs 31.3%). The bias needs self-attribution.
- **Design consequences:**
  - Planted values here sit in the model's own assistant turn.
  - They are **±15 points** rather than the gold map's ±30, to stay plausible. In experiment 4 run 3 the model rejected another person's provided ratings 30 points away.
- **Other precedents:** Thought Anchors (2506.19143) resamples chain-of-thought sentences. Lanham et al. (2307.13702) and Thought Branches (2510.27484) edit chains of thought. None of them uses graded multi-question chains or question-order effects.

## 3. Design

- **Items:** the first 10 experiment-5 candidates (`exp5_run.candidates()[:10]`, the run-2 items), each with its 4 frozen chain claims (`experiments/split-exp5.json`).
- **Chains:** O1–O4 (the four sub-questions in the four Latin-square orders, then M) and MF (M, then S1–S4, then M), built exactly as `exp5_run.turns_for`.
- **Scale:** one direction only, anchor (a): "0 = certainly false, 100 = certainly true".
- **Conditions:** shown, redacted, planted-high, planted-low.
- **Repeats:** R = 10 conversations per item × chain × condition. That gives 10 × 5 × 4 × 10 = **2,000 conversations** and about 10,800 calls.
- **Model and settings:** `claude-haiku-5-5`, thinking disabled, default temperature, and the structured output `{"rating": integer}`. The prompts are identical to experiment 5's.
- **Transcript editing:**
  - The model's actual reply is recorded at every turn.
  - What goes into the history for the *next* turn depends on the condition:
    - **shown:** the actual reply;
    - **redacted:** the text `[rating recorded]`;
    - **planted:** `{"rating": X}`, where X is that question's high or low value.
  - The final rating of each conversation is always real, and nothing follows it.
- **Planted values** are fixed in `experiments/gm2-planted-values.json` in this commit:
  - m is the archived anchor-(a) mean for that question: S from run 1, every anchor-(a) rating of the claim; M from run 2's 10 anchor-(a) B0 ratings;
  - high = min(98, round(m) + 15) and low = max(2, round(m) − 15).
  - Where m sits beyond 83 or below 17, clipping shrinks the difference. One S value (h261 claim 0, m = 99.3) has a "high" below its mean.
- **Cost:** about 10,800 calls at about $0.00003 each (experiment 5's rate) is about $0.35. Cap **$1**.

## 4. Statistics

- **Order effect within a condition, per item:**
  - From the final M of O1–O4, take the between-order variance component, VC = max(0, (MS_between − MS_within) / n), from a one-way ANOVA with n = 10 per order.
  - The condition's order effect is OE = √(mean over items of VC), in rating points.
- **Gate:** the shown condition must have an order effect.
  - The test is a permutation test of Σ_items MS_between, shuffling order labels within item (5,000 permutations, seed 2002).
  - If p ≥ 0.05, the run is reported as **untestable**: there is no order effect to decompose.
- **Primary:** R = OE_redacted / OE_shown, with a 2,000-resample item-bootstrap CI (seed 2003).
- **Planted effects (reported):**
  1. **Self-anchoring in MF:** b_MF = mean over items of [M₂(high) − M₂(low)] / [X_M(high) − X_M(low)]. This is how far the final main rating follows the planted first main rating. It comes with an item-bootstrap CI.
  2. **Next-rating pull:** in O1–O4 and MF, the actual ratings at positions 2 onward under planted-high minus planted-low, in points, averaged per item and with a CI.
  3. **Final M:** the shift in final M in O1–O4 between planted-high and planted-low. Two chain claims lean yes and two lean no, so a content-weighted reading predicts about 0 here.
  4. **Order effects under planting:** OE_planted-high and OE_planted-low.
- **Replicability (MF):** the share of MF conversations with |M₂ − M₁| ≤ 5 under shown, against redacted, where M₁ is the model's actual first rating.
  - In redacted, the model never sees M₁, so agreement there measures a stable judgment rather than memory.

## 5. Pre-registered reading

1. **Question-driven (a measurement effect in the strict sense):** the R CI lies wholly at or above 0.5. Asking alone changes the judgment, with no record of the answer.
2. **Self-anchoring:** the R CI lies wholly below 0.5. The order effects come from conditioning on the model's own recorded answers.
3. **Leaning:** otherwise. The point estimate is reported as leaning one way, and this is not counted as decisive.
4. **Supporting evidence for self-anchoring**, reported in every case: b_MF > 0 with a CI excluding 0 and the next-rating pull > 0 with a CI excluding 0.
5. **Memory versus stable judgment:** if MF agreement under redaction is close to agreement under shown (within 10 percentage points), the repeat agreement reflects a stable judgment. If it is much lower, it reflects memory of the earlier answer.

## 6. What it cannot do

- It uses 10 items. The R CI may be wide.
- Redaction removes the number but keeps the turn, so "[rating recorded]" is itself a small intervention. Planting tests whether the number matters, given that turn.

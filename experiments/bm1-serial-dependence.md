# Biomimetic map (rev. 1 §3.1; rev. 2 §§3.0–3.2): source dependence, with run 3's anchors re-presented as the model's own earlier answer (pre-registration)

Written and frozen 2026-11-04 (America/Denver), in its own commit, before any call. DEVIATIONS.md D44. Budget **$0.40**, enforced in code (the estimate is $0.23). Stop on any refusal: the request ID goes to `results/refusal.md`, and nothing is reworded or retried.

**Shared with direction 2** (`experiments/gm2-self-conditioning.md`, D37) where the two overlap:
- the planted value sits in the model's **own assistant turn**, formatted exactly as its structured output;
- one scale direction;
- the same model and settings.

Direction 2 plants answers inside graded multi-question chains. This test plants one answer to one statement and compares it with run 3's archived "another person" condition, which used the same values. **Direction 2's result was known when this was frozen** (`results/gm2-self-conditioning.md`). The design below is the one the biomimetic map specified before that result (§3.1).

**Revision 2 of the map** (`f824e14`), after full reads, changed the predictions. Sean's overnight list keeps revision 1's design and budget: run 3's ±30 anchors, own against the archived other-person condition, no lag arm, about $0.23. Within that design, the readings follow revision 2:
- **Choice-dependent self-consistency** (Kumaran: the bias is abolished when the answer is attributed to another LLM; Talluri) predicts **own > other**.
- **Stimulus-history serial dependence** (Fischer & Whitney: an attended value attracts whether or not it was responded to) predicts **attraction from both sources**.
- **Revision 1's "sign flip by source" is withdrawn.** No paper derives repulsion by source. Run 3's contrast item-orders are reported descriptively as the map's unexplained reactance (§4).
- **The distance-tuning and lag cells** of revision 2's §3.0 are not run. They are the natural follow-up.
- **Kumaran's caveat:** a planted answer that looks wrong was abandoned 74.5% of the time in their LLMs. A ±30 plant may read as a wrong answer, so weak own-uptake could reflect implausibility rather than resistance.

## 1. In plain English

In perception, people's decisions are pulled toward their own previous decisions, and pushed away from what they just saw (Fritsche, Mostert & de Lange 2017). In run 3, when another person's estimate was shown, the model resisted it, and sometimes moved away from it.

Here we show the model the *same numbers*, but as if it had given them itself in an earlier turn, and ask it to rate the statement again. If the pull comes from treating the earlier number as its own commitment (self-consistency), the model should follow its "own" number more than someone else's. If it comes from any recently seen number (stimulus-history serial dependence), both should pull.

## 2. Design

- **Items and anchors:** run 3's 16 items and its frozen anchors (`experiments/exp4-run-3-anchors.json`: A_lo and A_hi for X and for Y).
- **Cells:** X-lo, X-hi, Y-lo and Y-hi, with R = 40 each. That gives 16 × 4 × 40 = 2,560 conversations and 5,120 calls.
- **Conversation**, with `claude-haiku-5-5`, thinking disabled, default temperature, and run 3's scale wording ", where 0 = certainly false and 100 = certainly true":
  1. user: "{context}\n\nOn a scale from 0 to 100{SCALE}, how likely is it that {statement}? Give only the number."
  2. assistant (planted): `{"probability": A}`
  3. user: "Please give your rating again. On a scale from 0 to 100{SCALE}, how likely is it that {statement}? Give only the number." The model's answer is **r₁**.
  4. user: run 3's conjunction question. The model's answer is **r₂**.
- **Comparison condition:** run 3's archived anchored cells ("Another person estimated …"), with the same items, values and R. No rerun.

## 3. Statistics

- **Slope per item-order (o ∈ {X, Y}):** s = [mean r₁(hi) − mean r₁(lo)] / (A_hi − A_lo), for the own-answer condition (s_own) and for the archived other-person condition (s_other).
- **Primary:** the mean of s_own across the 32 item-orders, and the mean of s_own − s_other. Both come with 2,000-resample item-cluster bootstrap CIs (seed 5454), alongside the mean of s_other.
- **Contrast item-orders:** the item-orders with s_other < 0 in the archived run-3 data. The record lists 6.
- **Reported alongside:**
  - the share of conversations whose r₁ equals the planted value;
  - r₂ by condition;
  - per-item slopes.

## 4. Pre-registered reading

1. **Resists its own planted answer too:** the CI of mean s_own contains 0 or lies below it.
2. **Source-dependent self-consistency:** otherwise, if the CI of mean (s_own − s_other) lies above 0.
3. **Source-independent attraction (stimulus-history serial dependence):** otherwise, if the CI of mean s_other also lies above 0.
4. **Own attraction, other undetermined:** anything else.

**Reported descriptively:** s_own on the contrast item-orders (s_other < 0). The map has no mechanism for that reactance.

## 5. What it cannot do

- The map's optional lag arm (filler turns before the re-rating) is not run.
- "Please give your rating again" is itself a cue that the earlier answer might be revisited. Run 3's "accept or revise" was a cue too. The two conditions differ in wording as well as source, and the write-up says so.

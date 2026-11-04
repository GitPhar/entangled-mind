# Biomimetic map §3.0, the shared test: source × distance × lag (pre-registration)

Written and frozen 2026-11-04 (America/Denver), in its own commit, before any call. DEVIATIONS.md D47. Budget **$0.50**, enforced in code. Stop on any refusal: the request ID goes to `results/refusal.md`, and nothing is reworded or retried.

**What was already known at freezing.**
- bm1 (`results/bm1-serial-dependence.md`): own-planted ±30 gives a slope of +0.42, against +0.05 for another person's value; the difference is +0.37 [+0.17, +0.57].
- Direction 2 and the 40-item direction 2 run, which was still running at freezing.

This test extends bm1 to other distances and to a lag. It shares its planting convention with direction 2 (D37, D45):
- the value sits in the model's own assistant turn, as its structured output;
- one scale direction;
- the same model and settings.

## 1. In plain English

bm1 showed that a number pulls the model's re-rating when it is the model's "own" earlier answer, and not when another person gave it. Three accounts predict different things when the number is moved further away, or when a few turns pass first:

| account | own vs other | as the number moves further away | after a few intervening turns |
|---|---|---|---|
| **Self-consistency** (a commitment to its own answers; Kumaran et al.) | own > other | — | no decay, because the answer stays in view |
| **Serial dependence** (attraction to any recent value; Fischer & Whitney) | both attract | pull rises, then falls or reverses | decays |
| **Anchoring / precision weighting** | both pull, never away | pull grows steadily | — |

## 2. Design

- **Items:** run 3's 16 exp-4 items, both statements (X, Y), on one scale direction.
- **The value:** V = min(98, max(2, round(m) + d)), where m is the statement's archived mean in `experiments/exp4-run-3-anchors.json` (`m_X`, `m_Y`). At d = ±30 this reproduces run 3's anchors exactly.
- **Own framing:** bm1's conversation, unchanged:
  1. user: rate the statement;
  2. assistant: `{"probability": V}`, planted;
  3. user: "Please give your rating again …", which gives **r₁**;
  4. user: the conjunction question, which gives r₂.
- **Other framing:** run 3's conversation, unchanged: "Another person estimated … V … accept or revise", then the conjunction.
- **Lag:** in the own framing, 3 filler turns are inserted between the planted answer and the re-rating. Each filler is experiment 5's K0 turn, "Reply with the single word: continue", with structured output `{"reply": "continue"}`.

**Cells.**

| cell | distances d | lag | R | source of data |
|---|---|---|---|---|
| own | ±10, ±60 | 0 | 10 | new |
| own | ±30 | 0 | 40 | bm1, archived |
| other | ±10, ±60 | 0 | 10 | new |
| other | ±30 | 0 | 40 | run 3, archived |
| own | ±30 | 3 | 20 | new |

**Size and cost.** That is 16 × 2 × 4 × 10 × 2 + 16 × 2 × 2 × 20 = 3,840 new conversations, about $0.36 at bm1's rate, with the lag arm's longer conversations estimated at about $0.00015 each.
- The map's design used R = 20 throughout, at about $0.46. The new distance cells use R = 10 to fit the $0.50 cap with margin.
- Jobs run with the repeat index outermost and the lag arm last. If the cap stops the run, every cell keeps balanced, smaller R, and the lag arm is what gets cut.

## 3. Statistics

**Per item-order (statement):**
- **base:** the model's free first-rating mean from run 3's X→XY or Y→XY cell, on the 0–1 scale.
- **Per cell:** shift = mean r₁ − base, and the actual displacement D = V/100 − base.
- **Uptake:** u = shift / D, for cells with |D| ≥ 0.05. Cells where clipping collapses the displacement are dropped and counted.

**Across item-orders,** all with 2,000-resample item-cluster bootstrap CIs (seed 4747):
- **Source (primary):** the mean of u_own − u_other at lag 0, pooled over the three distance classes {10, 30, 60}, and also reported per class.
- **Distance shape (own, lag 0):**
  - shift ~ β₁·D + β₂·D·|D|, by OLS over all own lag-0 cells;
  - the turning point |D*| = β₁ / (2|β₂|) when β₂ < 0;
  - the sign-adjusted attraction at nominal |d| = 60, mean of sign(D)·shift.
- **Lag:** u_own at ±30, lag 0 (bm1) minus lag 3.
- **Reactance check:** the mean u_other at ±10 and ±60, and the number of item-orders with u_other < 0.

## 4. Pre-registered reading

1. **Source:** own > other if the CI of mean (u_own − u_other) lies above 0. That is consistent with self-consistency, and against pure stimulus-history serial dependence.
2. **Distance:**
   - **non-monotone** (serial-dependence tuning) if the CI of β₂ lies below 0 **and** |D*| lies within the tested range of |D|;
   - **reversal** if the sign-adjusted attraction at |d| = 60 has a CI below 0;
   - **monotone** otherwise.
   - **Named confound** (Kumaran et al.): a planted own answer far from the model's view may be abandoned as implausible. A non-monotone curve is therefore also expected under implausibility-discarding, and the write-up says so.
3. **Lag:**
   - **decays** if the CI of (lag 0 − lag 3) lies above 0;
   - **grows** if it lies below 0;
   - **no detectable change** otherwise. The write-up reports the CI, not "no decay".
4. **Overall:**
   - **self-consistency** if (1) holds and the lag does not decay;
   - **serial dependence** if (1) fails, the curve is non-monotone and the lag decays;
   - **anchoring / precision** if (1) fails, the curve is monotone and other uptake is ≥ 0;
   - **mixed** otherwise.

## 5. What it cannot do

- The own and other conditions still differ in wording ("give your rating again" against "accept or revise"), as in bm1.
- One lag value only, at one distance.
- The tuning width on a 0–100 belief scale has no counterpart in the orientation literature, so the distance grid is a guess (map §3.2).

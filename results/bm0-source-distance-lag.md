# Biomimetic §3.0: source × distance × lag

Pre-registered in `experiments/bm0-source-distance-lag.md` (D47), committed before any call. Run 3's 16 items, one scale direction; own ±30 lag 0 from bm1 and other ±30 from run 3 (archived). 3650 new conversations, **$0.50** of the $0.50 cap; no refusal. Cells dropped for |D| < 0.05 after clipping: 68 of 448.

## In plain English

**What was tested.** bm1 found that a number pulls the model's re-rating when it is planted as the model's *own* earlier answer, and barely at all when it is credited to another person. This run asks whether that holds when the number is near the model's own view (10 points away) or far from it (60 points), and whether the pull fades when three unrelated turns come between the planted answer and the re-rating.

**Own beats other at every distance.**
- At 10 points away, the model takes up 71% of its own planted answer and 19% of another person's. At 30 points it takes up 44% against −11%, and at 60 points 21% against −13%.
- Pooled over distances, own minus other is **+0.46 [+0.21, +0.84]**. The interval is well above zero at each distance on its own.
- No pull from another person's number was detected: mean uptake +0.02 at ±10 and ±60, and its interval includes 0 at each distance. No resistance was detected either: about a quarter of cells move away, and no more.

**The pull of its own answer has a limit.**
- The further away the planted answer, the smaller the share the model takes up. The actual movement is similar at 10 and 30 points and smaller at 60.
- Even at 60 points the model still moves toward its "own" answer, by about 6 points. It never moves away, so there is no reversal.
- By the pre-registered rule this is the *non-monotone* shape that serial-dependence tuning predicts. The named confound is that it is equally what a model would do if it discards an "own" answer as implausible once it is far from its view (Kumaran et al.). This test cannot tell the two apart.

**After three filler turns, uptake is if anything higher (lag 0 − lag 3 = −0.13 [−0.25, −0.00]).**
- After three "continue" turns, the model takes up 57% of its own planted answer at ±30, against 44% with no turns in between.
- Lag 0 minus lag 3 is −0.13 [−0.25, −0.00], so by the pre-registered rule the uptake *grows*, but the interval's upper end only just clears zero.

**Pre-registered reading: self-consistency.** The own framing beats the other framing at every distance, and uptake does not fall after three filler turns (it rises, at the edge of the CI). The framings differ in wording as well as source.

**Limits.**
- **Wording.** The own and other conditions still differ in wording ("give your rating again" against "accept or revise"), as in bm1.
- **Cap stop.** The $0.50 cap stopped the run at 3,650 of 3,840 conversations ($0.502, as calls already in flight finished). As planned, only the lag arm was cut: 17 of 20 repeats, plus 2 conversations of the 18th.
- **Clipping.** 68 of 448 cells were dropped because clipping at 2 or 98 left too small a displacement.

## Uptake u = shift / displacement (1 = takes the value fully, 0 = ignores it, < 0 = moves away)

| distance |d| | own (lag 0) | other | own − other (paired) |
|---|---|---|---|
| 10 | +0.71 [+0.54, +0.86] | +0.19 [-0.19, +0.50] | +0.52 [+0.21, +0.95] |
| 30 | +0.44 [+0.27, +0.62] | -0.11 [-0.40, +0.13] | +0.55 [+0.26, +0.92] |
| 60 | +0.21 [+0.11, +0.31] | -0.13 [-0.44, +0.10] | +0.33 [+0.07, +0.72] |

- **Source, pooled over distances: own − other = +0.46 [+0.21, +0.84]** → own > other.
- **Distance (own, lag 0):** shift = β₁·D + β₂·D·|D|: β₁ = +0.70 [+0.42, +1.01], β₂ = -0.99 [-1.53, -0.48]; turning point |D*| = 0.35 (largest tested |D| 0.67); sign-adjusted attraction at |d| = 60: +0.06 [+0.03, +0.10] → non-monotone.
- **Lag (own, ±30):** uptake at lag 3 +0.57 [+0.42, +0.72]; lag 0 − lag 3 = -0.13 [-0.25, -0.00] → grows.
- Reactance check, other at ±10 and ±60: mean u = +0.02; 28 of 106 cells below 0.

## Pre-registered reading: **self-consistency**

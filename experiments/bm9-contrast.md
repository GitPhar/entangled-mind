# Biomimetic map (rev. 1 §3.9): contrast or assimilation on the single-scale QQ conversations (pre-registration)

Written and frozen 2026-11-04 (America/Denver), in its own commit, before the archive was opened for this analysis. DEVIATIONS.md D42. Cost $0: no API calls.

**What was already known at freezing:**
- the QQ summaries (`results/exp5-run-2.md`, `results/exp5-run-1.md`);
- direction 9's N1M family: M shifts by 12 points on average when S_k comes first, with no consistent sign, mean d −0.0 [−6.1, +5.5].

The relation of those shifts to the level of the S rating has not been computed.

## 1. In plain English

Divisive normalization, the brain's way of coding values relative to their context, predicts **contrast**: after rating something high, the next rating comes out lower. Anchoring, and the attraction to one's own past answers, predict **assimilation**: the next rating moves toward the last one.

When the model rates a sub-question S just before the main question M, does M move toward or away from the number it just gave for S? The content of S matters too: a high rating of a yes-leaning claim should push M up for purely logical reasons. That content push is held fixed.

**Revision 2 of the map** (`f824e14`, §3.10) found, on a full read of Louie, Khaw & Glimcher 2013, that their context is *simultaneous*. Sequential normalization is untested there ("temporal normalization … remain[s] currently unknown"). So this analysis is **not a test of divisive normalization**. Sean's overnight list keeps it, and it is run as a descriptive check: after rating S, does the model's M assimilate toward that just-given number, or contrast with it? That bears on self-anchoring (direction 2) and on the unexplained reactance in run 3 (map §4).

## 2. Data

- **Primary:** `results/exp5-conversations.json`, QQ block, anchor (a) only: the 40 candidates × 2 pairs, 20 conversations per order.
- **Replication:** `results/exp5-run-2-conversations.json`: 10 items × 2 pairs, 40 per order, anchor (a).

## 3. Statistics

**Per pair (item i, claim k):**
- d_M = mean M(SM) − mean M(MS): M after S, minus M asked first.
- L = mean S(SM) − mean M(MS): how far the S rating sits above the model's unconditioned main rating.
- C = sign(lean_k) · (mean S(SM) − 50) / 50: the content push, yes-ward.

**Across pairs:**
- **Regression:** d_M = α + β·L + γ·C, by OLS.
- **CIs:** 2,000 item-cluster bootstrap resamples (seed 5252).
- **Contrast** predicts β < 0; **assimilation** predicts β > 0.

**Secondary, content-free:** within the SM order of each pair, the conversation-level correlation between the S rating and the M that follows it. The pair's content is fixed there, so only fluctuations of the same question vary.
- The correlation is multiplied by sign(lean_k), so that a positive value means M follows S in the direction the content implies. A negative value means M follows S against the content, which is contrast.
- The mean is reported across pairs with a defined correlation, with an item-cluster bootstrap CI.

## 4. Pre-registered reading

- **Contrast** (M moves away from the S level just given): the CI of β lies below 0.
- **Assimilation:** it lies above 0.
- **No level effect:** otherwise.

The replication set is reported the same way. With only 20 pairs, it is descriptive.

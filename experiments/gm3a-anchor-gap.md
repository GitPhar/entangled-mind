# Gold-map direction 3, free look: does the scale-direction gap predict the model's errors? (pre-registration)

Written and frozen 2026-11-04 (America/Denver), in its own commit, before the analysis was run. DEVIATIONS.md D35. Cost $0: no API calls, archived data only.

## 1. In plain English

In experiment 5 the model rated the same main question on two scale directions: "0 = certainly false" (anchor a) and "0 = certainly true" (anchor b). After recoding, its average answers should agree. They didn't: 33.8 against 71.3 overall. On some items the model reads the reversed scale correctly, and on others it doesn't.

If the model holds a settled credence, that gap is just a reading slip. Then it should have nothing to do with whether the model's answer was right. If the judgment is put together on the spot, a large gap may mark items where there is no settled view, and those may be the items it gets wrong. This analysis checks whether the per-item gap predicts the model's errors.

This analysis compares the two directions by design, so it is the one place in the overnight run where both are used. The two directions are never pooled into one rating.

## 2. Data

- **Items:** the 40 experiment-5 candidates (20 answered wrongly by Haiku in the hard pool, 20 rightly, by the experiment-5 selection rule).
- **Error label:** `correct` in `results/pool-run-3.json`, the model's archived hard-pool answer.
- **Primary ratings:** the B0 conversations in `results/exp5-conversations.json`, the main question asked alone. Each item has 5 conversations on anchor (a) and 5 on anchor (b), recoded to 0 = false.
- **Secondary ratings, the "B0-equivalent first turns":** every archived conversation whose first turn is the identical B0 prompt, namely B0, the first M of MF, and the first M of QQ order MS. That gives each item 50 per direction.

## 3. Scores and statistics

- **gap** = mean recoded rating on anchor (a) − mean recoded rating on anchor (b), in points.
- **Primary score: |gap|.** The positive class is "model wrong". The statistic is AUROC with a 2,000-resample stratified bootstrap CI (seed 3030).
- **Reported alongside:**
  - the signed gap;
  - |gap| on the B0-equivalent set;
  - the archived arm-G self-confidence on the same 40 items (`results/arm-g-confidence.json`; score 100 − G);
  - the extremity of the anchor-(a) B0 mean, |mean − 50| (score: 50 − extremity);
  - the paired bootstrap difference AUROC(|gap|) − AUROC(100 − G);
  - the Spearman correlation between |gap| and G.

## 4. Pre-registered reading

- **The gap predicts errors** if the AUROC CI of |gap| lies above 0.5.
- **The gap predicts correctness** if it lies below 0.5. That would be reported as the opposite finding.
- **No evidence either way** otherwise.

With 40 items the CI is wide, about ±0.17, so only a large effect can register. This is a first look that informs the six-format run (direction 3, `experiments/gm3b-format-invariance.md`). It is not a test of that run's hypothesis.

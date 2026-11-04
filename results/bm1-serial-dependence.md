# Biomimetic (rev. 2 §§3.0–3.2): source dependence, run 3's anchors as the model's own earlier answer

Pre-registered in `experiments/bm1-serial-dependence.md` (D44), committed before any call. 16 items × 4 cells × 40, `claude-haiku-5-5`, thinking disabled, one scale direction. 2560 conversations, **$0.24** of the $0.40 cap; no refusal. Comparison: run 3's archived "another person" cells.

## In plain English

**The question.** In run 3 the model was told "another person estimated the probability is A", and it ignored the number or pushed back against it. Here we showed the *same numbers*, but as if the model had given them itself in an earlier turn, and asked it to rate again. Does the source of a number matter?

**What we found.** It matters a great deal.
- **As its own earlier answer,** a number pulls the model's re-rating strongly. The rating moves about 0.42 of the way toward it [0.25, 0.60]. In 42% of conversations the model simply repeats the planted number.
- **As another person's estimate,** no pull from the same number was detected: 0.05 [−0.08, +0.17].
- **The difference** is +0.37 [+0.17, +0.57].
- **Reversal.** On the 7 item-orders where run 3's slope was negative (two of them within 0.06 of zero), the own slope is positive on 6, about the same rate as on all 32 (27).

**What it means.** A number planted as the model's own answer and followed by "give your rating again" pulls the re-rating far more than the same number offered as another person's estimate under "accept or revise". The two framings differ in wording and format as well as source, so this does not isolate source. This matches Kumaran et al.'s finding in other models that the "stickiness" of an earlier answer disappears when it is attributed to someone else. It favours choice-dependent self-consistency over stimulus-history serial dependence, which would have the model attracted to any recent number.

Taken with direction 2 and the assimilation result (`results/bm9-contrast.md`), this is consistent with the model leaning on its own transcript.

**Caveats.**
- The two conditions also differ in wording: "Please give your rating again" here, against "accept or revise" in run 3.
- Revision 2 of the map withdrew the "sign flip by source" as a unique prediction of any mechanism. The sign change on run 3's 7 negative item-orders occurs at about the base rate, so it is neither a confirmation of one nor evidence of a flip by source.
- The distance and lag cells that would separate the accounts further were not run.

## Slope of the re-rating r₁ on the shown value A

s = [mean r₁(high) − mean r₁(low)] / (A_high − A_low): 1 = takes the value fully, 0 = ignores it, < 0 = moves away. 95% item-cluster bootstrap CIs.

- **Mean s_own (planted as its own answer): +0.42 [+0.25, +0.60]**.
- Mean s_other (run 3, "another person"): +0.05 [-0.08, +0.17].
- **Mean s_own − s_other: +0.37 [+0.17, +0.57]**.
- Descriptive: contrast item-orders (s_other < 0 in run 3): 7; mean s_own − s_other there +0.76 [+0.14, +1.13]; s_own > 0 on 6 of 7.
- Share of re-ratings that repeat the planted value exactly: 42% (mean over item-orders).

| item-order | s_own | s_other (run 3) | echo rate | mean r₂, own / other |
|---|---|---|---|---|
| co01|X | +0.58 | -0.48 | 38% | 0.04 / 0.05 |
| co01|Y | +0.26 | -0.32 | 59% | 0.02 / 0.04 |
| co02|X | +0.03 | +0.27 | 50% | 0.03 / 0.03 |
| co02|Y | +0.08 | +0.13 | 50% | 0.02 / 0.02 |
| co03|X | +0.15 | -0.06 | 0% | 0.45 / 0.35 |
| co03|Y | +0.00 | +0.00 | 0% | 0.38 / 0.26 |
| co04|X | +0.12 | +0.06 | 1% | 0.23 / 0.47 |
| co04|Y | -0.02 | -0.01 | 0% | 0.18 / 0.19 |
| co-lin06|X | +0.92 | -0.49 | 75% | 0.14 / 0.06 |
| co-lin06|Y | +0.93 | +0.16 | 85% | 0.07 / 0.06 |
| co-lin08|X | +0.91 | +0.09 | 20% | 0.03 / 0.03 |
| co-lin08|Y | +0.66 | +0.19 | 81% | 0.08 / 0.03 |
| co-lin09|X | +0.60 | +0.02 | 50% | 0.32 / 0.36 |
| co-lin09|Y | +1.00 | +0.15 | 100% | 0.31 / 0.31 |
| co-lin10|X | +0.69 | -1.16 | 44% | 0.05 / 0.03 |
| co-lin10|Y | +0.10 | -0.10 | 50% | 0.02 / 0.03 |
| co05|X | +0.99 | +0.38 | 89% | 0.12 / 0.07 |
| co05|Y | +0.76 | +0.29 | 79% | 0.05 / 0.03 |
| co06|X | +0.98 | +0.43 | 78% | 0.10 / 0.10 |
| co06|Y | +0.59 | +0.34 | 57% | 0.06 / 0.06 |
| co07|X | +1.00 | +0.26 | 100% | 0.05 / 0.26 |
| co07|Y | +0.88 | +0.08 | 50% | 0.23 / 0.12 |
| co08|X | +0.00 | +0.00 | 0% | 0.12 / 0.12 |
| co08|Y | +0.00 | +0.00 | 0% | 0.11 / 0.12 |
| co09|X | +0.13 | +0.16 | 0% | 0.03 / 0.22 |
| co09|Y | +0.28 | +0.46 | 18% | 0.03 / 0.01 |
| co10|X | +0.26 | +0.25 | 40% | 0.02 / 0.02 |
| co10|Y | +0.03 | +0.10 | 50% | 0.02 / 0.02 |
| co11|X | +0.28 | +0.11 | 5% | 0.04 / 0.03 |
| co11|Y | +0.03 | +0.09 | 50% | 0.02 / 0.02 |
| co12|X | +0.19 | +0.05 | 18% | 0.24 / 0.28 |
| co12|Y | -0.00 | +0.09 | 0% | 0.18 / 0.26 |

## Pre-registered reading: **source-dependent self-consistency (own > other)**

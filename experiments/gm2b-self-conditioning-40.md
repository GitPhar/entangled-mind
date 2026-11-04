# Direction 2 on all 40 experiment-5 items: shown, redacted and planted transcripts (pre-registration)

Written and frozen 2026-11-04 (America/Denver), in its own commit, before any call. DEVIATIONS.md D45. Budget **$2.50**, enforced in code. Stop on any refusal: the request ID goes to `results/refusal.md`, and nothing is reworded or retried.

## 1. In plain English

Last night's direction 2 found that the order of questions still changes the model's verdict when its earlier answers are hidden. That result rests on 10 items, and much of the effect came from two of them (h191, h261). This run extends the identical design to all 40 experiment-5 items, so the headline no longer rests on two items.

## 2. Design

The design is identical to `experiments/gm2-self-conditioning.md` (D37) in every respect except the items:
- chains O1–O4 and MF;
- conditions shown, redacted, planted-high and planted-low;
- R = 10;
- anchor (a) only;
- `claude-haiku-5-5`, thinking disabled;
- the same prompts and the same transcript editing, run by the same code (`gm2_self_conditioning.converse`).

**Items.**
- **The 10 run last night** (`results/gm2-conversations.json`, `9e23b6f` design) are reused as archived, not re-run.
- **The other 30 candidates** are run now: 30 × 5 × 4 × 10 = 6,000 conversations, about $1.6 at last night's rate. They are cached in `results/gm2b-conversations.json`.

**Planted values** (`experiments/gm2b-planted-values.json`, fixed in this commit):
- **The first 10:** the frozen D37 values.
- **The other 30:** the same rule, high = min(98, round(m) + 15) and low = max(2, round(m) − 15).
  - **S:** m is every run-1 anchor-(a) rating of the claim.
  - **M:** run 2's anchor-(a) B0 covers only the first 10, so m is the mean of the run-1 anchor-(a) first turns identical to B0: B0, MF's first M and QQ-MS's first M. That is 50 ratings per item.

## 3. Statistics

These are D37's statistics, computed by the same function (`gm2_self_conditioning.compute`):
- the gate;
- OE per condition;
- R = OE_redacted / OE_shown;
- b_MF;
- the next-rating pull;
- the final-M shift;
- MF agreement.

They are computed on three item sets:
1. **all 40 (primary);**
2. **the 30 new items alone** (an independent replication);
3. **the 40 without h191 and h261** (sensitivity to the two items that carried last night's effect).

Also reported:
- **Concentration:** among items with a shown OE > 0, the share whose per-item redacted OE is at least half the shown OE.
- **The placeholder-variance check** (raised by the literature session): the mean within-order SD of final M, shown against redacted. If redaction mainly adds noise, that SD rises. The variance component already subtracts within-order variance, so R is not inflated by noise alone, but the SD is reported.

## 4. Pre-registered reading

This is D37's reading, applied to the primary 40-item set:
- **question-driven** if the R CI lies wholly at or above 0.5;
- **self-anchoring** if it lies wholly below 0.5;
- **leaning** otherwise.

The replication and sensitivity sets are reported with the same labels, but they do not decide the reading.

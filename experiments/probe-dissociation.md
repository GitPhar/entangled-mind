# Gold map direction 5: belief versus readout (pre-registration)

Written and frozen 2026-11-04 (America/Denver), in its own commit, before any call on the ten study items. DEVIATIONS.md D48. Cost: $0 API. Everything runs locally on Sean's MacBook (Apple M2 Pro, 16 GB) through MLX.

**What was run before freezing.** The backend was smoke-tested on pilot item h018, which is not a study item: three short conversations per model, to check speed and that the constrained rating decoder and the cache-trimmed probe branch work. The analysis code was checked on simulated data (section 6). Nothing else was run.

## 1. In plain English

When a language model's answer changes with the order of the questions before it, has its *belief* changed, or only the *answer it constructs* when asked? Claude's internals are closed, so this uses an open-weight 8B model whose activations can be read.

1. **Gate.** First check that the local model shows experiment 5's graded order effects at all: its 0–100 rating of the main question must change with the order of the four sub-questions before it. If neither candidate model does, stop and report that.
2. **Probe.** Train a standard truth probe (Marks & Tegmark's mass-mean probe) on thousands of simple true/false statements.
3. **Test.** Re-run the four chain orders. At the moment the model is asked the main question, read the probe on the main question's yes-answer stated as a sentence, then take the verbal rating.

- If the rating moves with order and the probe stays put within its noise, the answer is being constructed over a belief that holds still.
- If both move together, the belief itself moves.

A positive control makes "stays put" meaningful: a reliable-source cue ("the answer is yes" or "the answer is no") must visibly move the probe. Otherwise a flat probe could just be a blind probe.

## 2. Setup

- **Models.** Llama-3-8B-Instruct first, then Qwen2.5-7B-Instruct only if Llama fails the gate. Both are 4-bit MLX conversions: `mlx-community/Meta-Llama-3-8B-Instruct-4bit` and `mlx-community/Qwen2.5-7B-Instruct-4bit`. They run under `mlx` and `mlx-lm` 0.32.2, in a venv at `.venv` (gitignored).
- **Backend.** `experiments/local_lm.py`. Each conversation is held in a KV cache.
- **Ratings.** These copy the role of experiment 5's JSON schema.
  - The assistant turn is forced to begin `{"rating": `.
  - Digits are then sampled at temperature 1.0 from the model's own next-token distribution, restricted to the integers 0–100 (no leading zeros), followed by `}`.
  - The stored assistant turn is `{"rating": N}`, as Haiku's was.
- **Seeds.** Each conversation's sampling seed is a hash of model, item, cell and repeat.
- **Items.** Experiment 5 run 2's ten items: h190, h101, h112, h191, h261, h058, h221, h279, h127 and h238. All ten are items Haiku got wrong. The yes-answer is false for the first four and true for the last six.
- **Chain claims and wording.** The chain claims are experiment 5's, from `experiments/split-exp5.json`. The wording is experiment 5's, word for word, with one scale direction for every conversation: anchor (a), "0 = certainly false, 100 = certainly true".
- **Orders.** O1–O4 are the cyclic Latin square of S₁…S₄, followed by M.

## 3. Step 1: the gate

**Cells.** O1, O2, O3, O4 and B0 (M only), with R = 10 per cell, verbal ratings only. That is 500 conversations per model.

**Per item.**
- **Span:** the largest minus the smallest M mean across O1–O4.
- **p:** a permutation test of order. The statistic is the between-order variance of M means; order labels are permuted among the item's 40 conversations, 10,000 times, with seed 48.
- An item **shows a graded order effect** if its span is at least 5 points and p < 0.05.

**Gate:** at least 3 of the 10 items show one. This is experiment 5's G1 threshold (3 items), applied to order alone.

The gate items G are fixed by step 1's data and used unchanged in step 3. Selection and test therefore use different conversations.

B0 means and the span including B0 are reported beside Haiku's anchor-(a) numbers. Neither is part of the gate.

**If Llama fails,** Qwen runs the same gate. **If Qwen also fails,** the result is "no graded order effects on either local model", and steps 2–3 are not run.

## 4. Step 2: truth probes

**Data.** Marks & Tegmark's datasets (`saprmarks/geometry-of-truth`, commit `5d1c630`), downloaded at run time to `~/.cache`. They are not vendored, because the repository has no licence.
- **Train:** cities, neg_cities, sp_en_trans, neg_sp_en_trans, larger_than and smaller_than, 300 statements each (seed 48).
- **Layer selection:** companies_true_false (400) and counterfact_true_false (600).
- **Report only:** common_claim_true_false (600). It is never used for any choice.

**Format.** Each statement is its own user turn in the model's chat template. The residual stream (each block's output) is read at the statement's last token.

**Probe.** At every layer l, the mass-mean direction θ_l = μ_true − μ_false over the training statements. The probe score is θ_l · x. There is no covariance correction: Marks & Tegmark find the plain mass-mean direction generalises best.

**Layer.** The one with the highest mean AUROC over the two selection sets.

## 5. Step 3: probe and rating after each chain order

**Cells, per item, R = 10 each (700 conversations):**
- O1–O4;
- B0;
- **T+ / T−, the positive control.** The first user turn is the opening context plus "A reliable reference source states that the answer to the question is yes." (or "… no."), then M.

**At the M point of every conversation:**
1. **The probe branch.** The main question's text is replaced by STATEMENT[item], the yes-answer as a self-contained declarative sentence (listed in `experiments/probe_dissociation.py`, written before any data). The residual is read at its last token. The cache is then trimmed back, so the branch leaves no trace.
2. **The verbal M rating** is then taken in the untouched conversation.

So the probe and the rating see exactly the same preceding context: the same sub-questions and the model's own sampled sub-ratings.

**Also stored.** The probe projection at every layer, and, as an exploratory readout, the projection at the last prompt token before the rating digits ("M-prompt position").

### Statistics

For a measure X (verbal V, 0–100, or probe P, the raw projection at the selected layer) on item i:
- **Between-order variance of the order means:** B_i, with ddof 1.
- **Mean within-order variance:** W_i.
- **Noise-corrected order-effect variance:** S_i = max(0, B_i − W_i/R).
- **Dynamic range:** D_X = the mean over all ten items of [mean X(T+) − mean X(T−)].

**Q, the share of the verbal order effect that the probe also shows,** with each measure in units of its own told-yes-minus-told-no range:

  Q = [√(Σ_{i∈G} S_P,i) / D_P] / [√(Σ_{i∈G} S_V,i) / D_V].

Q = 0 means the probe holds still. Q = 1 means it moves as far, relative to its range, as the rating does.

**Also computed:**
- **r:** the Pearson correlation, over the (item, order) cells of G, of the within-item-centred order means of P and V. It gives the direction of tracking.
- **p_P and p_V:** pooled permutation tests of order over G. The statistic is the sum of B_i over G, with labels permuted within item, 10,000 times.
- **CIs:** 95% percentile intervals from 2,000 resamples (seed 48). Items are resampled with replacement, and repeats are resampled within each cell.

### The pass rule (frozen)

**Validity.** All four must hold, or the verdict is UNDECIDED (validity) and the failure is named:
- **V1:** the selected layer's selection-set AUROC is at least 0.70.
- **V2:** the probe moves under the positive control, with D_P's CI lower bound above 0.
- **V3:** the rating moves under it too, with D_V's CI lower bound above 0.
- **V4:** step 3's verbal order effect on G is significant (p_V < 0.05).

**Verdict.**

| condition | verdict |
|---|---|
| p_P ≥ 0.05 and Q's CI upper bound < 0.5 | **DISSOCIATION: the readout is constructed over a stable belief** |
| p_P ≥ 0.05 and Q's CI upper bound ≥ 0.5 | UNDECIDED (probe too noisy to tell) |
| p_P < 0.05 and r's CI lower bound > 0 | **BELIEF MOVES**: "fully" if Q's CI reaches 1, "partly" if it reaches 0.5, "a little" otherwise |
| p_P < 0.05 and r's CI does not exclude 0 from above | PROBE MOVES, BUT NOT WITH THE RATING |

- **The first row is the user's rule, made testable.** "The probe holds within its noise" means its order effect is not distinguishable from its between-repeat noise (p_P ≥ 0.05). Q < 0.5 is added so that a non-significant probe counts only if it was sensitive enough to have shown at least half the rating's shift.
- **The third row is "both shift"** in the same direction.

**Sensitivity, reported but outside the verdict:**
- the selected layer ± 2;
- the M-prompt readout position;
- all ten items in place of G.

**A known risk, stated now.** Any change of context moves activations a little. With near-deterministic sub-ratings, the within-order probe noise could be tiny, so p_P < 0.05 is likely even if the belief barely moves. In that case the verdict is a form of BELIEF MOVES, and Q says how much. "A little (Q < 0.5)" is the label for "mostly readout, slightly belief".

## 6. Check of the analysis before freezing

`probe_dissociation.py simulate` builds three worlds on the ten items, with order offsets of SD 12 on the rating.

| world | Q [95% CI] | r | p_P | verdict |
|---|---|---|---|---|
| stable belief (probe ignores order) | 0.03 [0.04, 0.11] | +0.05 | 0.78 | DISSOCIATION |
| moving belief (probe tracks order) | 1.04 [0.96, 1.16] | +0.98 | 0.0005 | BELIEF MOVES (fully) |
| noisy probe | 0.45 [0.57, 1.66] | +0.00 | 0.78 | UNDECIDED (too noisy) |

The percentile CI for Q sits above the point estimate when the true Q is near 0. Resampling repeats adds within-cell noise that the max(0, ·) correction cannot fully remove. That bias works *against* a dissociation verdict, and it is left as is.

## 7. Outputs

- `results/probe-dissociation-<model>-gate.json` and `-gate-summary.json` (step 1);
- `-probes.json` and `-theta.npz` (step 2);
- `-run.json` (step 3);
- `results/probe-dissociation.json` (analysis);
- `results/probe-dissociation.md`, plain English first, with one figure.

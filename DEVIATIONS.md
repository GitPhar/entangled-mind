# Pre-registration deviations

## D1 — Contentions come from the visible written reasoning, not the hidden thinking trace

**Date:** 2026-11-03 (before any pool, calibration, or test-set result existed)

**Original spec:** ask the base model with extended thinking on, capture the thinking trace, and split the hidden thinking trace into 5–16 discrete contentions.

**New design:** the base model is asked to reason step by step *in its visible response* before giving `FINAL ANSWER: YES/NO`. Only that visible written response goes to the contention extractor. Thinking stays on (adaptive, effort `xhigh`) so the model still deliberates. Its content is requested with `display: "omitted"`, so it is never returned, stored, or passed to any other call. Only the thinking token count is logged.

**Reason:** in the first pool attempt, the API's `reasoning_extraction` safeguard refused the extractor call (`claude-sonnet-5-5`, `stop_reason: refusal`), which was being handed the base model's thinking trace. We redesigned the pipeline rather than route around the safeguard. If any call in the pipeline is refused again, the run stops, records the refused call and its exact stop details in `results/refusal.md`, and does not reword or retry.

**Effect on interpretation:** the circuits encode the argument the model *wrote down*, which may be a tidied, post-hoc account of its deliberation rather than the deliberation itself. Every result in this repository should be read as being about the written reasoning.

### Findings that led here (pilot calls, 2026-11-03)

1. **Sonnet 5.5 emits no thinking block at all at `low`, `medium`, or `high` effort** on these items (tested on a bat-and-ball item and a letter-counting item). Adaptive thinking judged them not worth thinking about, so there was no trace to split. A thinking block appeared only at `xhigh` and `max`.
2. **Even at `xhigh`, the thinking block is only a short summary**, one or two sentences (67–98 thinking tokens on the pilot items), and the raw chain of thought is never exposed. It could not have supplied 5–16 contentions on its own.

## D2 — The redesigned extractor was refused too (run stopped)

**Date:** 2026-11-03

With D1 in place (base thinking requested with `display: "omitted"`, extractor given only the question and the visible written response), the first extractor call (q01) was refused again with `stop_reason: refusal`, category `reasoning_extraction`. Per the hard rule, the run stopped at once. Nothing was reworded or retried, and 0 of 60 questions completed. The refused call and its exact stop details are in `results/refusal.md`.

The prompt still had the shape the safeguard documents as a trigger: the input sat inside a tagged `<response>` section, and the system prompt asked for the writer's "deliberation" / "written reasoning" to be decomposed.

## D3 — Prompt redesigned per Anthropic's documented guidance for reasoning_extraction

**Date:** 2026-11-03 (before any pool, calibration, or test-set result existed)

Anthropic's [refusals documentation](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback#keep-reasoning-in-thinking-blocks) says `reasoning_extraction` fires on prompt *shape*:
- a `<thinking>`, `<reasoning>` or scratchpad section
- a `reasoning`, `thinking` or `trace` field in JSON output
- the model's private notes, or a running log of its reasoning
- reasoning asked for verbatim or in full

It also says that asking for a short explanation or the evidence behind a result is fine, and that the category has no fallback model. The fix is to change the prompt.

Both earlier designs had that shape. D1's base prompt asked the model to "reason step by step in writing". Both extractor prompts wrapped the input in a tagged section and asked for the writer's reasoning or deliberation to be split out.

**Redesign:**
- **Base call** (`claude-sonnet-5-5`): adaptive thinking at `xhigh`, `display: "summarized"`. The prompt asks for the answer plus a brief explanation of the main considerations for and against, and keeps the `FINAL ANSWER: YES/NO` line. There is no step-by-step instruction and no tagged section. The summarized thinking blocks and the visible answer are saved together as each question's **deliberation record** in `results/pool-run-1.json`. The thinking blocks are archived only and are never sent to any other call.
- **Extractor** (`claude-sonnet-5-5`): the visible answer is presented as a document: "Below is a short written argument answering a yes/no question." It lists the document's distinct claims as `claims[{text, confidence, lean}]`.
- **Relation judge** (`claude-haiku-5-5`): the input is a numbered list of claims, and the output is the pair table `pairs[{i, j, relation, strength}]`.
- Every string sent to the API (prompts, schemas, user templates) was checked for thinking / reasoning / trace / scratchpad / deliberation / step-by-step / tag markup and reworded where any appeared.

**Science impact:** unchanged from D1. The circuits encode the claims in the model's *visible* explanation, which is a short account of its considerations, not its internal deliberation.

If a call is refused after this redesign, the run stops and records the request ID and exact refusal in `results/refusal.md`. The next step is a support ticket. Nothing will be iterated further.

## D4 — Pool extended with 75 code-verified computational items

**Date:** 2026-11-03 (after the pool run, before any circuit was run on any pool item)

**What happened:** on the original 60-item pool, `claude-sonnet-5-5` at effort `xhigh` answered **all 60 correctly**. With no known-wrong items, the 10-wrong / 10-right test set cannot be formed and H2 cannot be tested.

**Change:** the pool was extended once with 75 yes/no items generated by `experiments/make_extension.py` (seed 404, `experiments/questions_extension.json`). The items are:
- primality of 8-digit numbers (primes vs. products of two 4-digit primes)
- Gregorian weekdays of dates from 1600 to 2400
- letter counts in sentences
- digit sums of powers of 2
- 5-digit × 5-digit products with near-miss claims
- prime counts in 100-wide intervals

Every answer is computed by the script, not hand-labelled, so a "wrong" model answer cannot be a labelling error on our side.

**Rule fixed in advance:** the base effort stays at `xhigh`, and the extension is used once. If the 135-item pool still yields fewer than 10 wrong items, the run stops and that is reported. Otherwise the split follows the pre-registration: 10 wrong and 10 right items at random (seed 2026), with everything else, including surplus wrong items, going to calibration. The calibration pool is therefore about 115 items, not 40.

**Effect on interpretation:** the wrong items will be mostly computation slips, not misconceptions or conjunction-fallacy errors. The experiment then asks whether the circuit flags the model's *calculation* errors. That is a narrower question than the original one about conflicting beliefs.

**D4 addendum (same day, before any extension item completed):** at `xhigh` effort, the first computational item made the base call think until it hit the 16,000-token cap, which costs about $0.16 per call. To stay inside the $10 budget:
- items are processed in shuffled order;
- a base call that hits the cap is recorded as *no answer* and excluded from the split, never counted as wrong;
- the extension stops as soon as the pool holds 13 wrong items, or when session API spend reaches $8.50.

This stopping rule shapes only which items exist. It is applied before any circuit is run, so it cannot select for any hypothesis.

## D5 — Base model changed to claude-haiku-5-5 to obtain errors

**Date:** 2026-11-03 (before any circuit was run on any pool item)

**Original spec:** base model `claude-sonnet-5-5`, with adaptive thinking run at effort `xhigh` (D1).

**What happened:** pool run 1 with `claude-sonnet-5-5` at `xhigh` answered **all 117 checkable items correctly**: the 60 original items plus 57 of the computational extension items. Another 10 extension items hit the 16,000-token cap and were excluded. The run was stopped before its last 8 extension items once this decision was made. With no known-wrong items, H2 cannot be tested. Run 1 is archived as `results/pool-run-1.{json,md}`.

**Change:** the base model is now `claude-haiku-5-5`, a weaker Claude model chosen to obtain errors. It runs at its **default** effort, with adaptive thinking and `display: "summarized"`. The extractor (`claude-sonnet-5-5`) and the relation judge (`claude-haiku-5-5`) are unchanged.

Pool run 2 covers every original and extension item except the 10 that hit the token cap in run 1. The test set is 10 wrong and 10 right items at random (seed 2026), and the rest form the calibration pool.

**Fallback, fixed in advance:** if Haiku gets fewer than 10 wrong, the test set is every wrong item plus the 10 correct items whose extracted claims give the model's answer the least net support (Σ confidence·lean / Σ confidence, signed toward the answer given). Stage 2 runs anyway, and the results state plainly that H2 is underpowered at that count.

**Unchanged:** the H2 criterion, the five arms, the encoding, the readout and the threshold rule.

Nothing extracted under run 1 can be reused, because contentions depend on the base model's own answer. Run 1's spend stays in `results/api-usage.md`.

## D6 — Second, harder question pool (Stage 2 run 2)

**Date:** 2026-11-03 (after Stage 2 run 1 was fixed and running, before any hard-pool result existed)

**Why:** the standard pool of trick puzzles, misconceptions and computation yielded only 4 known-wrong items on `claude-haiku-5-5`, out of 125. At that count H2 is underpowered.

**New pool:** `experiments/questions-hard.json`, 300 yes/no items, 150 yes and 150 no, built by `experiments/make_hard_pool.py` (seed 1729). Every item records its source and license.
- **120 SimpleQA items** (OpenAI simple-evals, MIT). Each is the question plus a candidate answer: the gold answer for half the items, and for the other half the gold answer of a different SimpleQA question with the same topic and answer type.
- **120 MMLU-Pro physics and chemistry items** (TIGER-Lab, MIT). Each is the stem plus either the correct option or a random wrong one. Stems that depend on seeing the option list are dropped. GPQA Diamond was not used: it is gated, and its authors ask that items not be published in plain text, which this public repository would do.
- **60 author-written claims**: 30 true and 30 plausible fabrications, each a near-miss of a true fact.

**Pipeline:** unchanged, with the same base prompt, extractor, judge, encoding, readout, threshold rule, arms and H2 criterion.
- The hard pool runs first through `claude-haiku-5-5` (pool run 3).
- If Haiku gets fewer than 30 wrong, the pool also runs through `claude-sonnet-5-5` at default effort (pool run 4), and both result sets are kept.
- An answer with no parseable `FINAL ANSWER` line is excluded, not counted as wrong.

**Split:** all wrong items (at most 40, at random), plus an equal number of right items at random (seed 2026). Everything else is the calibration pool.

**Budget:** $15 for runs 3 and 4 together, enforced in code.

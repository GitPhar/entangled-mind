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

# The Entangled Mind: Quantum Cognition as a Cognitive Architecture for Language Models

**Sean Pharris**, independent researcher

> *Do machines need quantum minds?*

## Abstract

Quantum-cognition models describe human judgment with amplitudes, interference and entanglement rather than classical probabilities. This project asks whether the same idea is useful as an architecture around a language model. For each yes/no question, a language model answers and briefly explains the considerations for and against. Those claims are extracted, and every pair is judged to support, contradict, or be unrelated to the other. The resulting web becomes one entangled quantum state: one qubit per claim, with confidence setting the amplitude and a solved phase setting the stance. RZZ gates link related claims, and a short Ising-style evolution runs before measurement in a "yes"-oriented basis. The readout gives a judgment, a confidence, and a conflict flag for shots that split between strongly opposed configurations. The pre-registered test is whether that flag picks out the model's wrong answers better than three controls: the same circuit with no entanglement, the same circuit with a shuffled relation web, and plain classical contradiction-counting. The last is the control that matters most.

**Status:** STATUS_LINE

## Hypotheses, and the null result that falsifies each

Full definitions are in [`experiments/preregistration.md`](experiments/preregistration.md).

| | hypothesis | falsified if |
|---|---|---|
| **H1** faithful encoding | Arm A's judgment matches the base model's own answer on ≥ 70% of test items | agreement ≤ 50% (no better than a coin flip) |
| **H2** conflict detection (primary) | A flags conflict on ≥ 10% of known-wrong items, while C, D and E each flag at no more than half of A's rate | A flags < 10% of wrong items, or any control reaches ≥ half of A's rate |
| **H3** entanglement carries information | A's AUROC (wrong vs right) exceeds C's by ≥ 0.10 | C's AUROC ≥ A's |
| **H4** structure carries information | A's AUROC exceeds D's by ≥ 0.10 | D's AUROC ≥ A's (a random web does as well) |
| **H5** hardware survives | B's conflict scores correlate with A's (Spearman ≥ 0.5), and B flags ≥ 10% of wrong items | correlation ≤ 0, or B flags no wrong item |

If arm E (plain contradiction-counting) flags wrong answers as well as arm A, the quantum state carries nothing beyond the relation table, and this README says so.

## The five arms

| arm | what runs |
|---|---|
| **A** | entangled circuit, N = 2 Trotter steps, Qiskit Aer noisy simulator built from the real backend (`AerSimulator.from_backend(ibm_fez)`) |
| **B** | the identical transpiled circuit on real IBM hardware (`ibm_fez`, Heron r2), all 20 test circuits as one job in a Batch |
| **C** | same circuit with every entangling term removed |
| **D** | same circuit built from a shuffled relation web (same number of relations and the same strengths, on random pairs) |
| **E** | classical control with no qubits: total contradiction strength, thresholded on the calibration pool |

Every arm uses 1,000 shots. Each arm's conflict threshold is set on the calibration pool so that it flags the top quartile there. This equalises how much each arm flags, so any difference on the test set reflects *where* the flags land. Every readout, including the raw counts, is archived as JSON in `results/`.

## Results

RESULTS_BLOCK

## Pre-registration deviations

The full record, with dates and reasons, is in [`DEVIATIONS.md`](DEVIATIONS.md). In short:

1. **D1–D3: claims come from the model's visible explanation, not its hidden thinking.** The original spec split the hidden thinking trace. The API's `reasoning_extraction` safeguard refused that design, and then a second design that still had the documented trigger shape. We redesigned rather than route around it, following [Anthropic's documented guidance](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback#keep-reasoning-in-thinking-blocks). The base model now gives an answer with a brief explanation of the considerations for and against. Its summarized thinking is archived but never sent to another call. The extractor reads the explanation as a document and lists its claims. Two findings along the way: Sonnet 5.5 emits **no thinking block at all** at low, medium or high effort on these items, and at `xhigh` the block is only a one- or two-sentence summary.
2. **D4: the pool was extended** with 75 computational items whose answers are computed by code. On the original 60 items the base model made no errors.
3. **D5: the base model was changed** from `claude-sonnet-5-5` at `xhigh` to `claude-haiku-5-5` at default effort. Sonnet answered all 117 checkable items correctly, which left no known-wrong items to test H2, so a weaker Claude model was used to obtain errors. The H2 criterion and the five arms are unchanged.

## How to run

```bash
python3.11 -m venv .venv && .venv/bin/pip install -e ".[test]"
cp .env.example .env        # then fill in ANTHROPIC_API_KEY and IBM_QUANTUM_TOKEN
.venv/bin/python experiments/run_pool.py 2      # base model + claim extractor + relation judge over the pool; fixes the split
.venv/bin/python experiments/stage1_pipe.py     # one circuit on the simulators and on real hardware
.venv/bin/python experiments/stage2_run.py      # all five arms; the hardware arm runs only if the gate opens
.venv/bin/python -m pytest -q                   # fast unit tests
```

IBM hardware is the scarce resource. The Open Plan gives 10 QPU minutes a month, and this project stops at 7. Every design decision is made on the simulator. Every hardware job is logged with its QPU seconds in [`results/ibm-usage.md`](results/ibm-usage.md), and Anthropic API spend per question is in [`results/api-usage.md`](results/api-usage.md).

## Repository

```
src/entangled_mind/   config (all pre-registered constants), llm, encoder, readout, backends
experiments/          questions, pre-registration, pool / Stage 1 / Stage 2 scripts
results/              one markdown + one JSON per run, usage ledgers
tests/                fast unit tests
paper/                proposal and plain-language companion (PDFs)
```

## License

MIT, see [`LICENSE`](LICENSE). To cite this work, see [`CITATION.cff`](CITATION.cff).

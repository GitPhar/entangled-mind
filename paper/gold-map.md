# Gold map: candidate directions after experiment 5

Written 2026-11-03 (America/Denver), after experiment 5's tie (`75744dc`) and the freezing of experiment 4 run 3 (D33). It is a docs-only scan. The literature notes were gathered by web fetch; nothing was run.

**What the project has established.**
- **Error prediction is closed.** No quantum edge survives a matched classical twin on two base models (Addenda D and E). The model's own stated confidence is the best error signal, at 0.82 on Haiku and 0.91 on Sonnet.
- **Sequential judgment is real but classical so far.** Graded ratings show large order effects: a median span of 24.7 points, and 60 of 80 claim–question pairs above 0.10. A matched classical updater ties the quantum state, and a dephased Markov chain matches it.

**What Sean wants next.** A finding that overturns an assumption about minds, judgment or reality, that the field has slept on, and that this stack can test.

**The stack.**
- the Anthropic API (no logprobs, no weights);
- about 10 QPU minutes a month on 156-qubit Heron r2 devices, with 46 s used of the project's 420 s hard stop;
- the deliberation-to-belief-web pipeline;
- the window visualiser;
- this record.

**How to read the probabilities.** Each P is my honest estimate that the first test gives a real, reportable result in the direction that would overturn the assumption. A clean null is often the likelier outcome, and it is still worth having.

**Citations.** Literature marked [abs] was read in abstract only by the scouts. Everything else was read in full or in part. All ids were fetched. Treat [abs] numbers as provisional until the papers are read.

## Ranking

| rank | direction | assumption at stake | first test | cost | P(real, overturning result) |
|---|---|---|---|---|---|
| 1 | Privileged self-knowledge: does a model know its own errors better than another model reading the same answer? | Verbal confidence is just text-reading | 2×2 cross-rating on archived answers | ≈ $2 | 0.30 |
| 2 | Measurement as self-conditioning: is the order effect the question, or the model seeing its own answer? | Asking changes the judge's state, as in quantum cognition | Replay: shown / redacted / planted answers | ≈ $0.50 | 0.25 (P ≈ 0.7 of a decisive result either way) |
| 3 | Is there a credence at all? Format invariance | LLMs hold credences that elicitation reads out | 6 elicitation formats × the same 160 claims | ≈ $0.40 (plus a free first look at existing data) | 0.45 |
| 4 | Active inference: does the model seek the evidence that would settle its own conflict? | LLMs are passive predictors with no epistemic drive toward their own uncertainty | EIG-scored question menus built from its own claim webs | ≈ $0.10 | 0.25 |
| 5 | Belief versus readout: does the internal truth probe move with question order? | Order effects live in the belief | Probes on an open-weight model, both orders | $0 API; CPU hours | 0.30 |
| 6 | Does representation geometry predict order-effect size? | The quantum geometry of judgment is a metaphor | Overlap of truth directions against measured order effects | $0 API; CPU hours | 0.12 |
| 7 | Two-friend, genuine local friendliness with external settings on `ibm_fez` | Observer-independent facts | 3×3 settings, friend register 1 → 8 qubits | ≈ 220 QPU s | 0.20 (novel form; a confirmation of quantum theory, not an overturn) |
| 8 | A physical baseline for our order-effect instrument: sequential Peres–Mermin under CbD | (method) that our QQ/CbD pipeline can see contextuality when it exists | Mid-circuit sequential contexts, both orders | ≈ 72–150 QPU s | 0.55 of certifying, but low overturn value |
| 9 | Clonable minds: macrorealism is guaranteed for an LLM, so every "quantum-like" effect is invasiveness | Quantum-cognition tests on LLMs measure the same thing as on humans | A theory note plus an NSIT analysis of existing data | ≈ $0 | 0.20 (as a conceptual result) |
| 10 | Post-quantum belief geometry on natural text, or CbD contextuality at scale | Model belief states are classical probability simplices | SAE or probe geometry on an open model; CbD on our ratings | $0 API | 0.08 |
| 11 | Hardware as an oracle for sampling the model cannot compute | Quantum resources could help a classical judge | (see entry) | — | 0.02 |

Two rules are fixed in advance across all directions:
- each first test is pre-registered before its first call, as before;
- QPU entries 7 and 8 cannot both run in one month under the 420 s hard stop (46 + 220 + 150 > 420).

---

## 1. Privileged self-knowledge

**Assumption it would overturn.** A language model's stated confidence is a reading of its own visible text. Any capable reader of the same answer could produce it, so "introspection" is confabulation.

**Who has looked, and why it is still open.**
- **No self-advantage in three studies:**
  - Song, Hu & Mahowald (arXiv:2503.07513, COLM 2025) [abs] found no self-access advantage for linguistic knowledge.
  - Singh, Linzen & Ravfogel (arXiv:2605.26242, COLM 2026) [abs] found that input-only classifiers match "introspective" predictions.
  - Xiao et al. (arXiv:2509.24988) [abs] found self-prediction of correctness no better than an unrelated LLM.
- **With a chain of thought, a reader matches the model.** Podolak & Verma (UncertaiNLP 2025, doi:10.18653/v1/2025.uncertainlp-main.21) had GPT-4o-mini read DeepSeek-R1's chain of thought. Its AUROC was 0.841 against the model's own 0.851.
- **Self-advantage after fine-tuning.** Binder et al. (arXiv:2410.13787, ICLR 2025) found self-prediction beats cross-prediction (48.5% against 31.8% for Llama-70B).
- **Where a self-advantage hides.** Ashuach et al. (arXiv:2604.12373) [abs] found it only on the subset where models disagree.
- **What is still open:** frontier models giving prompted verbal confidence on answer-only text, with no chain of thought, analysed on the disagreement subset. Nobody has run that condition, which is ours.

**What today's data say.**
- Stated confidence G beats every structural reading of the same answer, on both models: 0.82 (Haiku, run 2), 0.83 (Haiku, locked test), 0.91 (Sonnet).
- But our structural readings were our own feature extractors, not another model judging. So the data are consistent with privileged access *and* with excellent text-reading.

**Cheapest falsifiable first test.**
- **The 2×2 design.** Judges {Haiku, Sonnet} × answer authors {Haiku, Sonnet}, on the archived hard-pool answers: Haiku's 300 and Sonnet's 298. Use the existing arm-G prompt, changed to "this answer was written by another assistant".
- **Self ratings are already archived** for both models (arms G and D28).
- **The new calls:**
  - Haiku rates Sonnet's answers (298 calls);
  - Sonnet rates Haiku's answers (300 calls);
  - the same again on light paraphrases of each answer, to control for self-recognition (Panickssery et al., arXiv:2404.13076 [abs]).
- **Statistic.** The self advantage = AUROC(self) − AUROC(other) on each author's answers, on all items and on the subset where the two judges disagree.
- **Pass:** a positive self advantage on both authors, with the item-bootstrap CI excluding 0 on the disagreement subset.
- **Fail:** the other model matches or beats self. In that case the 0.82–0.91 is text-reading, and the paper says so.

**Cost.** About $2: roughly 600 Sonnet calls at the D28 rate of about $0.003 each, and Haiku's calls at well under $0.01.

**P(real self-advantage) = 0.30.** Most of the literature finds none. But no study has used this exact condition, and our self AUROCs are unusually high. Either outcome cleanly settles what the project's best signal is.

---

## 2. Measurement as self-conditioning: the question, or the model's own answer?

**Assumption it would overturn.** In quantum cognition, measuring changes the judge's state, and asking *is* the disturbance. An LLM is the first judging system whose state can be copied and edited, which no-cloning forbids for quantum systems and memory forbids for people. So we can ask what fraction of "measurement disturbance" is simply the model conditioning on the record of its own answer.

**Who has looked, and why it is still open.**
- **Kumaran et al. 2025** (arXiv:2507.03120, Google DeepMind) is the only replay precedent. In binary choice with advice, hiding the model's first answer raised change of mind under opposing advice from 39.2% to 85.0% for Gemma 3 12B.
- **Thought Anchors** (arXiv:2506.19143) [abs] resamples chain-of-thought sentences.
- **Nobody has done this** for graded multi-question chains, for question-order effects, or framed it as measurement disturbance or response replicability.
- **The replicability line has never been tested on LLMs.** That is Khrennikov et al. 2014 and Ozawa & Khrennikov 2020/2021.

**What today's data say.**
- **Experiment 5:** the main-rating means span a median of 24.7 points across orders and omissions. The main question repeated after the chain lands within 5 points 84% of the time. The classical belief-adjustment model BA5 predicts the main ratings best.
- **Experiment 4 run 2:** the order effect's mechanism is undetermined (D19). Run 3 (D33) manipulates a *provided* first rating.

**Cheapest falsifiable first test.**
- **Design:** take the first 10 experiment-5 items and chain types O1–O4 and MF, on one scale direction (D33's lesson). Run each chain under four transcript conditions:
  - **shown:** as in experiment 5;
  - **redacted:** each of the model's ratings replaced by "[rating recorded]" before the next turn;
  - **planted-high and planted-low:** each rating replaced by fixed values 30 points above or below the archived mean.
- **Predictions:**
  - **Anchoring on its own answers:** the redacted condition removes most of the order effect, and planted values move the main rating in proportion.
  - **Question exposure:** shown ≈ redacted, and planted values do little.
  - **Replicability:** MF repeat agreement under redaction against shown separates memory from a stable judgment.
- **Pass (the overturning direction):** redacted retains at least half of the shown order effect. That means asking alone changes the judgment even with no record of the answer, which is a measurement effect in the strict sense.
- **Fail:** redacted removes it. Then LLM "order effects" are self-anchoring, a classical, mechanistically explained effect, and the paper says so.

**Cost.** About 10 items × 5 chain types × 4 conditions × 10 conversations = 2,000 chains, about $0.50 at experiment 5's rate.

**Update (23:17).** Experiment 4 run 3 (`de38306`) found the model resists *another person's* provided first rating: accept rate 0% in 15 of 32 item-orders, and sometimes it moves away from the estimate. That makes the planted-own-answer condition here the remaining way to move a first rating independently of the item.

**Design note from experiment 5 run 2.** Use one scale direction. The baseline between-repeat SD is 7.1 points on one scale against 20.6 pooled.

**P(the overturning direction) = 0.25. P(a decisive result either way) ≈ 0.7.** Kumaran's data suggest self-anchoring is strong, so the expected outcome is the classical one.

---

## 3. Is there a credence at all? Format invariance

**Assumption it would overturn.** An LLM holds a credence in a proposition that different elicitations read out with distortion. This is implicit in calibration work, and in Kumaran et al.'s cached confidence (arXiv:2603.17839) [abs]. The alternative is that the judgment is constructed by the act of elicitation, with no stored state behind it: belief as measurement outcome.

**Who has looked, and why it is still open.**
- **The standard exists but has no black-box test.** Herrmann & Levinstein (arXiv:2405.21030, Minds and Machines 2025) [abs] propose *uniformity* across contexts as a standard for belief.
- **Constructed judgment, from the confidence and preference side:**
  - Zhu & Griffiths (arXiv:2401.16646) [abs] model LLM probability judgments as samples constructed at query time.
  - Pal et al. (arXiv:2511.13240) [abs] find an action–belief gap between stated confidence and bets.
  - Dominguez-Olmedo et al. (NeurIPS 2024) find survey answers near uniform once order is randomised.
- **Elicitation artefacts are treated as nuisance bias.** The LLM-as-judge literature averages them away (e.g. arXiv:2506.22316 [abs]). Nobody has measured the *same* propositions across ratings in both scale directions, yes/no, bets, pairwise comparisons and frequency formats, and asked whether one latent credence fits.

**What today's data say.**
- **Anchor direction.** Experiment 5's baseline main ratings average 33.8 under "0 = false" and 71.3 under "0 = true". That is a 37-point uniformity failure under a mere relabelling of the scale.
- **Binary against graded (experiment 4).** Yes/no truth questions saturate while ratings move.
- **Repeats.** In experiment 4 run 2, repeated ratings barely vary (SD 0–0.05).
- **Free first look.** The per-item anchor-direction gap is already in experiment 5's archived B0 conversations. Whether that gap predicts the model's errors (AUROC) can be checked offline, as a pre-registered analysis of existing data.

**Cheapest falsifiable first test.**
- **Design:** the 160 experiment-5 chain claims, each elicited in 6 formats with R = 10:
  - 0–100 ratings in both directions;
  - yes/no;
  - a bet at stated odds;
  - a pairwise "which is more likely" against a fixed reference claim;
  - "out of 100 such cases".
- **Analysis:** fit a single-latent-credence model with a monotone link per format, a Thurstonian/IRT model with one credence per proposition, against a model with format-specific credences. Use held-out prediction across formats, and a CbD-style consistency test.
- **Pass (no single credence):** the format-specific model wins on held-out formats on most claims, beyond what the monotone links absorb.
- **Fail:** one credence per proposition explains every format. That is evidence for a stored state, and a uniformity pass for LLM belief.

**Cost.** About 9,600 short Haiku calls, about $0.40.

**P(no single latent credence) = 0.45.** The 37-point anchor gap is large, but a scale-misreading link could absorb much of it. The format design is what separates misreading from construction.

---

## 4. Active inference: does the model seek the evidence that would resolve its own conflict?

**Assumption it would overturn.** Generative models are passive. They have no drive to act in order to reduce their own uncertainty (Pezzulo, Parr, Cisek, Clark & Friston 2024, *Trends Cogn. Sci.* 28:97, doi:10.1016/j.tics.2023.10.002).

**Who has looked, and why it is still open.** LLM question-asking has been scored against expected information gain (EIG), but only for **external** hidden targets:
- Battleship: Grand et al., arXiv:2510.20886 [abs];
- 20 Questions: BED-LLM, arXiv:2508.21184 [abs];
- clarification: Dutta et al., arXiv:2608.19202 [abs], with an exact EIG oracle.

The knowledge-conflict literature studies how models resolve conflicts that are *handed* to them (arXiv:2601.03746 [abs]), not whether they *seek* resolution of conflict inside their own deliberation.

**What today's data say.** Our pipeline already gives, for every item:
- the model's own competing claims and relation web;
- a fitted classical model of how verifying each claim would move its final rating (experiment 5's BA5 and D5).

So the EIG of each possible check about *its own* main answer is computable. That is the piece the literature lacks.

**Cheapest falsifiable first test.**
- **Design:** for the 40 experiment-5 items, show the model its own deliberation and offer a menu of 4 claims it could verify. Ask which it would check first, over 3 menus × 10 repeats.
- **Scoring:** compare the choice with:
  - the EIG-optimal check under the frozen D5 and BA5 fits;
  - the confirmatory check, the claim that most supports its current lean.
- **Pass:** choices track EIG above chance and above the confirmatory rule.
- **Fail:** choices are confirmatory or at chance. That supports the "passive" view for self-directed inquiry.

**Cost.** About 1,200 Haiku calls, about $0.10.

**P(EIG-tracking) = 0.25.**

---

## 5. Belief versus readout: does the internal truth probe move with question order?

**Assumption it would overturn.** When an LLM's answer shifts with question order, its belief has shifted. The alternative: the internal representation of truth holds still and only the verbal readout is constructed in context.

**Who has looked, and why it is still open.**
- **Probes can resist context.** CCS (Burns et al., arXiv:2212.03827) resisted misleading prefixes that moved zero-shot outputs (82.1% → 83.8%, against 80.4% → 70.9%).
- **Probes and answers disagree.** "Cognitive dissonance" (Liu et al., arXiv:2312.03729) [abs] finds probes and queries disagree mainly where one is uncertain.
- **Instructions move probes.** Even an "evaluate correctness" instruction changes probe geometry (Poulis et al., arXiv:2604.03754) [abs].
- **Knowing more than they say.** Models can encode the right answer while generating a wrong one (Orgad et al., arXiv:2410.02707).
- **The gap:** nobody has varied *question order* while reading probes.

**What today's data say.** Nothing yet: Claude's internals are not available. The behavioural side, large graded order effects, is established in experiment 5.

**Cheapest falsifiable first test.**
- **Model:** an open-weight model run locally. Good candidates are Llama-3-8B (4-bit) or Mistral-7B, where truth probes are established. Qwen2.5-1.5B is reported to have a truth axis (arXiv:2607.16741, search snippet only), but must be checked first.
- **Step 1, the gate:** replicate a subset of experiment 5's chains on that model and confirm its graded order effects.
- **Step 2:** train mass-mean truth probes (Marks & Tegmark, arXiv:2310.06824) on true/false statements.
- **Step 3:** read the probe for the main question after each chain order.
- **Pass:** the verbal rating shifts across orders while the probe does not, beyond its noise. That separates judgment from belief.
- **Also informative:** if both shift together, the belief really moves.

**Cost.** $0 API, a few CPU hours, or a few dollars of rented GPU (my estimate). This needs new local tooling outside the current stack.

**P(clean dissociation) = 0.30.**

---

## 6. Does representation geometry predict the size of an order effect?

**Assumption it would overturn.** The quantum geometry of judgment is a metaphor fitted to aggregates. It predicts order effects governed by the overlap |⟨A|B⟩|² of the two questions' subspaces. The claim is that this overlap would be literally present in a judge's representations.

**Who has looked, and why it is still open.**
- **No one has predicted order-effect size from internal overlap.** The scouts found no such study.
- **The nearest work:** Lo, Sadrzadeh & Mansfield (arXiv:2412.16806) [abs] related BERT embedding distance to contextuality. Riechers et al. (arXiv:2507.07432) [abs] report "nominally quantum" belief representations in transformers on synthetic processes.
- **A caution:** overlaps must use the causal inner product (Park et al., arXiv:2311.03658) [abs], not the raw cosine.

**What today's data say.** In experiment 5 the *encoder's* geometry failed to predict where order effects appear (1 win against 2 losses, D32). But that geometry was our phase solve, not the model's representation.

**Cheapest falsifiable first test.**
- **Setting:** the open model and probes from direction 5.
- **Step 1:** for about 100 claim pairs, compute the overlap of their truth directions under the causal inner product.
- **Step 2:** correlate it with the measured graded order effect for the pair (Spearman), against a classical predictor (anchoring distance |P(X) − P(Y)|).
- **Pass:** overlap predicts the order effect beyond the classical predictor.

**Cost.** $0 API, shared with direction 5.

**P = 0.12.** It is a long shot, but the only test that could make the quantum geometry literal.

---

## 7. Genuine local friendliness with external settings and a growing friend (hardware)

**Assumption it would overturn.** The local-friendliness assumptions (Bong et al. 2020) are:
- Absoluteness of Observed Events: an observed event is a real single event for everyone;
- free choice of settings;
- locality.

Quantum theory says they cannot all hold. A violation does not overturn quantum theory; it overturns observer-independent facts.

**Who has looked, and why it is still open.**
- **Photonic:** Proietti et al. 2019; Bong et al. 2020 (Nat. Phys. 16:1199), with 3×3 settings and genuine-LF violation at the top two μ values.
- **On quantum computers:**
  - Zeng, Labib & Russo (arXiv:2409.15302, Quantum 2025) used the semi-Brukner inequality and saw violation to branch factor about 4 on ibm_torino.
  - Laux & Cavalcanti (arXiv:2609.12527, Sept 2026) put rule-based agent friends on Heron r2 ibm_marrakesh. But they used a *single* friend, where LF reduces to Bell, with *on-chip* setting choices that they flag as uncertified.
- **Open:** a two-friend, genuine-LF (non-Bell) 3×3 test with externally chosen settings, scaling the friend register on Heron.
- **Where an LLM fits, honestly.** A classical LLM friend cannot be coherently undone, so it is a null control: quantum theory predicts LF holds. Its legitimate roles are an external setting chooser, which is a weak free-choice source if seeded, or a reversible toy agent compiled into the circuit.

**What today's data say.** On `ibm_fez`, the witness certified two-qubit entanglement on 3 of 3 items. The hardware washed states out more than its noise model predicts. Calibration was ordinary (CZ about 2 × 10⁻³).

**Cheapest falsifiable first test.**
- **Design:** 9 setting circuits per friend size, with sizes 1, 2, 4 and 8 qubits and 3 repeats, for 108 circuits at 4,000 shots. The settings are pre-registered from an external RNG.
- **Pass:** genuine-LF violation at friend size ≥ 2 with external settings.

**Cost.** About 220 QPU s (the scout's estimate at 2 s per circuit). That fits the remaining 374 s, but rules out direction 8 this month.

**P(a violation in a new form) = 0.20.** It would confirm quantum theory. It is novel in form, but it is not an overturn of anything a physicist currently believes.

---

## 8. A physical baseline: sequential Peres–Mermin under CbD

**What it tests.** It is not an assumption about minds. It tests our *instrument*: can the QQ / order-effect / CbD pipeline we pointed at the LLM certify contextuality in a system known to have it? That would make the LLM's Γ ≤ 0 a meaningful null rather than a limitation of the analysis.

**Who has looked, and why it is still open.**
- **Done on IBM hardware, but always jointly.** Peres–Mermin (arXiv:2009.10751) and larger state-independent inequalities (arXiv:2101.03812; arXiv:2505.21243 [abs]) have been violated on IBM devices, always measuring each context jointly.
- **Never under CbD, never sequentially.** The scouts found no CbD treatment of IBM contextuality data, and no sequential mid-circuit version that measures disturbance directly.

**What today's data say.** Experiment 5's QQ block:
- only 1 of 80 pairs has Γ > 0 (h248, Γ = +0.20). That is exploratory, and about what chance gives across 80 pairs;
- the mean q is +0.005 [−0.058, +0.065] pooled over both scale directions. But on one scale (run 2, `bffc4ab`) it is −0.146 [−0.439, +0.137], so the near-zero was an anchor-pooling artefact.

**Cheapest test.** 6 contexts × 2 orders × 3 states = 36 mid-circuit circuits.

**Cost.** About 72 QPU s; about 150 s with more states.

**P(certified Γ > 0 on hardware) = 0.55.** The overturn value is low, but it calibrates every LLM result.

---

## 9. Clonable minds: macrorealism is guaranteed for an LLM

**Assumption it would overturn.** That a quantum-cognition test means the same thing on a language model as on a person.

**The argument.**
- An LLM's state at any turn is its context: a classical, copyable string. So it satisfies macrorealism *by construction*. It has a definite state at every turn, and that state can be read without disturbance by copying it.
- Leggett–Garg-type and QQ-type violations in such a system can therefore come only from *invasiveness*: the measurement adds tokens to the state. They can never come from the absence of definite states.
- With people and with quantum systems, those two causes are confounded. In LLMs they come apart.

**Who has looked, and why it is still open.**
- **Cognition:** Leggett–Garg proposals in cognition (Atmanspacher & Filk 2010, J. Math. Psychol., doi:10.1016/j.jmp.2009.12.001) and NSIT tests on behaviour (Tressoldi et al. 2015, Front. Psychol. 6:1061) assume an unclonable mind.
- **Physics:** Leggett–Garg on IBM hardware is crowded (Huffman & Mizel 2017; Ku et al. 2020; Santini & Vitale 2022).
- **LLMs:** the scouts found no paper making the clonability point for LLM judgment.

**What today's data say.** Experiment 5's Kvam contrast is an NSIT (total-probability) test. Its residual is +0.58 points, with Δ_K = +0.29 [−1.12, +1.65]. Its omission chains measure invasiveness directly.

**First test.**
- A short theory note.
- A pre-registered NSIT analysis of the archived experiment 5 conversations: P(final | asked earlier, marginalised) against P(final | not asked).
- Combined with direction 2's redaction, it splits invasiveness into the question and the record.

**Cost.** $0.

**P(a publishable conceptual result) = 0.20.** It reframes what every LLM quantum-cognition test, ours and others', can and cannot show.

---

## 10. Post-quantum belief geometry on natural text, or contextuality at scale

**Assumption it would overturn.** That a language model's belief states over a proposition are classical probability simplices.

**Who has looked.**
- **Belief geometry:**
  - Riechers, Elliott & Shai (arXiv:2507.07432) [abs] report quantum and post-quantum belief representations in networks trained on synthetic processes.
  - Shai et al. (arXiv:2405.15943) [abs] find belief simplices linearly embedded in the residual stream.
  - Levinson (arXiv:2604.02685) [abs] reports preliminary simplex geometry in Gemma-2-9B on natural text.
- **Contextuality at scale:** Kumar et al. (arXiv:2603.23485) [abs] find CbD dependence beyond direct effects in 19–52% of cases, for pronoun choice.

**What today's data say.** Our graded QQ data show essentially no CbD contextuality: 1 of 80 pairs. Kang (2026) found none either.

**First test.** SAE or probe geometry on the open model from direction 5, testing whether natural-text belief states lie outside the classical simplex.

**Cost.** $0 API.

**P = 0.08.**

---

## 11. Hardware as an oracle for sampling the model cannot compute

**Assumption it would overturn.** That a quantum resource could give a classical judge something it cannot compute.

**Who has looked, and why it is closed for us.**
- **Certified randomness from random-circuit sampling** (Liu et al., Nature 640:343, 2025; arXiv:2503.20498) needed 56 high-fidelity qubits, one-shot circuits under a 2.2 s latency bound, and an exascale verifier. That is infeasible on the Open Plan.
- **Quantum random numbers inside AI** show no performance benefit:
  - neural-network initialisation (Heese et al., arXiv:2108.13329) [abs];
  - mixed effects (Bird et al., Soft Comput. 2020) [abs];
  - the only demonstrated benefit is security against seed hijacking (arXiv:2605.08313) [abs].
- **Our belief webs need no oracle.** At 5–16 claims, they are exactly simulable.

**The one feasible piece.** Leggett–Garg/NSIT semi-device-independent randomness (Nath et al., arXiv:2502.02973), about 10 QPU s, as a certified seed for experimental randomisation. That is practical, but not a finding.

**P = 0.02.**

---

## Recommended order

1. **Direction 9's free analysis** of the archived experiment 5 data ($0), together with **direction 3's free look** (the anchor-gap AUROC on existing B0 conversations, $0). Both are pre-registered before the analysis.
2. **Direction 1** (≈ $2). Then **direction 2** (≈ $0.50), whose redaction condition also completes direction 9.
3. **Direction 3's six-format run** (≈ $0.40) and **direction 4** (≈ $0.10).
4. **New local tooling** for directions 5, 6 and 10, if Sean wants internals. This is outside the current stack.
5. **Hardware.** Direction 7 *or* 8 in a given month, not both (QPU hard stop). Direction 8 first if the aim is to validate the instrument, direction 7 if the aim is a foundations result.

**What I would not do.** Further quantum encodings of the same deliberation webs for error or sequential prediction. That question has its pre-registered answer.

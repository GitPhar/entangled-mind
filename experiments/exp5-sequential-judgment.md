# Experiment 5: sequential, context-dependent judgment (pre-registration draft)

Written 2026-11-03, after the version-two result (`results/v2-run-1.md`), before any experiment-5 data. **Status: FROZEN 2026-11-03 20:15 MST, in its own commit, before any experiment-5 call (Sean's go-ahead; budget cap $4).** Nothing in it had been piloted at freezing. It is the second of the two remaining pre-registered tests. The first is experiment 4 run 2, the graded QQ/R2 test on the 7 fallacy items (D17), which is designed but not yet run. Running it needs Sean's go-ahead on the budget below, and the pre-registration is frozen in a commit before the pilot starts.

## 1. Why this experiment

Version two settled the error-flagging question.
- The learned quantum encoding A2 tied its classical twin F2 on the locked test set: AUROC 0.83 [0.75, 0.90] against 0.84 [0.78, 0.89], with a paired difference of −0.007 [−0.079, +0.062].
- The model's own stated confidence G scored 0.83.
- A2's fitted couplings were small (k_sup = 0.12, k_con = 0.21, against 1 in v1). Other candidates reached the same train AUROC with couplings from 0.06 to 1.5, so error prediction does not depend on the entangling structure at all.

Error flagging is a static classification of one judgment. The empirical case for quantum models of cognition was never made on static classification. It rests on *sequences* of judgments:
- question-order effects that obey the QQ equality (Wang & Busemeyer 2013; Wang et al. 2014);
- intermediate decisions that change later ones and violate the law of total probability (Busemeyer, Wang & Lambert-Mogiliansky 2009; Pothos & Busemeyer 2009; Kvam et al. 2015);
- order effects in evidence integration (Trueblood & Busemeyer 2011).

Experiment 5 moves the project's belief state onto that ground. The base model rates a chain of sub-questions about its own competing claims, and then the main question. The orders vary, sub-questions are omitted in some chains, and in some chains an intermediate decision is inserted.

The experiment asks two questions:
1. Does the existing encoder, read as a dynamic quantum belief state, predict the sequence of ratings better than a classical sequential updater with the same parameter count?
2. Do the two parameter-free signatures of the quantum account appear in the data?

The two earlier sequential experiments failed upstream of any model, and this design is built around that failure.
- **Experiment 3:** order effects in yes/no answers were undetectable. In 85% of items the model gave the same answer in all 5 baseline runs, and the order-label permutation test gave p = 0.24.
- **Experiment 4:** the conjunction fallacy appeared in 0–100 ratings on 7 of 16 items. The binary QQ phase saturated completely: the low-probability conjunct was answered "no" in 100 of 100 samples, so R2 was untestable.

So every measurement here is a graded 0–100 rating, and the binary constructs (QQ, total probability) are computed from a pre-registered cut of those ratings.

## 2. What the literature gives us

Each entry below gives the paradigm, the quantum prediction, the classical comparator, the result, and what we borrow. All entries were read in full text unless marked [abstract only]. DOIs and arXiv ids were checked on Crossref or arXiv. BibTeX keys are in `paper/references.bib`.

### 2.1 Trueblood & Busemeyer (2011), order effects in inference (`trueblood2011quantum`)
- **Paradigm:**
  - Experiment 1: 291 analysed undergraduates and 8 crime scenarios.
  - Design: prosecution strength (weak or strong) × defence strength (weak or strong) × order (P→D or D→P), within subjects across scenarios, with about 38 participants per cell.
  - Ratings: P(guilty) on a continuous 0–1 scale, before any case, after the first case and after the second.
  - Experiment 2: 164 participants, an extreme, irrefutable defence, and a 21-point scale.
  - The paper also reanalyses Bergus et al. (1998), where 315 physicians judged P(UTI) step by step, and McKenzie et al. (2002).
- **Quantum model:**
  - A 4-dimensional space (hypothesis × evidence type), with one basis per evidence source, related by unitaries exp(−i·x·(H₁+H₂)).
  - Each judgment projects onto the "guilty" subspace.
  - One rotation parameter per evidence item: 4 in Experiment 1.
  - Order effects arise from non-commuting projections.
- **Classical comparators:**
  - Hogarth & Einhorn's (1992) belief-adjustment model, in adding and averaging forms, with one strength parameter per piece of evidence. This matches the quantum model's parameter count.
  - McKenzie's minimum-acceptable-strength model.
  - All models were fitted by least squares.
- **Result:**
  - Recency in all four order pairs (p < .001), with order effects of about 9–15 points; for example, after WP,WD the mean is .516 and after WD,WP it is .619.
  - Average-data RMSE: quantum 0.22, adding 0.22, averaging 0.77.
  - Split-half cross-validation across response scales: quantum 0.32, adding 0.36, averaging 0.85.
  - Only the extreme-evidence test separates quantum from adding. Under data-derived constraints, the quantum model predicts a large effect of the prosecution when it comes first, while the adding model is forced to predict none. Observed recency: t = −2.30, p < .023.
  - The authors note that equal parameter counts are not equal complexity.
- **What we borrow:**
  - a rating after every item;
  - a belief-adjustment comparator matched on parameter count (BA5 below);
  - held-out prediction error as the model-comparison metric, rather than in-sample fit;
  - and the lesson that only a constrained, a priori prediction discriminated the models.

### 2.2 Busemeyer, Wang & Lambert-Mogiliansky (2009), Markov vs quantum (`busemeyer2009empirical`)
- **Paradigm:**
  - 26 participants. Faces (wide or narrow) were categorised as good or bad and then a decision was made (attack or withdraw), in four conditions: C-then-D, D-then-C, C-alone and D-alone.
  - Responses were binary keypresses, pooled over about 1,326 two-question trials and 442 single-question trials.
- **Quantum prediction:** asking for the categorisation first changes the later decision. The law of total probability (TP) fails: P(A | D-alone) ≠ P(G)P(A|G) + P(B)P(A|B).
- **Classical comparator:** 2-D and 4-D Markov models with the same 3 or 4 parameters. They provably obey TP for any parameters.
- **Result:**
  - Narrow faces: TP = .59 against an observed P(A) of .69, a 10-point violation. 20 of 26 participants showed it; t(25) = 2.54, p = .018.
  - Wide faces obeyed TP (.37 vs .39).
  - No fit statistics are reported.
  - The D-then-C order roughly obeyed TP. The authors' explanation is that people categorise silently anyway.
- **What we borrow:**
  - the total-probability statistic, computed per item, paired, from an "asked" against a "not asked" condition;
  - a same-state-space Markov comparator;
  - and the warning about *silent* first questions. An LLM that already "considers" a claim while reading the question would show no omission effect.

### 2.3 Pothos & Busemeyer (2009), the disjunction effect (`pothos2009quantum`)
- **Paradigm:** a reanalysis of the prisoner's dilemma with the opponent's move known-defect, known-cooperate or unknown. Defection rates averaged over 4 studies: 84%, 66% and 55%, so the unknown condition falls below both known ones. The two-stage gamble shows the same pattern: 69%, 59% and 36%.
- **Quantum model:**
  - A 4-dimensional state over belief × action, evolving by Schrödinger's equation under H = H_payoff + H_dissonance for a fixed time t = π/2.
  - 2 free parameters (µ, γ).
  - With γ = 0, the interference disappears.
- **Classical comparator:** the same structure, with Kolmogorov forward equations and the same 2 parameters. It is proven to obey TP for any parameters.
- **Result:** close point fits, with no fit statistics (2 parameters for 3 data points).
- **What we borrow:**
  - evolution *between* measurements as the source of interference;
  - the γ = 0 (no-coupling) ablation as the classical limit of the same model, which becomes the κ = 0 ablation below;
  - and the known/unknown contrast as our asked/omitted contrast.

### 2.4 Wang & Busemeyer (2013), the QQ equality (`wang2013quantum`)
- **Paradigm:** two yes/no questions in split-ballot orders A→B and B→A: four Gallup polls (Moore 2002) and two lab replications.
- **Quantum prediction (a priori, parameter-free):** for any state and any pair of projectors asked back to back,
  - q = [p(AyBn) + p(AnBy)] − [p(ByAn) + p(BnAy)] = 0.
  - The prediction needs *no information inserted before or between the two questions*.
- **Classical comparators:**
  - A Bayesian model needs "order events" to produce order effects, and then nothing forces q = 0.
  - Markov transitions need not satisfy reciprocity.
  - Both arguments are qualitative; no comparator was fitted.
- **Result:**
  - q ≈ 0 in five data sets (|z| ≤ 1.22).
  - Rose–Jackson violates it (q = 0.15, z = 5.30), as the authors predicted, because background text came between its questions.
- **Test statistic as we will compute it:** z = q / √(p̂(1−p̂)(1/N_AB + 1/N_BA)), where p̂ is pooled over both orders.
  - This reproduces every z in their Table 1. The printed formula's factor of 2 does not.
  - We also report their 1-df likelihood-ratio χ².
  - The project's earlier shorthand z = q/√(p(1−p)/N), in `experiments/items-borrowed.json`, is the same statistic only when N is the half-harmonic (1/N_AB + 1/N_BA)⁻¹.
- **What we borrow:**
  - the exact statistic;
  - strictly adjacent question pairs with an identical preceding context;
  - and dichotomising a graded answer at a fixed cut. Their White–Black item collapsed three response options to two.

### 2.5 Wang, Solloway, Shiffrin & Busemeyer (2014) (`wang2014context`)
- **Paradigm:** 70 national surveys (66 Pew studies from 2001–2011, with 651–3,006 respondents each) and 2 lab studies, all with two consecutive binary questions in both orders.
- **Prediction:** q = 0. It also holds for mixed states, so pooling over a population is allowed. It needs back-to-back questions from a common prior context.
- **Result:**
  - Across the 66 Pew surveys, a test of the distribution of per-survey statistics finds order effects (p = .0004) but no deviation of q from 0 (p = .4625).
  - The two context effects within a diagonal correlate r = −0.82, against a predicted slope of −1.
  - Where order effects exceed 0.10, |q|/order-effect falls toward 0.
  - The only clear counter-example is Rose–Jackson.
  - The alternative models (repeat-the-first-answer, anchoring-and-adjustment) are discussed in the SI, which we could not access. The main text says they can be constrained to satisfy QQ, but possibly only by losing their order effects.
- **What we borrow:**
  - the across-item test of the *distribution* of per-item z, rather than pooled counts, which ignore clustering;
  - the rule that a null q is informative only if order effects are large (reported first, with the ratio |q|/OE);
  - and the correlation of context effects as a secondary diagnostic.

### 2.6 Kvam, Pleskac, Yu & Busemeyer (2015), interference of choice on confidence (`kvam2015interference`)
- **Paradigm:**
  - 9 participants, each doing 2,688 random-dot-motion trials at coherences of 2%, 4%, 8% and 16%.
  - In choice blocks, a beep at 0.5 s prompts a left/right choice. In no-choice blocks, an instructed click with the same motor response replaces it.
  - The stimulus stays on, and a confidence rating from 0 to 100 (certain left to certain right) follows 0.05, 0.75 or 1.5 s later.
- **Quantum prediction:** the choice projects the state, and evidence arriving afterwards evolves it unitarily. Pooled over choices, confidence then differs from no-choice and is *less extreme*.
- **Classical comparator:** a Markov random walk on the same 103 states with the same 4 parameters, plus an extended version (MRW-E). Both obey total probability.
- **Result:**
  - Interference coefficient −0.11, 95% HDI [−0.18, −0.04]. Confidence was less extreme after a choice: mean half-scale 83.96 against 85.15.
  - The HDI excludes 0 for 6 of 9 participants.
  - Group log Bayes factor 1,713 for the quantum random walk; 7 of 9 participants favour it.
  - Interference needs *second-stage processing*. A companion experiment with no post-choice evidence showed none.
- **What we borrow:**
  - the choice against matched no-choice contrast;
  - new evidence *after* the choice;
  - the predicted direction (less extreme);
  - and the distribution-level total-probability check.
  - Their choice and confidence share one basis. The interference comes from evolution after the choice, which is a different mechanism from QQ's incompatible questions, and we test the two separately.

### 2.7 Language models, 2024–2026
- **Kang (2026)** [abstract only] (`kang2026auditing`), the closest precedent: a QQ audit of an LLM with forced-branch logprob protocols.
  - Binary-conditioned distributions were near-deterministic for 17 of 18 item pairs, and label assignment flipped several verdicts.
  - It also notes that classical repetition mechanisms satisfy QQ exactly.
  - Our experiments 3 and 4 reproduced the saturation.
- **Bessis, Wills, Wojciechowski, White & Pothos (2026)** (`bessis2026legal`): GPT-4o and GPT-5.2 rated guilt on a 1–10 scale for six criminal cases. The design crossed evidence order (incriminating–exonerating or the reverse) with single or intermediate-plus-final rating, with 720 independent trials per cell at T = 1.
  - All agents showed recency.
  - In humans, an intermediate rating amplifies the most recent evidence. GPT-4o instead showed a uniform upward shift, which the authors call a "measurement bias".
  - No quantum model was fitted.
  - This is the closest LLM analogue of our omission chains.
- **Imannezhad, Pothos & Wills (2026)** (`imannezhad2026divergent`): GPT-5 at T = 1, 553 persona sessions, 0–100 ratings.
  - Conjunction-fallacy rate 18.8%, against 58.5% in humans.
  - 99.5% of the fallacies were single, not double.
  - Complementarity was almost exact.
  - That is the noise-free quantum pattern, argued qualitatively. Our experiment 4 also found single fallacies and no double ones.
- **Wolf et al. (2026)** [abstract only] (`wolf2026partition`): LLM estimates violate the law of total probability across persona partitions.
- **Echterhoff et al. (2024)** (`echterhoff2024cognitive`): sequential anchoring. In multi-turn decisions the model's own earlier outputs act as the intermediate judgment.
- **Option-position and label artefacts:**
  - Rupprecht, Ahnert & Strohmaier (2025) (`rupprecht2025prompt`) found a strong recency bias toward the last answer option.
  - Dominguez-Olmedo et al. (2024) (`dominguezolmedo2024questioning`) found an A-bias, and near-uniform answers once orders are averaged.
  - Kreutner et al. (2025, QSTN) (`kreutner2025qstn`) found that presentation mode (sequential, battery or single item) changes results.
  - Meister et al. (2024) (`meister2024benchmarking`) found that verbalised distributions track reference distributions better than sampled tokens or logprobs.
- **Owusu & Feldman (2026)** [abstract only] (`owusu2026anchoring`): anchoring resistance tracks the model's confidence, so confident items will not move.
- **What to avoid: Aerts et al. (2025/2026)** (`aerts2026identifying`). Their CHSH = 4 for chat models comes from deterministic answers averaged over two models, with no check of marginal selectivity.

**Lessons applied below:**
1. **Dispersion.** Screen for dispersion before interpreting anything (a pilot gate).
2. **Ratings.** Use verbalised 0–100 ratings, not binary answers or logprobs.
3. **Counterbalancing.** Reverse the scale anchors in half the trials.
4. **Presentation mode.** Keep it fixed (sequential multi-turn throughout).
5. **Three conditions.** Separate "asked and answered" from "not asked".
6. **Items as the unit.** Treat items, not samples, as the unit of inference.
7. **Contamination.** Use unfamous items; ours come from the project's hard pool, not Linda or Clinton–Gore.

## 3. Materials

**Base model.**
- `claude-haiku-5-5`, the same base model as the pool runs, with thinking disabled as in experiment 4.
- Sampling temperature is the model default, 1.0. No temperature parameter is sent: the current API rejects an explicit temperature for this model (DEVIATIONS D17). So temperature is not a lever here, and the determinism in experiments 3 and 4 happened at the default 1.0.
- Each rating is returned as structured output: `{"rating": <integer 0-100>}`.

**Main questions.** The 40 candidates in §9. They come from Stage 2 run 2's hard pool (`results/pool-run-3.json`).

**Selection rule** (applied to the archived deliberation records, before this draft):
- A claim is *competing* if it has |lean| > 0.1 and a `contradicts` relation to a claim leaning the other way (also |lean| > 0.1).
- An item is eligible if it has at least 3 competing claims: 157 of 300 qualify.
- The 20 eligible items the model got wrong (of 29) and 20 it got right (of 128) are ranked by side balance, min(#yes-leaning, #no-leaning)/(#leaning), then by number of competing claims, then by id.
- Right items are capped at 5 per category.
- 14 of the 40 were also in experiment 3, which gives us their 5-run baseline P(yes).

**Sub-question claims per item.** K = 4 competing claims, two leaning yes and two leaning no, chosen by confidence × |lean| (ties broken by lower index). Where one side has only 1 competing claim, the remaining slots are filled from the other side. All 40 candidates have at least 4 competing claims.

**Wording.** Every conversation opens with the same context:

> *We are going to think about one question in steps. The question is: "<main question>". I will ask you to rate several statements, one at a time, and the question itself. Give each rating as an integer from 0 to 100, where <anchor>.*

- **Sub-question k:** *"How likely is it that this statement is true? '<claim k text>'"*
- **Main question:** *"How likely is it that the answer to the question is yes?"*
- **Anchors** are counterbalanced between conversations (half of the R repeats each):
  - **(a)** 0 = certainly false, 100 = certainly true;
  - **(b)** 0 = certainly true, 100 = certainly false.

  Ratings in (b) are recoded to r ↦ 100 − r before analysis. Anchor direction is reported as a factor.

## 4. Conditions (chain types)

In each item, S₁…S₄ are the four sub-questions and M is the main rating. A *chain* is one item × one chain type. It runs as R = 10 independent conversations, 5 per anchor direction.

| type | sequence | purpose |
|---|---|---|
| O1–O4 | four orders of S₁–S₄ (a Latin square: each S in each position once), then M | order effects on M and on each S |
| X1–X4 | the O1 order with S_k omitted (k = 1…4), then M | omission: does *asking* S_k move M? (the total-probability contrast of §2.2) |
| B0 | M only | baseline |
| MF | M, then S₁–S₄ (O1 order), then M again | main first; replicability of M after the chain (Khrennikov et al. 2014; Busemeyer & Wang 2017) |
| K1 | S₁, S₂, **choice**, S₃, S₄, M | Kvam: an intermediate binary decision on the main question ("Answer yes or no: is the answer yes?"), followed by new evidence (S₃, S₄), then the rating |
| K0 | S₁, S₂, **filler**, S₃, S₄, M | Kvam no-choice control: the filler turn is "Reply with the single word: continue", matched in length to the choice turn |

That makes 12 chain types per item.

**QQ block (separate two-turn conversations).**
- Each pair (S_k, M) is asked back to back, immediately after the opening context, in both orders, with R = 40 per order (20 per anchor direction).
- Each item has two pairs: the chain claims with the largest and the smallest predicted non-commutativity |sin Δφ_k| (§5.1), computed from the encoder before any data.
- The pairs are (S_k, M) rather than (S_i, S_j) for a reason. In the quantum model below, two single-claim sub-questions act on different qubits, so their projectors commute and the model predicts no order effect between them when they are adjacent. A sub-question and the main question share qubit k, so they do not commute when Δφ_k ≠ 0.

## 5. Models

All models predict every rating in a conversation from the opening context and the ratings the base model actually gave earlier in that conversation (one-step-ahead prediction).

All models share a rating link. A model probability p maps to a predicted rating r̂ = 100·(a + (b − a)·p), and an observed rating r maps back to a probability p_obs = clip((r/100 − a)/(b − a), 0.01, 0.99). The link has 2 parameters (a, b) with 0 ≤ a < b ≤ 1.

### 5.1 A5: the dynamic quantum belief state (built from the existing encoder)

**State.** Arm A's preparation and entangling layer from `src/entangled_mind/encoder.py`:
- RY(θ_k = confidence·π/2) RZ(φ_k) on each claim's qubit, then RZZ(κ·J_ij) on every related pair.
- **Phases, in this order:**
  1. Set aside the no-lean claims (|lean| ≤ 0.1).
  2. Solve the XY energy on the leaning claims and their mutual edges with the **anchored** solver, `encoder.solve_phases_anchored`. This is D15's working correction: lean anchors are scaled by λ = max(1, max_k Σ_j |J_kj|) in the phase solve only, which cuts the share of off-axis camps from 20% to 7%.
  3. Set every no-lean claim to φ = π/2 with lean 0. This is the version 2.1 honest-hedge orientation (Addendum B, `v2.hedge_phases`). The hedges keep their couplings in the circuit.

  No existing function composes these steps, so the runner will implement this order and test it against both parents: with no hedges it must equal `solve_phases_anchored`, and with a plain solve it must equal `hedge_phases`.
- **Why the anchored solver and not `pin_frame`.** D15 found that the drift is camps pulled *together*, not a rotated frame, so the rigid rotation of `pin_frame` leaves the off-axis share at 20%. Here the off-axis angle Δφ_k is itself the predicted source of order effects. Solver drift would therefore plant spurious "quantum" predictions, and the anchored solver keeps Δφ_k down to what the relation web genuinely forces.
- **Sensitivity, reported and not part of the verdict:** A5 refitted with the plain v1 solver (`solve_phases`), the encoding of every earlier arm.
- All claims of the item are in the state, not just the four that are asked about.

**Measurement operators.**
- **Main question:** Π_M is the arm-A readout projector, onto computational-X-basis configurations whose weighted vote is m = Σ w_k x_k > 0 (m = 0 counts as one half), with w ∝ |lean| (`readout._weights`).
- **Sub-question S_k:** P_k projects qubit k onto its own encoded direction n_k = (cos φ_k, sin φ_k, 0), "claim k is true". Then, at the encode stage, P(true) = (1 + sin θ_k)/2.
- **Non-commutation:**
  - P_k commutes with Π_M exactly when n_k lies on the yes/no axis (φ_k ∈ {0, π}).
  - The size of the non-commutation is set by |sin Δφ_k|, where Δφ_k is φ_k minus its snapped value (0 for a claim leaning yes, π for one leaning no).
  - This is an a priori, per-claim prediction of where order effects should appear. The encoder fixes it before any data.

**Dynamics.**
- Before each question, the state evolves by one Trotter step of arm A's evolution: exp(+iγ J_ij X_i X_j) on related pairs, the lean fields, then the mixer exp(+iβ Z_k), with per-question angles γ and β.
- This is the "evolution between measurements" of Pothos & Busemeyer (2009) and Kvam et al. (2015). Without it, sub-questions on different qubits could never show order effects among themselves.

**Update on a rating.**
- On an observed rating r of the operator P (P_k or Π_M), the state takes the Lüders update for the two-outcome POVM E = p_obs·P + (1 − p_obs)·(I − P): ρ ↦ √E ρ √E / tr(Eρ).
- At p_obs ∈ {0, 1} this is an ordinary projective collapse. Each sub-question "collapses part of the state" by an amount set by how decisive the rating was.
- **Binary choice (K1):** a projective collapse onto Π_M or I − Π_M, according to the answer given.
- **Filler (K0):** an evolution step only, with no update.

**Prediction.** r̂ = 100·(a + (b − a)·tr(P ρ)), evaluated just before the update.

**Parameters (5):**
- κ, the coupling scale (prep and evolution);
- γ, the evolution angle per question;
- β, the mixer angle per question;
- a and b, the link.

**A priori version (A5⁰, no fitting):** κ = π/4, γ = γ₀ = 0.5, β = β₀ = 0.4, a = 0, b = 1, the v1 constants.

**Ablation (A5, κ = 0):** with no coupling, the claims evolve independently. This is the Pothos–Busemeyer γ = 0 limit, and it is reported as A5's no-entanglement control.

### 5.2 F5: the classical twin (Markov / Bayesian updater, same parameter count)

**State.** A probability distribution over the 2ⁿ yes/no configurations x of the same claims. F5 is A5's commuting limit: every claim's direction is snapped onto the yes/no axis, so "claim k is true" ≡ x_k = sign(lean_k).

**Prior.** The product of the same single-claim marginals, p_k(true) = (1 + sin θ_k)/2. An entangling analogue then follows: one full Glauber heat-bath sweep under arm F's Ising energy, E(x) = −κ_F Σ J_ij s_i s_j (with s = ±1), at temperature T.

**Dynamics.** Before each question, the distribution takes a partial heat-bath sweep: P ↦ (1 − λ)P + λ·G(P), where G is one full sweep at temperature T.

**Update on a rating.**
- Bayes with the same likelihood as A5's POVM: P(x) ↦ P(x)·E(x)/Z, where E(x) = p_obs if claim k is true in x, and 1 − p_obs otherwise.
- When every operator commutes, A5's update reduces to exactly this rule. The only difference between the twins is therefore coherence and non-commutation.
- **Binary choice (K1):** sharp conditioning on the vote event.

**Prediction.** r̂ = 100·(a + (b − a)·P(event)).

**Parameters (5):** κ_F, T, λ, a, b.

**A priori version (F5⁰):** κ_F = 1, T = 1, λ = 1, a = 0, b = 1.

**What F5 implies.**
- Sequential Markov updating can depend on order (exp 3, D13), so F5 can produce order effects. This keeps it from being a strawman.
- F5 obeys the law of total probability for any parameters: pooled over the choice, K1 equals K0.

### 5.3 Secondary comparators (reported, not in the pass criterion)

- **D5, the dephased quantum model.** A5 with complete dephasing in the yes/no basis after every unitary step. That gives a Markov chain with transitions |U_xy|², the same state space and the same 5 parameters. It is the Markov random walk of Kvam et al. (2015), and it obeys total probability.
- **BA5, belief adjustment (Hogarth & Einhorn 1992).** It predicts M ratings only:
  - C₀ = 100·(A5⁰'s prior P(yes));
  - after rating S_k, C ↦ C + ω_side(k)·(r_k − 50)·sign(lean_k)·ρ^(K−pos), with separate weights ω_supp and ω_con for claims on the side of the model's answer and against it;
  - a recency factor ρ;
  - and the link (a, b).

  That is 5 parameters. It is scored on M ratings only.

## 6. Data split and fitting

**Units.**
- A *chain* is (item, chain type) with all its R = 10 conversations.
- 8 of the 40 items, 4 wrong and 4 right drawn with seed 2027, are held out entirely as an **item-held-out test**.
- The 384 chains of the other 32 items are split 60/20/20 **by chain** (230/77/77), stratified by chain type, with seed 2027.
- QQ-block conversations are never used for fitting; they serve only the parameter-free check.
- The split is written to `experiments/split-exp5.json` and committed before the full run.

**Fitting** (identical for A5, F5, D5 and BA5):
- 400 random draws over each parameter's box, then hill-climbing of the 10 best for 60 steps each, all on train mean squared error (MSE) of the ratings.
- Selection on validation MSE.
- Parameter boxes:
  - κ ∈ [0, 2], γ ∈ [0, 1.5], β ∈ [0, 1.5];
  - κ_F ∈ [0, 3], T ∈ [0.2, 5], λ ∈ [0, 1];
  - a ∈ [0, 0.4], b ∈ [0.6, 1].
- Seeds: A5 501, F5 502, D5 503, BA5 504.

The test chains and the held-out items are each scored **once**.

## 7. Tests and pass criterion

### 7.1 Gate: dispersion (pilot)

**Pilot items.** 5 items not among the 40: the next 3 wrong and the next 2 right in the selection ranking. *Clarification at freezing (DEVIATIONS.md, D22):*
- Under the 5-per-category cap there is no "next" right item. There are 4 categories, so the cap admits exactly the 20 right items already selected.
- The 2 right pilot items are therefore the next 2 in the **uncapped** right ranking, excluding the 40.
- The pilot is **h018, h088, h039** (wrong) and **h001, h170** (right).
- §3's rule was re-run from the archived records before freezing, and it reproduces §9's 40 ids exactly and in order. Each runs the full design (all 12 chain types and the QQ block). Pilot data are reported but never used in any test.

**Gate G1, the experiment's go/no-go** (stated in advance). On at least 3 of the 5 pilot items, either:
- the main-rating means across O1–O4, X1–X4 and B0 span at least 5 rating points, **or**
- at least 25% of the sub-question ratings have a between-repeat SD of at least 2 points.

If G1 fails, the base model's ratings do not move with sequence. The full run is not made, and experiment 5 is reported as **untestable** at that point, with the pilot data.

**Gate G2, for the QQ block only.** On at least 3 of the 10 pilot pairs, the binarised minority response (rating ≥ 50 vs < 50) appears in at least 10% of samples in at least one order. Otherwise the QQ check is reported as saturated, following Kang's (2026) health gate, and the rest of the experiment runs.

### 7.2 Primary: sequential prediction

- **Metric:** on the test chains, the mean squared error of every observed rating against its one-step-ahead prediction, MSE_A5 and MSE_F5.
- **Statistic:** Δ = MSE_F5 − MSE_A5, with a 95% CI from 2,000 paired bootstrap resamples of *items*. Chains within an item move together.
- **Verdict:**
  - **pass** if the CI lies entirely above 0;
  - **classical** if it lies entirely below 0;
  - **tie** otherwise.

### 7.3 Parameter-free check 1: the QQ equality (adjacent (S_k, M) pairs)

For each pair, the binarised response is yes = rating ≥ 50 (after anchor recoding). Rows that fail the integer schema are dropped, and the drop rate is reported per order. Then:

1. **Order effect first.** Report the 4-cell χ²(3) of order and the order-effect size OE, as defined by Wang et al. (2014):
   - each joint cell's context effect is c(xy) = p(S=x, M=y | S asked first) − p(S=x, M=y | M asked first);
   - OE is the larger of the two diagonal sums, |c(yy)| + |c(nn)| and |c(yn)| + |c(ny)|, and bounds |q|;
   - OE_S and OE_M, each question's yes-rate shift when asked second;
   - OSS = |OE_S| + |OE_M|.
2. **QQ.** q and z, by the formula in §2.4, and the 1-df likelihood-ratio χ². Also Γ = |q| − OSS for rank-2 Contextuality-by-Default, as in experiment 4.
3. **Across items.** A Kolmogorov–Smirnov test of the per-pair z values against N(0, 1), following Wang et al. (2014), plus the mean q with an item-bootstrap 95% CI.
4. **Robustness.** q is also reported at cuts of 30, 40, 60 and 70. These tests are correlated and are not used for the verdict.

**Signature present** if all of the following hold:
- G2 passed;
- at least 5 pairs have OE > 0.10 with a 95% CI excluding 0;
- on those pairs, the KS test does not reject N(0, 1) (p > .05);
- and the mean-q CI lies within ±0.05.

**Signature contradicted** if the mean-q CI excludes 0 on those pairs.

**A priori sub-test.** Is OE larger on the large-|sin Δφ| pair than on the small one, within items? A sign test over items.

### 7.4 Parameter-free check 2: Kvam-style interference (K1 against K0)

- **Statistic:** the final M rating's folded confidence, |r − 50|. The item-level paired difference is Δ_K = mean(K1) − mean(K0).
- **Models:**
  - Every Markov or read-out model, F5 and D5 included, predicts Δ_K = 0 in distribution: pooled over the choice, total probability holds.
  - Kvam's quantum prediction is Δ_K < 0: less extreme after a choice, given the new evidence S₃ and S₄.
  - A *commitment* mechanism, where the model stays consistent with an answer it has stated, predicts Δ_K > 0.
- **Signature present** if the item-bootstrap 95% CI of Δ_K lies entirely below 0.
- **Commitment** (classical, non-Markov) if it lies entirely above 0.
- Also reported:
  - a two-sample KS test of the pooled K1 and K0 final-rating distributions within each item;
  - the total-probability residual, mean(K0 rating) − Σ_c P(c)·mean(K1 rating | c);
  - and A5⁰'s per-item predicted sign of Δ_K, with its agreement rate.

### 7.5 Verdict

| verdict | condition |
|---|---|
| **quantum supported** | primary pass **and** at least one parameter-free signature present (QQ or Kvam), with neither contradicted |
| **quantum fits better, no unique signature** | primary pass, and neither signature present |
| **tie** | primary tie |
| **classical** | primary classical, or a signature contradicted with the primary not a pass |
| **untestable** | G1 failed |

**Reported alongside, outside the verdict:**
- the item-held-out test (same statistic);
- A5⁰ against F5⁰, the a priori, unfitted versions;
- A5 against A5 with κ = 0, which asks whether any A5 advantage comes from entanglement;
- D5 and BA5;
- MSE on M ratings only;
- the replicability rate in MF (|M₂ − M₁| ≤ 5 points);
- anchor-direction effects;
- results by category and by whether the model was right.

A "quantum supported" verdict would mean the quantum *probability* model describes this model's sequential ratings better than a matched classical updater, and shows a signature that the classical family cannot produce. It would not mean the network computes with quantum states. It would also not, on its own, rule out every classical account: Kang (2026) notes repetition mechanisms that satisfy QQ, and a richer non-Markov classical model with extra states can fit anything (Busemeyer et al. 2009).

## 8. Risks and mitigations

1. **The base model is near-deterministic.** In experiment 3, 85% of items gave the same yes/no answer in all 5 runs at T = 1. In experiment 4, every fallacy item saturated in binary form.

   **Mitigations:**
   - Graded 0–100 ratings throughout. Experiment 4's ratings had real spread and showed the fallacy.
   - Temperature cannot be raised: the API rejects an explicit temperature for this model (D17), so sampling stays at the default 1.0. Dispersion has to come from the measurement, not from sampling settings.
   - R = 10 repeats per chain and R = 40 per QQ order.
   - Anchor counterbalancing.
   - Inference over **items**. Even a chain whose ratings are identical across repeats still contributes its mean to the order and omission contrasts.
   - Pilot gates G1 and G2 stop the run before money is spent on a design the model cannot answer.
   - Items were chosen for internal competition between claims. Confident items resist anchoring (Owusu & Feldman 2026), so we avoided them.
2. **Context is everything for an LLM.** Any intermediate turn changes the context, so "asking changes later answers" is not by itself quantum. That is why the verdict rests on the matched-classical prediction contest and on two signatures that the classical families tested here cannot produce. The K0 filler matches K1's turn count.
3. **Silent consideration.** The model may weigh every claim while reading the question, as with the silent categorisation in Busemeyer et al. (2009). Then omissions do nothing. This is visible as X1–X4 ≈ O1, and it is reported, not explained away.
4. **Scale and label artefacts.** These are handled by anchor reversal and by a fixed sequential presentation mode (Kreutner et al. 2025).
5. **Equal parameter counts are not equal flexibility** (Trueblood & Busemeyer 2011). So the contest is on held-out chains and held-out items, never on in-sample fit.
6. **Encoder choices could bias the contest toward A5.** The anchored phase solve (D15) and the honest-hedge orientation (v2.1) are fixed here, before any data, and applied identically to F5's priors. F5 is A5's commuting limit by construction. The anchored solve works *against* A5: it shrinks the off-axis angles that give A5 its order effects, so whatever non-commutation remains comes from the relation web, not from solver drift. Expect A5 and F5 to be close on most claims.
7. **The grand-reciprocity tests do not apply.** Boyer-Kassem et al. (2016) apply them to non-degenerate projectors. Ours are degenerate (rank 2ⁿ⁻¹), so grand reciprocity is not a prediction and is not tested.

## 9. Candidate main questions (40)

The table is generated from the archived records by the rule in §3, with no model calls.
- **Claims** is the number of extracted claims.
- **Yes / no / hedge** counts claims with lean > 0.1, lean < −0.1 and |lean| ≤ 0.1.
- **Competing** counts the competing claims, split by side.
- **Exp-3 P(yes)** is the 5-run baseline from experiment 3, where the item was in it.

| # | id | category | model was | truth / model | claims | yes / no / hedge | competing | exp-3 P(yes) | main question |
|---|---|---|---|---|---|---|---|---|---|
| 1 | h190 | simpleqa | wrong | no / yes | 7 | 3 / 3 / 1 | 6 (3 yes, 3 no) |  | What is the name of the organization to which the Society of Illustrators sold the rights to their Illustrator Show skits in 1925? Is the answer "V… |
| 2 | h101 | simpleqa | wrong | no / yes | 8 | 4 / 3 / 1 | 7 (4 yes, 3 no) |  | From which university did Louise M. Antony (American philosopher) receive her bachelor's degree in philosophy? Is the answer "Duke University"? |
| 3 | h112 | simpleqa | wrong | no / yes | 9 | 4 / 3 / 2 | 7 (4 yes, 3 no) |  | What college did Anna Moriah Wilson graduate from in 2014? Is the answer "Emory & Henry College"? |
| 4 | h191 | simpleqa | wrong | no / yes | 10 | 4 / 3 / 3 | 4 (2 yes, 2 no) | 1.0 | Who won the 1991 Ig Nobel Prize for Peace? Is the answer "Patricia Mary Edmondson"? |
| 5 | h261 | simpleqa | wrong | yes / no | 8 | 3 / 5 / 0 | 5 (2 yes, 3 no) |  | On what date did the last total lunar eclipse for three years occur? Is the answer "November 8, 2022"? |
| 6 | h058 | sci-physics | wrong | yes / no | 9 | 3 / 6 / 0 | 8 (3 yes, 5 no) | 0.4 | What is the frequency of a 2-cm sound wave in sea water? What is the frequency of a 2-cm sound wave in sea water? The velocity of sound in sea wate… |
| 7 | h221 | simpleqa | wrong | yes / no | 8 | 2 / 4 / 2 | 6 (2 yes, 4 no) |  | How many years was the scholarship that Mary Fairchild MacMonnies Low won from the St. Louis School of Fine Arts for? Is the answer "three"? |
| 8 | h279 | simpleqa | wrong | yes / no | 10 | 3 / 6 / 1 | 5 (3 yes, 2 no) | 0.0 | In the 2012 research paper titled "Multiplication of EEG Samples through Replicating, Biasing, and Overlapping" by Adham Atyabi et al., between wha… |
| 9 | h127 | simpleqa | wrong | yes / no | 9 | 2 / 4 / 3 | 4 (1 yes, 3 no) |  | What was the original name of the show that conductor David Randolph hosted on the radio station WNYC? Is the answer "Music for the Connoisseur"? |
| 10 | h238 | sci-chemistry | wrong | yes / no | 8 | 2 / 4 / 2 | 4 (1 yes, 3 no) |  | A chemical reaction takes place in a container of cross-sectional area $50 \mathrm{~cm}^2$. As a result of the reaction, a piston is pushed out thr… |
| 11 | h111 | sci-physics | wrong | yes / no | 8 | 2 / 5 / 1 | 7 (2 yes, 5 no) | 0.0 | The planet Mercury travels around the Sun with a mean orbital radius of 5.8x10^10 m. The mass of the Sun is 1.99x10^30 kg. Use Newton's version of… |
| 12 | h197 | simpleqa | wrong | yes / no | 8 | 2 / 5 / 1 | 7 (2 yes, 5 no) | 0.0 | Between what dates was the Stanford University exhibition titled "Sam Richardson: Islands, Ice, and Sand" on view? Please give me the full dates (m… |
| 13 | h293 | simpleqa | wrong | yes / no | 8 | 2 / 5 / 1 | 7 (2 yes, 5 no) | 0.4 | In which year was the Kangri cancer effect first studied? Is the answer "1866"? |
| 14 | h102 | simpleqa | wrong | yes / no | 9 | 2 / 5 / 2 | 6 (1 yes, 5 no) | 0.0 | In what year was the beetle species Glipa angustilineata described? Is the answer "1993"? |
| 15 | h135 | sci-chemistry | wrong | yes / no | 9 | 2 / 5 / 2 | 6 (1 yes, 5 no) |  | A sample of bristle cone pine wood of age 7,000 \pm 100 years, known by counting growth rings, possesses an activity of 6.6 d(disintegrations) / mi… |
| 16 | h152 | simpleqa | wrong | yes / no | 9 | 2 / 5 / 2 | 6 (2 yes, 4 no) |  | What was the last year Charles Boyle, Viscount Dungarvan, 3rd Baron Clifford, was Member of Parliament for Tamworth in the British House of Commons… |
| 17 | h222 | simpleqa | wrong | yes / no | 11 | 2 / 5 / 4 | 6 (2 yes, 4 no) | 0.0 | What was the release price for the Sonic Free Riders original soundtrack in Japan in Japanese Yen? Is the answer "1800 JPY"? |
| 18 | h027 | simpleqa | wrong | yes / no | 9 | 2 / 5 / 2 | 5 (2 yes, 3 no) |  | What is the surname of the individual who won the Applied Inorganic Chemistry Award in 2015? Is the answer "Lu"? |
| 19 | h115 | simpleqa | wrong | yes / no | 7 | 2 / 5 / 0 | 4 (1 yes, 3 no) | 0.4 | To whom did Ragnar say, "When everyone wanted you dead, I kept you alive" in the Vikings episode "The Profit and the Loss"? Is the answer "Rollo"? |
| 20 | h137 | simpleqa | wrong | yes / no | 9 | 2 / 6 / 1 | 8 (2 yes, 6 no) | 0.0 | How many papers did Kunihiko Kodaira publish by 1941? Is the answer "10"? |
| 21 | h142 | simpleqa | right | yes / yes | 8 | 4 / 4 / 0 | 6 (3 yes, 3 no) | 1.0 | What was the day, month, and year when BSNL (Bharat Sanchar Nigam Limited) launched "BSNL Wings Services" in 22 telecom circles, in which there is… |
| 22 | h214 | simpleqa | right | yes / yes | 8 | 3 / 3 / 2 | 6 (3 yes, 3 no) |  | In what year was the Krieger–Nelson Prize awarded to Penny Haxell? Is the answer "2006"? |
| 23 | h187 | simpleqa | right | yes / yes | 10 | 3 / 3 / 4 | 4 (1 yes, 3 no) |  | What day, month, and year was Aniello Formisano, an Italian politician and lawyer, born? Is the answer "June 10, 1954."? |
| 24 | h019 | sci-chemistry | right | yes / yes | 9 | 5 / 4 / 0 | 8 (4 yes, 4 no) |  | For the indicator phenolphthalein (In^-),HInis colorless and In^- is red;K_dissis 10^-9. If one has a colorless solution of 50 ml phenolphthalein,… |
| 25 | h173 | simpleqa | right | no / no | 9 | 4 / 5 / 0 | 7 (3 yes, 4 no) | 0.0 | Cornelia Parker curated the "Black and White Room" for which exhibition? Is the answer "Titian Gallery"? |
| 26 | h149 | simpleqa | right | yes / yes | 10 | 5 / 4 / 1 | 5 (3 yes, 2 no) | 1.0 | What day, month, and year did the Nvidia GeForce GTX 460 SE (2010) launch? Is the answer "15th of November, 2010"? |
| 27 | h048 | sci-chemistry | right | yes / yes | 9 | 4 / 3 / 2 | 7 (4 yes, 3 no) |  | The atomic radius of hydrogen is 0.037 nm, Compare this figure with the length of the first Bohr radius. Explain any differences. Is the correct an… |
| 28 | h291 | sci-chemistry | right | yes / yes | 9 | 4 / 3 / 2 | 7 (4 yes, 3 no) |  | A line in the Lyman series of hydrogen has a wavelength of $1.03 \times 10^{-7} \mathrm{~m}$. Find the original energy level of the electron. Is th… |
| 29 | h093 | sci-chemistry | right | yes / yes | 8 | 5 / 3 / 0 | 6 (3 yes, 3 no) |  | Your supervisor asks you to determine the enthalpy of a certain chemical reaction. Which would you do? Is the correct answer "Use a solution calori… |
| 30 | h183 | claim | right | no / no | 9 | 3 / 5 / 1 | 6 (1 yes, 5 no) |  | Is the following claim true? Saturn's largest moon is Enceladus. |
| 31 | h237 | sci-physics | right | yes / yes | 8 | 5 / 3 / 0 | 6 (3 yes, 3 no) |  | Calculate the momentum uncertainty of a tennis ball constrained to be in a fence enclosure of length 35 m surrounding the court in kg m/s. Is the c… |
| 32 | h080 | claim | right | yes / yes | 10 | 6 / 3 / 1 | 9 (6 yes, 3 no) |  | Is the following claim true? The Berlin Wall fell in 1989. |
| 33 | h033 | claim | right | yes / yes | 9 | 6 / 3 / 0 | 7 (6 yes, 1 no) |  | Is the following claim true? Mount Kilimanjaro is in Tanzania. |
| 34 | h090 | claim | right | yes / yes | 9 | 6 / 3 / 0 | 7 (4 yes, 3 no) |  | Is the following claim true? Penicillin was discovered by Alexander Fleming. |
| 35 | h248 | sci-chemistry | right | no / no | 9 | 3 / 6 / 0 | 7 (1 yes, 6 no) |  | The mass of an electron is 9.109 × 10^-28 g. What is the atomic weight of electrons? Is the correct answer "9.109 × 10^-31 g/mole"? |
| 36 | h158 | claim | right | yes / yes | 9 | 6 / 3 / 0 | 6 (3 yes, 3 no) |  | Is the following claim true? Pluto was discovered by Clyde Tombaugh. |
| 37 | h126 | sci-physics | right | yes / yes | 10 | 7 / 3 / 0 | 4 (3 yes, 1 no) | 1.0 | What is the source of the material that causes meteor showers? Is the correct answer "The nuclei of comets gradually disintegrate and spread out al… |
| 38 | h043 | sci-physics | right | no / no | 9 | 2 / 5 / 2 | 4 (2 yes, 2 no) |  | a) The maximum pressure variation P that the ear can tolerate in loud sounds is about 28 N / m^2 (=28 Pa). Normal atmospheric pressure is about 100… |
| 39 | h203 | sci-physics | right | yes / yes | 8 | 6 / 2 / 0 | 7 (5 yes, 2 no) |  | One astronomical unit (AU) is equal to approximately ... Is the correct answer "150 million km"? |
| 40 | h294 | sci-physics | right | no / no | 10 | 2 / 7 / 1 | 6 (1 yes, 5 no) |  | Include air resistance proportional to the square of the ball's speed in the previous problem. Let the drag coefficient be $c_W=0.5$, the softball… |

## 10. Cost estimate (Anthropic API; no QPU time)

The estimate uses the per-token prices assumed in experiment 3's estimate ($0.10 in and $0.50 out per MTok for `claude-haiku-5-5`). It is cross-checked against experiment 4's measured cost: 5,480 short rating calls for $0.23, or $0.000042 per call. Thinking is disabled, and each answer is a JSON integer of about 20 output tokens.

| block | conversations | calls (turns) | tokens per conversation (in / out) | cost |
|---|---|---|---|---|
| chains: 40 items × 12 types × R = 10 | 4,800 | ≈ 22,000 (4.6 rating turns on average; each turn re-sends the history) | ≈ 1,730 / 115 | ≈ $1.11 |
| QQ block: 40 items × 2 pairs × 2 orders × R = 40 | 6,400 | 12,800 | ≈ 570 / 50 | ≈ $0.52 |
| pilot: 5 items, full design | 1,400 | ≈ 4,400 | as above | ≈ $0.20 |
| **total** | **12,600** | **≈ 39,000** | | **≈ $1.85** |

- At exp 4's measured cost per call, 39,000 calls would cost about $1.64. The history-length allowance above brings that to about $1.85.
- **Cap: $4.00, enforced in code.** That is roughly 2× the estimate, to cover longer questions in the science items and longer history in 6-turn chains.
- Wall-clock: roughly 2–4 hours at 4 parallel workers.
- No IBM time is used. A5 is evaluated by exact statevector simulation (at most 11 qubits per item).

## 11. What is deliberately left out

- **(S_i, S_j) QQ pairs.** A5 predicts commuting projectors there, so the test would be a trivial pass with no information.
- **A transcript-edited condition**, where the model's rating is removed from context before the next turn. It would separate the effect of the question from the effect of the model's own answer (Echterhoff et al. 2024), but it changes the presentation mode.
- **Binary yes/no versions of the sub-questions.** They saturated in experiment 4.
- **QPU runs.** No hardware time is requested unless the verdict is "quantum supported". In that case a follow-up would put the selected A5's states for the QQ items on `ibm_fez` as a separate, separately pre-registered step.


## Addendum — run 2: B0 and the QQ block re-run with one scale direction (pre-registered 2026-11-03 22:59 MST, D33)

**Why.** Run 1 counterbalanced the scale anchors. The model did not reliably reverse the flipped scale: recoded B0 means were 33.8 under (a) and 71.3 under (b). Do the order effects and the near-zero q survive without that confound?

**Design.** There is no refitting, and no model is involved. This is a descriptive re-measurement.
- **Items:** the first 10 candidates in §9's order: h190, h101, h112, h191, h261, h058, h221, h279, h127 and h238.
- **Cells:**
  - B0, the main question only, R = 10.
  - The QQ block: the same 2 pairs per item as in `experiments/split-exp5.json`, both orders, R = 40.
- **Every conversation uses anchor (a)**, "0 = certainly false, 100 = certainly true". Settings are otherwise identical to run 1. The cap is $1, and any refusal stops the run.

**Reported.**
- Per pair, as in §7.3: OE [95% CI], OE_S, OE_M, OSS, q and z.
- The number of pairs with OE > 0.10 and a CI excluding 0.
- Mean q with an item-bootstrap 95% CI, and KS of z.
- B0's mean and between-repeat SD.
- Each beside run 1's numbers for the same 10 items, computed two ways: all anchors pooled, and anchor (a) only.

**Reading, fixed now.**
- **The order effects "survive"** if at least half of the pairs that had a large OE in run 1 also have one in the re-run.
- **The near-zero q "survives"** if the re-run's mean-q CI contains 0. If the CI also lies within ±0.05, run 1's QQ near-miss is resolved in the equality's favour.

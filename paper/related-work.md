# Related work

*The Entangled Mind*: literature notes, written 2026-11-03. BibTeX keys refer to [`references.bib`](references.bib). Borrowed test items are in [`../experiments/items-borrowed.json`](../experiments/items-borrowed.json).

**How these notes were made.** The two most recent LLM papers (Aerts et al. 2025; Kang 2026) were read in full from arXiv HTML. The other papers were read by three reading passes, from full text where an open copy existed. Any paper read only in part is marked **[partial]**, with what the summary rests on. Numbers marked *recomputed* were derived by us from the authors' printed tables; the scripts are not in the repository, but every derived number is reproduced in `items-borrowed.json` next to the input counts.

This project joins a conversation that has run for about fifteen years. Most of what follows is what we can learn from it.

---

## 1. Quantum structure in concepts, and its extension to LLMs

### Aerts & Sozzo 2011: "Quantum structure in cognition: why and how concepts are entangled" `aerts2011quantum`

- **Tested:** whether choices of exemplars for the combination *The Animal Acts* violate the CHSH inequality. There are four 2-way observables:
  - A = Horse/Bear
  - A′ = Tiger/Cat
  - B = Growls/Whinnies
  - B′ = Snorts/Meows

  Each is coded +1/−1. They give four joint settings (AB, AB′, A′B, A′B′), each a forced choice among 4 sentences.
- **On whom:** 81 "friends and colleagues" (a convenience sample). Every participant did all four single-concept and all four joint settings, within subject.
- **How answers were collected:** a written questionnaire. Pick "a good example", exactly one per setting, letting "ratio, but also imagination, feeling, emotion" play a role.
- **Result:**
  - E(A,B) = −0.778, E(A′,B) = 0.654, E(A,B′) = 0.358, E(A′,B′) = 0.630.
  - **CHSH = 2.4197** (196/81), above the classical bound of 2 and below Tsirelson's bound of 2.83.
  - p = 0.0171 against 2, in the 2014 follow-up (`aerts2014quantum`).
- **Authors' limitations:** the 2014 paper notes that the marginal law fails (P(Tiger) is 0.864 in A′B but 0.234 in A′B′). The data therefore need "entangled measurements", not only an entangled state. The 2019 analysis (`aerts2019quantum`) repeats the counts and lists all eight marginal-law violations.
- **What we borrow:** the item (four settings, ±1 scoring), reproduced exactly in `items-borrowed.json → chsh_animal_acts`.
- **How we differ:** we do not test inequalities on choice frequencies. We build a state from one model's stated reasons for one answer, and ask whether it predicts errors.

### Aerts, Aerts Arguëlles, Beltran, Geriente, Leporini, Sassoli de Bianchi & Sozzo 2025: "Identifying Quantum Structure in AI Language" (arXiv:2511.21731; *Entropy* 28(6):622, 2026) `aerts2026identifying`

- **Tested:**
  1. The Animal Acts CHSH test with LLMs in place of humans.
  2. Whether word-rank frequencies in LLM-written stories follow Bose–Einstein rather than Maxwell–Boltzmann statistics.
- **On whom:** "ChatGPT" and "Gemini". No model versions are given.
- **How answers were collected:**
  - A guided single conversation.
  - Two prompts, "exploratory" (use imagination, creativity, originality) and "neutral". Each asked for 10 sessions of the four tests **inside one response** (11 in the last round), run in 8 conversations to reach 81 sets.
  - For the statistics test: one Winnie-the-Pooh story written by each model (Gemini also wrote an H. G. Wells pastiche), fitted with the two distributions constrained by total word count and total "energy" (rank − 1).
- **Result:**
  - The guided conversation gives CHSH = 4, the algebraic maximum.
  - ChatGPT gives CHSH = 2.25 (exploratory) and 3.09 (neutral). Gemini gives 2.12 and 4.
  - The authors average these to 2.67 (ChatGPT) and 3.06 (Gemini), "consistent with" the human 2.42.
  - Bose–Einstein fits each story closely and Maxwell–Boltzmann fails.
  - They read this as convergent evolution of meaning structure in human and artificial cognition, with relevance to AI safety.
- **Authors' limitations:** the paper has no limitations section. It notes that the guided conversation drives the model to "the most likely answers", producing maximal violation.
- **Our reading, offered as a colleague:**
  - Values above Tsirelson's 2.83 (3.09, and 4) cannot come from any quantum state measured by fixed local observables. They mean the marginals shift with context, i.e. signalling.
  - *Recomputed* from their printed Table 3: E(A′,B) = 1.000 (the text's 0.556 equals the marginal ⟨A′⟩), so the table implies CHSH = 3.53.
  - Under Contextuality-by-Default (`kujala2016proof`), the system is contextual only if the CHSH-type sum exceeds 2 + Δ, where Δ is the total shift of the four marginals between contexts. *Recomputed* Δ:

    | data | CHSH | Δ | bound 2 + Δ | contextual? |
    |---|---|---|---|---|
    | humans | 2.42 | 3.78 | 5.78 | no |
    | ChatGPT, exploratory | 2.25 | 3.75 | 5.75 | no |
    | ChatGPT, neutral | 3.53 | 4.50 | 6.50 | no |

    No dataset, human or LLM, is contextual in that sense. This is the critique Dzhafarov & Kujala (`dzhafarov2014selective`) made of the human study in 2014.
  - Sampling many "sessions" inside one generation also makes the 81 sets dependent draws.
- **What we borrow:**
  - The item.
  - Their two prompts, quoted in the JSON under CC BY 4.0.
  - A protocol fixed in the JSON to avoid the issues above: one fresh call per trial, randomised option order, Δ and the CbD verdict reported next to CHSH.
- **How we differ:** our entanglement lives in a state we construct and can certify physically. We do not infer it from behavioural correlations, which signalling alone can produce.

### Dzhafarov & Kujala 2014: "On selective influences, marginal selectivity, and Bell/CHSH inequalities" `dzhafarov2014selective` **[partial: abstract and secondary descriptions]**

- **Tested:** an analytical commentary on Aerts, Gabora & Sozzo 2013 (`aerts2013concepts`).
- **Argument:** Bell/CHSH tests are informative only if marginal selectivity (no-signalling) holds, and in behavioural data it "almost never" does. A CHSH violation together with a violation of marginal selectivity can mean only that one response is influenced by both factors. The later Contextuality-by-Default framework (`kujala2016proof`) turns this into the corrected inequality used above.
- **What we borrow:** the requirement to report Δ next to any Bell-type statistic.
- **How we differ:** we test prediction of errors, not inequality violation, so this critique applies only to the borrowed CHSH item.

---

## 2. Question-order effects and the QQ equality

### Wang & Busemeyer 2013: "A quantum question order model supported by empirical tests of an a priori and precise prediction" `wang2013quantum`

- **Tested:** the parameter-free QQ equality, which projective (Lüders) sequential measurement implies whenever nothing intervenes between the two questions:

  q = [p(Ay,Bn) + p(An,By)] − [p(By,An) + p(Bn,Ay)] = 0

  Joint arguments are written in asking order. In words, the probability that the two answers disagree is the same in both orders.
- **On whom:**
  - Four Gallup split-ballot national surveys reported by Moore (2002) (`moore2002measuring`): Clinton/Gore 1997, Gingrich/Dole 1995, White/Black hostility 1996, Rose/Jackson 1999. Each had 377–506 yes/no respondents per order.
  - Two between-subjects lab experiments (N = 224 and 224).
- **How answers were collected:** split-ballot surveys, with each respondent seeing one order. Binary answers only; others were excluded from the test.
- **Result:**
  - Clinton/Gore q = −0.003 (|z| = 0.11).
  - Gingrich/Dole q = −0.003.
  - White/Black q = −0.019.
  - Lab affirmative action q = +0.043.
  - The QQ equality holds in each of these, despite order effects of up to 9.5 points on the marginals (Gore: 76% first, 67% second). It also holds in the racial-hostility lab experiment (q = +0.076, n.s.).
  - Rose/Jackson, where a background paragraph precedes each question, was predicted in advance to fail, and does: q = +0.151, z = 5.30.
- **Authors' limitations:**
  - The derivation holds only if answering the first question is the only thing that changes the state.
  - The claim that Markov models violate QQ is asserted, with proof "available upon request".
- **What we borrow:**
  - The equality and test.
  - Four human joint tables.
  - The Rose/Jackson negative control.

  All are in `items-borrowed.json → qq_order_protocol`. Note that the printed variance formula 2p(1−p)/N does not reproduce the authors' own z values; p(1−p)/N does, and we use that.
- **How we differ:** we model one respondent's deliberation per item, not a population's aggregate answers.

### Wang, Solloway, Shiffrin & Busemeyer 2014: "Context effects produced by question orders reveal quantum nature of human judgments" (PNAS) `wang2014context` **[partial: main text via repeated web extraction; the supplement was not accessed]**

- **Tested:** the QQ equality across many datasets.
- **On whom:** 70 national representative surveys (each 651–3,006 respondents) plus 2 lab experiments, 72 in total. Sixty-six of the surveys are all the Pew Research Center surveys from 2001–2011 that manipulated the order of two questions.
- **How answers were collected:** split-ballot surveys.
- **Result:**
  - Across the 66 Pew surveys, the order-effect χ² values deviate from the null (p = 0.0004) but the q χ² values do not (p = 0.46).
  - The two diagonal context effects correlate at r = −0.82 across the 72 studies, against the a priori line of slope −1.
  - Among the 17 studies with order effects above 0.10, |q| stays small relative to the effect.
  - The PNAS text uses the diagonal sign convention in one place and the off-diagonal one in Table 1, so state the convention when citing it.
- **Authors' limitations:**
  - "Most studies on context effects only report the marginal proportions."
  - A model "narrowly constrained to satisfy the QQ equality" might be unable to produce order effects.
  - A general theory is still needed.
- **What we borrow:** the many-pairs aggregate test (distribution of q against distribution of order effects), for any LLM QQ audit with more than a handful of pairs.
- **How we differ:** same as Wang & Busemeyer 2013.

### Boyer-Kassem, Duchêne & Guerci 2016a: "Testing quantum-like models of judgment for question order effect" `boyerkassem2016testing`; and 2016b, "Quantum-like models cannot account for the conjunction fallacy" `boyerkassem2016conjunction`

- **Tested:** whether the data that satisfy QQ also satisfy the stronger "Grand Reciprocity" (GR) equations, p(b0|a0) = p(a0|b0) = p(b1|a1) = p(a1|b1) and the mirror equations. GR is required by any **non-degenerate** quantum model, i.e. one where each answer is a ray in a 2-D space.
- **On whom:** the same 72 datasets as Wang et al. 2014 (median 741 respondents), plus Conte et al.'s perception data. In 2016b, 1,152 participants in France (mostly students) across 7 order tasks built on Linda, Bill, Mr F. and K. scenarios.
- **How answers were collected:** the authors' own analysis of the original survey files (2016a). In 2016b, paper and computer questionnaires, paid and unpaid.
- **Result:**
  - QQ is "experimentally verified in all these cases", but more than 90% of the 72 experiments reject at least one GR test (mean 3.6 rejections out of 6).
  - The 7 that pass show no order effect at all. So "no non-degenerate quantum-like model is needed or, when needed, is possible."
  - In 2016b, GR is never satisfied, and QQ itself is rejected for the computer-administered Linda task (3 of 7 tasks before Bonferroni correction). The general quantum account is refuted "in at least three tasks out of seven".
- **Authors' limitations:** only degenerate (higher-dimensional) models survive, and these need an independent justification for their extra dimensions, or they become free parameters. Busemeyer & Wang reply that real models are multi-dimensional, so the GR test targets "toy" versions.
- **What we borrow:** the sharper three-step test battery (order effect present? QQ? GR?) and the argument that passing QQ "gives good grounds to think (but does not prove)" a quantum model can fit.
- **How we differ:** our state is 5–16 qubits by construction, with its dimension set by the number of extracted claims rather than chosen to fit.

### The replicability line: Khrennikov, Basieva, Dzhafarov & Busemeyer 2014 → Busemeyer & Wang 2017 → Ozawa & Khrennikov 2020/2021 → **Fuyama, Khrennikov & Ozawa 2025** `khrennikov2014quantum` `busemeyer2017problem` `ozawa2020application` `ozawa2021modeling` `fuyama2025quantum`

- **Tested (theory):**
  - Three properties: (1) asking A twice gives the same answer; (2) A–B–A also gives the same answer; (3) order effects exist. Khrennikov et al. (2014) prove the three are incompatible under projective measurement, and with POVMs that have the Lüders property.
  - Ozawa & Khrennikov (2020; 2021 adds QQ) recover them with non-projective quantum instruments over commuting observables. There, order effects come from non-commuting *state updates*, not non-commuting observables.
  - Fuyama, Khrennikov & Ozawa (2025, *Phil. Trans. R. Soc. A* 383:20240372) consolidate this. Cognition needs "sharp repeatable non-projective" measurements, which "can both satisfy and violate" the QQ equality.
- **On whom:** Busemeyer & Wang 2017 is the one empirical test: 325 MTurk workers, 12 pairs known to show order effects, presented A–B–A on 0–100 sliders under a memory load. Fuyama et al. note that "up to now, only one experiment was performed."
- **Result:**
  - Individual answers to the repeated A changed substantially (the SD of A1 − A2 is about 10 points).
  - Across pairs, the A–B correlation tracked the A1–A2 correlation (r = .86).
  - The B–A correlation exceeded A–B in 10 of 12 pairs.
- **Authors' limitations:** the memory load "does not guarantee" participants could not remember their answers. Fuyama et al. 2025 is theoretical, with no new data.
- **What we borrow:**
  - A critique we must answer in Experiment 3. An LLM that sees its own earlier answer in context is a near-perfect instance of A–A replicability. So a projective account of LLM order effects is already in tension with replicability, before any data.
  - The A–A versus A–B–A contrast is a cheap extra condition.
- **How we differ:** our "asking" operator in Experiment 3 is a local unitary evolution (the contention's own Hamiltonian term), not a projector, so it is closer to the instrument models than to the projective one. That should be stated explicitly when results are interpreted.

### Kang 2026: "Auditing Question-Order Effects in Large Language Models with the QQ Equality" (arXiv:2607.17219) `kang2026auditing`

- **Tested (theory):**
  - Which mechanism families satisfy QQ robustly. A purely classical *symmetric repetition* mechanism (repeat your first answer with probability r, otherwise answer fresh) satisfies q = 0 **identically** while producing order effects (Proposition 4).
  - For the rank-2 cyclic system, the Contextuality-by-Default criterion becomes |q| ≤ OSS = |OE_A| + |OE_B|. Only |q| > OSS certifies residual contextuality.
- **Tested (empirical):** 18 item pairs on Qwen3-4B-Instruct-2507 (bf16, non-thinking):
  - 10 historical survey pairs.
  - 3 name-swapped memorisation controls (e.g. Blair/Brown for Clinton/Gore).
  - 5 novel vignette pairs.
  - Two framings: direct evaluation, and a survey-respondent persona (8 pairs).
- **How answers were collected:** a committed multi-turn forced-branch protocol.
  - Read P(y | y or n) from next-token log-probabilities.
  - Commit each possible first answer as the assistant turn.
  - Read the second answer's distribution under each branch.
  - Neutral A/B labels, counterbalanced across both mappings.
  - Health gates: single-token labels, unassigned mass below 10⁻², and log-probabilities checked against sampling at T = 1 using Clopper–Pearson intervals.
- **Result:**
  - All gates passed, yet the distributions were **saturated** (max(p, 1−p) > 0.99 at most positions) for 17 of 18 pairs, and 7 of 8 under the persona framing.
  - Pooled verdicts: 13 VIOLATED, 5 SATISFIED, **0 certified contextual**.
  - Label mapping changed the QQ verdict for 4 pairs. q differed by up to 1.48 between mappings (s1-01: −0.56 vs +0.92).
  - Pair s1-07 (US/Japan trade limits) shows large, opposite order effects (±0.39), q ≈ 0, and a certified non-contextual result (Γ_upper = −0.77). Order sensitivity, QQ satisfaction and contextuality are three separate properties.
- **Author's limitations:**
  - One model, one measurement scheme, 18 English pairs mostly from US surveys.
  - Three memorisation controls is too few for inference.
  - No human joint data were used for calibration.
  - The no-prior-work claim covers searches to July 2026.
- **What we borrow:**
  - The whole protocol, the decision rules (ε = 0.02 band, saturation gate, Γ certification) and the 18 pairs (MIT licence), all in the JSON.
  - We adapt it to the Anthropic API, which returns no log-probabilities, by sampling R = 50 per position and recasting the saturation gate.
  - We attach Wang & Busemeyer's human joint tables to the 4 pairs that have them, which fills the gap the author names.
  - *Recomputed* from those tables, every human pair has Γ < 0, including Rose/Jackson (q = 0.151, OSS = 0.250). Human order data are also non-contextual under this criterion.
- **How we differ:** our pre-registered Experiment 3 asks which of the model's *own* contentions shift its answer, and whether the quantum state predicts that better than the classical twin. Kang's audit asks whether fixed external pairs satisfy an identity.

---

## 3. Conjunction fallacies, co-occurrence and dynamic models

### Tversky & Kahneman 1983: "Extensional versus intuitive reasoning" `tversky1983extensional`, with Fiedler 1988 `fiedler1988dependence` and Hertwig & Gigerenzer 1999 `hertwig1999conjunction` (frequency formats)

- **Tested:** the conjunction rule P(A∧B) ≤ P(B), using personality sketches such as Linda (T = bank teller, F = feminist) and Bill (A = accountant, J = plays jazz).
- **On whom:** undergraduates at Stanford and UBC, graduate and medical students, and decision-science doctoral students.
- **How answers were collected:** ranking 8 statements by probability; choosing between T and T&F; 9-point ratings; bets.
- **Result:**
  - Ranking, direct test, Linda: 89% (naive, N = 88), 90% (informed, N = 53) and 85% (sophisticated, N = 32) violated the rule. Bill: 92%, 86% and 83%.
  - Choosing between T and T&F: 85% chose T&F (N = 142). Reversing the order of the two options had no effect.
  - The "whether or not she is active" (T*) version: 57% (N = 75).
  - Betting version: 56% (N = 60).
  - Frequency formats ("Imagine 200 women…") reduce the rate. Fiedler 1988 reports 22% and 17% for Linda; Hertwig & Gigerenzer report 0–20% (N = 20–25 per condition), against 82–88% in matched probability-ranking conditions.
- **Authors' limitations:** TK themselves show that the rate depends on format and transparency. Hertwig & Gigerenzer argue that "probability" is read non-mathematically.
- **What we borrow:** ten yes/no pool items with normative answers (`linda_variants.pool_items`).
  - Each carries the published human rate where one exists.
  - Order and polarity controls are included.
  - Novel and name-swapped twins are included because these vignettes are almost certainly in training data.
- **How we differ:** we treat a fallacy as one more kind of model error to be predicted, not as the phenomenon to be fitted.

### Busemeyer, Pothos, Franco & Trueblood 2011 (*Psych. Rev.*) `busemeyer2011quantum`, and Yearsley & Trueblood 2018: "A quantum theory account of order effects and conjunction fallacies in political judgments" `yearsley2018quantum`

- **Tested:** whether order effects and conjunction fallacies co-occur, as they should if both arise from incompatible (non-commuting) events. Also two parameter-free constraints: an order-effect identity for sequential evidence, and quantum upper and lower bounds on a conjunction given its marginals.
- **On whom:** 1,200 US MTurk workers ($1.50 each), each judging one Democrat (Clinton or Sanders) and one Republican (Cruz, Rubio or Trump). The events were same-day Super Tuesday 2016 primaries, which participants were told were causally unlinked.
- **How answers were collected:**
  - Qualtrics, 17-point verbal-label scale.
  - Single, conditional and conjunction questions, in four randomised blocks.
  - CRT and ideology measures afterwards.
  - Bayesian tests (JASP).
- **Result:**
  - Recency order effects in all 10 comparisons (BF₁₀ > 10³).
  - Single conjunction fallacies in 37 of 40 comparisons (BF₁₀ > 12).
  - **No double fallacies** (all BF < 0.015), as quantum theory requires.
  - No evidence against the order constraint.
  - All mean points lie within the quantum bounds.
  - The CRT predicted both effects.
  - On co-occurrence the paper says only that "the majority of participants display both" and that the data lie mostly in the region a simple quantum model's simulation covers. **No correlation or count is reported.**
- **Authors' limitations:**
  - An unrepresentative MTurk sample (54% liberal; CRT scores the reverse of Frederick 2005).
  - Incompatibility cannot be measured directly, only inferred from order effects.
  - No rival model covers both effects, so a formal model comparison was not possible.
- **What we borrow:** the prediction, written as four rules (`cooccurrence_rule` in the JSON).
  - R1: a single fallacy implies incompatibility, which implies a nonzero order effect.
  - R2: our derivation from ‖P_Y P_X ψ‖² ≤ ‖P_X ψ‖². If P(X then Y) > P(Y), then P(X then Y) − P(Y then X) ≥ the size of the fallacy. The static classical twin (arm F) reads every judgment from one joint distribution, so it predicts no fallacy and no order difference. **Correction (2026-11-03):** a classical model in which each judgment updates the state (Experiment 3's sequential twin is one) can produce both, and it also satisfies this inequality, because P(Y then X) ≤ P(Y) holds for it too. R2 is therefore a necessary condition for the quantum account, not a discriminator against sequential classical models.
  - R3: no double fallacies.
  - R4: more likely conjunct first.

  Fictional same-day events are included so that outcomes cannot be known from training data.
- **How we differ:** R1–R3 make their qualitative "should co-occur" quantitative, and they rule out static classical accounts by construction. Against classical models whose judgments update the state, only per-item numerical predictions from a state fixed in advance (the model's own claims) can discriminate. That is the comparison style of the rest of this project.

### Busemeyer & Bruza 2012: *Quantum Models of Cognition and Decision* `busemeyer2012quantum` **[partial: official table of contents and preface, chapter abstract, and the underlying papers]**, Busemeyer, Wang & Townsend 2006 `busemeyer2006quantum`, and Pothos & Busemeyer 2009 `pothos2009quantum`

- **Tested:** dynamic models, in which a state evolves under a Hamiltonian before measurement:
  - Markov: dφ/dt = Qφ.
  - Quantum: dψ/dt = −iHψ, "the same rules … applied to probability amplitudes."
  - Book chapters 8–9 develop the two in parallel (bistable perception, categorisation then decision, random-walk signal detection, the disjunction effect, dynamic consistency).
  - Pothos & Busemeyer 2009 model the prisoner's dilemma and two-stage gamble with a 4-D state (belief ⊗ action), H = H_A (payoff, parameter μ) + H_B ("cognitive dissonance", rotating belief toward one's planned action, parameter γ), read out at t = π/2.
- **On whom:** published data.
  - Shafir & Tversky 1992 and three other PD studies: defection is 84% when the other is known to defect, 66% when known to cooperate, and 55% when unknown (averages). The unknown case falls below both known cases, violating the law of total probability.
  - Tversky & Shafir 1992 two-stage gamble: 69/59/36%.
- **Result:**
  - The quantum model fits the PD averages with μ = 0.51, γ = 2.09, predicting 81/65/57%. For the gamble, μ = 0.59, γ = 1.74, predicting 68/58/37%.
  - The paper proves that any Markov model with any intensity matrix makes the unknown case a convex mixture of the known cases, so it cannot fit.
  - Busemeyer, Wang & Townsend 2006, fitting the Ratcliff & Smith response-time data, found the **Markov** model fitted better (χ² = .05 vs .11). Dynamics do not automatically favour the quantum version.
- **Authors' limitations:** the 2009 model has 2 free parameters per dataset and a fixed read-out time. Belief and action are treated as compatible, so the interference comes from the dynamics alone.
- **What we borrow:** the design pattern of our encoding and of Experiment 3. A problem Hamiltonian built from the stakes, a mixer, a fixed short evolution, and a Markov comparator on the same graph, which is our arm F. The known/known/unknown "sure-thing" triple is a natural future item set.
- **How we differ:** our Hamiltonian's couplings come from a relation web extracted from the model's own explanation, not from two fitted parameters. The comparator is an exact classical twin with the same graph and fields.

### Pothos & Busemeyer 2013: "Can quantum probability provide a new direction for cognitive modeling?" (BBS target article, 34 commentaries, response) `pothos2013can`

- **Tested (argument):** that quantum probability is a computational-level framework covering conjunction and disjunction fallacies, order effects, the PD and gamble violations, and similarity asymmetries. Constraints include double stochasticity, reciprocity for rays, and Gleason's theorem.
- **On whom:** a review of published studies, including the Linda account: ψ close to "feminist", the more probable outcome evaluated first.
- **Result:** one complexity-controlled Bayesian comparison favoured quantum probability by Bayes factors of 2.1–2.5.
- **Commentators' main critiques:**
  - Tentori & Crupi: the 2-D model forbids double fallacies, yet in their "Russian woman" problem 70% of fallacious choices were of the form the model does not predict. A small shift of ψ flips the Linda prediction.
  - Kaznatcheev & Shultz: a framework, not a theory. The "more probable first" rule sits outside the formalism. Aerts & Sozzo's Bell test lacks separation, since both concepts are in one mind.
  - Rakow; Newell, van Ravenzwaaij & Donkin: the choice between compatible and incompatible representations, and the choice of order, add hidden flexibility.
  - Love; Navarro & Fuss; Marewski & Hoffrage: the framework needs grounding in mechanism.
  - Gonzalez & Lebiere: ACT-R memory retrieval produces the same effects.
- **Authors' response:**
  - "Dimensionality is not a free parameter."
  - Incompatibility is to be detected empirically, through order effects.
  - A 3-D model handles Tentori & Crupi's case.
  - They concede that Bell-type tests in psychology face noisy, ill-defined quantities.
- **What we borrow:** the flexibility critique as a design constraint. Every quantum arm here has a classical twin with the same inputs and the same parameter count, so flexibility cannot be what wins.
- **How we differ:** the target article's evidence is fits to aggregate data. Ours is out-of-sample error prediction on held-out items.

---

## 4. LLMs: cognitive probes and probability coherence

### Binz & Schulz 2023: "Using cognitive psychology to understand GPT-3" (PNAS) `binz2023using`

- **Tested:** 12 canonical vignettes (Linda, Cab, Hospital, Wason, the 3 CRT items, causal Blicket tasks and others) and four task-based paradigms: decisions from descriptions (over 13,000 problems), the horizon task, the two-step task, and causal reasoning.
- **On whom:** GPT-3 "Davinci". The released code uses `text-davinci-002`.
- **How answers were collected:**
  - Q:/A: completion prompts at temperature 0.
  - For choice proportions: first-token probabilities at T = 1, with option order counterbalanced.
  - For Linda, a third filler option was added: "Linda is a member of the NRA".
- **Result:**
  - 6 of 12 vignettes correct, and all 12 "human-like". It committed the Linda conjunction fallacy and gave the intuitive wrong answer on all three CRT items.
  - Small adversarial edits broke it. Reordering the Wason cards changed its choice. "The bat costs $1.00 more than the bat" still produced $0.10. It answered "20%" for the probability of a black cab when none exist.
  - Tasks: it was above chance but below humans on decisions from descriptions, showed 3 of 6 prospect-theory biases, a model-based signature in the two-step task, no directed exploration, and failed causal reasoning.
- **Authors' limitations:**
  - Vignettes are probably in the training data, and results are fragile under perturbation.
  - Cover stories shift behaviour (a casino frame versus an investment frame).
  - Whether a model is "a single participant or many" is open.
- **What we borrow:** perturbation and procedurally generated twins as a contamination check (used for `lin07`–`lin10`); first-token choice probabilities with counterbalanced option order.
- **How we differ:** we ask why a model errs on a given item, from its own stated considerations, not whether it errs like humans on average.

### Wolf, Kleine Buening, Krause & Mendler-Dünner 2026: "Partition, Prompt, Aggregate: Statistical Self-Consistency in Language Models" (arXiv:2607.15277) `wolf2026partition`

- **Tested:** whether in-context probability estimates obey the law of total probability (LTP) when the conditioning event is partitioned into binary trees of subgroups. Domains:
  - ACS 2024 income and commute times.
  - World Values Survey opinions (Canada, Indonesia).
  - Two synthetic forecasting tasks.
- **On whom:** GPT-5.4, Claude Sonnet 4.6, Grok 4.3 / 4.1 Fast and Qwen3.6 Plus in the main tables, plus about 20 more models (GPT, Qwen, Gemini 3, Opus 4.7) in a scaling figure.
- **How answers were collected:** verbalised probabilities in a fixed `[[p]]` format. Priors were averaged over 50 queries per tree level. Temperature and repeat count were held fixed across conditions.
- **Result:**
  - Estimates rebuilt from finer subgroups are **closer to ground truth** than the model's direct estimate (the "macro fallacy"). "Micro-to-macro" prompting partly recovers the gain.
  - Split-consistency (LTP holds within ε = 0.02) ranges from 0.00 to 1.00 across tasks and models.
  - Order-consistency (invariance to the order in which constraints are stated) is generally higher.
  - Neither improves with general capability.
- **Authors' limitations:**
  - Mostly ACS data.
  - Dependence on verbalised elicitation, normalisation and the choice of splits.
  - Self-consistency is necessary but not sufficient for accuracy.
- **What we borrow:** a reminder that LTP violations in LLMs have a systematic, *classical* explanation (direct versus decomposed prompting). Any "interference" reading of an LTP residual has to beat that explanation, and a classical twin should be given the same decomposition.
- **How we differ:** we do not test identities over many items. We test whether a per-item structure predicts per-item errors.

### Beuria 2026: "Emergent non-classical probabilistic structure in large language models under contextual modulations" (*Scientific Reports*) `beuria2026emergent` **[partial: published abstract and appendices; full v1 preprint, which differs substantially]**

- **Tested:**
  - Residuals of eight classical identities (Z1–Z8, including LTP).
  - QQ residuals.
  - Competing accounts: a coherent 2×2 joint, probability theory plus noise, the product rule, Nilsson configural weighting, and the quantum sequential "more likely first" rule.
- **On whom:** six open-weight LLMs. The appendices name Gemma 2 9B, Mistral 7B and Qwen 2. The v1 preprint used Llama3 8B, Mistral 7B, Qwen2 7B and Gemma 7B via ollama.
- **How answers were collected:**
  - Verbalised probabilities in JSON.
  - The identity battery uses one ambiguous person (A = scientist, B = enjoys mathematics, C = writes poetry).
  - The QQ battery shows the model its own p_X before asking about Y.
  - v1 used 1,000 queries per task at temperature 0.7.
- **Result:**
  - Classical identities are "systematically violated, with partition identities most strained", but no single framework explains the violations.
  - "More likely first" often reconstructs conjunctions best.
  - On order: "small QQ residuals coexist with similarly small errors from an order-invariant classical joint-distribution baseline, so the order data do not independently select a quantum account."
  - The conclusion is "model-dependent departures from classical probability, not a universal quantum signature."
- **Author's limitations:** not visible in the parts we could read.
- **Our reading:** the published version is more cautious than the preprint. The preprint's "quantum fit" R² of 0.80–0.92 rested on an angle defined from the residual itself.
- **What we borrow:** the non-stereotyped conjunction control (`lin09`); the habit of naming the classical competitors explicitly; and the sentence above, quoted in our "contested" section.
- **How we differ:** our classical competitor is not a different probability calculus. It is the same graph without amplitudes.

### Imannezhad, Pothos & Wills 2026: "Divergent patterns of probabilistic reasoning in humans and GPT-5" (*Frontiers in Psychology* 17:1782184) `imannezhad2026divergent`

The brief described this as a paper on comparative reasoning; it tests probability rules.

- **Tested:** the conjunction and disjunction rules, and marginal and joint binary complementarity. Items: 2020 US election forecasts for state triplets (Ohio/Missouri/Michigan, Georgia/Montana/Nevada), 78 items including reversed-order composites.
- **On whom:** `gpt-5-2025-08-07` (temperature 1.0, default reasoning), run as 553 personas matched to the demographics of human samples of n = 284 and n = 269. A 2028-election control used 100 personas.
- **How answers were collected:** integer estimates from 0 to 100, one run per persona, with a "working-memory" window of the last 7 question–answer pairs.
- **Result:**

  | measure | GPT-5 | humans |
  |---|---|---|
  | judgments with any conjunction fallacy | 18.8% | 58.5% |
  | judgments with any disjunction fallacy | 18.7% | 57.5% |
  | double fallacies, as a share of fallacious judgments | 0.5% | 37% |
  | marginal complementarity deviation | 0.00004 | 0.248 |
  | conjunction–disjunction fallacy correlation | r = .97 | r = .03 |

  GPT-5 fits the Busemeyer et al. 2011 "more likely first" quantum model (single fallacies only, complementarity intact) better than the noisy-sampler model that fits humans.
- **Authors' limitations:**
  - One model.
  - The election outcome was known (hence the 2028 control).
  - The persona and memory manipulations are of uncertain validity.
  - The r = .97 may be a **floor effect** when fallacies are rare.
- **What we borrow:** single versus double fallacy as a discriminating signature (rule R3 in the JSON); the floor-effect caveat for any correlational evidence; and the warning that frontier models may be too coherent to give errors. That is why our pool moved to a weaker base model and harder items (DEVIATIONS D5, D6, D9).
- **How we differ:** they compare a model's aggregate pattern with humans; we predict which items one model gets wrong.

### Zhu & Griffiths 2024: "Incoherent probability judgments in large language models" (arXiv:2401.16646; CogSci 2024) `zhu2024incoherent`

- **Tested:** the eight probabilistic identities Z1–Z8, and the mean–variance relation of repeated estimates.
- **On whom:** GPT-4, GPT-3.5-turbo-1106, LLaMA-2-70b and LLaMA-2-7b.
- **How answers were collected:** verbalised probabilities for 24 event pairs (weather and politics) at T = 0 and T = 1, with 5 repeats at T = 1.
- **Result:**
  - Deviations follow the human pattern, growing with the imbalance of positive and negative terms in each identity.
  - The mean–variance relation is an inverted U.
  - Larger models are more coherent, but none is fully coherent.
  - The authors favour the Bayesian-sampler account over probability-plus-noise. Numbers are reported in figures only.
- **Authors' limitations:** few event pairs, and verbalised elicitation.
- **What we borrow:** the identity battery and the mean–variance diagnostic, as *classical* noise models that any quantum reading of LLM incoherence must outperform.
- **How we differ:** same as Wolf et al.

### Measurement critiques: Tjuatja et al. 2024 (TACL) `tjuatja2024llms`; Dominguez-Olmedo, Hardt & Mendler-Dünner 2024 (NeurIPS) `dominguezolmedo2024questioning`; McCoy et al. 2024 (PNAS) `mccoy2024embers`

- **Tjuatja et al.:**
  - Five survey response biases (acquiescence, allow/forbid, response-option order, opinion floating, odd/even scale) plus three placebo perturbations.
  - Nine models, letter answers sampled 50 times at T = 1.
  - No model matches humans on all biases, and all shift significantly under the placebos.
  - Their "order" is answer-option order, not question order.
- **Dominguez-Olmedo et al.:**
  - 43 models answering 25 ACS questions, with renormalised next-token probabilities.
  - Every model shows a strong "A-bias". Once option order is randomised, answers drift toward uniform; even GPT-4 is closer to the census than to uniform on only 6 of 25 questions.
- **McCoy et al.:** GPT-3.5 and GPT-4 accuracy tracks the probability of the input and output text (shift cipher: 51% vs 13% for high- vs low-probability outputs).
- **What we borrow:**
  - Placebo rewordings and randomised labels as controls for any order-effect claim.
  - A uniform baseline.
  - Low-frequency twins of famous items.
- **How we differ:** these are critiques of the instrument, and we adopt them rather than contest them.

---

## What is established

These are findings we can build on without re-arguing them.

1. **Human question-order effects are real, and their joint structure is constrained.** Across about 70 datasets the QQ equality holds to within sampling error whenever nothing intervenes between the questions (Wang et al. 2014). It fails, as predicted, when information intervenes (Rose/Jackson). This regularity is not implied by order effects themselves, and it is the strongest a priori success of the quantum-cognition programme.
2. **Human conjunction fallacies are robust in probability formats and fragile in frequency formats.** 85–90% of people commit them in ranking tasks; 0–25% in frequency formats (Tversky & Kahneman 1983; Fiedler 1988; Hertwig & Gigerenzer 1999). When people judge real events with known marginals, double fallacies are essentially absent (Yearsley & Trueblood 2018).
3. **Classical Markov models cannot produce violations of the law of total probability, by construction.** Pothos & Busemeyer 2009 prove that the unknown case is always a convex mixture of the known cases. Anything that does violate LTP needs a different mechanism, but not necessarily a quantum one.
4. **LLMs depart from classical probability, in model-dependent ways.** Departures appear in identities (Zhu & Griffiths 2024; Beuria 2026), in the law of total probability, and in direction (Wolf et al. 2026). The strongest recent model tested (GPT-5) is close to coherent, with few fallacies, almost all single, and intact complementarity (Imannezhad et al. 2026).
5. **LLM "response distributions" are fragile instruments.** They shift with labels and option order (Dominguez-Olmedo et al. 2024; Tjuatja et al. 2024), saturate under forced binary choice (Kang 2026), and on famous vignettes are contaminated by training data (Binz & Schulz 2023; McCoy et al. 2024). Any order-effect or CHSH claim about an LLM needs label counterbalancing, a dispersion check, and novel twins.

## What is contested

1. **Whether order effects can select a quantum account.** On the current evidence they cannot do it alone.
   - QQ satisfaction is reproduced exactly by a classical symmetric-repetition mechanism (Kang 2026, Prop. 4). Beuria (2026) finds that "the order data do not independently select a quantum account", because an order-invariant classical joint does as well.
   - Boyer-Kassem et al. (2016a) show that the datasets satisfying QQ violate Grand Reciprocity. Only degenerate, higher-dimensional quantum models survive, and their extra dimensions need independent justification.
   - Busemeyer and colleagues reply that realistic models are multi-dimensional, so the GR test targets toy versions, and that "dimensionality is not a free parameter."
   - Our position: QQ is a good *necessary* check and a poor *selector*. Selecting a quantum account needs a prediction that an equally constrained classical model cannot make (per-item magnitudes predicted from a fixed state, as in Experiment 3; the inequality R2 alone separates quantum only from static classical accounts), or a structure that classical models forbid outright, as with LTP violations under Markov dynamics.
2. **Whether projective measurement is the right model at all.** Order effects plus response replicability are incompatible with projective measurement (Khrennikov et al. 2014). The proposed fix, non-projective quantum instruments (Ozawa & Khrennikov 2020, 2021; Fuyama et al. 2025), can both satisfy and violate QQ, so it gives up the QQ equality's predictive edge. Only one experiment has tested replicability (Busemeyer & Wang 2017), and its interpretation is disputed.
3. **Whether Bell/CHSH violations in concept combination show entanglement.** Aerts and colleagues read CHSH > 2 as non-Kolmogorovian structure, in humans (2.42) and now in LLMs (2.12–4). Dzhafarov & Kujala hold that when marginals shift between contexts, as they do strongly here, CHSH > 2 is explained by direct influences. Our recomputation finds every published Animal Acts dataset non-contextual under the corrected bound, and LLM values above Tsirelson's bound require signalling. We think the Bose–Einstein word-statistics result is a separate question that our work does not bear on.
4. **Whether quantum models are too flexible.** The BBS commentators (Tentori & Crupi; Kaznatcheev & Shultz; Rakow; Newell et al.) argue that the choice of compatibility, dimension, state placement and processing order, such as "more likely first", leaves the framework able to fit opposite patterns. The authors answer that these choices are empirically constrained. This is the critique our classical-twin design is built to answer.
5. **Whether LLM probability incoherence is quantum-like or noise-like.** Zhu & Griffiths favour a Bayesian sampler. Imannezhad et al. find GPT-5 fits a quantum "more likely first" model better than a noisy sampler, but warn of a floor effect. Beuria finds no single framework fits. Wolf et al. show a classical decomposition effect with a systematic direction.

## What this project adds

1. **States built from the model's own deliberation.**
   - Every quantum-cognition model above posits a state vector and fits its angle to aggregate answers. Here the state is *constructed per item*, before any outcome is seen:
     - one qubit per claim in the model's own explanation;
     - amplitudes from the claims' confidence;
     - couplings from a judged relation web.
   - This removes the state-placement freedom the BBS commentators objected to, because nothing about ψ is tuned to the answer.
   - The caveat is ours to state (DEVIATIONS D1–D3): the claims come from the model's visible explanation, which may be a tidied account of its deliberation rather than the deliberation itself.
2. **Prediction of errors against an equally tuned classical twin.**
   - The literature tests identities, such as QQ, CHSH, LTP and conjunction bounds, on aggregate frequencies. We test whether a per-item structure predicts per-item *errors* on held-out items.
   - The comparator is the same graph, couplings and fields with amplitudes and interference removed: arm F, and the learned twin F2 with the same parameter budget in v2.
   - This is the comparison the flexibility critique asks for, and its answer so far is negative. On the hard pool, the entangled readout (AUROC 0.55) did worse than the unentangled circuit (0.68), a shuffled web (0.65) and plain contradiction counting (0.64), and H2 failed.
   - We report that as a result, not an obstacle. A framework that can lose a fair, pre-registered comparison is more informative than one that is only ever fitted.
3. **Hardware certification.**
   - Behavioural Bell tests cannot separate "the system holds an entangled state" from "the marginals shift with context". We can, because we know the state we built.
   - The pre-registered negativity witness certified entanglement of the encoded contention pairs on `ibm_fez` for 3 of 3 items: N = 0.147, 0.063 and 0.067, all with lower 95% bounds above 0, with or without readout mitigation, for 44 QPU seconds.
   - This certifies the *encoding*, not its usefulness. The two questions are now answered separately: the entanglement is physically there, and on the simulator it does not help.
4. **The window.**
   - The window is the project's visual display of a single run.
     - Each of the model's contentions is a point in a point cloud.
     - Brightness is its amplitude (how strongly it is held) and hue is its phase (which way it leans).
     - Dashed links show which contentions are entangled.
     - A rewindable timeline steps through encoding, evolution and collapse to the readout.
     - Every run is archived.
   - Nothing like it exists in the work above. Quantum-cognition models are fitted to aggregate answer frequencies, so there is no per-item state to look at. The LLM studies observe only answers or probabilities.
   - Here the state behind each judgment is constructed, simulable exactly at 5–16 qubits, and recorded. A reader can watch a contradiction pair settle into opposed camps, or fail to, on the very item the model got wrong, and compare that run with the classical twin's.
   - The archive of runs is a dataset that cannot be rebuilt from the outside. Every arm's readout, including the raw counts, is already archived as JSON in `results/`.
   - The display itself is designed (v1 proposal, Stage 3) but not yet built.
   - Its scientific use is diagnostic rather than evidential. It shows *where* the entangling step moves probability mass on items that the classical contradiction count flags and the entangled readout misses (Stage 2, run 2). That is the most useful thing to look at next, given H2's result.

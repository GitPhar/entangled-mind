# Clonable minds: macrorealism holds for a language model by construction

Written 2026-11-04 (America/Denver). This is the theory note for gold-map direction 9 (`paper/gold-map.md`). It is docs only: nothing was run for it. Its numbers are copied from `results/exp5-run-1.md`, `results/exp5-run-2.md`, `results/exp4-run-3.md`, `results/gm9-nsit.md` (gold-map direction 9's pre-registered NSIT analysis, D34) and the per-item values archived in `results/exp5-run-1.json`; any tally of archived values that the results files do not themselves print is marked as such.

## 1. The claim

A language model served through a stateless API has, at every turn of a conversation, a complete state that is a classical string: the conversation so far. Everything the next response depends on is in that string, apart from the sampler's random draw, and the string can be copied exactly.

Three consequences follow, and the rest of this note argues them.
1. **Macrorealism holds by construction.** The model is in a definite state at every turn, and there is an ideal non-invasive measurement of it: copy the context and ask the copy.
2. **Every violation is invasiveness.** Any Leggett–Garg, no-signalling-in-time (NSIT), total-probability or question-order (QQ) effect found in a sequential protocol on such a model can come only from the measurement changing the state (the question, and the recorded answer, are appended to the context). It can never come from the absence of a definite state.
3. **The two parts of invasiveness come apart.** In people and in quantum systems, "the question disturbs" and "the answer is remembered" cannot be separated: no-cloning forbids copying a quantum state, and a person who has answered remembers answering. In a language model they are separated by editing the transcript: keep the question and delete the answer, keep the question and plant a different answer, or ask on a copy.

The first is close to a definition. The second is a short argument. The third is the reason the note is worth writing: it turns the quantum-cognition programme's central confound into an experimental variable.

## 2. What a test of macrorealism needs

**The assumptions.** Leggett and Garg (1985) derived their inequalities from two assumptions:
> "(A1) Macroscopic realism: A macroscopic system with two or more macroscopically distinct states available to it will at all times be in one or other of those states. (A2) Noninvasive measurability at the macroscopic level: It is possible, in principle, to determine the state of the system with arbitrarily small perturbation on its subsequent dynamics."

Later statements add a third, **induction**: "the outcome of a measurement on the system cannot be affected by what will or will not be measured on it later". That wording is the (A3) of Emary, Lambert & Nori (2014, §2.1). Leggett (2002) states the three as macrorealism *per se*, non-invasive measurability and induction.

**No-signalling in time (NSIT).** Kofler and Brukner (2013) give the weaker, statistical condition: "A measurement does not change the outcome statistics of a later measurement". Formally, P(B) = Σ_A P(A, B) when A is measured first.
- NSIT "can be viewed as a statistical version of non-invasive measurability".
- Macrorealism implies NSIT, which is the logic of this note: a system that violates NSIT under a measurement is either not macrorealist, or is measured invasively.
- They note that Bohmian mechanics is "macrorealistic per se, invasive, and signaling in time". That is the precedent for the case argued here: a definite state, measured invasively.

**The clumsiness loophole.** That either-or is the problem every physical test faces. Wilde and Mizel (2012) state it: "a violation of the inequality can only show that the system is either (i) non-macrorealistic or (ii) macrorealistic but subjected to a measurement technique that happens to disturb the system." They add that "macrorealism does not assert that it is impossible to affect a physical system by measurement but merely that it is possible for a sufficiently adroit measurement to avoid doing so."
- Their remedy is a control. A measurement counts as ε-adroit if performing it changes the statistics of the others by at most ε, checked statistically.
- Emary, Lambert & Nori say the same: violations "can be ascribed to the unwitting invasivity of the measurements". Classical models with invasive measurements reproduce the quantum pattern (Montina's four-state model). And "violations of a LGI cannot strictly-speaking be taken as evidence of quantum mechanics, but rather evidence of the absence of a description along the lines of (A1-3)".
- Maroney and Timpson (2014) separate *ontic* non-invasiveness from operational non-disturbance ("Ontic noninvasiveness implies operational non-disturbance, but not conversely"). They show that an LG violation refutes only one of three kinds of macrorealism.

**The two horns are confounded in physics and in people.** In physics, a measurement cannot be shown to be non-invasive except statistically, by control experiments. In people, there is no control at all for the measurement having been made: the person was asked, and knows it.

## 3. The state of a language model

**What the state is.** For a model reached through the Anthropic Messages API, as in every run in this project:
- **The API is stateless.** Each request carries the whole conversation, and the server keeps nothing between requests that changes the response distribution. (Prompt caching changes cost and latency, not the distribution.)
- **The weights are fixed** for a given model id over the time of an experiment.
- **The response distribution is a function of the context.** Given the system prompt, the conversation so far and the sampling settings, the distribution over the next response is fixed. Only the draw from it is random. The Messages API offers no seed, so the draw cannot be repeated, but the distribution can be estimated to any precision by asking copies.

So the state at turn t is c_t, a string. The observable "the answer to question Q, in format F" is a random variable whose distribution P(· | c_t, Q, F) is fixed by c_t.

**There is no free evolution.** Between two questions the context does not change on its own. It changes only when the experimenter appends a turn and the model's answer is appended after it. In a chain such as experiment 5's S₁ → S₂ → S₃ → S₄ → M, the "time evolution" between the measurement of S₂ and the measurement of S₃ is nothing but the S₃ question itself. The dynamics and the measurements are the same events. (When a protocol wants evolution between measurements, it has to supply it as text, as experiment 5's K-chains do with the new claims S₃ and S₄ after the choice.)

**An ideal non-invasive measurement exists.** To read the observable Q at turn t without disturbing the conversation, send c_t + Q to a copy and discard the copy. The original conversation c_t is untouched: no later answer can depend on that reading. This is the measurement the Leggett–Garg programme needs and cannot have in physics.
- It is *ontically* non-invasive in Maroney and Timpson's sense, the strongest of their notions: the original is not merely statistically undisturbed, it is untouched.
- Wilde and Mizel's adroitness condition can be checked exactly, by comparing a conversation with and without the extra read, rather than estimated.

### 3.1 The proposition

> **For any set of questions read on copies of one context, every Leggett–Garg inequality, every NSIT condition, the law of total probability and the QQ equality are satisfied, and every order effect is exactly zero.**

*Argument.* Read on copies, the answers to questions Q₁, …, Qₙ at context c are independent draws from P(· | c, Q₁), …, P(· | c, Qₙ). Their joint distribution is the product of the marginals, and it does not depend on which other questions were read or in which order. A single joint distribution over all the outcomes therefore exists, with every measured marginal as its marginal. By Fine's theorem that is exactly what a classical hidden-variable model needs, and every inequality derived from such a model holds. NSIT holds because reading Q₁ on a copy does not change the distribution of Q₂. The order effect P(A then B) − P(B then A) is zero because the two reads do not see each other. The QQ equality holds trivially, for the same reason. This is the content of "MR ⇒ NSIT" (Kofler & Brukner 2013, Table I) for the special case where a non-invasive measurement can actually be carried out.

When the reads are spread over several turns of one conversation, the same argument applies turn by turn: copy each c_t before reading it.

### 3.2 The corollary

> **In a sequential protocol, where each question and its answer stay in the context of later questions, any violation measures how the protocol's measurements change the state. It is never evidence that the state was indefinite.**

The violation is the difference between the sequential distributions and the clone-read distributions, which satisfy everything. The only thing that differs between the two protocols is that, in the sequential one, the measurement record is written into the state. In Leggett and Garg's terms, macrorealism per se cannot fail, so a violation can only be a failure of non-invasive measurability. That is the "clumsiness" explanation which physics tries to exclude. For a language model it is not a loophole to be closed; it is the only explanation available.

### 3.3 Subtleties

- **Sampling is random, so the seed belongs in the state.** Kofler and Brukner (2013, fn. 45) are explicit. A macrorealist may allow stochastic *evolution*, but must hold that each individual outcome is determined by the complete state at the time of measurement. So the ontic state is λ = (context, sampler state), not the context alone.
  - With λ so defined, each answer is a definite function of λ, and macrorealism per se holds in the strict sense.
  - With a fixed seed, a copy would return *the* answer, not just a sample of it.
  - The Messages API exposes no seed. A clone read therefore recovers the answer's *distribution* exactly, not the particular draw. That is enough for every result in §3.1, which concern statistics.
  - Even without the seed, the clone-read model is factorisable in Kofler and Brukner's sense (their eq. 5, with ρ over contexts and stochastic response functions). It therefore satisfies NSIT and every LG inequality.
  - Aaronson (2013, §5.3) makes the same point about a machine with a random-number source: its responses "would still be probabilistically predictable" by anyone with a copy.
- **The question's wording and format are part of the observable.** "Rate 0–100, 0 = false" and "rate 0–100, 0 = true" are two observables, not one observable read two ways. Experiment 5's 37-point gap between them (33.8 against 71.3) is therefore not a macrorealism question at all. Whether one credence underlies all formats is gold-map direction 3, a question about the *structure* of P(· | c, Q, F) across F, not about definiteness. Direction 3's six-format run (`results/gm3b-format-invariance.md`, D38) found that it does not, for this model on its own contested claims: format-specific credences beat one credence per claim on held-out repeats for 86% of claims. The answer depends on the observable, and that is fully compatible with a definite state.
- **Induction (the arrow of time) holds trivially for the original conversation.** A later turn cannot change an earlier answer: the earlier answer is fixed text by the time the later question is asked. Editing a transcript is an intervention on *later* states, not on earlier outcomes. Two things in an experiment's design still need care, the analogue of the freedom of choice that Kofler and Brukner attach to induction:
  - which question is asked when must not depend on the model's earlier answers;
  - branches that share a prefix are correlated through that prefix and must be analysed as such.
- **Hidden reasoning.** With thinking disabled, as in all our runs, the context is the visible transcript. With extended thinking, the thinking blocks become part of the context. They are returned to the client (in full, summarised, or as an opaque encrypted block) and sent back with the conversation, so the state is still a copyable string, though the experimenter may not be able to read or edit all of it. A system that kept conversation state on the server, out of the client's reach, would lose the experimenter's ability to clone. It would not lose definiteness.
- **Server-side numerical nondeterminism** (for example from batching) adds noise to P(· | c). It carries no memory from one request to the next, so it does not affect the argument.

## 4. Taking invasiveness apart

In a sequential protocol, appending "question Q, answer a" to the context can change later answers through three channels:

| channel | what changes the later answer |
|---|---|
| **L, length and turn** | that there is one more turn, of some length, whatever it says |
| **Q, question exposure** | that Q was asked: its content is now in context |
| **R, answer record** | that the model's own answer a is now in context |

Editing the transcript isolates them:

| condition | context before the later question | channels present |
|---|---|---|
| clone read | the original context only | none |
| filler | a content-free turn of matched length | L |
| redacted | Q, with the answer replaced by "[rating recorded]" | L, Q |
| planted | Q, with the answer replaced by a value the experimenter chooses | L, Q, and a record the model did not produce |
| shown | Q and the model's own answer, as in an ordinary conversation | L, Q, R |

With people, only the last row exists. With a quantum system, the clone row does not exist, and "redacted" has no meaning: the measurement's effect on the state is not a record that can be deleted. A language model offers every row.

## 5. The first measurements

The project has two sets of data that already bear on this, both from experiment 5 and both now analysed under direction 9's pre-registration (`results/exp5-run-1.md`; 40 items, 10 conversations per item and chain type, base model `claude-haiku-5-5`, thinking off).

**The omission chains (X₁–X₄ against O₁): an NSIT test on each claim question.**
- X_k is the O₁ chain with sub-question S_k left out. Compare the main rating's distribution after O₁ with its distribution after X_k. Marginalising over the answer to S_k simply means ignoring it, so this comparison is the NSIT condition for S_k. A difference measures the invasiveness of asking S_k, with the channels Q and R together.
- **Result** (gold-map direction 9, pre-registered before analysis: `experiments/gm9-nsit.md`, D34; `results/gm9-nsit.md`; anchor-(a) conversations only):
  - Asking S_k moves the final rating by a mean |d| of **8.7 points**, against 3.9 expected from the permutation null. The shift is at least 10 points in 19% of the 160 item–claim cells (Holm p = 0.001).
  - The mean signed shift is +0.7 [−3.7, +4.3]. Asking moves ratings a lot, in directions that differ from item to item, not uniformly up or down.
- **The same analysis on four other families:**
  - **One sub-question just before the main question** (N1M: 12.4 against 2.6).
  - **The main question just before a sub-question** (N1S: 15.7 against 3.1; +8.0 [+2.7, +13.3] signed).
  - **All four sub-questions against none** (N3: 22.6 against 5.2).
  - **Asking the main question at the start of the chain** (N5: 16.0 against 6.1; −10.1 [−18.2, −2.9] signed).
  - All are invasive.
  - The two single-question families replicate on the separate run-2 conversations (`results/exp5-run-2.md`): 17.4 against 2.9 and 15.7 against 2.3.

**The Kvam contrast (K₁ against K₀): an NSIT test on an intermediate choice, with the length channel controlled.**
- K₁ inserts a binary choice on the main question ("Answer yes or no") after S₂, and K₀ inserts a one-word filler of matched length. Both then continue with S₃, S₄ and M. The contrast holds L fixed and measures Q and R for a choice about the main question itself.
- **Result:** the final rating's folded confidence differs by Δ_K = +0.29 points [−1.12, +1.65]. The mean total-probability residual is +0.58 points.
- **Per item** (my tally of the archived per-item values, not printed in the results file): the two-sample KS test of K₁ against K₀ rejects at p < 0.05, uncorrected, on 5 of 40 items, against 2 expected by chance. The median absolute total-probability residual is 3.5 points, which is the size of the sampling error of a 10-conversation cell mean at these spreads.
- **Direction 9's pre-registered version of the contrast** (family N4, anchor (a) only) gives the same answer. Mean |d| is 5.0 points against 3.3 from the null, p = 0.16: **no detectable invasiveness** at 5 conversations per arm.
- **Reading:** at this resolution, no difference was detected between committing to a yes/no answer on the main question, with that answer in the context, and a filler turn. That is the one family with no detectable effect. It is all the more striking next to N5: asking the same main question first *as a 0–100 rating* lowers the final rating by 10 points. Whether the difference lies in the format of the earlier question or in the number it leaves in the record is a transcript-editing question (§4).

**Two related measurements.**
- **Replicability.** Asked the main question first and again after the four claims (chain MF), the model lands within 5 points of its first answer 84% of the time. The record of its first answer is in the context. Whether the agreement comes from that record (R) or from a stable judgment is exactly what the redacted condition would settle (Khrennikov et al.'s response-replicability problem, §7).
- **The first transcript-editing measurement** (gold-map direction 2, pre-registered before any call: `experiments/gm2-self-conditioning.md`, D37; `results/gm2-self-conditioning.md`; added 2026-11-04 after this note was first committed). Experiment 5's chains O1–O4 and MF were re-run on 10 items with the model's earlier ratings shown, redacted or planted ±15 points in its own turn.
  - **Channel Q is invasive.** With every earlier answer redacted, the order of the questions still changes the final rating. The ratio of redacted to shown order effect is 1.91 [0.92, 4.90], above the pre-registered 0.5.
  - **Channel R is invasive.** The final main rating follows a planted first main rating at 1.27 [0.70, 2.14] points per point.
  - **Replicability depends on the record.** MF agreement within 5 points is 81% shown and 23% redacted, against 74% between fresh first ratings. Khrennikov et al.'s response-replicability effect, in this model, depends on the R channel.
  - **Caveats.** The redaction placeholder is an unusual turn that may itself add variance (the redacted order effect is larger than the shown one), and two items drive much of it.
  - **On all 40 items** (D45, `results/gm2b-self-conditioning-40.md`, `758609a`), the second caveat is resolved and the first is narrowed. Channel Q: R = 1.23 [0.75, 2.02], still above 0.5; 0.99 on the 30 new items and 0.99 without the two items; 82% of items carry it; the within-order spread is the same shown and redacted (SD 5.1 against 5.4), so the placeholder adds no noise, though it may still shift ratings. Channel R: b_MF 0.85 [0.65, 1.13]. Replicability: 86% shown against 36% redacted. On these items the Q channel alone produces an order effect of about the same size, but the R channel changes its pattern (shown and redacted profiles correlate 0.32), and R raises replicability.
- **A record the model did not make.** In experiment 4 run 3 (`results/exp4-run-3.md`), a first rating presented as *another person's* estimate was accepted in 0% of conversations in 17 of 32 item-orders, and on three Linda-family items pushed the rating the other way. An external record is not treated like the model's own. The planted condition in §4, which puts a value in the model's own turn, is the untested case. *Since tested* (bm1, D44; D47, `e2c3b90`): the same values planted in the model's own turn pull its re-rating (uptake 0.71, 0.44 and 0.21 at 10, 30 and 60 points away), while another person's show no detectable uptake (mean +0.02); own − other is +0.46 [+0.21, +0.84], and own uptake did not fall after three filler turns. The R channel looks source-specific: a number in the model's own turn pulls the re-rating, while the same number credited to another person, under different wording, does not.

## 6. What this implies for quantum-cognition tests on language models

**The field's tests, sorted by design.** The six LLM studies that this project cites as closest to it were read in full on 2026-11-04, with one exception: Beuria's published version, for which the Research Square preprint and the author's public code were read instead. They fall into three classes. Only the first, sequential, involves a measurement before the measured judgment, so only the first is a test of anything sequential.

| class | study | what is in context when the judgment is made | what the note says the result can mean |
|---|---|---|---|
| **sequential, with the model's earlier answer in context** | Kang (2026), arXiv:2607.17219: Qwen3-4B, 18 item pairs, next-token probabilities. "Forced branching": each candidate first answer "is committed separately to the conversation history as an assistant turn" | the first question and a *committed* answer, which is in effect a planted one | the size and form of invasiveness. Kang already finds that "symmetric repetition", a classical mechanism, satisfies QQ "identically while still producing order effects" (Prop. 4), and that 17 of 18 pairs saturate |
| | Bessis, Wills, Wojciechowski, White & Pothos (2026), Behav. Sci. 16:437: GPT-4o and GPT-5.2, legal guilt ratings. In the double-rating condition "context was intentionally maintained across the two ratings" | the evidence, the intermediate question and the model's own intermediate rating | measured invasiveness. The authors call it a "measurement bias": giving an intermediate rating "systematically inflated GPT-4o's final guilt assessments" (for example 4.24 against 3.54). They name the open question as "self-conditioning or anchoring on the model's earlier output", which is exactly channel R against Q |
| **single prompt, or estimates from separate prompts** | Beuria (2026), Sci. Rep. (preprint read): four 7–8B open models, total probability assembled from separate fresh calls; the "order" task lists Q1 and Q2 in one prompt but asks only Q2 | the prompt only; the "earlier" question is never answered | context-dependence of one response, or incoherence across separately elicited estimates: a coherence result, not a measurement-disturbance result. (The published version's code adds a re-injected "You answered:" task; how the paper reports it was not checked.) |
| | Wolf, Kleine Buening, Krause & Mendler-Dünner (2026), arXiv:2607.15277: each subpopulation estimate is its own prompt | the prompt only | a failure of coherence across prompts ("widespread violations" of split and order consistency). This is the question of gold-map direction 3, not of macrorealism. The authors use no quantum framing |
| | Kumar, Flint, Aiello & Baronchelli (2026), arXiv:2603.23485: the priming pronoun is fixed by the experimenter "using a single prompt" | the prompt, with the prime as content | CbD-style dependence of one response on its context (19–52% of template pairs). Nothing was measured first |
| **contextuality across inputs** | Lo, Sadrzadeh & Mansfield (2025), arXiv:2412.16806: BERT, one masked input per context | the whole context, which the model reads | the dependence of outputs on context. 71% of instances are CbD-contextual, but only 0.15% are sheaf-contextual |

**What follows for each class.**
- **Sequential.** The proposition of §3 applies directly. The order effects are real, and they are invasiveness. A quantum model of them is a model of how a recorded question and answer perturb the next response. Kang's forced branching and Bessis et al.'s double rating are the two published designs that could already separate Q from R by redaction, and neither does. Bessis et al. propose a control "unrelated to guilt", which is channel L.
- **Single prompt.** Nothing is measured before the judgment, so neither macrorealism nor invasiveness is in play. Order and context effects inside one prompt are the input–output function of one stateless call. Their quantum description, where one is offered (Beuria: "sequential prompts act as measurement operations"), is a description of that function. It does not describe a state and its disturbance.
- **Contextuality across inputs.** In contextuality tests the model reads the whole context, so a classical mechanism that reads its input can produce any set of per-context distributions. Dzhafarov and colleagues already say that "(Non)contextuality per se … is a purely probabilistic concept, squarely within the classical, Kolmogorovian probability theory". They also classify dependence of an answer on a previously asked question as "a trivial sense of contextuality … We call this inconsistent connectedness". A contextual system of LLM outputs is therefore a fact about the outputs' joint structure. It is not evidence that the mechanism producing them is non-classical, or that values were indefinite. Lo et al. read contextuality as the failure of "deterministic pre-existing values". For a model that reads its context, values are fixed by the input, and the input differs between contexts.
- **No study** in the three classes discusses the model's statelessness, the copyability of its context, invasiveness or macrorealism, and none runs a fresh-context or redacted-answer control.

**For this project's tests.**
- **Experiment 3 and experiment 5's QQ block** asked one question and then another in the same conversation. Their order effects are measured invasiveness. The QQ equality, read this way, tests the *form* of the invasive update (a Lüders update with rank-one projectors gives q = 0) and not whether the judgment was definite. Single-scale q = −0.146 [−0.439, +0.137] (`results/exp5-run-2.md`) says the form is not the rank-one Lüders form, or not reliably.
- **A5, the quantum belief state of experiment 5,** applies one unitary step per question and a Lüders update per answer. Both are models of invasiveness: the first of channel Q, the second of channel R. Its primary tie with the classical twin F5 (the overall verdict is classical, re-issued in D52, because its QQ signature is contradicted on one scale direction), and its match by the dephased Markov chain D5, say that a classical model of the same invasiveness does as well.
- **None of our tests,** and none that could be run on this model in this way, could have shown that the model's judgments were indefinite before they were asked. They could only have shown that a quantum-probability model describes how asking changes them.

**What a quantum model of an LLM can still be.** It can be a compact description of how appended text perturbs the response distribution: quantum-*like* in the operational sense. That is a legitimate and testable claim, because the clone-read distributions give it a ground truth that human studies lack: the model's prediction of the undisturbed marginals can be checked against copies. The claim it cannot support, for this kind of system, is the one that motivates much of the human work: that the violations show judgments are constructed from a state with no definite values.

## 7. Why a language model is the first system where the two come apart

**Quantum systems cannot be copied.** "A single quantum cannot be cloned" (Wootters & Zurek 1982). So for a quantum system there is no clone read, and the "not asked" counterfactual exists only as a separately prepared ensemble.

**People cannot be copied, and they remember.** Aaronson (2013, §2.5) puts the contrast in terms of minds: the hope of escaping full predictability lies in whether "minds can't be copied perfectly from one physical substrate to another, as can programs on standard digital computers". The quantum states that might block copying have "a certain 'privacy'" (§3.2). A language model behind a stateless API is the clonable case. Its whole state at a turn is a program input that can be copied without limit.
- **Cognitive Leggett–Garg tests face non-invasiveness without a remedy.** Atmanspacher and Filk (2010) proposed a temporal Bell inequality for bistable (Necker cube) perception, derived from the assumption that "at each moment t the system is in one of the two states". (Their paper is paywalled. That passage, and the remark that "measurements must be as non-invasive as possible", are quoted from the authors' slides.) A perceiver who reports a percept has been measured and knows it.
- **A cautionary NSIT application.** Tressoldi, Maier, Buechner & Khrennikov (2015) report "a strong violation of NSIT in two out of three" behavioural studies. Their data, however, have no condition without the earlier measurement. The unmeasured probability "was estimated with a mean equal to 0.5 ... assuming a correct randomization". So it is not an NSIT test in Kofler and Brukner's sense. The counterfactual such a test needs is exactly what a language model supplies for free.
- **Replicability: the remembered answer.** Khrennikov, Basieva, Dzhafarov & Busemeyer (2014) set out "an unsolved problem" for quantum models of psychological measurement. Repeated questions get repeated answers (their Property 1), and standard quantum theory "can handle response replicability, but only in the way incompatible with the question order effect". They consider the reply that respondents "'merely' remember their previous answers" and set it aside as "irrelevant for our analysis". Ozawa and Khrennikov (2021) model the combination with quantum instruments: after A, B and A again, "Alice would definitely repeat her original answer." In a language model, memory is not an explanation to be set aside. It is a channel (R in §4) that can be switched off by deleting the answer from the transcript, while the question stays.

**So a language model is the first judging system in which "the question disturbs" and "the answer is remembered" can be pulled apart.** For a quantum system the first cannot be separated from the measurement, and the second does not apply. For a person the second cannot be switched off. For a language model, both are text in a copyable string, and each can be kept, deleted or replaced on its own.

**What is new here, and what is not.**
- Kang (2026) already edits LLM transcripts. His "forced-branch protocol" commits each candidate answer to the conversation history, as "the operational analogue of the state update", and he shows that "classical repetition can reproduce the equality exactly". He does not draw the macrorealism or invasiveness conclusion.
- Tull and Ozawa (2026, arXiv:2604.08604; abstract only) show that sequential decision data in general admit a classical instrument model with state disturbance.
- I found no prior statement that an LLM's copyable state makes macrorealism hold by construction, so that its LG, NSIT and QQ violations can only be invasiveness. The searches covered Leggett–Garg, macrorealism, NSIT and no-cloning with language models and neural networks.

## 8. Tests that follow

1. **The NSIT analysis of the archived experiment 5 data ($0): done** (D34, `results/gm9-nsit.md`). Asking is invasive in 5 of 6 families; the midway choice is not. Section 5 reports the numbers.
2. **The replay design (gold-map direction 2): done** (`results/gm2-self-conditioning.md`; §5). Both Q and R are invasive. It was pre-registered overnight (`experiments/gm2-self-conditioning.md`, D37) with four of §4's rows: shown, redacted, planted-high and planted-low (±15 points, in the model's own turn), on 10 experiment-5 items and one scale direction. Redacted against shown isolates R; planted against shown tests whether the record's *value* steers the later rating. The clone-read and filler rows are already covered by the "not asked" arms of direction 9 and by K₀.
3. **A clone-read control for any LLM order-effect claim.** It costs one extra call per question and gives the undisturbed marginals that every inequality in §3.1 compares against.

## 9. What would make this note wrong

- A server that keeps state between requests that the client cannot see or copy. Then the experimenter's clone is not a clone.
- Weights that change during an experiment.
- A model that is not reached through its context alone: for example, one with a persistent memory feature or online learning between calls.

None of these is known to apply to the runs in this project; the server's statelessness is taken from the API's documented behaviour, not tested.

## References

All were read in full on 2026-11-04 unless marked otherwise. Quotations are from the full texts.

- Aaronson, S. (2013). The ghost in the quantum Turing machine. arXiv:1306.0159. In S. B. Cooper & A. Hodges (Eds.), *The Once and Future Turing* (Cambridge University Press, 2016).
- Atmanspacher, H., & Filk, T. (2010). A proposed test of temporal nonlocality in bistable perception. *Journal of Mathematical Psychology, 54*(3), 314–321. doi:10.1016/j.jmp.2009.12.001. [Paywalled; read only through the authors' slides.]
- Bessis, T. F., Wills, A. J., Wojciechowski, B. W., White, L. C., & Pothos, E. M. (2026). Legal decision biases in GPT: A comparison with human judgment. *Behavioral Sciences, 16*(3), 437. doi:10.3390/bs16030437.
- Beuria, J. (2026). Emergent non-classical probabilistic structure in large language models under contextual modulations. *Scientific Reports*. doi:10.1038/s41598-026-65824-7. [Preprint rs-9326649/v1 and public code read; published version not accessible.]
- Dzhafarov, E. N., Kujala, J. V., & Cervantes, V. H. (2016). Contextuality-by-Default: A brief overview of ideas, concepts, and terminology. *LNCS 9535*, 12–23. doi:10.1007/978-3-319-28675-4_2.
- Dzhafarov, E. N., Zhang, R., & Kujala, J. (2016). Is there contextuality in behavioural and social systems? *Phil. Trans. R. Soc. A, 374*, 20150099. doi:10.1098/rsta.2015.0099.
- Emary, C., Lambert, N., & Nori, F. (2014). Leggett–Garg inequalities. *Reports on Progress in Physics, 77*, 016001. doi:10.1088/0034-4885/77/1/016001.
- Kang, P. (2026). Auditing question-order effects in large language models with the QQ equality: Mechanism characterization and a saturation caveat. arXiv:2607.17219.
- Khrennikov, A., Basieva, I., Dzhafarov, E. N., & Busemeyer, J. R. (2014). Quantum models for psychological measurements: An unsolved problem. *PLoS ONE, 9*(10), e110909. doi:10.1371/journal.pone.0110909.
- Kofler, J., & Brukner, Č. (2013). Condition for macroscopic realism beyond the Leggett-Garg inequalities. *Physical Review A, 87*, 052115. doi:10.1103/PhysRevA.87.052115.
- Kumar, S., Flint, A., Aiello, L. M., & Baronchelli, A. (2026). Failure of contextual invariance in large language models. arXiv:2603.23485.
- Kvam, P. D., Pleskac, T. J., Yu, S., & Busemeyer, J. R. (2015). Interference effects of choice on confidence. *PNAS, 112*(34), 10645–10650. doi:10.1073/pnas.1500688112.
- Leggett, A. J. (2002). Testing the limits of quantum mechanics: Motivation, state of play, prospects. *Journal of Physics: Condensed Matter, 14*, R415. [Cited for the three-postulate wording, as quoted by Kofler & Brukner; not read directly.]
- Leggett, A. J., & Garg, A. (1985). Quantum mechanics versus macroscopic realism: Is the flux there when nobody looks? *Physical Review Letters, 54*, 857–860. doi:10.1103/PhysRevLett.54.857. [Assumptions quoted as reproduced, identically, by Maroney & Timpson and by Emary et al.]
- Lo, K. I., Sadrzadeh, M., & Mansfield, S. (2025). Quantum-like contextuality in large language models. arXiv:2412.16806.
- Maroney, O. J. E., & Timpson, C. G. (2014). Quantum- vs. macro- realism: What does the Leggett-Garg inequality actually test? arXiv:1412.6139.
- Ozawa, M., & Khrennikov, A. (2021). Modeling combination of question order effect, response replicability effect, and QQ-equality with quantum instruments. *Journal of Mathematical Psychology, 100*, 102491. doi:10.1016/j.jmp.2020.102491.
- Tressoldi, P. E., Maier, M. A., Buechner, V. L., & Khrennikov, A. (2015). A macroscopic violation of no-signaling in time inequalities? How to test temporal entanglement with behavioral observables. *Frontiers in Psychology, 6*, 1061. doi:10.3389/fpsyg.2015.01061.
- Tull, S., & Ozawa, M. (2026). Quantum-like cognition in process theories: An analysis. arXiv:2604.08604. [Abstract only.]
- Wilde, M. M., & Mizel, A. (2012). Addressing the clumsiness loophole in a Leggett-Garg test of macrorealism. *Foundations of Physics, 42*(2), 256–265. doi:10.1007/s10701-011-9598-4.
- Wolf, P., Kleine Buening, T., Krause, A., & Mendler-Dünner, C. (2026). Partition, prompt, aggregate: Statistical self-consistency in language models. arXiv:2607.15277.
- Wootters, W. K., & Zurek, W. H. (1982). A single quantum cannot be cloned. *Nature, 299*, 802–803. doi:10.1038/299802a0. [Citation confirmed; not re-read.]

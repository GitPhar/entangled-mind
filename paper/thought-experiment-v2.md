# The Entangled Mind: A Thought Experiment

### A Plain-Language Companion to the Research Paper

**Sean Pharris**
Independent Researcher, Colorado Springs, Colorado
Version 2, November 3, 2026 (version 1: October 25, 2026)

**Author note.** This is the plain-language companion to the research paper of the same title. Version 1 described an experiment that had not been run. This version says what happened when we ran it, for a reader with no background in physics, psychology or machine learning.

Every result quoted here comes from the project's published result files. Anything not yet measured is marked [PENDING]. Technical detail, pre-registered criteria and references are in the paper.

Correspondence: seanm.pharris@gmail.com.

---

## Abstract

Do machines need quantum minds? Today's AI systems judge by adding up separate beliefs. Decades of psychology experiments suggest people do something stranger, as if their beliefs were tangled together, so that asking about one changes another. Physics has an exact word for things tangled together that way: *entangled*.

We took the competing considerations behind an AI's answers, built them into a single entangled state, let it settle, and read off a judgment. Then we tested whether that judgment could tell when the AI was wrong better than simpler methods could. It could not. A plain count of how much the AI's own reasons contradicted each other did better.

We also showed, on a real IBM quantum computer, that the entangled states we built really were entangled. So the entanglement is real, but in this design it does not help. This document explains what we built, what happened, what it means, and what we are testing next.

---

## The question

Every AI system that exists today reasons the way a careful accountant does. It holds a list of beliefs, gives each one a weight, and adds them up. That is called classical probability.

The question in one line: if a machine's beliefs were *entangled* instead of listed, would it judge better, and in particular, would it know better when it was about to be wrong?

Version 1 of this document asked that question. This version has an answer for the first design we tried: **no**. The rest of this document is about why that answer is still worth having, and what we are trying next.

---

## How a machine judges today

Ask a modern AI whether a tomato is a vegetable. It will weigh some considerations:
- botanically, a tomato is a fruit;
- in cooking it is treated as a vegetable;
- a court once ruled it a vegetable for tax purposes;
- the person is probably asking about cooking.

Each of these is a belief with a strength, and the AI combines them into an answer.

Version 1 worried about what cannot happen in that picture. "It is a fruit" and "it is a vegetable" conflict, but an accountant-style system can only weigh them, never let them collide. Two beliefs that flatly contradict each other and two that mildly agree can produce the same lukewarm number. The hope was that an entangled version would make that conflict visible.

---

## How a person judges

In a famous experiment, people read about a woman named Linda, outspoken and politically active. They were asked which was more likely: that Linda is a bank teller, or that Linda is a bank teller who is active in the feminist movement. Most people, 85 to 90 percent in the original studies, chose the second. That is logically impossible: a more specific description can't be more likely than a general one.

Ask people two questions in one order, ask another group the same questions in the other order, and the answers change. In a 1997 Gallup poll, Bill Clinton was rated honest by 50% when asked about first and 57% when asked about second.

Around 2009 a group of psychologists showed that these effects match the mathematics of quantum physics surprisingly well. They did not claim the brain is a quantum computer; they claimed the *shape* of human judgment matches the shape of quantum states. This field is called quantum cognition.

---

## What entanglement means here

Normally, if you have three things, you can describe each one on its own, and the description of all three is just the three descriptions side by side. An entangled set of things has no such description. There is one state for the whole, and the parts do not have states of their own. Ask about one part and you have, in a sense, asked about the whole.

On the classical side, three beliefs are three numbers. On the entangled side, three beliefs are one state with 8 parts, and sixteen beliefs are one state with 65,536 parts. None of those parts belongs to any single belief.

---

## What we actually built

Two things changed from the plan.

**First, where the beliefs come from.** Version 1 planned to read the AI's hidden "thinking". The AI provider's safety system declined that design, twice, and we chose to redesign rather than work around it. So now the AI answers each question with a short written explanation of the considerations for and against, and the beliefs come from that explanation. This means our results are about the reasons the AI *writes down*, which may be a tidied-up version of how it actually got there.

**Second, the bar for success.** Version 1 compared the entangled version with two controls. The final design added a third, and it is the one that matters most: a plain count of how strongly the AI's stated reasons contradict each other, with no quantum anything.

For each question, step by step:

1. **Collect the reasons.** The AI (Anthropic's Claude Haiku 5.5) answers and briefly explains itself. A second AI lists the separate claims in that explanation, with how confident each one is and which way it leans.
2. **Map the relations.** A third AI judges every pair of claims: support, contradict, or unrelated.
3. **Build one state.** Each claim gets one qubit, set by its confidence and its lean. Every related pair is then linked with an entangling gate, so the claims stop being separate and become one state.
4. **Let it settle.** The state evolves briefly under the pull of its own relations: supporting claims are drawn together, contradicting ones apart.
5. **Ask the question.** Measure the state 1,000 times in a "yes"-oriented way. The result is a judgment, a confidence, and a **conflict score**: how much of the outcome splits into two strongly opposed camps.
6. **Run the controls.** The same thing again:
   - with the entangling gates removed;
   - with the relations scrambled;
   - with no quantum part at all, just counting contradictions.

   Later we added three more comparisons:
   - a **classical twin** that uses exactly the same relations but no quantum effects;
   - the AI's own stated confidence in its answer;
   - (in version two) a simple weighted score of the relation web.

The test that decided everything was written down in advance. Does the entangled version's conflict score pick out the questions the AI got wrong better than every control? We gave every method the same quota of flags, so the only thing that differed was *which* questions each one flagged.

---

## What happened

**First, we needed the AI to make mistakes.** The stronger model we started with, Claude Sonnet 5.5, got every checkable question right: 117 out of 117. We switched to the smaller Claude Haiku 5.5 and built a harder set of 300 questions from published benchmarks. Haiku got 44 of those wrong. The main test used 40 wrong answers and 40 right ones.

**The main result.** We score each method by how well it separates wrong answers from right ones. A score of 0.5 means no better than a coin flip; 1.0 means perfect.

| method | score |
|---|---|
| entangled state (the idea being tested) | **0.55** |
| same circuit with the entangling gates removed | 0.68 |
| same circuit with the relations scrambled | 0.65 |
| plain contradiction-counting, no quantum part | 0.64 |
| entangled state on a perfect, noise-free simulator | 0.49 |

The entangled version came last. The method with the entanglement removed came first. Even scrambling the relations did better than wiring them correctly. The noise-free version did no better, so the problem is not a noisy machine. Our pre-registered primary test failed, and the result doesn't depend on any single question.

A first, smaller run on easier questions had only 4 wrong answers, too few to decide anything. It pointed the same way: plain contradiction-counting scored 0.69 there, the entangled version 0.45.

**The real quantum computer.** We used about 46 seconds of time on IBM's `ibm_fez` processor. With most of it, 44 seconds, we answered a narrower question: was the state on the real chip actually entangled, or just something that gives similar yes/no answers?

We used a pre-registered test called an **entanglement witness**, which measures a quantity called *negativity*. It is zero for anything that is not entangled and up to 0.5 for maximally entangled pairs. We tested 3 belief states; the rule set in advance was that at least 2 of 3 must clearly pass.

| question | negativity on the real chip (95% range) | passed? |
|---|---|---|
| h221 | 0.147 (0.134 to 0.157) | yes |
| h088 | 0.063 (0.051 to 0.075) | yes |
| h268 | 0.067 (0.055 to 0.081) | yes |

All three passed. The chip really did hold entangled belief states. It was noisier than IBM's own model of it predicts: two of the three came out at about half the simulated value. One of the three tested pairs turned out to be cut off from the rest of its belief state, so it was really a two-qubit test.

---

## What it means

**The entanglement is real, and it doesn't help.** Being one indivisible state did not make the judgment better at knowing when it was wrong. If anything, mixing the claims together blurred a signal that the unmixed version still had.

**The useful signal is ordinary.** When the AI is wrong, its own short explanation more often contains reasons that pull against each other. Counting how strongly they contradict catches that; no qubits are needed.

That is a small but real finding about how AI explanations relate to AI mistakes. Two numbers we are still waiting on will say how much it is worth:
- how much uncertainty there is in these scores [PENDING];
- whether the AI's own stated confidence already captures the same thing [PENDING].

**What it doesn't mean.** This tested one particular way of building the state, with settings chosen in advance and never tuned. It tested one AI model, whose mistakes were mostly gaps in knowledge rather than the judgment slips quantum cognition studies. It says nothing about whether quantum cognition describes *people* well. For this design, on these questions, the answer to "do machines need quantum minds?" is no.

---

## What other researchers have found

We read the work this project builds on. The full notes are in `paper/related-work.md`. In plain words:

- **The order effect in people has a hidden regularity.** Across about 70 surveys, the chance that someone's two answers *disagree* is the same in both orders, even when each answer moves. Quantum models predicted this in advance. But other researchers have since shown that simple non-quantum rules (such as "sometimes repeat your first answer") produce the same regularity. So order effects alone can't prove the quantum account.
- **The Linda effect in people is strong but depends on wording.** It nearly disappears when the question is put as counts ("of 200 women like Linda, how many…").
- **AI models break the rules of probability too, but each model does it differently.** The strongest model tested so far, GPT-5, barely breaks them at all.
- **One group tested AI chatbots on a quantum-style "Bell test"** about phrases like "the horse whinnies" and found large violations. Re-checking their published numbers, we found that the answers shift with context strongly enough to explain the violations without any entanglement. One of their tables also gives a different total from the one in their text. We offer this as a check from colleagues, not a takedown.
- **A study that measured an AI's answers to paired survey questions** found the AI's answers almost fully decided in advance on 17 of 18 pairs. There was too little variation to test anything quantum. Any order-effect test of an AI has to check for that first.

---

## What comes next

Three experiments are designed and waiting.

**Version two: let it learn.** The first design used settings chosen in advance. Version two lets the quantum model learn its settings from training questions. It is held to strict rules:
- the classical twin and a simple weighted score get exactly the same number of settings and the same learning procedure;
- the questions are split once, in advance, into training, checking and final-test sets that are never reshuffled.

If the learned quantum model still can't beat its classical twin, that is a much stronger "no". Results: [PENDING].

**Experiment 3: does the order of considering things matter?** Before asking the AI the real question, we ask it to consider two of its own reasons first, in one order or the other. The quantum model and the classical twin each predict, in advance, which pairs of reasons should shift the answer most. The winner is whichever prediction matches what the AI actually does. If the AI shows no order effects at all, we say the test couldn't decide. Results: [PENDING].

**Experiment 4: the sharpest test we have found** [PENDING: not yet pre-registered]. It borrows from Yearsley and Trueblood (2018).
- In quantum models, a Linda-style mistake (rating "A and B" above "B" alone) can only happen when the order of considering A and B matters.
- So a model that makes the mistake should also show an order effect at least as big as the mistake.
- It should never make the "double" mistake: rating "A and B" above *both* A and B.

Our classical twin cannot produce the Linda-style mistake under any settings, because it reads every judgment from one fixed table of possibilities. So a reliable mistake rules it out completely.

A different classical model, one where each judgment changes the state, can produce the mistake. Against that rival, the test has to compare precise predictions question by question. We first overstated this point in our notes and have corrected it.

---

## Why it was still worth doing

Version 1 said a clean negative result would be worth having, and it is. We now know, with data, that building a judgment layer as a genuine entangled whole does not by itself make it better at catching mistakes. We also know the conflicts it was meant to expose are already visible in plain bookkeeping.

We showed that a real quantum computer holds these belief states. And we built a way of testing quantum ideas about judgment, per question and against a fair classical rival, that others can reuse.

This document makes no claim that the system is conscious, that the brain is a quantum computer, or that entanglement is enough to make a mind. It claims only that the question was asked with real hardware, real controls, and results anyone can check.

---

## Limits to keep in mind

- **The reasons came from the AI's written explanation,** not its private reasoning.
- **One AI model was tested,** and its mistakes were mostly gaps in knowledge.
- **Other AI models did the extracting and relation-judging,** and they make mistakes too.
- **The test sets were small,** with 80 questions in the main run.
- **The display that would let you watch a run (the window) is designed but not yet built.** Every run is saved, though.
- **One person did this work.** Everything is public, but nobody has independently repeated it yet.

---

## Glossary

**Amplitude.** How strongly a claim is held, in the quantum encoding. Roughly, confidence.

**Phase.** Which way a claim leans relative to the others. Claims with opposite phase cancel; claims with the same phase add.

**Qubit.** The quantum version of a bit. Instead of being 0 or 1, it holds a blend of both until it is measured.

**Entanglement.** A condition in which several qubits share one state and have no separate states of their own. Measuring one changes what the others will say.

**Interference.** What happens when amplitudes combine: they can add up or cancel out, like waves.

**Contextuality.** The effect in which measuring one thing changes the result of measuring an unrelated thing.

**Collapse.** The moment of measurement, when a blended state becomes one definite answer.

**Shuffled-relations control.** The same experiment run with the support and contradiction links scrambled. If it performs as well as the real run, the structure carried no information. *(In our main run it performed better.)*

**Emergence.** Structure in the output that cannot be traced to any input or to their weighted sum.

*New in version 2:*

**AUROC (the score).** How well a method separates wrong answers from right ones. 0.5 is a coin flip; 1.0 is perfect. Our best method scored 0.68.

**Arm.** One version of the experiment run side by side with the others: entangled, unentangled, scrambled, classical, and so on.

**Calibration set and test set.** Questions used to set each method's flagging level (calibration), kept separate from the questions it is scored on (test), so no method can tune itself to the answers.

**Classical twin.** A non-quantum copy of the entangled model, using exactly the same claims, links and strengths, but with ordinary probabilities instead of amplitudes. It is the fairest possible rival: anything the quantum model does that the twin cannot do must come from the quantum part.

**Conflict score / conflict flag.** How much of the measured outcome splits into two strongly opposed camps. A question is flagged when its score is in the top quarter.

**Contradiction counting.** Adding up how strongly the AI's stated claims contradict each other. No qubits involved. It beat the entangled state.

**Entanglement witness.** A measurement that can prove a state is entangled. Ours uses *negativity*: zero for anything not entangled, up to 0.5 for a perfectly entangled pair.

**Noise model.** A computer simulation of a quantum chip's errors. Ours underestimated how noisy the real chip was.

**Pre-registration.** Writing down the tests, and what result would count as failure, before seeing any data. It stops anyone, including us, from moving the goalposts.

**Deviation.** A change to the pre-registered plan, recorded with its date and reason. We made ten and published all of them.

**Order effect.** When asking two questions in a different order changes the answers.

**QQ equality.** A regularity in human surveys: the chance that someone's two answers disagree is the same in both orders. Quantum models predicted it; some non-quantum models produce it too.

**Conjunction fallacy (the Linda effect).** Rating "A and B" as more likely than "B" alone. A *double* fallacy rates "A and B" above both; quantum models forbid that.

**Bell test (CHSH).** A test, borrowed from physics, of whether results could come from separate parts acting independently. In psychology and AI experiments, results that shift with context can pass it without any entanglement.

**Saturation.** When an AI's answers are almost completely decided in advance, so there is too little variation to measure effects like question order.

**Training, validation and test sets.** In version two, the questions are split once, in advance: training to learn settings, validation to choose between candidates, test for the final score. The split is locked and never redone.

**Learned encoding.** Version two's quantum model, which learns its settings from training questions instead of using fixed ones. Its classical rivals learn with the same budget.

**The window.** The project's planned visual display of a run: each claim is a glowing point, brightness is how strongly it is held, colour is which way it leans, and dashed links show entanglement. A timeline can be rewound through building the state, letting it settle, and measuring it. Every run is archived.

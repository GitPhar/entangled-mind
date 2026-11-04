# No Credence to Read: The Question, the Record and the Format Construct a Language Model's Judgments

**Sean Pharris**
Independent Researcher, Colorado Springs, Colorado
Draft, November 4, 2026. Dates and times are local, America/Denver (MST, UTC−7).

Correspondence: seanm.pharris@gmail.com. Code, data and pre-registrations: https://github.com/GitPhar/entangled-mind.

**Status of the numbers.** Every number below is copied from a results file in the repository's `results/` directory and was produced under a pre-registration committed before its data, unless it is labelled *exploratory*. Numbers whose robustness run has not yet landed carry the tag **[R-pending: run]**. Those runs are listed in Section 8. The replications on `claude-sonnet-5-5` and `claude-opus-5-5` (Section 4.6) are pre-registered in `DEVIATIONS.md` entries DM1–DM6; the claims below are narrowed to what they replicate (D48).

---

## Abstract

A language model reached through a stateless API has, at every turn, a complete state that is a classical string: the conversation so far, plus the sampler's random state. That string can be copied. So the model satisfies macrorealism by construction, and every "measurement disturbance" it shows can be decomposed by editing the transcript, which neither a person nor a quantum system allows. We use this to ask whether a model's stated degree of belief is a stored quantity that questions read out, or something that the act of asking constructs.

On `claude-haiku-5-5`, in pre-registered tests, the answer is the second. Three of the tests were then repeated on `claude-sonnet-5-5` and `claude-opus-5-5`, and the claims below are stated only as far as they replicate.
- **Asking is invasive.** Earlier questions change later ratings in 5 of 6 no-signalling-in-time comparisons on 40 hard questions. A midway yes/no choice is the one exception.
- **The question alone is enough.** With every earlier answer hidden, the order of the questions still changes the final rating. The ratio of redacted to shown order effect is 1.91 [0.92, 4.90] [R-pending: direction 2, 40 items].
- **The record also acts, but only when it is the model's own.**
  - Planting the model's own earlier answer pulls its re-rating 0.42 of the way toward the planted value. The same number attributed to another person pulls it 0.05 [R-pending: source × distance × lag].
  - The model's agreement with itself on a repeated question falls from 81% to 23% when its first answer is hidden [R-pending: direction 2, 40 items].
- **Formats disagree.** Across six elicitation formats, a separate credence per format predicts held-out answers better than one credence per statement for 86% of 160 statements. The formats rank the statements differently four to six times more often than repeat noise does. Predicting each format from the other five recovers only 0.39 [0.30, 0.50] of what is reproducible in that format.
- **Self-report is not privileged.** The model's confidence predicts its errors well (AUROC 0.85), but a stronger model reading the same answers predicts them better (0.93). The judge × author interaction is −0.055 [−0.103, −0.007].

**What replicates on Sonnet and Opus** (Section 4.6):
- **No privileged self-knowledge holds on all three models.** With Sonnet and Opus judging each other's answers, the judge × author interaction is −0.045 [−0.107, +0.017], again *no self-advantage*.
- **Reliance on the model's own record holds on all three.** Repeat agreement falls when the first answer is hidden: 78% → 25% (Haiku), 88% → 35% (Sonnet), 95% → 65% (Opus).
- **The no-format-free-credence claim holds for Haiku, partly for Sonnet, and not for Opus.** Agreement across the six formats rises with model strength: Kendall's W is 0.54 for Haiku, 0.71 for Sonnet and 0.86 for Opus. One credence predicts a left-out format with Q = 0.29 on Haiku and 0.69 on Sonnet, on the same 80 statements. On Opus's 26 statements, one credence per statement fits as well as one per format.
- **The question alone constructs the judgment on Sonnet** (R = 2.95 [0.99, 12.55]). On Opus the test is not decisive.

On Haiku, there is a stable process that turns a prompt and a transcript into a number, and no format-free credence behind it for that process to report. On stronger models, the transcript still conditions the number and self-report is still not privileged, but the formats increasingly read as one belief. We discuss what this means for confidence elicitation, calibration measurement and introspection evaluations.

---

## 1. Introduction

Language models are routinely asked how confident they are. Their answers are used:
- to flag likely errors;
- to calibrate deployments;
- as evidence about whether models "know what they know" (Kadavath et al., 2022; Tian et al., 2023; Xiong et al., 2024).

Behind that use sits an assumption: the model has a degree of belief in a proposition, and an elicitation reads it out, perhaps with distortion. The alternative is that the act of asking constructs the judgment, from the question, its format and the transcript it lands in. On that view there is nothing format-free for an elicitation to read.

The two views have been argued over for people, in the quantum-cognition literature especially (Busemeyer & Bruza, 2012; Wang & Busemeyer, 2013). There they cannot be cleanly separated, for two reasons:
- **You cannot copy a person.** So "what would they have said if not asked first?" is answered with a different person, or the same person on a different day.
- **A person who has answered remembers answering.** So the effect of the question cannot be pulled apart from the effect of the remembered answer.

Khrennikov et al. (2014) call the resulting tension between response replicability and order effects "an unsolved problem" for quantum models of psychological measurement.

A language model removes both obstacles. Its state at a turn is the conversation text, which can be copied exactly. Its memory of an answer is a line in that text, which can be deleted or replaced. This paper uses that fact, first as a framing (Section 2) and then as a method (Sections 3–5).

Our tests came out of a longer project that tried to model this model's judgments with quantum probability. The quantum models tied matched classical twins throughout, on error prediction and on sequential judgment (Pharris, 2026). The tests reported here ask the prior question: what is there to model?

**Contributions.**
1. **An argument.** For a model reached through its context, macrorealism holds by construction. Leggett–Garg, no-signalling-in-time (NSIT), total-probability and question-order violations in such a model can only measure invasiveness, never the absence of a definite state (Section 2).
2. **A decomposition.** Invasiveness splits into the turn itself, the question, and the recorded answer. Transcript editing measures each one (Sections 2.3 and 4.2).
3. **Pre-registered measurements on one model, with replications on two more.** On Haiku, they show that the question and the model's own recorded answer both construct later judgments, that the format constructs the credence, and that self-reported confidence carries no information a capable reader of the answer lacks (Sections 4.1–4.5). On Sonnet and Opus, the self-report and own-record findings replicate. The format finding weakens with model strength and does not hold on Opus (Section 4.6).

---

## 2. Framing: a clonable mind

### 2.1 Macrorealism and its loophole

Leggett and Garg (1985) derived their inequalities from two assumptions:
- **macroscopic realism**, which is that "a macroscopic system with two or more macroscopically distinct states available to it will at all times be in one or other of those states";
- **non-invasive measurability**, which is that "it is possible, in principle, to determine the state of the system with arbitrarily small perturbation on its subsequent dynamics".

Later statements add **induction**: later measurements cannot affect earlier outcomes (Emary, Lambert & Nori, 2014).

Kofler and Brukner (2013) give a weaker, statistical condition, **no-signalling in time (NSIT)**: "A measurement does not change the outcome statistics of a later measurement." Macrorealism implies NSIT.

A violation therefore shows that a system is either not macrorealist, or "macrorealistic but subjected to a measurement technique that happens to disturb the system". That is the clumsiness loophole (Wilde & Mizel, 2012). Physics can narrow the loophole only statistically, with control measurements.

### 2.2 The state of a language model

A model served through a stateless API, such as the Anthropic Messages API used here, has four properties that matter:
- **Each request carries the whole conversation.** The server keeps nothing between requests that changes the response distribution.
- **The weights are fixed** for a model id over the time of an experiment.
- **The context and the sampler's state fix the response,** so the complete state is λ = (context, sampler state). Kofler and Brukner (2013, footnote 45) require exactly this for strict macrorealism: each outcome must be determined by the complete state.
- **The API exposes no seed.** A copy of the context therefore reproduces the response *distribution* exactly, though not a particular draw.

Two consequences follow.
- **An ideal non-invasive measurement exists.** To read a question at turn t without disturbing the conversation, send the context plus the question to a copy, and discard the copy. The original is untouched, which is ontic non-invasiveness in Maroney and Timpson's (2014) sense.
- **There is no free evolution.** The context changes only when a turn is appended, so in a chain of questions the "dynamics" between two measurements is the next question.

**Proposition.** Read on copies of one context, the answers to any set of questions are conditionally independent given the context. A single joint distribution with every measured marginal therefore exists. So every Leggett–Garg inequality, NSIT condition and the law of total probability hold, and every order effect is zero.

**Corollary.** In a sequential protocol, where each question and answer stay in the context of later questions, any violation measures how the protocol's measurements change the state. It cannot be evidence that the state was indefinite.

For people, the "not asked" condition is a counterfactual. For this model it is a measurable condition.

### 2.3 Three channels

Appending "question Q, answer a" to the context can change later answers through three channels:
- **L:** a turn was added, whatever it says;
- **Q:** the question's content is now in context;
- **R:** the model's own answer is now in context.

Transcript conditions isolate them:

| condition | context before the later question | channels |
|---|---|---|
| not asked (equivalent to a copy) | the original context | none |
| filler turn | a content-free turn of matched length | L |
| redacted | the question, with the answer replaced by a placeholder | L, Q |
| planted | the question, with a chosen value in the model's own turn | L, Q, and a record the model did not produce |
| shown | the question and the model's own answer | L, Q, R |

For people, only "shown" exists. For a quantum system, "not asked" is not available on the same system, and "redacted" has no meaning. A language model offers every row.

---

## 3. Methods

### 3.1 Model and settings

All tests use `claude-haiku-5-5`, with thinking disabled and the default sampling temperature of 1.0. The API rejects an explicit temperature for this model. Outputs are structured (for example `{"rating": <integer>}`), and every rating scale states one direction: "0 = certainly false, 100 = certainly true".

Direction 1 also uses `claude-sonnet-5-5`, as both author and judge.

**The replications (Section 4.6)** re-run tests P, T and F with `claude-sonnet-5-5` and `claude-opus-5-5` as base models, through the Message Batches API. Thinking is as close to off as each model allows: Sonnet `between_tools` (Sonnet 5.5 rejects `disabled`), and Opus at effort `low` (Opus 5.5 cannot disable thinking). Opus's thinking text is never returned or placed in a transcript. The designs are scaled down to fit a $20 budget (DM1):
- test F on 80 of the 160 claims;
- test T at 4 conversations per cell (Opus: 2);
- test P with Opus authoring new answers to the 298 questions and the paraphrase and recognition arms not run.

Every run stops at its first refusal, logs the request ID, and neither rewords nor retries. No run in this paper was stopped.

### 3.2 Items

- **The 40 sequential-judgment items.** These come from a 300-question hard pool of SimpleQA-type factual and multi-step science questions, on which Haiku errs often: 20 answered wrongly and 20 rightly (experiment 5; Pharris, 2026).
  - Each item has a main question M and 4 of the model's own competing claims about it, S₁–S₄, extracted from its visible explanation.
  - In experiment 5, the model rated chains of these on 0–100, 10 conversations per item and chain type. The chain types:
    - four Latin-square orders O₁–O₄, ending in M;
    - each claim omitted in turn, X₁–X₄;
    - M alone (B0);
    - M first and again after the chain (MF);
    - a midway yes/no choice on M (K₁) against a length-matched filler (K₀);
    - adjacent (S_k, M) pairs in both orders.
- **The 298 hard-pool questions answered by both models** (direction 1).
- **The 16 conjunction items of experiment 4** (bm1).

### 3.3 Tests

Each test was pre-registered in its own commit before any call or analysis. The pre-registration files are in `experiments/`, and the commits and decisions are logged in `DEVIATIONS.md`.

| test | question | data | primary statistic | pre-registration |
|---|---|---|---|---|
| **N** (gold-map direction 9) | does asking change later answers? | archived experiment-5 conversations, one scale direction, $0 | six NSIT families: per-cell mean shift d between asked and not-asked conversations; permutation test of Σd²; Holm correction | `gm9-nsit.md`, D34 |
| **T** (direction 2) | the question, or the record? | 10 experiment-5 items, chains O₁–O₄ and MF; shown, redacted ("[rating recorded]") and planted ±15 points in the model's own turn; 10 conversations per cell; 2,000 conversations, $0.55 | R = OE_redacted / OE_shown, where OE is the between-order spread of the final M; question-driven if the CI lies wholly at or above 0.5 | `gm2-self-conditioning.md`, D37 |
| **S** (bm1) | does the source of a number matter? | experiment 4's 16 items, values 30 points below and above the model's mean, planted as its own earlier answer, then a re-rating; 40 per cell; 2,560 conversations, $0.24; compared with the archived condition in which the same values were "another person's estimate" | slope s of the re-rating on the shown value, own against other | `bm1-serial-dependence.md`, D44 |
| **A** (bm9) | does the next rating move toward the last number? | archived single-scale (S_k, M) conversations, $0 | β in d_M = α + β·L + γ·C, where L is the S rating's level relative to the unprompted M and C is the claim's content push | `bm9-contrast.md`, D42 |
| **P** (direction 1) | does authorship help judge errors? | both models rate confidence in both models' answers on 298 questions, with one matched prompt ("an answer another assistant gave"); 1,710 calls, $2.82 recorded | the judge × author interaction I = HH + SS − SH − HS (judge first, then author), which cancels each judge's skill | `gm1-self-knowledge.md`, D36 |
| **F′** (robustness) | is one credence at least useful? | test F's calls, $0 | Q = R² of each format predicted from the other five / that format's split-half R² | `gm3c-heldout-format.md`, D46 |
| **F** (direction 3) | is there one credence per statement? | the 160 experiment-5 claims × 6 formats × 10 repeats; 9,600 calls, $0.41 | held-out log-likelihood (even against odd repeats) of one latent credence per claim with a monotone link per format (L1) against one credence per claim and format (L6) | `gm3b-format-invariance.md`, D38 |

The six formats in F are:
- a 0–100 rating;
- yes/no;
- buying a $100 ticket at a stated price;
- "more likely than a fair coin landing heads?";
- "how many of 100 such statements would be true";
- a 7-point verbal scale.

### 3.4 Statistics

Intervals are 95% bootstrap intervals over items: 2,000 resamples unless stated, with fixed seeds recorded in each pre-registration. AUROCs are computed against the hard pool's correctness labels.

---

## 4. Results

### 4.1 Asking is invasive

**Test N, the six families.** Each family compares the later rating between conversations that differ only in whether an earlier question was put. The null column gives the mean |d| expected by chance.

| family | contrast | cells | mean |d| (null) | p (Holm) |
|---|---|---|---|---|
| N1M | M after S_k vs M first | 80 | 12.4 (2.6) | 0.0012 |
| N1S | S_k after M vs S_k first | 80 | 15.7 (3.1) | 0.0012 |
| N2 | final M with S_k asked vs omitted | 160 | 8.7 (3.9) | 0.0012 |
| N3 | final M after four sub-questions vs M alone | 40 | 22.6 (5.2) | 0.0012 |
| N4 | final M after a midway yes/no choice vs a filler | 40 | 5.0 (3.3) | 0.16 |
| N5 | final M with M asked first vs not | 40 | 16.0 (6.1) | 0.0012 |

- **Five of six families are invasive.**
- **Most shifts go both ways across items.** For example, N1M's mean signed shift is −0.0 [−6.1, +5.5], and N2's is +0.7 [−3.7, +4.3].
- **Two families shift one way:**
  - asking M first raises the next sub-question's rating, by +8.0 [+2.7, +13.3];
  - asking M at the start of a chain lowers the final M, by −10.1 [−18.2, −2.9].
- **N1 replicates** on a separate set of single-scale conversations (10 items, 40 per order): 17.4 against 2.9, and 15.7 against 2.3.

**The omission chains (family N2)** are the NSIT test for each claim question. Asking about one of its own claims moves the model's final verdict by 8.7 points on average, at least 10 points in 19% of cells.

**The midway choice (family N4, and experiment 5's pre-registered Kvam contrast)** is the one non-invasive family.
- Committing to yes or no on the main question changes the final confidence no more than a filler turn does. In experiment 5's statistic, the folded confidence |r − 50| differs by Δ_K = +0.29 [−1.12, +1.65] points, with a total-probability residual of +0.58.
- **Exploratory:** a two-sample KS test of K₁ against K₀ rejects at p < 0.05 on 5 of 40 items, uncorrected, against 2 expected by chance.
- Asking M as a *0–100 rating* at the start (N5) does move the final rating. So the format of the earlier measurement matters.

### 4.2 The question alone is enough, and the model's own record also steers

**Test T** [R-pending: direction 2, 40 items]

| condition | order effect across O₁–O₄ (points) | repeat agreement in MF (|M₂ − M₁| ≤ 5) |
|---|---|---|
| shown | 8.7 [4.1, 12.7] | 81% |
| redacted | 16.7 [8.0, 24.1] | 23% |
| planted high | 6.2 [3.6, 8.3] | 30% |
| planted low | 3.2 [2.2, 4.0] | 40% |

- **The question alone changes the judgment.** R = 1.91 [0.92, 4.90]. The interval lies wholly above 0.5, so the pre-registered reading is *question-driven*: with no record of its answers, the order of the questions still changes the model's final rating.
- **The record steers too.**
  - The final M follows a planted first M at 1.27 [0.70, 2.14] points per point.
  - Planted-high earlier ratings raise the next actual ratings by 5.6 [3.4, 7.6] points over planted-low, and the final M by 10.4 [4.2, 16.8].
- **Apparent stability is memory.** With its first answer visible, the model repeats it within 5 points 81% of the time, close to experiment 5's 84%. With it hidden, it does so 23% of the time.
- **Caveats.**
  - Much of the redacted order effect comes from 2 of the 10 items (h191, h261).
  - The redacted effect is *larger* than the shown one, so the placeholder turn may add variance of its own. The verdict stands by its rule, but the excess over "shown" should not be read as the question's own effect.

### 4.3 The record acts only when it is the model's own, and new ratings move toward old ones

**Test S** [R-pending: source × distance × lag]. The same numbers, presented two ways:
- **as the model's own earlier answer:** they pull its re-rating with slope **s_own = +0.42 [+0.25, +0.60]**, and the model repeats the planted value exactly in 42% of conversations;
- **as another person's estimate** (the archived condition): they barely pull it, with s_other = +0.05 [−0.08, +0.17].

The difference is **+0.37 [+0.17, +0.57]**, so the pre-registered reading is *source-dependent self-consistency*.

In the archived condition, 7 item-orders moved *away* from another person's higher estimate. On 6 of them, the same number framed as the model's own pulls it up (descriptive). This matches Kumaran et al. (2025), who found that the stickiness of an earlier answer in other models disappears when it is attributed to another model.

**Test A.** In unedited single-scale conversations, the main rating moves toward the level of the sub-question rating just given, beyond the claim's content: **β = +0.27 [+0.11, +0.43]**, replicating at +0.27 [+0.05, +0.58]. No contrast appears.

### 4.4 Self-reported confidence is not privileged

**Test P.** AUROC for each author's errors, judge first and author second:

| set | HH | SH | SS | HS | I [95% CI] |
|---|---|---|---|---|---|
| all 298 | 0.845 | 0.932 | 0.903 | 0.872 | −0.055 [−0.103, −0.007] |
| authors' correctness differs (26) | 0.432 | 0.850 | 0.865 | 0.583 | −0.135 [−0.496, +0.229] |
| paraphrased answers (subset) | 0.798 | 0.887 | 0.808 | 0.759 | −0.040 [−0.157, +0.075] |

- **Authorship does not help, and slightly hurts.** Sonnet predicts Haiku's errors better than Haiku does: 0.93 against 0.85.
- **Where the authors disagree,** Haiku is near chance on its own answers (0.43), and Sonnet is good on them (0.85).
- **Wording makes no difference.** "An answer you gave" instead of "another assistant" changes the self cells by −0.011 (Haiku) and +0.007 (Sonnet).
- **Haiku cannot pick out its own answers:** recognition AUROC 0.51 [0.36, 0.67].

### 4.5 On Haiku, there is no format-free credence

**Test F**

**The primary test.** The format-specific model L6 beats the single-credence model L1 on held-out repeats for **86% of 160 claims**. The mean ΔLL is **+19.4 [+16.5, +22.1]** per claim.

**Agreement between formats** (per-claim means):
- Spearman correlations between pairs of formats range from 0.37 to 0.74, and Kendall's W across all six is 0.56.
- Against the 0–100 rating, 20% to 34% of claim pairs are ordered the other way.
- The coin comparison is the most discordant: it chooses the statement 79% of the time, where the mean rating is 55.

**Noise baseline** (*exploratory*, computed after the run). Two halves of the same format's repeats disagree on the order of 4–8% of claim pairs. The 0–100 rating's even repeats against another format's odd repeats disagree on 21–35%. Cross-format reordering is therefore four to six times repeat noise, and no monotone link can absorb a reordering.

**An earlier, smaller check.** The free look of test F (`gm3a-anchor-gap.md`, D35) asked whether experiment 5's 37-point gap between the two scale directions marks the model's errors. It does not: AUROC 0.48 [0.28, 0.66], against 0.75 for the model's stated confidence on the same 40 items. A distortion of the credence that carries no error signal is what a reading slip would produce. So this check does not, on its own, support construction.

**Test F′: is one credence at least useful?** This is the like-for-like comparison with Smolin and Wilder (2026), pre-registered after test F (`gm3c-heldout-format.md`, D46, $0, test F's archived calls).
- **Method.** The single-credence model L1 is fitted on five formats and predicts the sixth, for each format in turn, with items held out in five folds. Each prediction is compared with the held-out format's own split-half ceiling (its even repeats predicting its odd ones).
- **The statistic** is Q = R²(cross) / R²(ceiling). Simulated checks before freezing gave Q = 1.06 in a one-belief world and 0.21 in a format-specific one.

| held-out format | R² from the other five | R² ceiling | Q |
|---|---|---|---|
| rating 0–100 | 0.51 | 0.96 | 0.53 |
| yes/no | 0.36 | 0.89 | 0.41 |
| bet | 0.43 | 0.92 | 0.47 |
| pairwise vs coin | 0.15 | 0.88 | 0.17 |
| frequency /100 | 0.30 | 0.94 | 0.32 |
| verbal 7-point | 0.46 | 0.97 | 0.47 |

- **Mean Q = 0.39 [0.30, 0.50]**, so the pre-registered reading is *little format-free belief*. The interval's upper end, 0.499, sits just under the 0.5 line, so a "partial" reading is excluded only narrowly.
- **Mean R² from the other five formats is 0.37 [0.28, 0.47].** Smolin and Wilder report held-out R² of 0.60–0.90 on other capable models. Haiku, on its own contested claims, is below that whole range.
- **Reading.** Each format's answers are highly reproducible (ceilings 0.88–0.97). Only a third to a half of that reproducible answer is shared with the other formats. On Haiku, there is a common component, but it is the smaller part. Section 4.6 shows that this does not carry over to stronger models.

### 4.6 Which findings hold on Sonnet and Opus

Tests P, T and F were re-run with `claude-sonnet-5-5` and `claude-opus-5-5` as base models. Each used the original's prompts, analysis code and pre-registered reading, and was pre-registered in its own commit before its first call (DM2–DM4; summary in `results/multi-model.md`). No call was refused. They cost $16.28 at batch rates.

| finding | Haiku | Sonnet | Opus | holds on |
|---|---|---|---|---|
| **no privileged self-knowledge** (test P: judge × author interaction I) | −0.055 [−0.103, −0.007] (Haiku × Sonnet) | −0.045 [−0.107, +0.017] (Sonnet × Opus); also in the Haiku pair | (Sonnet × Opus) | **all three** |
| **reliance on own record** (test T: MF repeat agreement, shown → redacted) | 78% → 25% | 88% → 35% | 95% → 65% | **all three** |
| the question alone (test T: R = OE_redacted / OE_shown) | 2.01 [1.04, 4.43] (repeats 0–3) | 2.95 [0.99, 12.55], question-driven | 0.93 [0.06, 7.31] at 2 per cell, not decisive | Haiku, Sonnet |
| **no format-free credence** (test F: mean ΔLL, L6 − L1) | +19.42 [+15.40, +23.21], 86% of claims | +9.22 [−1.29, +16.24], 92% of claims: *mixed* | +0.42 [−1.83, +2.69], 58% of claims (26 claims): *mixed* | Haiku; partly Sonnet; not Opus |
| test F′: one credence predicting a left-out format (Q) | 0.29 [0.19, 0.43] | 0.69 [0.53, 0.82], *partial* | not computed (arm incomplete) | |
| **agreement across formats** (Kendall's W) | 0.54 | 0.71 | 0.86 | rises with model strength |

Haiku's rows for test F are re-analyses of its archived calls on the same 80 claims. Its 160-claim figures are in Section 4.5.

**No privileged self-knowledge holds on all three models.**
- Opus predicts Sonnet's errors better than Sonnet does: AUROC 0.959 against 0.903.
- On Opus's own answers, being the author adds almost nothing: Opus reaches 0.904, Sonnet reading the same answers 0.893.
- With each judge's skill cancelled, I = −0.045 [−0.107, +0.017]. That is the same sign and size as the Haiku × Sonnet pair, and again the pre-registered reading is *no self-advantage*.

**Reliance on the model's own record holds on all three.**
- With its first answer visible, each model repeats it within 5 points far more often than with it hidden. The pre-registered memory reading (a drop of more than 10 points) holds on every model.
- Opus is the most stable without its record (65%), so less of its stability is memory.
- The per-point pull of a planted first answer is weaker on the stronger models: b_MF is 1.23 [0.65, 2.11] (Haiku), 0.39 [−0.05, 0.76] (Sonnet) and 0.35 [0.17, 0.54] (Opus).
- The own-against-other comparison (test S) was run on Haiku only.

**The no-format-free-credence claim holds for Haiku, partly for Sonnet, and not for Opus.**
- **Haiku** fails the one-credence test clearly, on the 80 claims as on all 160.
- **Sonnet's** formats disagree beyond one credence on 92% of claims. But one extreme claim (ΔLL −308) pulls the interval across zero, so the pre-registered reading is *mixed*. On test F′, one credence recovers about two-thirds of what a left-out format reproducibly says (Q = 0.69), against Haiku's 0.29 on the same claims.
- **Opus's** arm was budget-stopped after 26 claims, all from items Haiku answered wrongly. On those, one credence per statement fits as well as one per format (ΔLL +0.42 [−1.83, +2.69]), and its formats rank the statements almost alike (W 0.86; 3–14% of pairs reversed against the 0–100 rating, against Haiku's 25–35%). Its pre-registered reading is *mixed*, not *single credence*. So the claim is not shown false on Opus. It is not supported there, and the evidence that exists points the other way.
- **The trend.** Kendall's W rises from 0.54 (Haiku) to 0.71 (Sonnet) to 0.86 (Opus). The stronger the model, the more its six ways of answering behave like readings of one belief. Opus's W comes from a different and smaller set of claims, so the last step of the trend is not item-matched.

---

## 5. Discussion

### 5.1 A generator, not a credence

Taken together, the results describe two things.

**A stable generator.**
- Answers to one prompt repeat closely: two halves of a format's repeats disagree on only 4–8% of orderings.
- A midway yes/no choice leaves the final judgment alone.
- The scale-direction slip is unrelated to errors.

**A credence that is not format-free, on Haiku.** The generator's output depends on three things beyond the proposition:
- the question and the questions before it (Sections 4.1 and 4.2);
- the format (Section 4.5);
- the model's own recorded answers, but not other people's (Sections 4.2 and 4.3).

What looks like a stable belief within a conversation is, to a large degree, consistency with the transcript: repeat agreement falls from 81% to 23% when the first answer is hidden [R-pending: direction 2, 40 items].

By the argument of Section 2, none of this shows that the model "has no definite state". Its state is perfectly definite. What Haiku lacks is a format-free, transcript-free quantity for elicitation to read.

**How far this generalises** (Section 4.6). The transcript part does: on Sonnet and Opus too, repeat agreement is partly memory of the record. The format part does not. On Sonnet a single credence is partly usable, and on Opus the formats agree closely enough that one credence fits as well as six. "No credence to read" is therefore a finding about Haiku, and to a lesser degree Sonnet, on contested claims. It should not be stated for language models in general.

The finding sits alongside Smolin and Wilder (2026), who fit one latent belief across 16 framings of other capable models. Their criterion is usefulness: does one latent predict new framings? Test F's criterion was stricter, but test F′ applies theirs directly. On Haiku, one latent predicts a left-out format with R² 0.37, against their 0.60–0.90 for other models. It recovers 39% of what the format reproducibly says. On Sonnet, on 80 of the same claims, it predicts with R² 0.65, inside their range. So the difference from their result is mostly the model, not the criterion: the weaker the model, the less of a format-free belief there is to find.

### 5.2 Confidence elicitation

**The transcript is part of the measurement.** A confidence elicited in the same conversation as the answer, or after other questions, is conditioned on the record:
- planted own answers pull later ratings at 0.42 to 1.27 points per point (Sections 4.2 and 4.3) [R-pending: direction 2, 40 items; source × distance × lag];
- ratings move about a quarter of the way toward the last number given (Section 4.3).

Practical consequences:
- **Elicit on a copy.** Confidence meant to reflect the model's view of a proposition should be asked in a fresh context, or on a copy of the context taken before any earlier rating. That costs one extra call and gives the undisturbed distribution (Section 2.2).
- **Report the transcript.** Every confidence number should be reported with the conversation it was asked in.
- **Report the format.** The format is not a neutral wrapper. On contested claims, changing it reorders the propositions.

### 5.3 Calibration

Calibration is usually measured in one format, for example verbal 0–100 or a probability token.

**Calibration need not transfer across formats, at least on weaker models.** Haiku's six formats order the same statements differently on 21–35% of pairs (exploratory baseline). Predicting one format from the other five recovers only 39% of its reproducible answer (test F′). A model that is well calibrated in one format can therefore rank propositions differently in another. On the same 80 statements, against the 0–100 rating, Haiku's formats reverse 25–35% of pairs, Sonnet's 14–20%, and Opus's 3–14% on its 26, so the risk shrinks with model strength. Calibration claims should still name the format, and where possible be checked in more than one.

**Within-conversation consistency is not evidence of a stable credence.** A model that keeps giving the same number in one conversation may be reading its own earlier answer:
- it stays consistent with itself far more than with an external estimate (s_own +0.42, s_other +0.05) [R-pending: source × distance × lag];
- its repeat agreement collapses when its first answer is hidden [R-pending: direction 2, 40 items].

Test–retest reliability for model confidence should be measured across copies, not within a conversation.

### 5.4 Introspection evaluations

**Self-report against a reader.** A model's stated confidence is often taken as evidence that it knows what it knows. Here it is a good error signal (AUROC 0.85 for Haiku, 0.90 for Sonnet and Opus on their own answers), but a stronger model reading the same answer does better (Sonnet on Haiku's 0.93, Opus on Sonnet's 0.96). The absence of a self-advantage holds on all three models (Section 4.6).

**An evaluation of privileged self-knowledge needs three controls:**
- **A reader control with matched framing:** another model judges the same text with the same prompt.
- **A statistic that cancels capability.** The judge × author interaction does this. Per-author self-minus-other comparisons confound authorship with judge strength (Xiao et al., 2026, report the same pattern in open models).
- **Transcript-editing controls for any self-consistency claim,** because a model's agreement with its earlier self can be memory.

**What our result says.** On this test, and on all three models, self-reported confidence is text-reading. That does not rule out privileged access in other settings, such as hidden-state probes (Ashuach et al., 2026, find a small one there) or trained self-prediction (Binder et al., 2025). It does mean that a verbal-confidence AUROC, however high, is not by itself evidence of introspection.

### 5.5 Quantum-cognition tests on language models

The argument of Section 2 applies to the field's tests as well as ours.
- **Multi-turn tests** (Kang, 2026; Bessis et al., 2026; our experiments) measure invasiveness.
- **Single-prompt tests** measure the context-dependence of one response.
- **Contextuality tests** that present each context to the model measure how its outputs depend on what it reads.

None of these can show that a model's judgments lack definite values. A quantum-probability model can still be a compact description of how appended text perturbs the response distribution. It now has a ground truth that human studies lack: the clone-read marginals.

---

## 6. Limitations

- **Two items carry much of direction 2's redacted effect** (h191, h261), and there are 10 items in all. The 40-item run (Section 8) is the test of whether the question-driven reading survives. Until it lands, every direction 2 number in this paper is provisional.
- **The redaction placeholder** "[rating recorded]" is an unusual turn. It may add variance of its own: the redacted order effect is larger than the shown one.
- **Two criteria for the format result.** Test F's criterion (held-out *repeats*) is stricter than Smolin and Wilder's. Because Haiku's repeats vary little, any reproducible format-by-claim deviation favours the format-specific model. Test F′ applies their usefulness criterion (held-out *formats*) and also finds little format-free belief. Its interval's upper end, 0.499, lies just under the pre-registered 0.5 line, so the margin over a "partial" reading is thin.
- **Three models, unevenly.** Tests N, S, A and F′ on all 160 claims use `claude-haiku-5-5` alone. Tests P, T and F were replicated on `claude-sonnet-5-5` and `claude-opus-5-5` at reduced scale (Section 4.6):
  - Opus's six-format arm stopped at 26 of 80 claims, all from items Haiku answered wrongly;
  - Opus's transcript arm ran at 2 conversations per cell, too few to decide the question-alone reading;
  - the replications ran with each model's thinking as low as the API allows, which for Opus is not off.
  The format finding does not hold on Opus, and nothing here establishes any result for models outside the Claude 5.5 family.
- **Thinking was disabled, and the temperature is the default 1.0,** since the API rejects another. With extended thinking, the thinking text becomes part of the context, so the argument of Section 2 still applies, but the measurements may differ.
- **The source comparison (test S) differs in wording as well as source.** It uses "Please give your rating again" against the archived "accept or revise". The planted values were ±30 points from the model's mean, which is large enough to read as implausible.
- **Direction 1 was cut short** by cost overruns and a crash. The paraphrase arm covers 60 of 80 questions, and Sonnet's recognition check did not run. The primary statistic uses all 298 questions. Recorded spend was $2.82; calls lost in the crash bound the true spend at about $3.02, against a $3 cap.
- **The items are hard questions and the model's own contested claims about them.** Statements on which the model is certain may behave differently.
- **Several analyses reuse archived data** (N, A and the free look). They were pre-registered before the archive was opened for them, but the data had been collected for other tests.

---

## 7. Reproduction

Every table in this paper can be rebuilt from archived data.

- **`experiments/reproduce.py`** recomputes every results table from the archived JSON in `results/` with the network blocked. Each table matches the committed results file byte for byte above that file's "In plain English" and "Reading" sections, which are written by hand. The last full run reported "ALL TABLES REPRODUCED".
- **The raw calls and conversations** are archived next to each result:
  - `results/gm1-calls.json`
  - `results/gm2-conversations.json`
  - `results/gm3b-calls.json`
  - `results/bm1-calls.json`
  - `results/exp5-conversations.json`
  - `results/exp5-run-2-conversations.json`
- **Each analysis script** sits next to its pre-registration in `experiments/`:
  - `gm9_nsit.py`
  - `gm2_self_conditioning.py`
  - `gm1_self_knowledge.py`
  - `gm3b_format_invariance.py`
  - `gm3a_anchor_gap.py`
  - `gm3c_heldout_format.py` (test F′)
  - `bm_runs.py` (test S's calls)
  - `bm_offline.py` (test A and the other archived-data biomimetic analyses)
- **The replications (Section 4.6):** `experiments/mm_gm1.py`, `mm_gm2.py` and `mm_gm3b.py`, each with an `analyse` mode that rebuilds its table from `results/mm-*.json` with no API call. The summary is `results/multi-model.md`.
- **Pre-registrations and their commit hashes** are listed in `DEVIATIONS.md`, entries D34–D48 and DM1–DM6. A chronological record is in `paper/record.md`.
- **Costs.** The new tests reported here used $4.02 of recorded API spend: P $2.82, T $0.55, F $0.41, S $0.24, and N, A and the free look $0. At most $0.20 more was lost in direction 1's crash. The archived experiment-5 conversations they reuse cost $2.07 when collected. The replications on Sonnet and Opus cost $16.28 at batch rates. No QPU time was used.

---

## 8. Pending robustness runs

Three robustness runs were planned, each pre-registered in its own commit before its data. One has landed; the other two are pre-registered and not yet reported. No other robustness run is planned, so every number without a tag is final as pre-registered.

| tag | run | what it tests | affects |
|---|---|---|---|
| [R-pending: direction 2, 40 items] | D45, pre-registered at `4894bfc`, $2.50 cap; running | direction 2's design on all 40 experiment-5 items: the 10 already run pooled with 30 new ones, and the 30 also reported alone. Sensitivity checks: excluding h191 and h261; the share of items whose redacted order effect is at least half the shown one; and within-order spread, shown against redacted, to check the placeholder | Section 4.2 and the abstract: R, b_MF, the next-rating pull, MF agreement 81% against 23% |
| landed | D46 (`52aedb6`, pre-registered at `1f2a837`), $0 | the held-out-format prediction | reported in Section 4.5 as test F′: Q = 0.39 [0.30, 0.50], "little format-free belief" |
| [R-pending: source × distance × lag] | D47, pre-registered at `8acc007`, $0.50 cap; starts after D45 | own against other source at ±10 and ±60 points (lag 0, R = 10); own at ±30 after 3 filler turns (R = 20); bm1's own ±30 and run 3's other ±30 reused. Readings: own > other; non-monotone or reversal at ±60; decay over lag | Section 4.3: s_own, s_own − s_other and the 6-of-7 reversal. It addresses the wording caveat only in part, since the "other" cells keep run 3's accept-or-revise wording |

---

## References

- Ashuach, T., Gretz, S., Katz, Y., Belinkov, Y., & Ein-Dor, L. (2026). Masked by consensus: Disentangling privileged knowledge in LLM correctness. ACL 2026. arXiv:2604.12373.
- Bessis, T. F., Wills, A. J., Wojciechowski, B. W., White, L. C., & Pothos, E. M. (2026). Legal decision biases in GPT: A comparison with human judgment. *Behavioral Sciences, 16*(3), 437. doi:10.3390/bs16030437.
- Binder, F. J., et al. (2025). Looking inward: Language models can learn about themselves by introspection. ICLR 2025. arXiv:2410.13787.
- Busemeyer, J. R., & Bruza, P. D. (2012). *Quantum Models of Cognition and Decision*. Cambridge University Press.
- Emary, C., Lambert, N., & Nori, F. (2014). Leggett–Garg inequalities. *Reports on Progress in Physics, 77*, 016001. doi:10.1088/0034-4885/77/1/016001.
- Kadavath, S., et al. (2022). Language models (mostly) know what they know. arXiv:2207.05221.
- Kang, P. (2026). Auditing question-order effects in large language models with the QQ equality. arXiv:2607.17219.
- Khrennikov, A., Basieva, I., Dzhafarov, E. N., & Busemeyer, J. R. (2014). Quantum models for psychological measurements: An unsolved problem. *PLoS ONE, 9*(10), e110909. doi:10.1371/journal.pone.0110909.
- Kofler, J., & Brukner, Č. (2013). Condition for macroscopic realism beyond the Leggett-Garg inequalities. *Physical Review A, 87*, 052115. doi:10.1103/PhysRevA.87.052115.
- Kumaran, D., Fleming, S. M., Markeeva, L., Heyward, J., Banino, A., Mathur, M., Pascanu, R., Osindero, S., De Martino, B., Veličković, P., & Patraucean, V. (2025). arXiv:2507.03120.
- Kvam, P. D., Pleskac, T. J., Yu, S., & Busemeyer, J. R. (2015). Interference effects of choice on confidence. *PNAS, 112*(34), 10645–10650. doi:10.1073/pnas.1500688112.
- Leggett, A. J., & Garg, A. (1985). Quantum mechanics versus macroscopic realism: Is the flux there when nobody looks? *Physical Review Letters, 54*, 857–860. doi:10.1103/PhysRevLett.54.857.
- Maroney, O. J. E., & Timpson, C. G. (2014). Quantum- vs. macro- realism: What does the Leggett-Garg inequality actually test? arXiv:1412.6139.
- Pharris, S. (2026). The entangled mind: Quantum cognition as a cognitive architecture for language models. Version 3. `paper/the-entangled-mind-v3.md`.
- Smolin, A., & Wilder, B. (2026). Beliefs and behavior in language models. arXiv:2609.07943.
- Tian, K., et al. (2023). Just ask for calibration: Strategies for eliciting calibrated confidence scores from language models fine-tuned with human feedback. EMNLP 2023. arXiv:2305.14975.
- Wang, Z., & Busemeyer, J. R. (2013). A quantum question order model supported by empirical tests of an a priori and precise prediction. *Topics in Cognitive Science, 5*(4), 689–710. doi:10.1111/tops.12040.
- Wilde, M. M., & Mizel, A. (2012). Addressing the clumsiness loophole in a Leggett-Garg test of macrorealism. *Foundations of Physics, 42*(2), 256–265. doi:10.1007/s10701-011-9598-4.
- Xiao, H., Patil, V., Lee, H., Stengel-Eskin, E., & Bansal, M. (2026). Generalized correctness models. ICML 2026. arXiv:2509.24988.
- Xiong, M., et al. (2024). Can LLMs express their uncertainty? An empirical evaluation of confidence elicitation in LLMs. ICLR 2024. arXiv:2306.13063.

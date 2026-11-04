# Biomimetic map: how biological belief-resolution mechanisms fit the measured fingerprint

Written 2026-11-04 (America/Denver), after the standing summarised in `paper/record.md` (`de38306`, 23:17). This is a docs-only scan: nothing was run and no API was called. Every number below comes from `results/` or `paper/`. The cost figures are arithmetic on the repository's own per-call rates, and each one says which rate it uses. The literature was checked by web search on 2026-11-04.

**Citations.** Every paper below was found by web search, and its bibliographic record and abstract-level claims were confirmed. None was read in full here, so every citation in this file counts as [abs] in the sense of `paper/gold-map.md`. Treat specific effect sizes from the literature as provisional until the papers are read.

**What "mechanism" means here.** A transformer has no basal ganglia and no NMDA reverberation. Each biological mechanism is used as a *functional* hypothesis: a computation with a behavioural signature. Each test asks whether claude-haiku-5-5 shows that signature. A pass would say the model implements the same computation, not that it shares the biology.

---

## 1. The fingerprint, stated from the repository

The brief lists six features. Two of them are weaker in the record than the one-line summary suggests, so each feature below says what was measured and what was only inferred. Two constraints from the record are added (C1, C2), because several mechanisms stand or fall on them.

| id | feature | evidence (repo) | status |
|---|---|---|---|
| **F1** | Judgment is constructed at ask time, with large graded order effects | Exp 5: the main-rating means span a median of **24.7 points** across orders and omissions; 60 of 80 (S, M) pairs have OE > 0.10. Run 2 on one scale: 12 of the 16 large pairs survive (`bffc4ab`). Relabelling the scale moves the baseline from 33.8 to 71.3 (exp 5 run 1). | measured |
| **F2** | Self-anchoring on its own prior answer | Exp 4 run 2: "static twin with anchoring", but the estimator is near-tautological (D19). Exp 5: the main question repeated after a chain lands within 5 points 84% of the time (MF). The belief-adjustment model BA5 predicts main ratings best (827 against A5's 873; Δ = −46 [−94, +14], so the interval includes 0). | **inferred, not isolated.** Run 3 could not test it, and the planted-own-answer condition (gold map §2) has not been run |
| **F3** | Resistance, and some reactance, to another person's provided rating | Exp 4 run 3 (`de38306`): the accept rate is 0% in 15 of 32 item-orders, and revisions return close to the model's own value. In 6 item-orders a higher anchor gave a *lower* first rating, down to −0.50 (co-lin10, X first). The manipulation check passed in both orders on 1 of 16 items. r₂ > r₁ in at most 10% of conversations. | measured (resistance robust; reactance in 6 of 32 item-orders) |
| **F4** | Stated confidence is the best error signal on two models | Haiku run 2: G = 0.82 [0.71, 0.90], above every structural arm. Haiku locked test: G = 0.83 (A2 0.83, F2 0.84). Sonnet: G = 0.91, the same as A2 (0.90; +0.008). | measured: **best or tied-best**. It strictly beats the structural readings only on Haiku run 2 |
| **F5** | Weakly held claims tilt the vote through a per-claim readout angle | The F2+ readout P(yes) = (1 + sin θ cos φ cos α + cos θ sin α)/2 mixes each claim's uncommitted component (cos θ, large at low confidence) into its vote. F2+ − F2 = +0.082 [+0.045, +0.120] on Sonnet's pool and +0.088 [+0.014, +0.167] on Haiku's run-2 held-out set, but +0.009 [−0.057, +0.065] on Haiku's locked test. | measured on 2 of 3 sets; **one of the two positive sets is Sonnet's** |
| **F6** | Graded ratings are dispersive where yes/no answers are deterministic | Exp 3: 85% of items give the same yes/no answer in all 5 runs, and the order effect is not significant (permutation p = 0.243). Exp 4 run 1: the binary phase saturated. Graded: the B0 between-repeat SD is 7.1 points on one scale (exp 5 run 2). But in exp 4 run 2, repeats barely vary (SD 0.00–0.05 on the 0–1 scale). | measured. The robust contrast is **order effects in graded form, none in yes/no**. Graded *repeat* noise depends on the item and the design |
| **C1** | No interference; a classical Markov chain suffices | Kvam Δ_K = +0.29 [−1.12, +1.65]. One-scale q = −0.146 [−0.439, +0.137], so QQ is not supported. The dephased Markov D5 matches A5 (+3.8 [−21.8, +30.9] on the test chains). | measured |
| **C2** | Couplings between claims carry nothing | A2(κ=0) − A2 = −0.009 (Haiku) and −0.006 (Sonnet). A5 with κ = 0 costs +24.4 [−8.0, +60.5] on the test chains. | measured |

---

## 2. Ranking

The match column counts the features above, scored as ✔ (predicted), ~ (partly or under an extra assumption), ✗ (contradicted) or · (silent). "Discrimination" rates how sharply the cheapest test separates this mechanism from the others in this file, weighed against its cost.

| rank | mechanism | match (✔ / ~ / ✗) | key failure | cheapest discriminating test | cost | discrimination |
|---|---|---|---|---|---|---|
| 1 | **Serial dependence:** attraction to one's own past decisions, repulsion from past stimuli | F1 ✔ F2 ✔ F3 ✔/~ C1 ✔ (4 / 1 / 0) | silent on F4–F6. The repulsion literature is perceptual adaptation, so the mapping to a stated number is analogical | The run-3 anchors planted as the model's **own** earlier answer, against the archived "another person" condition | ≈ $0.23 | **high:** it is the only account here that predicts a sign flip by source at a fixed value |
| 2 | **Sampling:** probability theory plus noise, the Bayesian sampler, resource-rational anchoring | F1 ✔ F2 ✔ F6 ✔/~ C1 ✔ F4 ~ F5 ~ F3 ✗ (4 / 3 / 1) | it predicts assimilation to provided anchors, and run 3 shows resistance | The Costello–Watts identity P(A) + P(B) − P(A∧B) − P(A∨B) ≈ 0 on the exp-4 items | ≈ $0.05 | **high:** the prediction is parameter-free |
| 3 | **Confidence-gated confirmation bias** | F2 ✔ F4 ✔ F1 ~ F3 ~ C1 ~ (2 / 3 / 0) | reactance is not predicted, and K1 ≈ K0 shows no commitment boost on average | Archived run-3 calls: asymmetric uptake of confirmatory against disconfirmatory anchors, growing with the item's extremity | $0 | medium (anchor clipping at 2/98 confounds it) |
| 4 | **Predictive coding with precision weighting** | F4 ✔ F5 ✔ C1 ✔ F2 ~ F3 ~ F1 ✗ (3 / 2 / 1) | plain precision-weighted fusion commutes, so it predicts no order effects | A base-rate prime on the 160 exp-5 claims: does the shift track the claim's stated confidence (precision) or its repeat SD (samples)? | ≈ $0.15–0.25 | medium |
| 5 | **Two-stage drift diffusion (2DSD)** and bounded accumulation | F4 ✔ F6 ✔ C1 ✔ F1 ~ F2 ~ F3 ✗ (3 / 2 / 1) | it has no social term | Arm G with an item-reconsideration turn, against a matched filler, before the confidence rating | ≈ $0.10 | medium (it shares the prediction with second-order metacognition) |
| 6 | **Second-order metacognition** (Fleming & Daw) | F4 ✔ F2 ~ (1 / 1 / 0) | silent on everything except confidence | Gold map §1: self against other judges on the same answers | ≈ $0.9–2 | **high** (but it is the costliest test) |
| 7 | **Lateral inhibition, winner-take-all, leaky competing accumulator** | F1 ✔ F2 ✔ F6 ✔ C1 ✔ F3 ✗ C2 ✗/· (4 / 0 / 2) | inter-claim competition is absent (C2) | Serial-position weights from the O1–O4 Latin square ($0), then a primacy-to-recency test over chain length | $0 + ≈ $0.2 | medium-low |
| 8 | **Active inference:** epistemic action | F4 ~ F5 ~ (0 / 2 / 0) | no fingerprint feature tests its core claim | Gold map §4: EIG-scored menus of checks drawn from the model's own claim webs | ≈ $0.10 | medium (the EIG relies on our own fitted D5/BA5) |
| 9 | **Divisive normalization** | F1 ✔ F3 ✔ F2 ✗ (2 / 0 / 1) | it predicts contrast, not assimilation to the model's own answers | Archived single-scale QQ conversations: does M move *against* the level of the preceding S rating? | $0 | low (content-confounded, 20 pairs) |
| 10 | **Basal-ganglia action selection** (with STN "hold your horses") | F6 ✔ F4 ~ (1 / 1 / 0) | the fingerprint is about graded belief, not gated action | A "not yet" option on the yes/no items: does abstention track web conflict beyond stated confidence? | ≈ $0.02 | low |

**How the order was set.** Match rank and discrimination rank were summed (match order 1 sampling, 2 serial dependence, 3 2DSD, 4 precision, 5 confirmation, 6 LCA, 7 normalization, 8 second-order, 9 active inference, 10 basal ganglia; discrimination order 1 serial dependence, 2 sampling, 3 second-order, 4 confirmation, 5 precision, 6 active inference, 7 2DSD, 8 LCA, 9 normalization, 10 basal ganglia). Ties were then broken by test cost.
- Serial dependence and sampling tie at 3. Serial dependence goes first because its test also delivers the planted-own-answer condition that the record names as the next step (`paper/record.md`, last row; gold map §2).
- Confirmation and precision tie at 9. Confirmation goes first because its test costs $0.

---

## 3. Mechanism by mechanism

### 3.1 Serial dependence: attraction to one's own decisions, repulsion from stimuli (rank 1)

**The biology.**
- Perceived orientation is pulled toward recent input, through a "continuity field" (Fischer & Whitney 2014, *Nat. Neurosci.* 17:738, doi:10.1038/nn.3689).
- Fritsche, Mostert & de Lange (2017, *Curr. Biol.* 27:590, doi:10.1016/j.cub.2017.01.006) dissociated two opposite biases. Decisions are **attracted toward the previous decision**, while perception is **repelled from the previous stimulus**, as in the tilt aftereffect. The attraction grew when a longer interval separated perception from decision, which they read as working memory drifting toward recent history.
- Fritsche et al. (2020, *eLife*, 10.7554/eLife.55389) model the two biases together as a Bayesian, efficient observer.

**What it predicts for the fingerprint.**
- **F2 ✔:** attraction to the model's own prior answers. This is consistent with MF's 84% replicability and with BA5's lead, but it has not been isolated (see §1).
- **F3 ✔/~:** repulsion from an externally presented value. That is what the 6 contrast item-orders of run 3 show. Flat resistance (the 0% accept rate in 15 item-orders) is the zero-weight case, not repulsion, so it is only partly predicted.
- **F1 ✔:** order effects are history dependence. **C1 ✔:** the account is classical.

**Where it fails.**
- It is silent on F4–F6.
- The biological repulsion is low-level sensory adaptation. A number that "another person estimated" is not a stimulus feature, so the mapping is an analogy that the test must earn.
- Repulsion appeared in only 6 of 32 item-orders.

**What it uniquely predicts.** The **same value** in the transcript should pull the model's rating toward itself when it is framed as *the model's own* earlier answer, and push it away (or be ignored) when it is framed as *another person's* estimate. The attraction to its own answer should also grow with the number of intervening turns (the Fritsche delay effect).

None of the other mechanisms predicts a sign flip by source at a fixed value:
- confirmation bias predicts attraction to its own answer and *zero* weight on the other's;
- precision weighting and anchoring-and-adjustment predict non-negative weights for both sources;
- normalization predicts contrast for both sources.

**Cheapest test.**
- **Design:** run 3's 16 items with its frozen anchors (`experiments/exp4-run-3-anchors.json`, the same A_lo and A_hi values) and its anchored cells. Turn 1 changes: the anchor appears as a prior assistant turn ("rate X" → A), and the model is then asked to rate X again (r₁). The conjunction rating follows as in run 3.
- **Comparison:** compare the slope dr₁/dA, and its sign per item-order, with run 3's archived "another person" condition. That condition needs no rerun.
- **Optional lag arm:** three filler turns (K0's "continue") between the planted answer and the re-rating.
- **Pass:**
  - the own-answer slope is positive, with a CI excluding 0, across items;
  - **and** on the 6 item-orders that showed contrast in run 3, the sign is opposite between the two conditions;
  - **and** (with the lag arm) attraction is larger with lag.
- **Fail:** the model also resists its own planted answer. That would remove the decisional-attraction leg, and with it most of the evidence for F2.

**Cost.** The anchored cells are 16 × 4 × 40 × 2 = 5,120 calls. At run 3's rate ($0.30 for 6,720 calls) that is about **$0.23**. The lag arm at R = 20 adds about $0.12. The design should share a pre-registration with gold map §2.

### 3.2 Sampling: probability theory plus noise, the Bayesian sampler, resource-rational anchoring (rank 2)

**The biology and its cognitive models.**
- **Neural sampling.** Cortex may represent uncertainty with samples, which would explain neural variability and bistable perception (Fiser, Berkes, Orbán & Lengyel 2010, *Trends Cogn. Sci.* 14:119, doi:10.1016/j.tics.2010.01.003).
- **Probability theory plus noise.** Probability judgments read out noisy recalled instances. Conservatism and the conjunction and disjunction fallacies come from the noise. In particular expressions the noise cancels, and probability theory reappears (Costello & Watts 2014, *Psych. Rev.* 121:463, doi:10.1037/a0037010).
- **The Bayesian sampler.** It adds a generic prior to a small sample. It makes the same mean predictions as PT+N for simple events, conjunctions and disjunctions, and different ones for conditionals and for the distributions of estimates (Zhu, Sanborn & Chater 2020, *Psych. Rev.* 127:719, doi:10.1037/rev0000190).
- **Resource-rational anchoring.** Anchoring-and-adjustment is a sampler that starts from an anchor and stops early. It covers both self-generated and provided anchors (Lieder, Griffiths, Huys & Goodman 2018, *Psychon. Bull. Rev.* 25, doi:10.3758/s13423-017-1286-8).

**What it predicts.**
- **F1 ✔:** the judgment is built at query time from a few samples, and the earlier context biases where the sampler starts.
- **F2 ✔:** the sampler starts from the model's own last answer and adjusts insufficiently.
- **F6 ✔/~:** a yes/no answer is effectively a majority over samples, so it is deterministic whenever p is far from 0.5, while a graded rating carries the sampling noise (B0 repeat SD 7.1 points). But exp 4 run 2's near-zero repeat SD (0.00–0.05) is not what a small sample predicts unless the items sit near 0 or 1. Several of them do (P(Y) of 0.04–0.10), so this is ~, not ✗.
- **C1 ✔:** the account is classical.
- **F4 ~:** sample agreement gives a confidence signal.
- **F5 ~:** the generic prior shrinks weak evidence toward a default. That is shaped like F2+'s tilt, but the account does not specify it per claim.

**Where it fails.** **F3 ✗.** Lieder et al.'s model is built to explain assimilation to provided anchors, and run 3 shows resistance and some contrast. The sampler account would need a source-dependent starting rule, which is serial dependence's claim (§3.1).

**What it uniquely predicts.** For the same propositions, Z = P(A) + P(B) − P(A∧B) − P(A∨B) averages to 0, because the noise terms cancel, even on items where conjunction fallacies occur. Heuristic accounts of the fallacies predict a systematic Z ≠ 0; that is Costello & Watts' argument. Among the mechanisms here, only this family makes a parameter-free equality prediction about graded ratings. (The quantum QQ equality was the project's other one, and it is not supported on one scale.)

**Cheapest test.**
- **Design:** the 16 exp-4 items, rating X, Y, X∧Y and X∨Y alone, one scale direction (D33), R = 20. That is 1,280 single-turn calls.
- **Pass:** the item-bootstrap CI of mean Z lies within a pre-registered band around 0, while P(X∧Y) > min(P(X), P(Y)) on the run-2 fallacy items.
- **Fail:** Z is reliably non-zero.
- **Free first look:** the Bayesian sampler's variance–mean relation (between-repeat SD largest mid-scale) on the archived single-scale B0 conversations. This is weak, because floor and ceiling effects predict the same shape.

**Cost.** About **$0.05**, at exp 4 run 2's rate ($0.04 for 1,120 calls).

### 3.3 Confidence-gated confirmation bias (rank 3)

**The biology.**
- **Confidence gates post-decision evidence.** After a high-confidence decision, MEG shows confirmatory evidence amplified and disconfirmatory evidence processing abolished (Rollwage, Loosen, Hauser, Moran, Dolan & Fleming 2020, *Nat. Commun.* 11:2634, doi:10.1038/s41467-020-16278-6).
- **Choice raises sensitivity to consistent evidence.** After a choice, sensitivity to later evidence rises when that evidence agrees with the choice. A selective-gain model fits best (Talluri, Urai, Tsetsos, Usher & Donner 2018, *Curr. Biol.* 28:3128, doi:10.1016/j.cub.2018.07.052).
- **LLM precedent.** Kumaran et al. (arXiv:2507.03120) found a choice-supportive bias in GPT-4o and o1-preview, *but* also overweighting of contradictory advice. The second part runs opposite to our F3, on other models.

**What it predicts.**
- **F2 ✔:** choice-supportive persistence.
- **F3 ~:** resistance to a contradicting estimate ✔. Reactance ✗, because gating abolishes disconfirming evidence and does not reverse it.
- **F4 ✔:** confidence is a working internal variable, because it is the gate.
- **F1 ~:** order effects arise if earlier answers act as commitments.

**Where it fails.**
- **C1 ~.** In exp 5, an explicit mid-chain choice (K1) leaves the final confidence where the filler (K0) leaves it: Δ_K = +0.29 [−1.12, +1.65]. If commitment amplified the choice-consistent evidence that followed, confidence should rise on average. This is not decisive, because the effect is about *weighting* and could net out, but it counts against.

**What it uniquely predicts.** Uptake of a provided estimate is **asymmetric**: higher when the estimate agrees with the model's lean (more extreme on the same side) than when it contradicts it. The asymmetry **grows with the model's confidence**. No other mechanism here makes uptake depend on the agreement × confidence interaction.

**Cheapest test, at $0, on archived data.**
- **Data:** `results/exp4-run-3-calls.json` records A, r₁ and the accept/revise decision per conversation. `results/exp4-run-3.json` gives each statement's own mean.
- **Code each anchor** as confirmatory (on the side of 50 the model already leans to, but further out) or disconfirmatory. Regress uptake (r₁ − own)/(A − own) on that code × |own − 50|.
- **Confound to pre-register:** anchors were clipped at 2 and 98 (A_lo = max(2, m − 30), A_hi = min(98, m + 30)). On extreme items the confirmatory anchor is therefore closer, so the displacement |A − own| must be a covariate.
- **Second $0 look:** the 450 archived K1 conversations record the choice and the S₃ and S₄ ratings that follow it. Talluri predicts that S₃ and S₄ move M more when the claim-web labels make them consistent with the choice than in K0.
- **Both analyses must be pre-registered before the archive is opened for them.**

### 3.4 Predictive coding with precision weighting (rank 4)

**The biology.**
- **Precision as gain.** Prediction errors are weighted by their estimated precision, encoded as synaptic gain. Attention is the inference of precision (Feldman & Friston 2010, *Front. Hum. Neurosci.* 4:215, doi:10.3389/fnhum.2010.00215).
- **The hierarchy.** Rao & Ballard (1999) proposed the hierarchical predictive-coding scheme behind it; that paper was not fetched here.

**What it predicts.**
- **F5 ✔, a formal match.** Under precision weighting, a low-precision claim's estimate falls back to the prior. F2+'s readout does exactly that. As a claim's confidence falls (cos θ grows), its vote moves toward the fixed value (1 + sin α)/2. So the fitted tilt α is a prior mean toward which weakly held claims are shrunk.
- **F4 ✔:** confidence is the precision estimate.
- **F3 ~:** the other person's estimate is weighted low relative to the model's own (resistance ✔). But precision weights are non-negative, so reactance ✗.
- **C1 ✔:** the account is classical.

**Where it fails.** **F1 ✗ in its plain form.** Fusing Gaussian evidence with fixed precisions is commutative: the posterior does not depend on order. 60 of 80 pairs with order effects need precisions that change with context or time (volatility, leak). With that extension, the account no longer predicts the *direction* of an order effect.

**What it uniquely predicts.**
- A prior manipulation should move a claim's rating in proportion to the claim's **imprecision**: weak claims move, confident ones do not.
- The relevant measure of precision is the model's *stated or extracted confidence*.
- The Bayesian sampler (§3.2) predicts the same shrinkage, but driven by sample count, which shows up as between-repeat variability. The two can be told apart.

**Cheapest test.**
- **Design:** the 160 exp-5 chain claims, each rated alone under two base-rate primes ("most statements in this set are true" / "… false"), one scale, R = 10. That is 3,200 single-turn calls.
- **Statistic:** regress the prime-induced shift on the claim's extracted confidence (the θ the encoders use) and on its between-repeat SD, jointly.
- **Pass (precision):** confidence predicts the shift with the SD held fixed.
- **Pass (sampler):** the SD predicts it with confidence held fixed.

**Cost.** About **$0.15–0.25**. The low end uses the archived single-turn B0 cost of about $3.9 × 10⁻⁵ per call. The high end uses exp 5 run 2's $0.14 for 1,700 conversations.

### 3.5 Two-stage drift diffusion and bounded accumulation (rank 5)

**The biology and its models.**
- **2DSD.** Choice is a bound crossing in a sequential-sampling process, and confidence is read out after further post-decision accumulation. One process accounts for choice, decision time and confidence (Pleskac & Busemeyer 2010, *Psych. Rev.* 117:864, doi:10.1037/a0019737).
- **Time informs certainty.** In monkey LIP and in behaviour, certainty is informed by both the evidence and the elapsed decision time (Kiani, Corthell & Shadlen 2014, *Neuron* 84:1329, doi:10.1016/j.neuron.2014.12.015).
- **The quantum alternative.** Kvam, Pleskac, Yu & Busemeyer (2015, *PNAS* 112:10645, doi:10.1073/pnas.1500688112) found that a choice changes later confidence in humans. That interference favours a quantum walk over a Markov walk.

**What it predicts.**
- **F6 ✔:** a bound crossing with strong drift gives a near-deterministic yes/no answer, while a graded readout of the accumulator state keeps its variability.
- **F4 ✔:** confidence computed from the same accumulator carries accuracy information.
- **C1 ✔, notably.** Exp 5 reproduces Kvam's design (K1 against K0) and finds no interference (Δ_K ≈ 0). That is the Markov random walk's prediction, not the quantum walk's, and D5 (a Markov chain) matches A5. On this point Haiku behaves *unlike* Kvam's human participants.
- **F1, F2 ~:** these need the next question's starting point to be set by the last state.

**Where it fails.** **F3 ✗:** it has no term for a social estimate. **F5 ·:** it has no per-claim structure.

**What it uniquely predicts.** Confidence resolution improves with post-decision processing *of the same item*. An interval filled with unrelated activity should not improve it, whereas a pure elapsed-time cue would predict a change either way.

**Cheapest test.**
- **Design:** arm G on Haiku's run-2 set (40 wrong, 40 right). Ask for confidence (a) immediately (archived), (b) after one turn asking the model to reconsider the evidence for its answer, and (c) after a length-matched filler (K0's "continue").
- **Pass:** AUROC(b) > AUROC(a) ≈ AUROC(c).
- **Weakness:** second-order metacognition (§3.6) also predicts that (b) improves. What separates them is (c) together with §3.6's self/other test.

**Cost.** 80 items × R = 5 × 2 new conditions = 800 calls, at arm G's archived rate of about $7 × 10⁻⁵ per call (`results/arm-g-confidence.json`), plus longer outputs in (b). About **$0.10**.

### 3.6 Second-order metacognition (rank 6)

**The model.** Fleming & Daw (2017, *Psych. Rev.* 124:91, doi:10.1037/rev0000045) treat self-evaluation as second-order inference about a coupled but distinct decision system. It can use internal states that never reach the choice, including the agent's own actions. First-order models, by contrast, use one internal state for both the choice and the confidence.

**What it predicts.** **F4 ✔:** confidence beats structural readings of the visible text. That holds on Haiku run 2 and is tied elsewhere. **F2 ~:** one's own actions feed self-evaluation.

**Where it fails.** It is silent on F1, F3, F5 and F6.

**What it uniquely predicts.** Self-confidence beats a different judge's confidence *on the same answer text*. A first-order, text-reading account predicts parity. This is gold map §1's question, and §1 lists the mixed literature.

**Cheapest test.** Gold map §1's 2×2 cross-rating. Sonnet rating Haiku's 300 answers at the D28 rate (about $0.003 per call) costs about $0.90. Haiku's 298 calls on Sonnet's answers cost well under $0.05. With the paraphrase control, the total is about **$2**.

### 3.7 Lateral inhibition, winner-take-all, leaky competing accumulator (rank 7)

**The biology and its models.**
- **Attractor competition.** Slow NMDA-mediated recurrent excitation plus feedback inhibition gives attractor dynamics that amplify the difference between conflicting inputs into a binary choice (Wang 2002, *Neuron* 36:955).
- **The LCA.** Usher & McClelland (2001, *Psych. Rev.* 108:550, doi:10.1037/0033-295x.108.3.550) add leak and mutual inhibition to accumulation, and diffusion is a special case.
- **Primacy and recency.** The LCA gives **primacy** when inhibition is strong relative to leak, and can move to **recency** as the evidence stream lengthens, which bounded diffusion cannot (Tsetsos, Gao, McClelland & Usher 2012, *Front. Neurosci.* 6:79, doi:10.3389/fnins.2012.00079).

**What it predicts.**
- **F6 ✔:** categorical output from an attractor.
- **F2 ✔:** attractor persistence (hysteresis).
- **F1 ✔:** order effects with a primacy or recency signature.
- **C1 ✔:** the account is classical.

**Where it fails.**
- **C2 ✗/·.** If the competing units are the model's *claims*, the record already contradicts the account: the inter-claim couplings fit near zero, and removing them costs nothing on three comparisons. If the competing units are only the two answers, the C2 contradiction falls away, but the account reduces to bounded diffusion (§3.5) and adds nothing of its own.
- **F3 ✗:** there is no social term.

**What it uniquely predicts.** A transition from primacy to recency in the serial-position weights as the chain lengthens.

**Cheapest test.**
- **Free step:** estimate each position's weight on M from the archived O1–O4 conversations, a Latin square with each S in each position once. Predictions: primacy (LCA with inhibition dominant, or bounded diffusion), recency (Hogarth–Einhorn step-by-step adjustment), or flat (a perfect integrator).
- **Unique step:** chains of length 2, 4 and 8 on 20 items, forward and reversed, R = 10. That is 1,200 conversations, about $0.2 at exp 5 run 1's rate ($1.93 for 12,600 conversations).

### 3.8 Active inference (rank 8)

**The theory.**
- **Choice by expected free energy.** Agents choose by minimising expected free energy, which includes epistemic value (information gain) alongside extrinsic value. Precision updates in the simulations resemble dopaminergic responses (Friston, Rigoli, Ognibene, Mathys, FitzGerald & Pezzulo 2015, *Cogn. Neurosci.* 6:187, doi:10.1080/17588928.2015.1020053).
- **Generative models are passive.** That claim is from Pezzulo et al. (2024), as cited in gold map §4.

**What it predicts.** Its perceptual half is §3.4: **F4 ~** and **F5 ~**. Its distinctive half concerns *action*, and none of the fingerprint's measurements involves the model choosing what to observe.

**Where it fails.** It cannot fail on the present data. That is the problem: its match is untested, not good.

**What it uniquely predicts.** Given a menu of checks on its own claims, the model picks the one with the highest expected information gain about its own main answer, over the confirmatory check.

**Cheapest test.** Gold map §4, about **$0.10**. Its weakness is that the EIG is computed under our fitted D5 and BA5 models, so a fail could be a failure of those models.

### 3.9 Divisive normalization (rank 9)

**The biology.** Value coding in neurons is normalised by the context, and normalised value plus noise produces context-dependent choice in monkeys and people (Louie, Khaw & Glimcher 2013, *PNAS* 110:6139, doi:10.1073/pnas.1217854110).

**What it predicts.** **F1 ✔:** context effects. **F3 ✔:** contrast, where a high context value lowers the rating, which matches the 6 contrast item-orders.

**Where it fails.** **F2 ✗.** Normalization predicts contrast for every context value, including the model's own earlier answers, but F2 (as inferred) is assimilation.

**What it uniquely predicts.** Context acts *divisively*: a high-valued context should compress the differences between later ratings, not shift them.

**Cheapest test, at $0.** Use the single-scale QQ conversations (run 2's 20 pairs, plus run 1's anchor-(a) subset). Ask whether M rated after S moves *against* the level of the S rating (contrast) or toward it (assimilation).
- **Weaknesses:** the content relation between S and M confounds the sign. The claim-web support/conflict label must be a covariate, and 20 pairs give little power.

### 3.10 Basal-ganglia action selection (rank 10)

**The biology and its models.**
- **A central switch.** The basal ganglia act as a central selection device that resolves conflicts over limited resources (Redgrave, Prescott & Gurney 1999, *Neuroscience* 89:1009).
- **Optimal selection.** The cortico-basal-ganglia circuit implements the asymptotically optimal multi-hypothesis sequential test, MSPRT (Bogacz & Gurney 2007, *Neural Comput.* 19).
- **Holding under conflict.** The subthalamic nucleus raises the decision threshold in proportion to conflict, a "hold your horses" pause (Frank 2006, *Neural Netw.* 19:1120).

**What it predicts.** **F6 ✔:** selection gates one answer, giving deterministic yes/no output. **F4 ~:** MSPRT tracks a posterior.

**Where it fails.** It is silent on F1, F2, F3 and F5. Its learning half (dopaminergic reward-prediction errors) needs training, which this stack cannot do.

**What it uniquely predicts.** *Conflict* among the model's own claims, rather than low confidence, delays commitment.

**Cheapest test.**
- **Design:** the exp-3 items' main question with a third option, "not yet: I need more evidence", R = 10. That is about 400 calls, about **$0.02** at exp 4 run 2's rate.
- **Statistic:** regress the abstention rate on the archived web-conflict score with stated confidence G held fixed.
- **Discrimination is low.** A confidence-based abstention rule predicts most of the same pattern.

---

## 4. What no mechanism here explains

- **The scale-relabelling gap (33.8 against 71.3).** This is a failure to read the instruction, not a way of resolving a conflict, and none of the mechanisms speaks to it. D33's one-scale designs control for it rather than explain it.
- **The scale wording shrinks order effects** (exp 4 run 3: Marta from about +0.10 to +0.02 under explicit wording). This sensitivity to wording should be recorded in any test above that reuses the exp-4 items.
- **F5 on Haiku's locked test.** The readout tilt adds nothing there (+0.009). Every mechanism that claims F5 (§3.2, §3.4) must explain why the tilt helps on Sonnet's pool and on Haiku's run-2 held-out set but not on Haiku's locked test. None does yet.

## 5. Recommended order

1. **The three $0 analyses, each pre-registered before its archive is opened:** confirmation asymmetry on the run-3 calls (§3.3), serial-position weights from O1–O4 (§3.7), and the contrast sign on the single-scale QQ data (§3.9).
2. **The planted-own-answer test (§3.1, ≈ $0.23)** together with **the PT+N identity (§3.2, ≈ $0.05)**. Together they take the two top-ranked mechanisms to opposite-signed, parameter-free predictions for under $0.30. §3.1 should share a pre-registration with gold map §2.
3. **The prime × confidence test (§3.4)** and **the reconsider/filler test (§3.5)**, about $0.35 together.
4. **Gold map §1 (§3.6) and §4 (§3.8)**, as already costed there.

**What I would not do.** Build a biologically detailed model (a spiking WTA network, or a basal-ganglia loop) and fit it to these ratings. The record's lesson from the quantum encodings applies here too: a flexible model that fits sequential ratings ties a matched classical twin. Only the parameter-free or sign-flip predictions above can discriminate.

---

## Sources (web search, 2026-11-04)

- Fischer & Whitney 2014: [PMC4012025](https://pmc.ncbi.nlm.nih.gov/articles/PMC4012025)
- Fritsche, Mostert & de Lange 2017: [summary](https://mindblog.dericbownds.net/2017/03/opposite-effects-of-recent-history-on.html); Fritsche et al. 2020: [eLife 55389](https://elifesciences.org/articles/55389v1)
- Costello & Watts 2014: [arXiv:1211.0501](https://arxiv.org/abs/1211.0501v2)
- Zhu, Sanborn & Chater 2020: [PMC7571263](https://pmc.ncbi.nlm.nih.gov/articles/PMC7571263)
- Lieder et al. 2018: [Springer](https://link.springer.com/article/10.3758/s13423-017-1286-8/fulltext.html)
- Fiser et al. 2010: [PMC2939867](https://pmc.ncbi.nlm.nih.gov/articles/PMC2939867)
- Rollwage et al. 2020: [PubMed 32457308](https://pubmed.ncbi.nlm.nih.gov/32457308/)
- Talluri et al. 2018: [Leiden repository](https://scholarlypublications.universiteitleiden.nl/access/item%3A3210260/view)
- Kumaran et al. 2025: [arXiv:2507.03120](https://arxiv.org/abs/2507.03120v1)
- Feldman & Friston 2010: [PMC3001758](https://pmc.ncbi.nlm.nih.gov/articles/PMC3001758)
- Pleskac & Busemeyer 2010: [eScholarship](https://escholarship.org/content/qt0wm9g74s/qt0wm9g74s.pdf)
- Kiani, Corthell & Shadlen 2014: [PMC4271191](https://pmc.ncbi.nlm.nih.gov/articles/PMC4271191)
- Kvam et al. 2015: [Phys.org coverage](https://phys.org/news/2015-08-cognitive-decision-collapse-quantum-superstate.amp); [Sci. Rep. follow-up](https://www.nature.com/articles/s41598-019-54383-9.pdf)
- Fleming & Daw 2017: [PMC5178868](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5178868/)
- Usher & McClelland 2001: [PubMed 11488378](https://pubmed.ncbi.nlm.nih.gov/11488378/)
- Wang 2002: [PDF](https://cenl.ucsd.edu/Jclub/Wang02.pdf)
- Tsetsos et al. 2012: [PMC3372959](https://pmc.ncbi.nlm.nih.gov/articles/PMC3372959)
- Friston et al. 2015: [PDF](https://www.fil.ion.ucl.ac.uk/~karl/Active%20inference%20and%20epistemic%20value.pdf)
- Louie, Khaw & Glimcher 2013: [PMC3625302](https://pmc.ncbi.nlm.nih.gov/articles/PMC3625302)
- Redgrave, Prescott & Gurney 1999: [White Rose](https://eprints.whiterose.ac.uk/107033)
- Bogacz & Gurney 2007; Frank 2006: [PMC3296967](https://pmc.ncbi.nlm.nih.gov/articles/PMC3296967) (citing both)

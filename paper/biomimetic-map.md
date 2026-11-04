# Biomimetic map: how biological belief-resolution mechanisms fit the measured fingerprint

Written 2026-11-04 (America/Denver), after the standing summarised in `paper/record.md` (`de38306`, 23:17). This is a docs-only scan: nothing was run and no API was called.
- Every fingerprint number below comes from `results/` or `paper/`.
- Literature numbers come from the cited papers and are marked as such.
- The test costs are arithmetic on the repository's own per-call rates, and each one says which rate it uses.

**Revision 2 (same day).** Every cited paper was then read in full, and the map was corrected (§6 lists every change). The full reads changed four of the original top five:
- **Serial dependence** loses its "unique sign flip by source" prediction. The papers never flip the sign by source. The original lag prediction was also backwards: attraction *decays* with lag.
- **The sampling family's** Z identity is exactly 0 only in the 2014 model. The versions that produce fallacies predict a non-zero, item-dependent Z.
- **Confidence-gated confirmation** gains an LLM precedent (Kumaran et al.): a self-consistency effect that disappears when the same answer is attributed to another model.
- **Precision weighting, as published,** already has time-varying precision, so it is not order-invariant.

The ranking in §2 is redone from scratch.

**Citations.** The §7 source list says, for each paper, the copy read and whether it was read in full.
- **Read in full:** 22 of the 23 papers.
- **Not obtained in full:** Pleskac & Busemeyer 2010 (2DSD). Its 2007 proceedings precursor was read in full instead, and every 2DSD-specific claim below is marked **[2010 unread]**.
- **Partial reads:** supplements were not read for Fritsche et al. 2017, Talluri et al. 2018, Rollwage et al. 2020 or Kvam et al. 2015. The Lieder et al. companion paper could not be obtained.

**What "mechanism" means here.** A transformer has no basal ganglia and no NMDA reverberation. Each biological mechanism is used as a *functional* hypothesis: a computation with a behavioural signature. Each test asks whether claude-haiku-5-5 shows that signature. A pass would say the model implements the same computation, not that it shares the biology.

---

## 1. The fingerprint, stated from the repository

The brief lists six features. Two of them are weaker in the record than the one-line summary suggests, so each feature below says what was measured and what was only inferred. Two constraints from the record are added (C1, C2), because several mechanisms stand or fall on them.

| id | feature | evidence (repo) | status |
|---|---|---|---|
| **F1** | Large graded order effects (read as judgment constructed at ask time) | Exp 5: the main-rating means span a median of **24.7 points** across orders and omissions; 60 of 80 (S, M) pairs have OE > 0.10. Run 2 on one scale: 12 of the 16 large pairs survive (`bffc4ab`). Relabelling the scale moves the baseline from 33.8 to 71.3 (exp 5 run 1). | measured |
| **F2** | Self-anchoring on its own prior answer | Exp 4 run 2: "static twin with anchoring", but the estimator is near-tautological (D19). Exp 5: the main question repeated after a chain lands within 5 points 84% of the time (MF). The belief-adjustment model BA5 predicts main ratings best (827 against A5's 873; Δ = −46 [−94, +14], so the interval includes 0). | **inferred, not isolated.** Run 3 could not test it, and the planted-own-answer condition (gold map §2) has not been run |
| **F3** | Low uptake of, and some reversal against, another person's provided rating | Exp 4 run 3 (`de38306`): the accept rate is 0% in 17 of 32 item-orders, and the first rating moves a median 9% of the way to the provided value. In 5 item-orders, all Linda-family items, a higher anchor gave a reliably *lower* first rating, down to −0.50 (co-lin10, X first). The manipulation check passed in both orders on 1 of 16 items. r₂ > r₁ in at most 10% of conversations. | measured (low uptake robust; reversal in 5 of 32 item-orders, all on three Linda-family items) |
| **F4** | Stated confidence is the best error signal on two models | Haiku run 2: G = 0.82 [0.71, 0.90], above every structural arm. Haiku locked test: G = 0.83 (A2 0.83, F2 0.84). Sonnet: G = 0.91, level with A2 (0.90; +0.008 [−0.061, +0.080]). | measured: **best or tied-best**. It strictly beats only the fixed v1 arms on Haiku run 2 (the learned A2.1 scores 0.84 there) |
| **F5** | Weakly held claims tilt the vote through a per-claim readout angle | The F2+ readout P(yes) = (1 + sin θ cos φ cos α + cos θ sin α)/2 mixes each claim's uncommitted component (cos θ, large at low confidence) into its vote. F2+ − F2 = +0.082 [+0.045, +0.120] on Sonnet's pool and +0.088 [+0.014, +0.167] on Haiku's run-2 held-out set, but +0.009 [−0.057, +0.065] on Haiku's locked test. | measured on 2 of 3 sets; **one of the two positive sets is Sonnet's** |
| **F6** | Graded ratings are dispersive where yes/no answers are deterministic | Exp 3: 85% of items give the same yes/no answer in all 5 runs, and the order effect is not significant (permutation p = 0.243). Exp 4 run 1: the binary phase saturated. Graded: the B0 between-repeat SD is 7.1 points on one scale (exp 5 run 2). But in exp 4 run 2, repeats barely vary (SD 0.00–0.05 on the 0–1 scale). | measured. The robust contrast is **large graded order effects against near-deterministic yes/no answers**; yes/no order effects appear in experiment 4 run 1's marginals but not in experiment 3's design. Graded *repeat* noise depends on the item and the design |
| **C1** | No interference detected; a classical Markov chain suffices | Kvam Δ_K = +0.29 [−1.12, +1.65] on folded confidence \|r − 50\|. One-scale q = −0.146 [−0.439, +0.137], so QQ is not supported. The dephased Markov D5 is not detectably behind A5 (+3.8 [−21.8, +30.9] on the test chains). | measured. **Literature comparison:** Kvam et al.'s human effect on the same folded statistic was −1.19 points (83.96 after a choice against 85.15 without one). The project's interval only barely excludes a raw effect that size, so C1 is *consistent with* a Markov walk; it does not rule out a human-sized interference effect |
| **C2** | Couplings between claims carry nothing detectable | A2(κ=0) − A2 = −0.009 (Haiku) and −0.006 (Sonnet). A5 with κ = 0 costs +24.4 [−8.0, +60.5] on the test chains. | measured |

---

## 2. Ranking (revision 2)

The match column scores each feature as ✔ (predicted, by the paper's own model), ~ (partly, or only under an extension the paper names but does not fit), ✗ (contradicted) or · (silent). "Discrimination" rates how sharply the cheapest test separates this mechanism from the others here, weighed against its cost.

| rank | mechanism | match | key failure | cheapest discriminating test | cost | discrimination |
|---|---|---|---|---|---|---|
| 1 | **Choice-dependent confirmation and self-consistency** (Rollwage, Talluri; LLM precedent Kumaran) | F2 ✔ F4 ✔ F3 ~ F1 ~ C1 ~ | reactance not predicted; Kumaran's LLMs *over*weight opposing advice and show "no confirmation bias" | **The source × distance × lag test (§3.0):** own-planted against other-attributed answers | ≈ $0.46 (shared) | high: own > other, with no decay over lag |
| 2 | **Serial dependence** (Fischer & Whitney; Fritsche et al.) | F1 ✔ F2 ✔ C1 ✔ F3 ✗/~ | in F&W an attended value attracts *whether or not it was responded to*, so another person's number should attract; repulsion needs sensory adaptation | §3.0: attraction tuned to distance (rises, then falls or reverses) and **decaying** with lag | ≈ $0.46 (shared) | high: non-monotone distance tuning with decay over lag is unique to it |
| 3 | **Precision weighting** (Feldman & Friston) | F4 ✔ C1 ✔ F5 ~ F1 ~ F3 ~ F2 ~ | non-negative weights, so no reactance; time-varying precision allows order effects but does not predict their direction | A base-rate prime: does the shift track stated confidence or repeat SD? | ≈ $0.15–0.25 | medium |
| 4 | **Sampling:** PT+N, the Bayesian sampler, resource-rational anchoring | C1 ✔ F1 ~ F2 ~ F5 ~ F3 ~/✗ F6 ~/✗ | the basic sampler gives no order effects; anchoring never gives contrast | Item-level Z against P(X) + P(Y) − 1 on the exp-4 items | ≈ $0.05 | medium-high |
| 5 | **Lateral inhibition, WTA, LCA** | F1 ✔ F2 ✔ F6 ✔ C1 ✔ F3 ✗ C2 ✗/· | no inter-claim competition (C2) | Serial-position weights from O1–O4: the LCA cannot produce a U-shape | $0 | medium (it can falsify, not confirm) |
| 6 | **Bounded accumulation / 2DSD** | F4 ✔ F6 ✔ C1 ✔ F1 ~ F2 ~ F3 ✗ | no social term; its post-decision prediction is shared | Arm G: reconsider turn against a matched filler | ≈ $0.10 | low-medium |
| 7 | **Second-order metacognition** (Fleming & Daw) | F4 ~ F2 ~ C1 ✗ | it predicts *lower* confidence after a choice, which K1 ≈ K0 does not show | The archived K1/K0: does a choice raise M's sensitivity to the truth label? | $0 | medium |
| 8 | **Active inference** | F4 ~ F5 ~ | no fingerprint feature tests its core | Gold map §4's EIG menus, with fixed preferences | ≈ $0.10 | medium (preference-dependent) |
| 9 | **Basal-ganglia selection** | F6 ✔ F4 ~ | in the MSPRT, conflict *is* the low posterior | none cheap and valid on this stack | — | — |
| 10 | **Divisive normalization** | F1 ~ | the paper's context is simultaneous; sequential normalization is untested | Simultaneous-context compression of two target ratings | ≈ $0.05 | medium, but low relevance |

**How the order was set.** The match rank is a judgment weighted toward the central features (F1–F4, F6):

| match rank | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| mechanism | confirmation | precision | 2DSD | serial dependence | LCA | sampling | basal ganglia | active inference | second-order | normalization |

The discrimination ranks are serial dependence 1, confirmation 2, sampling 3, precision 4, LCA 5, second-order 6, active inference 7, 2DSD 8, normalization 9 and basal ganglia 10 (no valid cheap test).

Summing the two gives confirmation 3, serial dependence 5, precision 6, sampling 9, LCA 10, 2DSD 11, second-order 15, active inference 15, basal ganglia 17 and normalization 19. Second-order ranks above active inference on cost ($0).

**What moved, and why.**

| mechanism | revision 1 | revision 2 | reason |
|---|---|---|---|
| serial dependence | 1 | 2 | §3.2 |
| sampling | 2 | 4 | §3.4 |
| confirmation | 3 | 1 | it gains the LLM source precedent (§3.1) |
| 2DSD | 5 | 6 | — |
| LCA | 7 | 5 | its free test is a genuine falsification (§3.5) |
| second-order | 6 | 7 | it fails C1 (§3.7) |
| basal ganglia | 10 | 9 | normalization fell below it (§3.10) |
| normalization | 9 | 10 | its F1 and F3 claims are not in the paper (§3.10) |

---

## 3. Mechanism by mechanism

### 3.0 The shared test: source × distance × lag (≈ $0.46)

The full reads turned the top two mechanisms' tests into one design whose cells separate four accounts.

**Design.**
- **Items:** run 3's 16 items, one scale direction.
- **Turn 1:** a value V for the first conjunct, placed at a distance d ∈ {±10, ±30, ±60} from the item's own mean (clipped to 2–98). V appears in one of two framings:
  - **own:** a prior assistant turn ("rate X" → V), after which the model is asked to rate X again;
  - **other:** "another person estimated V", as in run 3.
- **Lag:** for the own framing, 0 or 3 filler turns (K0's "continue") before the re-rating.
- **Turn 2:** the conjunction, as in run 3.
- **Size:** R = 20.
- **Reused data:** run 3's archived "other" cells already cover d = ±30.

**What each account predicts.**

| account | own | other | as distance grows | as lag grows |
|---|---|---|---|---|
| **Stimulus-history serial dependence** (F&W: an attended but unresponded value attracts as strongly as a responded one, ±8.75° vs ±6.76°, P = 0.12) | attraction | attraction | rises, then falls; may reverse beyond the tuning width (repulsion beyond ~60° in Fritsche 2017) | **decays** (F&W 1-back ±8.19°, 3-back ±2.78°; eLife half-life about 4.5 s, with repulsion from items further back) |
| **Decision-history reading** (Fritsche 2017's inference) and **choice-dependent confirmation/self-consistency** (Talluri: the gain change is "linked to the participants' categorical choice"; Kumaran: the bias is "abolished" when the visible answer is attributed to another LLM) | attraction and resistance | ≈ 0 | — | **no decay**, because the answer stays in the transcript |
| **Precision weighting / anchoring-and-adjustment** (Lieder Eq. 4: E[x̂] ≈ a·rᵗ + (1 − rᵗ)·x) | uptake | uptake, smaller for a less trusted source | **monotone**, never reversing | — |
| **No mechanism read** (§4) | — | **repulsion** (run 3's 6 contrast item-orders) | — | — |

**Pass criteria (to pre-register).**
- **Source** (confirmation against stimulus history): own slope > other slope, with a CI excluding 0.
- **Distance shape** (serial dependence against linear accounts): a non-monotone own-uptake curve, with a significant quadratic term or a sign change at ±60.
- **Lag:** attraction falls with lag (serial dependence) or holds (self-consistency).

**Caveat from Kumaran.** A planted *wrong* own answer was abandoned 74.5% of the time in their LLMs. A ±60 own-plant is effectively a wrong answer, so self-consistency may break at large d for a reason other than serial-dependence tuning. The pre-registration should name this.

**Cost.**
- Own cells: 16 × 6 distances × 2 lags × 20 × 2 calls = 7,680 calls.
- New other cells (d = ±10, ±60): 16 × 4 × 20 × 2 = 2,560 calls.
- Total: 10,240 calls at run 3's rate ($0.30 for 6,720 calls), about **$0.46**. Dropping the lag arm halves the own cells, for about $0.28.
- The design should share a pre-registration with gold map §2.

### 3.1 Choice-dependent confirmation and self-consistency (rank 1)

**The papers, read in full.**
- **Rollwage et al. 2020** (*Nat. Commun.* 11:2634).
  - **Design:** dot motion → choice + confidence → post-decision dots → final choice and confidence.
  - **Result:** after high- against low-confidence decisions, confirmatory evidence was "facilitated" and disconfirmatory evidence "largely abolished" in MEG. The body text says "largely"; only the abstract says "abolished" without qualification.
  - **Three qualifiers:**
    - post-decision evidence always pointed the same way as the pre-decision evidence, so "disconfirmatory" occurs only after errors, which confounds consistency with accuracy;
    - the MEG confidence split was binary;
    - by the ±1 coding of the reported coefficients (initial decision β = 0.042, interaction β = 0.038), processing is roughly symmetric at low confidence.
  - **No reversal:** disconfirming evidence is never reversed.
  - **Behaviour:** across subjects, a larger confidence boost went with fewer changes of mind (r = −0.69).
- **Talluri et al. 2018** (*Curr. Biol.* 28:3128).
  - **Result:** after a choice, evidence consistent with it gets more weight and inconsistent evidence *less*, reduced but not zeroed. Consistency is defined by sign relative to the reference, not by how extreme the evidence is. A choice-linked selective-gain model beat a stimulus-based one. Confidence was never measured.
  - **Gaps:** No-Choice trials were run but excluded from analysis, and no externally cued choice was tested.
- **Kumaran et al. 2025** (arXiv:2507.03120; Gemma 3 12B and 27B, GPT-4o, o1-preview, DeepSeek 7B; **no Claude model**).
  - **Visible vs hidden answer:** for Gemma 3 12B, change of mind under opposing advice is 39.2% with its own answer shown against 85.0% with it hidden.
  - **Overweighting:** opposing advice is overweighted relative to a Bayesian observer (×2.44 to ×3.40); supporting advice is near normative.
  - **Their verdict:** "LLMs do not show a confirmation bias, at least under these experimental conditions." The effect is self-consistency: it is "abolished" when the visible answer is attributed to another LLM.

**What it predicts.**
- **F2 ✔:** persistence of the model's own answer. Kumaran shows this in other LLMs.
- **F4 ✔:** confidence acts as the gate (Rollwage).
- **F3 ~:** resistance ✔ for a high-confidence model. But Kumaran's LLMs *over*weight opposing advice, the opposite of Haiku's resistance, and no paper predicts reversal (reactance ✗).
- **F1 ~:** order effects arise if earlier answers act as commitments.
- **C1 ~:** Kvam et al. note that confirmation bias predicts *higher* confidence after a choice. Δ_K = +0.29 [−1.12, +1.65] does not show it.

**Unique prediction (revised).** The effect depends on whether the answer is the agent's *own*. The same value attributed to someone else should carry no persistence, and the effect does not decay with lag while the answer stays visible. This is §3.0's source and lag cells.

**What was dropped.** Revision 1 proposed a "confidence × agreement asymmetry" test on the archived run-3 calls ($0). It is not unique: on a bounded scale, Bayesian updating already gives asymmetric, confidence-dependent uptake (Kumaran Fig. 7), and Feldman & Friston's state-dependent precision does too. Recoded faithfully, it is also nearly empty. With consistency by sign relative to 50 (Talluri's definition), an item whose mean lies more than 30 points from 50 has both anchors on the same side. It survives only as a low-power $0 secondary.

The K1 analysis ("S₃/S₄ move M more when consistent with the choice") is not a Talluri prediction as published, because the choice/no-choice contrast was never reported. Bronfman et al. (2015, cited by Talluri) found sensitivity *generally reduced* after an overt choice. Dropped.

### 3.2 Serial dependence (rank 2)

**The papers, read in full.**
- **Fischer & Whitney 2014** (*Nat. Neurosci.* 17:738).
  - Perceived orientation is pulled toward the previous *stimulus* through a "continuity field".
  - Attraction is as strong after trials with no response (±8.75° against ±6.76°, P = 0.12), and it requires attention.
  - It decays over trials: 1-back ±8.19°, 2-back ±4.89°, 3-back ±2.78°, near 0 after that.
  - It is tuned as a derivative of a Gaussian, with a peak near 28° of difference.
- **Fritsche, Mostert & de Lange 2017** (*Curr. Biol.* 27:590).
  - **Repulsion:** 2AFC and equality *perceptual* judgments are repelled by the previous inducer (ΔPSE −1.40° at the same location against −0.42° elsewhere). This is retinotopic and resembles the tilt aftereffect, and the inducer was one participants had *just reproduced*.
  - **Attraction:** adjustment responses are attracted, with a peak near 17° (1.1–1.3°). They are repelled beyond about 60° of difference.
  - **"Toward previous decisions" is inferred, not regressed.** Every analysis regresses on previous stimuli. The decision reading comes from Exp 3, where previously seen 2AFC stimuli, judged on another dimension, exerted no pull (max −0.17°, p = 0.43).
  - **Delay effect:** attraction grew from 1.08° to 1.64° when the *within-trial* retention interval rose from 300 to 3,750 ms (p = 0.0235).
- **Fritsche, Spaak & de Lange 2020** (*eLife* 9:e55389).
  - **Attraction:** responses are attracted to the 1-back stimulus, with a half-life of about 4.5 s, "only clearly observable between adjacent trials".
  - **Repulsion:** responses are repelled by stimuli further back, peaking at 4-back (−1.07°) and lasting about 2 min, with a half-life of 20–40 s.
  - **Model:** a Bayesian efficient observer, with repulsion at "a low-level encoding stage" and attraction toward previous posteriors.
  - **Uncertainty:** attraction is stronger for more uncertain stimulus representations.

**What it predicts.**
- **F1 ✔:** order effects are history dependence.
- **F2 ✔:** attraction to the immediately preceding judgment.
- **C1 ✔:** the account is classical.
- **F3 ✗/~:**
  - In F&W, any *attended* value attracts whether or not it was responded to, which predicts that another person's number should *attract*: ✗.
  - Fritsche Exp 3 found seen-but-otherwise-judged stimuli simply ignored: ~ for resistance.
  - **Repulsion is not derivable.** It needs a sensory stimulus and a perceptual readout, and the sign flips with the measurement task, the lag and the difference between values, never with the source. Revision 1's "sign flip by source" is withdrawn.

**Unique prediction (revised).**
- Attraction to the model's own planted answer is **tuned to distance**: it rises, then falls, and may reverse at large d, unlike the monotone anchoring and precision accounts.
- It **decays with intervening turns**, and may turn repulsive.

Revision 1's lag prediction ("attraction grows with intervening turns") was the reverse of the literature. The Fritsche delay effect concerns the retention interval within the current trial. The faithful analogue is a delay between presenting the current item and asking for its rating, which a chat transcript cannot cleanly vary.

**The mapping is thin.** Orientation tuning widths (17–28°) have no defined counterpart on a 0–100 belief scale, so §3.0's distance grid is a guess at the scale of the tuning.

**Test.** §3.0's distance and lag cells.

### 3.3 Predictive coding with precision weighting (rank 3)

**The paper, read in full.** Feldman & Friston 2010 (*Front. Hum. Neurosci.* 4:215) is a simulation study, with no data.
- **Precision is gain:** "attention is the process of optimizing synaptic gain to represent the precision of sensory information (prediction error)".
- **Precision is dynamic and depends on state.** It is carried by hidden states that decay slowly, so a cue changes the weight given to a later target.
- **A confirmation-like effect:** a valid target "prevents the invalid target from reversing the precision bias established by the cue".
- **Weights are non-negative:** precision = exp(π).

**What it predicts.**
- **F4 ✔:** confidence is the precision estimate. Linking it to *error AUROC* is our mapping, not the paper's.
- **C1 ✔:** the account is classical.
- **F5 ~:** "a low-precision claim falls back to the prior", which F2+'s tilt resembles, is consistent with the framework but not stated in the paper.
- **F1 ~ (revised from ✗):** revision 1 said plain precision-weighted fusion commutes and so predicts no order effects. That is true only of static Gaussian fusion, which this paper does not use. Its time-varying precision makes it order-dependent by construction, but it does not predict the direction of an order effect.
- **F3 ~:** resistance ✔ (low weight on the other's estimate); reactance ✗ (weights are non-negative).
- **F2 ~:** a cue-established precision bias resists reversal.

**Unique prediction.** A prior shift moves weak claims more than confident ones, with the effect indexed by *stated confidence* (precision). The Bayesian sampler (§3.4) also predicts shrinkage, but indexes it by sample count, which appears as between-repeat variability.

**Test.**
- **Design:** the 160 exp-5 chain claims, each rated under two base-rate primes, one scale, R = 10. That is 3,200 single-turn calls.
- **Statistic:** regress the prime-induced shift on extracted confidence and between-repeat SD, jointly.
- **Cost:** about **$0.15–0.25**. The low end uses the archived B0 cost of about $3.9 × 10⁻⁵ per call; the high end uses exp 5 run 2's $0.14 for 1,700 conversations.

### 3.4 Sampling: PT+N, the Bayesian sampler, resource-rational anchoring (rank 4)

**The papers, read in full** (Lieder: author manuscript through the conclusion).
- **Costello & Watts 2014** (*Psych. Rev.* 121:463).
  - **Design:** one participant rates every query in one session, 0–100.
  - **The X_E identity:** E[P(A) + P(B) − P(A∧B) − P(A∨B)] = 0, "invariant … irrespective of the degree of co-occurrence or dependency".
  - **Observed X_E:** 0.66 (SD 27.1, n = 996) in Exp 1 and −3.90 (SD 27.7, n = 594) in Exp 2.
  - **Fallacy rates:** 40–51% conjunction and disjunction fallacies, which the model caps at 50%.
  - **Conservatism:** the mean estimate is P + d − 2dP.
  - **Variance:** constant, d(1 − d)/m, for every P.
  - **Heuristics:** the paper says only that heuristics have "no reason to produce this cancellation"; it derives no non-zero value for any heuristic model.
- **Zhu, Sanborn & Chater 2020** (*Psych. Rev.* 127:719).
  - **Estimate:** P̂ = (S + β)/(N + 2β), with mean N/(N + 2β)·P + β/(N + 2β).
  - **Variance:** N·P(1 − P)/(N + 2β)², which peaks mid-scale.
  - **Agreement with PT+N:** the same means for simple events, conjunctions and disjunctions; different predictions for conditionals and distributions.
  - **Table D1: Z need not be 0.** When conjunctions and disjunctions get extra noise (Δd > 0, or fewer samples), **E[Z] = 2Δd·(P(A) + P(B) − 1)**. That extra noise is the condition both models need to reach above-chance fallacy rates. Costello & Watts (2017) found Z "deviate[s] predictably from zero" item by item.
  - **No order effects:** "the Bayesian sampler as defined above does not produce order effects". Order effects need an autocorrelated sampler with a starting point.
  - **Choice against estimation:** with few samples, choice probability-matches. The paper speculates that a numerical response draws a *larger* sample than a choice.
- **Lieder, Griffiths, Huys & Goodman 2018** (*Psychon. Bull. Rev.* 25:322).
  - **The model:** E[x̂] ≈ a·rᵗ + (1 − rᵗ)·x, so the estimate lies between the anchor and the belief, never beyond.
  - **Uncertainty matters:** "Uncertainty increases anchoring". Knowledgeable participants failed to move to a high anchor.
  - **Discarding is discussed, not modelled:** the bias is "absent when the anchor was perceived as implausible", and people "discard the provided value when it appears irrelevant or misleading".
  - **No source term:** self-generated and provided anchors use the same mechanism.
- **Fiser, Berkes, Orbán & Lengyel 2010** (*Trends Cogn. Sci.* 14:119).
  - Sampling "provide[s] a natural explanation for neural variability and co-variability" and for bistable perception.
  - "To date there is no direct electrophysiological evidence."
  - It says nothing on categorical choice against graded estimates.

**What it predicts.**
- **C1 ✔:** the account is classical.
- **F1 ~ (revised from ✔):** only the autocorrelated or starting-point extension gives order effects.
- **F2 ~:** the paper says it is "reasonable to use the answer to a preceding question as the starting point", but this is verbal, not modelled.
- **F5 ~:** shrinkage toward 0.5 grows as N falls.
- **F3 ~/✗ (revised from ✗):**
  - resistance fits Lieder's anchor-discarding and low-uncertainty cases;
  - contrast is impossible.
- **F6 ~/✗ (revised from ✔/~):**
  - a yes/no answer is deterministic only if choices draw many samples;
  - Zhu's speculation (more samples for estimates) points the other way, toward *noisier* choices;
  - revision 1's claim that the sample agreement gives a confidence signal (F4) is not in these papers.

**Unique prediction (revised).** Z is not 0 in the versions that produce fallacies. Its sign follows P(X) + P(Y) − 1 item by item, with a zero crossing at P(X) + P(Y) = 1.
- **What cannot discriminate:** Z ≡ 0. Coherent probability and any shared affine distortion also predict it (and so does configural averaging with matched weights; that is the reader's own derivation, not in the papers).
- **"Parameter-free" is withdrawn.**
- **A second, within-family split:** repeat variance peaks mid-scale for the sampler and is constant for PT+N 2014.

**Test.**
- **Design:** the 16 exp-4 items, rating X, Y, X∧Y and X∨Y, one scale, R = 20. That is 1,280 single-turn calls, about **$0.05** at exp 4 run 2's rate ($0.04 for 1,120 calls).
- **Pass:** the item-level slope of Z on P(X) + P(Y) − 1 is positive, with an intercept near 0 at P(X) + P(Y) = 1.
- **Fail:** Z is flat (coherent or affine) or has the opposite slope.
- **Predictor range:** on run 2's 7 fallacy items, P(X) + P(Y) is above 1 only for co-lin09 (0.70 + 0.44). So most of the predicted Z values are negative, and the 9 non-fallacy items are needed for range.
- **Free secondary:** the variance shape on the archived single-scale B0 data, to separate the sampler from PT+N (floor and ceiling effects confound it).

### 3.5 Lateral inhibition, winner-take-all, LCA (rank 5)

**The papers, read in full.**
- **Usher & McClelland 2001** (*Psych. Rev.* 108:550).
  - **Diffusion is a special case:** "when K = 0 … a classical diffusion process results" (K = leak − inhibition). With 2 units the model is an Ornstein–Uhlenbeck process.
  - **Primacy and recency:** in Exp 3 (time-varying letter streams), 2 of 6 participants showed recency, 2 primacy and 2 were neutral.
  - **The U-shape is excluded** (p. 579): "differential attention might easily predict both a primacy and a recency effect. In contrast, the mechanism we have explored cannot produce such a U-shaped effect."
- **Wang 2002** (*Neuron* 36:955).
  - **Mechanism:** slow NMDA recurrent excitation (τ = 100 ms) plus feedback inhibition "amplify the difference between conflicting inputs and generate a binary choice".
  - **Persistence:** the attractor "will outlast the stimulus and persist during a mnemonic delay period".
  - **Not totally locked:** a reversed signal above 70–80% coherence overturns the choice.
- **Tsetsos, Gao, McClelland & Usher 2012** (*Front. Neurosci.* 6:79).
  - **Primacy:** the LCA produces it "when the inhibition is strong relative to the leak".
  - **The primacy-to-recency transition:** it needs a floor at zero and *moderate* inhibition dominance. It "does not occur in the linear case … nor … with a high level of inhibition dominance".
  - **Weak evidence:** the transition was seen in 2 of 10 participants, and the authors call their conclusions "tentative".

**What it predicts.**
- **F6 ✔:** binary attractor output.
- **F2 ✔:** persistence after offset. Redgrave et al. (§3.9) supply the term "hysteresis"; Wang does not use it.
- **F1 ✔:** order effects through leak or inhibition.
- **C1 ✔:** the account is classical.
- **F3 ✗:** there is no social term.
- **C2 ✗/·:**
  - if the competing units are claims, the near-zero couplings contradict it;
  - if they are only the two answers, it is a 2-unit Ornstein–Uhlenbeck accumulator. Revision 1 wrongly said "bounded diffusion".

**Unique prediction (revised).** Any monotone serial-position curve is allowed (primacy, recency or flat), but **never a U-shape**. Revision 1's free step assigned primacy to the LCA and recency to Hogarth–Einhorn, but the leak-dominant LCA also gives recency, so that step did not discriminate. The primacy-to-recency transition is too fragile to test cheaply, because its absence would not falsify the LCA.

**Test, at $0.** Fit position weights for S₁–S₄ on M from the archived O1–O4 Latin square. A U-shape, with both the first and last positions weighted above the middle, falsifies the LCA.

### 3.6 Bounded accumulation and 2DSD (rank 6)

**The papers.**
- **Pleskac & Busemeyer 2010** (*Psych. Rev.* 117:864): **[2010 unread]**.
  - The 2007 CogSci precursor was read in full: evidence "continues to accumulate after the choice", with an interjudgment time of τ = 700 ms, by further sampling of the same stimulus.
  - Whether the 2010 paper predicts or reports better resolution with longer interjudgment time is **unverified**.
- **Kiani, Corthell & Shadlen 2014** (*Neuron* 84:1329). Six human subjects; **no monkey or LIP recordings**, which revision 1 wrongly cited.
  - **Measurement:** choice and certainty were given together, by one saccade to a point on a bar.
  - **Time lowers certainty:** longer RTs gave lower certainty, errors included.
  - **The key manipulation:** a 160 ms reverse pulse lengthened RT by 222.6 ± 68.6 ms with no change in accuracy, and "reduced choice certainty by the amount expected for the change of RT".
- **Kvam, Pleskac, Yu & Busemeyer 2015** (*PNAS* 112:10645).
  - **Design:** 9 participants × 2,688 trials. Choice and no-choice blocks; confidence 0.05, 0.75 or 1.5 s later, folded to 50–100.
  - **Result:** confidence was *lower* after a choice (83.96 against 85.15). The interference coefficient was −0.11 [−0.18, −0.04], and the quantum walk was favoured for 7 of 9 participants.
  - **The Markov prediction:** confidence "should be identical" with and without a choice.
  - **A Markov variant** with extra no-choice accumulation (MRW-E) fit worse.

**What it predicts.**
- **F6 ✔:** a near-deterministic bound crossing alongside a graded accumulator readout.
- **F4 ✔:** confidence comes from the same evidence.
- **C1 ✔, weaker than revision 1 said.** The Markov walk predicts Δ_K = 0, as observed. Kvam's interference predicts Δ_K < 0 on the same folded statistic, and the project's interval [−1.12, +1.65] only barely excludes the human raw effect (−1.19). "Haiku behaves unlike Kvam's humans" is downgraded to "no evidence of a human-sized effect".
- **F1, F2 ~:** these need the next question's starting point to be set by the last state.
- **F3 ✗:** there is no social term.

**Unique prediction (revised).** Revision 1's "improvement only from same-item processing, none from a filler" is **not unique**. Fleming & Daw's post-decisional first-order model (X_conf = X_act + X_new) predicts the same improvement. Their decay passage also lets a filler change confidence under a second-order account. And Kiani's time cue concerns decision time *before* the choice, not a post-decision filler.

**Test.** The arm-G reconsider/filler test (≈ $0.10: 800 calls at arm G's archived rate of about $7 × 10⁻⁵ per call) now tests post-decision accumulation in general, not 2DSD specifically. Discrimination is downgraded to low-medium.

### 3.7 Second-order metacognition (rank 7)

**The paper, read in full.** Fleming & Daw 2017 (*Psych. Rev.* 124:91).
- **Self-evaluation as inference about another actor:** it is second-order inference about a coupled but distinct decision system, "computationally equivalent to inferring the performance of another actor".
- **The key parameter:** ρ, the correlation between the decision and confidence variables. It is "limited" between people and "may be higher" within one person.
- **Fig. 8B:** "As the correlation between the confidence and decision variables is increased, metacognitive sensitivity is decreased."
- **Hyper-metacognition** (meta-d′ > d′) occurs when σ_act > σ_conf.
- **Fig. 6:** after a choice, ratings "should be systematically lowered" and sensitivity "should increase".
- **First-order models** use one internal state, and without new evidence they give equal confidence before and after a decision.
- **No self-versus-other comparison** is tested or predicted.

**What it predicts.**
- **F4 ~:** confidence as a separate inference. The paper says nothing about structural readings of text.
- **F2 ~:** the observed action enters confidence.
- **C1 ✗ (new):** the act of choosing should *lower* later confidence, and K1 ≈ K0 (Δ_K = +0.29 [−1.12, +1.65]) does not show it, unless ρ is high.

**What was wrong in revision 1.**
- "Uniquely predicts self > other" is **not in the paper, and the sign may be wrong.** At equal confidence noise, Fig. 8B implies that a *less*-correlated outside rater has higher sensitivity. Self > other needs the outside rater's confidence noise to be larger.
- "Internal states that never reach the choice, including the agent's own actions" mis-states the model: the action *is* the choice, and confidence conditions on it.
- Gold map §1's self/other test remains a valid test of privileged access, but it is not derived from this paper.

**Unique prediction.** A choice raises *sensitivity* while lowering confidence.

**Test, at $0.** Use the archived K1 and K0 conversations (450 each). Compare the AUROC of the final M rating ("how likely is it that the answer is yes?") against each item's truth label, K1 against K0. Pass: K1 > K0. The confidence half (lowering) has already failed.

### 3.8 Active inference (rank 8)

**The paper, read in full.** Friston, Rigoli, Ognibene, Mathys, FitzGerald & Pezzulo 2015 (*Cogn. Neurosci.* 6:187; target article pp. 187–214).
- **Expected free energy** splits into extrinsic plus epistemic value (Eq. 3). Policies "search out observations … that resolve uncertainty".
- **No uncertainty, no preference:** "when there is no posterior uncertainty … epistemic value will be the same for all policies".
- **Cue-seeking depends on utility.** In the T-maze, seeking the cue first appears only when utility exceeds about 0.6 nats, close to the cue's information (ln 2).
- **Dopamine:** the link is a simulated resemblance ("assuming that dopamine mediates increases in precision").

**What it predicts.** F4 ~ and F5 ~, through its perceptual half (§3.3). Nothing measured tests its action half.

**Unique prediction.** The model chooses the check with the highest expected information gain about its own conflict.

**Caveat (new).** If the model holds a prior *preference* for confirmation (extrinsic value), active inference predicts the confirmatory check too. Gold map §4's menu test therefore discriminates only with preferences fixed or measured, for example by a matched no-conflict control. Cost about **$0.10** (gold map §4).

### 3.9 Basal-ganglia action selection (rank 9)

**The papers, read in full.**
- **Redgrave, Prescott & Gurney 1999** (*Neuroscience* 89:1009).
  - A theoretical commentary: a "centralised selection device … to resolve conflicts over access to limited motor and cognitive resources".
  - It names "clean switching" and "persistence … (also termed 'hysteresis')".
- **Bogacz & Gurney 2007** (*Neural Comput.* 19:442). The MSPRT is "asymptotically optimal" for "highly practiced tasks".
  - **The conflict term** S(T) = ln Σ exp(y_k) "may be thought of as representing response conflict". The STN supplies it.
  - **The posterior** is Lᵢ = yᵢ − S(T) = ln Pᵢ, so **conflict is exactly what lowers the posterior**.
- **Frank 2006** (*Neural Netw.* 19:1120).
  - **Threshold:** "Increased cortical response conflict leads to dynamic adjustments in response thresholds". Conflict is co-activation of competing responses, and its effect is a delay; lesioned networks respond prematurely.
  - **Withholding** is future work only. "In proportion" (revision 1) is not the paper's wording, and only two conflict levels were simulated.

**What it predicts.** F6 ✔ (gated selection). F4 ~ (the MSPRT tracks ln P).

**What was wrong in revision 1.** The abstention test asked whether conflict drives abstention beyond stated confidence. The MSPRT *anti-predicts* that, because conflict and the posterior are the same quantity. Frank's conflict is between response options, not claims, and neither paper predicts abstention.

**No cheap valid test.** The distinctive prediction, a conflict-dependent delay, needs a time variable that thinking-disabled single-number responses do not provide.

### 3.10 Divisive normalization (rank 10)

**The paper, read in full.** Louie, Khaw & Glimcher 2013 (*PNAS* 110:6139).
- **Context is simultaneous:** three options at once, in monkeys (2 animals) and people (n = 40, trinary snack choice).
- **Prediction:** a more valuable distracter "reduces the distance between target option distributions and decreases the relative choice ratio" (in humans β₃ = −0.42). The effect is biphasic: it rises again for distracter values above 0.8.
- **Sequential context is untested:** "temporal normalization … the consequences … remain currently unknown."

**What was wrong in revision 1.**
- Both normalization claims were extrapolations. "A high context value lowers the rating", credited as matching F3, is **not in the paper**: no rating is measured under context.
- "Compress the differences between later ratings, not shift them" is **wrong**, on two counts. Compression applies to the current choice set, not to later ratings, and dividing by a larger sum both lowers *and* compresses the coded values.
- So **F3 ✔ → ·** and **F1 ✔ → ~**.

**Test.** Two target claims rated together with a third claim of varied value, simultaneously. The signature is a smaller gap between the targets as the third's value rises. Cost about $0.05. It is a faithful test, but of a mechanism the fingerprint barely touches.

---

## 4. What no mechanism here explains

- **Reversal against another person's number** (the 5 reliable contrast item-orders in run 3, all on Linda-family items). After the full reads, no mechanism derives it:
  - serial-dependence repulsion needs sensory adaptation and a perceptual readout;
  - normalization's "contrast" is not in the paper;
  - Lieder's anchoring never goes beyond the belief;
  - precision weights are non-negative;
  - Rollwage's gating abolishes disconfirming evidence but never reverses it;
  - Kumaran's LLMs *over*weight opposing advice.

  If §3.0's "other" cells reproduce it, it is a finding with no biological model in this map.
- **The scale-relabelling gap (33.8 against 71.3).** This is a failure to read the instruction, not a way of resolving a conflict. D33's one-scale designs control for it rather than explain it.
- **The scale wording may shrink some order effects** (exp 4 run 3: Marta from about +0.10 to +0.02, co05 +0.07 to +0.04; Bill unchanged). §3.0 and §3.4 reuse the exp-4 items and must keep run 3's wording.
- **F5 on Haiku's locked test.** The readout tilt adds nothing detectable there (+0.009 [−0.057, +0.065]). Every mechanism that claims F5 must explain why it helps on Sonnet's pool and on Haiku's run-2 held-out set but not on Haiku's locked test. None does.

## 5. Recommended order

1. **The $0 analyses, each pre-registered before its archive is opened:**
   - the LCA's U-shape check (§3.5);
   - K1 against K0 sensitivity (§3.7);
   - the sampler/PT+N variance shape (§3.4);
   - the low-power run-3 asymmetry, recoded by sign (§3.1).
2. **§3.0, the source × distance × lag test** (≈ $0.46; ≈ $0.28 without lag). It decides the top two mechanisms, completes gold map §2's planted-answer condition, and re-probes the unexplained reversals. Share its pre-registration with gold map §2.
3. **§3.4's Z-slope test** (≈ $0.05) and **§3.3's prime × confidence test** (≈ $0.15–0.25).
4. **§3.6's reconsider/filler test** (≈ $0.10) and **gold map §4 with fixed preferences** (≈ $0.10).
5. **Before citing 2DSD's resolution claim,** obtain Pleskac & Busemeyer 2010 in full.

**What I would not do.**
- **Build a biologically detailed model** (a spiking WTA network, or a basal-ganglia loop) and fit it to these ratings. The record's lesson from the quantum encodings applies: a flexible model of sequential ratings ties a matched classical twin.
- **Treat any of these mechanisms as confirmed by fit alone.** The full reads cut most "unique" predictions back to shared ones. The ones that survive are §3.0's source and distance-tuning cells, §3.4's item-level Z slope, §3.5's U-shape exclusion and §3.7's choice-raises-sensitivity contrast.

---

## 6. Corrections made in revision 2

| § (rev. 2) | claim in revision 1 | what the full read showed | effect |
|---|---|---|---|
| 3.2 | Decisions are attracted toward the previous *decision* | Measured toward the previous *stimulus*; "decision" is Fritsche's inference from one contrast; F&W find equal attraction after unresponded trials | serial dependence predicts attraction to another's number: F3 ✔/~ → ✗/~ |
| 3.2 | It uniquely predicts a sign flip by source | The papers flip sign by task, lag and difference, never by source; repulsion is retinotopic adaptation | unique prediction replaced by distance tuning and lag decay |
| 3.2 | Attraction grows with intervening turns (the "Fritsche delay effect") | The delay is the within-trial retention interval; attraction *decays* across trials (half-life ≈ 4.5 s), with repulsion at long lags | lag prediction reversed; rank 1 → 2 |
| 3.4 | PT+N predicts Z ≈ 0, parameter-free; heuristics predict Z ≠ 0 | Z = 0 only in the 2014 model; the fallacy-producing versions give E[Z] = 2Δd(P(X)+P(Y)−1); coherent and affine accounts also give 0; C&W derive nothing for heuristics | test becomes the item-level Z slope; "parameter-free" withdrawn |
| 3.4 | F1 ✔, F3 ✗, F6 ✔/~, F4 ~ | Basic sampler has no order effects; resistance fits anchor-discarding; choice may use fewer samples; F4 not in the papers | F1 ~, F3 ~/✗, F6 ~/✗, F4 ·; rank 2 → 4 |
| 3.4 | Variance largest mid-scale (whole family) | True for the sampler; PT+N 2014 predicts constant variance | now a within-family test |
| 3.1 | Disconfirmatory evidence "abolished" | "Largely abolished"; confounded with accuracy; binary confidence; roughly symmetric at low confidence | wording and qualifiers |
| 3.1 | The confidence × agreement asymmetry is unique | Bounded-scale Bayes and state-dependent precision predict it too; coded by sign it is nearly empty | demoted to a low-power secondary |
| 3.1 | Kumaran: choice-supportive bias in GPT-4o and o1-preview | Mainly Gemma 3 12B/27B; the authors conclude "no confirmation bias"; self-consistency is abolished when the answer is attributed to another LLM; no Claude model tested | new source-dependence prediction; rank 3 → 1 |
| 3.1 | K1: S₃/S₄ move M more when consistent with the choice (Talluri) | Talluri never reported a choice/no-choice contrast; Bronfman found reduced sensitivity after a choice | dropped |
| 3.3 | Plain precision fusion commutes, so F1 ✗ | Feldman & Friston's precision is time-varying and order-dependent | F1 ✗ → ~ |
| 3.6 | Kiani: monkey LIP and behaviour | Human psychophysics only | corrected |
| 3.6 | Haiku behaves unlike Kvam's humans | The project's CI barely excludes the human raw effect (−1.19 points) | C1 downgraded to "consistent with Markov" |
| 3.6 | 2DSD uniquely predicts same-item improvement, none from a filler | Shared with Fleming & Daw's post-decisional first-order model; the 2010 paper was not obtained | discrimination downgraded; rank 5 → 6 |
| 3.7 | Fleming & Daw uniquely predict self > other | Not in the paper; at equal noise the less-correlated outside rater can be *more* sensitive | test replaced by K1/K0 sensitivity |
| 3.7 | — | Their model predicts lower confidence after a choice; K1 ≈ K0 | new C1 ✗; rank 6 → 7 |
| 3.5 | A 2-unit LCA reduces to bounded diffusion | It reduces to an Ornstein–Uhlenbeck process; it is diffusion only when leak = inhibition | corrected |
| 3.5 | The position-weight test discriminates the LCA from Hogarth–Einhorn | The LCA allows any monotone curve; it excludes only a U-shape (p. 579) | test becomes U-shape falsification; rank 7 → 5 |
| 3.10 | A high context value lowers the rating (F3 ✔); context compresses later ratings and does not shift them | Neither is in the paper; its context is simultaneous; sequential normalization is untested | F3 → ·, F1 → ~; new simultaneous test; rank 9 → 10 |
| 3.9 | Abstention tracks conflict beyond confidence | MSPRT conflict *is* the low posterior; Frank's conflict is between responses; abstention not in either paper | test withdrawn |
| 3.8 | — | Epistemic value is equal across policies without uncertainty; a confirmatory preference also predicts the confirmatory check | caveat added to gold map §4 |

---

## 7. Sources

"Read in full" means the whole main text was read. Supplements are noted where they were not.

| paper | copy read | status |
|---|---|---|
| Fischer & Whitney 2014, *Nat. Neurosci.* 17(5):738–743, doi:10.1038/nn.3689 | [PMC4012025](https://pmc.ncbi.nlm.nih.gov/articles/PMC4012025) (author manuscript) | read in full (supplementary experiments 6–7 not seen) |
| Fritsche, Mostert & de Lange 2017, *Curr. Biol.* 27(4):590–595, doi:10.1016/j.cub.2017.01.006 | [Cell open archive](https://www.cell.com/current-biology/fulltext/S0960-9822(17)30006-4) | read in full (main text; supplementary procedures not read) |
| Fritsche, Spaak & de Lange 2020, *eLife* 9:e55389 | [eLife VoR](https://elifesciences.org/articles/55389) | read in full |
| Costello & Watts 2014, *Psych. Rev.* 121(3):463–480, doi:10.1037/a0037010 | [arXiv:1211.0501v3](https://arxiv.org/pdf/1211.0501) (final preprint) | read in full |
| Zhu, Sanborn & Chater 2020, *Psych. Rev.* 127(5):719–748, doi:10.1037/rev0000190 | [PMC7571263](https://pmc.ncbi.nlm.nih.gov/articles/PMC7571263/) | read in full, with appendices |
| Lieder, Griffiths, Huys & Goodman 2018, *Psychon. Bull. Rev.* 25(1):322–349, doi:10.3758/s13423-017-1286-8 | [eScholarship author manuscript](https://escholarship.org/content/qt4fk2487n/qt4fk2487n.pdf) | read in full through the conclusion (appendices skimmed). Companion paper (25(2):775–784) not obtained |
| Fiser, Berkes, Orbán & Lengyel 2010, *Trends Cogn. Sci.* 14(3):119–130, doi:10.1016/j.tics.2010.01.003 | [PMC2939867](https://pmc.ncbi.nlm.nih.gov/articles/PMC2939867/) | read in full |
| Rollwage et al. 2020, *Nat. Commun.* 11:2634, doi:10.1038/s41467-020-16278-6 | [Europe PMC PMC7250867](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7250867/fullTextXML) | read in full (supplementary notes not read) |
| Talluri, Urai, Tsetsos, Usher & Donner 2018, *Curr. Biol.* 28(19):3128–3135, doi:10.1016/j.cub.2018.07.052 | [Leiden repository PDF](https://scholarlypublications.universiteitleiden.nl/download/1887/3210259/1?col=81522199280002711) | read in full, including STAR Methods (supplementary figures not read) |
| Kumaran et al. 2025, arXiv:2507.03120 | [arXiv HTML v1](https://arxiv.org/html/2507.03120) | read in full, with supplement |
| Feldman & Friston 2010, *Front. Hum. Neurosci.* 4:215, doi:10.3389/fnhum.2010.00215 | [Europe PMC PMC3001758](https://pmc.ncbi.nlm.nih.gov/articles/PMC3001758) | read in full |
| Pleskac & Busemeyer 2010, *Psych. Rev.* 117(3):864–901, doi:10.1037/a0019737 | — | **not obtained in full** (publisher, Semantic Scholar, ResearchGate, Scribd and scispace copies failed or were blocked). The 2007 precursor, "A dynamic and stochastic theory of choice, response time, and confidence" (CogSci 2007), [eScholarship](https://escholarship.org/content/qt0wm9g74s/qt0wm9g74s.pdf), was read in full instead |
| Kiani, Corthell & Shadlen 2014, *Neuron* 84(6):1329–1342, doi:10.1016/j.neuron.2014.12.015 | [PMC4271191](https://pmc.ncbi.nlm.nih.gov/articles/PMC4271191) | read in full |
| Kvam, Pleskac, Yu & Busemeyer 2015, *PNAS* 112(34):10645–10650, doi:10.1073/pnas.1500688112 | [PMC4553814](https://pmc.ncbi.nlm.nih.gov/articles/PMC4553814/) | read in full (SI not read) |
| Fleming & Daw 2017, *Psych. Rev.* 124(1):91–114, doi:10.1037/rev0000045 | [PMC5178868](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5178868/) | read in full |
| Usher & McClelland 2001, *Psych. Rev.* 108(3):550–592, doi:10.1037/0033-295X.108.3.550 | [Stanford PDF](https://web.stanford.edu/~jlmcc/papers/UsherMcC01.pdf) (scanned, OCR) | read in full |
| Wang 2002, *Neuron* 36:955–968 | [PDF](https://cenl.ucsd.edu/Jclub/Wang02.pdf) | read in full |
| Tsetsos, Gao, McClelland & Usher 2012, *Front. Neurosci.* 6:79, doi:10.3389/fnins.2012.00079 | [PMC3372959](https://pmc.ncbi.nlm.nih.gov/articles/PMC3372959) | read in full |
| Friston et al. 2015, *Cogn. Neurosci.* 6(4):187–214 (with commentaries, to 224), doi:10.1080/17588928.2015.1020053 | [PDF](https://www.fil.ion.ucl.ac.uk/~karl/Active%20inference%20and%20epistemic%20value.pdf) | read in full |
| Louie, Khaw & Glimcher 2013, *PNAS* 110(15):6139, doi:10.1073/pnas.1217854110 | [PMC3625302](https://pmc.ncbi.nlm.nih.gov/articles/PMC3625302) | read in full |
| Redgrave, Prescott & Gurney 1999, *Neuroscience* 89(4):1009–1023, doi:10.1016/S0306-4522(98)00319-4 | [White Rose preprint](https://eprints.whiterose.ac.uk/107033) | read in full |
| Bogacz & Gurney 2007, *Neural Comput.* 19(2):442–477, doi:10.1162/neco.2007.19.2.442 | MRC BNDU PDF (NeuCom07.pdf) | read in full |
| Frank 2006, *Neural Netw.* 19(8):1120–1136, doi:10.1016/j.neunet.2006.03.006 | [Brown PDF](https://ski.clps.brown.edu/papers/Frank06.pdf) | read in full |

Cited but not read here: Rao & Ballard 1999; Bronfman et al. 2015 and Costello & Watts 2017, both known only as cited inside the papers above; Pezzulo et al. 2024 (via gold map §4).

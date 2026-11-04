# Direction 4: does the model seek the evidence that would settle its own conflict?

Pre-registered in `experiments/gm4-evidence-seeking.md` (D39), committed before any call. 40 experiment-5 items × 3 menus of 4 of its own claims × 10 repeats, `claude-haiku-5-5`, thinking disabled. 1200 calls, **$0.11** of the $0.50 cap; no refusal.

## In plain English

**The question.** The model's answers argue both sides. If it could check one of its own claims, would it pick the one whose answer would most change its mind (the informative check), or the one that best supports what it already said (the confirmatory check)? We showed Haiku its own answer to each of 40 hard questions and a menu of four of its own claims, three menus per question and ten repeats each, and asked which it would check first.

**What we found.**
- **The choices are not random.** The model picks the same claim from a menu 87% of the time.
- **Its picks beat chance under every rule that scores a claim by how much it bears on the answer:**
  - the informative check under both frozen experiment-5 models: +14 and +21 points over chance;
  - the expected-change rules;
  - the confirmatory check: +21 points.
- **It avoids the most uncertain-sounding claim,** picking it 13 points less often than chance. So "informative" here is not "most hedged".
- **The decisive comparison is undecided.** On the menus where the informative and confirmatory checks differ (46 and 26 menus), the model picks the confirmatory claim more often: −0.24 [−0.52, +0.04] and −0.14 [−0.40, +0.14]. Neither difference is reliable. Under the pre-registered rule the verdict is **mixed**.

**What it means.** The model reliably chooses claims that bear strongly on its question, which is partly what an inquiring mind would do. When they come apart it shows no detectable preference for the informative check; if anything it leans confirmatory, as Jhaveri et al. found for hypothesis testing. Active-inference-style evidence seeking is not shown. Neither is a clear confirmation bias.

**Caveat.** "Informative" is computed from our own fitted models of the model, which the chooser never sees. A miss could be a miss of those models.

## Which rule picks the claim the model chose?

| rule | hit rate | chance | excess over chance [95% item-bootstrap CI] |
|---|---|---|---|
| EIG under D5 | 39% | 25% | +0.141 [+0.042, +0.245] |
| EIG under BA5 | 55% | 34% | +0.210 [+0.113, +0.310] |
| expected |ΔM| under D5 | 45% | 25% | +0.196 [+0.103, +0.299] |
| expected |ΔM| under BA5 | 61% | 44% | +0.166 [+0.083, +0.243] |
| confirmatory (supports its own answer) | 52% | 32% | +0.207 [+0.109, +0.313] |
| most uncertain claim (confidence nearest 0.5) | 21% | 34% | -0.128 [-0.205, -0.043] |

On menus where the EIG choice and the confirmatory choice differ:

| EIG model | menus | hit(EIG) − hit(confirmatory) [95% CI] | per-model reading |
|---|---|---|---|
| EIG under D5 | 46 | -0.237 [-0.523, +0.044] | neither |
| EIG under BA5 | 26 | -0.135 [-0.403, +0.142] | neither |

- Choice share by screen position A–D: 27%, 26%, 26%, 21%.
- Mean share of the modal choice per menu: 87%.
- D5 and BA5 EIG argmax sets agree on 41 of 120 menus.
- Most-uncertain explains choices at least as well as EIG: **False**.

## Pre-registered verdict: **mixed or at chance**

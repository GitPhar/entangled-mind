# Gold-map direction 4: does the model seek the evidence that would settle its own conflict? (pre-registration)

Written and frozen 2026-11-04 (America/Denver), in its own commit, before any call. DEVIATIONS.md D39. Budget **$0.50**, enforced in code. Stop on any refusal: the request ID goes to `results/refusal.md`, and nothing is reworded or retried.

## 1. In plain English

The model's written answers argue both sides: some of its claims push toward yes and some toward no. If it could check one of its own claims, which would it pick? Three possibilities:
- **The informative one:** the claim whose truth would most change its answer. This is expected information gain, EIG.
- **The comfortable one:** the claim that most supports the answer it already gave. This is a confirmatory check.
- **No pattern** at all.

Active-inference accounts say a mind seeks the information that reduces its own uncertainty. The standard view of language models says they are passive predictors with no such drive. We show the model its own answer and a menu of four of its own claims, and ask which one it would check first.

## 2. What the literature gives us (full-text reads by the literature session)

- **Grand et al.** (ICLR 2026, Battleship): unscaffolded GPT-4o gets 0.296 bits per question, against 0.476 with an EIG scaffold.
- **BED-LLM** (2508.21184) gains 37 points over prompting.
- **Dutta et al.** (2608.19202) is the closest in framing: active inference, with Claude Haiku 4.5 among the models. Its exact oracle is a dynamic-programming optimal questioner on an attribute-table game.
- **Jhaveri, GX-Chen, Sucholutsky & Choi, "Failing to Falsify"** (2604.02485): on Wason's 2-4-6 task, LLMs mostly run hypothesis-compatible tests. A confirmatory result here would be reportable in its own right.
- **All of these use external targets.** None asks whether a model seeks to resolve conflict inside its *own* deliberation.
- **A design risk the literature session raised:** EIG may be confounded with "the claim that sounds most uncertain". So a most-uncertain baseline is reported alongside.
- The gold map's P(EIG-tracking) is revised from 0.25 to 0.20.

## 3. Design

- **Items:** the 40 experiment-5 candidates, with Haiku's archived hard-pool answer (`results/pool-run-3.json`). Only the visible answer is shown; thinking content never is.
- **Menus:** 3 menus of 4 claims per item, built by `experiments/gm4_menus.py` and frozen in `experiments/gm4-menus.json` in this commit.
  - Menu 1 is the item's 4 chain claims.
  - Menus 2 and 3 are random 4-subsets of the leaning claims (|lean| > 0.1), each with at least one claim of each lean sign (`random.Random(4004)`).
- **Prompt** (`claude-haiku-5-5`, thinking disabled, structured output `{"choice": "A"|"B"|"C"|"D"}`):

  > Here is a yes/no question and an answer you gave to it.
  >
  > Question: {question}
  >
  > Your answer:
  > {visible answer}
  >
  > Suppose you could check exactly one of the following statements and find out for certain whether it is true. Which one would you check first, to best decide the answer to the question?
  >
  > A. {claim} … D. {claim}
  >
  > Answer with the letter only.

- **Option order:** in repeat r, the menu's i-th claim is shown at position (i + r) mod 4, which balances position bias.
- **Repeats:** R = 10 per menu, so 40 × 3 × 10 = **1,200 calls**, about $0.12.

## 4. Scores (fixed before any call, in `gm4-menus.json`)

For each claim k, let c_k be its extracted confidence, used as P(k true).
- **EIG under D5 and under BA5**, using the frozen experiment-5 fits:
  - EIG = H(p₀) − [c_k·H(p_true) + (1 − c_k)·H(p_false)], where H is binary entropy in bits.
  - p₀ is the model's predicted probability for the main question with no check.
  - p_true and p_false are the same after a sub-question rating of 100 or 0 on k, by the inverse of each model's link.
- **Expected |ΔM| under each model:** the expected move in the main rating, in points.
- **Confirmatory:** c_k·|lean_k| among the menu claims that lean toward the model's archived answer. It is undefined on a menu with no such claim.
- **Most-uncertain:** −|c_k − 0.5|.
- **Ties:** a menu's target set for a rule is every claim within 10⁻⁹ of the rule's maximum. A choice is a hit if it falls in that set. Chance for that menu is |set| / 4.

## 5. Statistics

- **Per rule:**
  - the hit rate over all choices;
  - the excess over chance, (hit rate − mean chance), with a 2,000-resample item-bootstrap CI (items resampled with their menus; seed 4040).
- **Discriminating menus:** for each EIG model X, the menus whose X-argmax set and confirmatory set do not overlap. On them, the paired difference hit(X) − hit(confirmatory) is reported with an item-bootstrap CI.
- **Reported alongside:**
  - the hit rates of expected |ΔM| and of most-uncertain;
  - the choice share by screen position;
  - the agreement between the D5 and BA5 argmax sets, whose argmax sets are identical on 41 of the 120 menus;
  - how concentrated the choices are (the modal share per menu).

## 6. Pre-registered reading

For each EIG model X (D5 and BA5):
- **Tracks EIG:** X's excess over chance has a CI above 0, **and** hit(X) − hit(confirmatory) on X's discriminating menus has a CI above 0.
- **Confirmatory:** the confirmatory excess has a CI above 0, **and** hit(confirmatory) − hit(X) on the discriminating menus has a CI above 0.
- **Neither:** otherwise.

**Verdict:**
- **EIG-tracking** if both models say "tracks EIG";
- **confirmatory** if both say "confirmatory";
- **mixed or at chance** otherwise.

If most-uncertain explains the choices at least as well as EIG (its excess at or above EIG's, by point estimate), the write-up says that EIG-tracking may be an uncertainty-seeking heuristic.

## 7. What it cannot do

- The chooser never sees the fitted models that define EIG. EIG here is the experiment-5 models' view of what would move the model, not ground truth.
- c_k is the extractor's reading of the writer's confidence, not the model's own sub-question rating.

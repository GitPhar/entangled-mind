# Audit: exp4-run-2

**Files audited:** `results/exp4-run-2.md`, `results/exp4-run-2.json`, `results/exp4-run-2-calls.json` (560 two-turn conversations, 1,120 request IDs), `results/exp4-run-2-anchoring-diagnostic.json`; `experiments/exp4-yearsley-trueblood.md` ("Addendum — run 2"); `experiments/exp4_graded.py`; D17, D19. Citations in README.md, paper/record.md, paper/the-entangled-mind-v3.md, paper/gold-map.md, paper/biomimetic-map.md, experiments/exp4-run-3.md.
**Pre-registration:** D17 `cb4e96e` (11-03 19:05:10), text in the run-2 addendum of `experiments/exp4-yearsley-trueblood.md`; runner `27121e9` (19:05:56). First call: 19:34:11 (decoded), last 19:36:02; result `2bac6be` 19:36:43, which also adds D19 ("logged after results").
Timing verdict: OK. The rule and the analysis code were both committed 28 min before the first call. D19 is openly post-results.

## Plain-English summary of the audit
The table is right: I rebuilt every number from the raw conversations and match o, f, r, OE_X and the verdict counts. The order effects are real but smaller than the summaries say. Six of seven items are reliably positive, ranging from +0.02 to +0.12, and only Bill and Marta are about +0.10; co05 is +0.07. "R2 holds on 3 of 3" is true but weak: algebraically it only says that, right after rating Y, the model does not rate "X and Y" more than 5 points above Y. Only 3 items were scored because the pre-registered rule (a graded fallacy with lower bound above 0) was met by only 3. That rule was fixed before the run. The run-1 fallacy vanished on 4 of 7 items here, including Linda. The frozen anchoring rule was degenerate. With the cells pooled, the slope is fixed by the cell means, so "o − o_rep ≈ 0" and the "static twin" verdict were guaranteed before any data. D19's diagnosis is mathematically correct (I confirm r ≈ o/(P(X) − P(Y)) on every item). The result file and v3 report the pre-registered verdict honestly, but README.md drops it and says only "mechanism undetermined". That moves a verdict that went against the sequential/quantum reading to a neutral one without saying so.

## What the frozen rule said
From `experiments/exp4-yearsley-trueblood.md`, Addendum — run 2 (committed `cb4e96e`, before any call):
> Anchoring on the first answer, the graded analogue of repetition. Fit second = r · first + (1 − r) · fresh by regressing the second rating on the first within cells 1–2, with fresh taken from the first-turn means. Then o_rep = r · (P(X) − P(Y)), and **o − o_rep** is the order effect beyond anchoring.
>
> Scored items are those with f's 95% lower bound above 0. **R2 is met** … if at least half the scored items have o ≥ f − 0.05 **and** at least half have o − o_rep reliably > 0. **The static twin is supported** if at least half have an o − o_rep interval that contains 0. **Untestable** if fewer than 3 items are scored.

"Within cells 1–2" is ambiguous: it can mean pooled over cells 1 and 2, or within each cell. The committed code (`exp4_graded.py`, `stats()`) pools, and D19 describes it the same way. Under the frozen rule, 3 items are scored, 3/3 meet o ≥ f − 0.05, 0/3 have o − o_rep > 0, and 3/3 have intervals containing 0. The machine verdict, "static classical twin (with anchoring) supported", is what the frozen rule returns.

## Claims checked
| # | claim (quoted or paraphrased, with file:line) | recomputed / evidence | status |
|---|---|---|---|
| 1 | Table values o, f, o − o_rep, r, OE_X, OE_Y (exp4-run-2.md:9–15) | All reproduced from raw calls with my own bootstrap (2,000). E.g. co-lin06 o +0.118 [+0.103, +0.132], f +0.094 [+0.079, +0.109], r 0.154. | holds |
| 2 | "Scored items … **3** of 7"; R2 3 of 3; beyond anchoring 0 of 3; static twin 3 of 3 (exp4-run-2.md:19–21) | 3 (co-lin06, co-lin10, co05); 3/3; 0/3; 3/3 | holds |
| 3 | Why only 3 scored | The scoring rule was fixed in D17 before the run. f = P(X∧Y \| X first) − P(Y \| Y first) is reliably > 0 only on 3; it is reliably *negative* on co-lin08 (−0.022), co-lin09 (−0.042) and co06 (−0.018), and null on co01 (−0.001). So run 1's rating fallacy did not carry into the two-turn design on 4 of 7 items, including Linda and co-lin09 (run 1's +0.143). | holds (rule pre-fixed); the failure to replicate is unreported |
| 4 | "o is reliably positive on 6 of the 7 items" (exp4-run-2.md:27; v3:478) | 6/7 (co-lin08 reliably negative, −0.005 [−0.008, −0.002]) | holds |
| 5 | "at about +0.10 for Bill (co-lin06), Marta (co-lin10) and co05" (exp4-run-2.md:27) | +0.118, +0.103, **+0.069** | holds (minor) |
| 6 | "Graded ratings show real order effects of about +0.10" (README.md:133); "order effects of about +0.10 on 6/7 items" (record.md:34) | The 6 positive o are +0.023, +0.039, +0.069, +0.080, +0.103, +0.118 (median +0.075). Only 2 are about +0.10. | overclaim |
| 7 | "Graded ratings show real order effects, where binary answers did not." (exp4-run-2.md:27) | Run 1's binary *marginals* did shift (OE_X +0.67, +0.50, −0.22, +0.43). Only the binary joint was pinned at 0. | overclaim |
| 8 | "OE_X = −0.12, −0.08, −0.23" (exp4-run-2.md:27) | −0.118, −0.080, −0.230 on those three. On the other four items OE_X is +0.071, +0.030, 0.000 and −0.122, so the sign is not general. | holds |
| 9 | "R2 holds where it applies … the order effect is at least as large as the fallacy" (exp4-run-2.md:28; README.md:133; v3:479) | Holds. Note that o − f = P(Y \| Y first) − P(X∧Y \| Y first), so R2 here is exactly "after rating Y, X∧Y is not rated > 5 points above Y". Margins are +0.024, +0.016, +0.028; it would hold on all 7 items. It is a weak, coherence-type test, consistent with anchoring too (D11 already says it is not quantum-specific). | holds (minor) |
| 10 | "The fitted slope is therefore close to o / (P(X) − P(Y)), and o − o_rep ≈ 0 almost by construction" (exp4-run-2.md:29; D19) | r against o/(P(X) − P(Y)): 0.028/0.028, 0.154/0.152, 0.000/−0.010 (clipped), 0.335/0.303, 0.128/0.128, 0.154/0.158, 0.104/0.105. Confirmed. | holds |
| 11 | "The verdict stands as pre-registered, but it does not show that anchoring explains the effect." (exp4-run-2.md:29; v3:480) | Honest and accurate. The frozen rule could not have returned "R2 met", because its second leg needs o − o_rep reliably > 0, which the construction prevents. | holds |
| 12 | "The pre-registered anchoring estimator turned out to be near-tautological (D19), so the mechanism is undetermined." (README.md:134) | The inference is right, but README never states the pre-registered verdict (static twin with anchoring) | overclaim (omission) |
| 13 | "SD 0.00–0.05 … within-cell slopes … range from 0.0 to 0.63" (exp4-run-2.md:30) | SDs are 0.000–0.083 (Y→X first ratings reach 0.083 on co-lin09; the 0.00–0.05 range holds for the anchoring cells 1–2 except co-lin09 Y→XY first at 0.070). Slopes are recomputable from calls. The co01 Y→XY slope (archived 0.275) is a floating-point artefact: all 20 first ratings are exactly 0.05. No script in the repo generates the diagnostic JSON. | holds (minor) |
| 14 | "mechanism is undetermined" (gold-map.md:117; biomimetic-map.md:32; v3:484) | Correct reading of an uninformative estimator | holds |
| 15 | v3:63 "Order effects of about +0.10 satisfied the Yearsley–Trueblood bound R2 on 3 of 3 scored items." | The 3 scored items have o = +0.118, +0.103, +0.069 | holds (minor) |

## Holes found
1. **The frozen verdict rule was degenerate, and that was knowable before any data.** With cells 1–2 pooled and within-cell SDs near 0, the OLS slope is Δsecond/Δfirst between cells, so o − o_rep ≈ 0 on any data. "Static twin supported" was therefore guaranteed and "R2 met" impossible. D19 says so after the results. The diagnosis is correct (claim 10), but the flaw is in the pre-registration's algebra, not in the data.
2. **The post-hoc reinterpretation runs toward the hypothesis.** The pre-registered outcome was the anti-sequential one (static twin). D19 and the summaries replace it with "mechanism undetermined", which is more favourable to the quantum/sequential reading. The result file, v3 §5.9, record.md:34 and the D19 table row all keep the pre-registered verdict visible, which is the honest course. README.md:132–134 drops it.
3. **The label "static twin (with anchoring)" is internally muddled.** Anchoring the second rating on the first is a sequential update, which D11 says R2 cannot distinguish. The static twin proper predicts o = 0, and o is reliably non-zero on 6/7, so the static twin *without* anchoring is refuted here. None of the summaries says that.
4. **The run-1 fallacy does not replicate in the two-turn design on 4 of 7 items** (claim 3). Linda's graded f is −0.001 here against +0.085 in run 1. Run 3's text ("R2 on all 3 scored items") and README carry the 3/3 forward without noting that 4 of the 7 items lost their fallacy.
5. **The size is overstated in summaries.** "About +0.10" describes 2 items. The median of the reliably positive effects is +0.075, and the smallest "reliable" effect (+0.023, co01) is reliable only because the ratings are near-deterministic (CI [+0.021, +0.025] from 20 repeats of one prompt).
6. **R2's evidential weight is small** (claim 9). Under these definitions, R2 holds whenever the Y-first cell has no conjunction fallacy. A simple anchoring or consistency model satisfies it.

## Overclaims to cut (exact sentences)
- `README.md:133` — "- Graded ratings show real order effects of about +0.10, and R2 holds on all 3 scored items." — Only 2 of the 6 positive effects are about +0.10, and R2 is a weak test. — Replace: "- Graded ratings show order effects reliably above 0 on 6 of 7 items (+0.02 to +0.12; about +0.10 on Bill and Marta), and R2 holds on all 3 scored items; here R2 only requires that, after rating Y, the model not rate X and Y more than 5 points above it."
- `README.md:134` — "- The pre-registered anchoring estimator turned out to be near-tautological (D19), so the mechanism is undetermined." — It omits the pre-registered verdict. — Replace: "- The pre-registered verdict is \"static classical twin (with anchoring) supported\", but its anchoring estimator is near-tautological (D19), so that verdict is uninformative and the mechanism is undetermined."
- `paper/record.md:34` — "order effects of about +0.10 on 6/7 items" — The 6 range from +0.02 to +0.12 (median +0.075). — Replace: "order effects reliably > 0 on 6/7 items (+0.02 to +0.12; about +0.10 on 2)".
- `results/exp4-run-2.md:27` — "- **Graded ratings show real order effects, where binary answers did not.**" — Run 1's binary marginals moved by up to +0.67; only the saturated joint did not. — Replace: "- **Graded ratings show order effects on the conjunction, which run 1's saturated binary joint could not show.**"

## Does the verdict stand?
Pre-registered verdict: **"static classical twin (with anchoring) supported."** It is reproduced exactly, but it is **UNDETERMINED** in substance: the estimator makes it a foregone conclusion. Of the descriptive results, the order effects (6/7 non-zero) and R2 on 3/3 stand, with the size and weight caveats above. "Mechanism undetermined" is the honest reading, provided the pre-registered verdict is stated next to it, as the result file and v3 do and README does not.

## Confidence
High. All statistics were rebuilt from `exp4-run-2-calls.json`, and the D19 algebra was confirmed numerically on all 7 items. The only thing not reproducible from repository code is the diagnostic JSON's generator, which is absent.

## Tally
claims_checked: 15
claims_failed: 3
overclaim_sentences: 4
verdict: UNDETERMINED
confidence: high

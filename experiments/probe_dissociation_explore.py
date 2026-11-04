"""Exploratory follow-ups to D48, run after the frozen verdict (not part of it).

1. What does the probe's order movement follow? Within-item centred probe means per order, against
   (a) the lean of the last sub-claim asked (+1 yes-leaning, -1 no-leaning) and (b) the mean rating it got.
2. Probe shifts in units of the held-out true-minus-false separation at the selected layer.
3. B0 (no chain): probe and rating against the gold answer across the ten items (AUROC, n = 10).
"""
import json, sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))
import probe_dissociation as P

model = sys.argv[1] if len(sys.argv) > 1 else "llama3-8b"
res = json.loads((ROOT / "results" / "probe-dissociation.json").read_text())["primary"]
probes = json.loads(P.out(model, "probes").read_text())
data = json.loads(P.out(model, "run").read_text())
L, its = res["layer"], P.items()
rng = np.random.default_rng(P.SEED)
rows = []
for q, (rec, S) in its.items():
    Pm = P.order_matrix(data, q, "probe_stmt", L).mean(1)
    Vm = P.order_matrix(data, q, "M").mean(1)
    for o in range(4):
        k = S[P.LATIN[o][3]]
        last_r = np.mean([data[f"{q}|O{o+1}|{r}"]["sub"][3]["rating"] for r in range(P.R)])
        rows.append((q, Pm[o] - Pm.mean(), Vm[o] - Vm.mean(), np.sign(rec["contentions"][k]["lean"]), last_r))
qs = np.array([r[0] for r in rows]); cp, cv, lean, lr = (np.array([r[i] for r in rows], float) for i in (1, 2, 3, 4))
lr_c = lr - np.array([lr[qs == q].mean() for q in qs])


def boot_r(x, y, n=2000):
    items = sorted(set(qs)); out = []
    for _ in range(n):
        pick = rng.choice(items, len(items))
        idx = np.concatenate([np.where(qs == i)[0] for i in pick])
        if x[idx].std() > 0 and y[idx].std() > 0:
            out.append(np.corrcoef(x[idx], y[idx])[0, 1])
    return float(np.corrcoef(x, y)[0, 1]), [float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5))]


ex = {"probe_vs_last_claim_lean": boot_r(cp, lean), "probe_vs_last_claim_rating": boot_r(cp, lr_c),
      "probe_vs_rating_all10": boot_r(cp, cv), "rating_vs_last_claim_lean": boot_r(cv, lean)}
sep = {s: probes["datasets"][s]["sep"][L] for s in ("counterfact_true_false", "companies_true_false", "common_claim_true_false")}
sep_mean = float(np.mean(list(sep.values())))
order_sd_P = float(np.sqrt(np.mean([res["per_item"][q]["P_order_sd"] ** 2 for q in res["gate_items"]])))
ex["probe_units"] = {"heldout_true_minus_false_sep": sep, "D_P_over_sep": res["stats"]["D_P"] / sep_mean,
                     "order_sd_gate_over_sep": order_sd_P / sep_mean,
                     "within_cell_sd_gate_over_sep": float(np.mean([res["per_item"][q]["P_sd"] for q in res["gate_items"]])) / sep_mean}
gold = {q: its[q][0]["answer"] == "yes" for q in P.ITEMS}
y = np.array([gold[q] for q in P.ITEMS], int)
ex["B0_auroc_vs_gold"] = {"probe": P.auroc([res["per_item"][q]["B0_P"] for q in P.ITEMS], y),
                         "rating": P.auroc([res["per_item"][q]["B0_V"] for q in P.ITEMS], y)}
(ROOT / "results" / "probe-dissociation-explore.json").write_text(json.dumps(ex, indent=1))
print(json.dumps(ex, indent=1))

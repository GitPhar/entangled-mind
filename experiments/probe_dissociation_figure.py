"""The one figure for results/probe-dissociation.md: rating vs probe across chain orders, in told-range units.

    .venv/bin/python experiments/probe_dissociation_figure.py
"""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
res = json.loads((ROOT / "results" / "probe-dissociation.json").read_text())["primary"]
data = json.loads((ROOT / "results" / f"probe-dissociation-{res['model']}-run.json").read_text())
L, G, R = res["layer"], res["gate_items"], 10
D_V, D_P = res["stats"]["D_V"], res["stats"]["D_P"]
BLUE, ORANGE, INK, MUTED, GRID = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e", "#e4e3df"
plt.rcParams.update({"font.family": "sans-serif", "font.size": 10, "axes.edgecolor": MUTED,
                     "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED, "svg.fonttype": "none"})


def cells(q, cell_names, field, layer=None):
    get = lambda d: d[field][layer] if layer is not None else d[field]
    return np.array([[get(data[f"{q}|{c}|{r}"]) for r in range(R)] for c in cell_names], float)


panels = [(f"Item {q}", q) for q in G]
fig, axes = plt.subplots(1, len(panels), figsize=(3.2 * len(panels), 3.5), sharey=True)
for ax, (title, q) in zip(axes, panels):
    names, x = ["O1", "O2", "O3", "O4"], np.arange(4)
    for field, layer, D, col, lab in [("M", None, D_V, BLUE, "verbal rating"), ("probe_stmt", L, D_P, ORANGE, "truth probe")]:
        M = cells(q, names, field, layer) / D
        m, se = M.mean(1) - M.mean(), M.std(1, ddof=1) / np.sqrt(R)
        ax.errorbar(x, m, se, color=col, lw=2, marker="o", ms=7, capsize=0, elinewidth=1.5, mec="white", mew=1.5,
                    label=lab)
    ax.set_xticks(x, names)
    ax.set_xlabel("chain order", color=MUTED)
    ax.set_title(title, fontsize=10, color=INK, loc="left")
    ax.axhline(0, color=MUTED, lw=0.8)
    ax.grid(axis="y", color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
axes[0].set_ylabel("shift from the item's mean\n(1 = the told-yes vs told-no shift)")
axes[0].legend(frameon=False, loc="upper left", fontsize=9)
s, c = res["stats"], res["ci"]
fig.suptitle("The truth probe moves with chain order (in told-range units; unverified, D53)\n"
             f"Llama-3-8B, layer {L}, the 3 gate items, mean \u00b1 SE of 10 repeats; Q = {s['Q']:.2f} "
             f"[{c['Q'][0]:.2f}, {c['Q'][1]:.2f}]", x=0.01, ha="left", fontsize=10.5, color=INK)
fig.tight_layout()
out = ROOT / "paper" / "figures" / "fig3-probe-dissociation.svg"
fig.savefig(out, format="svg", bbox_inches="tight")
fig.savefig(out.with_suffix(".png"), dpi=150, bbox_inches="tight")
print(out)

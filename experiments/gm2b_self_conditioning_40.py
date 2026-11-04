"""Direction 2 on all 40 experiment-5 items, as pre-registered in experiments/gm2b-self-conditioning-40.md
(D45). Reuses last night's 10 items (results/gm2-conversations.json) and runs the other 30 with the same
code. $2.50 cap; any refusal stops the run.

    python experiments/gm2b_self_conditioning_40.py            # run (cached), then analyse
    python experiments/gm2b_self_conditioning_40.py --analyse

Writes results/gm2b-self-conditioning-40.{json,md}."""

import json
import sys

import numpy as np

import exp5_run as er
import gm2_self_conditioning as g2
from entangled_mind import config
from gm_common import PLAIN, Caller

CACHE = config.RESULTS / "gm2b-conversations.json"
PLANTED = config.EXPERIMENTS / "gm2b-planted-values.json"
OUT_JSON, OUT_MD = config.RESULTS / "gm2b-self-conditioning-40.json", config.RESULTS / "gm2b-self-conditioning-40.md"
CAP, DROP = 2.50, ("h191", "h261")


def run():
    recs = {r["id"]: r for r in json.loads(er.POOL.read_text())["records"]}
    planted = json.loads(PLANTED.read_text())["items"]
    old = json.loads(g2.PLANTED.read_text())["items"]
    new = [q for q in planted if q not in old]
    c = Caller(CACHE, CAP, "direction 2, 40 items")
    jobs = [(f"{q}|{ch}|{cond}|{r}", q, ch, cond) for q in new for ch in g2.CHAINS for cond in g2.CONDS for r in range(g2.R)]
    c.run(jobs, lambda j: g2.converse(j, recs, planted), workers=8)


def within_sd(conv, items, cond):
    return float(np.mean([np.std(g2.finals(conv, q, f"O{i}", cond), ddof=1) for q in items for i in (1, 2, 3, 4)
                          if len(g2.finals(conv, q, f"O{i}", cond)) > 1]))


def analyse():
    planted = json.loads(PLANTED.read_text())["items"]
    old = json.loads(g2.PLANTED.read_text())["items"]
    conv = {**json.loads(g2.CACHE.read_text()), **json.loads(CACHE.read_text())}
    sets = {"all 40 (primary)": list(planted), "30 new items (replication)": [q for q in planted if q not in old],
            "40 without h191 and h261 (sensitivity)": [q for q in planted if q not in DROP]}
    res = {"sets": {}, "n_new_conversations": len(json.loads(CACHE.read_text())),
           "cost_new_usd": sum(v["cost"] for v in json.loads(CACHE.read_text()).values())}
    for name, items in sets.items():
        r = g2.compute(conv, planted, items)
        pi = r["per_item"]
        nz = [q for q in items if pi[q]["OE_shown"] > 0]
        r["concentration_share"] = float(np.mean([pi[q]["OE_redacted"] >= 0.5 * pi[q]["OE_shown"] for q in nz])) if nz else float("nan")
        r["n_items_shown_OE_positive"] = len(nz)
        r["within_order_SD"] = {cond: within_sd(conv, items, cond) for cond in ("shown", "redacted")}
        res["sets"][name] = r
    res["reading"] = res["sets"]["all 40 (primary)"]["reading"]
    OUT_JSON.write_text(json.dumps(res, indent=1))
    write_md(res)


def write_md(res):
    f = lambda d, p=2: f"{d[0]:.{p}f} [{d[1]:.{p}f}, {d[2]:.{p}f}]"
    lines = ["# Direction 2 on all 40 experiment-5 items (shown, redacted, planted transcripts)", "",
             "Pre-registered in `experiments/gm2b-self-conditioning-40.md` (D45), committed before any call. Design identical to D37; "
             "last night's 10 items reused, the other 30 run now. Anchor (a) only. "
             f"{res['n_new_conversations']} new conversations, **${res['cost_new_usd']:.2f}** of the $2.50 cap; no refusal.", "", PLAIN,
             "## Order effect and its decomposition", "",
             "| item set | gate p | OE shown | OE redacted | OE high | OE low | **R = redacted / shown** | items with redacted ≥ ½ shown | within-order SD shown / redacted | reading |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for name, r in res["sets"].items():
        oe = r["OE_ci"]
        lines.append(f"| {name} | {r['gate_p']:.4f} | {f(oe['shown'], 1)} | {f(oe['redacted'], 1)} | {oe['high'][0]:.1f} | {oe['low'][0]:.1f} | "
                     f"**{f(r['R'])}** | {r['concentration_share']:.0%} of {r['n_items_shown_OE_positive']} | "
                     f"{r['within_order_SD']['shown']:.1f} / {r['within_order_SD']['redacted']:.1f} | {r['reading']} |")
    lines += ["", "## The record: planted values and replicability", "",
              "| item set | b_MF (final M follows planted first M) | next-rating pull (points) | final-M shift, O chains (points) | MF agreement shown / redacted / high / low |",
              "|---|---|---|---|---|"]
    for name, r in res["sets"].items():
        a = r["MF_agreement"]
        lines.append(f"| {name} | {f(r['b_MF'])} | {f(r['next_rating_pull'], 1)} | {f(r['final_M_shift_O'], 1)} | "
                     f"{a['shown']:.0%} / {a['redacted']:.0%} / {a['high']:.0%} / {a['low']:.0%} |")
    lines += ["", f"## Pre-registered reading (all 40): **{res['reading']}**"]
    OUT_MD.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    if "--md-only" in sys.argv:
        write_md(json.loads(OUT_JSON.read_text()))
    else:
        if "--analyse" not in sys.argv:
            run()
        analyse()

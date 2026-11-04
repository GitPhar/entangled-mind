"""Biomimetic map §3.0, source x distance x lag, as pre-registered in experiments/bm0-source-distance-lag.md
(D47). $0.50 cap; any refusal stops the run. Reuses bm1 (own, +/-30, lag 0) and run 3 (other, +/-30).

    python experiments/bm0_source_distance_lag.py            # run (cached), then analyse
    python experiments/bm0_source_distance_lag.py --analyse

Calls cached in results/bm0-calls.json. Writes results/bm0-source-distance-lag.{json,md}."""

import json
import sys

import numpy as np

from bm_runs import ITEMS, MODEL, RATE, SCALE, ask
from entangled_mind import config
from gm_common import PLAIN, Caller, structured

CACHE = config.RESULTS / "bm0-calls.json"
OUT_JSON, OUT_MD = config.RESULTS / "bm0-source-distance-lag.json", config.RESULTS / "bm0-source-distance-lag.md"
ANCHORS = config.EXPERIMENTS / "exp4-run-3-anchors.json"
CAP, SEED = 0.50, 4747
DECIDE = {"type": "object", "properties": {"decision": {"type": "string", "enum": ["accept", "revise"]},
                                           "probability": {"type": "integer"}},
          "required": ["decision", "probability"], "additionalProperties": False}
FILLER = {"type": "object", "properties": {"reply": {"type": "string", "enum": ["continue"]}}, "required": ["reply"],
          "additionalProperties": False}


def V(m, d):
    return min(98, max(2, round(m) + d))


def call(msgs, schema):
    d, raw, cost, rid = structured(MODEL, msgs, schema, "bm0", max_tokens=200)
    return d, raw, cost, rid


def converse(job, anchors):
    _, it, o, src, d, lag, _r = job
    m = anchors[it["id"]][f"m_{o}"]
    A = V(m, d)
    stmt, ctx = it[o], it["context"]
    conj_q = f"On a scale from 0 to 100{SCALE}, how likely is it that {it['X']} and {it['Y']}? Give only the number."
    cost, rids = 0.0, []
    if src == "own":
        msgs = [{"role": "user", "content": ask(stmt, ctx)}, {"role": "assistant", "content": json.dumps({"probability": A})}]
        for _ in range(lag):
            msgs.append({"role": "user", "content": "Reply with the single word: continue"})
            _, raw, c, rid = call(msgs, FILLER)
            msgs.append({"role": "assistant", "content": raw})
            cost += c
            rids.append(rid)
        msgs.append({"role": "user", "content": f"Please give your rating again. On a scale from 0 to 100{SCALE}, how likely is it that "
                                                f"{stmt}? Give only the number."})
        d1, raw1, c, rid = call(msgs, RATE)
    else:      # run 3's wording, unchanged
        q1 = (f"{ctx}\n\nAnother person estimated, on a scale from 0 to 100{SCALE}, that the probability that {stmt} is {A}. "
              "Do you accept this estimate, or would you revise it? Give the estimate you will use as a number from 0 to 100.")
        msgs = [{"role": "user", "content": q1}]
        d1, raw1, c, rid = call(msgs, DECIDE)
    cost += c
    rids.append(rid)
    r1 = min(100, max(0, int(d1["probability"]))) / 100
    msgs += [{"role": "assistant", "content": raw1}, {"role": "user", "content": conj_q}]
    d2, _, c, rid = call(msgs, RATE)
    return {"A": A / 100, "r1": r1, "r2": min(100, max(0, int(d2["probability"]))) / 100, "decision": d1.get("decision"),
            "cost": cost + c, "request_ids": rids + [rid]}


def jobs():
    items = json.loads(ITEMS.read_text())
    out = []
    for r in range(10):                       # repeat index outermost: a cap stop leaves cells balanced
        for src in ("own", "other"):
            for it in items:
                for o in ("X", "Y"):
                    for d in (-60, -10, 10, 60):
                        out.append((f"{it['id']}|{o}|{src}|{d}|lag0|{r}", it, o, src, d, 0, r))
    for r in range(20):                       # the lag arm last
        for it in items:
            for o in ("X", "Y"):
                for d in (-30, 30):
                    out.append((f"{it['id']}|{o}|own|{d}|lag3|{r}", it, o, "own", d, 3, r))
    return out


def run():
    anchors = json.loads(ANCHORS.read_text())
    c = Caller(CACHE, CAP, "bm0 source x distance x lag")
    c.run(jobs(), lambda j: converse(j, anchors), workers=8)


# --- analysis -----------------------------------------------------------------

def cells():
    """{(item, o, src, d, lag): [rows]} merging the new cache with bm1 (own +/-30 lag 0) and run 3 (other +/-30)."""
    out = {}
    for k, v in json.loads(CACHE.read_text()).items():
        q, o, src, d, lag, _ = k.split("|")
        out.setdefault((q, o, src, int(d), int(lag[3:])), []).append(v)
    for path, src in ((config.RESULTS / "bm1-calls.json", "own"), (config.RESULTS / "exp4-run-3-calls.json", "other")):
        for k, v in json.loads(path.read_text()).items():
            q, cell, _ = k.split("|")
            if cell[1:] in ("-lo", "-hi"):
                out.setdefault((q, cell[0], src, -30 if cell.endswith("lo") else 30, 0), []).append(v)
    return out


def analyse():
    items = [it["id"] for it in json.loads(ITEMS.read_text())]
    run3 = json.loads((config.RESULTS / "exp4-run-3-calls.json").read_text())
    base = {(q, o): float(np.mean([v["r1"] for k, v in run3.items() if k.startswith(f"{q}|{o}->XY|")])) for q in items for o in "XY"}
    C = cells()
    rows, dropped = [], 0
    for (q, o, src, d, lag), vs in C.items():
        b = base[(q, o)]
        D = float(np.mean([v["A"] for v in vs])) - b
        shift = float(np.mean([v["r1"] for v in vs])) - b
        if abs(D) < 0.05:
            dropped += 1
            continue
        rows.append({"item": q, "o": o, "src": src, "d": d, "lag": lag, "D": D, "shift": shift, "u": shift / D, "n": len(vs)})
    by_item = {q: [r for r in rows if r["item"] == q] for q in items}
    rng = np.random.default_rng(SEED)
    samples = [list(rng.choice(items, len(items))) for _ in range(2000)]

    def boot(fn):
        point = fn(items)
        vals = np.array([fn(s) for s in samples], float)
        return [float(point), *map(float, np.nanpercentile(vals, [2.5, 97.5]))]

    def sel(s, **kw):
        return [r for q in s for r in by_item[q] if all(r[k] == v for k, v in kw.items())]

    def paired(s, cls=None, lag=0):
        diffs = []
        for q in s:
            for o in "XY":
                for d in ((-cls, cls) if cls else (-60, -30, -10, 10, 30, 60)):
                    a = [r["u"] for r in by_item[q] if r["o"] == o and r["src"] == "own" and r["d"] == d and r["lag"] == lag]
                    b = [r["u"] for r in by_item[q] if r["o"] == o and r["src"] == "other" and r["d"] == d and r["lag"] == 0]
                    if a and b:
                        diffs.append(a[0] - b[0])
        return np.mean(diffs) if diffs else np.nan
    res = {"dropped_cells_small_D": dropped, "n_cells": len(rows)}
    res["source_all"] = boot(lambda s: paired(s))
    res["source_by_class"] = {c: boot(lambda s, c=c: paired(s, c)) for c in (10, 30, 60)}
    res["u_mean"] = {f"{src}|{c}": boot(lambda s, src=src, c=c: np.mean([r["u"] for r in sel(s, src=src, lag=0) if abs(r["d"]) == c]))
                     for src in ("own", "other") for c in (10, 30, 60)}

    def quad(s):
        rr = sel(s, src="own", lag=0)
        D = np.array([r["D"] for r in rr])
        X = np.column_stack([D, D * np.abs(D)])
        return np.linalg.lstsq(X, np.array([r["shift"] for r in rr]), rcond=None)[0]
    b = quad(items)
    bb = np.array([quad(s) for s in samples])
    res["quad_beta"] = b.tolist()
    res["quad_beta_ci95"] = np.percentile(bb, [2.5, 97.5], axis=0).tolist()
    maxD = float(max(abs(r["D"]) for r in sel(items, src="own", lag=0)))
    res["turning_point"] = float(b[0] / (2 * abs(b[1]))) if b[1] < 0 else None
    res["max_abs_D"] = maxD
    res["attraction_60"] = boot(lambda s: np.mean([np.sign(r["D"]) * r["shift"] for r in sel(s, src="own", lag=0) if abs(r["d"]) == 60]))

    def lagdiff(s):
        diffs = []
        for q in s:
            for o in "XY":
                for d in (-30, 30):
                    a = [r["u"] for r in by_item[q] if r["o"] == o and r["src"] == "own" and r["d"] == d and r["lag"] == 0]
                    c3 = [r["u"] for r in by_item[q] if r["o"] == o and r["src"] == "own" and r["d"] == d and r["lag"] == 3]
                    if a and c3:
                        diffs.append(a[0] - c3[0])
        return np.mean(diffs) if diffs else np.nan
    res["lag_decay"] = boot(lagdiff)
    res["u_own_lag3"] = boot(lambda s: np.mean([r["u"] for r in sel(s, src="own", lag=3)]) if sel(s, src="own", lag=3) else np.nan)
    oth_new = [r for r in rows if r["src"] == "other" and abs(r["d"]) in (10, 60)]
    res["reactance"] = {"mean_u_other_new": float(np.mean([r["u"] for r in oth_new])),
                        "item_orders_u_other_negative": int(sum(r["u"] < 0 for r in oth_new)), "n": len(oth_new)}
    src_ok = res["source_all"][1] > 0
    nonmono = res["quad_beta_ci95"][1][1] < 0 and res["turning_point"] is not None and res["turning_point"] < maxD
    reversal = res["attraction_60"][2] < 0
    lag = res["lag_decay"]
    lag_read = "decays" if lag[1] > 0 else ("grows" if lag[2] < 0 else "no detectable change")
    other_nonneg = res["u_mean"]["other|10"][0] >= 0 and res["u_mean"]["other|60"][0] >= 0
    if src_ok and lag_read != "decays":
        overall = "self-consistency"
    elif not src_ok and (nonmono or reversal) and lag_read == "decays":
        overall = "serial dependence"
    elif not src_ok and not (nonmono or reversal) and other_nonneg:
        overall = "anchoring / precision"
    else:
        overall = "mixed"
    res.update(reading_source="own > other" if src_ok else "own not reliably above other",
               reading_distance="reversal" if reversal else ("non-monotone" if nonmono else "monotone"),
               reading_lag=lag_read, reading=overall)
    new = json.loads(CACHE.read_text())
    res["n_new_conversations"], res["cost_new_usd"] = len(new), sum(v["cost"] for v in new.values())
    res["rows"] = rows
    OUT_JSON.write_text(json.dumps(res, indent=1))
    write_md(res)


def write_md(r):
    f = lambda d, p=2: f"{d[0]:+.{p}f} [{d[1]:+.{p}f}, {d[2]:+.{p}f}]"
    lines = ["# Biomimetic §3.0: source × distance × lag", "",
             "Pre-registered in `experiments/bm0-source-distance-lag.md` (D47), committed before any call. Run 3's 16 items, one scale "
             f"direction; own ±30 lag 0 from bm1 and other ±30 from run 3 (archived). {r['n_new_conversations']} new conversations, "
             f"**${r['cost_new_usd']:.2f}** of the $0.50 cap; no refusal. Cells dropped for |D| < 0.05 after clipping: "
             f"{r['dropped_cells_small_D']} of {r['n_cells'] + r['dropped_cells_small_D']}.", "", PLAIN,
             "## Uptake u = shift / displacement (1 = takes the value fully, 0 = ignores it, < 0 = moves away)", "",
             "| distance |d| | own (lag 0) | other | own − other (paired) |", "|---|---|---|---|"]
    for c in (10, 30, 60):
        lines.append(f"| {c} | {f(r['u_mean'][f'own|{c}'])} | {f(r['u_mean'][f'other|{c}'])} | {f(r['source_by_class'][c])} |")
    lines += ["", f"- **Source, pooled over distances: own − other = {f(r['source_all'])}** → {r['reading_source']}.",
              f"- **Distance (own, lag 0):** shift = β₁·D + β₂·D·|D|: β₁ = {r['quad_beta'][0]:+.2f} [{r['quad_beta_ci95'][0][0]:+.2f}, "
              f"{r['quad_beta_ci95'][1][0]:+.2f}], β₂ = {r['quad_beta'][1]:+.2f} [{r['quad_beta_ci95'][0][1]:+.2f}, {r['quad_beta_ci95'][1][1]:+.2f}]"
              + (f"; turning point |D*| = {r['turning_point']:.2f} (largest tested |D| {r['max_abs_D']:.2f})" if r["turning_point"] else "")
              + f"; sign-adjusted attraction at |d| = 60: {f(r['attraction_60'])} → {r['reading_distance']}.",
              f"- **Lag (own, ±30):** uptake at lag 3 {f(r['u_own_lag3'])}; lag 0 − lag 3 = {f(r['lag_decay'])} → {r['reading_lag']}.",
              f"- Reactance check, other at ±10 and ±60: mean u = {r['reactance']['mean_u_other_new']:+.2f}; "
              f"{r['reactance']['item_orders_u_other_negative']} of {r['reactance']['n']} cells below 0.", "",
              f"## Pre-registered reading: **{r['reading']}**"]
    OUT_MD.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    if "--md-only" in sys.argv:
        write_md(json.loads(OUT_JSON.read_text()))
    else:
        if "--analyse" not in sys.argv:
            run()
        analyse()

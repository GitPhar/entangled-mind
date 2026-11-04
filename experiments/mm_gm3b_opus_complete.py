"""Completion of Opus's six-format arm, as pre-registered in experiments/mm-gm3b-opus-completion.md (D49).

    python experiments/mm_gm3b_opus_complete.py --dry     # request counts and order, no calls
    python experiments/mm_gm3b_opus_complete.py run       # one batch per item, $6.40 cap on new spend, stop on refusal
    python experiments/mm_gm3b_opus_complete.py analyse   # DM2's frozen analysis on all models, then test F' on Opus's complete items

Prompts, schemas, parsing, cache and analysis are mm_gm3b.py's (DM2), imported unchanged. Writes
results/mm-gm3b-format-invariance.{json,md} (via mm_gm3b.analyse) and results/mm-gm3b-opus-completion.{json,md}."""

import json
import sys

import numpy as np

import exp5_run as er
import gm3b_format_invariance as g
import gm3c_heldout_format as gc
import mm_common as mc
import mm_gm3b as mm
from entangled_mind import config

CAP, EST = 6.40, 0.00194              # EST: Opus's observed batch cost per call on its first 1,600 calls (DM2)
OUT_JSON, OUT_MD = config.RESULTS / "mm-gm3b-opus-completion.json", config.RESULTS / "mm-gm3b-opus-completion.md"
FIRST26 = config.RESULTS / "mm-gm3b-opus-first26.json"
BEYOND = config.RESULTS / "mm-gm3b-opus-h291-beyond-stop.json"   # D49a: ran past the frozen stopping rule; sensitivity only   # the 26 claims complete before this run, frozen at pre-registration


def item_order():
    """h221 (partly run) first, then Haiku-right and Haiku-wrong items alternating, so a cap stop stays balanced."""
    it = mm.items20()
    cache = json.loads(mm.cache_path("opus").read_text())
    touched = {k.split("|")[0] for k in cache}
    rest_wrong = [q for q in it[:10] if q not in touched]
    rest_right = [q for q in it[10:]]
    partial = [q for q in it if q in touched and
               not all(f"{q}|{k}|{f}|{r}" in cache for qq, k in mm.claims80() if qq == q for f in g.FORMATS for r in range(g.R))]
    order = list(partial)
    while rest_wrong or rest_right:
        if rest_right:
            order.append(rest_right.pop(0))
        if rest_wrong:
            order.append(rest_wrong.pop(0))
    return order


def requests_for(q, cache, recs):
    reqs = {}
    for qq, k in mm.claims80():
        if qq != q:
            continue
        for fmt in g.FORMATS:
            for r in range(g.R):
                key = f"{q}|{k}|{fmt}|{r}"
                if key not in cache:
                    text, schema = g.prompt(recs[q], k, fmt, r)
                    reqs[key] = mc.params(mm.MODELS["opus"], [{"role": "user", "content": text}], schema, max_tokens=1000)
    return reqs


def run(dry=False):
    path = mm.cache_path("opus")
    cache = json.loads(path.read_text())
    spent0 = sum(v["cost"] for v in cache.values())
    recs = {r["id"]: r for r in json.loads(er.POOL.read_text())["records"]}
    order = item_order()
    plan = [(q, requests_for(q, cache, recs)) for q in order]
    print(f"opus completion: {sum(len(r) for _, r in plan)} requests over {len(order)} items, {len(cache)} cached (${spent0:.2f} before this run)")
    for q, r in plan:
        print(f"  {q}: {len(r)} requests, ~${len(r) * EST:.2f}")
    if dry:
        return
    new_spent = lambda: sum(v["cost"] for v in cache.values()) - spent0
    br = mc.BatchRunner("gm3b-opus-completion", CAP, new_spent, chunk=10_000)   # one batch per item
    est = EST
    for q, reqs in plan:
        if reqs:
            est = br.run(reqs, lambda k, msg: {"value": next(iter(json.loads(mc.text_of(msg)).values()))},
                         cache.__setitem__, lambda: path.write_text(json.dumps(cache)), est)
            print(f"opus completion: {q} done, new spend ${new_spent():.3f}", flush=True)


def heldout_on_complete():
    """Test F' (gm3c's frozen analysis) on Opus's complete claims; on all 80 when the arm is complete."""
    conv = {k: v for k, v in json.loads(mm.cache_path("opus").read_text()).items() if "value" in v and v["value"] is not None}
    done = [(q, k) for q, k in mm.claims80() if all(f"{q}|{k}|{f}|{r}" in conv for f in g.FORMATS for r in range(g.R))]
    items_done = {q for q, _ in done}
    done = [(q, k) for q, k in done if all((q, kk) in set(done) for qq, kk in mm.claims80() if qq == q)]   # whole items only
    conv = {key: v for key, v in conv.items() if (key.split("|")[0], int(key.split("|")[1])) in set(done)}
    tmp = config.RESULTS / ".mm-opus-completion-tmp.json"
    tmp.write_text(json.dumps(conv))
    g.CACHE, g.claims = tmp, (lambda: done)
    gc.OUT_JSON, gc.OUT_MD = config.RESULTS / ".mm-opus-gm3c.json", config.RESULTS / ".mm-opus-gm3c.md"
    gc.main()
    res = json.loads(gc.OUT_JSON.read_text())
    for p in (tmp, gc.OUT_JSON, gc.OUT_MD):
        p.unlink(missing_ok=True)
    res["claims"], res["items"] = len(done), sorted({q for q, _ in done})
    return res, items_done


def paper_reading(primary, q_ci):
    """The rule frozen in mm-gm3b-opus-completion.md section 4 for the paper's Opus claim."""
    lo, hi = q_ci
    if lo > 0.75:
        return "does not hold on Opus: one credence predicts each left-out format close to its own ceiling"
    if hi < 0.5 and primary.startswith("no single credence"):
        return "holds on Opus"
    return "holds partly on Opus"


def analyse():
    mm.analyse()                                   # DM2's frozen analysis, rewritten with the completed Opus arm
    g.CACHE, g.claims = config.RESULTS / "gm3b-calls.json", mm._ALL_CLAIMS
    o = json.loads(mm.OUT_JSON.read_text())
    h, _ = heldout_on_complete()
    g.CACHE, g.claims = config.RESULTS / "gm3b-calls.json", mm._ALL_CLAIMS
    first26 = json.loads(FIRST26.read_text())
    op = o["opus"]
    res = {"primary_reading": op["reading"], "dLL": op["dLL"], "kendall_W": {m: o[m]["kendall_W"] for m in ("haiku", "sonnet", "opus")},
           "claims_complete": op["claims_complete"], "heldout_format": h, "cost_new_usd": None, "first26": first26}
    cache = json.loads(mm.cache_path("opus").read_text())
    res["cost_total_usd"] = sum(v["cost"] for v in cache.values())
    res["cost_new_usd"] = res["cost_total_usd"] - first26["cost_usd"]
    res["refusals"] = sum(1 for v in cache.values() if v.get("refused"))
    res["max_tokens"] = sum(1 for v in cache.values() if v.get("error") == "max_tokens")
    # exploratory split (pre-registered as descriptive): Opus's ΔLL on the 26 earlier claims against the rest
    conv = {k: v for k, v in cache.items() if "value" in v and v["value"] is not None}
    done = [(q, k) for q, k in mm.claims80() if all(f"{q}|{k}|{f}|{rr}" in conv for f in g.FORMATS for rr in range(g.R))]
    vals = dict(zip(done, op["per_claim_dLL"]))       # per_claim_dLL follows the complete claims in claims80 order
    old = set(map(tuple, first26["claims"]))
    res["dLL_first26_mean"] = float(np.mean([v for c, v in vals.items() if c in old]))
    res["dLL_rest_mean"] = float(np.mean([v for c, v in vals.items() if c not in old])) if len(vals) > len(old) else None
    res["paper_reading"] = paper_reading(op["reading"], h["mean_Q_ci95"])
    OUT_JSON.write_text(json.dumps(res, indent=1))
    write_md(res, o)


def write_md(r, o):
    h, d = r["heldout_format"], r["dLL"]
    L = ["# Opus six-format arm completed (80 claims), with test F′", "",
         "Pre-registered in `experiments/mm-gm3b-opus-completion.md` (D49), committed before any call. DM2's design, prompts and analysis "
         f"unchanged; the 54 claims the DM2 budget stopped are run now. **${r['cost_new_usd']:.2f}** new spend of the $6.40 cap "
         f"(${r['cost_total_usd']:.2f} for the whole Opus arm, batch rate); {r['refusals']} refusals; {r['max_tokens']} max_tokens stops.", "",
         "## In plain English", "", "(Hand-written after the run; excluded from reproduce.py's comparison.)", "",
         "## Primary (DM2's rule): one credence (L1) against one per format (L6)", "",
         "| Opus claims complete | mean ΔLL per claim [95% CI] | claims with ΔLL > 0 | reading |", "|---|---|---|---|",
         f"| {r['claims_complete']} | {d['mean']:+.2f} [{d['ci95'][0]:+.2f}, {d['ci95'][1]:+.2f}] | {d['share_positive']:.0%} | **{r['primary_reading']}** |",
         "", f"Before this run (26 claims, DM2): {r['first26']['dLL']['mean']:+.2f} [{r['first26']['dLL']['ci95'][0]:+.2f}, "
         f"{r['first26']['dLL']['ci95'][1]:+.2f}], {r['first26']['dLL']['share_positive']:.0%} positive, W {r['first26']['kendall_W']:.2f}.", "",
         "## Test F′ (D46's frozen analysis): predicting each format from the other five", "",
         f"On {h['claims']} claims ({len(h['items'])} items).", "",
         "| held-out format | R² from the other five | R² ceiling | Q |", "|---|---|---|---|"]
    for f, v in h["formats"].items():
        L.append(f"| {g.NAMES[f]} | {v['R2_cross']:.2f} | {v['R2_ceiling']:.2f} | {v['Q']:.2f} |")
    L += ["", f"- **Mean Q = {h['mean_Q']:.2f} [{h['mean_Q_ci95'][0]:.2f}, {h['mean_Q_ci95'][1]:.2f}]**: {h['reading']}.",
          f"- Mean R² from the other five: {h['mean_R2_cross']:.2f} [{h['mean_R2_cross_ci95'][0]:.2f}, {h['mean_R2_cross_ci95'][1]:.2f}].", "",
          f"## Kendall's W (Haiku and Sonnet on the 80 claims; Opus on its {r['claims_complete']} complete claims)", "",
          "| Haiku | Sonnet | Opus |", "|---|---|---|",
          f"| {r['kendall_W']['haiku']:.2f} | {r['kendall_W']['sonnet']:.2f} | {r['kendall_W']['opus']:.2f} |", ""]
    if r.get("dLL_rest_mean") is not None:
        L += [f"Descriptive: Opus's mean ΔLL on the 26 earlier claims {r['dLL_first26_mean']:+.2f}; on the others {r['dLL_rest_mean']:+.2f}.", ""]
    L += [f"## Pre-registered reading for the paper's Opus claim: **{r['paper_reading']}**"]
    OUT_MD.write_text("\n".join(L) + "\n")
    print("\n".join(L))


def analyse_with_h291():
    """D49a sensitivity: h291 ran past the frozen stopping rule (results/mm-gm3b-opus-h291-beyond-stop.json); same analysis with it added."""
    global OUT_JSON, OUT_MD
    merged = {**json.loads(mm.cache_path("opus").read_text()), **json.loads(BEYOND.read_text())}
    tmp = config.RESULTS / ".mm-gm3b-opus-with-h291-calls.json"
    tmp.write_text(json.dumps(merged))
    orig = mm.cache_path
    mm.cache_path = lambda m: tmp if m == "opus" else orig(m)
    mm.OUT_JSON, mm.OUT_MD = config.RESULTS / ".mm-gm3b-with-h291.json", config.RESULTS / ".mm-gm3b-with-h291.md"
    OUT_JSON, OUT_MD = config.RESULTS / "mm-gm3b-opus-completion-with-h291.json", config.RESULTS / "mm-gm3b-opus-completion-with-h291.md"
    try:
        analyse()
    finally:
        for p in (tmp, mm.OUT_JSON, mm.OUT_MD):
            p.unlink(missing_ok=True)


if __name__ == "__main__":
    if "--with-h291" in sys.argv:
        analyse_with_h291()
    elif "--dry" in sys.argv:
        run(dry=True)
    elif sys.argv[1] == "run":
        mc.main_guard(run)
    else:
        analyse()

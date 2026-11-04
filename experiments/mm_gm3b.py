"""Multi-model replication of direction 3 (six formats), as pre-registered in experiments/mm-gm3b-format-invariance.md (DM2).

    python experiments/mm_gm3b.py run sonnet|opus      # batches (cached), capped, stop on refusal
    python experiments/mm_gm3b.py analyse              # every model with data, plus the Haiku reference on the same 80 claims

Prompts, schemas, repeats, encoding, models (L1, L6), fitting, folds and bootstrap are those of gm3b_format_invariance.py,
imported unchanged. Calls cached in results/mm-gm3b-<model>-calls.json; writes results/mm-gm3b-format-invariance.{json,md}."""

import json
import sys

import numpy as np

import exp5_run as er
import gm3b_format_invariance as g
import gm3c_heldout_format as gc
import mm_common as mc
from entangled_mind import config

CAPS = {"sonnet": 2.2, "opus": 4.3}
EST = {"sonnet": 0.0004, "opus": 0.0009}            # per request at the batch rate, from the DM1 pilot
MODELS = {"sonnet": mc.S, "opus": mc.O}
OUT_JSON, OUT_MD = config.RESULTS / "mm-gm3b-format-invariance.json", config.RESULTS / "mm-gm3b-format-invariance.md"
_ALL_CLAIMS = g.claims


def items20():
    c = json.loads(er.SPLIT.read_text())["candidates"]
    return c[0:10] + c[20:30]           # 10 items Haiku got wrong, 10 it got right (the candidate list is 20 wrong, then 20 right)


def claims80():
    keep = set(items20())
    return [(q, k) for q, k in _ALL_CLAIMS() if q in keep]


def cache_path(m):
    return config.RESULTS / f"mm-gm3b-{m}-calls.json"


def run(m):
    model, path = MODELS[m], cache_path(m)
    cache = json.loads(path.read_text()) if path.exists() else {}
    recs = {r["id"]: r for r in json.loads(er.POOL.read_text())["records"]}
    reqs = {}
    for q, k in claims80():
        for fmt in g.FORMATS:
            for r in range(g.R):
                key = f"{q}|{k}|{fmt}|{r}"
                if key not in cache:
                    text, schema = g.prompt(recs[q], k, fmt, r)
                    reqs[key] = mc.params(model, [{"role": "user", "content": text}], schema, max_tokens=1000)
    print(f"{m}: {len(reqs)} requests to run, {len(cache)} cached", flush=True)
    br = mc.BatchRunner(f"gm3b-{m}", CAPS[m], lambda: sum(v["cost"] for v in cache.values()), chunk=400 if m == "sonnet" else 1600)   # DM2a
    br.run(reqs, lambda k, msg: {"value": next(iter(json.loads(mc.text_of(msg)).values()))},
           cache.__setitem__, lambda: path.write_text(json.dumps(cache)), EST[m])


def analyse_one(cache_file, label):
    """Runs gm3b's frozen analysis and gm3c's held-out-format analysis on one model's calls, restricted to the 80 claims."""
    conv = {k: v for k, v in json.loads(cache_file.read_text()).items() if "value" in v and v["value"] is not None}
    # DM4a: only claims with all 60 calls (6 formats x 10 repeats) enter the analysis
    done = [(q, k) for q, k in claims80() if all(f"{q}|{k}|{f}|{r}" in conv for f in g.FORMATS for r in range(g.R))]
    conv = {key: v for key, v in conv.items() if (key.split("|")[0], int(key.split("|")[1])) in set(done)}
    tmp = config.RESULTS / f".mm-gm3b-{label}-tmp.json"
    tmp.write_text(json.dumps(conv))
    g.CACHE, g.claims = tmp, (lambda: done)
    g.OUT_JSON, g.OUT_MD = config.RESULTS / f".mm-gm3b-{label}.json", config.RESULTS / f".mm-gm3b-{label}.md"
    g.write_md = lambda r: None
    g.analyse()
    res = json.loads(g.OUT_JSON.read_text())
    gc.OUT_JSON, gc.OUT_MD = config.RESULTS / f".mm-gm3c-{label}.json", config.RESULTS / f".mm-gm3c-{label}.md"
    if len(done) == len(claims80()):            # test F' only on complete arms: its fold rule needs the 20 items
        gc.main()
        res["heldout_format"] = json.loads(gc.OUT_JSON.read_text())
    else:
        res["heldout_format"] = None
    for p in (tmp, g.OUT_JSON, g.OUT_MD, gc.OUT_JSON, gc.OUT_MD):
        p.unlink(missing_ok=True)
    res["n_calls_used"] = len(conv)
    res["n_calls_expected"] = len(claims80()) * 6 * g.R
    res["claims_complete"] = len(done)
    res["items_complete"] = sorted({q for q, _ in done})
    return res


def analyse():
    out = {"items": items20(), "n_claims": len(claims80())}
    sources = [("haiku (archived, same 80 claims)", g.CACHE)] + [(m, cache_path(m)) for m in MODELS if cache_path(m).exists()]
    for label, path in sources:
        key = label.split()[0]
        r = analyse_one(path, key)
        full = json.loads(path.read_text())
        r["cost_usd"] = sum(v["cost"] for k, v in full.items() if tuple([k.split("|")[0], int(k.split("|")[1])]) in set(claims80()))
        r["refusals"] = sum(1 for v in full.values() if v.get("refused"))
        r["max_tokens"] = sum(1 for v in full.values() if v.get("error") == "max_tokens")
        out[key] = r
        g.CACHE = config.RESULTS / "gm3b-calls.json"
    OUT_JSON.write_text(json.dumps(out, indent=1))
    write_md(out)


def write_md(o):
    models = [m for m in ("haiku", "sonnet", "opus") if m in o]
    L = ["# Multi-model replication of direction 3: six elicitation formats (80 claims)", "",
         "Pre-registered in `experiments/mm-gm3b-format-invariance.md` (DM2), committed before any call. 20 of the 40 experiment-5 "
         "items (10 Haiku got wrong, 10 it got right), their 80 chain claims, six formats × 10 repeats, one scale direction. "
         "Haiku's row re-analyses its archived calls (D38) on the same 80 claims; Sonnet and Opus are new. Costs are at the batch rate.", "",
         "## In plain English", "", "(Hand-written after the run; excluded from reproduce.py's comparison.)", "",
         "## Primary: one credence (L1) against one per format (L6), held-out repeats", "",
         "| model | claims (items) complete | calls used / expected | cost | mean ΔLL per claim [95% CI] | claims with ΔLL > 0 | reading |", "|---|---|---|---|---|---|---|"]
    for m in models:
        r, d = o[m], o[m]["dLL"]
        L.append(f"| {m} | {r['claims_complete']} ({len(r['items_complete'])}) | {r['n_calls_used']} / {r['n_calls_expected']} | ${r['cost_usd']:.2f} | {d['mean']:+.2f} [{d['ci95'][0]:+.2f}, "
                 f"{d['ci95'][1]:+.2f}] | {d['share_positive']:.0%} | **{r['reading']}** |")
    L += ["", "## Agreement between formats", "", "| model | Kendall's W | Spearman ρ range | discordant pairs vs the 0–100 rating, range |",
          "|---|---|---|---|"]
    for m in models:
        r = o[m]
        sp, dc = list(r["spearman"].values()), list(r["discordant_vs_F1"].values())
        L.append(f"| {m} | {r['kendall_W']:.2f} | {min(sp):+.2f} to {max(sp):+.2f} | {min(dc):.0%} to {max(dc):.0%} |")
    L += ["", "## ΔLL by format (mean per claim)", "", "| format | " + " | ".join(models) + " |", "|---|" + "---|" * len(models)]
    for f in g.FORMATS:
        L.append(f"| {g.NAMES[f]} | " + " | ".join(f"{o[m]['dLL']['by_format_mean'][f]:+.3f}" for m in models) + " |")
    L += ["", "## Secondary: held-out-format prediction (test F′'s frozen analysis, D46)", "",
          "| model | mean Q [95% CI] | mean R² from the other five | reading |", "|---|---|---|---|"]
    for m in models:
        h = o[m]["heldout_format"]
        if h is None:
            L.append(f"| {m} | not computed: arm incomplete ({o[m]['claims_complete']} of 80 claims) | | |")
            continue
        L.append(f"| {m} | {h['mean_Q']:.2f} [{h['mean_Q_ci95'][0]:.2f}, {h['mean_Q_ci95'][1]:.2f}] | {h['mean_R2_cross']:.2f} | {h['reading']} |")
    OUT_MD.write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    if sys.argv[1] == "run":
        mc.main_guard(lambda: run(sys.argv[2]))
    else:
        analyse()

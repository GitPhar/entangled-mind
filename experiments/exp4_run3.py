"""Experiment 4, run 3: a manipulated first rating, as frozen in experiments/exp4-run-3.md (with the D33
amendment: one scale direction, 0 = certainly false, 100 = certainly true).

    python experiments/exp4_run3.py

Cells per item: X-lo, X-hi, Y-lo, Y-hi (provided first rating, accept or revise; R = 40), X->XY and
Y->XY (free first rating; R = 20), XY (conjunction alone; R = 20). Base model claude-haiku-5-5,
thinking disabled, default temperature. $2 cap; any refusal stops the run. Calls cached in
results/exp4-run-3-calls.json. Writes results/exp4-run-3.{json,md}."""

import json
import math
import sys
import threading
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from dotenv import load_dotenv

from entangled_mind import config, llm

load_dotenv(config.ROOT / ".env")
ITEMS = config.EXPERIMENTS / "exp4-items.json"
ANCHORS = config.EXPERIMENTS / "exp4-run-3-anchors.json"
RUN1 = config.RESULTS / "exp4-run-1.json"
CALLS = config.RESULTS / "exp4-run-3-calls.json"
OUT_JSON, OUT_MD = config.RESULTS / "exp4-run-3.json", config.RESULTS / "exp4-run-3.md"
MODEL, BUDGET, N_BOOT = "claude-haiku-5-5", 2.0, 1000
SCALE = ", where 0 = certainly false and 100 = certainly true"
RATE = {"type": "object", "properties": {"probability": {"type": "integer"}}, "required": ["probability"], "additionalProperties": False}
DECIDE = {"type": "object", "properties": {"decision": {"type": "string", "enum": ["accept", "revise"]},
                                           "probability": {"type": "integer"}},
          "required": ["decision", "probability"], "additionalProperties": False}
CELLS = {"X-lo": ("X", "lo", 40), "X-hi": ("X", "hi", 40), "Y-lo": ("Y", "lo", 40), "Y-hi": ("Y", "hi", 40),
         "X->XY": ("X", None, 20), "Y->XY": ("Y", None, 20), "XY": (None, None, 20)}

_cache, _lock, _stop, _refusal = {}, threading.Lock(), threading.Event(), {}


def conj(it):
    return f"{it['X']} and {it['Y']}"


def call(msgs, schema):
    resp = llm.client().messages.create(model=MODEL, max_tokens=200, thinking={"type": "disabled"},
                                        output_config={"format": {"type": "json_schema", "schema": schema}}, messages=msgs)
    llm._check_stop(resp, "exp4-run3")
    text = next(b.text for b in resp.content if b.type == "text")
    return text, json.loads(text), llm._usage(resp).cost, getattr(resp, "_request_id", None)


def run_conv(it, anchors, cell, rep):
    key = f"{it['id']}|{cell}|{rep}"
    if key in _cache or _stop.is_set():
        return
    with _lock:
        if sum(v["cost"] for v in _cache.values()) >= BUDGET:
            _stop.set()
            return
    first, level, _ = CELLS[cell]
    ctx = it["context"]
    conj_q = f"On a scale from 0 to 100{SCALE}, how likely is it that {conj(it)}? Give only the number."
    out, cost, rids = {}, 0.0, []
    try:
        if first is None:
            _, d, c, r = call([{"role": "user", "content": f"{ctx}\n\n{conj_q}"}], RATE)
            out = {"r2": min(100, max(0, d["probability"])) / 100}
            cost, rids = c, [r]
        else:
            stmt = it[first]
            if level is None:
                q1 = f"{ctx}\n\nOn a scale from 0 to 100{SCALE}, how likely is it that {stmt}? Give only the number."
                schema = RATE
            else:
                A = anchors[it["id"]][f"A_{first}"][0 if level == "lo" else 1]
                q1 = (f"{ctx}\n\nAnother person estimated, on a scale from 0 to 100{SCALE}, that the probability that "
                      f"{stmt} is {A}. Do you accept this estimate, or would you revise it? Give the estimate you will use "
                      "as a number from 0 to 100.")
                schema = DECIDE
                out["A"] = A / 100
            t1, d1, c1, r1 = call([{"role": "user", "content": q1}], schema)
            out["r1"] = min(100, max(0, d1["probability"])) / 100
            if "decision" in d1:
                out["decision"] = d1["decision"]
            msgs = [{"role": "user", "content": q1}, {"role": "assistant", "content": t1}, {"role": "user", "content": conj_q}]
            _, d2, c2, r2 = call(msgs, RATE)
            out["r2"] = min(100, max(0, d2["probability"])) / 100
            cost, rids = c1 + c2, [r1, r2]
    except llm.RefusalError as e:
        _refusal.setdefault("e", (key, e))
        _stop.set()
        return
    with _lock:
        _cache[key] = {**out, "cost": cost, "request_ids": rids}


def fit(rows):
    """r2 = b0 + b1 r1 + b2 A; falls back to r2 = b0 + b1 r1 if collinear (D33)."""
    r1, r2, A = (np.array([x[k] for x in rows]) for k in ("r1", "r2", "A"))
    X = np.column_stack([np.ones(len(r1)), r1, A])
    if np.linalg.cond(X) > 1e6:
        X = X[:, :2]
        b = np.linalg.lstsq(X, r2, rcond=None)[0]
        return float(b[0]), float(b[1]), None
    b = np.linalg.lstsq(X, r2, rcond=None)[0]
    return float(b[0]), float(b[1]), float(b[2])


def main() -> None:
    global _cache
    items = json.loads(ITEMS.read_text())
    anchors = {q: {"A_X": v["A_X"], "A_Y": v["A_Y"]} for q, v in json.loads(ANCHORS.read_text()).items()}
    _cache = json.loads(CALLS.read_text()) if CALLS.exists() else {}
    jobs = [(it, cell, k) for it in items for cell, (_, _, R) in CELLS.items() for k in range(R)]
    with ThreadPoolExecutor(max_workers=8) as ex:
        list(ex.map(lambda j: run_conv(j[0], anchors, j[1], j[2]), jobs))
    CALLS.write_text(json.dumps(_cache))
    if _refusal:
        key, e = _refusal["e"]
        (config.RESULTS / "refusal.md").write_text(
            f"# Pipeline stopped on a refusal\n\nExperiment 4 run 3, conversation `{key}`\n\nRefused call: **{e.call}**\n\n"
            f"Request ID: `{e.request_id}`\n\nExact stop details:\n\n```\n{e.stop_details}\n```\n\nNothing was reworded or retried.\n")
        sys.exit(f"STOPPED: {e}")
    if _stop.is_set():
        sys.exit("budget stop")
    analyse(items)


def analyse(items) -> None:
    rng = np.random.default_rng(31)
    fallacy = set(json.loads(RUN1.read_text())["fallacy_items"])
    get = lambda q, cell: [_cache[f"{q}|{cell}|{k}"] for k in range(CELLS[cell][2]) if f"{q}|{cell}|{k}" in _cache]
    per = {}
    for it in items:
        q = it["id"]
        fresh = float(np.mean([x["r2"] for x in get(q, "XY")]))
        pX = float(np.mean([x["r1"] for x in get(q, "X->XY")]))
        pY = float(np.mean([x["r1"] for x in get(q, "Y->XY")]))
        o_run2 = float(np.mean([x["r2"] for x in get(q, "X->XY")]) - np.mean([x["r2"] for x in get(q, "Y->XY")]))
        res = {"fresh": fresh, "P_X": pX, "P_Y": pY, "o_free": o_run2, "orders": {}}
        boots = {}
        for o in ("X", "Y"):
            lo, hi = get(q, f"{o}-lo"), get(q, f"{o}-hi")
            manip = float(np.mean([x["r1"] for x in hi]) - np.mean([x["r1"] for x in lo]))
            rows = lo + hi
            b0, b1, b2 = fit(rows)
            bs = []
            for _ in range(N_BOOT):
                s = [lo[i] for i in rng.integers(0, len(lo), len(lo))] + [hi[i] for i in rng.integers(0, len(hi), len(hi))]
                bs.append(fit(s)[:2])
            bs = np.array(bs)
            b0_ci = [float(np.percentile(bs[:, 0], 2.5)), float(np.percentile(bs[:, 0], 97.5))]
            target = (1 - b1) * fresh
            if manip < 0.10:
                cls = "not scored (manipulation check failed)"
            elif not (b0_ci[0] <= 0 <= b0_ci[1]) and b0_ci[0] <= target <= b0_ci[1]:
                cls = "anchoring"
            elif b0_ci[0] <= 0 <= b0_ci[1] and not (b0_ci[0] <= target <= b0_ci[1]):
                cls = "content"
            else:
                cls = "undetermined"
            accept = float(np.mean([x.get("decision") == "accept" for x in rows]))
            own = pX if o == "X" else pY
            rev = [(x["r1"] - x["A"]) / (own - x["A"]) for x in rows if abs(own - x["A"]) > 1e-9]
            res["orders"][o] = {"manipulation": manip, "b0": b0, "b0_ci95": b0_ci, "b1": b1, "b2": b2,
                                "anchoring_target": target, "class": cls, "accept_rate": accept,
                                "mean_revision_toward_own": float(np.mean(rev)) if rev else None,
                                "ceiling_violations": float(np.mean([x["r2"] > x["r1"] for x in rows]))}
            boots[o] = bs[:, 1]
        if all(res["orders"][o]["class"] == "content" for o in ("X", "Y")):
            ratio = boots["X"] / np.where(np.abs(boots["Y"]) > 1e-9, boots["Y"], np.nan)
            ratio = ratio[np.isfinite(ratio)]
            rc = [float(np.percentile(ratio, 2.5)), float(np.percentile(ratio, 97.5))]
            bayes = pY / pX if pX > 0 else float("nan")
            inside = lambda v: rc[0] <= v <= rc[1]
            res["ratio_ci95"], res["bayes_ratio"] = rc, bayes
            res["mechanism"] = ("reciprocity (rank-one quantum)" if inside(1) and not inside(bayes) else
                                "Bayes" if inside(bayes) and not inside(1) else "undetermined")
        per[q] = res
    def verdict(qs):
        orders = [per[q]["orders"][o]["class"] for q in qs for o in ("X", "Y")]
        scored = [c for c in orders if not c.startswith("not scored")]
        items_both = [q for q in qs if all(not per[q]["orders"][o]["class"].startswith("not scored") for o in ("X", "Y"))]
        if len(items_both) < 3:
            return f"untestable (fewer than 3 items pass the manipulation check in both orders: {len(items_both)})"
        n = len(scored)
        if sum(c == "anchoring" for c in scored) >= n / 2:
            return "anchoring explains the order effect"
        if sum(c == "content" for c in scored) >= n / 2:
            both = [q for q in qs if "mechanism" in per[q]]
            if both and sum(per[q]["mechanism"].startswith("reciprocity") for q in both) >= len(both) / 2:
                return "content-driven sequential updating: rank-one quantum (reciprocity)"
            if both and sum(per[q]["mechanism"] == "Bayes" for q in both) >= len(both) / 2:
                return "content-driven sequential updating: classical Bayes"
            return "content-driven sequential updating, mechanism undetermined"
        return "undetermined"
    allq = [it["id"] for it in items]
    v_all, v_fal = verdict(allq), verdict([q for q in allq if q in fallacy])
    cost = sum(v["cost"] for v in _cache.values())
    n_calls = sum(len(v["request_ids"]) for v in _cache.values())
    OUT_JSON.write_text(json.dumps({"items": per, "verdict_all": v_all, "verdict_fallacy_items": v_fal,
                                    "n_calls": n_calls, "cost_usd": cost}, indent=1))
    g = lambda c: f"[{c[0]:+.3f}, {c[1]:+.3f}]"
    lines = ["# Experiment 4, run 3: a manipulated first rating", "",
             "Frozen pre-registration: `experiments/exp4-run-3.md` with the D33 amendment (one scale direction: 0 = certainly "
             f"false, 100 = certainly true). Base model `{MODEL}`, thinking disabled, default temperature. {len(items)} items, "
             f"{n_calls} calls, **${cost:.2f}**.", "",
             "Fit per item and order: r₂ = β₀ + β₁·r₁ + β₂·A over the 80 anchored conversations (0–1 scale). "
             "Anchoring predicts β₀ ≈ (1 − β₁)·fresh; content-driven updating (quantum or Bayes) predicts β₀ ≈ 0.", "",
             "| item | order | manipulation (r₁ hi − lo) | accept rate | β₀ [95% CI] | (1 − β₁)·fresh | β₁ | β₂ | r₂ > r₁ | class |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for q, r in per.items():
        for o in ("X", "Y"):
            d = r["orders"][o]
            b2 = "unid." if d["b2"] is None else f"{d['b2']:+.2f}"
            lines.append(f"| {q}{' *' if q in fallacy else ''} | {o} first | {d['manipulation']:+.2f} | {d['accept_rate']:.0%} | "
                         f"{d['b0']:+.3f} {g(d['b0_ci95'])} | {d['anchoring_target']:+.3f} | {d['b1']:+.2f} | {b2} | "
                         f"{d['ceiling_violations']:.0%} | {d['class']} |")
    mech = [(q, r) for q, r in per.items() if "mechanism" in r]
    lines += ["", "\\* = one of run 2's 7 fallacy items.", "", "## Slope ratio, on items content-driven in both orders", ""]
    if mech:
        lines += ["| item | β₁(X first)/β₁(Y first) [95% CI] | Bayes prediction P(Y)/P(X) | rank-one quantum prediction | mechanism |",
                  "|---|---|---|---|---|"]
        lines += [f"| {q} | [{r['ratio_ci95'][0]:.2f}, {r['ratio_ci95'][1]:.2f}] | {r['bayes_ratio']:.2f} | 1 | {r['mechanism']} |" for q, r in mech]
    else:
        lines.append("No item was content-driven in both orders.")
    lines += ["", f"Replication of run 2's free-rating order effect o (X→XY minus Y→XY): "
              + ", ".join(f"{q} {r['o_free']:+.2f}" for q, r in per.items() if q in fallacy) + ".", "",
              f"## Verdict, all 16 items: **{v_all}**", "", f"Verdict, run 2's 7 fallacy items: **{v_fal}**"]
    OUT_MD.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()

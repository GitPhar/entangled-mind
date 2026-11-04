"""Experiment 5: sequential, context-dependent judgment - data collection, as frozen in
experiments/exp5-sequential-judgment.md (DEVIATIONS.md, D22-D23).

    python experiments/exp5_run.py split    # write experiments/split-exp5.json (no API calls)
    python experiments/exp5_run.py pilot    # 5 pilot items, full design; gates G1 and G2
    python experiments/exp5_run.py full     # the 40 items (only if G1 passed)

Base model claude-haiku-5-5, thinking disabled, default temperature (1.0; the API rejects an
explicit one). Every answer is structured output. Conversations are cached in
results/exp5-conversations.json; the $4 cap is enforced over all experiment-5 calls; on any
refusal the run stops and records the request ID, with nothing reworded or retried.

Implementation choices fixed before any data (D23): S1..S4 are the 4 chain claims in claim-index
order; O1..O4 are the cyclic Latin square (1234, 2341, 3412, 4123); the first user turn is the
opening context followed by the first question; K1's choice turn returns {"answer": "yes"|"no"}
and K0's filler turn returns {"reply": "continue"}, so both are matched structured turns."""

import json
import math
import random
import sys
import threading
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from dotenv import load_dotenv

from entangled_mind import config, encoder, llm, v2

load_dotenv(config.ROOT / ".env")
DOC = config.EXPERIMENTS / "exp5-sequential-judgment.md"
SPLIT = config.EXPERIMENTS / "split-exp5.json"
POOL = config.RESULTS / "pool-run-3.json"
CONV = config.RESULTS / "exp5-conversations.json"
PILOT_MD, PILOT_JSON = config.RESULTS / "exp5-pilot.md", config.RESULTS / "exp5-pilot.json"
MODEL, BUDGET_USD = "claude-haiku-5-5", 4.0
PILOT = ["h018", "h088", "h039", "h001", "h170"]
R_CHAIN, R_QQ = 10, 40
ANCHORS = {"a": "0 = certainly false, 100 = certainly true", "b": "0 = certainly true, 100 = certainly false"}
RATING = {"type": "object", "properties": {"rating": {"type": "integer"}}, "required": ["rating"], "additionalProperties": False}
CHOICE = {"type": "object", "properties": {"answer": {"type": "string", "enum": ["yes", "no"]}}, "required": ["answer"],
          "additionalProperties": False}
FILLER = {"type": "object", "properties": {"reply": {"type": "string", "enum": ["continue"]}}, "required": ["reply"],
          "additionalProperties": False}
LATIN = [[0, 1, 2, 3], [1, 2, 3, 0], [2, 3, 0, 1], [3, 0, 1, 2]]


# --- items, claims, phases --------------------------------------------------

def candidates() -> list[str]:
    import re
    return re.findall(r"^\| \d+ \| (h\d{3}) \|", DOC.read_text(), re.M)


def chain_claims(rec) -> list[int]:
    """K = 4 competing claims, two leaning yes and two leaning no, by confidence x |lean| (ties: lower index)."""
    cs, L = rec["contentions"], [c["lean"] for c in rec["contentions"]]
    comp = set()
    for p in rec["pairs"]:
        i, j = p["i"], p["j"]
        if p["relation"] == "contradicts" and abs(L[i]) > 0.1 and abs(L[j]) > 0.1 and (L[i] > 0) != (L[j] > 0):
            comp |= {i, j}
    score = lambda k: (-cs[k]["confidence"] * abs(L[k]), k)
    yes = sorted([k for k in comp if L[k] > 0], key=score)
    no = sorted([k for k in comp if L[k] < 0], key=score)
    pick = yes[:2] + no[:2]
    rest = sorted([k for k in comp if k not in pick], key=score)
    pick += rest[: 4 - len(pick)]
    if len(pick) < 4:   # D24: fewer than 4 competing claims (pilot item h001 only) - fill from leaning non-competing claims
        extra = sorted([k for k in range(len(cs)) if k not in pick and abs(L[k]) > 0.1], key=score)
        pick += extra[: 4 - len(pick)]
    return sorted(pick)


def exp5_phases(web: encoder.Web, no_lean: float = 0.1) -> np.ndarray:
    """Frozen order (§5.1): set hedges aside; anchored solve on the leaning claims and their mutual
    edges; hedges at pi/2 (their lean is set to 0 by the caller)."""
    mask = np.abs(web.lean) <= no_lean
    keep = np.where(~mask)[0]
    phi = np.full(web.n, math.pi / 2)
    if len(keep):
        pos = {k: a for a, k in enumerate(keep)}
        sub = encoder.Web(web.confidence[keep], web.lean[keep],
                          tuple((pos[i], pos[j], J) for i, j, J in web.edges if i in pos and j in pos))
        phi[keep] = encoder.solve_phases_anchored(sub)
    return phi


def check_exp5_phases(recs) -> dict:
    """§5.1's required test against both parents."""
    worst_a, worst_h, n_a, n_h = 0.0, 0.0, 0, 0
    for r in recs:
        if "contentions" not in r:
            continue
        web = encoder.build_web(r["contentions"], r["pairs"])
        mask = np.abs(web.lean) <= 0.1
        if not mask.any():   # no hedges: must equal solve_phases_anchored
            d = np.angle(np.exp(1j * (exp5_phases(web) - encoder.solve_phases_anchored(web))))
            worst_a, n_a = max(worst_a, float(np.abs(d).max())), n_a + 1
        # with a plain solve in place of the anchored one, must equal v2.hedge_phases
        orig = encoder.solve_phases_anchored
        encoder.solve_phases_anchored = lambda w: v2.solve_phases_fast(w)
        try:
            d = np.angle(np.exp(1j * (exp5_phases(web) - v2.hedge_phases(web, mask))))
        finally:
            encoder.solve_phases_anchored = orig
        worst_h, n_h = max(worst_h, float(np.abs(d).max())), n_h + 1
    return {"vs_anchored_no_hedges": {"items": n_a, "max_abs_diff_rad": worst_a},
            "vs_hedge_phases_plain_solve": {"items": n_h, "max_abs_diff_rad": worst_h}}


def qq_pairs(rec, claims) -> list[int]:
    """The chain claims with the largest and smallest |sin dphi_k| (dphi = phi minus its snapped value)."""
    web = encoder.build_web(rec["contentions"], rec["pairs"])
    web = encoder.Web(web.confidence, np.where(np.abs(web.lean) <= 0.1, 0.0, web.lean), web.edges)
    phi = exp5_phases(web)
    snap = lambda k: 0.0 if web.lean[k] > 0 else math.pi
    nc = {k: abs(math.sin(phi[k] - snap(k))) for k in claims}
    order = sorted(claims, key=lambda k: (-nc[k], k))
    return [order[0], order[-1]], nc


# --- conversation design ------------------------------------------------------

def opening(rec, anchor) -> str:
    return (f'We are going to think about one question in steps. The question is: "{rec["question"]}". '
            f"I will ask you to rate several statements, one at a time, and the question itself. "
            f"Give each rating as an integer from 0 to 100, where {ANCHORS[anchor]}.")


def turns_for(chain: str, S: list[int]) -> list[tuple]:
    """List of (kind, claim index or None). kind in S (sub-question), M, C (choice), F (filler)."""
    if chain.startswith("O"):
        return [("S", S[i]) for i in LATIN[int(chain[1]) - 1]] + [("M", None)]
    if chain.startswith("X"):
        k = int(chain[1]) - 1
        return [("S", S[i]) for i in LATIN[0] if i != k] + [("M", None)]
    if chain == "B0":
        return [("M", None)]
    if chain == "MF":
        return [("M", None)] + [("S", S[i]) for i in LATIN[0]] + [("M", None)]
    mid = ("C", None) if chain == "K1" else ("F", None)
    return [("S", S[0]), ("S", S[1]), mid, ("S", S[2]), ("S", S[3]), ("M", None)]


CHAINS = ["O1", "O2", "O3", "O4", "X1", "X2", "X3", "X4", "B0", "MF", "K1", "K0"]


def question(rec, kind, k):
    if kind == "S":
        return f"How likely is it that this statement is true? '{rec['contentions'][k]['text']}'"
    if kind == "M":
        return "How likely is it that the answer to the question is yes?"
    if kind == "C":
        return "Answer yes or no: is the answer yes?"
    return "Reply with the single word: continue"


def jobs_for(qid, rec) -> list[tuple]:
    S = chain_claims(rec)
    out = []
    for chain in CHAINS:
        for rep in range(R_CHAIN):
            out.append((f"{qid}|{chain}|{rep}", qid, turns_for(chain, S), "ab"[rep % 2]))
    pairs, _ = qq_pairs(rec, S)
    for k in pairs:
        for order in ("SM", "MS"):
            t = [("S", k), ("M", None)] if order == "SM" else [("M", None), ("S", k)]
            for rep in range(R_QQ):
                out.append((f"{qid}|QQ{k}{order}|{rep}", qid, t, "ab"[rep % 2]))
    return out


# --- calls --------------------------------------------------------------------

_cache, _lock, _stop, _refusal = {}, threading.Lock(), threading.Event(), {}


def converse(job, recs):
    key, qid, turns, anchor = job
    if key in _cache or _stop.is_set():
        return
    with _lock:
        if sum(v["cost"] for v in _cache.values()) >= BUDGET_USD:
            _stop.set()
            return
    rec = recs[qid]
    msgs, out, cost, rids = [], [], 0.0, []
    try:
        for t, (kind, k) in enumerate(turns):
            text = question(rec, kind, k)
            if t == 0:
                text = opening(rec, anchor) + "\n\n" + text
            msgs.append({"role": "user", "content": text})
            schema = {"S": RATING, "M": RATING, "C": CHOICE, "F": FILLER}[kind]
            resp = llm.client().messages.create(model=MODEL, max_tokens=200, thinking={"type": "disabled"},
                                                output_config={"format": {"type": "json_schema", "schema": schema}},
                                                messages=msgs)
            llm._check_stop(resp, "exp5")
            reply = next(b.text for b in resp.content if b.type == "text")
            msgs.append({"role": "assistant", "content": reply})
            d = json.loads(reply)
            if kind in ("S", "M"):
                r = min(100, max(0, int(d["rating"])))
                out.append({"kind": kind, "claim": k, "raw": r, "rating": r if anchor == "a" else 100 - r})
            else:
                out.append({"kind": kind, "answer": d.get("answer") or d.get("reply")})
            cost += llm._usage(resp).cost
            rids.append(getattr(resp, "_request_id", None))
    except llm.RefusalError as e:
        _refusal.setdefault("e", (key, e))
        _stop.set()
        return
    except (json.JSONDecodeError, KeyError, ValueError) as e:   # schema failure: recorded, row dropped in analysis
        out.append({"kind": "error", "error": str(e)})
    with _lock:
        _cache[key] = {"anchor": anchor, "turns": out, "cost": cost, "request_ids": rids}
        if len(_cache) % 200 == 0:
            CONV.write_text(json.dumps(_cache))
            print(f"{len(_cache)} conversations, ${sum(v['cost'] for v in _cache.values()):.2f}", flush=True)


def run(qids, recs):
    global _cache
    _cache = json.loads(CONV.read_text()) if CONV.exists() else {}
    jobs = [j for q in qids for j in jobs_for(q, recs[q])]
    with ThreadPoolExecutor(max_workers=6) as ex:
        list(ex.map(lambda j: converse(j, recs), jobs))
    CONV.write_text(json.dumps(_cache))
    if _refusal:
        key, e = _refusal["e"]
        (config.RESULTS / "refusal.md").write_text(
            f"# Pipeline stopped on a refusal\n\nExperiment 5, conversation `{key}`\n\nRefused call: **{e.call}**\n\n"
            f"Request ID: `{e.request_id}`\n\nExact stop details:\n\n```\n{e.stop_details}\n```\n\nNothing was reworded or retried.\n")
        sys.exit(f"STOPPED: {e}")
    if _stop.is_set():
        sys.exit("budget stop")
    return jobs


# --- gates --------------------------------------------------------------------

def ratings(key):
    return [t for t in _cache[key]["turns"] if t["kind"] in ("S", "M")]


def gates(qids, recs) -> dict:
    out = {"items": {}, "pairs": {}}
    g1_items = 0
    for q in qids:
        means = {}
        for chain in ["O1", "O2", "O3", "O4", "X1", "X2", "X3", "X4", "B0"]:
            finals = [ratings(f"{q}|{chain}|{r}")[-1]["rating"] for r in range(R_CHAIN)
                      if ratings(f"{q}|{chain}|{r}") and ratings(f"{q}|{chain}|{r}")[-1]["kind"] == "M"]
            means[chain] = float(np.mean(finals)) if finals else float("nan")
        span = float(np.nanmax(list(means.values())) - np.nanmin(list(means.values())))
        cells = {}   # (chain, position, anchor): SD within one anchor direction, so scale reversal cannot inflate it
        for chain in CHAINS:
            for r in range(R_CHAIN):
                key = f"{q}|{chain}|{r}"
                for pos, t in enumerate(ratings(key)):
                    if t["kind"] == "S":
                        cells.setdefault((chain, pos, _cache[key]["anchor"]), []).append(t["rating"])
        sds = [float(np.std(v, ddof=1)) for v in cells.values() if len(v) > 1]
        share = float(np.mean([s >= 2 for s in sds])) if sds else 0.0
        ok = span >= 5 or share >= 0.25
        g1_items += ok
        out["items"][q] = {"M_mean_by_chain": means, "M_span": span, "S_cells": len(sds),
                           "S_share_sd_ge_2": share, "G1_item": ok}
        S = chain_claims(recs[q])
        pairs, nc = qq_pairs(recs[q], S)
        for k in pairs:
            best = 0.0
            for order in ("SM", "MS"):
                rows = [ratings(f"{q}|QQ{k}{order}|{r}") for r in range(R_QQ)]
                rows = [x for x in rows if len(x) == 2]
                for which in range(2):
                    yes = np.array([x[which]["rating"] >= 50 for x in rows])
                    if len(yes):
                        best = max(best, float(min(yes.mean(), 1 - yes.mean())))
            out["pairs"][f"{q}:S{k}"] = {"max_minority_share": best, "noncommutativity": nc[k], "G2_pair": best >= 0.10}
    out["G1"] = g1_items >= 3
    out["G1_items_passing"] = g1_items
    out["G2"] = sum(p["G2_pair"] for p in out["pairs"].values()) >= 3
    out["G2_pairs_passing"] = sum(p["G2_pair"] for p in out["pairs"].values())
    return out


# --- commands -----------------------------------------------------------------

def cmd_split():
    if SPLIT.exists():
        sys.exit(f"{SPLIT} exists; the split is never re-made.")
    recs = {r["id"]: r for r in json.loads(POOL.read_text())["records"]}
    cand = candidates()
    assert len(cand) == 40
    rng = random.Random(2027)
    wrong = [q for q in cand if not recs[q]["correct"]]
    right = [q for q in cand if recs[q]["correct"]]
    held = sorted(rng.sample(wrong, 4) + rng.sample(right, 4))
    rest = [q for q in cand if q not in held]
    split = {"train": [], "validation": [], "test": []}
    leftovers = []
    for chain in CHAINS:                      # stratified by chain type: 19 / 6 / 6 each, then 12 leftovers
        chains = [f"{q}|{chain}" for q in rest]
        rng.shuffle(chains)
        split["train"] += chains[:19]
        split["validation"] += chains[19:25]
        split["test"] += chains[25:31]
        leftovers.append(chains[31])
    rng.shuffle(leftovers)                    # largest remainder: 2 to train, 5 to validation, 5 to test
    split["train"] += leftovers[:2]
    split["validation"] += leftovers[2:7]
    split["test"] += leftovers[7:]
    phases_check = check_exp5_phases(json.loads(POOL.read_text())["records"])
    out = {"seed": 2027, "candidates": cand, "pilot": PILOT, "item_heldout": held,
           **{k: sorted(v) for k, v in split.items()},
           "counts": {k: len(v) for k, v in split.items()},
           "chain_claims": {q: chain_claims(recs[q]) for q in cand + PILOT},
           "qq_pairs": {q: qq_pairs(recs[q], chain_claims(recs[q]))[0] for q in cand + PILOT},
           "phase_solver_checks": phases_check}
    SPLIT.write_text(json.dumps(out, indent=1))
    print(out["counts"], "held-out", held, phases_check)


def cmd_pilot():
    recs = {r["id"]: r for r in json.loads(POOL.read_text())["records"]}
    jobs = run(PILOT, recs)
    g = gates(PILOT, recs)
    cost = sum(_cache[j[0]]["cost"] for j in jobs if j[0] in _cache)   # the pilot's own conversations only
    PILOT_JSON.write_text(json.dumps({"gates": g, "n_conversations": len(jobs), "cost_usd": cost}, indent=1))
    lines = ["# Experiment 5: pilot (gates G1 and G2)", "",
             f"Frozen pre-registration: `experiments/exp5-sequential-judgment.md` (§7.1, D22-D23). Pilot items: "
             f"{', '.join(PILOT)}. Full design per item: 12 chain types × {R_CHAIN} conversations plus the QQ block "
             f"(2 pairs × 2 orders × {R_QQ}). {len(jobs)} conversations, **${cost:.2f}** so far for experiment 5. "
             "Pilot data are reported but never used in any test.", "",
             "## G1 — dispersion (go / no-go)", "",
             "| item | main-rating means across O1–O4, X1–X4, B0 | span (points) | sub-question cells with between-repeat SD ≥ 2 | item passes |",
             "|---|---|---|---|---|"]
    for q, v in g["items"].items():
        m = ", ".join(f"{c} {x:.0f}" for c, x in v["M_mean_by_chain"].items())
        lines.append(f"| {q} | {m} | {v['M_span']:.1f} | {v['S_share_sd_ge_2']:.0%} of {v['S_cells']} | {'yes' if v['G1_item'] else 'no'} |")
    lines += ["", f"**G1: {'PASS' if g['G1'] else 'FAIL'}** ({g['G1_items_passing']} of 5 items; the rule needs at least 3).", "",
              "## G2 — QQ-block dispersion", "",
              "| pair | predicted non-commutativity |sin Δφ| | largest binarised minority share (either question, either order) | pair passes |",
              "|---|---|---|---|"]
    for p, v in g["pairs"].items():
        lines.append(f"| {p} | {v['noncommutativity']:.3f} | {v['max_minority_share']:.0%} | {'yes' if v['G2_pair'] else 'no'} |")
    lines += ["", f"**G2: {'PASS' if g['G2'] else 'FAIL — the QQ check will be reported as saturated'}** "
              f"({g['G2_pairs_passing']} of 10 pairs; the rule needs at least 3)."]
    PILOT_MD.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


def cmd_full():
    pilot = json.loads(PILOT_JSON.read_text())
    if not pilot["gates"]["G1"]:
        sys.exit("G1 failed: experiment 5 is untestable; the full run is not made (§7.1).")
    if not SPLIT.exists():
        sys.exit("write and commit experiments/split-exp5.json first")
    recs = {r["id"]: r for r in json.loads(POOL.read_text())["records"]}
    run(candidates(), recs)
    print("full run complete", len(_cache), f"${sum(v['cost'] for v in _cache.values()):.2f}")


if __name__ == "__main__":
    {"split": cmd_split, "pilot": cmd_pilot, "full": cmd_full}[sys.argv[1]]()

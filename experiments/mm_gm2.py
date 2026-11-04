"""Multi-model replication of direction 2 (shown / redacted / planted transcripts), as pre-registered in
experiments/mm-gm2-self-conditioning.md (DM4).

    python experiments/mm_gm2.py run sonnet|opus     # turn-by-turn batch waves, capped, stop on refusal
    python experiments/mm_gm2.py analyse             # each model with data, plus the Haiku reference at R = 4

Prompts, chains, conditions, transcript editing and the analysis (gm2_self_conditioning.compute) are D37's, unchanged.
Conversations cached in results/mm-gm2-<model>-conversations.json; planted values (fixed by D37's rule from each model's
own first-turn ratings, after wave 1) in results/mm-gm2-<model>-planted.json. Writes results/mm-gm2-self-conditioning.{json,md}."""

import json
import sys

import numpy as np

import exp5_run as er
import gm2_self_conditioning as g2
import mm_common as mc
from entangled_mind import config

R = 4
CAPS = {"sonnet": 2.4, "opus": 6.0}
TOTAL_BUDGET, RESERVE = 20.0, 0.10      # DM4a: Opus's cap = $20 - all other recorded spend on the branch - $0.10, fixed at its start


def branch_spend_excluding_gm2_opus():
    tot = 0.0
    for f in [p for p in config.RESULTS.glob("mm-*-calls.json") if p.name != "mm-pilot-calls.json"]:
        tot += sum(v.get("cost", 0) for v in json.loads(f.read_text()).values())
    tot += sum(c["cost"] for c in json.loads(paths("sonnet")[0].read_text()).values()) if paths("sonnet")[0].exists() else 0
    pilot = json.loads((config.RESULTS / "mm-pilot-calls.json").read_text())
    tot += sum(x.get("cost", 0) + x.get("opus_base_cost", 0) for x in pilot)
    tot += 0.000737                       # the 2-request batch pilot (DM1), at the batch rate
    return tot
EST0 = {"sonnet": 0.0004, "opus": 0.0009}
GROWTH = 1.12                     # per-turn growth in cost used for the projection after wave 1
MODELS = {"sonnet": mc.S, "opus": mc.O}
OUT_JSON, OUT_MD = config.RESULTS / "mm-gm2-self-conditioning.json", config.RESULTS / "mm-gm2-self-conditioning.md"


def paths(m):
    return config.RESULTS / f"mm-gm2-{m}-conversations.json", config.RESULTS / f"mm-gm2-{m}-planted.json"


def design():
    items = json.loads(g2.PLANTED.read_text())["items"]
    return {q: v["chain_claims"] for q, v in items.items()}


def planted_from_wave1(conv, claims):
    """D37's rule, high = min(98, round(m) + 15), low = max(2, round(m) - 15), with m the mean of the model's own
    first-turn ratings: S_k from the first turn of every O-chain that opens with S_k, M from the first turn of every MF chain."""
    out = {}
    for q, S in claims.items():
        out[q] = {"chain_claims": S, "S": {}, "M": None}
        for i, k in enumerate(S):
            xs = [c["turns"][0]["rating"] for key, c in conv.items() if key.startswith(f"{q}|O{i + 1}|") and c["turns"]]
            m = float(np.mean(xs))
            out[q]["S"][str(k)] = {"m": m, "n": len(xs), "high": min(98, round(m) + 15), "low": max(2, round(m) - 15)}
        xs = [c["turns"][0]["rating"] for key, c in conv.items() if key.startswith(f"{q}|MF|") and c["turns"]]
        m = float(np.mean(xs))
        out[q]["M"] = {"m": m, "n": len(xs), "high": min(98, round(m) + 15), "low": max(2, round(m) - 15)}
    return out


def hist(cond, q, turn, planted):
    """D37's transcript editing: shown keeps the model's reply; redacted and planted replace it in the next turn's history."""
    if cond == "shown":
        return turn["raw"]
    if cond == "redacted":
        return "[rating recorded]"
    v = planted[q]["M"] if turn["kind"] == "M" else planted[q]["S"][str(turn["claim"])]
    return json.dumps({"rating": v[cond]})


def run(m):
    model = MODELS[m]
    if m == "opus":
        cap_file = config.RESULTS / "mm-gm2-opus-cap.json"
        if not cap_file.exists():
            other = branch_spend_excluding_gm2_opus()
            cap_file.write_text(json.dumps({"other_recorded_spend": other, "cap": round(TOTAL_BUDGET - other - RESERVE, 4)}, indent=1))
        CAPS["opus"] = json.loads(cap_file.read_text())["cap"]
        print(f"opus: DM4a cap ${CAPS['opus']:.2f}", flush=True)
    cpath, ppath = paths(m)
    claims = design()
    recs = {r["id"]: r for r in json.loads(er.POOL.read_text())["records"]}
    conv = json.loads(cpath.read_text()) if cpath.exists() else {}
    keys = [f"{q}|{ch}|{cond}|{r}" for q in claims for ch in g2.CHAINS for cond in g2.CONDS for r in range(R)]
    for k in keys:
        conv.setdefault(k, {"turns": [], "cost": 0.0, "msg_ids": [], "batches": []})
    planted = json.loads(ppath.read_text()) if ppath.exists() else None
    save = lambda: cpath.write_text(json.dumps(conv))
    spent = lambda: sum(c["cost"] for c in conv.values())
    turns_of = {k: er.turns_for(k.split("|")[1], claims[k.split("|")[0]]) for k in keys}
    est = EST0[m]
    for t in range(6):
        live = [k for k in keys if len(turns_of[k]) > t and len(conv[k]["turns"]) == t and not conv[k].get("abandoned")]
        if not live:
            continue
        reqs = {}
        for k in live:
            q, ch, cond, r = k.split("|")
            msgs = []
            for u, (kind, kk) in enumerate(turns_of[k][:t + 1]):
                text = er.question(recs[q], kind, kk)
                if u == 0:
                    text = er.opening(recs[q], "a") + "\n\n" + text
                msgs.append({"role": "user", "content": text})
                if u < t:
                    msgs.append({"role": "assistant", "content": hist(cond, q, conv[k]["turns"][u], planted)})
            reqs[k] = mc.params(model, msgs, er.RATING, max_tokens=1000)

        def store(k, rec):
            c = conv[k]
            c["cost"] += rec["cost"]
            c["msg_ids"].append(rec.get("msg_id"))
            c["batches"].append(rec.get("batch"))
            if "rating" not in rec:                     # refusal or max_tokens: the conversation ends here, incomplete
                c["abandoned"] = rec.get("error", "refused")
                return
            kind, kk = turns_of[k][len(c["turns"])]
            c["turns"].append({"kind": kind, "claim": kk, "rating": rec["rating"], "raw": rec["raw"]})
        br = mc.BatchRunner(f"gm2-{m}-wave{t + 1}", CAPS[m], spent, chunk=800)
        est = br.run(reqs, lambda k, msg: {"rating": min(100, max(0, int(json.loads(mc.text_of(msg))["rating"]))),
                                           "raw": mc.text_of(msg)}, store, save, est * (GROWTH if t else 1.0))
        if t == 0 and planted is None:
            planted = planted_from_wave1(conv, claims)
            ppath.write_text(json.dumps({"rule": "D37's rule on the model's own first-turn ratings (DM4)", "items": planted}, indent=1))
        # DM4 fallback, checked after every wave: while the projected total exceeds the cap, the highest remaining repeat is
        # abandoned (R = 4 -> 3 -> 2); the projection prices each later wave at this wave's mean cost x 1.12 per turn
        while True:
            kept = sorted({int(k.split("|")[3]) for k in keys if not conv[k].get("abandoned")})
            n_by_wave = [sum(1 for k in keys if len(turns_of[k]) > w and not conv[k].get("abandoned")) for w in range(6)]
            proj = spent() + sum(n_by_wave[w] * est * GROWTH ** (w - t) for w in range(t + 1, 6))
            print(f"{m}: after wave {t + 1}, projected total ${proj:.2f} against the ${CAPS[m]} cap (R = {len(kept)})", flush=True)
            if proj <= CAPS[m] or len(kept) <= 2:
                break
            for k in keys:
                if k.endswith(f"|{kept[-1]}") and not conv[k].get("abandoned"):
                    conv[k]["abandoned"] = f"DM4 fallback after wave {t + 1}: projected cost over cap"
        save()
        print(f"{m}: wave {t + 1} done, ${spent():.3f}", flush=True)


def complete(conv):
    claims = design()
    return {k: c for k, c in conv.items() if not c.get("abandoned")
            and len(c["turns"]) == len(er.turns_for(k.split("|")[1], claims[k.split("|")[0]]))}


def analyse_one(conv, planted, r_used):
    g2.R = r_used
    return g2.compute(conv, planted, list(planted))


def analyse():
    out = {}
    arch = json.loads(g2.CACHE.read_text())
    hk = {k: v for k, v in arch.items() if int(k.split("|")[3]) < R}
    out["haiku"] = analyse_one(hk, json.loads(g2.PLANTED.read_text())["items"], R)
    out["haiku"]["note"] = "D37's archived conversations, repeats 0-3 only (R = 4), with D37's planted values"
    for m in MODELS:
        cpath, ppath = paths(m)
        if not cpath.exists() or not ppath.exists():
            continue
        conv = json.loads(cpath.read_text())
        done = complete(conv)
        planted = json.loads(ppath.read_text())["items"]
        r_used = R - len({k.split("|")[3] for k, c in conv.items() if str(c.get("abandoned", "")).startswith("DM4 fallback")})
        res = analyse_one(done, planted, r_used)
        res.update(cost_usd=sum(c["cost"] for c in conv.values()), n_complete=len(done), n_designed=len(conv), R_repeats=r_used,
                   refusals=sum(1 for c in conv.values() if c.get("abandoned") == "refused"),
                   max_tokens=sum(1 for c in conv.values() if c.get("abandoned") == "max_tokens"),
                   planted_M={q: v["M"] for q, v in planted.items()})
        out[m] = res
    OUT_JSON.write_text(json.dumps(out, indent=1))
    write_md(out)


def write_md(o):
    f = lambda d, p=2: f"{d[0]:.{p}f} [{d[1]:.{p}f}, {d[2]:.{p}f}]"
    ms = [m for m in ("haiku", "sonnet", "opus") if m in o]
    L = ["# Multi-model replication of direction 2: shown, redacted and planted transcripts", "",
         "Pre-registered in `experiments/mm-gm2-self-conditioning.md` (DM4), committed before any call. D37's 10 items, chains O1–O4 "
         "and MF, four conditions, one scale direction, **R = 4** conversations per cell. Haiku's row is D37's archive restricted to "
         "repeats 0–3. Costs at the batch rate.", "",
         "## In plain English", "", "(Hand-written after the run; excluded from reproduce.py's comparison.)", "",
         "## Primary: the order effect with and without the record", "",
         "| model | complete conversations | cost | gate p | OE shown | OE redacted | **R = OE_redacted / OE_shown** | reading |",
         "|---|---|---|---|---|---|---|---|"]
    for m in ms:
        r = o[m]
        n = f"{r['n_complete']} / {r['n_designed']}" if "n_complete" in r else str(r["n_conversations"])
        cost = f"${r['cost_usd']:.2f}" if m != "haiku" else "archived"
        L.append(f"| {m} | {n} | {cost} | {r['gate_p']:.4f} | {f(r['OE_ci']['shown'], 1)} | {f(r['OE_ci']['redacted'], 1)} | "
                 f"**{f(r['R'])}** | **{r['reading']}** |")
    L += ["", "## Planted values and repeat agreement", "",
          "| model | b_MF | next-rating pull (points) | final-M shift, high − low | OE planted high / low | MF agreement shown / redacted / high / low |",
          "|---|---|---|---|---|---|"]
    for m in ms:
        r = o[m]
        a = r["MF_agreement"]
        L.append(f"| {m} | {f(r['b_MF'])} | {f(r['next_rating_pull'], 1)} | {f(r['final_M_shift_O'], 1)} | "
                 f"{r['OE']['high']:.1f} / {r['OE']['low']:.1f} | {a['shown']:.0%} / {a['redacted']:.0%} / {a['high']:.0%} / {a['low']:.0%} |")
    for m in ms:
        L += ["", f"### Per item, {m}", "", "| item | OE shown | OE redacted | final M by order, shown | redacted | MF M₂ shown / redacted / high / low |",
              "|---|---|---|---|---|---|"]
        for q, v in o[m]["per_item"].items():
            mm = v["M_means"]
            L.append(f"| {q} | {v['OE_shown']:.1f} | {v['OE_redacted']:.1f} | {', '.join(f'{x:.0f}' for x in mm['shown'])} | "
                     f"{', '.join(f'{x:.0f}' for x in mm['redacted'])} | {' / '.join(f'{v['MF_M2'][c]:.0f}' for c in g2.CONDS)} |")
    OUT_MD.write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    if sys.argv[1] == "run":
        mc.main_guard(lambda: run(sys.argv[2]))
    else:
        analyse()

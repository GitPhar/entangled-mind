"""Gold map direction 5: does an internal truth probe move with question order? (D48)

Frozen in experiments/probe-dissociation.md before any call on the study items. Local model, $0 API.

    .venv/bin/python experiments/probe_dissociation.py gate llama3-8b   # step 1
    .venv/bin/python experiments/probe_dissociation.py train MODEL      # step 2
    .venv/bin/python experiments/probe_dissociation.py run MODEL        # step 3
    .venv/bin/python experiments/probe_dissociation.py analyse MODEL    # verdict + results/probe-dissociation.json
    .venv/bin/python experiments/probe_dissociation.py simulate         # analysis check on simulated worlds

The venv needs mlx, mlx-lm, numpy, scipy and matplotlib (see the pre-registration, section 2).
"""

import csv
import json
import sys
import time
import urllib.request
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))
RESULTS, POOL = ROOT / "results", ROOT / "results" / "pool-run-3.json"

ITEMS = ["h190", "h101", "h112", "h191", "h261", "h058", "h221", "h279", "h127", "h238"]
R = 10
LATIN = [[0, 1, 2, 3], [1, 2, 3, 0], [2, 3, 0, 1], [3, 0, 1, 2]]
ORDERS = ["O1", "O2", "O3", "O4"]
ANCHOR = "0 = certainly false, 100 = certainly true"
TOLD = {"T+": "A reliable reference source states that the answer to the question is yes.",
        "T-": "A reliable reference source states that the answer to the question is no."}
# The main question's yes-answer as a self-contained declarative statement (written before any data).
STATEMENT = {
    "h190": 'The Society of Illustrators sold the rights to their Illustrator Show skits in 1925 to "Vice & Virtue".',
    "h101": "Louise M. Antony received her bachelor's degree in philosophy from Duke University.",
    "h112": "Anna Moriah Wilson graduated from Emory & Henry College in 2014.",
    "h191": "The 1991 Ig Nobel Prize for Peace was won by Patricia Mary Edmondson.",
    "h261": "The last total lunar eclipse for three years occurred on November 8, 2022.",
    "h058": "The frequency of a 2-cm sound wave in sea water, where sound travels at 1.53 x 10^5 cm/sec, is 76 kHz.",
    "h221": "The scholarship that Mary Fairchild MacMonnies Low won from the St. Louis School of Fine Arts was for three years.",
    "h279": 'In the 2012 paper "Multiplication of EEG Samples through Replicating, Biasing, and Overlapping" by Adham '
            "Atyabi et al., the EEG dataset was bandpass filtered between 1 and 50 Hz.",
    "h127": 'The original name of the show that conductor David Randolph hosted on WNYC was "Music for the Connoisseur".',
    "h238": "When a piston of cross-sectional area 50 cm^2 is pushed out 15 cm against an external pressure of 1.0 atm, "
            "the work done by the system is -75 J.",
}
GOT_SHA = "5d1c630c44f7e50bda7ad86d601ccadf9abc5ddb"
GOT_URL = f"https://raw.githubusercontent.com/saprmarks/geometry-of-truth/{GOT_SHA}/datasets/{{}}.csv"
GOT_DIR = Path.home() / ".cache" / "entangled-mind" / "geometry-of-truth" / GOT_SHA
TRAIN_SETS = ["cities", "neg_cities", "sp_en_trans", "neg_sp_en_trans", "larger_than", "smaller_than"]
SELECT_SETS = {"companies_true_false": 400, "counterfact_true_false": 600}
REPORT_SETS = {"common_claim_true_false": 600}
N_TRAIN, SEED, N_BOOT, N_PERM = 300, 48, 2000, 10000


def out(model, what):
    return RESULTS / f"probe-dissociation-{model}-{what}.json"


# --- items and conversations ---------------------------------------------------

def items():
    """Experiment 5's frozen chain claims (exp5_run.chain_claims, as written to split-exp5.json)."""
    cc = json.loads((ROOT / "experiments" / "split-exp5.json").read_text())["chain_claims"]
    recs = {r["id"]: r for r in json.loads(POOL.read_text())["records"]}
    return {q: (recs[q], cc[q]) for q in ITEMS}


def opening(rec):
    return (f'We are going to think about one question in steps. The question is: "{rec["question"]}". '
            f"I will ask you to rate several statements, one at a time, and the question itself. "
            f"Give each rating as an integer from 0 to 100, where {ANCHOR}.")


def sub_q(rec, k):
    return f"How likely is it that this statement is true? '{rec['contentions'][k]['text']}'"


MAIN = "How likely is it that the answer to the question is yes?"


def converse(lm, theta, key, rec, S, cell, qid):
    """One conversation: the cell's sub-questions, then (if theta given) the probe branch, then M."""
    import local_lm
    c = local_lm.Chat(lm, key)
    head = opening(rec)
    if cell in TOLD:
        head += "\n\n" + TOLD[cell]
    subs = [S[i] for i in LATIN[int(cell[1]) - 1]] if cell in ORDERS else []
    rec_out = {"sub": []}
    for t, k in enumerate(subs):
        txt = sub_q(rec, k)
        rec_out["sub"].append({"claim": k, "rating": c.rate(head + "\n\n" + txt if t == 0 else txt)})
    first = not subs
    if theta is not None:
        stmt = STATEMENT[qid]
        h = c.probe(head + "\n\n" + stmt if first else stmt, stmt)
        rec_out["probe_stmt"] = (theta * h).sum(1).tolist()           # projection at every layer
    rec_out["M"] = c.rate(head + "\n\n" + MAIN if first else MAIN)
    if theta is not None:
        rec_out["probe_mprompt"] = (theta * c.last_rate_hidden).sum(1).tolist()
    return rec_out


def collect(model, cells, theta, path):
    import local_lm
    lm = local_lm.LM(model)
    data = json.loads(path.read_text()) if path.exists() else {}
    t0, n = time.time(), 0
    for rep in range(R):   # repeat index outermost, so a stop leaves balanced cells
        for qid, (rec, S) in items().items():
            for cell in cells:
                key = f"{qid}|{cell}|{rep}"
                if key in data:
                    continue
                data[key] = converse(lm, theta, key, rec, S, cell, qid)
                n += 1
        path.write_text(json.dumps(data))
        print(f"rep {rep}: {len(data)} conversations, {time.time() - t0:.0f}s", flush=True)
    return data


# --- statistics -----------------------------------------------------------------

def order_matrix(data, qid, field, layer=None):
    """[4 orders x R repeats] of a measure for one item."""
    def val(d):
        v = d[field]
        return v[layer] if layer is not None else v
    return np.array([[val(data[f"{qid}|{o}|{r}"]) for r in range(R)] for o in ORDERS], dtype=float)


def between_within(X):
    """Between-order variance of means, mean within-order variance, noise-corrected signal variance."""
    B = X.mean(1).var(ddof=1)
    W = X.var(1, ddof=1).mean()
    return B, W, max(0.0, B - W / X.shape[1])


def perm_p(mats, rng, n=N_PERM):
    """Pooled within-item permutation test of order: statistic = sum over items of between-order variance."""
    stat = lambda Ms: sum(M.mean(1).var(ddof=1) for M in Ms)
    obs = stat(mats)
    flat = [M.ravel() for M in mats]
    hits = 0
    for _ in range(n):
        hits += stat([rng.permutation(f).reshape(4, -1) for f in flat]) >= obs - 1e-12
    return (hits + 1) / (n + 1), obs


def gate_item(M, rng):
    span = M.mean(1).max() - M.mean(1).min()
    p, _ = perm_p([M], rng)
    return {"means": M.mean(1).round(2).tolist(), "sds": M.std(1, ddof=1).round(2).tolist(),
            "span": round(float(span), 2), "p": round(float(p), 4), "shifts": bool(span >= 5 and p < 0.05)}


def q_stats(V, P, TV, TP, G):
    """V, P: {qid: 4xR}; TV, TP: {qid: (T+ array, T- array)}; G: gate items. Returns Q, r, D_V, D_P."""
    D_V = np.mean([TV[q][0].mean() - TV[q][1].mean() for q in TV])
    D_P = np.mean([TP[q][0].mean() - TP[q][1].mean() for q in TP])
    sV = sum(between_within(V[q])[2] for q in G)
    sP = sum(between_within(P[q])[2] for q in G)
    Q = (np.sqrt(sP) / D_P) / (np.sqrt(sV) / D_V) if sV > 0 and D_P != 0 else np.nan
    cv = np.concatenate([V[q].mean(1) - V[q].mean() for q in G])
    cp = np.concatenate([P[q].mean(1) - P[q].mean() for q in G])
    r = float(np.corrcoef(cv, cp)[0, 1]) if cv.std() > 0 and cp.std() > 0 else np.nan
    return {"Q": float(Q), "r": r, "D_V": float(D_V), "D_P": float(D_P)}


def bootstrap(V, P, TV, TP, G, rng, n=N_BOOT):
    """Items resampled with replacement (G membership travels with the item); repeats resampled within cells."""
    qs = list(TV)
    res = {k: [] for k in ("Q", "r", "D_V", "D_P")}
    rs = lambda a: a[rng.integers(0, len(a), len(a))]
    for _ in range(n):
        pick = [qs[i] for i in rng.integers(0, len(qs), len(qs))]
        Vb, Pb, TVb, TPb, Gb = {}, {}, {}, {}, []
        for j, q in enumerate(pick):
            name = f"{q}#{j}"
            TVb[name] = (rs(TV[q][0]), rs(TV[q][1]))
            TPb[name] = (rs(TP[q][0]), rs(TP[q][1]))
            if q in G:
                idx = rng.integers(0, R, (4, R))
                Vb[name] = np.take_along_axis(V[q], idx, 1)
                Pb[name] = np.take_along_axis(P[q], idx, 1)
                Gb.append(name)
        if not Gb:
            continue
        s = q_stats(Vb, Pb, TVb, TPb, Gb)
        for k in res:
            res[k].append(s[k])
    ci = lambda a: [float(np.nanpercentile(a, 2.5)), float(np.nanpercentile(a, 97.5))]
    return {k: ci(v) for k, v in res.items()}


def verdict(stats, ci, p_probe, p_verbal, sel_auroc):
    """The frozen rule of section 5. Returns (label, list of reasons)."""
    why = []
    if sel_auroc < 0.70:
        why.append(f"V1 probe selection AUROC {sel_auroc:.2f} < 0.70")
    if ci["D_P"][0] <= 0:
        why.append("V2 the probe does not move under the told-yes/told-no control (CI of D_P reaches 0)")
    if ci["D_V"][0] <= 0:
        why.append("V3 the rating does not move under the told-yes/told-no control")
    if p_verbal >= 0.05:
        why.append(f"V4 the step-3 verbal order effect on the gate items is not significant (p = {p_verbal:.3f})")
    if why:
        return "UNDECIDED (validity)", why
    if p_probe >= 0.05:
        if ci["Q"][1] < 0.5:
            return "DISSOCIATION: readout constructed over a stable belief", why
        return "UNDECIDED (probe too noisy to tell)", why
    if ci["r"][0] > 0:
        part = "fully" if ci["Q"][1] >= 1 else ("partly" if ci["Q"][1] >= 0.5 else "a little (Q < 0.5)")
        return f"BELIEF MOVES ({part})", why
    return "PROBE MOVES, BUT NOT WITH THE RATING", why


# --- steps ----------------------------------------------------------------------

def cmd_gate(model):
    path = out(model, "gate")
    data = collect(model, ORDERS + ["B0"], None, path)
    rng = np.random.default_rng(SEED)
    per = {q: gate_item(order_matrix(data, q, "M"), rng) for q in ITEMS}
    for q in ITEMS:
        b0 = np.array([data[f"{q}|B0|{r}"]["M"] for r in range(R)], float)
        allm = per[q]["means"] + [b0.mean()]
        per[q].update(b0_mean=round(float(b0.mean()), 2), b0_sd=round(float(b0.std(ddof=1)), 2),
                      span_with_b0=round(float(max(allm) - min(allm)), 2))
    G = [q for q in ITEMS if per[q]["shifts"]]
    summary = {"model": model, "per_item": per, "gate_items": G, "passes": len(G) >= 3}
    (RESULTS / f"probe-dissociation-{model}-gate-summary.json").write_text(json.dumps(summary, indent=1))
    for q in ITEMS:
        print(q, per[q])
    print("GATE", "PASS" if summary["passes"] else "FAIL", G)


def load_set(name, n=None, rng=None):
    GOT_DIR.mkdir(parents=True, exist_ok=True)
    f = GOT_DIR / f"{name}.csv"
    if not f.exists():
        urllib.request.urlretrieve(GOT_URL.format(name), f)
    rows = [(r["statement"], int(r["label"])) for r in csv.DictReader(f.open())]
    if n is not None and n < len(rows):
        rows = [rows[i] for i in sorted(rng.choice(len(rows), n, replace=False))]
    return rows


def auroc(score, y):
    from scipy.stats import rankdata
    score, y = np.asarray(score), np.asarray(y)
    rk = rankdata(score)
    n1, n0 = y.sum(), len(y) - y.sum()
    return float((rk[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def cmd_train(model):
    import local_lm
    lm = local_lm.LM(model)
    rng = np.random.default_rng(SEED)
    # Same sampling order as a one-pass version; two passes keep memory small (class sums, then projections).
    rows = {s: load_set(s, N_TRAIN, rng) for s in TRAIN_SETS}
    rows.update({s: load_set(s, n, rng) for s, n in {**SELECT_SETS, **REPORT_SETS}.items()})
    sums, counts = {1: 0.0, 0: 0.0}, {1: 0, 0: 0}
    for s in TRAIN_SETS:
        for st, y in rows[s]:
            sums[y] = sums[y] + lm.hidden_of(lm.statement_text(st))
            counts[y] += 1
        print("train", s, len(rows[s]), flush=True)
    mu1, mu0 = sums[1] / counts[1], sums[0] / counts[0]
    theta = mu1 - mu0                                                # mass-mean direction per layer
    mid = ((mu1 + mu0) / 2 * theta).sum(-1)
    feats = {}
    for s, rs in rows.items():
        feats[s] = (np.stack([(lm.hidden_of(lm.statement_text(st)) * theta).sum(-1) for st, _ in rs]),
                    np.array([y for _, y in rs]))
        print("score", s, len(rs), flush=True)
    table = {}
    for s, (sc, y) in feats.items():                                 # sc: [n, L+1] projections
        table[s] = {"auroc": [auroc(sc[:, l], y) if l else 0.5 for l in range(lm.n_layers + 1)],
                    "acc": [float(((sc[:, l] > mid[l]) == y).mean()) for l in range(lm.n_layers + 1)],
                    "sep": [float(sc[y == 1, l].mean() - sc[y == 0, l].mean()) for l in range(lm.n_layers + 1)]}
    sel = [float(np.mean([table[s]["auroc"][l] for s in SELECT_SETS])) for l in range(lm.n_layers + 1)]
    sel[0] = 0.0
    layer = int(np.argmax(sel))
    np.savez(RESULTS / f"probe-dissociation-{model}-theta.npz", theta=theta.astype(np.float32), mid=mid)
    summary = {"model": model, "layer": layer, "selection_auroc": sel[layer], "selection_by_layer": sel,
               "datasets": table, "got_sha": GOT_SHA}
    out(model, "probes").write_text(json.dumps(summary, indent=1))
    print(f"layer {layer}: selection AUROC {sel[layer]:.3f}; report set AUROC "
          f"{table['common_claim_true_false']['auroc'][layer]:.3f}")


def cmd_run(model):
    theta = np.load(RESULTS / f"probe-dissociation-{model}-theta.npz")["theta"]
    collect(model, ORDERS + ["B0", "T+", "T-"], theta, out(model, "run"))


def compute(model, layer=None, field="probe_stmt", items_override=None):
    probes = json.loads(out(model, "probes").read_text())
    gate = json.loads((RESULTS / f"probe-dissociation-{model}-gate-summary.json").read_text())
    data = json.loads(out(model, "run").read_text())
    layer = probes["layer"] if layer is None else layer
    G = items_override or gate["gate_items"]
    V = {q: order_matrix(data, q, "M") for q in ITEMS}
    P = {q: order_matrix(data, q, field, layer) for q in ITEMS}
    cell = lambda q, c, f, l=None: np.array([(data[f"{q}|{c}|{r}"][f][l] if l is not None else data[f"{q}|{c}|{r}"][f])
                                             for r in range(R)], float)
    TV = {q: (cell(q, "T+", "M"), cell(q, "T-", "M")) for q in ITEMS}
    TP = {q: (cell(q, "T+", field, layer), cell(q, "T-", field, layer)) for q in ITEMS}
    rng = np.random.default_rng(SEED)
    p_V, _ = perm_p([V[q] for q in G], rng)
    p_P, _ = perm_p([P[q] for q in G], rng)
    st = q_stats(V, P, TV, TP, G)
    ci = bootstrap(V, P, TV, TP, G, rng)
    label, why = verdict(st, ci, p_P, p_V, probes["selection_auroc"])
    per = {}
    for q in ITEMS:
        bV, wV, sV = between_within(V[q])
        bP, wP, sP = between_within(P[q])
        b0V, b0P = cell(q, "B0", "M"), cell(q, "B0", field, layer)
        per[q] = {"gate": q in G, "V_means": V[q].mean(1).round(2).tolist(), "V_sd": float(np.sqrt(wV)),
                  "P_means": P[q].mean(1).round(4).tolist(), "P_sd": float(np.sqrt(wP)),
                  "V_order_sd": float(np.sqrt(sV)), "P_order_sd": float(np.sqrt(sP)),
                  "B0_V": float(b0V.mean()), "B0_P": float(b0P.mean()),
                  "T+_V": float(TV[q][0].mean()), "T-_V": float(TV[q][1].mean()),
                  "T+_P": float(TP[q][0].mean()), "T-_P": float(TP[q][1].mean())}
    return {"model": model, "layer": layer, "field": field, "gate_items": G, "stats": st, "ci": ci,
            "p_verbal": p_V, "p_probe": p_P, "verdict": label, "validity_failures": why, "per_item": per}


def cmd_analyse(model):
    probes = json.loads(out(model, "probes").read_text())
    L = probes["layer"]
    res = {"primary": compute(model)}
    res["sensitivity"] = {f"layer {l}": compute(model, layer=l) for l in (L - 2, L + 2) if 1 <= l <= len(probes["selection_by_layer"]) - 1}
    res["sensitivity"]["M-prompt position"] = compute(model, field="probe_mprompt")
    res["sensitivity"]["all 10 items"] = compute(model, items_override=ITEMS)
    (RESULTS / "probe-dissociation.json").write_text(json.dumps(res, indent=1))
    for k, v in [("primary", res["primary"])] + list(res["sensitivity"].items()):
        s, c = v["stats"], v["ci"]
        print(f"{k:22s} Q = {s['Q']:.2f} [{c['Q'][0]:.2f}, {c['Q'][1]:.2f}]  r = {s['r']:+.2f} [{c['r'][0]:+.2f}, {c['r'][1]:+.2f}]"
              f"  p_P = {v['p_probe']:.4f}  p_V = {v['p_verbal']:.4f}  D_V = {s['D_V']:.1f}  D_P = {s['D_P']:.3f}  -> {v['verdict']}")


def cmd_simulate():
    """Analysis check: a stable-belief world must give DISSOCIATION, a moving-belief world BELIEF MOVES."""
    rng = np.random.default_rng(1)
    for world in ("stable", "moving", "noisy"):
        V, P, TV, TP = {}, {}, {}, {}
        for q in ITEMS:
            belief, off = rng.uniform(20, 80), rng.normal(0, 12, 4)
            v = belief + off[:, None] + rng.normal(0, 5, (4, R))
            move = off if world == "moving" else np.zeros(4)
            pn = 0.4 if world == "noisy" else 0.03
            P[q] = 0.01 * (belief + move)[:, None] + rng.normal(0, pn, (4, R))
            V[q] = np.clip(v, 0, 100)
            TV[q] = (np.clip(90 + rng.normal(0, 5, R), 0, 100), np.clip(10 + rng.normal(0, 5, R), 0, 100))
            TP[q] = (0.9 + rng.normal(0, pn, R), 0.1 + rng.normal(0, pn, R))
        G = [q for q in ITEMS if gate_item(V[q], rng)["shifts"]]
        p_V, _ = perm_p([V[q] for q in G], rng, 2000)
        p_P, _ = perm_p([P[q] for q in G], rng, 2000)
        st, ci = q_stats(V, P, TV, TP, G), bootstrap(V, P, TV, TP, G, rng, 500)
        print(f"{world:7s} |G|={len(G)} Q={st['Q']:.2f} [{ci['Q'][0]:.2f}, {ci['Q'][1]:.2f}] r={st['r']:+.2f} "
              f"p_P={p_P:.4f} -> {verdict(st, ci, p_P, p_V, 0.9)[0]}")


if __name__ == "__main__":
    cmd, *a = sys.argv[1:]
    {"gate": cmd_gate, "train": cmd_train, "run": cmd_run, "analyse": cmd_analyse, "simulate": cmd_simulate}[cmd](*a)

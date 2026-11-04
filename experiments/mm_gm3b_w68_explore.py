"""Exploratory (D49a): Kendall's W for each model on Opus's 68 complete claims, gm3b's formula unchanged."""
import json, numpy as np
import gm3b_format_invariance as g, mm_gm3b as mm
from entangled_mind import config
opus = {k: v for k, v in json.loads(mm.cache_path("opus").read_text()).items() if v.get("value") is not None}
done = [(q, k) for q, k in mm.claims80() if all(f"{q}|{k}|{f}|{r}" in opus for f in g.FORMATS for r in range(g.R))]
keep = set(done)
out = {}
for m, path in (("haiku", config.RESULTS / "gm3b-calls.json"), ("sonnet", mm.cache_path("sonnet")), ("opus", mm.cache_path("opus"))):
    conv = {k: v for k, v in json.loads(path.read_text()).items() if v.get("value") is not None and (k.split("|")[0], int(k.split("|")[1])) in keep}
    g.claims = lambda: done
    obs, nc = g.encode(conv)
    means = np.full((nc, 6), np.nan)
    for fi, f in enumerate(g.FORMATS):
        d = obs[f]
        for c in range(nc):
            y = d["y"][d["c"] == c]
            if len(y):
                means[c, fi] = y.mean() if f not in ("F1", "F5") else np.mean(1 / (1 + np.exp(-y)))
    rank = np.argsort(np.argsort(np.nan_to_num(means), axis=0), axis=0).astype(float)
    S = ((rank.sum(axis=1) - 6 * (nc - 1) / 2) ** 2).sum()
    out[m] = round(float(12 * S / (36 * (nc ** 3 - nc))), 3)
out["claims"] = len(done)
(config.RESULTS / "mm-gm3b-W-on-68-exploratory.json").write_text(json.dumps(out, indent=1))
print(out)

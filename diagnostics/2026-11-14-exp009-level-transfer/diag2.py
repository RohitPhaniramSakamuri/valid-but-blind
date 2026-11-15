"""Isolation step 1: is the uneven transfer predictable from dev streams alone? Leave-one-dev-family-out (LOFO) false alarms and misses of the frozen rule (twin, global conformal level)."""
import numpy as np, json
from lib9 import *
S = load(); out = {}
print("group | n_fam | level | LOFO per-family FA (safe n) ... | LOFO pooled FA, miss | held FA, miss | level SD over family-bootstrap | level if top family dropped")
for g, L in groups(S, "tent0.001").items():
    f = simple("twin"); dev = [s for s in L if s["split"] == "dev"]; held = [s for s in L if s["split"] == "held"]
    for s in L: s["m"] = float(f(s).max())
    fams = sorted({s["cor"] for s in dev}); ds = [s for s in dev if s["safe"]]
    if len(ds) < 19: continue
    lv = conformal([s["m"] for s in ds]); per = {}; fa = [0, 0]; mi = [0, 0]
    for c in fams:
        l = conformal([s["m"] for s in ds if s["cor"] != c]); a = [s["m"] > l for s in dev if s["cor"] == c and s["safe"]]; m = [s["m"] <= l for s in dev if s["cor"] == c and s["strict"]]
        per[c] = (sum(a), len(a), sum(m), len(m)); fa[0] += sum(a); fa[1] += len(a); mi[0] += sum(m); mi[1] += len(m)
    rng = np.random.default_rng(0); bl = []
    for _ in range(500):
        pick = rng.choice(len(fams), len(fams)); v = [s["m"] for i in pick for s in ds if s["cor"] == fams[i]]
        if len(v) >= 19: bl.append(conformal(v))
    drop = min(conformal([s["m"] for s in ds if s["cor"] != c]) for c in fams)
    hfa = [sum(s["m"] > lv for s in held if s["safe"]), sum(s["safe"] for s in held)]; hmi = [sum(s["m"] <= lv for s in held if s["strict"]), sum(s["strict"] for s in held)]
    out["/".join(g)] = dict(level=lv, lofo=per, lofo_fa=fa, lofo_miss=mi, held_fa=hfa, held_miss=hmi, boot_sd=float(np.std(bl)), boot_q=[float(x) for x in np.quantile(bl, [.05, .5, .95])], drop_top=drop)
    print(g[0], g[1], g[2][:10], "|", len(fams), f"| {lv:.3f} |", " ".join(f"{k[:6]}:{v[0]}/{v[1]}" for k, v in per.items()), f"| {fa[0]}/{fa[1]} {mi[0]}/{mi[1]} | {hfa[0]}/{hfa[1]} {hmi[0]}/{hmi[1]} | sd {np.std(bl):.3f} q {np.quantile(bl,.05):.2f}-{np.quantile(bl,.95):.2f} | {drop:.3f}")
json.dump(out, open("diag2.json", "w"), indent=1)

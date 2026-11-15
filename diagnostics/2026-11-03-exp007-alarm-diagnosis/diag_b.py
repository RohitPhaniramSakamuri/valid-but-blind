"""Diagnosis: which dev streams set the margin; 3-model agreement patterns; matched-false-alarm comparison (EXPLORATORY)."""
import glob, json, os, collections, numpy as np
from multiprocessing import Pool
from load7 import load, IDX, cum, conformal, R6
S = load(); G = sorted({(s["ds"], s["model"], s["arm"]) for s in S})
tw = lambda s: (cum(s["b"]["flag"]) - s["c"]["r_twin"])[IDX]
out = {}
# 1. top safe dev streams that set each primary margin
top = {}
for g in [g for g in G if g[2] == "tent0.001"]:
    sd = sorted([(float(tw(s).max()), s["cor"], s["sev"], s["prior"], round(s["err"] - s["c"]["r0"], 3), round(float(s["b"]["false_flag"].mean()), 3), round(float(s["b"]["errW"].mean() - s["b"]["errT"].mean()), 3)) for s in S if (s["ds"], s["model"], s["arm"]) == g and s["split"] == "dev" and s["safe"]], reverse=True)
    top["/".join(g)] = [dict(score=round(a, 3), cor=b, sev=c, prior=d, excess=e, false_flag=f, twin_minus_tent_err=h) for a, b, c, d, e, f, h in sd[:5]]
out["top_safe_dev"] = top
# 2. three-model agreement patterns: share of images and Tent error within each (needs per-image data)
def pat(p):
    I = np.load(p)["img"].astype(np.float32); tw_, ts, ws, e = I[:, :, 8] > .5, I[:, :, 9] > .5, I[:, :, 10] > .5, I[:, :, 17] > .5
    P = {"all_agree": tw_ & ts, "T=W!=S": tw_ & ~ts, "T=S!=W": ts & ~tw_, "W=S!=T": ws & ~tw_, "all_differ": ~tw_ & ~ts & ~ws}
    return {k: (float(v.mean()), float(e[v].mean()) if v.any() else np.nan) for k, v in P.items()}
files = {}
for p in sorted(f for f in glob.glob(f"{R6}/*/*.npz") if not f.endswith(".tmp.npz")): files[p] = None
with Pool(os.cpu_count()) as pool: pats = dict(zip(files, pool.map(pat, list(files), chunksize=16)))
keyof = lambda s: f"{R6}/{s['ds']}__{s['model']}__{s['arm']}/{s['split']}__{s['cor']}__{s['sev']}__{s['prior']}__{s['rep']}.npz"
for kind, f in (("strict", lambda s: s["strict"]), ("safe", lambda s: s["safe"])):
    for ds in ("path", "organa", "cifar"):
        x = [pats[keyof(s)] for s in S if s["arm"] == "tent0.001" and s["split"] == "held" and s["ds"] == ds and f(s)]
        out.setdefault("patterns", {})[f"{ds}/{kind}"] = {k: dict(share=round(float(np.nanmean([d[k][0] for d in x])), 3), tent_err=round(float(np.nanmean([d[k][1] for d in x])), 3)) for k in x[0]} if x else None
# 3. matched false-alarm comparison on held (oracle per-group thresholds; descriptive only)
DET = dict(twin=tw, released=lambda s: (cum(s["b"]["rel"]) - s["c"]["r0"])[IDX], prototype=lambda s: (cum(s["b"]["pro"]) - s["c"]["r0"])[IDX],
           doc=lambda s: (s["c"]["conf_clean"] - cum(s["b"]["confT"]))[IDX], dropout=lambda s: cum(s["b"]["dd"])[IDX], atc=lambda s: cum(s["b"]["atc"])[IDX],
           twin_minus_disagree_conf=lambda s: (cum(s["b"]["flag"]) - cum(s["b"]["confT"]) + s["c"]["conf_clean"])[IDX])
H = [s for s in S if s["arm"] == "tent0.001" and s["split"] == "held"]
res = {}
for f in (.024, .05, .066, .10):
    res[f] = {}
    for n, fn in DET.items():
        miss = [0, 0]; fa = [0, 0]
        for g in [g for g in G if g[2] == "tent0.001"]:
            hs = np.array([fn(s).max() for s in H if (s["ds"], s["model"]) == g[:2] and s["safe"]]); st = np.array([fn(s).max() for s in H if (s["ds"], s["model"]) == g[:2] and s["strict"]])
            thr = np.quantile(hs, 1 - f) if len(hs) else np.inf
            miss[0] += int((st <= thr).sum()); miss[1] += len(st); fa[0] += int((hs > thr).sum()); fa[1] += len(hs)
        res[f][n] = dict(missed=f"{miss[0]}/{miss[1]} ({miss[0]/miss[1]:.1%})", fa=f"{fa[0]}/{fa[1]} ({fa[0]/fa[1]:.1%})")
out["matched_fa_oracle"] = res
# pooled-within-group AUROC of max score
au = {}
for n, fn in DET.items():
    v = []
    for g in [g for g in G if g[2] == "tent0.001"]:
        hs = np.array([fn(s).max() for s in H if (s["ds"], s["model"]) == g[:2] and s["safe"]]); st = np.array([fn(s).max() for s in H if (s["ds"], s["model"]) == g[:2] and s["strict"]])
        if len(hs) and len(st): v.append(((st[:, None] > hs[None, :]).mean(), len(st) * len(hs)))
    au[n] = round(sum(a * w for a, w in v) / sum(w for _, w in v), 3)
out["auroc_within_group"] = au
json.dump(out, open("diag_b.json", "w"), indent=1)
print("TOP SAFE DEV (setting the margin):"); [print(" ", g, v[:3]) for g, v in top.items()]
print("PATTERNS:"); [print(" ", k, v) for k, v in out["patterns"].items()]
print("MATCHED FA (oracle):"); [print(" ", f, r) for f, r in res.items()]
print("AUROC within group:", au)

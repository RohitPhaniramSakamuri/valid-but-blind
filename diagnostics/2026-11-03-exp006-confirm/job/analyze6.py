"""exp006 analysis, frozen with experiments/006. Margins use dev streams of the same (dataset, model, arm) only; held streams are scored once."""
import glob, json, math, os, sys
from multiprocessing import Pool
import numpy as np, lightgbm as lgb
from confseq.conjmix_bounded import conjmix_empbern_lower_cs
from confseq.predmix import predmix_empbern_lower_cs
OUT = os.environ["OUT"]; MIN_T, STEP = 10, 5; IDX = np.arange(MIN_T, 120, STEP); ALPHA_C = .05
ALPHA, AL1, TOL = .15, .025, .1
def v_opt(x, t):
    m = np.cumsum(x) / np.arange(1, len(x) + 1); return np.cumsum((x - np.append(.5, m[:-1])) ** 2)[t] * t
def first_cs(z, L, level):
    x = np.clip(np.asarray(z, dtype=float), 0, 1)
    try: cs = np.asarray(conjmix_empbern_lower_cs(x=x, alpha=ALPHA, v_opt=v_opt(x, int(len(x) * .25))))
    except Exception: cs = np.asarray(predmix_empbern_lower_cs(x=x, alpha=ALPHA))
    h = np.where(np.maximum(cs - L, 0) > level)[0]; return int(h[0]) + 1 if len(h) else None
cum = lambda x: np.cumsum(x) / np.arange(1, len(x) + 1)
def load(p):
    d = os.path.dirname(p); c = json.load(open(d + "/calibration.json")); split, cor, sev, pr, rep = os.path.basename(p)[:-4].split("__")
    z = np.load(p); I = z["img"].astype(np.float32); Bv = z["batch"].astype(np.float32); e = I[:, :, 17].mean(1); m, l = e.mean(), e[-30:].mean()
    tw = (I[:, :, 23] + (1 - I[:, :, 23]) * (1 - I[:, :, 8])).mean(1); w = (math.log(2) - math.log(AL1)) / (2 * c["n"]); lv = c["r0"] + TOL
    bs = I[:, :, :17].mean(1)
    sc = dict(twin=cum(tw) - c["r_twin"], released=cum(I[:, :, 21].mean(1)) - c["r0"], prototype=cum(I[:, :, 22].mean(1)) - c["r0"], atc=cum((I[:, :, 0] < c["t_atc"]).mean(1)) - c["r0"], doc=c["conf_clean"] - cum(bs[:, 0]), dropout=cum(bs[:, 16]) - c["r0"])
    sc = {k: v[IDX] for k, v in sc.items()}
    cs = dict(twin_bound=first_cs(tw, c["fpt"] + c["fnt"] + w, lv), released_bound=first_cs(I[:, :, 21].mean(1), c["fp0"] + w, lv), prototype_bound=first_cs(I[:, :, 22].mean(1), c["fpp0"] + w, lv))
    X = np.hstack((bs, I[:, :, 21:24].mean(1), tw[:, None], Bv[:, :10])); n = np.arange(1, 121)[:, None]; cm = np.cumsum(X, 0) / n
    cx = np.vstack((np.zeros((1, X.shape[1])), np.cumsum(X, 0))); lo = np.maximum(np.arange(120) - 9, 0); rec = (cx[np.arange(120) + 1] - cx[lo]) / (np.arange(120) + 1 - lo)[:, None]
    F = np.hstack((cm, rec, np.tile([c["r0"], c["r_twin"], c["fpt"], c["fnt"], c["conf_clean"], math.log(c["K"])], (120, 1)), np.log(n)))[IDX]
    yv = (cum(e) - c["r0"])[IDX]
    return dict(ds=c["ds"], model=c["model"], arm=c["arm"], split=split, cor=cor, sev=int(sev), prior=pr, key=p, r0=c["r0"], err=float(m), strict=bool(m >= c["r0"] + .15 and l < .85), safe=bool(m < c["r0"] + .1 and l < .85), collapsed=bool(l >= .85), sc=sc, cs=cs, F=F.astype(np.float32), y=yv.astype(np.float32))
def conformal(maxes):
    n = len(maxes); k = math.ceil((n + 1) * (1 - ALPHA_C))
    return (float(np.sort(maxes)[k - 1]) if k <= n else float("inf")), n
def gbm(): return lgb.LGBMRegressor(n_estimators=250, learning_rate=.05, num_leaves=15, min_child_samples=40, subsample=.8, subsample_freq=1, colsample_bytree=.7, verbose=-1, n_jobs=4, random_state=0)
def summ(rows):
    st, sf = [r for r in rows if r["strict"]], [r for r in rows if r["safe"]]
    return dict(missed=[sum(not r["alarm"] for r in st), len(st)], false_alarm=[sum(r["alarm"] for r in sf), len(sf)], median_first=float(np.median([r["first"] for r in st if r["alarm"]] or [np.nan])))
sh = lambda x: x[0] / x[1] if x[1] else float("nan")
if __name__ == "__main__":
    files = sorted(glob.glob(f"{OUT}/streams/*/*.npz")); files = [f for f in files if not f.endswith(".tmp.npz")]
    with Pool(os.cpu_count()) as pool: S = pool.map(load, files, chunksize=8)
    print(len(S), "streams", flush=True)
    G = sorted({(s["ds"], s["model"], s["arm"]) for s in S}); UN = list(S[0]["sc"])
    # LightGBM (descriptive): fit per dataset on dev streams, out-of-fold by dev corruption for margins.
    lg = {}
    for ds in sorted({g[0] for g in G}):
        dev = [s for s in S if s["ds"] == ds and s["split"] == "dev"]
        for c in sorted({s["cor"] for s in dev}):
            tr = [s for s in dev if s["cor"] != c]; m = gbm().fit(np.vstack([s["F"] for s in tr]), np.concatenate([s["y"] for s in tr]))
            for s in dev:
                if s["cor"] == c: s["sc"]["lgbm"] = m.predict(s["F"])
        m = gbm().fit(np.vstack([s["F"] for s in dev]), np.concatenate([s["y"] for s in dev]))
        for s in S:
            if s["ds"] == ds and s["split"] == "held": s["sc"]["lgbm"] = m.predict(s["F"])
    DET = UN + ["lgbm"]; rows = {d: [] for d in DET}; margins = {}
    for g in G:
        dev = [s for s in S if (s["ds"], s["model"], s["arm"]) == g and s["split"] == "dev"]; held = [s for s in S if (s["ds"], s["model"], s["arm"]) == g and s["split"] == "held"]
        for d in DET:
            thr, n = conformal([s["sc"][d].max() for s in dev if s["safe"]]); margins[f"{'/'.join(g)}/{d}"] = [thr, n]
            for s in held:
                h = np.where(s["sc"][d] > thr)[0]; rows[d].append(dict(ds=g[0], model=g[1], arm=g[2], cor=s["cor"], sev=s["sev"], prior=s["prior"], strict=s["strict"], safe=s["safe"], alarm=bool(len(h)), first=int(IDX[h[0]]) + 1 if len(h) else None))
        for d in ("twin_bound", "released_bound", "prototype_bound"):
            for s in held: rows.setdefault(d, []).append(dict(ds=g[0], model=g[1], arm=g[2], cor=s["cor"], sev=s["sev"], prior=s["prior"], strict=s["strict"], safe=s["safe"], alarm=s["cs"][d] is not None, first=s["cs"][d]))
    rep = dict(counts={}, margins=margins, tables={})
    for g in G:
        for sp in ("dev", "held"):
            x = [s for s in S if (s["ds"], s["model"], s["arm"]) == g and s["split"] == sp]
            rep["counts"]["/".join(g) + "/" + sp] = dict(n=len(x), strict=sum(s["strict"] for s in x), safe=sum(s["safe"] for s in x), collapsed=sum(s["collapsed"] for s in x), err=round(float(np.mean([s["err"] for s in x])), 3) if x else None, r0=round(x[0]["r0"], 3) if x else None)
    sel = lambda f: {d: summ([r for r in R if f(r)]) for d, R in rows.items()}
    prim = lambda r: r["arm"] == "tent0.001"
    rep["tables"]["primary_pooled"] = sel(prim)
    for ds in ("path", "organa", "cifar"): rep["tables"][f"primary_{ds}"] = sel(lambda r, ds=ds: prim(r) and r["ds"] == ds)
    for m in sorted({g[1] for g in G if g[0] == "cifar"}): rep["tables"][f"cifar_{m}"] = sel(lambda r, m=m: prim(r) and r["model"] == m)
    for ds in ("path", "organa"):
        for a in ("tent0.005", "sar"): rep["tables"][f"{ds}_{a}"] = sel(lambda r, ds=ds, a=a: r["ds"] == ds and r["arm"] == a)
    rep["tables"]["by_corruption_twin"] = {f"{ds}/{c}": summ([r for r in rows["twin"] if prim(r) and r["ds"] == ds and r["cor"] == c]) for ds, c in sorted({(r["ds"], r["cor"]) for r in rows["twin"]})}
    P = rep["tables"]["primary_pooled"]; t, rl, tb = P["twin"], P["released"], P["twin_bound"]
    per = [rep["tables"][f"primary_{ds}"]["twin"] for ds in ("path", "organa", "cifar")]
    if t["missed"][1] < 40 or t["false_alarm"][1] < 60: v = "INCONCLUSIVE"
    else:
        pooled = sh(t["missed"]) <= .2 and sh(t["false_alarm"]) <= .1 and sh(rl["missed"]) - sh(t["missed"]) >= .15 and sh(tb["missed"]) - sh(t["missed"]) >= .15
        each = all(x["missed"][1] > 0 and sh(x["missed"]) <= .3 and (x["false_alarm"][1] == 0 or sh(x["false_alarm"]) <= .15) for x in per)
        v = "CONFIRMED" if pooled and each else "PARTIAL" if pooled else "NOT CONFIRMED"
    rep["VERDICT"] = v
    json.dump(rep, open(f"{OUT}/report6.json", "w"), indent=1); json.dump(rows, open(f"{OUT}/rows6.json", "w"))
    print("VERDICT", v)
    for k in [k for k in rep["tables"] if k.startswith("primary")]:
        print(k); [print(f"  {d:16s} missed {x['missed']} FA {x['false_alarm']} first {x['median_first']}") for d, x in rep["tables"][k].items()]

"""Frozen with experiments/005. Selection reads dev streams only; held streams are scored once afterwards."""
import glob, json, os, warnings
from os.path import basename
import numpy as np, torch, torch.nn as nn, lightgbm as lgb
from sklearn.decomposition import PCA
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
warnings.filterwarnings("ignore")
MIN_T, STEP, NJ = 10, 5, 4  # thread count only; 28 threads stalled on small tables
CS = json.load(open("cs.json"))
IMG = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
def load():
    S = []
    for d in sorted(glob.glob("*/streams_*")):
        c = json.load(open(d + "/calibration.json"))
        for p in sorted(glob.glob(d + "/*.npz")):
            split, cor, sev, pr, rep = basename(p)[:-4].split("__"); z = np.load(p); I, B = z["img"].astype(np.float32), z["batch"].astype(np.float32)
            e = I[:, :, 17].mean(1); m, l = e.mean(), e[-30:].mean()
            twin = (I[:, :, 23] + (1 - I[:, :, 23]) * (1 - I[:, :, 8])).mean(1); bs = I[:, :, IMG].mean(1)
            s = dict(ds=c["ds"], lr=c["lr"], split=split, cor=cor, sev=int(sev), prior=pr, path=p, c=c, e=e, strict=bool(m >= c["r0"] + .15 and l < .85), safe=bool(m < c["r0"] + .1 and l < .85), collapsed=bool(l >= .85), cs=CS[p], rel=I[:, :, 21].mean(1), pro=I[:, :, 22].mean(1), tw=twin, atc=(I[:, :, 0] < c["t_atc"]).mean(1), conf=bs[:, 0], confS=bs[:, 2], dd=bs[:, 16])
            s["bf"] = np.hstack((bs, I[:, :, 21:24].mean(1), twin[:, None], B[:, :10]))
            s["lat"] = B[:, 10:]; s["img"] = I[:, :, IMG]; s["ierr"] = I[:, :, 17]
            S.append(s)
    return S
def pref(s, key="bf"):
    X = s[key]; T = len(X); n = np.arange(1, T + 1)[:, None]; cm = np.cumsum(X, 0) / n; cs = np.cumsum(np.vstack((np.zeros((1, X.shape[1])), X)), 0)
    lo = np.maximum(np.arange(T) - 9, 0); rec = (cs[np.arange(T) + 1] - cs[lo]) / (np.arange(T) + 1 - lo)[:, None]; c = s["c"]
    return np.hstack((cm, rec, np.tile([c["r0"], c["r_twin"], c["fpt"], c["fnt"], c["conf_clean"], np.log(c["K"])], (T, 1)), np.log(n)))
def target(s): return np.cumsum(s["e"]) / np.arange(1, 121) - s["c"]["r0"]
def cum(x): return np.cumsum(x) / np.arange(1, 121)
IDX = np.arange(MIN_T, 120, STEP)
UNL = dict(released=lambda s: cum(s["rel"]) - s["c"]["r0"], prototype=lambda s: cum(s["pro"]) - s["c"]["r0"], twin=lambda s: cum(s["tw"]) - s["c"]["r_twin"], atc=lambda s: cum(s["atc"]) - s["c"]["r0"], doc=lambda s: s["c"]["conf_clean"] - cum(s["conf"]), doc_source=lambda s: s["c"]["conf_clean"] - cum(s["confS"]), dropout=lambda s: cum(s["dd"]) - s["c"]["r0"])
def gbm(**k): return lgb.LGBMRegressor(n_estimators=250, learning_rate=.05, num_leaves=15, min_child_samples=40, subsample=.8, subsample_freq=1, colsample_bytree=.7, verbose=-1, n_jobs=NJ, random_state=0, **k)
class Tab:
    def __init__(s, mk, key="bf"): s.mk, s.key = mk, key
    def fit(s, D):
        s.m = s.mk().fit(np.vstack([s.x(a)[IDX] for a in D]), np.concatenate([target(a)[IDX] for a in D])); return s
    def x(s, a): return pref(a) if s.key == "bf" else np.hstack((pref(a), pref(a, "lat")))
    def score(s, a): return s.m.predict(s.x(a)[IDX])
class Stack:
    def __init__(s): s.a, s.b = make_pipeline(StandardScaler(), Ridge(3.)), gbm()
    def fit(s, X, y): s.a.fit(X, y); s.b.fit(X, y - s.a.predict(X)); return s
    def predict(s, X): return s.a.predict(X) + s.b.predict(X)
class Latent:
    def __init__(s): s.m = make_pipeline(StandardScaler(), PCA(12, random_state=0), gbm())
    def fit(s, X, y): s.m.fit(X, y); return s
    def predict(s, X): return s.m.predict(X)
class PerImage:
    def fit(s, D):
        X = np.vstack([a["img"].reshape(-1, len(IMG)) for a in D]); y = np.concatenate([a["ierr"].ravel() for a in D])
        s.m = lgb.LGBMClassifier(n_estimators=200, learning_rate=.05, num_leaves=31, min_child_samples=200, subsample=.5, subsample_freq=1, colsample_bytree=.7, verbose=-1, n_jobs=NJ, random_state=0).fit(X, y); return s
    def score(s, a): return cum(s.m.predict_proba(a["img"].reshape(-1, len(IMG)))[:, 1].reshape(120, 48).mean(1))[IDX] - a["c"]["r0"]
class Avg:
    def __init__(s, *m): s.m = m
    def fit(s, D):
        for x in s.m: x.fit(D)
        return s
    def score(s, a): return np.mean([x.score(a) for x in s.m], 0)
class GRU(nn.Module):
    def __init__(s, d): super().__init__(); s.g = nn.GRU(d, 32, batch_first=True); s.o = nn.Linear(32, 1)
    def forward(s, x): return s.o(s.g(x)[0]).squeeze(2)
class Seq:
    def x(s, a): c = a["c"]; return np.hstack((a["bf"], np.tile([c["r0"], c["r_twin"], c["conf_clean"]], (120, 1))))
    def fit(s, D):
        torch.manual_seed(0); X = np.stack([s.x(a) for a in D]); s.mu, s.sd = X.mean((0, 1)), X.std((0, 1)) + 1e-6
        X = torch.tensor((X - s.mu) / s.sd, dtype=torch.float32).cuda(); y = torch.tensor(np.stack([target(a) for a in D]), dtype=torch.float32).cuda()
        s.m = GRU(X.shape[2]).cuda(); o = torch.optim.AdamW(s.m.parameters(), lr=2e-3, weight_decay=1e-3)
        for _ in range(150):
            o.zero_grad(); ((s.m(X) - y) ** 2).mean().backward(); o.step()
        return s
    def score(s, a):
        with torch.inference_mode(): return s.m(torch.tensor((s.x(a) - s.mu) / s.sd, dtype=torch.float32)[None].cuda())[0].cpu().numpy()[IDX]
LEARN = dict(ridge=lambda: Tab(lambda: make_pipeline(StandardScaler(), Ridge(3.))), lgbm=lambda: Tab(gbm), stack=lambda: Tab(Stack), latent_lgbm=lambda: Tab(Latent, "lat"), gru=Seq, per_image=PerImage, image_plus_stream=lambda: Avg(PerImage(), Tab(gbm)))
def oof(dev, name):
    """Out-of-fold scores by dev corruption. Returns {id: scores}."""
    out = {}
    for c in sorted({a["cor"] for a in dev}):
        te = [a for a in dev if a["cor"] == c]; tr = [a for a in dev if a["cor"] != c]
        if name in UNL: out.update({id(a): UNL[name](a)[IDX] for a in te}); continue
        m = LEARN[name]().fit(tr); out.update({id(a): m.score(a) for a in te})
    return out
def margin(dev, sc): return float(np.quantile([sc[id(a)].max() for a in dev if a["safe"]], .95))
def summ(rows):
    st, sf = [r for r in rows if r["strict"]], [r for r in rows if r["safe"]]; mi = sum(not r["alarm"] for r in st); fa = sum(r["alarm"] for r in sf)
    a, b = np.array([r["top"] for r in st]), np.array([r["top"] for r in sf]); auc = float((a[:, None] > b[None, :]).mean()) if len(a) and len(b) else float("nan")
    return dict(missed=[mi, len(st)], false_alarm=[fa, len(sf)], auroc=round(auc, 3), median_first=float(np.median([r["first"] for r in st if r["alarm"]] or [np.nan])))
def rows_of(streams, sc, thr):
    R = []
    for a in streams:
        p = sc(a); h = np.where(p > thr)[0]; R.append(dict(strict=a["strict"], safe=a["safe"], alarm=bool(len(h)), first=int(IDX[h[0]]) + 1 if len(h) else None, top=float(p.max()), ds=a["ds"], lr=a["lr"], cor=a["cor"], sev=a["sev"], prior=a["prior"]))
    return R
if __name__ == "__main__":
    S = load(); rep = dict(counts={}, dev_cv={}, held={})
    for ds in ("blood", "derma"):
        for sp in ("dev", "held"):
            for lr in (.001, .005):
                g = [a for a in S if a["ds"] == ds and a["split"] == sp and a["lr"] == lr]
                rep["counts"][f"{ds}/{sp}/{lr}"] = dict(n=len(g), strict=sum(a["strict"] for a in g), safe=sum(a["safe"] for a in g), collapsed=sum(a["collapsed"] for a in g), err=round(float(np.mean([a["e"].mean() for a in g])), 3), r0=g[0]["c"]["r0"] if g else None)
    print(json.dumps(rep["counts"], indent=0), flush=True)
    DEV = {ds: [a for a in S if a["ds"] == ds and a["split"] == "dev"] for ds in ("blood", "derma")}
    OOF, MARG = {}, {}
    for name in list(UNL) + list(LEARN):
        pool = []
        for ds, dev in DEV.items():
            sc = oof(dev, name); thr = margin(dev, sc); OOF[name, ds] = sc; MARG[name, ds] = thr
            pool += rows_of(dev, lambda a: sc[id(a)], thr)
        rep["dev_cv"][name] = summ(pool); print(name, rep["dev_cv"][name], flush=True)
    ok = {n: rep["dev_cv"][n] for n in LEARN if rep["dev_cv"][n]["false_alarm"][0] <= .10 * max(rep["dev_cv"][n]["false_alarm"][1], 1)}
    sel = min(ok or {n: rep["dev_cv"][n] for n in LEARN}, key=lambda n: (rep["dev_cv"][n]["missed"][0], -rep["dev_cv"][n]["auroc"])); rep["selected"] = sel
    print("SELECTED ON DEV:", sel, flush=True); json.dump(rep, open("selection.json", "w"), indent=1)
    FIN = {(n, ds): LEARN[n]().fit(DEV[ds]) for n in LEARN for ds in DEV}
    all_rows = {}
    for ds in DEV:
        for lr in (.001, .005):
            H = [a for a in S if a["ds"] == ds and a["split"] == "held" and a["lr"] == lr]; tab = {}
            for n in list(UNL) + list(LEARN):
                f = (lambda a, n=n: UNL[n](a)[IDX]) if n in UNL else (lambda a, n=n, ds=ds: FIN[n, ds].score(a))
                R = rows_of(H, f, MARG[n, ds]); tab[n] = summ(R); all_rows[f"{ds}/{lr}/{n}"] = R
            for k in ("released", "prototype", "twin"):
                st, sf = [a for a in H if a["strict"]], [a for a in H if a["safe"]]
                tab[k + "_bound"] = dict(missed=[sum(a["cs"][k] is None for a in st), len(st)], false_alarm=[sum(a["cs"][k] is not None for a in sf), len(sf)], median_first=float(np.median([a["cs"][k] for a in st if a["cs"][k]] or [np.nan])))
            rep["held"][f"{ds}/{lr}"] = tab
    # Cross-dataset, descriptive: fit and margin from the other dataset's dev streams.
    rep["cross"] = {}
    for tr, te in (("derma", "blood"), ("blood", "derma")):
        H = [a for a in S if a["ds"] == te and a["split"] == "held" and a["lr"] == .001]
        rep["cross"][f"{tr}->{te}"] = {n: summ(rows_of(H, (lambda a, n=n: UNL[n](a)[IDX]) if n in UNL else (lambda a, n=n: FIN[n, tr].score(a)), MARG[n, tr])) for n in ("twin", "released", sel)}
    t = rep["held"]["blood/0.001"]; a, b = t[sel], t["twin"]; sh = lambda x: x[0] / x[1] if x[1] else float("nan")
    if a["missed"][1] < 20 or a["false_alarm"][1] < 40: v = "INCONCLUSIVE"
    else: v = "BETTER DETECTOR" if sh(a["missed"]) <= .2 and sh(a["false_alarm"]) <= .1 and sh(b["missed"]) - sh(a["missed"]) >= .1 and sh(a["false_alarm"]) - sh(b["false_alarm"]) <= .05 else "NOT SHOWN"
    rep["VERDICT"] = v
    json.dump(rep, open("report.json", "w"), indent=1); json.dump(all_rows, open("rows.json", "w"))
    print("VERDICT", v, json.dumps(rep["held"], indent=0), json.dumps(rep["cross"], indent=0), flush=True)

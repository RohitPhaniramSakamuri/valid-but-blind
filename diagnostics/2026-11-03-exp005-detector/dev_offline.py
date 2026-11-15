"""EXPLORATORY development on results already seen. Nothing here is a held-out claim.
Question: on saved batch-level, label-free features, does any detector beat the twin at matched false alarms when moved to a new model, corruption or dataset?
Alarm margin is calibrated on separate training groups to 5% false alarms on safe streams, for every detector alike. Labels are used for fitting and scoring only."""
import glob, json, os, warnings
import numpy as np, lightgbm as lgb
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
warnings.filterwarnings("ignore")
ROOT = ".."
FA_TARGET, STEP, MIN_T = .05, 5, 10

def load():
    S = []
    for d in sorted(glob.glob(f"{ROOT}/2026-11-02-exp004-twin/results_twin_*")):
        c = json.load(open(d + "/calibration.json"))
        for l in open(d + "/streams.jsonl"):
            r = json.loads(l)
            S.append(dict(ds="cifar", model=c["model"], cor=r["corruption"], sev=r["severity"], key=r["key"], C=np.array(r["cells"]), pos=np.array(r["tent_fixed"]), conf=np.array(r["conf"]), conft=np.array(r["conf_twin"]), r0=c["r0"], rt=c["r_twin"], fp=c["fp_twin"], fn=c["fn_twin"], k=100))
    for arm in ("tent1e-3", "tent5e-3"):
        c = json.load(open(f"{ROOT}/2026-11-02-exp004-derma/results/calibration_{arm}.json"))
        for l in open(f"{ROOT}/2026-11-02-exp004-derma/results/{arm}.jsonl"):
            r = json.loads(l)
            S.append(dict(ds="derma", model="derma_" + arm, cor=r["corruption"], sev=r["severity"], key=r["key"], C=np.array(r["cells"]), pos=np.array(r["pos"]), conf=np.array(r["conf"]), conft=np.array(r["conf_twin"]), r0=c["r0"], rt=c["r_twin"], fp=c["fpt"], fn=c["fnt"], k=7))
    for s in S:
        C = s["C"]; e = C[4:8].sum(0); s["e"] = e; m = e.mean(); last = e[-len(e)//4:].mean()
        s["strict"] = m >= s["r0"] + .15 and last < .85
        s["safe"] = m < s["r0"] + .10 and last < .85
        s["FA"], s["Fa"], s["fA"], s["fa"] = C[3] + C[7], C[2] + C[6], C[1] + C[5], C[0] + C[4]
    return S

NAMES = "F_agree F_dis f_agree f_dis conf conf_twin flagged gap kl_proxy recent_gap recent_dis recent_conf r0 r_twin fp fn logt logk".split()
def feats(s):
    T = len(s["e"]); n = np.arange(1, T + 1)
    cm = lambda x: np.cumsum(x) / n
    a = [cm(s[k]) for k in ("FA", "Fa", "fA", "fa")] + [cm(s["conf"]), cm(s["conft"]), cm(s["pos"])]
    gap = s["conf"] - s["conft"]; a.append(cm(gap)); a.append(cm(np.maximum(gap, 0)))
    rec = lambda x: np.array([x[max(0, t - 9):t + 1].mean() for t in range(T)])
    a += [rec(gap), rec(s["Fa"] + s["fa"]), rec(s["conf"])]
    a += [np.full(T, s[k]) for k in ("r0", "rt", "fp", "fn")] + [np.log(n), np.full(T, np.log(s["k"]))]
    return np.stack(a, 1), cm(s["e"]) - s["r0"]

class Rule:
    def __init__(s, f): s.f = f
    def fit(s, X, y): return s
    def predict(s, X): return s.f(X)
ix = {n: i for i, n in enumerate(NAMES)}
def gbm(): return lgb.LGBMRegressor(n_estimators=250, learning_rate=.05, num_leaves=15, min_child_samples=40, subsample=.8, subsample_freq=1, colsample_bytree=.8, verbose=-1, n_jobs=4)
class Stack:
    def __init__(s): s.a, s.b = make_pipeline(StandardScaler(), Ridge(3.)), gbm()
    def fit(s, X, y):
        s.a.fit(X, y); s.b.fit(X, y - s.a.predict(X)); return s
    def predict(s, X): return s.a.predict(X) + s.b.predict(X)
L = lambda X: X[:, ix["fp"]] + X[:, ix["fn"]]
DET = dict(
    released=lambda: Rule(lambda X: X[:, ix["flagged"]] - X[:, ix["r0"]]),
    twin_bound=lambda: Rule(lambda X: X[:, ix["F_agree"]] + X[:, ix["F_dis"]] + X[:, ix["f_dis"]] - L(X) - X[:, ix["r0"]]),
    twin_raw=lambda: Rule(lambda X: X[:, ix["F_agree"]] + X[:, ix["F_dis"]] + X[:, ix["f_dis"]] - X[:, ix["r_twin"]]),
    conf_gap=lambda: Rule(lambda X: X[:, ix["gap"]]),
    gap_plus_twin=lambda: Rule(lambda X: X[:, ix["gap"]] + X[:, ix["F_agree"]] + X[:, ix["F_dis"]] + X[:, ix["f_dis"]] - X[:, ix["r_twin"]]),
    ridge=lambda: make_pipeline(StandardScaler(), Ridge(3.)),
    lgbm=gbm,
    stack=Stack)

def score(mod, S, cache):
    out = []
    for s in S:
        X, _ = cache[id(s)]
        t = np.arange(MIN_T, len(X), STEP)
        out.append((t, mod.predict(X[t])))
    return out

def run(S, train, test):
    groups = sorted({(s["model"], s["cor"]) for s in train})
    rng = np.random.default_rng(0); rng.shuffle(groups)
    cg = set(map(tuple, groups[:len(groups) // 3]))
    fit = [s for s in train if (s["model"], s["cor"]) not in cg]; cal = [s for s in train if (s["model"], s["cor"]) in cg and s["safe"]]
    cache = {id(s): feats(s) for s in train + test}
    Xf = np.concatenate([cache[id(s)][0][MIN_T::STEP] for s in fit]); yf = np.concatenate([cache[id(s)][1][MIN_T::STEP] for s in fit])
    res = {}
    for name, mk in DET.items():
        m = mk().fit(Xf, yf)
        mx = [p.max() for _, p in score(m, cal, cache)]
        thr = np.quantile(mx, 1 - FA_TARGET) if mx else np.inf
        rows = []
        for s, (t, p) in zip(test, score(m, test, cache)):
            hit = np.where(p > thr)[0]
            rows.append(dict(strict=bool(s["strict"]), safe=bool(s["safe"]), alarm=bool(len(hit)), first=int(t[hit[0]]) if len(hit) else None, top=float(p.max()), model=s["model"], cor=s["cor"]))
        res[name] = rows
    return res

def agg(all_rows):
    o = {}
    for n in DET:
        R = [r for rs in all_rows for r in rs[n]]
        st, sf = [r for r in R if r["strict"]], [r for r in R if r["safe"]]
        mi, fa = sum(not r["alarm"] for r in st), sum(r["alarm"] for r in sf)
        y = np.array([1] * len(st) + [0] * len(sf)); z = np.array([r["top"] for r in st] + [r["top"] for r in sf])
        auc = np.mean(z[y == 1][:, None] > z[y == 0][None, :]) if len(st) and len(sf) else float("nan")
        o[n] = dict(missed=[mi, len(st)], false_alarm=[fa, len(sf)], pooled_auroc=round(float(auc), 3), median_first=float(np.median([r["first"] for r in st if r["alarm"]] or [np.nan])))
    return o

if __name__ == "__main__":
    S = load()
    print(len(S), "streams", {d: (sum(s["ds"] == d and s["strict"] for s in S), sum(s["ds"] == d and s["safe"] for s in S)) for d in ("cifar", "derma")}, flush=True)
    C, D = [s for s in S if s["ds"] == "cifar"], [s for s in S if s["ds"] == "derma"]
    rep = {}
    rep["cifar_to_derma"] = agg([run(S, C, D)])
    rep["derma_to_cifar"] = agg([run(S, D, C)])
    print("cross done", flush=True)
    rep["cifar_leave_model_out"] = agg([run(S, [s for s in C if s["model"] != m], [s for s in C if s["model"] == m]) for m in sorted({s["model"] for s in C})])
    rep["cifar_leave_corruption_out"] = agg([run(S, [s for s in C if s["cor"] != c], [s for s in C if s["cor"] == c]) for c in sorted({s["cor"] for s in C})])
    rep["derma_leave_corruption_out"] = agg([run(S, [s for s in D if s["cor"] != c], [s for s in D if s["cor"] == c]) for c in sorted({s["cor"] for s in D})])
    m = lgb.LGBMRegressor(n_estimators=250, learning_rate=.05, num_leaves=15, verbose=-1, importance_type="gain").fit(*[np.concatenate(x) for x in zip(*[(feats(s)[0][10::5], feats(s)[1][10::5]) for s in S])])
    rep["gain"] = dict(sorted(zip(NAMES, (m.feature_importances_ / m.feature_importances_.sum()).round(3).tolist()), key=lambda x: -x[1]))
    json.dump(rep, open("dev_offline.json", "w"), indent=1)
    for k, v in rep.items():
        print("\n" + k)
        if k == "gain": print(v); continue
        for n, r in v.items(): print(f"  {n:14s} missed {r['missed'][0]:3d}/{r['missed'][1]:<3d} FA {r['false_alarm'][0]:3d}/{r['false_alarm'][1]:<3d} AUROC {r['pooled_auroc']:.3f} first {r['median_first']}")

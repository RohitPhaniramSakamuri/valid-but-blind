"""exp008 analysis, frozen with experiments/008 before any exp008 stream ran.
Every detector's level is set on development streams of the same (dataset, checkpoint, arm) only; held-out streams are scored once.
Signals x calibrations, plus the published monitor and the earlier twin bound (confidence sequences). Verdict uses relative criteria at matched false-alarm rates."""
import glob, json, math, os, sys
from multiprocessing import Pool
import numpy as np
import lightgbm as lgb
from scipy.optimize import nnls
from sklearn.ensemble import IsolationForest

OUT = os.environ["OUT"]; IDX = np.arange(10, 120, 5); ALPHA = .05; TOL = .10
C_ALPHA, C_AL1 = .15, .025
IMGF = [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 16]  # per-image label-free features
cum = lambda x: np.cumsum(x, 0) / np.arange(1, len(x) + 1).reshape(-1, *([1] * (np.ndim(x) - 1)))


def conformal(v, alpha=ALPHA):
    v = np.sort(np.asarray(v, dtype=float)); n = len(v); k = math.ceil((n + 1) * (1 - alpha))
    return float(v[k - 1]) if 0 < k <= n else float("inf")


def first_cs(z, L, level):
    from confseq.conjmix_bounded import conjmix_empbern_lower_cs
    from confseq.predmix import predmix_empbern_lower_cs
    x = np.clip(np.asarray(z, dtype=float), 0, 1); t = int(len(x) * .25)
    m = np.cumsum(x) / np.arange(1, len(x) + 1); v = np.cumsum((x - np.append(.5, m[:-1])) ** 2)[t] * t
    try: cs = np.asarray(conjmix_empbern_lower_cs(x=x, alpha=C_ALPHA, v_opt=v))
    except Exception: cs = np.asarray(predmix_empbern_lower_cs(x=x, alpha=C_ALPHA))
    h = np.where(np.maximum(cs - L, 0) > level)[0]; return int(h[0]) + 1 if len(h) else None


def load(p):
    d = os.path.dirname(p); c = json.load(open(d + "/calibration.json")); split, cor, sev, pr, rep = os.path.basename(p)[:-4].split("__")
    I = np.load(p)["img"].astype(np.float32); E = I[:, :, 17] > .5; F = I[:, :, 23] > .5; A = I[:, :, 8] > .5
    tw, ts, ws = A, I[:, :, 9] > .5, I[:, :, 10] > .5
    P = [tw & ts, tw & ~ts, ts & ~tw, ws & ~tw, ~tw & ~ts & ~ws]
    X = np.stack([(q & f).mean(1) for q in P for f in (F, ~F)], 1)
    flag = (F | ~A).mean(1); e = I[:, :, 17].mean(1); m, l = e.mean(), e[-30:].mean()
    K = c["K"]
    if I.shape[2] > 24: yW = I[:, :, 24].astype(int); hist = np.stack([np.bincount(r, minlength=K) for r in yW]).astype(np.float32) / I.shape[1]
    else: hist = np.stack([np.bincount(r, minlength=K) for r in I[:, :, 20].astype(int)]).astype(np.float32) / I.shape[1]
    b = dict(flag=flag, errT=e, rel=I[:, :, 21].mean(1), pro=I[:, :, 22].mean(1), atc=(I[:, :, 0] < c["t_atc"]).mean(1), confT=I[:, :, 0].mean(1), dd=I[:, :, 16].mean(1),
             confW=I[:, :, 1].mean(1), confS=I[:, :, 2].mean(1), agTS=I[:, :, 9].mean(1), agTW=I[:, :, 8].mean(1), kl=I[:, :, 11].mean(1), entT=I[:, :, 5].mean(1), entW=I[:, :, 6].mean(1))
    w = (math.log(2) - math.log(C_AL1)) / (2 * c["n"]); lv = c["r0"] + TOL
    FA, nFnA = (F & A).mean(1), (~F & ~A).mean(1)
    cs = dict(published=first_cs(b["rel"], c["fp0"] + w, lv), twin_bound=first_cs(flag, c["fpt"] + c["fnt"] + w, lv))
    return dict(key=p, ds=c["ds"], model=c["model"], arm=c["arm"], split=split, cor=cor, sev=int(sev), prior=pr, c=c, err=float(m),
                strict=bool(m >= c["r0"] + .15 and l < .85), safe=bool(m < c["r0"] + TOL and l < .85), collapsed=bool(l >= .85),
                b=b, X=X.astype(np.float32), hist=hist, cs=cs, img=I[:, :, IMGF].astype(np.float16))


BF = ["flag", "atc", "dd", "confT", "confW", "confS", "agTS", "agTW", "kl", "entT", "entW"]
def batch_feats(s): return np.hstack((np.stack([s["b"][k] for k in BF], 1), s["X"]))  # (120, 21)
def stream_feats(s): return np.hstack((cum(batch_feats(s)), np.log(np.arange(1, 121))[:, None]))[IDX]  # (22, 22)


# ---------- signals: each returns per-checkpoint scores (len(IDX)); fitted ones get (fit_streams) ----------
def sig_simple(name):
    def f(s, ctx):
        b, c = s["b"], s["c"]
        return dict(twin=cum(b["flag"]) - c["r_twin"], released=cum(b["rel"]) - c["r0"], prototype=cum(b["pro"]) - c["r0"], atc=cum(b["atc"]) - c["r0"],
                    doc=c["conf_clean"] - cum(b["confT"]), dropout=cum(b["dd"]))[name][IDX]
    return f
def fit_pattern(dev):
    return nnls(np.vstack([s["X"] for s in dev]).astype(float), np.concatenate([s["b"]["errT"] for s in dev]).astype(float))[0]
def sig_pattern(s, ctx): return (cum(s["X"] @ ctx["w"]) - s["c"]["r0"])[IDX]
MONO = [1, 1, 1, -1, -1, 0, -1, -1, 1, 1, 1] + [0] * 10 + [0]
def fit_lgbm(dev):
    X = np.vstack([stream_feats(s) for s in dev]); y = np.concatenate([(cum(s["b"]["errT"]) - s["c"]["r0"])[IDX] for s in dev])
    return lgb.LGBMRegressor(n_estimators=250, learning_rate=.05, num_leaves=15, min_child_samples=40, subsample=.8, subsample_freq=1, colsample_bytree=.8, monotone_constraints=MONO, verbose=-1, n_jobs=4, random_state=0).fit(X, y)
def sig_lgbm(s, ctx): return ctx["lgbm"].predict(stream_feats(s))
def fit_if_stream(dev):
    safe = [s for s in dev if s["safe"]]; return IsolationForest(n_estimators=200, random_state=0, n_jobs=4).fit(np.vstack([stream_feats(s) for s in safe]))
def sig_if_stream(s, ctx): return -ctx["ifs"].score_samples(stream_feats(s))
def fit_if_batch(dev):
    safe = [s for s in dev if s["safe"]]; return IsolationForest(n_estimators=200, random_state=0, n_jobs=4).fit(np.vstack([batch_feats(s) for s in safe]))
def sig_if_batch(s, ctx): return cum(-ctx["ifb"].score_samples(batch_feats(s)))[IDX]
def fit_if_image(dev):
    safe = [s for s in dev if s["safe"]]; rng = np.random.default_rng(0)
    X = np.vstack([s["img"].reshape(-1, len(IMGF)) for s in safe]).astype(np.float32); X = X[rng.choice(len(X), min(30000, len(X)), replace=False)]
    m = IsolationForest(n_estimators=200, random_state=0, n_jobs=4).fit(X); return m, float(np.quantile(-m.score_samples(X), .95))
def sig_if_image(s, ctx):
    m, q = ctx["ifi"]; a = -m.score_samples(s["img"].reshape(-1, len(IMGF)).astype(np.float32)).reshape(120, -1)
    return cum((a > q).mean(1))[IDX]
def ref_batches(dev): return np.sort(np.concatenate([s["b"]["flag"] for s in dev if s["safe"]]))
def sig_dominance(s, ctx):
    r = ctx["ref"]; F = np.searchsorted(r, s["b"]["flag"], side="left") / len(r); return cum(F)[IDX] - .5
def sig_martingale(s, ctx):
    r = ctx["ref"]; p = (1 + len(r) - np.searchsorted(r, s["b"]["flag"], side="left")) / (len(r) + 1)
    k = np.array([.25, .5, .75]); lm = np.cumsum(np.log(np.mean(k[None] * p[:, None] ** (k[None] - 1), 1))); return lm[IDX]

FITTERS = dict(pattern=("w", fit_pattern), lgbm_mono=("lgbm", fit_lgbm), if_stream=("ifs", fit_if_stream), if_batch=("ifb", fit_if_batch), if_image=("ifi", fit_if_image),
               dominance=("ref", ref_batches), martingale=("ref", ref_batches))
SIGNALS = dict(twin=sig_simple("twin"), released=sig_simple("released"), prototype=sig_simple("prototype"), atc=sig_simple("atc"), doc=sig_simple("doc"),
               dropout=sig_simple("dropout"), pattern=sig_pattern, lgbm_mono=sig_lgbm, if_stream=sig_if_stream, if_batch=sig_if_batch, if_image=sig_if_image,
               dominance=sig_dominance, martingale=sig_martingale)
COMBOS = dict(twin_pattern=("twin", "pattern"), fusion=("twin", "atc", "dropout"))


def group_scores(dev, held):
    """Out-of-fold dev scores (by dev corruption) and held scores for every signal and combination."""
    cors = sorted({s["cor"] for s in dev}); oof = {n: {} for n in SIGNALS}; hs = {n: {} for n in SIGNALS}
    full = {k: fn(dev) for k, fn in FITTERS.values()}
    for n, f in SIGNALS.items():
        if n in FITTERS:
            k, fn = FITTERS[n]
            for c in cors:
                tr = [s for s in dev if s["cor"] != c]
                if not any(s["safe"] for s in tr): continue
                ctx = {k: fn(tr)}
                for s in dev:
                    if s["cor"] == c: oof[n][id(s)] = f(s, ctx)
            for s in held: hs[n][id(s)] = f(s, {k: full[k]})
        else:
            for s in dev: oof[n][id(s)] = f(s, {})
            for s in held: hs[n][id(s)] = f(s, {})
    dsafe = [s for s in dev if s["safe"] and id(s) in oof["pattern"]]
    for cname, parts in COMBOS.items():
        Z = np.stack([np.stack([oof[p][id(s)] for p in parts], 1) for s in dsafe]); med = np.median(Z, 0); sp = np.quantile(Z, .9, 0) - np.quantile(Z, .1, 0) + 1e-6
        oof[cname] = {id(s): ((np.stack([oof[p][id(s)] for p in parts], 1) - med) / sp).mean(1) for s in dev if all(id(s) in oof[p] for p in parts)}
        hs[cname] = {id(s): ((np.stack([hs[p][id(s)] for p in parts], 1) - med) / sp).mean(1) for s in held}
    return oof, hs


def descriptor(s, ref_hist):
    h = s["hist"][:IDX[0] + 1].mean(0); return float(np.abs(h - ref_hist).sum() / 2)


def calibrate(dev, held, oof, hs):
    """Three calibrations per signal: G global conformal, M Mondrian by early class-skew descriptor (2 bins), Z per-checkpoint standardised."""
    dsafe = [s for s in dev if s["safe"]]
    nat = [s for s in dev if s["cor"] == "clean" and s["prior"] == "natural"] or dev
    ref_hist = np.mean([s["hist"].mean(0) for s in nat], 0)
    dd = {id(s): descriptor(s, ref_hist) for s in dev + held}
    cut = float(np.median([dd[id(s)] for s in dsafe])) if dsafe else 0.
    res = {}
    for n in oof:
        sd = [s for s in dsafe if id(s) in oof[n]]
        if len(sd) < 19: continue
        g = conformal([oof[n][id(s)].max() for s in sd])
        mb = {}
        for bin_ in (0, 1):
            v = [oof[n][id(s)].max() for s in sd if (dd[id(s)] > cut) == bool(bin_)]
            mb[bin_] = conformal(v) if len(v) >= 19 else g
        Z = np.stack([oof[n][id(s)] for s in sd]); med = np.median(Z, 0); sp = np.quantile(Z, .9, 0) - np.quantile(Z, .1, 0) + 1e-9
        zl = conformal([((oof[n][id(s)] - med) / sp).max() for s in sd])
        for s in held:
            x = hs[n][id(s)]
            res.setdefault(f"{n}|G", {})[id(s)] = x - g
            res.setdefault(f"{n}|M", {})[id(s)] = x - mb[int(dd[id(s)] > cut)]
            res.setdefault(f"{n}|Z", {})[id(s)] = (x - med) / sp - zl
    return res


def main():
    files = sorted(f for f in glob.glob(f"{OUT}/streams/*/*.npz") if not f.endswith(".tmp.npz"))
    with Pool(min(os.cpu_count(), 24)) as pool: S = pool.map(load, files, chunksize=8)
    print(len(S), "streams", flush=True)
    G = sorted({(s["ds"], s["model"], s["arm"]) for s in S}); rows = []
    for g in G:
        dev = [s for s in S if (s["ds"], s["model"], s["arm"]) == g and s["split"] == "dev"]; held = [s for s in S if (s["ds"], s["model"], s["arm"]) == g and s["split"] == "held"]
        if not dev or not held: continue
        oof, hs = group_scores(dev, held); cal = calibrate(dev, held, oof, hs)
        for s in held:
            r = dict(g="/".join(g), ds=g[0], model=g[1], arm=g[2], cor=s["cor"], sev=s["sev"], prior=s["prior"], strict=s["strict"], safe=s["safe"], err=s["err"], top={})
            for k, v in cal.items():
                if id(s) in v: r["top"][k] = float(v[id(s)].max())
            r["top"]["published|CS"] = 1. if s["cs"]["published"] else -1.; r["top"]["twin_bound|CS"] = 1. if s["cs"]["twin_bound"] else -1.
            rows.append(r)
        print("group", g, len(dev), len(held), flush=True)
    json.dump(rows, open(f"{OUT}/rows8.json", "w"))
    report = summarise(rows)
    json.dump(report, open(f"{OUT}/report8.json", "w"), indent=1)
    print(json.dumps({k: report[k] for k in ("VERDICT", "criteria", "counts")}, indent=1))
    for k, v in sorted(report["deployed_primary"].items(), key=lambda kv: kv[1]["missed_share"]): print(f"  {k:24s} missed {v['missed']} FA {v['false_alarm']} matched5 {report['matched_primary'].get(k.split('|')[0], {}).get('0.05', '-')}")


def share(x): return x[0] / x[1] if x[1] else float("nan")


def deployed(R, det):
    st, sf = [r for r in R if r["strict"] and det in r["top"]], [r for r in R if r["safe"] and det in r["top"]]
    m, f = [sum(r["top"][det] <= 0 for r in st), len(st)], [sum(r["top"][det] > 0 for r in sf), len(sf)]
    return dict(missed=m, false_alarm=f, missed_share=share(m), fa_share=share(f))


def matched(R, det, fa):
    m = [0, 0]
    for g in sorted({r["g"] for r in R}):
        sf = np.array([r["top"][det] for r in R if r["g"] == g and r["safe"] and det in r["top"]]); st = np.array([r["top"][det] for r in R if r["g"] == g and r["strict"] and det in r["top"]])
        if not len(st): continue
        t = np.quantile(sf, 1 - fa) if len(sf) else np.inf; m[0] += int((st <= t).sum()); m[1] += len(st)
    return share(m)


def summarise(rows):
    P = [r for r in rows if r["arm"] == "tent0.001"]; dets = sorted({k for r in rows for k in r["top"]})
    rep = dict(counts=dict(strict=sum(r["strict"] for r in P), safe=sum(r["safe"] for r in P), by_ds={d: dict(strict=sum(r["strict"] for r in P if r["ds"] == d), safe=sum(r["safe"] for r in P if r["ds"] == d)) for d in sorted({r["ds"] for r in P})}))
    rep["deployed_primary"] = {d: deployed(P, d) for d in dets}
    rep["deployed_all_arms"] = {d: deployed(rows, d) for d in dets}
    rep["deployed_by_ds"] = {ds: {d: deployed([r for r in P if r["ds"] == ds], d) for d in dets} for ds in sorted({r["ds"] for r in P})}
    sigs = sorted({d.split("|")[0] for d in dets if d.endswith("|G")})
    rep["matched_primary"] = {s: {str(fa): matched(P, f"{s}|G", fa) for fa in (.03, .05, .07)} for s in sigs}
    # frozen verdict (experiments/008)
    tp, rel = rep["matched_primary"].get("twin_pattern", {}).get("0.05", np.nan), rep["matched_primary"].get("released", {}).get("0.05", np.nan)
    dp, pub = rep["deployed_primary"].get("twin_pattern|G"), rep["deployed_primary"].get("published|CS")
    c1 = bool(tp <= .6 * rel)
    per = [rep["deployed_by_ds"][ds].get("twin_pattern|G") for ds in rep["deployed_by_ds"]]
    c2_pool = bool(dp["fa_share"] <= .10); c2_each = all(x["false_alarm"][1] == 0 or x["fa_share"] <= .15 for x in per)
    c3 = bool(dp["missed_share"] <= .20 and dp["missed_share"] <= .6 * pub["missed_share"])
    nonworse = bool(rep["matched_primary"]["twin_pattern"]["0.05"] <= 1.25 * rep["matched_primary"]["atc"]["0.05"])
    if rep["counts"]["strict"] < 80 or rep["counts"]["safe"] < 120: v = "INCONCLUSIVE"
    elif c1 and c2_pool and c2_each and c3: v = "CONFIRMED"
    elif c1 and c3 and (sum(not (x["false_alarm"][1] == 0 or x["fa_share"] <= .15) for x in per) <= 1) and dp["fa_share"] <= .15: v = "PARTIAL"
    else: v = "NOT CONFIRMED"
    rep["criteria"] = dict(C1_matched5_tp=tp, C1_matched5_released=rel, C1=c1, C2_pooled_fa=dp["fa_share"], C2_pooled=c2_pool, C2_each=c2_each,
                           C3_missed=dp["missed_share"], C3_published_missed=pub["missed_share"], C3=c3, secondary_noninferior_to_ATC=nonworse)
    rep["VERDICT"] = v
    return rep


if __name__ == "__main__":
    main()

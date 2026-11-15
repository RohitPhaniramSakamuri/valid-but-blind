"""exp010 analysis, frozen with experiments/010 before any exp010 stream ran.
Usage: OUT=<dir with streams/<ds>__<model>__<arm>/*.npz> [PRIMARY_ARM=tent0.001] python analyze10.py [--no-lgbm]
Every level and every choice is made on development streams of the same (dataset, checkpoint, arm) only; held-out streams are scored once.

PRIMARY detector, "FV" (family-validated alarm):
  candidates, in tie-break order:
    twin|G  decoupled channel: running share of images where the entropy-free twin is uncertain or disagrees with the adapted model, minus the twin's clean error; one constant level.
    doc|Z   coupled channel read in the loop: clean source confidence minus the adapted model's running confidence, standardised at every read-out time by the safe development streams (median and 10-90 spread at that time); level on the maximum.
    fus3|G  mean of the time-standardised twin, ATC and dropout-disagreement scores (the exp008 "fusion" detector, unchanged); level on the maximum.
  levels: the split-conformal rank at alpha = 0.05 on safe development streams. Because the time standardisation and the choice below use the same
          development streams, no coverage guarantee is claimed; realised false alarms are a criterion (C2, C4).
  choice: leave-one-development-family-out (LOFO). For each family, levels are set on the other families' safe streams and the left-out family is scored.
          The candidate with the smallest (LOFO missed share + LOFO false-alarm share) is deployed, with its level reset on all safe development streams.
  audit:  the chosen candidate's LOFO missed share is reported before deployment; a deployment is flagged "weak" when it exceeds 0.25 (with at least 10 LOFO failing streams).
"""
import glob, json, math, os, sys
from multiprocessing import Pool
import numpy as np

OUT = os.environ["OUT"]; PRIMARY_ARM = os.environ.get("PRIMARY_ARM", "tent0.001"); IDX = np.arange(10, 120, 5); ALPHA = .05; TOL = .10
C_ALPHA, C_AL1 = .15, .025; WEAK = .25; NO_LGBM = "--no-lgbm" in sys.argv
cum = lambda x: np.cumsum(x, 0) / np.arange(1, len(x) + 1).reshape(-1, *([1] * (np.ndim(x) - 1)))
BASE = ["twin", "doc", "atc", "dropout", "released", "prototype"]; FUS3 = ("twin", "atc", "dropout")
POOL = ["twin|G", "doc|Z", "fus3|G"]  # tie-break order
DETS = [f"{n}|{c}" for n in BASE for c in "GZ"] + ["fus3|G"]


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


def status(e, r0): m, l = float(e.mean()), float(e[-30:].mean()); return dict(err=m, strict=bool(m >= r0 + .15 and l < .85), safe=bool(m < r0 + TOL and l < .85), collapsed=bool(l >= .85))


def load(p):
    d = os.path.dirname(p); c = json.load(open(d + "/calibration.json")); split, cor, sev, pr, rep = os.path.basename(p)[:-4].split("__")
    if "model" not in c: c["model"] = c["ds"]; c["arm"] = f"tent{c['lr']}"
    I = np.load(p)["img"].astype(np.float32); F = I[:, :, 23] > .5; A = I[:, :, 8] > .5; ts, ws = I[:, :, 9] > .5, I[:, :, 10] > .5
    P = [A & ts, A & ~ts, ts & ~A, ws & ~A, ~A & ~ts & ~ws]; X = np.stack([(q & f).mean(1) for q in P for f in (F, ~F)], 1)
    ET, EW, ES = I[:, :, 17] > .5, I[:, :, 18] > .5, I[:, :, 19] > .5; FS = (1 - I[:, :, 2]) > c["q0"]; FT = I[:, :, 21] > .5
    flag = (F | ~A).mean(1)
    b = dict(flag=flag, errT=ET.mean(1), rel=FT.mean(1), pro=I[:, :, 22].mean(1), atc=(I[:, :, 0] < c["t_atc"]).mean(1), confT=I[:, :, 0].mean(1), dd=I[:, :, 16].mean(1),
             confW=I[:, :, 1].mean(1), confS=I[:, :, 2].mean(1), agTS=ts.mean(1), agTW=A.mean(1), kl=I[:, :, 11].mean(1), entT=I[:, :, 5].mean(1), entW=I[:, :, 6].mean(1),
             relS=FS.mean(1), relW=F.mean(1), errW=EW.mean(1), errS=ES.mean(1), capT=(FT & ET).mean(1), capW=(F & EW).mean(1), capS=(FS & ES).mean(1))
    w = (math.log(2) - math.log(C_AL1)) / (2 * c["n"])
    cs = dict(published=first_cs(b["rel"], c["fp0"] + w, c["r0"] + TOL), twin_bound=first_cs(flag, c["fpt"] + c["fnt"] + w, c["r0"] + TOL),
              source=first_cs(b["relS"], c["fp0"] + w, c["r0"] + TOL), bn=first_cs(b["relW"], c["fpt"] + w, c["r_twin"] + TOL))
    sT, sW, sS = status(b["errT"], c["r0"]), status(b["errW"], c["r_twin"]), status(b["errS"], c["r0"])
    return dict(key=os.path.basename(p)[:-4], ds=c["ds"], model=c["model"], arm=c["arm"], split=split, cor=cor, sev=int(sev), prior=pr, c=c, **sT, W=sW, S=sS,
                b={k: v.astype(np.float32) for k, v in b.items()}, X=X.astype(np.float32), cs=cs)


def base_scores(s):
    b, c = s["b"], s["c"]
    return np.stack([cum(b["flag"]) - c["r_twin"], c["conf_clean"] - cum(b["confT"]), cum(b["atc"]) - c["r0"], cum(b["dd"]), cum(b["rel"]) - c["r0"], cum(b["pro"]) - c["r0"]])[:, IDX]


def stat(A, ref, det):
    """A: (n, signal, time) base scores; ref: indices of safe calibration streams. Returns each stream's maximum statistic minus the conformal level (> 0 alarms)."""
    name, cal = det.split("|"); R = A[ref]; med = np.median(R, 0); sp = np.quantile(R, .9, 0) - np.quantile(R, .1, 0) + 1e-6; Zs = (A - med) / sp
    if name == "fus3": x = Zs[:, [BASE.index(p) for p in FUS3]].mean(1)
    else: x = (Zs if cal == "Z" else A)[:, BASE.index(name)]
    m = x.max(1); return m - conformal(m[ref])


# ---- comparator kept from exp008 (exploratory there): monotone LightGBM on running signals, per-time standardised (Z) ----
BF = ["flag", "atc", "dd", "confT", "confW", "confS", "agTS", "agTW", "kl", "entT", "entW"]; MONO = [1, 1, 1, -1, -1, 0, -1, -1, 1, 1, 1] + [0] * 10 + [0]
def stream_feats(s): return np.hstack((cum(np.hstack((np.stack([s["b"][k] for k in BF], 1), s["X"]))), np.log(np.arange(1, 121))[:, None]))[IDX]
def fit_lgbm(dev):
    import lightgbm as lgb
    X = np.vstack([stream_feats(s) for s in dev]); y = np.concatenate([(cum(s["b"]["errT"]) - s["c"]["r0"])[IDX] for s in dev])
    return lgb.LGBMRegressor(n_estimators=250, learning_rate=.05, num_leaves=15, min_child_samples=40, subsample=.8, subsample_freq=1, colsample_bytree=.8, monotone_constraints=MONO, verbose=-1, n_jobs=4, random_state=0).fit(X, y)
def lgbm_z(dev, held):
    cors = sorted({s["cor"] for s in dev}); oof = {}
    for c in cors:
        tr = [s for s in dev if s["cor"] != c]; m = fit_lgbm(tr)
        for s in dev:
            if s["cor"] == c: oof[id(s)] = m.predict(stream_feats(s))
    sd = [s for s in dev if s["safe"]]; Z = np.stack([oof[id(s)] for s in sd]); med = np.median(Z, 0); sp = np.quantile(Z, .9, 0) - np.quantile(Z, .1, 0) + 1e-9
    zl = conformal([((oof[id(s)] - med) / sp).max() for s in sd]); full = fit_lgbm(dev)
    return [float((((full.predict(stream_feats(s)) - med) / sp) - zl).max()) for s in held]


def analyse_group(L):
    dev = [s for s in L if s["split"] == "dev"]; held = [s for s in L if s["split"] == "held"]; S = dev + held
    A = np.stack([base_scores(s) for s in S]); isdev = np.arange(len(S)) < len(dev); safe = np.array([s["safe"] for s in S]); strict = np.array([s["strict"] for s in S]); cor = np.array([s["cor"] for s in S])
    ref_all = np.where(isdev & safe)[0]
    if len(ref_all) < 19:  # cannot be calibrated: every dev-calibrated detector abstains (never alarms) and the setting stays in all denominators
        rows = []
        for s in held:
            r = dict(g="/".join((s["ds"], s["model"], s["arm"])), ds=s["ds"], model=s["model"], arm=s["arm"], key=s["key"], cor=s["cor"], sev=s["sev"], prior=s["prior"], strict=s["strict"], safe=s["safe"], err=s["err"], weak=True, pick="abstain",
                     top={k: -1. for k in DETS + ["FV", "FV2", "lgbm_mono|Z"]}, S=s["S"], W=s["W"], cs={k: bool(v) for k, v in s["cs"].items()})
            r["top"]["published|CS"] = 1. if s["cs"]["published"] else -1.; r["top"]["twin_bound|CS"] = 1. if s["cs"]["twin_bound"] else -1.
            r["win"] = {k: [float(s["b"][k][j:j + 20].mean()) for j in range(0, 120, 20)] for k in ("confT", "confW", "confS", "errT", "errW", "errS", "rel", "relW", "relS", "capT", "capW", "capS", "flag")}
            rows.append(r)
        return rows, dict(pick="abstain", pick2="abstain", lofo={}, n_safe_dev=int(len(ref_all)), n_strict_dev=int((isdev & strict).sum()), n_fam=len(set(cor[isdev])), weak=True, abstained=True)
    lofo = {}
    for det in DETS:
        fa = [0, 0]; mi = [0, 0]
        for c in sorted(set(cor[isdev])):
            ref = np.where(isdev & safe & (cor != c))[0]; te = isdev & (cor == c)
            if len(ref) < 19: continue
            d = stat(A, ref, det); fa[0] += int((d[te & safe] > 0).sum()); fa[1] += int((te & safe).sum()); mi[0] += int((d[te & strict] <= 0).sum()); mi[1] += int((te & strict).sum())
        lofo[det] = dict(fa=fa, miss=mi, crit=mi[0] / max(1, mi[1]) + fa[0] / max(1, fa[1]))
    pick = min(POOL, key=lambda d: (lofo[d]["crit"], POOL.index(d))); pick2 = min(POOL[:2], key=lambda d: (lofo[d]["crit"], POOL.index(d)))
    top = {det: stat(A, ref_all, det)[~isdev] for det in DETS}; top["FV"] = top[pick]; top["FV2"] = top[pick2]
    if not NO_LGBM:
        try: top["lgbm_mono|Z"] = np.array(lgbm_z(dev, held))
        except Exception as e: print("lgbm failed", L[0]["ds"], L[0]["model"], e, flush=True)
    audit = dict(pick=pick, pick2=pick2, lofo=lofo, n_safe_dev=int(len(ref_all)), n_strict_dev=int((isdev & strict).sum()), n_fam=len(set(cor[isdev])),
                 weak=bool(lofo[pick]["miss"][1] >= 10 and lofo[pick]["miss"][0] / lofo[pick]["miss"][1] > WEAK))
    rows = []
    for i, s in enumerate(held):
        r = dict(g="/".join((s["ds"], s["model"], s["arm"])), ds=s["ds"], model=s["model"], arm=s["arm"], key=s["key"], cor=s["cor"], sev=s["sev"], prior=s["prior"], strict=s["strict"], safe=s["safe"], err=s["err"], weak=audit["weak"], pick=pick,
                 top={k: float(v[i]) for k, v in top.items()}, S=s["S"], W=s["W"], cs={k: bool(v) for k, v in s["cs"].items()})
        r["top"]["published|CS"] = 1. if s["cs"]["published"] else -1.; r["top"]["twin_bound|CS"] = 1. if s["cs"]["twin_bound"] else -1.
        # time-resolved separation inputs: window means (6 windows of 20 batches) of each model's confidence deficit and error capture
        r["win"] = {k: [float(s["b"][k][j:j + 20].mean()) for j in range(0, 120, 20)] for k in ("confT", "confW", "confS", "errT", "errW", "errS", "rel", "relW", "relS", "capT", "capW", "capS", "flag")}
        rows.append(r)
    return rows, audit


share = lambda x: x[0] / x[1] if x[1] else float("nan")
def deployed(R, det):
    st, sf = [r for r in R if r["strict"] and det in r["top"]], [r for r in R if r["safe"] and det in r["top"]]
    m, f = [sum(r["top"][det] <= 0 for r in st), len(st)], [sum(r["top"][det] > 0 for r in sf), len(sf)]
    return dict(missed=m, false_alarm=f, missed_share=share(m), fa_share=share(f))
MIN_SAFE_MATCHED = 10
def matched_full(R, det, fa):
    """Hindsight comparison: per-setting threshold at the (1 - fa) quantile of that setting's held safe streams. Settings with fewer than 10 held safe streams are left out (for every detector alike)."""
    m = [0, 0]; a = [0, 0]; left = []
    for g in sorted({r["g"] for r in R}):
        sf = np.array([r["top"][det] for r in R if r["g"] == g and r["safe"] and det in r["top"]]); st = np.array([r["top"][det] for r in R if r["g"] == g and r["strict"] and det in r["top"]])
        if not len(st): continue
        if len(sf) < MIN_SAFE_MATCHED: left.append(g); continue
        t = np.quantile(sf, 1 - fa); m[0] += int((st <= t).sum()); m[1] += len(st); a[0] += int((sf > t).sum()); a[1] += len(sf)
    return dict(missed=m, missed_share=share(m), achieved_fa=share(a), left_out=left)
def matched(R, det, fa): return matched_full(R, det, fa)["missed_share"]
def auroc(pos, neg):
    pos, neg = np.asarray(pos, float), np.asarray(neg, float)
    return float((pos[:, None] > neg[None]).mean() + .5 * (pos[:, None] == neg[None]).mean()) if len(pos) and len(neg) else float("nan")


def verdict(P):
    """Frozen criteria (experiments/010). P: held rows of the primary arm."""
    dss = sorted({r["ds"] for r in P}); by = {d: [r for r in P if r["ds"] == d] for d in dss}
    fv, pub, tw = deployed(P, "FV"), deployed(P, "published|CS"), deployed(P, "twin|G")
    m_fv, m_rel = matched(P, "FV", .05), matched(P, "released|G", .05)
    c1 = bool(m_fv <= .6 * m_rel)
    c2_pool = bool(fv["fa_share"] <= .10); c2_each = all(deployed(by[d], "FV")["fa_share"] <= .15 for d in dss if deployed(by[d], "FV")["false_alarm"][1] >= 20)
    big = [d for d in dss if deployed(by[d], "FV")["missed"][1] >= 15]
    c3_pool = bool(fv["missed_share"] <= .20 and fv["missed_share"] <= .6 * pub["missed_share"]); c3_each = all(deployed(by[d], "FV")["missed"][0] <= deployed(by[d], "published|CS")["missed"][0] for d in big)
    c4_pool = bool((fv["missed_share"] <= .7 * tw["missed_share"] or fv["missed_share"] <= .05) and fv["fa_share"] <= .075); c4_each = all(deployed(by[d], "FV")["missed"][0] <= deployed(by[d], "twin|G")["missed"][0] + 2 for d in big)
    c2, c3, c4 = c2_pool and c2_each, c3_pool and c3_each, c4_pool and c4_each
    n = dict(strict=sum(r["strict"] for r in P), safe=sum(r["safe"] for r in P))
    v = "INCONCLUSIVE" if n["strict"] < 80 or n["safe"] < 120 else "CONFIRMED" if c1 and c2 and c3 and c4 else "PARTIAL" if c1 and c2 and c3 else "NOT CONFIRMED"
    return dict(VERDICT=v, counts=n, C1=c1, C1_matched5_FV=m_fv, C1_matched5_released=m_rel, C1_detail=dict(FV=matched_full(P, "FV", .05), released=matched_full(P, "released|G", .05)), FV_fa=fv["fa_share"], twinG_fa=tw["fa_share"], C2=c2, C2_pooled_fa=fv["fa_share"], C2_each=c2_each, C3=c3, C3_missed=fv["missed_share"], C3_published=pub["missed_share"], C3_each=c3_each,
                C4=c4, C4_twinG=tw["missed_share"], C4_each=c4_each, per_ds={d: dict(FV=deployed(by[d], "FV"), published=deployed(by[d], "published|CS"), twinG=deployed(by[d], "twin|G")) for d in dss})


def coupling(rows):
    """Frozen generality test G1 and mechanism read-outs, per adaptation objective.
    Monitor = the published monitor (sequential lower bound) applied to each model's own flags. Source and BN-twin outcomes are the same for every arm on a stream, so they are counted once per (dataset, checkpoint, stream)."""
    out = {}; seen = {}
    for r in rows: seen.setdefault((r["ds"], r["model"], r["key"]), r)
    for arm in sorted({r["arm"] for r in rows}):
        R = [r for r in rows if r["arm"] == arm]; gs = sorted({(r["ds"], r["model"]) for r in R}); base = [seen[k] for k in seen if (k[0], k[1]) in gs]
        a = [sum(not r["cs"]["published"] for r in R if r["strict"]), sum(r["strict"] for r in R)]
        s = [sum(not r["cs"]["source"] for r in base if r["S"]["strict"]), sum(r["S"]["strict"] for r in base)]
        w = [sum(not r["cs"]["bn"] for r in base if r["W"]["strict"]), sum(r["W"]["strict"] for r in base)]
        higher = []; higher_bn = []; cap = []
        for g in gs:
            Rg = [r for r in R if (r["ds"], r["model"]) == g]; Bg = [r for r in base if (r["ds"], r["model"]) == g]
            ag = [sum(not r["cs"]["published"] for r in Rg if r["strict"]), sum(r["strict"] for r in Rg)]; sg = [sum(not r["cs"]["source"] for r in Bg if r["S"]["strict"]), sum(r["S"]["strict"] for r in Bg)]
            if ag[1] >= 5 and sg[1] >= 5: higher.append(bool(share(ag) > share(sg)))
            wg = [sum(not r["cs"]["bn"] for r in Bg if r["W"]["strict"]), sum(r["W"]["strict"] for r in Bg)]
            if ag[1] >= 5 and wg[1] >= 5: higher_bn.append(bool(share(ag) > share(wg)))
            st = [r for r in Rg if r["strict"]]; ss = [r for r in Bg if r["S"]["strict"]]
            if len(st) >= 5 and len(ss) >= 5:
                cT = np.mean([np.sum(r["win"]["capT"]) / max(1e-9, np.sum(r["win"]["errT"])) for r in st]); cS = np.mean([np.sum(r["win"]["capS"]) / max(1e-9, np.sum(r["win"]["errS"])) for r in ss]); cap.append((float(cT), float(cS)))
        # time-resolved separation: AUROC of the window confidence deficit between own failing and own safe streams, first vs last window, pooled within group then averaged
        dec = dict(T=[], W=[], S=[])
        for g in gs:
            Rg = [r for r in R if (r["ds"], r["model"]) == g]; Bg = [r for r in base if (r["ds"], r["model"]) == g]
            for tag, Q, st_, cf in (("T", Rg, lambda r: r, "confT"), ("W", Bg, lambda r: r["W"], "confW"), ("S", Bg, lambda r: r["S"], "confS")):
                pos = [r for r in Q if st_(r)["strict"]]; neg = [r for r in Q if st_(r)["safe"]]
                if len(pos) >= 5 and len(neg) >= 5: dec[tag].append([auroc([-r["win"][cf][j] for r in pos], [-r["win"][cf][j] for r in neg]) for j in range(6)])
        cl = sorted({(r["ds"], r["model"], r["cor"]) for r in base}); ci = {c: i for i, c in enumerate(cl)}
        def per_cluster(Q, is_strict, missed):
            M = np.zeros((len(cl), 2))
            for r in Q:
                if is_strict(r): i = ci[(r["ds"], r["model"], r["cor"])]; M[i, 0] += missed(r); M[i, 1] += 1
            return M
        CA = per_cluster(R, lambda r: r["strict"], lambda r: not r["cs"]["published"])
        def contrast(base_, CB):
            """Difference in missed share, arm minus baseline, with a 95% interval from 2,000 resamples of (setting, corruption) clusters. SHOWN if the interval's lower end is above 0."""
            ratio_ = share(a) / share(base_) if base_[1] and share(base_) > 0 else float("nan")
            if a[1] < 20 or base_[1] < 20: return "INCONCLUSIVE", ratio_, [float("nan")] * 3
            rng = np.random.default_rng(0); d = []
            for _ in range(2000):
                k = rng.integers(0, len(cl), len(cl)); x, y = CA[k].sum(0), CB[k].sum(0)
                if x[1] and y[1]: d.append(x[0] / x[1] - y[0] / y[1])
            lo, hi = np.quantile(d, [.025, .975]); diff = share(a) - share(base_)
            return ("SHOWN" if lo > 0 else "NOT SHOWN"), ratio_, [float(diff), float(lo), float(hi)]
        (vs_s, ratio, ci_s), (vs_w, ratio_w, ci_w) = contrast(s, per_cluster(base, lambda r: r["S"]["strict"], lambda r: not r["cs"]["source"])), contrast(w, per_cluster(base, lambda r: r["W"]["strict"], lambda r: not r["cs"]["bn"]))
        maj = "INCONCLUSIVE" if len(higher_bn) < 2 else "SHOWN" if sum(higher_bn) > len(higher_bn) / 2 else "NOT SHOWN"
        parts = (vs_w, maj)  # coupling-specific contrast: adapted model against the BN-only twin; the source contrast is reported as secondary
        dT, dW = (float(np.mean(dec["T"], 0)[0] - np.mean(dec["T"], 0)[-1]), float(np.mean(dec["W"], 0)[0] - np.mean(dec["W"], 0)[-1])) if dec["T"] and dec["W"] else (float("nan"), float("nan"))
        out[arm] = dict(arm_missed=a, source_missed=s, bn_missed=w, ratio=ratio, groups_higher=[int(sum(higher)), len(higher)], capture_arm_vs_source=cap,
                        capture_lower_groups=[int(sum(x < y for x, y in cap)), len(cap)],
                        blind_spot=("NOT SHOWN" if "NOT SHOWN" in parts else "INCONCLUSIVE" if "INCONCLUSIVE" in parts else "SHOWN"), vs_source=vs_s, vs_bn=vs_w, majority=maj, groups_higher_than_bn=[int(sum(higher_bn)), len(higher_bn)], decay_shown=(None if dT != dT else bool(dT - dW >= .10)), ratio_vs_bn=ratio_w, diff_ci_vs_source=ci_s, diff_ci_vs_bn=ci_w,
                        decay=(None if not (dec["T"] and dec["W"] and dec["S"]) else dict(T=float(np.mean(dec["T"], 0)[0] - np.mean(dec["T"], 0)[-1]), W=float(np.mean(dec["W"], 0)[0] - np.mean(dec["W"], 0)[-1]), S=float(np.mean(dec["S"], 0)[0] - np.mean(dec["S"], 0)[-1]))),
                        bn_vs_source_ratio=(share(w) / share(s) if s[1] and share(s) > 0 and w[1] else float("nan")),
                        auroc_by_window={k: (np.mean(v, 0).round(4).tolist() if v else None) for k, v in dec.items()}, n_groups_window={k: len(v) for k, v in dec.items()})
    return out


PLANNED = dict(cifar10=(200, 141), tissue=(200, 117), organs=(200, 117))  # (dev, held) streams per setting in run10.plan(); other datasets (dry runs) are not checked
def completeness(S):
    bad = []
    for g in sorted({(s["ds"], s["model"], s["arm"]) for s in S}):
        if g[0] not in PLANNED: continue
        n = (sum(1 for s in S if (s["ds"], s["model"], s["arm"]) == g and s["split"] == "dev"), sum(1 for s in S if (s["ds"], s["model"], s["arm"]) == g and s["split"] == "held"))
        if n != PLANNED[g[0]]: bad.append(("/".join(g), n, PLANNED[g[0]]))
    return bad


def main():
    files = sorted(f for f in glob.glob(f"{OUT}/streams/*/*.npz") if not f.endswith(".tmp.npz"))
    with Pool(min(os.cpu_count(), 8)) as pool: S = pool.map(load, files, chunksize=8)
    print(len(S), "streams", flush=True)
    G = sorted({(s["ds"], s["model"], s["arm"]) for s in S}); rows = []; audits = {}
    for g in G:
        res = analyse_group([s for s in S if (s["ds"], s["model"], s["arm"]) == g])
        rows += res[0]; audits["/".join(g)] = res[1]; print("group", g, "pick", res[1]["pick"], "weak", res[1]["weak"], flush=True)
    json.dump(rows, open(f"{OUT}/rows10.json", "w"))
    P = [r for r in rows if r["arm"] == PRIMARY_ARM]; dets = sorted({k for r in rows for k in r["top"]})
    rep = dict(verdict=verdict(P), audits=audits, coupling=coupling(rows)); bad = completeness(S); rep["incomplete_settings"] = bad
    exp = os.environ.get("EXPECT_SETTINGS", "").split(); missing = [e for e in exp if e not in audits]; rep["missing_settings"] = missing
    if bad or missing: rep["verdict"]["VERDICT_IF_COMPLETE"] = rep["verdict"]["VERDICT"]; rep["verdict"]["VERDICT"] = "INCOMPLETE (no verdict)"; print("INCOMPLETE:", bad, missing, flush=True)
    rep["deployed_primary"] = {d: deployed(P, d) for d in dets}
    rep["deployed_by_ds"] = {ds: {d: deployed([r for r in P if r["ds"] == ds], d) for d in dets} for ds in sorted({r["ds"] for r in P})}
    rep["deployed_by_arm"] = {a: {d: deployed([r for r in rows if r["arm"] == a], d) for d in dets} for a in sorted({r["arm"] for r in rows})}
    rep["matched_primary"] = {d: {str(fa): matched(P, d, fa) for fa in (.03, .05, .07)} for d in dets if not d.endswith("|CS")}
    rep["matched_achieved_fa"] = {d: matched_full(P, d, .05)["achieved_fa"] for d in dets if not d.endswith("|CS")}
    rep["weak_split"] = {str(w): deployed([r for r in P if r["weak"] == w], "FV") for w in (False, True)}
    json.dump(rep, open(f"{OUT}/report10.json", "w"), indent=1)
    v = rep["verdict"]; print(json.dumps({k: v[k] for k in v if k != "per_ds"}, indent=1))
    for d, x in v["per_ds"].items(): print(f"  {d:10s}", " | ".join(f"{k} missed {y['missed'][0]}/{y['missed'][1]} FA {y['false_alarm'][0]}/{y['false_alarm'][1]}" for k, y in x.items()))
    for k, x in sorted(rep["deployed_primary"].items(), key=lambda kv: kv[1]["missed_share"]): print(f"  {k:16s} missed {x['missed']} FA {x['false_alarm']} matched5 {rep['matched_primary'].get(k, {}).get('0.05', '-')}")
    for a, x in rep["coupling"].items(): print("coupling", a, {k: x[k] for k in ("arm_missed", "source_missed", "bn_missed", "ratio", "ratio_vs_bn", "vs_source", "vs_bn", "diff_ci_vs_source", "diff_ci_vs_bn", "majority", "groups_higher_than_bn", "decay", "decay_shown", "groups_higher", "capture_lower_groups", "blind_spot", "auroc_by_window")})


if __name__ == "__main__":
    main()

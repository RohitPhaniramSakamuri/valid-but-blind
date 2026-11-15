"""Candidate alarm fixes, chosen on dev streams only; scored on exp006 held and exp005 held (both already seen: EXPLORATORY).
Every candidate gets its alarm level from that group's dev streams (out-of-fold by dev corruption where something is fitted)."""
import json, sys, numpy as np
from scipy.optimize import nnls
from load7 import load, IDX, cum, conformal, R6, R5
TOL = .10
def score_twin(s, fit=None): return (cum(s["b"]["flag"]) - s["c"]["r_twin"])[IDX]
def est_twin(s, fit=None): return cum(s["b"]["flag"])[IDX]
def est_pattern(s, w): return cum(s["X"] @ w)[IDX]
def fit_pattern(dev):
    X = np.vstack([s["X"] for s in dev]); y = np.concatenate([s["b"]["errT"] for s in dev]); return nnls(X.astype(float), y.astype(float))[0]
def true_cum(s): return cum(s["b"]["errT"])[IDX]
def z_parts(s): return np.stack([(cum(s["b"]["flag"]) - s["c"]["r_twin"])[IDX], cum(s["b"]["atc"])[IDX] - s["c"]["r0"], cum(s["b"]["dd"])[IDX]], 1)
def run(S, tag):
    G = sorted({(s["ds"], s["model"], s["arm"]) for s in S}); rows = {}
    def add(name, s, sc, thr): rows.setdefault(name, []).append(dict(g="/".join((s["ds"], s["model"], s["arm"])), ds=s["ds"], arm=s["arm"], strict=s["strict"], safe=s["safe"], alarm=bool((sc > thr).any()), top=float((sc - thr).max())))
    for g in G:
        dev = [s for s in S if (s["ds"], s["model"], s["arm"]) == g and s["split"] == "dev"]; held = [s for s in S if (s["ds"], s["model"], s["arm"]) == g and s["split"] == "held"]
        dsafe = [s for s in dev if s["safe"]]; r0 = dev[0]["c"]["r0"]
        # 1 twin as frozen in exp006
        thr = conformal([score_twin(s).max() for s in dsafe])[0]; [add("twin", s, score_twin(s), thr) for s in held]
        # 2 twin, residual calibration: alarm if est - q > r0 + TOL, q from max overestimate on safe dev streams
        q = conformal([(est_twin(s) - true_cum(s)).max() for s in dsafe])[0]; [add("twin_resid", s, est_twin(s) - q - r0 - TOL, 0) for s in held]
        # 3/4 pattern estimator (3 models x twin uncertainty, 10 non-negative weights), out-of-fold by dev corruption
        cors = sorted({s["cor"] for s in dev}); oof = {}
        for c in cors:
            w = fit_pattern([s for s in dev if s["cor"] != c])
            for s in dev:
                if s["cor"] == c: oof[id(s)] = est_pattern(s, w)
        wall = fit_pattern(dev)
        q = conformal([(oof[id(s)] - true_cum(s)).max() for s in dsafe])[0]; [add("pattern_resid", s, est_pattern(s, wall) - q - r0 - TOL, 0) for s in held]
        thr = conformal([(oof[id(s)] - r0).max() for s in dsafe])[0]; [add("pattern_level", s, est_pattern(s, wall) - r0, thr) for s in held]
        # 5 fusion of twin, ATC, dropout: standardise each by dev-safe median and spread per checkpoint, average
        Z = np.stack([z_parts(s) for s in dsafe]); med = np.median(Z, 0); sp = np.quantile(Z, .9, 0) - np.quantile(Z, .1, 0) + 1e-6
        fz = lambda s: ((z_parts(s) - med) / sp).mean(1)
        thr = conformal([fz(s).max() for s in dsafe])[0]; [add("fusion", s, fz(s), thr) for s in held]
        # 6 twin + pattern fusion
        Z2 = np.stack([np.stack([score_twin(s), oof[id(s)] - r0], 1) for s in dsafe]); med2 = np.median(Z2, 0); sp2 = np.quantile(Z2, .9, 0) - np.quantile(Z2, .1, 0) + 1e-6
        thr = conformal([((np.stack([score_twin(s), oof[id(s)] - r0], 1) - med2) / sp2).mean(1).max() for s in dsafe])[0]
        [add("twin+pattern", s, ((np.stack([score_twin(s), est_pattern(s, wall) - r0], 1) - med2) / sp2).mean(1), thr) for s in held]
    def summ(R):
        st, sf = [r for r in R if r["strict"]], [r for r in R if r["safe"]]
        m, f = sum(not r["alarm"] for r in st), sum(r["alarm"] for r in sf)
        return f"missed {m}/{len(st)} ({m/max(len(st),1):.1%})  FA {f}/{len(sf)} ({f/max(len(sf),1):.1%})"
    def matched(R, fa):
        m = [0, 0]
        for g in sorted({r["g"] for r in R}):
            sf = np.array([r["top"] for r in R if r["g"] == g and r["safe"]]); st = np.array([r["top"] for r in R if r["g"] == g and r["strict"]])
            if not len(st): continue
            t = np.quantile(sf, 1 - fa) if len(sf) else np.inf; m[0] += int((st <= t).sum()); m[1] += len(st)
        return f"{m[0]/m[1]:.1%}"
    print(f"\n===== {tag}")
    for sel_name, sel in (("primary Tent 1e-3", lambda r: r["arm"] in ("tent0.001",)), ("all arms", lambda r: True)):
        print(f"-- {sel_name}")
        for n, R in rows.items():
            R2 = [r for r in R if sel(r)]; print(f"  {n:15s} {summ(R2)} | matched-FA miss @3%/5%/7%: {matched(R2,.03)} / {matched(R2,.05)} / {matched(R2,.07)}")
    for ds in sorted({r["ds"] for r in rows["twin"]}):
        print(f"-- {ds} (all arms)"); [print(f"  {n:15s} {summ([r for r in R if r['ds']==ds])}") for n, R in rows.items()]
    return rows
if __name__ == "__main__":
    for root, tag in (((R5, "exp005 (Blood, Derma)"),) if "5" in sys.argv[1:] else ((R6, "exp006 (Path, OrganA, CIFAR x6)"), (R5, "exp005 (Blood, Derma)"))):
        S = load(root); run(S, tag)

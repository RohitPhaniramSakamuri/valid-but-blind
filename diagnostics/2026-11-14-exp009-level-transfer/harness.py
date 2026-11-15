"""exp009 development harness (EXPLORATORY). For every group and candidate detector: leave-one-dev-family-out (LOFO) false alarms / misses on dev, and deployed false alarms / misses on held."""
import json, sys
import numpy as np
from lib9 import *
BASE = ["twin", "released", "prototype", "atc", "doc", "dropout"]
COMBOS = dict(fus3=("twin", "atc", "dropout"), fus5=("twin", "atc", "doc", "dropout", "released"), fus_td=("twin", "doc"), fus_ta=("twin", "atc"))
def stat(A, ref, det):
    """A: (n, sig, t) raw base scores; ref: indices of safe calibration streams. Returns (n,) alarm statistic minus level (>0 alarms)."""
    name, cal = det.split("|"); R = A[ref]
    med = np.median(R, 0); sp = np.quantile(R, .9, 0) - np.quantile(R, .1, 0) + 1e-6; Zs = (A - med) / sp
    if name in BASE: x = (Zs if cal == "Z" else A)[:, BASE.index(name)]
    else:
        kind, parts = ("max", COMBOS[name[3:]]) if name.startswith("mx_") else ("mean", COMBOS[name]); P = Zs[:, [BASE.index(p) for p in parts]]
        x = P.max(1) if kind == "max" else P.mean(1)
        if cal == "Z":
            r = x[ref]; x = (x - np.median(r, 0)) / (np.quantile(r, .9, 0) - np.quantile(r, .1, 0) + 1e-6)
    m = x.max(1); return m - conformal(m[ref])
DETS = [f"{n}|{c}" for n in BASE + list(COMBOS) + ["mx_" + k for k in COMBOS] for c in "GZ"]
def run(S, arm="tent0.001"):
    rows = []
    for g, L in groups(S, arm).items():
        A = np.stack([np.stack([simple(n)(s) for n in BASE]) for s in L]); split = np.array([s["split"] for s in L]); safe = np.array([s["safe"] for s in L]); strict = np.array([s["strict"] for s in L]); cor = np.array([s["cor"] for s in L])
        dev = split == "dev"; held = ~dev
        if (dev & safe).sum() < 19: continue
        for det in DETS:
            fa = [0, 0]; mi = [0, 0]; perfam = {}
            for c in sorted(set(cor[dev])):
                ref = np.where(dev & safe & (cor != c))[0]; te = dev & (cor == c)
                if len(ref) < 19: continue
                d = stat(A, ref, det); a = (int((d[te & safe] > 0).sum()), int((te & safe).sum())); m = (int((d[te & strict] <= 0).sum()), int((te & strict).sum()))
                perfam[c] = a + m; fa[0] += a[0]; fa[1] += a[1]; mi[0] += m[0]; mi[1] += m[1]
            d = stat(A, np.where(dev & safe)[0], det)
            rows.append(dict(g="/".join(g), exp=g[0], ds=g[1], model=g[2], det=det, lofo_fa=fa, lofo_miss=mi, perfam=perfam, held_fa=[int((d[held & safe] > 0).sum()), int((held & safe).sum())], held_miss=[int((d[held & strict] <= 0).sum()), int((held & strict).sum())],
                             held_top=dict(safe=d[held & safe].tolist(), strict=d[held & strict].tolist())))
    return rows
if __name__ == "__main__":
    S = load(); rows = run(S); json.dump(rows, open("harness_rows.json", "w"))
    sh = lambda x: f"{x[0]}/{x[1]}"
    for exp in ("exp005", "exp006", "exp008"):
        print("==", exp, " det: LOFO-dev miss, FA | held miss, FA | per ds held miss,FA")
        R = [r for r in rows if r["exp"] == exp]; dss = sorted({r["ds"] for r in R})
        for det in DETS:
            Q = [r for r in R if r["det"] == det]; t = lambda k, Q=Q: [sum(r[k][0] for r in Q), sum(r[k][1] for r in Q)]
            print(f"{det:14s} {sh(t('lofo_miss')):>8s} {sh(t('lofo_fa')):>8s} | {sh(t('held_miss')):>8s} {t('held_miss')[0]/max(1,t('held_miss')[1]):.3f} {sh(t('held_fa')):>7s} {t('held_fa')[0]/max(1,t('held_fa')[1]):.3f} | " + " | ".join(f"{sh([sum(r['held_miss'][0] for r in Q if r['ds']==d), sum(r['held_miss'][1] for r in Q if r['ds']==d)])} {sh([sum(r['held_fa'][0] for r in Q if r['ds']==d), sum(r['held_fa'][1] for r in Q if r['ds']==d)])}" for d in dss))

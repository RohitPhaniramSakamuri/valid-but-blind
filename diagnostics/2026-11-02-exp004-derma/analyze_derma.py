"""Frozen before any DermaMNIST stream ran. Held-out streams only. Clear failure: mean error >= r0 + 0.15, last-quarter error < 0.85. Safe: mean error < r0 + 0.10, not collapsed.
A comparison needs >= 20 strict streams in each arm, otherwise INCONCLUSIVE.
V1 blind spot: released monitor on Tent 1e-3 vs source. REPLICATES if missed share is higher by >= 0.25. Else NOT SHOWN.
V2 entropy: Tent 1e-3 vs BN, released. ENTROPY ADDS if higher by >= 0.15. Else NOT SHOWN.
V3 twin (rule fixed from CIFAR, w=1 c=1) vs released on Tent 1e-3: FIX WORKS if missed share falls by >= 0.20 and false alarms on Tent's safe streams are <= 10%, with >= 40 safe streams. If fewer than 40 safe: FALSE ALARMS NOT ESTIMABLE. Else NOT SHOWN.
V4 twin vs prototype-distance proxy on Tent 1e-3: BEATS PROTOTYPE if twin misses at least 0.10 less and its false-alarm share is not more than 0.05 higher. PROTOTYPE BEATS if the prototype misses at least 0.10 less under the same condition. Else NO CLEAR DIFFERENCE.
V5 SAR: released on SAR vs source; REPLICATES if higher by >= 0.25. Else NOT SHOWN.
V6 adaptation-caused harm on Tent 1e-3 and 5e-3 pooled: target Tent error >= r0 + 0.15 and twin error < r0 + 0.10, reported for all and for non-collapsed. CATCHES if twin alarm >= 75% on >= 20 targets and false alarms <= 10% with >= 40 safe. PARTIAL at >= 50%. INCONCLUSIVE under those counts. Else NOT SHOWN.
Descriptive: per prior and corruption, capture and precision, bound exceeding error, first alarm, certified form, SAR kept share, cluster bootstrap by corruption and severity.
"""
import json
import os
from multiprocessing import Pool

import numpy as np
from confseq.conjmix_bounded import conjmix_empbern_lower_cs
from confseq.predmix import predmix_empbern_lower_cs

ALPHA, AL1, TOL = 0.15, 0.025, 0.1
ARMS = ("source", "bn", "tent1e-3", "tent5e-3", "sar")


def v_opt(x, t):
    m = np.cumsum(x) / np.arange(1, len(x) + 1)
    return np.cumsum((x - np.append(0.5, m[:-1])) ** 2)[t] * t


def first(z, L, level):
    x = np.clip(np.asarray(z), 0, 1)
    try:
        cs = np.asarray(conjmix_empbern_lower_cs(x=x, alpha=ALPHA, v_opt=v_opt(x, int(len(x) * 0.25))))
    except RuntimeError:
        cs = np.asarray(predmix_empbern_lower_cs(x=x, alpha=ALPHA))
    h = np.where(np.maximum(cs - L, 0) > level)[0]
    return int(h[0]) + 1 if len(h) else None


def score(a):
    s, c = a
    C = np.asarray(s["cells"])
    err, r0 = C[4:8].sum(0), c["r0"]
    w = (np.log(2) - np.log(AL1)) / (2 * c["n"])
    F, FA, nFnA = C[2] + C[3] + C[6] + C[7], C[3] + C[7], C[0] + C[4]
    e, l, tw = err.mean(), err[-len(err) // 4:].mean(), float(np.mean(s["twin_err"]))
    level = r0 + TOL
    twinz = F + nFnA
    f = dict(released=first(s["pos"], c["fp0"] + w, level), prototype=first(s["pos_p"], c["fpp0"] + w, level), twin=first(twinz, c["fpt"] + c["fnt"] + w, level), cert=first(FA + nFnA, c["fpt"] + c["fnt"] + w, level))
    return dict(key=s["key"], arm=s["arm"], split=s["split"], corruption=s["corruption"], severity=s["severity"], prior=s["prior"], rep=s["rep"], err=float(e), excess=float(e - r0), twin_ex=tw - r0, strict=bool(e >= r0 + 0.15 and l < 0.85), collapsed=bool(l >= 0.85), failing=bool(e >= r0 + 0.15), safe=bool(e < r0 + TOL and l < 0.85), first=f, conf=float(np.mean(s["conf"])), conf_twin=float(np.mean(s["conf_twin"])), capture_rel=float(np.sum(s["hit"]) / max(np.sum(err), 1e-9)), prec_rel=float(np.sum(s["hit"]) / max(np.sum(s["pos"]), 1e-9)), flagged=float(np.mean(s["pos"])), agree=float(C[[1, 3, 5, 7]].sum(0).mean()), bound_over=bool(np.mean(twinz) - (c["fpt"] + c["fnt"] + w) > e), kept=s["kept"], resets=s["resets"])


def miss(g, k):
    return [sum(r["first"][k] is None for r in g), len(g)]


def share(x):
    return x[0] / x[1] if x[1] else float("nan")


if __name__ == "__main__":
    cal = json.load(open("results/calibration_source.json"))
    jobs = []
    for a in ARMS:
        p = f"results/{a}.jsonl"
        for line in open(p) if os.path.exists(p) else []:
            jobs.append((json.loads(line), cal))
    with Pool(os.cpu_count()) as pool:
        rows = pool.map(score, jobs, chunksize=4)
    H = [r for r in rows if r["split"] == "held"]
    strict = lambda a: [r for r in H if r["arm"] == a and r["strict"]]
    safe = lambda a: [r for r in H if r["arm"] == a and r["safe"]]

    def cmp(a, ka, b, kb, need):
        x, y = miss(strict(a), ka), miss(strict(b), kb)
        return dict(a=x, b=y, gap=share(x) - share(y), met=None if min(x[1], y[1]) < 20 else bool(share(x) - share(y) >= need))

    lab = lambda c, y, n="NOT SHOWN": "INCONCLUSIVE" if c["met"] is None else (y if c["met"] else n)
    v1, v2, v5 = cmp("tent1e-3", "released", "source", "released", 0.25), cmp("tent1e-3", "released", "bn", "released", 0.15), cmp("sar", "released", "source", "released", 0.25)
    t = strict("tent1e-3")
    rel, tw, pr = miss(t, "released"), miss(t, "twin"), miss(t, "prototype")
    sf = safe("tent1e-3")
    fa = {k: [sum(r["first"][k] is not None for r in sf), len(sf)] for k in ("released", "twin", "prototype", "cert")}
    if len(t) < 20:
        v3 = "INCONCLUSIVE"
    elif share(rel) - share(tw) < 0.20:
        v3 = "NOT SHOWN"
    elif len(sf) < 40:
        v3 = "FALSE ALARMS NOT ESTIMABLE"
    else:
        v3 = "FIX WORKS" if share(fa["twin"]) <= 0.10 else "NOT SHOWN"
    if len(t) < 20 or not sf:
        v4 = "INCONCLUSIVE"
    elif share(pr) - share(tw) >= 0.10 and share(fa["twin"]) - share(fa["prototype"]) <= 0.05:
        v4 = "BEATS PROTOTYPE"
    elif share(tw) - share(pr) >= 0.10 and share(fa["prototype"]) - share(fa["twin"]) <= 0.05:
        v4 = "PROTOTYPE BEATS"
    else:
        v4 = "NO CLEAR DIFFERENCE"
    hg = [r for r in H if r["arm"] in ("tent1e-3", "tent5e-3") and r["failing"] and r["twin_ex"] < TOL]
    hs = [r for r in H if r["arm"] in ("tent1e-3", "tent5e-3") and r["safe"]]
    hc = [sum(r["first"]["twin"] is not None for r in hg), len(hg)]
    hfa = [sum(r["first"]["twin"] is not None for r in hs), len(hs)]
    if hc[1] < 20 or hfa[1] < 40:
        v6 = "INCONCLUSIVE"
    elif share(hfa) > 0.10:
        v6 = "NOT SHOWN"
    else:
        v6 = "CATCHES" if share(hc) >= 0.75 else "PARTIAL" if share(hc) >= 0.5 else "NOT SHOWN"
    nc = [r for r in hg if not r["collapsed"]]
    rng = np.random.default_rng(20261102)
    cl = sorted({(r["corruption"], r["severity"]) for r in H})

    def boot(fn, n=4000):
        v = []
        for _ in range(n):
            pick = [cl[i] for i in rng.integers(0, len(cl), len(cl))]
            v.append(fn(pick))
        return np.round(np.nanpercentile(v, [2.5, 97.5]), 3).tolist()

    def gap_for(pick, a, ka, b, kb):
        x, y = [0, 0], [0, 0]
        for c in pick:
            gx, gy = [r for r in strict(a) if (r["corruption"], r["severity"]) == c], [r for r in strict(b) if (r["corruption"], r["severity"]) == c]
            mx, my = miss(gx, ka), miss(gy, kb)
            x[0] += mx[0]; x[1] += mx[1]; y[0] += my[0]; y[1] += my[1]
        return share(x) - share(y) if x[1] and y[1] else float("nan")

    arm_tab = {a: dict(streams=sum(r["arm"] == a for r in H), strict=len(strict(a)), safe=len(safe(a)), collapsed=sum(r["collapsed"] for r in H if r["arm"] == a), err=float(np.mean([r["err"] for r in H if r["arm"] == a] or [np.nan])), conf_strict=float(np.mean([r["conf"] for r in strict(a)] or [np.nan])), flagged_strict=float(np.mean([r["flagged"] for r in strict(a)] or [np.nan])), capture_strict=float(np.mean([r["capture_rel"] for r in strict(a)] or [np.nan])), precision_strict=float(np.mean([r["prec_rel"] for r in strict(a)] or [np.nan])), missed={k: miss(strict(a), k) for k in ("released", "prototype", "twin", "cert")}, false_alarms={k: [sum(r["first"][k] is not None for r in safe(a)), len(safe(a))] for k in ("released", "prototype", "twin", "cert")}, bound_over=float(np.mean([r["bound_over"] for r in H if r["arm"] == a] or [np.nan])), kept=float(np.mean([r["kept"] for r in H if r["arm"] == a and r["kept"] is not None] or [np.nan]))) for a in ARMS}
    by = {}
    for name, f in (("prior", lambda r: r["prior"]), ("corruption", lambda r: r["corruption"])):
        by[name] = {}
        for k in sorted({f(r) for r in H}):
            by[name][k] = {a: dict(released=miss([r for r in strict(a) if f(r) == k], "released"), twin=miss([r for r in strict(a) if f(r) == k], "twin"), prototype=miss([r for r in strict(a) if f(r) == k], "prototype")) for a in ("source", "bn", "tent1e-3")}
    rep = dict(V1=lab(v1, "REPLICATES"), V2=lab(v2, "ENTROPY ADDS"), V3=v3, V4=v4, V5=lab(v5, "REPLICATES"), V6=v6, v1=v1, v2=v2, v5=v5, twin=dict(released=rel, twin=tw, prototype=pr, cert=miss(t, "cert"), false_alarms=fa), harm=dict(target=hc, safe_fa=hfa, released=miss(hg, "released") , prototype=miss(hg, "prototype"), noncollapsed=dict(twin=[sum(r["first"]["twin"] is not None for r in nc), len(nc)], released=[sum(r["first"]["released"] is not None for r in nc), len(nc)])), boot=dict(v1=boot(lambda p: gap_for(p, "tent1e-3", "released", "source", "released")), v2=boot(lambda p: gap_for(p, "tent1e-3", "released", "bn", "released")), twin_fall=boot(lambda p: gap_for(p, "tent1e-3", "released", "tent1e-3", "twin"))), arms=arm_tab, by=by, dev={a: dict(strict=sum(r["strict"] for r in rows if r["split"] == "dev" and r["arm"] == a), err=float(np.mean([r["err"] for r in rows if r["split"] == "dev" and r["arm"] == a] or [np.nan]))) for a in ("source", "tent1e-3")}, r0=cal["r0"], level=cal["r0"] + TOL, n=len(rows))
    json.dump(dict(report=rep, rows=rows), open("derma_report.json", "w"), indent=1)
    print(json.dumps(rep, indent=0))

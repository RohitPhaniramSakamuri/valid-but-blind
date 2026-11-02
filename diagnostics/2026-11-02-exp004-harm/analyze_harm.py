"""Frozen before any harm stream ran. Twin statistic fixed at w = 1, c = 1 from the earlier held-out verdict; released monitor recalibrated.
Adaptation-caused failure (target): Tent mean error >= r0 + 0.15, including collapsed streams, and twin mean error < r0 + 0.10.
Primary verdict over all target streams, excluding by-class:
INCONCLUSIVE if under 20 target streams or under 3 models with a target stream.
CATCHES HARM: twin alarm fires on >= 75% and false alarms on safe streams (Tent mean error < r0 + 0.10, not collapsed) are <= 10%.
PARTIAL: >= 50% with the same false-alarm limit. Otherwise NOT SHOWN.
Reported regardless: the released monitor on the same streams, the certified forms, per model and per lr, by-class streams, and first alarm.
"""
import json
import os
from multiprocessing import Pool

import numpy as np
from confseq.conjmix_bounded import conjmix_empbern_lower_cs
from confseq.predmix import predmix_empbern_lower_cs

MODELS = ["Hendrycks2020AugMix_ResNeXt", "Modas2021PRIMEResNet18", "Hendrycks2020AugMix_WRN", "Addepalli2021Towards_PARN18", "Addepalli2021Towards_WRN34", "Addepalli2022Efficient_WRN_34_10"]
ALPHA, AL1, TOL = 0.15, 0.025, 0.1


def v_opt(x, t):
    m = np.cumsum(x) / np.arange(1, len(x) + 1)
    return np.cumsum((x - np.append(0.5, m[:-1])) ** 2)[t] * t


def lower(x):
    try:
        return np.asarray(conjmix_empbern_lower_cs(x=x, alpha=ALPHA, v_opt=v_opt(x, int(len(x) * 0.25))))
    except RuntimeError:
        return np.asarray(predmix_empbern_lower_cs(x=x, alpha=ALPHA))


def first(z, L, r0):
    h = np.where(np.maximum(lower(np.clip(z, 0, 1)) - L, 0) > r0 + TOL)[0]
    return int(h[0]) + 1 if len(h) else None


def score(a):
    s, m, c = a
    C = np.asarray(s["cells"])
    err = C[4:8].sum(0)
    r0 = c["r0"]
    w = (np.log(2) - np.log(AL1)) / (2 * c["n_calib"])
    F, FA, nFnA = C[2] + C[3] + C[6] + C[7], C[3] + C[7], C[0] + C[4]
    e, l, tw = err.mean(), err[-len(err) // 4:].mean(), float(np.mean(s["twin_err"]))
    t = {"twin": first(F + nFnA, c["fp_twin"] + c["fn_twin"] + w, r0), "released": first(np.asarray(s["pos_recal"]), c["false_alarm0"] + w, r0), "cert0": first(FA, c["fp_twin"] + w, r0), "cert1": first(FA + nFnA, c["fp_twin"] + c["fn_twin"] + w, r0)}
    return dict(model=m, key=s["key"], kind=s["kind"], lr=s["lr"], corruption=s["corruption"], err=float(e), excess=float(e - r0), twin_ex=tw - r0, collapsed=bool(l >= 0.85), target=bool(e >= r0 + 0.15 and tw < r0 + TOL), safe=bool(e < r0 + TOL and l < 0.85), agree=float(C[[1, 3, 5, 7]].sum(0).mean()), conf=float(np.mean(s["conf"])), first=t)


if __name__ == "__main__":
    jobs = []
    for m in MODELS:
        c = json.load(open(f"results_harm_{m}/calibration.json"))
        for line in open(f"results_harm_{m}/streams.jsonl"):
            jobs.append((json.loads(line), m, c))
    with Pool(os.cpu_count()) as p:
        rows = p.map(score, jobs, chunksize=2)

    def cnt(g, k):
        return [sum(r["first"][k] is not None for r in g), len(g)]

    main = [r for r in rows if r["kind"] != "by_class"]
    tg, sf = [r for r in main if r["target"]], [r for r in main if r["safe"]]
    n_models = len({r["model"] for r in tg})
    a, n = cnt(tg, "twin")
    fa, ns = cnt(sf, "twin")
    okfa = ns > 0 and fa / ns <= 0.10
    v = "INCONCLUSIVE" if n < 20 or n_models < 3 else "CATCHES HARM" if a / n >= 0.75 and okfa else "PARTIAL" if a / n >= 0.5 and okfa else "NOT SHOWN"
    med = lambda g, k: float(np.median([r["first"][k] for r in g if r["first"][k] is not None])) if any(r["first"][k] is not None for r in g) else None
    rep = dict(verdict=v, target=[a, n], models_with_target=n_models, false_alarms=[fa, ns], released_target=cnt(tg, "released"), released_false=cnt(sf, "released"), cert0_target=cnt(tg, "cert0"), cert1_target=cnt(tg, "cert1"), median_first=dict(twin=med(tg, "twin"), released=med(tg, "released")), collapsed_target=dict(n=sum(r["collapsed"] for r in tg), twin=cnt([r for r in tg if r["collapsed"]], "twin"), released=cnt([r for r in tg if r["collapsed"]], "released")), noncollapsed_target=dict(twin=cnt([r for r in tg if not r["collapsed"]], "twin"), released=cnt([r for r in tg if not r["collapsed"]], "released")),
               per_model={m: dict(twin=cnt([r for r in tg if r["model"] == m], "twin"), released=cnt([r for r in tg if r["model"] == m], "released"), safe_twin=cnt([r for r in sf if r["model"] == m], "twin")) for m in MODELS}, per_lr={str(l): dict(twin=cnt([r for r in tg if r["lr"] == l], "twin"), released=cnt([r for r in tg if r["lr"] == l], "released")) for l in (0.01, 0.05)},
               by_class=[{k: r[k] for k in ("model", "lr", "err", "twin_ex", "excess", "collapsed", "first")} for r in rows if r["kind"] == "by_class"], streams=len(rows), status={"target": len(tg), "safe": len(sf), "other": len(main) - len(tg) - len(sf)})
    json.dump(dict(report=rep, rows=rows), open("harm_report.json", "w"), indent=1)
    print(json.dumps(rep, indent=0))

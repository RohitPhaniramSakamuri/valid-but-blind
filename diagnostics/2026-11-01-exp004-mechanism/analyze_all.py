"""Experiment 004 mechanism and authors'-pipeline analysis. Frozen before any stream ran. Streams are scored in parallel.

Monitor and strict violation definitions are unchanged (released form). Scored: at least 5 strict violations in both compared
arms. Each verdict is INCONCLUSIVE under 5 scored models. Missed share below means strict violations with no alarm.

Q1, is threshold recalibration required? FIXED GAP HOLDS if Tent 1e-3 with the fixed threshold is missed more than source in at
   least 5 scored models with pooled gap >= 0.25. Otherwise RECALIBRATION MATTERS. Recalibrated Tent is the reference on these draws.
Q2, does the entropy step add misses beyond normalization? ENTROPY ADDS if Tent 1e-3 is missed more than BN in at least 5 scored
   models with pooled gap >= 0.15, both recalibrated. Otherwise NOT SHOWN.
Q3, does normalization alone produce the gap? NORMALIZATION SUFFICES if BN (recalibrated) is missed more than source in at least 5
   scored models with pooled gap >= 0.25. Otherwise NOT SHOWN.
Descriptive: BN fixed, Tent 1e-4 both forms, unflagged-error shares, excess-error bands.

A. Authors' pipeline, 2 models (AugMix ResNeXt and WRN-40-2), replication draws 0 and 1. REPRODUCED if there are at least 10 strict
   violations in each arm, Tent's pooled missed share is >= 0.75, the pooled gap against source is >= 0.25, and Tent is higher in both.
   Otherwise NOT REPRODUCED. PORT AGREES if alarms match the port on >= 90% of matched streams and median absolute difference in mean error is <= 0.01.
"""
import json
import os
import sys
from multiprocessing import Pool

import numpy as np
from confseq.conjmix_bounded import conjmix_empbern_lower_cs
from confseq.predmix import predmix_empbern_lower_cs

ALPHA_CS, ALPHA_L1, TOL = 0.15, 0.025, 0.1
MODELS = ["Hendrycks2020AugMix_ResNeXt", "Modas2021PRIMEResNet18", "Hendrycks2020AugMix_WRN", "Addepalli2021Towards_PARN18", "Addepalli2021Towards_WRN34", "Addepalli2022Efficient_WRN_34_10"]


def v_opt(x, t):
    m = np.cumsum(x) / np.arange(1, len(x) + 1)
    return np.cumsum((x - np.append(0.5, m[:-1])) ** 2)[t] * t


def lower_cs(x):
    x = np.asarray(x)
    try:
        return np.asarray(conjmix_empbern_lower_cs(x=x, alpha=ALPHA_CS, v_opt=v_opt(x, int(len(x) * 0.25)))), False
    except RuntimeError:
        return np.asarray(predmix_empbern_lower_cs(x=x, alpha=ALPHA_CS)), True


def score(job):
    s, r0, L1 = job
    err, last = float(np.mean(s["err"])), float(np.mean(s["err"][-len(s["err"]) // 4:]))
    r = dict(key=s["key"], model=s["model"], arm=s["arm"], err=err, strict=err >= r0 + TOL + 0.05 and last < 0.85, collapsed=last >= 0.85, excess=err - r0, conf=float(np.mean(s["conf"])))
    for form in ("recal", "fixed", "plain"):
        if f"pos_{form}" in s or (form == "plain" and "pos" in s):
            cs, fb = lower_cs(s["pos"] if form == "plain" else s[f"pos_{form}"])
            r[f"alarm_{form}"] = bool((np.maximum(cs - L1, 0) > r0 + TOL).any())
            r[f"fallback_{form}"] = fb
            if f"pfn_{form}" in s:
                r[f"pfn_{form}"] = float(np.mean(s[f"pfn_{form}"]))
    return r


def tally(rows, model, arm, form):
    st = [r for r in rows if r["model"] == model and r["arm"] == arm and r["strict"]]
    return len(st), sum(not r[f"alarm_{form}"] for r in st)


def compare(rows, a, af, b, bf, gap_needed, models=MODELS):
    scored = [m for m in models if min(tally(rows, m, a, af)[0], tally(rows, m, b, bf)[0]) >= 5]
    ta, tb = {m: tally(rows, m, a, af) for m in models}, {m: tally(rows, m, b, bf) for m in models}
    per = {m: dict(a=ta[m][::-1], b=tb[m][::-1]) for m in models}
    if len(scored) < 5:
        return dict(met=None, scored=scored, per=per)
    an, am = np.sum([ta[m] for m in scored], axis=0)
    bn, bm = np.sum([tb[m] for m in scored], axis=0)
    higher = [m for m in scored if ta[m][1] / ta[m][0] > tb[m][1] / tb[m][0]]
    gap = float(am / an - bm / bn)
    return dict(met=bool(len(higher) >= 5 and gap >= gap_needed), scored=scored, higher=len(higher), a=[int(am), int(an)], b=[int(bm), int(bn)], gap=gap, per=per)


if __name__ == "__main__":
    jobs = []
    for m in MODELS:
        cal = json.load(open(f"results_{m}/calibration.json"))
        L1 = cal["false_alarm0"] + (np.log(2) - np.log(ALPHA_L1)) / (2 * cal["n_calib"])
        for line in open(f"results_{m}/streams.jsonl"):
            s = json.loads(line)
            s["model"] = m
            if s["arm"] == "source":
                s.pop("pos_recal", None)
                s.pop("pfn_recal", None)
            jobs.append((s, cal["r0"], L1))
    with Pool(os.cpu_count()) as pool:
        rows = pool.map(score, jobs, chunksize=8)
        q1 = compare(rows, "tent1e-3", "fixed", "source", "fixed", 0.25)
        q2 = compare(rows, "tent1e-3", "recal", "bn", "recal", 0.15)
        q3 = compare(rows, "bn", "recal", "source", "fixed", 0.25)
        label = lambda c, y, n: "INCONCLUSIVE" if c["met"] is None else (y if c["met"] else n)
        report = dict(Q1=label(q1, "FIXED GAP HOLDS", "RECALIBRATION MATTERS"), Q2=label(q2, "ENTROPY ADDS", "NOT SHOWN"), Q3=label(q3, "NORMALIZATION SUFFICES", "NOT SHOWN"),
                      q1=q1, q2=q2, q3=q3, tent_recal_vs_source=compare(rows, "tent1e-3", "recal", "source", "fixed", 0.25),
                      bn_fixed_vs_source=compare(rows, "bn", "fixed", "source", "fixed", 0.25), low_lr_recal_vs_source=compare(rows, "tent1e-4", "recal", "source", "fixed", 0.25),
                      low_lr_fixed_vs_source=compare(rows, "tent1e-4", "fixed", "source", "fixed", 0.25),
                      fallbacks=sum(any(r.get(k) for k in ("fallback_recal", "fallback_fixed")) for r in rows))
        arms = {}
        for arm in ("source", "bn", "tent1e-4", "tent1e-3"):
            g = [r for r in rows if r["arm"] == arm]
            st = [r for r in g if r["strict"]]
            arms[arm] = dict(n=len(g), strict=len(st), collapsed=sum(r["collapsed"] for r in g), err=float(np.mean([r["err"] for r in g])), conf=float(np.mean([r["conf"] for r in g])),
                             strict_err=float(np.mean([r["err"] for r in st])) if st else None, strict_pfn_fixed=float(np.mean([r["pfn_fixed"] for r in st])) if st else None,
                             strict_pfn_recal=float(np.mean([r["pfn_recal"] for r in st])) if st and arm != "source" else None)
        report["arms"] = arms
        json.dump(dict(report=report, rows=rows), open("factorial_report.json", "w"), indent=1)

        port = {}
        for m in ("Hendrycks2020AugMix_ResNeXt", "Hendrycks2020AugMix_WRN"):
            cal = json.load(open(f"port_replicate/results_{m}/calibration.json"))
            L1 = cal["false_alarm0"] + (np.log(2) - np.log(ALPHA_L1)) / (2 * cal["n_calib"])
            for line in open(f"port_replicate/results_{m}/streams.jsonl"):
                s = json.loads(line)
                if s["rep"] < 2:
                    port[(m, s["key"])] = (s, cal["r0"], L1)
        ajobs, pjobs = [], []
        for m in ("Hendrycks2020AugMix_ResNeXt", "Hendrycks2020AugMix_WRN"):
            path = f"authors_{m}.jsonl"
            for line in open(path) if os.path.exists(path) else []:
                s = json.loads(line)
                s["model"] = m
                ajobs.append((s, s["r0"], s["L_1"]))
                pjobs.append(({**port[(m, s["key"])][0], "model": m}, *port[(m, s["key"])][1:]))
        a, p = pool.map(score, ajobs, chunksize=4), pool.map(score, pjobs, chunksize=4)
    ms = ("Hendrycks2020AugMix_ResNeXt", "Hendrycks2020AugMix_WRN")
    t = {m: tally(a, m, "tent", "plain") for m in ms}
    s = {m: tally(a, m, "source", "plain") for m in ms}
    ts, tm = np.sum(list(t.values()), axis=0)
    ss, sm = np.sum(list(s.values()), axis=0)
    both = all(s[m][0] and t[m][0] and t[m][1] / t[m][0] > s[m][1] / s[m][0] for m in ms)
    good = bool(ts >= 10 and ss >= 10 and tm / max(ts, 1) >= 0.75 and tm / max(ts, 1) - sm / max(ss, 1) >= 0.25 and both)
    agree = float(np.mean([x["alarm_plain"] == y["alarm_plain"] for x, y in zip(a, p)])) if a else None
    diff = float(np.median([abs(x["err"] - y["err"]) for x, y in zip(a, p)])) if a else None
    conf_diff = float(np.median([abs(x["conf"] - y["conf"]) for x, y in zip(a, p)])) if a else None
    auth = dict(verdict="REPRODUCED" if good else "NOT REPRODUCED", tent=[int(tm), int(ts)], source=[int(sm), int(ss)], per_tent={m: t[m][::-1] for m in ms}, per_source={m: s[m][::-1] for m in ms},
                n=len(a), alarm_agreement=agree, median_abs_err_diff=diff, median_abs_conf_diff=conf_diff, port_agrees=bool(a and agree >= 0.9 and diff <= 0.01))
    json.dump(dict(report=auth, rows=a, port_rows=p), open("authors_report.json", "w"), indent=1)
    print(json.dumps(dict(factorial=report, authors=auth), indent=0))

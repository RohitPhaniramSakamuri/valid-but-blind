"""Exploratory; definitions written before any false-alarm rate was computed, after all frozen verdicts. Saved streams only; enters no rule.

Safe stream: mean error < r0 + 0.10 and last-quarter error < 0.85. Stream false alarm: an alarm on a safe stream.
Alarm-time false alarm: over all streams with an alarm, running mean error at the first alarm <= r0 + 0.10.
Band streams (between r0 + 0.10 and the strict level) are neither safe nor strict. Collapsed streams are excluded from safe and strict.
Separation: M = max over t of (lower bound - L1 - r0). The released alarm is M > 0.10. AUROC of M, strict against safe streams, per model.
Matched sensitivity: per model and arm, set the alarm level to the (1-f) quantile of M on safe streams, f = 0.05 and 0.10; report strict misses.
Models with fewer than 5 safe or 5 strict streams in an arm are not used for that arm's AUROC or matched figures.
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


def job(a):
    study, arm, model, pos, err, r0, L1 = a
    x, err = np.asarray(pos), np.asarray(err)
    try:
        cs = np.asarray(conjmix_empbern_lower_cs(x=x, alpha=ALPHA, v_opt=v_opt(x, int(len(x) * 0.25))))
    except RuntimeError:
        cs = np.asarray(predmix_empbern_lower_cs(x=x, alpha=ALPHA))
    b = np.maximum(cs - L1, 0) - r0
    hit = np.where(b > TOL)[0]
    run = np.cumsum(err) / np.arange(1, len(err) + 1)
    e, l = err.mean(), err[-len(err) // 4:].mean()
    return dict(study=study, arm=arm, model=model, M=float(b.max()), alarm=bool(len(hit)), err=float(e), excess=float(e - r0), safe=bool(e < r0 + TOL and l < 0.85), strict=bool(e >= r0 + TOL + 0.05 and l < 0.85), collapsed=bool(l >= 0.85), alarm_false=bool(len(hit) and run[hit[0]] <= r0 + TOL))


def load(study, folder, spec, jobs):
    for m in MODELS:
        c = json.load(open(f"{folder.format(m=m)}/calibration.json"))
        r0, L1 = c["r0"], c["false_alarm0"] + (np.log(2) - np.log(AL1)) / (2 * c["n_calib"])
        for line in open(f"{folder.format(m=m)}/streams.jsonl"):
            s = json.loads(line)
            for arm, form, pk in spec:
                if s["arm"] == arm:
                    jobs.append((study, f"{arm}/{form}", m, s[pk], s["err"], r0, L1))


jobs = []
load("factorial", "results_{m}", [("source", "fixed", "pos_fixed"), ("bn", "recal", "pos_recal"), ("bn", "fixed", "pos_fixed"), ("tent1e-4", "recal", "pos_recal"), ("tent1e-4", "fixed", "pos_fixed"), ("tent1e-3", "recal", "pos_recal"), ("tent1e-3", "fixed", "pos_fixed")], jobs)
load("sar", "../2026-11-02-exp004-sar/results_sar_{m}", [("sar", "recal", "pos_recal"), ("sar", "fixed", "pos_fixed")], jobs)
load("replication", "../2026-11-01-exp004-replicate/results_{m}", [("tent", "recal", "pos"), ("source", "fixed", "pos")], jobs)
with Pool(os.cpu_count()) as p:
    R = p.map(job, jobs, chunksize=8)


def auroc(a, b):
    a, b = np.asarray(a)[:, None], np.asarray(b)[None, :]
    return float((a > b).mean() + 0.5 * (a == b).mean())


out = {}
for key in sorted({(r["study"], r["arm"]) for r in R}):
    g = [r for r in R if (r["study"], r["arm"]) == key]
    safe, strict, al = [r for r in g if r["safe"]], [r for r in g if r["strict"]], [r for r in g if r["alarm"]]
    per, match = {}, {0.05: [], 0.10: []}
    for m in MODELS:
        s0, s1 = [r["M"] for r in safe if r["model"] == m], [r["M"] for r in strict if r["model"] == m]
        fa = sum(r["alarm"] for r in safe if r["model"] == m)
        per[m] = dict(safe=len(s0), strict=len(s1), false_alarms=fa, missed=sum(not r["alarm"] for r in strict if r["model"] == m))
        if len(s0) >= 5 and len(s1) >= 5:
            per[m]["auroc"] = round(auroc(s1, s0), 3)
            for f in match:
                lv = np.quantile(s0, 1 - f)
                match[f].append((sum(x <= lv for x in s1), len(s1)))
                per[m][f"matched_{f}"] = [int(sum(x <= lv for x in s1)), len(s1)]
    au = [v["auroc"] for v in per.values() if "auroc" in v]
    out["|".join(key)] = dict(streams=len(g), safe=len(safe), band=len(g) - len(safe) - len(strict) - sum(r["collapsed"] for r in g), strict=len(strict), collapsed=sum(r["collapsed"] for r in g),
                              alarms_all=len(al), false_alarms_safe=sum(r["alarm"] for r in safe), alarm_time_false=sum(r["alarm_false"] for r in al), missed_strict=sum(not r["alarm"] for r in strict),
                              models_auroc=len(au), mean_auroc=round(float(np.mean(au)), 3) if au else None,
                              matched={str(f): dict(models=len(v), missed=int(sum(x[0] for x in v)), strict=int(sum(x[1] for x in v))) for f, v in match.items()}, per=per)
json.dump(out, open("explore_false_alarm.json", "w"), indent=1)
SAME = ["Addepalli2021Towards_PARN18", "Addepalli2021Towards_WRN34", "Addepalli2022Efficient_WRN_34_10"]
same = {}
for k in ("factorial|source/fixed", "factorial|tent1e-3/recal", "factorial|tent1e-3/fixed", "replication|source/fixed", "replication|tent/recal"):
    p = out[k]["per"]
    same[k] = dict(mean_auroc=round(float(np.mean([p[m]["auroc"] for m in SAME])), 3), auroc={m: p[m]["auroc"] for m in SAME}, matched_05=np.sum([p[m]["matched_0.05"] for m in SAME], axis=0).tolist(), matched_10=np.sum([p[m]["matched_0.1"] for m in SAME], axis=0).tolist(), released_missed=[int(sum(p[m]["missed"] for m in SAME)), int(sum(p[m]["strict"] for m in SAME))], false_alarms=[int(sum(p[m]["false_alarms"] for m in SAME)), int(sum(p[m]["safe"] for m in SAME))])
out["same_three_models"] = same
json.dump(out, open("explore_false_alarm.json", "w"), indent=1)
for k, v in same.items():
    print(k, v)

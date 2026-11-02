"""Experiment 004 replication analysis. Frozen before any replication stream ran.

Monitor, strict violation and alarm definitions are unchanged from analyze_confirm.py (released form).
A model is scored only with at least 5 strict violations in BOTH arms.

Verdict, across scored models:
INCONCLUSIVE if fewer than 5 models are scored.
REPLICATED if both hold:
  R1. Tent's missed share exceeds source's in at least 5 scored models.
  R2. Pooled missed share, Tent minus source, is at least 0.25.
Otherwise NOT REPLICATED.

Reported but not part of the verdict: the same verdict without AugMix ResNeXt (the only model that has
seen these images in monitoring); the square-root monitor form; streams where both arms violate on
the same draw; missed shares by excess error above r0, because a larger excess is easier to detect and
could explain an arm gap; bootstrap interval over models.
"""
import json
import sys

import numpy as np
from confseq.conjmix_bounded import conjmix_empbern_lower_cs
from confseq.predmix import predmix_empbern_lower_cs

ALPHA_CS, ALPHA_L1, TOL = 0.15, 0.025, 0.1
MODELS = sys.argv[1:]
BANDS = ((0.15, 0.25), (0.25, 0.35), (0.35, 9))


def v_opt(x, t):
    x = np.asarray(x)
    m = np.cumsum(x) / np.arange(1, len(x) + 1)
    return np.cumsum((x - np.append(0.5, m[:-1])) ** 2)[t] * t


def analyze(name):
    d = f"results_{name}"
    cal = json.load(open(f"{d}/calibration.json"))
    th, w, rows = cal["r0"] + TOL, (np.log(2) - np.log(ALPHA_L1)) / (2 * cal["n_calib"]), []
    for line in open(f"{d}/streams.jsonl"):
        s = json.loads(line)
        x = np.array(s["pos"])
        try:
            cs, fb = np.asarray(conjmix_empbern_lower_cs(x=x, alpha=ALPHA_CS, v_opt=v_opt(x, int(len(x) * 0.25)))), False
        except RuntimeError:
            cs, fb = np.asarray(predmix_empbern_lower_cs(x=x, alpha=ALPHA_CS)), True
        err, last = float(np.mean(s["err"])), float(np.mean(s["err"][-len(x) // 4:]))
        r = dict(key=s["key"], arm=s["arm"], draw=f'{s["corruption"]}/{s["severity"]}/{s["rep"]}', err=err, last=last, fallback=fb, conf=float(np.mean(s["conf"])),
                 excess=err - cal["r0"], collapsed=last >= 0.85, strict=err >= th + 0.05 and last < 0.85)
        for form, wid in (("released", w), ("sqrt", float(np.sqrt(w)))):
            bound = np.maximum(cs - (cal["false_alarm0"] + wid), 0)
            r[f"alarm_{form}"], r[f"final_bound_{form}"] = bool((bound > th).any()), float(bound[-1])
        rows.append(r)
    return cal, rows


def tally(rows, arm, form="released"):
    st = [r for r in rows if r["arm"] == arm and r["strict"]]
    return len(st), sum(not r[f"alarm_{form}"] for r in st)


def verdict(per, form="released"):
    scored = [m for m in per if min(tally(per[m], "tent", form)[0], tally(per[m], "source", form)[0]) >= 5]
    if len(scored) < 5:
        return dict(verdict="INCONCLUSIVE", scored=scored)
    ts, tm = np.sum([tally(per[m], "tent", form) for m in scored], axis=0)
    ss, sm = np.sum([tally(per[m], "source", form) for m in scored], axis=0)
    higher = [m for m in scored if tally(per[m], "tent", form)[1] / tally(per[m], "tent", form)[0] > tally(per[m], "source", form)[1] / tally(per[m], "source", form)[0]]
    gap = float(tm / ts - sm / ss)
    return dict(verdict="REPLICATED" if len(higher) >= 5 and gap >= 0.25 else "NOT REPLICATED", scored=scored, tent_higher=higher,
                tent=[int(tm), int(ts)], source=[int(sm), int(ss)], gap=gap)


per, cals = {}, {}
for m in MODELS:
    cals[m], per[m] = analyze(m)
table = {}
for m, rows in per.items():
    t, s = tally(rows, "tent"), tally(rows, "source")
    tent = [r for r in rows if r["arm"] == "tent"]
    src = [r for r in rows if r["arm"] == "source"]
    table[m] = dict(r0=cals[m]["r0"], conf=float(np.mean([r["conf"] for r in tent])), tent_err=float(np.mean([r["err"] for r in tent])), source_err=float(np.mean([r["err"] for r in src])),
                    tent_strict=t[0], tent_missed=t[1], source_strict=s[0], source_missed=s[1], tent_collapsed=sum(r["collapsed"] for r in tent), source_collapsed=sum(r["collapsed"] for r in src),
                    n_per_arm=len(tent), fallback=[r["key"] for r in rows if r["fallback"]])
paired = {"both": 0, "tent_missed": 0, "source_missed": 0, "tent_only_missed": 0, "source_only_missed": 0}
for rows in per.values():
    by = {(r["arm"], r["draw"]): r for r in rows}
    for r in rows:
        if r["arm"] == "tent" and r["strict"] and by[("source", r["draw"])]["strict"]:
            a, b = not r["alarm_released"], not by[("source", r["draw"])]["alarm_released"]
            paired["both"] += 1
            paired["tent_missed"] += a
            paired["source_missed"] += b
            paired["tent_only_missed"] += a and not b
            paired["source_only_missed"] += b and not a
bands = {}
for lo, hi in BANDS:
    for arm in ("tent", "source"):
        st = [r for rows in per.values() for r in rows if r["arm"] == arm and r["strict"] and lo <= r["excess"] < hi]
        bands[f"{arm}/{lo}-{hi}"] = [sum(not r["alarm_released"] for r in st), len(st)]
rng = np.random.RandomState(20261101)
names, boots = list(per), []
for _ in range(5000):
    pick = rng.choice(names, len(names))
    ts, tm = np.sum([tally(per[m], "tent") for m in pick], axis=0)
    ss, sm = np.sum([tally(per[m], "source") for m in pick], axis=0)
    if ts and ss:
        boots.append(tm / ts - sm / ss)
report = dict(primary=verdict(per), without_resnext=verdict({m: v for m, v in per.items() if m != "Hendrycks2020AugMix_ResNeXt"}), sqrt=verdict(per, "sqrt"),
              paired=paired, bands=bands, model_bootstrap_gap_95=[float(q) for q in np.percentile(boots, [2.5, 97.5])], table=table)
json.dump(report, open("replicate_report.json", "w"), indent=1)
print(json.dumps(report, indent=0))

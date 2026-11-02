"""Experiment 004 confirmation analysis. Frozen before the confirmation run.

Strict violation: final running error >= r0 + 0.15, last-quarter error < 0.85 (noncollapsed).
Released monitor form as in analyze_monitor.py; the square-root form is reported only.

PRIMARY population: Tent, corrupted, Dirichlet alpha 0.1, severities 3 and 5, held-out families.
CONFIRMED only if all of these hold:
1. At least 10 strict violations in the primary population.
2. Missed share >= 75% with exact 95% lower bound above 50%.
3. Control, Tent corrupted by-class: missed share <= 20%, if it has strict violations.
4. Mean Assumption 1 failure share in the primary population <= 0.05.
5. Replacement control: Tent corrupted Dirichlet mean error exceeds balanced_wr mean error by at least 0.03.

Everything else, including ETA, clean streams and other alpha values, is descriptive.
"""
import json
import os
from collections import defaultdict

import numpy as np
from confseq.conjmix_bounded import conjmix_empbern_lower_cs
from confseq.predmix import predmix_empbern_lower_cs
from scipy.stats import beta

ALPHA_CS, ALPHA_L1, TOL, T_MIN = 0.15, 0.025, 0.1, 10
DIR = os.environ.get("RESULTS_DIR", "results_confirm")


def v_opt(x, t):
    x = np.asarray(x)
    m = np.cumsum(x) / np.arange(1, len(x) + 1)
    return np.cumsum((x - np.append(0.5, m[:-1])) ** 2)[t] * t


def lower(k, n):
    return 0.0 if k == 0 else float(beta.ppf(0.025, k, n - k + 1))


def auroc(pos, neg):
    if not len(pos) or not len(neg):
        return None
    return round(float(np.mean([(p > n) + 0.5 * (p == n) for p in pos for n in neg])), 3)


cal = json.load(open(f"{DIR}/calibration.json"))
th = cal["r0"] + TOL
strict_th = th + 0.05
w = (np.log(2) - np.log(ALPHA_L1)) / (2 * cal["n_calib"])
rows = []
for line in open(f"{DIR}/streams.jsonl"):
    s = json.loads(line)
    x = np.array(s["pos"])
    T = len(x)
    try:
        cs, fb = np.asarray(conjmix_empbern_lower_cs(x=x, alpha=ALPHA_CS, v_opt=v_opt(x, int(T * 0.25)))), False
    except RuntimeError:
        cs, fb = np.asarray(predmix_empbern_lower_cs(x=x, alpha=ALPHA_CS)), True
    tt = np.arange(1, T + 1)
    margin = np.cumsum(s["pfn"]) / tt + cal["false_alarm0"] - np.cumsum(s["pfa"]) / tt
    r = dict(key=s["key"], arm=s["arm"], corruption=s["corruption"], severity=s["severity"], kind=s["kind"], alpha=s["alpha"], fallback=fb,
             err=float(np.mean(s["err"])), last=float(np.mean(s["err"][-T // 4:])), conf=float(np.mean(s["conf"])), pos=float(x.mean()),
             pfn=float(np.mean(s["pfn"])), pfa=float(np.mean(s["pfa"])), top=float(np.mean(s["top_share"])), disagree=float(np.mean(s["disagree"])),
             asm=float((margin[T_MIN:] < 0).mean()))
    r["collapsed"] = r["last"] >= 0.85
    r["strict"] = r["err"] >= strict_th and not r["collapsed"]
    for name, wid in (("released", w), ("sqrt", float(np.sqrt(w)))):
        bound = np.maximum(cs - (cal["false_alarm0"] + wid), 0)
        hit = np.where(bound > th)[0]
        r[f"alarm_{name}"] = bool(len(hit))
        r[f"final_bound_{name}"] = float(bound[-1])
    rows.append(r)


def group(pred):
    g = [r for r in rows if pred(r)]
    st = [r for r in g if r["strict"]]
    non = [r for r in g if not r["strict"] and not r["collapsed"]]
    return dict(n=len(g), err=round(float(np.mean([r["err"] for r in g])), 3) if g else None, conf=round(float(np.mean([r["conf"] for r in g])), 3) if g else None,
                pos=round(float(np.mean([r["pos"] for r in g])), 3) if g else None, pfn=round(float(np.mean([r["pfn"] for r in g])), 3) if g else None,
                asm=round(float(np.mean([r["asm"] for r in g])), 3) if g else None, collapsed=sum(r["collapsed"] for r in g), strict=len(st),
                missed=sum(not r["alarm_released"] for r in st), missed_sqrt=sum(not r["alarm_sqrt"] for r in st), others_alarmed=sum(r["alarm_released"] for r in non), others=len(non),
                final_bound=round(float(np.mean([r["final_bound_released"] for r in g])), 3) if g else None)


corrupted = lambda r: r["corruption"] != "clean"
primary = lambda r: r["arm"] == "tent" and corrupted(r) and r["kind"] == "dirichlet" and r["alpha"] == 0.1
P, C, BW = group(primary), group(lambda r: r["arm"] == "tent" and corrupted(r) and r["kind"] == "by_class"), group(lambda r: r["arm"] == "tent" and corrupted(r) and r["kind"] == "balanced_wr")
checks = dict(
    enough_violations=P["strict"] >= 10,
    missed_share=P["missed"] / P["strict"] if P["strict"] else None,
    missed_lower95=lower(P["missed"], P["strict"]) if P["strict"] else None,
    control_missed_share=C["missed"] / C["strict"] if C["strict"] else None,
    assumption_mean=P["asm"],
    replacement_gap=round(P["err"] - BW["err"], 3))
checks["confirmed"] = bool(checks["enough_violations"] and checks["missed_share"] >= 0.75 and checks["missed_lower95"] > 0.5
                           and (checks["control_missed_share"] is None or checks["control_missed_share"] <= 0.2)
                           and checks["assumption_mean"] <= 0.05 and checks["replacement_gap"] >= 0.03)
table = {}
keys = sorted({(r["arm"], "clean" if r["corruption"] == "clean" else "corrupted", r["kind"], r["alpha"]) for r in rows}, key=str)
for a, c, k, al in keys:
    table[f"{a}/{c}/{k}/{al}"] = group(lambda r: r["arm"] == a and (r["corruption"] == "clean") == (c == "clean") and r["kind"] == k and r["alpha"] == al)
tent = [r for r in rows if r["arm"] == "tent" and not r["collapsed"] and r["kind"] != "by_class"]
y = np.array([r["strict"] for r in tent])
aucs = {k: auroc(np.array([r[f] for r in tent])[y], np.array([r[f] for r in tent])[~y]) for k, f in (("source_disagreement", "disagree"), ("top_share", "top"), ("positive_rate", "pos"))}
aucs["uncertainty"] = auroc(1 - np.array([r["conf"] for r in tent])[y], 1 - np.array([r["conf"] for r in tent])[~y])
report = dict(threshold=th, strict_threshold=strict_th, n_streams=len(rows), fallback=[r["key"] for r in rows if r["fallback"]], primary=P, control=C, balanced_wr=BW, checks=checks, table=table, tent_auroc_no_by_class=aucs)
json.dump(dict(report=report, rows=rows), open(f"{DIR}/analysis.json", "w"), indent=1)
print(json.dumps(dict(primary=P, control=C, balanced_wr=BW, checks=checks, aucs=aucs), indent=0))

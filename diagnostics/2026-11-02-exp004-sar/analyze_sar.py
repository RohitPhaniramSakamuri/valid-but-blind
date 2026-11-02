"""SAR extension analysis. Frozen before any SAR stream ran. Monitor and strict-violation definitions are unchanged; calibration values
come from the factorial run so all comparators share them.

S1: GAP EXTENDS TO SAR if SAR (recalibrated) is missed more than source in at least 5 scored models with pooled gap >= 0.25. Otherwise
NOT SHOWN. INCONCLUSIVE under 5 scored models (a model is scored with at least 5 strict violations in both arms), or if any model has
fewer than 32 SAR streams when analyzed; a partial run is reported only as incomplete. (Cutoff removed by amendment before any stream ran.)
Descriptive: SAR fixed vs source; SAR vs BN and vs Tent 1e-3, recalibrated; error split; kept share; resets; paired draws.
"""
import json
import os
import sys
from multiprocessing import Pool

import numpy as np

M_DIR = sys.argv[1] if len(sys.argv) > 1 else "factorial"
sys.path.insert(0, ".")
from analyze_all import ALPHA_L1, MODELS, compare, score  # noqa: E402


def load(path, m, r0, L1, jobs, arms=None):
    for line in open(path) if os.path.exists(path) else []:
        s = json.loads(line)
        if arms and s["arm"] not in arms:
            continue
        s["model"] = m
        if s["arm"] == "source":
            s.pop("pos_recal", None)
            s.pop("pfn_recal", None)
        jobs.append((s, r0, L1))


jobs, cal = [], {}
for m in MODELS:
    c = json.load(open(f"{M_DIR}/results_{m}/calibration.json"))
    cal[m] = c
    L1 = c["false_alarm0"] + (np.log(2) - np.log(ALPHA_L1)) / (2 * c["n_calib"])
    load(f"{M_DIR}/results_{m}/streams.jsonl", m, c["r0"], L1, jobs, ("source", "bn", "tent1e-3"))
    load(f"results_sar_{m}/streams.jsonl", m, c["r0"], L1, jobs)
raw = {(j[0]["model"], j[0]["key"]): j[0] for j in jobs}
with Pool(os.cpu_count()) as pool:
    rows = pool.map(score, jobs, chunksize=8)
counts = {m: sum(r["model"] == m and r["arm"] == "sar" for r in rows) for m in MODELS}
complete = all(v == 32 for v in counts.values())
s1 = compare(rows, "sar", "recal", "source", "fixed", 0.25)
verdict = "INCOMPLETE" if not complete else "INCONCLUSIVE" if s1["met"] is None else "GAP EXTENDS TO SAR" if s1["met"] else "NOT SHOWN"


def split(arm, form):
    out = {}
    per = []
    for m in MODELS:
        g = [r for r in rows if r["model"] == m and r["arm"] == arm and r["strict"]]
        if not g:
            continue
        v = []
        for r in g:
            s = raw[(m, r["key"])]
            err, pos, un = np.mean(s["err"]), np.mean(s[f"pos_{form}"]), np.mean(s[f"pfn_{form}"])
            v.append((err, pos, err - un, un, pos - err + un, np.mean(s["conf"])))
        per.append(np.mean(v, axis=0))
    if per:
        out = dict(zip(("err", "flagged", "flagged_wrong", "unflagged_wrong", "flagged_correct", "conf"), np.round(np.mean(per, axis=0), 3).tolist()))
    return out


def paired(a, af, b, bf):
    pick = lambda arm: {(r["model"], r["key"].split("/", 1)[1]): r for r in rows if r["arm"] == arm and r["strict"]}
    A, B = pick(a), pick(b)
    both = [(A[k], B[k]) for k in A if k in B]
    return dict(draws=len(both), a_only_missed=sum(not x[f"alarm_{af}"] and y[f"alarm_{bf}"] for x, y in both), b_only_missed=sum(x[f"alarm_{af}"] and not y[f"alarm_{bf}"] for x, y in both))


sr = [r for r in rows if r["arm"] == "sar"]
sar_raw = [raw[(r["model"], r["key"])] for r in sr]
rep = dict(verdict=verdict, counts=counts, s1=s1, sar_fixed_vs_source=compare(rows, "sar", "fixed", "source", "fixed", 0.25), sar_vs_bn=compare(rows, "sar", "recal", "bn", "recal", 0.15), sar_vs_tent=compare(rows, "sar", "recal", "tent1e-3", "recal", 0.0),
           split={f"{a}/{f}": split(a, f) for a, f in (("source", "fixed"), ("bn", "recal"), ("sar", "recal"), ("sar", "fixed"), ("tent1e-3", "recal"))},
           paired=dict(sar_vs_source=paired("sar", "recal", "source", "fixed"), sar_vs_bn=paired("sar", "recal", "bn", "recal")),
           sar=dict(n=len(sr), strict=sum(r["strict"] for r in sr), collapsed=sum(r["collapsed"] for r in sr), err=float(np.mean([r["err"] for r in sr])) if sr else None, kept=float(np.mean([s["kept"] for s in sar_raw])) if sr else None, resets=int(sum(s["resets"] for s in sar_raw)), fallbacks=sum(bool(r.get("fallback_recal") or r.get("fallback_fixed")) for r in sr)))
json.dump(dict(report=rep, rows=sr), open("sar_report.json", "w"), indent=1)
print(json.dumps(rep, indent=0))

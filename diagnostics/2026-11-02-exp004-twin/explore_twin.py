"""Exploratory, written after the twin verdict; enters no rule. Stress checks on the selected statistic (w=1, c=1), held-out streams."""
import json
import os
from multiprocessing import Pool

import numpy as np
from analyze_twin import ALPHA, AL1, MODELS, lower

K = "a1.0_1"
CHEAP = {}


def job(a):
    s, m, cal = a
    C = np.asarray(s["cells"])
    err = C[4:8].sum(0)
    z = np.clip(C[3] + C[7] + C[2] + C[6] + C[0] + C[4], 0, 1)
    L = cal["fp_twin"] + cal["fn_twin"] + (np.log(2) - np.log(AL1)) / (2 * cal["n_calib"])
    b = np.maximum(lower(z) - L, 0) - cal["r0"]
    tw = np.asarray(s["twin_err"]).mean()
    h = len(err) // 2
    return dict(model=m, key=s["key"], split=s["split"], kind=s["kind"], M=float(b.max()), z=float(z.mean()), L=float(L), err=float(err.mean()), twin_ex=float(tw - cal["r0"]), tent_better=float(tw - err.mean()), t_err_only=float(C[5].mean() + C[4].mean()))


jobs = []
for m in MODELS:
    cal = json.load(open(f"results_twin_{m}/calibration.json"))
    for line in open(f"results_twin_{m}/streams.jsonl"):
        jobs.append((json.loads(line), m, cal))
with Pool(os.cpu_count()) as p:
    extra = {(r["model"], r["key"]): r for r in p.map(job, jobs, chunksize=4)}
rows = json.load(open("twin_report.json"))["rows"]
H = [r | extra[(r["model"], r["key"])] for r in rows if r["split"] == "held"]
out = {}


def tab(name, g):
    out[name] = dict(n=len(g), alarms=sum(r[K] for r in g), share=round(sum(r[K] for r in g) / max(len(g), 1), 3))


L, S = 0.10, 0.15
tab("tent_safe_twin_below_alarm", [r for r in H if r["safe"] and r["twin_ex"] < L])
tab("tent_safe_twin_band", [r for r in H if r["safe"] and L <= r["twin_ex"] < S])
tab("tent_safe_twin_strict", [r for r in H if r["safe"] and r["twin_ex"] >= S])
tab("tent_strict_twin_strict", [r for r in H if r["strict"] and r["twin_ex"] >= S])
tab("tent_strict_twin_band", [r for r in H if r["strict"] and L <= r["twin_ex"] < S])
tab("tent_strict_twin_below_alarm", [r for r in H if r["strict"] and r["twin_ex"] < L])
tab("all_strict_including_balanced", [r for r in H if r["strict"]])
for kind in ("dirichlet", "balanced_wr"):
    tab(f"strict_{kind}", [r for r in H if r["strict"] and r["kind"] == kind])
st = [r for r in H if r["strict"] and r["kind"] == "dirichlet"]
out["bound_above_tent_error_share"] = {m: round(float(np.mean([r["z"] - r["L"] > r["err"] for r in H if r["model"] == m])), 3) for m in MODELS}
out["bound_above_tent_error_mean_excess"] = round(float(np.mean([r["z"] - r["L"] - r["err"] for r in H if r["z"] - r["L"] > r["err"]])), 3)
out["tent_better_than_twin"] = dict(dirichlet=round(float(np.mean([r["tent_better"] for r in H if r["kind"] == "dirichlet"])), 3), balanced=round(float(np.mean([r["tent_better"] for r in H if r["kind"] == "balanced_wr"])), 3), max=round(float(max(r["tent_better"] for r in H)), 3), share_over_5pts=round(float(np.mean([r["tent_better"] > 0.05 for r in H])), 3), share_over_10pts=round(float(np.mean([r["tent_better"] > 0.10 for r in H])), 3))
base = {(r["model"], r["key"].split("/", 1)[1]): r for r in json.load(open("../2026-11-01-exp004-mechanism/factorial_report.json"))["rows"] if r["arm"] == "tent1e-3"}
pairs = [(r, base[(r["model"], "/".join(r["key"].split("/")[2:4]) + "/dirichlet/0.1/" + r["key"].split("/")[4])]) for r in H if r["kind"] == "dirichlet" and r["key"].split("/")[2] != "clean"]
out["same_draw_err_diff_median"] = round(float(np.median([abs(a["err"] - b["err"]) for a, b in pairs])), 4)
out["same_draw_err_diff_max"] = round(float(max(abs(a["err"] - b["err"]) for a, b in pairs)), 4)
both = [(a, b) for a, b in pairs if a["strict"] and b["strict"]]
out["paired_both_strict"] = dict(draws=len(both), fix_only_missed=sum(not a[K] and b["alarm_recal"] for a, b in both), released_only_missed=sum(a[K] and not b["alarm_recal"] for a, b in both), both_missed=sum(not a[K] and not b["alarm_recal"] for a, b in both), both_alarm=sum(a[K] and b["alarm_recal"] for a, b in both))
safe_b = [(a, b) for a, b in pairs if a["safe"]]
out["false_alarms_same_safe_dirichlet"] = dict(n=len(safe_b), fix=sum(a[K] for a, b in safe_b), released=sum(b["alarm_recal"] for a, b in safe_b))
rng = np.random.default_rng(20261102)
per = {m: (sum(not r[K] for r in st if r["model"] == m), sum(r["model"] == m for r in st), sum(not b["alarm_recal"] for b in [x for (mm, _), x in base.items() if mm == m and x["strict"]]), sum(1 for (mm, _), x in base.items() if mm == m and x["strict"])) for m in MODELS}
arr = np.array([per[m] for m in MODELS], float)
d = rng.integers(0, 6, (4000, 6))
t = arr[d].sum(1)
g = t[:, 2] / t[:, 3] - t[:, 0] / t[:, 1]
out["drop_model_bootstrap"] = dict(drop=round(float(arr[:, 2].sum() / arr[:, 3].sum() - arr[:, 0].sum() / arr[:, 1].sum()), 3), ci=np.round(np.percentile(g, [2.5, 97.5]), 3).tolist())
SAME = ["Addepalli2021Towards_PARN18", "Addepalli2021Towards_WRN34", "Addepalli2022Efficient_WRN_34_10"]


def auroc(a, b):
    a, b = np.asarray(a)[:, None], np.asarray(b)[None, :]
    return float((a > b).mean() + 0.5 * (a == b).mean())


sep = {}
for m in MODELS:
    s0 = [r["M"] for r in H if r["model"] == m and r["safe"] and r["kind"] == "dirichlet"]
    s1 = [r["M"] for r in st if r["model"] == m]
    if len(s0) >= 5 and len(s1) >= 5:
        lv = np.quantile(s0, 0.95)
        sep[m] = dict(auroc=round(auroc(s1, s0), 3), missed_5pct=[int(sum(x <= lv for x in s1)), len(s1)], safe=len(s0))
out["separation_dirichlet"] = sep
out["same_three_mean_auroc"] = round(float(np.mean([sep[m]["auroc"] for m in SAME if m in sep])), 3)
out["same_three_matched"] = np.sum([sep[m]["missed_5pct"] for m in SAME if m in sep], axis=0).tolist()
out["per_model_excess"] = {m: dict(tent_strict_excess=round(float(np.mean([r["excess"] for r in st if r["model"] == m])), 3), twin_excess=round(float(np.mean([r["twin_ex"] for r in st if r["model"] == m])), 3), z=round(float(np.mean([r["z"] for r in st if r["model"] == m])), 3), L=round(float(np.mean([r["L"] for r in st if r["model"] == m])), 3)) for m in MODELS}
json.dump(out, open("explore_twin.json", "w"), indent=1)
for k, v in out.items():
    print(k, v)

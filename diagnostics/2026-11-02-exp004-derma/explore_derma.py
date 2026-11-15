"""Exploratory, after the DermaMNIST verdicts; enters no rule. Saved report only."""
import json
from scipy.stats import beta
import numpy as np
R = json.load(open("derma_report.json"))["rows"]
H = [r for r in R if r["split"] == "held"]
idx = lambda a: {r["key"]: r for r in H if r["arm"] == a}
def cp(k, n):
    return [round(float(beta.ppf(.025, k, n-k+1)), 3) if k else 0.0, round(float(beta.ppf(.975, k+1, n-k)), 3) if k < n else 1.0]
out = {}
for b in ("source", "bn"):
    T, O = idx("tent1e-3"), idx(b)
    both = [(T[k], O[k]) for k in T if T[k]["strict"] and O[k]["strict"]]
    out[f"paired_vs_{b}"] = dict(draws=len(both), tent_only_missed=sum(x["first"]["released"] is None and y["first"]["released"] is not None for x, y in both), other_only_missed=sum(x["first"]["released"] is not None and y["first"]["released"] is None for x, y in both), both_missed=sum(x["first"]["released"] is None and y["first"]["released"] is None for x, y in both), err_diff=round(float(np.mean([x["err"]-y["err"] for x, y in both])), 3) if both else None, flagged_diff=round(float(np.mean([x["flagged"]-y["flagged"] for x, y in both])), 3) if both else None, conf_diff=round(float(np.mean([x["conf"]-y["conf"] for x, y in both])), 3) if both else None)
T = [r for r in H if r["arm"] == "tent1e-3" and r["strict"]]
out["paired_twin_vs_released_on_tent"] = dict(draws=len(T), twin_only_missed=sum(r["first"]["twin"] is None and r["first"]["released"] is not None for r in T), released_only_missed=sum(r["first"]["twin"] is not None and r["first"]["released"] is None for r in T), both_missed=sum(r["first"]["twin"] is None and r["first"]["released"] is None for r in T))
out["strict_excess"] = {a: round(float(np.mean([r["excess"] for r in H if r["arm"] == a and r["strict"]])), 3) for a in ("source", "bn", "tent1e-3", "sar")}
out["high_error_excluded"] = {a: dict(n=sum(r["collapsed"] for r in H if r["arm"] == a), **{m: sum(r["first"][m] is not None for r in H if r["arm"] == a and r["collapsed"]) for m in ("released", "twin", "prototype")}) for a in ("source", "bn", "tent1e-3", "sar")}
out["intervals"] = dict(false_alarm_0_of_28=cp(0, 28), twin_missed_17_of_33=cp(17, 33), released_missed_33_of_33=cp(33, 33), source_missed_12_of_44=cp(12, 44))
out["median_first"] = {f"{a}/{m}": (float(np.median([r["first"][m] for r in H if r["arm"] == a and r["strict"] and r["first"][m]])) if any(r["first"][m] for r in H if r["arm"] == a and r["strict"]) else None) for a, m in (("source", "released"), ("tent1e-3", "twin"), ("tent1e-3", "released"))}
k = {(r["corruption"], r["severity"], r["prior"], r["rep"]): r for r in H if r["arm"] == "tent1e-3"}
s = [r for r in T if r["twin_ex"] < 0.10]
out["tent_strict_twin_below_alarm"] = len(s)
out["tent_strict_by_twin_excess"] = dict(twin_strict=[sum(r["first"]["twin"] is not None for r in T if r["twin_ex"] >= .15), sum(r["twin_ex"] >= .15 for r in T)], twin_band=[sum(r["first"]["twin"] is not None for r in T if .10 <= r["twin_ex"] < .15), sum(.10 <= r["twin_ex"] < .15 for r in T)])
json.dump(out, open("explore_derma.json", "w"), indent=1)
for a, b in out.items():
    print(a, b)

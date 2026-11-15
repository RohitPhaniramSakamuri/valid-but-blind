"""Diagnosis A–D of the twin alarm on exp006 (EXPLORATORY, held data already seen)."""
import json, numpy as np, collections
from load7 import load, IDX, cum, conformal
S = load(); G = sorted({(s["ds"], s["model"], s["arm"]) for s in S}); out = {}
tw = lambda s: (cum(s["b"]["flag"]) - s["c"]["r_twin"])[IDX]
# A. margin anatomy
A = {}; when = collections.Counter(); held_safe_fa = []
for g in G:
    dev = [s for s in S if (s["ds"], s["model"], s["arm"]) == g and s["split"] == "dev"]; held = [s for s in S if (s["ds"], s["model"], s["arm"]) == g and s["split"] == "held"]
    sd = [tw(s) for s in dev if s["safe"]]; thr, n = conformal([x.max() for x in sd])
    for x in sd: when[int(IDX[x.argmax()])] += 1
    hs = [tw(s).max() for s in held if s["safe"]]
    A["/".join(g)] = dict(n_safe_dev=n, n_strict_dev=sum(s["strict"] for s in dev), margin=round(thr, 4), dev_safe_max_median=round(float(np.median([x.max() for x in sd])), 4) if sd else None,
                          held_safe_max_median=round(float(np.median(hs)), 4) if hs else None, held_fa=f"{sum(h > thr for h in hs)}/{len(hs)}")
out["A_margins"] = A; out["A_argmax_time_of_safe_dev_max"] = dict(sorted(when.items()))
# variance of running mean over time on safe dev streams (pooled, centred per group)
sdv = []
for g in G:
    X = np.array([tw(s) for s in S if (s["ds"], s["model"], s["arm"]) == g and s["split"] == "dev" and s["safe"]])
    if len(X) > 3: sdv.append(X.std(0))
out["A_safe_dev_sd_by_t"] = dict(zip(map(int, IDX), np.round(np.mean(sdv, 0), 4).tolist()))
# B/C. what the missed strict streams look like (primary arm)
P = [s for s in S if s["arm"] == "tent0.001" and s["split"] == "held"]
thrs = {g: conformal([tw(s).max() for s in S if (s["ds"], s["model"], s["arm"]) == g and s["split"] == "dev" and s["safe"]])[0] for g in G}
rows = []
for s in P:
    if not (s["strict"] or s["safe"]): continue
    th = thrs[(s["ds"], s["model"], s["arm"])]; sc = tw(s); b = s["b"]
    rows.append(dict(kind="strict" if s["strict"] else "safe", alarm=bool(sc.max() > th), ds=s["ds"], model=s["model"], cor=s["cor"], sev=s["sev"], prior=s["prior"],
                     excess=float(s["err"] - s["c"]["r0"]), score_max=float(sc.max()), margin=th, est_err=float(b["flag"].mean()), true_err=s["err"],
                     false_flag=float(b["false_flag"].mean()), hidden=float(b["hidden"].mean()), errW=float(b["errW"].mean()), r_twin=s["c"]["r_twin"]))
def grp(f):
    x = [r for r in rows if f(r)]
    return dict(n=len(x), **{k: round(float(np.mean([r[k] for r in x])), 3) for k in ("excess", "true_err", "est_err", "false_flag", "hidden", "errW", "score_max", "margin")}) if x else dict(n=0)
out["B_profile"] = dict(missed=grp(lambda r: r["kind"] == "strict" and not r["alarm"]), caught=grp(lambda r: r["kind"] == "strict" and r["alarm"]), safe_quiet=grp(lambda r: r["kind"] == "safe" and not r["alarm"]), safe_alarm=grp(lambda r: r["kind"] == "safe" and r["alarm"]))
out["B_missed_by"] = {k: dict(collections.Counter(r[k] for r in rows if r["kind"] == "strict" and not r["alarm"])) for k in ("ds", "cor", "prior", "sev")}
out["B_strict_by_ds_cor"] = {f"{d}/{c}": f"{sum(not r['alarm'] for r in rows if r['kind']=='strict' and r['ds']==d and r['cor']==c)}/{sum(1 for r in rows if r['kind']=='strict' and r['ds']==d and r['cor']==c)}" for d, c in sorted({(r['ds'], r['cor']) for r in rows if r['kind']=='strict'})}
out["B_missed_streams"] = sorted([{k: (round(v, 3) if isinstance(v, float) else v) for k, v in r.items()} for r in rows if r["kind"] == "strict" and not r["alarm"]], key=lambda r: -r["excess"])[:40]
json.dump(out, open("diag_a.json", "w"), indent=1)
for k in ("A_argmax_time_of_safe_dev_max", "A_safe_dev_sd_by_t", "B_profile", "B_missed_by", "B_strict_by_ds_cor"): print(k, json.dumps(out[k]))
print("A_margins (primary arm):"); [print(" ", g, v) for g, v in A.items() if "tent0.001" in g]
print("missed (top 15 by excess):"); [print(" ", r) for r in out["B_missed_streams"][:15]]

import pickle, numpy as np, math
from collections import defaultdict
S = pickle.load(open("cache9.pkl", "rb")); IDX = np.arange(10, 120, 5)
cum = lambda x: np.cumsum(x, 0) / np.arange(1, len(x) + 1)
def conformal(v, a=.05):
    v = np.sort(np.asarray(v, float)); n = len(v); k = math.ceil((n + 1) * (1 - a)); return float(v[k - 1]) if 0 < k <= n else float("inf")
G = defaultdict(list)
for s in S: G[(s["exp"], s["ds"], s["model"][:14], s["arm"])].append(s)
q = lambda v: "[" + " ".join(f"{x:.2f}" for x in np.quantile(v, [.05, .5, .95, 1.])) + "]" if len(v) else "[]"
print("group | r0 r_twin | n dev-safe, level | dev-safe max q05/50/95/100 | held-safe | held-strict | miss FA | mean over stream: held-safe (err-r0, falseflag, hidden) ; held-strict ; dev-safe top5%")
for g, L in sorted(G.items()):
    if not g[3].startswith("tent0.001"): continue
    c = L[0]["c"]; sc = lambda s: (cum(s["b"]["flag"]) - c["r_twin"])[IDX].max()
    ds = [s for s in L if s["split"] == "dev" and s["safe"]]; hs = [s for s in L if s["split"] == "held" and s["safe"]]; hx = [s for s in L if s["split"] == "held" and s["strict"]]
    if len(ds) < 5: print(g, "few dev safe", len(ds)); continue
    lv = conformal([sc(s) for s in ds])
    dec = lambda Q: " ".join(f"{np.mean([s['b'][k].mean() for s in Q]) - (c['r0'] if k == 'errT' else 0):.2f}" for k in ("errT", "false_flag", "hidden")) if Q else "-"
    top = sorted(ds, key=sc)[-max(1, len(ds) // 20):]
    print(g, f"| {c['r0']:.3f} {c['r_twin']:.3f} | {len(ds)} {lv:.3f} | {q([sc(s) for s in ds])} | {len(hs)} {q([sc(s) for s in hs])} | {len(hx)} {q([sc(s) for s in hx])} | {sum(sc(s) <= lv for s in hx)}/{len(hx)} {sum(sc(s) > lv for s in hs)}/{len(hs)} | {dec(hs)} ; {dec(hx)} ; {dec(top)} | top:", ",".join(sorted({s['cor'] + str(s['sev']) + s['prior'] for s in top}))[:150])

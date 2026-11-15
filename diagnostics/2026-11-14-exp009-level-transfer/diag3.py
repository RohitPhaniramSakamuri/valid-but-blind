"""Isolation step 2 (EXPLORATORY): what sets the level? Signal-specific nuisance on safe dev streams, and whether it is shared between the decoupled (twin) and coupled (Tent confidence) channels."""
import json, numpy as np
from scipy.stats import spearmanr
from lib9 import *
S = load(); out = {}
def z(A, ref): return (A - np.median(A[ref], 0)) / (np.quantile(A[ref], .9, 0) - np.quantile(A[ref], .1, 0) + 1e-6)
print("group | rho(twin,doc) safe / strict | top-5% safe by twin: errW-errT, their doc pct-rank | top-5% safe by doc: errW-errT, conf drop, their twin pct-rank | tail ratio twin doc fused | sep twin doc fused")
agg = dict(rs=[], rx=[], tw_gap=[], tw_rank=[], dc_gap=[], dc_rank=[], tail=[], sep=[])
for g, L in groups(S, "tent0.001").items():
    dev = [s for s in L if s["split"] == "dev"]; sf = [i for i, s in enumerate(dev) if s["safe"]]; st = [i for i, s in enumerate(dev) if s["strict"]]
    if len(sf) < 19 or len(st) < 5: continue
    T = np.stack([simple("twin")(s) for s in dev]); D = np.stack([simple("doc")(s) for s in dev]); zt, zd = z(T, sf), z(D, sf); F = (zt + zd) / 2
    mt, md, mf = zt.max(1), zd.max(1), F.max(1); gap = np.array([s["b"]["errW"].mean() - s["b"]["errT"].mean() for s in dev])
    rs = spearmanr(mt[sf], md[sf])[0]; rx = spearmanr(mt[st], md[st])[0]; k = max(1, len(sf) // 20); sf = np.array(sf)
    rank = lambda v, i: float(np.mean([(v[sf] <= v[j]).mean() for j in i]))
    tt = sf[np.argsort(mt[sf])[-k:]]; td = sf[np.argsort(md[sf])[-k:]]
    tail = [float((np.quantile(m[sf], .95) - np.median(m[sf])) / (np.median(m[st]) - np.median(m[sf]))) for m in (mt, md, mf)]
    sep = [auroc(m[st], m[sf]) for m in (mt, md, mf)]
    out["/".join(g)] = dict(rho_safe=rs, rho_strict=rx, twin_top_gap=float(gap[tt].mean()), twin_top_docrank=rank(md, tt), doc_top_gap=float(gap[td].mean()), doc_top_twinrank=rank(mt, td), safe_gap=float(gap[sf].mean()), tail=tail, auroc_dev=sep)
    print(g[0], g[1], g[2][:10], f"| {rs:+.2f} {rx:+.2f} | {gap[tt].mean():+.3f} (all safe {gap[sf].mean():+.3f}) {rank(md, tt):.2f} | {gap[td].mean():+.3f} {rank(mt, td):.2f} | {tail[0]:.2f} {tail[1]:.2f} {tail[2]:.2f} | {sep[0]:.3f} {sep[1]:.3f} {sep[2]:.3f}")
    for k_, v in zip(("rs", "rx", "tw_gap", "tw_rank", "dc_gap", "dc_rank", "tail", "sep"), (rs, rx, gap[tt].mean(), rank(md, tt), gap[td].mean(), rank(mt, td), tail, sep)): agg[k_].append(v)
print("MEAN over groups: rho safe %.2f strict %.2f | twin-top gap %+.3f docrank %.2f | doc-top gap %+.3f twinrank %.2f | tail %s | auroc %s" % (np.mean(agg["rs"]), np.mean(agg["rx"]), np.mean(agg["tw_gap"]), np.mean(agg["tw_rank"]), np.mean(agg["dc_gap"]), np.mean(agg["dc_rank"]), np.round(np.mean(agg["tail"], 0), 3), np.round(np.mean(agg["sep"], 0), 4)))
json.dump(out, open("diag3.json", "w"), indent=1)

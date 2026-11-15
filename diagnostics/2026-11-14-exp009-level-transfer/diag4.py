import numpy as np
from lib9 import *
S = load(); T = [0, 3, 7, 12, 17, 21]
for g, L in groups(S, "tent0.001").items():
    if g[0] != "exp008" and g[1] not in ("organa",): continue
    if g[1] == "cifar" and "PRIME" not in g[2] and "WRN_34_10" not in g[2]: continue
    print("==", g[:3])
    for sig in ("twin", "doc"):
        A = np.stack([simple(sig)(s) for s in L]); sp = np.array([s["split"] for s in L]); sf = np.array([s["safe"] for s in L]); st = np.array([s["strict"] for s in L])
        f = lambda m, q: " ".join(f"{x:+.2f}" for x in np.quantile(A[m], q, 0)[T]) if m.sum() else "-"
        am = lambda m: np.bincount(A[m].argmax(1) // 6, minlength=4) if m.sum() else "-"
        d, h = sp == "dev", sp == "held"
        print(f" {sig:5s} dev-safe q50  {f(d & sf, .5)} | q95 {f(d & sf, .95)} | argmax quartiles {am(d & sf)}")
        print(f"       held-safe q50 {f(h & sf, .5)} | q95 {f(h & sf, .95)} | {am(h & sf)}")
        print(f"       held-strict q10 {f(h & st, .1)} | q50 {f(h & st, .5)} | {am(h & st)}   dev-strict q10 {f(d & st, .1)}")

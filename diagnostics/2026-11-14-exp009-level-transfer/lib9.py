"""exp009 shared helpers. Scores are per-stream arrays over the 22 read-out checkpoints (batch 11, 16, ..., 116)."""
import math, os, pickle
from collections import defaultdict
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); IDX = np.arange(10, 120, 5)
cum = lambda x: np.cumsum(x, 0) / np.arange(1, len(x) + 1).reshape(-1, *([1] * (np.ndim(x) - 1)))
def conformal(v, a=.05):
    v = np.sort(np.asarray(v, float)); n = len(v); k = math.ceil((n + 1) * (1 - a)); return float(v[k - 1]) if 0 < k <= n else float("inf")
def load():
    S = pickle.load(open(f"{HERE}/cache9.pkl", "rb"))
    for i, s in enumerate(S): s["id"] = i; s["g"] = (s["exp"], s["ds"], s["model"], s["arm"])
    return S
def groups(S, arm=None):
    G = defaultdict(list)
    for s in S:
        if arm is None or s["arm"] == arm: G[s["g"]].append(s)
    return dict(sorted(G.items()))
def simple(name):
    def f(s):
        b, c = s["b"], s["c"]
        return dict(twin=lambda: cum(b["flag"]) - c["r_twin"], released=lambda: cum(b["rel"]) - c["r0"], prototype=lambda: cum(b["pro"]) - c["r0"], atc=lambda: cum(b["atc"]) - c["r0"],
                    doc=lambda: c["conf_clean"] - cum(b["confT"]), dropout=lambda: cum(b["dd"]))[name]()[IDX]
    return f
def auroc(pos, neg):
    pos, neg = np.asarray(pos), np.asarray(neg)
    if not len(pos) or not len(neg): return float("nan")
    return float(((pos[:, None] > neg[None]).mean() + .5 * (pos[:, None] == neg[None]).mean()))

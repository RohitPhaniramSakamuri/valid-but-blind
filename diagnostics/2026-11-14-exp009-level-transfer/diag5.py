import json, numpy as np
from scipy.stats import spearmanr
R = json.load(open("harness_rows.json")); sh = lambda x: f"{x[0]}/{x[1]}"
for det in ("twin|G", "fus3|G", "fus_td|G", "doc|Z"):
    Q = [r for r in R if r["det"] == det and r["lofo_miss"][1] >= 5 and r["held_miss"][1] >= 5]
    a = [r["lofo_miss"][0] / r["lofo_miss"][1] for r in Q]; b = [r["held_miss"][0] / r["held_miss"][1] for r in Q]
    fa = [r["lofo_fa"][0] / r["lofo_fa"][1] for r in Q]; fb = [r["held_fa"][0] / max(1, r["held_fa"][1]) for r in Q]
    print(det, "n groups", len(Q), "spearman LOFO-miss vs held-miss %.2f" % spearmanr(a, b)[0], "| LOFO-FA vs held-FA %.2f" % spearmanr(fa, fb)[0])
    if det == "fus3|G":
        for r, x, y in zip(Q, a, b): print("   ", r["exp"], r["ds"], r["model"][:12], f"LOFO miss {sh(r['lofo_miss'])} FA {sh(r['lofo_fa'])} | held miss {sh(r['held_miss'])} FA {sh(r['held_fa'])}")
# selection by LOFO: per group choose detector minimising LOFO miss share + LOFO FA share (ties -> first)
G = sorted({r["g"] for r in R})
for pool in (["twin|G", "atc|G", "doc|G", "dropout|G", "released|G", "fus3|G"], [r for r in sorted({r["det"] for r in R})]):
    tot = {}
    for g in G:
        Q = [r for r in R if r["g"] == g and r["det"] in pool]; best = min(Q, key=lambda r: r["lofo_miss"][0] / max(1, r["lofo_miss"][1]) + r["lofo_fa"][0] / max(1, r["lofo_fa"][1]))
        t = tot.setdefault(best["exp"], [0, 0, 0, 0]); t[0] += best["held_miss"][0]; t[1] += best["held_miss"][1]; t[2] += best["held_fa"][0]; t[3] += best["held_fa"][1]
    print("LOFO-selected from", len(pool), {k: f"{v[0]}/{v[1]} {v[2]}/{v[3]}" for k, v in tot.items()})

import json, numpy as np
R = json.load(open("harness_rows.json")); G = sorted({r["g"] for r in R}); sh = lambda a, b: f"{a}/{b}"
sm = lambda r, k: r[k][0] / max(1, r[k][1])
POOLS = dict(p6=["fus3|G", "twin|G", "doc|G", "atc|G", "dropout|G", "released|G"], p6z=["fus3|G", "twin|G", "doc|Z", "atc|Z", "dropout|Z", "released|Z"], p3=["fus3|G", "twin|G", "doc|G"], p2=["fus3|G", "twin|G"], fus=["fus3|G"], twin=["twin|G"])
CRIT = dict(sum=lambda r: sm(r, "lofo_miss") + sm(r, "lofo_fa"), miss_fa10=lambda r: (sm(r, "lofo_fa") > .10, sm(r, "lofo_miss"), sm(r, "lofo_fa")), wsum=lambda r: sm(r, "lofo_miss") + 2 * sm(r, "lofo_fa"))
for pn, pool in POOLS.items():
    for cn, crit in CRIT.items():
        tot = {}; ch = {}
        for g in G:
            Q = sorted([r for r in R if r["g"] == g and r["det"] in pool], key=lambda r: pool.index(r["det"])); b = min(Q, key=crit)
            for key in (b["exp"], b["exp"] + ":" + b["ds"]):
                t = tot.setdefault(key, [0, 0, 0, 0]); t[0] += b["held_miss"][0]; t[1] += b["held_miss"][1]; t[2] += b["held_fa"][0]; t[3] += b["held_fa"][1]
            ch[b["det"]] = ch.get(b["det"], 0) + 1
        print(f"{pn:5s} {cn:9s}", " ".join(f"{k}: {sh(v[0], v[1])} {sh(v[2], v[3])}" for k, v in tot.items() if ":" not in k), "|", " ".join(f"{k.split(':')[1][:5]} {sh(v[0], v[1])},{sh(v[2], v[3])}" for k, v in tot.items() if ":" in k and "cifar" not in k), "|", ch)
        if pn in ("fus", "twin"): break

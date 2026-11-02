"""Experiment 005 analysis. Written before any data was processed. See the experiment record for the frozen rule."""
import json
import sys
from collections import defaultdict

import numpy as np

path = sys.argv[1] if len(sys.argv) > 1 else "results/streams.jsonl"
out = sys.argv[2] if len(sys.argv) > 2 else "results/analysis.json"
rows = [json.loads(l) for l in open(path)]
SEEDS = (1, 2, 3)
ADAPT = ("bn", "tent", "eta", "blend")
pool = defaultdict(lambda: [np.zeros((2, 2)), np.zeros((2, 2))])
for r in rows:
    c = pool[(r["pool"], r["target"], r["seed"], r["corruption"], r["arm"], r["mix"])]
    c[0] += np.array(r["n"])
    c[1] += np.array(r["k"])


def ba(key, g):
    n, k = pool[key]
    rates = [k[y, g] / n[y, g] for y in (0, 1) if n[y, g] > 0]
    return float(np.mean(rates)) if len(rates) == 2 else float("nan")


def ce(p, t, s, c, a):
    """Mean across groups of BA at 10% share minus BA at 50% share. Group 1 is Male, group 0 is not."""
    male = ba((p, t, s, c, a, "m10"), 1) - ba((p, t, s, c, a, "m50"), 1)
    other = ba((p, t, s, c, a, "m90"), 0) - ba((p, t, s, c, a, "m50"), 0)
    return (male + other) / 2, male, other


def corrs(p):
    return sorted({r["corruption"] for r in rows if r["pool"] == p and r["corruption"] != "clean"})


def did_table(p, t, a):
    return {(s, c): ce(p, t, s, c, a)[0] - ce(p, t, s, c, "source")[0] for s in SEEDS for c in corrs(p)}


def boot(tab, B=4000, seed=0):
    rng = np.random.RandomState(seed)
    ss, cs = sorted({k[0] for k in tab}), sorted({k[1] for k in tab})
    vals = []
    for _ in range(B):
        a, b = rng.choice(ss, len(ss)), rng.choice(cs, len(cs))
        vals.append(np.nanmean([tab[(x, y)] for x in a for y in b]))
    return [round(100 * float(v), 2) for v in np.percentile(vals, [2.5, 97.5])]


report = {"pools": {}}
for p in ("valid", "test"):
    report["pools"][p] = {}
    for t in ("Blond_Hair", "Smiling"):
        block = {}
        for a in ADAPT:
            tab = did_table(p, t, a)
            per_seed = {s: 100 * float(np.nanmean([tab[(s, c)] for c in corrs(p)])) for s in SEEDS}
            per_corr = {c: round(100 * float(np.nanmean([tab[(s, c)] for s in SEEDS])), 2) for c in corrs(p)}
            did = 100 * float(np.nanmean(list(tab.values())))
            ci = boot(tab)
            own = 100 * float(np.nanmean([ce(p, t, s, c, a)[0] for s in SEEDS for c in corrs(p)]))
            src = 100 * float(np.nanmean([ce(p, t, s, c, "source")[0] for s in SEEDS for c in corrs(p)]))
            male = 100 * float(np.nanmean([ce(p, t, s, c, a)[1] - ce(p, t, s, c, "source")[1] for s in SEEDS for c in corrs(p)]))
            other = 100 * float(np.nanmean([ce(p, t, s, c, a)[2] - ce(p, t, s, c, "source")[2] for s in SEEDS for c in corrs(p)]))
            block[a] = dict(did_pp=round(did, 2), ci95=ci, per_seed={str(k): round(v, 2) for k, v in per_seed.items()}, per_corruption=per_corr,
                            ce_arm=round(own, 2), ce_source=round(src, 2), did_male_minority=round(male, 2), did_other_minority=round(other, 2),
                            supported=bool(did <= -2 and ci[1] < 0 and all(v < 0 for v in per_seed.values())))
        desc = {}
        for a in ("source",) + ADAPT:
            for mix in ("natural", "m10", "m50", "m90"):
                ks = [(p, t, s, c, a, mix) for s in SEEDS for c in corrs(p)]
                bam = np.nanmean([ba(k, 1) for k in ks])
                baf = np.nanmean([ba(k, 0) for k in ks])
                cells = defaultdict(list)
                for k in ks:
                    n, c_ = pool[k]
                    for y in (0, 1):
                        for g in (0, 1):
                            if n[y, g] > 0:
                                cells[(y, g)].append(c_[y, g] / n[y, g])
                desc[f"{a}/{mix}"] = dict(ba_male=round(100 * float(bam), 2), ba_other=round(100 * float(baf), 2), gap=round(100 * float(abs(bam - baf)), 2),
                                          cells={f"y{y}g{g}": round(100 * float(np.mean(v)), 1) for (y, g), v in sorted(cells.items())})
        ckeys = [(p, t, s, "clean", "source", "natural") for s in SEEDS]
        block["descriptive"] = desc
        block["clean_source_ba"] = dict(male=round(100 * float(np.nanmean([ba(k, 1) for k in ckeys])), 2), other=round(100 * float(np.nanmean([ba(k, 0) for k in ckeys])), 2))
        report["pools"][p][t] = block
primary = {a: report["pools"]["test"]["Blond_Hair"][a] for a in ("bn", "tent")}
second = {a: report["pools"]["test"]["Smiling"][a] for a in ("bn", "tent")}
report["verdict"] = {a: dict(supported=primary[a]["supported"], generalizes=bool(primary[a]["supported"] and second[a]["supported"])) for a in primary}
json.dump(report, open(out, "w"), indent=1)
print(json.dumps(report["verdict"]))

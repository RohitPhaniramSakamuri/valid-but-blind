"""Frozen before any twin stream ran. Definitions and comparator are unchanged: strict, safe, collapse, alpha 0.15, alarm level r0 + 0.10.
Cells: E Tent wrong, F twin flagged, A agree. Statistic z = P(F,A) + w P(F,not A) + c P(not F,not A); bound = CS(z) - [fp_twin + c fn_twin + (log2-log0.025)/(2n)].
For w = 0, the expected value of the statistic minus the twin's FP (and FN for c = 1) is a lower bound on Tent's error, needing the assumption only on the twin.
For w > 0 the form is heuristic. Candidates: w in {0, .25, .5, .75, 1}, c in {0, 1}.
SELECTION, DEV ONLY (dev labels allowed): among candidates with pooled false alarms on dev safe streams (Dirichlet and balanced) <= 5%, lowest missed share on dev
Dirichlet strict streams; ties to smaller w, then smaller c. If none qualifies, lowest false-alarm share, then lowest missed share.
VERDICT, HELD-OUT, once, for the selected candidate, against the released monitor on the same draws (factorial Tent 1e-3 recalibrated):
FIX WORKS: missed lower in >= 5 of 6 models (>= 5 strict in both, else INCONCLUSIVE under 5 scored), pooled missed share falls by >= 0.40, pooled false alarms on all held-out safe streams (Dirichlet, balanced, clean) <= 10%.
PARTIAL: pooled fall >= 0.20, same false-alarm limit. Otherwise NOT SHOWN. The certified forms (w = 0) are reported whatever is selected.
"""
import itertools
import json
import os
from multiprocessing import Pool

import numpy as np
from confseq.conjmix_bounded import conjmix_empbern_lower_cs
from confseq.predmix import predmix_empbern_lower_cs

MODELS = ["Hendrycks2020AugMix_ResNeXt", "Modas2021PRIMEResNet18", "Hendrycks2020AugMix_WRN", "Addepalli2021Towards_PARN18", "Addepalli2021Towards_WRN34", "Addepalli2022Efficient_WRN_34_10"]
ALPHA, AL1, TOL = 0.15, 0.025, 0.1
CANDS = list(itertools.product((0.0, 0.25, 0.5, 0.75, 1.0), (0, 1)))


def v_opt(x, t):
    m = np.cumsum(x) / np.arange(1, len(x) + 1)
    return np.cumsum((x - np.append(0.5, m[:-1])) ** 2)[t] * t


def lower(x):
    try:
        return np.asarray(conjmix_empbern_lower_cs(x=x, alpha=ALPHA, v_opt=v_opt(x, int(len(x) * 0.25))))
    except RuntimeError:
        return np.asarray(predmix_empbern_lower_cs(x=x, alpha=ALPHA))


def score(a):
    s, m, cal = a
    C = np.asarray(s["cells"])  # index E*4 + F*2 + A
    err = C[4:8].sum(0)
    FA, FnA, nFnA = C[3] + C[7], C[2] + C[6], C[0] + C[4]
    r0 = cal["r0"]
    e, l = err.mean(), err[-len(err) // 4:].mean()
    row = dict(model=m, key=s["key"], split=s["split"], kind=s["kind"], corruption=s["corruption"], err=float(e), excess=float(e - r0), safe=bool(e < r0 + TOL and l < 0.85), strict=bool(e >= r0 + TOL + 0.05 and l < 0.85), collapsed=bool(l >= 0.85), agree=float(C[[1, 3, 5, 7]].sum(0).mean()), twin_err=float(np.mean(s["twin_err"])), flagged=float((C[2:4].sum(0) + C[6:8].sum(0)).mean()), conf=float(np.mean(s["conf"])), conf_twin=float(np.mean(s["conf_twin"])))
    for w, c in CANDS:
        z = np.clip(FA + w * FnA + c * nFnA, 0, 1)
        L = cal["fp_twin"] + c * cal["fn_twin"] + (np.log(2) - np.log(AL1)) / (2 * cal["n_calib"])
        b = np.maximum(lower(z) - L, 0)
        hit = np.where(b > r0 + TOL)[0]
        row[f"a{w}_{c}"] = bool(len(hit))
        row[f"t{w}_{c}"] = int(hit[0]) + 1 if len(hit) else None
        # Validity of the stream-average bound against Tent's actual error.
        row[f"v{w}_{c}"] = bool(z.mean() - L <= e)
    return row


if __name__ == "__main__":
    jobs = []
    for m in MODELS:
        cal = json.load(open(f"results_twin_{m}/calibration.json"))
        for line in open(f"results_twin_{m}/streams.jsonl"):
            jobs.append((json.loads(line), m, cal))
    with Pool(os.cpu_count()) as p:
        rows = p.map(score, jobs, chunksize=4)

    def stat(cand, split):
        k = f"a{cand[0]}_{cand[1]}"
        g = [r for r in rows if r["split"] == split]
        safe = [r for r in g if r["safe"]]
        st = [r for r in g if r["strict"] and r["kind"] == "dirichlet"]
        allst = [r for r in g if r["strict"]]
        coll = [r for r in g if r["collapsed"]]
        return dict(w=cand[0], c=cand[1], safe=len(safe), false_alarms=sum(r[k] for r in safe), strict=len(st), missed=sum(not r[k] for r in st), strict_all=len(allst), missed_all=sum(not r[k] for r in allst), collapsed=len(coll), collapsed_alarmed=sum(r[k] for r in coll), bound_valid=float(np.mean([r[f"v{cand[0]}_{cand[1]}"] for r in g])))

    dev = [stat(c, "dev") for c in CANDS]
    ok = [d for d in dev if d["false_alarms"] / max(d["safe"], 1) <= 0.05]
    pick = sorted(ok, key=lambda d: (d["missed"] / max(d["strict"], 1), d["w"], d["c"]))[0] if ok else sorted(dev, key=lambda d: (d["false_alarms"] / max(d["safe"], 1), d["missed"] / max(d["strict"], 1), d["w"], d["c"]))[0]
    chosen = (pick["w"], pick["c"])
    base = {(r["model"], r["key"].split("/", 1)[1]): r for r in json.load(open("factorial/factorial_report.json"))["rows"] if r["arm"] == "tent1e-3"}
    k = f"a{chosen[0]}_{chosen[1]}"
    held = [r for r in rows if r["split"] == "held"]
    per, scored, higher = {}, [], 0
    for m in MODELS:
        g = [r for r in held if r["model"] == m and r["kind"] == "dirichlet" and r["strict"]]
        mine = sum(not r[k] for r in g)
        ks = [(m, "/".join(r["key"].split("/")[2:4]) + "/dirichlet/0.1/" + r["key"].split("/")[4]) for r in held if r["model"] == m and r["kind"] == "dirichlet"]
        b = [base[x] for x in ks if x in base and base[x]["strict"]]
        rel = sum(not x["alarm_recal"] for x in b)
        per[m] = dict(fix=[mine, len(g)], released=[rel, len(b)], certified0=[sum(not r["a0.0_0"] for r in g), len(g)], certified1=[sum(not r["a0.0_1"] for r in g), len(g)])
        if len(g) >= 5 and len(b) >= 5:
            scored.append(m)
            higher += mine / len(g) < rel / len(b)
    fm, fn = sum(per[m]["fix"][0] for m in scored), sum(per[m]["fix"][1] for m in scored)
    bm, bn = sum(per[m]["released"][0] for m in scored), sum(per[m]["released"][1] for m in scored)
    safe = [r for r in held if r["safe"]]
    fa = sum(r[k] for r in safe)
    drop = bm / max(bn, 1) - fm / max(fn, 1)
    okfa = fa / max(len(safe), 1) <= 0.10
    verdict = "INCONCLUSIVE" if len(scored) < 5 else "FIX WORKS" if higher >= 5 and drop >= 0.40 and okfa else "PARTIAL" if drop >= 0.20 and okfa else "NOT SHOWN"
    held_all = [stat(c, "held") for c in CANDS]
    delay = [r[f"t{chosen[0]}_{chosen[1]}"] for r in held if r["strict"] and r["kind"] == "dirichlet" and r[k]]
    rep = dict(verdict=verdict, chosen=chosen, dev=dev, dev_pick=pick, scored=len(scored), models_lower=int(higher), fix=[fm, fn], released=[bm, bn], drop=drop, held_safe=len(safe), held_false_alarms=fa, held_safe_by_kind={kk: [sum(r[k] for r in safe if r["kind"] == kk and r["corruption"] != "clean"), sum(1 for r in safe if r["kind"] == kk and r["corruption"] != "clean")] for kk in ("dirichlet", "balanced_wr")}, clean_safe=[sum(r[k] for r in safe if r["corruption"] == "clean"), sum(1 for r in safe if r["corruption"] == "clean")], per=per, held_all=held_all, median_first_alarm=float(np.median(delay)) if delay else None,
               means={kk: {x: round(float(np.mean([r[x] for r in held if r["kind"] == kk and r["strict"]] or [0])), 3) for x in ("err", "twin_err", "agree", "flagged", "conf", "conf_twin")} for kk in ("dirichlet", "balanced_wr")}, n=len(rows))
    json.dump(dict(report=rep, rows=rows), open("twin_report.json", "w"), indent=1)
    print(json.dumps({a: rep[a] for a in rep if a not in ("dev", "held_all")}, indent=0))
    for d in dev:
        print("dev", d)
    for d in held_all:
        print("held", d)

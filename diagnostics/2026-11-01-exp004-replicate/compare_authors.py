"""Exploratory, written after the verdict. Two label-using offline summaries; neither enters any rule.

1. Applies analyze_confirm's monitor formula to per-batch outputs saved by the authors' code, beside the port's
   development result for the same corruption. Streams differ (authors: 10,000 images once; port: 4,000 IDs for three epochs).
2. Compares Tent and source quantities on replication draws, to look at where the alarm gap comes from.
"""
import glob
import json
import re

import numpy as np
import torch
from confseq.conjmix_bounded import conjmix_empbern_lower_cs

ALPHA_CS, ALPHA_L1, TOL = 0.15, 0.025, 0.1


def v_opt(x, t):
    m = np.cumsum(x) / np.arange(1, len(x) + 1)
    return np.cumsum((x - np.append(0.5, m[:-1])) ** 2)[t] * t


def loaded(p):
    return torch.load(p, map_location="cpu")


out = {}
for order in ("uniform", "by_class"):
    root = f"authors_out/saved/cifar100/tent_authors_{order}"
    cal = loaded(f"{root}/calib.pt")
    if order == "uniform":
        print({k: (v.shape if hasattr(v, "shape") else type(v).__name__) for k, v in cal.items()})
    E, proxy = cal["E"].float().cpu(), cal["E_hat"].float().cpu()
    q0 = float(cal["q_hat"]) if "q_hat" in cal else None
    r0, fa0 = float(E.mean()), float(((proxy > q0) & (E < 0.5)).float().mean())
    n = len(glob.glob(f"{root}/gaussian_noise/5/*_output_*.pt"))
    err, pos = [], []
    for i in range(n):
        lg, y, q = (loaded(f"{root}/gaussian_noise/5/1None_{s}_{i}.pt") for s in ("output", "labels", "qhat"))
        u = 1 - lg.softmax(1).max(1).values
        err.append(float((lg.argmax(1) != y).float().mean()))
        pos.append(float((u > float(q)).float().mean()))
    x = np.array(pos)
    cs = np.asarray(conjmix_empbern_lower_cs(x=x, alpha=ALPHA_CS, v_opt=v_opt(x, int(n * 0.25))))
    w = (np.log(2) - np.log(ALPHA_L1)) / (2 * len(E))
    bound = np.maximum(cs - (fa0 + w), 0)
    hit = np.where(bound > r0 + TOL)[0]
    out[f"authors/{order}"] = dict(batches=n, r0=r0, q0=q0, false_alarm0=fa0, err=float(np.mean(err)), last_quarter_err=float(np.mean(err[-n // 4:])), pos=float(x.mean()),
                                   final_bound=float(bound[-1]), alarm=bool(len(hit)), first_alarm=int(hit[0]) if len(hit) else None)


comparison = {}
for path in glob.glob("results_*/streams.jsonl"):
    model = re.sub(r"results_|/streams.jsonl", "", path)
    cal = json.load(open(path.replace("streams.jsonl", "calibration.json")))
    rows = [json.loads(l) for l in open(path)]
    stat = {}
    for arm in ("tent", "source"):
        g = [r for r in rows if r["arm"] == arm and np.mean(r["err"]) >= cal["r0"] + 0.15 and np.mean(r["err"][-30:]) < 0.85]
        stat[arm] = {k: round(float(np.mean([np.mean(r[k]) for r in g])), 3) for k in ("err", "pos", "pfa", "pfn", "q_hat", "conf")}
    comparison[model] = dict(r0=round(cal["r0"], 3), q0=round(cal["q_hat0"], 3), **stat)
out["strict_stream_means"] = comparison
json.dump(out, open("authors_comparison.json", "w"), indent=1)
print(json.dumps(out, indent=0))

"""Robustness and exploratory follow-up to the Experiment 004 gate; run after seeing it.

Strict violation: final running error at least threshold + 0.05, on noncollapsed streams.
Exploratory signal check: how well simple label-free signals separate strict violations.
"""
import json
from collections import defaultdict

import numpy as np

d = json.load(open("results_monitor/analysis.json"))
rows = d["rows"]
raw = {}
for line in open("results_monitor/streams.jsonl"):
    s = json.loads(line)
    raw[s["key"]] = s
cal = json.load(open("results_monitor/calibration.json"))
th = d["report"]["threshold"]
out = {"threshold": th, "strict_threshold": th + 0.05, "false_alarm0": cal["false_alarm0"], "q_hat0": cal["q_hat0"], "groups": {}}
g = defaultdict(list)
for r in rows:
    g[(r["arm"], r["kind"], "clean" if r["corruption"] == "clean" else "corrupted")].append(r)
for k, v in sorted(g.items()):
    strict = [r for r in v if r["mean_err"] >= th + 0.05 and not r["collapsed"]]
    s = [raw[r["key"]] for r in v]
    out["groups"]["/".join(k)] = dict(n=len(v), strict_violating=len(strict), strict_missed=sum(not r["alarm_released"] for r in strict),
        strict_missed_sqrt=sum(not r["alarm_sqrt"] for r in strict), mean_err=round(np.mean([r["mean_err"] for r in v]), 3),
        mean_conf=round(np.mean([r["mean_conf"] for r in v]), 3), mean_pos=round(np.mean([r["mean_pos"] for r in v]), 3),
        mean_q_hat=round(float(np.mean([np.mean(x["q_hat"]) for x in s])), 3), top_share=round(np.mean([r["mean_top_share"] for r in v]), 3),
        disagree=round(float(np.mean([np.mean(x["disagree"]) for x in s])), 3), pfn=round(np.mean([r["mean_pfn"] for r in v]), 3),
        pfa=round(np.mean([r["mean_pfa"] for r in v]), 3), assumption_fail_share=round(np.mean([r["assumption_fail_share"] for r in v]), 3))


def auroc(pos, neg):
    if not len(pos) or not len(neg):
        return None
    return round(float(np.mean([(p > n) + 0.5 * (p == n) for p in pos for n in neg])), 3)


tent = [r for r in rows if r["arm"] == "tent" and not r["collapsed"]]
y = np.array([r["mean_err"] >= th + 0.05 for r in tent])
sig = dict(uncertainty=[1 - r["mean_conf"] for r in tent], monitor_positive_rate=[r["mean_pos"] for r in tent],
           source_disagreement=[np.mean(raw[r["key"]]["disagree"]) for r in tent], top_share=[r["mean_top_share"] for r in tent])
out["tent_auroc_strict_violation"] = {k: auroc(np.array(v)[y], np.array(v)[~y]) for k, v in sig.items()}
out["tent_counts"] = dict(n=len(tent), strict=int(y.sum()))
sub = [r for r in tent if r["kind"] in ("balanced", "dirichlet", "easy")]
ys = np.array([r["mean_err"] >= th + 0.05 for r in sub])
sigs = dict(uncertainty=[1 - r["mean_conf"] for r in sub], source_disagreement=[np.mean(raw[r["key"]]["disagree"]) for r in sub], top_share=[r["mean_top_share"] for r in sub])
out["tent_auroc_without_by_class"] = {k: auroc(np.array(v)[ys], np.array(v)[~ys]) for k, v in sigs.items()}
json.dump(out, open("results_monitor/robustness.json", "w"), indent=1)
print(json.dumps(out, indent=0))

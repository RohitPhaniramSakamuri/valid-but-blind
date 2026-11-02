"""Experiment 004 analysis. Written before any stream was run.

Monitor, following plotting_utils.compute_quantities at the pinned commit:
L_t = max(conjmix lower CS on positive rate, alpha 0.15, minus L_1, 0); alarm if L_t > r0 + 0.1.
"released" uses the repository's L_1 width, (log 2 - log alpha) / (2n).
"sqrt" uses the Hoeffding width, sqrt of that quantity, as a sensitivity check only.

Truth, from evaluator labels: a stream violates if running error exceeds r0 + 0.1 at any t >= 10.
Collapsed: mean error over the last quarter of the stream is at least 0.85.

Gate: passes if at least two cells show missed alarms >= 20% on violating noncollapsed streams,
or false alarms >= 10% on non-violating clean streams, with exact 95% lower bound above zero.
A cell is one stream kind and severity, pooling arms and corruptions. Clean streams form one cell per kind.
"""
import argparse
import json
from collections import defaultdict

import numpy as np
from confseq.conjmix_bounded import conjmix_empbern_lower_cs
from confseq.predmix import predmix_empbern_lower_cs
from scipy.stats import beta

ALPHA_CS, ALPHA_L1, TOL, T_MIN = 0.15, 0.025, 0.1, 10


def v_opt(x, t):
    x = np.asarray(x)
    means = np.cumsum(x) / np.arange(1, len(x) + 1)
    previous = np.append(0.5, means[:-1])
    return np.cumsum((x - previous) ** 2)[t] * t


def lower(n_success, n):
    return 0.0 if n_success == 0 else float(beta.ppf(0.025, n_success, n - n_success + 1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="results_monitor")
    args = ap.parse_args()
    cal = json.load(open(f"{args.dir}/calibration.json"))
    streams = [json.loads(l) for l in open(f"{args.dir}/streams.jsonl")]
    n = cal["n_calib"]
    width = (np.log(2) - np.log(ALPHA_L1)) / (2 * n)
    threshold = cal["r0"] + TOL
    rows = []
    for s in streams:
        x = np.array(s["pos"])
        T = len(x)
        # A numerical failure in one stream falls back to the repository's other option, and is flagged.
        try:
            cs = np.asarray(conjmix_empbern_lower_cs(x=x, alpha=ALPHA_CS, v_opt=v_opt(x, int(T * 0.25))))
            fallback = False
        except RuntimeError:
            cs = np.asarray(predmix_empbern_lower_cs(x=x, alpha=ALPHA_CS))
            fallback = True
        running = np.cumsum(s["err"]) / np.arange(1, T + 1)
        viol_t = np.where((running > threshold) & (np.arange(T) >= T_MIN))[0]
        out = dict(key=s["key"], arm=s["arm"], corruption=s["corruption"], severity=s["severity"], kind=s["kind"],
                   mean_err=float(np.mean(s["err"])), last_err=float(np.mean(s["err"][-T // 4:])),
                   violates=bool(len(viol_t)), violate_t=int(viol_t[0]) if len(viol_t) else None,
                   mean_conf=float(np.mean(s["conf"])), mean_top_share=float(np.mean(s["top_share"])),
                   mean_pos=float(x.mean()), cs_fallback=fallback)
        out["collapsed"] = out["last_err"] >= 0.85
        pfa, pfn = np.cumsum(s["pfa"]) / np.arange(1, T + 1), np.cumsum(s["pfn"]) / np.arange(1, T + 1)
        margin = pfn + cal["false_alarm0"] - pfa
        out["assumption_fail_share"] = float((margin[T_MIN:] < 0).mean())
        out["mean_pfn"], out["mean_pfa"] = float(pfn[-1]), float(pfa[-1])
        for name, w in (("released", width), ("sqrt", np.sqrt(width))):
            bound = np.maximum(cs - (cal["false_alarm0"] + w), 0)
            alarm_t = np.where(bound > threshold)[0]
            out[f"alarm_{name}"] = bool(len(alarm_t))
            out[f"alarm_t_{name}"] = int(alarm_t[0]) if len(alarm_t) else None
            out[f"final_gap_{name}"] = float(running[-1] - bound[-1])
        rows.append(out)

    report = dict(threshold=threshold, r0=cal["r0"], n_streams=len(rows), l1_width_released=width, l1_width_sqrt=float(np.sqrt(width)), cells={}, by_arm={})
    gates = defaultdict(lambda: dict(passing=[]))
    for name in ("released", "sqrt"):
        cells = defaultdict(list)
        for r in rows:
            cells[(r["kind"], "clean" if r["corruption"] == "clean" else r["severity"])].append(r)
        table = {}
        for (kind, sev), g in sorted(cells.items(), key=str):
            v = [r for r in g if r["violates"] and not r["collapsed"]]
            b = [r for r in g if not r["violates"]]
            miss = sum(not r[f"alarm_{name}"] for r in v)
            fa = sum(r[f"alarm_{name}"] for r in b)
            delays = [r[f"alarm_t_{name}"] - r["violate_t"] for r in v if r[f"alarm_{name}"]]
            entry = dict(n=len(g), violating_noncollapsed=len(v), collapsed=sum(r["collapsed"] for r in g), missed=miss,
                         missed_rate=round(miss / len(v), 3) if v else None, missed_lower95=round(lower(miss, len(v)), 3) if v else None,
                         benign=len(b), false_alarms=fa, false_alarm_rate=round(fa / len(b), 3) if b else None,
                         false_alarm_lower95=round(lower(fa, len(b)), 3) if b else None,
                         median_delay=float(np.median(delays)) if delays else None,
                         mean_err=round(float(np.mean([r["mean_err"] for r in g])), 3),
                         mean_final_gap=round(float(np.mean([r[f"final_gap_{name}"] for r in g])), 3),
                         mean_assumption_fail_share=round(float(np.mean([r["assumption_fail_share"] for r in g])), 3))
            table[f"{kind}/{sev}"] = entry
            if v and miss / len(v) >= 0.2 and lower(miss, len(v)) > 0:
                gates[name]["passing"].append(f"missed:{kind}/{sev}")
            if sev == "clean" and b and fa / len(b) >= 0.1 and lower(fa, len(b)) > 0:
                gates[name]["passing"].append(f"false_alarm:{kind}/{sev}")
        report["cells"][name] = table
        gates[name]["passed"] = len(gates[name]["passing"]) >= 2
    report["gate"] = dict(gates)
    for arm in ("source", "tent"):
        g = [r for r in rows if r["arm"] == arm]
        report["by_arm"][arm] = dict(mean_err=round(float(np.mean([r["mean_err"] for r in g])), 3), violating=sum(r["violates"] for r in g), collapsed=sum(r["collapsed"] for r in g),
                                     missed_released=sum(r["violates"] and not r["collapsed"] and not r["alarm_released"] for r in g),
                                     missed_sqrt=sum(r["violates"] and not r["collapsed"] and not r["alarm_sqrt"] for r in g),
                                     false_alarm_released=sum(not r["violates"] and r["alarm_released"] for r in g),
                                     false_alarm_sqrt=sum(not r["violates"] and r["alarm_sqrt"] for r in g),
                                     assumption_fail_share=round(float(np.mean([r["assumption_fail_share"] for r in g])), 3))
    json.dump(dict(report=report, rows=rows), open(f"{args.dir}/analysis.json", "w"), indent=1)
    print(json.dumps(report, indent=0))


if __name__ == "__main__":
    main()

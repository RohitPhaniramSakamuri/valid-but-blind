"""Exploratory, written after every frozen verdict was known. Uses saved factorial streams only; enters no rule.

For each strict violation, splits the error rate into what the monitor can see and cannot see:
  err = flagged_wrong + unflagged_wrong;  flagged = flagged_wrong + flagged_correct.
"Rate gap": flagged rate minus L_1 stays at or below the alarm level r0 + 0.1 on the stream average, so at this average rate more
data would not help (proxy shortfall). Otherwise a miss is attributed to confidence-sequence width and stream length. This is a
stream-average summary, not a population limit. Also reports paired same-draw contrasts and excess-error bands.
"""
import json

import numpy as np

ALPHA_L1 = 0.025
MODELS = ["Hendrycks2020AugMix_ResNeXt", "Modas2021PRIMEResNet18", "Hendrycks2020AugMix_WRN", "Addepalli2021Towards_PARN18", "Addepalli2021Towards_WRN34", "Addepalli2022Efficient_WRN_34_10"]
FORMS = [("source", "fixed"), ("bn", "fixed"), ("bn", "recal"), ("tent1e-4", "fixed"), ("tent1e-4", "recal"), ("tent1e-3", "fixed"), ("tent1e-3", "recal")]
BANDS = [(0.15, 0.25), (0.25, 0.35), (0.35, 9)]

verdict_rows = {(r["model"], r["key"]): r for r in json.load(open("factorial_report.json"))["rows"]}
A = {}  # model, arm, form -> stacked arrays over strict streams
every = []
for m in MODELS:
    cal = json.load(open(f"results_{m}/calibration.json"))
    r0, L1 = cal["r0"], cal["false_alarm0"] + (np.log(2) - np.log(ALPHA_L1)) / (2 * cal["n_calib"])
    for line in open(f"results_{m}/streams.jsonl"):
        s = json.loads(line)
        v = verdict_rows[(m, s["key"])]
        err = np.asarray(s["err"])
        half = len(err) // 2
        for form in ("recal", "fixed"):
            if s["arm"] == "source" and form == "recal":
                continue
            pos, un = np.asarray(s[f"pos_{form}"]), np.asarray(s[f"pfn_{form}"])
            every.append(dict(model=m, arm=s["arm"], form=form, key=s["key"], draw="/".join(s["key"].split("/")[1:]), strict=v["strict"], alarm=v[f"alarm_{form}"], r0=r0, L1=L1,
                              excess=v["excess"], err=err.mean(), flagged=pos.mean(), unflagged_wrong=un.mean(), flagged_wrong=(err - un).mean(), flagged_correct=(pos - err + un).mean(),
                              rate_gap=pos.mean() - L1 <= r0 + 0.1, conf=float(np.mean(s["conf"])), q=float(np.mean(s["q_hat"])), flagged_first=pos[:half].mean(), flagged_last=pos[half:].mean(),
                              err_first=err[:half].mean(), err_last=err[half:].mean()))


def pick(arm, form, model=None):
    return [r for r in every if r["arm"] == arm and r["form"] == form and r["strict"] and (model is None or r["model"] == model)]


def by_model_mean(arm, form, k):
    vals = [np.mean([r[k] for r in pick(arm, form, m)]) for m in MODELS if pick(arm, form, m)]
    return round(float(np.mean(vals)), 3)


out = {"note": "exploratory; equal-weight model means over strict streams", "forms": {}, "per_model_tent_vs_source": {}, "bands": {}, "paired": {}}
for arm, form in FORMS:
    g = pick(arm, form)
    miss = [r for r in g if not r["alarm"]]
    d = {k: by_model_mean(arm, form, k) for k in ("err", "flagged", "flagged_wrong", "unflagged_wrong", "flagged_correct", "conf", "q", "flagged_first", "flagged_last", "err_first", "err_last", "L1", "r0")}
    d.update(strict=len(g), missed=len(miss), missed_with_rate_gap=sum(r["rate_gap"] for r in miss), missed_without_rate_gap=sum(not r["rate_gap"] for r in miss), alarmed_with_rate_gap=sum(r["rate_gap"] and r["alarm"] for r in g))
    out["forms"][f"{arm}/{form}"] = d
    out["bands"][f"{arm}/{form}"] = {f"{lo}-{hi}": [sum(not r["alarm"] for r in g if lo <= r["excess"] < hi), sum(lo <= r["excess"] < hi for r in g)] for lo, hi in BANDS}
for m in MODELS:
    out["per_model_tent_vs_source"][m] = {f"{a}/{f}": {k: (round(float(np.mean([r[k] for r in pick(a, f, m)])), 3) if pick(a, f, m) else None) for k in ("err", "flagged", "unflagged_wrong", "flagged_correct", "conf")} | {"n": len(pick(a, f, m))} for a, f in (("source", "fixed"), ("bn", "recal"), ("tent1e-3", "recal"))}


def paired(a, af, b, bf):
    ix = {(r["model"], r["draw"]): r for r in pick(b, bf)}
    both = [(r, ix[(r["model"], r["draw"])]) for r in pick(a, af) if (r["model"], r["draw"]) in ix]
    only_a = sum(not x["alarm"] and y["alarm"] for x, y in both)
    only_b = sum(x["alarm"] and not y["alarm"] for x, y in both)
    return dict(draws=len(both), a_only_missed=only_a, b_only_missed=only_b, both_missed=sum(not x["alarm"] and not y["alarm"] for x, y in both), neither=sum(x["alarm"] and y["alarm"] for x, y in both),
                mean_err_a_minus_b=round(float(np.mean([x["err"] - y["err"] for x, y in both])), 3) if both else None, mean_flagged_a_minus_b=round(float(np.mean([x["flagged"] - y["flagged"] for x, y in both])), 3) if both else None,
                mean_unflagged_wrong_a_minus_b=round(float(np.mean([x["unflagged_wrong"] - y["unflagged_wrong"] for x, y in both])), 3) if both else None)


out["paired"]["tent1e-3_recal__vs__source"] = paired("tent1e-3", "recal", "source", "fixed")
out["paired"]["tent1e-3_recal__vs__bn_recal"] = paired("tent1e-3", "recal", "bn", "recal")
out["paired"]["bn_recal__vs__source"] = paired("bn", "recal", "source", "fixed")
out["arms_all_streams"] = json.load(open("factorial_report.json"))["report"]["arms"]
out = json.loads(json.dumps(out, default=lambda v: v.item()))
json.dump(out, open("explore_masses.json", "w"), indent=1)
for k in ("forms", "bands", "paired"):
    print(k)
    for a, b in out[k].items():
        print(" ", a, b)
print("per model")
for a, b in out["per_model_tent_vs_source"].items():
    print(" ", a, b)
print({a: {k: b[k] for k in ("n", "strict", "collapsed", "err", "conf")} for a, b in out["arms_all_streams"].items()})

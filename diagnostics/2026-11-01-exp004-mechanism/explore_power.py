"""Exploratory, written after every frozen verdict; enters no rule. Saved streams only. Does not compute false-alarm rates.

Part A: recall (flagged wrong / wrong) and precision (flagged wrong / flagged) on strict streams, per model and arm.
Part B: bootstrap intervals for missed-share gaps, resampling corruption types within model and, separately, models.
Part C: logistic regression of a miss on arm, excess error and model, with standard errors clustered on model x corruption.
Part D: first-alarm batch among streams that alarm.
"""
import json
import os
from multiprocessing import Pool

import numpy as np
import pandas as pd
import statsmodels.api as sm
from confseq.conjmix_bounded import conjmix_empbern_lower_cs
from confseq.predmix import predmix_empbern_lower_cs

MODELS = ["Hendrycks2020AugMix_ResNeXt", "Modas2021PRIMEResNet18", "Hendrycks2020AugMix_WRN", "Addepalli2021Towards_PARN18", "Addepalli2021Towards_WRN34", "Addepalli2022Efficient_WRN_34_10"]
ALPHA, AL1, TOL = 0.15, 0.025, 0.1
SEED = 20261102


def v_opt(x, t):
    m = np.cumsum(x) / np.arange(1, len(x) + 1)
    return np.cumsum((x - np.append(0.5, m[:-1])) ** 2)[t] * t


def first_alarm(a):
    pos, r0, L1 = a
    x = np.asarray(pos)
    try:
        cs = np.asarray(conjmix_empbern_lower_cs(x=x, alpha=ALPHA, v_opt=v_opt(x, int(len(x) * 0.25))))
    except RuntimeError:
        cs = np.asarray(predmix_empbern_lower_cs(x=x, alpha=ALPHA))
    hit = np.where(np.maximum(cs - L1, 0) > r0 + TOL)[0]
    return int(hit[0]) + 1 if len(hit) else -1


def load(study, folder, spec):
    out, jobs = [], []
    for m in MODELS:
        c = json.load(open(f"{folder.format(m=m)}/calibration.json"))
        r0, L1 = c["r0"], c["false_alarm0"] + (np.log(2) - np.log(AL1)) / (2 * c["n_calib"])
        for line in open(f"{folder.format(m=m)}/streams.jsonl"):
            s = json.loads(line)
            for arm, form, pk, nk in spec:
                if s["arm"] != arm:
                    continue
                err, pos, un = np.asarray(s["err"]), np.asarray(s[pk]), np.asarray(s[nk])
                e, l = float(err.mean()), float(err[-len(err) // 4:].mean())
                out.append(dict(study=study, model=m, arm=f"{arm}/{form}", corruption=s["corruption"], draw=f'{s["corruption"]}/{s["severity"]}/{s["rep"]}', err=e, excess=e - r0, strict=e >= r0 + TOL + 0.05 and l < 0.85, wrong=e, flagged=float(pos.mean()), hit=float((err - un).mean())))
                jobs.append((pos.tolist(), r0, L1))
    return out, jobs


def add_arm(spec_arm):
    return [(spec_arm, "recal", "pos_recal", "pfn_recal"), (spec_arm, "fixed", "pos_fixed", "pfn_fixed")]


FAC = "{m}"
rows, jobs = [], []
spec = [("source", "fixed", "pos_fixed", "pfn_fixed")] + add_arm("bn") + add_arm("tent1e-4") + add_arm("tent1e-3")
a, b = load("factorial", "results_{m}", spec); rows += a; jobs += b
a, b = load("sar", "../2026-11-02-exp004-sar/results_sar_{m}", add_arm("sar")); rows += a; jobs += b
a, b = load("replication", "../2026-11-01-exp004-replicate/results_{m}", [("tent", "recal", "pos", "pfn"), ("source", "fixed", "pos", "pfn")]); rows += a; jobs += b
with Pool(os.cpu_count()) as pool:
    fa = pool.map(first_alarm, jobs, chunksize=8)
df = pd.DataFrame(rows)
df["first"] = fa
df["alarm"] = df["first"] > 0
df["miss"] = (~df["alarm"]).astype(int)
st = df[df.strict].copy()
st["cl"] = st.model + "|" + st.corruption
# Check against frozen counts.
check = {f"{k[0]}|{k[1]}": [int(g.miss.sum()), len(g)] for k, g in st.groupby(["study", "arm"])}

res = dict(note="exploratory; post-verdict", check=check)
# A
A = {}
for (study, arm), g in st.groupby(["study", "arm"]):
    p = g.groupby("model")[["wrong", "flagged", "hit"]].mean()
    rec, pre = p.hit / p.wrong, p.hit / p.flagged
    A[f"{study}|{arm}"] = dict(recall=round(float(rec.mean()), 3), precision=round(float(pre.mean()), 3), recall_by_model={k: round(float(v), 3) for k, v in rec.items()}, precision_by_model={k: round(float(v), 3) for k, v in pre.items()}, n=len(g))
res["A"] = A


def contrast_a(study, a_arm, b_arm, base_study=None):
    x = st[(st.study == study) & (st.arm == a_arm)].groupby("model")[["wrong", "flagged", "hit"]].mean()
    y = st[(st.study == (base_study or study)) & (st.arm == b_arm)].groupby("model")[["wrong", "flagged", "hit"]].mean()
    return dict(recall_lower_models=int(((x.hit / x.wrong) < (y.hit / y.wrong)).sum()), precision_lower_models=int(((x.hit / x.flagged) < (y.hit / y.flagged)).sum()), mean_recall_diff=round(float(((x.hit / x.wrong) - (y.hit / y.wrong)).mean()), 3), mean_precision_diff=round(float(((x.hit / x.flagged) - (y.hit / y.flagged)).mean()), 3))


res["A_contrasts"] = dict(tent_vs_source_factorial=contrast_a("factorial", "tent1e-3/recal", "source/fixed"), tent_vs_bn_factorial=contrast_a("factorial", "tent1e-3/recal", "bn/recal"), tent_vs_source_replication=contrast_a("replication", "tent/recal", "source/fixed"), bn_vs_source=contrast_a("factorial", "bn/recal", "source/fixed"))


# B
def boot(study, a_arm, b_arm, base=None, n=4000):
    s0 = st[((st.study == study) & (st.arm == a_arm)) | ((st.study == (base or study)) & (st.arm == b_arm))]
    tag = (s0.arm == a_arm).to_numpy()
    tab = pd.DataFrame(dict(model=s0.model.to_numpy(), c=s0.corruption.to_numpy(), a=tag, m=s0.miss.to_numpy()))
    agg = tab.groupby(["model", "c", "a"]).m.agg(["sum", "count"]).unstack("a", fill_value=0)
    keys = agg.index.to_frame(index=False)
    ms, ma, na, mb, nb = agg[("sum", True)].to_numpy(), agg[("sum", True)].to_numpy(), agg[("count", True)].to_numpy(), agg[("sum", False)].to_numpy(), agg[("count", False)].to_numpy()
    rng = np.random.default_rng(SEED)
    idx_by_model = [np.where(keys.model == m)[0] for m in MODELS]
    w = np.zeros((n, len(keys)))
    for ix in idx_by_model:
        draws = rng.integers(0, len(ix), (n, len(ix)))
        w[np.arange(n)[:, None], ix[draws]] += 0
        for j in range(len(ix)):
            np.add.at(w, (np.arange(n), ix[draws[:, j]]), 1)
    g1 = (w @ ma) / np.maximum(w @ na, 1) - (w @ mb) / np.maximum(w @ nb, 1)
    # Models resampled whole.
    mm = keys.model.to_numpy()
    by = np.stack([[ma[mm == m].sum(), na[mm == m].sum(), mb[mm == m].sum(), nb[mm == m].sum()] for m in MODELS]).astype(float)
    d = rng.integers(0, 6, (n, 6))
    t = by[d].sum(1)
    g2 = t[:, 0] / np.maximum(t[:, 1], 1) - t[:, 2] / np.maximum(t[:, 3], 1)
    return dict(gap=round(float(ma.sum() / na.sum() - mb.sum() / nb.sum()), 3), corruption_within_model=np.round(np.percentile(g1, [2.5, 97.5]), 3).tolist(), models=np.round(np.percentile(g2, [2.5, 97.5]), 3).tolist(), n_a=int(na.sum()), n_b=int(nb.sum()))


res["B"] = dict(tent_vs_source_replication=boot("replication", "tent/recal", "source/fixed"), tent_fixed_vs_source=boot("factorial", "tent1e-3/fixed", "source/fixed"), tent_vs_source=boot("factorial", "tent1e-3/recal", "source/fixed"), tent_vs_bn=boot("factorial", "tent1e-3/recal", "bn/recal"), bn_vs_source=boot("factorial", "bn/recal", "source/fixed"))


# C
def logit(study, a_arm, b_arm):
    d = st[(st.study == study) & st.arm.isin([a_arm, b_arm])].copy()
    X = pd.DataFrame(dict(const=1.0, treated=(d.arm == a_arm).astype(float), excess=(d.excess - d.excess.mean()) / 0.1))
    for m in MODELS[1:]:
        X[m] = (d.model == m).astype(float)
    try:
        f = sm.GLM(d.miss, X, family=sm.families.Binomial()).fit(cov_type="cluster", cov_kwds=dict(groups=pd.factorize(d.cl)[0]))
        ci = f.conf_int().loc["treated"]
        X1, X0 = X.copy(), X.copy()
        X1["treated"], X0["treated"] = 1.0, 0.0
        return dict(n=len(d), odds_ratio=round(float(np.exp(f.params["treated"])), 2), ci=[round(float(np.exp(ci[0])), 2), round(float(np.exp(ci[1])), 2)], excess_per_10pts_or=round(float(np.exp(f.params["excess"])), 3), adjusted_miss_diff=round(float((f.predict(X1) - f.predict(X0)).mean()), 3))
    except Exception as e:
        return dict(error=repr(e)[:200], n=len(d))


res["C"] = dict(replication_tent_vs_source=logit("replication", "tent/recal", "source/fixed"), factorial_tent_vs_source=logit("factorial", "tent1e-3/recal", "source/fixed"), factorial_tent_vs_bn=logit("factorial", "tent1e-3/recal", "bn/recal"), factorial_bn_vs_source=logit("factorial", "bn/recal", "source/fixed"))
sar = pd.concat([st[(st.study == "sar") & (st.arm == "sar/recal")], st[(st.study == "factorial") & (st.arm == "source/fixed")]]).copy()
sar["study"] = "sarcmp"
st2 = st
st = pd.concat([st2, sar])
res["C"]["sar_vs_source"] = logit("sarcmp", "sar/recal", "source/fixed")
st = st2
# D
D = {}
for (study, arm), g in st.groupby(["study", "arm"]):
    al = g[g.alarm]
    D[f"{study}|{arm}"] = dict(alarmed=len(al), of=len(g), median_first_batch=float(al["first"].median()) if len(al) else None, q25=float(al["first"].quantile(.25)) if len(al) else None, q75=float(al["first"].quantile(.75)) if len(al) else None)
res["D"] = D
res["excess_mean"] = {f"{k[0]}|{k[1]}": round(float(v), 3) for k, v in st.groupby(["study", "arm"]).excess.mean().items()}
json.dump(res, open("explore_power.json", "w"), indent=1)
print(json.dumps({k: res[k] for k in ("check", "A_contrasts", "B", "C", "D", "excess_mean")}, indent=0))
for k, v in res["A"].items():
    print(k, v["recall"], v["precision"], v["n"], v["recall_by_model"], v["precision_by_model"])

"""Analyze actual saved action outcomes; final labels never fit runtime models.

Diagnostic purpose only: correlated episode resampling on one small dataset.
"""
import os
for variable in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[variable] = "1"
from pathlib import Path
import argparse
import json
import time
import hashlib
import numpy as np
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.model_selection import GroupKFold
from threadpoolctl import threadpool_limits

ROOT = Path(__file__).resolve().parent
ACTION_NAMES = np.array(["SOURCE", "BN", "ENTROPY"])


def regression(alpha=10.0):
    return make_pipeline(StandardScaler(), Ridge(alpha=alpha))


def rowpick(array, actions):
    return array[np.arange(len(actions)), actions]


def latency_ms(model, features):
    sample = features[:1]
    for _ in range(10):
        model.predict(sample)
    values = []
    for _ in range(80):
        start = time.perf_counter_ns()
        model.predict(sample)
        values.append((time.perf_counter_ns() - start) / 1e6)
    return float(np.median(values))


def get(data, *names):
    for name in names:
        if name in data:
            return data[name]
    raise KeyError(f"Missing arrays {names}; available: {data.files}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(ROOT / "outcomes.npz"))
    args = parser.parse_args()
    started = time.time()
    data = np.load(args.input, allow_pickle=False)
    cheap = get(data, "cheap").astype(float)
    rich = get(data, "rich").astype(float)
    errors = get(data, "errors", "losses").astype(float)
    costs = get(data, "action_cost_ms", "costs").astype(float)
    cheap_cost = get(data, "cheap_cost_ms").astype(float)
    rich_cost = get(data, "rich_extra_cost_ms").astype(float)
    splits = get(data, "splits", "split").astype(str)
    families = get(data, "families", "family").astype(str)
    groups = get(data, "groups", "group").astype(str)
    train = np.flatnonzero(splits == "train")
    cal = np.flatnonzero(splits == "cal")
    all_test = np.flatnonzero(splits == "test")
    test = np.flatnonzero((splits == "test") & data["heldout_family"]) if "heldout_family" in data else all_test
    if not len(train) or not len(cal) or not len(test):
        raise ValueError("Need nonempty train/cal/test partitions.")
    if errors.shape[1] != 3 or costs.shape != errors.shape:
        raise ValueError("Expected three declared actions and matched errors/costs.")
    if not all(np.isfinite(array).all() for array in [cheap, rich, errors, costs, cheap_cost, rich_cost]):
        raise ValueError("Nonfinite observed outcomes/features/costs.")

    # Fixed before reading final outcomes: ridge alpha, utility weights and rate grid.
    config = {"regression_alpha": 10.0, "seed": 314159,
              "lambda_error_per_source_cost_unit": [0.0, 0.002, 0.01, 0.03],
              "calibration_probe_rates": [0.0, 0.25, 0.5, 0.75, 1.0],
              "gate_fit": "GroupKFold predictions from disjoint original-ID pools; separate cal thresholds",
              "uncertainty": "Conditional descriptive episode bootstrap; not population-independent CIs"}
    (ROOT / "analysis_config.json").write_text(json.dumps(config, indent=2) + "\n")
    oof0 = np.full_like(errors[train], np.nan)
    oof1 = np.full_like(errors[train], np.nan)
    n_groups = len(np.unique(groups[train]))
    if n_groups < 2:
        raise ValueError("OOF requires at least two disjoint image-pool groups.")
    folds = []
    for left, right in GroupKFold(n_splits=n_groups).split(cheap[train], errors[train], groups[train]):
        m0 = regression().fit(cheap[train[left]], errors[train[left]])
        m1 = regression().fit(rich[train[left]], errors[train[left]])
        oof0[right] = m0.predict(cheap[train[right]])
        oof1[right] = m1.predict(rich[train[right]])
        folds.append({"train_groups": sorted(set(groups[train[left]])),
                      "heldout_groups": sorted(set(groups[train[right]])),
                      "train_episodes": len(left), "heldout_episodes": len(right)})
    m0 = regression().fit(cheap[train], errors[train])
    m1 = regression().fit(rich[train], errors[train])
    model_cost0 = latency_ms(m0, cheap[cal])
    model_cost1 = latency_ms(m1, rich[cal])
    pred0, pred1 = m0.predict(cheap), m1.predict(rich)
    # Source-cost scaling uses calibration timing only.
    scale_ms = max(float(np.median(costs[cal, 0])), 1e-6)
    action_cost_est = np.median(costs[train], axis=0)
    rng = np.random.default_rng(config["seed"])
    random_scores = rng.uniform(size=len(errors))
    frequency = np.arange(len(errors)) % 4 / 4
    # Metadata includes which cheap dimension is entropy; first feature contract.
    entropy_scores = cheap[:, 0]
    sorted_preds = np.sort(pred0, axis=1)
    ambiguity_scores = -(sorted_preds[:, 1] - sorted_preds[:, 0])
    rows, episode_rows, gate_records = [], [], []

    def record(name, indices, acts, route_cost, probes, lam, extra=None, observed_errors=None):
        idx = np.asarray(indices)
        err = rowpick(errors[idx], acts) if observed_errors is None else observed_errors
        c = np.asarray(route_cost)
        base_err = errors[idx, 0]
        allin = err + lam * c / scale_ms
        # Free-information terminal-action oracle; intentionally optimistic diagnostic.
        oracle = np.min(errors[idx] + lam * costs[idx] / scale_ms, axis=1)
        row = {"policy": name, "lambda": lam, "n_episodes": len(idx),
               "mean_error": float(err.mean()), "accuracy": float(1 - err.mean()),
               "mean_cost_ms": float(c.mean()), "median_cost_ms": float(np.median(c)),
               "p95_cost_ms": float(np.quantile(c, .95)),
               "source_cost_units": float(c.mean() / scale_ms),
               "mean_objective": float(allin.mean()), "oracle_regret": float((allin-oracle).mean()),
               "harmful_episode_fraction": float(np.mean(err > base_err + 1e-12)),
               "mean_error_gain_over_source": float(np.mean(base_err-err)),
               "acquisition_fraction": float(np.mean(probes)),
               "source_choice_fraction": float(np.mean(acts == 0))}
        if extra: row.update(extra)
        rows.append(row)
        for j, original in enumerate(idx):
            episode_rows.append({"episode_index": int(original), "family": families[original],
                                 "policy": name, "lambda": lam, "action": str(ACTION_NAMES[acts[j]]),
                                 "error": float(err[j]), "cost_ms": float(c[j]),
                                 "acquired": bool(probes[j])})

    for lam in config["lambda_error_per_source_cost_unit"]:
        value0 = pred0 + lam * action_cost_est[None, :] / scale_ms
        value1 = pred1 + lam * action_cost_est[None, :] / scale_ms
        acts0, acts1 = value0.argmin(axis=1), value1.argmin(axis=1)
        oacts0 = (oof0 + lam * action_cost_est[None, :] / scale_ms).argmin(axis=1)
        oacts1 = (oof1 + lam * action_cost_est[None, :] / scale_ms).argmin(axis=1)
        # OOF realized decision improvement, with distinct route inference costs.
        gain = (rowpick(errors[train], oacts0) - rowpick(errors[train], oacts1)
                + lam * (rowpick(costs[train], oacts0) - rowpick(costs[train], oacts1)
                         + model_cost0 - model_cost1 - rich_cost[train]) / scale_ms)
        gate = regression().fit(cheap[train], gain)
        gate_scores = gate.predict(cheap)
        gate_cost = latency_ms(gate, cheap[cal])
        def route(idx, acquired):
            chosen = np.where(acquired, acts1[idx], acts0[idx])
            allin = cheap_cost[idx] + rowpick(costs[idx], chosen)
            allin += np.where(acquired, rich_cost[idx] + model_cost1, model_cost0)
            return chosen, allin

        for action in range(3):
            record(f"fixed_{ACTION_NAMES[action]}", test, np.full(len(test),action), costs[test,action],
                   np.zeros(len(test),bool), lam)
        if "ensemble_errors" in data:
            record("source_three_view_ensemble",test,np.zeros(len(test),int),data["ensemble_cost_ms"][test],
                   np.zeros(len(test),bool),lam,{"oracle_regret":np.nan,"out_of_menu":True},
                   observed_errors=data["ensemble_errors"][test])
        devfixed = int(np.argmin(np.mean(errors[cal] + lam*costs[cal]/scale_ms,axis=0)))
        hindsight = int(np.argmin(np.mean(errors[test] + lam*costs[test]/scale_ms,axis=0)))
        record("development_fixed",test,np.full(len(test),devfixed),costs[test,devfixed],np.zeros(len(test),bool),lam)
        record("hindsight_fixed_diagnostic",test,np.full(len(test),hindsight),costs[test,hindsight],np.zeros(len(test),bool),lam)
        oracle_acts=(errors[test]+lam*costs[test]/scale_ms).argmin(axis=1)
        record("terminal_oracle_diagnostic",test,oracle_acts,rowpick(costs[test],oracle_acts),np.zeros(len(test),bool),lam)
        for name, acquired in [("cheap_only",np.zeros(len(test),bool)),("always_rich",np.ones(len(test),bool))]:
            acts,c=route(test,acquired);record(name,test,acts,c,acquired,lam)
        # Random and fixed controls are actual policies, with cal-fixed rates.
        for rate in config["calibration_probe_rates"]:
            for trigger, scores in [("random",random_scores),("entropy",entropy_scores),
                                    ("ambiguity",ambiguity_scores),("learned_value",gate_scores)]:
                if rate==0: threshold=float("inf")
                elif rate==1: threshold=-float("inf")
                else: threshold=float(np.quantile(scores[cal],1-rate))
                acquire=scores[test] >= threshold
                acts,c=route(test,acquire)
                if trigger=="ambiguity":c+=model_cost0*acquire
                if trigger=="learned_value":c+=gate_cost
                record(f"{trigger}_rate_{rate:.2f}",test,acts,c,acquire,lam,
                       {"calibration_rate_target":rate,"calibration_threshold":threshold})
            acquire=frequency[test] < rate
            acts,c=route(test,acquire)
            record(f"fixed_schedule_rate_{rate:.2f}",test,acts,c,acquire,lam,{"calibration_rate_target":rate})
        acquire=gate_scores[test] > 0
        acts,c=route(test,acquire);c+=gate_cost
        record("learned_positive_value",test,acts,c,acquire,lam)
        # Choose a single value-gate threshold on calibration, never on test.
        options=[]
        for rate in config["calibration_probe_rates"]:
            threshold = float("inf") if rate==0 else (-float("inf") if rate==1 else float(np.quantile(gate_scores[cal],1-rate)))
            ca=gate_scores[cal] >= threshold; aa,cc=route(cal,ca);cc+=gate_cost
            obj=float(np.mean(rowpick(errors[cal],aa)+lam*cc/scale_ms))
            options.append((obj,rate,threshold))
        _,chosen_rate,threshold=min(options,key=lambda x:(x[0],x[1]))
        acquire=gate_scores[test]>=threshold;acts,c=route(test,acquire);c+=gate_cost
        record("learned_calibration_selected",test,acts,c,acquire,lam,
               {"calibration_rate_target":chosen_rate,"calibration_threshold":threshold})
        gate_records.append({"lambda":lam,"gate_latency_ms":gate_cost,"calibration_rate":chosen_rate,
                             "oof_mean_gain":float(gain.mean()),"oof_positive_fraction":float(np.mean(gain>0)),
                             "calibration_gain_target_vs_refit_warning":"Fold predictors differ from final refit; test untouched"})

    frame=pd.DataFrame(rows)
    frame.to_csv(ROOT/'policy_comparisons.csv',index=False)
    pd.DataFrame(episode_rows).to_csv(ROOT/'policy_episode_outcomes.csv',index=False)
    detailed=pd.DataFrame(episode_rows)
    family=detailed.groupby(['lambda','policy','family']).agg(mean_error=('error','mean'),mean_cost_ms=('cost_ms','mean'),acquisition_fraction=('acquired','mean'),episodes=('error','size')).reset_index()
    family.to_csv(ROOT/'policy_by_family.csv',index=False)
    rawfamily=[]
    for fam in sorted(set(families[test])):
        idx=test[families[test]==fam]
        for action in range(3):
            rawfamily.append({'family':fam,'action':str(ACTION_NAMES[action]),'mean_error':float(errors[idx,action].mean()),'mean_cost_ms':float(costs[idx,action].mean()),'episodes':len(idx)})
    pd.DataFrame(rawfamily).to_csv(ROOT/'action_by_family.csv',index=False)
    with threadpool_limits(limits=1):
        zero=frame[frame['lambda']==0].set_index('policy')
        base=float(zero.loc['fixed_SOURCE','mean_error'])
        fixed=float(zero.loc['development_fixed','mean_error'])
        oracle=float(zero.loc['terminal_oracle_diagnostic','mean_error'])
        cheaperr=float(zero.loc['cheap_only','mean_error'])
        richerr=float(zero.loc['always_rich','mean_error'])
        # Paired descriptive resampling of episodes, conditional on this finite pool.
        a0=pred0[test].argmin(axis=1);a1=pred1[test].argmin(axis=1)
        paired=rowpick(errors[test],a0)-rowpick(errors[test],a1)
        draws=np.random.default_rng(20261023).choice(paired,size=(1500,len(paired)),replace=True).mean(axis=1)
        interval=np.quantile(draws,[.025,.975]).tolist()
    summary={'status':'completed','run_date':'2026-10-23','input':str(Path(args.input).name),
             'episodes':{'train':len(train),'cal':len(cal),'primary_heldout_test':len(test),'all_test':len(all_test)},
             'train_families':sorted(set(families[train])),'test_families':sorted(set(families[test])),
             'source_query_cost_scale_ms':scale_ms,'cheap_selector_latency_ms':model_cost0,'rich_selector_latency_ms':model_cost1,
             'source_error':base,'development_fixed_error':fixed,'hindsight_fixed_error':float(zero.loc['hindsight_fixed_diagnostic','mean_error']),
             'terminal_oracle_error':oracle,'oracle_headroom_vs_development_fixed':fixed-oracle,
             'cheap_selector_error':cheaperr,'rich_selector_error':richerr,'rich_evidence_error_improvement':cheaperr-richerr,
             'rich_evidence_paired_episode_bootstrap_interval':interval,
             'bootstrap_caveat':'Conditional resampling of overlapping episodes; not independent dataset/population uncertainty.',
             'folds':folds,'gates':gate_records,'analysis_seconds':time.time()-started,
             'claims':'Alternate-data mechanism diagnostic; no original benchmark replication or verified novelty.'}
    (ROOT/'analysis_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(figsize=(7,4.3))
    z=frame[frame['lambda']==0]
    for prefix,label in [('learned_value_rate_','Learned value'),('random_rate_','Random'),('entropy_rate_','Entropy'),('ambiguity_rate_','Selector ambiguity')]:
        part=z[z.policy.str.startswith(prefix)].sort_values('mean_cost_ms')
        ax.plot(part.mean_cost_ms,100*(1-part.mean_error),marker='o',label=label)
    for policy,label in [('fixed_SOURCE','Source'),('development_fixed','Development fixed'),('cheap_only','Cheap selector'),('always_rich','Always rich')]:
        row=z[z.policy==policy].iloc[0];ax.scatter(row.mean_cost_ms,100*(1-row.mean_error),marker='x',s=70,label=label)
    ax.set_xlabel('Mean estimated all-in CPU route time (ms)')
    ax.set_ylabel('Query accuracy (%)')
    ax.set_title('Digits mechanism diagnostic: held-out shift families')
    ax.legend(fontsize=8,ncol=2);ax.grid(alpha=.2);fig.tight_layout();fig.savefig(ROOT/'accuracy_cost_frontier.png',dpi=150);plt.close(fig)
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    with threadpool_limits(limits=1):
        main()

"""Post-hoc exploratory SOURCE/BN concentration gate, calibrated without test labels.

The baseline was added after observing the overall prior-dependent action
breakdown. It is not a predeclared or independent confirmatory test.
"""
from pathlib import Path
import hashlib
import json
import time
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
THRESHOLDS = [0.15, 0.2, 0.25, 0.35, 0.5, 0.65, 0.8]
LAMBDAS = [0.0, 0.002, 0.01, 0.03]


def gate(concentration, threshold):
    return np.where(concentration <= threshold, 1, 0)


def main():
    started = time.perf_counter()
    with np.load(HERE / "outcomes.npz") as saved:
        data = {key: saved[key].copy() for key in saved.files}
    frame = pd.read_csv(HERE / "episodes.csv")
    concentration = data["cheap"][:, 6]
    cal = data["splits"] == "cal"
    test_all = data["splits"] == "test"
    test_primary = test_all & data["heldout_family"]
    sample = concentration[:1]
    for _ in range(10):
        gate(sample, 0.35)
    timings = []
    for _ in range(80):
        start = time.perf_counter_ns()
        gate(sample, 0.35)
        timings.append((time.perf_counter_ns() - start) / 1e6)
    gate_ms = float(np.median(timings))
    scale_ms = max(float(np.median(data["action_cost_ms"][cal, 0])), 1e-6)
    config = {"status": "post-hoc exploratory baseline", "selection_feature": "cheap index 6 = max predicted-class frequency",
              "rule": "BN if concentration <= threshold, otherwise SOURCE", "thresholds": THRESHOLDS,
              "lambdas": LAMBDAS, "fit_labels": "calibration only", "gate_latency_ms": gate_ms,
              "source_cost_scale_ms": scale_ms, "source_direct_fallback": True,
              "design_timing": "Added after viewing original test action-by-prior breakdown; no fresh confirmatory claim"}
    (HERE / "prior_gate_config.json").write_text(json.dumps(config, indent=2) + "\n")
    rows, candidates, episode_rows = [], [], []
    all_i = np.arange(len(concentration))
    for lam in LAMBDAS:
        best = None
        settings = [("SOURCE_DIRECT", None)] + [("concentration_gate", threshold) for threshold in THRESHOLDS]
        for name, threshold in settings:
            if name == "SOURCE_DIRECT":
                chosen = np.zeros(len(concentration), dtype=int)
                total_cost = data["action_cost_ms"][:, 0]
            else:
                chosen = gate(concentration, threshold)
                total_cost = data["cheap_cost_ms"] + gate_ms + data["action_cost_ms"][all_i, chosen]
            error = data["errors"][all_i, chosen]
            objective = float(np.mean(error[cal] + lam * total_cost[cal] / scale_ms))
            candidates.append({"lambda": lam, "policy": name, "threshold": threshold,
                               "cal_objective": objective, "cal_error": float(error[cal].mean()),
                               "cal_cost_ms": float(total_cost[cal].mean())})
            if best is None or objective < best[0]:
                best = (objective, name, threshold, chosen, error, total_cost)
        _, name, threshold, chosen, error, total_cost = best
        for scope, test in (("primary_heldout", test_primary), ("all_test", test_all)):
            source_error = data["errors"][test, 0]
            source_cost = data["action_cost_ms"][test, 0]
            index = np.flatnonzero(test)
            oracle_objective = np.min(data["errors"][test] + lam * data["action_cost_ms"][test] / scale_ms, axis=1)
            policy_objective = error[test] + lam * total_cost[test] / scale_ms
            rows.append({"lambda": lam, "scope": scope, "selected_policy": name, "threshold": threshold,
                         "episodes": int(test.sum()), "error": float(error[test].mean()),
                         "accuracy": float(1 - error[test].mean()), "source_error": float(source_error.mean()),
                         "gain_over_source_pp": float(100 * (source_error - error[test]).mean()),
                         "total_cost_ms": float(total_cost[test].mean()),
                         "source_cost_ms": float(source_cost.mean()),
                         "source_cost_units": float(total_cost[test].mean() / scale_ms),
                         "mean_objective": float(policy_objective.mean()),
                         "source_objective": float(np.mean(source_error + lam * source_cost / scale_ms)),
                         "oracle_regret": float(np.mean(policy_objective - oracle_objective)),
                         "source_fraction": float(np.mean(chosen[test] == 0))})
            for original in index:
                episode_rows.append({"episode_id": int(frame.iloc[original].episode_id), "scope": scope,
                                     "lambda": lam, "selected_policy": name, "threshold": threshold,
                                     "action": str(data['action_names'][chosen[original]]),
                                     "family": frame.iloc[original].family,
                                     "prior": frame.iloc[original].prior,
                                     "error": float(error[original]), "cost_ms": float(total_cost[original]),
                                     "source_error": float(data['errors'][original, 0])})
    pd.DataFrame(rows).to_csv(HERE / "prior_gate_results.csv", index=False)
    pd.DataFrame(candidates).to_csv(HERE / "prior_gate_calibration.csv", index=False)
    pd.DataFrame(episode_rows).to_csv(HERE / "prior_gate_episode_outcomes.csv", index=False)
    summary = {"status": "completed", "scope": "Post-hoc exploratory, cal-only threshold fitting; existing final evaluation reused",
               "config": config, "elapsed_seconds": time.perf_counter() - started,
               "outcomes_sha256": hashlib.sha256((HERE / 'outcomes.npz').read_bytes()).hexdigest(),
               "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE / "prior_gate_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(pd.DataFrame(rows).to_string(index=False), flush=True)
    print(json.dumps({"completed": True, "elapsed_seconds": summary["elapsed_seconds"]}, indent=2), flush=True)


if __name__ == "__main__":
    main()

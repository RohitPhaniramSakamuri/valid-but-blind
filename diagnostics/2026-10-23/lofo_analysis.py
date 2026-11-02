"""Exploratory leave-one-training-family-out selector diagnostic.

Fits fixed-alpha Ridge predictors using only the original training partition.
Each held-out family's final-test labels are used only for evaluation after
selection. Reuses already generated episodes; this is not a fresh experiment.
"""
import os
for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[name] = "1"

from pathlib import Path
import hashlib
import json
import time

import numpy as np
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge

HERE = Path(__file__).resolve().parent
ALPHA = 10.0
FAMILIES = ("noise", "brightness", "blur", "translation")


def fit_predict(features, targets, train, test):
    model = make_pipeline(StandardScaler(), Ridge(alpha=ALPHA))
    model.fit(features[train], targets[train])
    predictions = model.predict(features[test])
    sample = features[test][:1]
    for _ in range(10):
        model.predict(sample)
    timings = []
    for _ in range(80):
        start = time.perf_counter()
        model.predict(sample)
        timings.append(1000 * (time.perf_counter() - start))
    return predictions.argmin(axis=1), float(np.median(timings))


def main():
    started = time.perf_counter()
    with np.load(HERE / "outcomes.npz") as saved:
        data = {key: saved[key].copy() for key in saved.files}
    episodes = pd.read_csv(HERE / "episodes.csv")
    rows, paired = [], []
    actions = data["action_names"].tolist()
    for family in FAMILIES:
        train = (data["splits"] == "train") & (data["families"] != family)
        allowed_cal = (data["splits"] == "cal") & (data["families"] != family)
        test = (data["splits"] == "test") & (data["families"] == family)
        cheap_actions, cheap_selector_ms = fit_predict(data["cheap"], data["errors"], train, test)
        rich_actions, rich_selector_ms = fit_predict(data["rich"], data["errors"], train, test)
        losses = data["errors"][test]
        cost = data["action_cost_ms"][test]
        index = np.arange(len(losses))
        source = losses[:, 0]
        oracle = losses.min(axis=1)
        cheap_error = losses[index, cheap_actions]
        rich_error = losses[index, rich_actions]
        cheap_cost = data["cheap_cost_ms"][test] + cheap_selector_ms + cost[index, cheap_actions]
        rich_cost = data["cheap_cost_ms"][test] + data["rich_extra_cost_ms"][test] + rich_selector_ms + cost[index, rich_actions]
        row = {
            "heldout_family": family, "train_episodes": int(train.sum()),
            "allowed_cal_episodes_unused": int(allowed_cal.sum()), "test_episodes": int(test.sum()),
            "source_error": float(source.mean()), "oracle_error": float(oracle.mean()),
            "cheap_error": float(cheap_error.mean()), "rich_error": float(rich_error.mean()),
            "oracle_headroom_pp": float(100 * (source - oracle).mean()),
            "cheap_gain_vs_source_pp": float(100 * (source - cheap_error).mean()),
            "rich_gain_vs_source_pp": float(100 * (source - rich_error).mean()),
            "rich_gain_vs_cheap_pp": float(100 * (cheap_error - rich_error).mean()),
            "source_cost_ms": float(cost[:, 0].mean()),
            "cheap_total_cost_ms": float(cheap_cost.mean()), "rich_total_cost_ms": float(rich_cost.mean()),
            "cheap_selector_ms": cheap_selector_ms, "rich_selector_ms": rich_selector_ms,
            "cheap_source_fraction": float(np.mean(cheap_actions == 0)),
            "rich_source_fraction": float(np.mean(rich_actions == 0)),
        }
        rows.append(row)
        for local, original in enumerate(np.flatnonzero(test)):
            paired.append({
                "episode_id": int(episodes.iloc[original].episode_id), "heldout_family": family,
                "source_error": source[local], "oracle_error": oracle[local],
                "cheap_action": actions[int(cheap_actions[local])], "rich_action": actions[int(rich_actions[local])],
                "cheap_error": cheap_error[local], "rich_error": rich_error[local],
                "cheap_gain_vs_source": source[local] - cheap_error[local],
                "rich_gain_vs_source": source[local] - rich_error[local],
                "rich_gain_vs_cheap": cheap_error[local] - rich_error[local],
                "cheap_total_cost_ms": cheap_cost[local], "rich_total_cost_ms": rich_cost[local],
                "prior": episodes.iloc[original].prior, "batch_size": int(episodes.iloc[original].batch_size),
            })
    pd.DataFrame(rows).to_csv(HERE / "lofo_results.csv", index=False)
    pd.DataFrame(paired).to_csv(HERE / "lofo_episode_gains.csv", index=False)
    action_columns = [f"error_{action}" for action in actions] + ["ensemble_error"]
    breakdown = episodes.groupby(["split", "family", "prior", "batch_size"])[action_columns].agg(["mean", "count"])
    breakdown.columns = ["_".join(column) for column in breakdown.columns]
    breakdown.reset_index().to_csv(HERE / "action_by_prior_batch.csv", index=False)
    mean = pd.DataFrame(rows).select_dtypes(include="number").mean().to_dict()
    summary = {
        "status": "completed", "scope": "Exploratory reanalysis of original outcomes; no new independent data or source model",
        "model": "StandardScaler + Ridge(alpha=10), same regression family and tuning budget for cheap and rich",
        "heldout_families": list(FAMILIES), "each_family_excluded_from_train_and_cal": True,
        "calibration_use": "None: alpha=10 and raw predicted-error argmin fixed before this analysis; calibration family removed but unused",
        "split_access": "Only training-partition labels fit the predictors; final-test labels score already selected actions",
        "selection": "argmin of un-clipped predicted error; identical to primary error-only comparison",
        "cost": "Saved per-episode evidence/action execution costs plus measured median single-episode predictor-inference cost over 80 timed repetitions after 10 warmups; source direct has no evidence-routing overhead",
        "uncertainty": "Finite query samples and shared image pools; rows are descriptive paired outcomes, not independent trial counts",
        "mean_across_families": mean,
        "elapsed_seconds": time.perf_counter() - started,
        "outcomes_sha256": hashlib.sha256((HERE / "outcomes.npz").read_bytes()).hexdigest(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    (HERE / "lofo_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(pd.DataFrame(rows).to_string(index=False), flush=True)
    print(json.dumps({"status": "completed", "elapsed_seconds": summary["elapsed_seconds"]}, indent=2), flush=True)


if __name__ == "__main__":
    main()

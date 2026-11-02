"""Independent query-identity grouped checks of oracle and evidence headroom.

Uses already frozen predictions/policy choices. Never refits or selects deployed
controllers. The cross-query oracle is label-assisted analysis only.
"""
from pathlib import Path
import argparse
import json

import numpy as np
import pandas as pd


HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", type=Path, default=HERE)
    parser.add_argument("--split-repeats", type=int, default=300)
    parser.add_argument("--bootstrap-repeats", type=int, default=4000)
    args = parser.parse_args()
    directory = args.directory
    data = np.load(directory / "outcomes.npz", allow_pickle=False)
    indices = np.flatnonzero((data["splits"] == "test") & data["heldout_family"])
    ids = data["query_ids"][indices]
    labels = data["query_labels"][indices]
    predictions = data["predictions"][indices]
    loss = (predictions != labels[:, None, :]).astype(float)
    source_error = float(loss[:, 0, :].mean())
    full_query_oracle_error = float(loss.mean(axis=2).min(axis=1).mean())
    rng = np.random.default_rng(24102399)
    cross_errors = []
    chosen_counts = np.zeros(loss.shape[1], dtype=int)
    for repeat in range(args.split_repeats):
        episode_errors = []
        for row in range(len(indices)):
            unique = np.unique(ids[row]).copy()
            rng.shuffle(unique)
            first_ids = unique[:len(unique) // 2]
            mask = np.isin(ids[row], first_ids)
            if not mask.any() or mask.all():
                raise ValueError("Degenerate query identity split")
            # All duplicates of a query identity remain together. Choose on one
            # side and score on the other, then reverse. Ties favor SOURCE.
            best_first = int(loss[row, :, mask].mean(axis=0).argmin())
            best_second = int(loss[row, :, ~mask].mean(axis=0).argmin())
            chosen_counts[best_first] += 1
            chosen_counts[best_second] += 1
            transferred = np.r_[loss[row, best_second, mask], loss[row, best_first, ~mask]]
            episode_errors.append(float(transferred.mean()))
        cross_errors.append(float(np.mean(episode_errors)))
    cross_errors = np.asarray(cross_errors)

    policies = pd.read_csv(directory / "policy_episode_outcomes.csv")
    policies = policies[np.isclose(policies["lambda"], 0)]
    names = data["action_names"].tolist()
    choices = {}
    for policy in ("cheap_only", "always_rich"):
        sub = policies[policies["policy"] == policy].set_index("episode_index")
        choices[policy] = np.array([names.index(sub.loc[int(index), "action"]) for index in indices])
    row = np.arange(len(indices))
    cheap_loss = loss[row, choices["cheap_only"]]
    rich_loss = loss[row, choices["always_rich"]]
    paired = cheap_loss - rich_loss
    unique_ids, inverse = np.unique(ids.reshape(-1), return_inverse=True)
    cluster_gain = np.bincount(inverse, weights=paired.reshape(-1))
    cluster_count = np.bincount(inverse)
    rng = np.random.default_rng(241023100)
    cluster_samples = rng.multinomial(len(unique_ids), np.full(len(unique_ids), 1 / len(unique_ids)),
                                     size=args.bootstrap_repeats)
    draws = (cluster_samples @ cluster_gain) / (cluster_samples @ cluster_count)
    interval = np.quantile(draws, [.025, .975])
    gain_by_identity = pd.DataFrame({"original_query_id": unique_ids,
                                    "query_occurrences": cluster_count,
                                    "sum_error_reduction_cheap_minus_rich": cluster_gain,
                                    "mean_error_reduction": cluster_gain / cluster_count})
    gain_by_identity.to_csv(directory / "audit_query_identity_gains.csv", index=False)
    result = {
        "scope": "Analysis of frozen source model, support batches and deployed selector choices; no model/controller refit",
        "primary_episodes": len(indices),
        "source_error": source_error,
        "observed_full_query_oracle_error": full_query_oracle_error,
        "observed_full_query_oracle_gain_over_source": source_error - full_query_oracle_error,
        "cross_query_identity_oracle": {
            "split_repeats": args.split_repeats,
            "mean_transfer_error": float(cross_errors.mean()),
            "mean_transfer_gain_over_source": float(source_error - cross_errors.mean()),
            "split_randomization_error_quantiles_2_5_97_5": np.quantile(cross_errors, [.025, .975]).tolist(),
            "action_choice_counts": dict(zip(names, chosen_counts.tolist())),
            "definition": "Within each episode split unique query IDs in two; use labels to select action on half and score other half, reverse and combine all 32 scoring draws. Repeated identity draws stay together. Ties favor SOURCE.",
            "limits": "Label-assisted retrospective diagnostic, not a deployable oracle or estimate of unlimited-data true action risk. Split quantiles measure random partition sensitivity, not independent population uncertainty.",
        },
        "cheap_vs_rich_query_identity_cluster_bootstrap": {
            "mean_error_reduction": float(paired.mean()),
            "interval_95": interval.tolist(),
            "bootstrap_repeats": args.bootstrap_repeats,
            "unique_query_identity_clusters": len(unique_ids),
            "query_occurrences": int(ids.size),
            "positive_bootstrap_fraction": float(np.mean(draws > 0)),
            "definition": "Resample original query identities, keeping every occurrence of a sampled identity across all final episodes together; recompute weighted cheap-minus-rich error reduction.",
            "limits": "Policies, source fit, support sets and family construction remain fixed. Correlation induced by repeated support IDs and shared fitted models is not removed. This is a more dependence-aware conditional sensitivity analysis, not a full population confidence guarantee.",
        },
    }
    (directory / "audit_headroom.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

"""Independent finite-difference and saved-artifact checks for the diagnostic.

Only this audit script and audit.md are owned by the audit agent.
"""
from pathlib import Path
import importlib.util
import json
import sys
import hashlib
import argparse

import numpy as np


HERE = Path(__file__).resolve().parent


def entropy_gradient_check(module):
    rng = np.random.default_rng(8041)
    z = rng.normal(size=(17, 7))
    w = rng.normal(scale=0.4, size=(7, 5))
    b = rng.normal(scale=0.1, size=5)
    gamma = rng.normal(loc=1.0, scale=0.2, size=7)
    beta = rng.normal(scale=0.2, size=7)
    scalar, dg, db = module.entropy_and_grad(z, w, b, gamma, beta)
    errors = {}
    epsilon = 1e-5
    for name, parameter, analytic in (("gamma", gamma, dg), ("beta", beta, db)):
        numerical = np.empty_like(parameter)
        for j in range(len(parameter)):
            plus = parameter.copy()
            minus = parameter.copy()
            plus[j] += epsilon
            minus[j] -= epsilon
            if name == "gamma":
                vp = module.entropy_and_grad(z, w, b, plus, beta)[0]
                vm = module.entropy_and_grad(z, w, b, minus, beta)[0]
            else:
                vp = module.entropy_and_grad(z, w, b, gamma, plus)[0]
                vm = module.entropy_and_grad(z, w, b, gamma, minus)[0]
            numerical[j] = (vp - vm) / (2 * epsilon)
        absolute = float(np.max(np.abs(numerical - analytic)))
        errors[name] = {"max_absolute_error": absolute,
                        "max_relative_error": float(np.max(np.abs(numerical - analytic) /
                                                            np.maximum(1e-8, np.abs(numerical)))),
                        "passed_at_1e-6_absolute": absolute < 1e-6}
    return {"entropy": float(scalar), "coordinates_checked": 14, "epsilon": epsilon, **errors}


def state_and_split_check(module):
    from sklearn.datasets import load_digits
    digits = load_digits()
    x = digits.data / 16.
    splits = json.loads((HERE / "splits.json").read_text())
    keys = list(splits)
    intersections = {f"{left}/{right}": len(set(splits[left]) & set(splits[right]))
                     for i, left in enumerate(keys) for right in keys[i + 1:]}
    union = set().union(*(set(values) for values in splits.values()))
    model = module.load_model()
    before = {key: hashlib.sha256(value.tobytes()).hexdigest() for key, value in model.items()}
    support = x[np.array(splits["meta_train"][:16])]
    query = x[np.array(splits["meta_cal"][:32])]
    rng = np.random.default_rng(81)
    support = np.clip(support + rng.normal(0, 0.15, size=support.shape), 0, 1)
    query = np.clip(query + rng.normal(0, 0.15, size=query.shape), 0, 1)
    action_checks = {}
    for action in module.ACTIONS:
        full = module.action_predict(model, support, query, action)["probs"]
        first = module.action_predict(model, support, query[:1], action)["probs"]
        after = {key: hashlib.sha256(value.tobytes()).hexdigest() for key, value in model.items()}
        context_delta = float(np.max(np.abs(full[:1] - first)))
        action_checks[action] = {
            "source_state_unchanged": before == after,
            "probabilities_finite": bool(np.isfinite(full).all()),
            "probability_sum_max_error": float(np.max(np.abs(full.sum(1) - 1))),
            "query_context_max_difference": context_delta,
            "pointwise_query_at_1e-10": context_delta < 1e-10,
        }
    mean, var, gamma, beta = module.support_state(model, support, "ENTROPY")
    z = (module.hidden(model, support) - mean) / np.sqrt(var + module.EPS)
    initial_h = module.entropy_and_grad(z, model["head_W"], model["head_b"],
                                        np.ones_like(gamma), np.zeros_like(beta))[0]
    final_h = module.entropy_and_grad(z, model["head_W"], model["head_b"], gamma, beta)[0]
    return {
        "split_sizes": {key: len(value) for key, value in splits.items()},
        "pairwise_intersection_counts": intersections,
        "union_size": len(union),
        "complete_dataset_partition": union == set(range(len(x))),
        "action_checks": action_checks,
        "support_entropy_before": initial_h,
        "support_entropy_after": final_h,
        "entropy_decreased_on_checked_support": final_h <= initial_h,
    }


def outcome_check():
    from sklearn.datasets import load_digits
    from scipy.special import softmax
    digits = load_digits()
    design = json.loads((HERE / "outcomes_design.json").read_text())
    data = np.load(HERE / "outcomes.npz", allow_pickle=False)
    pool_sets = {key: set(value) for key, value in design["meta_pool_ids"].items()}
    sample_overlap = []
    containment_failures = []
    for row, group in enumerate(data["groups"]):
        support = set(data["support_ids"][row][data["support_ids"][row] >= 0].tolist())
        query = set(data["query_ids"][row].tolist())
        if support & query:
            sample_overlap.append(row)
        if not (support | query) <= pool_sets[group]:
            containment_failures.append(row)
    label_match = bool(np.array_equal(data["query_labels"], digits.target[data["query_ids"]]))
    reconstructed = np.mean(data["predictions"] != data["query_labels"][:, None, :], axis=2)
    error_difference = float(np.max(np.abs(reconstructed - data["errors"])))
    heldout = set(design["heldout_families"])
    seen_train = set(data["families"][data["splits"] == "train"].tolist())
    seen_cal = set(data["families"][data["splits"] == "cal"].tolist())
    feature_finite = {key: bool(np.isfinite(data[key]).all()) for key in ("cheap", "rich")}
    timing = {key: {"finite": bool(np.isfinite(data[key]).all()),
                    "positive": bool((data[key] > 0).all()),
                    "median_ms": float(np.median(data[key]))}
              for key in ("action_cost_ms", "cheap_cost_ms", "rich_extra_cost_ms")}
    pool_pairs = {f"{left}/{right}": len(pool_sets[left] & pool_sets[right])
                  for i, left in enumerate(pool_sets) for right in list(pool_sets)[i + 1:]}
    primary = (data["splits"] == "test") & data["heldout_family"]
    unique_queries = np.array([len(set(row.tolist())) for row in data["query_ids"]])
    return {
        "episodes": len(data["splits"]),
        "primary_heldout_family_test_episodes": int(primary.sum()),
        "support_query_overlap_episode_ids": sample_overlap,
        "group_pool_containment_failures": containment_failures,
        "pairwise_meta_pool_overlap": pool_pairs,
        "query_labels_match_original_dataset": label_match,
        "error_reconstruction_max_difference": error_difference,
        "heldout_families_absent_from_train_and_cal": not bool(heldout & (seen_train | seen_cal)),
        "feature_values_finite": feature_finite,
        "rich_prefix_equals_cheap": bool(np.array_equal(data["cheap"], data["rich"][:, :data["cheap"].shape[1]])),
        "timing_checks": timing,
        "query_unique_min": int(unique_queries.min()),
        "episodes_with_repeated_query_draws": int((unique_queries < 32).sum()),
        "test_image_ids_available": len(set(data["query_ids"][data["splits"] == "test"].reshape(-1).tolist())),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", type=Path, default=HERE)
    args = parser.parse_args()
    HERE = args.directory.resolve()
    spec = importlib.util.spec_from_file_location("diagnostic_core_audit", HERE / "core_model.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    result = {"entropy_gradient": entropy_gradient_check(module)}
    if (HERE / "source_model.npz").exists() and (HERE / "splits.json").exists():
        result["state_and_splits"] = state_and_split_check(module)
    if (HERE / "outcomes.npz").exists():
        result["outcome_checks"] = outcome_check()
    (HERE / "audit_results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))

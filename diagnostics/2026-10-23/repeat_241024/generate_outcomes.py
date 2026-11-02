"""Generate a bounded CPU action/evidence diagnostic on bundled digits.

Custom shifted digits, not CIFAR-C and not an exact paper reproduction.
All episode design is saved before evaluating candidate action outcomes.
"""
from __future__ import annotations

import os
for _name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_name] = "1"

from pathlib import Path
import argparse
import hashlib
import json
import time

import numpy as np
import pandas as pd
from scipy.ndimage import gaussian_filter, shift
from sklearn.datasets import load_digits

from core_model import ACTIONS, load_model, source_predict, cheap_features, rich_features, action_predict

HERE = Path(__file__).resolve().parent
TRAIN_FAMILIES = ("clean", "noise", "brightness", "blur", "translation")
HELDOUT_FAMILIES = ("contrast", "occlusion")
ALL_FAMILIES = TRAIN_FAMILIES + HELDOUT_FAMILIES


def transform(x: np.ndarray, family: str, severity: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    images = np.asarray(x, dtype=np.float64).reshape(-1, 8, 8).copy()
    if family == "noise":
        images += rng.normal(0, (0.15, 0.35)[severity], size=images.shape)
    elif family == "brightness":
        images -= (0.18, 0.35)[severity]
    elif family == "blur":
        images = gaussian_filter(images, sigma=(0, (0.5, 0.9)[severity], (0.5, 0.9)[severity]), mode="nearest")
    elif family == "translation":
        images = shift(images, shift=(0, 1, severity), order=1, mode="constant", cval=0)
    elif family == "contrast":
        images = (images - 0.5) * (0.6, 0.3)[severity] + 0.5
    elif family == "occlusion":
        side = (2, 3)[severity]
        # Independent random positions, same declared transform mechanism for S/Q.
        for image in images:
            top, left = rng.integers(1, 8 - side, size=2)
            image[top:top + side, left:left + side] = 0
    elif family != "clean":
        raise ValueError(family)
    return np.clip(images, 0, 1).reshape(-1, 64)


def split_candidate_pools(ids, labels, rng):
    support, query = [], []
    for label in range(10):
        group = np.asarray(ids)[labels[np.asarray(ids)] == label].copy()
        rng.shuffle(group)
        midpoint = len(group) // 2
        support.extend(group[:midpoint].tolist())
        query.extend(group[midpoint:].tolist())
    return np.asarray(support, dtype=int), np.asarray(query, dtype=int)


def draw(pool, labels, count, prior, dominant, rng):
    if prior == "balanced":
        wanted = np.tile(np.arange(10), int(np.ceil(count / 10)))[:count]
        rng.shuffle(wanted)
    else:
        major = int(round(0.75 * count))
        alternatives = np.asarray([c for c in range(10) if c != dominant])
        wanted = np.r_[np.full(major, dominant), rng.choice(alternatives, count - major)]
        rng.shuffle(wanted)
    result = []
    for label in range(10):
        n = int(np.sum(wanted == label))
        if not n:
            continue
        candidates = pool[labels[pool] == label]
        if not len(candidates):
            raise ValueError(f"Missing class {label} in candidate pool")
        result.extend(rng.choice(candidates, size=n, replace=n > len(candidates)).tolist())
    result = np.asarray(result, dtype=int)
    rng.shuffle(result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=4)
    parser.add_argument("--model", type=Path, default=HERE / "source_model.npz")
    parser.add_argument("--splits", type=Path, default=HERE / "splits.json")
    args = parser.parse_args()
    started = time.perf_counter()
    dataset = load_digits()
    X = np.asarray(dataset.data, dtype=np.float64) / 16.0
    y = np.asarray(dataset.target, dtype=int)
    model = load_model(args.model)
    partition = json.loads(args.splits.read_text())
    # Core split record may nest the actual mapping under a metadata field.
    if "partitions" in partition:
        partition = partition["partitions"]
    elif "splits" in partition:
        partition = partition["splits"]
    ids = {}
    for key in ("source_fit", "meta_train", "meta_cal", "final_test"):
        value = partition[key]
        if isinstance(value, dict):
            value = value.get("ids", value.get("indices"))
        ids[key] = np.asarray(value, dtype=int)
    pool_rng = np.random.default_rng(7221)
    train_groups = [[], []]
    for label in range(10):
        local = ids["meta_train"][y[ids["meta_train"]] == label].copy()
        pool_rng.shuffle(local)
        for i, part in enumerate(np.array_split(local, 2)):
            train_groups[i].extend(part.tolist())
    pools = [("train", "train_pool_0", np.asarray(train_groups[0])),
             ("train", "train_pool_1", np.asarray(train_groups[1])),
             ("cal", "cal_pool", ids["meta_cal"]),
             ("test", "test_pool", ids["final_test"])]
    config = {
        "date": "2026-10-23", "setting": "custom shifted bundled digits; alternate-data mechanism diagnostic",
        "train_families": list(TRAIN_FAMILIES), "heldout_families": list(HELDOUT_FAMILIES),
        "support_batch_sizes": [16, 32], "query_draws": 32, "severities": [0, 1],
        "trials": args.trials, "prior_conditions": ["balanced", "75pct_dominant"],
        "sampling": "S/Q candidate pools disjoint by original image ID. Per-class draws use replacement only when requested class counts exceed available images, explicitly recorded.",
        "meta_pool_ids": {group: pool.tolist() for _, group, pool in pools},
        "fixed_seed": 7221, "actions": list(ACTIONS),
        "dataset_sha256": hashlib.sha256(dataset.data.tobytes() + dataset.target.tobytes()).hexdigest(),
        "split_sha256": hashlib.sha256(args.splits.read_bytes()).hexdigest(),
        "no_target_labels_in_features": True,
    }
    (HERE / "outcomes_design.json").write_text(json.dumps(config, indent=2) + "\n")
    # Warm up the tiny numerical routines; this is excluded from deployment cost.
    for _ in range(10):
        source_predict(model, X[ids["source_fit"][:32]])
    metadata, cheap_rows, rich_rows, errors, nlls, costs, cheap_costs, rich_costs = [], [], [], [], [], [], [], []
    query_ids_rows, support_ids_rows, prediction_rows, label_rows = [], [], [], []
    ensemble_errors, ensemble_nlls, ensemble_costs, ensemble_predictions = [], [], [], []
    index = 0
    for split_name, group_name, pool in pools:
        families = ALL_FAMILIES if split_name == "test" else TRAIN_FAMILIES
        for family_i, family in enumerate(families):
            levels = [0] if family == "clean" else [0, 1]
            for level in levels:
                for batch_size in (16, 32):
                    for prior in ("balanced", "75pct_dominant"):
                        for trial in range(args.trials):
                            seed = 100000 + index * 13
                            rng = np.random.default_rng(seed)
                            support_pool, query_pool = split_candidate_pools(pool, y, rng)
                            dominant = int(rng.integers(10))
                            support_ids = draw(support_pool, y, batch_size, prior, dominant, rng)
                            query_ids = draw(query_pool, y, 32, prior, dominant, rng)
                            S = transform(X[support_ids], family, level, seed + 1)
                            Q = transform(X[query_ids], family, level, seed + 2)
                            cheap, cheap_ms = cheap_features(model, S)
                            rich, rich_ms = rich_features(model, S, cheap=cheap)
                            action_results = {}
                            for a in rng.permutation(len(ACTIONS)):
                                action_results[int(a)] = action_predict(model, S, Q, ACTIONS[int(a)])
                            probs = np.asarray([action_results[a]["probs"] for a in range(len(ACTIONS))])
                            predicted = probs.argmax(axis=2)
                            error = np.mean(predicted != y[query_ids][None, :], axis=1)
                            logloss = -np.log(np.maximum(probs[:, np.arange(32), y[query_ids]], 1e-12)).mean(axis=1)
                            durations = np.asarray([action_results[a]["elapsed_ms"] for a in range(len(ACTIONS))])
                            ensemble_start = time.perf_counter()
                            query_images = Q.reshape(-1, 8, 8)
                            qv1 = shift(query_images, (0, 0, 0.35), order=1, mode="nearest", prefilter=False).reshape(-1, 64)
                            qv2 = shift(query_images, (0, 0, -0.35), order=1, mode="nearest", prefilter=False).reshape(-1, 64)
                            ensemble_probs = (source_predict(model, Q)[0] + source_predict(model, qv1)[0] + source_predict(model, qv2)[0]) / 3
                            ensemble_ms = 1000 * (time.perf_counter() - ensemble_start)
                            ensemble_pred = ensemble_probs.argmax(axis=1)
                            ensemble_error = float(np.mean(ensemble_pred != y[query_ids]))
                            ensemble_nll = float(-np.log(np.maximum(ensemble_probs[np.arange(32), y[query_ids]], 1e-12)).mean())
                            ensemble_errors.append(ensemble_error)
                            ensemble_nlls.append(ensemble_nll)
                            ensemble_costs.append(ensemble_ms)
                            ensemble_predictions.append(ensemble_pred)
                            padded_support = np.full(32, -1, dtype=int)
                            padded_support[:batch_size] = support_ids
                            support_ids_rows.append(padded_support)
                            query_ids_rows.append(query_ids)
                            prediction_rows.append(predicted)
                            label_rows.append(y[query_ids])
                            cheap_rows.append(cheap)
                            rich_rows.append(rich)
                            errors.append(error)
                            nlls.append(logloss)
                            costs.append(durations)
                            cheap_costs.append(cheap_ms)
                            rich_costs.append(rich_ms)
                            row = {"episode_id": index, "split": split_name, "group": group_name,
                                   "family": family, "severity": level, "batch_size": batch_size,
                                   "prior": prior, "dominant_class": dominant, "trial": trial, "seed": seed,
                                   "queryn": 32, "support_unique": len(np.unique(support_ids)),
                                   "query_unique": len(np.unique(query_ids)),
                                   "support_query_overlap": len(np.intersect1d(support_ids, query_ids)),
                                   "is_heldout_family": family in HELDOUT_FAMILIES,
                                   "cheap_cost_ms": cheap_ms, "rich_extra_cost_ms": rich_ms}
                            row.update({"ensemble_error": ensemble_error, "ensemble_nll": ensemble_nll,
                                        "ensemble_cost_ms": ensemble_ms, "ensemble_forward_images": 96})
                            for a, action in enumerate(ACTIONS):
                                row[f"error_{action}"] = error[a]
                                row[f"nll_{action}"] = logloss[a]
                                row[f"cost_ms_{action}"] = durations[a]
                                row[f"forward_images_{action}"] = action_results[a].get("forward_images", 0)
                                row[f"backward_images_{action}"] = action_results[a].get("backward_images", 0)
                                row[f"head_forward_images_{action}"] = action_results[a].get("head_forward_images", action_results[a]["forward_images"])
                            metadata.append(row)
                            index += 1
        print(json.dumps({"completed_pool": group_name, "episodes": index, "elapsed_seconds": time.perf_counter() - started}), flush=True)
    frame = pd.DataFrame(metadata)
    frame.to_csv(HERE / "episodes.csv", index=False)
    np.savez_compressed(HERE / "outcomes.npz", cheap=np.asarray(cheap_rows), rich=np.asarray(rich_rows),
        errors=np.asarray(errors), nll=np.asarray(nlls), action_cost_ms=np.asarray(costs),
        cheap_cost_ms=np.asarray(cheap_costs), rich_extra_cost_ms=np.asarray(rich_costs),
        families=frame.family.to_numpy(dtype=str), splits=frame.split.to_numpy(dtype=str),
        groups=frame.group.to_numpy(dtype=str), queryn=frame.queryn.to_numpy(),
        heldout_family=frame.is_heldout_family.to_numpy(), support_ids=np.asarray(support_ids_rows),
        query_ids=np.asarray(query_ids_rows), predictions=np.asarray(prediction_rows),
        query_labels=np.asarray(label_rows), action_names=np.asarray(ACTIONS),
        ensemble_errors=np.asarray(ensemble_errors), ensemble_nll=np.asarray(ensemble_nlls),
        ensemble_cost_ms=np.asarray(ensemble_costs), ensemble_predictions=np.asarray(ensemble_predictions))
    summary = {"episodes": len(frame), "by_split": frame.groupby("split").size().to_dict(),
               "heldout_test_episodes": int(((frame.split == "test") & frame.is_heldout_family).sum()),
               "cheap_dimensions": int(np.asarray(cheap_rows).shape[1]),
               "rich_dimensions": int(np.asarray(rich_rows).shape[1]),
               "elapsed_seconds": time.perf_counter() - started,
               "original_image_pools_disjoint": len(set().union(*(set(pool) for _, _, pool in pools))) == sum(len(pool) for _, _, pool in pools),
               "support_query_overlaps": int(frame.support_query_overlap.sum()),
               "source_fit_pool_disjoint": not any(np.intersect1d(ids['source_fit'], pool).size for _, _, pool in pools),
               "input_code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE / "outcomes_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()

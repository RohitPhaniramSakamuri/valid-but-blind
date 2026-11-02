"""CPU-only source classifier and support-only affine entropy adaptation.

This is a small mechanism diagnostic on sklearn digits, NOT a reproduction of
native Tent or any original CIFAR-C benchmark. The encoder is a learned MLP
hidden layer; source-standardized hidden activations feed a logistic head.
BN and ENTROPY replace hidden normalization statistics with support statistics;
those statistics remain fixed during disjoint query scoring. ENTROPY additionally
updates only the normalization affine gamma and beta using unlabeled support.
"""
from pathlib import Path
import time
import numpy as np
from scipy.special import softmax
from scipy.ndimage import shift as image_shift

HERE = Path(__file__).resolve().parent
ACTIONS = ("SOURCE", "BN", "ENTROPY")
ENTROPY_STEPS = 3
ENTROPY_LR = 0.05
EPS = 1e-3


def load_model(path=HERE / "source_model.npz"):
    with np.load(path) as record:
        return {key: record[key].copy() for key in record.files}


def hidden(model, X):
    return np.maximum(np.asarray(X, dtype=np.float64) @ model["encoder_W"] + model["encoder_b"], 0.)


def source_predict(model, X):
    h = hidden(model, X)
    z = (h - model["mean"]) / np.sqrt(model["var"] + EPS)
    return softmax(z @ model["head_W"] + model["head_b"], axis=1), z


def entropy_and_grad(z, W, b, gamma, beta):
    logits = (z * gamma + beta) @ W + b
    probabilities = softmax(logits, axis=1)
    logp = np.log(np.maximum(probabilities, 1e-300))
    per_entropy = -(probabilities * logp).sum(axis=1)
    dlogits = -probabilities * (logp + per_entropy[:, None]) / len(z)
    du = dlogits @ W.T
    return float(per_entropy.mean()), (du * z).sum(axis=0), du.sum(axis=0)


def support_state(model, S, action):
    hs = hidden(model, S)
    mean, var = hs.mean(axis=0), hs.var(axis=0)
    z = (hs - mean) / np.sqrt(var + EPS)
    gamma = np.ones(z.shape[1], dtype=np.float64)
    beta = np.zeros(z.shape[1], dtype=np.float64)
    if action == "ENTROPY":
        for _ in range(ENTROPY_STEPS):
            _, dg, db = entropy_and_grad(z, model["head_W"], model["head_b"], gamma, beta)
            # Fixed numerical guard, independent of evaluation outcomes.
            grad_norm = np.sqrt(np.sum(dg * dg) + np.sum(db * db))
            scale = min(1., 5. / max(float(grad_norm), 1e-12))
            gamma -= ENTROPY_LR * dg * scale
            beta -= ENTROPY_LR * db * scale
    return mean, var, gamma, beta


def action_predict(model, S, Q, action):
    if action not in ACTIONS:
        raise ValueError(action)
    start = time.perf_counter()
    if action == "SOURCE":
        probabilities, _ = source_predict(model, Q)
        forward = len(Q)
        backward = 0
        head_forward = len(Q)
    else:
        mean, var, gamma, beta = support_state(model, S, action)
        zq = (hidden(model, Q) - mean) / np.sqrt(var + EPS)
        probabilities = softmax((zq * gamma + beta) @ model["head_W"] + model["head_b"], axis=1)
        forward = len(S) + len(Q)
        backward = ENTROPY_STEPS * len(S) if action == "ENTROPY" else 0
        head_forward = len(Q) + backward
    return {"probs": probabilities, "elapsed_ms": 1000 * (time.perf_counter() - start),
            "forward_images": forward, "encoder_forward_images": forward,
            "head_forward_images": head_forward,
            "backward_images": backward, "affine_gradient_images": backward,
            "encoder_backward_images": 0}


def summarize(probabilities, z):
    entropy = -(probabilities * np.log(np.maximum(probabilities, 1e-300))).sum(axis=1)
    ranked = np.sort(probabilities, axis=1)
    confidence, margin = ranked[:, -1], ranked[:, -1] - ranked[:, -2]
    frequency = np.bincount(probabilities.argmax(axis=1), minlength=10) / len(probabilities)
    parts = [np.array([entropy.mean(), entropy.std(), confidence.mean(), confidence.std(),
                      margin.mean(), margin.std(), frequency.max(), np.sum(frequency ** 2)]),
             frequency, z.mean(axis=0), z.std(axis=0)]
    return np.concatenate(parts)


def cheap_features(model, S):
    start = time.perf_counter()
    probabilities, z = source_predict(model, S)
    features = summarize(probabilities, z)
    return features, 1000 * (time.perf_counter() - start)


def rich_features(model, S, cheap=None):
    """Returns concatenated features and EXTRA evidence cost (cheap is separate).

    Views globally fixed: mild left/right subpixel translations with nearest
    boundary handling. No corruption identifier selects augmentation parameters.
    Source observations are recomputed here for paired probability diagnostics,
    and that additional source pass is fully charged in the measured runtime.
    """
    start = time.perf_counter()
    if cheap is None:
        base_p, base_z = source_predict(model, S)
        cheap = summarize(base_p, base_z)
    else:
        base_p, _ = source_predict(model, S)
    images = np.asarray(S).reshape(-1, 8, 8)
    view1 = image_shift(images, (0, 0, 0.35), order=1, mode="nearest", prefilter=False).reshape(-1, 64)
    view2 = image_shift(images, (0, 0, -0.35), order=1, mode="nearest", prefilter=False).reshape(-1, 64)
    p1, z1 = source_predict(model, view1)
    p2, z2 = source_predict(model, view2)
    middle = (p1 + p2) / 2
    js = .5 * np.sum(p1 * np.log(np.maximum(p1, 1e-300) / np.maximum(middle, 1e-300)), axis=1)
    js += .5 * np.sum(p2 * np.log(np.maximum(p2, 1e-300) / np.maximum(middle, 1e-300)), axis=1)
    summary = np.array([js.mean(), js.std(), (p1.argmax(1) != p2.argmax(1)).mean(),
                        np.abs(p1 - base_p).mean(), np.abs(p2 - base_p).mean(),
                        p1.max(1).mean(), p2.max(1).mean(),
                        np.sqrt(np.square(z1 - z2).mean())])
    extra = np.concatenate([summary, p1.mean(axis=0), p2.mean(axis=0)])
    return np.concatenate([cheap, extra]), 1000 * (time.perf_counter() - start)


def evaluate_actions(model, support, query, yquery):
    results = {}
    for action in ACTIONS:
        outcome = action_predict(model, support, query, action)
        probabilities = outcome["probs"]
        outcome["accuracy"] = float((probabilities.argmax(1) == yquery).mean())
        outcome["nll"] = float(-np.log(np.maximum(probabilities[np.arange(len(yquery)), yquery], 1e-300)).mean())
        results[action] = outcome
    return results

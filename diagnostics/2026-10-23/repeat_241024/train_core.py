"""Train a small source model using only its declared source split."""
import os
for variable in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[variable] = "1"

from pathlib import Path
import hashlib
import json
import platform
import time
import warnings
import numpy as np
import scipy
import sklearn
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from threadpoolctl import threadpool_limits
from core_model import EPS, source_predict

HERE = Path(__file__).resolve().parent
SEED = 241024
start = time.perf_counter()
digits = load_digits()
X, y = digits.data.astype(np.float64) / 16., digits.target
ids = np.arange(len(y))
source_ids, remaining = train_test_split(ids, train_size=900, stratify=y, random_state=SEED)
meta_train, remaining = train_test_split(remaining, train_size=400, stratify=y[remaining], random_state=SEED + 1)
meta_cal, final_test = train_test_split(remaining, train_size=200, stratify=y[remaining], random_state=SEED + 2)
splits = {"source_fit": source_ids.tolist(), "meta_train": meta_train.tolist(),
          "meta_cal": meta_cal.tolist(), "final_test": final_test.tolist()}
(HERE / "splits.json").write_text(json.dumps(splits, indent=2) + "\n")
with threadpool_limits(limits=1), warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    encoder = MLPClassifier(hidden_layer_sizes=(32,), activation="relu", solver="lbfgs", alpha=.01,
                            max_iter=250, random_state=SEED, tol=1e-5)
    encoder.fit(X[source_ids], y[source_ids])
    h = np.maximum(X[source_ids] @ encoder.coefs_[0] + encoder.intercepts_[0], 0.)
    mean, var = h.mean(0), h.var(0)
    normalized = (h - mean) / np.sqrt(var + EPS)
    head = LogisticRegression(C=1., max_iter=500, solver="lbfgs", random_state=SEED)
    head.fit(normalized, y[source_ids])
model = {"encoder_W": encoder.coefs_[0], "encoder_b": encoder.intercepts_[0],
         "mean": mean, "var": var, "head_W": head.coef_.T, "head_b": head.intercept_}
np.savez_compressed(HERE / "source_model.npz", **model)
summaries = {}
for name in ("source_fit", "meta_train", "meta_cal"):
    selected = np.array(splits[name])
    probabilities, _ = source_predict(model, X[selected])
    summaries[name] = {"n": len(selected), "accuracy": float((probabilities.argmax(1) == y[selected]).mean()),
                       "nll": float(-np.log(np.maximum(probabilities[np.arange(len(selected)), y[selected]], 1e-300)).mean())}
record = {"dataset": "sklearn bundled digits, 1797 grayscale 8x8 images, labels0-9",
          "dataset_sha256": hashlib.sha256(digits.data.tobytes() + y.tobytes()).hexdigest(),
          "scaling": "divide pixels by16; no fitting of scaling on held-out data",
          "seed": SEED, "source_fit_n": 900, "feature_width": 32,
          "encoder": "MLPClassifier hidden32 ReLU, lbfgs alpha0.01 max_iter250",
          "head": "source-standardized hidden features + LogisticRegression C1 max_iter500",
          "python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__,
          "sklearn": sklearn.__version__, "threads": 1,
          "source_checks": summaries, "warnings": [str(item.message) for item in caught],
          "elapsed_seconds": time.perf_counter() - start,
          "adaptation": {"normalization": "support-only hidden means/variances frozen for query", "entropy_steps": 3,
                         "entropy_lr": .05, "gamma_beta_only": True, "head_encoder_frozen": True},
          "scope": "Alternate-data CPU mechanism demonstration; not native Tent/CIFAR-C reproduction"}
(HERE / "source_manifest.json").write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps(record, indent=2))

"""Saves the exact replication draws (draws 0 and 1) as index arrays, so the authors' pipeline sees the same batches as the port."""
import numpy as np

import run as R
import run_monitor as M
from run_confirm import stream

labels = np.load("data/CIFAR-100-C/labels.npy")[:10000].astype(np.int64)
perm = np.random.RandomState(R.SPLIT_SEED).permutation(10000)
out = {"calib_ids": perm[:1000]}
for c in M.CORRUPTIONS:
    for s in R.SEVERITIES:
        for d in range(2):
            rng = np.random.RandomState(R.seed_of("exp004-replicate", c, s, d))
            out[f"{c}/{s}/{d}"] = np.stack(stream("dirichlet", 0.1, perm[1000:5000], labels, rng))
np.savez("authors_streams.npz", **out)

"""Runs the authors' monitor.py evaluate() on one replication draw. Their files stay as in cifar100_calibration.patch.
Only load_dataset and load_calibration_dataset are replaced at run time, to supply our batches and our 1,000 calibration IDs.
Run from inside tta-monitor: authors_stream.py ARCH ARM CORRUPTION SEVERITY DRAW
"""
import glob
import json
import os
import pickle
import shutil
import sys

import numpy as np
import torch
from torch.utils.data import DataLoader, TensorDataset

ROOT = "/root/exp004"
arch, arm, corr, sev, draw = sys.argv[1:6]
run = f"_{arch}_{corr}_{sev}_{draw}"
tmp = f"{ROOT}/authors_tmp/{arm}{run}"
sys.argv = ["monitor.py", "--cfg", "cfgs/cifar100/tent.yaml", "MODEL.ARCH", arch, "MODEL.ADAPTATION", arm, "RUN_NAME", run,
            "MONITORING.ERROR_DIST", "expectation", "MONITORING.E", "0_1_loss", "MONITORING.E_HAT", "max_class_prob", "MONITORING.CONT_CALIB", "True",
            "MONITORING.CALIB_SIZE", "1000", "MONITORING.CALIB_PROC", "max_f1", "MONITORING.CONT_CALIB_PROC", "max_f1", "CORRUPTION.SEVERITY", f"[{sev}]",
            "CORRUPTION.TYPE", f'["{corr}"]', "MONITORING.CALIB_SEED", "12", "RNG_SEED", "12", "TEST.SAVE", "True", "SAVE_PATH", tmp, "OPTIM.LR", "0.001",
            "DATA_DIR", f"{ROOT}/data", "CKPT_DIR", f"{ROOT}/models"]
sys.path.insert(0, os.getcwd())
import monitor  # noqa: E402
import lib.calibration as C  # noqa: E402

Z = np.load(f"{ROOT}/authors_streams.npz")
labels = np.load(f"{ROOT}/data/CIFAR-100-C/labels.npy")[:10000].astype(np.int64)
with open(f"{ROOT}/data/cifar-100-python/test", "rb") as f:
    d = pickle.load(f, encoding="latin1")
clean = d["data"].reshape(-1, 3, 32, 32)
ids = Z["calib_ids"]


def calib(*a, **k):
    return torch.from_numpy(clean[ids]).float().div_(255), torch.from_numpy(labels[ids])


def stream(*a, **k):
    b = Z[f"{corr}/{sev}/{draw}"].reshape(-1)
    arr = np.load(f"{ROOT}/data/CIFAR-100-C/{corr}.npy", mmap_mode="r")[(int(sev) - 1) * 10000:int(sev) * 10000]
    x = torch.from_numpy(np.array(arr[b])).permute(0, 3, 1, 2).float().div_(255)
    return DataLoader(TensorDataset(x, torch.from_numpy(labels[b])), batch_size=100, shuffle=False)


monitor.load_dataset, monitor.load_calibration_dataset, C.load_calibration_dataset = stream, calib, calib
monitor.evaluate("evaluation")

root = f"{tmp}/saved/cifar100/{arm}{run}"
cal = torch.load(f"{root}/calib.pt", map_location="cpu")
base = glob.glob(f"{root}/{corr}/{sev}/*_output_0.pt")[0][:-len("_output_0.pt")]
n = len(glob.glob(base + "_output_*.pt"))
L = [torch.load(f"{base}_output_{i}.pt", map_location="cpu") for i in range(n)]
Y = [torch.load(f"{base}_labels_{i}.pt", map_location="cpu") for i in range(n)]
if os.path.exists(f"{base}_qhat_0.pt"):
    Q = torch.tensor([float(torch.load(f"{base}_qhat_{i}.pt", map_location="cpu")) for i in range(n)])
else:
    Q = torch.full((n,), float(cal["q_hat"]))
L, Y = torch.stack(L), torch.stack(Y)
P = L.softmax(-1).max(-1)
u = 1 - P.values
row = dict(key=f"{arm}/{corr}/{sev}/dirichlet/0.1/{draw}", arch=arch, arm=arm, corruption=corr, severity=int(sev), rep=int(draw),
           err=(P.indices != Y).float().mean(1).tolist(), pos=(u > Q[:, None]).float().mean(1).tolist(), q_hat=Q.tolist(), conf=P.values.mean(1).tolist(),
           r0=float(cal["mean_error"]), L_1=float(cal["L_1"]), q_hat0=float(cal["q_hat"]))
with open(f"{ROOT}/authors_{arch}.jsonl", "a") as out:
    out.write(json.dumps(row) + "\n")
shutil.rmtree(tmp, ignore_errors=True)

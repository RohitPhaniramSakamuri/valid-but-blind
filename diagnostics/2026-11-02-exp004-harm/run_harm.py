"""Experiment 004 adaptation-harm test of the twin alarm. Frozen before running.

Aim: make Tent fail while its entropy-free twin stays fine. Tent uses high learning rates on easy data, IDs perm[5000:9000]. Twin threshold and
the alarm statistic are frozen from analyze_twin.py (w = 1, c = 1). The released monitor runs on the same streams, recalibrated each batch.
Grid per model: clean, snow, fog, contrast, jpeg_compression at severity 1 (clean has one form); Dirichlet 0.1 and balanced; Adam lr 1e-2 and 5e-2; one draw.
Plus by-class clean streams at lr 1e-3 and 1e-2. By-class streams can also break the twin's batch statistics, which the analysis keeps visible.
"""
import json
import os
import sys
import time

import numpy as np
import torch

import run as R
import run_monitor as M
from run_confirm import stream
from run_factorial import threshold
from run_replicate import loader

CS = [("clean", 0), ("snow", 1), ("fog", 1), ("contrast", 1), ("jpeg_compression", 1)]


def plan():
    p = [(k, c, s, lr) for c, s in CS for k in ("dirichlet", "balanced_wr") for lr in (1e-2, 5e-2)]
    return p + [("by_class", "clean", 0, 1e-3), ("by_class", "clean", 0, 1e-2)]


def main(name):
    out_dir, ckpt = f"results_harm_{name}", f"models/{name}.pt"
    R.load_model = loader(name)
    device = "cuda"
    torch.backends.cudnn.benchmark = True
    torch.set_num_threads(1)
    os.makedirs(out_dir, exist_ok=True)
    labels = np.load("data/CIFAR-100-C/labels.npy")[:10000].astype(np.int64)
    clean_x, clean_y = M.load_clean("data/cifar-100-python")
    assert (clean_y == labels).all()
    perm = np.random.RandomState(R.SPLIT_SEED).permutation(10000)
    calib_ids, ids = perm[:1000], perm[5000:9000]
    images = {("clean", 0): torch.from_numpy(clean_x.copy()).to(device)}
    for c, s in CS[1:]:
        arr = np.load(f"data/CIFAR-100-C/{c}.npy", mmap_mode="r")
        images[(c, s)] = torch.from_numpy(np.array(arr[(s - 1) * 10000:s * 10000])).to(device)
    y_all = torch.from_numpy(labels).to(device)
    source = R.load_model(ckpt, device, False).eval().requires_grad_(False)
    cx, cy = M.to_tensor(clean_x[calib_ids], device), y_all[torch.from_numpy(calib_ids).to(device)]
    lg = M.outputs(source, cx)
    err0, prox0 = lg.argmax(1) != cy, M.proxy_of(lg)
    q0 = M.max_f1(err0, prox0, device)
    del source
    twin, _ = M.make_tent(ckpt, device)
    twin = twin.requires_grad_(False)
    with torch.inference_mode():
        lt = M.outputs(twin, cx)
    et, pt = lt.argmax(1) != cy, M.proxy_of(lt)
    qt = M.max_f1(et, pt, device)
    ft = pt > qt
    json.dump(dict(model=name, r0=float(err0.float().mean()), q_hat0=q0, false_alarm0=float(((prox0 > q0) & ~err0).float().mean()), q_twin=qt, r_twin=float(et.float().mean()), fp_twin=float((ft & ~et).float().mean()), fn_twin=float((~ft & et).float().mean()), n_calib=len(cy), torch=torch.__version__, gpu=torch.cuda.get_device_name(0)), open(f"{out_dir}/calibration.json", "w"), indent=1)
    model, params = M.make_tent(ckpt, device)
    init = [p.detach().clone() for p in params]
    path = f"{out_dir}/streams.jsonl"
    done = {json.loads(l)["key"] for l in open(path)} if os.path.exists(path) else set()
    t0 = time.time()
    P = plan()
    with open(path, "a") as out:
        for n, (kind, c, s, lr) in enumerate(P):
            key = f"{kind}/{c}/{s}/{lr}"
            if key in done:
                continue
            rng = np.random.RandomState(R.seed_of("exp004-harm", kind, c, s))
            batches = torch.from_numpy(np.stack(stream(kind, 0.1, ids, labels, rng))).to(device)
            with torch.no_grad():
                for p, v in zip(params, init):
                    p.copy_(v)
            opt = torch.optim.Adam(params, lr=lr, betas=(0.9, 0.999), weight_decay=0.0)
            xs = images[(c, s)][batches].permute(0, 1, 4, 2, 3).float().div_(255)
            ys = y_all[batches]
            rows = []
            for x, y in zip(xs, ys):
                logits = model(x)
                loss = -(logits.softmax(1) * logits.log_softmax(1)).sum(1).mean()
                opt.zero_grad(set_to_none=True)
                loss.backward()
                opt.step()
                logits = logits.detach()
                qr = threshold(model, cx, cy, device)
                with torch.inference_mode():
                    lw = twin(x)
                E, A, F = logits.argmax(1) != y, logits.argmax(1) == lw.argmax(1), M.proxy_of(lw) > qt
                cells = torch.bincount(E.long() * 4 + F.long() * 2 + A.long(), minlength=8).float() / len(y)
                rows.append(torch.cat((cells, torch.stack(((M.proxy_of(logits) > qr).float().mean(), (lw.argmax(1) != y).float().mean(), 1 - M.proxy_of(logits).mean(), 1 - M.proxy_of(lw).mean())))))
            v = torch.stack(rows).T.tolist()
            out.write(json.dumps(dict(key=key, kind=kind, corruption=c, severity=s, lr=lr, cells=v[:8], pos_recal=v[8], twin_err=v[9], conf=v[10], conf_twin=v[11])) + "\n")
            out.flush()
            print(name, n + 1, len(P), key, f"err={np.sum(v[4:8], axis=0).mean():.3f}", f"twin={np.mean(v[9]):.3f}", f"elapsed={time.time() - t0:.0f}s", flush=True)
    print("complete", name, f"{time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main(sys.argv[1])

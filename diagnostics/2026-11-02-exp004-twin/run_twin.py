"""Experiment 004 entropy-free twin. Frozen before running.

Tent 1e-3 runs as in run_factorial.py. Beside it, a twin of the same checkpoint uses test-batch BN statistics and never takes a gradient
step. The twin's threshold, FP0 and FN0 are computed once on the 1,000 clean calibration images; there is no per-batch calibration pass.
Per batch we save the joint counts of Tent wrong (E), twin flagged (F) and predictions agree (A); labels only score results offline.
Streams: DEV noise and blur (replication IDs and seeds, draw 0), Dirichlet and balanced. HELD-OUT weather and digital (factorial IDs,
seeds, draws 0 and 1, so released-monitor results compare directly), Dirichlet; balanced draw 0. Clean: Dirichlet and balanced.
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
from run_replicate import loader

DEV, HELD = R.FAMILIES["noise"] + R.FAMILIES["blur"], R.FAMILIES["weather"] + R.FAMILIES["digital"]


def plan():
    p = []
    for c in DEV:
        for s in R.SEVERITIES:
            p.append(("dev", "dirichlet", c, s, 0, ("exp004-replicate", c, s, 0)))
            p.append(("dev", "balanced_wr", c, s, 0, ("exp004-twin", "bal", c, s, 0)))
    for c in HELD:
        for s in R.SEVERITIES:
            for d in range(2):
                p.append(("held", "dirichlet", c, s, d, ("exp004-factorial", c, s, d)))
            p.append(("held", "balanced_wr", c, s, 0, ("exp004-twin", "bal", c, s, 0)))
    p.append(("held", "dirichlet", "clean", 0, 0, ("exp004-twin", "clean", 0)))
    p.append(("held", "balanced_wr", "clean", 0, 0, ("exp004-twin", "cleanbal", 0)))
    return p


def main(name):
    out_dir, ckpt = f"results_twin_{name}", f"models/{name}.pt"
    R.load_model = loader(name)
    device = "cuda"
    torch.backends.cudnn.benchmark = True
    torch.set_num_threads(1)
    os.makedirs(out_dir, exist_ok=True)
    labels = np.load("data/CIFAR-100-C/labels.npy")[:10000].astype(np.int64)
    clean_x, clean_y = M.load_clean("data/cifar-100-python")
    assert (clean_y == labels).all()
    perm = np.random.RandomState(R.SPLIT_SEED).permutation(10000)
    calib_ids = perm[:1000]
    ids = dict(dev=perm[1000:5000], held=perm[5000:9000])
    images = {("clean", 0): torch.from_numpy(clean_x.copy()).to(device)}
    for c in DEV + HELD:
        arr = np.load(f"data/CIFAR-100-C/{c}.npy", mmap_mode="r")
        for s in R.SEVERITIES:
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
    json.dump(dict(model=name, r0=float(err0.float().mean()), q_hat0=q0, q_twin=qt, r_twin=float(et.float().mean()), fp_twin=float((ft & ~et).float().mean()), fn_twin=float((~ft & et).float().mean()), n_calib=len(cy), torch=torch.__version__, gpu=torch.cuda.get_device_name(0)), open(f"{out_dir}/calibration.json", "w"), indent=1)
    model, params = M.make_tent(ckpt, device)
    init = [p.detach().clone() for p in params]
    path = f"{out_dir}/streams.jsonl"
    done = {json.loads(l)["key"] for l in open(path)} if os.path.exists(path) else set()
    t0 = time.time()
    P = plan()
    with open(path, "a") as out:
        for n, (split, kind, c, s, d, seed) in enumerate(P):
            key = f"{split}/{kind}/{c}/{s}/{d}"
            if key in done:
                continue
            rng = np.random.RandomState(R.seed_of(*seed))
            batches = torch.from_numpy(np.stack(stream(kind, 0.1, ids[split], labels, rng))).to(device)
            with torch.no_grad():
                for p, v in zip(params, init):
                    p.copy_(v)
            opt = torch.optim.Adam(params, lr=1e-3, betas=(0.9, 0.999), weight_decay=0.0)
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
                with torch.inference_mode():
                    lw = twin(x)
                E, A, F = logits.argmax(1) != y, logits.argmax(1) == lw.argmax(1), M.proxy_of(lw) > qt
                idx = E.long() * 4 + F.long() * 2 + A.long()
                cells = torch.bincount(idx, minlength=8).float() / len(y)
                rows.append(torch.cat((cells, torch.stack(((M.proxy_of(logits) > q0).float().mean(), (lw.argmax(1) != y).float().mean(), 1 - M.proxy_of(logits).mean(), 1 - M.proxy_of(lw).mean())))))
            v = torch.stack(rows).T.tolist()
            out.write(json.dumps(dict(key=key, split=split, kind=kind, corruption=c, severity=s, rep=d, cells=v[:8], tent_fixed=v[8], twin_err=v[9], conf=v[10], conf_twin=v[11])) + "\n")
            out.flush()
            print(name, n + 1, len(P), key, f"err={np.sum(v[4:8], axis=0).mean():.3f}", f"elapsed={time.time() - t0:.0f}s", flush=True)
    print("complete", name, f"{time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main(sys.argv[1])

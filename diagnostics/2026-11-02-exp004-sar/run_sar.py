"""Experiment 004 SAR extension. Frozen before running.

Same harness, checkpoints, final IDs, weather and digital families, severities 3 and 5, Dirichlet 0.1 and draws as run_factorial.py,
so source, BN and Tent comparators are reused from it. SAR (Niu et al., ICLR 2023) at its published defaults: SGD lr 0.00025, momentum
0.9, SAM rho 0.05, entropy margin 0.4 ln(100), reset when the loss EMA falls below 0.2. Disclosed departures: BN models, as in every
arm here, and all BN layers update (the published code freezes top blocks of its own architectures). Predictions come from the first
forward pass, then the update, then threshold recalibration, matching the Tent arm.
"""
import copy
import json
import math
import os
import sys
import time

import numpy as np
import torch

import run as R
import run_monitor as M
from run_confirm import CORRUPTIONS, stream
from run_factorial import DRAWS, threshold
from run_replicate import loader

LR, MOMENTUM, RHO, RESET = 0.00025, 0.9, 0.05, 0.2
MARGIN = 0.4 * math.log(100)


def entropy(logits):
    return -(logits.softmax(1) * logits.log_softmax(1)).sum(1)


def sar_step(model, params, opt, x, state):
    logits = model(x)
    e1 = entropy(logits)
    keep1 = e1 < MARGIN
    resets = 0
    if keep1.any():
        opt.zero_grad(set_to_none=True)
        e1[keep1].mean().backward()
        grads = [p.grad for p in params if p.grad is not None]
        norm = torch.norm(torch.stack([g.norm(2) for g in grads]), 2)
        scale = RHO / (norm + 1e-12)
        saved = [p.detach().clone() for p in params]
        with torch.no_grad():
            for p in params:
                if p.grad is not None:
                    p.add_(p.grad * scale)
        opt.zero_grad(set_to_none=True)
        e2 = entropy(model(x))[keep1]
        keep2 = e2 < MARGIN
        if keep2.any():
            loss2 = e2[keep2].mean()
            loss2.backward()
            value = float(loss2.detach())
            state["ema"] = value if state["ema"] is None else 0.9 * state["ema"] + 0.1 * value
        with torch.no_grad():
            for p, v in zip(params, saved):
                p.copy_(v)
        if keep2.any():
            opt.step()
        opt.zero_grad(set_to_none=True)
    if state["ema"] is not None and state["ema"] < RESET:
        with torch.no_grad():
            for p, v in zip(params, state["init"]):
                p.copy_(v)
        opt.load_state_dict(copy.deepcopy(state["opt0"]))
        state["ema"] = None
        resets = 1
    return logits.detach(), float(keep1.float().mean()), resets


def main(name):
    out_dir, ckpt = f"results_sar_{name}", f"models/{name}.pt"
    R.load_model = loader(name)
    device = "cuda"
    torch.backends.cudnn.benchmark = True
    torch.set_num_threads(1)
    os.makedirs(out_dir, exist_ok=True)
    labels = np.load("data/CIFAR-100-C/labels.npy")[:10000].astype(np.int64)
    clean_x, clean_y = M.load_clean("data/cifar-100-python")
    assert (clean_y == labels).all()
    perm = np.random.RandomState(R.SPLIT_SEED).permutation(10000)
    calib_ids, stream_ids = perm[:1000], perm[5000:9000]
    images = {}
    for c in CORRUPTIONS:
        arr = np.load(f"data/CIFAR-100-C/{c}.npy", mmap_mode="r")
        for s in R.SEVERITIES:
            images[(c, s)] = torch.from_numpy(np.array(arr[(s - 1) * 10000:s * 10000])).to(device)
    y_all = torch.from_numpy(labels).to(device)
    source = R.load_model(ckpt, device, False).eval().requires_grad_(False)
    cx, cy = M.to_tensor(clean_x[calib_ids], device), y_all[torch.from_numpy(calib_ids).to(device)]
    lg = M.outputs(source, cx)
    err0, prox0 = lg.argmax(1) != cy, M.proxy_of(lg)
    q0 = M.max_f1(err0, prox0, device)
    json.dump(dict(model=name, r0=float(err0.float().mean()), q_hat0=q0, false_alarm0=float(((prox0 > q0) & ~err0).float().mean()), n_calib=len(cy), torch=torch.__version__, gpu=torch.cuda.get_device_name(0)), open(f"{out_dir}/calibration.json", "w"), indent=1)
    del source
    model, params = M.make_tent(ckpt, device)
    init = [p.detach().clone() for p in params]
    opt = torch.optim.SGD(params, lr=LR, momentum=MOMENTUM)
    opt0 = copy.deepcopy(opt.state_dict())
    plan = [(c, s, d) for c in CORRUPTIONS for s in R.SEVERITIES for d in range(DRAWS)]
    path = f"{out_dir}/streams.jsonl"
    done = {json.loads(l)["key"] for l in open(path)} if os.path.exists(path) else set()
    t0 = time.time()
    with open(path, "a") as out:
        for n, (c, s, d) in enumerate(plan):
            key = f"sar/{c}/{s}/dirichlet/0.1/{d}"
            if key in done:
                continue
            rng = np.random.RandomState(R.seed_of("exp004-factorial", c, s, d))
            batches = torch.from_numpy(np.stack(stream("dirichlet", 0.1, stream_ids, labels, rng))).to(device)
            with torch.no_grad():
                for p, v in zip(params, init):
                    p.copy_(v)
            opt.load_state_dict(copy.deepcopy(opt0))
            state = dict(ema=None, init=init, opt0=opt0)
            xs = images[(c, s)][batches].permute(0, 1, 4, 2, 3).float().div_(255)
            ys = y_all[batches]
            rows, kept, resets = [], [], 0
            for x, y in zip(xs, ys):
                logits, k, r = sar_step(model, params, opt, x, state)
                kept.append(k)
                resets += r
                qr = threshold(model, cx, cy, device)
                u, e = M.proxy_of(logits), logits.argmax(1) != y
                flags = u.unsqueeze(0) > torch.tensor([qr, q0], device=device).view(2, 1)
                rows.append(torch.stack((e.float().mean(), flags[0].float().mean(), flags[1].float().mean(), (~flags[0] & e).float().mean(), (~flags[1] & e).float().mean(), 1 - u.mean(), torch.tensor(qr, device=device))))
            v = torch.stack(rows).T.tolist()
            out.write(json.dumps(dict(key=key, arm="sar", corruption=c, severity=s, rep=d, err=v[0], pos_recal=v[1], pos_fixed=v[2], pfn_recal=v[3], pfn_fixed=v[4], conf=v[5], q_hat=v[6], kept=float(np.mean(kept)), resets=resets)) + "\n")
            out.flush()
            print(name, n + 1, len(plan), key, f"err={np.mean(v[0]):.3f}", f"kept={np.mean(kept):.2f}", f"resets={resets}", f"elapsed={time.time() - t0:.0f}s", flush=True)
    print("complete", name, f"{time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main(sys.argv[1])

"""Experiment 004 replication of Tent versus source. Frozen before running.

Six published checkpoints. Calibration: the same 1,000 clean development IDs as every earlier run.
Streams: the other 4,000 development IDs, noise and blur families, severities 3 and 5, Dirichlet
alpha 0.1, three draws, three epochs at batch 100. Draws use a new seed namespace and each draw is
identical for both arms. Tent and monitor settings are unchanged from run_second.py.
"""
import json
import os
import sys
import time

import numpy as np
import torch

import run as R
import run_monitor as M
import run_more
import run_second as RS
from run_confirm import stream

MODELS = ["Hendrycks2020AugMix_ResNeXt", "Modas2021PRIMEResNet18", "Hendrycks2020AugMix_WRN",
          "Addepalli2021Towards_PARN18", "Addepalli2021Towards_WRN34", "Addepalli2022Efficient_WRN_34_10"]
RESNEXT_LOAD = R.load_model
DRAWS = 3


def loader(name):
    if name == "Hendrycks2020AugMix_ResNeXt":
        return RESNEXT_LOAD
    if name == "Modas2021PRIMEResNet18":
        return RS.load
    return run_more.loader(name)


def main(name):
    out_dir, ckpt = f"results_{name}", f"models/{name}.pt"
    R.load_model = loader(name)
    device = "cuda"
    torch.backends.cudnn.benchmark = True
    os.makedirs(out_dir, exist_ok=True)
    labels_all = np.load("data/CIFAR-100-C/labels.npy")[:10000].astype(np.int64)
    clean_x, clean_y = M.load_clean("data/cifar-100-python")
    if not (clean_y == labels_all).all():
        raise SystemExit("Clean labels do not match CIFAR-100-C labels")
    perm = np.random.RandomState(R.SPLIT_SEED).permutation(10000)
    calib_ids, stream_ids = perm[:1000], perm[1000:5000]
    corruptions = M.CORRUPTIONS
    images = {}
    for c in corruptions:
        arr = np.load(f"data/CIFAR-100-C/{c}.npy", mmap_mode="r")
        for s in R.SEVERITIES:
            images[(c, s)] = torch.from_numpy(np.array(arr[(s - 1) * 10000:s * 10000])).to(device)
    y_all = torch.from_numpy(labels_all).to(device)

    source = R.load_model(ckpt, device, False).eval()
    for p in source.parameters():
        p.requires_grad_(False)
    cx, cy = M.to_tensor(clean_x[calib_ids], device), y_all[torch.from_numpy(calib_ids).to(device)]
    lg = M.outputs(source, cx)
    err0, prox0 = lg.argmax(1) != cy, M.proxy_of(lg)
    q0 = M.max_f1(err0, prox0, device)
    meta = dict(model=name, r0=float(err0.float().mean()), q_hat0=q0, false_alarm0=float(((prox0 > q0) & ~err0).float().mean()),
                n_calib=len(cy), torch=torch.__version__, gpu=torch.cuda.get_device_name(0))
    json.dump(meta, open(f"{out_dir}/calibration.json", "w"), indent=1)
    print(meta, flush=True)

    model, params = M.make_tent(ckpt, device)
    init = [p.detach().clone() for p in params]
    plan = [(arm, c, s, d) for c in corruptions for s in R.SEVERITIES for d in range(DRAWS) for arm in ("source", "tent")]
    path = f"{out_dir}/streams.jsonl"
    done = {json.loads(l)["key"] for l in open(path)} if os.path.exists(path) else set()
    t0 = time.time()
    with open(path, "a") as out:
        for n, (arm, c, s, d) in enumerate(plan):
            key = f"{arm}/{c}/{s}/dirichlet/0.1/{d}"
            if key in done:
                continue
            rng = np.random.RandomState(R.seed_of("exp004-replicate", c, s, d))
            if arm == "tent":
                with torch.no_grad():
                    for p, v in zip(params, init):
                        p.copy_(v)
                opt = torch.optim.Adam(params, lr=1e-3, betas=(0.9, 0.999), weight_decay=0.0)
            rec = {k: [] for k in ("err", "pos", "pfa", "pfn", "q_hat", "conf", "top_share", "disagree", "src_conf")}
            data = images[(c, s)]
            for b in stream("dirichlet", 0.1, stream_ids, labels_all, rng):
                idx = torch.from_numpy(b).to(device)
                x = data[idx].permute(0, 3, 1, 2).float().div_(255)
                y = y_all[idx]
                if arm == "source":
                    with torch.no_grad():
                        logits = source(x)
                    q = q0
                else:
                    logits = model(x)
                    loss = -(logits.softmax(1) * logits.log_softmax(1)).sum(1).mean()
                    opt.zero_grad()
                    loss.backward()
                    opt.step()
                    logits = logits.detach()
                    l = M.outputs(model, cx)
                    q = M.max_f1(l.argmax(1) != cy, M.proxy_of(l), device)
                with torch.no_grad():
                    src = source(x) if arm != "source" else logits
                e, u = logits.argmax(1) != y, M.proxy_of(logits)
                rec["err"].append(float(e.float().mean()))
                rec["pos"].append(float((u > q).float().mean()))
                rec["pfa"].append(float(((u > q) & ~e).float().mean()))
                rec["pfn"].append(float(((u <= q) & e).float().mean()))
                rec["q_hat"].append(q)
                rec["conf"].append(float((1 - u).mean()))
                rec["top_share"].append(torch.bincount(logits.argmax(1), minlength=100).max().item() / len(y))
                rec["disagree"].append(float((logits.argmax(1) != src.argmax(1)).float().mean()))
                rec["src_conf"].append(float(src.softmax(1).max(1).values.mean()))
            out.write(json.dumps(dict(key=key, arm=arm, corruption=c, severity=s, kind="dirichlet", alpha=0.1, rep=d, **rec)) + "\n")
            out.flush()
            print(name, n + 1, len(plan), key, f"err={np.mean(rec['err']):.3f}", f"elapsed={time.time() - t0:.0f}s", flush=True)
    print("complete", name, f"{time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main(sys.argv[1])

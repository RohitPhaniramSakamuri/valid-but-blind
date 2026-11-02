"""Experiment 004 mechanism run. Frozen before running.

Final IDs, weather and digital families, severities 3 and 5, Dirichlet 0.1, two new draws shared by all arms.
Arms: source; bn (batch statistics, no gradient); tent1e-4; tent1e-3. Each adapted arm is scored with both thresholds from the
same logits: recalibrated each batch as in the monitor, and fixed at the source threshold. Recalibrating a frozen model returns
the same threshold, so source has only one form. Calibration forward passes use autocast for speed; Tent's own passes do not.
"""
import json
import os
import sys
import time

import numpy as np
import torch

import run as R
import run_monitor as M
from run_confirm import CORRUPTIONS, stream
from run_replicate import loader

ARMS = (("source", 0.0), ("bn", 0.0), ("tent1e-4", 1e-4), ("tent1e-3", 1e-3))
DRAWS = 2


@torch.inference_mode()
def threshold(model, cx, cy, device):
    with torch.autocast("cuda", dtype=torch.float16):
        lg = torch.cat([model(cx[i:i + 1000]) for i in range(0, len(cx), 1000)]).float()
    return M.max_f1(lg.argmax(1) != cy, M.proxy_of(lg), device)


def main(name):
    out_dir, ckpt = f"results_{name}", f"models/{name}.pt"
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
    json.dump(dict(model=name, r0=float(err0.float().mean()), q_hat0=q0, false_alarm0=float(((prox0 > q0) & ~err0).float().mean()), n_calib=len(cy), torch=torch.__version__, gpu=torch.cuda.get_device_name(0)),
              open(f"{out_dir}/calibration.json", "w"), indent=1)
    model, params = M.make_tent(ckpt, device)
    init = [p.detach().clone() for p in params]
    plan = [(a, lr, c, s, d) for c in CORRUPTIONS for s in R.SEVERITIES for d in range(DRAWS) for a, lr in ARMS]
    path = f"{out_dir}/streams.jsonl"
    done = {json.loads(l)["key"] for l in open(path)} if os.path.exists(path) else set()
    t0 = time.time()
    with open(path, "a") as out:
        for n, (arm, lr, c, s, d) in enumerate(plan):
            key = f"{arm}/{c}/{s}/dirichlet/0.1/{d}"
            if key in done:
                continue
            rng = np.random.RandomState(R.seed_of("exp004-factorial", c, s, d))
            batches = torch.from_numpy(np.stack(stream("dirichlet", 0.1, stream_ids, labels, rng))).to(device)
            if arm != "source":
                with torch.no_grad():
                    for p, v in zip(params, init):
                        p.copy_(v)
            opt = torch.optim.Adam(params, lr=lr, betas=(0.9, 0.999), weight_decay=0.0) if lr else None
            xs = images[(c, s)][batches].permute(0, 1, 4, 2, 3).float().div_(255)
            ys = y_all[batches]
            rows = []
            for x, y in zip(xs, ys):
                if opt:
                    logits = model(x)
                    loss = -(logits.softmax(1) * logits.log_softmax(1)).sum(1).mean()
                    opt.zero_grad(set_to_none=True)
                    loss.backward()
                    opt.step()
                    logits = logits.detach()
                else:
                    with torch.inference_mode():
                        logits = (source if arm == "source" else model)(x)
                qr = threshold(model, cx, cy, device) if arm != "source" else q0
                u, e = M.proxy_of(logits), logits.argmax(1) != y
                flags = u.unsqueeze(0) > torch.tensor([qr, q0], device=device).view(2, 1)
                rows.append(torch.stack((e.float().mean(), flags[0].float().mean(), flags[1].float().mean(), (~flags[0] & e).float().mean(), (~flags[1] & e).float().mean(),
                                         1 - u.mean(), torch.tensor(qr, device=device))))
            v = torch.stack(rows).T.tolist()
            out.write(json.dumps(dict(key=key, arm=arm, corruption=c, severity=s, rep=d, err=v[0], pos_recal=v[1], pos_fixed=v[2], pfn_recal=v[3], pfn_fixed=v[4], conf=v[5], q_hat=v[6])) + "\n")
            out.flush()
            print(name, n + 1, len(plan), key, f"err={np.mean(v[0]):.3f}", f"elapsed={time.time() - t0:.0f}s", flush=True)
    print("complete", name, f"{time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main(sys.argv[1])

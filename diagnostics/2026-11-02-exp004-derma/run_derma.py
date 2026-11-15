"""DermaMNIST-224 blind-spot and twin test. Frozen before any stream ran. One process per arm.
Dev (official val images): noise, speckle, brightness; only a sanity check, source and Tent 1e-3; nothing is selected on it.
Held (official test images): blur, JPEG, contrast, pixelate at two severities, plus clean; priors natural, Dirichlet 1.0 and 0.1; three draws. Stream: 120 batches of 48.
Arms: source, bn, tent1e-3, tent5e-3, sar. Monitors from the same logits: released (threshold recalibrated every 5 batches, a disclosed speed choice), prototype distance
(our port of Schirmer et al. section 5.4 with L2-normalized features and class weights, same recalibration), and the twin rule fixed from the CIFAR test: twin uncertain or models disagree.
Labels build streams and score results offline only.
"""
import copy
import json
import math
import os
import sys
import time
import zlib

import numpy as np
import torch
import torch.nn as nn
import torchvision as tv

MEAN, STD = torch.tensor([0.485, 0.456, 0.406]).view(1, 3, 1, 1).cuda(), torch.tensor([0.229, 0.224, 0.225]).view(1, 3, 1, 1).cuda()
BATCH, TOTAL, RECAL = 48, 120, 5
GRID = torch.arange(0.001, 0.99, 0.001).cuda()
QS = torch.linspace(0.005, 0.995, 199).cuda()
PRIORS = (("natural", None), ("dir1", 1.0), ("dir01", 0.1))
DEV = dict(gaussian_noise=2, speckle_noise=2, brightness=2)
HELD = dict(gaussian_blur=2, jpeg_compression=2, contrast=2, pixelate=2)
ARMS = dict(source=None, bn=None, **{"tent1e-3": 1e-3, "tent5e-3": 5e-3}, sar=None)
LR_SAR, MOM, RHO, RESET, MARGIN = 0.00025, 0.9, 0.05, 0.2, 0.4 * math.log(7)


def seed_of(*p):
    return zlib.crc32("|".join(map(str, p)).encode()) % 2**31


def build():
    m = tv.models.resnet18(weights=None)
    m.fc = nn.Linear(512, 7)
    m.load_state_dict(torch.load("data/source.pt", weights_only=True))
    return m.cuda().eval()


def adaptive():
    m = build().requires_grad_(False)
    params = []
    for b in m.modules():
        if isinstance(b, nn.BatchNorm2d):
            b.requires_grad_(True)
            b.track_running_stats = False
            b.running_mean = None
            b.running_var = None
            params += [b.weight, b.bias]
    return m, params


def forward(m, x):
    x = (x - MEAN) / STD
    x = m.maxpool(m.relu(m.bn1(m.conv1(x))))
    x = m.avgpool(m.layer4(m.layer3(m.layer2(m.layer1(x))))).flatten(1)
    return m.fc(x), x


def conf_u(l):
    return 1 - l.softmax(1).max(1).values


def proto_u(f, m):
    return torch.cdist(nn.functional.normalize(f, dim=1), nn.functional.normalize(m.fc.weight, dim=1)).pow(2).min(1).values


def max_f1(err, u, grid):
    pos = u.view(1, -1) > grid.view(-1, 1)
    e = err.view(1, -1)
    tp, fp, fn = (pos & e).sum(1).float(), (pos & ~e).sum(1).float(), (~pos & e).sum(1).float()
    return grid[(2 * tp / (2 * tp + fp + fn).clamp_min(1)).argmax()].item()


def thresholds(m, cx, cy):
    with torch.inference_mode(), torch.autocast("cuda", dtype=torch.float16):
        l, f = forward(m, cx)
    l, f = l.float(), f.float()
    e = l.argmax(1) != cy
    uc, up = conf_u(l), proto_u(f, m)
    return max_f1(e, uc, GRID), max_f1(e, up, torch.quantile(up, QS)), e, uc, up


def entropy(l):
    return -(l.softmax(1) * l.log_softmax(1)).sum(1)


def sar_step(m, params, opt, x, st):
    l, f = forward(m, x)
    e1 = entropy(l)
    k1 = e1 < MARGIN
    resets = 0
    if k1.any():
        opt.zero_grad(set_to_none=True)
        e1[k1].mean().backward()
        grads = [p.grad for p in params if p.grad is not None]
        scale = RHO / (torch.norm(torch.stack([g.norm(2) for g in grads]), 2) + 1e-12)
        saved = [p.detach().clone() for p in params]
        with torch.no_grad():
            for p in params:
                if p.grad is not None:
                    p.add_(p.grad * scale)
        opt.zero_grad(set_to_none=True)
        e2 = entropy(forward(m, x)[0])[k1]
        k2 = e2 < MARGIN
        if k2.any():
            l2 = e2[k2].mean()
            l2.backward()
            st["ema"] = float(l2.detach()) if st["ema"] is None else 0.9 * st["ema"] + 0.1 * float(l2.detach())
        with torch.no_grad():
            for p, v in zip(params, saved):
                p.copy_(v)
        if k2.any():
            opt.step()
        opt.zero_grad(set_to_none=True)
    if st["ema"] is not None and st["ema"] < RESET:
        with torch.no_grad():
            for p, v in zip(params, st["init"]):
                p.copy_(v)
        opt.load_state_dict(copy.deepcopy(st["opt0"]))
        st["ema"] = None
        resets = 1
    return l.detach(), f.detach(), float(k1.float().mean()), resets


def stream(prior, ids, labels, rng):
    if prior is None:
        return [rng.choice(ids, BATCH, replace=True) for _ in range(TOTAL)]
    p = rng.dirichlet(np.full(7, prior))
    counts = np.bincount(labels[ids], minlength=7)
    with np.errstate(divide="ignore", invalid="ignore"):
        w = p[labels[ids]] / counts[labels[ids]]
    w /= w.sum()
    return [rng.choice(ids, BATCH, replace=True, p=w) for _ in range(TOTAL)]


def plan(arm):
    out = []
    if arm in ("source", "tent1e-3"):
        for c, n in DEV.items():
            for s in range(1, n + 1):
                for pn, a in PRIORS:
                    out.append(("dev", c, s, pn, a, 0))
        for pn, a in PRIORS:
            out.append(("dev", "clean", 0, pn, a, 0))
    for c, n in HELD.items():
        for s in range(1, n + 1):
            for pn, a in PRIORS:
                for d in range(3):
                    out.append(("held", c, s, pn, a, d))
    for pn, a in PRIORS:
        for d in range(3):
            out.append(("held", "clean", 0, pn, a, d))
    return out


def main(arm):
    os.makedirs("results", exist_ok=True)
    torch.backends.cudnn.benchmark = True
    torch.set_num_threads(2)
    Z = np.load("data/derma.npz")
    sp = np.load("data/splits.npz")
    cx = torch.from_numpy(Z["train_images"][sp["calib"]]).permute(0, 3, 1, 2).float().div_(255).cuda()
    cy = torch.from_numpy(Z["train_labels"].ravel().astype(np.int64)[sp["calib"]]).cuda()
    base = dict(dev=Z["val_images"], held=Z["test_images"])
    ylab = dict(dev=Z["val_labels"].ravel().astype(np.int64), held=Z["test_labels"].ravel().astype(np.int64))
    src = build().requires_grad_(False)
    q0c, q0p, e0, uc0, up0 = thresholds(src, cx, cy)
    twin, _ = adaptive()
    twin.requires_grad_(False)
    qt, _, et, ut0, _ = thresholds(twin, cx, cy)
    ft = ut0 > qt
    pc0, pp0 = uc0 > q0c, up0 > q0p
    w0 = dict(arm=arm, r0=float(e0.float().mean()), q0=q0c, qp0=q0p, qt=qt, fp0=float((pc0 & ~e0).float().mean()), fpp0=float((pp0 & ~e0).float().mean()), r_twin=float(et.float().mean()), fpt=float((ft & ~et).float().mean()), fnt=float((~ft & et).float().mean()), n=len(cy), gpu=torch.cuda.get_device_name(0), torch=torch.__version__)
    json.dump(w0, open(f"results/calibration_{arm}.json", "w"), indent=1)
    if arm == "source":
        model, params = src, []
    else:
        model, params = adaptive()
    init = [p.detach().clone() for p in params]
    path = f"results/{arm}.jsonl"
    done = {json.loads(l)["key"] for l in open(path)} if os.path.exists(path) else set()
    P, t0 = plan(arm), time.time()
    cache = {}
    with open(path, "a") as out:
        for n, (split, c, s, pn, a, d) in enumerate(P):
            key = f"{split}/{c}/{s}/{pn}/{d}"
            if key in done:
                continue
            if (split, c, s) not in cache:
                if len(cache) > 3:
                    cache.clear()
                cache[(split, c, s)] = base[split] if c == "clean" else np.load(f"data/{split}_{c}_{s}.npy")
            imgs = cache[(split, c, s)]
            labels = ylab[split]
            rng = np.random.RandomState(seed_of("exp004-derma", split, c, s, pn, d))
            order = stream(a, np.arange(len(labels)), labels, rng)
            with torch.no_grad():
                for p, v in zip(params, init):
                    p.copy_(v)
            lr = ARMS[arm]
            opt = None
            if lr:
                opt = torch.optim.Adam(params, lr=lr, betas=(0.9, 0.999), weight_decay=0.0)
            elif arm == "sar":
                opt = torch.optim.SGD(params, lr=LR_SAR, momentum=MOM)
                st = dict(ema=None, init=init, opt0=copy.deepcopy(opt.state_dict()))
            rows, kept, resets = [], [], 0
            qc, qp = q0c, q0p
            for t, ids in enumerate(order):
                x = torch.from_numpy(imgs[ids]).cuda().permute(0, 3, 1, 2).float().div_(255)
                y = torch.from_numpy(labels[ids]).cuda()
                if arm == "sar":
                    l, f, k, r = sar_step(model, params, opt, x, st)
                    kept.append(k)
                    resets += r
                elif opt:
                    l, f = forward(model, x)
                    opt.zero_grad(set_to_none=True)
                    entropy(l).mean().backward()
                    opt.step()
                    l, f = l.detach(), f.detach()
                else:
                    with torch.inference_mode():
                        l, f = forward(model, x)
                with torch.inference_mode():
                    lw, _ = forward(twin, x)
                if arm != "source" and t % RECAL == 0:
                    qc, qp, *_ = thresholds(model, cx, cy)
                uc, up = conf_u(l), proto_u(f, model)
                E, A, F = l.argmax(1) != y, l.argmax(1) == lw.argmax(1), conf_u(lw) > qt
                cells = torch.bincount(E.long() * 4 + F.long() * 2 + A.long(), minlength=8).float() / len(y)
                Fr, Fp = uc > qc, up > qp
                rows.append(torch.cat((cells, torch.stack((Fr.float().mean(), (E & Fr).float().mean(), Fp.float().mean(), (E & Fp).float().mean(), (lw.argmax(1) != y).float().mean(), 1 - uc.mean(), 1 - conf_u(lw).mean())))))
            v = torch.stack(rows).T.tolist()
            out.write(json.dumps(dict(key=key, arm=arm, split=split, corruption=c, severity=s, prior=pn, rep=d, cells=v[:8], pos=v[8], hit=v[9], pos_p=v[10], hit_p=v[11], twin_err=v[12], conf=v[13], conf_twin=v[14], kept=float(np.mean(kept)) if kept else None, resets=resets)) + "\n")
            out.flush()
            print(arm, n + 1, len(P), key, f"err={np.sum(v[4:8], axis=0).mean():.3f}", f"twin={np.mean(v[12]):.3f}", f"elapsed={time.time() - t0:.0f}s", flush=True)
    print("complete", arm, f"{time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main(sys.argv[1])

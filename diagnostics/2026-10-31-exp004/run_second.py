"""Experiment 004, second model. Frozen before running: same streams, monitor and pass rule as
run_confirm.py and analyze_confirm.py, with Modas2021PRIMEResNet18 instead of the AugMix ResNeXt.
Arms: source and tent. The final IDs were used once before, for the first model; this is disclosed.
"""
import json
import os
import time

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

import run as R
from run_confirm import CORRUPTIONS, stream
from run_monitor import BATCH, load_clean, make_tent, max_f1, outputs, proxy_of, to_tensor

OUT = "results_second"
CKPT = "models/Modas2021PRIMEResNet18.pt"


class Block(nn.Module):
    def __init__(self, inp, planes, stride=1):
        super().__init__()
        self.conv1 = nn.Conv2d(inp, planes, 3, stride, 1, bias=False)
        self.bn1 = nn.BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(planes, planes, 3, 1, 1, bias=False)
        self.bn2 = nn.BatchNorm2d(planes)
        self.shortcut = nn.Sequential()
        if stride != 1 or inp != planes:
            self.shortcut = nn.Sequential(nn.Conv2d(inp, planes, 1, stride, bias=False), nn.BatchNorm2d(planes))

    def forward(self, x):
        y = self.bn2(self.conv2(F.relu(self.bn1(self.conv1(x)))))
        return F.relu(y + self.shortcut(x))


class ResNet18(nn.Module):
    def __init__(self):
        super().__init__()
        self.inp = 64
        self.conv1 = nn.Conv2d(3, 64, 3, 1, 1, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.layer1 = self._layer(64, 1)
        self.layer2 = self._layer(128, 2)
        self.layer3 = self._layer(256, 2)
        self.layer4 = self._layer(512, 2)
        self.linear = nn.Linear(512, 100)
        self.register_buffer("mu", torch.zeros(1, 3, 1, 1))
        self.register_buffer("sigma", torch.ones(1, 3, 1, 1))

    def _layer(self, planes, stride):
        layers = [Block(self.inp, planes, stride), Block(planes, planes)]
        self.inp = planes
        return nn.Sequential(*layers)

    def forward(self, x):
        x = (x - self.mu) / self.sigma
        x = F.relu(self.bn1(self.conv1(x)))
        x = self.layer4(self.layer3(self.layer2(self.layer1(x))))
        return self.linear(F.avg_pool2d(x, 4).flatten(1))


def load(path, device, smoke=False):
    model = ResNet18()
    model.load_state_dict(torch.load(path, map_location="cpu", weights_only=True), strict=True)
    return model.to(device).eval()


def main():
    R.load_model = load
    device = "cuda"
    torch.backends.cudnn.benchmark = True
    os.makedirs(OUT, exist_ok=True)
    labels_all = np.load("data/CIFAR-100-C/labels.npy")[:10000].astype(np.int64)
    clean_x, clean_y = load_clean("data/cifar-100-python")
    if not (clean_y == labels_all).all():
        raise SystemExit("Clean labels do not match CIFAR-100-C labels")
    perm = np.random.RandomState(R.SPLIT_SEED).permutation(10000)
    calib_ids, stream_ids = perm[:1000], perm[5000:9000]
    images = {("clean", 0): torch.from_numpy(clean_x).to(device)}
    for c in CORRUPTIONS:
        arr = np.load(f"data/CIFAR-100-C/{c}.npy", mmap_mode="r")
        for s in R.SEVERITIES:
            images[(c, s)] = torch.from_numpy(np.array(arr[(s - 1) * 10000:s * 10000])).to(device)
    y_all = torch.from_numpy(labels_all).to(device)

    source = load(CKPT, device)
    for p in source.parameters():
        p.requires_grad_(False)
    cx, cy = to_tensor(clean_x[calib_ids], device), y_all[torch.from_numpy(calib_ids).to(device)]
    lg = outputs(source, cx)
    err0, prox0 = lg.argmax(1) != cy, proxy_of(lg)
    q0 = max_f1(err0, prox0, device)
    meta = dict(model="Modas2021PRIMEResNet18", r0=float(err0.float().mean()), q_hat0=q0, false_alarm0=float(((prox0 > q0) & ~err0).float().mean()),
                n_calib=len(cy), torch=torch.__version__, gpu=torch.cuda.get_device_name(0))
    json.dump(meta, open(f"{OUT}/calibration.json", "w"), indent=1)
    print(meta, flush=True)

    model, params = make_tent(CKPT, device)
    init = [p.detach().clone() for p in params]
    base = [("balanced_wr", 0, 0), ("by_class", 0, 0), ("dirichlet", 0.1, 0), ("dirichlet", 0.1, 1)]
    plan = [(arm, c, s, k, a, r) for c in CORRUPTIONS for s in R.SEVERITIES for k, a, r in base for arm in ("source", "tent")]
    plan += [(arm, "clean", 0, k, a, rep) for rep in range(3) for k, a, _ in base[:3] for arm in ("source", "tent")]

    path = f"{OUT}/streams.jsonl"
    done = {json.loads(l)["key"] for l in open(path)} if os.path.exists(path) else set()
    t0 = time.time()
    with open(path, "a") as out:
        for n, (arm, c, s, kind, alpha, rep) in enumerate(plan):
            key = f"{arm}/{c}/{s}/{kind}/{alpha}/{rep}"
            if key in done:
                continue
            rng = np.random.RandomState(R.seed_of("exp004-confirm", c, s, kind, alpha, rep))
            if arm == "tent":
                with torch.no_grad():
                    for p, v in zip(params, init):
                        p.copy_(v)
                opt = torch.optim.Adam(params, lr=1e-3, betas=(0.9, 0.999), weight_decay=0.0)
            rec = {k: [] for k in ("err", "pos", "pfa", "pfn", "q_hat", "conf", "top_share", "disagree", "src_conf")}
            data = images[(c, s)]
            for b in stream(kind, alpha, stream_ids, labels_all, rng):
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
                    l = outputs(model, cx)
                    q = max_f1(l.argmax(1) != cy, proxy_of(l), device)
                with torch.no_grad():
                    src = source(x) if arm != "source" else logits
                e, u = logits.argmax(1) != y, proxy_of(logits)
                rec["err"].append(float(e.float().mean()))
                rec["pos"].append(float((u > q).float().mean()))
                rec["pfa"].append(float(((u > q) & ~e).float().mean()))
                rec["pfn"].append(float(((u <= q) & e).float().mean()))
                rec["q_hat"].append(q)
                rec["conf"].append(float((1 - u).mean()))
                rec["top_share"].append(torch.bincount(logits.argmax(1), minlength=100).max().item() / len(y))
                rec["disagree"].append(float((logits.argmax(1) != src.argmax(1)).float().mean()))
                rec["src_conf"].append(float(src.softmax(1).max(1).values.mean()))
            out.write(json.dumps(dict(key=key, arm=arm, corruption=c, severity=s, kind=kind, alpha=alpha, rep=rep, **rec)) + "\n")
            out.flush()
            print(n + 1, len(plan), key, f"err={np.mean(rec['err']):.3f}", f"elapsed={time.time() - t0:.0f}s", flush=True)
    print("complete", f"{time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()

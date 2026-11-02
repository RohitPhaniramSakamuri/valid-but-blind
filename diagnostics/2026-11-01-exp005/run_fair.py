"""Experiment 005: group accuracy under online adaptation on CelebA. Protocol in
experiments/005-group-gaps-under-online-adaptation.md. Stages: prepare, train, streams."""
import argparse
import glob
import io
import json
import math
import multiprocessing as mp
import os
import time
import zlib

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image

SIZE, BATCH, STEPS, REPS = 96, 64, 150, 2
TARGETS = ("Blond_Hair", "Smiling")
SEEDS = (1, 2, 3)
ARMS = ("source", "bn", "tent", "eta", "blend")
MIXES = {"m10": 0.1, "natural": None, "m50": 0.5, "m90": 0.9}
POOLS = {"valid": ("clean", "gaussian_noise", "gaussian_blur"), "test": ("clean", "contrast", "brightness", "pixelate", "haze")}
EXPECTED = {"train": 162770, "valid": 19867, "test": 19962}
MEAN = torch.tensor([0.485, 0.456, 0.406]).view(1, 3, 1, 1)
STD = torch.tensor([0.229, 0.224, 0.225]).view(1, 3, 1, 1)


def decode(b):
    im = Image.open(io.BytesIO(b)).convert("RGB")
    w, h = im.size
    s = min(w, h)
    im = im.crop(((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s)).resize((SIZE, SIZE), Image.BILINEAR)
    return np.asarray(im, dtype=np.uint8)


def prepare(root, data):
    import pyarrow.parquet as pq
    os.makedirs(data, exist_ok=True)
    names = {"train": "train", "valid": "valid", "test": "test"}
    seen = {}
    with mp.Pool(16) as pool:
        for split, prefix in names.items():
            files = sorted(glob.glob(f"{root}/**/{prefix}*-*.parquet", recursive=True))
            if not files and split == "valid":
                files = sorted(glob.glob(f"{root}/**/validation*-*.parquet", recursive=True))
            imgs, attrs, ids = [], {k: [] for k in TARGETS + ("Male",)}, []
            for f in files:
                t = pq.read_table(f, columns=["image", "celeb_id", *attrs.keys()])
                bytes_ = [x["bytes"] for x in t.column("image").to_pylist()]
                imgs.append(np.stack(pool.map(decode, bytes_, chunksize=256)))
                ids += t.column("celeb_id").to_pylist()
                for k in attrs:
                    attrs[k] += t.column(k).to_pylist()
            x = np.concatenate(imgs)
            if len(x) != EXPECTED[split]:
                raise SystemExit(f"{split}: {len(x)} images, expected {EXPECTED[split]}")
            np.save(f"{data}/{split}_x.npy", x)
            np.savez(f"{data}/{split}_y.npz", celeb_id=np.array(ids), **{k: np.array(v, dtype=np.int64) for k, v in attrs.items()})
            seen[split] = set(ids)
            print(split, x.shape, {k: float(np.mean(v)) for k, v in attrs.items()}, flush=True)
    if seen["train"] & seen["test"] or seen["train"] & seen["valid"] or seen["valid"] & seen["test"]:
        raise SystemExit("Identity overlap across splits")
    print("identity-disjoint ok", flush=True)


def net():
    from torchvision.models import ResNet18_Weights, resnet18
    m = resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)
    m.fc = nn.Linear(512, 2)
    return m


def norm(x):
    return (x - MEAN.to(x.device)) / STD.to(x.device)


def train(data, out):
    device = "cuda"
    os.makedirs(out, exist_ok=True)
    x = torch.from_numpy(np.load(f"{data}/train_x.npy")).to(device)
    ys = np.load(f"{data}/train_y.npz")
    vx = torch.from_numpy(np.load(f"{data}/valid_x.npy")).to(device)
    vs = np.load(f"{data}/valid_y.npz")
    for target in TARGETS:
        y = torch.from_numpy(ys[target]).to(device)
        for seed in SEEDS:
            path = f"{out}/{target}_{seed}.pt"
            if os.path.exists(path):
                continue
            torch.manual_seed(seed)
            model = net().to(device)
            opt = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9, weight_decay=1e-4)
            t0 = time.time()
            for _ in range(5):
                model.train()
                perm = torch.randperm(len(x), device=device)
                for i in range(0, len(x) - 255, 256):
                    idx = perm[i:i + 256]
                    b = x[idx].permute(0, 3, 1, 2).float().div_(255)
                    flip = torch.rand(len(b), device=device) < 0.5
                    b[flip] = b[flip].flip(3)
                    loss = F.cross_entropy(model(norm(b)), y[idx])
                    opt.zero_grad()
                    loss.backward()
                    opt.step()
            model.eval()
            with torch.no_grad():
                pred = torch.cat([model(norm(vx[i:i + 512].permute(0, 3, 1, 2).float().div_(255))).argmax(1) for i in range(0, len(vx), 512)]).cpu().numpy()
            print(target, seed, f"valid_acc={np.mean(pred == vs[target]):.4f}", f"{time.time() - t0:.0f}s", flush=True)
            torch.save(model.state_dict(), path)


def disk_kernel(r, device):
    g = torch.arange(-r, r + 1, device=device).float()
    k = ((g.view(-1, 1) ** 2 + g.view(1, -1) ** 2) <= r * r).float()
    return k / k.sum()


def gauss_kernel(sigma, device):
    r = int(3 * sigma)
    g = torch.arange(-r, r + 1, device=device).float()
    k = torch.exp(-(g ** 2) / (2 * sigma ** 2))
    k = k.view(-1, 1) * k.view(1, -1)
    return k / k.sum()


def corrupt(x, name, gen):
    """x in [0, 1]. One fixed strength each; inspired by ImageNet-C, not the official benchmark."""
    if name == "clean":
        return x
    if name == "gaussian_noise":
        return (x + 0.15 * torch.randn(x.shape, device=x.device, generator=gen)).clamp(0, 1)
    if name == "gaussian_blur":
        k = gauss_kernel(2.0, x.device)[None, None].repeat(3, 1, 1, 1)
        return F.conv2d(F.pad(x, [k.shape[-1] // 2] * 4, mode="reflect"), k, groups=3)
    if name == "contrast":
        return ((x - x.mean((1, 2, 3), keepdim=True)) * 0.35 + x.mean((1, 2, 3), keepdim=True)).clamp(0, 1)
    if name == "brightness":
        return (x + 0.35).clamp(0, 1)
    if name == "pixelate":
        return F.interpolate(F.interpolate(x, size=24, mode="area"), size=SIZE, mode="nearest")
    if name == "haze":
        low = F.interpolate(torch.rand(len(x), 1, 6, 6, device=x.device, generator=gen), size=SIZE, mode="bicubic", align_corners=False).clamp(0, 1)
        a = 0.45 + 0.3 * low
        return (x * (1 - a) + a * 0.9).clamp(0, 1)
    raise ValueError(name)


class BlendBN(nn.Module):
    def __init__(self, bn, a=0.5):
        super().__init__()
        self.bn, self.a = bn, a

    def forward(self, x):
        m = x.mean((0, 2, 3))
        v = x.var((0, 2, 3), unbiased=False)
        mean = self.a * m + (1 - self.a) * self.bn.running_mean
        var = self.a * v + (1 - self.a) * self.bn.running_var
        z = (x - mean[None, :, None, None]) / (var[None, :, None, None] + 1e-5).sqrt()
        return z * self.bn.weight[None, :, None, None] + self.bn.bias[None, :, None, None]


def swap_blend(mod):
    for name, child in mod.named_children():
        if isinstance(child, nn.BatchNorm2d):
            setattr(mod, name, BlendBN(child))
        else:
            swap_blend(child)


def build(arm, state, device):
    m = net()
    m.load_state_dict(state)
    m = m.to(device).eval()
    m.requires_grad_(False)
    params = []
    if arm == "blend":
        swap_blend(m)
    elif arm != "source":
        for b in m.modules():
            if isinstance(b, nn.BatchNorm2d):
                b.track_running_stats = False
                b.running_mean = None
                b.running_var = None
                if arm in ("tent", "eta"):
                    b.requires_grad_(True)
                    params += [b.weight, b.bias]
    return m, params


def streams(data, ckpts, out):
    device = "cuda"
    torch.backends.cudnn.benchmark = True
    os.makedirs(out, exist_ok=True)
    path = f"{out}/streams.jsonl"
    done = {json.loads(l)["key"] for l in open(path)} if os.path.exists(path) else set()
    margin = 0.4 * math.log(2)
    t0 = time.time()
    with open(path, "a") as f:
        for pool, corruptions in POOLS.items():
            x = torch.from_numpy(np.load(f"{data}/{pool}_x.npy")).to(device)
            ys = np.load(f"{data}/{pool}_y.npz")
            male = ys["Male"]
            idx = {0: np.where(male == 0)[0], 1: np.where(male == 1)[0]}
            for target in TARGETS:
                y_np = ys[target]
                y = torch.from_numpy(y_np).to(device)
                for seed in SEEDS:
                    state = torch.load(f"{ckpts}/{target}_{seed}.pt", map_location="cpu", weights_only=True)
                    models = {a: build(a, state, device) for a in ARMS}
                    inits = {a: [p.detach().clone() for p in models[a][1]] for a in ARMS}
                    for c in corruptions:
                        for mix, share in MIXES.items():
                            for rep in range(REPS):
                                base = zlib.crc32(f"{pool}|{target}|{c}|{mix}|{rep}".encode()) % 2**31
                                rng = np.random.RandomState(base)
                                plan = []
                                for _ in range(STEPS):
                                    if share is None:
                                        plan.append(rng.randint(0, len(x), BATCH))
                                    else:
                                        n_m = rng.binomial(BATCH, share)
                                        b = np.concatenate([rng.choice(idx[1], n_m), rng.choice(idx[0], BATCH - n_m)])
                                        rng.shuffle(b)
                                        plan.append(b)
                                for arm in ARMS:
                                    key = f"{pool}/{target}/{seed}/{c}/{mix}/{rep}/{arm}"
                                    if key in done:
                                        continue
                                    model, params = models[arm]
                                    opt = None
                                    if params:
                                        with torch.no_grad():
                                            for p, v in zip(params, inits[arm]):
                                                p.copy_(v)
                                        opt = torch.optim.Adam(params, lr=1e-3, betas=(0.9, 0.999))
                                    gen = torch.Generator(device=device).manual_seed(base)
                                    # counts[class][group] and correct[class][group]
                                    n, k = np.zeros((2, 2)), np.zeros((2, 2))
                                    conf = 0.0
                                    for b in plan:
                                        bt = torch.from_numpy(b).to(device)
                                        im = norm(corrupt(x[bt].permute(0, 3, 1, 2).float().div_(255), c, gen))
                                        if opt:
                                            lg = model(im)
                                            ent = -(lg.softmax(1) * lg.log_softmax(1)).sum(1)
                                            if arm == "tent":
                                                loss = ent.mean()
                                            else:
                                                keep = ent < margin
                                                loss = (ent[keep] / torch.exp(ent[keep].detach() - margin)).mean() if keep.any() else None
                                            if loss is not None:
                                                opt.zero_grad()
                                                loss.backward()
                                                opt.step()
                                            lg = lg.detach()
                                        else:
                                            with torch.no_grad():
                                                lg = model(im)
                                        ok = (lg.argmax(1) == y[bt]).cpu().numpy()
                                        np.add.at(n, (y_np[b], male[b]), 1)
                                        np.add.at(k, (y_np[b], male[b]), ok)
                                        conf += float(lg.softmax(1).max(1).values.mean())
                                    f.write(json.dumps(dict(key=key, pool=pool, target=target, seed=seed, corruption=c, mix=mix, rep=rep, arm=arm, n=n.tolist(), k=k.tolist(), conf=conf / STEPS)) + "\n")
                                f.flush()
                    print(pool, target, seed, f"elapsed={time.time() - t0:.0f}s", flush=True)
    print("complete", f"{time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["prepare", "train", "streams"])
    ap.add_argument("--raw", default="raw")
    ap.add_argument("--data", default="data")
    ap.add_argument("--ckpts", default="ckpts")
    ap.add_argument("--out", default="results")
    a = ap.parse_args()
    if a.stage == "prepare":
        prepare(a.raw, a.data)
    elif a.stage == "train":
        train(a.data, a.ckpts)
    else:
        streams(a.data, a.ckpts, a.out)

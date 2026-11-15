"""Downloads DermaMNIST-224, checks for near-duplicates across splits, trains one ResNet-18, and writes the corrupted image sets. Frozen before any stream ran."""
import io
import json
import os
import urllib.request

import numpy as np
import torch
import torch.nn as nn
import torchvision as tv
from PIL import Image, ImageFilter
from multiprocessing import Pool

SEED = 20261102
URL = "https://zenodo.org/api/records/10519652/files/dermamnist_224.npz/content"
MEAN, STD = torch.tensor([0.485, 0.456, 0.406]).view(1, 3, 1, 1), torch.tensor([0.229, 0.224, 0.225]).view(1, 3, 1, 1)
SETS = dict(dev=dict(gaussian_noise=(0.08, 0.16), speckle_noise=(0.15, 0.30), brightness=(0.2, 0.4)), held=dict(gaussian_blur=(2, 4), jpeg_compression=(15, 6), contrast=(0.35, 0.15), pixelate=(56, 28)))


def corrupt(a):
    img, name, v, seed = a
    rng = np.random.default_rng(seed)
    x = img.astype(np.float32) / 255
    if name == "gaussian_noise":
        x = x + rng.normal(0, v, x.shape)
    elif name == "speckle_noise":
        x = x * (1 + rng.normal(0, v, x.shape))
    elif name == "brightness":
        x = x + v
    elif name == "contrast":
        x = (x - x.mean((0, 1), keepdims=True)) * v + x.mean((0, 1), keepdims=True)
    else:
        p = Image.fromarray(img)
        if name == "gaussian_blur":
            return np.asarray(p.filter(ImageFilter.GaussianBlur(v)))
        if name == "pixelate":
            return np.asarray(p.resize((v, v), Image.BOX).resize((224, 224), Image.NEAREST))
        if name == "jpeg_compression":
            b = io.BytesIO()
            p.save(b, "JPEG", quality=v)
            return np.asarray(Image.open(io.BytesIO(b.getvalue())).convert("RGB"))
    return (np.clip(x, 0, 1) * 255).astype(np.uint8)


def signature(x):
    t = torch.from_numpy(x).permute(0, 3, 1, 2).float()
    s = torch.nn.functional.adaptive_avg_pool2d(t, 16).flatten(1)
    return s - s.mean(1, keepdim=True)


if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    if not os.path.exists("data/derma.npz"):
        urllib.request.urlretrieve(URL, "data/derma.npz")
    Z = np.load("data/derma.npz")
    print({k: Z[k].shape for k in Z.files}, flush=True)
    tr, va, te = Z["train_images"], Z["val_images"], Z["test_images"]
    ytr, yva, yte = Z["train_labels"].ravel().astype(np.int64), Z["val_labels"].ravel().astype(np.int64), Z["test_labels"].ravel().astype(np.int64)
    # Near-duplicate check. MedMNIST has no lesion IDs, so this cannot prove patient-level separation.
    sig = {k: signature(v).cuda() for k, v in dict(train=tr, val=va, test=te).items()}
    dup = {}
    for a, b in (("test", "train"), ("val", "train"), ("test", "val")):
        d = torch.cat([torch.cdist(sig[a][i:i + 256], sig[b]).min(1).values for i in range(0, len(sig[a]), 256)]) / np.sqrt(sig[a].shape[1])
        dup[f"{a}_vs_{b}"] = dict(rmse_below_3=float((d < 3).float().mean()), rmse_below_6=float((d < 6).float().mean()), median=float(d.median()))
    print("near-duplicates", dup, flush=True)
    rng = np.random.RandomState(SEED)
    perm = rng.permutation(len(tr))
    calib, select, fit = perm[:1000], perm[1000:1500], perm[1500:]
    np.savez("data/splits.npz", calib=calib, select=select, fit=fit)
    torch.manual_seed(SEED)
    m = tv.models.resnet18(weights="IMAGENET1K_V1")
    m.fc = nn.Linear(512, 7)
    m = m.cuda()
    opt = torch.optim.AdamW(m.parameters(), lr=3e-4, weight_decay=1e-4)
    scaler = torch.amp.GradScaler("cuda")
    xfit, yfit = torch.from_numpy(tr[fit]).permute(0, 3, 1, 2), torch.from_numpy(ytr[fit])
    xsel, ysel = torch.from_numpy(tr[select]).permute(0, 3, 1, 2), torch.from_numpy(ytr[select])

    def norm(x):
        return (x.float().cuda() / 255 - MEAN.cuda()) / STD.cuda()

    best, log = -1, []
    for ep in range(12):
        m.train()
        order = torch.randperm(len(xfit))
        for i in range(0, len(order) - 63, 64):
            b = order[i:i + 64]
            x = xfit[b]
            if ep % 1 == 0:
                flip = torch.rand(len(b)) < 0.5
                x[flip] = x[flip].flip(3)
            with torch.autocast("cuda"):
                loss = nn.functional.cross_entropy(m(norm(x)), yfit[b].cuda())
            opt.zero_grad(set_to_none=True)
            scaler.scale(loss).backward()
            scaler.step(opt)
            scaler.update()
        m.eval()
        with torch.inference_mode():
            pred = torch.cat([m(norm(xsel[i:i + 256])).argmax(1).cpu() for i in range(0, len(xsel), 256)])
        acc = float((pred == ysel).float().mean())
        log.append(acc)
        print("epoch", ep, "select accuracy", round(acc, 4), flush=True)
        if acc > best:
            best = acc
            torch.save(m.state_dict(), "data/source.pt")
    m.load_state_dict(torch.load("data/source.pt", weights_only=True))
    m.eval()
    with torch.inference_mode():
        xv = torch.from_numpy(va).permute(0, 3, 1, 2)
        pv = torch.cat([m(norm(xv[i:i + 256])).argmax(1).cpu() for i in range(0, len(xv), 256)])
    json.dump(dict(select_best=best, log=log, val_accuracy=float((pv.numpy() == yva).mean()), duplicates=dup, sizes=dict(fit=len(fit), select=len(select), calib=len(calib), dev=len(va), held=len(te)), class_counts_test=np.bincount(yte, minlength=7).tolist()), open("data/source_report.json", "w"), indent=1)
    print("source val accuracy", float((pv.numpy() == yva).mean()), flush=True)
    with Pool(min(32, os.cpu_count())) as pool:
        for split, imgs in (("dev", va), ("held", te)):
            for name, levels in SETS[split].items():
                for lv, v in enumerate(levels, 1):
                    out = pool.map(corrupt, [(im, name, v, SEED + i) for i, im in enumerate(imgs)], chunksize=32)
                    np.save(f"data/{split}_{name}_{lv}.npy", np.stack(out))
                    print("wrote", split, name, lv, flush=True)
    print("=== PREPARE DONE", flush=True)

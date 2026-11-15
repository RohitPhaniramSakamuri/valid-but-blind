"""Train one ResNet-18 and write corrupted sets. Usage: prepare.py <blood|derma> <n_classes>. Frozen with experiments/005."""
import io, json, os, sys
from multiprocessing import Pool
import numpy as np, torch, torch.nn as nn, torchvision as tv
from PIL import Image, ImageFilter
DS, K = sys.argv[1], int(sys.argv[2]); SEED = 20261103
MEAN, STD = torch.tensor([0.485, 0.456, 0.406]).view(1, 3, 1, 1), torch.tensor([0.229, 0.224, 0.225]).view(1, 3, 1, 1)
SETS = dict(dev=dict(gaussian_noise=(.04, .08, .16), speckle_noise=(.08, .15, .30), brightness=(.1, .2, .4), gamma=(1.4, 2., 3.), saturation=(.6, .3, .05)), held=dict(gaussian_blur=(1, 2, 4), jpeg_compression=(30, 15, 6), contrast=(.6, .35, .15), pixelate=(112, 56, 28)))
def corrupt(a):
    img, name, v, seed = a
    rng = np.random.default_rng(seed); x = img.astype(np.float32) / 255
    if name == "gaussian_noise": x = x + rng.normal(0, v, x.shape)
    elif name == "speckle_noise": x = x * (1 + rng.normal(0, v, x.shape))
    elif name == "brightness": x = x + v
    elif name == "gamma": x = x ** v
    elif name == "saturation": g = x.mean(2, keepdims=True); x = g + v * (x - g)
    elif name == "contrast": m = x.mean((0, 1), keepdims=True); x = (x - m) * v + m
    else:
        p = Image.fromarray(img)
        if name == "gaussian_blur": return np.asarray(p.filter(ImageFilter.GaussianBlur(v)))
        if name == "pixelate": return np.asarray(p.resize((v, v), Image.BOX).resize((224, 224), Image.NEAREST))
        b = io.BytesIO(); p.save(b, "JPEG", quality=v); return np.asarray(Image.open(io.BytesIO(b.getvalue())).convert("RGB"))
    return (np.clip(x, 0, 1) * 255).astype(np.uint8)
if __name__ == "__main__":
    os.chdir(DS)
    Z = np.load("data.npz"); tr, va, te = Z["train_images"], Z["val_images"], Z["test_images"]
    ytr, yva = Z["train_labels"].ravel().astype(np.int64), Z["val_labels"].ravel().astype(np.int64)
    np.save("val.npy", va); np.save("test.npy", te); np.save("val_y.npy", yva); np.save("test_y.npy", Z["test_labels"].ravel().astype(np.int64))
    perm = np.random.RandomState(SEED).permutation(len(tr)); calib, select, fit = perm[:1000], perm[1000:1500], perm[1500:]
    np.save("calib_x.npy", tr[calib]); np.save("calib_y.npy", ytr[calib])
    torch.manual_seed(SEED)
    m = tv.models.resnet18(weights="IMAGENET1K_V1"); m.fc = nn.Linear(512, K); m = m.cuda()
    opt = torch.optim.AdamW(m.parameters(), lr=3e-4, weight_decay=1e-4); sc = torch.amp.GradScaler("cuda")
    xf, yf = torch.from_numpy(tr[fit]).permute(0, 3, 1, 2), torch.from_numpy(ytr[fit]); xs, ys = torch.from_numpy(tr[select]).permute(0, 3, 1, 2), torch.from_numpy(ytr[select])
    norm = lambda x: (x.float().cuda() / 255 - MEAN.cuda()) / STD.cuda()
    best = -1
    for ep in range(8):
        m.train(); o = torch.randperm(len(xf))
        for i in range(0, len(o) - 63, 64):
            b = o[i:i + 64]; x = xf[b]; f = torch.rand(len(b)) < .5; x[f] = x[f].flip(3)
            with torch.autocast("cuda"): loss = nn.functional.cross_entropy(m(norm(x)), yf[b].cuda())
            opt.zero_grad(set_to_none=True); sc.scale(loss).backward(); sc.step(opt); sc.update()
        m.eval()
        with torch.inference_mode(): p = torch.cat([m(norm(xs[i:i + 256])).argmax(1).cpu() for i in range(0, len(xs), 256)])
        acc = float((p == ys).float().mean()); print("epoch", ep, acc, flush=True)
        if acc > best: best = acc; torch.save(m.state_dict(), "source.pt")
    m.load_state_dict(torch.load("source.pt", weights_only=True)); m.eval()
    xv = torch.from_numpy(va).permute(0, 3, 1, 2)
    with torch.inference_mode(): p = torch.cat([m(norm(xv[i:i + 256])).argmax(1).cpu() for i in range(0, len(xv), 256)])
    json.dump(dict(select=best, val_accuracy=float((p.numpy() == yva).mean()), classes=np.bincount(yva, minlength=K).tolist()), open("source_report.json", "w"))
    with Pool(min(16, os.cpu_count())) as pool:
        for split, imgs in (("dev", va), ("held", te)):
            for name, levels in SETS[split].items():
                for lv, v in enumerate(levels, 1):
                    np.save(f"{split}_{name}_{lv}.npy", np.stack(pool.map(corrupt, [(im, name, v, SEED + i) for i, im in enumerate(imgs)], chunksize=32)))
    print("=== PREPARE DONE", DS, flush=True)

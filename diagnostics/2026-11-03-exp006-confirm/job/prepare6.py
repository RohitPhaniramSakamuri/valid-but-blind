"""Train one ResNet-18 and write corrupted sets for a MedMNIST-224 dataset. Usage: prepare6.py <path|organa> <classes>. Frozen with experiments/006."""
import io, json, os, sys
from multiprocessing import Pool
import numpy as np, torch, torch.nn as nn, torchvision as tv
from PIL import Image, ImageFilter
DS, K = sys.argv[1], int(sys.argv[2]); SEED = 20261103; WORK = os.environ["WORK"]
MEAN, STD = torch.tensor([0.485, 0.456, 0.406]).view(1, 3, 1, 1).cuda(), torch.tensor([0.229, 0.224, 0.225]).view(1, 3, 1, 1).cuda()
DEV = dict(gaussian_noise=(.04, .08, .16), speckle_noise=(.08, .15, .30), brightness=(.1, .2, .4), gamma=(1.4, 2., 3.))
DEV.update(dict(saturation=(.6, .3, .05)) if DS == "path" else dict(shot_noise=(60, 25, 10)))
SETS = dict(dev=DEV, held=dict(gaussian_blur=(1, 2, 4), jpeg_compression=(30, 15, 6), contrast=(.6, .35, .15), pixelate=(112, 56, 28)))
def corrupt(a):
    img, name, v, seed = a
    rng = np.random.default_rng(seed); x = img.astype(np.float32) / 255
    if name == "gaussian_noise": x = x + rng.normal(0, v, x.shape)
    elif name == "speckle_noise": x = x * (1 + rng.normal(0, v, x.shape))
    elif name == "shot_noise": x = rng.poisson(x * v) / v
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
rgb = lambda a: np.repeat(a[..., None], 3, -1) if a.ndim == 3 else a
if __name__ == "__main__":
    os.chdir(f"{WORK}/{DS}"); Z = np.load("data.npz")
    ytr, yva, yte = (Z[k].ravel().astype(np.int64) for k in ("train_labels", "val_labels", "test_labels"))
    va, te = rgb(Z["val_images"]), rgb(Z["test_images"]); tr = Z["train_images"]
    np.save("val.npy", va); np.save("test.npy", te); np.save("val_y.npy", yva); np.save("test_y.npy", yte)
    perm = np.random.RandomState(SEED).permutation(len(tr)); calib, select, fit = perm[:1000], perm[1000:1500], perm[1500:31500]
    np.save("calib_x.npy", rgb(tr[calib])); np.save("calib_y.npy", ytr[calib])
    xf = torch.from_numpy(rgb(tr[np.sort(fit)])).cuda().permute(0, 3, 1, 2); yf = torch.from_numpy(ytr[np.sort(fit)]).cuda()
    xs = torch.from_numpy(rgb(tr[select])).cuda().permute(0, 3, 1, 2); ys = torch.from_numpy(ytr[select]).cuda(); del tr
    torch.manual_seed(SEED); m = tv.models.resnet18(weights="IMAGENET1K_V1"); m.fc = nn.Linear(512, K); m = m.cuda()
    opt = torch.optim.AdamW(m.parameters(), lr=3e-4, weight_decay=1e-4); norm = lambda x: (x.float() / 255 - MEAN) / STD; best, log = -1, []
    for ep in range(8):
        m.train(); o = torch.randperm(len(xf), device="cuda")
        for i in range(0, len(o) - 63, 64):
            b = o[i:i + 64]; x = xf[b]; f = torch.rand(len(b), device="cuda") < .5; x = torch.where(f.view(-1, 1, 1, 1), x.flip(3), x)
            with torch.autocast("cuda", dtype=torch.bfloat16): loss = nn.functional.cross_entropy(m(norm(x)), yf[b])
            opt.zero_grad(set_to_none=True); loss.backward(); opt.step()
        m.eval()
        with torch.inference_mode(): acc = float(torch.cat([m(norm(xs[i:i + 256])).argmax(1) for i in range(0, len(xs), 256)]).eq(ys).float().mean())
        log.append(acc); print(DS, "epoch", ep, acc, flush=True)
        if acc > best: best = acc; torch.save(m.state_dict(), "source.pt")
    m.load_state_dict(torch.load("source.pt", weights_only=True)); m.eval(); xv = torch.from_numpy(va).cuda().permute(0, 3, 1, 2)
    with torch.inference_mode(): pv = torch.cat([m(norm(xv[i:i + 256])).argmax(1).cpu() for i in range(0, len(xv), 256)])
    json.dump(dict(select=best, log=log, val_accuracy=float((pv.numpy() == yva).mean()), sizes=dict(fit=len(fit), val=len(va), test=len(te)), classes_test=np.bincount(yte, minlength=K).tolist()), open("source_report.json", "w"))
    del xf, xv; torch.cuda.empty_cache()
    with Pool(int(os.environ.get("PREP_PROCS", "8"))) as pool:
        for split, imgs in (("dev", va), ("held", te)):
            for name, levels in SETS[split].items():
                for lv, v in enumerate(levels, 1):
                    np.save(f"{split}_{name}_{lv}.npy", np.stack(pool.map(corrupt, [(im, name, v, SEED + i) for i, im in enumerate(imgs)], chunksize=64)))
    print("=== PREPARE DONE", DS, flush=True)

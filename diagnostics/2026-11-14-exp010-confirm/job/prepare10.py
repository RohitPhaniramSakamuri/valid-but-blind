"""Train one ResNet-18 and write corrupted sets for a MedMNIST-224 dataset. Usage: prepare10.py <tissue|organs> <classes>. Frozen with experiments/010.
As prepare8.py, except: held (test) images are also capped at 4,000 by a fixed seed (TissueMNIST has 47,280), new seed, and CPU fallback for smoke tests."""
import io, json, os, sys
from multiprocessing import Pool
import numpy as np, torch, torch.nn as nn, torchvision as tv
DS, K = sys.argv[1], int(sys.argv[2]); SEED = 20261114; WORK = os.environ["WORK"]; SMOKE = int(os.environ.get("SMOKE", "0"))
DEV_ = "cuda" if torch.cuda.is_available() else "cpu"
MEAN, STD = torch.tensor([0.485, 0.456, 0.406], device=DEV_).view(1, 3, 1, 1), torch.tensor([0.229, 0.224, 0.225], device=DEV_).view(1, 3, 1, 1)
DEV = dict(gaussian_noise=(.04, .08, .16), speckle_noise=(.08, .15, .30), brightness=(.1, .2, .4), gamma=(1.4, 2., 3.), shot_noise=(60, 25, 10),
           posterize=(16, 8, 4), salt_pepper=(.02, .05, .10), darken=(.8, .6, .4))
SETS = dict(dev=DEV, held=dict(gaussian_blur=(1, 2, 4), jpeg_compression=(30, 15, 6), contrast=(.6, .35, .15), pixelate=(112, 56, 28)))
from corrupt10 import corrupt
rgb = lambda a: np.repeat(a[..., None], 3, -1) if a.ndim == 3 else a
def cap(x, y, n, seed):
    if len(x) <= n: return x, y
    keep = np.sort(np.random.RandomState(seed).permutation(len(x))[:n]); return x[keep], y[keep]
if __name__ == "__main__":
    os.chdir(f"{WORK}/{DS}"); Z = np.load("data.npz")
    ytr, yva, yte = (Z[k].ravel().astype(np.int64) for k in ("train_labels", "val_labels", "test_labels"))
    assert int(ytr.max()) + 1 == K, f"class count {K} disagrees with labels ({int(ytr.max()) + 1})"
    va, yva = cap(Z["val_images"], yva, 4000, SEED); te, yte = cap(Z["test_images"], yte, 4000, SEED + 1); va, te = rgb(va), rgb(te)  # caps fixed before any run
    np.save("val.npy", va); np.save("test.npy", te); np.save("val_y.npy", yva); np.save("test_y.npy", yte)
    ntr = len(ytr); perm = np.random.RandomState(SEED).permutation(ntr); nfit = min(30000, ntr - 1500) if not SMOKE else 256
    calib, select, fit = perm[:1000], perm[1000:1500], np.sort(perm[1500:1500 + nfit]); tr = Z["train_images"]
    np.save("calib_x.npy", rgb(tr[np.sort(calib)])); np.save("calib_y.npy", ytr[np.sort(calib)])
    xf = torch.from_numpy(rgb(tr[fit])).to(DEV_).permute(0, 3, 1, 2); yf = torch.from_numpy(ytr[fit]).to(DEV_)
    xs = torch.from_numpy(rgb(tr[np.sort(select)])).to(DEV_).permute(0, 3, 1, 2); ys = torch.from_numpy(ytr[np.sort(select)]).to(DEV_); del tr
    torch.manual_seed(SEED); m = tv.models.resnet18(weights=None if SMOKE else "IMAGENET1K_V1"); m.fc = nn.Linear(512, K); m = m.to(DEV_)
    opt = torch.optim.AdamW(m.parameters(), lr=3e-4, weight_decay=1e-4); norm = lambda x: (x.float() / 255 - MEAN) / STD; best, log = -1, []
    for ep in range(1 if SMOKE else 8):
        m.train(); o = torch.randperm(len(xf), device=DEV_)
        for i in range(0, len(o) - 63, 64):
            b = o[i:i + 64]; x = xf[b]; f = torch.rand(len(b), device=DEV_) < .5; x = torch.where(f.view(-1, 1, 1, 1), x.flip(3), x)
            with torch.autocast(DEV_, dtype=torch.bfloat16, enabled=DEV_ == "cuda"): loss = nn.functional.cross_entropy(m(norm(x)), yf[b])
            opt.zero_grad(set_to_none=True); loss.backward(); opt.step()
        m.eval()
        with torch.inference_mode(): acc = float(torch.cat([m(norm(xs[i:i + 256])).argmax(1) for i in range(0, len(xs), 256)]).eq(ys).float().mean())
        log.append(acc); print(DS, "epoch", ep, acc, flush=True)
        if acc > best: best = acc; torch.save(m.state_dict(), "source.pt")
    m.load_state_dict(torch.load("source.pt", weights_only=True)); m.eval(); xv = torch.from_numpy(va).to(DEV_).permute(0, 3, 1, 2)
    with torch.inference_mode(): pv = torch.cat([m(norm(xv[i:i + 256])).argmax(1).cpu() for i in range(0, len(xv), 256)])
    json.dump(dict(select=best, log=log, val_accuracy=float((pv.numpy() == yva).mean()), sizes=dict(fit=len(fit), val=len(va), test=len(te)), classes_test=np.bincount(yte, minlength=K).tolist()), open("source_report.json", "w"))
    del xf, xv
    if DEV_ == "cuda": torch.cuda.empty_cache()
    with Pool(int(os.environ.get("PREP_PROCS", "8"))) as pool:
        for split, imgs in (("dev", va), ("held", te)):
            for name, levels in SETS[split].items():
                for lv, v in enumerate(levels, 1):
                    np.save(f"{split}_{name}_{lv}.npy", np.stack(pool.map(corrupt, [(im, name, v, SEED + i) for i, im in enumerate(imgs)], chunksize=64)))
    print("=== PREPARE DONE", DS, flush=True)

"""Log rich label-free signals per image and per batch. Usage: run.py <ds> <classes> <lr> <shard> <shards>. Labels are logged only for offline fitting on dev and scoring."""
import json, os, sys, time, zlib
import numpy as np, torch, torch.nn as nn, torchvision as tv
DS, K, LR, SH, NSH = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
os.chdir(DS); torch.set_num_threads(2); torch.backends.cudnn.benchmark = True
MEAN, STD = torch.tensor([0.485, 0.456, 0.406]).view(1, 3, 1, 1).cuda(), torch.tensor([0.229, 0.224, 0.225]).view(1, 3, 1, 1).cuda()
BATCH, TOTAL, RECAL, NDROP = 48, 120, 5, 10
GRID = torch.arange(.001, .99, .001).cuda(); QS = torch.linspace(.005, .995, 199).cuda()
PRIORS = (("natural", None), ("dir1", 1.), ("dir01", .1))
DEV = "gaussian_noise speckle_noise brightness gamma saturation".split(); HELD = "gaussian_blur jpeg_compression contrast pixelate".split()
seed_of = lambda *p: zlib.crc32("|".join(map(str, p)).encode()) % 2**31
def build():
    m = tv.models.resnet18(weights=None); m.fc = nn.Linear(512, K); m.load_state_dict(torch.load("source.pt", weights_only=True)); return m.cuda().eval().requires_grad_(False)
def adaptive():
    m = build(); P = []
    for b in m.modules():
        if isinstance(b, nn.BatchNorm2d):
            b.requires_grad_(True); b.track_running_stats = False; b.running_mean = None; b.running_var = None; P += [b.weight, b.bias]
    return m, P
def fwd(m, x):
    x = (x - MEAN) / STD; x = m.maxpool(m.relu(m.bn1(m.conv1(x)))); x = m.avgpool(m.layer4(m.layer3(m.layer2(m.layer1(x))))).flatten(1); return m.fc(x), x
def proto(f, m): return torch.cdist(nn.functional.normalize(f, dim=1), nn.functional.normalize(m.fc.weight, dim=1)).pow(2).min(1).values
def max_f1(err, u, grid):
    pos = u.view(1, -1) > grid.view(-1, 1); e = err.view(1, -1)
    tp, fp, fn = (pos & e).sum(1).float(), (pos & ~e).sum(1).float(), (~pos & e).sum(1).float()
    return grid[(2 * tp / (2 * tp + fp + fn).clamp_min(1)).argmax()].item()
def thr(m, cx, cy):
    with torch.inference_mode(): l, f = fwd(m, cx)
    e = l.argmax(1) != cy; u = 1 - l.softmax(1).max(1).values; p = proto(f, m)
    return max_f1(e, u, GRID), max_f1(e, p, torch.quantile(p, QS)), e, u, p, f
def stream(a, labels, rng):
    ids = np.arange(len(labels))
    if a is None: return [rng.choice(ids, BATCH) for _ in range(TOTAL)]
    p = rng.dirichlet(np.full(K, a)); c = np.bincount(labels, minlength=K)
    with np.errstate(divide="ignore", invalid="ignore"): w = np.nan_to_num(p[labels] / c[labels])
    w /= w.sum(); return [rng.choice(ids, BATCH, p=w) for _ in range(TOTAL)]
def plan():
    o = [("dev", c, s, pn, a, d) for c in DEV for s in (1, 2, 3) for pn, a in PRIORS for d in range(2)] + [("dev", "clean", 0, pn, a, d) for pn, a in PRIORS for d in range(2)]
    o += [("held", c, s, pn, a, d) for c in HELD for s in (1, 2, 3) for pn, a in PRIORS for d in range(3)] + [("held", "clean", 0, pn, a, d) for pn, a in PRIORS for d in range(3)]
    return o[SH::NSH]
if __name__ == "__main__":
    out_dir = f"streams_{LR}"; os.makedirs(out_dir, exist_ok=True)
    cx = torch.from_numpy(np.load("calib_x.npy")).permute(0, 3, 1, 2).float().div_(255).cuda(); cy = torch.from_numpy(np.load("calib_y.npy")).cuda()
    S = build(); W, _ = adaptive(); W.requires_grad_(False); T, P = adaptive(); init = [p.detach().clone() for p in P]
    q0, qp0, e0, u0, p0, f0 = thr(S, cx, cy); qt, _, et, ut, _, _ = thr(W, cx, cy)
    conf_clean = 1 - u0; srt = conf_clean.sort().values; t_atc = srt[int(e0.float().mean() * len(srt))].item()
    F = f0 - f0.mean(0); U = torch.pca_lowrank(F, q=16, center=False)[2]; mu = f0.mean(0)
    pw = {k: v.detach().cpu().numpy() for k, v in dict(pca=U, mu=mu).items()}
    ft = ut > qt
    cal = dict(ds=DS, lr=LR, r0=e0.float().mean().item(), q0=q0, qp0=qp0, qt=qt, t_atc=t_atc, conf_clean=conf_clean.mean().item(), fp0=((u0 > q0) & ~e0).float().mean().item(), fpp0=((p0 > qp0) & ~e0).float().mean().item(), r_twin=et.float().mean().item(), fpt=(ft & ~et).float().mean().item(), fnt=(~ft & et).float().mean().item(), n=len(cy), K=K, gpu=torch.cuda.get_device_name(0))
    json.dump(cal, open(f"{out_dir}/calibration.json", "w"))
    prior_c = np.bincount(np.load("calib_y.npy"), minlength=K) / len(cy)
    bns = [(n, b, b.running_mean.clone(), b.running_var.sqrt().clone()) for n, b in S.named_modules() if isinstance(b, nn.BatchNorm2d)]
    store = {}
    def hook(n, mean, std):
        block = n.split(".")[0] if n.startswith("layer") else "bn1"
        def f(_, inp):
            z = ((inp[0].mean((0, 2, 3)) - mean) / std.clamp_min(1e-5)).abs().mean(); store.setdefault(block, []).append(z)
        return f
    for n, b, mean, std in bns: b.register_forward_pre_hook(hook(n, mean, std))
    BL = ["bn1", "layer1", "layer2", "layer3", "layer4"]
    base = dict(dev=np.load("val.npy", mmap_mode="r"), held=np.load("test.npy", mmap_mode="r")); Y = dict(dev=np.load("val_y.npy"), held=np.load("test_y.npy"))
    t0 = time.time(); pl = plan()
    for n, (split, c, s, pn, a, d) in enumerate(pl):
        key = f"{split}__{c}__{s}__{pn}__{d}"; path = f"{out_dir}/{key}.npz"
        if os.path.exists(path): continue
        imgs = base[split] if c == "clean" else np.load(f"{split}_{c}_{s}.npy", mmap_mode="r"); labels = Y[split]
        order = stream(a, labels, np.random.RandomState(seed_of("exp005", DS, split, c, s, pn, d)))
        with torch.no_grad():
            for p, v in zip(P, init): p.copy_(v)
        opt = torch.optim.Adam(P, lr=LR); qc, qp = q0, qp0; I, B = [], []
        g = torch.Generator(device="cuda").manual_seed(seed_of(key))
        for t, ids in enumerate(order):
            sid = np.sort(ids); x = torch.from_numpy(np.asarray(imgs[sid])).cuda().permute(0, 3, 1, 2).float().div_(255); y = torch.from_numpy(labels[sid]).cuda()
            lT, fT = fwd(T, x); pT = lT.softmax(1); ent = -(pT * lT.log_softmax(1)).sum(1)
            opt.zero_grad(set_to_none=True); ent.mean().backward(); opt.step(); lT, fT = lT.detach(), fT.detach()
            if t % RECAL == 0: qc, qp, *_ = thr(T, cx, cy)
            store.clear()
            with torch.inference_mode():
                lW, fW = fwd(W, x); lS, _ = fwd(S, x)
                pT, pW, pS = lT.softmax(1), lW.softmax(1), lS.softmax(1); aT, aW, aS = lT.log_softmax(1), lW.log_softmax(1), lS.log_softmax(1)
                tT, tW = pT.topk(2, 1).values, pW.topk(2, 1).values; yT, yW, yS = lT.argmax(1), lW.argmax(1), lS.argmax(1)
                en = lambda p, a: -(p * a).sum(1)
                mask = (torch.rand((NDROP, *fT.shape), device=x.device, generator=g) > .4).float() / .6
                dd = (T.fc(mask * fT).argmax(2) != yT).float().mean(0)
                pr = proto(fT, T); prW = proto(fW, W); uT = 1 - tT[:, 0]
                row = torch.stack((tT[:, 0], tW[:, 0], pS.max(1).values, tT[:, 0] - tT[:, 1], tW[:, 0] - tW[:, 1], en(pT, aT), en(pW, aW), en(pS, aS), (yT == yW).float(), (yT == yS).float(), (yW == yS).float(), (pT * (aT - aW)).sum(1), (pT * (aT - aS)).sum(1), pr, prW, fT.norm(dim=1), dd, (yT != y).float(), (yW != y).float(), (yS != y).float(), yT.float(), (uT > qc).float(), (pr > qp).float(), ((1 - tW[:, 0]) > qt).float()), 1)
                ph = torch.bincount(yT, minlength=K).float() / len(y); phs = ph.clamp_min(1e-6)
                up = torch.as_tensor(U); bv = torch.cat((torch.stack([torch.stack(store[b]).mean() for b in BL]), torch.stack((-(ph * phs.log()).sum() / np.log(K), (ph - torch.as_tensor(prior_c, device=ph.device, dtype=ph.dtype)).abs().sum() / 2, torch.cat([(p - v).flatten() for p, v in zip(P, init)]).norm(), (fT.mean(0) - mu).norm(), (fW.mean(0) - mu).norm())), (fT - mu).mean(0) @ up, (fW - mu).mean(0) @ up))
            I.append(row.half().cpu()); B.append(bv.float().cpu())
        np.savez(path, img=torch.stack(I).numpy(), batch=torch.stack(B).numpy())
        print(DS, LR, n + 1, len(pl), key, f"err={torch.stack(I)[:, :, 17].float().mean():.3f}", f"elapsed={time.time() - t0:.0f}s", flush=True)
    print("complete", flush=True)

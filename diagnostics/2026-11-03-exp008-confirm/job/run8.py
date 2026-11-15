"""exp008 streams. Usage: run8.py <ds> <model> <arm> <shard> <nshards>. ds in organc, oct, pneumonia, cifar. Frozen with experiments/008."""
import copy, json, math, os, pickle, sys, time, zlib
import numpy as np, torch, torch.nn as nn, torchvision as tv
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
DS, NAME, ARM, SH, NSH = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
WORK, OUT = os.environ["WORK"], os.environ["OUT"]
torch.set_num_threads(1); torch.backends.cudnn.benchmark = True
BATCH, TOTAL, RECAL, NDROP = 48, 120, 5, 10
GRID = torch.arange(.001, .99, .001).cuda(); QS = torch.linspace(.005, .995, 199).cuda()
PRIORS = (("natural", None), ("dir1", 1.), ("dir01", .1)); PRIORS_DEV = PRIORS + (("dir03", .3),)
MEAN, STD = torch.tensor([0.485, 0.456, 0.406]).view(1, 3, 1, 1).cuda(), torch.tensor([0.229, 0.224, 0.225]).view(1, 3, 1, 1).cuda()
seed_of = lambda *p: zlib.crc32("|".join(map(str, p)).encode()) % 2**31
if DS == "cifar":
    K = 100; SYN = ["gamma", "posterize", "salt_pepper", "darken"]; DEV = "speckle_noise gaussian_blur spatter saturate".split() + SYN; SEV = (1, 3, 5); DRAW_DEV, DRAW_HELD = 2, 1
    SYN_LV = dict(gamma={1: 1.4, 3: 2., 5: 3.}, posterize={1: 16, 3: 8, 5: 4}, salt_pepper={1: .02, 3: .05, 5: .10}, darken={1: .8, 3: .6, 5: .4})
    HELD = "gaussian_noise shot_noise impulse_noise defocus_blur glass_blur motion_blur zoom_blur snow frost fog brightness contrast elastic_transform pixelate jpeg_compression".split()
else:
    K = dict(organc=11, oct=4, pneumonia=2)[DS]; DEV = "gaussian_noise speckle_noise brightness gamma shot_noise posterize salt_pepper darken".split()
    HELD = "gaussian_blur jpeg_compression contrast pixelate".split(); SEV = (1, 2, 3); DRAW_DEV, DRAW_HELD = 2, 3
class Net(nn.Module):
    """Wraps a classifier; returns logits and the input of its last linear layer."""
    def __init__(s, m, norm):
        super().__init__(); s.m, s.norm = m, norm; s.head = [x for x in m.modules() if isinstance(x, nn.Linear)][-1]; s.f = {}
        s.head.register_forward_hook(lambda mod, i, o: s.f.__setitem__("x", i[0]))
    def forward(s, x):
        o = s.m((x - MEAN) / STD if s.norm else x); return o, s.f["x"]
def build():
    if DS == "cifar":
        import cifar_models as CM; m = CM.load_cifar(NAME, f"{WORK}/models/{NAME}.pt", HERE); return Net(m, False).cuda().eval().requires_grad_(False)
    m = tv.models.resnet18(weights=None); m.fc = nn.Linear(512, K); m.load_state_dict(torch.load(f"{WORK}/{DS}/source.pt", weights_only=True)); return Net(m, True).cuda().eval().requires_grad_(False)
def adaptive():
    m = build(); P = []
    for b in m.modules():
        if isinstance(b, nn.BatchNorm2d):
            b.requires_grad_(True); b.track_running_stats = False; b.running_mean = None; b.running_var = None; P += [b.weight, b.bias]
    return m, P
def proto(f, m): return torch.cdist(nn.functional.normalize(f, dim=1), nn.functional.normalize(m.head.weight, dim=1)).pow(2).min(1).values
def max_f1(err, u, grid):
    pos = u.view(1, -1) > grid.view(-1, 1); e = err.view(1, -1)
    tp, fp, fn = (pos & e).sum(1).float(), (pos & ~e).sum(1).float(), (~pos & e).sum(1).float()
    return grid[(2 * tp / (2 * tp + fp + fn).clamp_min(1)).argmax()].item()
def thr(m, cx, cy):
    with torch.inference_mode(): l, f = m(cx); l, f = l.float(), f.float()
    e = l.argmax(1) != cy; u = 1 - l.softmax(1).max(1).values; p = proto(f, m)
    return max_f1(e, u, GRID), max_f1(e, p, torch.quantile(p, QS)), e, u, p, f
def ent(l): return -(l.softmax(1) * l.log_softmax(1)).sum(1)
LR_SAR, MOM, RHO, RESET, MARGIN = 0.00025, 0.9, 0.05, 0.2, 0.4 * math.log(K)
def sar_step(m, P, opt, x, st):
    l, f = m(x); e1 = ent(l); k1 = e1 < MARGIN
    if k1.any():
        opt.zero_grad(set_to_none=True); e1[k1].mean().backward(); g = [p.grad for p in P if p.grad is not None]
        sc = RHO / (torch.norm(torch.stack([x.norm(2) for x in g]), 2) + 1e-12); saved = [p.detach().clone() for p in P]
        with torch.no_grad():
            for p in P:
                if p.grad is not None: p.add_(p.grad * sc)
        opt.zero_grad(set_to_none=True); e2 = ent(m(x)[0])[k1]; k2 = e2 < MARGIN
        if k2.any():
            l2 = e2[k2].mean(); l2.backward(); st["ema"] = float(l2) if st["ema"] is None else .9 * st["ema"] + .1 * float(l2)
        with torch.no_grad():
            for p, v in zip(P, saved): p.copy_(v)
        if k2.any(): opt.step()
        opt.zero_grad(set_to_none=True)
    if st["ema"] is not None and st["ema"] < RESET:
        with torch.no_grad():
            for p, v in zip(P, st["init"]): p.copy_(v)
        opt.load_state_dict(copy.deepcopy(st["opt0"])); st["ema"] = None
    return l.detach(), f.detach()
def stream(a, pool, labels, rng):
    if a is None: return [rng.choice(pool, BATCH) for _ in range(TOTAL)]
    p = rng.dirichlet(np.full(K, a)); c = np.bincount(labels[pool], minlength=K)
    with np.errstate(divide="ignore", invalid="ignore"): w = np.nan_to_num(p[labels[pool]] / c[labels[pool]])
    w /= w.sum(); return [rng.choice(pool, BATCH, p=w) for _ in range(TOTAL)]
def plan():
    o = [("dev", c, s, pn, a, d) for c in DEV for s in SEV for pn, a in PRIORS_DEV for d in range(DRAW_DEV)] + [("dev", "clean", 0, pn, a, d) for pn, a in PRIORS_DEV for d in range(2)]
    o += [("held", c, s, pn, a, d) for c in HELD for s in SEV for pn, a in PRIORS for d in range(DRAW_HELD)] + [("held", "clean", 0, pn, a, d) for pn, a in PRIORS for d in range(2 if DS == "cifar" else 3)]
    return o[SH::NSH]
class Data:
    def __init__(s):
        if DS == "cifar":
            r = f"{WORK}/cifar"; s.y = np.load(f"{r}/CIFAR-100-C/labels.npy")[:10000].astype(np.int64)
            d = pickle.load(open(f"{r}/cifar-100-python/test", "rb"), encoding="latin1"); s.clean = np.asarray(d["data"]).reshape(-1, 3, 32, 32).transpose(0, 2, 3, 1).copy()
            assert (np.asarray(d["fine_labels"]) == s.y).all()
            perm = np.random.RandomState(20261103).permutation(10000); s.calib = perm[:1000]; s.pool = dict(dev=perm[1000:5000], held=perm[5000:]); s.cy = s.y[s.calib]; s.cx = s.clean[s.calib]; s.cache = {}
        else:
            r = f"{WORK}/{DS}"; s.cx, s.cy = np.load(f"{r}/calib_x.npy"), np.load(f"{r}/calib_y.npy"); s.Y = dict(dev=np.load(f"{r}/val_y.npy"), held=np.load(f"{r}/test_y.npy"))
            s.base = dict(dev=np.load(f"{r}/val.npy", mmap_mode="r"), held=np.load(f"{r}/test.npy", mmap_mode="r"))
    def get(s, split, c, sev):
        if DS == "cifar":
            if c == "clean": return s.clean, s.y, s.pool[split]
            if c in SYN:
                key = (c, sev)
                if key not in s.cache:
                    from corrupt8 import corrupt
                    s.cache = {key: np.stack([corrupt((im, c, SYN_LV[c][sev], 20261103 + i)) for i, im in enumerate(s.clean)])}
                return s.cache[key], s.y, s.pool[split]
            if c not in s.cache: s.cache = {c: np.load(f"{WORK}/cifar/CIFAR-100-C/{c}.npy", mmap_mode="r")}
            return s.cache[c][(sev - 1) * 10000:sev * 10000], s.y, s.pool[split]
        imgs = s.base[split] if c == "clean" else np.load(f"{WORK}/{DS}/{split}_{c}_{sev}.npy", mmap_mode="r"); return imgs, s.Y[split], np.arange(len(s.Y[split]))
if __name__ == "__main__":
    tag = f"{DS}__{NAME}__{ARM}"; out_dir = f"{OUT}/streams/{tag}"; os.makedirs(out_dir, exist_ok=True)
    D = Data(); cx = torch.from_numpy(D.cx).permute(0, 3, 1, 2).float().div_(255).cuda(); cy = torch.from_numpy(D.cy).cuda()
    S = build(); W, _ = adaptive(); W.requires_grad_(False); T, P = adaptive(); init = [p.detach().clone() for p in P]
    q0, qp0, e0, u0, p0, f0 = thr(S, cx, cy); qt, _, et, ut, _, _ = thr(W, cx, cy)
    conf_clean = 1 - u0; srt = conf_clean.sort().values; t_atc = srt[min(int(e0.float().mean() * len(srt)), len(srt) - 1)].item()
    mu = f0.mean(0); U = torch.pca_lowrank(f0 - mu, q=16, center=False)[2]; ft = ut > qt
    cal = dict(ds=DS, model=NAME, arm=ARM, r0=e0.float().mean().item(), q0=q0, qp0=qp0, qt=qt, t_atc=t_atc, conf_clean=conf_clean.mean().item(), fp0=((u0 > q0) & ~e0).float().mean().item(), fpp0=((p0 > qp0) & ~e0).float().mean().item(), r_twin=et.float().mean().item(), fpt=(ft & ~et).float().mean().item(), fnt=(~ft & et).float().mean().item(), n=len(cy), K=K, gpu=torch.cuda.get_device_name(0), torch=torch.__version__)
    json.dump(cal, open(f"{out_dir}/calibration.json", "w"))
    prior_c = torch.as_tensor(np.bincount(D.cy, minlength=K) / len(D.cy), device="cuda", dtype=torch.float32)
    bns = [b for b in S.modules() if isinstance(b, nn.BatchNorm2d)]; groups = np.array_split(np.arange(len(bns)), 5); zs = [None] * len(bns); used = None
    def hook(i, b):
        def f(_, inp): zs[i] = ((inp[0].float().mean((0, 2, 3)) - b.running_mean) / b.running_var.sqrt().clamp_min(1e-5)).abs().mean()
        return f
    for i, b in enumerate(bns): b.register_forward_pre_hook(hook(i, b))
    t0 = time.time(); pl = plan()
    for n, (split, c, s, pn, a, d) in enumerate(pl):
        key = f"{split}__{c}__{s}__{pn}__{d}"; path = f"{out_dir}/{key}.npz"
        if os.path.exists(path): continue
        imgs, labels, pool = D.get(split, c, s)
        order = stream(a, pool, labels, np.random.RandomState(seed_of("exp008", DS, NAME, split, c, s, pn, d)))
        with torch.no_grad():
            for p, v in zip(P, init): p.copy_(v)
        if ARM == "sar": opt = torch.optim.SGD(P, lr=LR_SAR, momentum=MOM); st = dict(ema=None, init=init, opt0=copy.deepcopy(opt.state_dict()))
        else: opt = torch.optim.Adam(P, lr=float(ARM[4:]))
        qc, qp = q0, qp0; I, B = [], []; g = torch.Generator(device="cuda").manual_seed(seed_of(tag, key))
        for t, ids in enumerate(order):
            sid = np.sort(ids); x = torch.from_numpy(np.asarray(imgs[sid])).cuda().permute(0, 3, 1, 2).float().div_(255); y = torch.from_numpy(labels[sid]).cuda()
            if ARM == "sar": lT, fT = sar_step(T, P, opt, x, st)
            else:
                lT, fT = T(x); opt.zero_grad(set_to_none=True); ent(lT).mean().backward(); opt.step(); lT, fT = lT.detach(), fT.detach()
            if t % RECAL == 0: qc, qp, *_ = thr(T, cx, cy)
            with torch.inference_mode():
                lW, fW = W(x); lS, _ = S(x); lT, fT, lW, fW, lS = lT.float(), fT.float(), lW.float(), fW.float(), lS.float()
                pT, pW, pS = lT.softmax(1), lW.softmax(1), lS.softmax(1); aT, aW, aS = lT.log_softmax(1), lW.log_softmax(1), lS.log_softmax(1)
                tT, tW = pT.topk(2, 1).values, pW.topk(2, 1).values; yT, yW, yS = lT.argmax(1), lW.argmax(1), lS.argmax(1)
                en = lambda p, a: -(p * a).sum(1)
                mask = (torch.rand((NDROP, *fT.shape), device=x.device, generator=g) > .4).float() / .6
                dd = (T.head(mask * fT).argmax(2) != yT).float().mean(0)
                pr = proto(fT, T); prW = proto(fW, W); uT = 1 - tT[:, 0]
                row = torch.stack((tT[:, 0], tW[:, 0], pS.max(1).values, tT[:, 0] - tT[:, 1], tW[:, 0] - tW[:, 1], en(pT, aT), en(pW, aW), en(pS, aS), (yT == yW).float(), (yT == yS).float(), (yW == yS).float(), (pT * (aT - aW)).sum(1), (pT * (aT - aS)).sum(1), pr, prW, fT.norm(dim=1), dd, (yT != y).float(), (yW != y).float(), (yS != y).float(), yT.float(), (uT > qc).float(), (pr > qp).float(), ((1 - tW[:, 0]) > qt).float(), yW.float(), yS.float()), 1)
                ph = torch.bincount(yT, minlength=K).float() / len(y)
                if used is None: used = [i for i, v in enumerate(zs) if v is not None]; groups = np.array_split(np.arange(len(used)), 5)  # some architectures hold unused BN layers
                z = torch.stack([zs[i] for i in used]); bv = torch.cat((torch.stack([z[gi].mean() for gi in groups]), torch.stack((-(ph * ph.clamp_min(1e-6).log()).sum() / math.log(K), (ph - prior_c).abs().sum() / 2, torch.cat([(p - v).flatten() for p, v in zip(P, init)]).norm(), (fT.mean(0) - mu).norm(), (fW.mean(0) - mu).norm())), (fT - mu).mean(0) @ U, (fW - mu).mean(0) @ U))
            I.append(row.half()); B.append(bv.float())
        I = torch.stack(I).cpu(); np.savez(path + ".tmp.npz", img=I.numpy(), batch=torch.stack(B).cpu().numpy()); os.replace(path + ".tmp.npz", path)
        print(tag, n + 1, len(pl), key, f"err={I[:, :, 17].float().mean():.3f}", f"elapsed={time.time() - t0:.0f}s", flush=True)
    print("complete", tag, flush=True)

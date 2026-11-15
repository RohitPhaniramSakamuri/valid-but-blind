"""exp010 streams. Usage: run10.py <ds> <model> <arm> <shard> <nshards>. ds in tissue, organs, cifar10. Frozen with experiments/010.
Same per-image columns as exp008 (run8.py), so the analysis loader is shared. Differences from run8.py:
  - new datasets (TissueMNIST-224, OrganSMNIST-224, CIFAR-10-C with RobustBench CIFAR-10 checkpoints) and new seeds (tag exp010);
  - adaptation objective is an arm: tent<lr> (entropy), pl<lr> (hard pseudo-label cross-entropy), im<lr> (information maximisation: entropy minus marginal entropy);
  - runs on CPU when no GPU exists (smoke tests only); SMOKE=<n> keeps n batches per stream and a few streams."""
import copy, json, math, os, pickle, sys, time, zlib
import numpy as np, torch, torch.nn as nn, torchvision as tv
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
DS, NAME, ARM, SH, NSH = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
WORK, OUT = os.environ["WORK"], os.environ["OUT"]; SMOKE = int(os.environ.get("SMOKE", "0"))
DEV_ = "cuda" if torch.cuda.is_available() else "cpu"
if DEV_ == "cuda": torch.set_num_threads(1); torch.backends.cudnn.benchmark = True
BATCH, TOTAL, RECAL, NDROP = 48, (SMOKE or 120), 5, 10
GRID = torch.arange(.001, .99, .001, device=DEV_); QS = torch.linspace(.005, .995, 199, device=DEV_)
PRIORS = (("natural", None), ("dir1", 1.), ("dir01", .1)); PRIORS_DEV = PRIORS + (("dir03", .3),)
MEAN, STD = torch.tensor([0.485, 0.456, 0.406], device=DEV_).view(1, 3, 1, 1), torch.tensor([0.229, 0.224, 0.225], device=DEV_).view(1, 3, 1, 1)
seed_of = lambda *p: zlib.crc32("|".join(map(str, p)).encode()) % 2**31
OBJ, LR = next((k, float(ARM[len(k):])) for k in ("tent", "pl", "im") if ARM.startswith(k))
if DS == "cifar10":
    K = 10; SYN = ["gamma", "posterize", "salt_pepper", "darken"]; DEV = "speckle_noise gaussian_blur spatter saturate".split() + SYN; SEV = (1, 3, 5); DRAW_DEV, DRAW_HELD = 2, 1
    SYN_LV = dict(gamma={1: 1.4, 3: 2., 5: 3.}, posterize={1: 16, 3: 8, 5: 4}, salt_pepper={1: .02, 3: .05, 5: .10}, darken={1: .8, 3: .6, 5: .4})
    HELD = "gaussian_noise shot_noise impulse_noise defocus_blur glass_blur motion_blur zoom_blur snow frost fog brightness contrast elastic_transform pixelate jpeg_compression".split()
else:
    K = dict(tissue=8, organs=11)[DS]; DEV = "gaussian_noise speckle_noise brightness gamma shot_noise posterize salt_pepper darken".split()
    HELD = "gaussian_blur jpeg_compression contrast pixelate".split(); SEV = (1, 2, 3); DRAW_DEV, DRAW_HELD = 2, 3
class Net(nn.Module):
    """Wraps a classifier; returns logits and the input of its last linear layer."""
    def __init__(s, m, norm):
        super().__init__(); s.m, s.norm = m, norm; s.head = [x for x in m.modules() if isinstance(x, nn.Linear)][-1]; s.f = {}
        s.head.register_forward_hook(lambda mod, i, o: s.f.__setitem__("x", i[0]))
    def forward(s, x):
        o = s.m((x - MEAN) / STD if s.norm else x); return o, s.f["x"]
def build():
    if DS == "cifar10":
        import cifar_models as CM; m = CM.load_cifar10(NAME, f"{WORK}/models/c10_{NAME}.pt", HERE); return Net(m, False).to(DEV_).eval().requires_grad_(False)
    m = tv.models.resnet18(weights=None); m.fc = nn.Linear(512, K); m.load_state_dict(torch.load(f"{WORK}/{DS}/source.pt", weights_only=True, map_location="cpu")); return Net(m, True).to(DEV_).eval().requires_grad_(False)
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
    with torch.inference_mode():
        o = [m(cx[i:i + 250]) for i in range(0, len(cx), 250)]; l, f = torch.cat([a for a, _ in o]).float(), torch.cat([b for _, b in o]).float()
    e = l.argmax(1) != cy; u = 1 - l.softmax(1).max(1).values; p = proto(f, m)
    return max_f1(e, u, GRID), max_f1(e, p, torch.quantile(p, QS)), e, u, p, f
def ent(l): return -(l.softmax(1) * l.log_softmax(1)).sum(1)
def objective(l):
    if OBJ == "tent": return ent(l).mean()
    if OBJ == "pl": return nn.functional.cross_entropy(l, l.argmax(1).detach())
    pb = l.softmax(1).mean(0); return ent(l).mean() + (pb * pb.clamp_min(1e-8).log()).sum()  # im: minimise entropy, maximise marginal entropy
def stream(a, pool, labels, rng):
    if a is None: return [rng.choice(pool, BATCH) for _ in range(TOTAL)]
    p = rng.dirichlet(np.full(K, a)); c = np.bincount(labels[pool], minlength=K)
    with np.errstate(divide="ignore", invalid="ignore"): w = np.nan_to_num(p[labels[pool]] / c[labels[pool]])
    w /= w.sum(); return [rng.choice(pool, BATCH, p=w) for _ in range(TOTAL)]
def plan():
    o = [("dev", c, s, pn, a, d) for c in DEV for s in SEV for pn, a in PRIORS_DEV for d in range(DRAW_DEV)] + [("dev", "clean", 0, pn, a, d) for pn, a in PRIORS_DEV for d in range(2)]
    o += [("held", c, s, pn, a, d) for c in HELD for s in SEV for pn, a in PRIORS for d in range(DRAW_HELD)] + [("held", "clean", 0, pn, a, d) for pn, a in PRIORS for d in range(2 if DS == "cifar10" else 3)]
    if SMOKE: o = [x for x in o if x[1] in os.environ.get("SMOKE_COR", "clean").split(",")][::7][:6]
    return o[SH::NSH]
class Data:
    def __init__(s):
        if DS == "cifar10":
            r = f"{WORK}/cifar10"; s.y = np.load(f"{r}/CIFAR-10-C/labels.npy")[:10000].astype(np.int64); s.clean = np.load(f"{r}/clean_x.npy")
            assert (np.load(f"{r}/clean_y.npy") == s.y).all()
            perm = np.random.RandomState(20261114).permutation(10000); s.calib = perm[:1000]; s.pool = dict(dev=perm[1000:5000], held=perm[5000:]); s.cy = s.y[s.calib]; s.cx = s.clean[s.calib]; s.cache = {}
        else:
            r = f"{WORK}/{DS}"; s.cx, s.cy = np.load(f"{r}/calib_x.npy"), np.load(f"{r}/calib_y.npy"); s.Y = dict(dev=np.load(f"{r}/val_y.npy"), held=np.load(f"{r}/test_y.npy"))
            s.base = dict(dev=np.load(f"{r}/val.npy", mmap_mode="r"), held=np.load(f"{r}/test.npy", mmap_mode="r"))
    def get(s, split, c, sev):
        if DS == "cifar10":
            if c == "clean": return s.clean, s.y, s.pool[split]
            if c in SYN:
                key = (c, sev)
                if key not in s.cache:
                    from corrupt10 import corrupt
                    s.cache = {key: np.stack([corrupt((im, c, SYN_LV[c][sev], 20261114 + i)) for i, im in enumerate(s.clean)])}
                return s.cache[key], s.y, s.pool[split]
            if c not in s.cache: s.cache = {c: np.load(f"{WORK}/cifar10/CIFAR-10-C/{c}.npy", mmap_mode="r")}
            return s.cache[c][(sev - 1) * 10000:sev * 10000], s.y, s.pool[split]
        imgs = s.base[split] if c == "clean" else np.load(f"{WORK}/{DS}/{split}_{c}_{sev}.npy", mmap_mode="r"); return imgs, s.Y[split], np.arange(len(s.Y[split]))
if __name__ == "__main__":
    tag = f"{DS}__{NAME}__{ARM}"; out_dir = f"{OUT}/streams/{tag}"; os.makedirs(out_dir, exist_ok=True)
    D = Data(); cx = torch.from_numpy(D.cx).permute(0, 3, 1, 2).float().div_(255).to(DEV_); cy = torch.from_numpy(D.cy).to(DEV_)
    S = build(); W, _ = adaptive(); W.requires_grad_(False); T, P = adaptive(); init = [p.detach().clone() for p in P]
    q0, qp0, e0, u0, p0, f0 = thr(S, cx, cy); qt, _, et, ut, _, _ = thr(W, cx, cy)
    conf_clean = 1 - u0; srt = conf_clean.sort().values; t_atc = srt[min(int(e0.float().mean() * len(srt)), len(srt) - 1)].item()
    mu = f0.mean(0); U = torch.pca_lowrank(f0 - mu, q=16, center=False)[2]; ft = ut > qt
    cal = dict(ds=DS, model=NAME, arm=ARM, r0=e0.float().mean().item(), q0=q0, qp0=qp0, qt=qt, t_atc=t_atc, conf_clean=conf_clean.mean().item(), fp0=((u0 > q0) & ~e0).float().mean().item(), fpp0=((p0 > qp0) & ~e0).float().mean().item(), r_twin=et.float().mean().item(), fpt=(ft & ~et).float().mean().item(), fnt=(~ft & et).float().mean().item(), n=len(cy), K=K, gpu=(torch.cuda.get_device_name(0) if DEV_ == "cuda" else "cpu"), torch=torch.__version__)
    json.dump(cal, open(f"{out_dir}/calibration.json", "w"))
    prior_c = torch.as_tensor(np.bincount(D.cy, minlength=K) / len(D.cy), device=DEV_, dtype=torch.float32)
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
        order = stream(a, pool, labels, np.random.RandomState(seed_of("exp010", DS, NAME, split, c, s, pn, d)))
        with torch.no_grad():
            for p, v in zip(P, init): p.copy_(v)
        opt = torch.optim.Adam(P, lr=LR)
        qc, qp = q0, qp0; I, B = [], []; g = torch.Generator(device=DEV_).manual_seed(seed_of(tag, key))
        for t, ids in enumerate(order):
            sid = np.sort(ids); x = torch.from_numpy(np.asarray(imgs[sid])).to(DEV_).permute(0, 3, 1, 2).float().div_(255); y = torch.from_numpy(labels[sid]).to(DEV_)
            lT, fT = T(x); opt.zero_grad(set_to_none=True); objective(lT).backward(); opt.step(); lT, fT = lT.detach(), fT.detach()
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
                if used is None: used = [i for i, v in enumerate(zs) if v is not None]; groups = np.array_split(np.arange(len(used)), 5)
                z = torch.stack([zs[i] for i in used]); bv = torch.cat((torch.stack([z[gi].mean() for gi in groups]), torch.stack((-(ph * ph.clamp_min(1e-6).log()).sum() / math.log(K), (ph - prior_c).abs().sum() / 2, torch.cat([(p - v).flatten() for p, v in zip(P, init)]).norm(), (fT.mean(0) - mu).norm(), (fW.mean(0) - mu).norm())), (fT - mu).mean(0) @ U, (fW - mu).mean(0) @ U))
            I.append(row.half()); B.append(bv.float())
        I = torch.stack(I).cpu(); np.savez(path + ".tmp.npz", img=I.numpy(), batch=torch.stack(B).cpu().numpy()); os.replace(path + ".tmp.npz", path)
        print(tag, n + 1, len(pl), key, f"err={I[:, :, 17].float().mean():.3f}", f"errS={I[:, :, 19].float().mean():.3f}", f"elapsed={time.time() - t0:.0f}s", flush=True)
    print("complete", tag, flush=True)

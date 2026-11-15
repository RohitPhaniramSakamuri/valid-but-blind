"""Shared loader for the alarm diagnosis. exp006 streams and exp005 streams (BloodMNIST/DermaMNIST) into per-batch label-free signals plus labels for scoring.
EXPLORATORY: every held stream here has already been seen."""
import glob, json, math, os
from multiprocessing import Pool
import numpy as np
R6 = "../2026-11-03-exp006-confirm/results/streams"; R5 = "exp005_streams"
COLS = dict(errT=17, errW=18, errS=19, confT=0, confW=1, confS=2, agreeTW=8, agreeTS=9, agreeWS=10, kl=11, dd=16, rel=21, pro=22, twF=23, entT=5, entW=6, marT=3, marW=4)
def cells(I):
    tw, ts, ws, F = I[:, :, 8] > .5, I[:, :, 9] > .5, I[:, :, 10] > .5, I[:, :, 23] > .5
    P = [tw & ts, tw & ~ts, ts & ~tw, ws & ~tw, ~tw & ~ts & ~ws]
    return np.stack([(p & f).mean(1) for p in P for f in (F, ~F)], 1)  # (T,10): pattern x twin-uncertain
def one(p):
    d = os.path.dirname(p); c = json.load(open(d + "/calibration.json")); split, cor, sev, pr, rep = os.path.basename(p)[:-4].split("__")
    if "model" not in c: c["model"] = c["ds"]; c["arm"] = f"tent{c['lr']}"
    z = np.load(p); I = z["img"].astype(np.float32); B = z["batch"].astype(np.float32)
    E = I[:, :, 17] > .5; F = I[:, :, 23] > .5; A = I[:, :, 8] > .5
    b = {k: I[:, :, v].mean(1) for k, v in COLS.items()}
    flag = F | ~A
    b.update(flag=flag.mean(1), false_flag=(flag & ~E).mean(1), hidden=(E & ~flag).mean(1), atc=(I[:, :, 0] < c["t_atc"]).mean(1), predH=B[:, 5], tv=B[:, 6], drift=B[:, 7], bn=B[:, :5].mean(1))
    e = b["errT"]; m, l = e.mean(), e[-30:].mean()
    return dict(ds=c["ds"], model=c["model"], arm=c["arm"], split=split, cor=cor, sev=int(sev), prior=pr, rep=int(rep), c=c,
                strict=bool(m >= c["r0"] + .15 and l < .85), safe=bool(m < c["r0"] + .1 and l < .85), collapsed=bool(l >= .85),
                err=float(m), b={k: v.astype(np.float32) for k, v in b.items()}, X=cells(I).astype(np.float32))
def load(root=R6):
    files = sorted(f for f in glob.glob(f"{root}/*/*.npz") + glob.glob(f"{root}/*/*/*.npz") if not f.endswith(".tmp.npz"))
    with Pool(os.cpu_count()) as pool: return pool.map(one, files, chunksize=16)
IDX = np.arange(10, 120, 5)
cum = lambda x: np.cumsum(x, 0) / np.arange(1, len(x) + 1).reshape(-1, *([1] * (np.ndim(x) - 1)))
def conformal(v, alpha=.05):
    v = np.sort(np.asarray(v)); n = len(v); k = math.ceil((n + 1) * (1 - alpha))
    return (float(v[k - 1]) if k <= n else float("inf")), n

"""exp009 cache: per-batch label-free signals (and labels for scoring) for every saved stream of exp005, exp006 and exp008.
Reads the saved per-image arrays; runs no model. Output: cache9.pkl (list of dicts)."""
import glob, json, math, os, pickle, sys
from multiprocessing import Pool
import numpy as np
D = os.path.dirname(os.path.abspath(__file__)) + "/.."
ROOTS = dict(exp005=[f"{D}/2026-11-03-exp007-alarm-diagnosis/exp005_streams"], exp006=[f"{D}/2026-11-03-exp006-confirm/results/streams"],
             exp008=[f"{D}/2026-11-03-exp008-confirm/results/streams", f"{D}/2026-11-03-exp008-confirm/results_med/*/streams"])
def one(a):
    exp, p = a
    d = os.path.dirname(p); c = json.load(open(d + "/calibration.json")); split, cor, sev, pr, rep = os.path.basename(p)[:-4].split("__")
    if "model" not in c: c["model"] = c["ds"]; c["arm"] = f"tent{c['lr']}"
    z = np.load(p); I = z["img"].astype(np.float32); B = z["batch"].astype(np.float32)
    E = I[:, :, 17] > .5; F = I[:, :, 23] > .5; tw, ts, ws = I[:, :, 8] > .5, I[:, :, 9] > .5, I[:, :, 10] > .5
    P = [tw & ts, tw & ~ts, ts & ~tw, ws & ~tw, ~tw & ~ts & ~ws]
    X = np.stack([(q & f).mean(1) for q in P for f in (F, ~F)], 1)
    XE = np.stack([(q & f & E).mean(1) for q in P for f in (F, ~F)], 1)  # labelled: error mass per cell (scoring/diagnosis only)
    FS = (1 - I[:, :, 2]) > c["q0"]; FT = I[:, :, 21] > .5  # source uncertain (clean max-F1 threshold); Tent uncertain (recalibrated threshold)
    C40 = [q & (F == a) & (FS == b_) & (FT == d_) for q in P for a in (True, False) for b_ in (True, False) for d_ in (True, False)]
    X40 = np.stack([q.mean(1) for q in C40], 1); XE40 = np.stack([(q & E).mean(1) for q in C40], 1)
    flag = F | ~tw
    b = dict(flag=flag.mean(1), twF=F.mean(1), dis=(~tw).mean(1), errT=I[:, :, 17].mean(1), errW=I[:, :, 18].mean(1), errS=I[:, :, 19].mean(1),
             rel=I[:, :, 21].mean(1), pro=I[:, :, 22].mean(1), atc=(I[:, :, 0] < c["t_atc"]).mean(1), confT=I[:, :, 0].mean(1), confW=I[:, :, 1].mean(1), confS=I[:, :, 2].mean(1),
             dd=I[:, :, 16].mean(1), agTS=ts.mean(1), agTW=tw.mean(1), agWS=ws.mean(1), kl=I[:, :, 11].mean(1), klS=I[:, :, 12].mean(1), entT=I[:, :, 5].mean(1), entW=I[:, :, 6].mean(1), entS=I[:, :, 7].mean(1),
             marT=I[:, :, 3].mean(1), marW=I[:, :, 4].mean(1), false_flag=(flag & ~E).mean(1), hidden=(E & ~flag).mean(1),
             bn=B[:, :5].mean(1), predH=B[:, 5], tv=B[:, 6], drift=B[:, 7])
    e = b["errT"]; m, l = e.mean(), e[-30:].mean()
    return dict(exp=exp, ds=c["ds"], model=c["model"], arm=c["arm"], split=split, cor=cor, sev=int(sev), prior=pr, rep=int(rep), c=c, T=I.shape[0], n=I.shape[1],
                strict=bool(m >= c["r0"] + .15 and l < .85), safe=bool(m < c["r0"] + .1 and l < .85), collapsed=bool(l >= .85), err=float(m),
                b={k: v.astype(np.float32) for k, v in b.items()}, X=X.astype(np.float32), XE=XE.astype(np.float32), X40=X40.astype(np.float32), XE40=XE40.astype(np.float32))
if __name__ == "__main__":
    jobs = []
    for exp, roots in ROOTS.items():
        for r in roots: jobs += [(exp, f) for f in sorted(glob.glob(f"{r}/*/*.npz") + glob.glob(f"{r}/*/*/*.npz")) if not f.endswith(".tmp.npz")]
    print(len(jobs), "files", flush=True)
    with Pool(6) as pool: S = pool.map(one, jobs, chunksize=16)
    pickle.dump(S, open(os.path.dirname(os.path.abspath(__file__)) + "/cache9.pkl", "wb"), protocol=4)
    from collections import Counter
    for k, v in sorted(Counter((s["exp"], s["ds"], s["arm"], s["split"]) for s in S).items()): print(k, v)

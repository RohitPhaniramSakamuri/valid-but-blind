"""Sequential-bound alarms as in exp004 (conjugate-mixture empirical Bernstein, alpha .15). Runs in the confseq environment."""
import glob, json, os
from multiprocessing import Pool
import numpy as np
from confseq.conjmix_bounded import conjmix_empbern_lower_cs
from confseq.predmix import predmix_empbern_lower_cs
ALPHA, AL1, TOL = .15, .025, .1
def v_opt(x, t):
    m = np.cumsum(x) / np.arange(1, len(x) + 1); return np.cumsum((x - np.append(.5, m[:-1])) ** 2)[t] * t
def first(z, L, level):
    x = np.clip(np.asarray(z, dtype=float), 0, 1)
    try: cs = np.asarray(conjmix_empbern_lower_cs(x=x, alpha=ALPHA, v_opt=v_opt(x, int(len(x) * .25))))
    except RuntimeError: cs = np.asarray(predmix_empbern_lower_cs(x=x, alpha=ALPHA))
    h = np.where(np.maximum(cs - L, 0) > level)[0]; return int(h[0]) + 1 if len(h) else None
def job(a):
    p, c = a; I = np.load(p)["img"].astype(np.float64); w = (np.log(2) - np.log(AL1)) / (2 * c["n"]); lv = c["r0"] + TOL
    agree, Ft = I[:, :, 8], I[:, :, 23]; twin = (Ft + (1 - Ft) * (1 - agree)).mean(1)
    return p, dict(released=first(I[:, :, 21].mean(1), c["fp0"] + w, lv), prototype=first(I[:, :, 22].mean(1), c["fpp0"] + w, lv), twin=first(twin, c["fpt"] + c["fnt"] + w, lv))
if __name__ == "__main__":
    J = []
    for d in glob.glob("*/streams_*"):
        c = json.load(open(d + "/calibration.json")); J += [(p, c) for p in glob.glob(d + "/*.npz")]
    with Pool(os.cpu_count()) as pool: R = dict(pool.map(job, J, chunksize=8))
    json.dump(R, open("cs.json", "w"))

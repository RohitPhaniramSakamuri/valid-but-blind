"""Experiment 004 confirmation, frozen before running. Uses final IDs and held-out families.

Calibration stays the same 1,000 clean development IDs. Streams use 4,000 final IDs on
weather and digital corruptions, severities 3 and 5, and clean images, 3 epochs at batch 100.

Arms: source, tent, eta (port of the repository's eata.py with FISHER_ALPHA 0,
entropy margin 0.4 ln 100, cosine margin 0.4, Adam lr 1e-3).
Kinds: balanced_wr (uniform with replacement, controls for repeats), by_class,
dirichlet at alpha 0.1 with two draws, plus alpha 0.5 and 1.0 at severity 5 and on clean.
"""
import json
import math
import os
import time

import numpy as np
import torch
import torch.nn.functional as F

import run as R
from run_monitor import BATCH, EPOCHS, load_clean, make_tent, max_f1, outputs, proxy_of, to_tensor

E_MARGIN, D_MARGIN = 0.4 * math.log(100), 0.4
CORRUPTIONS = R.FAMILIES["weather"] + R.FAMILIES["digital"]
OUT = "results_confirm"


def stream(kind, alpha, ids, labels, rng):
    total = EPOCHS * (len(ids) // BATCH)
    if kind == "by_class":
        seq = np.concatenate([ids[np.argsort(labels[ids], kind="stable")] for _ in range(EPOCHS)])
        return [seq[i * BATCH:(i + 1) * BATCH] for i in range(total)]
    p = np.full(100, 0.01) if kind == "balanced_wr" else rng.dirichlet(np.full(100, alpha))
    counts = np.bincount(labels[ids], minlength=100)
    w = p[labels[ids]] / counts[labels[ids]]
    w /= w.sum()
    return [rng.choice(ids, BATCH, replace=True, p=w) for _ in range(total)]


def main():
    device = "cuda"
    torch.backends.cudnn.benchmark = True
    os.makedirs(OUT, exist_ok=True)
    labels_all = np.load("data/CIFAR-100-C/labels.npy")[:10000].astype(np.int64)
    clean_x, clean_y = load_clean("data/cifar-100-python")
    if not (clean_y == labels_all).all():
        raise SystemExit("Clean labels do not match CIFAR-100-C labels")
    perm = np.random.RandomState(R.SPLIT_SEED).permutation(10000)
    calib_ids, stream_ids = perm[:1000], perm[5000:9000]
    images = {("clean", 0): torch.from_numpy(clean_x).to(device)}
    for c in CORRUPTIONS:
        arr = np.load(f"data/CIFAR-100-C/{c}.npy", mmap_mode="r")
        for s in R.SEVERITIES:
            images[(c, s)] = torch.from_numpy(np.array(arr[(s - 1) * 10000:s * 10000])).to(device)
    y_all = torch.from_numpy(labels_all).to(device)

    ckpt = "models/Hendrycks2020AugMix_ResNeXt.pt"
    source = R.load_model(ckpt, device, False).eval()
    for p in source.parameters():
        p.requires_grad_(False)
    cx, cy = to_tensor(clean_x[calib_ids], device), y_all[torch.from_numpy(calib_ids).to(device)]
    lg = outputs(source, cx)
    err0, prox0 = lg.argmax(1) != cy, proxy_of(lg)
    q0 = max_f1(err0, prox0, device)
    meta = dict(r0=float(err0.float().mean()), q_hat0=q0, false_alarm0=float(((prox0 > q0) & ~err0).float().mean()), n_calib=len(cy),
                stream_ids_sha=str(hash(stream_ids.tobytes())), torch=torch.__version__, gpu=torch.cuda.get_device_name(0))
    json.dump(meta, open(f"{OUT}/calibration.json", "w"), indent=1)
    print(meta, flush=True)

    model, params = make_tent(ckpt, device)
    init = [p.detach().clone() for p in params]

    plan = []
    base = [("balanced_wr", 0, 0), ("by_class", 0, 0), ("dirichlet", 0.1, 0), ("dirichlet", 0.1, 1)]
    extra = [("dirichlet", 0.5, 0), ("dirichlet", 1.0, 0)]
    for c in CORRUPTIONS:
        for s in R.SEVERITIES:
            for kind, alpha, rep in base + (extra if s == 5 else []):
                plan += [(arm, c, s, kind, alpha, rep) for arm in ("source", "tent", "eta")]
    for rep in range(3):
        for kind, alpha, _ in base[:3] + extra:
            plan += [(arm, "clean", 0, kind, alpha, rep) for arm in ("source", "tent", "eta")]

    path = f"{OUT}/streams.jsonl"
    done = {json.loads(l)["key"] for l in open(path)} if os.path.exists(path) else set()
    t0 = time.time()
    with open(path, "a") as out:
        for n, (arm, c, s, kind, alpha, rep) in enumerate(plan):
            key = f"{arm}/{c}/{s}/{kind}/{alpha}/{rep}"
            if key in done:
                continue
            rng = np.random.RandomState(R.seed_of("exp004-confirm", c, s, kind, alpha, rep))
            if arm != "source":
                with torch.no_grad():
                    for p, v in zip(params, init):
                        p.copy_(v)
                opt = torch.optim.Adam(params, lr=1e-3, betas=(0.9, 0.999), weight_decay=0.0)
            probs = None
            rec = {k: [] for k in ("err", "pos", "pfa", "pfn", "q_hat", "conf", "top_share", "disagree", "src_conf")}
            data = images[(c, s)]
            for b in stream(kind, alpha, stream_ids, labels_all, rng):
                idx = torch.from_numpy(b).to(device)
                x = data[idx].permute(0, 3, 1, 2).float().div_(255)
                y = y_all[idx]
                if arm == "source":
                    with torch.no_grad():
                        logits = source(x)
                    q = q0
                else:
                    logits = model(x)
                    ent = -(logits.softmax(1) * logits.log_softmax(1)).sum(1)
                    if arm == "tent":
                        loss = ent.mean()
                    else:
                        keep = ent < E_MARGIN
                        pr = logits.softmax(1)[keep].detach()
                        ent_k = ent[keep]
                        if probs is not None and len(pr):
                            sim = F.cosine_similarity(probs.unsqueeze(0), pr, dim=1)
                            fresh = sim.abs() < D_MARGIN
                            ent_k, pr = ent_k[fresh], pr[fresh]
                        if len(pr):
                            probs = pr.mean(0) if probs is None else 0.9 * probs + 0.1 * pr.mean(0)
                        coeff = 1 / torch.exp(ent_k.detach() - E_MARGIN)
                        loss = (ent_k * coeff).mean() if len(ent_k) else None
                    if loss is not None:
                        opt.zero_grad()
                        loss.backward()
                        opt.step()
                    logits = logits.detach()
                    l = outputs(model, cx)
                    q = max_f1(l.argmax(1) != cy, proxy_of(l), device)
                with torch.no_grad():
                    src = source(x) if arm != "source" else logits
                e, u = logits.argmax(1) != y, proxy_of(logits)
                rec["err"].append(float(e.float().mean()))
                rec["pos"].append(float((u > q).float().mean()))
                rec["pfa"].append(float(((u > q) & ~e).float().mean()))
                rec["pfn"].append(float(((u <= q) & e).float().mean()))
                rec["q_hat"].append(q)
                rec["conf"].append(float((1 - u).mean()))
                rec["top_share"].append(torch.bincount(logits.argmax(1), minlength=100).max().item() / len(y))
                rec["disagree"].append(float((logits.argmax(1) != src.argmax(1)).float().mean()))
                rec["src_conf"].append(float(src.softmax(1).max(1).values.mean()))
            out.write(json.dumps(dict(key=key, arm=arm, corruption=c, severity=s, kind=kind, alpha=alpha, rep=rep, **rec)) + "\n")
            out.flush()
            print(n + 1, len(plan), key, f"err={np.mean(rec['err']):.3f}", f"elapsed={time.time() - t0:.0f}s", flush=True)
    print("complete", f"{time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()

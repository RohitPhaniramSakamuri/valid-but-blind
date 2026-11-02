"""Experiment 004: per-batch monitor quantities on corrupted and class-skewed streams.

Ports the calibration and proxy logic of github.com/monasch/tta-monitor
(commit f200f00d4ca79567df0214bdd46150bb729c2227) with its CIFAR-100 Tent settings:
Adam, lr 1e-3, beta 0.9, batch statistics, batch size 100, max_class_prob proxy,
0-1 loss, max-F1 thresholds, calibration size 1000. The confidence sequence and alarm
are computed afterwards by analyze_monitor.py. Development IDs only.
"""
import argparse
import json
import os
import sys
import time

import numpy as np
import torch
import torch.nn as nn

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "2026-10-31-exp003"))
import run as R  # noqa: E402

BATCH, EPOCHS, DIR_ALPHA, EASY_K, EASY_MASS = 100, 3, 0.1, 20, 0.8
Q_HAT = torch.arange(0.001, 0.99, 0.001)
CORRUPTIONS = R.FAMILIES["noise"] + R.FAMILIES["blur"]


def to_tensor(arr, device):
    return torch.from_numpy(arr).permute(0, 3, 1, 2).float().div_(255).to(device)


def load_clean(root):
    import pickle
    with open(os.path.join(root, "test"), "rb") as f:
        d = pickle.load(f, encoding="latin1")
    return d["data"].reshape(-1, 3, 32, 32).transpose(0, 2, 3, 1), np.array(d["fine_labels"])


def max_f1(err, proxy, device):
    """Same choice as the repository's grid: first threshold with the largest F1."""
    grid = Q_HAT.to(device).view(-1, 1)
    pos = proxy.view(1, -1) > grid
    e = err.bool().view(1, -1)
    tp, fp, fn = (pos & e).sum(1).float(), (pos & ~e).sum(1).float(), (~pos & e).sum(1).float()
    return grid[(2 * tp / (2 * tp + fp + fn).clamp_min(1)).argmax()].item()


@torch.no_grad()
def outputs(model, x, chunk=1000):
    return torch.cat([model(x[i:i + chunk]) for i in range(0, len(x), chunk)])


def proxy_of(logits):
    return 1 - logits.softmax(1).max(1).values


def make_tent(ckpt, device):
    model = R.load_model(ckpt, device, False)
    model.requires_grad_(False)
    params = []
    for m in model.modules():
        if isinstance(m, nn.BatchNorm2d):
            m.requires_grad_(True)
            m.track_running_stats = False
            m.running_mean = None
            m.running_var = None
            params += [m.weight, m.bias]
    return model, params


def batches(kind, ids, labels, easy, rng):
    """Returns EPOCHS * len(ids) // BATCH index batches. Labels only build the stream."""
    total = EPOCHS * (len(ids) // BATCH)
    if kind == "balanced":
        seq = np.concatenate([rng.permutation(ids) for _ in range(EPOCHS)])
        return [seq[i * BATCH:(i + 1) * BATCH] for i in range(total)]
    if kind == "by_class":
        seq = np.concatenate([ids[np.argsort(labels[ids], kind="stable")] for _ in range(EPOCHS)])
        return [seq[i * BATCH:(i + 1) * BATCH] for i in range(total)]
    if kind == "dirichlet":
        p = rng.dirichlet(np.full(100, DIR_ALPHA))
    elif kind == "easy":
        p = np.full(100, (1 - EASY_MASS) / (100 - EASY_K))
        p[easy] = EASY_MASS / EASY_K
    weights = p[labels[ids]]
    counts = np.bincount(labels[ids], minlength=100)
    weights = weights / counts[labels[ids]]
    weights /= weights.sum()
    return [rng.choice(ids, BATCH, replace=True, p=weights) for _ in range(total)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data/CIFAR-100-C")
    ap.add_argument("--clean-dir", default="data/cifar-100-python")
    ap.add_argument("--ckpt", default="models/Hendrycks2020AugMix_ResNeXt.pt")
    ap.add_argument("--out", default="results_monitor")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()
    device = "cuda"
    torch.backends.cudnn.benchmark = True
    os.makedirs(args.out, exist_ok=True)

    data = R.Data(args.data_dir, False, device)
    clean_x, clean_y = load_clean(args.clean_dir)
    if not (clean_y == data.labels).all():
        raise SystemExit("Clean labels do not match CIFAR-100-C labels")
    dev = np.random.RandomState(R.SPLIT_SEED).permutation(10000)[:5000]
    calib_ids, stream_ids = dev[:1000], dev[1000:]
    labels = data.labels

    source = R.load_model(args.ckpt, device, False).eval()
    for p in source.parameters():
        p.requires_grad_(False)
    cx, cy = to_tensor(clean_x[calib_ids], device), torch.from_numpy(labels[calib_ids]).to(device)
    lg = outputs(source, cx)
    err0 = lg.argmax(1) != cy
    prox0 = proxy_of(lg)
    q0 = max_f1(err0, prox0, device)
    fa0 = float(((prox0 > q0) & ~err0).float().mean())
    fn0 = float(((prox0 <= q0) & err0).float().mean())
    per_class = np.array([float((~err0[cy == c]).float().mean()) if (cy == c).any() else 0.0 for c in range(100)])
    easy = np.argsort(-per_class, kind="stable")[:EASY_K]
    meta = dict(r0=float(err0.float().mean()), q_hat0=q0, false_alarm0=fa0, pfn0=fn0, n_calib=len(cy), easy=easy.tolist(),
                torch=torch.__version__, gpu=torch.cuda.get_device_name(0), batch=BATCH, epochs=EPOCHS)
    json.dump(meta, open(os.path.join(args.out, "calibration.json"), "w"), indent=1)
    print(meta, flush=True)

    tent, params = make_tent(args.ckpt, device)
    init = [p.detach().clone() for p in params]

    plan = []
    for c in CORRUPTIONS:
        for s in R.SEVERITIES:
            for kind in ("balanced", "dirichlet", "easy", "by_class"):
                plan += [("source", c, s, kind, 0), ("tent", c, s, kind, 0)]
    for rep in range(3):
        for kind in ("balanced", "dirichlet", "easy", "by_class"):
            plan += [("source", "clean", 0, kind, rep), ("tent", "clean", 0, kind, rep)]
    if args.limit:
        plan = plan[:args.limit]

    path = os.path.join(args.out, "streams.jsonl")
    done = {json.loads(l)["key"] for l in open(path)} if os.path.exists(path) else set()
    t0 = time.time()
    with open(path, "a") as out:
        for n, (arm, c, s, kind, rep) in enumerate(plan):
            key = f"{arm}/{c}/{s}/{kind}/{rep}"
            if key in done:
                continue
            rng = np.random.RandomState(R.seed_of("exp004", c, s, kind, rep))
            if arm == "tent":
                with torch.no_grad():
                    for p, v in zip(params, init):
                        p.copy_(v)
                opt = torch.optim.Adam(params, lr=1e-3, betas=(0.9, 0.999), weight_decay=0.0)
            rec = {k: [] for k in ("err", "pos", "pfa", "pfn", "q_hat", "conf", "top_share", "disagree")}
            for b in batches(kind, stream_ids, labels, easy, rng):
                if c == "clean":
                    x = to_tensor(clean_x[b], device)
                else:
                    x = data.images(c, s, b)
                y = torch.from_numpy(labels[b]).to(device)
                if arm == "tent":
                    logits = tent(x)
                    prob = logits.softmax(1)
                    loss = -(prob * logits.log_softmax(1)).sum(1).mean()
                    opt.zero_grad()
                    loss.backward()
                    opt.step()
                    logits = logits.detach()
                    q = max_f1(*(lambda l: (l.argmax(1) != cy, proxy_of(l)))(outputs(tent, cx)), device)
                else:
                    with torch.no_grad():
                        logits = source(x)
                    q = q0
                with torch.no_grad():
                    src_pred = source(x).argmax(1) if arm == "tent" else logits.argmax(1)
                e, u = logits.argmax(1) != y, proxy_of(logits)
                share = torch.bincount(logits.argmax(1), minlength=100).max().item() / len(y)
                rec["err"].append(float(e.float().mean()))
                rec["pos"].append(float((u > q).float().mean()))
                rec["pfa"].append(float(((u > q) & ~e).float().mean()))
                rec["pfn"].append(float(((u <= q) & e).float().mean()))
                rec["q_hat"].append(q)
                rec["conf"].append(float((1 - u).mean()))
                rec["top_share"].append(share)
                rec["disagree"].append(float((logits.argmax(1) != src_pred).float().mean()))
            out.write(json.dumps(dict(key=key, arm=arm, corruption=c, severity=s, kind=kind, rep=rep, **rec)) + "\n")
            out.flush()
            print(n + 1, len(plan), key, f"final_err={np.mean(rec['err']):.3f}", f"elapsed={time.time() - t0:.0f}s", flush=True)
    print("complete", f"{time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()

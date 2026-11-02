"""Experiment 003: collect branched action outcomes and evidence by adaptation exposure.

Writes one JSON line per state. Evaluator labels are only used for scores; no
evidence feature reads labels. Resumable: finished trajectories are skipped.
See ../../experiments/003-evidence-decay-under-adaptation.md.

ResNeXt architecture adapted from RobustBench/AugMix (MIT, Xuanyi Dong 2017);
strict state_dict loading confirms it matches the published checkpoint.
"""
import argparse
import hashlib
import json
import math
import os
import platform
import time
import zlib

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

FAMILIES = {
    "noise": ["gaussian_noise", "shot_noise", "impulse_noise"],
    "blur": ["defocus_blur", "glass_blur", "motion_blur", "zoom_blur"],
    "weather": ["snow", "frost", "fog", "brightness"],
    "digital": ["contrast", "elastic_transform", "pixelate", "jpeg_compression"],
}
FOLD_DEV = {1: ["noise", "blur"], 2: ["weather", "digital"]}
FOLD_FINAL = {1: ["weather", "digital"], 2: ["noise", "blur"]}
SPLIT_SEED = 20261031
BATCH = 64
EXPOSURES = (8, 32, 128)
SEVERITIES = (3, 5)
N_TRIPLES = 10
ACTIONS = ("KEEP", "NORMALIZE", "UPDATE", "RESET")
E0 = 0.4 * math.log(100)  # ETA-style reliability filter; this is not native ETA.


class Bottleneck(nn.Module):
    def __init__(self, inp, planes, card, width, stride=1, down=None):
        super().__init__()
        dim = int(math.floor(planes * (width / 64.0)))
        self.conv_reduce = nn.Conv2d(inp, dim * card, 1, 1, 0, bias=False)
        self.bn_reduce = nn.BatchNorm2d(dim * card)
        self.conv_conv = nn.Conv2d(dim * card, dim * card, 3, stride, 1, groups=card, bias=False)
        self.bn = nn.BatchNorm2d(dim * card)
        self.conv_expand = nn.Conv2d(dim * card, planes * 4, 1, 1, 0, bias=False)
        self.bn_expand = nn.BatchNorm2d(planes * 4)
        self.downsample = down

    def forward(self, x):
        y = F.relu(self.bn_reduce(self.conv_reduce(x)))
        y = F.relu(self.bn(self.conv_conv(y)))
        y = self.bn_expand(self.conv_expand(y))
        return F.relu((self.downsample(x) if self.downsample is not None else x) + y)


class ResNeXt29(nn.Module):
    def __init__(self, card=4, width=32, classes=100):
        super().__init__()
        self.card, self.width, self.inplanes = card, width, 64
        self.conv_1_3x3 = nn.Conv2d(3, 64, 3, 1, 1, bias=False)
        self.bn_1 = nn.BatchNorm2d(64)
        self.stage_1 = self._layer(64, 3, 1)
        self.stage_2 = self._layer(128, 3, 2)
        self.stage_3 = self._layer(256, 3, 2)
        self.avgpool = nn.AvgPool2d(8)
        self.classifier = nn.Linear(1024, classes)
        self.register_buffer("mu", torch.tensor([0.5] * 3).view(1, 3, 1, 1))
        self.register_buffer("sigma", torch.tensor([0.5] * 3).view(1, 3, 1, 1))

    def _layer(self, planes, blocks, stride):
        down = None
        if stride != 1 or self.inplanes != planes * 4:
            down = nn.Sequential(nn.Conv2d(self.inplanes, planes * 4, 1, stride, bias=False),
                                 nn.BatchNorm2d(planes * 4))
        layers = [Bottleneck(self.inplanes, planes, self.card, self.width, stride, down)]
        self.inplanes = planes * 4
        layers += [Bottleneck(self.inplanes, planes, self.card, self.width) for _ in range(1, blocks)]
        return nn.Sequential(*layers)

    def forward(self, x, feats=False):
        x = (x - self.mu) / self.sigma
        x = F.relu(self.bn_1(self.conv_1_3x3(x)))
        x = self.stage_3(self.stage_2(self.stage_1(x)))
        z = self.avgpool(x).flatten(1)
        logits = self.classifier(z)
        return (logits, z) if feats else logits


def load_model(path, device, smoke):
    model = ResNeXt29()
    if not smoke or os.path.exists(path):
        ck = torch.load(path, map_location="cpu", weights_only=True)
        sd = ck.get("state_dict", ck)
        sd = {k.replace("module.", ""): v for k, v in sd.items()}
        missing, unexpected = model.load_state_dict(sd, strict=False)
        allowed = {"mu", "sigma"}
        if set(missing) - allowed or unexpected:
            raise SystemExit(f"Checkpoint mismatch: {missing} {unexpected}")
    return model.to(device).eval()


class Data:
    """CIFAR-100-C reader. In smoke mode it returns random images and labels."""

    def __init__(self, root, smoke, device):
        self.root, self.smoke, self.device, self.arrays = root, smoke, device, {}
        if smoke:
            self.labels = np.random.RandomState(0).randint(0, 100, 10000)
            return
        labels = np.load(os.path.join(root, "labels.npy"))
        if len(labels) != 50000 or any((labels[i * 10000:(i + 1) * 10000] != labels[:10000]).any() for i in range(5)):
            raise SystemExit("Labels are not aligned across severities")
        self.labels = labels[:10000].astype(np.int64)

    def images(self, corruption, severity, ids):
        ids = np.asarray(ids)
        if self.smoke:
            arr = np.random.RandomState(zlib.crc32(corruption.encode()) % 2**31).randint(0, 255, (len(ids), 32, 32, 3), dtype=np.uint8)
        else:
            if corruption not in self.arrays:
                self.arrays[corruption] = np.load(os.path.join(self.root, corruption + ".npy"), mmap_mode="r")
            order = np.argsort(ids)
            arr = np.empty((len(ids), 32, 32, 3), dtype=np.uint8)
            arr[order] = self.arrays[corruption][(severity - 1) * 10000 + ids[order]]
        return torch.from_numpy(arr).permute(0, 3, 1, 2).float().div_(255).to(self.device, non_blocking=True)

    def targets(self, ids):
        return torch.from_numpy(self.labels[np.asarray(ids)]).to(self.device)


def split_pools(pool):
    perm = np.random.RandomState(SPLIT_SEED).permutation(10000)
    ids = perm[:5000] if pool == "dev" else perm[5000:]
    prefix, present = ids[:3000], ids[3000:]
    triples = [(present[i * 192:i * 192 + 64], present[i * 192 + 64:i * 192 + 128], present[i * 192 + 128:i * 192 + 192])
               for i in range(N_TRIPLES)]
    return prefix, triples


class Learner:
    """Holds the live model. Only BN parameters and buffers ever change."""

    def __init__(self, model):
        self.model = model
        self.bns = [m for m in model.modules() if isinstance(m, nn.BatchNorm2d)]
        for p in model.parameters():
            p.requires_grad_(False)
        self.params = [p for b in self.bns for p in (b.weight, b.bias)]
        self.tensors = [t for b in self.bns for t in (b.weight, b.bias, b.running_mean, b.running_var, b.num_batches_tracked)]
        self.source = self.snapshot()

    def snapshot(self):
        return [t.detach().clone() for t in self.tensors]

    @torch.no_grad()
    def restore(self, snap):
        for t, s in zip(self.tensors, snap):
            t.copy_(s)

    @torch.no_grad()
    def predict(self, x):
        return self.model(x, feats=True)

    @torch.no_grad()
    def normalize(self, x, alpha):
        for b in self.bns:
            b.train()
            b.momentum = alpha
        self.model(x)
        self.model.eval()

    def update(self, x, lr):
        """One entropy step on BN affine parameters; running statistics stay frozen."""
        for p in self.params:
            p.requires_grad_(True)
        prob = self.model(x).softmax(1)
        ent = -(prob * prob.clamp_min(1e-12).log()).sum(1)
        keep = ent < E0
        n = int(keep.sum())
        if n:
            grads = torch.autograd.grad(ent[keep].mean(), self.params)
            with torch.no_grad():
                for p, g in zip(self.params, grads):
                    p.add_(g, alpha=-lr)
        for p in self.params:
            p.requires_grad_(False)
        return n

    @torch.no_grad()
    def drift(self):
        total = 0.0
        for t, s in zip(self.tensors, self.source):
            if t.is_floating_point():
                total += float((t - s).pow(2).sum())
        return math.sqrt(total)

    def apply(self, action, x, cfg):
        if action == "NORMALIZE":
            self.normalize(x, cfg["alpha"])
        elif action == "UPDATE":
            return self.update(x, cfg["lr"])
        elif action == "RESET":
            self.restore(self.source)
        return None


def output_stats(logits):
    prob = logits.softmax(1)
    ent = -(prob * prob.clamp_min(1e-12).log()).sum(1)
    top2 = prob.topk(2, dim=1).values
    share = torch.bincount(prob.argmax(1), minlength=100).float() / len(prob)
    return {"ent_mean": ent.mean(), "ent_std": ent.std(), "conf_mean": top2[:, 0].mean(),
            "margin_mean": (top2[:, 0] - top2[:, 1]).mean(), "top_share": share.max(),
            "pred_entropy": -(share * share.clamp_min(1e-12).log()).sum()}


def geometry_stats(z, logits, classifier):
    pred = logits.argmax(1)
    centers = torch.stack([z[pred == c].mean(0) for c in pred.unique()])
    within = (z - z.mean(0)).pow(2).sum(1).mean()
    assigned = z - centers[torch.searchsorted(pred.unique(), pred)]
    between = (centers - centers.mean(0)).pow(2).sum(1).mean() if len(centers) > 1 else torch.tensor(0.0, device=z.device)
    align = F.cosine_similarity(z, classifier.weight[pred], dim=1).mean()
    return {"norm_mean": z.norm(dim=1).mean(), "dim_std": z.std(0).mean(), "total_var": within,
            "within_var": assigned.pow(2).sum(1).mean(), "between_var": between, "classifier_align": align}


def evidence(prefix, logits, z, classifier):
    out = {**output_stats(logits), **geometry_stats(z, logits, classifier)}
    return {f"{prefix}_{k}": float(v) for k, v in out.items()}


def score(learner, x, y):
    """Scores query and fresh together; BN is frozen so joint batching changes nothing."""
    logits, _ = learner.predict(x)
    wrong = (logits.argmax(1) != y).float()
    ce = F.cross_entropy(logits, y, reduction="none")
    share = torch.bincount(logits[:BATCH].argmax(1), minlength=100).float().max() / BATCH
    return dict(err_q=float(wrong[:BATCH].mean()), err_f=float(wrong[BATCH:].mean()),
                ce_q=float(ce[:BATCH].mean()), ce_f=float(ce[BATCH:].mean()), top_share_q=float(share))


def eval_state(learner, data, corruption, severity, triples, cfg, source_cache, meta):
    snap = learner.snapshot()
    rows = []
    classifier = learner.model.classifier
    for ti, (sup, qry, fresh) in enumerate(triples):
        xs = data.images(corruption, severity, sup)
        ids = np.concatenate([qry, fresh])
        xq, yq = data.images(corruption, severity, ids), data.targets(ids)
        key = (corruption, severity, ti)
        if key not in source_cache:
            learner.restore(learner.source)
            lg, z = learner.predict(xs)
            source_cache[key] = (lg.cpu(), evidence("S", lg, z, classifier), score(learner, xq, yq))
            learner.restore(snap)
        src_logits, src_ev, src_score = source_cache[key]
        lg, z = learner.predict(xs)
        src_logits = src_logits.to(lg.device)
        logp_s, logp_l = src_logits.log_softmax(1), lg.log_softmax(1)
        row = {**meta, "triple": ti, **src_ev, **evidence("L", lg, z, classifier),
               "X_disagree": float((src_logits.argmax(1) != lg.argmax(1)).float().mean()),
               "X_kl": float(F.kl_div(logp_l, logp_s, log_target=True, reduction="batchmean")),
               "drift": learner.drift(), "source": src_score, "actions": {}}
        for action in ACTIONS:
            learner.restore(snap)
            used = learner.apply(action, xs, cfg)
            result = score(learner, xq, yq)
            result["n_filtered"] = used
            row["actions"][action] = result
        learner.restore(snap)
        rows.append(row)
    return rows


def prefix_corruptions(corruption, relation, dev_families):
    family = next(f for f in dev_families if corruption in FAMILIES[f])
    if relation == "same":
        return [c for c in FAMILIES[family] if c != corruption]
    other = next(f for f in dev_families if f != family)
    return list(FAMILIES[other])


def run_prefix(learner, data, rng, ids, corruptions, severity, policy, cfg, steps, state):
    """Advances `steps` prefix batches. RESET is excluded: it would erase exposure."""
    for _ in range(steps):
        if state["pos"] + BATCH > len(state["order"]):
            state["order"], state["pos"] = rng.permutation(ids), 0
            state["epoch"] += 1
        batch = state["order"][state["pos"]:state["pos"] + BATCH]
        state["pos"] += BATCH
        x = data.images(corruptions[state["epoch"] % len(corruptions)], severity, batch)
        action = "UPDATE" if policy == "update" else ("KEEP", "NORMALIZE", "UPDATE")[rng.randint(3)]
        learner.apply(action, x, cfg)
        state["counts"][action] += 1


def seed_of(*parts):
    return zlib.crc32("|".join(map(str, parts)).encode()) % 2**31


def tune(args, learner, data, prefix_ids, triples, dev_families, path):
    """Development-only choice of alpha and learning rate, using severity 5."""
    corruptions = [c for f in dev_families for c in FAMILIES[f]]
    if args.smoke:
        corruptions = corruptions[:1]
    subset = triples[:3]
    def err():
        total = []
        for c in corruptions_now:
            for _, q, f in subset:
                ids = np.concatenate([q, f])
                total.append(score(learner, data.images(c, 5, ids), data.targets(ids))["err_q"])
        return float(np.mean(total))
    result = {"alpha": {}, "lr": {}}
    for alpha in (0.1, 0.3, 1.0):
        vals = []
        for c in corruptions:
            for s, q, f in subset:
                learner.restore(learner.source)
                learner.normalize(data.images(c, 5, s), alpha)
                ids = np.concatenate([q, f])
                vals.append(score(learner, data.images(c, 5, ids), data.targets(ids))["err_q"])
        result["alpha"][str(alpha)] = float(np.mean(vals))
    source_err = {}
    for c in corruptions:
        learner.restore(learner.source)
        corruptions_now = [c]
        source_err[c] = err()
    steps = 4 if args.smoke else 128
    for lr in (1e-4, 1e-3, 1e-2, 1e-1):
        cfg = {"lr": lr, "alpha": 1.0}
        per = {}
        for c in corruptions:
            learner.restore(learner.source)
            rng = np.random.RandomState(seed_of("tune", c, lr))
            state = dict(order=rng.permutation(prefix_ids), pos=0, epoch=0, counts=dict(KEEP=0, NORMALIZE=0, UPDATE=0))
            run_prefix(learner, data, rng, prefix_ids, prefix_corruptions(c, "same", dev_families), 5, "update", cfg, steps, state)
            corruptions_now = [c]
            per[c] = err()
        result["lr"][str(lr)] = dict(mean_err=float(np.mean(list(per.values()))),
                                     worst_excess=float(max(per[c] - source_err[c] for c in per)))
    learner.restore(learner.source)
    safe = {k: v for k, v in result["lr"].items() if v["worst_excess"] <= 0.05}
    pool = safe or result["lr"]
    result["chosen"] = dict(alpha=float(min(result["alpha"], key=result["alpha"].get)),
                            lr=float(min(pool, key=lambda k: pool[k]["mean_err"])), any_safe_lr=bool(safe))
    result["source_err"] = source_err
    with open(path, "w") as f:
        json.dump(result, f, indent=2)
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data/CIFAR-100-C")
    ap.add_argument("--ckpt", default="models/Hendrycks2020AugMix_ResNeXt.pt")
    ap.add_argument("--out", default="results")
    ap.add_argument("--fold", type=int, default=1, choices=[1, 2])
    ap.add_argument("--pool", default="dev", choices=["dev", "final"])
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--freeze-file", help="Required for --pool final: frozen development manifest")
    ap.add_argument("--smoke", action="store_true", help="Random images, tiny scale; checks the code path only")
    args = ap.parse_args()
    if args.pool == "final" and not (args.freeze_file and os.path.exists(args.freeze_file)):
        raise SystemExit("The final pool needs a frozen manifest.")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    if device == "cuda":
        torch.backends.cudnn.benchmark = True
    torch.manual_seed(args.seed)
    os.makedirs(args.out, exist_ok=True)
    tag = f"fold{args.fold}_{args.pool}_seed{args.seed}" + ("_smoke" if args.smoke else "")
    data = Data(args.data_dir, args.smoke, device)
    learner = Learner(load_model(args.ckpt, device, args.smoke))
    prefix_ids, triples = split_pools(args.pool)
    dev_families = FOLD_DEV[args.fold]
    tune_path = os.path.join(args.out, f"tune_fold{args.fold}" + ("_smoke" if args.smoke else "") + ".json")
    if not os.path.exists(tune_path):
        if args.pool != "dev":
            raise SystemExit("Tune on the development pool first.")
        _, dev_triples = split_pools("dev")
        t0 = time.time()
        tuned = tune(args, learner, data, split_pools("dev")[0], dev_triples, dev_families, tune_path)
        print("tuned", tuned["chosen"], f"{time.time() - t0:.0f}s", flush=True)
    cfg = json.load(open(tune_path))["chosen"]

    families = FOLD_DEV[args.fold] if args.pool == "dev" else FOLD_FINAL[args.fold]
    corruptions = [c for f in families for c in FAMILIES[f]]
    severities, exposures, use_triples = SEVERITIES, EXPOSURES, triples
    if args.smoke:
        corruptions, severities, exposures, use_triples = corruptions[:1], (5,), (2, 4), triples[:2]

    manifest = dict(args=vars(args), cfg=cfg, device=device, torch=torch.__version__, python=platform.python_version(),
                    gpu=torch.cuda.get_device_name(0) if device == "cuda" else None,
                    ckpt_sha256=hashlib.sha256(open(args.ckpt, "rb").read()).hexdigest() if os.path.exists(args.ckpt) else None,
                    split_seed=SPLIT_SEED, e0=E0, exposures=exposures, severities=severities)
    json.dump(manifest, open(os.path.join(args.out, tag + ".manifest.json"), "w"), indent=2)

    path = os.path.join(args.out, tag + ".jsonl")
    done_path = path + ".done"
    done = set(open(done_path).read().split()) if os.path.exists(done_path) else set()
    source_cache = {}
    t0 = time.time()
    with open(path, "a") as out:
        def emit(key, rows):
            out.write("".join(json.dumps(r) + "\n" for r in rows))
            out.flush()
            with open(done_path, "a") as d:
                d.write(key + "\n")
            print(key, f"elapsed={time.time() - t0:.0f}s", flush=True)

        for c in corruptions:
            for s in severities:
                key = f"{c}/{s}/none/none"
                if key not in done:
                    learner.restore(learner.source)
                    meta = dict(corruption=c, severity=s, relation="none", policy="none", k=0, seed=args.seed, counts=dict(KEEP=0, NORMALIZE=0, UPDATE=0))
                    emit(key, eval_state(learner, data, c, s, use_triples, cfg, source_cache, meta))
                for relation in ("same", "different"):
                    for policy in ("update", "random"):
                        key = f"{c}/{s}/{relation}/{policy}"
                        if key in done:
                            continue
                        learner.restore(learner.source)
                        rng = np.random.RandomState(seed_of(args.seed, args.fold, args.pool, key))
                        state = dict(order=rng.permutation(prefix_ids), pos=0, epoch=0, counts=dict(KEEP=0, NORMALIZE=0, UPDATE=0))
                        names = prefix_corruptions(c, relation, families)
                        rows, reached = [], 0
                        for k in exposures:
                            run_prefix(learner, data, rng, prefix_ids, names, s, policy, cfg, k - reached, state)
                            reached = k
                            meta = dict(corruption=c, severity=s, relation=relation, policy=policy, k=k, seed=args.seed, counts=dict(state["counts"]))
                            rows += eval_state(learner, data, c, s, use_triples, cfg, source_cache, meta)
                        emit(key, rows)
    print("complete", tag, f"{time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()

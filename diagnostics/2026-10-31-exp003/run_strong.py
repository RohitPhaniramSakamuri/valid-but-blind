"""Exploratory stronger-adaptation check for Experiment 003.

Designed after the H0 gate failed, so nothing here can pass that gate.
Development pool only. Differences from run.py:
- NORMALIZE blends statistics with alpha 0.1, so history persists.
- An "adapt" prefix applies NORMALIZE then UPDATE on every batch.
- Learning rate: the largest of {2e-4, 3e-4, 5e-4} whose worst development corruption
  stays within 5 pp of source after 128 adapt steps at severity 5; 2e-4 if none does.
- "change" streams score the query on a different corruption from the support batch.
"""
import argparse
import json
import os
import time

import numpy as np
import torch
import torch.nn.functional as F

import run as R

ALPHA = 0.1
LRS = (2e-4, 3e-4, 5e-4)


def next_corruption(c):
    noise, blur = R.FAMILIES["noise"], R.FAMILIES["blur"]
    return blur[noise.index(c)] if c in noise else noise[blur.index(c) % len(noise)]


def advance(learner, data, rng, ids, names, severity, policy, cfg, steps, state):
    for _ in range(steps):
        if state["pos"] + R.BATCH > len(state["order"]):
            state["order"], state["pos"] = rng.permutation(ids), 0
            state["epoch"] += 1
        batch = state["order"][state["pos"]:state["pos"] + R.BATCH]
        state["pos"] += R.BATCH
        x = data.images(names[state["epoch"] % len(names)], severity, batch)
        if policy == "adapt":
            learner.normalize(x, cfg["alpha"])
            learner.update(x, cfg["lr"])
            state["counts"]["NORMALIZE"] += 1
            state["counts"]["UPDATE"] += 1
        else:
            action = ("KEEP", "NORMALIZE", "UPDATE")[rng.randint(3)]
            learner.apply(action, x, cfg)
            state["counts"][action] += 1


def eval_state(learner, data, c_support, c_query, stream, severity, triples, cfg, cache, meta):
    snap = learner.snapshot()
    rows, clf = [], learner.model.classifier
    for ti, (sup, qry, fresh) in enumerate(triples):
        xs = data.images(c_support, severity, sup)
        ids = np.concatenate([qry, fresh])
        xq, yq = data.images(c_query, severity, ids), data.targets(ids)
        key = (c_support, c_query, severity, ti)
        if key not in cache:
            learner.restore(learner.source)
            lg, z = learner.predict(xs)
            cache[key] = (lg.cpu(), R.evidence("S", lg, z, clf), R.score(learner, xq, yq))
            learner.restore(snap)
        src_lg, src_ev, src_score = cache[key]
        lg, z = learner.predict(xs)
        src_lg = src_lg.to(lg.device)
        row = {**meta, "stream": stream, "triple": ti, **src_ev, **R.evidence("L", lg, z, clf),
               "X_disagree": float((src_lg.argmax(1) != lg.argmax(1)).float().mean()),
               "X_kl": float(F.kl_div(lg.log_softmax(1), src_lg.log_softmax(1), log_target=True, reduction="batchmean")),
               "drift": learner.drift(), "source": src_score, "actions": {}}
        for action in R.ACTIONS:
            learner.restore(snap)
            used = learner.apply(action, xs, cfg)
            result = R.score(learner, xq, yq)
            result["n_filtered"] = used
            row["actions"][action] = result
        learner.restore(snap)
        rows.append(row)
    return rows


def tune(learner, data, prefix_ids, triples, families, path):
    corruptions = [c for f in families for c in R.FAMILIES[f]]
    out = {}
    def err(c):
        vals = []
        for _, q, f in triples[:3]:
            ids = np.concatenate([q, f])
            vals.append(R.score(learner, data.images(c, 5, ids), data.targets(ids))["err_q"])
        return float(np.mean(vals))
    learner.restore(learner.source)
    source = {c: err(c) for c in corruptions}
    for lr in LRS:
        per = {}
        cfg = dict(alpha=ALPHA, lr=lr)
        for c in corruptions:
            learner.restore(learner.source)
            rng = np.random.RandomState(R.seed_of("strong-tune", c, lr))
            state = dict(order=rng.permutation(prefix_ids), pos=0, epoch=0, counts=dict(KEEP=0, NORMALIZE=0, UPDATE=0))
            advance(learner, data, rng, prefix_ids, R.prefix_corruptions(c, "same", families), 5, "adapt", cfg, 128, state)
            per[c] = err(c)
        out[str(lr)] = dict(mean_err=float(np.mean(list(per.values()))), worst_excess=float(max(per[c] - source[c] for c in per)),
                            drift=learner.drift())
    learner.restore(learner.source)
    safe = [lr for lr in LRS if out[str(lr)]["worst_excess"] <= 0.05]
    chosen = dict(alpha=ALPHA, lr=float(max(safe)) if safe else LRS[0], any_safe_lr=bool(safe))
    json.dump(dict(grid=out, chosen=chosen, source_err=source), open(path, "w"), indent=2)
    return chosen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data/CIFAR-100-C")
    ap.add_argument("--ckpt", default="models/Hendrycks2020AugMix_ResNeXt.pt")
    ap.add_argument("--out", default="results_strong")
    ap.add_argument("--seed", type=int, default=1)
    args = ap.parse_args()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    torch.backends.cudnn.benchmark = True
    torch.manual_seed(args.seed)
    os.makedirs(args.out, exist_ok=True)
    data = R.Data(args.data_dir, False, device)
    learner = R.Learner(R.load_model(args.ckpt, device, False))
    prefix_ids, triples = R.split_pools("dev")
    families = R.FOLD_DEV[1]
    t0 = time.time()
    cfg = tune(learner, data, prefix_ids, triples, families, os.path.join(args.out, "tune.json"))
    print("tuned", cfg, f"{time.time() - t0:.0f}s", flush=True)
    json.dump(dict(args=vars(args), cfg=cfg, torch=torch.__version__, gpu=torch.cuda.get_device_name(0), status="exploratory, post-hoc"),
              open(os.path.join(args.out, "manifest.json"), "w"), indent=2)
    cache, new = {}, lambda: dict(KEEP=0, NORMALIZE=0, UPDATE=0)
    with open(os.path.join(args.out, "rows.jsonl"), "w") as out:
        for c in [c for f in families for c in R.FAMILIES[f]]:
            q2 = next_corruption(c)
            for s in R.SEVERITIES:
                def both(meta):
                    for stream, cq in (("stationary", c), ("change", q2)):
                        rows = eval_state(learner, data, c, cq, stream, s, triples, cfg, cache, meta)
                        out.write("".join(json.dumps(r) + "\n" for r in rows))
                    out.flush()
                learner.restore(learner.source)
                both(dict(corruption=c, severity=s, relation="none", policy="none", k=0, seed=args.seed, counts=new()))
                for relation in ("same", "different"):
                    for policy in ("adapt", "random"):
                        key = f"{c}/{s}/{relation}/{policy}"
                        learner.restore(learner.source)
                        rng = np.random.RandomState(R.seed_of("strong", args.seed, key))
                        state = dict(order=rng.permutation(prefix_ids), pos=0, epoch=0, counts=new())
                        names, reached = R.prefix_corruptions(c, relation, families), 0
                        for k in R.EXPOSURES:
                            advance(learner, data, rng, prefix_ids, names, s, policy, cfg, k - reached, state)
                            reached = k
                            both(dict(corruption=c, severity=s, relation=relation, policy=policy, k=k, seed=args.seed, counts=dict(state["counts"])))
                        print(key, f"elapsed={time.time() - t0:.0f}s", flush=True)
    print("complete", f"{time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()

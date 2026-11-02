"""Experiment 003 analysis. Written before any real outcome was seen.

Gate H0: cross-fit headroom. The oracle picks an action on the query block and is
scored on the disjoint fresh block (and vice versa), which removes the optimism of
picking and scoring on the same 64 images. Headroom = best fixed action's error
minus that oracle's error, in percentage points.

H1-H3 on development data are exploratory: leave-one-corruption-out ridge
predictors, selecting on predicted query error and scoring on the fresh block.
"""
import argparse
import json
from collections import defaultdict

import numpy as np

ACTIONS = ("KEEP", "NORMALIZE", "UPDATE", "RESET")
EV = ["ent_mean", "ent_std", "conf_mean", "margin_mean", "top_share", "pred_entropy"]
GEO = ["norm_mean", "dim_std", "total_var", "within_var", "between_var", "classifier_align"]
SETS = {
    "S": [f"S_{n}" for n in EV + GEO],
    "L-opt": [f"L_{n}" for n in EV],
    "L-other": [f"L_{n}" for n in GEO],
    "X": ["X_disagree", "X_kl"],
}
SETS["All"] = sum(SETS.values(), [])
RIDGE = 10.0
NBOOT = 2000
HEADROOM_GATE = 1.0
COLLAPSE_MARGIN = 0.05
COLLAPSE_SHARE = 0.5


def load(paths):
    rows = [json.loads(l) for p in paths for l in open(p)]
    for r in rows:
        r["q"] = np.array([r["actions"][a]["err_q"] for a in ACTIONS])
        r["f"] = np.array([r["actions"][a]["err_f"] for a in ACTIONS])
        keep = r["actions"]["KEEP"]
        src = r["source"]
        r["noncollapsed"] = ((keep["err_q"] + keep["err_f"]) / 2 <= (src["err_q"] + src["err_f"]) / 2 + COLLAPSE_MARGIN
                             and keep["top_share_q"] < COLLAPSE_SHARE)
        r["cell"] = (r["corruption"], r["severity"])
    return rows


def crossfit_oracle(q, f):
    """Mean error when the choice is made on one block and scored on the other."""
    n = np.arange(len(q))
    return (f[n, q.argmin(1)] + q[n, f.argmin(1)]) / 2


def headroom_stats(rows, rng):
    if not rows:
        return None
    q, f = np.stack([r["q"] for r in rows]), np.stack([r["f"] for r in rows])
    mean = (q + f) / 2
    fixed = int(mean.mean(0).argmin())
    per_row = mean[:, fixed] - crossfit_oracle(q, f)
    naive = (mean[:, fixed] - (q.min(1) + f.min(1)) / 2).mean()
    # Two-way bootstrap: corruption/severity cells and image triples are crossed.
    cells = sorted({r["cell"] for r in rows})
    triples = sorted({r["triple"] for r in rows})
    groups = defaultdict(list)
    for i, r in enumerate(rows):
        groups[(r["cell"], r["triple"])].append(i)
    boots = []
    for _ in range(NBOOT):
        cs = [cells[i] for i in rng.randint(len(cells), size=len(cells))]
        ts = [triples[i] for i in rng.randint(len(triples), size=len(triples))]
        idx = [i for c in cs for t in ts for i in groups.get((c, t), [])]
        if idx:
            boots.append(per_row[idx].mean())
    lo, hi = np.percentile(boots, [2.5, 97.5])
    return dict(n=len(rows), best_fixed=ACTIONS[fixed], action_err_pct={a: round(100 * float(mean[:, i].mean()), 2) for i, a in enumerate(ACTIONS)},
                headroom_pp=round(100 * float(per_row.mean()), 2), ci95_pp=[round(100 * float(lo), 2), round(100 * float(hi), 2)],
                naive_headroom_pp=round(100 * float(naive), 2))


def ridge_fit(X, Y):
    mu, sd = X.mean(0), X.std(0) + 1e-8
    Z = (X - mu) / sd
    w = np.linalg.solve(Z.T @ Z + RIDGE * np.eye(Z.shape[1]), Z.T @ (Y - Y.mean(0)))
    return lambda A: ((A - mu) / sd) @ w + Y.mean(0)


def selection(rows, names, train_filter, n_train, seed, with_k=False):
    """Leave-one-corruption-out selection; returns (k, row index, fresh error) lists."""
    rng = np.random.RandomState(seed)
    feats = lambda rs: np.array([[r[n] for n in names] + ([np.log1p(r["k"])] if with_k else []) for r in rs])
    results = defaultdict(list)
    for held in sorted({r["corruption"] for r in rows}):
        train = [r for r in rows if r["corruption"] != held and train_filter(r)]
        test = [r for r in rows if r["corruption"] == held]
        if n_train and len(train) > n_train:
            train = [train[i] for i in rng.choice(len(train), n_train, replace=False)]
        predict = ridge_fit(feats(train), np.stack([r["q"] for r in train]))
        for r, p in zip(test, predict(feats(test))):
            results[r["k"]].append(r["f"][int(p.argmin())] - crossfit_single(r))
    return {k: float(np.mean(v)) * 100 for k, v in sorted(results.items())}


def crossfit_single(r):
    return (r["f"][r["q"].argmin()] + r["q"][r["f"].argmin()]) / 2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    rows = load(args.paths)
    rng = np.random.RandomState(0)
    report = dict(n_rows=len(rows), gate={}, by_k={}, by_policy={}, noncollapsed_share={})
    # Filter hit-rates tell us whether UPDATE acted at all.
    report["update_filter_mean_kept"] = float(np.mean([r["actions"]["UPDATE"]["n_filtered"] for r in rows]))
    for k in sorted({r["k"] for r in rows}):
        sub = [r for r in rows if r["k"] == k]
        report["by_k"][str(k)] = dict(all=headroom_stats(sub, rng), noncollapsed=headroom_stats([r for r in sub if r["noncollapsed"]], rng))
        report["noncollapsed_share"][str(k)] = float(np.mean([r["noncollapsed"] for r in sub]))
    for p in ("update", "random"):
        for k in (8, 32, 128):
            sub = [r for r in rows if r["k"] == k and r["policy"] == p]
            report["by_policy"][f"{p}/k{k}"] = headroom_stats([r for r in sub if r["noncollapsed"]], rng)
    late = [r for r in rows if r["k"] >= 32 and r["noncollapsed"]]
    gate = headroom_stats(late, rng)
    report["gate"] = dict(rule=f"cross-fit headroom >= {HEADROOM_GATE} pp at k>=32 on noncollapsed states", result=gate,
                          passed=bool(gate and gate["headroom_pp"] >= HEADROOM_GATE))

    # Exploratory H1-H3. Low-exposure training uses k<=8, because at k=0 KEEP and RESET coincide.
    low = lambda r: r["k"] <= 8
    n_low = sum(low(r) for r in rows)
    report["exploratory_excess_error_pp"] = {}
    for name, cols in SETS.items():
        report["exploratory_excess_error_pp"][name] = dict(
            low_exposure=selection(rows, cols, low, None, 1),
            all_exposure_matched=selection(rows, cols, lambda r: True, n_low, 1),
            all_exposure_matched_plus_k=selection(rows, cols, lambda r: True, n_low, 1, with_k=True))
    with open(args.out, "w") as f:
        json.dump(report, f, indent=2)
    print(json.dumps(dict(gate=report["gate"], noncollapsed=report["noncollapsed_share"]), indent=1))
    print(json.dumps(report["exploratory_excess_error_pp"], indent=1))


if __name__ == "__main__":
    main()

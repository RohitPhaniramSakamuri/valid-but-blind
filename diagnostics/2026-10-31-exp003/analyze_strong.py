"""Exploratory analysis of run_strong.py. Written before its data existed.

Reports, by stream and exposure: action errors, cross-fit headroom, whether exposure
really changed the model, whether evidence still tracks error (the thermometer test),
and selector excess error for low-exposure versus all-exposure training.
"""
import argparse
import json

import numpy as np

import analyze as A


def corr(a, b):
    a, b = np.asarray(a), np.asarray(b)
    return float(np.corrcoef(a, b)[0, 1]) if len(a) > 2 and a.std() > 0 and b.std() > 0 else None


def tracking(rows):
    """Within-cell correlation of evidence with KEEP error, removing corruption/severity means."""
    keep_err = np.array([(r["actions"]["KEEP"]["err_q"] + r["actions"]["KEEP"]["err_f"]) / 2 for r in rows])
    out = {}
    cells = sorted({r["cell"] for r in rows})
    for name in ("L_ent_mean", "L_conf_mean", "L_classifier_align", "L_between_var", "S_ent_mean", "X_disagree"):
        v = np.array([r[name] for r in rows])
        vc, ec = v.copy(), keep_err.copy()
        for c in cells:
            m = np.array([r["cell"] == c for r in rows])
            vc[m] -= vc[m].mean()
            ec[m] -= ec[m].mean()
        out[name] = dict(pooled=corr(v, keep_err), within_cell=corr(vc, ec))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    rows = A.load(args.paths)
    rng = np.random.RandomState(0)
    report = {}
    for stream in ("stationary", "change"):
        sub = [r for r in rows if r["stream"] == stream]
        late = [r for r in sub if r["k"] >= 32 and r["noncollapsed"]]
        block = dict(late_noncollapsed=A.headroom_stats(late, rng), late_all=A.headroom_stats([r for r in sub if r["k"] >= 32], rng), by_group={})
        for policy, ks in (("none", (0,)), ("adapt", A_KS), ("random", A_KS)):
            for k in ks:
                g = [r for r in sub if r["policy"] == policy and r["k"] == k]
                n = [r for r in g if r["noncollapsed"]]
                block["by_group"][f"{policy}/k{k}"] = dict(
                    all=A.headroom_stats(g, rng),
                    noncollapsed_share=round(float(np.mean([r["noncollapsed"] for r in g])), 3),
                    noncollapsed_headroom=(A.headroom_stats(n, rng) or {}).get("headroom_pp"),
                    drift=round(float(np.mean([r["drift"] for r in g])), 3),
                    disagree_with_source=round(float(np.mean([r["X_disagree"] for r in g])), 3),
                    live_entropy=round(float(np.mean([r["L_ent_mean"] for r in g])), 3),
                    source_entropy=round(float(np.mean([r["S_ent_mean"] for r in g])), 3),
                    live_conf=round(float(np.mean([r["L_conf_mean"] for r in g])), 3),
                    source_err=round(100 * float(np.mean([(r["source"]["err_q"] + r["source"]["err_f"]) / 2 for r in g])), 2),
                    tracking=tracking(g))
        low = lambda r: r["k"] <= 8
        n_low = sum(low(r) for r in sub)
        block["selector_excess_pp"] = {
            name: dict(low=A.selection(sub, cols, low, None, 1), all_matched=A.selection(sub, cols, lambda r: True, n_low, 1))
            for name, cols in A.SETS.items()}
        adapt = [r for r in sub if r["policy"] in ("none", "adapt")]
        n_low2 = sum(low(r) for r in adapt)
        block["selector_excess_pp_adapt_only"] = {
            name: dict(low=A.selection(adapt, cols, low, None, 1), all_matched=A.selection(adapt, cols, lambda r: True, n_low2, 1))
            for name, cols in A.SETS.items()}
        report[stream] = block
    json.dump(report, open(args.out, "w"), indent=1)
    print("written", args.out, len(rows))


A_KS = (8, 32, 128)
if __name__ == "__main__":
    main()

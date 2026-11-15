"""Builds figures/level_time.pdf from the exp009 cache (saved exp008 streams; no model is run). Run from the paper folder with:
uv run --no-project --with matplotlib --with "numpy<2" python make_figures_level.py"""
import sys
sys.path.insert(0, "../diagnostics/2026-11-14-exp009-level-transfer")
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from lib9 import load, groups, simple, conformal, IDX
plt.rcParams.update({"font.family": "serif", "font.size": 8, "axes.spines.top": False, "axes.spines.right": False, "pdf.fonttype": 42, "axes.edgecolor": "#52514e", "xtick.color": "#52514e", "ytick.color": "#0b0b0b"})
S = load(); G = groups(S, "tent0.001"); x = IDX + 1
panels = [(("exp008", "organc", "organc", "tent0.001"), "OrganCMNIST"), (("exp008", "cifar", "Addepalli2022Efficient_WRN_34_10", "tent0.001"), "CIFAR-100-C, WRN-34-10")]
fig, axes = plt.subplots(1, 2, figsize=(4.8, 2.1), sharex=True)
for ax, (g, title) in zip(axes, panels):
    L = G[g]; A = np.stack([simple("doc")(s) for s in L]); dev = np.array([s["split"] == "dev" for s in L]); safe = np.array([s["safe"] for s in L]); strict = np.array([s["strict"] for s in L])
    lv = conformal(A[dev & safe].max(1))
    ax.fill_between(x, np.quantile(A[dev & safe], .05, 0), np.quantile(A[dev & safe], .95, 0), color="#2a78d6", alpha=.18, lw=0, label="Safe development streams, 5–95%")
    ax.plot(x, np.quantile(A[dev & safe], .95, 0), color="#2a78d6", lw=1.2)
    ax.plot(x, np.quantile(A[~dev & strict], .5, 0), color="#eb6834", lw=1.4, label="Held-out failing streams, median")
    ax.plot(x, np.quantile(A[~dev & strict], .1, 0), color="#eb6834", lw=1, ls=":", label="Held-out failing streams, 10th pct.")
    ax.axhline(lv, color="#52514e", lw=1, ls="--", label="Constant level")
    ax.set_title(title, fontsize=8); ax.set_xlabel("Batch of read-out"); ax.tick_params(length=2)
axes[0].set_ylabel("Confidence drop (DoC)")
h, l = axes[0].get_legend_handles_labels(); fig.legend(h, l, ncol=2, frameon=False, loc="lower center", bbox_to_anchor=(.5, .98), handletextpad=.4, columnspacing=1.2)
fig.tight_layout(); fig.savefig("figures/level_time.pdf", bbox_inches="tight")

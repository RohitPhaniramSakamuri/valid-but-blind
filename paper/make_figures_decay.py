"""Builds figures/decay.pdf from the frozen exp010 report. Run from the paper folder with:
uv run --no-project --with matplotlib --with "numpy<2" python make_figures_decay.py"""
import json, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.family": "serif", "font.size": 8, "axes.spines.top": False, "axes.spines.right": False, "pdf.fonttype": 42, "axes.edgecolor": "#52514e", "xtick.color": "#52514e", "ytick.color": "#0b0b0b"})
c = json.load(open("../diagnostics/2026-11-14-exp010-confirm/results/report10.json"))["coupling"]; x = [10, 30, 50, 70, 90, 110]
fig, ax = plt.subplots(figsize=(4.4, 2.3))
for arm, lab, col, mk in (("tent0.001", "Entropy (Tent)", "#eb6834", "^"), ("pl0.001", "Pseudo-labels", "#eda100", "D"), ("im0.001", "Information maximization", "#8a5cd6", "v")):
    ax.plot(x, c[arm]["auroc_by_window"]["T"], color=col, marker=mk, ms=4, lw=1.4, label=lab)
ax.plot(x, c["tent0.001"]["auroc_by_window"]["W"], color="#1baf7a", marker="s", ms=4, lw=1.4, label="BN-only twin")
ax.plot(x, c["tent0.001"]["auroc_by_window"]["S"], color="#2a78d6", marker="o", ms=4, lw=1.4, label="Frozen source")
ax.axhline(.5, color="#b5b3ac", lw=.8, ls=":"); ax.set_ylim(.45, 1.02); ax.set_xlabel("Batches into the stream (20-batch windows)"); ax.set_ylabel("AUROC, failing vs. safe streams")
ax.tick_params(length=2); ax.legend(ncol=2, frameon=False, loc="lower center", bbox_to_anchor=(.5, 1), handletextpad=.4, columnspacing=1.2)
fig.savefig("figures/decay.pdf", bbox_inches="tight")

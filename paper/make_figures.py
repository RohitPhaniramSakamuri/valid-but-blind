"""Builds figures/*.pdf from the frozen report and the exploratory split. Run from the paper folder with:
uv run --no-project --with matplotlib --with numpy python make_figures.py"""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
M = "../diagnostics/2026-11-01-exp004-mechanism/"
rep = json.load(open(M + "factorial_report.json"))["report"]
split = json.load(open(M + "explore_masses.json"))["forms"]
plt.rcParams.update({"font.family": "serif", "font.size": 8, "axes.spines.top": False, "axes.spines.right": False, "pdf.fonttype": 42, "axes.edgecolor": "#52514e", "xtick.color": "#52514e", "ytick.color": "#0b0b0b"})
names = {"Hendrycks2020AugMix_ResNeXt": "AugMix ResNeXt", "Hendrycks2020AugMix_WRN": "AugMix WRN-40-2", "Modas2021PRIMEResNet18": "PRIME ResNet-18", "Addepalli2021Towards_PARN18": "Addepalli PARN-18", "Addepalli2021Towards_WRN34": "Addepalli WRN-34", "Addepalli2022Efficient_WRN_34_10": "Addepalli WRN-34-10"}
order = list(names)[::-1]
series = [("Frozen source", rep["q1"], "b", "#2a78d6", "o"), ("BN only", rep["q2"], "b", "#1baf7a", "s"), ("Tent, recalibrated", rep["q2"], "a", "#eb6834", "^"), ("Tent, fixed threshold", rep["q1"], "a", "#eda100", "D")]
fig, ax = plt.subplots(figsize=(4.7, 2.5))
for i in range(len(order)):
    ax.axhline(i, color="#e5e4df", lw=.6, zorder=0)
for j, (lab, q, side, col, mk) in enumerate(series):
    xs = [100 * q["per"][m][side][0] / q["per"][m][side][1] for m in order]
    ax.scatter(xs, [i + (j - 1.5) * .15 for i in range(len(order))], s=26, c=col, marker=mk, edgecolors="white", linewidths=.5, label=lab, zorder=3)
ax.set_yticks(range(len(order)), [names[m] for m in order])
ax.set_xlim(-3, 103)
ax.set_xlabel("Strict violations with no alarm (%)")
ax.tick_params(length=0)
ax.legend(ncol=2, frameon=False, loc="lower center", bbox_to_anchor=(.42, 1), handletextpad=.1, columnspacing=1)
fig.savefig("figures/missed_by_model.pdf", bbox_inches="tight")
split["sar/recal"] = json.load(open("../diagnostics/2026-11-02-exp004-sar/sar_report.json"))["report"]["split"]["sar/recal"]
rows = [("source/fixed", "Frozen source"), ("bn/recal", "BN only, recalibrated"), ("sar/recal", "SAR, recalibrated"), ("tent1e-4/recal", "Tent $10^{-4}$, recalibrated"), ("tent1e-3/recal", "Tent $10^{-3}$, recalibrated"), ("tent1e-3/fixed", "Tent $10^{-3}$, fixed")][::-1]
parts = [("flagged_wrong", "Wrong, flagged", "#2a78d6", ""), ("unflagged_wrong", "Wrong, not flagged", "#eb6834", "///"), ("flagged_correct", "Correct, flagged", "#1baf7a", "")]
fig, ax = plt.subplots(figsize=(4.7, 2.2))
for i, (k, _) in enumerate(rows):
    x = 0
    for p, lab, col, h in parts:
        v = split[k][p]
        ax.barh(i, v, left=x, height=.62, color=col, hatch=h, edgecolor="white", linewidth=1.2, label=lab if i == 0 else None)
        ax.text(x + v / 2, i, f"{v:.2f}", ha="center", va="center", fontsize=6.5, color="#0b0b0b", bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=.85))
        x += v
ax.set_yticks(range(len(rows)), [r[1] for r in rows])
ax.set_xlabel("Share of all predictions, mean over strict streams")
ax.tick_params(length=0)
ax.legend(ncol=3, frameon=False, loc="lower center", bbox_to_anchor=(.3, 1), handletextpad=.3, columnspacing=1)
fig.savefig("figures/error_split.pdf", bbox_inches="tight")

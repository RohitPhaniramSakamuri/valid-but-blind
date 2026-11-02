"""Experiment 004, confidence-dependence test. Frozen before any new model ran.

PREDICTION: on corrupted Dirichlet 0.1 streams, Tent's missed share of strict violations rises with
Tent's mean confidence. A model is scored only with at least 5 strict violations.

Verdict across the new models only (the first two models suggested the prediction):
INCONCLUSIVE if fewer than 3 new models are scored, or their confidence range is under 0.15.
SUPPORTED if all hold:
  P1. Spearman(confidence, missed share) >= 0.8 across new models.
  P2. Spearman >= 0.7 across all scored models, including the first two (descriptive inputs).
  P3. Every new scored model with confidence >= 0.85 misses at least 75%, and every one with
      confidence <= 0.65 misses at most 60%.
Otherwise NOT SUPPORTED. With so few models this is a coarse check, not a precise estimate.
"""
import json
import sys

from scipy.stats import spearmanr

NEW = sys.argv[1:]
OLD = {"AugMix_ResNeXt": "results_confirm_copy", "PRIME_ResNet18": "results_second_copy"}


def row(path):
    r = json.load(open(f"{path}/analysis.json"))["report"]
    t = r["table"]
    p = r["primary"]
    src = t.get("source/corrupted/dirichlet/0.1", {})
    bc = r["control"]
    return dict(conf=p["conf"], err=p["err"], pos=p["pos"], strict=p["strict"], missed=p["missed"], missed_sqrt=p["missed_sqrt"],
                share=p["missed"] / p["strict"] if p["strict"] else None, collapsed=p["collapsed"], asm=p["asm"], final_bound=p["final_bound"],
                source_strict=src.get("strict"), source_missed=src.get("missed"), source_conf=src.get("conf"), source_err=src.get("err"),
                by_class_strict=bc["strict"], by_class_missed=bc["missed"], by_class_collapsed=bc["collapsed"], replacement_gap=r["checks"]["replacement_gap"], others_alarmed=p["others_alarmed"], others=p["others"])


models = {}
for n in NEW:
    models[n] = dict(new=True, **row(f"results_{n}"))
for n, path in OLD.items():
    models[n] = dict(new=False, **row(path))
scored = {k: v for k, v in models.items() if v["strict"] >= 5}
new = {k: v for k, v in scored.items() if v["new"]}


def rho(group):
    c, s = [v["conf"] for v in group.values()], [v["share"] for v in group.values()]
    return float(spearmanr(c, s).statistic) if len(set(c)) > 1 and len(set(s)) > 1 else None


span = max(v["conf"] for v in new.values()) - min(v["conf"] for v in new.values()) if new else 0
p1, p2 = rho(new), rho(scored)
p3 = all((v["conf"] < 0.85 or v["share"] >= 0.75) and (v["conf"] > 0.65 or v["share"] <= 0.60) for v in new.values())
if len(new) < 3 or span < 0.15:
    verdict = "INCONCLUSIVE"
elif p1 is not None and p1 >= 0.8 and p2 is not None and p2 >= 0.7 and p3:
    verdict = "SUPPORTED"
else:
    verdict = "NOT SUPPORTED"
out = dict(verdict=verdict, rho_new=p1, rho_all=p2, p3=p3, new_conf_range=span, models=models)
json.dump(out, open("models_report.json", "w"), indent=1)
print(json.dumps(out, indent=0))

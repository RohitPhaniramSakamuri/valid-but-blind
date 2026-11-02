"""How much post-change selector error could any selector avoid? Saved data only; exploratory.

All numbers are excess error (pp) over the cross-fit oracle: choices use query-block
errors or evidence, and scores use the fresh block. Comparators, weakest to strongest:

- fixed: best single action from other corruptions.
- history table: best action per (policy, k, severity, relation), learned on other
  corruptions. It uses history metadata and no image evidence.
- context table: as above plus support and query corruption, learned on other image
  triples. It knows the next corruption, so it is an upper bound on evidence value.
- ridge and random forest on All evidence, learned on other corruptions.
- ridge trained on stationary rows, tested on change rows: a selector unaware of changes.
- disagreement rule: RESET if source-live disagreement exceeds a learned threshold, else KEEP.
"""
import json
from collections import defaultdict

import numpy as np
from sklearn.ensemble import RandomForestRegressor

import analyze as A

KS = (0, 8, 32, 128)
ACT = {a: i for i, a in enumerate(A.ACTIONS)}
rows = A.load(["results_strong/rows.jsonl"])
for r in rows:
    r["excess_base"] = A.crossfit_single(r)
change = [r for r in rows if r["stream"] == "change"]
stationary = [r for r in rows if r["stream"] == "stationary"]
ALL = A.SETS["All"]


def X(rs):
    return np.array([[r[n] for n in ALL] + [np.log1p(r["k"])] for r in rs])


def excess(items):
    """items: (row, chosen action index)."""
    by = defaultdict(list)
    for r, a in items:
        by[r["k"]].append(r["f"][a] - r["excess_base"])
    return {k: round(100 * float(np.mean(by[k])), 2) for k in KS}


def table(train, test, key):
    sums = defaultdict(lambda: np.zeros(4))
    for r in train:
        sums[key(r)] += r["q"]
    overall = np.mean([r["q"] for r in train], axis=0)
    return [(r, int(sums[key(r)].argmin()) if key(r) in sums else int(overall.argmin())) for r in test]


def loco(rs, choose):
    out = []
    for c in sorted({r["corruption"] for r in rs}):
        out += choose([r for r in rs if r["corruption"] != c], [r for r in rs if r["corruption"] == c])
    return out


def model_choice(train, test, make):
    m = make().fit(X(train), np.stack([r["q"] for r in train]))
    return [(r, int(p.argmin())) for r, p in zip(test, m.predict(X(test)))]


class Ridge:
    def fit(self, x, y):
        self.predict = A.ridge_fit(x, y)
        return self


def disagreement(train, test):
    grid = np.unique(np.quantile([r["X_disagree"] for r in train], np.linspace(0, 1, 41)))
    errs = [np.mean([r["q"][ACT["RESET"] if r["X_disagree"] > t else ACT["KEEP"]] for r in train]) for t in grid]
    t = grid[int(np.argmin(errs))]
    return [(r, ACT["RESET"] if r["X_disagree"] > t else ACT["KEEP"]) for r in test]


hist = lambda r: (r["policy"], r["k"], r["severity"], r["relation"])
hist_runtime = lambda r: (r["policy"], r["k"], r["severity"])
ctx = lambda r: (r["corruption"], r["severity"], r["relation"], r["policy"], r["k"])


def by_triple(rs):
    out = []
    for t in sorted({r["triple"] for r in rs}):
        out += table([r for r in rs if r["triple"] != t], [r for r in rs if r["triple"] == t], ctx)
    return out


def forest():
    return RandomForestRegressor(n_estimators=200, min_samples_leaf=5, max_features=0.5, n_jobs=4, random_state=0)


def fixed(train, test):
    a = int(np.mean([r["q"] for r in train], axis=0).argmin())
    return [(r, a) for r in test]


report = {}
for name, rs in (("change", change), ("stationary", stationary)):
    report[name] = dict(
        fixed=excess(loco(rs, fixed)),
        always_reset=excess([(r, ACT["RESET"]) for r in rs]),
        always_keep=excess([(r, ACT["KEEP"]) for r in rs]),
        disagreement_rule=excess(loco(rs, disagreement)),
        history_table_with_relation=excess(loco(rs, lambda a, b: table(a, b, hist))),
        history_table_runtime=excess(loco(rs, lambda a, b: table(a, b, hist_runtime))),
        context_table_knows_next=excess(by_triple(rs)),
        ridge_all=excess(loco(rs, lambda a, b: model_choice(a, b, Ridge))),
        forest_all=excess(loco(rs, lambda a, b: model_choice(a, b, forest))),
    )


def stationary_to_change(train, test):
    held = {r["corruption"] for r in test}
    return model_choice([r for r in stationary if r["corruption"] not in held], test, Ridge)


report["change"]["ridge_trained_on_stationary"] = excess(loco(change, stationary_to_change))

# Does the same state's reset benefit carry from stationary to change queries?
pairs = {}
for r in stationary:
    pairs[(r["corruption"], r["severity"], r["relation"], r["policy"], r["k"], r["triple"])] = r
gain = lambda r: (r["q"][ACT["KEEP"]] + r["f"][ACT["KEEP"]] - r["q"][ACT["RESET"]] - r["f"][ACT["RESET"]]) / 2
report["reset_benefit_stationary_vs_change"] = {}
for k in (8, 32, 128):
    a, b = [], []
    for r in change:
        if r["k"] == k:
            a.append(gain(pairs[(r["corruption"], r["severity"], r["relation"], r["policy"], r["k"], r["triple"])]))
            b.append(gain(r))
    a, b = np.array(a), np.array(b)
    report["reset_benefit_stationary_vs_change"][k] = dict(corr=round(float(np.corrcoef(a, b)[0, 1]), 3),
                                                            mean_stationary_pp=round(100 * float(a.mean()), 2),
                                                            mean_change_pp=round(100 * float(b.mean()), 2),
                                                            same_sign_share=round(float((np.sign(a) == np.sign(b)).mean()), 3))

# Entropy flip: separate prefix relation from everything else (adapt prefix, k = 128).
report["entropy_vs_keep_error_k128_adapt"] = {}
for stream, rs in (("stationary", stationary), ("change", change)):
    for rel in ("same", "different"):
        g = [r for r in rs if r["k"] == 128 and r["policy"] == "adapt" and r["relation"] == rel]
        v = np.array([r["L_ent_mean"] for r in g])
        e = np.array([(r["actions"]["KEEP"]["err_q"] + r["actions"]["KEEP"]["err_f"]) / 2 for r in g])
        for c in {r["cell"] for r in g}:
            m = np.array([r["cell"] == c for r in g])
            v[m] -= v[m].mean()
            e[m] -= e[m].mean()
        report["entropy_vs_keep_error_k128_adapt"][f"{stream}/{rel}"] = round(float(np.corrcoef(v, e)[0, 1]), 3)

json.dump(report, open("results_strong/analysis_change.json", "w"), indent=1)
print(json.dumps(report, indent=0))

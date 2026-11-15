"""Exploratory, after all frozen verdicts; enters no rule. Saved results only. Where does the blind spot appear, by image degradation?"""
import json
from collections import defaultdict

F = dict(gaussian_noise="noise", shot_noise="noise", impulse_noise="noise", defocus_blur="blur", glass_blur="blur", motion_blur="blur", zoom_blur="blur", snow="weather", frost="weather", fog="weather", brightness="weather", contrast="digital", elastic_transform="digital", pixelate="digital", jpeg_compression="digital")


def tab(rows, group):
    t = defaultdict(lambda: [0, 0])
    for key, missed in rows:
        k = group(key)
        t[k][1] += 1
        t[k][0] += int(missed)
    return {k: v for k, v in t.items()}


out = {}
rep = json.load(open("factorial_report.json"))["rows"]
for name, arm, form in (("source", "source", "fixed"), ("bn", "bn", "recal"), ("tent", "tent1e-3", "recal"), ("tent_fixed", "tent1e-3", "fixed")):
    g = [r for r in rep if r["arm"] == arm and r["strict"]]
    rows = [(r["key"].split("/"), not r[f"alarm_{form}"]) for r in g]
    out[f"factorial/{name}"] = dict(by_corruption=tab(rows, lambda k: k[1]), by_severity=tab(rows, lambda k: k[2]), by_family=tab(rows, lambda k: F[k[1]]))
tw = json.load(open("../2026-11-02-exp004-twin/twin_report.json"))["rows"]
g = [r for r in tw if r["split"] == "held" and r["kind"] == "dirichlet" and r["strict"]]
rows = [(r["key"].split("/"), not r["a1.0_1"]) for r in g]
out["held/twin"] = dict(by_corruption=tab([(k, m) for k, m in rows], lambda k: k[2]), by_severity=tab(rows, lambda k: k[3]))
d = [r for r in tw if r["split"] == "dev" and r["kind"] == "dirichlet" and r["strict"]]
out["dev/twin"] = dict(by_family=tab([(r["key"].split("/"), not r["a1.0_1"]) for r in d], lambda k: F[k[2]]))
json.dump(out, open("explore_by_corruption.json", "w"), indent=1)
fmt = lambda d: {k: f"{v[0]}/{v[1]}" for k, v in sorted(d.items())}
for k, v in out.items():
    for a, b in v.items():
        print(k, a, fmt(b))

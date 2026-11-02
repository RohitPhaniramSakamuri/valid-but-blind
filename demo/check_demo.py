"""One-off check: runs paper streams through the live demo server and compares them with recorded GPU runs."""
import json, time, urllib.request
import numpy as np
U = "http://127.0.0.1:8765"
REC = {(x["key"]): x for x in json.load(open("../diagnostics/2026-11-02-exp004-twin/twin_report.json"))["rows"] if x["model"] == "Hendrycks2020AugMix_WRN"}
BASE = {x["key"]: x for x in json.load(open("../diagnostics/2026-11-01-exp004-mechanism/factorial_report.json"))["rows"] if x["model"] == "Hendrycks2020AugMix_WRN" and x["arm"] == "tent1e-3"}
SAVED = {json.loads(l)["key"]: json.loads(l) for l in open("../diagnostics/2026-11-02-exp004-twin/results_twin_Hendrycks2020AugMix_WRN/streams.jsonl")}
out = []
for c, s, d, recal in (("frost", 5, 0, 1), ("frost", 5, 0, 5), ("fog", 3, 1, 5), ("frost", 3, 1, 5)):
    body = json.dumps(dict(model="Hendrycks2020AugMix_WRN", corruption=c, severity=s, kind="dirichlet", draw=d, lr="0.001", recal=str(recal))).encode()
    urllib.request.urlopen(urllib.request.Request(U + "/api/start", data=body, method="POST"))
    time.sleep(5)
    t0 = time.time(); B = []
    while True:
        st = json.load(urllib.request.urlopen(f"{U}/api/state?since={len(B)}"))
        B += st["batches"]
        if st["status"] in ("finished", "error"):
            break
        time.sleep(3)
    k = f"held/dirichlet/{c}/{s}/{d}"
    live = np.array([b["err"] for b in B])
    saved = np.sum(np.asarray(SAVED[k]["cells"])[4:8], axis=0)
    r = dict(stream=k, recal=recal, status=st["status"], msg=st["message"], seconds=round(time.time() - t0), per_batch=round(float(np.mean([b["sec"]["total"] for b in B])), 2), err_live=round(float(live.mean()), 4), err_recorded=round(float(saved.mean()), 4), max_batch_err_diff=round(float(np.abs(live - saved).max()), 3), twin_live=B[-1]["alarm_t"], twin_recorded=REC[k]["t1.0_1"], released_live=B[-1]["alarm_r"], released_recorded=BASE[f"tent1e-3/{c}/{s}/dirichlet/0.1/{d}"]["alarm_recal"], final_br=round(B[-1]["br"], 3), final_bt=round(B[-1]["bt"], 3), level=round(st["info"]["level"], 3))
    out.append(r); print(r, flush=True)
    json.dump(out, open("check_results.json", "w"), indent=1)

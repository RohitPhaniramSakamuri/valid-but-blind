"""Saves one live run to recorded_run.json for the backup replay."""
import json, time, urllib.request
U = "http://127.0.0.1:8765"
urllib.request.urlopen(urllib.request.Request(U + "/api/start", data=json.dumps(dict(model="Hendrycks2020AugMix_WRN", corruption="frost", severity=5, kind="dirichlet", draw=0, lr="0.001", recal="5")).encode(), method="POST"))
B, s = [], {}
while True:
    s = json.load(urllib.request.urlopen(f"{U}/api/state?since={len(B)}"))
    B += s["batches"]
    if s["status"] in ("finished", "error"):
        break
    time.sleep(2)
json.dump(dict(info=s["info"], batches=B), open("recorded_run.json", "w"))
print(s["status"], len(B), B[-1]["alarm_r"], B[-1]["alarm_t"], flush=True)

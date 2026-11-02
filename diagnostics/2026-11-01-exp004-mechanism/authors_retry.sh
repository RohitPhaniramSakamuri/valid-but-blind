#!/usr/bin/env bash
# Tmux session "authors3". Reruns authors' streams that wrote no row (GPU out-of-memory with 4 concurrent ResNeXt processes), with fewer processes per pass.
cd /root/exp004
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
while tmux has-session -t authors2 2>/dev/null; do sleep 20; done
cd tta-monitor
for p in 3 2 1; do
  ../.venv_cs/bin/python - > ../authors_missing.txt <<'PY'
import json, os
for a in ("Hendrycks2020AugMix_ResNeXt", "Hendrycks2020AugMix_WRN"):
    f = f"../authors_{a}.jsonl"
    done = {json.loads(l)["key"] for l in open(f)} if os.path.exists(f) else set()
    for arm in ("tent", "source"):
        for c in "gaussian_noise shot_noise impulse_noise defocus_blur glass_blur motion_blur zoom_blur".split():
            for s in (3, 5):
                for d in (0, 1):
                    if f"{arm}/{c}/{s}/dirichlet/0.1/{d}" not in done:
                        print(a, arm, c, s, d)
PY
  echo "pass P=$p missing $(wc -l < ../authors_missing.txt) $(date -u)" >> ../authors_progress3.log
  [ -s ../authors_missing.txt ] || break
  xargs -P $p -L 1 sh -c '../.venv_auth/bin/python ../authors_stream.py "$0" "$1" "$2" "$3" "$4" >/dev/null 2>>../authors_err.log; echo "authors $0 $1 $2 $3 $4 exit $?" >> ../authors_progress3.log' < ../authors_missing.txt
done
cd ..
.venv_cs/bin/python analyze_all.py > analysis.log 2>&1
echo "=== RETRY DONE" >> mech.log

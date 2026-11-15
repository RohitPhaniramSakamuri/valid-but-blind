#!/usr/bin/env bash
# Tmux session "derma". uv environments only. One process per arm on one GPU.
set -uo pipefail
cd /root/exp004
export PATH="$HOME/.local/bin:$PATH" OMP_NUM_THREADS=2 MKL_NUM_THREADS=2
command -v uv >/dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv --system-site-packages --python "$(command -v python3)" .venv
uv venv --python 3.10 .venv_cs
uv pip install --python .venv_cs/bin/python -q confseq scipy "numpy<2"
OMP_NUM_THREADS=8 .venv/bin/python prepare_derma.py 2>&1 | tee prepare.log
grep -q "PREPARE DONE" prepare.log || { echo "=== PREPARE FAILED"; exit 1; }
echo "=== SETUP DONE"
pids=()
for a in source bn tent1e-3 tent5e-3 sar; do
  .venv/bin/python run_derma.py "$a" > "derma_$a.log" 2>&1 &
  pids+=($!)
done
for p in "${pids[@]}"; do wait "$p" || echo "process $p failed"; done
echo "=== STREAMS DONE"
.venv_cs/bin/python analyze_derma.py > analysis.log 2>&1 || tail -20 analysis.log
echo "=== ALL DONE"

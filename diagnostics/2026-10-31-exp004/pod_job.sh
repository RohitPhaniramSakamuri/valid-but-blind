#!/usr/bin/env bash
# Runs on the RunPod pod inside tmux session "exp004". Development IDs only.
# confseq does not build on Python 3.11 (old pybind11), so analysis uses a separate 3.10 venv.
set -euo pipefail
cd /root/exp003
export PATH="$HOME/.local/bin:$PATH"
if [ ! -f data/cifar-100-python/test ]; then
  wget -q https://www.cs.toronto.edu/~kriz/cifar-100-python.tar.gz -O data/cifar-100-python.tar.gz
  sha256sum data/cifar-100-python.tar.gz | tee data/cifar-100-python.sha256
  tar -xzf data/cifar-100-python.tar.gz -C data && rm data/cifar-100-python.tar.gz
fi
[ -d .venv_cs ] || uv venv --python 3.10 .venv_cs
uv pip install --python .venv_cs/bin/python "numpy<2"; .venv_cs/bin/python -c "import confseq" 2>/dev/null || uv pip install --python .venv_cs/bin/python confseq scipy "numpy<2"
.venv_cs/bin/python -c "from confseq.conjmix_bounded import conjmix_empbern_lower_cs; print('confseq ok')"
echo "=== streams"
.venv/bin/python run_monitor.py
.venv_cs/bin/python analyze_monitor.py
echo "=== EXP004 DONE"

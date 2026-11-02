#!/usr/bin/env bash
# Runs on a new RunPod pod in tmux session "confirm". Downloads run in parallel to reduce paid time.
set -uo pipefail
cd /root/exp004
export PATH="$HOME/.local/bin:$PATH"
mkdir -p data
if [ ! -f data/CIFAR-100-C/labels.npy ]; then
  wget -q https://zenodo.org/records/3555552/files/CIFAR-100-C.tar -O data/CIFAR-100-C.tar &
  P1=$!
fi
if [ ! -f data/cifar-100-python/test ]; then
  wget -q https://www.cs.toronto.edu/~kriz/cifar-100-python.tar.gz -O data/cifar-100-python.tar.gz &
  P2=$!
fi
set -e
command -v uv >/dev/null || { curl -LsSf https://astral.sh/uv/install.sh | sh; export PATH="$HOME/.local/bin:$PATH"; }
[ -d .venv ] || uv venv --system-site-packages --python "$(command -v python3)" .venv
[ -d .venv_cs ] || uv venv --python 3.10 .venv_cs
uv pip install --python .venv_cs/bin/python confseq scipy "numpy<2"
.venv_cs/bin/python -c "from confseq.conjmix_bounded import conjmix_empbern_lower_cs; print('confseq ok')"
[ -z "${P1:-}" ] || { wait "$P1"; sha256sum data/CIFAR-100-C.tar | tee data/CIFAR-100-C.sha256; tar -xf data/CIFAR-100-C.tar -C data; rm data/CIFAR-100-C.tar; }
[ -z "${P2:-}" ] || { wait "$P2"; sha256sum data/cifar-100-python.tar.gz | tee data/cifar.sha256; tar -xzf data/cifar-100-python.tar.gz -C data; rm data/cifar-100-python.tar.gz; }
echo "=== streams"
.venv/bin/python run_confirm.py
.venv_cs/bin/python analyze_confirm.py
echo "=== CONFIRM DONE"

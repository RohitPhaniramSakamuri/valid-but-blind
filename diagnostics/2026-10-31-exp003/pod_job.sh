#!/usr/bin/env bash
# Runs on the RunPod pod inside tmux session "exp003". Development pool only.
set -euo pipefail
cd /root/exp003
command -v uv >/dev/null || { curl -LsSf https://astral.sh/uv/install.sh | sh; export PATH="$HOME/.local/bin:$PATH"; }
[ -d .venv ] || uv venv --system-site-packages --python "$(command -v python3)" .venv
PY=.venv/bin/python
"$PY" -c "import torch,numpy;print('torch',torch.__version__,'numpy',numpy.__version__,'cuda',torch.cuda.is_available(),torch.cuda.get_device_name(0))"
mkdir -p data
if [ ! -f data/CIFAR-100-C/labels.npy ]; then
  echo "downloading CIFAR-100-C"
  wget -q -c https://zenodo.org/records/3555552/files/CIFAR-100-C.tar -O data/CIFAR-100-C.tar
  sha256sum data/CIFAR-100-C.tar | tee data/CIFAR-100-C.tar.sha256
  tar -xf data/CIFAR-100-C.tar -C data
  rm data/CIFAR-100-C.tar
fi
echo "=== code-path check on random images"
"$PY" run.py --smoke --out results_smoke
echo "=== fold 1, development pool, seed 1"
"$PY" run.py --fold 1 --pool dev --seed 1 --out results
"$PY" analyze.py results/fold1_dev_seed1.jsonl --out results/analysis_fold1_dev_seed1.json
echo "=== JOB DONE"

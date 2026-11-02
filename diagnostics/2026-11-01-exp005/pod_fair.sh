#!/usr/bin/env bash
# Runs on a RunPod pod in tmux session "fair".
set -euo pipefail
cd /root/exp005
export PATH="$HOME/.local/bin:$PATH"
[ -d .venv ] || uv venv --system-site-packages --python "$(command -v python3)" .venv
uv pip install --python .venv/bin/python -q "pyarrow==17.0.0" pillow huggingface_hub
export HF_HUB_DISABLE_PROGRESS_BARS=1
.venv/bin/python - <<'E'
from huggingface_hub import snapshot_download
print(snapshot_download("flwrlabs/celeba", repo_type="dataset", allow_patterns=["img_align+identity+attr/*", "LICENSE", "README.md"], local_dir="raw"))
E
du -sh raw
.venv/bin/python run_fair.py prepare
rm -rf raw
.venv/bin/python run_fair.py train
.venv/bin/python run_fair.py streams
.venv/bin/python analyze_fair.py
echo "=== FAIR DONE"

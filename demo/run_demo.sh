#!/usr/bin/env bash
# Starts the demo at http://127.0.0.1:8765. Environments are managed by uv.
cd "$(dirname "$0")"
UVA=(--no-project --python 3.10 --index https://download.pytorch.org/whl/cpu --index-strategy unsafe-best-match --with torch --with "numpy<2" --with scipy --with confseq --with pillow)
[ -f data/clean_test.npz ] || UV_PYTHON_DOWNLOADS=automatic uv run --no-project --python 3.10 --with pyarrow --with pillow --with "numpy<2" python prepare.py
exec env UV_PYTHON_DOWNLOADS=automatic uv run "${UVA[@]}" python app.py

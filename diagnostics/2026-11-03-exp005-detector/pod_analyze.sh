#!/usr/bin/env bash
cd /root/exp005; export PATH="$HOME/.local/bin:$PATH"
uv venv --python 3.10 .venv_cs -q; uv pip install --python .venv_cs/bin/python -q confseq scipy "numpy<2"
uv pip install --python .venv/bin/python -q lightgbm scikit-learn
.venv_cs/bin/python cs_bounds.py > cs.log 2>&1 && .venv/bin/python analyze.py > analyze.log 2>&1; echo "=== ANALYSIS DONE $?" >> analyze.log

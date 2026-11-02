#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
# Uses the recorded existing system numerical environment; installs nothing.
# Re-running these commands overwrites derived artifacts in this directory.
uv run --no-project --no-python-downloads --python /usr/bin/python python train_core.py
uv run --no-project --no-python-downloads --python /usr/bin/python python generate_outcomes.py
uv run --no-project --no-python-downloads --python /usr/bin/python python analyze_diagnostic.py
uv run --no-project --no-python-downloads --python /usr/bin/python python lofo_analysis.py
uv run --no-project --no-python-downloads --python /usr/bin/python python prior_gate_analysis.py
uv run --no-project --no-python-downloads --python /usr/bin/python python latency_sensitivity.py
uv run --no-project --no-python-downloads --python /usr/bin/python python audit_checks.py
uv run --no-project --no-python-downloads --python /usr/bin/python python audit_headroom.py

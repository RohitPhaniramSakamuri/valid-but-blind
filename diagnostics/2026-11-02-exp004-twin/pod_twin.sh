#!/usr/bin/env bash
# Tmux session "twin". uv only. Tent and twin per model, concurrently. Waits for uploaded checkpoints.
set -uo pipefail
cd /root/exp004
export PATH="$HOME/.local/bin:$PATH" OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
command -v uv >/dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh
mkdir -p data models
wget -q https://zenodo.org/records/3555552/files/CIFAR-100-C.tar -O data/CIFAR-100-C.tar &
P1=$!
uv venv --system-site-packages --python "$(command -v python3)" .venv
uv venv --python 3.10 .venv_cs
uv pip install --python .venv_cs/bin/python -q confseq scipy "numpy<2"
get() { uvx -q gdown "$2" -O "models/$1.pt" >/dev/null 2>&1; }
G=()
get Hendrycks2020AugMix_WRN 1XpFFdCdU9LcDtcyNfo6_BV1RZHKKkBVE & G+=($!)
get Addepalli2022Efficient_WRN_34_10 1-3c-iniqNfiwGoGPHC3nSostnG6J9fDt & G+=($!)
get Addepalli2021Towards_WRN34 1-9GAld_105-jWBLXL73btmfOCwAqvz7Y & G+=($!)
get Addepalli2021Towards_PARN18 1-FwVya1sDvdFXr0_ZBoXEJW9ukGC7hPK & G+=($!)
wait "${G[@]}"
wait "$P1"; tar -xf data/CIFAR-100-C.tar -C data; rm data/CIFAR-100-C.tar
uv run --no-project -q --with pyarrow --with pillow --with numpy python make_clean.py
[ -f data/cifar-100-python/test ] || { wget -q https://www.cs.toronto.edu/~kriz/cifar-100-python.tar.gz -O data/c.tgz; tar -xzf data/c.tgz -C data; rm data/c.tgz; }
until [ -f models/.uploaded ]; do sleep 5; done
sha256sum models/*.pt | cut -c1-16,65-
echo "=== SETUP DONE"
pids=()
for n in Hendrycks2020AugMix_ResNeXt Modas2021PRIMEResNet18 Hendrycks2020AugMix_WRN Addepalli2021Towards_PARN18 Addepalli2021Towards_WRN34 Addepalli2022Efficient_WRN_34_10; do
  .venv/bin/python run_twin.py "$n" > "twin_$n.log" 2>&1 &
  pids+=($!)
done
for p in "${pids[@]}"; do wait "$p" || echo "process $p failed"; done
echo "=== STREAMS DONE"
.venv_cs/bin/python analyze_twin.py > analysis.log 2>&1 || tail -20 analysis.log
echo "=== ALL DONE"

#!/usr/bin/env bash
# Tmux session "sar". uv environments only. Six models run concurrently on one GPU.
set -uo pipefail
cd /root/exp004
export PATH="$HOME/.local/bin:$PATH" OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
command -v uv >/dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh
mkdir -p data
wget -q https://zenodo.org/records/3555552/files/CIFAR-100-C.tar -O data/CIFAR-100-C.tar &
P1=$!
wget -q https://www.cs.toronto.edu/~kriz/cifar-100-python.tar.gz -O data/cifar-100-python.tar.gz &
P2=$!
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
sha256sum models/*.pt | cut -c1-16,65-
wait "$P1"; tar -xf data/CIFAR-100-C.tar -C data; rm data/CIFAR-100-C.tar
wait "$P2"; tar -xzf data/cifar-100-python.tar.gz -C data; rm data/cifar-100-python.tar.gz
echo "=== SETUP DONE"
N=$(nvidia-smi -L | wc -l)
if [ "$N" -ge 4 ]; then MAP="Hendrycks2020AugMix_ResNeXt:0 Modas2021PRIMEResNet18:1 Hendrycks2020AugMix_WRN:1 Addepalli2021Towards_PARN18:1 Addepalli2021Towards_WRN34:2 Addepalli2022Efficient_WRN_34_10:3"
elif [ "$N" -ge 2 ]; then MAP="Addepalli2021Towards_WRN34:0 Modas2021PRIMEResNet18:0 Addepalli2021Towards_PARN18:0 Addepalli2022Efficient_WRN_34_10:1 Hendrycks2020AugMix_ResNeXt:1 Hendrycks2020AugMix_WRN:1"
else MAP="Hendrycks2020AugMix_ResNeXt:0 Modas2021PRIMEResNet18:0 Hendrycks2020AugMix_WRN:0 Addepalli2021Towards_PARN18:0 Addepalli2021Towards_WRN34:0 Addepalli2022Efficient_WRN_34_10:0"; fi
pids=()
for e in $MAP; do
  n=${e%%:*}
  CUDA_VISIBLE_DEVICES=${e##*:} .venv/bin/python run_sar.py "$n" > "sar_$n.log" 2>&1 &
  pids+=($!)
done
for p in "${pids[@]}"; do wait "$p" || echo "process $p failed"; done
echo "=== STREAMS DONE"
.venv_cs/bin/python analyze_sar.py factorial > analysis.log 2>&1 || tail -20 analysis.log
echo "=== ALL DONE"

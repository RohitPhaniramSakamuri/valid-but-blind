#!/usr/bin/env bash
# Tmux session "replicate". Uses uv environments only. The authors' check runs alongside, logging to authors.log.
set -uo pipefail
cd /root/exp004
export PATH="$HOME/.local/bin:$PATH"
mkdir -p data models
wget -q https://zenodo.org/records/3555552/files/CIFAR-100-C.tar -O data/CIFAR-100-C.tar &
P1=$!
wget -q https://www.cs.toronto.edu/~kriz/cifar-100-python.tar.gz -O data/cifar-100-python.tar.gz &
P2=$!
set -e
sha256sum arch_*.py
[ -d .venv ] || uv venv --system-site-packages --python "$(command -v python3)" .venv
[ -d .venv_cs ] || uv venv --python 3.10 .venv_cs
uv pip install --python .venv_cs/bin/python -q confseq scipy "numpy<2"
get() { uvx -q gdown "$2" -O "models/$1.pt" >/dev/null 2>&1; }
get Hendrycks2020AugMix_WRN 1XpFFdCdU9LcDtcyNfo6_BV1RZHKKkBVE
get Addepalli2022Efficient_WRN_34_10 1-3c-iniqNfiwGoGPHC3nSostnG6J9fDt
get Addepalli2021Towards_WRN34 1-9GAld_105-jWBLXL73btmfOCwAqvz7Y
get Addepalli2021Towards_PARN18 1-FwVya1sDvdFXr0_ZBoXEJW9ukGC7hPK
sha256sum models/*.pt | cut -c1-16,65-
wait "$P1"; sha256sum data/CIFAR-100-C.tar | cut -c1-16; tar -xf data/CIFAR-100-C.tar -C data; rm data/CIFAR-100-C.tar
wait "$P2"; tar -xzf data/cifar-100-python.tar.gz -C data; rm data/cifar-100-python.tar.gz
(set +e; timeout 2400 bash authors_check.sh > authors.log 2>&1) &
A=$!
MODELS="Hendrycks2020AugMix_ResNeXt Modas2021PRIMEResNet18 Hendrycks2020AugMix_WRN Addepalli2021Towards_PARN18 Addepalli2021Towards_WRN34 Addepalli2022Efficient_WRN_34_10"
for n in $MODELS; do
  echo "=== model $n"
  .venv/bin/python run_replicate.py "$n"
done
.venv_cs/bin/python analyze_replicate.py $MODELS
echo "=== REPLICATION DONE"
set +e
wait "$A"
echo "=== ALL DONE"

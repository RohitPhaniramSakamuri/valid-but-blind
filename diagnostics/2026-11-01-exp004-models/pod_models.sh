#!/usr/bin/env bash
# Tmux session "models". Downloads run in parallel. Uses uv environments only.
set -uo pipefail
cd /root/exp004
export PATH="$HOME/.local/bin:$PATH"
mkdir -p data models
wget -q https://zenodo.org/records/3555552/files/CIFAR-100-C.tar -O data/CIFAR-100-C.tar &
P1=$!
wget -q https://www.cs.toronto.edu/~kriz/cifar-100-python.tar.gz -O data/cifar-100-python.tar.gz &
P2=$!
set -e
base=https://raw.githubusercontent.com/RobustBench/robustbench/master/robustbench/model_zoo/architectures
curl -sL $base/wide_resnet.py -o arch_wide_resnet.py
curl -sL $base/resnet.py -o arch_resnet.py
sha256sum arch_*.py
[ -d .venv ] || uv venv --system-site-packages --python "$(command -v python3)" .venv
[ -d .venv_cs ] || uv venv --python 3.10 .venv_cs
uv pip install --python .venv_cs/bin/python -q confseq scipy "numpy<2"
get() { uvx -q gdown "$2" -O "models/$1.pt" >/dev/null 2>&1; ls -la "models/$1.pt" | cut -c24-; sha256sum "models/$1.pt" | cut -c1-16; }
get Hendrycks2020AugMix_WRN 1XpFFdCdU9LcDtcyNfo6_BV1RZHKKkBVE
get Addepalli2022Efficient_WRN_34_10 1-3c-iniqNfiwGoGPHC3nSostnG6J9fDt
get Addepalli2021Towards_WRN34 1-9GAld_105-jWBLXL73btmfOCwAqvz7Y
get Addepalli2021Towards_PARN18 1-FwVya1sDvdFXr0_ZBoXEJW9ukGC7hPK
echo "=== key check"
.venv/bin/python - <<'E'
import run_more as M
for n in ["Hendrycks2020AugMix_WRN", "Addepalli2022Efficient_WRN_34_10", "Addepalli2021Towards_WRN34", "Addepalli2021Towards_PARN18"]:
    M.loader(n)(f"models/{n}.pt", "cuda")
    print("keys ok", n, flush=True)
E
wait "$P1"; sha256sum data/CIFAR-100-C.tar | cut -c1-16; tar -xf data/CIFAR-100-C.tar -C data; rm data/CIFAR-100-C.tar
wait "$P2"; tar -xzf data/cifar-100-python.tar.gz -C data; rm data/cifar-100-python.tar.gz
for n in Hendrycks2020AugMix_WRN Addepalli2021Towards_PARN18 Addepalli2021Towards_WRN34 Addepalli2022Efficient_WRN_34_10; do
  echo "=== model $n"
  .venv/bin/python run_more.py "$n"
  RESULTS_DIR="results_$n" .venv_cs/bin/python analyze_confirm.py | tail -1 | cut -c1-40
done
.venv_cs/bin/python analyze_models.py Hendrycks2020AugMix_WRN Addepalli2021Towards_PARN18 Addepalli2021Towards_WRN34 Addepalli2022Efficient_WRN_34_10
echo "=== MODELS DONE"
set +e
echo "=== authors code"
timeout 1500 bash authors_check.sh
echo "=== ALL DONE"

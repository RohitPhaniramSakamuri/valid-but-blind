#!/usr/bin/env bash
# Tmux session "mech". uv environments only. Models and authors' streams run concurrently on one GPU.
set -uo pipefail
cd /root/exp004
export PATH="$HOME/.local/bin:$PATH" OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
mkdir -p data models models/cifar100/corruptions
wget -q https://zenodo.org/records/3555552/files/CIFAR-100-C.tar -O data/CIFAR-100-C.tar &
P1=$!
wget -q https://www.cs.toronto.edu/~kriz/cifar-100-python.tar.gz -O data/cifar-100-python.tar.gz &
P2=$!
set -e
[ -d .venv ] || uv venv --system-site-packages --python "$(command -v python3)" .venv
[ -d .venv_cs ] || uv venv --python 3.10 .venv_cs
uv pip install --python .venv_cs/bin/python -q confseq scipy "numpy<2"
get() { uvx -q gdown "$2" -O "models/$1.pt" >/dev/null 2>&1; }
get Hendrycks2020AugMix_WRN 1XpFFdCdU9LcDtcyNfo6_BV1RZHKKkBVE &
get Addepalli2022Efficient_WRN_34_10 1-3c-iniqNfiwGoGPHC3nSostnG6J9fDt &
get Addepalli2021Towards_WRN34 1-9GAld_105-jWBLXL73btmfOCwAqvz7Y &
get Addepalli2021Towards_PARN18 1-FwVya1sDvdFXr0_ZBoXEJW9ukGC7hPK &
for j in $(jobs -p | grep -v -E "^($P1|$P2)$"); do wait "$j"; done
sha256sum models/*.pt | cut -c1-16,65-
for n in Hendrycks2020AugMix_ResNeXt Hendrycks2020AugMix_WRN; do ln -sf /root/exp004/models/$n.pt models/cifar100/corruptions/$n.pt; done
git clone -q https://github.com/monasch/tta-monitor.git
(cd tta-monitor && git checkout -q f200f00d4ca79567df0214bdd46150bb729c2227 && git apply ../cifar100_calibration.patch && git status --short)
uv venv --python 3.9 .venv_auth
uv pip install --python .venv_auth/bin/python -q --index-strategy unsafe-best-match --extra-index-url https://download.pytorch.org/whl/cu115 "torch==1.11.0+cu115" "torchvision==0.12.0+cu115" "numpy<1.24" yacs==0.1.8 timm==0.4.12 scikit-learn pandas pillow tqdm requests pyyaml transformers==4.21.0 wilds gdown matplotlib pytorchcv scikit-image lmdb einops mpmath confseq scipy prettytable iopath jinja2 "git+https://github.com/fra31/auto-attack"
wait "$P1"; sha256sum data/CIFAR-100-C.tar | cut -c1-16; tar -xf data/CIFAR-100-C.tar -C data; rm data/CIFAR-100-C.tar
wait "$P2"; tar -xzf data/cifar-100-python.tar.gz -C data; rm data/cifar-100-python.tar.gz
.venv/bin/python make_streams.py
echo "=== authors one-stream gate"
set +e
(cd tta-monitor && ../.venv_auth/bin/python ../authors_stream.py Hendrycks2020AugMix_ResNeXt tent gaussian_noise 5 0 2>&1 | tail -3 | cut -c1-200)
wc -l authors_Hendrycks2020AugMix_ResNeXt.jsonl || true
set +e
( cd tta-monitor; for a in Hendrycks2020AugMix_ResNeXt Hendrycks2020AugMix_WRN; do for arm in tent source; do for c in gaussian_noise shot_noise impulse_noise defocus_blur glass_blur motion_blur zoom_blur; do for s in 3 5; do for d in 0 1; do
  [ "$a/$arm/$c/$s/$d" = "Hendrycks2020AugMix_ResNeXt/tent/gaussian_noise/5/0" ] || echo "$a $arm $c $s $d"; done; done; done; done; done | timeout 5400 xargs -P 3 -L 1 sh -c '../.venv_auth/bin/python ../authors_stream.py "$0" "$1" "$2" "$3" "$4" >/dev/null 2>>../authors_err.log; echo "authors $0 $1 $2 $3 $4 exit $?"' ) > authors_progress.log 2>&1 &
A=$!
pids=()
for n in Hendrycks2020AugMix_ResNeXt Modas2021PRIMEResNet18 Hendrycks2020AugMix_WRN Addepalli2021Towards_PARN18 Addepalli2021Towards_WRN34 Addepalli2022Efficient_WRN_34_10; do
  .venv/bin/python run_factorial.py "$n" > "factorial_$n.log" 2>&1 &
  pids+=($!)
done
for p in "${pids[@]}"; do wait "$p" || echo "factorial process $p failed"; done
wait "$A"
echo "=== STREAMS DONE"
.venv_cs/bin/python analyze_all.py > analysis.log 2>&1 || tail -20 analysis.log
echo "=== ALL DONE"

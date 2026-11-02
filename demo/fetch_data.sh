#!/usr/bin/env bash
# Downloads what the demo needs into demo/data and demo/models (about 3 GB). prepare.py runs on first launch of run_demo.sh.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p data models
curl -L --fail -C - https://zenodo.org/records/3555552/files/CIFAR-100-C.tar -o data/c.tar
[ "$(stat -c%s data/c.tar)" = 2918473216 ] || { echo "Incomplete download; run again to resume."; exit 1; }
tar -xf data/c.tar -C data && rm data/c.tar
uvx gdown 1XpFFdCdU9LcDtcyNfo6_BV1RZHKKkBVE -O models/Hendrycks2020AugMix_WRN.pt

#!/usr/bin/env bash
# Run the frozen analysis once on downloaded exp010 streams. Usage: bash analyze_local.sh [results dir]
# Put the notebook output so that <results dir>/streams/<ds>__<model>__<arm>/*.npz exists (default: ./results). uv only.
set -euo pipefail
cd "$(dirname "$0")"; R=$(realpath "${1:-results}")
E=""; for m in Addepalli2021Towards_WRN34 Hendrycks2020AugMix_ResNeXt Hendrycks2020AugMix_WRN Modas2021PRIMEResNet18; do E="$E cifar10/$m/tent0.001"; done
for a in tent0.001 pl0.001 im0.001; do E="$E organs/organs/$a tissue/tissue/$a"; done
for m in Hendrycks2020AugMix_WRN Modas2021PRIMEResNet18; do for a in pl0.001 im0.001; do E="$E cifar10/$m/$a"; done; done
echo "streams found: $(find "$R/streams" -name '*.npz' | wc -l) (planned 4,630)"
OUT="$R" EXPECT_SETTINGS="$E" uv run --no-project --python 3.10 --with "numpy<2" --with confseq --with scipy --with lightgbm --with scikit-learn python job/analyze10.py 2>&1 | tee "$R/analysis.log" | grep -v "^Installed"

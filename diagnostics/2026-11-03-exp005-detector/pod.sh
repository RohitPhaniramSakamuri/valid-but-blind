#!/usr/bin/env bash
set -uo pipefail
cd /root/exp005; export PATH="$HOME/.local/bin:$PATH" OMP_NUM_THREADS=2 MKL_NUM_THREADS=2
command -v uv >/dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"; uv venv --system-site-packages --python "$(command -v python3)" .venv
fetch(){ ds=$1; name=$2; size=$3; md=$4; mkdir -p $ds/parts; U="https://zenodo.org/records/10519652/files/$name?download=1"; CH=20000000
 seq 0 $(( (size-1)/CH )) | xargs -P 40 -I{} sh -c 'i={}; s=$((i*'$CH')); e=$((s+'$CH'-1)); f='$ds'/parts/$(printf %05d $i); want=$(( e<'$size'-1 ? '$CH' : '$size'-s )); for t in 1 2 3 4 5 6 7 8; do [ "$(stat -c%s $f 2>/dev/null)" = "$want" ] && exit 0; curl -s -L --max-time 400 -r $s-$e -o $f "'"$U"'"; sleep 2; done'
 cat $ds/parts/* > $ds/data.npz; [ "$(md5sum $ds/data.npz | cut -d' ' -f1)" = "$md" ] || { echo "CHECKSUM FAILED $ds"; exit 1; }; rm -rf $ds/parts; echo "fetched $ds"; }
fetch blood bloodmnist_224.npz 1540731655 b718ff6835fcbdb22ba9eacccd7b2601 & fetch derma dermamnist_224.npz 1091112502 8974907d8e169bef5f5b96bc506ae45d & wait
.venv/bin/python prepare.py blood 8 > prep_blood.log 2>&1 & .venv/bin/python prepare.py derma 7 > prep_derma.log 2>&1 & wait
grep -q DONE prep_blood.log && grep -q DONE prep_derma.log || { echo "=== PREPARE FAILED"; exit 1; }
echo "=== SETUP DONE"; pids=()
for spec in "blood 8" "derma 7"; do for lr in 0.001 0.005; do for sh in 0 1 2; do set -- $spec; .venv/bin/python run.py $1 $2 $lr $sh 3 > run_$1_${lr}_$sh.log 2>&1 & pids+=($!); done; done; done
for p in "${pids[@]}"; do wait $p || echo "failed $p"; done
tar czf results.tgz blood/streams_* derma/streams_* blood/source_report.json derma/source_report.json run_*.log prep_*.log
echo "=== ALL DONE"

#!/usr/bin/env bash
# Tmux session "derma2". Zenodo throttles each connection, so fetch ranges in parallel, verify, then restart the frozen pipeline. Code and rules are unchanged.
cd /root/exp004
U="https://zenodo.org/records/10519652/files/dermamnist_224.npz?download=1"; SIZE=1091112502; CH=20000000; mkdir -p data/parts
seq 0 $(( (SIZE-1)/CH )) | xargs -P 40 -I{} sh -c 'i={}; s=$((i*'$CH')); e=$((s+'$CH'-1)); f=data/parts/$(printf %05d $i); want=$(( e<'$SIZE'-1 ? '$CH' : '$SIZE'-s )); for t in 1 2 3 4 5 6 7 8; do [ "$(stat -c%s $f 2>/dev/null)" = "$want" ] && exit 0; curl -s -L --max-time 400 -r $s-$e -o $f "'"$U"'"; sleep 2; done'
cat data/parts/* > data/derma_full.npz
md5=$(md5sum data/derma_full.npz | cut -d" " -f1); echo "md5 $md5" | tee fetch.log
case "$md5" in 8974907d8e169bef*) ;; *) echo "CHECKSUM FAILED" | tee -a fetch.log; sleep 7200; exit 1;; esac
pkill -f "[p]repare_derma.py"; while tmux has-session -t derma 2>/dev/null; do sleep 2; done
mv data/derma_full.npz data/derma.npz; rm -rf data/parts
bash pod_derma.sh > derma.log 2>&1

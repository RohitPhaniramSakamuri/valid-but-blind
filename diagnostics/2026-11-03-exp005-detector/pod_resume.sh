#!/usr/bin/env bash
# Same code and seeds as pod.sh; fewer processes because 12 exhausted GPU memory. Existing streams are skipped.
cd /root/exp005; export OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True; pids=()
for spec in "blood 8" "derma 7"; do for lr in 0.001 0.005; do for sh in 0 1; do set -- $spec; .venv/bin/python run.py $1 $2 $lr $sh 2 > run2_$1_${lr}_$sh.log 2>&1 & pids+=($!); sleep 12; done; done; done
for p in "${pids[@]}"; do wait $p || echo "failed $p"; done
echo "=== STREAMS DONE"
bash pod_analyze.sh
tar czf results.tgz blood/streams_* derma/streams_* blood/source_report.json derma/source_report.json run*.log prep_*.log cs.json cs.log analyze.log selection.json report.json rows.json
echo "=== ALL DONE"

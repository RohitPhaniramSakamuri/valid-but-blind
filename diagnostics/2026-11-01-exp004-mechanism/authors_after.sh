#!/usr/bin/env bash
# Tmux session "authors2". Runs the authors' streams after the factorial processes free the GPU, then repeats the analysis.
cd /root/exp004
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
while pgrep -f run_factorial.py >/dev/null; do sleep 20; done
mv authors_err.log authors_err_oom_first_attempt.log 2>/dev/null
cd tta-monitor
for a in Hendrycks2020AugMix_ResNeXt Hendrycks2020AugMix_WRN; do for arm in tent source; do for c in gaussian_noise shot_noise impulse_noise defocus_blur glass_blur motion_blur zoom_blur; do for s in 3 5; do for d in 0 1; do
  [ "$a/$arm/$c/$s/$d" = "Hendrycks2020AugMix_ResNeXt/tent/gaussian_noise/5/0" ] || echo "$a $arm $c $s $d"; done; done; done; done; done | timeout 5400 xargs -P 4 -L 1 sh -c '../.venv_auth/bin/python ../authors_stream.py "$0" "$1" "$2" "$3" "$4" >/dev/null 2>>../authors_err.log; echo "authors $0 $1 $2 $3 $4 exit $?"' > ../authors_progress2.log 2>&1
cd ..
while tmux has-session -t mech 2>/dev/null; do sleep 5; done
.venv_cs/bin/python analyze_all.py > analysis.log 2>&1
echo "=== AFTER DONE" >> mech.log

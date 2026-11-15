#!/usr/bin/env bash
# exp008 SageMaker job. uv only. Self-contained: data, models, streams, analysis. Results in /opt/ml/checkpoints (synced to S3 while running).
set -uo pipefail
export HERE=$(cd "$(dirname "$0")" && pwd) WORK=/opt/ml/work OUT=/opt/ml/checkpoints OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTORCH_ALLOC_CONF=expandable_segments:True
mkdir -p $WORK/models $WORK/cifar $OUT/logs; cd $HERE; L=$OUT/logs
JOB=$(python3 -c "import json,os;print(json.loads(os.environ.get('SM_TRAINING_ENV','{}')).get('job_name',''))" 2>/dev/null); [ -n "$JOB" ] || JOB="$(hostname)-$RANDOM"
echo "start $(date -u) job=$JOB $(nvidia-smi -L | tr '\n' ' ') $(free -g | awk '/Mem/{print $2}')G" | tee -a $L/job.log
# One owner across regions: claim s3://<east bucket>/claims/exp008; a second job exits if the claim is fresh (heartbeat < 30 min).
NG=$(nvidia-smi -L | grep -c "GPU "); [ "${SKIP_CLAIM:-0}" = 1 ] || python3 claim.py claim "$JOB" "$NG" || { echo "another job owns exp008; exiting" | tee -a $L/job.log; exit 0; }
HB=""; [ "${SKIP_CLAIM:-0}" = 1 ] || { ( while true; do python3 claim.py beat "$JOB" "$NG"; sleep 300; done ) & HB=$!; }
command -v uv >/dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh; export PATH="$HOME/.local/bin:$PATH"
uv venv -q --system-site-packages --python $(command -v python3) $WORK/.venv; uv venv -q --python 3.10 $WORK/.venv_an
uv pip install -q --python $WORK/.venv_an/bin/python confseq scipy "numpy<2" lightgbm scikit-learn
python3 -c "import boto3;b=boto3.resource('s3').Bucket('vbb-exp008-286879406788-use1');[b.download_file(o.key,'$WORK/models/'+o.key.split('/')[-1]) for o in b.objects.filter(Prefix='models/')]"
# Download with waiting: Zenodo can return 503 for long periods. Up to 18 rounds 20 min apart (6 h); every part's size and the full md5 are checked.
fetch(){ local out=$1 url=$2 size=$3 md=$4 CH=50000000 np round ok part ps pe pw; np=$(( (size-1)/CH + 1 ))
 for round in $(seq 1 18); do
  mkdir -p $out.parts
  seq 0 $((np-1)) | xargs -P 16 -I{} sh -c 'i={}; s=$((i*'$CH')); e=$((s+'$CH'-1)); f='$out'.parts/$(printf %05d $i); want=$(( e<'$size'-1 ? '$CH' : '$size'-s )); for t in $(seq 1 12); do [ "$(stat -c%s $f 2>/dev/null)" = "$want" ] && exit 0; curl -sf -L --max-time 600 -r $s-$e -o $f.tmp "'"$url"'" && mv $f.tmp $f; sleep $((t*5)); done'
  ok=0; for part in $(seq 0 $((np-1))); do ps=$((part*CH)); pe=$((ps+CH-1)); pw=$(( pe<size-1 ? CH : size-ps )); [ "$(stat -c%s $out.parts/$(printf %05d $part) 2>/dev/null)" = "$pw" ] && ok=$((ok+1)); done
  if [ $ok -eq $np ]; then cat $out.parts/* > $out; if [ "$(md5sum $out | cut -d' ' -f1)" = "$md" ]; then rm -rf $out.parts; echo "fetched $out (round $round)" | tee -a $L/job.log; return 0; fi; rm -rf $out.parts $out; echo "md5 mismatch $out; refetching" | tee -a $L/job.log; fi
  echo "fetch round $round incomplete for $out ($ok/$np parts); waiting 20 min" | tee -a $L/job.log; sleep 1200
 done; echo "CHECKSUM FAILED $out (gave up)" | tee -a $L/job.log; return 1; }
Z=https://zenodo.org/records/10519652/files
CIFAR_PART=${CIFAR_PART:-1}; MED_LIST=${MED_LIST:-"oct organc pneumonia"}
[ "$CIFAR_PART" = 1 ] && ( fetch $WORK/cifar/c.tar "https://zenodo.org/records/3555552/files/CIFAR-100-C.tar?download=1" 2918473216 11f0ed0f1191edbf9fa23466ae6021d3 && tar -xf $WORK/cifar/c.tar -C $WORK/cifar && rm $WORK/cifar/c.tar
  for t in 1 2 3; do timeout 600 uvx -q --with pyarrow --with pillow --with numpy python make_clean6.py $WORK/cifar 2>&1 | tee -a $L/job.log | grep -q "True" && break; echo "clean cifar retry $t" | tee -a $L/job.log; done
  G(){ for t in 1 2 3; do timeout 600 uvx -q gdown "$2" -O $WORK/models/$1.pt && [ -s $WORK/models/$1.pt ] && { echo "model $1 ok" | tee -a $L/job.log; return 0; }; echo "model $1 retry $t" | tee -a $L/job.log; sleep 10; done; return 1; }
  G Addepalli2022Efficient_WRN_34_10 1-3c-iniqNfiwGoGPHC3nSostnG6J9fDt; G Addepalli2021Towards_WRN34 1-9GAld_105-jWBLXL73btmfOCwAqvz7Y; G Addepalli2021Towards_PARN18 1-FwVya1sDvdFXr0_ZBoXEJW9ukGC7hPK
  [ -f $WORK/cifar/CIFAR-100-C/labels.npy ] && grep -q "clean cifar (10000, 32, 32, 3) True" $L/job.log && [ -f $WORK/cifar/cifar-100-python/test ] && [ $(ls $WORK/models/*.pt | wc -l) -ge 6 ] && touch $WORK/cifar/READY || { touch $WORK/cifar/FAILED; echo "CIFAR SETUP FAILED" | tee -a $L/job.log; } ) & PIDS="$!"
[ "$CIFAR_PART" = 1 ] || { mkdir -p $WORK/cifar; touch $WORK/cifar/FAILED; PIDS=""; }
med(){ local ds=$1 k=$2 f=$3 s=$4 m=$5; mkdir -p $WORK/$ds
  fetch $WORK/$ds/data.npz "$Z/$f?download=1" $s $m || { touch $WORK/$ds/FAILED; return 1; }
  PREP_PROCS=8 $WORK/.venv/bin/python prepare8.py $ds $k > $L/prep_$ds.log 2>&1; grep -q DONE $L/prep_$ds.log && { rm -f $WORK/$ds/data.npz; touch $WORK/$ds/READY; echo "prepared $ds $(date -u)" | tee -a $L/job.log; } || { touch $WORK/$ds/FAILED; echo "PREP FAILED $ds" | tee -a $L/job.log; }; }
for d in oct organc pneumonia; do echo " $MED_LIST " | grep -q " $d " || { mkdir -p $WORK/$d; touch $WORK/$d/FAILED; }; done
echo " $MED_LIST " | grep -q " oct " && { med oct 4 octmnist_224.npz 3959197818 abc493b6d529d5de7569faaef2773ba3 & PIDS="$PIDS $!"; }
echo " $MED_LIST " | grep -q " organc " && { med organc 11 organcmnist_224.npz 760231860 050f5e875dc056f6768abf94ec9995d1 & PIDS="$PIDS $!"; }
echo " $MED_LIST " | grep -q " pneumonia " && { med pneumonia 2 pneumoniamnist_224.npz 214384716 d6a3c71de1b945ea11211b03746c1fe1 & PIDS="$PIDS $!"; }
sleep 30; $WORK/.venv/bin/python launcher.py 2>&1 | tee -a $L/launcher_stdout.log
for p in $PIDS; do wait $p; done  # never a bare wait: the heartbeat loop runs forever
echo "=== STREAMS DONE $(date -u)" | tee -a $L/job.log
$WORK/.venv_an/bin/python analyze8.py > $L/analysis.log 2>&1; echo "=== ANALYSIS DONE rc=$? $(date -u)" | tee -a $L/job.log; tail -70 $L/analysis.log
python3 -c "import boto3,glob,os;b=boto3.client('s3');[b.upload_file(f,'vbb-exp008-286879406788-use1','results/$JOB/'+os.path.basename(f)) for f in glob.glob('$OUT/*.json')+glob.glob('$OUT/logs/*.log')]" && echo "copied reports to east bucket" | tee -a $L/job.log
[ "${SKIP_CLAIM:-0}" = 1 ] || python3 claim.py done "$JOB" "$NG"; [ -n "$HB" ] && kill $HB 2>/dev/null; exit 0

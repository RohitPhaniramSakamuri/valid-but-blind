#!/usr/bin/env bash
# exp010 SageMaker job. uv only. Streams only; the frozen analysis (analyze10.py) runs locally on the downloaded streams.
# Env: BUCKET, TASKS (ds:model:arm:nshards ...), CIFAR_PART=0|1, MED_LIST="tissue organs"|"", PER_GPU.
# Exits by itself: no background loops; every wait names its PIDs. Results are in /opt/ml/checkpoints (synced to S3 while running).
set -uo pipefail
export HERE=$(cd "$(dirname "$0")" && pwd) WORK=${WORK:-/opt/ml/work} OUT=${OUT:-/opt/ml/checkpoints} OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTORCH_ALLOC_CONF=expandable_segments:True
mkdir -p $WORK/models $WORK/cifar10 $OUT/logs; cd $HERE; L=$OUT/logs
echo "start $(date -u) $(nvidia-smi -L | tr '\n' ' ') $(free -g | awk '/Mem/{print $2}')G tasks: $TASKS" | tee -a $L/job.log
command -v uv >/dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh; export PATH="$HOME/.local/bin:$PATH"
uv venv -q --system-site-packages --python $(command -v python3) $WORK/.venv
fetch(){ local out=$1 url=$2 size=$3 md=$4 CH=50000000 np round ok part ps pe pw; np=$(( (size-1)/CH + 1 ))
 for round in $(seq 1 6); do
  mkdir -p $out.parts
  seq 0 $((np-1)) | xargs -P 16 -I{} sh -c 'i={}; s=$((i*'$CH')); e=$((s+'$CH'-1)); f='$out'.parts/$(printf %05d $i); want=$(( e<'$size'-1 ? '$CH' : '$size'-s )); for t in $(seq 1 12); do [ "$(stat -c%s $f 2>/dev/null)" = "$want" ] && exit 0; curl -sf -L --max-time 600 -r $s-$e -o $f.tmp "'"$url"'" && mv $f.tmp $f; sleep $((t*5)); done'
  ok=0; for part in $(seq 0 $((np-1))); do ps=$((part*CH)); pe=$((ps+CH-1)); pw=$(( pe<size-1 ? CH : size-ps )); [ "$(stat -c%s $out.parts/$(printf %05d $part) 2>/dev/null)" = "$pw" ] && ok=$((ok+1)); done
  if [ $ok -eq $np ]; then cat $out.parts/* > $out; if [ "$(md5sum $out | cut -d' ' -f1)" = "$md" ]; then rm -rf $out.parts; echo "fetched $out (round $round)" | tee -a $L/job.log; return 0; fi; rm -rf $out.parts $out; echo "md5 mismatch $out; refetching" | tee -a $L/job.log; fi
  echo "fetch round $round incomplete for $out ($ok/$np parts); waiting 10 min" | tee -a $L/job.log; sleep 600
 done; echo "CHECKSUM FAILED $out (gave up)" | tee -a $L/job.log; return 1; }
PIDS=""
cifar(){ python3 -c "import boto3;b=boto3.resource('s3').Bucket('$BUCKET');[b.download_file(o.key,'$WORK/models/'+o.key.split('/')[-1]) for o in b.objects.filter(Prefix='models/')]"
  local t g; for g in "Addepalli2021Towards_WRN34 1-3vgjTNfSq7LSMKuayEQ-jLflAP196dB" "Hendrycks2020AugMix_WRN 1wy7gSRsUZzCzj8QhmTbcnwmES_2kkNph" "Hendrycks2020AugMix_ResNeXt 1uGP3nZbL3LC160kOsxwkkt6tDd4qbZT1" "Modas2021PRIMEResNet18 13oDyqi16FeXy5j4Vm6IghnjTVqp_XF5U"; do set -- $g
    for t in 1 2 3; do [ -s $WORK/models/c10_$1.pt ] && break; timeout 600 uvx -q gdown "$2" -O $WORK/models/c10_$1.pt; sleep 5; done; [ -s $WORK/models/c10_$1.pt ] && echo "model c10_$1 ok $(stat -c%s $WORK/models/c10_$1.pt)" | tee -a $L/job.log; done
  fetch $WORK/cifar10/c.tar "https://zenodo.org/records/2535967/files/CIFAR-10-C.tar?download=1" 2918471680 56bf5dcef84df0e2308c6dcbcbbd8499 && tar -xf $WORK/cifar10/c.tar -C $WORK/cifar10 && rm $WORK/cifar10/c.tar
  for t in 1 2 3; do timeout 600 uvx -q --with pyarrow --with pillow --with numpy python make_clean10.py $WORK/cifar10 2>&1 | tee -a $L/job.log | grep -q "True" && break; echo "clean cifar10 retry $t" | tee -a $L/job.log; done
  if [ -f $WORK/cifar10/CIFAR-10-C/labels.npy ] && grep -q "clean cifar10 (10000, 32, 32, 3) True" $L/job.log && [ $(ls $WORK/models/c10_*.pt | wc -l) -ge 4 ]; then touch $WORK/cifar10/READY; echo "cifar10 ready $(date -u)" | tee -a $L/job.log; else touch $WORK/cifar10/FAILED; echo "CIFAR10 SETUP FAILED" | tee -a $L/job.log; fi; }
med(){ local ds=$1 ncls=$2 file=$3 size=$4 md=$5; mkdir -p $WORK/$ds
  fetch $WORK/$ds/data.npz "https://zenodo.org/records/10519652/files/$file?download=1" $size $md || { touch $WORK/$ds/FAILED; return 1; }
  PREP_PROCS=8 $WORK/.venv/bin/python prepare10.py $ds $ncls > $L/prep_$ds.log 2>&1
  if grep -q "PREPARE DONE" $L/prep_$ds.log; then rm -f $WORK/$ds/data.npz; touch $WORK/$ds/READY; echo "prepared $ds $(date -u) $(cat $WORK/$ds/source_report.json | head -c 300)" | tee -a $L/job.log; else touch $WORK/$ds/FAILED; echo "PREP FAILED $ds" | tee -a $L/job.log; tail -5 $L/prep_$ds.log | tee -a $L/job.log; fi; }
if [ "${CIFAR_PART:-0}" = 1 ]; then cifar & PIDS="$PIDS $!"; fi
for d in tissue organs; do echo " ${MED_LIST:-} " | grep -q " $d " || { mkdir -p $WORK/$d; touch $WORK/$d/FAILED; }; done
[ "${CIFAR_PART:-0}" = 1 ] || touch $WORK/cifar10/FAILED
echo " ${MED_LIST:-} " | grep -q " organs " && { med organs 11 organsmnist_224.npz 802713625 b354719e553fbbb2513d5533f52a4cb1 & PIDS="$PIDS $!"; }
echo " ${MED_LIST:-} " | grep -q " tissue " && { med tissue 8 tissuemnist_224.npz 3433703243 b077128c4a949f0a4eb01517f9037b9c & PIDS="$PIDS $!"; }
sleep 20; $WORK/.venv/bin/python launcher10.py 2>&1 | tee -a $L/launcher_stdout.log
for p in $PIDS; do wait $p; done
echo "=== STREAMS DONE $(date -u) files: $(find $OUT/streams -name '*.npz' | wc -l)" | tee -a $L/job.log
exit 0

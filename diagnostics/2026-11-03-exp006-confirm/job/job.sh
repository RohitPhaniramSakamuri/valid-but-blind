#!/usr/bin/env bash
# exp006 SageMaker job. uv only. Results go to /opt/ml/checkpoints (synced to S3 while running).
set -uo pipefail
# Split across two L40S jobs: MED (path|organa) and CIFAR_MODELS (space-separated) come from the job environment.
export HERE=$(cd "$(dirname "$0")" && pwd) WORK=/opt/ml/work OUT=/opt/ml/checkpoints OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
mkdir -p $WORK/models $WORK/path $WORK/organa $WORK/cifar $OUT/logs; cd $HERE
python3 -c "import boto3;b=boto3.resource('s3').Bucket('vbb-exp006-286879406788-use1');[b.download_file(o.key,'$WORK/models/'+o.key.split('/')[-1]) for o in b.objects.filter(Prefix='models/')]"
L=$OUT/logs; echo "start $(date -u) $(nvidia-smi -L) $(nproc) cpus $(free -g | awk '/Mem/{print $2}')G" | tee $L/job.log
command -v uv >/dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh; export PATH="$HOME/.local/bin:$PATH"
PY=$(command -v python3); uv venv -q --system-site-packages --python $PY $WORK/.venv; uv venv -q --python 3.10 $WORK/.venv_an
uv pip install -q --python $WORK/.venv_an/bin/python confseq scipy "numpy<2" lightgbm scikit-learn
$WORK/.venv/bin/python -c "import torch,torchvision;print(torch.__version__,torchvision.__version__,torch.cuda.get_device_name(0))" | tee -a $L/job.log
fetch(){ out=$1; url=$2; size=$3; md=$4; mkdir -p $out.parts; CH=50000000
 seq 0 $(( (size-1)/CH )) | xargs -P 48 -I{} sh -c 'i={}; s=$((i*'$CH')); e=$((s+'$CH'-1)); f='$out'.parts/$(printf %05d $i); want=$(( e<'$size'-1 ? '$CH' : '$size'-s )); for t in 1 2 3 4 5 6 7 8 9 10; do [ "$(stat -c%s $f 2>/dev/null)" = "$want" ] && exit 0; curl -s -L --max-time 600 -r $s-$e -o $f "'"$url"'"; sleep 3; done'
 cat $out.parts/* > $out; rm -rf $out.parts; [ "$(md5sum $out | cut -d' ' -f1)" = "$md" ] && echo "fetched $out" | tee -a $L/job.log || { echo "CHECKSUM FAILED $out" | tee -a $L/job.log; return 1; }; }
# Retries resume from finished streams (e.g. after a GPU out-of-memory); same code and seeds.
R(){ for t in 1 2 3 4; do $WORK/.venv/bin/python run6.py $1 $2 $3 $4 $5 >> $6 2>&1; grep -q "^complete" $6 && return 0; echo "retry $t $2 $3" >> $6; sleep $((20*t)); done; return 1; }
Z=https://zenodo.org/records/10519652/files
( fetch $WORK/cifar/c.tar https://zenodo.org/records/3555552/files/CIFAR-100-C.tar?download=1 2918473216 11f0ed0f1191edbf9fa23466ae6021d3 && tar -xf $WORK/cifar/c.tar -C $WORK/cifar && rm $WORK/cifar/c.tar
  echo "cifar-100-c extracted $(date -u)" | tee -a $L/job.log
  for t in 1 2 3; do timeout 600 uvx -q --with pyarrow --with pillow --with numpy python make_clean6.py $WORK/cifar 2>&1 | tee -a $L/job.log | grep -q "True" && break; echo "clean cifar (HF) retry $t" | tee -a $L/job.log; done
  G(){ for t in 1 2 3; do timeout 600 uvx -q gdown "$2" -O $WORK/models/$1.pt && [ -s $WORK/models/$1.pt ] && { echo "model $1 ok" | tee -a $L/job.log; return 0; }; echo "model $1 retry $t" | tee -a $L/job.log; sleep 10; done; return 1; }
  G Addepalli2022Efficient_WRN_34_10 1-3c-iniqNfiwGoGPHC3nSostnG6J9fDt; G Addepalli2021Towards_WRN34 1-9GAld_105-jWBLXL73btmfOCwAqvz7Y; G Addepalli2021Towards_PARN18 1-FwVya1sDvdFXr0_ZBoXEJW9ukGC7hPK
  ls -la $WORK/models $WORK/cifar | tee -a $L/job.log
  pids=(); for m in $CIFAR_MODELS; do
    R cifar $m tent0.001 0 1 $L/cifar_$m.log & pids+=($!); sleep 5; done
  for p in "${pids[@]}"; do wait $p || echo "cifar process failed $p" | tee -a $L/job.log; done; echo "cifar done $(date -u)" | tee -a $L/job.log ) &
CIF=$!
med(){ ds=$1; k=$2; f=$3; s=$4; m=$5
  fetch $WORK/$ds/data.npz "$Z/$f?download=1" $s $m || return 1
  PREP_PROCS=6 $WORK/.venv/bin/python prepare6.py $ds $k > $L/prep_$ds.log 2>&1; grep -q DONE $L/prep_$ds.log || { echo "PREP FAILED $ds" | tee -a $L/job.log; return 1; }
  rm -f $WORK/$ds/data.npz; pids=()
  for a in tent0.001 tent0.005 sar; do R $ds $ds $a 0 1 $L/${ds}_$a.log & pids+=($!); sleep 8; done
  for p in "${pids[@]}"; do wait $p || echo "$ds process failed $p" | tee -a $L/job.log; done; echo "$ds done $(date -u)" | tee -a $L/job.log; }
O1=""; case "${MED:-}" in
 organa) med organa 11 organamnist_224.npz 1803859544 50747347e05c87dd3aaf92c49f9f3170 & O1=$!;;
 path) med path 9 pathmnist_224.npz 12629854322 2c51a510bcdc9cf8ddb2af93af1eadec & O1=$!;;
esac
wait $CIF ${O1:-}
echo "=== STREAMS DONE $(date -u)" | tee -a $L/job.log
# Analysis runs afterwards on the merged results of both jobs.

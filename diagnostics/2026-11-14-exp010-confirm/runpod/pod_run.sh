#!/usr/bin/env bash
# exp010 on a RunPod pod (derived from kaggle_run.sh; frozen run10.py / prepare10.py / launcher10.py unchanged). Usage: env MED_DS=.. MED_ARMS=.. C_TASKS=.. bash pod_run.sh
#   part 1: CIFAR-10-C, Tent, 4 checkpoints (primary)      part 2: OrganSMNIST + TissueMNIST, Tent (primary)
#   part 3: CIFAR-10-C, pl and im arms, 2 light checkpoints  part 4: OrganSMNIST + TissueMNIST, pl and im arms
# Runs the frozen run10.py / prepare10.py / launcher10.py unchanged. Re-running a part resumes: finished streams are skipped.
# Streams are written to $OUT (default /kaggle/working/exp010), which Kaggle keeps as the notebook output. uv only.
set -uo pipefail
PART=${1:-pod}; export HERE=$(cd "$(dirname "$0")" && pwd)
pick(){ local best="" bf=0 d f; for d in /kaggle/temp /kaggle/tmp /tmp /content; do [ -d $d ] || continue; f=$(df -Pk $d | awk 'NR==2{print $4}'); [ "$f" -gt "$bf" ] && { bf=$f; best=$d; }; done; echo $best; }
export WORK=${WORK:-/root/exp010_work} OUT=${OUT:-/root/exp010} OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTORCH_ALLOC_CONF=expandable_segments:True
mkdir -p $WORK/models $WORK/cifar10 $OUT/logs $OUT/streams; cd $HERE; L=$OUT/logs
echo "start part $PART $(date -u) work=$WORK free=$(df -Ph $WORK | awk 'NR==2{print $4}') $(nvidia-smi -L | tr '\n' ' ') ram=$(free -g | awk '/Mem/{print $2}')G" | tee -a $L/job.log
# resume from an earlier session's output attached as an input dataset (any /kaggle/input/*/exp010/streams)
for d in /kaggle/input/*/exp010/models /kaggle/input/*/models; do [ -d "$d" ] && { mkdir -p $OUT/models; cp -n "$d"/*_source.pt $OUT/models/ 2>/dev/null; }; done
for d in /kaggle/input/*/exp010/streams /kaggle/input/*/streams; do [ -d "$d" ] && { cp -rn "$d"/. $OUT/streams/ && echo "resumed from $d: $(find $OUT/streams -name '*.npz' | wc -l) streams" | tee -a $L/job.log; }; done
command -v uv >/dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh; export PATH="$HOME/.local/bin:$PATH"
uv venv -q --system-site-packages --python $(command -v python3) $WORK/.venv; PY=$WORK/.venv/bin/python
TV=$($PY -c "import torch;v=torch.__version__.split('+')[0].split('.');print('0.%d.%s'%(int(v[1])+15,v[2]))"); CU=$($PY -c "import torch;print('cu'+torch.version.cuda.replace('.',''))")
$PY -c "import numpy, PIL" 2>/dev/null || uv pip install -q --python $PY "numpy<2.3" pillow 2>&1 | tail -2
$PY -c "import torchvision" 2>/dev/null || uv pip install -q --no-deps --python $PY "torchvision==$TV" --index-url https://download.pytorch.org/whl/$CU 2>&1 | tail -2
$PY -c "import torch, torchvision" 2>/dev/null || { PY=$(command -v python3); echo "venv cannot see torch; using system python $PY" | tee -a $L/job.log; }
$PY -c "import torch, torchvision, numpy; print('torchvision', torchvision.__version__, 'numpy', numpy.__version__); print('torch', torch.__version__, 'cuda', torch.cuda.is_available(), torch.cuda.device_count())" | tee -a $L/job.log
fetch(){ local out=$1 url=$2 size=$3 md=$4; [ "$(stat -c%s $out 2>/dev/null)" = "$size" ] && [ "$(md5sum $out | cut -d' ' -f1)" = "$md" ] && return 0
  bash $HERE/parfetch.sh $out "$url" $size $md 2>&1 | tee -a $L/job.log; [ "$(stat -c%s $out 2>/dev/null)" = "$size" ] && { echo "fetched $out $(date -u +%H:%M:%S)" | tee -a $L/job.log; return 0; }; echo "FETCH FAILED $out" | tee -a $L/job.log; return 1; }
cifar(){ [ -f $WORK/cifar10/READY ] && return 0; local t g
  for g in "Addepalli2021Towards_WRN34 1-3vgjTNfSq7LSMKuayEQ-jLflAP196dB" "Hendrycks2020AugMix_WRN 1wy7gSRsUZzCzj8QhmTbcnwmES_2kkNph" "Hendrycks2020AugMix_ResNeXt 1uGP3nZbL3LC160kOsxwkkt6tDd4qbZT1" "Modas2021PRIMEResNet18 13oDyqi16FeXy5j4Vm6IghnjTVqp_XF5U"; do set -- $g
    for t in 1 2 3; do [ -s $WORK/models/c10_$1.pt ] && break; timeout 900 uvx -q gdown "$2" -O $WORK/models/c10_$1.pt; sleep 5; done; [ -s $WORK/models/c10_$1.pt ] && echo "model c10_$1 ok $(stat -c%s $WORK/models/c10_$1.pt)" | tee -a $L/job.log; done
  fetch $WORK/cifar10/c.tar "https://zenodo.org/records/2535967/files/CIFAR-10-C.tar?download=1" 2918471680 56bf5dcef84df0e2308c6dcbcbbd8499 && tar -xf $WORK/cifar10/c.tar -C $WORK/cifar10 && rm $WORK/cifar10/c.tar
  for t in 1 2 3; do timeout 600 uvx -q --with pyarrow --with pillow --with numpy python make_clean10.py $WORK/cifar10 2>&1 | tee -a $L/job.log | grep -q "True" && break; echo "clean cifar10 retry $t" | tee -a $L/job.log; done
  if [ -f $WORK/cifar10/CIFAR-10-C/labels.npy ] && grep -q "clean cifar10 (10000, 32, 32, 3) True" $L/job.log && [ $(ls $WORK/models/c10_*.pt | wc -l) -ge 4 ]; then touch $WORK/cifar10/READY; echo "cifar10 ready" | tee -a $L/job.log; else touch $WORK/cifar10/FAILED; echo "CIFAR10 SETUP FAILED" | tee -a $L/job.log; fi; }
med(){ local ds=$1 ncls=$2 file=$3 size=$4 md=$5; [ -f $WORK/$ds/READY ] && return 0; mkdir -p $WORK/$ds
  fetch $WORK/$ds/data.npz "https://zenodo.org/records/10519652/files/$file?download=1" $size $md || { touch $WORK/$ds/FAILED; return 1; }
  PREP_PROCS=${PREP_PROCS:-4} $PY prepare10.py $ds $ncls > $L/prep_$ds.log 2>&1
  if grep -q "PREPARE DONE" $L/prep_$ds.log; then rm -f $WORK/$ds/data.npz; mkdir -p $OUT/models
    # every arm of a dataset must use the SAME source model: keep the first trained one in $OUT/models and reuse it in later sessions (image sets are regenerated from fixed seeds)
    if [ -s $OUT/models/${ds}_source.pt ]; then cp $OUT/models/${ds}_source.pt $WORK/$ds/source.pt; echo "reused saved source model for $ds" | tee -a $L/job.log; else cp $WORK/$ds/source.pt $OUT/models/${ds}_source.pt; cp $WORK/$ds/source_report.json $OUT/logs/source_report_$ds.json; fi; touch $WORK/$ds/READY; echo "prepared $ds $(head -c 300 $WORK/$ds/source_report.json)" | tee -a $L/job.log; else touch $WORK/$ds/FAILED; echo "PREP FAILED $ds" | tee -a $L/job.log; tail -5 $L/prep_$ds.log | tee -a $L/job.log; fi; }
run(){ TASKS="$1" PER_GPU=$2 $PY launcher10.py 2>&1 | tee -a $L/launcher_stdout.log; }
C4="cifar10:Addepalli2021Towards_WRN34:tent0.001:3 cifar10:Hendrycks2020AugMix_ResNeXt:tent0.001:3 cifar10:Hendrycks2020AugMix_WRN:tent0.001:2 cifar10:Modas2021PRIMEResNet18:tent0.001:2"
CA="cifar10:Hendrycks2020AugMix_WRN:pl0.001:2 cifar10:Hendrycks2020AugMix_WRN:im0.001:2 cifar10:Modas2021PRIMEResNet18:pl0.001:2 cifar10:Modas2021PRIMEResNet18:im0.001:2"
medpart(){ # one dataset at a time so the corrupted image sets (about 22 GB each) never coexist on disk
  local arms="$1" ds; for ds in organs tissue; do
    if [ $ds = organs ]; then med organs 11 organsmnist_224.npz 802713625 b354719e553fbbb2513d5533f52a4cb1; else med tissue 8 tissuemnist_224.npz 3433703243 b077128c4a949f0a4eb01517f9037b9c; fi
    run "$(for a in $arms; do printf '%s:%s:%s:2 ' $ds $ds $a; done)" ${PER_GPU:-3}; rm -rf $WORK/$ds; done; }
# RunPod: medical and CIFAR work run side by side on the pod's GPUs. Env: MED_DS (organs|tissue|""), MED_ARMS, C_TASKS, PER_GPU_MED, PER_GPU_C
PIDS=""
if [ -n "${MED_DS:-}" ]; then ( if [ $MED_DS = organs ]; then med organs 11 organsmnist_224.npz 802713625 b354719e553fbbb2513d5533f52a4cb1; else med tissue 8 tissuemnist_224.npz 3433703243 b077128c4a949f0a4eb01517f9037b9c; fi
    TASKS="$(for a in $MED_ARMS; do printf '%s:%s:%s:%s ' $MED_DS $MED_DS $a ${MED_SHARDS:-2}; done)" PER_GPU=${PER_GPU_MED:-3} $PY launcher10.py > $L/launcher_med_stdout.log 2>&1 ) & PIDS="$PIDS $!"; fi
if [ -n "${C_TASKS:-}" ]; then ( cifar; TASKS="$C_TASKS" PER_GPU=${PER_GPU_C:-3} $PY launcher10.py > $L/launcher_cifar_stdout.log 2>&1 ) & PIDS="$PIDS $!"; fi
for p in $PIDS; do wait $p; done
echo "=== PART $PART DONE $(date -u) streams so far: $(find $OUT/streams -name '*.npz' | wc -l)" | tee -a $L/job.log
for d in $OUT/streams/*/; do echo "$(basename $d) $(ls $d | grep -c npz)"; done | tee -a $L/job.log

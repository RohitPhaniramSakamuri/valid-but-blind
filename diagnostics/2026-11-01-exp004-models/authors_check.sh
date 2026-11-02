#!/usr/bin/env bash
# Their monitor.py, unmodified at the pinned commit, in a uv venv. Their file pins torch 1.10 / torchvision 0.11;
# we use torch 1.11 and torchvision 0.12 for a CUDA build that may run on this GPU, and disclose that.
cd /root/exp004
export PATH="$HOME/.local/bin:$PATH"
COMMIT=f200f00d4ca79567df0214bdd46150bb729c2227
[ -d tta-monitor ] || git clone -q https://github.com/monasch/tta-monitor.git
cd tta-monitor && git checkout -q "$COMMIT" && echo "modified files: $(git status --short | wc -l)"
[ -d ../.venv_auth ] || uv venv --python 3.9 ../.venv_auth
PY=../.venv_auth/bin/python
uv pip install --python $PY -q --index-strategy unsafe-best-match --extra-index-url https://download.pytorch.org/whl/cu115 "torch==1.11.0+cu115" "torchvision==0.12.0+cu115" "numpy<1.24" yacs==0.1.8 timm==0.4.12 scikit-learn pandas pillow tqdm requests pyyaml transformers==4.21.0 wilds gdown matplotlib pytorchcv scikit-image lmdb einops 2>&1 | tail -2 | cut -c1-200
$PY -c "import torch,torchvision;print(torch.__version__,torchvision.__version__,torch.cuda.is_available());print(torch.ones(1).cuda()+1)" 2>&1 | tail -2 | cut -c1-160
for order in uniform by_class; do
  echo "--- authors $order"
  timeout 500 $PY monitor.py --cfg cfgs/cifar100/tent.yaml RUN_NAME _authors_$order MONITORING.ERROR_DIST expectation MONITORING.E 0_1_loss MONITORING.E_HAT max_class_prob MONITORING.CONT_CALIB True MONITORING.CALIB_SIZE 1000 MONITORING.CALIB_PROC max_f1 MONITORING.CONT_CALIB_PROC max_f1 CORRUPTION.SEVERITY "[5]" CORRUPTION.TYPE '["gaussian_noise"]' MONITORING.CALIB_SEED 12 RNG_SEED 12 TEST.BATCH_ORDER $order TEST.SAVE True SAVE_PATH /root/exp004/authors_out OPTIM.LR 0.001 DATA_DIR /root/exp004/data CKPT_DIR /root/exp004/models 2>&1 | grep -v -E 'Calibration (q_hat|pfa|pfn)|FutureWarning|warnings.warn' | tail -14 | cut -c1-190
  echo "exit ${PIPESTATUS[0]}"
done
cd /root/exp004
.venv_cs/bin/python - <<'E' 2>&1 | tail -8 | cut -c1-200
import glob, os
print({p: len(glob.glob(p + "/**/*", recursive=True)) for p in glob.glob("authors_out/saved/*/*")})
E

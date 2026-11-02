#!/usr/bin/env bash
# Step 3: their monitor.py, unchanged at the pinned commit, on one CIFAR-100-C Tent stream (uniform order).
# Time-boxed. A failure is recorded and does not affect the second-model results.
cd /root/exp004
export PATH="$HOME/.local/bin:$PATH"
COMMIT=f200f00d4ca79567df0214bdd46150bb729c2227
[ -d tta-monitor ] || git clone -q https://github.com/monasch/tta-monitor.git
cd tta-monitor && git checkout -q "$COMMIT" && git status --short | head -3
[ -d ../.venv_repo ] || uv venv --system-site-packages --python "$(command -v python3)" ../.venv_repo
uv pip install --python ../.venv_repo/bin/python -q yacs gdown scikit-learn pandas timm pyyaml pillow tqdm requests matplotlib wilds transformers lmdb einops 2>&1 | tail -1
timeout 900 ../.venv_repo/bin/python monitor.py --cfg cfgs/cifar100/tent.yaml \
  RUN_NAME _authors MONITORING.ERROR_DIST expectation MONITORING.E 0_1_loss MONITORING.E_HAT max_class_prob \
  MONITORING.CONT_CALIB True MONITORING.CALIB_SIZE 1000 MONITORING.CALIB_PROC max_f1 MONITORING.CONT_CALIB_PROC max_f1 \
  CORRUPTION.SEVERITY "[5]" CORRUPTION.TYPE '["gaussian_noise"]' MONITORING.CALIB_SEED 12 RNG_SEED 12 \
  TEST.SAVE True SAVE_PATH /root/exp004/authors_out OPTIM.LR 0.001 DATA_DIR /root/exp004/data CKPT_DIR /root/exp004/models 2>&1 | grep -v -E 'Calibration (q_hat|pfa|pfn)' | tail -25 | cut -c1-200
echo "authors exit: ${PIPESTATUS[0]}"
find /root/exp004/authors_out -name '*qhat*' 2>/dev/null | wc -l

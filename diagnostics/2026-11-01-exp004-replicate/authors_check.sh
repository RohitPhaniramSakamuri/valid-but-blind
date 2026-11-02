#!/usr/bin/env bash
# Their monitor.py, unmodified at the pinned commit, in a uv venv. Their file pins torch 1.10 / torchvision 0.11;
# we use torch 1.11 and torchvision 0.12 for a CUDA build that runs on this GPU, and disclose that.
# Missing imports are installed one at a time, at most 12, and logged, so a gap does not end the check.
cd /root/exp004
export PATH="$HOME/.local/bin:$PATH"
COMMIT=f200f00d4ca79567df0214bdd46150bb729c2227
[ -d tta-monitor ] || git clone -q https://github.com/monasch/tta-monitor.git
cd tta-monitor && git checkout -q "$COMMIT" && echo "modified files: $(git status --short | wc -l)"
[ -d ../.venv_auth ] || uv venv --python 3.9 ../.venv_auth
PY=../.venv_auth/bin/python
uv pip install --python $PY -q --index-strategy unsafe-best-match --extra-index-url https://download.pytorch.org/whl/cu115 "torch==1.11.0+cu115" "torchvision==0.12.0+cu115" "numpy<1.24" yacs==0.1.8 timm==0.4.12 scikit-learn pandas pillow tqdm requests pyyaml transformers==4.21.0 wilds gdown matplotlib pytorchcv scikit-image lmdb einops mpmath confseq scipy prettytable iopath jinja2 "git+https://github.com/fra31/auto-attack" 2>&1 | tail -3 | cut -c1-200
ARGS='MONITORING.ERROR_DIST expectation MONITORING.E 0_1_loss MONITORING.E_HAT max_class_prob MONITORING.CONT_CALIB True MONITORING.CALIB_SIZE 1000 MONITORING.CALIB_PROC max_f1 MONITORING.CONT_CALIB_PROC max_f1 CORRUPTION.SEVERITY [5] CORRUPTION.TYPE ["gaussian_noise"] MONITORING.CALIB_SEED 12 RNG_SEED 12 TEST.SAVE True SAVE_PATH /root/exp004/authors_out OPTIM.LR 0.001 DATA_DIR /root/exp004/data CKPT_DIR /root/exp004/models'
for attempt in $(seq 1 12); do
  $PY -c "import monitor" > /tmp/imp.log 2>&1 && { echo "imports ok after $((attempt-1)) additions"; break; }
  mod=$(grep -oP "No module named '\K[^'.]+" /tmp/imp.log | tail -1)
  [ -n "$mod" ] || { tail -5 /tmp/imp.log | cut -c1-200; break; }
  echo "adding missing module: $mod"
  uv pip install --python $PY -q "$mod" 2>&1 | tail -1 | cut -c1-200
done
for order in uniform by_class; do
  echo "--- authors $order"
  timeout 600 $PY monitor.py --cfg cfgs/cifar100/tent.yaml RUN_NAME _authors_$order TEST.BATCH_ORDER $order $ARGS 2>&1 | grep -v -E 'Calibration (q_hat|pfa|pfn)|FutureWarning|warnings.warn' | tail -14 | cut -c1-190
  echo "exit ${PIPESTATUS[0]}"
done
find /root/exp004/authors_out -type f | head -20
du -sh /root/exp004/authors_out
echo "=== AUTHORS DONE"

"""Clean CIFAR-10 test set from the Hugging Face mirror in original order; run10.py asserts labels match CIFAR-10-C."""
import io, os, pickle, sys, urllib.request
import numpy as np, pyarrow.parquet as pq
from PIL import Image
r = sys.argv[1]; os.makedirs(r, exist_ok=True)
urllib.request.urlretrieve("https://huggingface.co/datasets/uoft-cs/cifar10/resolve/main/plain_text/test-00000-of-00001.parquet", f"{r}/test.parquet")
t = pq.read_table(f"{r}/test.parquet").to_pylist()
x = np.stack([np.asarray(Image.open(io.BytesIO(q["img"]["bytes"])).convert("RGB")) for q in t]); y = np.array([q["label"] for q in t], dtype=np.int64)
np.save(f"{r}/clean_x.npy", x); np.save(f"{r}/clean_y.npy", y)
lab = f"{r}/CIFAR-10-C/labels.npy"
print("clean cifar10", x.shape, bool((np.load(lab)[:10000] == y).all()) if os.path.exists(lab) else "nolabels", flush=True)

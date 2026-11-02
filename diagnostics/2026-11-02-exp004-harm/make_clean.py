"""Writes data/cifar-100-python/test from a Hugging Face mirror, keeping the original order; run_twin.py asserts labels match CIFAR-100-C."""
import io, os, pickle, urllib.request
import numpy as np, pyarrow.parquet as pq
from PIL import Image
os.makedirs("data/cifar-100-python", exist_ok=True)
urllib.request.urlretrieve("https://huggingface.co/datasets/uoft-cs/cifar100/resolve/main/cifar100/test-00000-of-00001.parquet", "data/test.parquet")
t = pq.read_table("data/test.parquet").to_pylist()
x = np.stack([np.asarray(Image.open(io.BytesIO(r["img"]["bytes"])).convert("RGB")) for r in t])
y = [r["fine_label"] for r in t]
pickle.dump(dict(data=x.transpose(0, 3, 1, 2).reshape(len(x), -1), fine_labels=y), open("data/cifar-100-python/test", "wb"))
print(x.shape, np.load("data/CIFAR-100-C/labels.npy")[:10000].tolist() == y)

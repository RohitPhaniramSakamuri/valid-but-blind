"""Clean CIFAR-100 test set from the Hugging Face mirror in original order (Toronto mirror unreliable from cloud). run6.py asserts labels match CIFAR-100-C."""
import io, os, pickle, sys, urllib.request
import numpy as np, pyarrow.parquet as pq
from PIL import Image
r = sys.argv[1]; os.makedirs(f"{r}/cifar-100-python", exist_ok=True)
urllib.request.urlretrieve("https://huggingface.co/datasets/uoft-cs/cifar100/resolve/main/cifar100/test-00000-of-00001.parquet", f"{r}/test.parquet")
t = pq.read_table(f"{r}/test.parquet").to_pylist()
x = np.stack([np.asarray(Image.open(io.BytesIO(q["img"]["bytes"])).convert("RGB")) for q in t]); y = [q["fine_label"] for q in t]
pickle.dump(dict(data=x.transpose(0, 3, 1, 2).reshape(len(x), -1), fine_labels=y), open(f"{r}/cifar-100-python/test", "wb"))
print("clean cifar", x.shape, np.load(f"{r}/CIFAR-100-C/labels.npy")[:10000].tolist() == y, flush=True)

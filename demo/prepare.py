"""Writes data/clean_test.npz from a Hugging Face copy of CIFAR-100 test images, keeping the original order, and checks labels against CIFAR-100-C."""
import io
import os
import urllib.request

import numpy as np
import pyarrow.parquet as pq
from PIL import Image

URL = "https://huggingface.co/datasets/uoft-cs/cifar100/resolve/main/cifar100/test-00000-of-00001.parquet"
urllib.request.urlretrieve(URL, "data/test.parquet")
t = pq.read_table("data/test.parquet").to_pylist()
x = np.stack([np.asarray(Image.open(io.BytesIO(r["img"]["bytes"])).convert("RGB")) for r in t])
y = np.array([r["fine_label"] for r in t])
if os.path.exists("data/CIFAR-100-C/labels.npy"):
    assert (np.load("data/CIFAR-100-C/labels.npy")[:10000] == y).all(), "labels differ from CIFAR-100-C"
np.savez_compressed("data/clean_test.npz", x=x, y=y)
print("clean images ready", x.shape)

"""Corruptions for exp008 (shared by prepare8.py and run8.py)."""
import io
import numpy as np
from PIL import Image, ImageFilter

def corrupt(a):
    img, name, v, seed = a
    rng = np.random.default_rng(seed); x = img.astype(np.float32) / 255
    if name == "gaussian_noise": x = x + rng.normal(0, v, x.shape)
    elif name == "speckle_noise": x = x * (1 + rng.normal(0, v, x.shape))
    elif name == "shot_noise": x = rng.poisson(x * v) / v
    elif name == "posterize": x = np.floor(x * v) / (v - 1)
    elif name == "salt_pepper": m = rng.random(x.shape[:2]); x = x.copy(); x[m < v / 2] = 0; x[m > 1 - v / 2] = 1
    elif name == "darken": x = x * v
    elif name == "brightness": x = x + v
    elif name == "gamma": x = x ** v
    elif name == "saturation": g = x.mean(2, keepdims=True); x = g + v * (x - g)
    elif name == "contrast": m = x.mean((0, 1), keepdims=True); x = (x - m) * v + m
    else:
        p = Image.fromarray(img)
        if name == "gaussian_blur": return np.asarray(p.filter(ImageFilter.GaussianBlur(v)))
        if name == "pixelate": return np.asarray(p.resize((v, v), Image.BOX).resize((224, 224), Image.NEAREST))
        b = io.BytesIO(); p.save(b, "JPEG", quality=v); return np.asarray(Image.open(io.BytesIO(b.getvalue())).convert("RGB"))
    return (np.clip(x, 0, 1) * 255).astype(np.uint8)

"""Experiment 004 more models: same streams, Tent and monitor as run_second.py, one published checkpoint each.

Architectures come from RobustBench files fetched at run time from the master branch; each
checkpoint must load with no missing or unexpected keys apart from the mu/sigma buffers.
"""
import argparse
import importlib.util
import json
import os

import torch
import torch.nn as nn

import run_second as RS


def module(path):
    spec = importlib.util.spec_from_file_location(os.path.basename(path)[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


class Norm(nn.Module):
    def __init__(self, inner, mu=None, sigma=None):
        super().__init__()
        self.inner = inner
        self.mu, self.sigma = mu, sigma

    def forward(self, x):
        if self.mu is not None:
            x = (x - self.mu.to(x.device)) / self.sigma.to(x.device)
        return self.inner(x)


def architecture(name):
    wrn, res = module("arch_wide_resnet.py"), module("arch_resnet.py")
    half = torch.tensor([0.5] * 3).view(1, 3, 1, 1)
    if name == "Hendrycks2020AugMix_WRN":
        return wrn.WideResNet(depth=40, widen_factor=2, sub_block1=False, num_classes=100), half, half
    if name == "Addepalli2022Efficient_WRN_34_10":
        return wrn.WideResNet(depth=34, widen_factor=10, num_classes=100), None, None
    if name == "Addepalli2021Towards_WRN34":
        return wrn.WideResNet(num_classes=100, depth=34, sub_block1=True), None, None
    if name == "Addepalli2021Towards_PARN18":
        return res.PreActResNet(res.PreActBlockV2, [2, 2, 2, 2], num_classes=100, bn_before_fc=True), None, None
    raise ValueError(name)


def loader(name):
    def load(path, device, smoke=False):
        inner, mu, sigma = architecture(name)
        ck = torch.load(path, map_location="cpu", weights_only=False)
        sd = ck.get("state_dict", ck) if hasattr(ck, "get") else ck
        sd = {k.replace("module.", "", 1).replace("model.", "", 1): v for k, v in sd.items()}
        if "mu" in sd:
            mu, sigma = sd.pop("mu"), sd.pop("sigma")
        missing, unexpected = inner.load_state_dict(sd, strict=False)
        if missing or unexpected:
            raise SystemExit(f"{name}: missing {missing[:5]} unexpected {unexpected[:5]}")
        return Norm(inner, mu, sigma).to(device).eval()
    return load


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    a = ap.parse_args()
    RS.OUT = f"results_{a.name}"
    RS.CKPT = f"models/{a.name}.pt"
    RS.load = loader(a.name)
    RS.main()
    meta = json.load(open(f"{RS.OUT}/calibration.json"))
    meta["model"] = a.name
    json.dump(meta, open(f"{RS.OUT}/calibration.json", "w"), indent=1)

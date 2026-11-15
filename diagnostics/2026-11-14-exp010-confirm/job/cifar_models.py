"""exp010: CIFAR-10 loaders added (load_cifar10); same architectures with 10 classes.
CIFAR-100 RobustBench architectures copied from exp003 run.py (ResNeXt29), exp004 run_second.py (PRIME ResNet18) and exp004-models (RobustBench arch files)."""
import math
import torch
import torch.nn as nn
import torch.nn.functional as F
class Bottleneck(nn.Module):
    def __init__(self, inp, planes, card, width, stride=1, down=None):
        super().__init__()
        dim = int(math.floor(planes * (width / 64.0)))
        self.conv_reduce = nn.Conv2d(inp, dim * card, 1, 1, 0, bias=False)
        self.bn_reduce = nn.BatchNorm2d(dim * card)
        self.conv_conv = nn.Conv2d(dim * card, dim * card, 3, stride, 1, groups=card, bias=False)
        self.bn = nn.BatchNorm2d(dim * card)
        self.conv_expand = nn.Conv2d(dim * card, planes * 4, 1, 1, 0, bias=False)
        self.bn_expand = nn.BatchNorm2d(planes * 4)
        self.downsample = down

    def forward(self, x):
        y = F.relu(self.bn_reduce(self.conv_reduce(x)))
        y = F.relu(self.bn(self.conv_conv(y)))
        y = self.bn_expand(self.conv_expand(y))
        return F.relu((self.downsample(x) if self.downsample is not None else x) + y)


class ResNeXt29(nn.Module):
    def __init__(self, card=4, width=32, classes=100):
        super().__init__()
        self.card, self.width, self.inplanes = card, width, 64
        self.conv_1_3x3 = nn.Conv2d(3, 64, 3, 1, 1, bias=False)
        self.bn_1 = nn.BatchNorm2d(64)
        self.stage_1 = self._layer(64, 3, 1)
        self.stage_2 = self._layer(128, 3, 2)
        self.stage_3 = self._layer(256, 3, 2)
        self.avgpool = nn.AvgPool2d(8)
        self.classifier = nn.Linear(1024, classes)
        self.register_buffer("mu", torch.tensor([0.5] * 3).view(1, 3, 1, 1))
        self.register_buffer("sigma", torch.tensor([0.5] * 3).view(1, 3, 1, 1))

    def _layer(self, planes, blocks, stride):
        down = None
        if stride != 1 or self.inplanes != planes * 4:
            down = nn.Sequential(nn.Conv2d(self.inplanes, planes * 4, 1, stride, bias=False),
                                 nn.BatchNorm2d(planes * 4))
        layers = [Bottleneck(self.inplanes, planes, self.card, self.width, stride, down)]
        self.inplanes = planes * 4
        layers += [Bottleneck(self.inplanes, planes, self.card, self.width) for _ in range(1, blocks)]
        return nn.Sequential(*layers)

    def forward(self, x, feats=False):
        x = (x - self.mu) / self.sigma
        x = F.relu(self.bn_1(self.conv_1_3x3(x)))
        x = self.stage_3(self.stage_2(self.stage_1(x)))
        z = self.avgpool(x).flatten(1)
        logits = self.classifier(z)
        return (logits, z) if feats else logits


class Block(nn.Module):
    def __init__(self, inp, planes, stride=1):
        super().__init__()
        self.conv1 = nn.Conv2d(inp, planes, 3, stride, 1, bias=False)
        self.bn1 = nn.BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(planes, planes, 3, 1, 1, bias=False)
        self.bn2 = nn.BatchNorm2d(planes)
        self.shortcut = nn.Sequential()
        if stride != 1 or inp != planes:
            self.shortcut = nn.Sequential(nn.Conv2d(inp, planes, 1, stride, bias=False), nn.BatchNorm2d(planes))

    def forward(self, x):
        y = self.bn2(self.conv2(F.relu(self.bn1(self.conv1(x)))))
        return F.relu(y + self.shortcut(x))


class ResNet18(nn.Module):
    def __init__(self, classes=100):
        super().__init__()
        self.inp = 64
        self.conv1 = nn.Conv2d(3, 64, 3, 1, 1, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.layer1 = self._layer(64, 1)
        self.layer2 = self._layer(128, 2)
        self.layer3 = self._layer(256, 2)
        self.layer4 = self._layer(512, 2)
        self.linear = nn.Linear(512, classes)
        self.register_buffer("mu", torch.zeros(1, 3, 1, 1))
        self.register_buffer("sigma", torch.ones(1, 3, 1, 1))

    def _layer(self, planes, stride):
        layers = [Block(self.inp, planes, stride), Block(planes, planes)]
        self.inp = planes
        return nn.Sequential(*layers)

    def forward(self, x):
        x = (x - self.mu) / self.sigma
        x = F.relu(self.bn1(self.conv1(x)))
        x = self.layer4(self.layer3(self.layer2(self.layer1(x))))
        return self.linear(F.avg_pool2d(x, 4).flatten(1))




import importlib.util, os
def _module(path):
    spec = importlib.util.spec_from_file_location(os.path.basename(path)[:-3], path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
class Norm(nn.Module):
    def __init__(self, inner, mu=None, sigma=None):
        super().__init__(); self.inner, self.mu, self.sigma = inner, mu, sigma
    def forward(self, x):
        if self.mu is not None: x = (x - self.mu.to(x.device)) / self.sigma.to(x.device)
        return self.inner(x)
def load_cifar(name, path, here):
    if name == "Hendrycks2020AugMix_ResNeXt":
        m = ResNeXt29(); ck = torch.load(path, map_location="cpu", weights_only=True); sd = {k.replace("module.", ""): v for k, v in ck.get("state_dict", ck).items()}
        miss, unexp = m.load_state_dict(sd, strict=False); assert not (set(miss) - {"mu", "sigma"}) and not unexp, (miss, unexp); return m
    if name == "Modas2021PRIMEResNet18":
        m = ResNet18(); m.load_state_dict(torch.load(path, map_location="cpu", weights_only=True), strict=True); return m
    wrn, res = _module(os.path.join(here, "arch_wide_resnet.py")), _module(os.path.join(here, "arch_resnet.py")); half = torch.tensor([0.5] * 3).view(1, 3, 1, 1)
    inner, mu, sigma = {"Hendrycks2020AugMix_WRN": lambda: (wrn.WideResNet(depth=40, widen_factor=2, sub_block1=False, num_classes=100), half, half), "Addepalli2022Efficient_WRN_34_10": lambda: (wrn.WideResNet(depth=34, widen_factor=10, num_classes=100), None, None), "Addepalli2021Towards_WRN34": lambda: (wrn.WideResNet(num_classes=100, depth=34, sub_block1=True), None, None), "Addepalli2021Towards_PARN18": lambda: (res.PreActResNet(res.PreActBlockV2, [2, 2, 2, 2], num_classes=100, bn_before_fc=True), None, None)}[name]()
    ck = torch.load(path, map_location="cpu", weights_only=False); sd = ck.get("state_dict", ck) if hasattr(ck, "get") else ck
    sd = {k.replace("module.", "", 1).replace("model.", "", 1): v for k, v in sd.items()}
    if "mu" in sd: mu, sigma = sd.pop("mu"), sd.pop("sigma")
    miss, unexp = inner.load_state_dict(sd, strict=False); assert not miss and not unexp, (name, miss[:5], unexp[:5]); return Norm(inner, mu, sigma)

def load_cifar10(name, path, here):
    """RobustBench CIFAR-10 common-corruption checkpoints (same architectures as the CIFAR-100 ones, 10 classes)."""
    if name == "Hendrycks2020AugMix_ResNeXt":
        m = ResNeXt29(classes=10); ck = torch.load(path, map_location="cpu", weights_only=True); sd = {k.replace("module.", ""): v for k, v in ck.get("state_dict", ck).items()}
        miss, unexp = m.load_state_dict(sd, strict=False); assert not (set(miss) - {"mu", "sigma"}) and not unexp, (miss, unexp); return m
    if name == "Modas2021PRIMEResNet18":
        m = ResNet18(classes=10); ck = torch.load(path, map_location="cpu", weights_only=True); sd = {k.replace("module.", "", 1): v for k, v in ck.get("state_dict", ck).items()}
        miss, unexp = m.load_state_dict(sd, strict=False); assert not (set(miss) - {"mu", "sigma"}) and not unexp, (miss, unexp); return m
    wrn = _module(os.path.join(here, "arch_wide_resnet.py")); half = torch.tensor([0.5] * 3).view(1, 3, 1, 1)
    inner, mu, sigma = {"Hendrycks2020AugMix_WRN": lambda: (wrn.WideResNet(depth=40, widen_factor=2, sub_block1=False, num_classes=10), half, half), "Addepalli2021Towards_WRN34": lambda: (wrn.WideResNet(num_classes=10, depth=34, sub_block1=True), None, None)}[name]()
    ck = torch.load(path, map_location="cpu", weights_only=False); sd = ck.get("state_dict", ck) if hasattr(ck, "get") else ck
    sd = {k.replace("module.", "", 1).replace("model.", "", 1): v for k, v in sd.items()}
    if "mu" in sd: mu, sigma = sd.pop("mu"), sd.pop("sigma")
    miss, unexp = inner.load_state_dict(sd, strict=False); assert not miss and not unexp, (name, miss[:5], unexp[:5]); return Norm(inner, mu, sigma)

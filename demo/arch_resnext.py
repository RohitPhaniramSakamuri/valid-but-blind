"""ResNeXt-29 used in Experiment 003, copied unchanged."""
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

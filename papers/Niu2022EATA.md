# Efficient Test-Time Model Adaptation without Forgetting

Citation key: `Niu2022EATA`.
Authors: Shuaicheng Niu; Jiaxiang Wu; Yifan Zhang; Yaofo Chen; Shijian Zheng; Peilin Zhao; Mingkui Tan.
Year and venue: 2022; ICML, PMLR 162:16888–16905.
Publication/version status: conference paper.
[Authoritative source](https://proceedings.mlr.press/v162/niu22a.html). No local PDF in this project.
Reading progress: official metadata, abstract and PDF first-page methodological introduction

## Research question and contribution

Filters reliable/nonredundant samples for entropy updates and regularizes important parameters against forgetting.

## Background needed

See the linked review for the decision variable and information regime; clarify prerequisites during reading.

## Reading notes

Inspected locations: Abstract; Section 1.

## Method and implementation

[Public implementation / author resource](https://github.com/mr-eggplant/EATA) The literature-review stage did not execute this paper's code or reproduce its benchmark. The later custom digit diagnostic is a separate surrogate study, described in the project README.

## Evidence and limitations

Selective sample updates and compute reduction already exist; selecting entire adaptation methods is a different variable.

## Connection to our research

This source constrains the proposed contribution; distinguish its actual decision and evidence access from our acquisition hypothesis. [Review](../outputs/shift-aware-tta-review.md).

## Possible experiment

Compare legal evidence and total cost under the [planned protocol](../experiments/001-policy-selection-pilot.md) where the source's task and method can be matched.

## Next reading step

Inspect remaining method, split and code details before choosing an implementation baseline or claiming the paper omits a specific test.

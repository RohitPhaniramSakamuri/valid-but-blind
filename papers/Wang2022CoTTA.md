# Continual Test-Time Domain Adaptation

Citation key: `Wang2022CoTTA`.
Authors: Qin Wang; Olga Fink; Luc Van Gool; Dengxin Dai.
Year and venue: 2022; CVPR.
Publication/version status: conference paper.
[Authoritative source](https://openaccess.thecvf.com/content/CVPR2022/html/Wang_Continual_Test-Time_Domain_Adaptation_CVPR_2022_paper.html). No local PDF in this project.
Reading progress: official metadata, abstract, first-page introduction and author README

## Research question and contribution

Weight/augmentation averaging and stochastic restoration maintain continual adaptation state.

## Background needed

See the linked review for the decision variable and information regime; clarify prerequisites during reading.

## Reading notes

Inspected locations: Abstract; Introduction, Figure 1.

## Method and implementation

[Public implementation / author resource](https://github.com/qinenergy/cotta) The literature-review stage did not execute this paper's code or reproduce its benchmark. The later custom digit diagnostic is a separate surrogate study, described in the project README.

## Evidence and limitations

Mechanisms already address nonstationary adaptation and forgetting; not a guarantee of safe policy selection.

## Connection to our research

This source constrains the proposed contribution; distinguish its actual decision and evidence access from our acquisition hypothesis. [Review](../outputs/shift-aware-tta-review.md).

## Possible experiment

Compare legal evidence and total cost under the [planned protocol](../experiments/001-policy-selection-pilot.md) where the source's task and method can be matched.

## Next reading step

Inspect remaining method, split and code details before choosing an implementation baseline or claiming the paper omits a specific test.

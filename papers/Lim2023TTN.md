# TTN: A Domain-Shift Aware Batch Normalization in Test-Time Adaptation

Citation key: `Lim2023TTN`.
Authors: Hyesu Lim; Byeonggeun Kim; Jaegul Choo; Sungha Choi.
Year and venue: 2023; ICLR 2023.
Publication/version status: Conference paper; arXiv 2302.05155.
[Authoritative source](https://arxiv.org/abs/2302.05155). No local PDF in this project.
Reading progress: Abstract and author project-page sections on layer/channel shift sensitivity and post-training.

## Research question and contribution

Combines source and current-batch normalization using layer/channel shift sensitivity; shifts alter appropriate reliance on source/test statistics.

## Background needed

See the linked review for the decision variable and information regime; clarify prerequisites during reading.

## Reading notes

Inspected locations: Method: Test-Time Normalization Layer; Post-training prior; Optimize interpolating weights.

## Method and implementation

Implementation availability not established by this review. The literature-review stage did not execute this paper's code or reproduce its benchmark. The later custom digit diagnostic is a separate surrogate study, described in the project README.

## Evidence and limitations

Interpolation weights are learned using labeled source data during post-training and frozen at deployment. Do not conflate this with label-free source preparation or whole-method routing.

## Connection to our research

This source constrains the proposed contribution; distinguish its actual decision and evidence access from our acquisition hypothesis. [Review](../outputs/shift-aware-tta-review.md).

## Possible experiment

Compare legal evidence and total cost under the [planned protocol](../experiments/001-policy-selection-pilot.md) where the source's task and method can be matched.

## Next reading step

Inspect remaining method, split and code details before choosing an implementation baseline or claiming the paper omits a specific test.

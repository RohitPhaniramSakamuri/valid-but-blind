# Benchmarking Neural Network Robustness to Common Corruptions and Perturbations

Citation key: `Hendrycks2019Corruptions`.
Authors: Dan Hendrycks; Thomas Dietterich.
Year and venue: 2019; ICLR 2019.
Publication/version status: Conference paper.
[Authoritative source](https://arxiv.org/abs/1903.12261). No local PDF in this project.
Reading progress: Abstract and official dataset repository README

## Research question and contribution

Standard corruption benchmarks and deterministic stored evaluation data.

## Background needed

See the linked review for the decision variable and information regime; clarify prerequisites during reading.

## Reading notes

Inspected locations: Abstract; repository ImageNet-C and CIFAR download/evaluation notes.

## Method and implementation

[Public implementation / author resource](https://github.com/hendrycks/robustness) The literature-review stage did not execute this paper's code or reproduce its benchmark. The later custom digit diagnostic is a separate surrogate study, described in the project README.

## Evidence and limitations

Generated corruption tests do not establish performance on naturally occurring deployment shifts.

## Connection to our research

This source constrains the proposed contribution; distinguish its actual decision and evidence access from our acquisition hypothesis. [Review](../outputs/shift-aware-tta-review.md).

## Possible experiment

Compare legal evidence and total cost under the [planned protocol](../experiments/001-policy-selection-pilot.md) where the source's task and method can be matched.

## Next reading step

Inspect remaining method, split and code details before choosing an implementation baseline or claiming the paper omits a specific test.

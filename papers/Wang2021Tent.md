# Tent: Fully Test-Time Adaptation by Entropy Minimization

Citation key: `Wang2021Tent`.
Authors: Dequan Wang; Evan Shelhamer; Shaoteng Liu; Bruno Olshausen; Trevor Darrell.
Year and venue: 2021; ICLR.
Publication/version status: conference paper; preprint first posted 2020.
[Authoritative source](https://arxiv.org/abs/2006.10726). No local PDF in this project.
Reading progress: abstract, conference PDF first page and method overview

## Research question and contribution

Updates normalization statistics and affine transformations with entropy minimization on unlabeled test batches.

## Background needed

See the linked review for the decision variable and information regime; clarify prerequisites during reading.

## Reading notes

Inspected locations: Abstract; Introduction.

## Method and implementation

[Public implementation / author resource](https://github.com/DequanWang/tent) The literature-review stage did not execute this paper's code or reproduce its benchmark. The later custom digit diagnostic is a separate surrogate study, described in the project README.

## Evidence and limitations

A low-entropy objective is not direct evidence of correctness; no whole-policy selector in the inspected passages.

## Connection to our research

This source constrains the proposed contribution; distinguish its actual decision and evidence access from our acquisition hypothesis. [Review](../outputs/shift-aware-tta-review.md).

## Possible experiment

Compare legal evidence and total cost under the [planned protocol](../experiments/001-policy-selection-pilot.md) where the source's task and method can be matched.

## Next reading step

Inspect remaining method, split and code details before choosing an implementation baseline or claiming the paper omits a specific test.

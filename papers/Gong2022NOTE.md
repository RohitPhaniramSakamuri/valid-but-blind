# NOTE: Robust Continual Test-time Adaptation Against Temporal Correlation

Citation key: `Gong2022NOTE`.
Authors: Taesik Gong; Jongheon Jeong; Taewon Kim; Yewon Kim; Jinwoo Shin; Sung-Ju Lee.
Year and venue: 2022; NeurIPS 35.
Publication/version status: conference paper.
[Authoritative source](https://papers.nips.cc/paper_files/paper/2022/hash/ae6c7dbd9429b3a75c41b5fb47e57c9e-Abstract-Conference.html). No local PDF in this project.
Reading progress: official metadata and abstract; author repository README

## Research question and contribution

Instance-aware normalization and prediction-balanced reservoir sampling mitigate temporal correlation.

## Background needed

See the linked review for the decision variable and information regime; clarify prerequisites during reading.

## Reading notes

Inspected locations: Abstract.

## Method and implementation

[Public implementation / author resource](https://github.com/TaesikGong/NOTE) The literature-review stage did not execute this paper's code or reproduce its benchmark. The later custom digit diagnostic is a separate surrogate study, described in the project README.

## Evidence and limitations

An IID-only selector test would ignore a long-established threat.

## Connection to our research

This source constrains the proposed contribution; distinguish its actual decision and evidence access from our acquisition hypothesis. [Review](../outputs/shift-aware-tta-review.md).

## Possible experiment

Compare legal evidence and total cost under the [planned protocol](../experiments/001-policy-selection-pilot.md) where the source's task and method can be matched.

## Next reading step

Inspect remaining method, split and code details before choosing an implementation baseline or claiming the paper omits a specific test.

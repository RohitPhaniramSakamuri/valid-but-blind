# DATTA: Domain Diversity Aware Test-Time Adaptation for Dynamic Domain Shift Data Streams

Citation key: `Ye2025DATTA`.
Authors: Chuyang Ye; Dongyan Wei; Zhendong Liu; Yuanyi Pang; Yixi Lin; Qinting Jiang; Jingyan Jiang; Dongbiao He.
Year and venue: 2025; ICME 2025.
Publication/version status: Accepted oral per author arXiv record; DOI 10.1109/ICME59968.2025.11209053; preprint first2024, v2 Dec2025 inspected.
[Authoritative source](https://arxiv.org/abs/2408.08056). No local PDF in this project.
Reading progress: Abstract, introduction, method overview and section headings.

## Research question and contribution

Recognizes single-versus-multiple-domain batches, changes normalization interpolation and selectively fine-tunes to mitigate gradient conflict.

## Background needed

See the linked review for the decision variable and information regime; clarify prerequisites during reading.

## Reading notes

Inspected locations: Section III-A Domain-Diversity Discrimination; Section III-B DABN; Section III-C DAFT.

## Method and implementation

[Public implementation / author resource](https://github.com/DYW77/DATTA) The literature-review stage did not execute this paper's code or reproduce its benchmark. The later custom digit diagnostic is a separate surrogate study, described in the project README.

## Evidence and limitations

Domain diversity is not physical shift-cause identification. Dynamic heterogeneous input batches already studied; a generic multi-domain claim is insufficient.

## Connection to our research

This source constrains the proposed contribution; distinguish its actual decision and evidence access from our acquisition hypothesis. [Review](../outputs/shift-aware-tta-review.md).

## Possible experiment

Compare legal evidence and total cost under the [planned protocol](../experiments/001-policy-selection-pilot.md) where the source's task and method can be matched.

## Next reading step

Inspect remaining method, split and code details before choosing an implementation baseline or claiming the paper omits a specific test.

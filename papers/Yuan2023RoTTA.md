# Robust Test-Time Adaptation in Dynamic Scenarios

Citation key: `Yuan2023RoTTA`.
Authors: Longhui Yuan; Binhui Xie; Shuang Li.
Year and venue: 2023; CVPR, pp.15922–15932.
Publication/version status: conference paper.
[Authoritative source](https://openaccess.thecvf.com/content/CVPR2023/html/Yuan_Robust_Test-Time_Adaptation_in_Dynamic_Scenarios_CVPR_2023_paper.html). No local PDF in this project.
Reading progress: official metadata/abstract and introduction/method overview

## Research question and contribution

Robust normalization, balanced/timely memory and teacher-student updates jointly address changing domains and correlated sampling.

## Background needed

See the linked review for the decision variable and information regime; clarify prerequisites during reading.

## Reading notes

Inspected locations: Section 1; Table 1; batch-size comparison passage.

## Method and implementation

[Public implementation / author resource](https://github.com/BIT-DA/RoTTA) The literature-review stage did not execute this paper's code or reproduce its benchmark. The later custom digit diagnostic is a separate surrogate study, described in the project README.

## Evidence and limitations

Continual joint-stream realism is already studied; memory, teacher and update frequency must be included in fairness accounting.

## Connection to our research

This source constrains the proposed contribution; distinguish its actual decision and evidence access from our acquisition hypothesis. [Review](../outputs/shift-aware-tta-review.md).

## Possible experiment

Compare legal evidence and total cost under the [planned protocol](../experiments/001-policy-selection-pilot.md) where the source's task and method can be matched.

## Next reading step

Inspect remaining method, split and code details before choosing an implementation baseline or claiming the paper omits a specific test.

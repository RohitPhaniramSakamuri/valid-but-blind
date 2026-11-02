# Shift-ACT: Test-time adaptation via shift-aware class-specific dynamic thresholding for domain generalization

Citation key: `Karimi2026ShiftACT`.
Authors: Saeed Karimi; Hamdi Dibeklioglu.
Year and venue: 2026; Neurocomputing 663, article132013.
Publication/version status: Published28January2026, DOI10.1016/j.neucom.2025.132013.
[Authoritative source](https://www.sciencedirect.com/science/article/pii/S0925231225026852). No local PDF in this project.
Reading progress: Publisher abstract/metadata and author repository README.

## Research question and contribution

Class-specific source-target confidence gaps adjust thresholds; reliable samples get entropy minimization, unreliable samples get prototype contrastive alignment.

## Background needed

See the linked review for the decision variable and information regime; clarify prerequisites during reading.

## Reading notes

Inspected locations: Abstract; Repository preparation/run instructions.

## Method and implementation

[Public implementation / author resource](https://github.com/saeedkarimi90/Shift-act) The literature-review stage did not execute this paper's code or reproduce its benchmark. The later custom digit diagnostic is a separate surrogate study, described in the project README.

## Evidence and limitations

Source-derived class confidence information required; selected method passages/full detailed protocol not read. Class-wise signal-dependent objective choice is already present.

## Connection to our research

This source constrains the proposed contribution; distinguish its actual decision and evidence access from our acquisition hypothesis. [Review](../outputs/shift-aware-tta-review.md).

## Possible experiment

Compare legal evidence and total cost under the [planned protocol](../experiments/001-policy-selection-pilot.md) where the source's task and method can be matched.

## Next reading step

Inspect remaining method, split and code details before choosing an implementation baseline or claiming the paper omits a specific test.

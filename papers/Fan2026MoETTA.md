# MoETTA: Test-Time Adaptation Under Mixed Distribution Shifts with MoE-LayerNorm

Citation key: `Fan2026MoETTA`.
Authors: Xiao Fan; Jingyan Jiang; Zhaoru Chen; Fanding Huang; Xiao Chen; Qinting Jiang; Bowen Zhang; Xing Tang; Zhi Wang.
Year and venue: 2026; AAAI2026 Main Technical Track.
Publication/version status: Acceptance reported by authorarXiv; firstpreprint14November2025; v1 inspected.
[Authoritative source](https://arxiv.org/abs/2511.13760). No local PDF in this project.
Reading progress: Abstract,introduction,routing/mechanism description and §5.3/table excerpts.

## Research question and contribution

LayerNorm experts permit sample-specific gradient directions under mixed shifts; potpourri mixes natural/artistic/adversarial shifts, potpourri+ includes source examples.

## Background needed

See the linked review for the decision variable and information regime; clarify prerequisites during reading.

## Reading notes

Inspected locations: Mixture-of-Experts LayerNorm routing; 5.3 Computation Efficiency; Potpourri/potpourri+ design.

## Method and implementation

[Public implementation / author resource](https://github.com/AnikiFan/MoETTA) The literature-review stage did not execute this paper's code or reproduce its benchmark. The later custom digit diagnostic is a separate surrogate study, described in the project README.

## Evidence and limitations

Mixed domains/source returns are covered as benchmarks; action-menu policy selection and image-level composed corruptions remain distinct, but no novelty inferred from this distinction.

## Connection to our research

This source constrains the proposed contribution; distinguish its actual decision and evidence access from our acquisition hypothesis. [Review](../outputs/shift-aware-tta-review.md).

## Possible experiment

Compare legal evidence and total cost under the [planned protocol](../experiments/001-policy-selection-pilot.md) where the source's task and method can be matched.

## Next reading step

Inspect remaining method, split and code details before choosing an implementation baseline or claiming the paper omits a specific test.

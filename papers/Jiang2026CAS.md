# To Adapt or Not to Adapt? Selective Adaptation for Vision-Language Models

Citation key: `Jiang2026CAS`.
Authors: Siru Jiang; Yuwei Liang; Jian Liang; Ran He; Tieniu Tan.
Year and venue: 2026; arXiv:2609.08367v1; author record comments identify ECCV 2026.
Publication/version status: Preprint submitted 8 September 2026; ECCV 2026 is stated on primary arXiv record, proceedings metadata not independently checked by reviewer.
[Authoritative source](https://arxiv.org/abs/2609.08367v1). No local PDF in this project.
Reading progress: Primary arXiv metadata and full HTML sections 2–3.3, including episodic scope and the CAS decision rule; no code audit.

## Research question and contribution

Cross-Augmentation Similarity decides whether to perform or skip a VLM adaptation, directly overlapping extra-view evidence for an update/no-update decision.

## Background needed

See the linked review for the decision variable and information regime; clarify prerequisites during reading.

## Reading notes

Inspected locations: Abstract; Section 3.2; Section 3.3.

## Method and implementation

[Public implementation / author resource](https://github.com/sirujiang/selective-adaptation) The literature-review stage did not execute this paper's code or reproduce its benchmark. The later custom digit diagnostic is a separate surrogate study, described in the project README.

## Evidence and limitations

The candidate needs multi-action value-based evidence acquisition beyond this fixed view-based skip rule. Adaptation skipping is not itself new.

## Connection to our research

This source constrains the proposed contribution; distinguish its actual decision and evidence access from our acquisition hypothesis. [Review](../outputs/shift-aware-tta-review.md).

## Possible experiment

Compare legal evidence and total cost under the [planned protocol](../experiments/001-policy-selection-pilot.md) where the source's task and method can be matched.

## Next reading step

Inspect remaining method, split and code details before choosing an implementation baseline or claiming the paper omits a specific test.

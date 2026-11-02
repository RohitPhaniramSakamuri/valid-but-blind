# When Does Test-Time Physical Diagnosis Pay? A Frozen Policy Buys Evidence It Never Reads

Citation key: `Zhang2026PhysicalDiagnosis`.
Authors: Zhengshu Zhang.
Year and venue: 2026; arXiv:2609.22299v1.
Publication/version status: Preprint submitted 14 September 2026.
[Authoritative source](https://arxiv.org/abs/2609.22299v1). No local PDF in this project.
Reading progress: Primary metadata, abstract and introduction; full experiments not audited

## Research question and contribution

Separates identifying context, using acquired evidence, decision value, selection value over a fixed action and safe realization. Supports distinct headroom/evidence-use diagnostics.

## Background needed

See the linked review for the decision variable and information regime; clarify prerequisites during reading.

## Reading notes

Inspected locations: Abstract; Section 1.

## Method and implementation

Implementation availability not established by this review. The literature-review stage did not execute this paper's code or reproduce its benchmark. The later custom digit diagnostic is a separate surrogate study, described in the project README.

## Evidence and limitations

Robotics rather than visual-classification TTA; cannot be treated as a matched numerical baseline or proof that the candidate is novel.

## Connection to our research

This source constrains the proposed contribution; distinguish its actual decision and evidence access from our acquisition hypothesis. [Review](../outputs/shift-aware-tta-review.md).

## Possible experiment

Compare legal evidence and total cost under the [planned protocol](../experiments/001-policy-selection-pilot.md) where the source's task and method can be matched.

## Next reading step

Inspect remaining method, split and code details before choosing an implementation baseline or claiming the paper omits a specific test.

# MoASE++: Mixture of Activation Sparsity Experts with Domain-Adaptive On-policy Distillation for Continual Test Time Adaptation

Citation key: `Zhang2026MoASEPlusPlus`.
Authors: Ronyu Zhang; Aosong Cheng; Gaole Dai; Yulin Luo; Jiaming Liu; Li Du; Huanrui Yang; Dan Wang; Leyuan Fang; Yuan Du; Shanghang Zhang.
Year and venue: 2026; arXiv preprint.
Publication/version status: arXiv2605.17743v1,18May2026; no venueverified.
[Authoritative source](https://arxiv.org/abs/2605.17743). [Local PDF](../sources/pdfs/Zhang2026MoASEPlusPlus.pdf)
Reading progress: Abstract, routing description and section 5.2 including equations 11–16 from downloaded PDF; partial reading.

## Research question and contribution

Domain-aware router weights experts using texture cues; entropy/confidence condition augmentation policy and EMA distillation.

## Background needed

See the linked review for the decision variable and information regime; clarify prerequisites during reading.

## Reading notes

Inspected locations: Section 5.2; Equations 11–16.

## Method and implementation

Implementation availability not established by this review. The literature-review stage did not execute this paper's code or reproduce its benchmark. The later custom digit diagnostic is a separate surrogate study, described in the project README.

## Evidence and limitations

Learned augmentation strength uses a teacher-distillation/strength reward. That is close prior art for policy-driven augmentation, not an audited costed whole-method evidence selector. No implementation execution.

## Connection to our research

This source constrains the proposed contribution; distinguish its actual decision and evidence access from our acquisition hypothesis. [Review](../outputs/shift-aware-tta-review.md).

## Possible experiment

Compare legal evidence and total cost under the [planned protocol](../experiments/001-policy-selection-pilot.md) where the source's task and method can be matched.

## Next reading step

Inspect remaining method, split and code details before choosing an implementation baseline or claiming the paper omits a specific test.

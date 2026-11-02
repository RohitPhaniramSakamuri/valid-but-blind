# Channel-Selective Normalization for Label-Shift Robust Test-Time Adaptation

Citation key: `Vianna2025ChannelSelective`.
Authors: Pedro Vianna; Muawiz Sajjad Chaudhary; Paria Mehrbod; An Tang; Guy Cloutier; Guy Wolf; Michael Eickenberg; Eugene Belilovsky.
Year and venue: 2025; Proceedings of The 3rd Conference on Lifelong Learning Agents, PMLR 274:514–533.
Publication/version status: Published proceedings record uses year 2025; record event/version dates separately if expanded.
[Authoritative source](https://proceedings.mlr.press/v274/vianna25a.html). No local PDF in this project.
Reading progress: Primary proceedings metadata and abstract only during approach selection; full method not read

## Research question and contribution

Selective normalization channels reduce label-shift sensitivity; evaluates covariate and label shifts together on CIFAR10-C, ImageNet-C and fatty-liver classification.

## Background needed

See the linked review for the decision variable and information regime; clarify prerequisites during reading.

## Reading notes

Inspected locations: Abstract; Official BibTeX.

## Method and implementation

Implementation availability not established by this review. The literature-review stage did not execute this paper's code or reproduce its benchmark. The later custom digit diagnostic is a separate surrogate study, described in the project README.

## Evidence and limitations

Direct predecessor for imbalance-aware normalization. A simple SOURCE/normalization gate and showing normalization fails under imbalance do not establish novelty. Exact matched-concentration evaluation overlap requires full-method inspection.

## Connection to our research

This source constrains the proposed contribution; distinguish its actual decision and evidence access from our acquisition hypothesis. [Review](../outputs/shift-aware-tta-review.md).

## Possible experiment

Compare legal evidence and total cost under the [planned protocol](../experiments/001-policy-selection-pilot.md) where the source's task and method can be matched.

## Next reading step

Inspect remaining method, split and code details before choosing an implementation baseline or claiming the paper omits a specific test.

## Literature refresh — 26 October 2026

Primary source: [Channel-Selective Normalization for Label-Shift Robust Test-Time Adaptation](https://proceedings.mlr.press/v274/vianna25a.html).

Reading scope: Official metadata and downloaded official PDF §§3-5, Algorithms 1-2, selected result descriptions; partial reading.

Inspected locations: Section 3; Algorithms 1-2; Section 4 Adaptation Details; Section 5 Limitations.

Relevance (our reading): Source-labeled class/channel sensitivity scores; uniform-prior adaptation pass followed by pseudolabel-based prior rescoring. Direct predecessor for selective normalization under combined covariate/label shift.

Boundary / reviewer qualification: BN networks and labeled-source post-training preparation; offline single-batch setting with batch500 for CIFAR/ImageNet rather than a learned closed-loop persistent selector.

Publication qualification: PMLR volume published 2025 for the 3rd CoLLAs conference held 2024; established citation key preserved. Official PDF selectively read during refresh.

No code or benchmark was run for this refresh. [Current synthesis](../outputs/shift-aware-tta-deep-review-2026-10-26.md). Detailed reading histories and original metadata remain in [catalog](../sources/catalog.json).

[Preserved primary PDF](../notes/review-refresh-2026-10-26/verifier-evidence/Vianna2025ChannelSelective.pdf).

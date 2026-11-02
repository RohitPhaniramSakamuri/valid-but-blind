# Hybrid-TTA: Continual Test-time Adaptation via Dynamic Domain Shift Detection

Citation key: `Park2025HybridTTA`.
Authors: Hyewon Park; Hyejin Park; Jueun Ko; Dongbo Min.
Year and venue: 2025; ICCV 2025.
Publication/version status: Conference paper; arXiv first September 2024, inspected v2 August 2025.
[Authoritative source](https://arxiv.org/abs/2409.08566). No local PDF in this project.
Reading progress: Abstract, introduction, section 4 mechanism and experiment/appendix headings; selected results, not exhaustive full paper.

## Research question and contribution

Teacher/student discrepancy with dynamic loss thresholding detects domain changes and switches between full tuning and adapter tuning for each input.

## Background needed

See the linked review for the decision variable and information regime; clarify prerequisites during reading.

## Reading notes

Inspected locations: Section 4.1 Dynamic Domain Shift Detection; Section 4.2 Masked Image Modeling Adaptation; Section 5; Appendix source forgetting/long-term adaptation.

## Method and implementation

Implementation availability not established by this review. The literature-review stage did not execute this paper's code or reproduce its benchmark. The later custom digit diagnostic is a separate surrogate study, described in the project README.

## Evidence and limitations

Segmentation-specific FT/ET menu and reconstruction preparation; not a general selector over arbitrary TTA algorithms. Still invalidates broad novelty of dynamic policy switching.

## Connection to our research

This source constrains the proposed contribution; distinguish its actual decision and evidence access from our acquisition hypothesis. [Review](../outputs/shift-aware-tta-review.md).

## Possible experiment

Compare legal evidence and total cost under the [planned protocol](../experiments/001-policy-selection-pilot.md) where the source's task and method can be matched.

## Next reading step

Inspect remaining method, split and code details before choosing an implementation baseline or claiming the paper omits a specific test.

## Literature refresh — 26 October 2026

Primary source: [Hybrid-TTA: Continual Test-time Adaptation via Dynamic Domain Shift Detection](https://arxiv.org/html/2409.08566v2).

Reading scope: Fresh arXiv v2 HTML selective reading; primary arXiv metadata and official CVF search result checked.

Inspected locations: Sections 4.1.1–4.1.2; Section 4.2; Section 5.4.

Relevance (our reading): Evolving student/EMA-teacher discrepancy and dynamic threshold switch full versus adapter tuning.

Boundary / reviewer qualification: Already uses current/historical model state. No inspected same-current-data/different-history action-ranking experiment or learned per-action utility target.

Publication qualification: Conference paper; arXiv first September 2024, inspected v2 August 2025

No code or benchmark was run for this refresh. [Current synthesis](../outputs/shift-aware-tta-deep-review-2026-10-26.md). Detailed reading histories and original metadata remain in [catalog](../sources/catalog.json).

## Reading update 2026-10-31

§4.1 and supplement: hand-set loss-EMA rule; values chosen on a subset of the first target domain. Locations: Section 4.1, Supplement. See the [dossier](../outputs/novelty-dossier-2026-10-31.md).

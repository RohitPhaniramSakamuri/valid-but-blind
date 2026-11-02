# MORPHEUS: Meta Test-Time Adaptation via Neural Collapse Geometry

Citation key: `Danilowski2026MORPHEUS`.
Authors: Michal Danilowski; Alexander Murphy; Young D. Kwon; Abhirup Ghosh.
Year and venue: 2026; ICLR 2026 Test-Time Updates Workshop.
Publication/version status: Workshop paper, not main-track ICLR; author research page corroborates.
[Authoritative source](https://openreview.net/forum?id=YfyApJH1Rj). [Local PDF](../sources/pdfs/Danilowski2026MORPHEUS.pdf)
Reading progress: Author PDF downloaded; abstract, sections 1–3, meta-training description and selected appendix/table passages read. Workshop status checked against PDF header and author publication page.

## Research question and contribution

Predicts per-TTA post-adaptation accuracy from source-model entropy and Neural-Collapse embedding statistics, then selects a complete TTA method without executing all candidates. Direct collision with a learned pre-adaptation router.

## Background needed

See the linked review for the decision variable and information regime; clarify prerequisites during reading.

## Reading notes

Inspected locations: Section 2, Problem and Methodology; Section 3; Appendix split descriptions.

## Method and implementation

Implementation availability not established by this review. The literature-review stage did not execute this paper's code or reproduce its benchmark. The later custom digit diagnostic is a separate surrogate study, described in the project README.

## Evidence and limitations

Supervised auxiliary-domain development precedes unlabeled selection. Text/table numbers and feature definitions need care; no numerical result is copied as our reproduction. Official code not verified.

## Connection to our research

This source constrains the proposed contribution; distinguish its actual decision and evidence access from our acquisition hypothesis. [Review](../outputs/shift-aware-tta-review.md).

## Possible experiment

Compare legal evidence and total cost under the [planned protocol](../experiments/001-policy-selection-pilot.md) where the source's task and method can be matched.

## Next reading step

Inspect remaining method, split and code details before choosing an implementation baseline or claiming the paper omits a specific test.

## Literature refresh — 26 October 2026

Primary source: [MORPHEUS: Meta Test-Time Adaptation via Neural Collapse Geometry](https://theyoungkwon.github.io/papers/articles/danilowski_morpheus_iclr-ttu26.pdf).

Reading scope: Fresh author-hosted PDF selective reading; method, experimental setup and appendix feature definitions.

Inspected locations: PDF header; Section 2; Section 3; Appendix B.

Relevance (our reading): Source entropy and pseudo-label neural-collapse geometry feed random-forest predictions of whole-method post-adaptation accuracy before executing the chosen method.

Boundary / reviewer qualification: Auxiliary labeled outcomes train predictors. Inspected setting starts from source model/domain data; does not establish autonomous state-history generalization.

Publication qualification: Workshop paper, not main-track ICLR; author research page corroborates

No code or benchmark was run for this refresh. [Current synthesis](../outputs/shift-aware-tta-deep-review-2026-10-26.md). Detailed reading histories and original metadata remain in [catalog](../sources/catalog.json).

[Preserved primary PDF](../sources/pdfs/Danilowski2026MORPHEUS.pdf).

## Reading update 2026-10-31

Saved text §§1–3 and Table 1. Our arithmetic: per-corruption oracle 65.75% versus SPA 65.25%. Locations: Sections 1–3, Table 1. See the [dossier](../outputs/novelty-dossier-2026-10-31.md).

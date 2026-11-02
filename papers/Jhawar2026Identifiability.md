# When is Test-Time Adaptation Identifiable From Unlabeled Evidence?

Citation key: `Jhawar2026Identifiability`.
Authors: Kartik Jhawar; Lipo Wang.
Year and venue: 2026; arXiv.
Publication/version status: preprint v1, submitted 10 September 2026.
[Authoritative source](https://arxiv.org/abs/2609.11235). [Local PDF](../sources/pdfs/Jhawar2026Identifiability.pdf)
Reading progress: Sections 2–7 and Appendix B

## Research question and contribution

SOURCE/KEEP plus modern TTA menu, prior/stream-regime changes, order-aware pre-action evidence, held-out corruption/transfer evaluation, regret and negative-transfer metrics.

## Background needed

See the linked review for the decision variable and information regime; clarify prerequisites during reading.

## Reading notes

Inspected locations: Section 3.5; Sections 4.1–4.3; Sections 5.1–5.4; Section 7; Appendix B.5.

## Method and implementation

Implementation availability not established by this review. The literature-review stage did not execute this paper's code or reproduce its benchmark. The later custom digit diagnostic is a separate surrogate study, described in the project README.

## Evidence and limitations

Finite action menu and main source-model family; evidence sufficiency depends on deployment family. Does not evaluate costed active evidence acquisition or claim universally superior evidence.

## Connection to our research

This source constrains the proposed contribution; distinguish its actual decision and evidence access from our acquisition hypothesis. [Review](../outputs/shift-aware-tta-review.md).

## Possible experiment

Compare legal evidence and total cost under the [planned protocol](../experiments/001-policy-selection-pilot.md) where the source's task and method can be matched.

## Next reading step

Inspect remaining method, split and code details before choosing an implementation baseline or claiming the paper omits a specific test.

## Literature refresh — 26 October 2026

Primary source: [When is Test-Time Adaptation Identifiable From Unlabeled Evidence?](https://arxiv.org/abs/2609.11235).

Reading scope: Fresh arXiv HTML selective reading: setup, theory, complete experimental design, limitations and experimental appendix.

Inspected locations: Sections 2–5; Section 7; Appendix B.

Relevance (our reading): Same unlabeled evidence can conceal action reversals; stream structure, prior mechanism and batch size affect selection. SOURCE is an explicit action.

Boundary / reviewer qualification: Section 4.1 starts every action from the same frozen source per world. No arbitrary-deployment or universal evidence guarantee; live policy-induced state study not inspected.

Publication qualification: preprint v1, submitted 10 September 2026

No code or benchmark was run for this refresh. [Current synthesis](../outputs/shift-aware-tta-deep-review-2026-10-26.md). Detailed reading histories and original metadata remain in [catalog](../sources/catalog.json).

[Preserved primary PDF](../sources/pdfs/Jhawar2026Identifiability.pdf).

## Reading update 2026-10-31

§4.1, Table 1, §5.2 and §7 rechecked; paper marked under review at ICLR 2027. Locations: Section 4.1, Table 1, Section 7. See the [dossier](../outputs/novelty-dossier-2026-10-31.md).

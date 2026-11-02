# Agentic-TTT: Training test-time policy for test-time training

Citation key: `Lu2026AgenticTTT`.
Authors: Jiahao Lu; Mohan Kankanhalli.
Publication: 2026; arXiv preprint2610.12002.
Status: selectively inspected; not a replication.

## Literature refresh — 26 October 2026

Primary source: [Agentic-TTT: Training test-time policy for test-time training](https://arxiv.org/abs/2610.12002).

Reading scope: Metadata, introduction, §2.2.2, execution-harness descriptions and AppendixE limitations. Partial reading.

Inspected locations: Section2.2.2; AppendixD.1; AppendixE: Cross-query credit assignment.

Relevance (our reading): Learned state-conditioned method selection with same-snapshot local counterfactuals; explicitly identifies gold-history/autonomous-history exposure bias and leaves autonomous-stream credit assignment open.

Boundary / reviewer qualification: Isolated LoRA skill library over frozen LLM, gold-generated training successor states and query-level reward; benefit-enriched benchmark. Not a continual shared-weights visual TTA evaluation.

Publication qualification: arXiv v1 submitted8October2026; no independently verified venue

No code or benchmark was run for this refresh. [Current synthesis](../outputs/shift-aware-tta-deep-review-2026-10-26.md). Detailed reading histories and original metadata remain in [catalog](../sources/catalog.json).

## Reading update 2026-10-31

Fresh text of §2.2.2 and Appendix E; quotations checked. Locations: Section 2.2.2, Appendix E. See the [dossier](../outputs/novelty-dossier-2026-10-31.md).

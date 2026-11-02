# MEMO: Test Time Robustness via Adaptation and Augmentation

Citation key: `Zhang2022MEMO`.
Authors: Marvin Zhang; Sergey Levine; Chelsea Finn.
Publication: 2022; NeurIPS 2022, Advances in Neural Information Processing Systems 35.
Status: selectively inspected; not a replication.

## Literature refresh — 26 October 2026

Primary source: [MEMO: Test Time Robustness via Adaptation and Augmentation](https://papers.neurips.cc/paper_files/paper/2022/hash/fc28053a08f59fccb48b11f2e31e81c7-Abstract-Conference.html).

Reading scope: Official metadata/abstract and PDF introductory method description.

Inspected locations: Abstract; Introduction.

Relevance (our reading): Minimizes entropy of predictions averaged over augmented views of one input; removes a multi-input batch requirement.

Boundary / reviewer qualification: Our interpretation: multiple views and adaptation cost must be charged; the chosen transformations encode invariance assumptions that can fail under severe shifts.

Publication qualification: Official NeurIPS proceedings verified.

No code or benchmark was run for this refresh. [Current synthesis](../outputs/shift-aware-tta-deep-review-2026-10-26.md). Detailed reading histories and original metadata remain in [catalog](../sources/catalog.json).

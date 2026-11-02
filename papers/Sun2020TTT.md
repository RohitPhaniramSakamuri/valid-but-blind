# Test-Time Training with Self-Supervision for Generalization under Distribution Shifts

Citation key: `Sun2020TTT`.
Authors: Yu Sun; Xiaolong Wang; Zhuang Liu; John Miller; Alexei Efros; Moritz Hardt.
Publication: 2020; ICML 2020, PMLR 119:9229–9248.
Status: selectively inspected; not a replication.

## Literature refresh — 26 October 2026

Primary source: [Test-Time Training with Self-Supervision for Generalization under Distribution Shifts](https://proceedings.mlr.press/v119/sun20b.html).

Reading scope: Official metadata, abstract and PDF introduction/method summary, not full experimental audit.

Inspected locations: Abstract; Introduction; Section 4 overview.

Relevance (our reading): Learns from an auxiliary self-supervised task at test time; online variant retains updates. Gradient alignment gives a restricted condition for improvement.

Boundary / reviewer qualification: Requires source-stage preparation of the auxiliary task. Our interpretation: improvement of that task need not imply improvement of classification on a new shift.

Publication qualification: ICML 2020 official proceedings; linked 2019 preprint is the same work.

No code or benchmark was run for this refresh. [Current synthesis](../outputs/shift-aware-tta-deep-review-2026-10-26.md). Detailed reading histories and original metadata remain in [catalog](../sources/catalog.json).

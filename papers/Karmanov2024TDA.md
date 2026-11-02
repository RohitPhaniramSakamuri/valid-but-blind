# Efficient Test-Time Adaptation of Vision-Language Models

Citation key: `Karmanov2024TDA`.
Authors: Adilbek Karmanov; Dayan Guan; Shijian Lu; Abdulmotaleb El Saddik; Eric Xing.
Publication: 2024; CVPR 2024, pages 14162–14171.
Status: selectively inspected; not a replication.

## Literature refresh — 26 October 2026

Primary source: [Efficient Test-Time Adaptation of Vision-Language Models](https://openaccess.thecvf.com/content/CVPR2024/papers/Karmanov_Efficient_Test-Time_Adaptation_of_Vision-Language_Models_CVPR_2024_paper.pdf).

Reading scope: Official CVF PDF first page, efficiency/comparison passages and author repository.

Inspected locations: Abstract; Section 4.2; Tables 1–3.

Relevance (our reading): Dynamic positive/negative pseudo-label caches refine CLIP outputs without gradient updates; a useful inexpensive VLM reference.

Boundary / reviewer qualification: Our interpretation: caches depend on feature/pseudo-label quality and history. Backbone and natural-shift protocol must match; published timing is device-specific.

Publication qualification: Official CVF PDF verified; HTML access returned 403.

No code or benchmark was run for this refresh. [Current synthesis](../outputs/shift-aware-tta-deep-review-2026-10-26.md). Detailed reading histories and original metadata remain in [catalog](../sources/catalog.json).

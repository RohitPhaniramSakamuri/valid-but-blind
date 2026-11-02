# Rapid Network Adaptation: Learning to Adapt Neural Networks Using Test-Time Feedback

Citation key: `Yeo2023RNA`.
Authors: Teresa Yeo; Oğuzhan Fatih Kar; Zahra Sodagar; Amir Zamir.
Publication: 2023; ICCV 2023.
Status: selectively inspected; not a replication.

## Literature refresh — 26 October 2026

Primary source: [Rapid Network Adaptation: Learning to Adapt Neural Networks Using Test-Time Feedback](https://openaccess.thecvf.com/content/ICCV2023/papers/Yeo_Rapid_Network_Adaptation_Learning_to_Adapt_Neural_Networks_Using_Test-Time_ICCV_2023_paper.pdf).

Reading scope: Indexed official CVF PDF title block/abstract/introduction and author project feedback descriptions; direct CVF fetch returned 403, full training rollouts not audited.

Inspected locations: Abstract; Figure 1; Author project Employed Test-time Adaptation Signals.

Relevance (our reading): Learns an amortized adaptation controller from error feedback; closed-loop learned updates and controller terminology are prior art.

Boundary / reviewer qualification: Classification examples use coarse/retrieval feedback from labeled training images; depth uses sparse geometric feedback. Not a weights-only unlabeled comparator. Exact training-state coverage remains to check; project code link is not verified RNA code.

Publication qualification: Official ICCV PDF and author site verified; CVF HTML returned 403 during refresh.

No code or benchmark was run for this refresh. [Current synthesis](../outputs/shift-aware-tta-deep-review-2026-10-26.md). Detailed reading histories and original metadata remain in [catalog](../sources/catalog.json).

## Reading update 2026-10-31

arXiv v1 2309.15762 §3: original weights frozen; controller needs only a forward pass. CVF PDF still returned 403. Locations: Section 3. See the [dossier](../outputs/novelty-dossier-2026-10-31.md).

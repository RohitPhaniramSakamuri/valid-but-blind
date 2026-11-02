# Label Shift Adapter for Test-Time Adaptation under Covariate and Label Shifts

Citation key: `Park2023LSA`.
Authors: Sunghyun Park; Seunghan Yang; Jaegul Choo; Sungrack Yun.
Publication: 2023; Proceedings of the IEEE/CVF International Conference on Computer Vision, pages 16375-16385.
Status: selectively inspected; not a replication.

## Literature refresh — 26 October 2026

Primary source: [Label Shift Adapter for Test-Time Adaptation under Covariate and Label Shifts](https://arxiv.org/abs/2308.08810).

Reading scope: arXiv title/authors/abstract; official CVF PDF §5 and conclusion visible in primary index; partial reading.

Inspected locations: Abstract; Section 5 Discussions; Section 6 Conclusion.

Relevance (our reading): Estimates target label distribution and generates adaptation parameters conditional on it, integrating with existing TTA objectives.

Boundary / reviewer qualification: Additional source-stage adapter training; paper notes normalization hyperparameter sensitivity. Source and target imbalance adaptation already part of scope.

Publication qualification: ICCV 2023 official paper; linked arXiv preprint 2308.08810

No code or benchmark was run for this refresh. [Current synthesis](../outputs/shift-aware-tta-deep-review-2026-10-26.md). Detailed reading histories and original metadata remain in [catalog](../sources/catalog.json).

## Adversarial review — 2 November 2026

Sunghyun Park, Seunghan Yang, Jaegul Choo, Sungrack Yun. 2023. Proceedings of the IEEE/CVF International Conference on Computer Vision, pages 16375-16385. [Primary source](https://arxiv.org/abs/2308.08810).

Publication/version qualification: ICCV 2023 official paper; linked arXiv preprint 2308.08810

**Actual reading:** Primary arxiv PDF §3 adapter/prior estimation, §4/Tables1–2/§4.4 and §6 conclusion; main text only, referenced supplementary not independently audited.

**Locations:** §3; §4 Tables1–2; §4.4; §6

**Method/evidence and connection:** Combines corruption and forward/uniform/backward long-tailed class distributions; source/BN/Tent comparisons and prior-conditioned adapter. Source training can itself be long-tailed; no sequential alarms.

**Limit:** Additional source-stage adapter training; paper notes normalization hyperparameter sensitivity. Source and target imbalance adaptation already part of scope.

**Next reading step:** resolve access/version limits and the precise C1–C5 overlap before stronger claims. [Detailed claim review](../notes/novelty-review-2026-11-02/review.md); [source-level reading and extraction](../notes/novelty-review-2026-11-02/review.md). No experiments were run for this reading.

# Leveraging Unlabeled Data to Predict Out-of-Distribution Performance

Citation key: `Garg2022ATC`.
Authors: Saurabh Garg; Sivaraman Balakrishnan; Zachary C. Lipton; Behnam Neyshabur; Hanie Sedghi.
Publication: 2022; International Conference on Learning Representations.
Status: selectively inspected; not a replication.

## Literature refresh — 26 October 2026

Primary source: [Leveraging Unlabeled Data to Predict Out-of-Distribution Performance](https://arxiv.org/abs/2201.04234).

Reading scope: arXiv metadata/abstract; official ICLR Downloads listing; primary paper §3.1 and ATC discussion via author/institutional PDF. Partial reading.

Inspected locations: Section 3.1; ATC method and conclusion; ICLR official Downloads 2022.

Relevance (our reading): Source-calibrated confidence threshold estimates unlabeled target accuracy; impossibility result blocks arbitrary-shift accuracy identification.

Boundary / reviewer qualification: Requires labeled source validation; empirical target transfer of confidence/error relation is conditional and can fail. Accuracy estimation is distinct from selecting an intervention before adaptation.

Publication qualification: ICLR 2022 official program listing and paper header verified; arXiv v3 revised 15 October 2022

No code or benchmark was run for this refresh. [Current synthesis](../outputs/shift-aware-tta-deep-review-2026-10-26.md). Detailed reading histories and original metadata remain in [catalog](../sources/catalog.json).

## Adversarial review — 2 November 2026

Saurabh Garg, Sivaraman Balakrishnan, Zachary C. Lipton, Behnam Neyshabur, Hanie Sedghi. 2022. International Conference on Learning Representations. [Primary source](https://arxiv.org/abs/2201.04234).

Publication/version qualification: ICLR 2022 official program listing and paper header verified; arXiv v3 revised 15 October 2022

**Actual reading:** Primary PDF §§3.1–4/Proposition1/Corollary1/Example1, §5 experimental setup; AppendixA proof/example map. Not full proof verification.

**Locations:** §3.1 Proposition1/Corollary1/Example1; §4; §5

**Method/evidence and connection:** Target accuracy unidentifiable without assumptions even with source joint and target marginal; ATC calibrates a fixed classifier threshold. Not an adaptation-proof risk alarm.

**Limit:** Requires labeled source validation; empirical target transfer of confidence/error relation is conditional and can fail. Accuracy estimation is distinct from selecting an intervention before adaptation.

**Next reading step:** resolve access/version limits and the precise C1–C5 overlap before stronger claims. [Detailed claim review](../notes/novelty-review-2026-11-02/review.md); [source-level reading and extraction](../notes/novelty-review-2026-11-02/review.md). No experiments were run for this reading.

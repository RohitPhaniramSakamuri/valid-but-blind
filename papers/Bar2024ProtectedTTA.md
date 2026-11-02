# Protected Test-Time Adaptation via Online Entropy Matching: A Betting Approach

Citation key: `Bar2024ProtectedTTA`.
Authors: Yarin Bar; Shalev Shaer; Yaniv Romano.
Year and venue: 2024; NeurIPS 37.
Publication/version status: conference paper; inspected arXiv v1.
[Authoritative source](https://proceedings.neurips.cc/paper_files/paper/2024/hash/9b35a0a20d617dc68ae98a7a57df2f51-Abstract-Conference.html). No local PDF in this project.
Reading progress: official metadata, abstract and arXiv method outline

## Research question and contribution

Entropy-distribution shift detection dynamically drives an entropy-matching adaptation process.

## Background needed

See the linked review for the decision variable and information regime; clarify prerequisites during reading.

## Reading notes

Inspected locations: Section 3, POEM; Sections 3.3–3.5.

## Method and implementation

Implementation availability not established by this review. The literature-review stage did not execute this paper's code or reproduce its benchmark. The later custom digit diagnostic is a separate surrogate study, described in the project README.

## Evidence and limitations

Shift-triggered adaptation and protecting in-distribution behavior already exist; statistical detector guarantees should not be restated as universal classification-safety guarantees.

## Connection to our research

This source constrains the proposed contribution; distinguish its actual decision and evidence access from our acquisition hypothesis. [Review](../outputs/shift-aware-tta-review.md).

## Possible experiment

Compare legal evidence and total cost under the [planned protocol](../experiments/001-policy-selection-pilot.md) where the source's task and method can be matched.

## Next reading step

Inspect remaining method, split and code details before choosing an implementation baseline or claiming the paper omits a specific test.

## Adversarial review — 2 November 2026

Yarin Bar, Shalev Shaer, Yaniv Romano. 2024. NeurIPS 37. [Primary source](https://proceedings.neurips.cc/paper_files/paper/2024/hash/9b35a0a20d617dc68ae98a7a57df2f51-Abstract-Conference.html).

Publication/version qualification: conference paper; inspected arXiv v1

**Actual reading:** §§2–4/Figures1,3/AppendicesF.4,G; S2 all27 citations and110 reference metadata screened.

**Locations:** §§2–4; AppendicesF.4,G

**Method/evidence and connection:** Betting/entropy monitoring controls adaptation; label-prior caveats already recognized.

**Limit:** Shift-triggered adaptation and protecting in-distribution behavior already exist; statistical detector guarantees should not be restated as universal classification-safety guarantees.

**Next reading step:** resolve access/version limits and the precise C1–C5 overlap before stronger claims. [Detailed claim review](../notes/novelty-review-2026-11-02/review.md); [source-level reading and extraction](../notes/novelty-review-2026-11-02/review.md). No experiments were run for this reading.

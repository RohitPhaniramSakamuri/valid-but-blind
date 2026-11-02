# Entropy is not Enough for Test-Time Adaptation: From the Perspective of Disentangled Factors

Citation key: `Lee2024DeYO`.
Authors: Jonghyun Lee; Dahuin Jung; Saehyung Lee; Junsung Park; Juhyeon Shin; Uiwon Hwang; Sungroh Yoon.
Year and venue: 2024; ICLR 2024.
Publication/version status: Conference paper; linked arXiv first posted March 2024.
[Authoritative source](https://arxiv.org/abs/2403.07366). No local PDF in this project.
Reading progress: Primary arXiv abstract, official conference PDF first page and author repository README

## Research question and contribution

Object-destructive transformations supply pseudo-label probability differences for sample selection and weighting alongside entropy.

## Background needed

See the linked review for the decision variable and information regime; clarify prerequisites during reading.

## Reading notes

Inspected locations: Abstract; Official implementation overview.

## Method and implementation

[Public implementation / author resource](https://github.com/Jhyun17/DeYO) The literature-review stage did not execute this paper's code or reproduce its benchmark. The later custom digit diagnostic is a separate surrogate study, described in the project README.

## Evidence and limitations

Perturbation-derived evidence and entropy unreliability already have a strong predecessor; native computation and biased-task assumptions must be preserved when used as a baseline.

## Connection to our research

This source constrains the proposed contribution; distinguish its actual decision and evidence access from our acquisition hypothesis. [Review](../outputs/shift-aware-tta-review.md).

## Possible experiment

Compare legal evidence and total cost under the [planned protocol](../experiments/001-policy-selection-pilot.md) where the source's task and method can be matched.

## Next reading step

Inspect remaining method, split and code details before choosing an implementation baseline or claiming the paper omits a specific test.

## Adversarial review — 2 November 2026

Jonghyun Lee, Dahuin Jung, Saehyung Lee, Junsung Park, Juhyeon Shin, Uiwon Hwang, Sungroh Yoon. 2024. ICLR 2024. [Primary source](https://arxiv.org/abs/2403.07366).

Publication/version qualification: Conference paper; linked arXiv first posted March 2024

**Actual reading:** §§3–4/Table5/AppendixM selectively inspected.

**Locations:** §§3–4; Table5; AppendixM

**Method/evidence and connection:** Perturbation-derived reliability and stable updates; accuracy improvement is not a monitoring remedy guarantee.

**Limit:** Perturbation-derived evidence and entropy unreliability already have a strong predecessor; native computation and biased-task assumptions must be preserved when used as a baseline.

**Next reading step:** resolve access/version limits and the precise C1–C5 overlap before stronger claims. [Detailed claim review](../notes/novelty-review-2026-11-02/review.md); [source-level reading and extraction](../notes/novelty-review-2026-11-02/review.md). No experiments were run for this reading.

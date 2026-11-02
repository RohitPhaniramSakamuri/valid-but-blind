# Universal Test-Time Adaptation Through Weight Ensembling, Diversity Weighting, and Prior Correction

Citation key: `Marsden2024ROID`.
Authors: Robert A. Marsden; Mario Döbler; Bin Yang.
Year and venue: 2024; WACV 2024; official CVF page lists pages 2555–2565.
Publication/version status: Conference paper; primary CVF metadata used rather than inconsistent secondary pagination.
[Authoritative source](https://openaccess.thecvf.com/content/WACV2024/html/Marsden_Universal_Test-Time_Adaptation_Through_Weight_Ensembling_Diversity_Weighting_and_Prior_WACV_2024_paper.html). No local PDF in this project.
Reading progress: Official metadata/abstract and indexed method sections 4.1–4.3

## Research question and contribution

Universal TTA covers nonstationarity, temporal correlation and priors using certainty/diversity weights, source averaging and prediction prior correction.

## Background needed

See the linked review for the decision variable and information regime; clarify prerequisites during reading.

## Reading notes

Inspected locations: Abstract; Sections 4.1–4.3.

## Method and implementation

[Public implementation / author resource](https://github.com/mariodoebler/test-time-adaptation) The literature-review stage did not execute this paper's code or reproduce its benchmark. The later custom digit diagnostic is a separate surrogate study, described in the project README.

## Evidence and limitations

A strong fixed-method comparison; these deployment factors alone do not establish a new selection problem.

## Connection to our research

This source constrains the proposed contribution; distinguish its actual decision and evidence access from our acquisition hypothesis. [Review](../outputs/shift-aware-tta-review.md).

## Possible experiment

Compare legal evidence and total cost under the [planned protocol](../experiments/001-policy-selection-pilot.md) where the source's task and method can be matched.

## Next reading step

Inspect remaining method, split and code details before choosing an implementation baseline or claiming the paper omits a specific test.

## Adversarial review — 2 November 2026

Robert A. Marsden, Mario Döbler, Bin Yang. 2024. WACV 2024; official CVF page lists pages 2555–2565. [Primary source](https://openaccess.thecvf.com/content/WACV2024/html/Marsden_Universal_Test-Time_Adaptation_Through_Weight_Ensembling_Diversity_Weighting_and_Prior_WACV_2024_paper.html).

Publication/version qualification: Conference paper; primary CVF metadata used rather than inconsistent secondary pagination

**Actual reading:** §§3–5/Figure4/Tables3–4/selectedAppendixB.

**Locations:** §§3–5; Tables3–4

**Method/evidence and connection:** Prior correction/diversity already address correlated class/corruption streams; no exact monitor-sensitivity evaluation.

**Limit:** A strong fixed-method comparison; these deployment factors alone do not establish a new selection problem.

**Next reading step:** resolve access/version limits and the precise C1–C5 overlap before stronger claims. [Detailed claim review](../notes/novelty-review-2026-11-02/review.md); [source-level reading and extraction](../notes/novelty-review-2026-11-02/review.md). No experiments were run for this reading.

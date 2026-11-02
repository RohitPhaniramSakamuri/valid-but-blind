# AETTA: Label-Free Accuracy Estimation for Test-Time Adaptation

Citation key: `Lee2024AETTA`.
Authors: Taeckyung Lee; Sorn Chottananurak; Taesik Gong; Sung-Ju Lee.
Year and venue: 2024; CVPR, pp.28643–28652.
Publication/version status: conference paper.
[Authoritative source](https://openaccess.thecvf.com/content/CVPR2024/html/Lee_AETTA_Label-Free_Accuracy_Estimation_for_Test-Time_Adaptation_CVPR_2024_paper.html). No local PDF in this project.
Reading progress: official abstract/metadata, indexed accuracy-estimation comparisons and supplemental model-recovery details

## Research question and contribution

Uses dropout disagreement to estimate current adapted-model accuracy; demonstrates model recovery from estimated degradation.

## Background needed

See the linked review for the decision variable and information regime; clarify prerequisites during reading.

## Reading notes

Inspected locations: Abstract; Accuracy Estimation Baselines/results, p.28648; Supplement D.4, Model Recovery Details.

## Method and implementation

[Public implementation / author resource](https://github.com/taeckyung/AETTA) The literature-review stage did not execute this paper's code or reproduce its benchmark. The later custom digit diagnostic is a separate surrogate study, described in the project README.

## Evidence and limitations

Already covers label-free recovery decisions, but dropout observations and estimator assumptions incur cost; does not establish pre-action benefit for every candidate.

## Connection to our research

This source constrains the proposed contribution; distinguish its actual decision and evidence access from our acquisition hypothesis. [Review](../outputs/shift-aware-tta-review.md).

## Possible experiment

Compare legal evidence and total cost under the [planned protocol](../experiments/001-policy-selection-pilot.md) where the source's task and method can be matched.

## Next reading step

Inspect remaining method, split and code details before choosing an implementation baseline or claiming the paper omits a specific test.

## Reading update 2026-10-31

CVF PDF §3.2 and results discussion on calibration violation under adaptation failure. Locations: Section 3.2, Results. See the [dossier](../outputs/novelty-dossier-2026-10-31.md).

## Adversarial review — 2 November 2026

Taeckyung Lee, Sorn Chottananurak, Taesik Gong, Sung-Ju Lee. 2024. CVPR, pp.28643–28652. [Primary source](https://openaccess.thecvf.com/content/CVPR2024/html/Lee_AETTA_Label-Free_Accuracy_Estimation_for_Test-Time_Adaptation_CVPR_2024_paper.html).

Publication/version qualification: conference paper

**Actual reading:** Main §§3–5/Figures2–4,6/Tables1–3; supplementA/C/D.1/D.4/F; Fig2 visually inspected by TTA subreview.

**Locations:** §3.2/Figure2; §3.3; Tables1–2; SupplementC,D.1,D.4

**Method/evidence and connection:** Confidence/accuracy decoupling and corrected disagreement/recovery are prior art; no same sequential missed-risk comparison.

**Limit:** Already covers label-free recovery decisions, but dropout observations and estimator assumptions incur cost; does not establish pre-action benefit for every candidate.

**Next reading step:** resolve access/version limits and the precise C1–C5 overlap before stronger claims. [Detailed claim review](../notes/novelty-review-2026-11-02/review.md); [source-level reading and extraction](../notes/novelty-review-2026-11-02/review.md). No experiments were run for this reading.

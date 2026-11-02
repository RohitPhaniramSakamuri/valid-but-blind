# Test-Time Adaptation Induces Stronger Accuracy and Agreement-on-the-Line

Citation key: `Kim2024TTALine`.
Authors: Eungyeup Kim; Mingjie Sun; Christina Baek; Aditi Raghunathan; J. Zico Kolter.
Year and venue: 2024; NeurIPS 37.
Publication/version status: conference paper; preprint first posted 2023.
[Authoritative source](https://arxiv.org/abs/2310.04941). No local PDF in this project.
Reading progress: abstract/introduction and Section 5.2 selection passages

## Research question and contribution

Uses post-adaptation accuracy/agreement relationships for hyperparameter and TTA-strategy selection without OOD labels.

## Background needed

See the linked review for the decision variable and information regime; clarify prerequisites during reading.

## Reading notes

Inspected locations: Section 5.2, Unsupervised validation for TTA; Extension to selecting best TTA strategy.

## Method and implementation

[Public implementation / author resource](https://github.com/EungyeupKim/TTALine) The literature-review stage did not execute this paper's code or reproduce its benchmark. The later custom digit diagnostic is a separate surrogate study, described in the project README.

## Evidence and limitations

Needs source/ID and multiple-model agreement evidence; observed linearity is not arbitrary-shift identifiability.

## Connection to our research

This source constrains the proposed contribution; distinguish its actual decision and evidence access from our acquisition hypothesis. [Review](../outputs/shift-aware-tta-review.md).

## Possible experiment

Compare legal evidence and total cost under the [planned protocol](../experiments/001-policy-selection-pilot.md) where the source's task and method can be matched.

## Next reading step

Inspect remaining method, split and code details before choosing an implementation baseline or claiming the paper omits a specific test.

## Adversarial review — 2 November 2026

Eungyeup Kim, Mingjie Sun, Christina Baek, Aditi Raghunathan, J. Zico Kolter. 2024. NeurIPS 37. [Primary source](https://arxiv.org/abs/2310.04941).

Publication/version qualification: conference paper; preprint first posted 2023

**Actual reading:** Primary PDF §§3–5.2/Table3/Figure3, §§6–7, appendix algorithm/data-budget map. Relevant methods/results selective, not all theoretical proofs.

**Locations:** §5.2 Table3/Figure3; §6; §7; AppendixD

**Method/evidence and connection:** Agreement-based unlabeled performance and TTA-method selection already exist; adaptation can improve those estimators. Needs multiple candidates and sufficient ID data; no sequential risk guarantee or class-prior-skew test established.

**Limit:** Needs source/ID and multiple-model agreement evidence; observed linearity is not arbitrary-shift identifiability.

**Next reading step:** resolve access/version limits and the precise C1–C5 overlap before stronger claims. [Detailed claim review](../notes/novelty-review-2026-11-02/review.md); [source-level reading and extraction](../notes/novelty-review-2026-11-02/review.md). No experiments were run for this reading.

# Towards Stable Test-Time Adaptation in Dynamic Wild World

Citation key: `Niu2023SAR`.
Authors: Shuaicheng Niu; Jiaxiang Wu; Yifan Zhang; Zhiquan Wen; Yaofo Chen; Peilin Zhao; Mingkui Tan.
Year and venue: 2023; ICLR.
Publication/version status: conference paper.
[Authoritative source](https://arxiv.org/abs/2302.12400). No local PDF in this project.
Reading progress: abstract and conference PDF first-page description

## Research question and contribution

Reliable entropy minimization and sharpness-aware updates target instability under small batches, mixed shifts and imbalance.

## Background needed

See the linked review for the decision variable and information regime; clarify prerequisites during reading.

## Reading notes

Inspected locations: Abstract.

## Method and implementation

Implementation availability not established by this review. The literature-review stage did not execute this paper's code or reproduce its benchmark. The later custom digit diagnostic is a separate surrogate study, described in the project README.

## Evidence and limitations

Those deployment challenges are established, not a new gap; specific new policies must beat robust existing updates.

## Connection to our research

This source constrains the proposed contribution; distinguish its actual decision and evidence access from our acquisition hypothesis. [Review](../outputs/shift-aware-tta-review.md).

## Possible experiment

Compare legal evidence and total cost under the [planned protocol](../experiments/001-policy-selection-pilot.md) where the source's task and method can be matched.

## Next reading step

Inspect remaining method, split and code details before choosing an implementation baseline or claiming the paper omits a specific test.

## Adversarial review — 2 November 2026

Shuaicheng Niu, Jiaxiang Wu, Yifan Zhang, Zhiquan Wen, Yaofo Chen, Peilin Zhao, Mingkui Tan. 2023. ICLR. [Primary source](https://arxiv.org/abs/2302.12400).

Publication/version qualification: conference paper

**Actual reading:** §§3.1–3.2,4,5/Figure2/Table5 selectively inspected.

**Locations:** §3.1; Figure2; Table5

**Method/evidence and connection:** Separates statistics problems and entropy collapse, gives heuristic reset; no sequential power guarantee.

**Limit:** Those deployment challenges are established, not a new gap; specific new policies must beat robust existing updates.

**Next reading step:** resolve access/version limits and the precise C1–C5 overlap before stronger claims. [Detailed claim review](../notes/novelty-review-2026-11-02/review.md); [source-level reading and extraction](../notes/novelty-review-2026-11-02/review.md). No experiments were run for this reading.

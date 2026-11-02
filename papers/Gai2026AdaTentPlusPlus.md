# AdaTent++: reliability-guided hybrid test-time adaptation for traffic sign detection under distribution shift

Citation key: `Gai2026AdaTentPlusPlus`.
Authors: Xiaomei Gai; Meichun Wang; Yantong Guo; Shiyu Wang; Ye Li; Rui Fu.
Year and venue: 2026; Frontiers in Signal Processing6.
Publication/version status: Published9September2026, DOI10.3389/frsip.2026.1842851.
[Authoritative source](https://www.frontiersin.org/journals/signal-processing/articles/10.3389/frsip.2026.1842851/full). No local PDF in this project.
Reading progress: Publisher full text selectively read: abstract, sections2.1–2.4, ablations, discussion, limitations and conclusion.

## Research question and contribution

Entropy and multiview agreement route to BN-stat update, guarded BN-affine update or skip; EMA/hysteresis, dynamic1–2steps and BN rollback stabilize.

## Background needed

See the linked review for the decision variable and information regime; clarify prerequisites during reading.

## Reading notes

Inspected locations: 2.3 multiview reliability and dynamic routing; 2.4 threepath mechanics; 3.4 ablations; 4 Discussion; 5 Limitations; 6 Conclusion item4.

## Method and implementation

Implementation availability not established by this review. The literature-review stage did not execute this paper's code or reproduce its benchmark. The later custom digit diagnostic is a separate surrogate study, described in the project README.

## Evidence and limitations

§5 admits benchmark-condition IDs for views/filtering, one deterministic run and no longstream. §4 says not compute-matched despite conflicting conclusion wording. §6 requests budget-aware adaptive viewcount/step controllers. No guarantees verified.

## Connection to our research

This source constrains the proposed contribution; distinguish its actual decision and evidence access from our acquisition hypothesis. [Review](../outputs/shift-aware-tta-review.md).

## Possible experiment

Compare legal evidence and total cost under the [planned protocol](../experiments/001-policy-selection-pilot.md) where the source's task and method can be matched.

## Next reading step

Inspect remaining method, split and code details before choosing an implementation baseline or claiming the paper omits a specific test.

## Literature refresh — 26 October 2026

Primary source: [AdaTent++: reliability-guided hybrid test-time adaptation for traffic sign detection under distribution shift](https://www.frontiersin.org/journals/signal-processing/articles/10.3389/frsip.2026.1842851/full).

Reading scope: Fresh open publisher full text, selective method and limitation reading.

Inspected locations: Sections 2.1–2.4; Sections 4–6.

Relevance (our reading): Entropy/cross-view reliability routes traffic-sign frames to BN statistics, guarded BN-affine updates, or skip/rollback.

Boundary / reviewer qualification: Declared condition-aware configuration, balanced subset, deterministic run and no long-stream evaluation limit transfer claims; budget comparison qualified in discussion.

Publication qualification: Published9September2026, DOI10.3389/frsip.2026.1842851

No code or benchmark was run for this refresh. [Current synthesis](../outputs/shift-aware-tta-deep-review-2026-10-26.md). Detailed reading histories and original metadata remain in [catalog](../sources/catalog.json).

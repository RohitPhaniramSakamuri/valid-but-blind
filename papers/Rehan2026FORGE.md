# FORGE: Forward-Only Test-Time Adaptation for Integer-Only Vision Models on Microcontrollers

Citation key: `Rehan2026FORGE`.
Authors: Muhammad Rehan; Haider Ali; Muhammad Ali Munir; Moaz Amjad.
Year and venue: 2026; arXiv:2609.01683v1; arXiv record identifies Transactions on Machine Learning Research 2026 publication.
Publication/version status: Preprint submitted 1 September 2026; TMLR venue claim present on primary author record, but acceptance independently unverified by reviewer.
[Authoritative source](https://arxiv.org/abs/2609.01683v1). No local PDF in this project.
Reading progress: Abstract/metadata, full HTML section 4.6, Algorithm 2 and section 5 limitations; selected deployment text inspected

## Research question and contribution

Runs source and adapted paths during a short unlabeled calibration window, charges duplicate forward passes, then commits using confidence improvement. Paid probing and no-update fallback are prior art.

## Background needed

See the linked review for the decision variable and information regime; clarify prerequisites during reading.

## Reading notes

Inspected locations: Section 4.6; Algorithm 2; Section 5.

## Method and implementation

Implementation availability not established by this review. The literature-review stage did not execute this paper's code or reproduce its benchmark. The later custom digit diagnostic is a separate surrogate study, described in the project README.

## Evidence and limitations

Reported confidence gate loses useful adaptation under many-class overconfidence; source statistics and BN-folded convolutional deployment requirements differ from generic backbones. Its result is not a universal safety guarantee.

## Connection to our research

This source constrains the proposed contribution; distinguish its actual decision and evidence access from our acquisition hypothesis. [Review](../outputs/shift-aware-tta-review.md).

## Possible experiment

Compare legal evidence and total cost under the [planned protocol](../experiments/001-policy-selection-pilot.md) where the source's task and method can be matched.

## Next reading step

Inspect remaining method, split and code details before choosing an implementation baseline or claiming the paper omits a specific test.

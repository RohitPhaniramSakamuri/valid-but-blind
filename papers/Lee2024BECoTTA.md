# BECoTTA: Input-dependent Online Blending of Experts for Continual Test-time Adaptation

Citation key: `Lee2024BECoTTA`.
Authors: Daeun Lee; Jaehong Yoon; Sung Ju Hwang.
Year and venue: 2024; ICML 2024, PMLR 235:27072–27093.
Publication/version status: Conference paper; arXiv v3 31 May 2024 inspected.
[Authoritative source](https://proceedings.mlr.press/v235/lee24ab.html). No local PDF in this project.
Reading progress: Abstract, introduction, method and benchmark design descriptions plus author project page.

## Research question and contribution

Pseudo-domain inference routes inputs to low-rank experts; updates relevant experts and blends domain-adaptive knowledge.

## Background needed

See the linked review for the decision variable and information regime; clarify prerequisites during reading.

## Reading notes

Inspected locations: Section 3.2 Domain-Augmented Initialization; Section 3.3 MoDE; Section 3.4 CTTA process; Continual gradual shifts construction.

## Method and implementation

[Public implementation / author resource](https://github.com/daeunni/becotta) The literature-review stage did not execute this paper's code or reproduce its benchmark. The later custom digit diagnostic is a separate surrogate study, described in the project README.

## Evidence and limitations

Expert routing is distinct from selecting complete standalone TTA methods. Initialization and source augmentation variants must be distinguished; gradual/mixed shifts alone are covered.

## Connection to our research

This source constrains the proposed contribution; distinguish its actual decision and evidence access from our acquisition hypothesis. [Review](../outputs/shift-aware-tta-review.md).

## Possible experiment

Compare legal evidence and total cost under the [planned protocol](../experiments/001-policy-selection-pilot.md) where the source's task and method can be matched.

## Next reading step

Inspect remaining method, split and code details before choosing an implementation baseline or claiming the paper omits a specific test.

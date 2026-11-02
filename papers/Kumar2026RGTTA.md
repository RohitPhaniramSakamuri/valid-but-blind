# RG-TTA: Regime-Guided Meta-Control for Test-Time Adaptation in Streaming Time Series

Citation key: `Kumar2026RGTTA`.
Authors: Indar Kumar; Akanksha Tiwari; Sai Krishna Jasti; Ankit Hemant Lade.
Year and venue: 2026; arXiv preprint.
Publication/version status: arXiv2603.27814v1,29March2026; no venue acceptance verified.
[Authoritative source](https://arxiv.org/abs/2603.27814). No local PDF in this project.
Reading progress: Abstract,introduction,method outline and limitations/ablation table of contents.

## Research question and contribution

Uses similarity to stored regimes to scale learning rate, stop updates when loss plateaus and reuse checkpoints only when predicted loss benefit passes a gate.

## Background needed

See the linked review for the decision variable and information regime; clarify prerequisites during reading.

## Reading notes

Inspected locations: III-C continuous regime guidance; III-F checkpoint management; VII-H component contribution; IX Limitations.

## Method and implementation

[Public implementation / author resource](https://github.com/IndarKarhana/RGTTA-Regime-Guided-Test-Time-Adaptation) The literature-review stage did not execute this paper's code or reproduce its benchmark. The later custom digit diagnostic is a separate surrogate study, described in the project README.

## Evidence and limitations

Temporal forecasting setup has observed outcomes; checkpoint bank/rate controller is not fully unlabeled image-classification method selection.

## Connection to our research

This source constrains the proposed contribution; distinguish its actual decision and evidence access from our acquisition hypothesis. [Review](../outputs/shift-aware-tta-review.md).

## Possible experiment

Compare legal evidence and total cost under the [planned protocol](../experiments/001-policy-selection-pilot.md) where the source's task and method can be matched.

## Next reading step

Inspect remaining method, split and code details before choosing an implementation baseline or claiming the paper omits a specific test.

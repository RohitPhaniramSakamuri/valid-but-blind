# Measure Less, Know More: Self-Supervised Test-Time Feature Acquisition

Citation key: `Jain2026MeasureLess`.
Authors: Eeshaan Jain; Linus Bleistein; Bart Deplancke; Charlotte Bunne.
Year and venue: 2026; arXiv:2610.03454v1, 2 October 2026; manuscript carries a NeurIPS 2026 footer, acceptance not independently confirmed.
Publication/version status: Verified arXiv preprint.
[Authoritative source](https://arxiv.org/abs/2610.03454). [Local PDF](../sources/pdfs/Jain2026MeasureLess.pdf)
Reading progress: Abstract and introductory acquisition formulation from downloaded PDF

## Research question and contribution

ECHO-k selects costly modalities using pretrained representation recovery as label-free feedback.

## Background needed

See the linked review for the decision variable and information regime; clarify prerequisites during reading.

## Reading notes

Inspected locations: Page 1; abstract and section 1.

## Method and implementation

[Public implementation / author resource](https://github.com/bunnelab/echo-k) The literature-review stage did not execute this paper's code or reproduce its benchmark. The later custom digit diagnostic is a separate surrogate study, described in the project README.

## Evidence and limitations

Acquiring views without task labels is already studied; proposed distinction must concern adaptation-action benefit.

## Connection to our research

This source constrains the proposed contribution; distinguish its actual decision and evidence access from our acquisition hypothesis. [Review](../outputs/shift-aware-tta-review.md).

## Possible experiment

Compare legal evidence and total cost under the [planned protocol](../experiments/001-policy-selection-pilot.md) where the source's task and method can be matched.

## Next reading step

Inspect remaining method, split and code details before choosing an implementation baseline or claiming the paper omits a specific test.

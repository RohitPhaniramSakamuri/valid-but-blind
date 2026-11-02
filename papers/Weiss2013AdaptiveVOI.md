# Learning Adaptive Value of Information for Structured Prediction

Citation key: `Weiss2013AdaptiveVOI`.
Authors: David J Weiss; Ben Taskar.
Year and venue: 2013; Advances in Neural Information Processing Systems 26.
Publication/version status: Conference paper.
[Authoritative source](https://proceedings.neurips.cc/paper_files/paper/2013/hash/ebd9629fc3ae5e9f6611e2ee05a31cef-Abstract.html). No local PDF in this project.
Reading progress: Official proceedings metadata/abstract and introduction

## Research question and contribution

Learned runtime control of feature acquisition by decision value and computation cost.

## Background needed

See the linked review for the decision variable and information regime; clarify prerequisites during reading.

## Reading notes

Inspected locations: Abstract; section 1.

## Method and implementation

Implementation availability not established by this review. The literature-review stage did not execute this paper's code or reproduce its benchmark. The later custom digit diagnostic is a separate surrogate study, described in the project README.

## Evidence and limitations

Value of information and adaptive acquisition are established principles; no claim of inventing them here.

## Connection to our research

This source constrains the proposed contribution; distinguish its actual decision and evidence access from our acquisition hypothesis. [Review](../outputs/shift-aware-tta-review.md).

## Possible experiment

Compare legal evidence and total cost under the [planned protocol](../experiments/001-policy-selection-pilot.md) where the source's task and method can be matched.

## Next reading step

Inspect remaining method, split and code details before choosing an implementation baseline or claiming the paper omits a specific test.

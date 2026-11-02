# WILDS: A Benchmark of in-the-Wild Distribution Shifts

Citation key: `Koh2021WILDS`.
Authors: Pang Wei Koh; Shiori Sagawa; Henrik Marklund; Sang Michael Xie; Marvin Zhang; Akshay Balsubramani; Weihua Hu; Michihiro Yasunaga; Richard Lanas Phillips; Irena Gao; Tony Lee; Etienne David; Ian Stavness; Wei Guo; Berton Earnshaw; Imran Haque; Sara M Beery; Jure Leskovec; Anshul Kundaje; Emma Pierson; Sergey Levine; Chelsea Finn; Percy Liang.
Year and venue: 2021; ICML 2021, PMLR 139:5637–5664.
Publication/version status: Conference paper.
[Authoritative source](https://proceedings.mlr.press/v139/koh21a.html). No local PDF in this project.
Reading progress: Official proceedings metadata/abstract and opening dataset examples

## Research question and contribution

Natural domain and subpopulation shifts with dataset-specific evaluation.

## Background needed

See the linked review for the decision variable and information regime; clarify prerequisites during reading.

## Reading notes

Inspected locations: Abstract; figure 1; author blog's FMoW/domain/subpopulation examples.

## Method and implementation

[Public implementation / author resource](https://wilds.stanford.edu/) The literature-review stage did not execute this paper's code or reproduce its benchmark. The later custom digit diagnostic is a separate surrogate study, described in the project README.

## Evidence and limitations

WILDS is a suite of tasks; saying 'evaluate on WILDS' does not specify a reproducible experiment.

## Connection to our research

This source constrains the proposed contribution; distinguish its actual decision and evidence access from our acquisition hypothesis. [Review](../outputs/shift-aware-tta-review.md).

## Possible experiment

Compare legal evidence and total cost under the [planned protocol](../experiments/001-policy-selection-pilot.md) where the source's task and method can be matched.

## Next reading step

Inspect remaining method, split and code details before choosing an implementation baseline or claiming the paper omits a specific test.

# On Pitfalls of Test-Time Adaptation

Citation key: `Zhao2023Pitfalls`.
Authors: Hao Zhao; Yuejiang Liu; Alexandre Alahi; Tao Lin.
Year and venue: 2023; ICML, PMLR 202:42058–42080.
Publication/version status: conference paper.
[Authoritative source](https://proceedings.mlr.press/v202/zhao23d.html). No local PDF in this project.
Reading progress: abstract, setting/model-selection discussion, label/temporal shift results and conclusion

## Research question and contribution

TTAB documents hyperparameter dependence, model-property effects and failure under difficult shifts.

## Background needed

See the linked review for the decision variable and information regime; clarify prerequisites during reading.

## Reading notes

Inspected locations: Sections 1, 3; Table 3; Section 7.

## Method and implementation

[Public implementation / author resource](https://github.com/LINs-lab/ttab) The literature-review stage did not execute this paper's code or reproduce its benchmark. The later custom digit diagnostic is a separate surrogate study, described in the project README.

## Evidence and limitations

Even labeled oracle tuning has online batch-dependence complications; model-selection assumptions must be explicit.

## Connection to our research

This source constrains the proposed contribution; distinguish its actual decision and evidence access from our acquisition hypothesis. [Review](../outputs/shift-aware-tta-review.md).

## Possible experiment

Compare legal evidence and total cost under the [planned protocol](../experiments/001-policy-selection-pilot.md) where the source's task and method can be matched.

## Next reading step

Inspect remaining method, split and code details before choosing an implementation baseline or claiming the paper omits a specific test.

## Literature refresh — 26 October 2026

Primary source: [On Pitfalls of Test-Time Adaptation](https://proceedings.mlr.press/v202/zhao23d.html).

Reading scope: Fresh official abstract and selective PDF sections1-2 plus implementation/protocol passages

Inspected locations: Abstract and sections1-2; repository.

Relevance (our reading): TTAB documents hyperparameter dependence, model-property effects and failure under difficult shifts.

Boundary / reviewer qualification: Even labeled oracle tuning has online batch-dependence complications; model-selection assumptions must be explicit.

Publication qualification: conference paper

No code or benchmark was run for this refresh. [Current synthesis](../outputs/shift-aware-tta-deep-review-2026-10-26.md). Detailed reading histories and original metadata remain in [catalog](../sources/catalog.json).

## Reading update 2026-10-31

PMLR PDF abstract and §4.1 on batch dependency. Locations: Abstract, Section 4.1. See the [dossier](../outputs/novelty-dossier-2026-10-31.md).

## Adversarial review — 2 November 2026

Hao Zhao, Yuejiang Liu, Alexandre Alahi, Tao Lin. 2023. ICML, PMLR 202:42058–42080. [Primary source](https://proceedings.mlr.press/v202/zhao23d.html).

Publication/version qualification: conference paper

**Actual reading:** §§4–6/Tables3–5/AppendixF.1; clean label-shift tables distinguished from corruption evaluations.

**Locations:** §6; Tables3–5; AppendixF.1

**Method/evidence and connection:** Dirichlet/TTA degradation and BN vulnerabilities established; not a Schirmer missed-alarm test.

**Limit:** Even labeled oracle tuning has online batch-dependence complications; model-selection assumptions must be explicit.

**Next reading step:** resolve access/version limits and the precise C1–C5 overlap before stronger claims. [Detailed claim review](../notes/novelty-review-2026-11-02/review.md); [source-level reading and extraction](../notes/novelty-review-2026-11-02/review.md). No experiments were run for this reading.

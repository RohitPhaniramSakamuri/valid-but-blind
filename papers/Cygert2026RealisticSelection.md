# Realistic Evaluation of Test-Time Adaptation: Unsupervised Model Selection

Citation key: `Cygert2026RealisticSelection`.
Authors: Sebastian Cygert; Damian Sójka; Tomasz Trzciński; Bartłomiej Twardowski.
Year and venue: 2026; VISAPP, volume 1, pp.75–86.
Publication/version status: conference paper; linked 2024 preprint titled Realistic Evaluation of Test-Time Adaptation Algorithms: Unsupervised Hyperparameter Selection.
[Authoritative source](https://doi.org/10.5220/0014320100004084). [Local PDF](../sources/pdfs/Cygert2026Selection.pdf)
Reading progress: published first-page metadata; linked 2024 HTML selection definitions, setup, discussion and conclusions; published PDF downloaded and title/author block checked

## Research question and contribution

Evaluates source validation, cross-dataset supervision and unlabeled proxy metrics for candidate selection.

## Background needed

See the linked review for the decision variable and information regime; clarify prerequisites during reading.

## Reading notes

Inspected locations: Improved hyperparameter selection in TTA; Experimental Setup; Discussion; Conclusions.

## Method and implementation

[Public implementation / author resource](https://github.com/cygerts/unsupervisedtta) The literature-review stage did not execute this paper's code or reproduce its benchmark. The later custom digit diagnostic is a separate surrogate study, described in the project README.

## Evidence and limitations

Most evidence is obtained after executing candidates; comparisons to pre-action routing must charge the different information/computation budget.

## Connection to our research

This source constrains the proposed contribution; distinguish its actual decision and evidence access from our acquisition hypothesis. [Review](../outputs/shift-aware-tta-review.md).

## Possible experiment

Compare legal evidence and total cost under the [planned protocol](../experiments/001-policy-selection-pilot.md) where the source's task and method can be matched.

## Next reading step

Inspect remaining method, split and code details before choosing an implementation baseline or claiming the paper omits a specific test.

## Reading update 2026-10-31

Saved text: selection-over-time figure discussion and §6. Locations: Selection figure text, Section 6. See the [dossier](../outputs/novelty-dossier-2026-10-31.md).

## Adversarial review — 2 November 2026

Sebastian Cygert, Damian Sójka, Tomasz Trzciński, Bartłomiej Twardowski. 2026. VISAPP, volume 1, pp.75–86. [Primary source](https://doi.org/10.5220/0014320100004084).

Publication/version qualification: conference paper; linked 2024 preprint titled Realistic Evaluation of Test-Time Adaptation Algorithms: Unsupervised Hyperparameter Selection

**Actual reading:** Published2026 PDF §§3.1,4,5.1–5.3/Figures6–8; Figure6 visually inspected. Older preprint distinguished.

**Locations:** §5.2/Figure6 p81; Figures7–8 p82

**Method/evidence and connection:** Corrupted CIFAR100 Dirichlet-class-correlation proxy selection already studied; no Schirmer alarm comparison.

**Limit:** Most evidence is obtained after executing candidates; comparisons to pre-action routing must charge the different information/computation budget.

**Next reading step:** resolve access/version limits and the precise C1–C5 overlap before stronger claims. [Detailed claim review](../notes/novelty-review-2026-11-02/review.md); [source-level reading and extraction](../notes/novelty-review-2026-11-02/review.md). No experiments were run for this reading.

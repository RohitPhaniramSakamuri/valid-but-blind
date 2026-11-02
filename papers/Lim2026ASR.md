# When and Where to Reset Matters for Long-Term Test-Time Adaptation

Citation key: `Lim2026ASR`.
Authors: Taejun Lim; Joong-Won Hwang; Kibok Lee.
Year and venue: 2026; ICLR.
Publication/version status: conference paper; arXiv v1 submitted 4 March 2026.
[Authoritative source](https://arxiv.org/abs/2603.03796). No local PDF in this project.
Reading progress: abstract/introduction, method outline and selected Sections 3.3–3.5

## Research question and contribution

Adaptive/selective reset, importance-aware knowledge recovery and domain-discrepancy-based adaptation adjustment.

## Background needed

See the linked review for the decision variable and information regime; clarify prerequisites during reading.

## Reading notes

Inspected locations: Sections 3.3–3.5; Figure 1; Appendix headings A.5 and A.10.

## Method and implementation

[Public implementation / author resource](https://github.com/YonseiML/asr) The literature-review stage did not execute this paper's code or reproduce its benchmark. The later custom digit diagnostic is a separate surrogate study, described in the project README.

## Evidence and limitations

Choosing reset timing, scope or update strength is not new; whole-method benefit conditioned on live optimizer/memory state would need a separate precise comparison.

## Connection to our research

This source constrains the proposed contribution; distinguish its actual decision and evidence access from our acquisition hypothesis. [Review](../outputs/shift-aware-tta-review.md).

## Possible experiment

Compare legal evidence and total cost under the [planned protocol](../experiments/001-policy-selection-pilot.md) where the source's task and method can be matched.

## Next reading step

Inspect remaining method, split and code details before choosing an implementation baseline or claiming the paper omits a specific test.

## Literature refresh — 26 October 2026

Primary source: [When and Where to Reset Matters for Long-Term Test-Time Adaptation](https://arxiv.org/abs/2603.03796).

Reading scope: Fresh arXiv HTML selective method and appendix reading.

Inspected locations: Sections 3.3–3.5; Appendices A.1–A.5.

Relevance (our reading): Collapse-aware selective reset, knowledge recovery and source/current disagreement regulate adaptation.

Boundary / reviewer qualification: Source/live disagreement and state-dependent recovery are already prior art. Remaining decision gap must be narrower than these ingredients.

Publication qualification: conference paper; arXiv v1 submitted 4 March 2026

No code or benchmark was run for this refresh. [Current synthesis](../outputs/shift-aware-tta-deep-review-2026-10-26.md). Detailed reading histories and original metadata remain in [catalog](../sources/catalog.json).

## Reading update 2026-10-31

§§3.3–3.5 passages and released methods/base.py asr_reset (default branch, commit not pinned): the code restores optimizer state on reset. Locations: Sections 3.3–3.5, methods/base.py. See the [dossier](../outputs/novelty-dossier-2026-10-31.md).

# A Layer Selection Approach to Test Time Adaptation

Citation key: `Sahoo2025GALA`.
Authors: Sabyasachi Sahoo; Mostafa ElAraby; Jonas Ngnawe; Yann Pequignot; Frederic Precioso; Christian Gagne.
Year and venue: 2025; AAAI 2025.
Publication/version status: Accepted per arXiv record; firstpreprint April2024, v2 Feb2025 inspected.
[Authoritative source](https://arxiv.org/abs/2404.03784). No local PDF in this project.
Reading progress: Abstract, introduction, section2 description, discussion/appendix analysis of current gradients versus accumulated state.

## Research question and contribution

Uses proposed gradients relative to accumulated parameter displacement to select one layer, skip updates or reset alignment history. Adaptation utility depends on state, loss and shift.

## Background needed

See the linked review for the decision variable and information regime; clarify prerequisites during reading.

## Reading notes

Inspected locations: Section 2.1 layer selection; Section 2.2 cosine criterion; Section 2.3 reset; Appendix A.5.4 alignment vs magnitude.

## Method and implementation

Implementation availability not established by this review. The literature-review stage did not execute this paper's code or reproduce its benchmark. The later custom digit diagnostic is a separate surrogate study, described in the project README.

## Evidence and limitations

Selecting update layers is not arbitrary whole-method selection, but state/drift/gradient features and skip/reset are established; cannot sell these alone as a gap.

## Connection to our research

This source constrains the proposed contribution; distinguish its actual decision and evidence access from our acquisition hypothesis. [Review](../outputs/shift-aware-tta-review.md).

## Possible experiment

Compare legal evidence and total cost under the [planned protocol](../experiments/001-policy-selection-pilot.md) where the source's task and method can be matched.

## Next reading step

Inspect remaining method, split and code details before choosing an implementation baseline or claiming the paper omits a specific test.

## Literature refresh — 26 October 2026

Primary source: [A Layer Selection Approach to Test Time Adaptation](https://arxiv.org/abs/2404.03784).

Reading scope: Fresh arXiv HTML selective method and experiment reading.

Inspected locations: Sections 2.2–2.3; Section 3; Appendix A.5.

Relevance (our reading): Proposed-gradient alignment with accumulated displacement chooses layers or skips; periodic anchor resets allow trajectory changes.

Boundary / reviewer qualification: State/history-based parameter selection already exists; not an audited whole-policy value learner. Uses hyperparameter sweeps in inspected benchmark setup.

Publication qualification: Accepted per arXiv record; firstpreprint April2024, v2 Feb2025 inspected

No code or benchmark was run for this refresh. [Current synthesis](../outputs/shift-aware-tta-deep-review-2026-10-26.md). Detailed reading histories and original metadata remain in [catalog](../sources/catalog.json).

## Reading update 2026-10-31

§§2.1–2.3: hand-set cosine threshold on displacement since an anchor. Locations: Sections 2.1–2.3. See the [dossier](../outputs/novelty-dossier-2026-10-31.md).

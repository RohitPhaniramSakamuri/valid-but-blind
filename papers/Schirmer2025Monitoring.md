# Monitoring Risks in Test-Time Adaptation

Citation key: `Schirmer2025Monitoring`.
Authors: Mona Schirmer; Metod Jazbec; Christian A. Naesseth; Eric Nalisnick.
Year and venue: 2025; NeurIPS2025, Advances in Neural Information Processing Systems38 (39th conference).
Publication/version status: conference paper; inspected arXiv v1 July 2025.
[Authoritative source](https://arxiv.org/abs/2507.08721). Current primary PDF: [saved NeurIPS version](../notes/novelty-review-2026-11-02/evidence/root/Schirmer2025Monitoring-neurips.pdf); earlier reading history retained below.
Reading progress: Sections 2–3, experiments, conclusion/limitations, selected appendices

## Research question and contribution

Sequential monitoring of the risk of an adapting model using unlabeled loss proxies and source calibration.

## Background needed

See the linked review for the decision variable and information regime; clarify prerequisites during reading.

## Reading notes

Inspected locations: Section 3.2, Assumption 1; Section 3.4; Section 6, Limitations and Future Work; Appendix A.4.

## Method and implementation

Implementation availability not established by this review. The literature-review stage did not execute this paper's code or reproduce its benchmark. The later custom digit diagnostic is a separate surrogate study, described in the project README.

## Evidence and limitations

Proxy-informativeness assumption needs labeled data to verify; unsupervised diagnostics for its violation and reducing monitoring delay/cost remain open.

## Connection to our research

This source constrains the proposed contribution; distinguish its actual decision and evidence access from our acquisition hypothesis. [Review](../outputs/shift-aware-tta-review.md).

## Possible experiment

Compare legal evidence and total cost under the [planned protocol](../experiments/001-policy-selection-pilot.md) where the source's task and method can be matched.

## Next reading step

Inspect remaining method, split and code details before choosing an implementation baseline or claiming the paper omits a specific test.

## Literature refresh — 26 October 2026

Primary source: [Monitoring Risks in Test-Time Adaptation](https://proceedings.neurips.cc/paper_files/paper/2025/hash/746960ad49ddb47248970a0e1404230c-Abstract-Conference.html).

Reading scope: Official NeurIPS metadata; arXiv v2 Assumption1, Proposition1, §§5.2-5.4, §6 and AppendixA.5. Partial reading.

Inspected locations: Assumption 1; Proposition 1; Section 5.4; Section 6; Appendix A.5.

Relevance (our reading): Label-free sequential risk lower bounds for adapting models, conditional on calibrated proxy informativeness; alternative proxies and explicit prior-shift experiment.

Boundary / reviewer qualification: Assumption verification needs target labels. A lower risk bound crossing detects excess risk; staying below threshold does not certify safety. Paper explicitly leaves unlabeled assumption diagnostics open.

Publication qualification: NeurIPS 2025 main conference verified; earlier workshop versions must not be confused with full version

No code or benchmark was run for this refresh. [Current synthesis](../outputs/shift-aware-tta-deep-review-2026-10-26.md). Detailed reading histories and original metadata remain in [catalog](../sources/catalog.json).

## Adversarial review — 2 November 2026

Mona Schirmer, Metod Jazbec, Christian Andersson Naesseth, Eric Nalisnick. 2025. NeurIPS2025, Advances in Neural Information Processing Systems38. [Primary source](https://proceedings.neurips.cc/paper_files/paper/2025/hash/746960ad49ddb47248970a0e1404230c-Abstract-Conference.html).

Publication/version qualification: NeurIPS 2025 main conference verified; earlier workshop versions must not be confused with full version

**Actual reading:** Official NeurIPS PDF §§2–6, AppendicesA.1–A.5/B.1–B.4 and experimental configuration; Fig5 rendered/visually inspected. Cross-read arxivv2. Selective, not all proofs/checklist.

**Locations:** §§3.2–3.4; §§5.1–5.4; Figure5; AppendicesA.1–A.5,B.1–B.4

**Method/evidence and connection:** Already documents uncertainty-proxy alarm failure for T3A/STAD and prototype-distance repair; no exact C1 comparison established.

**Limit:** Assumption verification needs target labels. A lower risk bound crossing detects excess risk; staying below threshold does not certify safety. Paper explicitly leaves unlabeled assumption diagnostics open.

**Next reading step:** resolve access/version limits and the precise C1–C5 overlap before stronger claims. [Detailed claim review](../notes/novelty-review-2026-11-02/review.md); [source-level reading and extraction](../notes/novelty-review-2026-11-02/review.md). No experiments were run for this reading.

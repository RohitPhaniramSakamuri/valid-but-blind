# Provenance for the shift aware TTA review

Date and knowledge cutoff for this investigation: 23 October 2026. Topic: the user's proposed shift-aware adaptation-policy selector and a narrowed evidence-acquisition hypothesis.

## Source accounting

- **47 distinct primary scholarly sources** in [the catalog](../sources/catalog.json), [readable index](../REFERENCES.md) and [BibTeX](../references.bib).
- **47 paper notes**, each stating the reading scope, inspected locations, overlap and limitations. An indexed or downloaded paper is not automatically fully read.
- **9 downloaded PDFs**, with extracted text for selective inspection. [Download manifest](../sources/manifest.json) records retrieval URLs, failed attempts, successful alternatives, byte counts and SHA-256 hashes.
- Primary evidence: publisher/proceedings pages, papers, author-hosted PDFs, arXiv records/HTML and author repositories. Search snippets and secondary indexes were used for discovery, not as the final support for novelty or empirical claims.
- No new experiment, training, benchmark reproduction, implementation test, dataset download, checkpoint download, package installation or paid model/API experiment was performed. Paper downloads are literature artifacts.

## Search scope

Searches combined the following terms rather than restricting discovery to the exact proposed title:

- Shift-aware / shift-level / domain-shift detection + test-time adaptation.
- Dynamic / adaptive / algorithm / policy / whole-method selection; meta-controller; hyperparameter selection.
- Expert routing / mixtures; layer selection; objective choice; normalization interpolation; augmentation control.
- Unsupervised validation; post-adaptation accuracy estimation; no-update; negative transfer; risk monitoring; reset and recovery.
- Temporal correlation; label-prior shift; heterogeneous or compound shifts; accumulated model/optimizer state.
- Value of information; active feature/evidence acquisition; adaptive probing; conditional views; budget allocation; deadlines and latency.

Backward and cross-source chaining followed the nearest methods' references, particularly MORPHEUS and the September 2026 identifiability paper. Recent 2026 work was actively included. This is a targeted deep review, not a preregistered systematic review with database completeness guarantees. Search absence does not establish novelty.

## Research and review stages

The deep-research and literature-review skills name researcher, verifier and reviewer roles. Available research agents performed those tracks while the lead assembled foundations, datasets, the synthesis and protocol.

1. [Researcher source ledger](../notes/shift-aware-tta-review-researcher-sources.json) and [findings](../notes/shift-aware-tta-review-researcher.md): closest shift-conditioned policy, routing and composition collisions.
2. [Verifier ledger](../notes/shift-aware-tta-review-verifier-sources.json) and [findings](../notes/shift-aware-tta-review-verifier.md): label-free selection, safety assumptions, causal access and evaluation.
3. [Reviewer ledger](../notes/shift-aware-tta-review-reviewer-sources.json) and [findings](../notes/reviewer-findings.md): counterexamples, adaptive evidence neighbors and falsification criteria.
4. [Lead ledger](../notes/shift-aware-tta-review-lead-sources.json): surveys, acquisition foundations, dataset definitions and additional action baselines.
5. [Final verification](../notes/shift-aware-tta-review-final-verification.md) and [final critique](../notes/shift-aware-tta-review-final-review.md): adversarial passes over the actual synthesis, followed by corrections to costs, normalization semantics, validation nesting, finite-query uncertainty and oracle definitions. The verifier re-read the revised protocol and found no remaining blocking error. That is a document/evidence review, not implementation validation.

## Critical claim evidence

| Claim | Supporting source location | Verification boundary |
| --- | --- | --- |
| Shift-conditioned adaptation strategy selection already exists. | Hybrid-TTA §4.1; SLRF publisher abstract; AdaTent++ §§2.1–2.4. | SLRF full text is subscription-only; exact internals/protocol were not inferred. |
| Whole-method pre-action prediction is a direct predecessor. | MORPHEUS §2, author PDF header and author publication list. | Workshop status verified; official public code not verified. |
| No-update, prior/order ambiguity and richer stream evidence are already studied. | Jhawar and Wang §§2–5, §7, Appendix B. | Preprint; finite menu/main model family; conditional evidence advantage, not a universal solution. |
| Conditional evidence/computation itself is prior art. | SA-TTS Algorithm 1; CAS §3.3; SEGA Algorithm 1; MoASE++ §5.2; adaptive VOI and acquisition survey. | These have different terminal decisions and training signals; no claim they exactly implement the proposed whole-method net-value gate. |
| A close method explicitly requests budget-aware controllers and discloses domain-aware configuration. | AdaTent++ §§4–6. | Its “matched budgets” conclusion conflicts with §4's compute qualification; review uses the narrower qualification. |
| Operational timing can change adaptation rankings. | Tempora proceedings abstract and §§3–5. | Does not prove our controller improves the tradeoff. |
| Statistical safety requires assumptions beyond confidence. | Monitoring Risks in TTA §3.2, Assumption 1, and §6. | No arbitrary-shift guarantee is claimed for our development-calibrated gate. |
| Dataset families should not be conflated. | Corruption-benchmark author repository; DomainNet author source; WILDS proceedings abstract/figure 1. | Our proposed benchmark plan is not an executed multi-dataset evaluation. |

## Access and metadata qualifications

- OpenReview browser challenges blocked some live pages. MORPHEUS was obtained from a verified author-hosted PDF. It is an **ICLR 2026 Test-Time Updates workshop paper**, not a verified main-track ICLR paper.
- Cygert et al.'s VISAPP 2026 title is *Realistic Evaluation of Test-Time Adaptation: Unsupervised Model Selection*. Its linked 2024 preprint has the longer hyperparameter-selection title. The published PDF title/author block was checked.
- SLRF was checked against publisher metadata/abstract, not full subscription content. No omitted experiment is inferred from that access limit.
- Some CVF/SCITEPRESS endpoints failed or returned HTML. Successful alternate PDF downloads are retained alongside the failure records; primary content was then selectively inspected.
- Liang et al.'s survey has a 2023 preprint, 2024 online publication and 2025 journal volume. Wang et al.'s online-TTA survey likewise has a 2024 online/2025 volume distinction. These dates are linked versions, not different sources.
- FORGE's arXiv record reports TMLR and CAS's record reports ECCV; independent acceptance/proceedings confirmation was not completed. The catalog retains author-reported status.
- ECHO-k's downloaded preprint carries a NeurIPS 2026 footer. Independent acceptance confirmation was not completed; it is cited as a verified October 2026 arXiv preprint.
- BoTTA's publisher identifies SenSys 2026, while its older preprint report-number field differs. The publisher citation is used; the discrepancy is preserved in its source note. Its paper-linked code URL returned 404 in the reviewer pass, so access is not asserted.
- ROID's primary CVF record identifies WACV 2024; secondary pagination differs. The source record follows the primary page and does not relabel it CVPR.
- The 2016 AdaBN preprint and its related 2018 journal extension have different titles/author order. Only the directly inspected preprint is added as a source here.
- A guessed “FAR video selective” reference was excluded after no reliable title/identifier was established. No invented entry was added.

## Tool limits

The installed Feynman CLI reported alphaXiv authentication but returned `Unknown alpha command: search` for the documented paper-search subcommand. The skill's slash commands are not exposed in this session. The researcher/verifier/reviewer workflow was carried out with available agents and primary-source web tools; no alphaXiv search success, unseen workflow run or account/configuration repair is claimed.

## Claim status and unresolved work

- Established by prior art: shift-dependent normalization, update selection, expert composition, method selection, no-update decisions, evidence insufficiency, adaptive acquisition and timing-aware evaluation.
- Inferred candidate intersection: predict the net value of extra observations for **parameter-update policy selection**, beyond cheap selectors and equal-cost acquisition heuristics under held-out shifts.
- Proposed, not run: the action-headroom, evidence-headroom and learned-acquisition experiments.
- Unresolved: exhaustive novelty, implementability/fidelity of exact baseline versions, valid source checkpoint/development data, empirical effect size, device costs, robustness and publication venue.

There is no basis yet for claiming a successful method, a confirmed open research gap, or a high-quality-conference outcome.

# Provenance: fresh shift-aware TTA investigation

Date: **26 October 2026**. Topic: the user's proposed shift-conditioned adaptation framework, benchmark landscape, novelty and a falsifiable research direction. The user explicitly permitted disregarding previous work, especially for novelty. Historical work was preserved; its favored method and outcomes were not treated as evidence for the new candidate.

## Delivered artifacts

- [Deep review and novelty audit](shift-aware-tta-deep-review-2026-10-26.md): approximately 5,600 words, 18 direction/limitation rows, benchmark roles, direct collisions, three candidate gaps and a conditional recommendation.
- [Detailed benchmark investigation](../notes/review-refresh-2026-10-26/benchmarks.md): approximately 2,400 words, dataset/metric/protocol distinctions and limitations.
- [Experiment 002](../experiments/002-state-conditioned-selection.md): approximately 2,400 words, planned only; state/identity/timing/resource contracts and rejection conditions.
- [Reference index](../REFERENCES.md), [BibTeX](../references.bib), [JSON catalog](../sources/catalog.json), [CSV catalog](../sources/catalog.csv) and per-source notes in `papers/`.
- [Researcher overlap investigation](../notes/review-refresh-2026-10-26/researcher.md), [independent gap assessment](../notes/review-refresh-2026-10-26/verifier.md), [final critique](../notes/review-refresh-2026-10-26/final-review.md) and [final verification](../notes/review-refresh-2026-10-26/final-verification.md).

## Source accounting and reading boundaries

The integrated library has **103 distinct records: 101 scholarly works and two live benchmark/documentation records**. It started from 48 earlier records, adds 55 distinct works/documents and freshly inspects **68 distinct records** in this turn. The other 35 retain their earlier inspected status. This count does not mean 101 papers were fully read or all metadata were independently reverified today.

Four raw ledgers contain 77 observations before reconciliation:

| Ledger | Raw records | Focus |
| --- | ---: | --- |
| [Lead](../notes/review-refresh-2026-10-26/lead-sources.json) | 19 | Foundations, inexpensive alternatives, VLM/feature methods, DAgger and recent efficient adaptation. |
| [Researcher](../notes/review-refresh-2026-10-26/researcher-sources.json) | 20 | Direct selection/routing collisions, dynamic state control and missing recent predecessors. |
| [Benchmarks](../notes/review-refresh-2026-10-26/benchmarks-sources.json) | 22 | Dataset definitions, real protocol restrictions, benchmark tools and cost. |
| [Verifier](../notes/review-refresh-2026-10-26/verifier-sources.json) | 16 | Prior/normalization confounding, statistical assumptions and adversarial gap assessment. |

Deduplication uses existing keys, normalized titles and verified DOI where available. Canonical aliases: Schneider2020CovariateAdaptation → Schneider2020BNAdapt; Zhou2026RecoveryComplexity → Zhou2026Learnability; Park2023LabelShiftAdapter → Park2023LSA. [Alias record](../notes/review-refresh-2026-10-26/citation-aliases.json), [accounting summary](../notes/review-refresh-2026-10-26/library-summary.json).

Original keys remain stable. Original catalog/index/BibTeX files are preserved in [the before-refresh archive](../sources/library-before-refresh-2026-10-26/) with hashes. Paper notes are preserved and receive dated refresh sections; old experimental outputs/manifests are unchanged. The compiler [build_library.py](../notes/review-refresh-2026-10-26/build_library.py) performs record preparation only, using Python standard libraries through uv.

Each catalog entry records title, authors, year/version qualification, venue, authoritative URL, verified DOI when available, actual reading scope, inspected locations, overlap, limitations and implementation links when supported. Date-specific reading histories preserve narrower and deeper passes rather than presenting an abstract as full-paper reading. Web documents have access dates; the generated BibTeX does not invent publication years for them.

## Search scope and inclusion logic

This is an extensive targeted review with backward/sideways citation chaining, not a preregistered systematic review with exhaustive database coverage. Search absence does not establish novelty. The [search record](../notes/review-refresh-2026-10-26/search-scope.md) lists representative actually used queries and selection boundaries; it is not falsely described as a complete machine event log.

Search families covered:

- Shift-level/cause/domain inference, whole-method selection, policy composition and expert routing.
- Source-free adaptation versus one-pass online, episodic and continual settings.
- Class-prior change, partial class absence, temporal correlation and mixed/compound shifts.
- Normalization, entropy/consistency, robustness, teachers/memory, prototype/output refinement and feature geometry.
- Accuracy estimation, model/hyperparameter selection, harmful adaptation, protected updates and monitoring assumptions.
- State/history dependence, optimizer memory, reset/recovery, replay evaluation and autonomous policy-state distributions.
- Evidence acquisition, view/step/subspace selection, physical runtime/deadlines and on-device benchmarks.
- 2025/2026 conference work, preprints and adjacent learned-controller literature that could defeat a narrow novelty claim.

Primary sources support included claims: proceedings/publisher pages, official PDFs, arXiv versions, author sites/repositories and official benchmark documentation. Secondary search summaries were discovery leads; they do not support the claimed gap, numerical results or bibliography metadata by themselves. Inclusion as a neighbor does not make robotics/forecasting/LLM feedback a matched strictly unlabeled image-classification baseline.

## Evidence preservation

The earlier nine PDFs and their original [manifest](../sources/manifest.json) remain unchanged. The verifier additionally saved the official Channel-Selective Normalization PDF and extracted text in [verifier-evidence](../notes/review-refresh-2026-10-26/verifier-evidence/). Seven primary HTML snapshots were saved for Agentic-TTT, action identifiability, Hybrid-TTA, ASR, TTABC, RNA's author site and WILDS submission rules.

The [snapshot manifest](../notes/review-refresh-2026-10-26/snapshot-manifest.json) records retrieval URLs/timestamps, file names, sizes, hashes and failures. All seven HTML retrievals succeeded. Snapshot retention is not full-reading evidence. The download utility retrieved only scholarly/documentation reading material, not datasets or checkpoints.

## Critical claims and supporting locations

| Claim | Primary support | Limit of conclusion |
| --- | --- | --- |
| Broad shift-aware selection is already covered. | SLRF publisher abstract; MORPHEUS §2; Hybrid-TTA §4.1; AdaTent++ method. | SLRF subscription full text unavailable; no exact absence claim. |
| Marginal change/uncertainty is not a universal action-benefit signal. | ATC §3.1; action-identifiability §§3–5; prior-aware adaptation methods. | Does not prove all richer evidence is useless. |
| State-aware adaptation already exists. | ASR §§3.3–3.5 and §4.4; GALA §§2.2–2.3; Hybrid-TTA §4.1. | Proposed feature names and reset logic cannot be main novelty. |
| Autonomous-state training mismatch is already named. | Agentic-TTT §2.2.2 and Appendix E; DAgger foundational abstract/introduction. | The fresh visual mechanism/evaluation is an unverified research scope, not a new general principle. |
| Monitor guarantees require informative proxies. | Monitoring Risks Assumption 1, Proposition 1 and §6; POEM future-directions appendix. | No assumption-free target safety is claimed. |
| Standard WILDS comparisons restrict adaptation access. | Current submission standard items 2/6, nonstandard item 2; leaderboard metrics/historical BN rows. | No blanket assertion about every inference-only refinement; custom online updating must be declared. |
| Mixed-class/domain streams and realistic costs already have benchmarks. | UniTTA §§3–5; CCC/RDumb; time-constrained evaluation; Tempora; BoTTA; TTABC. | Their existence does not establish a universal comparable SOTA. |

## Workflow and independent critique

Applied Feynman skills: [deep-research](../../.agents/skills/feynman/deep-research/SKILL.md), [literature-review](../../.agents/skills/feynman/literature-review/SKILL.md), [alpha-research](../../.agents/skills/feynman/alpha-research/SKILL.md), [pdf-explore](../../.agents/skills/feynman/pdf-explore/SKILL.md), and [research-review](../../.agents/skills/feynman/research-review/SKILL.md).

The skills explicitly name researcher/verifier/reviewer agent roles; those roles were used for parallel investigation and subsequent critique. The lead assembled records and the report. No other research project's scope, budget or deadlines were imported.

The installed Feynman CLI reports alphaXiv authentication, but the documented `feynman alpha search --mode semantic ...` returns **Unknown alpha command: search**. The skill slash workflows are not invocable as commands in this chat. Their research/verification/critique stages were carried out with available tools and agents. No alpha search success or unseen Feynman workflow execution is claimed; no account/configuration repair was attempted.

The independent passes required and checked these corrections:

1. UPDATE uses frozen-live BN statistics and affine optimization in the minimal diagnostic; it is not mislabeled native ETA/Tent.
2. Feature observations and query scoring are state-pure; RNG/optimizer/memory/buffers and external time bookkeeping are explicit.
3. The primary learned menu excludes a selectable SOURCE answer path; SOURCE baseline and RESET state change remain distinct.
4. Current-model baselines include logits, geometry and order evidence, preventing a deliberately weak comparator.
5. Development comparisons account for unique labeled query IDs/reuse, action scoring, candidate steps, support forwards and state-generation compute.
6. Prefix/support/query/fresh-query IDs are disjoint in local matched cases; finite-query ranking noise and repetitions are acknowledged.
7. Next-block64 prediction loss is distinct from a frozen512 fixed-KEEP diagnostic horizon.
8. Local/replay oracles are not presented as deployable full-stream optimal policies.

The verifier reread the delivered amendments and found no remaining blocking document error. This is scientific/document review, **not implementation validation, experimental confirmation, exhaustive novelty certification or a prediction of acceptance**.

## What did and did not happen

Completed: primary-source literature search/reading, bibliography expansion/deduplication, paper-note updates, benchmark/access analysis, scientific critique, hypothesis/protocol definition and preservation of reading artifacts.

Not performed: model training, benchmark reproduction, implementation tests, new model experiments, dataset/checkpoint download, package installation, paid API/cloud use or deployment. Historical local digits and user-reported external gate aggregates remain separate. The fresh proposed method has **no results**.

Remaining work: exact-overlap checks where full methods/training dynamics remain uninspected, freeze a practical protocol, choose a legitimate source/development regime and an authorized compute environment, then test initial residual headroom before developing a controller.

## Final record-integrity inspection

The saved catalog and BibTeX each contain 103 unique matching citation keys, and all 103 indexed source-note files are present. Local links in the README, approach status, reference index, main review/provenance and Experiment 002 resolve. This was a documentation/record inspection, not a test of an adaptation implementation or a network audit of every external source. The final review is approximately 5,800 words; the benchmark companion and experiment protocol add approximately 4,800 words.

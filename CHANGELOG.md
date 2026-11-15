# Project research log

## Repository synchronization and rights notice

- Prepared the current experiment 005–010 source, saved aggregate/per-stream summaries, manuscript, figures, demo and submission documents for publication. Added the source catalog needed by document builders and allowed project-authored report PDFs while excluding datasets, checkpoints, caches, private cloud records and new machine/agent logs.
- Added an all-rights-reserved notice requiring Rohit Phaniram Sakamuri's prior express written permission for reuse of his original material, with explicit exceptions for applicable law, GitHub platform rights and third-party licenses. Preserved upstream architecture and document-style notices, and included the notices in the submission and Overleaf archives. Frozen research source files and result values were not modified.
- Corrected the README's stale pending-test summary to the completed PARTIAL result and added a source/evidence/reproduction index. Redacted temporary signed-download credential values from two literature-search ledgers; their scientific entries and source paths were retained. Private copies of the original ledgers were preserved locally outside the repository.
- Checked publication contents and credentials without rerunning scientific experiments or installing dependencies.

## Review presentation package

- Completed the supplied Review I, II and III templates for Rohit Phaniram Sakamuri, 23BDS0051: 8, 13 and 16 slides respectively. Saved editable decks, PDF copies, speaker notes, native charts/diagrams, a Word/PDF companion and an A3 poster in [reports/reviews](reports/reviews/README.md).
- Preserved the initial proposal as a proposal and presented the project’s progression into risk monitoring. The final deck retains the fresh confirmation’s PARTIAL verdict, exact false-alarm limit, denominator qualifications, offline-label requirements and negative findings.
- Omitted dates from the deliverables and removed inherited date placeholders and Office/PDF date metadata. Original templates and scientific artifacts remain unchanged. Document generation and rendering used existing libraries through uv; no new scientific experiments, implementation tests, literature search or paid compute.

## 2 November 2026 — DermaMNIST stress test

- Frozen test on DermaMNIST-224: blind spot replicates (33/33 vs 12/44), entropy adds, twin 17/33 with false alarms not estimable, SAR not shown, harm inconclusive. Added to the paper. Codex reviews are in `notes/medimg-novelty-2026-11-02/`.

## 2 November 2026 — twin denominator correction and corruption breakdown

- The twin's frozen pool (30/115) included six clean streams the released monitor never ran. Paper, decks and records now use the matching 30/109 (86% to 28%). Verdict unchanged.
- Added by-corruption breakdown: `explore_by_corruption.py`, `explore_by_corruption.json`, `explore_by_corruption_replication.json`.
- Started a Codex literature review on image-based monitoring in medical imaging: `notes/medimg-novelty-2026-11-02/`.

## 2 November 2026 — assessment report

- Prepared the user's requested [Word assessment report](reports/assessment/ML_Assessment_Rohit_23BDS0051.docx), with [PDF copy](reports/assessment/ML_Assessment_Rohit_23BDS0051.pdf), for Rohit Phaniram Sakamuri, 23BDS0051. Used the supplied Word example as a layout reference and included all eleven requested sections.
- Eight A4 pages, about 2,640 words, five tables and twelve references, with black text/borders and white backgrounds. Saved editable content, builder and source snapshots in `reports/assessment/`.
- Checked scientific claims against the current manuscript and Experiment 004; preserved different comparison denominators, the uncertified twin, the SAR negative result and the unmet combined harm-test rule. Reviewed rendered layout and removed an inherited coloured title border.
- Used installed Python packages through uv and LibreOffice for document preparation. No new experiments, implementation tests, dependency installation, literature search or paid compute. Existing manuscript, results and demo edits preserved.

## 2 November 2026 — live laptop demo

- Added [`demo/`](demo/README.md): a live CPU demo with per-image caught, missed and false-flag views. Three paper streams were compared with recorded GPU runs in `check_results.json`; alarm decisions matched, with twin alarm batches within 4.

## 2 November 2026 — entropy-free twin alarm

- Frozen twin test: FIX WORKS on held-out corruptions for the uncertified form (30/115 missed, released 94/109; 5/121 false alarms). Certified forms missed 115/115.
- Frozen adaptation-harm test: NOT SHOWN (51/61 detection, 1/6 false alarms on too few safe streams). Both are in the [experiment record](experiments/004-monitor-blind-spots.md) and the paper. Balance $31.57; no pods running.

## 2 November 2026 — false-alarm check added to paper

- Added [`explore_false_alarm.py`](diagnostics/2026-11-01-exp004-mechanism/explore_false_alarm.py) results to the paper as exploratory. The frozen-sentinel mitigation test was skipped at the user's request.

## 2 November 2026 — exploratory capture and adjusted estimates

- Added [`explore_power.py`](diagnostics/2026-11-01-exp004-mechanism/explore_power.py) on saved streams, after all verdicts, and added it to the paper labeled exploratory. False-alarm rates and the frozen-sentinel test are not yet done.

## 2 November 2026 — SAR extension and paper package

- Froze and ran the [SAR extension](experiments/004-monitor-blind-spots.md): NOT SHOWN (47/159 against 18/73). The 10:30 IST cutoff was removed at the user's request before any stream ran.
- Created [`paper/`](paper/) in Springer LNCS with `springer_overleaf.zip`. Compiled from a clean folder with pdflatex and bibtex; not tested on Overleaf itself. Author details are placeholders.
- AWS `predictions-cup` has zero GPU quota in us-west-1, so RunPod was used. An interrupted launch left an idle RTX 4090 pod for about 40 minutes, about $0.60; deleted. Balance $34.91.

## 2 November 2026 — Experiment 004 mechanism and authors' pipeline results

- Recorded all frozen verdicts in [Experiment 004](experiments/004-monitor-blind-spots.md): FIXED GAP HOLDS, ENTROPY ADDS, normalization NOT SHOWN, authors' pipeline REPRODUCED, PORT AGREES. Execution deviations (out-of-memory reruns of streams with no row) are recorded there.
- Added exploratory [`explore_masses.py`](diagnostics/2026-11-01-exp004-mechanism/explore_masses.py), run after the verdicts on saved streams only.
- These results supersede the "pending" status of C2 and the authors' pipeline in the adversarial review; the review file is unchanged as a dated record. Pod deleted after hashes matched; balance $40.03.

## 2 November 2026 — SSRN7602585 download follow-up

- Attempted public SSRN delivery routes, fresh browsers, bibliographic/repository lookups and the author's verified site/repository. No complete PDF retrieved; verification continued looping after six user attempts. Further challenge retries stopped.
- Saved [access evidence](notes/ssrn-7602585-retrieval-2026-11-02/retrieval-report.md); corrected the source's erroneous arXiv classification to SSRN. No experiment, full-text reading, or novelty-verdict change. No external messages sent.

## 2 November 2026 — adversarial novelty review of Experiment004

- Created [claim-by-claim review](notes/novelty-review-2026-11-02/review.md), repeatable search/screen ledgers, close-work matrices, primary evidence/manifests, provenance, and independent verification/critique records.
- Recovered 20 Schirmer citers from Scholar/S2 plus PORTAL through final adversarial follow-up; traced preprint/workshop/host versions and documented index disagreement/rate limits. Global citation saturation was not reached.
- C1/C2: no exact matching accessible report found, with explicit coverage limits; C2 and authors'-pipeline outcomes remain locally pending. C3 substantially anticipated; C4 general vulnerability already published; C5 partially covered.
- Added 32 distinct source records (library 148), preserved stable keys and old reading histories, corrected stale publication metadata for SHSD/D3M/PPRM, and added/updated source notes. Central files were backed up before append-only migration.
- No experiments, model runs, implementation tests, package installation, or paid compute. Python retrieval/document work used `uv run --no-project`. SSRN/TRUST-ADAPT/ODFD full texts and parts of the citation graphs remain unresolved.

Next: resolve blocked close work and document the already frozen causal/implementation checks before advancing the diagnostic or a remedy.


## 1 November 2026 — Experiment 004 replication

- Frozen Tent-versus-source rule passed: 89% against 40% missed, all six models. Authors' code ran with a disclosed patch; no Dirichlet option. Cost $1.77; balance $44.97; this project's pod deleted.

## 1 November 2026 — Experiment 004 confidence test

- Four more models. Frozen prediction not supported. Post-hoc pattern across six models recorded as unconfirmed. Authors' code failed on a dependency I omitted. Balance $46.75; no pods running.

## 1 November 2026 — Experiment 005

- Collision search found no direct study. Ran 1,920 CelebA streams with 3 seeds and 2 targets. Frozen rule not met; a design flaw tied group mix to class mix. Candidate not supported. Balance $49.13; no pods running.

## 1 November 2026 — future-work gap review

- User chose to change direction. Extracted future-work passages from 42 library papers, ran targeted searches and wrote the [gap review](outputs/future-work-gaps-2026-11-01.md). Library now has 116 records. No model run.

## 1 November 2026 — Experiment 004 second model

- Confirmed the code differs from the paper on the Hoeffding terms, in the alarm-prone direction. The second model failed the frozen rule (13 of 24 missed). The authors' code failed on import. ImageNet-C skipped. Balance $49.98; no pods running.

## 1 November 2026 — Experiment 004 confirmation

- Frozen confirmation passed on final IDs and held-out families: 20 of 20 missed for Tent under Dirichlet 0.1, Assumption 1 intact. Effect concentrated at strong skew. Top share mainly detects skew. RunPod pod deleted; balance $50.56.

## 1 November 2026 — Experiment 004 Q1

- Ran 136 monitor streams on development IDs, using a port of the authors' monitor. Gate passed; the strict post-hoc check narrows it to Tent under persistent class skew, 12 of 12 missed with Assumption 1 holding. No false alarms. RunPod pod deleted.

## 31 October 2026 — candidate B dossier

- User chose candidate B. Wrote the [dossier](outputs/candidate-b-dossier-2026-10-31.md) and planned [Experiment 004](experiments/004-monitor-blind-spots.md). Added five library records. No new model run.

## 31 October 2026 — Experiment 003 first stage and Review II notebook

- Ran Experiment 003 on fold 1 development data, seed 1, on a RunPod RTX 4090. The H0 gate failed: 0.45 pp cross-fit headroom (95% interval -0.44 to 1.67, threshold 1.0). The final pool is untouched. Tuned UPDATE was close to a no-op, so decay was not strongly tested.
- Ran the post-hoc stronger check (`run_strong.py`). Mechanism not supported; change-stream selector error grew with exposure, an unverified lead. See Experiment 003.
- Saved-data follow-up (`analyze_change.py`): change-stream lead rejected, entropy sign flip retracted, design flaw recorded. RunPod pod left running idle pending user approval to delete; balance fell from $62.89 to $57.52 by 22:15 IST.
- Added `review2_three_feature_gate.ipynb`, a fresh five-seed digits implementation written from the report and executed locally with uv. Three-feature gate 79.2 ± 2.2%, concentration-only 79.7 ± 2.2%, SOURCE 78.2 ± 2.8%, always normalize 62.2 ± 1.5% on all families. This neither reproduces nor validates the external Review II table.

## 31 October 2026 — novelty dossier and refined candidate

- Attacked candidate A against primary text and wrote the [dossier](outputs/novelty-dossier-2026-10-31.md). Result: H1 is prior art, H2 is demoted, H3 is a control. New working candidate A′ (evidence decay under adaptation) is unverified; AETTA and Cygert et al. are its closest neighbours.
- New evidence: Harness Learning §5.4 reports no consistent gain from training on successive states (LLM setting). RNA keeps original weights frozen. ASR's code restores the optimizer on reset. Our arithmetic on MORPHEUS Table 1 gives about 0.5 points of per-domain oracle headroom over SPA.
- Added [Experiment 003](experiments/003-evidence-decay-under-adaptation.md), planned only. Experiment 002 stays on record and would follow only if 003 passes.
- Library grew from 103 to 107 records through the append-only [apply_records.py](notes/novelty-refresh-2026-10-31/apply_records.py); pre-change copies are in `notes/novelty-refresh-2026-10-31/backup-before-apply/`. Evidence text and hashes are in `notes/novelty-refresh-2026-10-31/evidence/`. Rerunning the 26 October `build_library.py` would drop these additions.
- `feynman alpha search` still returns `Unknown alpha command: search`; web search and primary texts were used instead. SLRF's full text remains closed. No model run, test or dependency installation.

Next step: authorize execution and name a machine, then run the Experiment 003 timing probe.

## 31 October 2026 — successor handoff and full context export

- User requested all necessary learned context and a handoff so another agent can find genuine novelty and complete a solid research piece; continued after an intentional interruption.
- Wrote [HANDOFF.md](HANDOFF.md) and [NEXT_AGENT_PROMPT.md](NEXT_AGENT_PROMPT.md) with user intent, novelty collisions, candidate alternatives, exact reviewed protocol, historical/local/external result distinctions, benchmark constraints, remaining unknowns, script hazards and research milestones.
- Exported every indexed source into [a readable dossier](notes/handoff-2026-10-31/source-dossier.md), and saved a project [artifact manifest](notes/handoff-2026-10-31/artifact-manifest.json). Source catalog and scientific outcomes remain unchanged. The exporter reads current records and does not invoke historical bibliography/model scripts.
- Added [the durable session log](notes/session-logs/2026-10-31-research-handoff.md) and linked the handoff from README/AGENTS. The last substantive literature search remains 26 October, with 103 records and explicitly selective reading; no fresh novelty certification is claimed.
- No research experiment, implementation test, dependency installation, paid compute or new literature retrieval was performed for this handoff.

Next step for the successor: read the handoff; refresh/attack the precise novelty claim and write a closest-art dossier; move to the smallest residual-headroom diagnostic only under the next task's actual execution scope and conditions.

## 26 October 2026 — fresh deep review and novelty reset

- Honored the user's instruction to disregard earlier choices when reassessing novelty. Preserved the old gate/acquisition records, local diagnostic and externally reported aggregate results as history.
- Expanded the library from 48 to 103 distinct records: 101 scholarly works plus two benchmark documents; 55 additions and 68 fresh selective source inspections. Stable keys, linked versions, reading scopes and publication qualifications remain explicit. Added CSV export and dated source histories; archived original catalog/index/BibTeX with hashes.
- Reverified direct collisions and added substantial missing prior work: normalization/prior methods, current benchmark programs, efficient/VLM alternatives, recent theory, Agentic-TTT and DAgger. Rejected broad shift-aware routing as sufficient novelty.
- Wrote [new review](outputs/shift-aware-tta-deep-review-2026-10-26.md), [provenance](outputs/shift-aware-tta-deep-review-2026-10-26.provenance.md), benchmark/source investigation and [Experiment 002](experiments/002-state-conditioned-selection.md), all with honest planned/unrun status.
- Recommended first diagnosing selection on policy-generated live states, conditional on significant residual effects beyond current-model evidence, reset/optimizer controls and ordinary dataset aggregation. No verified gap, successful controller or conference-ready result is claimed.
- Independent critique/verification clarified BN action semantics, state-pure inference, RNG/time, SOURCE versus RESET, development-label/compute accounting, original-ID separation, rich current evidence and distinct nextblock64/frozen512 horizons.
- Saved seven primary HTML snapshots plus one additional official PDF/extracted text with hashes. Alpha semantic-search CLI remained unavailable; used available primary-source tools and skill-prescribed researcher/verifier/reviewer roles. No experiments, implementation tests, installations, datasets/checkpoints or paid compute were run/downloaded.

Next step: complete precise overlap checks, freeze the protocol and choose execution conditions when requested; test only initial residual headroom before building a controller.

## 23 October 2026 — shift-aware-tta-review

- Opened a separate research prospect and preserved the user's original title/abstract as a proposal.
- Indexed 47 distinct primary scholarly sources with reading scopes, citation keys and publication/version qualifications. Saved 9 paper PDFs and extracted text with a retrieval/hash manifest.
- Found direct overlap in Hybrid-TTA, SLRF, MORPHEUS, expert-routing methods and AdaTent++; rejected the broad novelty premise.
- Inspected limitations and recent evidence-selection neighbors, including the identifiability preprint, SA-TTS, CAS, SEGA, MoASE++, Tempora and general acquisition work.
- Proposed a narrowed, unverified question about the net decision value of costly observations for adaptation selection. Recorded a secondary live-state selection branch.
- Wrote the cited review, provenance and staged experiment protocol. Independent verifier/reviewer passes led to all-in route-cost accounting, nested grouped validation, explicit Tent/BN query semantics, finite-query uncertainty, fixed/oracle distinctions and separate continual evaluation.
- No research experiment, implementation test or dependency installation was performed. The alpha paper-search subcommand was unavailable; available primary-source web tools supported the investigation.

Next step: select a legitimate source-model/development-data regime and implement the small action-headroom diagnostic only when execution is requested. Continue toward a learned gate only if action and evidence headroom exist.

## 23 October 2026 — bounded diagnostic execution

- The user explicitly authorized running the diagnostic with subagents within 15 minutes. Start 17:48:26 UTC; execution/report artifacts recorded by 17:57:51 UTC, within the requested limit.
- Implemented a NumPy/scikit-learn CPU surrogate using bundled digits because PyTorch/torchvision were not installed. No packages were installed. Initial source commands used existing Python; following the user's explicit instruction, runs/checks used uv, and no pip was used.
- Executed three fixed source/split repeats, totaling 1,920 correlated episode definitions and 5,760 three-action outcomes, plus ensemble, acquisition and limited robustness controls. These are not independent datasets or original-paper benchmark replications.
- All three stages were exercised: action headroom, cheap versus rich evidence, and acquisition controls. Rich evidence improved held-out accuracy variably; the calibrated acquisition policy chose zero acquisition at all positive declared cost penalties in every repeat.
- Additional checks covered four family holdouts, a post-hoc concentration gate, linear-inference timing sensitivity, analytic entropy gradients, immutable state, original-ID separation, outcome integrity and query-identity sensitivity. Three source convergence-limit warnings are retained.
- Saved [results](outputs/shift-aware-tta-diagnostic-2026-10-23.md), [raw artifacts](diagnostics/2026-10-23/), [audit](diagnostics/2026-10-23/audit.md), [run manifest](diagnostics/2026-10-23/run_manifest.json) and [uv recipe](diagnostics/2026-10-23/autoresearch.sh). Broader datasets, faithful modern backbones and continual controllers remain unrun.

Next step: preserve the negative acquisition result. A simpler low-dimensional selector on a faithful model and fresh split is a possible follow-up; no automatic paid or large-scale experiment is scheduled.

## 23 October 2026 — select one working approach

- The user asked to choose and define one approach under tighter time constraints, without requesting another experiment.
- Selected [cheap harm prediction for test-time normalization](outputs/selected-approach-cheap-normalization-gate.md): one depth-two gate with predicted concentration, entropy and source-relative feature displacement; actions SOURCE or normalization.
- Defined the main empirical question around matched predicted concentration under genuine class-mixture change versus corruption-induced prediction collapse, with dominant-class and corruption-family holdouts. Hidden labels construct/evaluate research cases but never enter runtime gating.
- Researcher/reviewer checks agreed the simple gate is a baseline, not established algorithmic novelty. Added the close channel-selective-normalization predecessor to the verified index (48 sources total; original review47). Exact overlap of the proposed matched-case protocol remains open.
- Preserved the original concentration rule as post-hoc exploratory evidence; it neither validates the proposed three-feature gate nor proves efficiency or conference readiness. No new diagnostic was run.

Next step: freeze the protocol and verify evaluation overlap before fresh confirmation. Use uv for Python work.

## 2026-11-03
- exp005: rich/learned detector test on BloodMNIST and DermaMNIST. Primary verdict NOT SHOWN (learned detector selected on dev lost to the twin). Secondary: twin with dev-calibrated margin missed 9/165, false alarms 15/185. Paper not updated, as asked.
- exp006 frozen confirmation (PathMNIST, OrganAMNIST, CIFAR-100-C x6; 2,592 streams): NOT CONFIRMED. Twin missed 13%, false alarms 2.4%; published monitor 49%/2.1%; same-margin monitor 26%/5.4%; required gaps not met (0.13 vs 0.15; 0.04 vs 0.15 over exp004 bound).
- exp007 diagnosis (exploratory): conditions 3/4 of exp006 were mis-specified (absolute gaps, unmatched FA). At matched FA the twin cuts misses 66-72% vs the released signal and the exp004 bound; within-group AUROC 0.992 (best). The weak part is transfer of the dev-calibrated alarm level (realised FA 2.4% on exp006 vs 5.9-7.6% on exp005 from the same 5% rule). laya assessed: not applicable beyond the conditional-calibration idea.
- Paper updated (3 Nov, 13:15 IST): new title; abstract; contribution 7; new section "Alarm Levels Calibrated on Shifted Development Streams" (exp005/006 results, frozen verdicts with the criteria flaw stated, matched-FA table, level-transfer diagnosis); medical section points to 4 MedMNIST sets; Limits and Conclusion updated; bib: Vovk2005ALRW, Guillory2021DoC, Ke2017LightGBM. All new numbers verified by script against report JSONs; 19 pages, 0 LaTeX errors.
- exp008 launched on SageMaker (13:27 IST): frozen relative/matched-FA protocol, fresh OCT/OrganC/Pneumonia + CIFAR new seeds, 13 signals x 3 calibrations incl. isolation forests at stream/batch/image level, dominance and conformal test martingale. Self-analysing; reports copied to s3://vbb-exp008-286879406788-use1/results/<job>/.
- exp008 partial (CIFAR only, descriptive): twin+pattern 14.9% missed / 3.2% FA vs published 44.8% / 4.3%; matched-5% best = monotone LightGBM 3.6%; isolation forests did not help. Medical half failed (fetch() clobbered class count; bare wait hung the job; ~$45 wasted); bugs fixed, rerun pending user decision.

## 2026-11-04
- exp008 medical rerun (jobs m: OrganC + Pneumonia; p: OCT) completed and self-terminated; merged with CIFAR, 3,948 streams (351 strict, 637 safe held-out).
- exp008 frozen verdict: NOT CONFIRMED. C1 met (matched-5% misses 11.1% vs released 25.9%, −57%); C2 met (2.5% FA pooled); C3 failed (31.9% missed vs published 59.5%: −46% relative met, 20% ceiling not met). Cause: dev-calibrated level too high on medical sets (0 FA on each; Pneumonia 38/38 missed).
- Exploratory: monotone LightGBM|Z 14.5% missed / 1.9% FA (best matched-5%, 6.3%), chosen after the CIFAR partial, so it is a candidate for a fresh frozen test only. Paper not yet updated with exp008.
- All exp008 AWS resources deleted (see AWS_RESOURCES.md).

## 2026-11-14
- exp009 (exploratory): isolated the uneven transfer of the dev-calibrated alarm level on saved exp005/006/008 streams; see experiments/009. Chose a family-validated alarm (FV) on already-seen streams.
- exp010 frozen (protocol, criteria, file hashes in experiments/010) after a read-only pre-run review by the Codex session; two SageMaker jobs launched, results pending. AWS bucket and role vbb-exp010-* are ACTIVE (AWS_RESOURCES.md).
- Paper source partly reframed (coupling subsection, hypotheses table, third study, level-failure isolation with new figure, FV design). UNFINISHED: abstract, introduction, exp010 results section, discussion and conclusion still describe the old framing; PDF and zip not rebuilt.
- 08:25 IST: the `predictions-cup` AWS key was rejected (InvalidAccessKeyId), so exp010 status/results/teardown could not be reached; no other credentials were tried. Paper reframing finished with exp010 marked pending: new title and abstract, four-step introduction, hypotheses table (E1–E10), exploratory time-resolved separation (AUROC 0.98 to 0.42–0.46 for Tent, 0.99 for the twin), frozen exp010 protocol in Sect. 9.2, updated discussion, limits and conclusion. 24 pages, 0 LaTeX errors; new numbers checked against diag3.json, harness_rows.json and the analyze10 dry-run reports. README updated.
- AWS credits exhausted (user report). exp010 moved to a free GPU notebook: `diagnostics/2026-11-14-exp010-confirm/kaggle/` (self-contained notebook with the frozen code, four resumable parts) and `analyze_local.sh`. Still no exp010 result.
- exp010 ran on RunPod (3 pods, 2 x RTX 4090 each, $9.76; all pods deleted). 4,630 streams complete. Frozen analysis, run once: **PARTIAL** (C1, C2, C3 met; C4 failed on its false-alarm band: 30/399 = 7.52% against 7.5%). FV missed 22/272 (8.1%) against 171/272 for the published monitor and 40/272 for the earlier rule. Coupling: SHOWN for Tent and pseudo-labels, NOT SHOWN for information maximisation; decay SHOWN for all three. One calibration.json repaired (extra brace from a concurrent write; original kept).
- Paper updated with the exp010 outcome: abstract, introduction step 4, Table 1 row E10, Sect. 9.2 results with Table 10 and Fig. 4 (decay), discussion, limits, conclusion. 26 pages, 0 LaTeX errors; numbers taken from results/report10.json and rows10.json.

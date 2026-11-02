# Project research log

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

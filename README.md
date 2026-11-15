# Valid but Blind: test-time adaptation and label-free risk monitoring

**Finding:** on CIFAR-100-C with strong class skew, a released label-free risk monitor missed Tent's clear failures far more often than a frozen model's (147/166 vs. 44/110). Tent's entropy step adds the misses. An entropy-free twin alarm cut misses on held-out corruptions from 94/109 to 30/109, with 5/121 false alarms. It is a detector with no guarantee, and its test on adaptation-caused failures returned NOT SHOWN under the frozen rule. The latest family-validated alarm has completed its frozen test: 22/272 failures missed (8.1%) at 30/399 false alarms (7.52%). The verdict is **PARTIAL**, because the 7.5% level-transfer band was exceeded. Novelty is not established.

**Rights:** original project material is **all rights reserved**. Reuse requires Rohit Phaniram Sakamuri's **prior express written permission**, subject to applicable law, GitHub's platform terms and retained third-party licenses. See [LICENSE](LICENSE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). Public visibility does not grant an open-source or general reuse license.

Current methods, saved results and reproduction boundaries are indexed in [REPRODUCIBILITY.md](REPRODUCIBILITY.md). The completed submission files are in [reports/reviews](reports/reviews/README.md).

| Where | What |
| --- | --- |
| [`paper/`](paper/) | Manuscript (Springer LNCS), PDF preview and Overleaf zip |
| [`reports/assessment/`](reports/assessment/README.md) | Plain black-and-white assessment report for Rohit Phaniram Sakamuri, 23BDS0051; editable Word and PDF |
| [`reports/reviews/`](reports/reviews/README.md) | Completed Review I, II and III template-based decks, PDFs, Word summary and A3 poster for Rohit Phaniram Sakamuri, 23BDS0051; presentation content omits dates |
| [`demo/`](demo/README.md) | Live laptop demo. Run `demo/fetch_data.sh`, then `demo/run_demo.sh` |
| [`experiments/004-monitor-blind-spots.md`](experiments/004-monitor-blind-spots.md) | Protocols, frozen rules and all verdicts (later studies: 005–010 in the same folder) |
| [`diagnostics/`](diagnostics/) | Run and analysis code, per-stream results and reports |
| [`notes/novelty-review-2026-11-02/review.md`](notes/novelty-review-2026-11-02/review.md) | Literature review and its coverage limits |
| `Valid but Blind*.pptx` | Presentation decks |

Datasets, checkpoints, saved tensors and third-party PDFs are not in this repository. Python runs use [uv](https://docs.astral.sh/uv/). The sections below are the original project record.

---

# Shift-aware test-time adaptation

## Historical review — 2 November 2026

The [adversarial novelty review](notes/novelty-review-2026-11-02/review.md) narrows the monitor finding. C1 exact adapted/frozen miss-rate comparison: no matching report found within incomplete coverage. C2 fixed-threshold/entropy-versus-BN contrast: no matching accessible report found, **and locally still pending**. C3 mechanism: substantially anticipated. C4 general self-masking vulnerability: already published; universal wording unsupported. C5 independent label-free remedy: partially covered by existing methods; no exact sensitive fix established.

Known prior art includes Schirmer's own proxy-failure/repair experiment, AETTA, corrupted Dirichlet model-selection experiments, Han's self-masking/frozen-sentinel study, and recent calibration/monitor-staleness work. The library has 148 records, 32 added. [Queries/screens/evidence](notes/novelty-review-2026-11-02/) preserve reading scope. 21 Schirmer citers are known from 20 indexed titles plus PORTAL. Citation saturation was not reached; SSRN/TRUST-ADAPT/ODFD full texts remain blocked. No experiments or implementation tests ran.

**Next concrete step:** resolve blocked close predecessors and finish documenting the already frozen implementation/factorial outcomes before strengthening C2 or proposing a fix. Retain only a bounded diagnostic claim; broad confidence failure and independent monitoring are established ideas. Earlier dated statuses below are historical, not the current conclusion.


New research prospect opened 23 October 2026: infer properties of an unlabeled deployment stream and select an adaptation action suited to its current conditions.

## Agent handoff — 31 October 2026

**Start with [HANDOFF.md](HANDOFF.md)** for the complete research context, closest prior art, unresolved novelty, actual/historical results, exact proposed protocol, file/tool hazards and continuation plan. [NEXT_AGENT_PROMPT.md](NEXT_AGENT_PROMPT.md) is a paste-ready bootstrap. The [handoff package](notes/handoff-2026-10-31/README.md) includes a full 103-source dossier and artifact inventory. This is a documentation handoff; the last substantive literature search remains 26 October and Experiment 002 remains unrun.

## Current status — 31 October 2026

[Novelty dossier](outputs/novelty-dossier-2026-10-31.md): candidate A's history-effect claim is prior art, its deeper-state claim has low expected value, and its aggregation remedy is a control rather than a contribution. The working candidate is now **A′, evidence decay under adaptation**, which is unverified. [Experiment 003](experiments/003-evidence-decay-under-adaptation.md) is its small falsification test and is **planned, not run**. The library has 107 records. SLRF's full text remains inaccessible.

**Update:** Experiment 003's first stage ran on fold 1 development data and **failed its headroom gate** (0.45 pp, 95% interval -0.44 to 1.67, threshold 1.0). UPDATE was close to a no-op at the tuned learning rate, so evidence decay itself was not strongly tested. See the [results](experiments/003-evidence-decay-under-adaptation.md#actual-results).

[`review2_three_feature_gate.ipynb`](review2_three_feature_gate.ipynb) is a fresh digits implementation of the Review II method. It does not reproduce the externally reported Review II table, and its gate ordering differs.

The exploratory stronger check ran too: the optimized-signal mechanism was not supported, headroom appeared only on degraded states and mostly as a reset choice, and selector error grew with exposure after corruption changes (unverified lead).

The saved-data follow-up rejected that lead: no evidence selector beat always RESET after a change, and knowing the next corruption closes almost all the gap. The entropy sign flip was a prefix-mixing artifact and is retracted. A′ is not supported in this setup.

**Candidate B, chosen by the user:** the [candidate B dossier](outputs/candidate-b-dossier-2026-10-31.md) rejects a universal proxy diagnostic and treats proxy-error prediction as crowded accuracy estimation. The working candidate is B′, monitor blind spots under combined corruption and class-prior shift, which is unverified. [Experiment 004](experiments/004-monitor-blind-spots.md) is planned, not run.

**Experiment 004 Q1 (development data only):** gate passed, but it overstates the finding. Under a stricter check added afterwards, the clear result is that Tent under persistent class skew (Dirichlet) grew more confident while error rose, and the monitor missed 12 of 12 violations. By-class order was caught in all 16 cases. Not confirmed on held-out data, and novelty is unchecked. See the [results](experiments/004-monitor-blind-spots.md#actual-results).

**Held-out confirmation passed for this setup:** Tent under strong persistent skew, 20 of 20 clear failures missed with Assumption 1 intact, while the same monitor caught 14 of 15 on the unadapted source at similar error. One checkpoint and dataset; effect concentrated at Dirichlet 0.1; novelty unverified. No alarm fix exists yet.

**Second model: the frozen rule failed.** PRIME ResNet-18 missed 13 of 24, not near-total, with Assumption 1 failing more often. The finding is model-dependent and is not a general result. The authors' code failed on import, so the port is unverified. The ImageNet-C step is not being run.

**Direction changed by the user, 1 November 2026.** The [future-work gap review](outputs/future-work-gaps-2026-11-01.md) recommends a new candidate question, unverified: does online adaptation widen error gaps between demographic groups, and does stream make-up drive this? Planned only.

**[Experiment 005](experiments/005-group-gaps-under-online-adaptation.md): frozen rule not met.** Effects on Blond_Hair appear driven by class mix, not group minority status, and Smiling shows little effect. Adaptation improved both groups at natural mix.

**Experiment 004 on six models:** the confidence prediction was not supported (Spearman 0.00 on new models). Post hoc, Tent is missed more than source in all six models, 78% vs 24% pooled, which needs fresh confirmation. The authors' code has still not run.

**Replication, 1 November 2026:** the frozen Tent-versus-source rule passed on CIFAR-100-C development images: missed 147/166 (89%) against 44/110 (40%), higher for Tent in all six models. The authors' code ran with a disclosed CIFAR-100 loader patch, but it has no Dirichlet stream, so the blind spot is not yet reproduced in their pipeline. Novelty is unverified.

**Mechanism and authors' pipeline, finished 2 November 2026 IST:** all frozen verdicts are in [Experiment 004](experiments/004-monitor-blind-spots.md). Fixed-threshold Tent was missed 109/109 against source 18/73 (gap holds). Tent was missed 94/109 against BN 37/154 (entropy adds). BN alone did not produce the gap across models (37/154 against 18/73). The authors' own code reproduced it (Tent 40/40, source 10/28), and alarms matched our port on 99.1% of streams. An exploratory split shows similar error with fewer flagged predictions under Tent. CIFAR-100-C and Tent only. The [adversarial review](notes/novelty-review-2026-11-02/review.md) found no report of the exact comparison, but coverage was incomplete and the broad mechanism is prior art; novelty is not established.

**SAR extension, 2 November 2026:** the frozen verdict is NOT SHOWN (SAR 47/159, source 18/73, higher in 3 of 6 models). SAR kept only 4-9% of samples on four models, so this is not evidence of a fix. The finding is therefore for Tent, not entropy-based adaptation in general.

**Paper:** [`paper/main.tex`](paper/main.tex), Springer LNCS, with Overleaf package [`paper/springer_overleaf.zip`](paper/springer_overleaf.zip). Due 2 November 2026, 12:00 IST.

**Twin alarm, 2 November 2026:** an entropy-free twin passed its frozen held-out test for an uncertified form (30/115 missed against 94/109), while its certified forms missed all violations. Its frozen test on adaptation-caused failures returned NOT SHOWN.

**Shifted-level alarms, 3 November 2026:**
- [Experiment 005](experiments/005-rich-detector.md): learned detectors did not beat the twin (NOT SHOWN).
- [Experiment 006](experiments/006-twin-confirmation.md): the twin with a level set on synthetic dev streams missed 13% at 2.4% false alarms on PathMNIST, OrganAMNIST and CIFAR-100-C. The published monitor missed 49% at 2.1%. The frozen verdict was NOT CONFIRMED, because its criteria used absolute gaps at unequal false-alarm rates.
- [Experiment 007](experiments/007-alarm-diagnosis.md) (diagnosis):
  - at matched false-alarm rates the twin misses 67–72% fewer failures than the two criteria comparators, and has the best AUROC (0.992);
  - ATC is close;
  - the level transfers unevenly from dev to held-out shifts.

**Paper:** updated 3 November with these results; all new numbers were verified by script. Author affiliation and email are still placeholders.

**Finished, 4 November 01:38 IST:** [Experiment 008](experiments/008-shifted-level-confirmation.md), a frozen confirmation on 3,948 streams (CIFAR-100-C, OCT, OrganC, Pneumonia). Verdict **NOT CONFIRMED**:
- ranking held: at matched 5% false alarms, twin+pattern missed 57% fewer failures than the released proxy;
- false alarms held: 2.5%;
- deployed misses failed: 31.9%, which is 46% fewer than the published monitor but above the 20% ceiling. The dev-calibrated level sat too high on the medical sets and missed every Pneumonia failure.

Exploratory: monotone LightGBM with calibration Z reached 14.5% missed and 1.9% false alarms. It was chosen after the CIFAR partial, so it needs a fresh frozen test. All exp008 AWS resources have been deleted.

Next step: the user decides whether to add exp008 to the paper, and whether to run a fresh frozen test of monotone LightGBM|Z.

**Level-transfer diagnosis and fresh test, 14 November 2026:**
- [Experiment 009](experiments/009-level-transfer-diagnosis.md) (exploratory, saved streams only): the dev-calibrated level failed because a constant level was applied to a score that Tent keeps moving, and because no single signal has power on every dataset. Leave-one-shift-family-out validation on dev streams forecast the misses (Spearman 0.73) but not the false alarms.
- Candidate fix, the family-validated (FV) alarm: per deployment, choose between the twin, Tent's confidence with a time-resolved level, and the exp008 fusion by leave-one-family-out validation. On the already-seen exp005/006/008 streams it missed 2/86, 16/307 and 22/351. Those streams shaped the rule, so this is not evidence.
- Exploratory mechanism read-out on exp006/exp008: Tent's confidence separates failing from safe streams with AUROC 0.98 in the first 20 batches and 0.42–0.46 in the last 20; the twin stays at 0.99.
- [Experiment 010](experiments/010-family-validated-alarm-confirmation.md), frozen and run on unused data (TissueMNIST, OrganSMNIST, CIFAR-10-C; 4,630 streams on RunPod): verdict **PARTIAL**. FV missed 22/272 (8.1%) at 30/399 false alarms (7.5%), against 171/272 for the published monitor and 40/272 for the earlier rule. Ranking, safety and power criteria held; the level-transfer criterion failed because false alarms exceeded its 7.5% band by a fraction of one stream. The blind spot was shown for Tent and for pseudo-labels, not for information maximisation.
- Paper reframed around the coupling between an adaptation objective and its monitor, with Tent as the worked case. The current manuscript includes the exp010 PARTIAL result and the full comparison table.

Next step: the user decides how to present the PARTIAL verdict. Open scientific items: realised false alarms above the 5% target on CIFAR-10-C, TissueMNIST misses (11/55), natural shifts, and models without batch normalization. Delete `vbb-exp010-*` from the AWS console if that account is still open.

## Research status

Current status, 26 October 2026: **fresh novelty assessment completed at the user's request**. The [deep review](outputs/shift-aware-tta-deep-review-2026-10-26.md) maps 18 research directions and their limits, benchmark protocols and direct prior-art collisions. The library now contains 103 distinct records (101 scholarly sources and two benchmark documents); 55 are additions and 68 received fresh selective inspection. Broad shift-aware policy routing is already established. No verified conference-ready gap or new benchmark result is claimed.

The recommended first investigation is [Experiment 002](experiments/002-state-conditioned-selection.md): does a visual TTA selector remain useful on the live model states created by its own decisions? Its exact novelty remains unverified; state-aware control, exposure bias and dataset aggregation are prior art. The protocol requires residual headroom beyond rich current-model evidence, strong reset/update controls and equal-budget learner-state aggregation. **All new experiments remain planned.**

Historical status, 23 October 2026: literature review and experiment design were followed by a user-authorized bounded CPU diagnostic. Three source/split repeats covered action headroom, richer evidence and acquisition controls on custom shifted digits. That study did not validate cost-aware acquisition. Original image benchmarks remain unrun. Earlier favored approaches/results do not determine the fresh recommendation.

Keep this prospect separate from the earlier CPU OOD study and other research projects. Prior budgets and submission milestones are not current commitments for this project.

## Review II progress report

The user subsequently reported completing the three-feature gate on another system and supplied actual aggregate results across five seeds: SOURCE 76.4 ± 1.0%, always-normalize 74.8 ± 1.8%, concentration-only gate 77.3 ± 1.1%, and three-feature gate 77.9 ± 0.9%. Harmful-update episodes were 31%, 15% and 11% for the three updating policies. These user-reported external results supersede the earlier planned-only status for the gate; raw runs and configuration manifests have not yet been imported. They remain separate from the recorded local three-seed digit diagnostic.

The [Word report](reports/review-ii/Shift_Aware_TTA_Review_II.docx) and [presentation](reports/review-ii/Shift_Aware_TTA_Review_II.pptx) follow the supplied `Review2.pptx` section order. The original template is preserved. [Report source](papers/review-ii-five-seed-progress.md), [builder](reports/review-ii/build_report.py) and [result provenance](reports/review-ii/result_provenance.json) are saved. No new model experiments were run for document preparation.

Historical follow-up: consolidate the external code and seed-level results if that earlier gate study is resumed. These aggregates do not validate the new state-distribution proposal.

## Current review and proposed study

- [Fresh deep literature review and novelty audit](outputs/shift-aware-tta-deep-review-2026-10-26.md).
- [Benchmark, metric, protocol and limitation matrix](notes/review-refresh-2026-10-26/benchmarks.md).
- [Provenance, reading scope and source accounting](outputs/shift-aware-tta-deep-review-2026-10-26.provenance.md).
- [Experiment 002: state-conditioned selection](experiments/002-state-conditioned-selection.md), planned only.
- [Final scientific verification](notes/review-refresh-2026-10-26/final-verification.md) and [critique](notes/review-refresh-2026-10-26/final-review.md).
- [Reference index](REFERENCES.md), [BibTeX](references.bib), [JSON catalog](sources/catalog.json), [CSV catalog](sources/catalog.csv), [reading/source ledgers](notes/review-refresh-2026-10-26/) and [preserved original library](sources/library-before-refresh-2026-10-26/).

## Historical selected working approach — 23 October

Retained as history. The user permitted a clean-slate reassessment, especially novelty; this earlier choice is not the current recommendation.

[Approach only](APPROACH.md).

[Cheap harm prediction for test-time normalization](outputs/selected-approach-cheap-normalization-gate.md): a depth-two, three-feature gate chooses SOURCE or a support-statistics update. The candidate empirical contribution tests whether genuine class concentration and corruption-induced prediction collapse lead to different action benefits at matched predicted concentration. This is a concrete direction to investigate; its novelty and high-quality-conference suitability remain unproven. It was defined after the diagnostic and has not received fresh validation.

## Historical reading and diagnostic records

- [Completed diagnostic results](outputs/shift-aware-tta-diagnostic-2026-10-23.md): three source/split repeats, 1,920 correlated episode definitions, headroom/evidence/acquisition comparisons, simple controls and limitations.
- [Diagnostic code and artifacts](diagnostics/2026-10-23/), [audit](diagnostics/2026-10-23/audit.md) and [uv execution recipe](diagnostics/2026-10-23/autoresearch.sh). No packages were installed.
- [Literature review and proposal](outputs/shift-aware-tta-review.md): closest prior art, limitation chain, candidate gap and proposed approach.
- [Provenance](outputs/shift-aware-tta-review.provenance.md): source accounting, checked locations, access/version limits and review stages.
- [Experiment 001](experiments/001-policy-selection-pilot.md): larger proposed protocol, with the completed bounded surrogate diagnostic linked separately. Full benchmark execution remains planned.
- [Reference index](REFERENCES.md), [BibTeX](references.bib), [source catalog](sources/catalog.json): now 103 records with reading scopes and paper notes. The original review covered 47 sources, expanded to 48 during earlier approach selection; that library snapshot is preserved.
- [Downloaded papers](sources/pdfs/) and [retrieval manifest](sources/manifest.json): 9 PDFs with extracted text and hashes.
- [Research branches](notes/research-branches.md) and [original proposal](notes/original-proposal-2026-10-23.md).
- [Research log](CHANGELOG.md), [verification](notes/shift-aware-tta-review-final-verification.md), [critique](notes/shift-aware-tta-review-final-review.md) and [workflow plan](outputs/.plans/shift-aware-tta-review.md).

Next step: finish the exact-overlap checks identified in the fresh review, freeze Experiment 002's source/development/state protocol, then run its initial residual-headroom diagnostic only when execution and environment/compute conditions are specified. Do not develop a large controller if simple controls remove the problem. The earlier costly-evidence result remains negative. Use uv rather than pip for future Python work; no experiment is automatically scheduled.

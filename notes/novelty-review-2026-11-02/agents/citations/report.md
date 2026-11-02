# Citation tracing and close forward neighbors

Search/reading date: **2026-11-02, Asia/Kolkata**. Research only: no experiments, tests, model runs, package installation or external messages. Python was invoked with `uv run --no-project` using the standard library. This subreview writes only its assigned review/evidence directories.

## Findings that matter for the verdict

The canonical Schirmer paper now has a substantially better citation audit than the 1 November note: **20 distinct forward-citation titles** were recovered from Google Scholar and Semantic Scholar combined. There is **no fully inspected direct report of C1 or C2 in these citation neighbors**. This statement is limited: several forward citations were title/abstract screened and the SSRN close source was inaccessible here; the adjacent subreview investigates it. It is not proof of absence.

Important additional predecessors are:

- **Atarmla, arXiv:2609.23254:** an adaptive threshold can absorb persistent faults and return the alarm rate to its target. This substantially anticipates the broad self-masking-monitor narrative in C4. Its scalar quantile tracker is different from updating a classifier while holding the threshold fixed.
- **Shaer et al., ICML2026, arXiv:2602.13848:** expanding the conformal reference set makes sustained changes look normal. Fixed-reference tests retain power. The paper explicitly requires a **fixed scoring function**, so it is not a remedy for adaptation modifying confidence.
- **Khazem and Serouis, CASTER, arXiv:2609.00374:** an independent frozen-feature geometry gate works for its own transport mechanism but transfers very poorly to Tent. Merely proposing an independent signal is already anticipated and is insufficient as a contribution or fix.
- **Wang et al., arXiv:2609.20700:** source/live disagreement geometry predicts harmful adaptation edits better than confidence on some medical benchmarks and controls rollback/stopping. It also fails in reported regimes and needs labeled offline threshold selection.
- **Tang, REFIT, arXiv:2610.08991:** performs label-free ATC verification after input/BN correction and abstains on unrecovered sensor shifts. It demonstrates practical verification, with no sequential false-alarm guarantee.
- **Schirmer et al., arXiv:2607.02510:** monitors LLM outputs with an external verifier; its signal ablation reports substantially more power than internal token confidence at matched false-alarm settings. This is adjacent independent-verifier monitoring rather than TTA.

These make C5's generic design space crowded. None establishes that its method stays sensitive under the project's exact Dirichlet/corruption/Tent failure.

## Schirmer identity and version map

Canonical key remains `Schirmer2025Monitoring`. Primary title is *Monitoring Risks in Test-Time Adaptation*. Authors: Mona Schirmer, Metod Jazbec, Christian A. Naesseth, Eric Nalisnick; official proceedings expand Naesseth's middle name. Official NeurIPS record is **Advances in Neural Information Processing Systems 38**, DOI **10.52202/085713-2705**, not volume39. The repository README and Scholar's 2026 date are inconsistent with the official conference metadata; they do not change the canonical key/year.

Verified versions/hosts:

| Version | Evidence and status |
| --- | --- |
| arXiv2507.08721v1 | Submitted11 July2025; arXiv submission history. |
| arXiv2507.08721v2 | Revised8 November2025; arXiv submission history, current main preprint. |
| ICML2025 PUT workshop | OpenReview forum `k14ktterKG`, PDF hash `fe3f4ba2a11506af0889b1f1e625c2e16ac116f7`; official accepted-paper list and schedule identify paper72 and oral18 July2025. Header says PMLR267 but a standalone PMLR paper record was not verified. |
| NeurIPS2025 | OpenReview forum `TzHX2RWUdE`; proceedings hash `746960ad49ddb47248970a0e1404230c`, DOI above. |
| Institutional copy | `https://pure.uva.nl/ws/files/340219841/085713-2705open.pdf`; UvA record `6156d96b-db4d-4ac9-ade9-77bd59197db0`. Scholar lists these among6 versions, not independent research papers. |
| Other conference hosts | `papers.neurips.cc` PDF and ACM DOI landing page are copies/records of the same paper. |

The Google Scholar cluster is **7250704993477156062**. Its “all6 versions” list includes conference copies but omits the separate workshop/preprint hosts; the version map therefore combines it with arXiv and the official workshop list. No alternate title was discovered.

## Forward citation audit and limits

| Index | Actual retrieval | Limit |
| --- | --- | --- |
| Google Scholar | Title query, “all6 versions”, cited-by pages start0 and10 saved. These pages contain16 entries,15 unique titles (sports maintenance occurs twice). | Title page count16, page0 says13, page2 says16; further20-per-page/date-sorted/arXiv probes return429. Enumeration is not a certified16-paper set. |
| Semantic Scholar | `ARXIV:2507.08721` resolves to paperId`6631660c936a204606798af54c5235d0c729203e`; citation count12. Citation endpoint limit100 returns12 records and no next cursor. References endpoint limit100 returns80 records and no next cursor. | Snapshot complete for this canonical S2 record; published DOI lookup404; workshop may not be separately indexed. Reference80 includes an obvious checklist-text extraction artifact. |
| OpenAlex | Exact-title recordW7197038270 (published DOI); direct arXiv DOI recordW6929305892. Both report0cited and citations queries return0. | Strong disagreement with Scholar/S2. A DOI-filter query also fails to recover the directly accessible arXiv record. Empty index is not evidence of no citers. Broad search returned981,624 hits and only first100; used for identity discovery only. |
| Crossref | Exact/title/bibliographic works queries and DOI record saved. Canonical DOI reports1citing work. | Crossref's public works response does not identify its forward citer. Count1 does not provide an exhaustive citation list. |
| OpenReview | Workshop and main forum identities located; static forum shells reachable. | API notes endpoints403, direct workshop PDF403. Search-index excerpts/official list support version identity, not a complete discussion/review audit. |
| DBLP | Canonical NeurIPS record confirmed through indexed HTML. | XML endpoint202 serves challenge content rather than XML. DBLP provides identity, not complete forward citations. |

### Forward citation union

The S2-only records and Scholar-only records are retained, even when one index omits them. Titles are deduplicated, not citation counts summed.

1. *Adapt in the Wild: Test-Time Entropy Minimization with Sharpness and Feature Regularization* (2509.04977): primary abstract verified; SAR extension/SAR², not full monitor evaluation audited here.
2. *E-valuator: Reliable Agent Verifiers with Sequential Hypothesis Testing* (2512.03109): primary abstract verified, agent monitoring; main/adjacent review handles fuller scope.
3. *A Survey on Self-Improving Test-Time Intelligence: Feedback-Driven Adapting, Learning, and Scaling at Inference* (2609.01679): primary abstract/metadata screen.
4. *Adapting Without Gradients: Affine Statistics Transport and What Its Certificate Can Tell You* (2609.00374): close selective full-text reading below.
5. *Fairness-Aware Test-Time Prompt Tuning* (2608.25707): pre-existing canonical key retained; abstract/metadata here.
6. *On the Limits of Representation-Based Test-Time Adaptation for Multimodal LLMs* (2610.19892): abstract/metadata here.
7. *Online Dynamic Fault Diagnosis for Rotating Machinery Under Source-Free Streaming Test-Time Adaptation* (IEEE11737673): Scholar title/snippet only, primary not inspected here.
8. *The Anatomy and Boundary of Adaptation under Temporal Tabular Shift* (2609.12136): primary abstract and full source retrieved; not sufficiently read to establish detailed omissions.
9. *Continual Test-Time Adaptation via Entropy Sensitivity-Guidance in Strict Online Setting* (2608.29920): existing key/source retained; not fully reread in this arm.
10. *Risk-Guided Maintenance of Sports AI Under Seasonal Shift: Empirical-Bayes Recalibration with Anytime-Valid Certification* (Preprints202609.0541): primary indexed§§2.1/2.4 clearly require revealed outcomes/labeled calibration; directHTML/PDF403.
11. *Correcting Split Selection in Online Decision Trees via Anytime-Valid Inference* (2605.31239): abstract/metadata, split selection rather than risk proxy under TTA.
12. *Safety-Relevant Biomedical Machine Learning Should Adopt Stability-First Reporting* (medRxiv10.64898/2026.09.30.26364447): Scholar title/snippet only.
13. *REFIT: Recognize, Fix, and Test Wearable Sensor Placement Shifts without Labels* (2610.08991): close selective full-text reading below.
14. *Ten Deployment Anti-Patterns and an Implementation Framework for Centralized Monitoring under ICH E6(R3)* (ResearchSquare rs-10999114): Scholar title/snippet only.
15. *Diagnosing and repairing the conformal coverage guarantee of test-time-adapted image classifiers* (SSRN7602585): close title/snippet lead, referred to adjacent agent; not silently excluded.
16. *Should This Case Be Adapted? Prediction Fragmentation Controls Test-Time Adaptation* (2609.20700): close selective full-text reading below.
17. *Online Safety Monitoring for LLMs* (2607.02510): close selective full-text reading below.
18. *Certifying Whether to Adapt: Baseline-Relative PAC-Bayes-MMD Guarantees for Test-Time Adaptation* (2605.21783): close selective full-text reading below.
19. *Testing For Distribution Shifts with Conditional Conformal Test Martingales* (2602.13848): close selective full-text reading below.
20. *Prediction-Powered Risk Monitoring of Deployed Models for Detecting Harmful Distribution Shifts* (2602.02229): existing key; referred to adjacent review for semi-supervised requirement.

One further keyword lead, Koziak/Guo's *Reliability-Guided Adaptive Ensembling for Robust Test-Time Adaptation* (2606.22351), was primary-abstract screened. It is not in the recovered canonical forward union; search summaries merely describe Schirmer as related work. We do not count it as a verified citer.

## Close-source extraction matrix

Every row is a **selective reading**, except Hong's short paper whose full main text/appendices were inspected. Full sources and reading scopes are saved. No proof was independently verified.

| Source; exact locations | Signal, adaptation and data | Shift/labels/metrics | Sequential control, frozen comparison, cause | Claim overlap/boundary |
| --- | --- | --- | --- | --- |
| `Khazem2026CASTER`,§§3.1–3.3,4.3,4.6–4.7,Tables1–3 | Source class moments, residual-to-margin geometry, affine transport outside frozen network; Tent/EATA transfer test. CIFAR-C/ImageNet-C, natural datasets. | Corruptions; B64/C1000 class-coverage stress; no class-prior Dirichlet+corruption protocol established. Offline labeled source moments; no target labels for gate. Accuracy, harmful acceptance, retained gain. | Static per-batch gate, no sequential false-alarm theorem. Frozen baseline and matched57CIFAR10-C cells. Tests gate-transfer failure rather than isolating entropy cause. | C5 is strongly anticipated at design level. Gate admits4.3%Tent updates, retains0.6%Tent gain, so independence alone is not a fix. |
| `Tang2026REFIT`,§§3.4,4.1,4.5–4.7,5;Table6/Fig5 | Axis-transform correction+BN re-estimation, fixed classifier; ATC/DoC/negative entropy verify corrected wearable models. Real left/right pairs and REALDISP; simulated reattachment. | No Dirichlet priors/corruption combination. Offline labeled held-out training users set ATC threshold, unlabeled deployment. AUROC, accuracy-estimation MAE, abstention. | No sequential false-alarm control. Before/after correction estimates, frozen source and TTA comparison. No entropy/BN causal monitor ablation. | C5 verification/abstention already exists. ATC AUROC .686→.925 after correction, opposite monitoring-direction result. |
| `Ariq2026CertifyingAdapt`,§§2–6;AppJ/Table10–13 | Static candidate-vs-pilot baseline PAC-Bayes–MMD excess-risk certificates; finite-state constructions, Covertype; diagnostic Tent/CIFAR10-C/ImageNet-C. | Conditional-shift assumptions or label audit required. Some finite-state pure label-shift cases; no exact combined persistent-skew alarm. Excess risk, acceptance/rejection, certificate width. | StaticIID certificates, explicitly not arbitrary continual-stream guarantee. Covertype rejects all; deep vision diagnostic explicitly structurally vacuous and noncertified. | C5 theoretical safety alternative exists under conditions; no deployed label-free neural fix demonstrated. |
| `Shaer2026ConditionalCTM`,§§1,3.1,3.3,4,5;AppA,B,H;Fig1–4 | Fixed-reference conditional conformal test martingale; ONS bets. Synthetic Gaussian shifts and frozenViT entropy on ImageNet-C severity5. | Reference contamination by postchange data; no classifier updates or class priors. Offline reference unlabeled; no deployment labels. TypeI error, power, delay. | Anytime control conditional on finite reference; power under detectable alternatives. Requires fixed score; no adapted/frozen-model comparison. | C4 self-normalizing contamination anticipated; C5 independent/fixed reference sequential detection established but detects distribution shift, not classifier risk. |
| `Liu2026ConditionalCTM`,§§2–5,AppF;Figs1–3 | Restarts universal-portfolio conditional martingales; same frozenViT entropy/ImageNet-C synthetic benchmark with long null phase. | Fixed scoring function, severity5; no label-shift/TTA combination. No runtime labels. False alarms, power/delay. | Anytime false-alarm/delay theory, fixed-score setting. Explicit limitation§5: power depends on score revealing shift. | Newer2026 power/delay repair exists for observable score shifts; does not recover a signal erased by TTA. |
| `Schirmer2026LLMMonitoring`,§§3,4.1–4.3,5;Fig3 | ExternalPRM/safeguard scores vs internal token log probabilities; thresholded online alarm; MATH, FineHarm, RedTeaming. | No TTA. Labeled held-out calibration drawn exchangeably with deployment; runtime labels unnecessary. False alarm, power, delay. | Risk-controlled sequence alarm; Fig3 externalPRM much stronger power than self-confidence. No adaptation cause. | C5 independent-verifier idea and its cost already studied; task/assumption differences remain. |
| `Wang2026PredictionFragmentation`,§§3–6;Table2;selectedS1.3,S4,S9,S10 | Disagreement components/area between source and adapted segmentation masks; EATA/Tent; M&Ms/prostate MRI, ACDC driving. Rollback/stop/router. | No class-prior Dirichlet/corruption combination. No runtime labels; labeled calibration required. Harmful accepted area(HA), Dice/mIoU, correlations. | No sequential risk guarantee. Source/live comparison; level and step-differenced associations; modified baselines/design leakage explicitly disclosed. | C3 confidence not enough for adaptation harm partially covered; C5 independent geometry control anticipated. LargerTent step inverts component-count association; no universal remedy. |
| `Atarmla2026SelfCalibration`,§§2–7,AppA;Thm1,2,4,Prop4;Fig2 visual | Adaptive scalar quantile threshold on synthetic noisy score stream, no classifier specified. | Persistent steps and ramps; nuisance drift vsfault; no class shift/corruption combination. No runtime ground truth. Excess alarm mass, rate, power, certificate fluctuation. | Long-run calibration differs from the Schirmer guarantee. Thm4 standard indistinguishability under uniform tolerated-drift class; no fixed-threshold arm. | C4 substantially anticipated broadly. Does not establish C1 or C2; cannot be cited as proof every confidence monitor necessarily fails. |
| `Hong2026BoilingFrog`,§§3–5,AppA–E;Fig5 visual | PPO locomotion and pretrainedMLP world-model prediction error; z/variance/percentile detectors, fourMuJoCo environments. | Synthetic additive velocity drift, linear/sinusoidal; no classification priors. No labels at detector runtime. Detection rate/FPR/survival gap. | No distribution-free guarantees. No online world-model or policy weight updates specified, no TTA/frozen arms. | Adjacent score blindness and failure-before-detection, not proof adaptation causes signal loss. Authors' universal-language interpretations exceed the finite tested scope. |

## Citation expansion rounds and stopping

1. Schirmer:80backward records and20unique forward titles recovered. Full-text focus selected9neighbors.
2. Forward citation endpoints for REFIT0, PAC-Bayes0, OnlineSafety0, CASTER2, conditionalCTM6 and parameter-freeCTM1 yielded additional papers. CASTER led to REFIT/already-seen WiMoT. ConditionalCTM led to Atarmla, reference-null thresholds, predictive-rank martingales, federatedRAG refresh, changepoint localization and parameter-freeCTM. New complete sources/abstracts saved.
3. Atarmla backward citation led to Hong and weighted-conformal anomaly-detection power limits. Hong forward citation returns Atarmla only; Atarmla0 and reference-null thresholds0. Other branches still yielded new nodes (federatedRAG, optimal priors) and were screened at title/abstract level.

**The required global saturation condition was not reached.** Some selected branches close, but two successive whole-graph rounds with no new close source cannot honestly be claimed. The graph is explicitly incomplete rather than silently capped and declared exhaustive. Tent has a large citation graph handled by the parallelTTA subreview; this arm does not claim full traversal of it.

## Repositories, discussions and theses

Monitor repository `monasch/tta-monitor`: GitHubAPI showed0issues(allstates),0forks,2commits. Discussions URL404; not treated as read. README source saved; supportedlossproxies include `min_proto_dist`, entropy,energy and maxclassprobability. Repository code was not executed or patched.

Exact-title GitHub global issues query returned3items: an abstract/AI-generated paper note, a daily-arXiv announcement, and a machine-monitoring researchbacklog. The backlog at `https://github.com/kuo1234/xlstm_anomaly/issues/12` claims persistence-onlypromotion can absorb faults and lists M2N2/MemStream/CANDI/COMET/AnDri as prior art. This is an unreplicated nonpaper discoverylead, not evidence of publishedC1; parent notified. A broad`tta-monitor` GitHubissue query returned100total but first30mostly unrelated TechnicalTrainingAssistanceissues; not exhaustively paginated because exact-titlequeryisolated relevantresults. Thesiskeywordsearch found no close identifiableprimarythesis; coverage is search-limited, not a thesisrepositoryaudit.

## Recommended implication

Do not sell C4 or “independent signal” as a new principle. For C1, the defensible question is whether this **particular supported monitor loses material detection power under a controlled noncollapsed regime, relative to the same frozen checkpoint**, beyond the failures Schirmer already reports in§5.4. The pendingfixed-threshold/Tent-vsBN results must staypendinguntil theauthoritativeexperimentrecordchanges. A fix would need sensitivity **at matchedfalsealarms**, usefulgainretention, and limits relative toCASTER/ATC/geometry/external-verifier alternatives. Merely improvingconfidencecalibrationdoesnotestablishsuchafix.

Initial artifacts: `search-log.csv` had 120 rows, `screened-papers.csv` 113 rows and `metadata.json` 9 verified close-source records. Follow-up retrievals and reading are recorded in [direct-citers-followup.md](direct-citers-followup.md); the current file counts are in `stats.json`. Sources and the hash manifest are under `../../evidence/citations/`. Counts describe this arm and require deduplication across agents.

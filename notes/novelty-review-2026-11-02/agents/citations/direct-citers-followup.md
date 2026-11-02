# Three direct citers: follow-up reading, 2 November 2026

No experiments or tests were run. This follows the parent review's request to resolve three citation-screening uncertainties; no new citation-graph expansion was undertaken.

## Wang et al., The Anatomy and Boundary of Adaptation under Temporal Tabular Shift

Primary source: [arXiv2609.12136](https://arxiv.org/abs/2609.12136). Authors, verified on the primary record: Tianyu Wang, Xi Vincent Wang, Lihui Wang, Mian Li, Zhihao Liu. Preprint; no accepted venue verified. Suggested new key: `Wang2026TemporalBoundary`.

**Reading scope:** abstract and metadata, §§2–3 on labels/protocol, §§4.1–4.2 on the classification harm case, §§5.4–5.6 on monitor/proxy behavior, §7 limitations, AppendixJ.1 protocol. Mapped the entire methods/results/appendix structure and searched all Schirmer, monitor, alarm, confidence, entropy and Tent occurrences. Figure1(c) visually inspected in the PDF on **page14**, saved as `evidence/citations/anatomy-page14.png`. Remaining mathematical identification proofs were not audited.

**Decisive result:** §5.5 is titled *Currency-Mismatched Gates Miss Deployment Harm*. On the `homecredit-default` stream, the authors monitor a streaming correction's **log-loss regret against a frozen predictor** with a betting e-process. The corrector consumes labels after prediction. The alarm locks the corrector out at15.1%of the stream, after84%of the AUC harm has already accrued. The first1%loses11.4AUC points while log loss barely changes; during2–5%the correction improves log loss while ranking harm continues. Figure1(c) plots AUC harm against lock time and also shows that midstream shutoff can worsen AUC by introducing a score-scale discontinuity. These are the paper's reported measurements, not independently recomputed results.

**What it actually monitors:** AppendixJ.1 specifies a past-label kNN residual corrector, k20, correction scale0.7, block64, minimum past buffer100; e-process burn-in at least20 and level0.05; corrected probabilities clipped to[1e-6,1−1e-6]. Its validity statement is supported empirically by permutation-null checks, not a full independent guarantee audit here. The e-process itself is **not included in their reproduction deposit**, as stated in AppendixJ.1.

**Is Schirmer's monitor a baseline? No evidence of that in the inspected methods/results/appendix.** Schirmer is cited in §2 as an example of loss-denominated TTA risk monitoring. The authors' actual gate is their own revealed-label log-loss-regret e-process. They do not port Schirmer's label-free risk lower bound, test Tent, isolate entropy versus BN, or combine class-prior Dirichlet skew with image corruption. Their label-free identification theory must not be confused with their empirical corrector, which consumes outcomes; §2 makes that distinction explicitly.

**Claim implications:** strong partial coverage of the general warning that a statistically controlled monitor can miss adaptation harm when its observable target is misaligned with the deployment objective. It does not report C1's adapted-versus-frozen missed-risk rate under the same target risk. Its cause is **metric mismatch** (log loss versus AUC), not confidence being optimized while zero-one error rises. It neither establishes nor repairs C2/C3. It reinforces C5's requirement to monitor the actual task risk rather than a convenient score.

## Sadhuka et al., E-valuator

Primary source: [arXiv2512.03109](https://arxiv.org/abs/2512.03109). Suggested new key: `Sadhuka2025EValuator`; primary authors: Shuvom Sadhuka, Drew Prinster, Clara Fannjiang, Gabriele Scalia, Bonnie Berger, Aviv Regev, Hanchen Wang. First submitted2December2025. No accepted venue independently verified in this arm.

**Reading scope:** §§2.1–2.4 (hypotheses, calibration split, PAC thresholds, density-ratio process), §3 related work, §§4.1–4.3 experiments/baselines, §5 discussion, Appendices8.1.2/8.1.6 on small calibration/insufficiency of marginal calibration and selected8.2 experimental details. Paper source and PDF saved. Proofs were not independently checked.

**Signal/method:** black-box verifier probabilities for partial LLM-agent trajectories. The method learns a density ratio from labeled successful/unsuccessful calibration trajectories and calibrates the maximum trajectory statistic on a disjoint split. It yields high-probability false-alarm control under the stated trajectory sampling/calibration assumptions. Within a trajectory the verifier scores may be dependent; that does not make the calibration distribution invariant to an adapting classifier. Calibration and deployment null trajectories must have the required common law.

**Experiments:** six mathematical/QA benchmarks, three agent-verifier combinations. Comparators are a raw verifier, isotonic-calibrated verifier, PAC-thresholded verifier and randomized-Ville procedure. Outcomes include false alarms, power, run length and tokens versus retained accuracy. Figures2–3 and §§4.1–4.3 compare these methods. Appendix8.1.6 gives an explicit example where marginal score calibration fails to control false alarms. §2.2 notes that controlling false alarms alone can be achieved by never rejecting; §2.1 notes that indistinguishable verifier-score laws cannot yield power.

**Is Schirmer's monitor a baseline? No.** The Schirmer citation occurs in related work (§3); none of the baseline definitions or experimental descriptions runs the TTA monitor. No visual Tent, BN, class-prior Dirichlet or corruption protocol appears in these experiments, and there is no adapted-versus-frozen classifier risk comparison.

**Claim implications:** existing C5 methodology for converting independent verifier evidence into controlled sequential decisions, with power evaluation. It does not demonstrate a fix for the project's adaptive-confidence failure. Calibration improvement, true-score information and sequential alarm control are distinct. This also supports the reviewer's first objection in principle, without invalidating an empirical detection-power study.

## Jia et al., Online Dynamic Fault Diagnosis

Verified metadata from the publisher's Crossref deposit: Wanying Jia, Yuqing Chang, Fuli Wang, Cunhe Huang; *Online Dynamic Fault Diagnosis for Rotating Machinery Under Source-Free Streaming Test-Time Adaptation*, IEEE Sensors Journal2026; DOI[10.1109/JSEN.2026.3741562](https://doi.org/10.1109/JSEN.2026.3741562). Article11737673. Suggested key if retained: `Jia2026ODFD`.

**Access remains blocked.** IEEE document, stamp, DOI redirect and publisher PDF endpoints each returned HTTP202 with zero-byte bodies; the web tool reported the primary document inaccessible. OpenAlexW7221761298 reports closed access and no repository full text; exact-title Scholar returns one record and no alternate-version link. Semantic Scholar title search429. Crossref provides metadata and a publisher PDF link, which also returns202empty. Exact-title/author searches found only the Scholar abstract and a secondary EurekaMag reproduction of it. No methods/results/appendix were read, and the paper is therefore an **unresolved direct citer**, not a negative finding.

The abstract describes source prototype alignment, dual uncertainty thresholds calibrated on the first target batches and then held fixed, confidence-weighted pseudo-labeling, a Gaussian-mixture feature-distance constraint, and private/CWRU machine data across closed/partial/open domains. These are **abstract-level indications only**. It is not permissible to infer from them that the full paper lacks Schirmer-baseline comparisons, missed-risk plots or the requested failure. In particular, its fixed thresholds and confidence dependence make full-text access worth prioritizing before asserting complete direct-citer clearance.

The Crossref response contains no reference list. Its forward-citer relationship to Schirmer comes from the saved Google Scholar cited-by page; the actual in-paper use is unknown. No author contact or purchase was attempted.

## Consequence for the parent review

Anatomy and E-valuator can now be assessed beyond their abstracts and do not directly report C1/C2 in their inspected methods/results/appendices. Anatomy adds a relevant known **risk-target/proxy mismatch** failure. ODFD remains a concrete access hole, alongside SSRN7602585. “No report found” is consequently a bounded search result; the direct-citer/full-text audit is incomplete.

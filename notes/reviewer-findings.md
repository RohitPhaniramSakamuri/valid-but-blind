# Reviewer findings: novelty risks and falsifiable scope

Date: 23 October 2026. Role: independent constructive reviewer. No experiment, benchmark, package installation or code execution was performed. Search results were used to locate primary papers and author repositories. Reading is partial, with locations below; these notes do not certify an exhaustive novelty search.

## Assessment

The supplied abstract's broad contribution is already occupied. Shift-dependent parameter/statistics changes, expert routing, selection among distinct TTA algorithms, and deciding whether to adapt all have direct predecessors. Its final sentence reports experiments and gains that have not been supplied. Treat that sentence as a proposed evaluation, not as completed evidence.

The most defensible next question is conditional: **can we learn when an additional unlabeled observation is worth its computational cost specifically because it changes the best adaptation decision?** General value-of-information acquisition is old, and recent vision inference work already escalates computation using uncertainty. The distinction must be adaptation-action utility, rigorous cost accounting, and held-out deployment transfer. A different collection of familiar modules would not by itself establish novelty.

## Primary-source overlap ledger

### 1. MORPHEUS — closest broad collision

- Michal Danilowski, Alexander Murphy, Young D. Kwon, Abhirup Ghosh. *MORPHEUS: Meta Test-Time Adaptation via Neural Collapse Geometry.* ICLR 2026 **Test-Time Updates Workshop**, not verified as an ICLR main-conference paper.
- [Author PDF](https://theyoungkwon.github.io/papers/articles/danilowski_morpheus_iclr-ttu26.pdf); [author publication list](https://theyoungkwon.github.io/research.html); [OpenReview record](https://openreview.net/forum?id=YfyApJH1Rj).
- Inspected: author-PDF first page/abstract and introduction; author publication listing confirms workshop.
- It uses source-model entropy and embedding geometry to predict which TTA algorithm will be most accurate before executing candidate adaptations. This directly anticipates 'infer shift characteristics, then pick an adaptation policy efficiently.' Any proposal must compare against it, not cite it as generic background.

### 2. Identifiability — limits and stream evidence already studied

- Kartik Jhawar, Lipo Wang. *When is Test-Time Adaptation Identifiable From Unlabeled Evidence?* arXiv:2609.11235v1, 10 September 2026; preprint.
- [Record](https://arxiv.org/abs/2609.11235); [full text](https://arxiv.org/html/2609.11235v1).
- Inspected: §§2–4, §7, Appendix B.3–B.5.
- It distinguishes a weak selector from evidence that cannot identify the correct action; compares KEEP, normalization, Tent, DeYO and ROID. Controlled CIFAR-100-C and DomainNet-126 studies alter deployment organization while preserving image bags; order-sensitive evidence can help. The authors retain a stochastic counter-result where this advantage disappears. Limitations include a restricted action menu and main source-model family. Neither order-aware selection nor an unlabeled-ambiguity theorem is available as a new broad claim.

### 3. MoETTA — mixed-shift expert routing

- Xiao Fan, Jingyan Jiang, Zhaoru Chen, Fanding Huang, Xiao Chen, Qinting Jiang, Bowen Zhang, Xing Tang, Zhi Wang. *MoETTA: Test-Time Adaptation Under Mixed Distribution Shifts with MoE-LayerNorm.* AAAI 2026, 40(25):21011–21019, DOI 10.1609/aaai.v40i25.39243. Preprint: arXiv:2511.13760v1.
- [Paper](https://arxiv.org/html/2511.13760v1); [official code](https://github.com/AnikiFan/MoETTA).
- Inspected: abstract, method's key design/routing subsections, computation comparison and dataset descriptions.
- It uses sample- and layer-dependent routing to structurally separated LayerNorm experts, with a frozen shared source component. Its potpourri and potpourri+ evaluations mix synthetic, natural, artistic, adversarial and source-domain images. This blocks broad claims that heterogeneous adaptation directions, expert selection, or source-return evaluation are unexplored.

### 4. AdaTent++ — action routing with a particularly relevant limitation

- Xiaomei Gai, Meichun Wang, Yantong Guo, Shiyu Wang, Ye Li, Rui Fu. *AdaTent++: reliability-guided hybrid test-time adaptation for traffic sign detection under distribution shift.* Frontiers in Signal Processing 6, 9 September 2026; DOI 10.3389/frsip.2026.1842851.
- [Publisher full text](https://www.frontiersin.org/journals/signal-processing/articles/10.3389/frsip.2026.1842851/full).
- Inspected: §§2.2–2.3, §4 discussion, §5 limitations and §6 conclusion.
- It chooses BN-statistics adaptation, guarded BN-affine optimization, or skipping using entropy and cross-view agreement, with restoration safeguards. Crucially, §5 discloses benchmark condition identifiers used in view selection/candidate filtering, a fixed class-balanced subset, one deterministic run and no long-stream study. The discussion also disclaims strict compute matching. These are concrete limitations for a globally fixed, domain-agnostic protocol to address, but addressing them alone may be incremental.

### 5. FORGE — paid probing and confidence-gain limitations

- Muhammad Rehan, Haider Ali, Muhammad Ali Munir, Moaz Amjad. *FORGE: Forward-Only Test-Time Adaptation for Integer-Only Vision Models on Microcontrollers.* arXiv:2609.01683v1, 1 September 2026. The arXiv record identifies TMLR 2026 publication; that venue status was not independently checked here.
- [Record](https://arxiv.org/abs/2609.01683); [full text](https://arxiv.org/html/2609.01683v1).
- Inspected: §4.6, Algorithm 2 and §5.
- It runs source and adapted paths during a short calibration window, then commits to one path based on confidence improvement. The extra forward passes are explicit. The gate loses useful adaptation on many-class overconfident models, rejecting every Tiny-ImageNet-C stream in its reported run. Its limitation suggests better benefit evidence, not a claim that gating or short paid probes are new.

### 6. SEGA — probing-derived sensitivity already drives adaptation

- Chandler Timm C. Doloriel, Yunbei Zhang, Muhammad Salman Siddiqui, Tor Kristian Stevik, Fadi Al Machot, Kristian Hovde Liland, Habib Ullah. *Continual Test-Time Adaptation via Entropy Sensitivity-Guidance in Strict Online Setting.* arXiv:2608.29920v1, 30 August 2026; preprint.
- [Record](https://arxiv.org/abs/2608.29920); [PDF](https://arxiv.org/pdf/2608.29920).
- Inspected: introduction, §§3.2–3.3 and experiment/computation discussion.
- It probes progressive structured erasures, derives entropy sensitivity, and controls sample gating and recovery. It studies strict batch-size-one corruption-style streams. It is a strong counterexample to novelty claims about adding perturbation-based probes to an adaptation controller. Its main control signal concerns sensitivity/collapse, rather than learned marginal decision value for choosing among an arbitrary method menu.

### 7. SA-TTS — a direct adaptive-computation comparator

- Youla Yang. *SA-TTS: Stress-Aware Test-Time Scaling for Vision Models.* CVPR Workshops 2026, pp.11480–11487.
- [Official CVF record](https://openaccess.thecvf.com/content/CVPR2026W/Viscale/html/Yang_SA-TTS_Stress-Aware_Test-Time_Scaling_for_Vision_Models_CVPRW_2026_paper.html).
- Inspected: official abstract and indexed first-page Algorithm 1/method text. Direct PDF fetching was blocked in this session, so detailed experiments were not inspected.
- It uses cheap entropy/margin, escalates to augmented-view disagreement, then possibly multi-crop evaluation. This makes 'buy more evidence on uncertain inputs' insufficient as a novelty claim. Its actions are inference policies rather than parameter-update TTA algorithms. A decision-value-based adaptation selector must outperform its uncertainty-driven acquisition principle under matched cost.

### 8. Value-of-information foundation

- David J. Weiss, Ben Taskar. *Learning Adaptive Value of Information for Structured Prediction.* NeurIPS 2013.
- [Official record](https://proceedings.neurips.cc/paper_files/paper/2013/hash/ebd9629fc3ae5e9f6611e2ee05a31cef-Abstract.html); [paper](https://proceedings.neurips.cc/paper_files/paper/2013/file/ebd9629fc3ae5e9f6611e2ee05a31cef-Paper.pdf).
- Inspected: abstract and §3/Algorithm 1.
- It learns input-dependent feature acquisition with value approximation under a budget. The general idea of learning whether a feature's expected decision improvement justifies its cost is established. A TTA paper should position its contribution as a domain-specific decision problem and evidence, not invent a new general VOI principle.

### 9. Recent label-free acquisition neighbor

- Eeshaan Jain, Linus Bleistein, Bart Deplancke, Charlotte Bunne. *Measure Less, Know More: Self-Supervised Test-Time Feature Acquisition.* arXiv:2610.03454v1, 2 October 2026; preprint.
- [Record](https://arxiv.org/abs/2610.03454); [full text](https://arxiv.org/html/2610.03454v1).
- Inspected: abstract, structure of §§2–5 and Appendix A limitations.
- ECHO-k learns sequential acquisition using a full-view pretrained representation as a self-supervised target, without downstream labels. It is relevant because representation recovery and policy-selection benefit are different objectives. Adapting this acquisition idea to TTA requires showing that action-regret supervision is materially more useful than representation recovery or confidence alone.

### 10. Tempora — efficiency must reflect delivered utility

- Sudarshan Sreeram, Young D. Kwon, Cecilia Mascolo. *Tempora: Characterising the Time-Contingent Utility of Online Test-Time Adaptation.* ICML 2026, PMLR 306:115420–115456.
- [Official paper record](https://proceedings.mlr.press/v306/sreeram26a.html); [official code](https://github.com/sudotensor/tempora).
- Inspected: official abstract and metadata.
- It studies hard-deadline, latency-decaying and amortized utility. Method rankings vary with timing pressure. Therefore 'computationally efficient' needs measured latency/throughput and all acquisition/update overhead, rather than counting only selected update steps.

### 11. BoTTA — compound and resource-constrained tests already exist

- Michal Danilowski, Soumyajit Chatterjee, Abhirup Ghosh. *BoTTA: Benchmarking On-device Test Time Adaptation.* SenSys 2026, pp.465–477, published 10 May 2026; DOI 10.1145/3774906.3800498. Preprint arXiv:2504.10149.
- [Publisher full text](https://doi.org/10.1145/3774906.3800498); [preprint](https://arxiv.org/abs/2504.10149).
- Inspected: publisher abstract, §§2 and 4, system metrics and conclusion.
- It studies few target samples, incomplete category coverage, diverse and overlapping shifts, periodic adaptation, and real-device cost. The paper's linked code URL returned 404 here; do not represent it as accessible without another check. 'We finally evaluate compound shifts/cost' alone does not establish a gap.

### 12. Adjacent diagnostic warning

- Zhengshu Zhang. *When Does Test-Time Physical Diagnosis Pay? A Frozen Policy Buys Evidence It Never Reads.* arXiv:2609.22299v1, 14 September 2026; preprint in robotics.
- [Record](https://arxiv.org/abs/2609.22299); [full text](https://arxiv.org/html/2609.22299v1).
- Inspected: abstract and introduction.
- It separates identifying a condition, using evidence, decision value, improvement beyond a fixed action, and safe realization. The work is outside visual classification but reinforces that better diagnosis or recoverable information does not automatically imply useful adaptive selection.

## Benchmark cautions

- [CIFAR/ImageNet corruption benchmark author repository](https://github.com/hendrycks/robustness) describes synthetic corruption evaluation; fixed released images are preferred for reproducibility. CIFAR-10-C is an inexpensive starting point, but it does not by itself support broad real-world deployment claims.
- [DomainNet's author project](https://ai.bu.edu/M3SDA/) lists six domains: clipart, infograph, painting, quickdraw, real and sketch, across 345 categories. DomainNet-126 is a particular subset used by TTA papers, not interchangeable with the full dataset. Checkpoint labels and source/target protocols must match.
- [WILDS official project](https://wilds.stanford.edu/) and [ICML paper](https://proceedings.mlr.press/v139/koh21a.html) describe a collection spanning tasks, modalities and natural domain/subpopulation shifts. Specify one dataset, source model, metric, target access and metadata policy; 'we evaluate on WILDS' is underspecified. Its unlabeled-data extension is not automatically an online TTA protocol.
- Corruption metadata can define evaluator splits, but cannot secretly select augmentations, methods or thresholds during deployment.
- Holding out severity while showing the same corruption type to the selector is weaker than holding out a whole family. Reusing the same original image under different corruptions across meta-training and test creates another leakage route.

## Narrow candidate and implementation plan

**Candidate:** budgeted acquisition of adaptation-relevant evidence when a cheap selector is decision-ambiguous. Status: literature-supported hypothesis, not a verified open problem.

Start with a finite action menu such as SOURCE/no update, BN-statistics adaptation and Tent, plus one robust alternative after the first diagnostic. For each episode, save an adaptation prefix and a disjoint subsequent evaluation segment. Offline development can use labeled source-derived episodes; deployment never sees target labels. Explicitly disclose this distinction instead of implying no labels were used anywhere.

1. Fit a cheap action-value predictor using source outputs and inexpensive batch/stream statistics.
2. Define one additional evidence action, such as two label-preserving views; later compare context statistics or frozen-feature diagnostics. Charge its measured forward cost.
3. Cross-fit the cheap and richer selectors over episode groups. Their out-of-fold difference in **realized adaptation utility**, after acquisition cost, supplies a target for an acquisition gate. Do not use the gain of the in-sample oracle as if it were a realizable deployment reward.
4. At deployment, buy the probe only when expected reduction in action regret exceeds its cost. Select among the same adaptation actions afterward. A no-update fallback remains an explicit action.
5. Keep a richer-evidence always-on selector, cheap selector, entropy acquisition and random same-rate acquisition as ablations. Acquisition can help only if the extra evidence changes a useful decision; plotting uncertainty alone is insufficient.

This is an application of established acquisition ideas. A credible contribution needs a TTA-specific insight about when information changes update utility, plus reproducible evidence under held-out mechanisms. A two-stage threshold cascade with more modules is unlikely to be enough.

## Falsification and stop conditions

- **No selection headroom:** if the cost-aware oracle barely beats the best fixed action, stop developing a selector for that regime. Report that result.
- **No evidence headroom:** if an always-on richer selector cannot beat the cheap selector out of family, selective acquisition cannot rescue it.
- **No acquisition advantage:** if random or entropy-triggered probing matches the learned gate at equal total cost, its claimed decision-value mechanism is unsupported.
- **Only familiar-family gains:** failure on whole-family holdouts/compositions weakens the claim of shift generalization; image-level random splits are insufficient.
- **Confidence without benefit:** evaluate correct-to-wrong flips and avoidable adaptation harm separately. No-update everywhere can look safe while delivering no useful adaptation.
- **State mismatch:** do not evaluate an action from a clean reset during development and deploy it on a drifted state without a separate stateful protocol. Parameter, normalization, optimizer, teacher and memory states must be reset or cloned consistently.
- **Invisible future information:** prequential predictions must be committed before future batches or labels are accessed. Label-assisted oracle comparisons are analysis-only upper bounds.
- **Compute loss:** count evidence, duplicate forwards, candidate probes, synchronization, state copying, updates and routing. Include a fixed method using the same extra budget.

## Small staged study

Stage 0: fix the source checkpoint and action semantics; use a small CIFAR-C diagnostic to measure actual runtime and oracle headroom. No hard GPU-hour claim can be made before profiling.

Stage 1: create meta-training/development episodes from disjoint source-image identities, with family-level holdouts, joint class-prior shifts and clean-return controls. Use only 2–3 candidate actions and one extra observation to isolate the mechanism. If needed, a small-model CPU implementation is a mechanism demonstration, not original benchmark replication.

Stage 2: evaluate at least a second source architecture and one natural-domain dataset, then a properly specified continual-state protocol with abrupt/gradual/recurring shifts and temporal dependence. Broader menus and policy composition belong after the minimal mechanism works.

Metrics: prediction error and NLL, regret to the action oracle, regret to the best fixed action, harmful-update rate, correct-to-wrong flips, no-update frequency, gain among adaptations, total runtime, peak memory and accuracy–cost curves. Use paired episode/stream-level intervals and all declared seeds. Sequential windows do not provide independent sample sizes.

## Baselines and reusable implementation sources

- SOURCE/no update and a fixed BN-statistics method: essential controls.
- Tent, EATA/ETA, SAR, RoTTA and ROID are available in the [authors' maintained online TTA benchmark](https://github.com/mariodoebler/test-time-adaptation). The repository also exposes continual, reset-each-shift, mixed-domain and correlated settings. Method-specific official code may be preferable for fidelity; this note verifies the common repository's availability, not every method implementation.
- MORPHEUS-style pre-action selection: closest selection comparator; this session did not verify a public official repository.
- MoETTA: [official repository](https://github.com/AnikiFan/MoETTA), especially when using LayerNorm backbones and mixed shifts.
- Cheap versus always-rich, random-probe versus entropy-probe, fixed-probe versus learned-probe acquisition: required causal ablations.
- [Tempora](https://github.com/sudotensor/tempora): utility evaluation rather than an adaptation algorithm baseline.

## Open audit items

The parent researcher is separately auditing SLRF and related selector literature. The exact 'FAR video selective' citation requested by the parent was not located from that name; search results mostly returned unrelated robotic Failure-Aware Retry. Confirm its title or identifier before completing the close-neighbor comparison. Recent selective-adaptation work (Jiang et al., arXiv:2609.08367, CAS) and medical prediction-fragmentation gating (arXiv:2609.20700) also deserve targeted full-method checks. No claim of zero prior work is warranted.

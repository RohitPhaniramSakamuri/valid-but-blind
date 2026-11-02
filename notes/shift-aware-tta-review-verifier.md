# Independent verification: selection, reliability and evaluation

Date: 23 October 2026. Role: verifier under the deep-research/literature-review workflow. Scope: primary-source literature, particularly claims that could invalidate a proposed gap. No experiments, implementation tests, repository execution or dependency installation were performed.

## Assessment

The broad proposal to infer shift properties and dynamically choose a TTA method is already covered by close prior work. In particular, MORPHEUS selects a method before adaptation using source-model entropy and feature geometry. The September 2026 identifiability preprint goes further: it includes a frozen SOURCE action, shows how batch/order structure changes the best action, and evaluates selectors using evidence with different information content. Thus **adding no-adaptation, temporal summaries, action-benefit regression, or held-out corruptions is insufficient by itself to establish a new contribution**.

The claim that earlier TTA always applies one strategy independently of the shift is too broad. Sample selection, online learning-rate modulation, adaptive normalization, reset rules, method selection and multi-hypothesis adaptation already exist. Their degrees of freedom differ, but a proposal must explain its decision variable rather than dismiss the whole field as static.

## Closest collisions

### Jhawar2026Identifiability — strongest contemporary collision

[When is Test-Time Adaptation Identifiable From Unlabeled Evidence?](https://arxiv.org/abs/2609.11235), Kartik Jhawar and Lipo Wang, arXiv v1, 10 September 2026. Read: §§2–7 and Appendix B. Candidates are SOURCE/KEEP, DeYO, Tent, ROID and normalization, each starting from the same source state for a deployment world. The paper tests prior/stream regimes, leave-one-corruption-out and DomainNet transfer holdouts, and shows action reversals under reordering of the same images. Order-aware evidence can recover information absent from global summaries. Its §7 limits include a finite action menu and one main source-model family. It does not claim a universally best selector.

**Implication:** the initial candidate “predict per-action benefit under prior/corruption shifts, include no-update and unseen-family evaluation” overlaps heavily. A current-state online controller or costed evidence-acquisition mechanism would be a different unit of study, but novelty is still unverified.

### Cygert2026RealisticSelection — actual model-selection baseline

[Realistic Evaluation of Test-Time Adaptation: Unsupervised Model Selection](https://www.scitepress.org/Papers/2026/143201/143201.pdf), Sebastian Cygert, Damian Sójka, Tomasz Trzciński and Bartłomiej Twardowski, VISAPP 2026, pp.75–86, DOI 10.5220/0014320100004084. Linked [2024 preprint](https://arxiv.org/html/2407.14231v1) has the longer hyperparameter-selection title. Read: preprint selection definitions, experimental setup, discussion and conclusions; published first-page metadata. Source validation, cross-dataset supervision and label-free proxy selection have different information budgets. Entropy/consistency/feature-neighborhood criteria are not uniformly reliable; small target supervision helps. Selection after executing candidates consumes more information and compute than a pre-action selector. The public [author repository](https://github.com/cygerts/unsupervisedtta) mixes the old title in its BibTeX with the newer report title, so cite the proceedings title and link the preprint explicitly.

### Schirmer2025Monitoring — safety cannot be claimed merely from confidence

[Monitoring Risks in Test-Time Adaptation](https://arxiv.org/html/2507.08721v1), Mona Schirmer, Metod Jazbec, Christian A. Naesseth and Eric Nalisnick; NeurIPS 2025. Read: §§2–3, experiments, conclusion/limitations and selected appendices. The paper builds sequential risk monitoring for changing models with unlabeled loss proxies. Its guarantee depends on proxy informativeness (Assumption 1), not merely absence of target labels. Authors explicitly identify label-free diagnostics of assumption violations as open work. Detection delay and calibration cost remain practical issues.

**Implication:** a router's uncertainty interval calibrated on development shifts cannot be advertised as a target accuracy safety guarantee for arbitrary unseen shifts.

### Sreeram2026Tempora — cost-aware evaluation is established

[Tempora](https://proceedings.mlr.press/v306/sreeram26a.html), Sudarshan Sreeram, Young D. Kwon and Cecilia Mascolo, ICML 2026. Read: v2 §§3–5 and appendix hardware descriptions. The May 2026 version evaluates 11 methods across 750+ temporal evaluations and defines hard-deadline, latency-penalty and amortized-budget utility. Thus reporting average runtime alongside accuracy is weaker than existing evaluation. Its discussion specifically motivates integrating temporal constraints with continual/nonstationary distributional realism. Main comparisons use episodic IID conditions and default hyperparameters, with scope limits explicitly acknowledged.

### Additional collisions that constrain candidate A

- [SA-TTS: Stress-Aware Test-Time Scaling for Vision Models](https://openaccess.thecvf.com/content/CVPR2026W/Viscale/papers/Yang_SA-TTS_Stress-Aware_Test-Time_Scaling_for_Vision_Models_CVPRW_2026_paper.pdf), Youla Yang, CVPR 2026 VisScale workshop. Read abstract, methodology/Algorithm 1 and experimental overview through indexed official PDF. It already starts with entropy/margin, spends augmentation passes when needed, and uses disagreement to decide between ensembling and multicrop inference. It changes inference computation with frozen parameters. A generic uncertainty cascade or “buy augmentations when unsure” is therefore not new. A distinction worth testing would be the value of extra observations **for selecting parameter updates**, with acquisition and adaptation jointly charged.
- [When Does Test-Time Physical Diagnosis Pay? A Frozen Policy Buys Evidence It Never Reads](https://arxiv.org/html/2609.22299v1), Zhengshu Zhang, arXiv v1, 14 September 2026. Read §§1–3 and limitations. In robotics, the paper distinguishes identifying a condition, using purchased evidence, decision value, selection value over a fixed intervention and safe realization. The general value-of-information argument is established outside image-classification TTA and must be acknowledged.

### Additional collisions that constrain candidate B

- [When and Where to Reset Matters for Long-Term Test-Time Adaptation](https://arxiv.org/html/2603.03796v1), Taejun Lim, Joong-Won Hwang and Kibok Lee; ICLR 2026. Read abstract, introduction, method headings and selected §§3.3–3.5. ASR uses prediction concentration to determine when/which layers to reset, recovers useful knowledge and adjusts adaptation using domain discrepancy. Broad state-responsive reset or update-strength selection is already covered.
- [RG-TTA](https://arxiv.org/html/2603.27814v1), Indar Kumar, Akanksha Tiwari, Sai Krishna Jasti and Ankit Hemant Lade; arXiv, 29 March 2026. Read abstract, method overview and protocol headings. Similarity to stored regimes modulates learning rate, early stopping and specialist checkpoint reuse for forecasting. It is an important cross-domain neighbor; forecasting protocols may access subsequently observed outcomes, so its information setting must be checked before equating it with strictly unlabeled image classification.
- [Multi-Hypothesis Test-Time Adaptation to Mitigate Underspecification](https://arxiv.org/html/2607.00259v1), Afshar Shamsi, Xiao-Yu Guo, Hamid Alinejad-Rokny, Arash Mohammadi, Damien Teney and Ehsan Abbasnejad; arXiv, 30 June 2026. Read abstract/introduction and method outline. Maintaining multiple normalization-parameter particles with distinct optimization trajectories and aggregating them already addresses uncertainty over adaptation outcomes; candidate branching by itself is not new.

## Residual candidate A: active acquisition of unlabeled decision evidence

This is a **candidate intersection**, not a verified untouched gap: a selector decides whether the expected improvement in its parameter-update choice justifies paying for more observations under a causal deadline. Cheap evidence may suffice for some batches. Other batches could justify additional augmentation views, frozen-feature statistics or past-only temporal summaries; if the ambiguity persists, keep SOURCE or the current state according to a declared action definition.

Distinctions that must be demonstrated:

1. The controller chooses parameter-update policies, rather than only frozen-model inference budgets as in SA-TTS.
2. The added observation changes the policy choice and improves net utility relative to using it indiscriminately, following the diagnosis-use-value separation.
3. All source forward passes, augmented views, feature extraction, selector inference, adaptation steps, checkpoint copying and fallbacks are charged.
4. The evidence is available causally. A longer history is legitimate; waiting for future frames before deciding incurs delay. A full-target feature summary is a transductive setting.
5. Gains survive held-out corruption families, compositions and label/temporal shifts, without using those hidden labels for router fitting, calibration, thresholding or stopping.
6. A simple fixed richer-evidence selector and an equal-cost random allocation baseline are necessary. Otherwise a complicated learned acquisition mechanism may add nothing beyond extra compute.

**Kill criterion:** if every useful observation is cheap enough to collect on every batch, or a fixed action dominates net utility, active acquisition has no meaningful headroom. If the router confidently chooses wrong actions on unseen families, development calibration has not solved selection reliability.

## Residual candidate B: current-state-conditioned action benefit

A whole-deployment SOURCE-clone comparison does not answer which update helps a model already changed by earlier adaptation. A concrete diagnostic would hold the next unlabeled batch fixed while varying model/optimizer/normalization/memory states obtained from different histories, then measure action rankings on clones of each live state. Candidates could include retaining the current state, one conservative update, a different update, and reset to SOURCE. The reset action has its own cost and must restore the declared buffers and optimizer state.

This could separate current-stream features from information about the controller's accumulated state. However, ASR, recovery methods, dynamic normalization, teacher/memory methods and regime-conditioned control are close neighbors. A simple current-versus-source disagreement feature may explain most apparent gains. Compare against it before proposing a new controller.

**Kill criterion:** no repeatable action-rank reversal across histories on matched current batches, or no improvement over simple state proxies at matched budget. No guarantee of safety follows merely from snapshot-and-rollback mechanics.

## Requirements for the eventual experiment

- Declare episodic versus continual operation, prediction-before-update versus adaptation-before-prediction, legal target lookahead and reset boundaries.
- Distinguish source data, stored source statistics, offline labeled synthetic meta-training examples and target labels. “No labeled target data online” is compatible with supervised offline router training but is not “no supervision.”
- Group train/validation/test splits by original image ID as well as shift family, severity/order design and stream seed. The same clean image appearing under multiple corruptions can otherwise leak between selector training and testing.
- Fix nested development choices before evaluation; use hidden labels only afterward for action losses, oracle and significance analysis. Oracle-selected actions are diagnostics, not deployable baselines.
- Compare SOURCE, each fixed action, validation-selected best fixed action, an explicit shift classifier/router, MORPHEUS, global and stream-aware evidence selectors, uncertainty-driven cascades, and equal-cost random allocation.
- Measure net utility, per-shift/stream accuracy, regret relative to a cost-aware oracle, negative transfer relative to SOURCE and/or live-state KEEP, harmful-action rate, deadline misses, return-to-source performance, acquisition frequency, forward/backward counts and peak memory.
- Use independent complete streams as repeat units. Correlated batches from one stream do not justify treating every batch as an independent replicate; report paired stream-level intervals.
- Do not declare all CIFAR-C corruptions “real-world,” or treat WILDS as a single dataset. Pick specific tasks and report subgroup/worst-group behavior where appropriate.

## Search and access record

Searches included combinations of TTA with model selection, unsupervised validation, safe adaptation, risk monitoring, hyperparameter selection, counterfactual action choice, value of information, state-conditioned selection, adaptive probing, optimizer state and reset policy. Author/proceedings PDFs and arXiv HTML/metadata were preferred. Browser access to some CVF and SCITEPRESS URLs intermittently returned 403; indexed official PDF passages, author repositories and linked arXiv versions were used where available. Some foundational records were inspected at abstract/first-page level only, as marked in the JSON companion. No claim of exhaustive literature coverage or empirical replication is made.

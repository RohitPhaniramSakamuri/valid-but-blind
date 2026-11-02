# Full source dossier for the continuing research agent

Exported 2026-10-31 from the existing catalog: **103 distinct records, 101 scholarly works and 2 benchmark documents**. Last substantive review: 26 October 2026. This export performs no fresh source verification, full-paper reading or experiment.

Read [HANDOFF](../../HANDOFF.md) first. [Current catalog](../../sources/catalog.json) retains machine-readable records; [BibTeX](../../references.bib) preserves citation keys. A source's presence does not mean its full method was read or its code executed. Read the per-entry scope/history and primary text before using an absence claim as novelty evidence.

## Source index

| Key | Source | Publication/status |
| --- | --- | --- |
| [Ross2011DAgger](#ross2011dagger) | A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning | Proceedings of the Fourteenth International Conference on Artificial Intelligence and Statistics, PMLR 15:627-635 |
| [Weiss2013AdaptiveVOI](#weiss2013adaptivevoi) | Learning Adaptive Value of Information for Structured Prediction | Advances in Neural Information Processing Systems 26 |
| [Li2016AdaBN](#li2016adabn) | Revisiting Batch Normalization For Practical Domain Adaptation | arXiv:1603.04779 |
| [Lipton2018BBSE](#lipton2018bbse) | Detecting and Correcting for Label Shift with Black Box Predictors | Proceedings of the 35th International Conference on Machine Learning, PMLR 80:3122-3130 |
| [Hendrycks2019Corruptions](#hendrycks2019corruptions) | Benchmarking Neural Network Robustness to Common Corruptions and Perturbations | ICLR 2019 |
| [Peng2019DomainNet](#peng2019domainnet) | Moment Matching for Multi-Source Domain Adaptation | ICCV 2019 |
| [Recht2019ImageNetV2](#recht2019imagenetv2) | Do ImageNet Classifiers Generalize to ImageNet? | ICML2019, PMLR97:5389-5400 |
| [Wang2019ImageNetSketch](#wang2019imagenetsketch) | Learning Robust Global Representations by Penalizing Local Predictive Power | NeurIPS2019 |
| [Hendrycks2020AugMix](#hendrycks2020augmix) | AugMix: A Simple Data Processing Method to Improve Robustness and Uncertainty | ICLR 2020 |
| [Liang2020SHOT](#liang2020shot) | Do We Really Need to Access the Source Data? Source Hypothesis Transfer for Unsupervised Domain Adaptation | ICML 2020, PMLR 119:6028–6039 |
| [Schneider2020BNAdapt](#schneider2020bnadapt) | Improving robustness against common corruptions by covariate shift adaptation | NeurIPS 2020 |
| [Sun2020TTT](#sun2020ttt) | Test-Time Training with Self-Supervision for Generalization under Distribution Shifts | ICML 2020, PMLR 119:9229–9248 |
| [Croce2021RobustBench](#croce2021robustbench) | RobustBench: a standardized adversarial robustness benchmark | NeurIPS 2021 Datasets and Benchmarks track |
| [Hendrycks2021ManyFaces](#hendrycks2021manyfaces) | The Many Faces of Robustness: A Critical Analysis of Out-of-Distribution Generalization | ICCV2021, pages8340-8349 per CVF |
| [Hendrycks2021NaturalAdversarial](#hendrycks2021naturaladversarial) | Natural Adversarial Examples | CVPR2021 |
| [Iwasawa2021T3A](#iwasawa2021t3a) | Test-Time Classifier Adjustment Module for Model-Agnostic Domain Generalization | NeurIPS 2021, Advances in Neural Information Processing Systems 34 |
| [Koh2021WILDS](#koh2021wilds) | WILDS: A Benchmark of in-the-Wild Distribution Shifts | ICML 2021, PMLR 139:5637–5664 |
| [Sagawa2021WILDSUnlabeled](#sagawa2021wildsunlabeled) | Extending the WILDS Benchmark for Unsupervised Adaptation | arXiv preprint; WILDS 2.0 update |
| [Sakaridis2021ACDC](#sakaridis2021acdc) | ACDC: The Adverse Conditions Dataset With Correspondences for Semantic Driving Scene Understanding | ICCV 2021, pages10765-10775 |
| [Wang2021Tent](#wang2021tent) | Tent: Fully Test-Time Adaptation by Entropy Minimization | ICLR |
| [Boudiaf2022LAME](#boudiaf2022lame) | Parameter-Free Online Test-Time Adaptation | CVPR 2022, pages 8344–8353 |
| [Gandelsman2022TTTMAE](#gandelsman2022tttmae) | Test-Time Training with Masked Autoencoders | NeurIPS 2022, Advances in Neural Information Processing Systems 35 |
| [Garg2022ATC](#garg2022atc) | Leveraging Unlabeled Data to Predict Out-of-Distribution Performance | International Conference on Learning Representations |
| [Gong2022NOTE](#gong2022note) | NOTE: Robust Continual Test-time Adaptation Against Temporal Correlation | NeurIPS 35 |
| [Kar2022ImageNet3DCC](#kar2022imagenet3dcc) | 3D Common Corruptions for Object Recognition | ICML 2022 Shift Happens workshop / benchmark report |
| [Mirza2022DUA](#mirza2022dua) | The Norm Must Go On: Dynamic Unsupervised Domain Adaptation by Normalization | CVPR 2022, pages 14765–14775 |
| [Niu2022EATA](#niu2022eata) | Efficient Test-Time Model Adaptation without Forgetting | ICML, PMLR 162:16888–16905 |
| [Shu2022TPT](#shu2022tpt) | Test-Time Prompt Tuning for Zero-Shot Generalization in Vision-Language Models | NeurIPS 2022, Advances in Neural Information Processing Systems 35 |
| [Wang2022CoTTA](#wang2022cotta) | Continual Test-Time Domain Adaptation | CVPR |
| [Zhang2022MEMO](#zhang2022memo) | MEMO: Test Time Robustness via Adaptation and Augmentation | NeurIPS 2022, Advances in Neural Information Processing Systems 35 |
| [Dobler2023RMT](#dobler2023rmt) | Robust Mean Teacher for Continual and Gradual Test-Time Adaptation | CVPR 2023, pages 7704–7714 |
| [Lim2023TTN](#lim2023ttn) | TTN: A Domain-Shift Aware Batch Normalization in Test-Time Adaptation | ICLR 2023 |
| [Niu2023SAR](#niu2023sar) | Towards Stable Test-Time Adaptation in Dynamic Wild World | ICLR |
| [Park2023LSA](#park2023lsa) | Label Shift Adapter for Test-Time Adaptation under Covariate and Label Shifts | Proceedings of the IEEE/CVF International Conference on Computer Vision, pages 16375-16385 |
| [Press2023RDumb](#press2023rdumb) | RDumb: A simple approach that questions our progress in continual test-time adaptation | NeurIPS 2023, Advances in Neural Information Processing Systems 36 |
| [Sun2023TTLSA](#sun2023ttlsa) | Beyond Invariance: Test-Time Label-Shift Adaptation for Addressing "Spurious" Correlations | Advances in Neural Information Processing Systems 36 |
| [Yeo2023RNA](#yeo2023rna) | Rapid Network Adaptation: Learning to Adapt Neural Networks Using Test-Time Feedback | ICCV 2023 |
| [Yu2023BenchmarkTTA](#yu2023benchmarktta) | Benchmarking Test-Time Adaptation against Distribution Shifts in Image Classification | arXiv preprint |
| [Yuan2023RoTTA](#yuan2023rotta) | Robust Test-Time Adaptation in Dynamic Scenarios | CVPR, pp.15922–15932 |
| [Zhao2023DELTA](#zhao2023delta) | DELTA: Degradation-Free Fully Test-Time Adaptation | International Conference on Learning Representations |
| [Zhao2023Pitfalls](#zhao2023pitfalls) | On Pitfalls of Test-Time Adaptation | ICML, PMLR 202:42058–42080 |
| [Alfarra2024TimeConstraints](#alfarra2024timeconstraints) | Evaluation of Test-Time Adaptation Under Computational Time Constraints | ICML 2024, PMLR 235:976-991 |
| [Bar2024ProtectedTTA](#bar2024protectedtta) | Protected Test-Time Adaptation via Online Entropy Matching: A Betting Approach | NeurIPS 37 |
| [Du2024UniTTA](#du2024unitta) | UniTTA: Unified Benchmark and Versatile Framework Towards Realistic Test-Time Adaptation | arXiv preprint |
| [Gao2024UniEnt](#gao2024unient) | Unified Entropy Optimization for Open-Set Test-Time Adaptation | CVPR 2024, pages 23975–23984 |
| [Karmanov2024TDA](#karmanov2024tda) | Efficient Test-Time Adaptation of Vision-Language Models | CVPR 2024, pages 14162–14171 |
| [Kim2024TTALine](#kim2024ttaline) | Test-Time Adaptation Induces Stronger Accuracy and Agreement-on-the-Line | NeurIPS 37 |
| [Lee2024AETTA](#lee2024aetta) | AETTA: Label-Free Accuracy Estimation for Test-Time Adaptation | CVPR, pp.28643–28652 |
| [Lee2024BECoTTA](#lee2024becotta) | BECoTTA: Input-dependent Online Blending of Experts for Continual Test-time Adaptation | ICML 2024, PMLR 235:27072–27093 |
| [Lee2024DeYO](#lee2024deyo) | Entropy is not Enough for Test-Time Adaptation: From the Perspective of Disentangled Factors | ICLR 2024 |
| [Marsden2024ROID](#marsden2024roid) | Universal Test-Time Adaptation Through Weight Ensembling, Diversity Weighting, and Prior Correction | WACV 2024; official CVF page lists pages 2555–2565 |
| [Park2024LAW](#park2024law) | Layer-wise Auto-Weighting for Non-Stationary Test-Time Adaptation | Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision |
| [Su2024TRIBE](#su2024tribe) | Towards Real-World Test-Time Adaptation: Tri-Net Self-Training with Balanced Normalization | Proceedings of the AAAI Conference on Artificial Intelligence 38(13) |
| [Bao2025Mint](#bao2025mint) | Mint: A Simple Test-Time Adaptation of Vision-Language Models against Common Corruptions | NeurIPS 2025, Advances in Neural Information Processing Systems 38 |
| [Dai2025FreeTTA](#dai2025freetta) | Free on the Fly: Enhancing Flexibility in Test-Time Adaptation with Online EM | CVPR 2025, pages 9538–9548 |
| [Grover2025DynaTTA](#grover2025dynatta) | Shift-Aware Test Time Adaptation and Benchmarking for Time-Series Forecasting | ICML 2025 Workshop on Test-Time Adaptation: Putting Updates to the Test! |
| [Jang2025DART](#jang2025dart) | Label Distribution Shift-Aware Prediction Refinement for Test-Time Adaptation | Transactions on Machine Learning Research |
| [Liang2025TTASurvey](#liang2025ttasurvey) | A Comprehensive Survey on Test-Time Adaptation under Distribution Shifts | International Journal of Computer Vision 133, 31–64; preprint first posted 2023 |
| [Liu2025TACT](#liu2025tact) | Test-Time Adaptation by Causal Trimming | Advances in Neural Information Processing Systems 38 |
| [Park2025HybridTTA](#park2025hybridtta) | Hybrid-TTA: Continual Test-time Adaptation via Dynamic Domain Shift Detection | ICCV 2025 |
| [Sahoo2025GALA](#sahoo2025gala) | A Layer Selection Approach to Test Time Adaptation | AAAI 2025 |
| [Schirmer2025Monitoring](#schirmer2025monitoring) | Monitoring Risks in Test-Time Adaptation | NeurIPS 2025, Advances in Neural Information Processing Systems 38 |
| [Tan2025EATAC](#tan2025eatac) | Uncertainty-Calibrated Test-Time Model Adaptation without Forgetting | IEEE Transactions on Pattern Analysis and Machine Intelligence |
| [Vianna2025ChannelSelective](#vianna2025channelselective) | Channel-Selective Normalization for Label-Shift Robust Test-Time Adaptation | Proceedings of The 3rd Conference on Lifelong Learning Agents, PMLR 274:514-533 |
| [Wang2025OTTASurvey](#wang2025ottasurvey) | In Search of Lost Online Test-Time Adaptation: A Survey | International Journal of Computer Vision 133, 1106–1139; online publication 15 September 2024 |
| [Ye2025DATTA](#ye2025datta) | DATTA: Domain Diversity Aware Test-Time Adaptation for Dynamic Domain Shift Data Streams | ICME 2025 |
| [Zanella2025StatA](#zanella2025stata) | Realistic Test-Time Adaptation of Vision-Language Models | CVPR 2025, pages25103-25112 |
| [Aronsson2026FeatureAcquisitionSurvey](#aronsson2026featureacquisitionsurvey) | A Survey on Active Feature Acquisition Strategies | IJCAI 2026 Survey Track, 7740–7748 |
| [Cygert2026RealisticSelection](#cygert2026realisticselection) | Realistic Evaluation of Test-Time Adaptation: Unsupervised Model Selection | VISAPP, volume 1, pp.75–86 |
| [Danilowski2026BoTTA](#danilowski2026botta) | BoTTA: Benchmarking On-device Test Time Adaptation | Proceedings of the 2026 ACM/IEEE International Conference on Embedded Artificial Intelligence and Sensing Systems, pages 465–477 |
| [Danilowski2026MORPHEUS](#danilowski2026morpheus) | MORPHEUS: Meta Test-Time Adaptation via Neural Collapse Geometry | ICLR 2026 Test-Time Updates Workshop |
| [Doloriel2026SEGA](#doloriel2026sega) | Continual Test-Time Adaptation via Entropy Sensitivity-Guidance in Strict Online Setting | arXiv preprint |
| [Fan2026MoETTA](#fan2026moetta) | MoETTA: Test-Time Adaptation Under Mixed Distribution Shifts with MoE-LayerNorm | AAAI2026 Main Technical Track |
| [Gai2026AdaTentPlusPlus](#gai2026adatentplusplus) | AdaTent++: reliability-guided hybrid test-time adaptation for traffic sign detection under distribution shift | Frontiers in Signal Processing6 |
| [Han2026Exchangeability](#han2026exchangeability) | The Premise Is the Problem: Exchangeability Failure in Self-Monitored Test-Time Adaptation | arXiv preprint 2610.07038 |
| [Huang2026TTABC](#huang2026ttabc) | What Drives Test-Time Adaptation for CLIP? A Controlled Empirical Study from an Update Perspective | arXiv preprint; author-reported NeurIPS2026 E&D |
| [Huzaifa2026WISEATTA](#huzaifa2026wiseatta) | WISE-ATTA: When to Ask for Labels in Budgeted Active Test-Time Adaptation | arXiv:2609.37687, 29 September 2026 |
| [Jain2026MeasureLess](#jain2026measureless) | Measure Less, Know More: Self-Supervised Test-Time Feature Acquisition | arXiv:2610.03454v1, 2 October 2026; manuscript carries a NeurIPS 2026 footer, acceptance not independently confirmed |
| [Jeong2026CalibrationAware](#jeong2026calibrationaware) | Calibration-Aware Online Adaptation under Label Shift | Proceedings of the 42nd Conference on Uncertainty in Artificial Intelligence, PMLR 337:2480-2516 |
| [Jhawar2026HDTTA](#jhawar2026hdtta) | HD-TTA: Hypothesis-Driven Test-Time Adaptation for Safer Brain Tumor Segmentation | MICCAI2026 (official page found); inspected arXiv preprint |
| [Jhawar2026Identifiability](#jhawar2026identifiability) | When is Test-Time Adaptation Identifiable From Unlabeled Evidence? | arXiv |
| [Jiang2026CAS](#jiang2026cas) | To Adapt or Not to Adapt? Selective Adaptation for Vision-Language Models | arXiv:2609.08367v1; author record comments identify ECCV 2026 |
| [Karimi2026ShiftACT](#karimi2026shiftact) | Shift-ACT: Test-time adaptation via shift-aware class-specific dynamic thresholding for domain generalization | Neurocomputing 663, article132013 |
| [Kumar2026RGTTA](#kumar2026rgtta) | RG-TTA: Regime-Guided Meta-Control for Test-Time Adaptation in Streaming Time Series | arXiv preprint |
| [Lai2026GOLD](#lai2026gold) | The Golden Subspace: Where Efficiency Meets Generalization in Continual Test-Time Adaptation | CVPR 2026, pages 3866–3875 |
| [Lim2026ASR](#lim2026asr) | When and Where to Reset Matters for Long-Term Test-Time Adaptation | ICLR |
| [Liu2026TiME](#liu2026time) | TiME: Test-Time Mixture-of-Experts Routing via Asymmetric CO-Optimal Transport for Continual Test-Time Adaptation | Proceedings of the 43rd International Conference on Machine Learning, PMLR 306:78597–78632 |
| [Lu2026AgenticTTT](#lu2026agenticttt) | Agentic-TTT: Training test-time policy for test-time training | arXiv preprint2610.12002 |
| [Majumdar2026HelpHarm](#majumdar2026helpharm) | When Test-Time Adaptation Helps, Harms, or Becomes Inactive: A Condition-Level Study on CIFAR-10-C | arXiv preprint |
| [Rehan2026FORGE](#rehan2026forge) | FORGE: Forward-Only Test-Time Adaptation for Integer-Only Vision Models on Microcontrollers | arXiv:2609.01683v1; arXiv record identifies Transactions on Machine Learning Research 2026 publication |
| [Sabour2026DriftTTA](#sabour2026drifttta) | Hidden Trajectories Don't Lie: Correcting Corruption Drift for Test-Time Adaptation | arXiv:2610.24220v1 |
| [Shamsi2026MultiHypothesis](#shamsi2026multihypothesis) | Multi-Hypothesis Test-Time Adaptation to Mitigate Underspecification | arXiv preprint 2607.00259 |
| [Sreeram2026Tempora](#sreeram2026tempora) | Tempora: Characterising the Time-Contingent Utility of Online Test-Time Adaptation | ICML, PMLR 306:115420–115456 |
| [Su2026SLRF](#su2026slrf) | Shift-level regulated continual test-time adaptation framework | Data Mining and Knowledge Discovery 40, article 63 |
| [TestTimeLearning2026Leaderboard](#testtimelearning2026leaderboard) | Test-Time Adaptation Leaderboard | Living benchmark website and repository |
| [WILDS2026SubmissionRules](#wilds2026submissionrules) | WILDS leaderboard submission guidelines | Official benchmark documentation |
| [Wakayama2026DecisionTTT](#wakayama2026decisionttt) | A Decision-Theoretic View of Test-Time Training: When, How Far, and Which Directions to Adapt | Proceedings of the 43rd International Conference on Machine Learning, PMLR 306:124279–124317 |
| [Weerasinghe2026LATTA](#weerasinghe2026latta) | Logit-Adjusted Test-Time Adaptation under Partial Class Imbalance | Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision, pages 5977-5985 |
| [Yang2026SATTS](#yang2026satts) | SA-TTS: Stress-Aware Test-Time Scaling for Vision Models | Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops, pages 11480–11487 |
| [Zhang2026MoASEPlusPlus](#zhang2026moaseplusplus) | MoASE++: Mixture of Activation Sparsity Experts with Domain-Adaptive On-policy Distillation for Continual Test Time Adaptation | arXiv preprint |
| [Zhang2026PhysicalDiagnosis](#zhang2026physicaldiagnosis) | When Does Test-Time Physical Diagnosis Pay? A Frozen Policy Buys Evidence It Never Reads | arXiv:2609.22299v1 |
| [Zhao2026FACTOR](#zhao2026factor) | FACTOR: Counterfactual Training-Free Test-Time Adaptation for Open-Vocabulary Object Detection | arXiv preprint |
| [Zhou2026Learnability](#zhou2026learnability) | On the Learnability of Test-Time Adaptation: A Recovery Complexity Perspective | ICML 2026, PMLR 306:166172–166195 |

## Ross2011DAgger

**A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning**

Authors: Stephane Ross; Geoffrey Gordon; Drew Bagnell.

Publication: 2011; Proceedings of the Fourteenth International Conference on Artificial Intelligence and Statistics, PMLR 15:627-635.

Primary source: [A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning](https://proceedings.mlr.press/v15/ross11a.html). [Project paper note](../../papers/Ross2011DAgger.md).

Publication qualification: AISTATS 2011 proceedings verified

Recorded reading scope: Official proceedings metadata and abstract; foundational scope checked, proof and full algorithm not reread in this pass.

Inspected locations: Official abstract; Bibliographic metadata.

Relevance / overlap from our reading: Learning on the state distribution induced by one's own sequential policy is established; essential baseline for learner-state aggregation in TTA selection.

Limitation / reviewer boundary: Imitation learning generally; not a vision-TTA benchmark or matched empirical baseline without an explicit adaptation.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

[Source ledger](../../notes/review-refresh-2026-10-26/verifier-sources.json).

### Recorded reading history

- **2026-10-26**: Official proceedings metadata, abstract and PDF introduction; selective reading.
  Locations: Abstract; Introduction.
  Qualification: Its expert-feedback and reduction assumptions must not be silently transferred to unlabeled target TTA. Auxiliary labeled rollouts are development supervision.
  [Dated ledger](../../notes/review-refresh-2026-10-26/lead-sources.json).

- **2026-10-26**: Official proceedings metadata and abstract; foundational scope checked, proof and full algorithm not reread in this pass.
  Locations: Official abstract; Bibliographic metadata.
  Qualification: Imitation learning generally; not a vision-TTA benchmark or matched empirical baseline without an explicit adaptation.
  [Dated ledger](../../notes/review-refresh-2026-10-26/verifier-sources.json).

### Other stored metadata

```json
{
  "entry_type": "inproceedings",
  "accessed": "2026-10-26"
}
```


## Weiss2013AdaptiveVOI

**Learning Adaptive Value of Information for Structured Prediction**

Authors: David J Weiss; Ben Taskar.

Publication: 2013; Advances in Neural Information Processing Systems 26.

Primary source: [Learning Adaptive Value of Information for Structured Prediction](https://proceedings.neurips.cc/paper_files/paper/2013/hash/ebd9629fc3ae5e9f6611e2ee05a31cef-Abstract.html). [Project paper note](../../papers/Weiss2013AdaptiveVOI.md).

Publication qualification: Conference paper

Recorded reading scope: Official proceedings metadata/abstract and introduction

Inspected locations: Abstract; section 1.

Relevance / overlap from our reading: Learned runtime control of feature acquisition by decision value and computation cost.

Limitation / reviewer boundary: Value of information and adaptive acquisition are established principles; no claim of inventing them here.

[Source ledger](../../notes/shift-aware-tta-review-lead-sources.json).


## Li2016AdaBN

**Revisiting Batch Normalization For Practical Domain Adaptation**

Authors: Yanghao Li; Naiyan Wang; Jianping Shi; Jiaying Liu; Xiaodi Hou.

Publication: 2016; arXiv:1603.04779.

Primary source: [Revisiting Batch Normalization For Practical Domain Adaptation](https://arxiv.org/abs/1603.04779). [Project paper note](../../papers/Li2016AdaBN.md).

Publication qualification: Verified preprint; related 2018 journal extension has a different title and author order and is not merged here

Recorded reading scope: Primary arXiv metadata and abstract only

Inspected locations: Abstract.

Relevance / overlap from our reading: Adapting normalization statistics without gradient updates provides a simple terminal-action baseline.

Limitation / reviewer boundary: The proposed episodic statistics update still needs a declared support/query configuration; the abstract does not specify our exact wrapper.

[Source ledger](../../notes/shift-aware-tta-review-lead-sources.json).


## Lipton2018BBSE

**Detecting and Correcting for Label Shift with Black Box Predictors**

Authors: Zachary Lipton; Yu-Xiang Wang; Alexander Smola.

Publication: 2018; Proceedings of the 35th International Conference on Machine Learning, PMLR 80:3122-3130.

Primary source: [Detecting and Correcting for Label Shift with Black Box Predictors](https://proceedings.mlr.press/v80/lipton18a.html). [Project paper note](../../papers/Lipton2018BBSE.md).

Publication qualification: ICML 2018 proceedings verified

Recorded reading scope: Official metadata/abstract and visible official PDF introduction on estimator assumptions; partial reading.

Inspected locations: Abstract; Introduction and confusion-matrix condition.

Relevance / overlap from our reading: Estimates target class priors from unlabeled predictions and labeled source confusion statistics; detects and corrects pure label shift.

Limitation / reviewer boundary: Requires invariant class-conditionals and invertible confusion matrix; simultaneous nuisance shifts can invalidate its source confusion statistics.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

[Source ledger](../../notes/review-refresh-2026-10-26/verifier-sources.json).

### Recorded reading history

- **2026-10-26**: Official metadata/abstract and visible official PDF introduction on estimator assumptions; partial reading.
  Locations: Abstract; Introduction and confusion-matrix condition.
  Qualification: Requires invariant class-conditionals and invertible confusion matrix; simultaneous nuisance shifts can invalidate its source confusion statistics.
  [Dated ledger](../../notes/review-refresh-2026-10-26/verifier-sources.json).

### Other stored metadata

```json
{
  "pdf_url": "https://proceedings.mlr.press/v80/lipton18a/lipton18a.pdf",
  "accessed": "2026-10-26"
}
```


## Hendrycks2019Corruptions

**Benchmarking Neural Network Robustness to Common Corruptions and Perturbations**

Authors: Dan Hendrycks; Thomas Dietterich.

Publication: 2019; ICLR 2019.

Primary source: [Benchmarking Neural Network Robustness to Common Corruptions and Perturbations](https://arxiv.org/abs/1903.12261). [Project paper note](../../papers/Hendrycks2019Corruptions.md).

Publication qualification: Conference paper

Recorded reading scope: Abstract and official dataset repository README

Inspected locations: Abstract; repository ImageNet-C and CIFAR download/evaluation notes.

Relevance / overlap from our reading: Standard corruption benchmarks and deterministic stored evaluation data.

Limitation / reviewer boundary: Generated corruption tests do not establish performance on naturally occurring deployment shifts.

Recorded implementation/author resource: [link](https://github.com/hendrycks/robustness). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/shift-aware-tta-review-lead-sources.json).


## Peng2019DomainNet

**Moment Matching for Multi-Source Domain Adaptation**

Authors: Xingchao Peng; Qinxun Bai; Xide Xia; Zijun Huang; Kate Saenko; Bo Wang.

Publication: 2019; ICCV 2019.

Primary source: [Moment Matching for Multi-Source Domain Adaptation](https://arxiv.org/abs/1812.01754). [Project paper note](../../papers/Peng2019DomainNet.md).

Publication qualification: Conference paper

Recorded reading scope: Fresh author-site overview, cleaned split definitions, citation metadata

Inspected locations: Author site dataset and citation.

Relevance / overlap from our reading: Natural visual domains for external validation.

Limitation / reviewer boundary: Full DomainNet and the commonly used DomainNet-126 subset are different protocols and must be named accurately.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

Recorded implementation/author resource: [link](https://ai.bu.edu/DomainNet/). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/review-refresh-2026-10-26/benchmarks-sources.json).

### Recorded reading history

- **2026-10-23**: Dataset description in paper and author dataset page; not full method
  Locations: DomainNet dataset and experiment sections.
  Qualification: Full DomainNet and the commonly used DomainNet-126 subset are different protocols and must be named accurately.
  [Dated ledger](../../notes/shift-aware-tta-review-lead-sources.json).

- **2026-10-26**: Fresh author-site overview, cleaned split definitions, citation metadata
  Locations: Author site dataset and citation.
  Qualification: Do not conflate full345-class six-domain dataset with DomainNet126.
  [Dated ledger](../../notes/review-refresh-2026-10-26/benchmarks-sources.json).

### Other stored metadata

```json
{
  "refresh_read_scope": "Fresh author-site overview, cleaned split definitions, citation metadata",
  "refresh_locations": "Author site dataset and citation",
  "refresh_limitation": "Do not conflate full345-class six-domain dataset with DomainNet126.",
  "verified_on": "2026-10-26"
}
```


## Recht2019ImageNetV2

**Do ImageNet Classifiers Generalize to ImageNet?**

Authors: Benjamin Recht; Rebecca Roelofs; Ludwig Schmidt; Vaishaal Shankar.

Publication: 2019; ICML2019, PMLR97:5389-5400.

Primary source: [Do ImageNet Classifiers Generalize to ImageNet?](https://proceedings.mlr.press/v97/recht19a.html). [Project paper note](../../papers/Recht2019ImageNetV2.md).

Publication qualification: Official ICML2019 verified

Recorded reading scope: Official abstract and metadata

Inspected locations: Abstract.

Relevance / overlap from our reading: Natural resampling shift test for CIFAR/ImageNet.

Limitation / reviewer boundary: Dataset collection difficulty differs from identifiable corruption cause; specify V2 subset.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

[Source ledger](../../notes/review-refresh-2026-10-26/benchmarks-sources.json).

### Recorded reading history

- **2026-10-26**: Official abstract and metadata
  Locations: Abstract.
  Qualification: Dataset collection difficulty differs from identifiable corruption cause; specify V2 subset.
  [Dated ledger](../../notes/review-refresh-2026-10-26/benchmarks-sources.json).

### Other stored metadata

```json
{
  "verified_on": "2026-10-26"
}
```


## Wang2019ImageNetSketch

**Learning Robust Global Representations by Penalizing Local Predictive Power**

Authors: Haohan Wang; Songwei Ge; Zachary Lipton; Eric P. Xing.

Publication: 2019; NeurIPS2019.

Primary source: [Learning Robust Global Representations by Penalizing Local Predictive Power](https://papers.nips.cc/paper_files/paper/2019/hash/3eefceb8087e964f89c2d59e8a249915-Abstract.html). [Project paper note](../../papers/Wang2019ImageNetSketch.md).

Publication qualification: Official NeurIPS2019 verified

Recorded reading scope: Official abstract/author metadata and arXiv abstract

Inspected locations: Abstract.

Relevance / overlap from our reading: Introduces ImageNet-Sketch; source representation should rely on global structure rather than local shortcuts.

Limitation / reviewer boundary: Proceedings author order used; arXiv listing order differs. Sketch is representation/style shift not physical sensor corruption.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

[Source ledger](../../notes/review-refresh-2026-10-26/benchmarks-sources.json).

### Recorded reading history

- **2026-10-26**: Official abstract/author metadata and arXiv abstract
  Locations: Abstract.
  Qualification: Proceedings author order used; arXiv listing order differs. Sketch is representation/style shift not physical sensor corruption.
  [Dated ledger](../../notes/review-refresh-2026-10-26/benchmarks-sources.json).

### Other stored metadata

```json
{
  "verified_on": "2026-10-26",
  "preprint_url": "https://arxiv.org/abs/1905.13549"
}
```


## Hendrycks2020AugMix

**AugMix: A Simple Data Processing Method to Improve Robustness and Uncertainty**

Authors: Dan Hendrycks; Norman Mu; Ekin D. Cubuk; Barret Zoph; Justin Gilmer; Balaji Lakshminarayanan.

Publication: 2020; ICLR 2020.

Primary source: [AugMix: A Simple Data Processing Method to Improve Robustness and Uncertainty](https://iclr.cc/virtual_2020/poster_S1gmrxHFvB.html). [Project paper note](../../papers/Hendrycks2020AugMix.md).

Publication qualification: Official ICLR2020 verified; preprint2019

Recorded reading scope: Official conference abstract/author metadata, arXiv and author repository method/checkpoint description

Inspected locations: Abstract; Repository Introduction and Pretrained weights.

Relevance / overlap from our reading: Robust source-training control using mixed augmentations and consistency; available ResNet50 checkpoint.

Limitation / reviewer boundary: Source training intervention, not test-time policy selection; compare same preparation and checkpoint quality.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

Recorded implementation/author resource: [link](https://github.com/google-research/augmix). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/review-refresh-2026-10-26/benchmarks-sources.json).

### Recorded reading history

- **2026-10-26**: Official conference abstract/author metadata, arXiv and author repository method/checkpoint description
  Locations: Abstract; Repository Introduction and Pretrained weights.
  Qualification: Source training intervention, not test-time policy selection; compare same preparation and checkpoint quality.
  [Dated ledger](../../notes/review-refresh-2026-10-26/benchmarks-sources.json).

### Other stored metadata

```json
{
  "verified_on": "2026-10-26",
  "preprint_url": "https://arxiv.org/abs/1912.02781"
}
```


## Liang2020SHOT

**Do We Really Need to Access the Source Data? Source Hypothesis Transfer for Unsupervised Domain Adaptation**

Authors: Jian Liang; Dapeng Hu; Jiashi Feng.

Publication: 2020; ICML 2020, PMLR 119:6028–6039.

Primary source: [Do We Really Need to Access the Source Data? Source Hypothesis Transfer for Unsupervised Domain Adaptation](https://proceedings.mlr.press/v119/liang20a.html). [Project paper note](../../papers/Liang2020SHOT.md).

Publication qualification: Official ICML proceedings verified.

Recorded reading scope: Official proceedings metadata and abstract only.

Inspected locations: Abstract.

Relevance / overlap from our reading: Freezes the source classifier and adapts the target feature extractor with information maximization and pseudo-labeling; foundational source-free adaptation comparator.

Limitation / reviewer boundary: Source-free domain adaptation is not automatically one-pass online TTA. Target access, clustering passes and source training must be matched before numerical comparison.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

[Source ledger](../../notes/review-refresh-2026-10-26/lead-sources.json).

### Recorded reading history

- **2026-10-26**: Official proceedings metadata and abstract only.
  Locations: Abstract.
  Qualification: Source-free domain adaptation is not automatically one-pass online TTA. Target access, clustering passes and source training must be matched before numerical comparison.
  [Dated ledger](../../notes/review-refresh-2026-10-26/lead-sources.json).

### Other stored metadata

```json
{
  "entry_type": "inproceedings"
}
```


## Schneider2020BNAdapt

**Improving robustness against common corruptions by covariate shift adaptation**

Authors: Steffen Schneider; Evgenia Rusak; Luisa Eck; Oliver Bringmann; Wieland Brendel; Matthias Bethge.

Publication: 2020; NeurIPS 2020.

Primary source: [Improving robustness against common corruptions by covariate shift adaptation](https://papers.nips.cc/paper_files/paper/2020/hash/85690f81aadc1749175c187784afc9ee-Abstract.html). [Project paper note](../../papers/Schneider2020BNAdapt.md).

Publication qualification: Official NeurIPS2020 verified

Recorded reading scope: Primary abstract, metadata, author project page; selective PDF header inspection

Inspected locations: Abstract; Project explanation.

Relevance / overlap from our reading: Strong simple BN-statistics adaptation across models; essential cheap baseline and robust-source comparison.

Limitation / reviewer boundary: Multiple target examples and contamination/class-mixture assumptions matter; improvements do not prove arbitrary covariate-shift correction.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

Recorded implementation/author resource: [link](https://github.com/bethgelab/robustness). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/review-refresh-2026-10-26/benchmarks-sources.json).

### Recorded reading history

- **2026-10-26**: Official abstract, PDF introduction and normalization formulation; selective reading.
  Locations: Abstract; Section 2; Section 4 discussion of mixed shifts.
  Qualification: Moment correction assumes useful shared target statistics; mixed conditions and class-mixture effects constrain it. Small batches require estimation/shrinkage choices.
  [Dated ledger](../../notes/review-refresh-2026-10-26/lead-sources.json).

- **2026-10-26**: Primary abstract, metadata, author project page; selective PDF header inspection
  Locations: Abstract; Project explanation.
  Qualification: Multiple target examples and contamination/class-mixture assumptions matter; improvements do not prove arbitrary covariate-shift correction.
  [Dated ledger](../../notes/review-refresh-2026-10-26/benchmarks-sources.json).

### Other stored metadata

```json
{
  "entry_type": "inproceedings",
  "verified_on": "2026-10-26",
  "preprint_url": "https://arxiv.org/abs/2006.16971"
}
```


## Sun2020TTT

**Test-Time Training with Self-Supervision for Generalization under Distribution Shifts**

Authors: Yu Sun; Xiaolong Wang; Zhuang Liu; John Miller; Alexei Efros; Moritz Hardt.

Publication: 2020; ICML 2020, PMLR 119:9229–9248.

Primary source: [Test-Time Training with Self-Supervision for Generalization under Distribution Shifts](https://proceedings.mlr.press/v119/sun20b.html). [Project paper note](../../papers/Sun2020TTT.md).

Publication qualification: ICML 2020 official proceedings; linked 2019 preprint is the same work.

Recorded reading scope: Official metadata, abstract and PDF introduction/method summary, not full experimental audit.

Inspected locations: Abstract; Introduction; Section 4 overview.

Relevance / overlap from our reading: Learns from an auxiliary self-supervised task at test time; online variant retains updates. Gradient alignment gives a restricted condition for improvement.

Limitation / reviewer boundary: Requires source-stage preparation of the auxiliary task. Our interpretation: improvement of that task need not imply improvement of classification on a new shift.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

[Source ledger](../../notes/review-refresh-2026-10-26/lead-sources.json).

### Recorded reading history

- **2026-10-26**: Official metadata, abstract and PDF introduction/method summary, not full experimental audit.
  Locations: Abstract; Introduction; Section 4 overview.
  Qualification: Requires source-stage preparation of the auxiliary task. Our interpretation: improvement of that task need not imply improvement of classification on a new shift.
  [Dated ledger](../../notes/review-refresh-2026-10-26/lead-sources.json).

### Other stored metadata

```json
{
  "entry_type": "inproceedings"
}
```


## Croce2021RobustBench

**RobustBench: a standardized adversarial robustness benchmark**

Authors: Francesco Croce; Maksym Andriushchenko; Vikash Sehwag; Edoardo Debenedetti; Nicolas Flammarion; Mung Chiang; Prateek Mittal; Matthias Hein.

Publication: 2021; NeurIPS 2021 Datasets and Benchmarks track.

Primary source: [RobustBench: a standardized adversarial robustness benchmark](https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/hash/a3c65c2974270fd093ee8a9bf8ae7d0b-Abstract-round2.html). [Project paper note](../../papers/Croce2021RobustBench.md).

Publication qualification: Official proceedings verified

Recorded reading scope: Official abstract and current author-maintained repository/site; not all leaderboard methods audited

Inspected locations: Abstract; Repository common-corruption section; Site May2022 news.

Relevance / overlap from our reading: Standardized models and corruption metrics/checkpoints; ImageNet-3DCC extension.

Limitation / reviewer boundary: Primarily robustness benchmark; a fixed checkpoint score does not uniquely specify a streaming TTA protocol.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

Recorded implementation/author resource: [link](https://github.com/RobustBench/robustbench). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/review-refresh-2026-10-26/benchmarks-sources.json).

### Recorded reading history

- **2026-10-26**: Official abstract and current author-maintained repository/site; not all leaderboard methods audited
  Locations: Abstract; Repository common-corruption section; Site May2022 news.
  Qualification: Primarily robustness benchmark; a fixed checkpoint score does not uniquely specify a streaming TTA protocol.
  [Dated ledger](../../notes/review-refresh-2026-10-26/benchmarks-sources.json).

### Other stored metadata

```json
{
  "verified_on": "2026-10-26"
}
```


## Hendrycks2021ManyFaces

**The Many Faces of Robustness: A Critical Analysis of Out-of-Distribution Generalization**

Authors: Dan Hendrycks; Steven Basart; Norman Mu; Saurav Kadavath; Frank Wang; Evan Dorundo; Rahul Desai; Tyler Zhu; Samyak Parajuli; Mike Guo; Dawn Song; Jacob Steinhardt; Justin Gilmer.

Publication: 2021; ICCV2021, pages8340-8349 per CVF.

Primary source: [The Many Faces of Robustness: A Critical Analysis of Out-of-Distribution Generalization](https://openaccess.thecvf.com/content/ICCV2021/html/Hendrycks_The_Many_Faces_of_Robustness_A_Critical_Analysis_of_Out-of-Distribution_ICCV_2021_paper.html). [Project paper note](../../papers/Hendrycks2021ManyFaces.md).

Publication qualification: Official ICCV2021 verified; CVF page pagination followed

Recorded reading scope: CVF metadata/abstract and selective PDF robustness discussion

Inspected locations: Abstract; PDF synthetic-to-natural robustness discussion.

Relevance / overlap from our reading: ImageNet-R and other real shifts; DeepAugment robust-source controls; simultaneous multiple shifts.

Limitation / reviewer boundary: Improvements on local texture/corruption do not imply gains on geographic shifts; source training differs from test-time routing.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

[Source ledger](../../notes/review-refresh-2026-10-26/benchmarks-sources.json).

### Recorded reading history

- **2026-10-26**: CVF metadata/abstract and selective PDF robustness discussion
  Locations: Abstract; PDF synthetic-to-natural robustness discussion.
  Qualification: Improvements on local texture/corruption do not imply gains on geographic shifts; source training differs from test-time routing.
  [Dated ledger](../../notes/review-refresh-2026-10-26/benchmarks-sources.json).

### Other stored metadata

```json
{
  "verified_on": "2026-10-26"
}
```


## Hendrycks2021NaturalAdversarial

**Natural Adversarial Examples**

Authors: Dan Hendrycks; Kevin Zhao; Steven Basart; Jacob Steinhardt; Dawn Song.

Publication: 2021; CVPR2021.

Primary source: [Natural Adversarial Examples](https://openaccess.thecvf.com/content/CVPR2021/papers/Hendrycks_Natural_Adversarial_Examples_CVPR_2021_paper.pdf). [Project paper note](../../papers/Hendrycks2021NaturalAdversarial.md).

Publication qualification: Official CVPR2021 PDF verified

Recorded reading scope: Official PDF header/abstract/introduction/figure1

Inspected locations: Abstract; Figure1; Introduction.

Relevance / overlap from our reading: ImageNet-A natural hard examples; ImageNet-O unseen-class detection is a separate task.

Limitation / reviewer boundary: Subset class mapping and adversarial filtration matter; performance is not an illumination-only test.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

[Source ledger](../../notes/review-refresh-2026-10-26/benchmarks-sources.json).

### Recorded reading history

- **2026-10-26**: Official PDF header/abstract/introduction/figure1
  Locations: Abstract; Figure1; Introduction.
  Qualification: Subset class mapping and adversarial filtration matter; performance is not an illumination-only test.
  [Dated ledger](../../notes/review-refresh-2026-10-26/benchmarks-sources.json).

### Other stored metadata

```json
{
  "verified_on": "2026-10-26",
  "preprint_url": "https://arxiv.org/abs/1907.07174"
}
```


## Iwasawa2021T3A

**Test-Time Classifier Adjustment Module for Model-Agnostic Domain Generalization**

Authors: Yusuke Iwasawa; Yutaka Matsuo.

Publication: 2021; NeurIPS 2021, Advances in Neural Information Processing Systems 34.

Primary source: [Test-Time Classifier Adjustment Module for Model-Agnostic Domain Generalization](https://proceedings.neurips.cc/paper_files/paper/2021/hash/1415fe9fea0fa1e45dddcff5682239a0-Abstract.html). [Project paper note](../../papers/Iwasawa2021T3A.md).

Publication qualification: Official NeurIPS 2021 proceedings verified.

Recorded reading scope: Official proceedings abstract and metadata; PDF first page.

Inspected locations: Abstract.

Relevance / overlap from our reading: Updates pseudo-prototype class templates using unlabeled features without backpropagation; important inexpensive alternative to parameter adaptation.

Limitation / reviewer boundary: Our interpretation: pseudo-prototype quality depends on source features and pseudo-labels. Its DG source-training protocol differs from single-source corruption experiments.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

[Source ledger](../../notes/review-refresh-2026-10-26/lead-sources.json).

### Recorded reading history

- **2026-10-26**: Official proceedings abstract and metadata; PDF first page.
  Locations: Abstract.
  Qualification: Our interpretation: pseudo-prototype quality depends on source features and pseudo-labels. Its DG source-training protocol differs from single-source corruption experiments.
  [Dated ledger](../../notes/review-refresh-2026-10-26/lead-sources.json).

### Other stored metadata

```json
{
  "entry_type": "inproceedings"
}
```


## Koh2021WILDS

**WILDS: A Benchmark of in-the-Wild Distribution Shifts**

Authors: Pang Wei Koh; Shiori Sagawa; Henrik Marklund; Sang Michael Xie; Marvin Zhang; Akshay Balsubramani; Weihua Hu; Michihiro Yasunaga; Richard Lanas Phillips; Irena Gao; Tony Lee; Etienne David; Ian Stavness; Wei Guo; Berton Earnshaw; Imran Haque; Sara M Beery; Jure Leskovec; Anshul Kundaje; Emma Pierson; Sergey Levine; Chelsea Finn; Percy Liang.

Publication: 2021; ICML 2021, PMLR 139:5637–5664.

Primary source: [WILDS: A Benchmark of in-the-Wild Distribution Shifts](https://proceedings.mlr.press/v139/koh21a.html). [Project paper note](../../papers/Koh2021WILDS.md).

Publication qualification: Conference paper

Recorded reading scope: Official proceedings metadata/abstract and opening dataset examples

Inspected locations: Abstract; figure 1; author blog's FMoW/domain/subpopulation examples.

Relevance / overlap from our reading: Natural domain and subpopulation shifts with dataset-specific evaluation.

Limitation / reviewer boundary: WILDS is a suite of tasks; saying 'evaluate on WILDS' does not specify a reproducible experiment.

Recorded implementation/author resource: [link](https://wilds.stanford.edu/). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/shift-aware-tta-review-lead-sources.json).


## Sagawa2021WILDSUnlabeled

**Extending the WILDS Benchmark for Unsupervised Adaptation**

Authors: Shiori Sagawa; Pang Wei Koh; Tony Lee; Irena Gao; Sang Michael Xie; Kendrick Shen; Ananya Kumar; Weihua Hu; Michihiro Yasunaga; Henrik Marklund; Sara Beery; Etienne David; Ian Stavness; Wei Guo; Jure Leskovec; Kate Saenko; Tatsunori Hashimoto; Sergey Levine; Chelsea Finn; Percy Liang.

Publication: 2021; arXiv preprint; WILDS 2.0 update.

Primary source: [Extending the WILDS Benchmark for Unsupervised Adaptation](https://arxiv.org/abs/2112.05090). [Project paper note](../../papers/Sagawa2021WILDSUnlabeled.md).

Publication qualification: Preprint submitted December2021; latest arXiv v2 April2022; venue not independently verified

Recorded reading scope: Primary abstract/metadata, official WILDS data and submission documentation; no full experimental audit

Inspected locations: Abstract; Official data documentation.

Relevance / overlap from our reading: Adds curated unlabeled splits to 8 of10 WILDS datasets with unchanged labeled splits/metrics; adaptation success is limited.

Limitation / reviewer boundary: Designated unlabeled adaptation before final evaluation differs from adapting on test inputs.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

Recorded implementation/author resource: [link](https://github.com/p-lambda/wilds). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/review-refresh-2026-10-26/benchmarks-sources.json).

### Recorded reading history

- **2026-10-26**: Primary abstract/metadata, official WILDS data and submission documentation; no full experimental audit
  Locations: Abstract; Official data documentation.
  Qualification: Designated unlabeled adaptation before final evaluation differs from adapting on test inputs.
  [Dated ledger](../../notes/review-refresh-2026-10-26/benchmarks-sources.json).

### Other stored metadata

```json
{
  "verified_on": "2026-10-26"
}
```


## Sakaridis2021ACDC

**ACDC: The Adverse Conditions Dataset With Correspondences for Semantic Driving Scene Understanding**

Authors: Christos Sakaridis; Dengxin Dai; Luc Van Gool.

Publication: 2021; ICCV 2021, pages10765-10775.

Primary source: [ACDC: The Adverse Conditions Dataset With Correspondences for Semantic Driving Scene Understanding](https://openaccess.thecvf.com/content/ICCV2021/html/Sakaridis_ACDC_The_Adverse_Conditions_Dataset_With_Correspondences_for_Semantic_Driving_ICCV_2021_paper.html). [Project paper note](../../papers/Sakaridis2021ACDC.md).

Publication qualification: Official ICCV2021 verified

Recorded reading scope: Official proceedings metadata/abstract and author dataset overview

Inspected locations: Abstract; Dataset overview and splits.

Relevance / overlap from our reading: Real fog/night/rain/snow driving scenes and normal correspondences; dense prediction extension beyond artificial corruptions.

Limitation / reviewer boundary: Later TPAMI extension has revised title, additional authors/annotations; do not silently merge versions or use panoptic metrics as semantic mIoU.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

[Source ledger](../../notes/review-refresh-2026-10-26/benchmarks-sources.json).

### Recorded reading history

- **2026-10-26**: Official proceedings metadata/abstract and author dataset overview
  Locations: Abstract; Dataset overview and splits.
  Qualification: Later TPAMI extension has revised title, additional authors/annotations; do not silently merge versions or use panoptic metrics as semantic mIoU.
  [Dated ledger](../../notes/review-refresh-2026-10-26/benchmarks-sources.json).

### Other stored metadata

```json
{
  "verified_on": "2026-10-26",
  "project_url": "https://acdc.vision.ee.ethz.ch/"
}
```


## Wang2021Tent

**Tent: Fully Test-Time Adaptation by Entropy Minimization**

Authors: Dequan Wang; Evan Shelhamer; Shaoteng Liu; Bruno Olshausen; Trevor Darrell.

Publication: 2021; ICLR.

Primary source: [Tent: Fully Test-Time Adaptation by Entropy Minimization](https://arxiv.org/abs/2006.10726). [Project paper note](../../papers/Wang2021Tent.md).

Publication qualification: conference paper; preprint first posted 2020

Recorded reading scope: abstract, conference PDF first page and method overview

Inspected locations: Abstract; Introduction.

Relevance / overlap from our reading: Updates normalization statistics and affine transformations with entropy minimization on unlabeled test batches.

Limitation / reviewer boundary: A low-entropy objective is not direct evidence of correctness; no whole-policy selector in the inspected passages.

Recorded implementation/author resource: [link](https://github.com/DequanWang/tent). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/shift-aware-tta-review-verifier-sources.json).

### Other stored metadata

```json
{
  "pdf_url": "https://openreview.net/pdf/4de0af9691a5dcc52de7de756676fded33d037ef.pdf"
}
```


## Boudiaf2022LAME

**Parameter-Free Online Test-Time Adaptation**

Authors: Malik Boudiaf; Romain Mueller; Ismail Ben Ayed; Luca Bertinetto.

Publication: 2022; CVPR 2022, pages 8344–8353.

Primary source: [Parameter-Free Online Test-Time Adaptation](https://openaccess.thecvf.com/content/CVPR2022/html/Boudiaf_Parameter-Free_Online_Test-Time_Adaptation_CVPR_2022_paper.html). [Project paper note](../../papers/Boudiaf2022LAME.md).

Publication qualification: Official CVPR proceedings and author repository verified.

Recorded reading scope: Official abstract/metadata and PDF objective/cross-shift validation passages.

Inspected locations: Abstract; Equation 3; Figure 3.

Relevance / overlap from our reading: Conservative graph-regularized output correction with frozen model parameters; already studies failure of scenario-specific tuning across shifts.

Limitation / reviewer boundary: Our interpretation: graph quality and the number/composition of simultaneously available samples limit refinement. Parameter-free does not mean hyperparameter-free.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

Recorded implementation/author resource: [link](https://github.com/fiveai/LAME). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/review-refresh-2026-10-26/lead-sources.json).

### Recorded reading history

- **2026-10-26**: Official abstract/metadata and PDF objective/cross-shift validation passages.
  Locations: Abstract; Equation 3; Figure 3.
  Qualification: Our interpretation: graph quality and the number/composition of simultaneously available samples limit refinement. Parameter-free does not mean hyperparameter-free.
  [Dated ledger](../../notes/review-refresh-2026-10-26/lead-sources.json).

### Other stored metadata

```json
{
  "entry_type": "inproceedings"
}
```


## Gandelsman2022TTTMAE

**Test-Time Training with Masked Autoencoders**

Authors: Yossi Gandelsman; Yu Sun; Xinlei Chen; Alexei Efros.

Publication: 2022; NeurIPS 2022, Advances in Neural Information Processing Systems 35.

Primary source: [Test-Time Training with Masked Autoencoders](https://proceedings.neurips.cc/paper_files/paper/2022/hash/bcdec1c2d60f94a93b6e36f937aa0530-Abstract-Conference.html). [Project paper note](../../papers/Gandelsman2022TTTMAE.md).

Verified DOI in saved record: `10.52202/068431-2130`.

Publication qualification: Official NeurIPS proceedings verified.

Recorded reading scope: Official abstract, metadata, PDF introduction and source repository overview.

Inspected locations: Abstract; Introduction.

Relevance / overlap from our reading: Single-sample reconstruction-based adaptation supplies a self-supervised alternative to confidence minimization.

Limitation / reviewer boundary: Requires a reconstruction-compatible source setup. Our interpretation: reconstruction quality and classification utility can diverge; runtime includes repeated adaptation.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

Recorded implementation/author resource: [link](https://github.com/yossigandelsman/test_time_training_mae). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/review-refresh-2026-10-26/lead-sources.json).

### Recorded reading history

- **2026-10-26**: Official abstract, metadata, PDF introduction and source repository overview.
  Locations: Abstract; Introduction.
  Qualification: Requires a reconstruction-compatible source setup. Our interpretation: reconstruction quality and classification utility can diverge; runtime includes repeated adaptation.
  [Dated ledger](../../notes/review-refresh-2026-10-26/lead-sources.json).

### Other stored metadata

```json
{
  "entry_type": "inproceedings"
}
```


## Garg2022ATC

**Leveraging Unlabeled Data to Predict Out-of-Distribution Performance**

Authors: Saurabh Garg; Sivaraman Balakrishnan; Zachary C. Lipton; Behnam Neyshabur; Hanie Sedghi.

Publication: 2022; International Conference on Learning Representations.

Primary source: [Leveraging Unlabeled Data to Predict Out-of-Distribution Performance](https://arxiv.org/abs/2201.04234). [Project paper note](../../papers/Garg2022ATC.md).

Publication qualification: ICLR 2022 official program listing and paper header verified; arXiv v3 revised 15 October 2022

Recorded reading scope: arXiv metadata/abstract; official ICLR Downloads listing; primary paper §3.1 and ATC discussion via author/institutional PDF. Partial reading.

Inspected locations: Section 3.1; ATC method and conclusion; ICLR official Downloads 2022.

Relevance / overlap from our reading: Source-calibrated confidence threshold estimates unlabeled target accuracy; impossibility result blocks arbitrary-shift accuracy identification.

Limitation / reviewer boundary: Requires labeled source validation; empirical target transfer of confidence/error relation is conditional and can fail. Accuracy estimation is distinct from selecting an intervention before adaptation.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

[Source ledger](../../notes/review-refresh-2026-10-26/verifier-sources.json).

### Recorded reading history

- **2026-10-26**: arXiv metadata/abstract; official ICLR Downloads listing; primary paper §3.1 and ATC discussion via author/institutional PDF. Partial reading.
  Locations: Section 3.1; ATC method and conclusion; ICLR official Downloads 2022.
  Qualification: Requires labeled source validation; empirical target transfer of confidence/error relation is conditional and can fail. Accuracy estimation is distinct from selecting an intervention before adaptation.
  [Dated ledger](../../notes/review-refresh-2026-10-26/verifier-sources.json).

### Other stored metadata

```json
{
  "pdf_url": "https://openreview.net/pdf?id=wcrff7Gh0RR",
  "accessed": "2026-10-26"
}
```


## Gong2022NOTE

**NOTE: Robust Continual Test-time Adaptation Against Temporal Correlation**

Authors: Taesik Gong; Jongheon Jeong; Taewon Kim; Yewon Kim; Jinwoo Shin; Sung-Ju Lee.

Publication: 2022; NeurIPS 35.

Primary source: [NOTE: Robust Continual Test-time Adaptation Against Temporal Correlation](https://papers.nips.cc/paper_files/paper/2022/hash/ae6c7dbd9429b3a75c41b5fb47e57c9e-Abstract-Conference.html). [Project paper note](../../papers/Gong2022NOTE.md).

Publication qualification: conference paper

Recorded reading scope: official metadata and abstract; author repository README

Inspected locations: Abstract.

Relevance / overlap from our reading: Instance-aware normalization and prediction-balanced reservoir sampling mitigate temporal correlation.

Limitation / reviewer boundary: An IID-only selector test would ignore a long-established threat.

Recorded implementation/author resource: [link](https://github.com/TaesikGong/NOTE). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/shift-aware-tta-review-verifier-sources.json).


## Kar2022ImageNet3DCC

**3D Common Corruptions for Object Recognition**

Authors: Oguzhan Fatih Kar; Teresa Yeo; Amir Zamir.

Publication: 2022; ICML 2022 Shift Happens workshop / benchmark report.

Primary source: [3D Common Corruptions for Object Recognition](https://openreview.net/pdf?id=Evar7nqAQtL). [Project paper note](../../papers/Kar2022ImageNet3DCC.md).

Publication qualification: 2022 benchmark report verified; workshop designation supported by linked project ecosystem, main-track not established

Recorded reading scope: Benchmark PDF title/authors, abstract and sections1-2; author project news and RobustBench link

Inspected locations: Abstract; Section2; Project May2022 news.

Relevance / overlap from our reading: ImageNet-3DCC12 corruptions, many incorporating inferred depth; useful held-out physical-transformation families.

Limitation / reviewer boundary: OpenReview HTML challenged; short paper generic ICML footer is not proof of main-track status; derived images share clean IDs with ImageNet-C.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

[Source ledger](../../notes/review-refresh-2026-10-26/benchmarks-sources.json).

### Recorded reading history

- **2026-10-26**: Benchmark PDF title/authors, abstract and sections1-2; author project news and RobustBench link
  Locations: Abstract; Section2; Project May2022 news.
  Qualification: OpenReview HTML challenged; short paper generic ICML footer is not proof of main-track status; derived images share clean IDs with ImageNet-C.
  [Dated ledger](../../notes/review-refresh-2026-10-26/benchmarks-sources.json).

### Other stored metadata

```json
{
  "verified_on": "2026-10-26",
  "project_url": "https://3dcommoncorruptions.epfl.ch/"
}
```


## Mirza2022DUA

**The Norm Must Go On: Dynamic Unsupervised Domain Adaptation by Normalization**

Authors: M. Jehanzeb Mirza; Jakub Micorek; Horst Possegger; Horst Bischof.

Publication: 2022; CVPR 2022, pages 14765–14775.

Primary source: [The Norm Must Go On: Dynamic Unsupervised Domain Adaptation by Normalization](https://openaccess.thecvf.com/content/CVPR2022/html/Mirza_The_Norm_Must_Go_On_Dynamic_Unsupervised_Domain_Adaptation_by_CVPR_2022_paper.html). [Project paper note](../../papers/Mirza2022DUA.md).

Publication qualification: Official CVPR proceedings verified; related 2021 preprint linked work.

Recorded reading scope: Official metadata/abstract and PDF first-page adaptive-momentum description.

Inspected locations: Abstract; Figure 1.

Relevance / overlap from our reading: Continuously updates BN statistics with adaptive momentum from limited unlabeled data; dynamic statistics control predates the proposed router.

Limitation / reviewer boundary: BN-dependent; our interpretation is that statistics updates cannot recover arbitrary lost semantic features and can mix incompatible stream conditions.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

[Source ledger](../../notes/review-refresh-2026-10-26/lead-sources.json).

### Recorded reading history

- **2026-10-26**: Official metadata/abstract and PDF first-page adaptive-momentum description.
  Locations: Abstract; Figure 1.
  Qualification: BN-dependent; our interpretation is that statistics updates cannot recover arbitrary lost semantic features and can mix incompatible stream conditions.
  [Dated ledger](../../notes/review-refresh-2026-10-26/lead-sources.json).

### Other stored metadata

```json
{
  "entry_type": "inproceedings"
}
```


## Niu2022EATA

**Efficient Test-Time Model Adaptation without Forgetting**

Authors: Shuaicheng Niu; Jiaxiang Wu; Yifan Zhang; Yaofo Chen; Shijian Zheng; Peilin Zhao; Mingkui Tan.

Publication: 2022; ICML, PMLR 162:16888–16905.

Primary source: [Efficient Test-Time Model Adaptation without Forgetting](https://proceedings.mlr.press/v162/niu22a.html). [Project paper note](../../papers/Niu2022EATA.md).

Publication qualification: conference paper

Recorded reading scope: official metadata, abstract and PDF first-page methodological introduction

Inspected locations: Abstract; Section 1.

Relevance / overlap from our reading: Filters reliable/nonredundant samples for entropy updates and regularizes important parameters against forgetting.

Limitation / reviewer boundary: Selective sample updates and compute reduction already exist; selecting entire adaptation methods is a different variable.

Recorded implementation/author resource: [link](https://github.com/mr-eggplant/EATA). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/shift-aware-tta-review-verifier-sources.json).

### Other stored metadata

```json
{
  "pdf_url": "https://proceedings.mlr.press/v162/niu22a/niu22a.pdf"
}
```


## Shu2022TPT

**Test-Time Prompt Tuning for Zero-Shot Generalization in Vision-Language Models**

Authors: Manli Shu; Weili Nie; De-An Huang; Zhiding Yu; Tom Goldstein; Anima Anandkumar; Chaowei Xiao.

Publication: 2022; NeurIPS 2022, Advances in Neural Information Processing Systems 35.

Primary source: [Test-Time Prompt Tuning for Zero-Shot Generalization in Vision-Language Models](https://proceedings.neurips.cc/paper_files/paper/2022/hash/5bf2b802e24106064dc547ae9283bb0c-Abstract-Conference.html). [Project paper note](../../papers/Shu2022TPT.md).

Verified DOI in saved record: `10.52202/068431-1038`.

Publication qualification: Official NeurIPS proceedings verified.

Recorded reading scope: Official proceedings abstract/metadata and repository setting descriptions.

Inspected locations: Abstract; Repository overview.

Relevance / overlap from our reading: Optimizes text prompts on confidence-selected augmented views of a single test image for CLIP zero-shot classification.

Limitation / reviewer boundary: VLM setup and multiple views differ from CNN BN adaptation; source/pretrained prompt initialization and adaptation latency must be declared.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

Recorded implementation/author resource: [link](https://github.com/azshue/tpt). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/review-refresh-2026-10-26/lead-sources.json).

### Recorded reading history

- **2026-10-26**: Official proceedings abstract/metadata and repository setting descriptions.
  Locations: Abstract; Repository overview.
  Qualification: VLM setup and multiple views differ from CNN BN adaptation; source/pretrained prompt initialization and adaptation latency must be declared.
  [Dated ledger](../../notes/review-refresh-2026-10-26/lead-sources.json).

### Other stored metadata

```json
{
  "entry_type": "inproceedings"
}
```


## Wang2022CoTTA

**Continual Test-Time Domain Adaptation**

Authors: Qin Wang; Olga Fink; Luc Van Gool; Dengxin Dai.

Publication: 2022; CVPR.

Primary source: [Continual Test-Time Domain Adaptation](https://openaccess.thecvf.com/content/CVPR2022/html/Wang_Continual_Test-Time_Domain_Adaptation_CVPR_2022_paper.html). [Project paper note](../../papers/Wang2022CoTTA.md).

Publication qualification: conference paper

Recorded reading scope: official metadata, abstract, first-page introduction and author README

Inspected locations: Abstract; Introduction, Figure 1.

Relevance / overlap from our reading: Weight/augmentation averaging and stochastic restoration maintain continual adaptation state.

Limitation / reviewer boundary: Mechanisms already address nonstationary adaptation and forgetting; not a guarantee of safe policy selection.

Recorded implementation/author resource: [link](https://github.com/qinenergy/cotta). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/shift-aware-tta-review-verifier-sources.json).

### Other stored metadata

```json
{
  "pdf_url": "https://openaccess.thecvf.com/content/CVPR2022/papers/Wang_Continual_Test-Time_Domain_Adaptation_CVPR_2022_paper.pdf"
}
```


## Zhang2022MEMO

**MEMO: Test Time Robustness via Adaptation and Augmentation**

Authors: Marvin Zhang; Sergey Levine; Chelsea Finn.

Publication: 2022; NeurIPS 2022, Advances in Neural Information Processing Systems 35.

Primary source: [MEMO: Test Time Robustness via Adaptation and Augmentation](https://papers.neurips.cc/paper_files/paper/2022/hash/fc28053a08f59fccb48b11f2e31e81c7-Abstract-Conference.html). [Project paper note](../../papers/Zhang2022MEMO.md).

Verified DOI in saved record: `10.52202/068431-2799`.

Publication qualification: Official NeurIPS proceedings verified.

Recorded reading scope: Official metadata/abstract and PDF introductory method description.

Inspected locations: Abstract; Introduction.

Relevance / overlap from our reading: Minimizes entropy of predictions averaged over augmented views of one input; removes a multi-input batch requirement.

Limitation / reviewer boundary: Our interpretation: multiple views and adaptation cost must be charged; the chosen transformations encode invariance assumptions that can fail under severe shifts.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

[Source ledger](../../notes/review-refresh-2026-10-26/lead-sources.json).

### Recorded reading history

- **2026-10-26**: Official metadata/abstract and PDF introductory method description.
  Locations: Abstract; Introduction.
  Qualification: Our interpretation: multiple views and adaptation cost must be charged; the chosen transformations encode invariance assumptions that can fail under severe shifts.
  [Dated ledger](../../notes/review-refresh-2026-10-26/lead-sources.json).

### Other stored metadata

```json
{
  "entry_type": "inproceedings"
}
```


## Dobler2023RMT

**Robust Mean Teacher for Continual and Gradual Test-Time Adaptation**

Authors: Mario Döbler; Robert A. Marsden; Bin Yang.

Publication: 2023; CVPR 2023, pages 7704–7714.

Primary source: [Robust Mean Teacher for Continual and Gradual Test-Time Adaptation](https://openaccess.thecvf.com/content/CVPR2023/html/Dobler_Robust_Mean_Teacher_for_Continual_and_Gradual_Test-Time_Adaptation_CVPR_2023_paper.html). [Project paper note](../../papers/Dobler2023RMT.md).

Publication qualification: Official CVPR proceedings verified.

Recorded reading scope: Official metadata, abstract and PDF introduction describing source-free/source-data variants and DomainNet-126.

Inspected locations: Abstract; Introduction.

Relevance / overlap from our reading: Symmetric consistency loss and source-anchored contrastive adaptation for continual/gradual shifts; establishes continual DomainNet-126 protocol.

Limitation / reviewer boundary: Source-access and source-free variants differ; teachers, augmentation and contrastive computation must be charged. Our interpretation: pseudo-label error remains a constraint.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

Recorded implementation/author resource: [link](https://github.com/mariodoebler/test-time-adaptation). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/review-refresh-2026-10-26/lead-sources.json).

### Recorded reading history

- **2026-10-26**: Official metadata, abstract and PDF introduction describing source-free/source-data variants and DomainNet-126.
  Locations: Abstract; Introduction.
  Qualification: Source-access and source-free variants differ; teachers, augmentation and contrastive computation must be charged. Our interpretation: pseudo-label error remains a constraint.
  [Dated ledger](../../notes/review-refresh-2026-10-26/lead-sources.json).

### Other stored metadata

```json
{
  "entry_type": "inproceedings"
}
```


## Lim2023TTN

**TTN: A Domain-Shift Aware Batch Normalization in Test-Time Adaptation**

Authors: Hyesu Lim; Byeonggeun Kim; Jaegul Choo; Sungha Choi.

Publication: 2023; ICLR 2023.

Primary source: [TTN: A Domain-Shift Aware Batch Normalization in Test-Time Adaptation](https://arxiv.org/abs/2302.05155). [Project paper note](../../papers/Lim2023TTN.md).

Publication qualification: Conference paper; arXiv 2302.05155

Recorded reading scope: Abstract and author project-page sections on layer/channel shift sensitivity and post-training.

Inspected locations: Method: Test-Time Normalization Layer; Post-training prior; Optimize interpolating weights.

Relevance / overlap from our reading: Combines source and current-batch normalization using layer/channel shift sensitivity; shifts alter appropriate reliance on source/test statistics.

Limitation / reviewer boundary: Interpolation weights are learned using labeled source data during post-training and frozen at deployment. Do not conflate this with label-free source preparation or whole-method routing.

[Source ledger](../../notes/shift-aware-tta-review-researcher-sources.json).

### Other stored metadata

```json
{
  "pdf_url": "https://openreview.net/pdf?id=EQfeudmWLQ"
}
```


## Niu2023SAR

**Towards Stable Test-Time Adaptation in Dynamic Wild World**

Authors: Shuaicheng Niu; Jiaxiang Wu; Yifan Zhang; Zhiquan Wen; Yaofo Chen; Peilin Zhao; Mingkui Tan.

Publication: 2023; ICLR.

Primary source: [Towards Stable Test-Time Adaptation in Dynamic Wild World](https://arxiv.org/abs/2302.12400). [Project paper note](../../papers/Niu2023SAR.md).

Publication qualification: conference paper

Recorded reading scope: abstract and conference PDF first-page description

Inspected locations: Abstract.

Relevance / overlap from our reading: Reliable entropy minimization and sharpness-aware updates target instability under small batches, mixed shifts and imbalance.

Limitation / reviewer boundary: Those deployment challenges are established, not a new gap; specific new policies must beat robust existing updates.

[Source ledger](../../notes/shift-aware-tta-review-verifier-sources.json).

### Other stored metadata

```json
{
  "pdf_url": "https://openreview.net/pdf?id=g2YraF75Tj"
}
```


## Park2023LSA

**Label Shift Adapter for Test-Time Adaptation under Covariate and Label Shifts**

Authors: Sunghyun Park; Seunghan Yang; Jaegul Choo; Sungrack Yun.

Publication: 2023; Proceedings of the IEEE/CVF International Conference on Computer Vision, pages 16375-16385.

Primary source: [Label Shift Adapter for Test-Time Adaptation under Covariate and Label Shifts](https://arxiv.org/abs/2308.08810). [Project paper note](../../papers/Park2023LSA.md).

Publication qualification: ICCV 2023 official paper; linked arXiv preprint 2308.08810

Recorded reading scope: arXiv title/authors/abstract; official CVF PDF §5 and conclusion visible in primary index; partial reading.

Inspected locations: Abstract; Section 5 Discussions; Section 6 Conclusion.

Relevance / overlap from our reading: Estimates target label distribution and generates adaptation parameters conditional on it, integrating with existing TTA objectives.

Limitation / reviewer boundary: Additional source-stage adapter training; paper notes normalization hyperparameter sensitivity. Source and target imbalance adaptation already part of scope.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

[Source ledger](../../notes/review-refresh-2026-10-26/verifier-sources.json).

### Recorded reading history

- **2026-10-26**: Fresh arXiv metadata/abstract; official CVF page inaccessible.
  Locations: Abstract; arXiv comments.
  Qualification: Prior-estimation error can matter; exact assumptions/preparation and empirical robustness need full-method audit. Generic shift-conditioned parameter production is covered.
  [Dated ledger](../../notes/review-refresh-2026-10-26/researcher-sources.json).

- **2026-10-26**: arXiv title/authors/abstract; official CVF PDF §5 and conclusion visible in primary index; partial reading.
  Locations: Abstract; Section 5 Discussions; Section 6 Conclusion.
  Qualification: Additional source-stage adapter training; paper notes normalization hyperparameter sensitivity. Source and target imbalance adaptation already part of scope.
  [Dated ledger](../../notes/review-refresh-2026-10-26/verifier-sources.json).

### Other stored metadata

```json
{
  "pdf_url": "https://openaccess.thecvf.com/content/ICCV2023/papers/Park_Label_Shift_Adapter_for_Test-Time_Adaptation_under_Covariate_and_Label_ICCV_2023_paper.pdf",
  "accessed": "2026-10-26"
}
```


## Press2023RDumb

**RDumb: A simple approach that questions our progress in continual test-time adaptation**

Authors: Ori Press; Steffen Schneider; Matthias Kümmerer; Matthias Bethge.

Publication: 2023; NeurIPS 2023, Advances in Neural Information Processing Systems 36.

Primary source: [RDumb: A simple approach that questions our progress in continual test-time adaptation](https://papers.neurips.cc/paper_files/paper/2023/hash/7d640f377893fc5f22b5610e175ef7c3-Abstract-Conference.html). [Project paper note](../../papers/Press2023RDumb.md).

Verified DOI in saved record: `10.52202/075280-1735`.

Publication qualification: Official NeurIPS proceedings verified.

Recorded reading scope: Official metadata/abstract and selected PDF collapse/toy-model appendix passages.

Inspected locations: Abstract; Figure 8; Appendix toy-model analysis.

Relevance / overlap from our reading: Introduces CCC long streams and a periodic-reset baseline that challenges apparent continual-adaptation gains.

Limitation / reviewer boundary: Our interpretation: fixed resets discard useful state and introduce a schedule, but sophisticated controllers must first beat this inexpensive comparator.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

[Source ledger](../../notes/review-refresh-2026-10-26/lead-sources.json).

### Recorded reading history

- **2026-10-26**: Official metadata/abstract and selected PDF collapse/toy-model appendix passages.
  Locations: Abstract; Figure 8; Appendix toy-model analysis.
  Qualification: Our interpretation: fixed resets discard useful state and introduce a schedule, but sophisticated controllers must first beat this inexpensive comparator.
  [Dated ledger](../../notes/review-refresh-2026-10-26/lead-sources.json).

### Other stored metadata

```json
{
  "entry_type": "inproceedings"
}
```


## Sun2023TTLSA

**Beyond Invariance: Test-Time Label-Shift Adaptation for Addressing "Spurious" Correlations**

Authors: Qingyao Sun; Kevin P. Murphy; Sayna Ebrahimi; Alexander D'Amour.

Publication: 2023; Advances in Neural Information Processing Systems 36.

Primary source: [Beyond Invariance: Test-Time Label-Shift Adaptation for Addressing "Spurious" Correlations](https://papers.nips.cc/paper/2023/hash/4b0c1645f3d6a1730931e65ecbf91ac3-Abstract-Conference.html). [Project paper note](../../papers/Sun2023TTLSA.md).

Verified DOI in saved record: `10.52202/075280-1033`.

Publication qualification: NeurIPS 2023 main conference proceedings verified

Recorded reading scope: Official NeurIPS metadata and abstract; not a full-method read.

Inspected locations: Abstract; Official DOI.

Relevance / overlap from our reading: Uses unlabeled EM to adapt joint class/nuisance priors through a discriminative source model.

Limitation / reviewer boundary: Source group metadata and invariant p(x|y,z) assumption; not arbitrary causal shift identification or generic weights-only TTA.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

Recorded implementation/author resource: [link](https://github.com/nalzok/test-time-label-shift). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/review-refresh-2026-10-26/verifier-sources.json).

### Recorded reading history

- **2026-10-26**: Official NeurIPS metadata and abstract; not a full-method read.
  Locations: Abstract; Official DOI.
  Qualification: Source group metadata and invariant p(x|y,z) assumption; not arbitrary causal shift identification or generic weights-only TTA.
  [Dated ledger](../../notes/review-refresh-2026-10-26/verifier-sources.json).

### Other stored metadata

```json
{
  "accessed": "2026-10-26"
}
```


## Yeo2023RNA

**Rapid Network Adaptation: Learning to Adapt Neural Networks Using Test-Time Feedback**

Authors: Teresa Yeo; Oğuzhan Fatih Kar; Zahra Sodagar; Amir Zamir.

Publication: 2023; ICCV 2023.

Primary source: [Rapid Network Adaptation: Learning to Adapt Neural Networks Using Test-Time Feedback](https://openaccess.thecvf.com/content/ICCV2023/papers/Yeo_Rapid_Network_Adaptation_Learning_to_Adapt_Neural_Networks_Using_Test-Time_ICCV_2023_paper.pdf). [Project paper note](../../papers/Yeo2023RNA.md).

Publication qualification: Official ICCV PDF and author site verified; CVF HTML returned 403 during refresh.

Recorded reading scope: Indexed official CVF PDF title block/abstract/introduction and author project feedback descriptions; direct CVF fetch returned 403, full training rollouts not audited.

Inspected locations: Abstract; Figure 1; Author project Employed Test-time Adaptation Signals.

Relevance / overlap from our reading: Learns an amortized adaptation controller from error feedback; closed-loop learned updates and controller terminology are prior art.

Limitation / reviewer boundary: Classification examples use coarse/retrieval feedback from labeled training images; depth uses sparse geometric feedback. Not a weights-only unlabeled comparator. Exact training-state coverage remains to check; project code link is not verified RNA code.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

[Source ledger](../../notes/review-refresh-2026-10-26/lead-sources.json).

### Recorded reading history

- **2026-10-26**: Indexed official CVF PDF title block/abstract/introduction and author project adaptation-signal descriptions; full training rollouts not audited.
  Locations: Abstract; Figure 1; Author project Employed Test-time Adaptation Signals.
  Qualification: Classification examples use coarse/retrieval feedback from labeled training images; depth uses sparse geometric feedback. Not a weights-only unlabeled comparator. Exact training-state coverage remains to check; project code link is not verified RNA code.
  [Dated ledger](../../notes/review-refresh-2026-10-26/lead-sources.json).

### Other stored metadata

```json
{
  "entry_type": "inproceedings",
  "project_url": "https://rapid-network-adaptation.epfl.ch/"
}
```


## Yu2023BenchmarkTTA

**Benchmarking Test-Time Adaptation against Distribution Shifts in Image Classification**

Authors: Yongcan Yu; Lijun Sheng; Ran He; Jian Liang.

Publication: 2023; arXiv preprint.

Primary source: [Benchmarking Test-Time Adaptation against Distribution Shifts in Image Classification](https://arxiv.org/abs/2307.03133). [Project paper note](../../papers/Yu2023BenchmarkTTA.md).

Publication qualification: arXiv preprint 2307.03133; no later venue verified

Recorded reading scope: Primary metadata, abstract, author repository README; no full experiment audit

Inspected locations: Abstract; Repository README.

Relevance / overlap from our reading: Unified 13 methods/variants and online/offline, instance/batch/domain adaptation over CIFAR10/100-C, ImageNet-C, DomainNet, Office-Home.

Limitation / reviewer boundary: Version and access regimes must be matched; source does not establish 2026 leaderboard.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

Recorded implementation/author resource: [link](https://github.com/yuyongcan/Benchmark-TTA). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/review-refresh-2026-10-26/benchmarks-sources.json).

### Recorded reading history

- **2026-10-26**: Primary metadata, abstract, author repository README; no full experiment audit
  Locations: Abstract; Repository README.
  Qualification: Version and access regimes must be matched; source does not establish 2026 leaderboard.
  [Dated ledger](../../notes/review-refresh-2026-10-26/benchmarks-sources.json).

### Other stored metadata

```json
{
  "verified_on": "2026-10-26"
}
```


## Yuan2023RoTTA

**Robust Test-Time Adaptation in Dynamic Scenarios**

Authors: Longhui Yuan; Binhui Xie; Shuang Li.

Publication: 2023; CVPR, pp.15922–15932.

Primary source: [Robust Test-Time Adaptation in Dynamic Scenarios](https://openaccess.thecvf.com/content/CVPR2023/html/Yuan_Robust_Test-Time_Adaptation_in_Dynamic_Scenarios_CVPR_2023_paper.html). [Project paper note](../../papers/Yuan2023RoTTA.md).

Publication qualification: conference paper

Recorded reading scope: official metadata/abstract and introduction/method overview

Inspected locations: Section 1; Table 1; batch-size comparison passage.

Relevance / overlap from our reading: Robust normalization, balanced/timely memory and teacher-student updates jointly address changing domains and correlated sampling.

Limitation / reviewer boundary: Continual joint-stream realism is already studied; memory, teacher and update frequency must be included in fairness accounting.

Recorded implementation/author resource: [link](https://github.com/BIT-DA/RoTTA). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/shift-aware-tta-review-verifier-sources.json).

### Other stored metadata

```json
{
  "pdf_url": "https://openaccess.thecvf.com/content/CVPR2023/papers/Yuan_Robust_Test-Time_Adaptation_in_Dynamic_Scenarios_CVPR_2023_paper.pdf"
}
```


## Zhao2023DELTA

**DELTA: Degradation-Free Fully Test-Time Adaptation**

Authors: Bowen Zhao; Chen Chen; Shu-Tao Xia.

Publication: 2023; International Conference on Learning Representations.

Primary source: [DELTA: Degradation-Free Fully Test-Time Adaptation](https://arxiv.org/abs/2301.13018). [Project paper note](../../papers/Zhao2023DELTA.md).

Publication qualification: ICLR 2023 official listing and PDF header verified

Recorded reading scope: Official ICLR listing/paper header, arXiv metadata and HTML §§1, 3.1-3.3; partial reading.

Inspected locations: Section 3.1; Section 3.2; Section 3.3.

Relevance / overlap from our reading: Test-time batch renormalization and dynamic reweighting address correlated/imbalanced-stream moment errors and biased self-learning.

Limitation / reviewer boundary: Prediction-frequency estimates combine true class skew and model bias; its empirical degradation-free title is not an unrestricted safety guarantee. Full results not audited here.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

[Source ledger](../../notes/review-refresh-2026-10-26/verifier-sources.json).

### Recorded reading history

- **2026-10-26**: Fresh arXiv abstract and indexed official OpenReview PDF header; direct OpenReview browser challenge blocked full reading.
  Locations: Abstract; Official indexed PDF title/header.
  Qualification: Normalization/class-prior confounding is established; theoretical degradation-free wording is not a universal safety guarantee. Full method not audited.
  [Dated ledger](../../notes/review-refresh-2026-10-26/researcher-sources.json).

- **2026-10-26**: Official ICLR listing/paper header, arXiv metadata and HTML §§1, 3.1-3.3; partial reading.
  Locations: Section 3.1; Section 3.2; Section 3.3.
  Qualification: Prediction-frequency estimates combine true class skew and model bias; its empirical degradation-free title is not an unrestricted safety guarantee. Full results not audited here.
  [Dated ledger](../../notes/review-refresh-2026-10-26/verifier-sources.json).

### Other stored metadata

```json
{
  "openreview_url": "https://openreview.net/forum?id=eGm22rqG93",
  "html_url": "https://arxiv.org/html/2301.13018v1",
  "pdf_url": "https://openreview.net/pdf?id=eGm22rqG93",
  "accessed": "2026-10-26"
}
```


## Zhao2023Pitfalls

**On Pitfalls of Test-Time Adaptation**

Authors: Hao Zhao; Yuejiang Liu; Alexandre Alahi; Tao Lin.

Publication: 2023; ICML, PMLR 202:42058–42080.

Primary source: [On Pitfalls of Test-Time Adaptation](https://proceedings.mlr.press/v202/zhao23d.html). [Project paper note](../../papers/Zhao2023Pitfalls.md).

Publication qualification: conference paper

Recorded reading scope: Fresh official abstract and selective PDF sections1-2 plus implementation/protocol passages

Inspected locations: Abstract and sections1-2; repository.

Relevance / overlap from our reading: TTAB documents hyperparameter dependence, model-property effects and failure under difficult shifts.

Limitation / reviewer boundary: Even labeled oracle tuning has online batch-dependence complications; model-selection assumptions must be explicit.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

Recorded implementation/author resource: [link](https://github.com/LINs-lab/ttab). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/review-refresh-2026-10-26/benchmarks-sources.json).

### Recorded reading history

- **2026-10-23**: abstract, setting/model-selection discussion, label/temporal shift results and conclusion
  Locations: Sections 1, 3; Table 3; Section 7.
  Qualification: Even labeled oracle tuning has online batch-dependence complications; model-selection assumptions must be explicit.
  [Dated ledger](../../notes/shift-aware-tta-review-verifier-sources.json).

- **2026-10-26**: Fresh official abstract and selective PDF sections1-2 plus implementation/protocol passages
  Locations: Abstract and sections1-2; repository.
  Qualification: Official abstract nine vs PDF ten algorithms discrepancy retained; not substantive.
  [Dated ledger](../../notes/review-refresh-2026-10-26/benchmarks-sources.json).

### Other stored metadata

```json
{
  "pdf_url": "https://proceedings.mlr.press/v202/zhao23d/zhao23d.pdf",
  "refresh_read_scope": "Fresh official abstract and selective PDF sections1-2 plus implementation/protocol passages",
  "refresh_locations": "Abstract and sections1-2; repository",
  "refresh_limitation": "Official abstract nine vs PDF ten algorithms discrepancy retained; not substantive.",
  "verified_on": "2026-10-26"
}
```


## Alfarra2024TimeConstraints

**Evaluation of Test-Time Adaptation Under Computational Time Constraints**

Authors: Motasem Alfarra; Hani Itani; Alejandro Pardo; Shyma Yaser Alhuwaider; Merey Ramazanova; Juan Camilo Perez; Zhipeng Cai; Matthias Müller; Bernard Ghanem.

Publication: 2024; ICML 2024, PMLR 235:976-991.

Primary source: [Evaluation of Test-Time Adaptation Under Computational Time Constraints](https://proceedings.mlr.press/v235/alfarra24a.html). [Project paper note](../../papers/Alfarra2024TimeConstraints.md).

Publication qualification: Official ICML2024 proceedings verified; preprint began April2023

Recorded reading scope: Official proceedings abstract/metadata and original arXiv abstract; no full method audit

Inspected locations: Abstract; Official BibTeX.

Relevance / overlap from our reading: Already evaluates online adaptation using a constant-rate stream that reduces adaptation access for slower methods.

Limitation / reviewer boundary: Choice of arrival model matters; this protocol is not all possible latency-sensitive deployment.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

[Source ledger](../../notes/review-refresh-2026-10-26/benchmarks-sources.json).

### Recorded reading history

- **2026-10-26**: Official proceedings abstract/metadata and original arXiv abstract; no full method audit
  Locations: Abstract; Official BibTeX.
  Qualification: Choice of arrival model matters; this protocol is not all possible latency-sensitive deployment.
  [Dated ledger](../../notes/review-refresh-2026-10-26/benchmarks-sources.json).

### Other stored metadata

```json
{
  "verified_on": "2026-10-26",
  "preprint_url": "https://arxiv.org/abs/2304.04795"
}
```


## Bar2024ProtectedTTA

**Protected Test-Time Adaptation via Online Entropy Matching: A Betting Approach**

Authors: Yarin Bar; Shalev Shaer; Yaniv Romano.

Publication: 2024; NeurIPS 37.

Primary source: [Protected Test-Time Adaptation via Online Entropy Matching: A Betting Approach](https://proceedings.neurips.cc/paper_files/paper/2024/hash/9b35a0a20d617dc68ae98a7a57df2f51-Abstract-Conference.html). [Project paper note](../../papers/Bar2024ProtectedTTA.md).

Publication qualification: conference paper; inspected arXiv v1

Recorded reading scope: official metadata, abstract and arXiv method outline

Inspected locations: Section 3, POEM; Sections 3.3–3.5.

Relevance / overlap from our reading: Entropy-distribution shift detection dynamically drives an entropy-matching adaptation process.

Limitation / reviewer boundary: Shift-triggered adaptation and protecting in-distribution behavior already exist; statistical detector guarantees should not be restated as universal classification-safety guarantees.

[Source ledger](../../notes/shift-aware-tta-review-verifier-sources.json).

### Other stored metadata

```json
{
  "pdf_url": "https://openreview.net/pdf?id=qamfjyhPeg"
}
```


## Du2024UniTTA

**UniTTA: Unified Benchmark and Versatile Framework Towards Realistic Test-Time Adaptation**

Authors: Chaoqun Du; Yulin Wang; Jiayi Guo; Yizeng Han; Jie Zhou; Gao Huang.

Publication: 2024; arXiv preprint.

Primary source: [UniTTA: Unified Benchmark and Versatile Framework Towards Realistic Test-Time Adaptation](https://arxiv.org/abs/2407.20080). [Project paper note](../../papers/Du2024UniTTA.md).

Publication qualification: arXiv July2024; later venue not verified

Recorded reading scope: Abstract, sections3-5 and AppendixB selected passages, official README

Inspected locations: Section3; Section4; Section5; AppendixB; README sampler qualification.

Relevance / overlap from our reading: Markov domain/class correlation and imbalance;36 formal cases,24 evaluated; domain-class balanced statistics, dynamic domain expansion and correlated feature adaptation.

Limitation / reviewer boundary: Independent domain/class sampling is a modeled regime, not arbitrary real causal dependence. Repo warns optimized sampler may change published numbers.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

Recorded implementation/author resource: [link](https://github.com/LeapLabTHU/UniTTA). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/review-refresh-2026-10-26/benchmarks-sources.json).

### Recorded reading history

- **2026-10-26**: Abstract, sections3-5 and AppendixB selected passages, official README
  Locations: Section3; Section4; Section5; AppendixB; README sampler qualification.
  Qualification: Independent domain/class sampling is a modeled regime, not arbitrary real causal dependence. Repo warns optimized sampler may change published numbers.
  [Dated ledger](../../notes/review-refresh-2026-10-26/benchmarks-sources.json).

### Other stored metadata

```json
{
  "verified_on": "2026-10-26",
  "html_url": "https://arxiv.org/html/2407.20080v1"
}
```


## Gao2024UniEnt

**Unified Entropy Optimization for Open-Set Test-Time Adaptation**

Authors: Zhengqing Gao; Xu-Yao Zhang; Cheng-Lin Liu.

Publication: 2024; CVPR 2024, pages 23975–23984.

Primary source: [Unified Entropy Optimization for Open-Set Test-Time Adaptation](https://openaccess.thecvf.com/content/CVPR2024/html/Gao_Unified_Entropy_Optimization_for_Open-Set_Test-Time_Adaptation_CVPR_2024_paper.html). [Project paper note](../../papers/Gao2024UniEnt.md).

Publication qualification: Official CVPR proceedings verified.

Recorded reading scope: Official abstract/metadata and PDF first-page setup.

Inspected locations: Abstract; Introduction.

Relevance / overlap from our reading: Separates candidate known/unknown inputs and applies opposing entropy objectives; selecting an objective according to shift/sample type is established.

Limitation / reviewer boundary: Our interpretation: noisy unknown/known partitions can corrupt adaptation. Closed-set accuracy alone misses unknown detection failures; its open-set scope is separate.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

Recorded implementation/author resource: [link](https://github.com/gaozhengqing/UniEnt). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/review-refresh-2026-10-26/lead-sources.json).

### Recorded reading history

- **2026-10-26**: Official abstract/metadata and PDF first-page setup.
  Locations: Abstract; Introduction.
  Qualification: Our interpretation: noisy unknown/known partitions can corrupt adaptation. Closed-set accuracy alone misses unknown detection failures; its open-set scope is separate.
  [Dated ledger](../../notes/review-refresh-2026-10-26/lead-sources.json).

### Other stored metadata

```json
{
  "entry_type": "inproceedings"
}
```


## Karmanov2024TDA

**Efficient Test-Time Adaptation of Vision-Language Models**

Authors: Adilbek Karmanov; Dayan Guan; Shijian Lu; Abdulmotaleb El Saddik; Eric Xing.

Publication: 2024; CVPR 2024, pages 14162–14171.

Primary source: [Efficient Test-Time Adaptation of Vision-Language Models](https://openaccess.thecvf.com/content/CVPR2024/papers/Karmanov_Efficient_Test-Time_Adaptation_of_Vision-Language_Models_CVPR_2024_paper.pdf). [Project paper note](../../papers/Karmanov2024TDA.md).

Publication qualification: Official CVF PDF verified; HTML access returned 403.

Recorded reading scope: Official CVF PDF first page, efficiency/comparison passages and author repository.

Inspected locations: Abstract; Section 4.2; Tables 1–3.

Relevance / overlap from our reading: Dynamic positive/negative pseudo-label caches refine CLIP outputs without gradient updates; a useful inexpensive VLM reference.

Limitation / reviewer boundary: Our interpretation: caches depend on feature/pseudo-label quality and history. Backbone and natural-shift protocol must match; published timing is device-specific.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

Recorded implementation/author resource: [link](https://github.com/kdiAAA/TDA). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/review-refresh-2026-10-26/lead-sources.json).

### Recorded reading history

- **2026-10-26**: Official CVF PDF first page, efficiency/comparison passages and author repository.
  Locations: Abstract; Section 4.2; Tables 1–3.
  Qualification: Our interpretation: caches depend on feature/pseudo-label quality and history. Backbone and natural-shift protocol must match; published timing is device-specific.
  [Dated ledger](../../notes/review-refresh-2026-10-26/lead-sources.json).

### Other stored metadata

```json
{
  "entry_type": "inproceedings"
}
```


## Kim2024TTALine

**Test-Time Adaptation Induces Stronger Accuracy and Agreement-on-the-Line**

Authors: Eungyeup Kim; Mingjie Sun; Christina Baek; Aditi Raghunathan; J. Zico Kolter.

Publication: 2024; NeurIPS 37.

Primary source: [Test-Time Adaptation Induces Stronger Accuracy and Agreement-on-the-Line](https://arxiv.org/abs/2310.04941). [Project paper note](../../papers/Kim2024TTALine.md).

Publication qualification: conference paper; preprint first posted 2023

Recorded reading scope: abstract/introduction and Section 5.2 selection passages

Inspected locations: Section 5.2, Unsupervised validation for TTA; Extension to selecting best TTA strategy.

Relevance / overlap from our reading: Uses post-adaptation accuracy/agreement relationships for hyperparameter and TTA-strategy selection without OOD labels.

Limitation / reviewer boundary: Needs source/ID and multiple-model agreement evidence; observed linearity is not arbitrary-shift identifiability.

Recorded implementation/author resource: [link](https://github.com/EungyeupKim/TTALine). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/shift-aware-tta-review-verifier-sources.json).

### Other stored metadata

```json
{
  "pdf_url": "https://proceedings.neurips.cc/paper_files/paper/2024/file/d96fcc07d623a9eba68616629911143a-Paper-Conference.pdf"
}
```


## Lee2024AETTA

**AETTA: Label-Free Accuracy Estimation for Test-Time Adaptation**

Authors: Taeckyung Lee; Sorn Chottananurak; Taesik Gong; Sung-Ju Lee.

Publication: 2024; CVPR, pp.28643–28652.

Primary source: [AETTA: Label-Free Accuracy Estimation for Test-Time Adaptation](https://openaccess.thecvf.com/content/CVPR2024/html/Lee_AETTA_Label-Free_Accuracy_Estimation_for_Test-Time_Adaptation_CVPR_2024_paper.html). [Project paper note](../../papers/Lee2024AETTA.md).

Publication qualification: conference paper

Recorded reading scope: official abstract/metadata, indexed accuracy-estimation comparisons and supplemental model-recovery details

Inspected locations: Abstract; Accuracy Estimation Baselines/results, p.28648; Supplement D.4, Model Recovery Details.

Relevance / overlap from our reading: Uses dropout disagreement to estimate current adapted-model accuracy; demonstrates model recovery from estimated degradation.

Limitation / reviewer boundary: Already covers label-free recovery decisions, but dropout observations and estimator assumptions incur cost; does not establish pre-action benefit for every candidate.

Recorded implementation/author resource: [link](https://github.com/taeckyung/AETTA). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/shift-aware-tta-review-verifier-sources.json).

### Other stored metadata

```json
{
  "pdf_url": "https://openaccess.thecvf.com/content/CVPR2024/papers/Lee_AETTA_Label-Free_Accuracy_Estimation_for_Test-Time_Adaptation_CVPR_2024_paper.pdf"
}
```


## Lee2024BECoTTA

**BECoTTA: Input-dependent Online Blending of Experts for Continual Test-time Adaptation**

Authors: Daeun Lee; Jaehong Yoon; Sung Ju Hwang.

Publication: 2024; ICML 2024, PMLR 235:27072–27093.

Primary source: [BECoTTA: Input-dependent Online Blending of Experts for Continual Test-time Adaptation](https://proceedings.mlr.press/v235/lee24ab.html). [Project paper note](../../papers/Lee2024BECoTTA.md).

Publication qualification: Conference paper; arXiv v3 31 May 2024 inspected

Recorded reading scope: Abstract, introduction, method and benchmark design descriptions plus author project page.

Inspected locations: Section 3.2 Domain-Augmented Initialization; Section 3.3 MoDE; Section 3.4 CTTA process; Continual gradual shifts construction.

Relevance / overlap from our reading: Pseudo-domain inference routes inputs to low-rank experts; updates relevant experts and blends domain-adaptive knowledge.

Limitation / reviewer boundary: Expert routing is distinct from selecting complete standalone TTA methods. Initialization and source augmentation variants must be distinguished; gradual/mixed shifts alone are covered.

Recorded implementation/author resource: [link](https://github.com/daeunni/becotta). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/shift-aware-tta-review-researcher-sources.json).

### Other stored metadata

```json
{
  "pdf_url": "https://arxiv.org/pdf/2402.08712v3",
  "html_url": "https://arxiv.org/html/2402.08712v3"
}
```


## Lee2024DeYO

**Entropy is not Enough for Test-Time Adaptation: From the Perspective of Disentangled Factors**

Authors: Jonghyun Lee; Dahuin Jung; Saehyung Lee; Junsung Park; Juhyeon Shin; Uiwon Hwang; Sungroh Yoon.

Publication: 2024; ICLR 2024.

Primary source: [Entropy is not Enough for Test-Time Adaptation: From the Perspective of Disentangled Factors](https://arxiv.org/abs/2403.07366). [Project paper note](../../papers/Lee2024DeYO.md).

Publication qualification: Conference paper; linked arXiv first posted March 2024

Recorded reading scope: Primary arXiv abstract, official conference PDF first page and author repository README

Inspected locations: Abstract; Official implementation overview.

Relevance / overlap from our reading: Object-destructive transformations supply pseudo-label probability differences for sample selection and weighting alongside entropy.

Limitation / reviewer boundary: Perturbation-derived evidence and entropy unreliability already have a strong predecessor; native computation and biased-task assumptions must be preserved when used as a baseline.

Recorded implementation/author resource: [link](https://github.com/Jhyun17/DeYO). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/shift-aware-tta-review-lead-sources.json).


## Marsden2024ROID

**Universal Test-Time Adaptation Through Weight Ensembling, Diversity Weighting, and Prior Correction**

Authors: Robert A. Marsden; Mario Döbler; Bin Yang.

Publication: 2024; WACV 2024; official CVF page lists pages 2555–2565.

Primary source: [Universal Test-Time Adaptation Through Weight Ensembling, Diversity Weighting, and Prior Correction](https://openaccess.thecvf.com/content/WACV2024/html/Marsden_Universal_Test-Time_Adaptation_Through_Weight_Ensembling_Diversity_Weighting_and_Prior_WACV_2024_paper.html). [Project paper note](../../papers/Marsden2024ROID.md).

Publication qualification: Conference paper; primary CVF metadata used rather than inconsistent secondary pagination

Recorded reading scope: Official metadata/abstract and indexed method sections 4.1–4.3

Inspected locations: Abstract; Sections 4.1–4.3.

Relevance / overlap from our reading: Universal TTA covers nonstationarity, temporal correlation and priors using certainty/diversity weights, source averaging and prediction prior correction.

Limitation / reviewer boundary: A strong fixed-method comparison; these deployment factors alone do not establish a new selection problem.

Recorded implementation/author resource: [link](https://github.com/mariodoebler/test-time-adaptation). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/shift-aware-tta-review-lead-sources.json).


## Park2024LAW

**Layer-wise Auto-Weighting for Non-Stationary Test-Time Adaptation**

Authors: Junyoung Park; Jin Kim; Hyeongjun Kwon; Ilhoon Yoon; Kwanghoon Sohn.

Publication: 2024; Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision.

Primary source: [Layer-wise Auto-Weighting for Non-Stationary Test-Time Adaptation](https://github.com/junia3/LayerwiseTTA). [Project paper note](../../papers/Park2024LAW.md).

Publication qualification: WACV 2024 author repository citation; pages 1414–1423 reported there.

Recorded reading scope: Fresh author repository README and citation; official CVF page inaccessible.

Inspected locations: Author README experimental settings; Author README citation.

Relevance / overlap from our reading: Layer-wise adaptation is evaluated under episodic, continual and gradual regimes.

Limitation / reviewer boundary: Exact Fisher/weighting internals not newly audited; author repository is primary code evidence, not independent reproduction.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

Recorded implementation/author resource: [link](https://github.com/junia3/LayerwiseTTA). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/review-refresh-2026-10-26/researcher-sources.json).

### Recorded reading history

- **2026-10-26**: Fresh author repository README and citation; official CVF page inaccessible.
  Locations: Author README experimental settings; Author README citation.
  Qualification: Exact Fisher/weighting internals not newly audited; author repository is primary code evidence, not independent reproduction.
  [Dated ledger](../../notes/review-refresh-2026-10-26/researcher-sources.json).


## Su2024TRIBE

**Towards Real-World Test-Time Adaptation: Tri-Net Self-Training with Balanced Normalization**

Authors: Yongyi Su; Xun Xu; Kui Jia.

Publication: 2024; Proceedings of the AAAI Conference on Artificial Intelligence 38(13).

Primary source: [Towards Real-World Test-Time Adaptation: Tri-Net Self-Training with Balanced Normalization](https://ojs.aaai.org/index.php/AAAI/article/view/29435). [Project paper note](../../papers/Su2024TRIBE.md).

Verified DOI in saved record: `10.1609/aaai.v38i13.29435`.

Publication qualification: AAAI 2024 proceedings verified; linked arXiv v2 updated 26 March 2025

Recorded reading scope: Official AAAI metadata and abstract; arXiv v2 protocol and methodology sections inspected. Partial reading; version revised March 2025.

Inspected locations: Methodology: Real-World TTA Protocol; Balanced Batch Normalization; Tri-Net Self-Training; AAAI DOI.

Relevance / overlap from our reading: Combines global/local class imbalance and continual shifts; balances category-wise moments and anchors self-training.

Limitation / reviewer boundary: Predicted category estimates and teacher reliability remain consequential. Not a no-label guarantee of real class mixture or a pre-action whole-method selector.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

Recorded implementation/author resource: [link](https://github.com/Gorilla-Lab-SCUT/TRIBE). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/review-refresh-2026-10-26/verifier-sources.json).

### Recorded reading history

- **2026-10-26**: Fresh official AAAI abstract/citation and author repository README.
  Locations: Official abstract; Official citation; Author README.
  Qualification: Known class-mixture-aware adaptation baseline; tri-net storage and runtime need measurement. No new execution or full experiment audit.
  [Dated ledger](../../notes/review-refresh-2026-10-26/researcher-sources.json).

- **2026-10-26**: Official AAAI metadata and abstract; arXiv v2 protocol and methodology sections inspected. Partial reading; version revised March 2025.
  Locations: Methodology: Real-World TTA Protocol; Balanced Batch Normalization; Tri-Net Self-Training; AAAI DOI.
  Qualification: Predicted category estimates and teacher reliability remain consequential. Not a no-label guarantee of real class mixture or a pre-action whole-method selector.
  [Dated ledger](../../notes/review-refresh-2026-10-26/verifier-sources.json).

### Other stored metadata

```json
{
  "arxiv_url": "https://arxiv.org/abs/2309.14949",
  "html_url": "https://arxiv.org/html/2309.14949v2",
  "accessed": "2026-10-26"
}
```


## Bao2025Mint

**Mint: A Simple Test-Time Adaptation of Vision-Language Models against Common Corruptions**

Authors: Wenxuan Bao; Ruxi Deng; Jingrui He.

Publication: 2025; NeurIPS 2025, Advances in Neural Information Processing Systems 38.

Primary source: [Mint: A Simple Test-Time Adaptation of Vision-Language Models against Common Corruptions](https://proceedings.neurips.cc/paper_files/paper/2025/file/54df19dc823e2cacff6d26640bac6c10-Paper-Conference.pdf). [Project paper note](../../papers/Bao2025Mint.md).

Publication qualification: NeurIPS 2025 main proceedings PDF verified, beyond author-reported arXiv acceptance.

Recorded reading scope: Official proceedings PDF first page and primary arXiv abstract/metadata; partial reading.

Inspected locations: Abstract; Introduction.

Relevance / overlap from our reading: Targets corruption-related collapse of embedding variance by maximizing estimated inter-class variance using accumulators.

Limitation / reviewer boundary: Our interpretation: pseudo-label-based variance estimates can change with class priors; successful corruption adaptation does not establish arbitrary mixed-prior robustness.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

Recorded implementation/author resource: [link](https://github.com/baowenxuan/Mint). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/review-refresh-2026-10-26/lead-sources.json).

### Recorded reading history

- **2026-10-26**: Official proceedings PDF first page and primary arXiv abstract/metadata; partial reading.
  Locations: Abstract; Introduction.
  Qualification: Our interpretation: pseudo-label-based variance estimates can change with class priors; successful corruption adaptation does not establish arbitrary mixed-prior robustness.
  [Dated ledger](../../notes/review-refresh-2026-10-26/lead-sources.json).

### Other stored metadata

```json
{
  "entry_type": "inproceedings"
}
```


## Dai2025FreeTTA

**Free on the Fly: Enhancing Flexibility in Test-Time Adaptation with Online EM**

Authors: Qiyuan Dai; Sibei Yang.

Publication: 2025; CVPR 2025, pages 9538–9548.

Primary source: [Free on the Fly: Enhancing Flexibility in Test-Time Adaptation with Online EM](https://openaccess.thecvf.com/content/CVPR2025/html/Dai_Free_on_the_Fly_Enhancing_Flexibility_in_Test-Time_Adaptation_with_CVPR_2025_paper.html). [Project paper note](../../papers/Dai2025FreeTTA.md).

Publication qualification: Official CVPR 2025 proceedings verified; 2025 arXiv is linked version.

Recorded reading scope: Official abstract/metadata and PDF comparison passages only.

Inspected locations: Abstract; Comparison on cross-domain/OOD benchmarks.

Relevance / overlap from our reading: Models target distributions using online expectation-maximization and zero-shot VLM priors without retaining individual past test samples.

Limitation / reviewer boundary: The abstract's 'no assumptions' is author framing, not accepted literally here. Our interpretation: model family and pseudo-posterior assumptions still govern updates.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

[Source ledger](../../notes/review-refresh-2026-10-26/lead-sources.json).

### Recorded reading history

- **2026-10-26**: Official abstract/metadata and PDF comparison passages only.
  Locations: Abstract; Comparison on cross-domain/OOD benchmarks.
  Qualification: The abstract's 'no assumptions' is author framing, not accepted literally here. Our interpretation: model family and pseudo-posterior assumptions still govern updates.
  [Dated ledger](../../notes/review-refresh-2026-10-26/lead-sources.json).

### Other stored metadata

```json
{
  "entry_type": "inproceedings"
}
```


## Grover2025DynaTTA

**Shift-Aware Test Time Adaptation and Benchmarking for Time-Series Forecasting**

Authors: Shivam Grover; Ali Etemad.

Publication: 2025; ICML 2025 Workshop on Test-Time Adaptation: Putting Updates to the Test!.

Primary source: [Shift-Aware Test Time Adaptation and Benchmarking for Time-Series Forecasting](https://openreview.net/forum?id=a399SmgWGl). [Project paper note](../../papers/Grover2025DynaTTA.md).

Publication qualification: Workshop oral, not verified main-track ICML; official workshop list verifies acceptance

Recorded reading scope: Indexed primary PDF abstract/introduction excerpts, official workshop list and author talk summary.

Inspected locations: Abstract; Introduction dynamic rate and shift-conditioned gating; Official workshop acceptedpaper61.

Relevance / overlap from our reading: Prediction-error and embedding-drift signals control adaptation rate and reliance on adapted outputs, with synthetic shifted forecast benchmark.

Limitation / reviewer boundary: Forecasting can reveal past outcomes as future inputs; does not automatically satisfy strict label-free classification protocol.

Recorded implementation/author resource: [link](https://github.com/shivam-grover/DynaTTA). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/shift-aware-tta-review-researcher-sources.json).

### Other stored metadata

```json
{
  "pdf_url": "https://openreview.net/pdf?id=a399SmgWGl"
}
```


## Jang2025DART

**Label Distribution Shift-Aware Prediction Refinement for Test-Time Adaptation**

Authors: Minguk Jang; Hye Won Chung.

Publication: 2025; Transactions on Machine Learning Research.

Primary source: [Label Distribution Shift-Aware Prediction Refinement for Test-Time Adaptation](https://arxiv.org/abs/2411.15204). [Project paper note](../../papers/Jang2025DART.md).

Publication qualification: TMLR February 2025 shown in indexed official PDF header; arXiv v2, 5 February 2025.

Recorded reading scope: Fresh arXiv metadata/abstract and indexed primary OpenReview PDF section 3; direct PDF challenge blocked.

Inspected locations: Abstract; Section 3 indexed official PDF.

Relevance / overlap from our reading: A source-data-trained module uses batch prediction distribution/variance to correct class-wise confusion under label shift.

Limitation / reviewer boundary: Requires intermediate labeled-source preparation and transfer of learned confusion structure; full experiments not audited.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

[Source ledger](../../notes/review-refresh-2026-10-26/researcher-sources.json).

### Recorded reading history

- **2026-10-26**: Fresh arXiv metadata/abstract and indexed primary OpenReview PDF section 3; direct PDF challenge blocked.
  Locations: Abstract; Section 3 indexed official PDF.
  Qualification: Requires intermediate labeled-source preparation and transfer of learned confusion structure; full experiments not audited.
  [Dated ledger](../../notes/review-refresh-2026-10-26/researcher-sources.json).

### Other stored metadata

```json
{
  "openreview_url": "https://openreview.net/forum?id=c7AAHdEYz5"
}
```


## Liang2025TTASurvey

**A Comprehensive Survey on Test-Time Adaptation under Distribution Shifts**

Authors: Jian Liang; Ran He; Tieniu Tan.

Publication: 2025; International Journal of Computer Vision 133, 31–64; preprint first posted 2023.

Primary source: [A Comprehensive Survey on Test-Time Adaptation under Distribution Shifts](https://arxiv.org/abs/2303.15361). [Project paper note](../../papers/Liang2025TTASurvey.md).

Verified DOI in saved record: `10.1007/s11263-024-02181-w`.

Publication qualification: Journal article; linked preprint versions differ in date; publisher metadata checked: online 18 July 2024, volume year 2025

Recorded reading scope: Abstract and taxonomy description; not full survey

Inspected locations: Abstract; source linked in the online-TTA survey introduction.

Relevance / overlap from our reading: Taxonomy distinguishes batch, online and source-free adaptation settings.

Limitation / reviewer boundary: Orientation source; no novelty conclusion inferred from the abstract.

[Source ledger](../../notes/shift-aware-tta-review-lead-sources.json).


## Liu2025TACT

**Test-Time Adaptation by Causal Trimming**

Authors: Yingnan Liu; Rui Qiao; Mong-Li Lee; Wynne Hsu.

Publication: 2025; Advances in Neural Information Processing Systems 38.

Primary source: [Test-Time Adaptation by Causal Trimming](https://papers.neurips.cc/paper_files/paper/2025/hash/09d6e2295eb50b4cdcb45d75220a2598-Abstract-Conference.html). [Project paper note](../../papers/Liu2025TACT.md).

Verified DOI in saved record: `10.52202/085713-0227`.

Publication qualification: NeurIPS 2025 main proceedings verified

Recorded reading scope: Official metadata and author repository overview; arXiv methods/theoretical scope and conclusion, selected appendix directions. Partial reading.

Inspected locations: Sections 4-5; Section 7; Appendix C.

Relevance / overlap from our reading: Controlled augmentations, PCA nuisance directions, trimming representations and prototypes; a gradient-updating variant also described.

Limitation / reviewer boundary: Requires prior knowledge for causal-content-preserving augmentations; PCA separation assumptions and view generation cost. Sensitivity under a transform does not establish physical shift causality.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

Recorded implementation/author resource: [link](https://github.com/NancyQuris/TACT). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/review-refresh-2026-10-26/verifier-sources.json).

### Recorded reading history

- **2026-10-26**: Official metadata and author repository overview; arXiv methods/theoretical scope and conclusion, selected appendix directions. Partial reading.
  Locations: Sections 4-5; Section 7; Appendix C.
  Qualification: Requires prior knowledge for causal-content-preserving augmentations; PCA separation assumptions and view generation cost. Sensitivity under a transform does not establish physical shift causality.
  [Dated ledger](../../notes/review-refresh-2026-10-26/verifier-sources.json).

### Other stored metadata

```json
{
  "html_url": "https://arxiv.org/html/2510.11133v1",
  "accessed": "2026-10-26"
}
```


## Park2025HybridTTA

**Hybrid-TTA: Continual Test-time Adaptation via Dynamic Domain Shift Detection**

Authors: Hyewon Park; Hyejin Park; Jueun Ko; Dongbo Min.

Publication: 2025; ICCV 2025.

Primary source: [Hybrid-TTA: Continual Test-time Adaptation via Dynamic Domain Shift Detection](https://arxiv.org/html/2409.08566v2). [Project paper note](../../papers/Park2025HybridTTA.md).

Publication qualification: Conference paper; arXiv first September 2024, inspected v2 August 2025

Recorded reading scope: Fresh arXiv v2 HTML selective reading; primary arXiv metadata and official CVF search result checked.

Inspected locations: Sections 4.1.1–4.1.2; Section 4.2; Section 5.4.

Relevance / overlap from our reading: Evolving student/EMA-teacher discrepancy and dynamic threshold switch full versus adapter tuning.

Limitation / reviewer boundary: Already uses current/historical model state. No inspected same-current-data/different-history action-ranking experiment or learned per-action utility target.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

[Source ledger](../../notes/review-refresh-2026-10-26/researcher-sources.json).

### Recorded reading history

- **2026-10-23**: Abstract, introduction, section 4 mechanism and experiment/appendix headings; selected results, not exhaustive full paper.
  Locations: Section 4.1 Dynamic Domain Shift Detection; Section 4.2 Masked Image Modeling Adaptation; Section 5; Appendix source forgetting/long-term adaptation.
  Qualification: Segmentation-specific FT/ET menu and reconstruction preparation; not a general selector over arbitrary TTA algorithms. Still invalidates broad novelty of dynamic policy switching.
  [Dated ledger](../../notes/shift-aware-tta-review-researcher-sources.json).

- **2026-10-26**: Fresh arXiv v2 HTML selective reading; primary arXiv metadata and official CVF search result checked.
  Locations: Sections 4.1.1–4.1.2; Section 4.2; Section 5.4.
  Qualification: Already uses current/historical model state. No inspected same-current-data/different-history action-ranking experiment or learned per-action utility target.
  [Dated ledger](../../notes/review-refresh-2026-10-26/researcher-sources.json).

### Other stored metadata

```json
{
  "pdf_url": "https://openaccess.thecvf.com/content/ICCV2025/papers/Park_Hybrid-TTA_Continual_Test-time_Adaptation_via_Dynamic_Domain_Shift_Detection_ICCV_2025_paper.pdf",
  "html_url": "https://arxiv.org/html/2409.08566v2"
}
```


## Sahoo2025GALA

**A Layer Selection Approach to Test Time Adaptation**

Authors: Sabyasachi Sahoo; Mostafa ElAraby; Jonas Ngnawe; Yann Pequignot; Frederic Precioso; Christian Gagne.

Publication: 2025; AAAI 2025.

Primary source: [A Layer Selection Approach to Test Time Adaptation](https://arxiv.org/abs/2404.03784). [Project paper note](../../papers/Sahoo2025GALA.md).

Publication qualification: Accepted per arXiv record; firstpreprint April2024, v2 Feb2025 inspected

Recorded reading scope: Fresh arXiv HTML selective method and experiment reading.

Inspected locations: Sections 2.2–2.3; Section 3; Appendix A.5.

Relevance / overlap from our reading: Proposed-gradient alignment with accumulated displacement chooses layers or skips; periodic anchor resets allow trajectory changes.

Limitation / reviewer boundary: State/history-based parameter selection already exists; not an audited whole-policy value learner. Uses hyperparameter sweeps in inspected benchmark setup.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

[Source ledger](../../notes/review-refresh-2026-10-26/researcher-sources.json).

### Recorded reading history

- **2026-10-23**: Abstract, introduction, section2 description, discussion/appendix analysis of current gradients versus accumulated state.
  Locations: Section 2.1 layer selection; Section 2.2 cosine criterion; Section 2.3 reset; Appendix A.5.4 alignment vs magnitude.
  Qualification: Selecting update layers is not arbitrary whole-method selection, but state/drift/gradient features and skip/reset are established; cannot sell these alone as a gap.
  [Dated ledger](../../notes/shift-aware-tta-review-researcher-sources.json).

- **2026-10-26**: Fresh arXiv HTML selective method and experiment reading.
  Locations: Sections 2.2–2.3; Section 3; Appendix A.5.
  Qualification: State/history-based parameter selection already exists; not an audited whole-policy value learner. Uses hyperparameter sweeps in inspected benchmark setup.
  [Dated ledger](../../notes/review-refresh-2026-10-26/researcher-sources.json).

### Other stored metadata

```json
{
  "pdf_url": "https://arxiv.org/pdf/2404.03784v2",
  "html_url": "https://arxiv.org/html/2404.03784v2"
}
```


## Schirmer2025Monitoring

**Monitoring Risks in Test-Time Adaptation**

Authors: Mona Schirmer; Metod Jazbec; Christian Andersson Naesseth; Eric Nalisnick.

Publication: 2025; NeurIPS 2025, Advances in Neural Information Processing Systems 38.

Primary source: [Monitoring Risks in Test-Time Adaptation](https://proceedings.neurips.cc/paper_files/paper/2025/hash/746960ad49ddb47248970a0e1404230c-Abstract-Conference.html). [Project paper note](../../papers/Schirmer2025Monitoring.md).

Verified DOI in saved record: `10.52202/085713-2705`.

Publication qualification: NeurIPS 2025 main conference verified; earlier workshop versions must not be confused with full version

Recorded reading scope: Official NeurIPS metadata; arXiv v2 Assumption1, Proposition1, §§5.2-5.4, §6 and AppendixA.5. Partial reading.

Inspected locations: Assumption 1; Proposition 1; Section 5.4; Section 6; Appendix A.5.

Relevance / overlap from our reading: Label-free sequential risk lower bounds for adapting models, conditional on calibrated proxy informativeness; alternative proxies and explicit prior-shift experiment.

Limitation / reviewer boundary: Assumption verification needs target labels. A lower risk bound crossing detects excess risk; staying below threshold does not certify safety. Paper explicitly leaves unlabeled assumption diagnostics open.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

Recorded implementation/author resource: [link](https://github.com/monasch/tta-monitor). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/review-refresh-2026-10-26/verifier-sources.json).

### Recorded reading history

- **2026-10-23**: Sections 2–3, experiments, conclusion/limitations, selected appendices
  Locations: Section 3.2, Assumption 1; Section 3.4; Section 6, Limitations and Future Work; Appendix A.4.
  Qualification: Proxy-informativeness assumption needs labeled data to verify; unsupervised diagnostics for its violation and reducing monitoring delay/cost remain open.
  [Dated ledger](../../notes/shift-aware-tta-review-verifier-sources.json).

- **2026-10-26**: Official NeurIPS metadata; arXiv v2 Assumption1, Proposition1, §§5.2-5.4, §6 and AppendixA.5. Partial reading.
  Locations: Assumption 1; Proposition 1; Section 5.4; Section 6; Appendix A.5.
  Qualification: Assumption verification needs target labels. A lower risk bound crossing detects excess risk; staying below threshold does not certify safety. Paper explicitly leaves unlabeled assumption diagnostics open.
  [Dated ledger](../../notes/review-refresh-2026-10-26/verifier-sources.json).

### Other stored metadata

```json
{
  "pdf_url": "https://proceedings.neurips.cc/paper_files/paper/2025/file/746960ad49ddb47248970a0e1404230c-Paper-Conference.pdf",
  "html_url": "https://arxiv.org/html/2507.08721v2",
  "accessed": "2026-10-26"
}
```


## Tan2025EATAC

**Uncertainty-Calibrated Test-Time Model Adaptation without Forgetting**

Authors: Mingkui Tan; Guohao Chen; Jiaxiang Wu; Yifan Zhang; Yaofo Chen; Peilin Zhao; Shuaicheng Niu.

Publication: 2025; IEEE Transactions on Pattern Analysis and Machine Intelligence.

Primary source: [Uncertainty-Calibrated Test-Time Model Adaptation without Forgetting](https://arxiv.org/abs/2403.11491). [Project paper note](../../papers/Tan2025EATAC.md).

Verified DOI in saved record: `10.1109/TPAMI.2025.3560696`.

Publication qualification: 2024 preprint; TPAMI 2025 author-confirmed journal version.

Recorded reading scope: Fresh arXiv abstract, author-hosted paper introduction and author publication metadata; selective reading.

Inspected locations: Abstract; Introduction; Author publication page.

Relevance / overlap from our reading: EATA-C separates reducible model and data uncertainty via full/subnetwork disagreement and min-max entropy calibration.

Limitation / reviewer boundary: A calibration/uncertainty baseline, not whole-method selection. Subnetwork probes and source/ID Fisher preparation must be costed and disclosed.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

[Source ledger](../../notes/review-refresh-2026-10-26/researcher-sources.json).

### Recorded reading history

- **2026-10-26**: Fresh arXiv abstract, author-hosted paper introduction and author publication metadata; selective reading.
  Locations: Abstract; Introduction; Author publication page.
  Qualification: A calibration/uncertainty baseline, not whole-method selection. Subnetwork probes and source/ID Fisher preparation must be costed and disclosed.
  [Dated ledger](../../notes/review-refresh-2026-10-26/researcher-sources.json).

### Other stored metadata

```json
{
  "pdf_url": "https://www.chenyaofo.com/papers/tan-uncertainty-calibrated-test-time-model-adaptation-without-forgetting.pdf"
}
```


## Vianna2025ChannelSelective

**Channel-Selective Normalization for Label-Shift Robust Test-Time Adaptation**

Authors: Pedro Vianna; Muawiz Sajjad Chaudhary; Paria Mehrbod; An Tang; Guy Cloutier; Guy Wolf; Michael Eickenberg; Eugene Belilovsky.

Publication: 2025; Proceedings of The 3rd Conference on Lifelong Learning Agents, PMLR 274:514-533.

Primary source: [Channel-Selective Normalization for Label-Shift Robust Test-Time Adaptation](https://proceedings.mlr.press/v274/vianna25a.html). [Project paper note](../../papers/Vianna2025ChannelSelective.md).

Publication qualification: PMLR volume published 2025 for the 3rd CoLLAs conference held 2024; established citation key preserved. Official PDF selectively read during refresh.

Recorded reading scope: Official metadata and downloaded official PDF §§3-5, Algorithms 1-2, selected result descriptions; partial reading.

Inspected locations: Section 3; Algorithms 1-2; Section 4 Adaptation Details; Section 5 Limitations.

Relevance / overlap from our reading: Source-labeled class/channel sensitivity scores; uniform-prior adaptation pass followed by pseudolabel-based prior rescoring. Direct predecessor for selective normalization under combined covariate/label shift.

Limitation / reviewer boundary: BN networks and labeled-source post-training preparation; offline single-batch setting with batch500 for CIFAR/ImageNet rather than a learned closed-loop persistent selector.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

[Preserved primary PDF](../../notes/review-refresh-2026-10-26/verifier-evidence/Vianna2025ChannelSelective.pdf).

[Extracted text](../../notes/review-refresh-2026-10-26/verifier-evidence/Vianna2025ChannelSelective.txt).

[Source ledger](../../notes/review-refresh-2026-10-26/verifier-sources.json).

### Recorded reading history

- **2026-10-23**: Primary proceedings metadata and abstract only during approach selection; full method not read
  Locations: Abstract; Official BibTeX.
  Qualification: Direct predecessor for imbalance-aware normalization. A simple SOURCE/normalization gate and showing normalization fails under imbalance do not establish novelty. Exact matched-concentration evaluation overlap requires full-method inspection.
  [Dated ledger](../../notes/shift-aware-tta-review-followup-sources.json).

- **2026-10-26**: Fresh PMLR publication metadata and abstract checked; PDF browser returned unsupported octet-stream.
  Locations: PMLR abstract; Citation metadata.
  Qualification: Exact matching protocol/evaluation overlap requires full-method reading; cannot treat label-prior ambiguity or selective normalization as novel.
  [Dated ledger](../../notes/review-refresh-2026-10-26/researcher-sources.json).

- **2026-10-26**: Official metadata and downloaded official PDF §§3-5, Algorithms 1-2, selected result descriptions; partial reading.
  Locations: Section 3; Algorithms 1-2; Section 4 Adaptation Details; Section 5 Limitations.
  Qualification: BN networks and labeled-source post-training preparation; offline single-batch setting with batch500 for CIFAR/ImageNet rather than a learned closed-loop persistent selector.
  [Dated ledger](../../notes/review-refresh-2026-10-26/verifier-sources.json).

### Other stored metadata

```json
{
  "pdf_url": "https://raw.githubusercontent.com/mlresearch/v274/main/assets/vianna25a/vianna25a.pdf",
  "pdf_sha256": "62cc8cc25502aba8a2adf4af87b5eeb4168d4ff2adfa755792783e5f11a4e3a7",
  "accessed": "2026-10-26"
}
```


## Wang2025OTTASurvey

**In Search of Lost Online Test-Time Adaptation: A Survey**

Authors: Zixin Wang; Yadan Luo; Liang Zheng; Zhuoxiao Chen; Sen Wang; Zi Huang.

Publication: 2025; International Journal of Computer Vision 133, 1106–1139; online publication 15 September 2024.

Primary source: [In Search of Lost Online Test-Time Adaptation: A Survey](https://link.springer.com/article/10.1007/s11263-024-02213-5). [Project paper note](../../papers/Wang2025OTTASurvey.md).

Verified DOI in saved record: `10.1007/s11263-024-02213-5`.

Publication qualification: Journal article

Recorded reading scope: Abstract, introduction, taxonomy and scope exclusions

Inspected locations: Abstract; section 1.

Relevance / overlap from our reading: Optimization/data/model categories and explicit accuracy, wall-time, FLOPs and memory comparisons.

Limitation / reviewer boundary: Reported efficiency evaluation means adding a runtime table alone is insufficient novelty.

Recorded implementation/author resource: [link](https://github.com/Jo-wang/OTTA_ViT_survey). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/shift-aware-tta-review-lead-sources.json).


## Ye2025DATTA

**DATTA: Domain Diversity Aware Test-Time Adaptation for Dynamic Domain Shift Data Streams**

Authors: Chuyang Ye; Dongyan Wei; Zhendong Liu; Yuanyi Pang; Yixi Lin; Qinting Jiang; Jingyan Jiang; Dongbiao He.

Publication: 2025; ICME 2025.

Primary source: [DATTA: Domain Diversity Aware Test-Time Adaptation for Dynamic Domain Shift Data Streams](https://arxiv.org/abs/2408.08056). [Project paper note](../../papers/Ye2025DATTA.md).

Publication qualification: Accepted oral per author arXiv record; DOI 10.1109/ICME59968.2025.11209053; preprint first2024, v2 Dec2025 inspected

Recorded reading scope: Abstract, introduction, method overview and section headings.

Inspected locations: Section III-A Domain-Diversity Discrimination; Section III-B DABN; Section III-C DAFT.

Relevance / overlap from our reading: Recognizes single-versus-multiple-domain batches, changes normalization interpolation and selectively fine-tunes to mitigate gradient conflict.

Limitation / reviewer boundary: Domain diversity is not physical shift-cause identification. Dynamic heterogeneous input batches already studied; a generic multi-domain claim is insufficient.

Recorded implementation/author resource: [link](https://github.com/DYW77/DATTA). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/shift-aware-tta-review-researcher-sources.json).

### Other stored metadata

```json
{
  "pdf_url": "https://arxiv.org/pdf/2408.08056v2",
  "html_url": "https://arxiv.org/html/2408.08056v2"
}
```


## Zanella2025StatA

**Realistic Test-Time Adaptation of Vision-Language Models**

Authors: Maxime Zanella; Clément Fuchs; Christophe De Vleeschouwer; Ismail Ben Ayed.

Publication: 2025; CVPR 2025, pages25103-25112.

Primary source: [Realistic Test-Time Adaptation of Vision-Language Models](https://openaccess.thecvf.com/content/CVPR2025/html/Zanella_Realistic_Test-Time_Adaptation_of_Vision-Language_Models_CVPR_2025_paper.html). [Project paper note](../../papers/Zanella2025StatA.md).

Publication qualification: Official CVPR2025 verified

Recorded reading scope: Official abstract/metadata and PDF introduction/figure1; partial reading

Inspected locations: Abstract; Figure1; Introduction.

Relevance / overlap from our reading: Variable effective class count and non-i.i.d. batches can undermine VLM adaptation; StatA anchors initial text knowledge.

Limitation / reviewer boundary: CLIP/VLM and cluster/semantic priors differ from ordinary source classifiers; no claim that all methods collapse universally.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

Recorded implementation/author resource: [link](https://github.com/MaxZanella/StatA). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/review-refresh-2026-10-26/benchmarks-sources.json).

### Recorded reading history

- **2026-10-26**: Official abstract/metadata and PDF introduction/figure1; partial reading
  Locations: Abstract; Figure1; Introduction.
  Qualification: CLIP/VLM and cluster/semantic priors differ from ordinary source classifiers; no claim that all methods collapse universally.
  [Dated ledger](../../notes/review-refresh-2026-10-26/benchmarks-sources.json).

### Other stored metadata

```json
{
  "verified_on": "2026-10-26",
  "preprint_url": "https://arxiv.org/abs/2501.03729"
}
```


## Aronsson2026FeatureAcquisitionSurvey

**A Survey on Active Feature Acquisition Strategies**

Authors: Linus Aronsson; Arman Rahbar; Morteza Haghir Chehreghani.

Publication: 2026; IJCAI 2026 Survey Track, 7740–7748.

Primary source: [A Survey on Active Feature Acquisition Strategies](https://www.ijcai.org/proceedings/2026/860). [Project paper note](../../papers/Aronsson2026FeatureAcquisitionSurvey.md).

Verified DOI in saved record: `10.24963/ijcai.2026/860`.

Publication qualification: Conference survey

Recorded reading scope: Title, authors, abstract and introductory problem formulation from PDF

Inspected locations: Page 1; abstract and introduction.

Relevance / overlap from our reading: Sequential feature acquisition, stopping and prediction under cost constraints.

Limitation / reviewer boundary: A sequential acquisition controller is not a new general problem formulation.

[Preserved primary PDF](../../sources/pdfs/Aronsson2026FeatureAcquisitionSurvey.pdf).

[Source ledger](../../notes/shift-aware-tta-review-lead-sources.json).

### Other stored metadata

```json
{
  "pdf_url": "https://www.ijcai.org/proceedings/2026/0860.pdf",
  "pdf_sha256": "8e4b2af316db8c2669e17a18c4ed8c4469ede4510a813e8667f6b06d71805a6e"
}
```


## Cygert2026RealisticSelection

**Realistic Evaluation of Test-Time Adaptation: Unsupervised Model Selection**

Authors: Sebastian Cygert; Damian Sójka; Tomasz Trzciński; Bartłomiej Twardowski.

Publication: 2026; VISAPP, volume 1, pp.75–86.

Primary source: [Realistic Evaluation of Test-Time Adaptation: Unsupervised Model Selection](https://doi.org/10.5220/0014320100004084). [Project paper note](../../papers/Cygert2026RealisticSelection.md).

Verified DOI in saved record: `10.5220/0014320100004084`.

Publication qualification: conference paper; linked 2024 preprint titled Realistic Evaluation of Test-Time Adaptation Algorithms: Unsupervised Hyperparameter Selection

Recorded reading scope: published first-page metadata; linked 2024 HTML selection definitions, setup, discussion and conclusions; published PDF downloaded and title/author block checked

Inspected locations: Improved hyperparameter selection in TTA; Experimental Setup; Discussion; Conclusions.

Relevance / overlap from our reading: Evaluates source validation, cross-dataset supervision and unlabeled proxy metrics for candidate selection.

Limitation / reviewer boundary: Most evidence is obtained after executing candidates; comparisons to pre-action routing must charge the different information/computation budget.

Recorded implementation/author resource: [link](https://github.com/cygerts/unsupervisedtta). Availability/role follows the reading qualification; no execution is implied.

[Preserved primary PDF](../../sources/pdfs/Cygert2026Selection.pdf).

[Source ledger](../../notes/shift-aware-tta-review-verifier-sources.json).

### Other stored metadata

```json
{
  "pdf_url": "https://www.scitepress.org/Papers/2026/143201/143201.pdf",
  "preprint_url": "https://arxiv.org/abs/2407.14231",
  "pdf_sha256": "932eacd0919d445b443250fa430cf82bc9a75f1a953786c063828e8b0ef072b5"
}
```


## Danilowski2026BoTTA

**BoTTA: Benchmarking On-device Test Time Adaptation**

Authors: Michal Danilowski; Soumyajit Chatterjee; Abhirup Ghosh.

Publication: 2026; Proceedings of the 2026 ACM/IEEE International Conference on Embedded Artificial Intelligence and Sensing Systems, pages 465–477.

Primary source: [BoTTA: Benchmarking On-device Test Time Adaptation](https://doi.org/10.1145/3774906.3800498). [Project paper note](../../papers/Danilowski2026BoTTA.md).

Verified DOI in saved record: `10.1145/3774906.3800498`.

Publication qualification: Publisher full text identifies SenSys 2026, published 10 May 2026; older arXiv:2504.10149v2 record instead carries a SenSys 2025 report-number statement. Preserve this discrepancy; publisher version is used for conference citation.

Recorded reading scope: Fresh publisher fulltext excerpt surfaced in search; DOI direct access returned403

Inspected locations: Abstract; sections2-4 and listed hardware.

Relevance / overlap from our reading: Limited target data, incomplete category coverage, overlapping shifts and hardware-constrained periodic adaptation are already benchmarked.

Limitation / reviewer boundary: This is an evaluation framework, not the proposed learned multi-action acquisition policy. Paper-linked code URL https://github.com/m-danilow/BoTTA returned 404 in this review, so availability is not established.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

[Source ledger](../../notes/review-refresh-2026-10-26/benchmarks-sources.json).

### Recorded reading history

- **2026-10-23**: Publisher metadata/abstract, sections 2 and 4, system metric descriptions and conclusion; preprint metadata checked separately
  Locations: Abstract; Section 2; Section 4; System metrics; Conclusion.
  Qualification: This is an evaluation framework, not the proposed learned multi-action acquisition policy. Paper-linked code URL https://github.com/m-danilow/BoTTA returned 404 in this review, so availability is not established.
  [Dated ledger](../../notes/shift-aware-tta-review-reviewer-sources.json).

- **2026-10-26**: Fresh publisher fulltext excerpt surfaced in search; DOI direct access returned403
  Locations: Abstract; sections2-4 and listed hardware.
  Qualification: Periodic adaptation differs from same-batch adaptation; quantitative tables not audited in refresh.
  [Dated ledger](../../notes/review-refresh-2026-10-26/benchmarks-sources.json).

### Other stored metadata

```json
{
  "preprint_url": "https://arxiv.org/abs/2504.10149v2",
  "pdf_url": null,
  "refresh_read_scope": "Fresh publisher fulltext excerpt surfaced in search; DOI direct access returned403",
  "refresh_locations": "Abstract; sections2-4 and listed hardware",
  "refresh_limitation": "Periodic adaptation differs from same-batch adaptation; quantitative tables not audited in refresh.",
  "verified_on": "2026-10-26"
}
```


## Danilowski2026MORPHEUS

**MORPHEUS: Meta Test-Time Adaptation via Neural Collapse Geometry**

Authors: Michal Danilowski; Alexander Murphy; Young D. Kwon; Abhirup Ghosh.

Publication: 2026; ICLR 2026 Test-Time Updates Workshop.

Primary source: [MORPHEUS: Meta Test-Time Adaptation via Neural Collapse Geometry](https://theyoungkwon.github.io/papers/articles/danilowski_morpheus_iclr-ttu26.pdf). [Project paper note](../../papers/Danilowski2026MORPHEUS.md).

Publication qualification: Workshop paper, not main-track ICLR; author research page corroborates

Recorded reading scope: Fresh author-hosted PDF selective reading; method, experimental setup and appendix feature definitions.

Inspected locations: PDF header; Section 2; Section 3; Appendix B.

Relevance / overlap from our reading: Source entropy and pseudo-label neural-collapse geometry feed random-forest predictions of whole-method post-adaptation accuracy before executing the chosen method.

Limitation / reviewer boundary: Auxiliary labeled outcomes train predictors. Inspected setting starts from source model/domain data; does not establish autonomous state-history generalization.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

[Preserved primary PDF](../../sources/pdfs/Danilowski2026MORPHEUS.pdf).

[Source ledger](../../notes/review-refresh-2026-10-26/researcher-sources.json).

### Recorded reading history

- **2026-10-23**: Author PDF downloaded; abstract, sections 1–3, meta-training description and selected appendix/table passages read. Workshop status checked against PDF header and author publication page.
  Locations: Section 2, Problem and Methodology; Section 3; Appendix split descriptions.
  Qualification: Supervised auxiliary-domain development precedes unlabeled selection. Text/table numbers and feature definitions need care; no numerical result is copied as our reproduction. Official code not verified.
  [Dated ledger](../../notes/shift-aware-tta-review-researcher-sources.json).

- **2026-10-26**: Fresh author-hosted PDF selective reading; method, experimental setup and appendix feature definitions.
  Locations: PDF header; Section 2; Section 3; Appendix B.
  Qualification: Auxiliary labeled outcomes train predictors. Inspected setting starts from source model/domain data; does not establish autonomous state-history generalization.
  [Dated ledger](../../notes/review-refresh-2026-10-26/researcher-sources.json).

### Other stored metadata

```json
{
  "pdf_url": "https://theyoungkwon.github.io/papers/articles/danilowski_morpheus_iclr-ttu26.pdf",
  "pdf_sha256": "c9aaf6308fe8973e49d66315c2352b5561ae42679b92e4271bb0f75d56d5fc22"
}
```


## Doloriel2026SEGA

**Continual Test-Time Adaptation via Entropy Sensitivity-Guidance in Strict Online Setting**

Authors: Chandler Timm C. Doloriel; Yunbei Zhang; Muhammad Salman Siddiqui; Tor Kristian Stevik; Fadi Al Machot; Kristian Hovde Liland; Habib Ullah.

Publication: 2026; arXiv preprint.

Primary source: [Continual Test-Time Adaptation via Entropy Sensitivity-Guidance in Strict Online Setting](https://arxiv.org/abs/2608.29920). [Project paper note](../../papers/Doloriel2026SEGA.md).

Publication qualification: arXiv2608.29920v1,30August2026,underreview per record

Recorded reading scope: Abstract, sections 3.2–3.3, Algorithm 1 and selected conclusion passages from downloaded PDF; partial reading.

Inspected locations: Sections 3.2–3.3; Algorithm 1; Conclusion.

Relevance / overlap from our reading: Structured erasure probes produce entropy-sensitivity trajectories for recovery/sample selection and reduce backward updates in batchsizeonecontinual streams.

Limitation / reviewer boundary: Algorithm 1 computes N declared erasure levels and gates updates/recovery. This is probe-based adaptation control, rather than the proposed learned net-value acquisition across a whole-method menu. No full code audit.

[Preserved primary PDF](../../sources/pdfs/Doloriel2026SEGA.pdf).

[Source ledger](../../notes/shift-aware-tta-review-researcher-sources.json).

### Other stored metadata

```json
{
  "pdf_url": "https://arxiv.org/pdf/2608.29920v1",
  "pdf_sha256": "8f8a8c573eb1e6738378a7ea5afd72de158b57b97fc33b59a47cc9244010f0fb"
}
```


## Fan2026MoETTA

**MoETTA: Test-Time Adaptation Under Mixed Distribution Shifts with MoE-LayerNorm**

Authors: Xiao Fan; Jingyan Jiang; Zhaoru Chen; Fanding Huang; Xiao Chen; Qinting Jiang; Bowen Zhang; Xing Tang; Zhi Wang.

Publication: 2026; AAAI2026 Main Technical Track.

Primary source: [MoETTA: Test-Time Adaptation Under Mixed Distribution Shifts with MoE-LayerNorm](https://arxiv.org/abs/2511.13760). [Project paper note](../../papers/Fan2026MoETTA.md).

Publication qualification: Acceptance reported by authorarXiv; firstpreprint14November2025; v1 inspected

Recorded reading scope: Abstract,introduction,routing/mechanism description and §5.3/table excerpts.

Inspected locations: Mixture-of-Experts LayerNorm routing; 5.3 Computation Efficiency; Potpourri/potpourri+ design.

Relevance / overlap from our reading: LayerNorm experts permit sample-specific gradient directions under mixed shifts; potpourri mixes natural/artistic/adversarial shifts, potpourri+ includes source examples.

Limitation / reviewer boundary: Mixed domains/source returns are covered as benchmarks; action-menu policy selection and image-level composed corruptions remain distinct, but no novelty inferred from this distinction.

Recorded implementation/author resource: [link](https://github.com/AnikiFan/MoETTA). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/shift-aware-tta-review-researcher-sources.json).

### Other stored metadata

```json
{
  "pdf_url": "https://arxiv.org/pdf/2511.13760v1",
  "html_url": "https://arxiv.org/html/2511.13760v1"
}
```


## Gai2026AdaTentPlusPlus

**AdaTent++: reliability-guided hybrid test-time adaptation for traffic sign detection under distribution shift**

Authors: Xiaomei Gai; Meichun Wang; Yantong Guo; Shiyu Wang; Ye Li; Rui Fu.

Publication: 2026; Frontiers in Signal Processing6.

Primary source: [AdaTent++: reliability-guided hybrid test-time adaptation for traffic sign detection under distribution shift](https://www.frontiersin.org/journals/signal-processing/articles/10.3389/frsip.2026.1842851/full). [Project paper note](../../papers/Gai2026AdaTentPlusPlus.md).

Verified DOI in saved record: `10.3389/frsip.2026.1842851`.

Publication qualification: Published9September2026, DOI10.3389/frsip.2026.1842851

Recorded reading scope: Fresh open publisher full text, selective method and limitation reading.

Inspected locations: Sections 2.1–2.4; Sections 4–6.

Relevance / overlap from our reading: Entropy/cross-view reliability routes traffic-sign frames to BN statistics, guarded BN-affine updates, or skip/rollback.

Limitation / reviewer boundary: Declared condition-aware configuration, balanced subset, deterministic run and no long-stream evaluation limit transfer claims; budget comparison qualified in discussion.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

[Source ledger](../../notes/review-refresh-2026-10-26/researcher-sources.json).

### Recorded reading history

- **2026-10-23**: Publisher full text selectively read: abstract, sections2.1–2.4, ablations, discussion, limitations and conclusion.
  Locations: 2.3 multiview reliability and dynamic routing; 2.4 threepath mechanics; 3.4 ablations; 4 Discussion; 5 Limitations; 6 Conclusion item4.
  Qualification: §5 admits benchmark-condition IDs for views/filtering, one deterministic run and no longstream. §4 says not compute-matched despite conflicting conclusion wording. §6 requests budget-aware adaptive viewcount/step controllers. No guarantees verified.
  [Dated ledger](../../notes/shift-aware-tta-review-researcher-sources.json).

- **2026-10-26**: Fresh open publisher full text, selective method and limitation reading.
  Locations: Sections 2.1–2.4; Sections 4–6.
  Qualification: Declared condition-aware configuration, balanced subset, deterministic run and no long-stream evaluation limit transfer claims; budget comparison qualified in discussion.
  [Dated ledger](../../notes/review-refresh-2026-10-26/researcher-sources.json).

### Other stored metadata

```json
{
  "pdf_url": null
}
```


## Han2026Exchangeability

**The Premise Is the Problem: Exchangeability Failure in Self-Monitored Test-Time Adaptation**

Authors: Weijia Han; Lisha Qu; Zhenda Li; Liying Liang.

Publication: 2026; arXiv preprint 2610.07038.

Primary source: [The Premise Is the Problem: Exchangeability Failure in Self-Monitored Test-Time Adaptation](https://arxiv.org/abs/2610.07038). [Project paper note](../../papers/Han2026Exchangeability.md).

Publication qualification: arXiv v1 submitted4October2026; no independently verified venue

Recorded reading scope: arXiv metadata/abstract, introduction and selected discussion of feedback, dependence and evaluation limits; partial reading of a49-page paper.

Inspected locations: Abstract; Introduction; Selected evaluation/limitations discussion.

Relevance / overlap from our reading: Self-monitoring feedback can hide sustained shifts or produce invalid alarms; frozen source can retain a clearer signal.

Limitation / reviewer boundary: Multi-step time-series forecasting with revealed forecast outcomes; not strictly unlabeled visual classification or a verified universal monitor impossibility theorem.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

[Source ledger](../../notes/review-refresh-2026-10-26/verifier-sources.json).

### Recorded reading history

- **2026-10-26**: arXiv metadata/abstract, introduction and selected discussion of feedback, dependence and evaluation limits; partial reading of a49-page paper.
  Locations: Abstract; Introduction; Selected evaluation/limitations discussion.
  Qualification: Multi-step time-series forecasting with revealed forecast outcomes; not strictly unlabeled visual classification or a verified universal monitor impossibility theorem.
  [Dated ledger](../../notes/review-refresh-2026-10-26/verifier-sources.json).

### Other stored metadata

```json
{
  "html_url": "https://arxiv.org/html/2610.07038v1",
  "accessed": "2026-10-26"
}
```


## Huang2026TTABC

**What Drives Test-Time Adaptation for CLIP? A Controlled Empirical Study from an Update Perspective**

Authors: Jiazhen Huang; Xiao Chen; Zhiming Liu; Yaru Sun; Jingyan Jiang; Zhi Wang.

Publication: 2026; arXiv preprint; author-reported NeurIPS2026 E&D.

Primary source: [What Drives Test-Time Adaptation for CLIP? A Controlled Empirical Study from an Update Perspective](https://arxiv.org/abs/2606.14299). [Project paper note](../../papers/Huang2026TTABC.md).

Publication qualification: ArXiv v1 June12 and v3 October12 2026 verified; venue author-reported

Recorded reading scope: arXiv v3 metadata and selective fulltext reading sections2-5, AppendixB/E; author site. Lead additionally checked Table4 and table/prose consistency.

Inspected locations: Sections2-5; Table4; AppendixB Limitations; AppendixE datasets/stream construction.

Relevance / overlap from our reading: 20+ CLIP methods, parameter/state/inference taxonomy, shift-dependent paradigm preferences; dynamic paradigm selection listed as future problem.

Limitation / reviewer boundary: CLIP classification; paradigm preferences do not certify novel routing. Venue author-reported, not independently checked in proceedings. V3 natural-average prose and tables disagree (e.g. TPS63.01 vs64.46); numerical use must identify its exact table. Metadata title uses 'an Update', HTML heading 'a Update'.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

Recorded implementation/author resource: [link](https://github.com/walawalagoose/TTABC). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/review-refresh-2026-10-26/benchmarks-sources.json).

### Recorded reading history

- **2026-10-26**: arXiv v3 metadata and selective fulltext reading sections2-5, AppendixB/E; author site. Lead additionally checked Table4 and table/prose consistency.
  Locations: Sections2-5; Table4; AppendixB Limitations; AppendixE datasets/stream construction.
  Qualification: CLIP classification; paradigm preferences do not certify novel routing. Venue author-reported, not independently checked in proceedings. V3 natural-average prose and tables disagree (e.g. TPS63.01 vs64.46); numerical use must identify its exact table. Metadata title uses 'an Update', HTML heading 'a Update'.
  [Dated ledger](../../notes/review-refresh-2026-10-26/benchmarks-sources.json).

### Other stored metadata

```json
{
  "verified_on": "2026-10-26",
  "html_url": "https://arxiv.org/html/2606.14299v3",
  "project_url": "https://walawalagoose.github.io/TTABC/"
}
```


## Huzaifa2026WISEATTA

**WISE-ATTA: When to Ask for Labels in Budgeted Active Test-Time Adaptation**

Authors: Muhammad Huzaifa; Lea Schönherr; Thorsten Eisenhofer.

Publication: 2026; arXiv:2609.37687, 29 September 2026.

Primary source: [WISE-ATTA: When to Ask for Labels in Budgeted Active Test-Time Adaptation](https://arxiv.org/abs/2609.37687). [Project paper note](../../papers/Huzaifa2026WISEATTA.md).

Publication qualification: Preprint

Recorded reading scope: Abstract and arXiv metadata only

Inspected locations: Abstract.

Relevance / overlap from our reading: Online budget allocation across adaptation windows.

Limitation / reviewer boundary: Uses queried target labels, unlike the proposed zero-target-label deployment regime.

Recorded implementation/author resource: [link](https://github.com/Muhammad-Huzaifaa/WISE-ATTA). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/shift-aware-tta-review-lead-sources.json).


## Jain2026MeasureLess

**Measure Less, Know More: Self-Supervised Test-Time Feature Acquisition**

Authors: Eeshaan Jain; Linus Bleistein; Bart Deplancke; Charlotte Bunne.

Publication: 2026; arXiv:2610.03454v1, 2 October 2026; manuscript carries a NeurIPS 2026 footer, acceptance not independently confirmed.

Primary source: [Measure Less, Know More: Self-Supervised Test-Time Feature Acquisition](https://arxiv.org/abs/2610.03454). [Project paper note](../../papers/Jain2026MeasureLess.md).

Publication qualification: Verified arXiv preprint

Recorded reading scope: Abstract and introductory acquisition formulation from downloaded PDF

Inspected locations: Page 1; abstract and section 1.

Relevance / overlap from our reading: ECHO-k selects costly modalities using pretrained representation recovery as label-free feedback.

Limitation / reviewer boundary: Acquiring views without task labels is already studied; proposed distinction must concern adaptation-action benefit.

Recorded implementation/author resource: [link](https://github.com/bunnelab/echo-k). Availability/role follows the reading qualification; no execution is implied.

[Preserved primary PDF](../../sources/pdfs/Jain2026MeasureLess.pdf).

[Source ledger](../../notes/shift-aware-tta-review-lead-sources.json).

### Other stored metadata

```json
{
  "pdf_url": "https://arxiv.org/pdf/2610.03454v1",
  "pdf_sha256": "fa223817bdcbb9ce565fe6aa684d614dd6d74f8478bc946df5bcbf66cb0a990a"
}
```


## Jeong2026CalibrationAware

**Calibration-Aware Online Adaptation under Label Shift**

Authors: Jiun Jeong; Byeongwoo An; Gi-Soo Kim; Kyubo Shin.

Publication: 2026; Proceedings of the 42nd Conference on Uncertainty in Artificial Intelligence, PMLR 337:2480-2516.

Primary source: [Calibration-Aware Online Adaptation under Label Shift](https://proceedings.mlr.press/v337/jeong26a.html). [Project paper note](../../papers/Jeong2026CalibrationAware.md).

Publication qualification: UAI2026 official proceedings and accepted list verified

Recorded reading scope: Official PMLR metadata/abstract and official accepted-paper page. Not full method or proof read.

Inspected locations: Official abstract; Official accepted-paper metadata.

Relevance / overlap from our reading: Separately calibrated auxiliary classifier estimates streaming target priors; analyzes calibration-dependent estimation error and calibration-granularity tradeoff.

Limitation / reviewer boundary: Label-shift setting; no arbitrary simultaneous nuisance-shift guarantee established by the inspected abstract.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

[Source ledger](../../notes/review-refresh-2026-10-26/verifier-sources.json).

### Recorded reading history

- **2026-10-26**: Official PMLR metadata/abstract and official accepted-paper page. Not full method or proof read.
  Locations: Official abstract; Official accepted-paper metadata.
  Qualification: Label-shift setting; no arbitrary simultaneous nuisance-shift guarantee established by the inspected abstract.
  [Dated ledger](../../notes/review-refresh-2026-10-26/verifier-sources.json).

### Other stored metadata

```json
{
  "pdf_url": "https://raw.githubusercontent.com/mlresearch/v337/main/assets/jeong26a/jeong26a.pdf",
  "accessed": "2026-10-26"
}
```


## Jhawar2026HDTTA

**HD-TTA: Hypothesis-Driven Test-Time Adaptation for Safer Brain Tumor Segmentation**

Authors: Kartik Jhawar; Lipo Wang.

Publication: 2026; MICCAI2026 (official page found); inspected arXiv preprint.

Primary source: [HD-TTA: Hypothesis-Driven Test-Time Adaptation for Safer Brain Tumor Segmentation](https://arxiv.org/abs/2602.19454). [Project paper note](../../papers/Jhawar2026HDTTA.md).

Publication qualification: arXiv2602.19454v1,23February2026; officialMICCAI2026 paper3549 supports venue

Recorded reading scope: arXiv abstract and official MICCAI paper-page abstract/review summaries; full method not read.

Inspected locations: Abstract; MICCAI2026 paper3549 review summaries.

Relevance / overlap from our reading: Gatekeeper skips confident masks; competing compaction/inflation hypotheses are scored by intrinsic representation consistency to select safer refinement.

Limitation / reviewer boundary: Clinical binary segmentation proof of concept; not evidence a general classification method selector is new. Code was promised on acceptance; release not verified.

[Source ledger](../../notes/shift-aware-tta-review-researcher-sources.json).

### Other stored metadata

```json
{
  "pdf_url": "https://arxiv.org/pdf/2602.19454v1"
}
```


## Jhawar2026Identifiability

**When is Test-Time Adaptation Identifiable From Unlabeled Evidence?**

Authors: Kartik Jhawar; Lipo Wang.

Publication: 2026; arXiv.

Primary source: [When is Test-Time Adaptation Identifiable From Unlabeled Evidence?](https://arxiv.org/abs/2609.11235). [Project paper note](../../papers/Jhawar2026Identifiability.md).

Publication qualification: preprint v1, submitted 10 September 2026

Recorded reading scope: Fresh arXiv HTML selective reading: setup, theory, complete experimental design, limitations and experimental appendix.

Inspected locations: Sections 2–5; Section 7; Appendix B.

Relevance / overlap from our reading: Same unlabeled evidence can conceal action reversals; stream structure, prior mechanism and batch size affect selection. SOURCE is an explicit action.

Limitation / reviewer boundary: Section 4.1 starts every action from the same frozen source per world. No arbitrary-deployment or universal evidence guarantee; live policy-induced state study not inspected.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

[Preserved primary PDF](../../sources/pdfs/Jhawar2026Identifiability.pdf).

[Source ledger](../../notes/review-refresh-2026-10-26/researcher-sources.json).

### Recorded reading history

- **2026-10-23**: Sections 2–7 and Appendix B
  Locations: Section 3.5; Sections 4.1–4.3; Sections 5.1–5.4; Section 7; Appendix B.5.
  Qualification: Finite action menu and main source-model family; evidence sufficiency depends on deployment family. Does not evaluate costed active evidence acquisition or claim universally superior evidence.
  [Dated ledger](../../notes/shift-aware-tta-review-verifier-sources.json).

- **2026-10-26**: Fresh arXiv HTML selective reading: setup, theory, complete experimental design, limitations and experimental appendix.
  Locations: Sections 2–5; Section 7; Appendix B.
  Qualification: Section 4.1 starts every action from the same frozen source per world. No arbitrary-deployment or universal evidence guarantee; live policy-induced state study not inspected.
  [Dated ledger](../../notes/review-refresh-2026-10-26/researcher-sources.json).

### Other stored metadata

```json
{
  "pdf_url": "https://arxiv.org/pdf/2609.11235v1",
  "pdf_sha256": "5e916b909334a04175089cef8617d9426a8ecbea6bf7f3e48624483eec190203"
}
```


## Jiang2026CAS

**To Adapt or Not to Adapt? Selective Adaptation for Vision-Language Models**

Authors: Siru Jiang; Yuwei Liang; Jian Liang; Ran He; Tieniu Tan.

Publication: 2026; arXiv:2609.08367v1; author record comments identify ECCV 2026.

Primary source: [To Adapt or Not to Adapt? Selective Adaptation for Vision-Language Models](https://arxiv.org/abs/2609.08367v1). [Project paper note](../../papers/Jiang2026CAS.md).

Publication qualification: Preprint submitted 8 September 2026; ECCV 2026 is stated on primary arXiv record, proceedings metadata not independently checked by reviewer

Recorded reading scope: Primary arXiv metadata and full HTML sections 2–3.3, including episodic scope and the CAS decision rule; no code audit.

Inspected locations: Abstract; Section 3.2; Section 3.3.

Relevance / overlap from our reading: Cross-Augmentation Similarity decides whether to perform or skip a VLM adaptation, directly overlapping extra-view evidence for an update/no-update decision.

Limitation / reviewer boundary: The candidate needs multi-action value-based evidence acquisition beyond this fixed view-based skip rule. Adaptation skipping is not itself new.

Recorded implementation/author resource: [link](https://github.com/sirujiang/selective-adaptation). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/shift-aware-tta-review-reviewer-sources.json).

### Other stored metadata

```json
{
  "html_url": "https://arxiv.org/html/2609.08367v1",
  "pdf_url": null
}
```


## Karimi2026ShiftACT

**Shift-ACT: Test-time adaptation via shift-aware class-specific dynamic thresholding for domain generalization**

Authors: Saeed Karimi; Hamdi Dibeklioglu.

Publication: 2026; Neurocomputing 663, article132013.

Primary source: [Shift-ACT: Test-time adaptation via shift-aware class-specific dynamic thresholding for domain generalization](https://www.sciencedirect.com/science/article/pii/S0925231225026852). [Project paper note](../../papers/Karimi2026ShiftACT.md).

Verified DOI in saved record: `10.1016/j.neucom.2025.132013`.

Publication qualification: Published28January2026, DOI10.1016/j.neucom.2025.132013

Recorded reading scope: Publisher abstract/metadata and author repository README.

Inspected locations: Abstract; Repository preparation/run instructions.

Relevance / overlap from our reading: Class-specific source-target confidence gaps adjust thresholds; reliable samples get entropy minimization, unreliable samples get prototype contrastive alignment.

Limitation / reviewer boundary: Source-derived class confidence information required; selected method passages/full detailed protocol not read. Class-wise signal-dependent objective choice is already present.

Recorded implementation/author resource: [link](https://github.com/saeedkarimi90/Shift-act). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/shift-aware-tta-review-researcher-sources.json).

### Other stored metadata

```json
{
  "pdf_url": null
}
```


## Kumar2026RGTTA

**RG-TTA: Regime-Guided Meta-Control for Test-Time Adaptation in Streaming Time Series**

Authors: Indar Kumar; Akanksha Tiwari; Sai Krishna Jasti; Ankit Hemant Lade.

Publication: 2026; arXiv preprint.

Primary source: [RG-TTA: Regime-Guided Meta-Control for Test-Time Adaptation in Streaming Time Series](https://arxiv.org/abs/2603.27814). [Project paper note](../../papers/Kumar2026RGTTA.md).

Publication qualification: arXiv2603.27814v1,29March2026; no venue acceptance verified

Recorded reading scope: Abstract,introduction,method outline and limitations/ablation table of contents.

Inspected locations: III-C continuous regime guidance; III-F checkpoint management; VII-H component contribution; IX Limitations.

Relevance / overlap from our reading: Uses similarity to stored regimes to scale learning rate, stop updates when loss plateaus and reuse checkpoints only when predicted loss benefit passes a gate.

Limitation / reviewer boundary: Temporal forecasting setup has observed outcomes; checkpoint bank/rate controller is not fully unlabeled image-classification method selection.

Recorded implementation/author resource: [link](https://github.com/IndarKarhana/RGTTA-Regime-Guided-Test-Time-Adaptation). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/shift-aware-tta-review-researcher-sources.json).

### Other stored metadata

```json
{
  "pdf_url": "https://arxiv.org/pdf/2603.27814v1",
  "html_url": "https://arxiv.org/html/2603.27814v1"
}
```


## Lai2026GOLD

**The Golden Subspace: Where Efficiency Meets Generalization in Continual Test-Time Adaptation**

Authors: Guannan Lai; Da-Wei Zhou; Zhenguo Li; Han-Jia Ye.

Publication: 2026; CVPR 2026, pages 3866–3875.

Primary source: [The Golden Subspace: Where Efficiency Meets Generalization in Continual Test-Time Adaptation](https://openaccess.thecvf.com/content/CVPR2026/html/Lai_The_Golden_Subspace_Where_Efficiency_Meets_Generalization_in_Continual_Test-Time_CVPR_2026_paper.html). [Project paper note](../../papers/Lai2026GOLD.md).

Publication qualification: Official CVPR 2026 proceedings verified.

Recorded reading scope: Official CVF metadata and abstract only.

Inspected locations: Abstract.

Relevance / overlap from our reading: Low-rank directional feature adaptation with online subspace maintenance addresses efficiency/generalization in continual classification and segmentation.

Limitation / reviewer boundary: The stated subspace result is restricted to a single-step setting; no general multi-step stability theorem was verified. Full empirical protocol remains to read.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

Recorded implementation/author resource: [link](https://github.com/AIGNLAI/GOLD). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/review-refresh-2026-10-26/lead-sources.json).

### Recorded reading history

- **2026-10-26**: Official CVF metadata and abstract only.
  Locations: Abstract.
  Qualification: The stated subspace result is restricted to a single-step setting; no general multi-step stability theorem was verified. Full empirical protocol remains to read.
  [Dated ledger](../../notes/review-refresh-2026-10-26/lead-sources.json).

### Other stored metadata

```json
{
  "entry_type": "inproceedings"
}
```


## Lim2026ASR

**When and Where to Reset Matters for Long-Term Test-Time Adaptation**

Authors: Taejun Lim; Joong-Won Hwang; Kibok Lee.

Publication: 2026; ICLR.

Primary source: [When and Where to Reset Matters for Long-Term Test-Time Adaptation](https://arxiv.org/abs/2603.03796). [Project paper note](../../papers/Lim2026ASR.md).

Publication qualification: conference paper; arXiv v1 submitted 4 March 2026

Recorded reading scope: Fresh arXiv HTML selective method and appendix reading.

Inspected locations: Sections 3.3–3.5; Appendices A.1–A.5.

Relevance / overlap from our reading: Collapse-aware selective reset, knowledge recovery and source/current disagreement regulate adaptation.

Limitation / reviewer boundary: Source/live disagreement and state-dependent recovery are already prior art. Remaining decision gap must be narrower than these ingredients.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

Recorded implementation/author resource: [link](https://github.com/YonseiML/asr). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/review-refresh-2026-10-26/researcher-sources.json).

### Recorded reading history

- **2026-10-23**: abstract/introduction, method outline and selected Sections 3.3–3.5
  Locations: Sections 3.3–3.5; Figure 1; Appendix headings A.5 and A.10.
  Qualification: Choosing reset timing, scope or update strength is not new; whole-method benefit conditioned on live optimizer/memory state would need a separate precise comparison.
  [Dated ledger](../../notes/shift-aware-tta-review-verifier-sources.json).

- **2026-10-26**: Fresh arXiv HTML selective method and appendix reading.
  Locations: Sections 3.3–3.5; Appendices A.1–A.5.
  Qualification: Source/live disagreement and state-dependent recovery are already prior art. Remaining decision gap must be narrower than these ingredients.
  [Dated ledger](../../notes/review-refresh-2026-10-26/researcher-sources.json).

### Other stored metadata

```json
{
  "pdf_url": "https://arxiv.org/pdf/2603.03796v1"
}
```


## Liu2026TiME

**TiME: Test-Time Mixture-of-Experts Routing via Asymmetric CO-Optimal Transport for Continual Test-Time Adaptation**

Authors: Tianlun Liu; Zhiliang Tian; Zhen Huang; Tianle Liu; Xingzhi Zhou; Feng Liu; Dongsheng Li.

Publication: 2026; Proceedings of the 43rd International Conference on Machine Learning, PMLR 306:78597–78632.

Primary source: [TiME: Test-Time Mixture-of-Experts Routing via Asymmetric CO-Optimal Transport for Continual Test-Time Adaptation](https://proceedings.mlr.press/v306/liu26ec.html). [Project paper note](../../papers/Liu2026TiME.md).

Publication qualification: ICML 2026 primary PMLR proceedings verified.

Recorded reading scope: Fresh PMLR abstract and citation metadata only.

Inspected locations: Abstract; Citation metadata.

Relevance / overlap from our reading: LLM continual adaptation routes unseen-domain samples to experts using asymmetric co-optimal transport and semantic alignment.

Limitation / reviewer boundary: Expert allocation differs from whole-method selection, but domain-aware composition is prior art. Detailed preparation, tests and costs not audited.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

[Source ledger](../../notes/review-refresh-2026-10-26/researcher-sources.json).

### Recorded reading history

- **2026-10-26**: Fresh PMLR abstract and citation metadata only.
  Locations: Abstract; Citation metadata.
  Qualification: Expert allocation differs from whole-method selection, but domain-aware composition is prior art. Detailed preparation, tests and costs not audited.
  [Dated ledger](../../notes/review-refresh-2026-10-26/researcher-sources.json).


## Lu2026AgenticTTT

**Agentic-TTT: Training test-time policy for test-time training**

Authors: Jiahao Lu; Mohan Kankanhalli.

Publication: 2026; arXiv preprint2610.12002.

Primary source: [Agentic-TTT: Training test-time policy for test-time training](https://arxiv.org/abs/2610.12002). [Project paper note](../../papers/Lu2026AgenticTTT.md).

Publication qualification: arXiv v1 submitted8October2026; no independently verified venue

Recorded reading scope: Metadata, introduction, §2.2.2, execution-harness descriptions and AppendixE limitations. Partial reading.

Inspected locations: Section2.2.2; AppendixD.1; AppendixE: Cross-query credit assignment.

Relevance / overlap from our reading: Learned state-conditioned method selection with same-snapshot local counterfactuals; explicitly identifies gold-history/autonomous-history exposure bias and leaves autonomous-stream credit assignment open.

Limitation / reviewer boundary: Isolated LoRA skill library over frozen LLM, gold-generated training successor states and query-level reward; benefit-enriched benchmark. Not a continual shared-weights visual TTA evaluation.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

[Source ledger](../../notes/review-refresh-2026-10-26/verifier-sources.json).

### Recorded reading history

- **2026-10-26**: Fresh arXiv metadata and HTML selective method and limitations reading.
  Locations: Section 2.1; Section 2.2.2; Appendix D.2; Appendix E.
  Qualification: Gold-history training states differ from autonomous deployment; Appendix E explicitly leaves cross-query credit assignment to future work. Frozen backbone; adapters can be warm-started.
  [Dated ledger](../../notes/review-refresh-2026-10-26/researcher-sources.json).

- **2026-10-26**: Metadata, introduction, §2.2.2, execution-harness descriptions and AppendixE limitations. Partial reading.
  Locations: Section2.2.2; AppendixD.1; AppendixE: Cross-query credit assignment.
  Qualification: Isolated LoRA skill library over frozen LLM, gold-generated training successor states and query-level reward; benefit-enriched benchmark. Not a continual shared-weights visual TTA evaluation.
  [Dated ledger](../../notes/review-refresh-2026-10-26/verifier-sources.json).

### Other stored metadata

```json
{
  "html_url": "https://arxiv.org/html/2610.12002v1",
  "accessed": "2026-10-26"
}
```


## Majumdar2026HelpHarm

**When Test-Time Adaptation Helps, Harms, or Becomes Inactive: A Condition-Level Study on CIFAR-10-C**

Authors: Sreeja Guha Majumdar; Aratrika Saha.

Publication: 2026; arXiv preprint.

Primary source: [When Test-Time Adaptation Helps, Harms, or Becomes Inactive: A Condition-Level Study on CIFAR-10-C](https://arxiv.org/abs/2608.22233). [Project paper note](../../papers/Majumdar2026HelpHarm.md).

Publication qualification: arXiv v1, 23 August 2026; no venue verified.

Recorded reading scope: Fresh arXiv abstract and metadata only.

Inspected locations: Abstract.

Relevance / overlap from our reading: Condition-level SOURCE/BN-Adapt/Tent/scoped EATA comparison studies harms hidden by mean accuracy.

Limitation / reviewer boundary: Single corruption benchmark and scoped EATA reimplementation; no full-method audit. Help/harm reporting alone cannot establish novelty.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

[Source ledger](../../notes/review-refresh-2026-10-26/researcher-sources.json).

### Recorded reading history

- **2026-10-26**: Fresh arXiv abstract and metadata only.
  Locations: Abstract.
  Qualification: Single corruption benchmark and scoped EATA reimplementation; no full-method audit. Help/harm reporting alone cannot establish novelty.
  [Dated ledger](../../notes/review-refresh-2026-10-26/researcher-sources.json).


## Rehan2026FORGE

**FORGE: Forward-Only Test-Time Adaptation for Integer-Only Vision Models on Microcontrollers**

Authors: Muhammad Rehan; Haider Ali; Muhammad Ali Munir; Moaz Amjad.

Publication: 2026; arXiv:2609.01683v1; arXiv record identifies Transactions on Machine Learning Research 2026 publication.

Primary source: [FORGE: Forward-Only Test-Time Adaptation for Integer-Only Vision Models on Microcontrollers](https://arxiv.org/abs/2609.01683v1). [Project paper note](../../papers/Rehan2026FORGE.md).

Publication qualification: Preprint submitted 1 September 2026; TMLR venue claim present on primary author record, but acceptance independently unverified by reviewer

Recorded reading scope: Abstract/metadata, full HTML section 4.6, Algorithm 2 and section 5 limitations; selected deployment text inspected

Inspected locations: Section 4.6; Algorithm 2; Section 5.

Relevance / overlap from our reading: Runs source and adapted paths during a short unlabeled calibration window, charges duplicate forward passes, then commits using confidence improvement. Paid probing and no-update fallback are prior art.

Limitation / reviewer boundary: Reported confidence gate loses useful adaptation under many-class overconfidence; source statistics and BN-folded convolutional deployment requirements differ from generic backbones. Its result is not a universal safety guarantee.

[Source ledger](../../notes/shift-aware-tta-review-reviewer-sources.json).

### Other stored metadata

```json
{
  "html_url": "https://arxiv.org/html/2609.01683v1",
  "pdf_url": null
}
```


## Sabour2026DriftTTA

**Hidden Trajectories Don't Lie: Correcting Corruption Drift for Test-Time Adaptation**

Authors: Amirhossein Sabour; Amir Khasahmadi; Mengliu Zhao.

Publication: 2026; arXiv:2610.24220v1.

Primary source: [Hidden Trajectories Don't Lie: Correcting Corruption Drift for Test-Time Adaptation](https://arxiv.org/abs/2610.24220). [Project paper note](../../papers/Sabour2026DriftTTA.md).

Publication qualification: Preprint submitted 16 October 2026; no accepted venue verified.

Recorded reading scope: Primary metadata, abstract, introduction, Sections 3.1–3.3 and setting table; selective reading.

Inspected locations: Sections 3.1–3.3; Tables 1–2; Appendix D heading.

Relevance / overlap from our reading: Learns offline hidden-trajectory correction adapters; online entropy optimization changes correction-strength scalars. Intermediate-feature shift gates are prior art.

Limitation / reviewer boundary: Source-free training still uses corrupted/further-corrupted pairs; Table 1 describes episodic online adaptation. Held-out-family training details need full audit before comparisons.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

[Source ledger](../../notes/review-refresh-2026-10-26/lead-sources.json).

### Recorded reading history

- **2026-10-26**: Primary metadata, abstract, introduction, Sections 3.1–3.3 and setting table; selective reading.
  Locations: Sections 3.1–3.3; Tables 1–2; Appendix D heading.
  Qualification: Source-free training still uses corrupted/further-corrupted pairs; Table 1 describes episodic online adaptation. Held-out-family training details need full audit before comparisons.
  [Dated ledger](../../notes/review-refresh-2026-10-26/lead-sources.json).

### Other stored metadata

```json
{
  "entry_type": "misc",
  "html_url": "https://arxiv.org/html/2610.24220v1"
}
```


## Shamsi2026MultiHypothesis

**Multi-Hypothesis Test-Time Adaptation to Mitigate Underspecification**

Authors: Afshar Shamsi; Xiao-Yu Guo; Hamid Alinejad-Rokny; Arash Mohammadi; Damien Teney; Ehsan Abbasnejad.

Publication: 2026; arXiv preprint 2607.00259.

Primary source: [Multi-Hypothesis Test-Time Adaptation to Mitigate Underspecification](https://arxiv.org/abs/2607.00259). [Project paper note](../../papers/Shamsi2026MultiHypothesis.md).

Publication qualification: arXiv v1 submitted30June2026; no independently verified venue

Recorded reading scope: arXiv metadata/abstract, §§3-4 and appendicesH-I; partial reading.

Inspected locations: Sections3-4; Appendix0.H Runtime; Appendix0.I Limitation.

Relevance / overlap from our reading: Population-based diversification of output, parameters, optimizer and inputs creates multiple adaptation hypotheses; mixed-shift, small-batch and label-shift evaluation.

Limitation / reviewer boundary: Runtime grows roughly with particle count; reported gains are author results, not independent evidence that this wrapper dominates all protocols.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

[Source ledger](../../notes/review-refresh-2026-10-26/verifier-sources.json).

### Recorded reading history

- **2026-10-26**: arXiv metadata/abstract, §§3-4 and appendicesH-I; partial reading.
  Locations: Sections3-4; Appendix0.H Runtime; Appendix0.I Limitation.
  Qualification: Runtime grows roughly with particle count; reported gains are author results, not independent evidence that this wrapper dominates all protocols.
  [Dated ledger](../../notes/review-refresh-2026-10-26/verifier-sources.json).

### Other stored metadata

```json
{
  "html_url": "https://arxiv.org/html/2607.00259v1",
  "accessed": "2026-10-26"
}
```


## Sreeram2026Tempora

**Tempora: Characterising the Time-Contingent Utility of Online Test-Time Adaptation**

Authors: Sudarshan Sreeram; Young D. Kwon; Cecilia Mascolo.

Publication: 2026; ICML, PMLR 306:115420–115456.

Primary source: [Tempora: Characterising the Time-Contingent Utility of Online Test-Time Adaptation](https://proceedings.mlr.press/v306/sreeram26a.html). [Project paper note](../../papers/Sreeram2026Tempora.md).

Publication qualification: conference paper; inspected arXiv v2 dated 31 May 2026

Recorded reading scope: Fresh proceedings abstract/metadata; selective author PDF utility definitions

Inspected locations: Abstract; sections3 utility definitions.

Relevance / overlap from our reading: Method utility under physical deadlines, latency penalties and amortized compute budgets; ranking changes with hardware and shift.

Limitation / reviewer boundary: Main episodic IID/default-hyperparameter comparisons leave integration with continual/nonstationary realism as future work; latency-aware ranking itself is established.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

Recorded implementation/author resource: [link](https://github.com/sudotensor/tempora). Availability/role follows the reading qualification; no execution is implied.

[Preserved primary PDF](../../sources/pdfs/Sreeram2026Tempora.pdf).

[Source ledger](../../notes/review-refresh-2026-10-26/benchmarks-sources.json).

### Recorded reading history

- **2026-10-23**: Sections 3–5, version metadata and hardware appendix descriptions
  Locations: Sections 3.1–3.3; Section 4; Section 5, Limitations/Future Work; Appendix C.8.
  Qualification: Main episodic IID/default-hyperparameter comparisons leave integration with continual/nonstationary realism as future work; latency-aware ranking itself is established.
  [Dated ledger](../../notes/shift-aware-tta-review-verifier-sources.json).

- **2026-10-26**: Fresh proceedings abstract/metadata; selective author PDF utility definitions
  Locations: Abstract; sections3 utility definitions.
  Qualification: Ranking depends on time objective and hardware; utility must be fixed before comparing.
  [Dated ledger](../../notes/review-refresh-2026-10-26/benchmarks-sources.json).

### Other stored metadata

```json
{
  "pdf_url": "https://raw.githubusercontent.com/mlresearch/v306/main/assets/sreeram26a/sreeram26a.pdf",
  "pdf_sha256": "c82b4a7bdb3be2502bb954d7ba30d63ae3f5d19376a3f48c30ffa28369c8fcbf",
  "refresh_read_scope": "Fresh proceedings abstract/metadata; selective author PDF utility definitions",
  "refresh_locations": "Abstract; sections3 utility definitions",
  "refresh_limitation": "Ranking depends on time objective and hardware; utility must be fixed before comparing.",
  "verified_on": "2026-10-26"
}
```


## Su2026SLRF

**Shift-level regulated continual test-time adaptation framework**

Authors: Rui Su; Hang Xu; Wendong Zheng; Husheng Guo; Wenjian Wang.

Publication: 2026; Data Mining and Knowledge Discovery 40, article 63.

Primary source: [Shift-level regulated continual test-time adaptation framework](https://link.springer.com/article/10.1007/s10618-026-01222-x). [Project paper note](../../papers/Su2026SLRF.md).

Verified DOI in saved record: `10.1007/s10618-026-01222-x`.

Publication qualification: Published 2 July 2026; DOI 10.1007/s10618-026-01222-x

Recorded reading scope: Fresh Springer publisher metadata and abstract only; subscription full text unavailable.

Inspected locations: Abstract; Publication metadata.

Relevance / overlap from our reading: Adaptive detector classifies aligned/weak/strong shift; strategy decision module routes accordingly.

Limitation / reviewer boundary: Full method, exact state dependencies and tests remain inaccessible. Cannot exclude exact controller overlap from abstract alone.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

[Source ledger](../../notes/review-refresh-2026-10-26/researcher-sources.json).

### Recorded reading history

- **2026-10-23**: Publisher abstract, metadata, data availability and visible reference list; subscription full text not read.
  Locations: Abstract; Data Availability.
  Qualification: Exact detector, objectives and protocol require full text. Do not infer omitted experiments from paywall. No code verified.
  [Dated ledger](../../notes/shift-aware-tta-review-researcher-sources.json).

- **2026-10-26**: Fresh Springer publisher metadata and abstract only; subscription full text unavailable.
  Locations: Abstract; Publication metadata.
  Qualification: Full method, exact state dependencies and tests remain inaccessible. Cannot exclude exact controller overlap from abstract alone.
  [Dated ledger](../../notes/review-refresh-2026-10-26/researcher-sources.json).

### Other stored metadata

```json
{
  "pdf_url": null
}
```


## TestTimeLearning2026Leaderboard

**Test-Time Adaptation Leaderboard**

Authors: Test-Time-Learning maintainers.

Publication: Publication year unknown; documentation accessed 2026; Living benchmark website and repository.

Primary source: [Test-Time Adaptation Leaderboard](https://test-time.cc/tta-leaderboard/). [Project paper note](../../papers/TestTimeLearning2026Leaderboard.md).

Publication qualification: Live website/repository verified26October2026; scholarly publication not established

Recorded reading scope: Full about/protocol/efficiency documentation; no underlying runs reproduced

Inspected locations: About; Tasks Benchmarks Source Models; Protocols and Efficiency; Code and Reproduce.

Relevance / overlap from our reading: Shared-framework five-seed performance across classification/segmentation/detection, fixed models, RTX4090 cost; online/continual/Dirichlet settings.

Limitation / reviewer boundary: Website code link remains TBD; reproductions/independence not verified. No cross-source SOTA ranking inferred.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

Recorded implementation/author resource: [link](https://github.com/Test-Time-Learning/tta-leaderboard). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/review-refresh-2026-10-26/benchmarks-sources.json).

### Recorded reading history

- **2026-10-26**: Full about/protocol/efficiency documentation; no underlying runs reproduced
  Locations: About; Tasks Benchmarks Source Models; Protocols and Efficiency; Code and Reproduce.
  Qualification: Website code link remains TBD; reproductions/independence not verified. No cross-source SOTA ranking inferred.
  [Dated ledger](../../notes/review-refresh-2026-10-26/benchmarks-sources.json).

### Other stored metadata

```json
{
  "verified_on": "2026-10-26",
  "kind": "benchmark_documentation"
}
```


## WILDS2026SubmissionRules

**WILDS leaderboard submission guidelines**

Authors: WILDS benchmark maintainers.

Publication: Publication year unknown; documentation accessed 2026; Official benchmark documentation.

Primary source: [WILDS leaderboard submission guidelines](https://wilds.stanford.edu/submit/). [Project paper note](../../papers/WILDS2026SubmissionRules.md).

Publication qualification: Official live documentation accessed26October2026

Recorded reading scope: Full standard/non-standard submission rules and current leaderboard metric headers

Inspected locations: Standard submissions items1-7; Non-standard submissions items1-2; Dataset-specific leaderboard headers.

Relevance / overlap from our reading: Test training and model selection prohibited even for non-standard submissions; batch statistics prohibited standard; designated unlabeled adaptation is different.

Limitation / reviewer boundary: Accessed2026 date is not publication date. Official leaderboard contains historical ARM-BN and Test-time BN adaptation baseline rows; these do not establish permission for new test-trained submissions. Inference-only adaptation legality should not be blanket asserted. Declare a custom online-updating research protocol separately.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

[Source ledger](../../notes/review-refresh-2026-10-26/benchmarks-sources.json).

### Recorded reading history

- **2026-10-26**: Full standard/non-standard submission rules and current leaderboard metric headers
  Locations: Standard submissions items1-7; Non-standard submissions items1-2; Dataset-specific leaderboard headers.
  Qualification: Accessed2026 date is not publication date. Official leaderboard contains historical ARM-BN and Test-time BN adaptation baseline rows; these do not establish permission for new test-trained submissions. Inference-only adaptation legality should not be blanket asserted. Declare a custom online-updating research protocol separately.
  [Dated ledger](../../notes/review-refresh-2026-10-26/benchmarks-sources.json).

### Other stored metadata

```json
{
  "verified_on": "2026-10-26",
  "kind": "benchmark_documentation",
  "related_urls": [
    "https://wilds.stanford.edu/leaderboard/",
    "https://wilds.stanford.edu/datasets/"
  ]
}
```


## Wakayama2026DecisionTTT

**A Decision-Theoretic View of Test-Time Training: When, How Far, and Which Directions to Adapt**

Authors: Tomoya Wakayama.

Publication: 2026; Proceedings of the 43rd International Conference on Machine Learning, PMLR 306:124279–124317.

Primary source: [A Decision-Theoretic View of Test-Time Training: When, How Far, and Which Directions to Adapt](https://proceedings.mlr.press/v306/wakayama26a.html). [Project paper note](../../papers/Wakayama2026DecisionTTT.md).

Publication qualification: ICML 2026 primary PMLR publication verified; arXiv v2 revised 19 October 2026.

Recorded reading scope: Fresh PMLR abstract/citation metadata and linked arXiv version history.

Inspected locations: PMLR abstract; PMLR citation metadata.

Relevance / overlap from our reading: Decision-theoretic kernel/linear-Gaussian analysis covers evidence-based step selection and update-subspace scoring.

Limitation / reviewer boundary: Theoretical results require stated surrogate assumptions; no full proof or applicability audit. Not a visual continual-controller implementation.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

[Source ledger](../../notes/review-refresh-2026-10-26/researcher-sources.json).

### Recorded reading history

- **2026-10-26**: Fresh PMLR abstract/citation metadata and linked arXiv version history.
  Locations: PMLR abstract; PMLR citation metadata.
  Qualification: Theoretical results require stated surrogate assumptions; no full proof or applicability audit. Not a visual continual-controller implementation.
  [Dated ledger](../../notes/review-refresh-2026-10-26/researcher-sources.json).

### Other stored metadata

```json
{
  "arxiv_url": "https://arxiv.org/abs/2606.15569"
}
```


## Weerasinghe2026LATTA

**Logit-Adjusted Test-Time Adaptation under Partial Class Imbalance**

Authors: Thilina Weerasinghe; Ruwan Tennakoon; WeiQin Chuah; Alireza Bab-Hadiashar.

Publication: 2026; Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision, pages 5977-5985.

Primary source: [Logit-Adjusted Test-Time Adaptation under Partial Class Imbalance](https://openaccess.thecvf.com/content/WACV2026/html/Weerasinghe_Logit-Adjusted_Test-Time_Adaptation_under_Partial_Class_Imbalance_WACV_2026_paper.html). [Project paper note](../../papers/Weerasinghe2026LATTA.md).

Verified DOI in saved record: `10.1109/WACV61042.2026.00578`.

Publication qualification: WACV2026 official proceedings and IEEE DOI verified

Recorded reading scope: Official CVF/IEEE metadata, abstract, visible official PDF §3 drift argument and supplemental simplified derivation. Partial reading; later direct PDF fetch returned403.

Inspected locations: Abstract; Section 3.1; Supplementary theoretical analysis; IEEE DOI.

Relevance / overlap from our reading: Long-term partial-class TTA, BN beta drift, target-prior logit adjustment and evaluations on CIFAR100-C/ImageNet-C/DomainNet126.

Limitation / reviewer boundary: Specific partial-class setting and simplified drift analysis; neither arbitrary cause inference nor pre-action whole-method safety guarantee. Full experiments not audited.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

Recorded implementation/author resource: [link](https://github.com/thilinawee/latta). Availability/role follows the reading qualification; no execution is implied.

[Source ledger](../../notes/review-refresh-2026-10-26/verifier-sources.json).

### Recorded reading history

- **2026-10-26**: Official CVF/IEEE metadata, abstract, visible official PDF §3 drift argument and supplemental simplified derivation. Partial reading; later direct PDF fetch returned403.
  Locations: Abstract; Section 3.1; Supplementary theoretical analysis; IEEE DOI.
  Qualification: Specific partial-class setting and simplified drift analysis; neither arbitrary cause inference nor pre-action whole-method safety guarantee. Full experiments not audited.
  [Dated ledger](../../notes/review-refresh-2026-10-26/verifier-sources.json).

### Other stored metadata

```json
{
  "pdf_url": "https://openaccess.thecvf.com/content/WACV2026/papers/Weerasinghe_Logit-Adjusted_Test-Time_Adaptation_under_Partial_Class_Imbalance_WACV_2026_paper.pdf",
  "accessed": "2026-10-26"
}
```


## Yang2026SATTS

**SA-TTS: Stress-Aware Test-Time Scaling for Vision Models**

Authors: Youla Yang.

Publication: 2026; Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops, pages 11480–11487.

Primary source: [SA-TTS: Stress-Aware Test-Time Scaling for Vision Models](https://openaccess.thecvf.com/content/CVPR2026W/Viscale/html/Yang_SA-TTS_Stress-Aware_Test-Time_Scaling_for_Vision_Models_CVPRW_2026_paper.html). [Project paper note](../../papers/Yang2026SATTS.md).

Publication qualification: CVPR 2026 workshop proceedings; primary CVF metadata verified

Recorded reading scope: Downloaded official CVF PDF: title/author block, abstract, Algorithm 1, methodology and scope discussion; partial reading.

Inspected locations: Abstract; Methodology; Algorithm 1.

Relevance / overlap from our reading: Staged acquisition: entropy/margin first, augmentation disagreement when needed, then multi-crop inference. Blocks a generic novelty claim about escalating evidence on uncertain inputs.

Limitation / reviewer boundary: Inspected terminal actions are inference policies with a fixed backbone rather than selection among parameter-update TTA methods. Detailed experiments were not audited by reviewer.

[Preserved primary PDF](../../sources/pdfs/Yang2026SATTS.pdf).

[Source ledger](../../notes/shift-aware-tta-review-reviewer-sources.json).

### Other stored metadata

```json
{
  "pdf_url": "https://openaccess.thecvf.com/content/CVPR2026W/Viscale/papers/Yang_SA-TTS_Stress-Aware_Test-Time_Scaling_for_Vision_Models_CVPRW_2026_paper.pdf",
  "pdf_sha256": "b64b9378e1fbcba3790eb136c524b94d6207744a6bd8fbcf29ec08a1efcf7792"
}
```


## Zhang2026MoASEPlusPlus

**MoASE++: Mixture of Activation Sparsity Experts with Domain-Adaptive On-policy Distillation for Continual Test Time Adaptation**

Authors: Ronyu Zhang; Aosong Cheng; Gaole Dai; Yulin Luo; Jiaming Liu; Li Du; Huanrui Yang; Dan Wang; Leyuan Fang; Yuan Du; Shanghang Zhang.

Publication: 2026; arXiv preprint.

Primary source: [MoASE++: Mixture of Activation Sparsity Experts with Domain-Adaptive On-policy Distillation for Continual Test Time Adaptation](https://arxiv.org/abs/2605.17743). [Project paper note](../../papers/Zhang2026MoASEPlusPlus.md).

Publication qualification: arXiv2605.17743v1,18May2026; no venueverified

Recorded reading scope: Abstract, routing description and section 5.2 including equations 11–16 from downloaded PDF; partial reading.

Inspected locations: Section 5.2; Equations 11–16.

Relevance / overlap from our reading: Domain-aware router weights experts using texture cues; entropy/confidence condition augmentation policy and EMA distillation.

Limitation / reviewer boundary: Learned augmentation strength uses a teacher-distillation/strength reward. That is close prior art for policy-driven augmentation, not an audited costed whole-method evidence selector. No implementation execution.

[Preserved primary PDF](../../sources/pdfs/Zhang2026MoASEPlusPlus.pdf).

[Source ledger](../../notes/shift-aware-tta-review-researcher-sources.json).

### Other stored metadata

```json
{
  "pdf_url": "https://arxiv.org/pdf/2605.17743v1",
  "pdf_sha256": "c7fb3cc9619af9f30b457a524999ad99032cf35f0b52e37c8bad9c0c63993051"
}
```


## Zhang2026PhysicalDiagnosis

**When Does Test-Time Physical Diagnosis Pay? A Frozen Policy Buys Evidence It Never Reads**

Authors: Zhengshu Zhang.

Publication: 2026; arXiv:2609.22299v1.

Primary source: [When Does Test-Time Physical Diagnosis Pay? A Frozen Policy Buys Evidence It Never Reads](https://arxiv.org/abs/2609.22299v1). [Project paper note](../../papers/Zhang2026PhysicalDiagnosis.md).

Publication qualification: Preprint submitted 14 September 2026

Recorded reading scope: Primary metadata, abstract and introduction; full experiments not audited

Inspected locations: Abstract; Section 1.

Relevance / overlap from our reading: Separates identifying context, using acquired evidence, decision value, selection value over a fixed action and safe realization. Supports distinct headroom/evidence-use diagnostics.

Limitation / reviewer boundary: Robotics rather than visual-classification TTA; cannot be treated as a matched numerical baseline or proof that the candidate is novel.

[Source ledger](../../notes/shift-aware-tta-review-reviewer-sources.json).

### Other stored metadata

```json
{
  "html_url": "https://arxiv.org/html/2609.22299v1",
  "pdf_url": null
}
```


## Zhao2026FACTOR

**FACTOR: Counterfactual Training-Free Test-Time Adaptation for Open-Vocabulary Object Detection**

Authors: Kaixiang Zhao; Mao Ye; Lihua Zhou; Hu Wang; Luping Ji; Song Tang; Xiatian Zhu.

Publication: 2026; arXiv preprint.

Primary source: [FACTOR: Counterfactual Training-Free Test-Time Adaptation for Open-Vocabulary Object Detection](https://arxiv.org/abs/2605.03294). [Project paper note](../../papers/Zhao2026FACTOR.md).

Publication qualification: arXiv v1, 5 May 2026; no venue verified.

Recorded reading scope: Fresh arXiv abstract/metadata only.

Inspected locations: Abstract.

Relevance / overlap from our reading: Attribute perturbations probe region sensitivity and suppress attribute-dependent detections without gradient updates.

Limitation / reviewer boundary: Counterfactual input probing is already prior art; distinct from comparing update policies from a cloned live model state. Experiments not audited.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

[Source ledger](../../notes/review-refresh-2026-10-26/researcher-sources.json).

### Recorded reading history

- **2026-10-26**: Fresh arXiv abstract/metadata only.
  Locations: Abstract.
  Qualification: Counterfactual input probing is already prior art; distinct from comparing update policies from a cloned live model state. Experiments not audited.
  [Dated ledger](../../notes/review-refresh-2026-10-26/researcher-sources.json).


## Zhou2026Learnability

**On the Learnability of Test-Time Adaptation: A Recovery Complexity Perspective**

Authors: Zhi Zhou; Ming Yang; Shi-Yu Tian; Kun-Yang Yu; Lan-Zhe Guo; Yu-Feng Li.

Publication: 2026; ICML 2026, PMLR 306:166172–166195.

Primary source: [On the Learnability of Test-Time Adaptation: A Recovery Complexity Perspective](https://proceedings.mlr.press/v306/zhou26be.html). [Project paper note](../../papers/Zhou2026Learnability.md).

Publication qualification: Official ICML 2026 proceedings verified; linked arXiv is the same work.

Recorded reading scope: Official PMLR metadata; arXiv v2 §§2-4 assumptions/definitions, §7 limitations, selected proof discussion. Partial reading; no proof verification.

Inspected locations: Assumptions2.1-2.2; Assumptions2.4 and2.7; Sections3-4; Section7.

Relevance / overlap from our reading: Recovery complexity, learnability, dynamic regret, effective batch size under dependence and proxy/task alignment.

Limitation / reviewer boundary: Structural assumptions on proxy alignment and losses; not guarantees for arbitrary deep entropy adaptation. Paper leaves comprehensive empirical/large-scale study to future work.

Fresh inspection date recorded by the earlier review: 2026-10-26. This is not the handoff-export date.

[Source ledger](../../notes/review-refresh-2026-10-26/verifier-sources.json).

### Recorded reading history

- **2026-10-26**: Fresh arXiv metadata/abstract, author project assumptions and official ICML download index title.
  Locations: Abstract; Author project Framework/Motivation; Official ICML 2026 download index.
  Qualification: Requires alignment and nonstationarity assumptions; does not make unlabeled task risk observable. Full proofs not audited.
  [Dated ledger](../../notes/review-refresh-2026-10-26/researcher-sources.json).

- **2026-10-26**: Official proceedings abstract and metadata only; full proofs not read
  Locations: Abstract; Official BibTeX.
  Qualification: Cannot rely on specific bounds without reading assumptions/proofs; abstract does not imply a deployable selector guarantee.
  [Dated ledger](../../notes/review-refresh-2026-10-26/benchmarks-sources.json).

- **2026-10-26**: Official PMLR metadata; arXiv v2 §§2-4 assumptions/definitions, §7 limitations, selected proof discussion. Partial reading; no proof verification.
  Locations: Assumptions2.1-2.2; Assumptions2.4 and2.7; Sections3-4; Section7.
  Qualification: Structural assumptions on proxy alignment and losses; not guarantees for arbitrary deep entropy adaptation. Paper leaves comprehensive empirical/large-scale study to future work.
  [Dated ledger](../../notes/review-refresh-2026-10-26/verifier-sources.json).

### Other stored metadata

```json
{
  "project_url": "https://zhouz.dev/TTA-Learnability/",
  "verified_on": "2026-10-26",
  "html_url": "https://arxiv.org/html/2605.28057v2",
  "pdf_url": "https://raw.githubusercontent.com/mlresearch/v306/main/assets/zhou26be/zhou26be.pdf",
  "accessed": "2026-10-26",
  "arxiv_url": "https://arxiv.org/abs/2605.28057"
}
```


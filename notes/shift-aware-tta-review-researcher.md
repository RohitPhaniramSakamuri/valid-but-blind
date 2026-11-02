# Researcher findings: shift-aware dynamic TTA selection

Date: 23 October 2026. Scope: targeted primary-source search and selected method/limitation reading. No model or benchmark was run. No claim of exhaustive coverage or established novelty.

## Assessment

The submitted abstract's core architecture already has direct predecessors. SLRF detects shift levels and selects adaptation strategies; Hybrid-TTA detects domain changes and switches full/efficient tuning; MORPHEUS predicts whole-method utility before adaptation. Distinguish expert routing, parameter selection and whole-method selection, but do not use the distinction to dismiss substantial conceptual overlap.

The strongest conceptual boundary is the Jhawar–Wang identifiability paper: an unlabeled signal may erase variables that change action rankings. Changing the selector architecture cannot restore erased information. That paper already checks stream-aware evidence and held-out corruption/DomainNet transfers. The verifier is examining it in detail; do not propose those features alone as the gap.

## Closest primary sources

Reading below is partial unless explicitly described. Metadata, reading locations and access limits are also recorded in [the source JSON](shift-aware-tta-review-researcher-sources.json). Conference year and original preprint year can differ.

### Su2026SLRF

**Shift-level regulated continual test-time adaptation framework** — Rui Su, Hang Xu, Wendong Zheng, Husheng Guo, Wenjian Wang. Data Mining and Knowledge Discovery 40, article 63, 2026. [Primary record](https://link.springer.com/article/10.1007/s10618-026-01222-x).

- **Reading:** Publisher abstract, metadata, data availability and visible reference list; subscription full text not read. Locations: Abstract; Data Availability.
- **Overlap:** ASLD categorizes aligned/weak/strong shifts; ASDM selects corresponding adaptation strategies. This directly overlaps shift inference followed by policy selection.
- **Limit:** Exact detector, objectives and protocol require full text. Do not infer omitted experiments from paywall. No code verified.

### Park2025HybridTTA

**Hybrid-TTA: Continual Test-time Adaptation via Dynamic Domain Shift Detection** — Hyewon Park, Hyejin Park, Jueun Ko, Dongbo Min. ICCV 2025, 2025. [Primary record](https://arxiv.org/abs/2409.08566).

- **Reading:** Abstract, introduction, section 4 mechanism and experiment/appendix headings; selected results, not exhaustive full paper. Locations: Section 4.1 Dynamic Domain Shift Detection; Section 4.2 Masked Image Modeling Adaptation; Section 5; Appendix source forgetting/long-term adaptation.
- **Overlap:** Teacher/student discrepancy with dynamic loss thresholding detects domain changes and switches between full tuning and adapter tuning for each input.
- **Limit:** Segmentation-specific FT/ET menu and reconstruction preparation; not a general selector over arbitrary TTA algorithms. Still invalidates broad novelty of dynamic policy switching.

### Lee2024BECoTTA

**BECoTTA: Input-dependent Online Blending of Experts for Continual Test-time Adaptation** — Daeun Lee, Jaehong Yoon, Sung Ju Hwang. ICML 2024, PMLR 235:27072–27093, 2024. [Primary record](https://proceedings.mlr.press/v235/lee24ab.html).

- **Reading:** Abstract, introduction, method and benchmark design descriptions plus author project page. Locations: Section 3.2 Domain-Augmented Initialization; Section 3.3 MoDE; Section 3.4 CTTA process; Continual gradual shifts construction.
- **Overlap:** Pseudo-domain inference routes inputs to low-rank experts; updates relevant experts and blends domain-adaptive knowledge.
- **Limit:** Expert routing is distinct from selecting complete standalone TTA methods. Initialization and source augmentation variants must be distinguished; gradual/mixed shifts alone are covered.
- **Author-linked code:** https://github.com/daeunni/becotta

### Danilowski2026MORPHEUS

**MORPHEUS: Meta Test-Time Adaptation via Neural Collapse Geometry** — Michal Danilowski, Alexander Murphy, Young D. Kwon, Abhirup Ghosh. ICLR 2026 Test-Time Updates Workshop, 2026. [Primary record](https://openreview.net/forum?id=YfyApJH1Rj).

- **Reading:** Indexed primary OpenReview PDF abstract, introduction and section 2 excerpts; live direct PDF fetch encountered browser challenge. Locations: Abstract; Introduction contributions; Section 2 Problem and Methodology.
- **Overlap:** Predicts per-TTA post-adaptation accuracy from source-model entropy and Neural-Collapse embedding statistics, then selects a complete TTA method without executing all candidates. Direct collision with a learned pre-adaptation router.
- **Limit:** Detailed meta-training split/code require further verification. Do not claim feature-only method selection or cheap single-forward routing is new.

### Lim2023TTN

**TTN: A Domain-Shift Aware Batch Normalization in Test-Time Adaptation** — Hyesu Lim, Byeonggeun Kim, Jaegul Choo, Sungha Choi. ICLR 2023, 2023. [Primary record](https://arxiv.org/abs/2302.05155).

- **Reading:** Abstract and author project-page sections on layer/channel shift sensitivity and post-training. Locations: Method: Test-Time Normalization Layer; Post-training prior; Optimize interpolating weights.
- **Overlap:** Combines source and current-batch normalization using layer/channel shift sensitivity; shifts alter appropriate reliance on source/test statistics.
- **Limit:** Interpolation weights are learned using labeled source data during post-training and frozen at deployment. Do not conflate this with label-free source preparation or whole-method routing.

### Ye2025DATTA

**DATTA: Domain Diversity Aware Test-Time Adaptation for Dynamic Domain Shift Data Streams** — Chuyang Ye, Dongyan Wei, Zhendong Liu, Yuanyi Pang, Yixi Lin, Qinting Jiang, Jingyan Jiang, Dongbiao He. ICME 2025, 2025. [Primary record](https://arxiv.org/abs/2408.08056).

- **Reading:** Abstract, introduction, method overview and section headings. Locations: Section III-A Domain-Diversity Discrimination; Section III-B DABN; Section III-C DAFT.
- **Overlap:** Recognizes single-versus-multiple-domain batches, changes normalization interpolation and selectively fine-tunes to mitigate gradient conflict.
- **Limit:** Domain diversity is not physical shift-cause identification. Dynamic heterogeneous input batches already studied; a generic multi-domain claim is insufficient.
- **Author-linked code:** https://github.com/DYW77/DATTA

### Sahoo2025GALA

**A Layer Selection Approach to Test Time Adaptation** — Sabyasachi Sahoo, Mostafa ElAraby, Jonas Ngnawe, Yann Pequignot, Frederic Precioso, Christian Gagne. AAAI 2025, 2025. [Primary record](https://arxiv.org/abs/2404.03784).

- **Reading:** Abstract, introduction, section2 description, discussion/appendix analysis of current gradients versus accumulated state. Locations: Section 2.1 layer selection; Section 2.2 cosine criterion; Section 2.3 reset; Appendix A.5.4 alignment vs magnitude.
- **Overlap:** Uses proposed gradients relative to accumulated parameter displacement to select one layer, skip updates or reset alignment history. Adaptation utility depends on state, loss and shift.
- **Limit:** Selecting update layers is not arbitrary whole-method selection, but state/drift/gradient features and skip/reset are established; cannot sell these alone as a gap.

### Karimi2026ShiftACT

**Shift-ACT: Test-time adaptation via shift-aware class-specific dynamic thresholding for domain generalization** — Saeed Karimi, Hamdi Dibeklioglu. Neurocomputing 663, article132013, 2026. [Primary record](https://www.sciencedirect.com/science/article/pii/S0925231225026852).

- **Reading:** Publisher abstract/metadata and author repository README. Locations: Abstract; Repository preparation/run instructions.
- **Overlap:** Class-specific source-target confidence gaps adjust thresholds; reliable samples get entropy minimization, unreliable samples get prototype contrastive alignment.
- **Limit:** Source-derived class confidence information required; selected method passages/full detailed protocol not read. Class-wise signal-dependent objective choice is already present.
- **Author-linked code:** https://github.com/saeedkarimi90/Shift-act

### Grover2025DynaTTA

**Shift-Aware Test Time Adaptation and Benchmarking for Time-Series Forecasting** — Shivam Grover, Ali Etemad. ICML 2025 Workshop on Test-Time Adaptation: Putting Updates to the Test!, 2025. [Primary record](https://openreview.net/forum?id=a399SmgWGl).

- **Reading:** Indexed primary PDF abstract/introduction excerpts, official workshop list and author talk summary. Locations: Abstract; Introduction dynamic rate and shift-conditioned gating; Official workshop acceptedpaper61.
- **Overlap:** Prediction-error and embedding-drift signals control adaptation rate and reliance on adapted outputs, with synthetic shifted forecast benchmark.
- **Limit:** Forecasting can reveal past outcomes as future inputs; does not automatically satisfy strict label-free classification protocol.
- **Author-linked code:** https://github.com/shivam-grover/DynaTTA

### Kumar2026RGTTA

**RG-TTA: Regime-Guided Meta-Control for Test-Time Adaptation in Streaming Time Series** — Indar Kumar, Akanksha Tiwari, Sai Krishna Jasti, Ankit Hemant Lade. arXiv preprint, 2026. [Primary record](https://arxiv.org/abs/2603.27814).

- **Reading:** Abstract,introduction,method outline and limitations/ablation table of contents. Locations: III-C continuous regime guidance; III-F checkpoint management; VII-H component contribution; IX Limitations.
- **Overlap:** Uses similarity to stored regimes to scale learning rate, stop updates when loss plateaus and reuse checkpoints only when predicted loss benefit passes a gate.
- **Limit:** Temporal forecasting setup has observed outcomes; checkpoint bank/rate controller is not fully unlabeled image-classification method selection.
- **Author-linked code:** https://github.com/IndarKarhana/RGTTA-Regime-Guided-Test-Time-Adaptation

### Gai2026AdaTentPlusPlus

**AdaTent++: reliability-guided hybrid test-time adaptation for traffic sign detection under distribution shift** — Xiaomei Gai, Meichun Wang, Yantong Guo, Shiyu Wang, Ye Li, Rui Fu. Frontiers in Signal Processing6, 2026. [Primary record](https://www.frontiersin.org/journals/signal-processing/articles/10.3389/frsip.2026.1842851/full).

- **Reading:** Publisher full text selectively read: abstract, sections2.1–2.4, ablations, discussion, limitations and conclusion. Locations: 2.3 multiview reliability and dynamic routing; 2.4 threepath mechanics; 3.4 ablations; 4 Discussion; 5 Limitations; 6 Conclusion item4.
- **Overlap:** Entropy and multiview agreement route to BN-stat update, guarded BN-affine update or skip; EMA/hysteresis, dynamic1–2steps and BN rollback stabilize.
- **Limit:** §5 admits benchmark-condition IDs for views/filtering, one deterministic run and no longstream. §4 says not compute-matched despite conflicting conclusion wording. §6 requests budget-aware adaptive viewcount/step controllers. No guarantees verified.

### Jhawar2026HDTTA

**HD-TTA: Hypothesis-Driven Test-Time Adaptation for Safer Brain Tumor Segmentation** — Kartik Jhawar, Lipo Wang. MICCAI2026 (official page found); inspected arXiv preprint, 2026. [Primary record](https://arxiv.org/abs/2602.19454).

- **Reading:** arXiv abstract and official MICCAI paper-page abstract/review summaries; full method not read. Locations: Abstract; MICCAI2026 paper3549 review summaries.
- **Overlap:** Gatekeeper skips confident masks; competing compaction/inflation hypotheses are scored by intrinsic representation consistency to select safer refinement.
- **Limit:** Clinical binary segmentation proof of concept; not evidence a general classification method selector is new. Code was promised on acceptance; release not verified.

### Fan2026MoETTA

**MoETTA: Test-Time Adaptation Under Mixed Distribution Shifts with MoE-LayerNorm** — Xiao Fan, Jingyan Jiang, Zhaoru Chen, Fanding Huang, Xiao Chen, Qinting Jiang, Bowen Zhang, Xing Tang, Zhi Wang. AAAI2026 Main Technical Track, 2026. [Primary record](https://arxiv.org/abs/2511.13760).

- **Reading:** Abstract,introduction,routing/mechanism description and §5.3/table excerpts. Locations: Mixture-of-Experts LayerNorm routing; 5.3 Computation Efficiency; Potpourri/potpourri+ design.
- **Overlap:** LayerNorm experts permit sample-specific gradient directions under mixed shifts; potpourri mixes natural/artistic/adversarial shifts, potpourri+ includes source examples.
- **Limit:** Mixed domains/source returns are covered as benchmarks; action-menu policy selection and image-level composed corruptions remain distinct, but no novelty inferred from this distinction.
- **Author-linked code:** https://github.com/AnikiFan/MoETTA

### Doloriel2026SEGA

**Continual Test-Time Adaptation via Entropy Sensitivity-Guidance in Strict Online Setting** — Chandler Timm C. Doloriel, Yunbei Zhang, Muhammad Salman Siddiqui, Tor Kristian Stevik, Fadi Al Machot, Kristian Hovde Liland, Habib Ullah. arXiv preprint, 2026. [Primary record](https://arxiv.org/abs/2608.29920).

- **Reading:** arXiv abstract/metadata only; HTML unavailable and code link fetch failed. Locations: Abstract.
- **Overlap:** Structured erasure probes produce entropy-sensitivity trajectories for recovery/sample selection and reduce backward updates in batchsizeonecontinual streams.
- **Limit:** Evidence probes and sensitivity gating already proposed. Adaptive purchasing of probe types/counts is not established by the read abstract; fullmethod/code needed before negativeclaim.

### Zhang2026MoASEPlusPlus

**MoASE++: Mixture of Activation Sparsity Experts with Domain-Adaptive On-policy Distillation for Continual Test Time Adaptation** — Ronyu Zhang, Aosong Cheng, Gaole Dai, Yulin Luo, Jiaming Liu, Li Du, Huanrui Yang, Dan Wang, Leyuan Fang, Yuan Du, Shanghang Zhang. arXiv preprint, 2026. [Primary record](https://arxiv.org/abs/2605.17743).

- **Reading:** arXivabstractandmetadataonly. Locations: Abstract.
- **Overlap:** Domain-aware router weights experts using texture cues; entropy/confidence condition augmentation policy and EMA distillation.
- **Limit:** Dynamic expertcomposition and signal-conditioned augmentation arecovered. Fullimplementation/evaluationnotread; do not infer costed evidence acquisitionabsent.

## Candidate-gap audit

### Candidate A: adaptively acquire unlabeled evidence under a compute budget

**Precise question:** When a cheap pre-action router cannot clearly distinguish two adaptation actions, can selectively buying additional unlabeled observations improve the accuracy–latency frontier on held-out shift families, compared with always buying them, never buying them, or using confidence-only triggers?

A practical evidence ladder might begin with source outputs already required for inference, then buy two extra label-preserving views, then one bounded disposable update probe if the remaining budget permits. The selector predicts whether the richer evidence will resolve a decision with enough expected utility to justify its measured cost. Doing nothing is an explicit action. Stop collecting evidence when the ranking is sufficiently stable or the per-batch budget is exhausted.

**Why this is more specific:** MORPHEUS selects a method from fixed source-derived evidence. The identifiability paper studies what richer evidence can resolve; it does not, in the read sections, establish a learned costed acquisition schedule. EATA gates updates, SEGA obtains probe sensitivity, and expert methods route computation. Consequently the contribution would need to be the evidence-acquisition decision and a fair budgeted evaluation, rather than adding another uncertainty score or gating adaptation itself.

**Published limitation supporting investigation:** AdaTent++ §5 acknowledges benchmark-condition IDs for augmentation/candidate filtering, no longstream test and a single deterministic run. Its §6 explicitly proposes budget-aware controllers for view count and update steps. This is a request for future work, not proof that no other paper solved it. The paper also contains a compute-matching inconsistency between §4 and §6; do not cite its conclusion as proof of measured budget parity.

**Novelty status:** Candidate intersection after targeted search; not a verified open problem. Full SEGA and MoASE++ methods, relevant sequential experimental-design literature and current dynamic-TTA implementations still require inspection.

**Necessary ablations:** cheap-only router; always-rich router; randomized evidence schedule at equal measured cost; confidence/entropy triggers; learned acquisition with shuffled utility targets; oracle acquisition upper bound for diagnosis only. Account for evidence views, gradient probes, state snapshots, teachers and final selected adaptation. Separate offline calibration labels from hidden final target labels. A selector trained on labeled synthetic shifts is label-free at deployment, not label-free throughout development.

### Candidate B: policy utility conditional on the live adapted state

**Precise question:** For identical current batches, do different attainable parameter/buffer/optimizer/memory states reverse the best whole-policy decision, and can inexpensive state summaries predict that reversal and its delayed harm?

Generate paired states through disjoint development histories, clone all mutable state, execute counterfactual menu actions from the same state, and score immediate plus prespecified future effects on separate data. Restrict deployment to the chosen action; branch evaluation is an offline measurement device whose cost must still be disclosed. Include reset/keep rather than treating adaptation as compulsory.

**Overlap hazards:** GALA already conditions its layer decision on the proposed gradient relative to accumulated parameter displacement. Hybrid-TTA uses teacher/student temporal state. SAR, CoTTA and AdaTent++ already recover or restore state. RG-TTA stores/reuses regime specialists in forecasting. A method that merely concatenates weight drift or adds skip/rollback would be weakly differentiated.

**Novelty status:** Unverified empirical-design extension, not established new state-aware TTA. It is potentially expensive because policy utility depends on earlier actions; off-policy replay can be invalid when states diverge. Whole-method counterfactuals and delayed future costs must be defined precisely.

### Recommendation

Prefer Candidate A for a bounded first investigation if no closer method appears after remaining full-method checks. It has a concrete supporting future-work request and can be falsified at small scale. Candidate B is a strong diagnostic question but has greater state-control complexity and more overlap with existing history-dependent adaptation.

Reject or narrow either candidate if a single fixed method dominates after cost accounting, if the oracle policy menu has negligible headroom, or if the extra evidence fails to improve held-out action rankings. Do not promise a novel algorithm before this check.

## Search and access provenance

Primary query families included exact shift-aware/policy/strategy selection; adaptive TTA and mixtures of experts; cost-aware adaptation and value of information; current-state/optimizer/counterfactual selectors; skip/rollback policies; structured probes; and 2025/2026 recent papers. Search-result aggregators were used only as leads and replaced with author, arXiv, publisher or proceedings evidence.

Important corrections: DynaTTA is ICML **workshop**, and MORPHEUS is ICLR **workshop**. MoETTA is AAAI 2026 with a November 2025 preprint. DATTA's ICME 2025 record has a 2024 original preprint and revised 2025 title. SLRF is a July 2026 journal paper despite search indexing relative-date noise. MoASE++'s author list on arXiv spells the first author “Ronyu Zhang”; the submitter field says “Rongyu Zhang,” so verify the PDF before silently normalizing the name.

Access limitations: SLRF full text is subscription-only; several OpenReview direct requests hit browser challenges although indexed primary excerpts were accessible; SEGA abstract was accessible but HTML was unavailable. Claims of omitted features or experiments cannot be based on these access limits.

All excerpts were paraphrased; no paper's empirical claims were treated as independently reproduced.


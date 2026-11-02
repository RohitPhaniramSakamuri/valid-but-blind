# Independent verification and adversarial gap assessment

Date: 26 October 2026. Role: verifier in the Feynman literature-review/deep-research workflow. Scope: primary-source inspection, not a replication. No experiment, implementation test, package installation, or checkpoint/dataset download was performed. Previous project choices and digit outcomes were read as history; they do not select the new contribution.

## Assessment

The general proposal is not novel. The most dangerous omissions from a short bibliography would be learned method selection, domain-aware normalization, class-prior adaptation, state-dependent resets, and the very recent work on identifiability and learned TTT policies. An algorithm that detects a changed marginal distribution and selects an action is not enough. No verified conference-ready gap or empirical success has been established by this review.

The old three-feature normalization gate is particularly crowded: methods already protect normalization against class imbalance, infer target priors, estimate update reliability, and include a no-update option. A matched-concentration study can be an informative diagnostic; matching one summary is not evidence of a new identifiability theorem.

## Freshly checked collisions and boundaries

| Source | Relevant inspected evidence | Consequence for novelty |
| --- | --- | --- |
| [Jhawar and Wang 2026](https://arxiv.org/html/2609.11235v1), §§3.1–3.5, 4–5, 7 | Formalizes pre-action evidence and action regret; proves an observation ambiguity result; studies KEEP versus RECENTER and a class-prior/translation ambiguity; compares methods on CIFAR-100-C and DomainNet-126. | “The same input summary can require opposite actions,” KEEP as an action, and richer evidence restoring some decisions are direct predecessors. Preprint status; empirical findings are the authors' results. |
| [Hybrid-TTN / Channel-Selective Normalization](https://proceedings.mlr.press/v274/vianna25a.html), §§3–5 and Algorithms 1–2 in official PDF | Stores labeled-source, per-class channel sensitivities. First pass uses uniform class weights; predictions supply a prior for a second channel-selection pass. Experiments use offline single-batch adaptation, batch 500 on CIFAR/ImageNet. | Prior-aware, conservative normalization selection is already implemented. BN-only architecture and predeployment source-data access are explicit limits. Continual deployment is a protocol difference, but NOTE/DELTA/TRIBE already address continual imbalance. |
| [DELTA](https://arxiv.org/html/2301.13018v1), §§3.1–3.3 | Separates biased batch moments from dominant-class optimization, uses moving-statistics renormalization and online reweighting. | Corruption-induced prediction imbalance is not a new observation, and normalization plus prior correction is established. “Degradation-free” in the title is not an arbitrary-shift safety theorem. |
| [TRIBE](https://arxiv.org/html/2309.14949v2), methodology and protocol | Combines local imbalance, global imbalance and continual shifts; category-wise moments and anchored tri-net self-training. | “Evaluate both corruptions and changing class mixture” is necessary but not new. Pseudo-label error remains relevant; absence of labels does not verify the estimated class mixture. |
| [Label Shift Adapter](https://openaccess.thecvf.com/content/ICCV2023/papers/Park_Label_Shift_Adapter_for_Test-Time_Adaptation_under_Covariate_and_Label_ICCV_2023_paper.pdf), abstract and §5 | Estimates target priors and predicts adaptation parameters; discusses normalization sensitivity and extra adapter training. | Learned shift-conditioned parameter generation already exists. Must disclose source-stage preparation and avoid calling an extra trained controller weights-only TTA. |
| [Logit-Adjusted TTA, WACV 2026](https://openaccess.thecvf.com/content/WACV2026/html/Weerasinghe_Logit-Adjusted_Test-Time_Adaptation_under_Partial_Class_Imbalance_WACV_2026_paper.html), abstract, §3 and official supplement | Studies long sequences with only a subset of classes and BN shift-parameter drift; proposes target-prior-dependent entropy adjustment on CIFAR-100-C/ImageNet-C/DomainNet-126. | Partial class absence, long-term drift, and prior correction cannot be presented as untouched gaps. Derivation is a simplified model, not a universal diagnosis. |
| [TACT, NeurIPS 2025](https://arxiv.org/html/2510.11133v1), §§4–5, 7, Appendix C | Controlled augmentations and PCA identify directions treated as nuisance; representation and prototypes are trimmed. Explicitly requires knowledge for choosing transformations that preserve causal content. | “Probe the shift with augmentations” and “remove nuisance directions” are prior art. Causal identification does not follow merely from augmentation sensitivity. |
| [Multi-Hypothesis TTA](https://arxiv.org/html/2607.00259v1), §§3–4 and Appendices H–I | Diversifies adaptation trajectories rather than choosing a single entropy minimum. States runtime increases roughly with particle count. | Multiple candidate trajectories and uncertainty over adaptation solutions are established. Savings from avoiding multiple particles must charge equivalent evidence, not only trainable parameters. |

The source ledger records fresh metadata, reading scope and version limits. A paper not fully inspected is never marked fully read.

## Statistical safety and the strongest explicit limitations

[Monitoring Risks in TTA](https://arxiv.org/html/2507.08721v2), Assumption 1 and Proposition 1, obtains a lower risk bound from a loss proxy plus labeled-source calibration. Its §6 explicitly leaves unlabeled diagnostics of proxy-assumption violations open. Its §5.4 shows that uncertainty is ineffective for some last-layer adaptation methods and considers prototype distance. This is an opportunity to investigate a restricted, observable mechanism; it is not permission to promise assumption-free target-risk monitoring. The supplement already includes label-shift experiments on Yearbook, so claiming the paper ignores label shift would be wrong.

[POEM / Protected TTA](https://arxiv.org/html/2408.07511v2), future-directions appendix, explicitly says pure label shift can trigger unwanted updates and proposes balanced reservoirs or a target-prior-weighted source CDF. It identifies reliable prior-ratio estimation under simultaneous covariate and label shift as a difficulty. A generic weighted-CDF fix would therefore be following a stated prior-art suggestion. An extension needs demonstrably reliable estimation or a sharply defined robustness result.

The foundational [BBSE](https://proceedings.mlr.press/v80/lipton18a.html) requires invariant class-conditionals and an invertible confusion matrix. [ATC](https://arxiv.org/abs/2201.04234), §3.1, proves general label-free accuracy estimation is not identifiable without assumptions. [TTLSA](https://papers.nips.cc/paper/2023/hash/4b0c1645f3d6a1730931e65ecbf91ac3-Abstract-Conference.html) uses group-conditional invariance and source group labels. [Calibration-Aware Online Adaptation](https://proceedings.mlr.press/v337/jeong26a.html) already studies calibration error in streaming prior estimation. These references prevent treating “estimate the prior from unlabeled observations” as a solved subroutine under arbitrary nuisance changes.

[Recovery Complexity](https://proceedings.mlr.press/v306/zhou26be.html) formalizes continual TTA limits, but its §§2–3 assume proxy/task-gradient alignment, regularity and controlled dependence. It supports studying failure of assumptions; it does not guarantee reliable adaptation when those assumptions fail. [The Premise Is the Problem](https://arxiv.org/abs/2610.07038) is an October 2026 forecasting preprint about dependence and self-monitoring feedback. Forecast outcomes become observed labels; it must not be described as a matched strictly unlabeled visual classifier result.

## Adversarial assessment of the fresh state/history candidate

The lead's fresh candidate asks whether a selector trained on source-reset or fixed-policy trajectories fails when its own adaptation decisions change the model states it later encounters. This is more specific than inferring a corruption name, but its broad principles are established.

[Agentic-TTT](https://arxiv.org/html/2610.12002v1), §2.2.2, already conditions decisions on evolving skill state and evaluates multiple local counterfactual trajectories from the same state snapshot. Appendix E explicitly identifies the mismatch between gold-generated training states and autonomous deployment, calls it exposure bias, and leaves autonomous-stream training and cross-query credit assignment for future work. Its backbone is frozen and skills are isolated LoRA modules, whereas continually updating a shared visual network has different state dynamics. That distinction defines a candidate application scope; it is not an invention of closed-loop learning.

[DAgger](https://proceedings.mlr.press/v15/ross11a.html) established the general solution of collecting supervision on states induced by a learned sequential policy. A visual TTA method that aggregates its own development trajectories must cite and compare this baseline. A new name for dataset aggregation, history conditioning, or an MDP formulation would not be a contribution by itself.

Visual methods already inspect state: [GALA](https://arxiv.org/html/2404.03784v2), §§2.2–2.3, uses displacement from the source and gradient alignment for layer selection/reset; [ASR](https://arxiv.org/html/2603.03796v1), §§3.3–3.5, uses running predicted-class concentration, selective resets, knowledge recovery and online hyperparameter adjustment; [Hybrid-TTA](https://arxiv.org/html/2409.08566v2), §4.1, uses teacher/student disagreement and temporal statistics to switch tuning scope. None of the inspected passages establishes that these methods run a learned whole-method value selector trained on its own free-running visual adaptation states. That is an observed scope boundary, not a completeness claim.

ASR §4.4 also studies non-i.i.d. imbalance, concentration relative to a moving baseline, and randomly varying corruption durations. Appendix E explicitly describes resets responsive to current model state. Therefore state awareness, a class-skew/reset confound, and variable dwell time are already addressed; the remaining candidate concerns learned selector training-state coverage and autonomous rollout performance.

### What would make the candidate scientifically meaningful

The deliverable should establish a previously undermeasured failure mode and its size, followed by a minimal remedy. The contribution would need all of the following evidence:

1. On the same held-out present support/query images and realistic different histories, best actions change by a material loss margin, including noncollapsed states. Merely showing different weights make different predictions is trivial.
2. A model using current predictions already receives information about history. Adding parameter/memory/optimizer summaries should improve beyond that strong baseline, not just a deliberately blind frozen-input detector.
3. State coverage at training matters independently of predictor size and supervision budget. A learner-state aggregation method must beat equal-budget random/fixed-prefix coverage and standard DAgger-style aggregation, or identify a visual TTA-specific reason the standard approach fails.
4. Improvements hold during autonomous rollout, where the controller's earlier choices determine later model states. Replay accuracy on saved baseline states alone is inadequate.
5. Reset, age/entropy/concentration thresholds, ASR/GALA, a good fixed robust method and a frozen robust source remain competitive controls. If periodic reset solves the issue, the claimed new controller may add little.
6. A static corruption-policy lookup or source-return effect does not explain the gain. Hold out histories/order patterns and dominant classes, not only individual frames.

### Smallest proposed fail-fast diagnostic

This is a proposed study; it has not run.

Use one faithful source model and two real update procedures plus current-model KEEP and an explicit RESET action. Construct prefix histories from real, unaltered sequences of nuisance shifts, class-prior changes and source returns. Vary histories while fixing exactly the present support/query identities and continuation order. Snapshot all relevant state: weights, buffers, teacher, optimizer, memory, counters and RNG. Branch candidate actions from each same snapshot. Evaluation labels score outcomes offline; neither shift IDs nor evaluation labels enter policy inputs.

First compare four models on development-derived counterfactuals: frozen-source input summaries; current-model prediction summaries; those summaries plus a few state diagnostics; and the same state-aware selector trained on its own aggregated development states. Equalize the number of scored action outcomes and report total offline cost. Leave an independent development split for hyperparameters and all final stream families untouched.

Initially use a short fixed continuation to diagnose local reversals. Record both immediate and multi-step outcome, since the preferred update may differ across horizons. Select horizons globally before final evaluation. Only after a clear diagnostic effect run each controller freely over complete held-out streams.

Define KEEP as using the current adapted model, SOURCE as answering with immutable source weights, RESET as changing persistent state to a declared checkpoint, and ADAPT as updating the live state. SOURCE and RESET can yield identical immediate predictions but different future states. Do not conflate them. If the first experiment excludes SOURCE as an answering action, state that the menu is intentionally restricted; compare it separately to source inference.

A hindsight local action oracle is diagnostic. An oracle choosing independent best actions from states generated by someone else's trajectory is not a realizable dynamic policy. For sequence comparisons, simulate the oracle's own state transitions or name the result a replay oracle, not an upper bound on a deployable sequence policy.

### Stop conditions

Reject the direction if useful action differences are tiny, appear only after an artificially destructive learning rate, disappear after a basic reset baseline, are fully explained by current-model entropy, or do not transfer beyond the training trajectory generator. Reject a learned controller contribution if state aggregation provides no gain once labeled development queries/offline candidate runs are matched. A negative result may still justify a clear benchmark/protocol note; it does not justify claiming a new successful method.

## Interpretation of historical evidence

The three-seed digit diagnostic used a small normalized-head surrogate, not native modern TTA. It did not support cost-aware evidence acquisition under positive penalties. User-reported five-seed gate aggregates remain separate from that local experiment and lack imported raw runs/manifests. Neither is evidence that the new state-distribution question is novel or that its proposed controller works.

## Access and version notes

- The official Vianna PDF is saved in `verifier-evidence/`; its footer identifies the 2024 CoLLAs conference while PMLR publishes the volume in 2025. Preserve the established citation key and note the distinction.
- Vianna official PDF retrieval: `https://raw.githubusercontent.com/mlresearch/v274/main/assets/vianna25a/vianna25a.pdf`, 26 October 2026. SHA-256: `62cc8cc25502aba8a2adf4af87b5eeb4168d4ff2adfa755792783e5f11a4e3a7`. Text was extracted with installed `pdftotext -layout` for selective reading.
- OpenReview pages were sometimes blocked by browser challenges; arXiv HTML, primary proceedings records, official PDFs and author code links supplied alternatives. No failed fetch is described as a full read.
- WACV LATTA metadata and DOI were checked against CVF/IEEE; some later PDF fetches returned 403. The visible indexed official PDF supports the inspected §3 passage; the full paper was not audited.
- All numeric SOTA claims are authors' claims and are not independently replicated. The report deliberately does not rank method numbers across incompatible source models/protocols.

The ledger `verifier-sources.json` is intended for bibliography integration after deduplication by existing citation key, DOI, title and linked versions. Main records were not edited by this verifier.

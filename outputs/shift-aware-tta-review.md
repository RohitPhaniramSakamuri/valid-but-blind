# Shift aware test time adaptation literature review and research proposal

Review date: 23 October 2026. Status: primary-source investigation and proposed experiments; no new empirical results.

Subsequent work: the user later authorized a bounded CPU diagnostic. Its [actual results](shift-aware-tta-diagnostic-2026-10-23.md) are separate from this literature-review snapshot and do not establish the proposed method or the original benchmark claims.

## 1. Assessment of the supplied proposal

The broad idea is already established: deployment signals can control whether, where, how strongly, or by which procedure a model adapts. A paper whose contribution is simply “infer the shift, then select an adaptation” would overlap direct predecessors. A stronger prospect is **learning whether an additional unlabeled observation will improve an adaptation-policy decision enough to justify its cost**. That is a candidate research question, with unresolved novelty, rather than a demonstrated gap.

The original abstract needs three changes. Its description of existing TTA as uniformly applying one strategy is too sweeping. Inferring a useful decision signal does not establish identification of the physical shift cause. Its evaluation and improvement sentences must be prospective: no results on CIFAR-10-C, ImageNet-C, DomainNet or WILDS exist for this project. [Original proposal](../notes/original-proposal-2026-10-23.md).

### The closest collisions

| Prior work | What is already covered | What a new study would have to establish |
| --- | --- | --- |
| [Hybrid-TTA, ICCV 2025](https://arxiv.org/abs/2409.08566), §4.1 | Detects change and switches between full tuning and adapter tuning. | More than changing the tuning scope after a shift alarm. |
| [SLRF, 2026 journal article](https://link.springer.com/article/10.1007/s10618-026-01222-x), abstract | Assigns aligned/weak/strong shift levels and selects corresponding adaptation strategies. | A specific decision variable or evidence problem beyond shift-level routing. Full method remains paywalled. |
| [MORPHEUS, ICLR 2026 TTU workshop](https://theyoungkwon.github.io/papers/articles/danilowski_morpheus_iclr-ttu26.pdf), §2 | Uses source-model entropy and embedding geometry to predict which complete TTA method will perform best before executing candidates. | More than a feature-based router predicting post-adaptation accuracy. |
| [BECoTTA, ICML 2024](https://proceedings.mlr.press/v235/lee24ab.html), §3 | Routes inputs to adaptation experts and blends their knowledge. | More than dynamic composition or a mixture of experts. |
| [Identifiability of TTA selection, September 2026 preprint](https://arxiv.org/abs/2609.11235), §§3–5 | Studies no-update, action-ranking reversals, prior/stream effects, order-aware evidence and held-out shift evaluation. | More than adding time summaries, a KEEP action, or an evidence-insufficiency argument. |
| [AdaTent++, 2026](https://doi.org/10.3389/frsip.2026.1842851), §2 | Chooses a BN-statistics update, guarded BN-affine optimization, or skipping from reliability signals. | More than confidence/consistency routing with rollback. |

These papers make the initial architecture a starting point for investigation, not a sufficient novelty claim.

## 2. The underlying decisions

Suppose a camera image looks different from the source training images. There are several distinct questions:

1. **Has the input distribution changed?** A feature or output-distribution test can provide an alarm.
2. **Is the source classifier now wrong?** A visible change may preserve classification accuracy.
3. **Will a particular update improve it?** An uncertain prediction is not automatically repairable by entropy minimization.
4. **Which action is worth its total cost?** A more accurate update can lose under a hard deadline.
5. **Should the controller buy another observation before deciding?** Extra views may resolve action ambiguity, or merely consume time.

The important distinction is between **prediction uncertainty** and **uncertainty about the best intervention**. For an invented example, a classifier may be equally uncertain on blur and a class-imbalanced batch, while BN-statistics adaptation helps only one of them. Conversely, two methods might produce nearly identical outcomes on a difficult batch; more diagnostic computation would then have little selection value. This example is a proposed mechanism to test, not an observed result.

Unlabeled selection has limits. Jhawar and Wang distinguish errors caused by a weak selector from decisions that its observations cannot identify. More information helps only when it resolves the relevant ambiguity; their stochastic comparison also rejects a universally superior evidence representation. This rules out claiming that richer features alone solve arbitrary deployment shifts. [Jhawar2026Identifiability, §§3, 5.4 and 7](https://arxiv.org/html/2609.11235v1).

## 3. Literature map

### 3.1 Adaptation objectives and stable updates

[Tent](https://arxiv.org/abs/2006.10726) updates normalization-related parameters using prediction entropy. [CoTTA](https://openaccess.thecvf.com/content/CVPR2022/html/Wang_Continual_Test-Time_Domain_Adaptation_CVPR_2022_paper.html) combines averaged teachers/predictions with stochastic source restoration for continually changing conditions. [EATA](https://proceedings.mlr.press/v162/niu22a.html) filters unreliable or redundant samples and adds anti-forgetting regularization. [SAR](https://arxiv.org/abs/2302.12400) targets unstable updates under mixed shifts, imbalance and small batches. These are necessary controls: an elaborate selector should not be compared only with a fragile always-update baseline.

EATA and its entropy-only ETA variant must be distinguished. If a reproduction needs source-derived Fisher information, disclose its acquisition and storage rather than presenting the variant as using only pretrained weights. A common action menu, implementation and preparation budget are needed for policy comparisons. [AdaBN](https://arxiv.org/abs/1603.04779) supplies a simple statistics-only alternative; [ROID, WACV 2024](https://arxiv.org/abs/2306.00650) is a stronger fixed alternative for nonstationarity, correlation and prior changes. [DeYO, ICLR 2024](https://arxiv.org/abs/2403.07366) already uses perturbation-derived evidence beyond entropy, further constraining claims about new diagnostic signals.

### 3.2 Shift-aware normalization, objective choice and expert composition

[TTN](https://arxiv.org/abs/2302.05155) makes source-versus-batch normalization depend on layer/channel shift sensitivity, with learned source-stage preparation. [Shift-ACT](https://doi.org/10.1016/j.neucom.2025.132013) uses class-specific confidence differences to control reliability thresholds and objectives. [DATTA](https://arxiv.org/abs/2408.08056) responds to within-batch domain diversity. Their inputs and source requirements differ, but all weaken the premise that adaptation ignores shift characteristics.

[MoETTA](https://arxiv.org/abs/2511.13760) routes through LayerNorm experts under mixed shifts, including source-return evaluation. [MoASE++](https://arxiv.org/abs/2605.17743), particularly §5.2, additionally learns augmentation strength using entropy/confidence state and a teacher-distillation reward. Thus neither expert composition nor learned augmentation control is available as an untouched contribution. In the inspected MoASE++ equations, the policy reward penalizes augmentation strength and distillation mismatch; it does not directly measure the net value of evidence for choosing among independent TTA methods.

### 3.3 Online structure, accumulated state and recovery

[NOTE](https://papers.nips.cc/paper_files/paper/2022/hash/ae6c7dbd9429b3a75c41b5fb47e57c9e-Abstract-Conference.html) and [RoTTA](https://openaccess.thecvf.com/content/CVPR2023/html/Yuan_Robust_Test-Time_Adaptation_in_Dynamic_Scenarios_CVPR_2023_paper.html) already address temporal correlation, changing domains and balancing recent observations. [GALA](https://arxiv.org/abs/2404.03784) uses proposed gradients relative to accumulated parameter displacement for layer selection, skipping and reset behavior. [ASR](https://arxiv.org/abs/2603.03796) studies when and where to reset. Consequently, “consider the current state” is too broad a gap.

Forecasting neighbors [DynaTTA](https://openreview.net/forum?id=a399SmgWGl) and [RG-TTA](https://arxiv.org/abs/2603.27814) modulate adaptation using changing regimes. Their access to subsequently observed forecast outcomes must be separated from classification that never receives target labels. A forecasting controller cannot be silently imported as a strictly unlabeled classification baseline.

### 3.4 Estimating performance and selecting methods

[AETTA](https://openaccess.thecvf.com/content/CVPR2024/html/Lee_AETTA_Label-Free_Accuracy_Estimation_for_Test-Time_Adaptation_CVPR_2024_paper.html) estimates adapted-model accuracy using label-free disagreement signals and supports recovery. [TTALine](https://arxiv.org/abs/2310.04941), §5.2, applies accuracy/agreement relationships to selection. [Realistic Evaluation of TTA](https://doi.org/10.5220/0014320100004084) examines unsupervised selection criteria and their dependence on the evaluation regime. These approaches may inspect already-adapted candidates; that is a different information budget from pre-action routing.

MORPHEUS is the operationally closest predecessor. Its development procedure runs candidate adaptations on auxiliary domains to train random-forest predictors, then uses source-model observations to choose a method. Our learned acquisition controller would inherit a comparable offline supervision/preparation requirement. “No target labels during deployment” must not become “no labeled development data.” [MORPHEUS, §2](https://theyoungkwon.github.io/papers/articles/danilowski_morpheus_iclr-ttu26.pdf).

### 3.5 Deciding whether to adapt and what evidence to inspect

[HD-TTA](https://arxiv.org/abs/2602.19454) selects geometric refinement hypotheses after a skip gate in brain-tumor segmentation. [Selective adaptation with CAS](https://arxiv.org/abs/2609.08367), §3, uses cross-augmentation similarity to skip ineffective VLM updates. [SEGA](https://arxiv.org/abs/2608.29920), Algorithm 1, computes a fixed sequence of structured-erasure probes and uses entropy sensitivity for recovery and sample gating. [FORGE](https://arxiv.org/abs/2609.01683), §4.6, probes source/adapted paths during a short initial window before committing. Extra observations, update skipping and paid probing all have direct predecessors.

[SA-TTS](https://openaccess.thecvf.com/content/CVPR2026W/Viscale/html/Yang_SA-TTS_Stress-Aware_Test-Time_Scaling_for_Vision_Models_CVPRW_2026_paper.html), Algorithm 1, already escalates from cheap uncertainty to augmentation disagreement and possibly multi-crop inference. It keeps the backbone fixed. Its acquisition principle is a necessary comparator even though its terminal actions differ from parameter-updating TTA.

The general decision principle is also established: [Weiss and Taskar, 2013](https://proceedings.neurips.cc/paper_files/paper/2013/hash/ebd9629fc3ae5e9f6611e2ee05a31cef-Abstract.html) learn adaptive feature-acquisition value; the [2026 acquisition survey](https://www.ijcai.org/proceedings/2026/860) organizes sequential measurement and stopping under cost. [ECHO-k](https://arxiv.org/abs/2610.03454), October 2026, learns task-agnostic label-free modality acquisition from representation recovery. A TTA contribution must establish the importance of **adaptation-action value**, beyond information recovery, generic uncertainty or a familiar cascade.

### 3.6 Reliability and the meaning of computational efficiency

[Protected TTA](https://proceedings.neurips.cc/paper_files/paper/2024/hash/9b35a0a20d617dc68ae98a7a57df2f51-Abstract-Conference.html) and [Monitoring Risks in TTA](https://arxiv.org/abs/2507.08721) provide stronger precedents than a confidence threshold presented as safety. Their assumptions matter: monitoring with a calibrated proxy does not create arbitrary-shift target-risk guarantees.

[Tempora](https://proceedings.mlr.press/v306/sreeram26a.html) evaluates hard deadlines, latency-dependent utility and amortized budgets; a method’s ranking can change with timing pressure. [BoTTA](https://doi.org/10.1145/3774906.3800498) evaluates resource-constrained, periodic adaptation with limited samples, incomplete class coverage and compound shifts. Neither runtime reporting nor a compound-shift test is individually new. [The online-TTA survey](https://link.springer.com/article/10.1007/s11263-024-02213-5) likewise includes computation and memory comparisons.

## 4. A concrete limitation chain

Three sources support a narrower, testable intersection:

1. **Practical routing lacks sufficient validation in a close method.** AdaTent++ §5 explicitly discloses benchmark condition identifiers used for configuration, a fixed balanced subset, one deterministic run and no long-stream experiment. Its §4 says the comparison is not strictly compute matched; §6 requests controllers that adapt view and step counts to budgets. The stronger “matched budgets” wording in its conclusion should not override that qualification. [Publisher §§4–6](https://www.frontiersin.org/journals/signal-processing/articles/10.3389/frsip.2026.1842851/full).
2. **Richer evidence has conditional value.** The identifiability paper’s §7 limits the action/model family and emphasizes matching observations to the deployment. It does not demonstrate a costed controller that decides when to acquire those observations. This is a scope distinction from the inspected method, not proof that no other paper has done it.
3. **Cost changes the desired decision.** Tempora’s discussion motivates joining temporal constraints with continual/nonstationary realism. Evaluating a label-free policy selector’s evidence acquisition under that tradeoff is more specific than reporting accuracy plus mean runtime.

The remaining question is therefore:

> On held-out deployment shifts, can a controller predict when additional unlabeled observations will improve its choice among adaptation procedures, enough to offset their acquisition cost, while retaining a useful no-update option?

**Gap status:** a literature-supported candidate intersection. We found no exact demonstration of the complete proposed combination in the inspected sources. General value of information, adaptive probing, dynamic policy selection, no-update and cost-aware evaluation are all prior art. A first-in-field or guaranteed-publication claim is unsupported.

## 5. Proposed approach

Working title: **Budgeted Evidence Acquisition for Label-Free Adaptation Policy Selection**.

### Start with one acquisition decision

Use an episodic diagnostic first. Each episode starts from an identical source checkpoint and receives an unlabeled support batch. It must choose a procedure before predicting on a separate subsequent query batch. Development labels may score query outcomes offline; final evaluation labels remain hidden from the controller.

The initial action menu is frozen source inference, a BN-statistics update, and Tent. Add ETA/SAR only if the first diagnostic establishes useful action diversity. Do not begin with an unrestricted composition of many methods; update order, interaction and state costs would obscure the acquisition mechanism.

- **Cheap evidence:** entropy, confidence margin, predicted-class concentration, and compact feature statistics already available from one frozen-source pass.
- **Additional evidence:** a fixed small number of label-preserving augmented views, giving disagreement and stability features. Transformation choices are globally fixed using development data. Their identities never depend on a hidden benchmark corruption label.
- **Decision:** choose an adaptation action immediately or pay for those observations, then choose. Do not run every candidate update online.

Importantly, features extracted from the existing source pass do not incur an imaginary extra forward pass. Additional views do incur real execution and latency costs. Extra-view predictions must initially be used only for routing, so that any gain is attributable to decision evidence rather than unreported prediction ensembling.

### Train the gate on realized selection improvement

Let \(g_0\) select an action from cheap evidence and \(g_1\) select from richer evidence. Cross-fit both on labeled auxiliary development episodes. For each held-out development episode, measure the query loss of the actions that the two fitted selectors actually choose. Train a lightweight gate to predict that difference, using cheap evidence only.

For loss \(L\), all-in cheap-route cost \(C_0\), all-in rich-route cost \(C_1\), and a development-fixed cost weight \(\lambda\), define the empirical acquisition target:

\[
d=\big[L(g_0)+\lambda C_0\big]
 -\big[L(g_1)+\lambda C_1\big].
\]

The costs include each route's evidence generation and processing, selector inference, state copies, terminal adaptation and prediction. A genuinely shared source pass cancels in this paired difference but remains charged when comparing with direct SOURCE inference. Positive \(d\) means the richer selector improved this episode’s decision enough to pay for its full extra route. At deployment the gate predicts this value; it never observes target query loss. Cross-fit selector predictions inside grouped training folds, fit the gate only on those held-out predictions, use a separate outer development split for thresholds and cost weights, and leave final evaluation untouched. This is a proposed application of established acquisition ideas, not a new general value-of-information theorem.

A development-calibrated positive-margin trigger can be tested for conservative acquisition. It provides no universal risk guarantee on unseen shifts. Report a frontier over predeclared budgets rather than choosing a favorable \(\lambda\) after inspecting evaluation labels.

### Three reasons the method could fail

1. A fixed procedure could dominate: nothing useful remains to select.
2. Additional views could be uninformative about update benefit even when informative about prediction confidence.
3. A useful richer selector could exist, but its benefit could be unpredictable from cheap evidence; then selective purchase may not beat a fixed or random allocation.

Those are distinct negative findings and require separate experiments.

## 6. Evaluation that can falsify the proposal

The detailed [experiment protocol](../experiments/001-policy-selection-pilot.md) defines data access, action states, metrics, controls and stop conditions. Its central requirements are:

- Separate original image identities as well as shift families across router training, validation and final evaluation. The same clean image under another corruption is not an independent hold-out.
- Use corruption-family holdouts, held-out compositions, class-prior changes and temporal correlation. Domain names are evaluator metadata, never router inputs.
- Keep support and query images disjoint. Freeze hyperparameters, acquisition thresholds and cost weights before final evaluation. Declare query-time normalization: Tent can use unlabeled query-batch statistics, so a support-only wrapper or a pointwise frozen-statistics variant must be identified explicitly; prohibit query gradients and unintended persistent buffer writes.
- Compare SOURCE, every fixed action, a development-selected fixed action, a shift-ID router, a MORPHEUS-style selector and an order-aware selector. Learned selectors receive the same offline development information.
- Compare cheap-only, always-rich, fixed-schedule, random, entropy-triggered, ambiguity-triggered and learned-value acquisition at matched all-in cost.
- Add a same-cost frozen-inference augmentation/ensemble control. Otherwise additional views might buy better predictions without needing adaptation selection.
- Count preprocessing, views, source forwards, feature computation, router/gate inference, updates, state copies and synchronization. For deadlines, include missed/late predictions.
- Use paired complete episodes or streams as repeat units, not thousands of correlated batches treated as independent trials.

The principal outcome is a better error–cost or deadline-utility frontier, with lower regret to a cost-aware action oracle and a lower measured harmful-adaptation rate relative to SOURCE. A router that chooses SOURCE everywhere may avoid harm but fail to capture useful adaptation. An oracle that uses true evaluation labels is a diagnostic, never a deployable algorithm.

### Stop before scaling if the mechanism is absent

First measure best-action versus best-fixed-action headroom. Then test richer evidence against cheap evidence out of family. Only if both exist should a learned acquisition gate be built. Stop the proposed method if equal-cost random or uncertainty-triggered acquisition matches it, if its gains vanish after charging evidence cost, or if it works only when corruption identities are disclosed.

## 7. Benchmark and compute scope

| Benchmark | What it contributes | Role in this prospect |
| --- | --- | --- |
| CIFAR-10-C / CIFAR-100-C | Controlled low-resolution corruption study. | Small first diagnostic; use released conditions or explicitly named source-derived synthetic development episodes. |
| ImageNet-C | Larger-model corruption scaling. | Later external check after the acquisition mechanism works. |
| DomainNet or a named DomainNet-126 protocol | Natural visual-domain transfers. | A second test of transfer beyond constructed corruptions. Source checkpoint and label mapping must match the chosen subset. |
| A specific WILDS dataset | Natural domain/subpopulation shifts with task-specific metrics. | Optional later validation; specify the dataset and target-access rules. |

The [corruption benchmark](https://arxiv.org/abs/1903.12261) uses generated corruptions. [DomainNet](https://arxiv.org/abs/1812.01754) and [WILDS](https://proceedings.mlr.press/v139/koh21a.html) address different deployment structures. They should not all be described as heterogeneous real-world corruptions. WILDS is a suite, not one classification dataset.

CPU is suitable for source inspection, routing regressors and small mechanism checks. Generating many neural-adaptation outcomes is the likely expensive stage. Start with a few actions, small batches and a pinned compatible checkpoint; profile actual forward/backward costs before committing to a full grid or GPU rental. Existing credits and deadlines from other projects are not assumed current. No dataset, checkpoint or training dependency was installed during this review.

## 8. Alternative branch

An alternative question is whether whole-method selection should depend on a model’s **current adapted state**, including optimizer, normalization and memory, rather than only source-derived target statistics. A matched diagnostic would hold the incoming batch fixed while varying history-derived live states and compare action rankings from consistent clones. GALA, ASR, recovery and regime-controller work already cover much of the broader idea. This branch has more state and delayed-outcome complexity and is not the recommended first experiment. [Branch record](../notes/research-branches.md).

## 9. Proposed abstract without invented results

Test-time adaptation provides multiple ways to update a deployed model, but selecting an update from unlabeled observations can be unreliable and computationally costly. We investigate whether additional diagnostic observations should be acquired selectively according to their expected value for adaptation-policy selection. A controller first evaluates inexpensive source-model statistics and optionally obtains a small set of augmented-view observations before choosing among no adaptation and lightweight update procedures. The proposed evaluation separates labeled auxiliary development from unlabeled deployment, holds out image identities and shift families, and accounts jointly for evidence acquisition and adaptation cost. Experiments will test whether decision-value-based acquisition improves the error–cost frontier over fixed policies, existing selectors and uncertainty-triggered probing, including regimes where selecting or acquiring additional evidence provides no benefit.

## 10. Reading order and immediate next step

1. MORPHEUS §2: understand the closest complete-method selector and its development supervision.
2. The identifiability preprint §§3.5, 4 and 7: distinguish observation ambiguity from a poor predictor.
3. AdaTent++ §§5–6: read a concrete limitation and future-direction request before its method.
4. SA-TTS Algorithm 1, CAS §3 and SEGA Algorithm 1: inspect the nearest acquisition/skip baselines.
5. Tempora §§3–5: choose the operational cost/latency objective.
6. Tent, BN adaptation and ETA/SAR: implement and understand the actual update actions only after the selection question is fixed.

The next concrete step is the small action-headroom diagnostic described in the experiment plan. The review supports doing that diagnostic; it does not yet support drafting a successful method paper.

See [source index](../REFERENCES.md), [bibliography](../references.bib), [provenance](shift-aware-tta-review.provenance.md) and the independent [verifier](../notes/shift-aware-tta-review-verifier.md) and [reviewer](../notes/reviewer-findings.md) records for evidence and access limits.

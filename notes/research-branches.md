# Research branches for shift aware adaptation

## Mechanism update — 2 November 2026

**Status: replicated and controlled empirical finding on CIFAR-100-C with Tent, reproduced in the authors' code. Candidate contribution, not a verified gap.** The gap survives a fixed threshold, the entropy step adds misses beyond BN updates, and BN alone did not produce the gap across models. See [Experiment 004](../experiments/004-monitor-blind-spots.md). The local "pending" qualifiers in the review below are superseded by that record. SAR at default settings: NOT SHOWN, with low sample use on four models, so the gap is established for Tent only. Open: other datasets and adaptation methods, separating SAR's filtering and optimizer effects, a remedy at matched false alarms, and the unread Mahdiani full text.

## Adversarial review update — 2 November 2026

The [new review](novelty-review-2026-11-02/review.md) rejects broad originality for entropy/confidence failure and adaptation undermining its own monitoring signal. Existing independent estimators, disagreement/conformal methods, and frozen sentinels constrain any remedy.

**Remaining candidate question, not an established gap:** does Schirmer's supported confidence monitor have materially worse sensitivity for Tent than frozen checkpoints under persistent many-class skew and corruption, beyond its already documented proxy failures? The local port replication reports 147/166 versus 44/110 missed, but the exact literature audit is incomplete. Fixed-threshold/BN cause and authors' Dirichlet-pipeline outcomes remain pending in the authoritative experiment record. Mean-confidence dependence previously failed and is not revived as an explanation.

The review recovered 20 indexed Schirmer citers and a 21st through full-text follow-up. Mahdiani's conformal/BN-control paper, TRUST-ADAPT, and ODFD remain access blockers. Continue as a narrow diagnostic only after those checks; change direction if ordinary proxy/current-method controls remove the useful residual. No experiments ran for this review.


## Replication update — 1 November 2026

**Status: replicated empirical finding on CIFAR-100-C, not a verified research gap.** Under Dirichlet 0.1 class skew, the Schirmer et al. monitor (our port) misses clear Tent failures more often than source failures across six models. Candidate mechanism, exploratory: Tent raises confidence, so fewer wrong predictions are flagged. Open: adaptation versus recalibration, the authors' own pipeline, other datasets and methods, and a targeted novelty search.

## Six-model update — 1 November 2026

Confidence dependence rejected in this setup. **Current candidate, post hoc and unconfirmed:** under strong class skew, this monitor misses Tent's failures more often than the unadapted model's, across models. Needs fresh confirmation and an authors'-code check, and novelty is unverified.

## Experiment 005 update — 1 November 2026

Fairness candidate not supported as stated: evidence points to class prior, not group minority status. Strongest remaining line is Experiment 004, with confidence dependence untested.

## Gap review update — 1 November 2026

**Current candidate (candidate question, not a verified gap):** does online TTA widen demographic error gaps, driven by stream group make-up? Origin: `Launay2026FairTPT` limits itself to episodic VLM adaptation; our Experiment 004 showed skew effects. Closest: FairTPT, TTAB Waterbirds, FairDomain. Monitor line paused, not rejected.

## Second-model update — 1 November 2026

The blind spot did not generalize under the frozen rule. Remaining candidate question: does monitor blindness under skew depend on the adapted model's confidence level? Unverified, based on two models.

## Experiment 004 update — 1 November 2026

**Narrowed candidate (unverified):** a validity assumption for label-free TTA monitors can hold while the monitor is blind, as seen for Tent under persistent class skew, where error and confidence rise together. Needs a literature check for the exact claim, held-out confirmation, more adaptation methods and a tested alarm for Q2.

## Candidate B update — 31 October 2026

**Current candidate B′ (candidate question, not a verified gap):** does a label-free TTA monitor miss real risk rises, or over-alarm, under combined corruption and class-prior shift, and can an independent signal help beyond accuracy estimation? Origin: Monitoring Risks §6 and our reading that Assumption 1 gets easier as proxy misses grow. A′ and the change-stream lead are not supported; see Experiment 003.

## Dossier update — 31 October 2026

**Current candidate A′ (candidate question, not a verified gap):** does a pre-action selector's evidence decay as the model adapts, more for quantities the update directly optimizes, in a way that fitting across exposure levels does not fix? Originating observation: entropy-based updates optimize a signal that selectors read. Closest work: `Lee2024AETTA`, `Cygert2026RealisticSelection`, `Press2024EntropyEnigma`, `Jhawar2026Identifiability`, `Singh2026ReliabilityGated`. Test: [Experiment 003](../experiments/003-evidence-decay-under-adaptation.md), planned. Evidence: [dossier](../outputs/novelty-dossier-2026-10-31.md).

**Candidate A status:** H1 prior art, H2 demoted, H3 retained as a control. B and C were not re-attacked in this pass.

## Fresh assessment — 26 October 2026

The user permitted a clean-slate restart, especially novelty. The [new deep review](../outputs/shift-aware-tta-deep-review-2026-10-26.md) supersedes the earlier preference as a recommendation; historical results and documents remain intact.

**Current candidate A:** determine whether a visual adaptation selector fails on the state distribution created by its own actions. Originating observation: source-reset method-selection studies and live-state recovery methods answer different parts of the deployment problem. Agentic-TTT Appendix E explicitly identifies gold-history/autonomous-history exposure bias; DAgger gives an established general remedy. The candidate contribution is the size, mechanism and residual difficulty of this issue in visual TTA, not inventing state-aware routing or dataset aggregation. Closest work: MORPHEUS; Jhawar/Wang identifiability; ASR; GALA; Hybrid-TTA; Agentic-TTT; RNA; DAgger. [Experiment 002](../experiments/002-state-conditioned-selection.md) is planned, with matched present inputs, realistic prefixes, complete-state counterfactuals, rich current-model controls, autonomy and equal-resource collection comparisons. Novelty and usefulness remain unverified.

**Candidate B:** flag failure of label-free risk-monitoring proxies under restricted combined shifts. Origin: Monitoring Risks §6 explicitly leaves unlabeled assumption diagnostics open; POEM describes label-shift-triggered unnecessary updates. ATC/BBSE and prior-aware methods constrain what is identifiable. This is secondary; no arbitrary-shift guarantee or novel prior correction is claimed.

**Candidate C:** specific interactions among ordered adaptation actions under compound shifts. BoTTA and mixtures already cover broad compound/routed settings. Defer unless a consequential, unstudied interaction is identified.

Next: complete close full-method overlap checks and freeze the diagnostic; proceed to implementation/execution only with new project-specific authorization/conditions. Abandon a method claim if current-model evidence, reset controls or ordinary equal-budget aggregation remove the residual problem.

## Historical branches — 23 October 2026

Opened 23 October 2026 from the user's proposed dynamic adaptation-policy selector. No branch has a verified novelty claim. A subsequent [bounded CPU diagnostic](../outputs/shift-aware-tta-diagnostic-2026-10-23.md) exercised the acquisition branch on alternate small data; it did not establish the proposed controller.

| Branch | Precise question | Closest prior work | Status |
| --- | --- | --- | --- |
| Cheap normalization harm gate | At matched predicted concentration, can entropy and source-relative feature displacement distinguish normalization benefits across true class-mixture changes and corruption-induced prediction collapse? | NOTE, channel-selective normalization, MORPHEUS and the identifiability preprint. | Selected working approach for definition after the user requested one direction. Simple three-feature tree; empirical contribution and novelty unverified. [Definition](../outputs/selected-approach-cheap-normalization-gate.md). |
| Original broad selector | Can shift signals choose or compose an adaptation policy? | Hybrid-TTA, SLRF, MORPHEUS, BECoTTA, MoETTA, AdaTent++. | Established direction with direct overlap; insufficient as the contribution. |
| Acquisition for action decisions | When does acquiring extra unlabeled evidence improve the choice of a parameter-update procedure enough to pay for its cost? | MORPHEUS; identifiability preprint; SA-TTS; CAS; SEGA; adaptive VOI; ECHO-k; Tempora. | Bounded CPU diagnostic completed: headroom exists, richer evidence helps variably, cost-aware acquisition was not validated. Full benchmark remains planned; no verified gap. [Plan](../experiments/001-policy-selection-pilot.md). |
| Selection conditioned on live state | For the same next input batch, do history-induced model/optimizer/BN/memory states change which complete update should be selected? | GALA, ASR, CoTTA, AETTA recovery, RG-TTA; source-clone selectors address a different unit. | Historical secondary branch; freshly reassessed above with Agentic-TTT/DAgger collisions and stricter controls. No novelty established. |
| Joint policy composition | Are short ordered sequences of updates better than selecting one action? | Expert routing, multi-hypothesis/refinement methods, augmentation-policy learning. | Defer; interaction, order and cost would obscure the initial acquisition test. |
| No benefit from further diagnosis | Is cheap evidence already sufficient, or does a fixed action dominate after cost? | Identifiability, Tempora, physical-diagnosis decision-value distinctions. | A meaningful possible negative outcome, not a fallback claim of successful selection. |

## Historical candidate gap statement

The inspected literature separately establishes method selection, conditional evidence/computation, and cost-aware TTA evaluation. The proposed test asks whether **learned realized decision value** can allocate costly evidence for parameter-update selection better than always acquiring it or using uncertainty thresholds, under fixed causal access and held-out shift families. The intersection still needs empirical headroom and further prior-art checks before being claimed as a contribution.

## Source limitation that motivated the candidate

AdaTent++ sections 5–6 explicitly disclose domain-aware benchmark configuration and limited validation, and request budget-aware view/step controllers. Tempora's discussion motivates integration with continual/nonstationary realism. The identifiability preprint makes evidence sufficiency conditional on the observation/deployment pair. These are reasons to test a specific question; none proves that a missing combination is important or untouched.

## Historical next step

Freeze the selected cheap gate and matching protocol, verify closest experimental overlap, then use fresh evaluation when further execution is requested. Preserve the failed cost-aware acquisition and post-hoc status of the original concentration rule.

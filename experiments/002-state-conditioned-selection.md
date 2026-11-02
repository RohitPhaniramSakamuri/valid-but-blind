# Does an adaptation selector survive the states created by its own choices?

Experiment ID: **002-state-conditioned-selection**. Date proposed: **26 October 2026**.

Status: **Planned; not implemented or executed.** This protocol follows a clean-slate novelty assessment requested by the user. Earlier digit and externally reported gate results do not validate its hypotheses. No environment, hardware reservation, compute allowance or execution deadline is assumed from previous projects.

Related records: [current deep review](../outputs/shift-aware-tta-deep-review-2026-10-26.md), [independent overlap investigation](../notes/review-refresh-2026-10-26/verifier.md), [reference library](../REFERENCES.md).

## Question and hypotheses

Does the benefit of the next adaptation depend materially on inherited live state after current inputs and current-model prediction information are controlled? Does a selector trained on externally generated states lose performance when its own actions create the states it subsequently encounters?

Three distinct hypotheses, to register before final evaluation:

- **H1, state effects:** realistic prefix histories produce meaningful action-ranking differences on identical current support/query sequences, including noncollapsed states.
- **H2, observable state value:** a small explicit state representation improves action-loss prediction and selection beyond strong current-model prediction summaries and simple reset controls.
- **H3, autonomous generalization:** selecting on one's own states differs from replay selection, and a correction trained on auxiliary learner-generated states improves useful adaptation on untouched autonomous streams at matched development supervision/computation.

All three are empirical questions. State-conditioned control, exposure bias and DAgger-style state aggregation are prior art. A method contribution requires a specific TTA mechanism or improvement beyond these known ideas. H1 alone does not establish novelty: different parameters yielding different predictions is unsurprising. See [Agentic-TTT Appendix E](https://arxiv.org/html/2610.12002v1), [DAgger](https://proceedings.mlr.press/v15/ross11a.html), [ASR](https://arxiv.org/abs/2603.03796), [GALA](https://arxiv.org/abs/2404.03784).

## Small example and comparisons

Fix a foggy support batch and the following disjoint foggy query batch. Reach the support through a balanced related-corruption history, a class-skewed history, a different corruption history and a source-return history. Histories and sample identities are chosen without examining which action wins. At the decision, clone each live state and compare KEEP, NORMALIZE, UPDATE and RESET on that same support/query.

An informative result is not simply a ranking flip. It is a reproducible loss margin that remains after reasonable learning rates, fixed/periodic resets, optimizer-memory resets and current-prediction-only selection have been considered. If a simple control removes the residual problem, the larger controller is unnecessary.

## Setup and data access

Implementation will use **uv**, never pip. Source code, dependency versions, hardware, checkpoint hash, seed manifests and commands must be recorded when implementation/execution is requested. None is claimed here.

Primary small benchmark: CIFAR-100-C on a faithful BN image classifier. CIFAR-10-C may be a debugging/scoping dataset but cannot select favorable final claims. Later confirmation: ImageNet-C and natural DomainNet-126, followed by a second normalization architecture with an appropriate action menu. WILDS-derived online experiments need an explicitly separate protocol; standard WILDS test-training/batch-statistics restrictions apply to official comparisons.

One source-access regime to freeze before implementation:

| Partition | Proposed CIFAR-100 role | Legal use |
| --- | --- | --- |
| 45,000 official training IDs | Source-classifier training | Labeled; train the shared source checkpoint. |
| 3,000 other training IDs | Auxiliary selector fitting/state collection | Labels score cloned actions offline. |
| 2,000 remaining training IDs | Calibration/model selection | Freeze thresholds, cost weights, models and history parameters. |
| Official 10,000 test IDs | Final evaluation | Unlabeled observations at runtime; labels used only by evaluator after decisions. |

This deliberately uses a 45,000-image source model. Do not compare its numbers directly with published 50,000-image source results as if preparation were equal. An alternative off-the-shelf checkpoint needs a declared valid auxiliary-data regime; it cannot be silently substituted. Keep every source class available during classifier training.

Partition **original identities before creating corruptions**. A blurred and noisy version of the same image must not cross selector-training/calibration/final partitions. Within a local matched case, prefix IDs, support IDs, query IDs and fresh query-replication IDs are disjoint pools. Prefixes must never expose the query images through a different corruption. Matched histories/branches intentionally share a query to make paired comparisons; that dependence must be respected in analysis. Longer autonomous protocols that revisit original IDs are separately disclosed and grouped.

Initial candidate values, to freeze or revise using development data only:

- Source seeds: 11, 29, 47, 71, 101; stream seeds separate and recorded.
- Support and prediction block: 64. The primary one-decision query is the next 64-example prediction block. A separate frozen post-action diagnostic window uses 512 examples with subsequent transitions fixed to KEEP. Do not pool this fixed-horizon loss with one-step training/rollout results. Sensitivity block sizes 16/32/128 and fresh query repetitions are subject to disjoint-data availability.
- Prefix lengths: two development-fixed scales, for example 2,048 and 8,192 observations. Repeated IDs within a long prefix must be disclosed and grouped; repetitions are not new independent data.
- Corruption severities: development includes mild/moderate/severe cases; final aggregation and severity subset are fixed in the manifest.
- History families: balanced IID, class-correlated, globally skewed/partial-class, alternating unrelated corruptions, gradual changes, and source returns. These labels describe the evaluator's construction, never controller inputs.

No numerical setting above is selected from an actual result. The first implementation may require a smaller collection; any change belongs in a dated amendment before final evaluation.

## Source, calibration and shift holdouts

Use outer held-out corruption **families**, rather than only leaving one severity out. Noise/blur/weather/digital groupings must be explicitly listed; group ambiguities are fixed before evaluation. In each outer run, selector fitting and calibration use only permitted development families. Keep final IDs unavailable throughout fitting even when a corruption family appears in a different outer run.

Independently hold out prefix/history patterns and identities of dominant classes from selector fitting. Holding out dominant classes does not mean removing those classes from source training. Natural-domain confirmation uses held-out source-to-target transfers/order patterns. Source robustness training may have seen related augmentations; disclose this separately from the selector's shift holdout.

Evaluate simultaneous nuisance and class-mixture changes, but do not call this setting new: UniTTA, TRIBE, DELTA, ROID and LATTA already cover related regimes.

## State and action contract

Save the immutable source state separately. A live snapshot includes parameters, normalization buffers, optimizer state, any teacher/replay memory, counters and random-number state. Include mode flags where they affect inference. The minimal implementation has no teacher or replay; adding one later changes the snapshot contract.

| Transition | Required behavior |
| --- | --- |
| KEEP | Preserve predictive/learning state; external stream time and elapsed-age bookkeeping still advance. Never update during query scoring. |
| NORMALIZE | Change only explicitly selected BN statistics using support; fix the estimator/interpolation on development and freeze statistics on query. |
| UPDATE | One reliable entropy step on normalization affine parameters using frozen live running statistics; BN buffers stay unchanged. Filter/optimizer/LR fixed on development. This ETA-inspired primitive differs from native ETA/Tent and must be labeled accordingly. |
| RESET | Restore the declared source parameters, buffers, optimizer/counters and any auxiliary state. Restoring only weights is a different action. |

The primary minimal study evaluates these four transitions. **SOURCE** is also a baseline answering with the immutable source classifier. If later made a selectable fallback, it answers the next block while retaining live adaptation state; it must not be conflated with RESET. Prediction choice and successor-state transition are separate variables. Announce the expanded action space before evaluation.

All actions use the same legal support, checkpoint and query. Candidate execution starts from identical cloned states within a decision. Restore random-number states and use declared common random numbers where stochastic operations are comparable. Observation forwards are state-pure: no BN/teacher/memory/counter/RNG mutation that affects a later action; disable stochastic inference or restore its state. Method-specific state must not be discarded silently when adding complete TTA algorithms later. Complete-method baselines can retain their own faithfully implemented state machines in separate autonomous comparisons.

## Prediction and update timing

Primary deployment is **predict then update**:

1. Receive current batch B_t; score predictions using the live state selected before B_t arrived.
2. Compute legal observations from B_t and the current state. Labels remain unavailable.
3. Choose a transition using only these observations and past information.
4. Apply the transition on B_t's unlabeled inputs to obtain the state for B_(t+1).

At a local decision, B_t is support and a fixed following window is the evaluator's query. That future window never enters the decision features. Query inference must perform no gradients, statistics updates or persistent memory writes. If a baseline normally uses same-query batch statistics, its different access must be declared; do not silently present a support-only wrapper as its original benchmark implementation.

A separate same-batch adapt-then-predict analysis is secondary, with separate tables. Short/variable dwell times can make support and future conditions differ; preserve this realistic failure rather than granting boundary labels or lookahead.

## Stages and measurements

### Stage 1: action headroom and mechanism

Predefine present sequences and prefixes independently of outcome labels. Evaluate every allowed action from each state, preserving all outcomes and ties. Analyze paired action differences across histories.

Report:

- Mean/local loss per action and best development-fixed action.
- Frequency and margin of ranking reversals at matched present inputs.
- Results stratified by collapsed/noncollapsed state using a source/development-fixed definition; report the full unfiltered population too.
- Effect of periodic reset, optimizer-memory reset and one stateless-update variant.
- Immediate query performance and an explicitly fixed short continuation. For a multi-batch continuation, define subsequent transitions (initially KEEP) so actions are comparable.

For the optimizer ablation, hold weights and BN buffers fixed while resetting versus carrying optimizer memory. This intervention intentionally constructs paired successor possibilities; it is a diagnostic, not an independently occurring deployment. Do not manufacture ranking reversals by selecting unusual optimizer scales.

Set a practical loss margin on calibration data before final scoring. Use paired uncertainty and repeat across independent source/stream seeds. Finite query uncertainty and repeated query identities matter. More branches are not more independent datasets.

**Gate to further work:** meaningful residual action headroom on plausible states beyond straightforward controls. If absent, stop controller development.

### Stage 2: incremental evidence value

Fit equal-capacity action-loss predictors using:

1. Frozen-source global summaries.
2. Frozen-source ordered summaries.
3. Current-model logits, feature geometry and ordered summaries mirroring the rich source-side representation.
4. The same current-model evidence plus declared state descriptors.

Use the same scored action outcomes and nested development/calibration splits. Additional state features can include layerwise parameter/buffer drift, age, source/live disagreement and compact optimizer summaries. Predeclare the maximum feature set; do not mine evaluation outcomes for a favorable combination. Check apparent ranking reversals with a fresh disjoint query repetition and predeclared pairwise/tie-aware margins, without selecting only successful cases.

Also include fixed actions and simple age/entropy/concentration/reset rules. MORPHEUS-style and stream-aware pre-action selectors are essential neighboring baselines. Do not claim a faithful numerical reproduction without matching their exact features, architecture, preparation and access.

**Gate:** state features improve beyond current predictions and simple controls, with useful accuracy/harm/cost effects on held-out regimes.

### Stage 3: state collection and free rollout

Compare development collections generated by fixed policies, broad random policies and successive frozen versions of the learned policy. Match unique labeled query IDs and allowed reuse, scored action outcomes, candidate steps, support forwards and state-collection compute; report a frontier where simultaneous equality is impossible. Account for all cloned updates/queries. Hold separate calibration streams fixed. Add plain DAgger-style learner-state aggregation as an explicit baseline before claiming a special training remedy.

Evaluate replay action-loss prediction on logged states, then **autonomous streams** in which each selector changes its own state. Match external input order across policies; their endogenous states are allowed to diverge. Report how saved-state evaluation and autonomous performance differ, with the sampling/weighting of saved states stated.

An apparent win due only to extra labeled development queries or additional candidate executions is not an H3 success. One-step training does not establish long-horizon optimality; include a delayed-effect diagnostic before adding claims about credit assignment.

### Stage 4: faithful external comparisons

Scale only if Stages 1–3 support their corresponding hypotheses. Include SOURCE, statistics adaptation, faithful reliable/stable-update methods, ROID/RoTTA, RDumb, and compatible ASR/GALA/Hybrid-TTA controls. Class-mixture investigations need imbalance-aware controls. Source-dependent and source-free variants, different normalization backbones, and different tasks receive separately qualified comparisons.

Main outcomes:

- Classification error/accuracy and per-shift/per-class/group results.
- Excess error relative to immutable SOURCE and same-state KEEP.
- Harmful-update frequency at a declared tolerance, plus harm magnitude and severe-tail events.
- Local action regret: chosen loss minus minimum branched candidate loss from that same state/support/query.
- End-to-end latency, throughput, number of forward/backward passes, peak device memory and reset/state-copy/feature cost.
- Offline source preparation, selector data-generation and fitting cost separately.

Use paired stream comparisons and resampling that respects source seed, original image IDs, shared continuations and temporal blocks. Predeclare primary comparisons and handle multiplicity if formal significance is claimed. Specify what seed variation represents; classifier/stream/router seeds are not interchangeable.

## Oracle interpretation

A local hindsight oracle scores cloned actions on a fixed query after labels are revealed to the evaluator. It is unavailable to the selector and only diagnoses local headroom.

Independent best actions from a baseline's logged states form a **replay oracle**, not a realizable dynamic upper bound. A sequence oracle must create its own successor states and use a declared horizon/objective; exact search may be infeasible. Do not present a myopic action-loss predictor as solving full-stream optimal control.

## Steps to run

No implementation exists for this new protocol, so no runnable benchmark command is invented. Before execution: freeze a manifest; choose an authorized environment/hardware budget; implement state snapshots, transitions and evaluator separation; pin source checkpoint/data/library versions; then record exact **uv** commands and output paths here.

The present request is literature review and proposal, not authorization for training, package installation, dataset/checkpoint download, paid APIs or cloud experiments. No implementation tests are added or run by this task.

## Actual results

**None.** Historical local digit outcomes and user-reported five-seed normalization-gate aggregates belong to earlier records and are not results of this experiment.

## Interpretation and rejection rules

Reject the method direction if effects are negligible, require pathological histories/LRs, vanish after basic resets, are explained by current predictions, fail on autonomous runs, or disappear on unseen histories/models after costs. If plain equal-budget aggregation matches the proposed remedy, acknowledge the established principle and assess whether the controlled TTA finding alone is sufficiently important.

An outcome where no complex selector is needed is useful scientific evidence. It is not evidence for a successful shift-aware framework or a guaranteed publication.

## Next step

Finish the exact-overlap checks named in the review, then request/record execution conditions only when moving from this proposed study to an authorized implementation/run. Begin with Stage 1; do not launch the whole benchmark suite automatically.

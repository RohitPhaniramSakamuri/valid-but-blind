# Testing the value of additional evidence for adaptation selection

Experiment ID: 001. Status: **full protocol planned; bounded surrogate diagnostic completed**. Designed 23 October 2026.

The user subsequently authorized a 15-minute local run. [Actual diagnostic results](../outputs/shift-aware-tta-diagnostic-2026-10-23.md) and [code/artifacts](../diagnostics/2026-10-23/) describe the three-stage CPU surrogate study. The full original-benchmark, multi-architecture and continual-state protocol below was not completed by that smaller run.

Related sources: `Danilowski2026MORPHEUS`, `Jhawar2026Identifiability`, `Gai2026AdaTentPlusPlus`, `Yang2026SATTS`, `Doloriel2026SEGA`, `Jiang2026CAS`, `Sreeram2026Tempora`, `Weiss2013AdaptiveVOI`.

## Question and hypotheses

Can additional unlabeled views improve the selected parameter-update action, and can a cheap gate predict when that improvement justifies the observation cost on held-out shift families?

- H1: the cost-aware action oracle outperforms the best development-selected fixed action by a practically meaningful margin.
- H2: a richer-evidence selector outperforms an otherwise matched cheap selector on held-out families in a regime where acquisition cost can be justified.
- H3: predicting realized decision benefit allocates acquisition more effectively than random, fixed-schedule, entropy or selector-margin triggers at equal total cost.
- H4: the proposed policy retains useful adaptation gains while reducing harmful updates; simply choosing SOURCE everywhere does not satisfy H4.

H1–H3 are separate requirements. A failure at any stage can end the proposed controller study. No hypothesis is an actual result.

## Small worked example

The following numbers are invented to explain the objective. Suppose a cheap selector chooses Tent and produces 20% query error at 4 ms. An additional observation costs 2 ms and makes a richer selector choose BN adaptation, producing 12% error at 2 ms. At a declared conversion of one percentage point of error per millisecond, both paths cost 4 ms overall, and acquiring the observation reduces the combined objective by eight percentage points. On another episode the rich selector might choose exactly the same action, so acquisition wastes 2 ms. The gate must learn the difference using only information available before purchase.

Real costs must be measured; a forward pass on a batch is not interchangeable with a pass on one image. The conversion is a study parameter, not a universal economic value.

## Regime and legal information

**Primary regime:** supervised auxiliary development, followed by deployment with zero target labels. A labeled source development split supplies generated shifted episodes for training action-value predictors and the acquisition gate. No source images are required online; stored source statistics and frozen learned routing models are allowed and listed.

This is not a method requiring only arbitrary pretrained weights and nothing else. If only a pretrained checkpoint is available and no legitimate auxiliary development data can be obtained, the learned-controller protocol must change. Do not silently fit the router with final benchmark labels.

### Resolve the checkpoint and development split first

Preferred clean protocol: fit the source model on a declared subset of the source training data, retain disjoint images for router development, and reserve the official test identities for final evaluation. If using a checkpoint trained on all official source-training images, do not reuse those images as supposedly independent adaptation-benefit development cases. Instead obtain a legitimate independent labeled auxiliary split and state its provenance, or retrain the source model with an explicit hold-out.

Development shift-generation families, source-image partitions, selector fitting/calibration folds and final held-out corruption families must all be fixed before benchmark outcomes are inspected. Versions, checkpoint URL/hash, normalization and class mapping remain to be selected.

## State and prediction semantics

Start with **episodic adaptation** to isolate acquisition effects. Every episode begins from the same source checkpoint, normalization buffers and declared optimizer initialization. Steps:

1. Receive an unlabeled support batch \(S\).
2. Compute cheap evidence with the frozen source model in evaluation mode; this pass must not change BN running statistics.
3. The gate chooses immediate selection or the additional observation.
4. If purchased, compute fixed augmented views of \(S\), still with frozen source weights and buffers.
5. Select one terminal action and execute it on \(S\).
6. Predict on a subsequent disjoint query batch \(Q\); query labels are inaccessible to the policy.
7. Commit predictions. The evaluator later reveals query labels to calculate metrics.
8. Reset all state before the next primary episode.

This is a causal support-then-query adaptation decision, not an evaluation that adapts on query labels or uses the whole future target sequence. The main diagnostic assumes the episode's support/query relationship is specified; a shifted query distribution is a separate stress test. A same-batch transductive benchmark can be added as a separately labeled evaluation.

For counterfactual outcome generation offline, each action gets an independent clone of the **same pre-action state**, support batch and stochastic seed. Restore parameters, BN buffers, optimizer moments and any teacher/memory state consistently. Query computation must not mutate persistent buffers. Query-local normalization can differ by action if declared; no query gradients or future-query lookahead are allowed.

**Normalization detail:** native Tent commonly recomputes normalization statistics from its current batch. In the proposed support/query diagnostic, define a Tent-derived wrapper that updates affine parameters using support only and performs no gradient step on query images. If it uses query-batch statistics during prediction, declare that transductive use of the current query batch; do not describe the inference as pointwise frozen-statistics prediction. A variant using fixed support statistics is a different adaptation and must be named accordingly. Include a standard same-batch native-Tent evaluation separately before claiming comparison with published benchmark results. Resolve and record these semantics before implementation.

## Initial action menu

| Action | Implementation requirement | Interpretation |
| --- | --- | --- |
| SOURCE | Frozen weights and source normalization. | No adaptation; still produces an answer. |
| BN statistics | Fixed rule for blending or replacing statistics, then frozen query inference. | Forward-only normalization adaptation. |
| Tent-derived support update | Declared support/query wrapper, normalization semantics and fixed development-selected step count/rate. | Entropy-based affine update; distinct from a claimed exact native benchmark reproduction. |

Add ETA and/or SAR only after stage 0 establishes meaningful diversity. Distinguish ETA from Fisher-regularized EATA. A novel approximation to a baseline must be named as an adaptation of that method. The same menu is offered to learned selectors and analysis-only oracles.

No policy composition is included initially. Sequentially combining updates is noncommutative and adds a separate intervention/state question.

## Observation channels

### Cheap channel

One frozen-source support pass gives mean/dispersion of entropy, confidence and margin, predicted-class concentration, and compact hidden-feature summaries. Features obtained from that pass are charged for their computation but not as extra model forwards. Any source centroids or moments require documented source preparation. Do not supply true target class counts, corruption names or severity IDs.

### One additional observation action

Compute two globally declared, approximately label-preserving views per support image. The transformation policy is fixed on development data. Derive view disagreement, confidence changes and feature stability. Do not change transformation type when the evaluator changes from fog to blur. Verify suitability of transformations for each task; horizontal flips are not universally label-preserving.

Use these views for evidence only in the primary study. The selected adaptation action sees the same original support batch as the cheap-only policy. A separate control allows reusing views for adaptation/prediction, with identical access and charged cost for every comparator, to measure whether evidence-only acquisition is worthwhile.

## Learning without a contaminated acquisition target

1. On auxiliary episodes, execute all actions offline and record disjoint query losses and measured costs. This supervision generation cost is part of development, not hidden deployment computation.
2. Group episodes by original image identities, generation seed and shift construction. Split groups, not rows.
3. Within training folds, fit matched low-capacity action-loss predictors using cheap and richer evidence. Start with ridge regression or small tree ensembles, not a large controller network.
4. Predict actions on held-out development folds. Evaluate the **actions chosen by those out-of-fold selectors**, not the per-episode oracle, to obtain the observed net value of the additional evidence.
5. Fit the acquisition gate from cheap observations and those out-of-fold values. Use an outer development fold for acquisition thresholds and cost tradeoffs. No validation label may also be used as a final-test outcome.
6. Refit the selected configuration on the permitted development data and freeze it. Record nested-fold logic explicitly to prevent gate/selector coadaptation leakage.
7. At deployment, the gate sees only cheap evidence and the declared remaining budget. A bought observation allows the rich selector to choose an action; otherwise the cheap selector chooses. Never update the gate from unrevealed target correctness.

Define the acquisition-training target as query loss plus **all-in route cost** for the out-of-fold cheap choice, minus query loss plus all-in route cost for the out-of-fold rich choice. Include selector inference, feature processing, augmented forwards, state operations, terminal updates and prediction in route costs. Shared costs cancel only inside that paired target; they remain present in comparisons with direct SOURCE. The learned gate's own inference is additionally charged for the deployed controller.

The gate can begin as a regression predicting net benefit, with a fixed positive trigger margin. Prediction intervals calibrated on development shifts have empirical meaning there; they do not guarantee target safety under arbitrary new mechanisms.

Finite query batches make each realized gain noisy. Prefer gain regression or a development-fixed indifference region around zero over treating every tiny positive value as a reliable acquisition label. Inspect paired query-loss uncertainty and increase diagnostic repeats when the effect is unresolved.

Validate the final refitted cheap/rich selectors together with the gate on held-out development episodes before freezing the system: selectors refit on more data can behave differently from the fold-trained models that generated gate targets. Keep this stacking mismatch visible. Match selector family and tuning budget, and include a higher-capacity cheap selector to check whether apparent information gains are actually model-capacity gains.

## Stage 0: headroom and actual cost

Use small development-only data and a compatible source model. Profile all three terminal actions, the evidence pass, added views, feature summaries and gate inference on the intended hardware.

Construct a few corruptions representing different mechanisms, two severities, two batch sizes, balanced and imbalanced label mixtures, and several independent episode seeds. This is scoping data and cannot later become the final untouched test set. Report per-action outcomes, oracle-versus-fixed headroom, confidence in action differences, and the cost frontier.

Stop if all methods are effectively tied, a fixed action dominates at relevant budgets, or acquisition is more expensive than any plausible selection gain. Small pilots may be inconclusive; add repeats to resolve uncertainty before asserting that headroom is absent.

## Stage 1: isolate acquisition value

With image identities disjoint, compare cheap and richer selectors under leave-one-whole-corruption-family-out evaluation. Rotate outer family holdouts; each fold trains and calibrates only on permitted families. Predeclare which transformations constitute development families and which are unavailable until evaluation.

Two axes must be separated:

- Extra evidence improves selection before its cost is charged.
- That improvement survives total-cost accounting.

If the richer selector provides no out-of-family improvement, a learned purchase gate has no supported mechanism. If it improves actions but loses after cost, report an information–computation tradeoff rather than claiming efficient adaptation.

## Stage 2: locked generalization and controls

Test held-out within-image corruption compositions, single-class/imbalanced bursts, abrupt transitions, recurring source/clean segments and mixed-domain windows. Generated compound corruptions are a custom stress set; they are not standard CIFAR-C results. Publish the generation order, parameters, seeds and hashes. Keep domain labels available to the evaluator only.

After the episodic mechanism survives, separately evaluate a continuous stream. Define live KEEP versus reset-to-SOURCE distinctly. Update the development data generation so candidate actions are evaluated from clones of live states, not pristine source states. Report optimizer/BN/teacher/memory reset semantics and delayed clean-return effects. Episodic training success alone cannot support a continual deployment claim.

External validation: a second backbone with appropriately compatible actions, then a named DomainNet-126 transfer protocol or another natural-domain dataset. ImageNet-C and a specified WILDS task are later extensions. Do not promise all of them before profiling and data access.

## Comparisons

### Adaptation and selection

- SOURCE; each fixed action; fixed action selected using development data.
- Analysis-only best fixed action on test, clearly labeled optimistic hindsight.
- Analysis-only per-episode action oracle with and without cost, never called a deployable method.
- A simple shift classifier followed by a development-learned action map; corruption IDs are training labels only.
- MORPHEUS-style pre-action selection on the common menu; report reproduction differences.
- Global versus order-aware evidence predictors motivated by the identifiability paper; match their legal access and timing to this protocol.
- Relevant robust fixed TTA alternatives (ETA/SAR/ROID and DeYO) as the menu grows. Their availability does not justify an unfairly weak fixed baseline in the final study.

### Acquisition

- Never acquire; always acquire.
- Random acquisition at a matched development-fixed rate and budget.
- Fixed schedule or fixed observation count.
- Entropy-triggered acquisition, selector-margin-triggered acquisition and a SA-TTS-inspired uncertainty cascade.
- CAS-inspired cross-view adapt/skip and SEGA-inspired sensitivity gating where their action/task assumptions can be matched. These are adaptations unless their native setting is separately reproduced.
- Proposed learned decision-value gate.
- Frozen-model same-cost augmentation/ensembling, to detect gains that require no adaptation selection.

A matched acquisition fraction is useful but insufficient: policies may select terminal actions with different costs. Match the full runtime budget and show complete cost/error curves. Charge all post-adaptation candidate scoring if adding Cygert-style proxy selection.

## Measurements

For each episode/action/policy, record:

| Quantity | Definition and interpretation |
| --- | --- |
| Query error and NLL | Classification error and probability loss on disjoint query examples. |
| Combined objective | Query loss plus the predeclared cost penalty; also show each component separately. |
| Action-oracle regret | Combined objective minus the best allowed terminal action on that episode; charge unavoidable information cost consistently and disclose oracle information. |
| Gain over fixed policy | Difference from the development-selected fixed action at equal total cost. |
| Harmful adaptation | Selected action worsens query performance versus SOURCE by a declared margin; report magnitude and frequency. |
| Correct-to-wrong and wrong-to-correct | Paired query prediction transitions relative to SOURCE. |
| Acquisition effectiveness | Selection changes, loss changes, positive net-gain fraction, budget spent and missed useful acquisitions. |
| Update benefit capture | Gains obtained relative to available action headroom; accompanies SOURCE-choice rate. |
| Runtime and deadlines | End-to-end median and tail latency, throughput, deadline misses and a Tempora-style utility where appropriate. |
| Resource cost | Forward/backward image counts, state-copy and feature costs, peak memory; energy only if measured. |

There are two different oracle diagnostics: (1) terminal action oracle with free perfect outcome knowledge, a lower bound on achievable loss; (2) acquisition oracle choosing between the fitted cheap and rich policies after paying their real execution costs. Neither is a deployed competitor or a learned guarantee. Avoid rewarding an oracle by omitting mandatory evidence costs while charging them to only one method without explanation.

Report per-family and worst-regime results as well as averages. Use paired episode- or full-stream-level bootstrap intervals with independent image groups/streams as units. Repeat declared seeds; group the same underlying image/episode across all compared methods. Batches inside a continuous stream are dependent. Hypothesis multiplicity and final-test reuse must be documented.

## Falsification and stop criteria

Predeclare a practical improvement threshold using development variability and deployment needs, not final-test outcomes. The project does not yet assign a numeric minimum gain without profiling.

- No action diversity or oracle headroom: the selection premise fails for that regime.
- Richer evidence cannot improve action choice on held-out families: the acquisition premise fails.
- Learned purchase does not beat random/entropy/ambiguity allocation under matched total cost: the claimed acquisition mechanism fails.
- Gains arise only from prediction ensembling or an action getting extra adaptation views: evidence-only selection is not established.
- Performance requires corruption IDs, same-image leakage, target-label tuning or future lookahead: the intended protocol fails.
- Consistently harmful updates or poor clean-return behavior: average shifted accuracy cannot establish a robust controller.

## Environment and reproducibility records to create before running

The bounded diagnostic used existing local CPU libraries; its manifests record versions, source parameters and splits. No GPU/cloud environment has been selected for the larger study. Do not infer current funding or deadlines from older projects. Record hardware, environment, code/checkpoint versions, data/split provenance, parameters, seeds and exact commands before scaling. The user explicitly requires uv instead of pip for Python setup and execution.

Save predictions, selected actions, all evidence costs, development out-of-fold predictions, meta-training folds, frozen configuration and every negative result. The initial deliverable should be an action-outcome table and error–cost plot, followed by the acquisition comparisons if headroom exists.

## Actual results

The bounded alternate-data run completed three source/split repeats on the bundled digits dataset. It demonstrates action headroom and variable richer-evidence gains, but calibration rejected acquisition at all positive tested cost penalties. See the [results report](../outputs/shift-aware-tta-diagnostic-2026-10-23.md) for actual outcomes, caveats and omitted parts. No result on CIFAR-C, ImageNet-C, DomainNet or WILDS has been produced.

## Next step

Keep the negative acquisition finding. A simpler cheap selector on a faithful larger model with fresh evaluation is a possible follow-up; the present run does not justify automatic scaling.

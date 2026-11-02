# Cheap harm prediction for test time normalization

Working approach selected for definition on 23 October 2026. Status: proposed study and simple method; the existing digit gate remains a post-hoc pilot, not validation of this design. No new experiment is authorized or run by this definition.

## Decision

Study a small controller that chooses between the unchanged source model and a single normalization update. Its core empirical question is:

> When can predicted-class concentration support the decision to normalize, and when does corruption-induced prediction collapse make that signal misleading?

This follows the completed diagnostic: useful actions varied with class composition; richer evidence helped inconsistently; acquisition failed to justify its cost under the tested positive penalties. The narrow study retains a decision that can be measured and removes extra-view acquisition from the main method. It does not claim a new general adaptation framework.

## Intuition and example

Suppose 80 of 100 images receive the same predicted class. Two explanations are possible:

- The incoming batch actually contains mostly that class.
- The batch contains many classes, but corruption makes the source classifier output the same class repeatedly.

The controller sees predictions and features, not the true class proportions. A concentration threshold alone may give the same decision in both cases. We want to learn whether cheap additional summaries separate cases in which normalization helps from cases in which it hurts. Neither explanation automatically implies a particular correct action; measure the effect of both actions.

## Exact method

### Source preparation

Use a source-trained classifier with a declared normalization layer and source feature moments. Estimate stored moments using source training data only. For the small existing architecture, the action operates on normalized hidden features. A later full-network BatchNorm evaluation is a different, explicitly costed implementation.

### Runtime inputs

For an unlabeled support batch B, run the frozen source model and compute three scalar features:

1. **Predicted-class concentration c:** the fraction of support examples assigned to the most common predicted class. This measures output concentration, not the true class prior.
2. **Mean predictive entropy h:** how spread out the model's probabilities are, averaged over the batch. Low entropy can still accompany confident mistakes.
3. **Source-relative feature displacement d:** average absolute displacement of support feature means from stored source means, scaled by source standard deviations. Both corruption and changing class proportions can change this statistic; it is not a causal shift detector.

With feature dimension j from 1 to D, define the third feature as

\[
d(B)=\frac{1}{D}\sum_{j=1}^{D}
\frac{|\mu_{B,j}-\mu_{S,j}|}{\sqrt{\sigma^2_{S,j}+\epsilon}}.
\]

Here mu_B is the mean feature vector of the support batch, mu_S and sigma_S squared are source feature means and variances, D is the number of feature coordinates, and epsilon is a fixed positive numerical guard.

### The gate

Fit one depth-two regression tree using only these three features. Its target is measured auxiliary-development query error of SOURCE minus query error after normalization. Positive target values mean the update helped. A depth-two tree has at most four leaves, so the controller can be inspected and has little inference cost.

At deployment:

\[
\text{use normalization if }\widehat{\Delta}(c,h,d)>\tau;
\quad\text{otherwise use SOURCE}.
\]

Delta-hat is predicted error reduction; tau is one global development-calibrated margin. Calibration selects the margin under a declared error-plus-total-cost objective. It may select SOURCE everywhere; that is a failed adaptation claim, not a result to conceal. A positive-margin rule is empirical and does not guarantee safety on arbitrary new shifts.

### Allowed actions

- SOURCE: retain the source normalization and output its predictions.
- NORMALIZE: estimate declared normalization statistics from support, apply them to the classifier, and output predictions without gradient descent.

Every episode begins from the same source state. Support-derived statistics remain fixed when scoring a disjoint subsequent query batch. All model weights remain fixed. SOURCE is an answering action; it does not defer the input to a human.

No extra augmentation views, entropy-gradient optimization, online controller training or target labels are required at runtime. Do not call the full pipeline one-pass without measuring its implementation: an unchanged full-network pass followed by an adapted full-network pass is two passes. With the existing hidden-normalization architecture, cached activations may permit only a classifier-head recomputation; that advantage cannot be silently generalized to a deep BatchNorm network.

## Where the research contribution could lie

The intended contribution is a **controlled empirical characterization of a policy-selection failure**, accompanied by a minimal baseline. The gate is an instrument to test the hypothesis; its architecture does not itself establish novelty.

Construct two families of episodes:

1. A changed true class mixture with little corruption.
2. A balanced true class mixture under corruption that concentrates source predictions.

Use true labels only to construct/evaluate the research conditions. Match or stratify episodes by the **observed pre-action concentration c**, using bins/calipers fixed on development data. Never select matches because evaluation labels reveal opposite adaptation benefits. Record unmatched cases and the fraction of data covered; keep full, unmatched evaluation results too.

Then ask:

- Do comparable concentrations actually occur in both families?
- At comparable concentration, do normalization benefits differ meaningfully?
- Do h and d improve the action decision over c alone?
- Does that improvement transfer to unseen dominant classes and corruption families, after total cost is charged?

If overlap is absent or actions do not differ, report that and do not manufacture a matching success. If the three features cannot resolve relevant ambiguity, state the observed limit rather than claim the model recognizes the shift cause.

## Offline supervision and data separation

Source labels train the classifier. Separate labeled auxiliary-development episodes score both SOURCE and NORMALIZE on disjoint query cases, providing gate-training targets. Use grouped fitting/validation so the same underlying image does not appear in both development and evaluation. Freeze the gate and margin before a fresh final test.

Keep all source classes available to the source classifier. Hold out the **identity of dominant target classes** from gate development, in addition to holding out whole corruption families. A dominant-class holdout does not mean holding that class out of source training.

Deployment uses unlabeled support only. Neither final query features nor their labels enter the gate. Source-derived means and variances are explicitly permitted preparation; this is not an arbitrary-weights-only setup. The existing digit evaluation has already informed the design, so further reuse is exploratory. A claim of transfer needs a new fixed split or dataset/model protocol.

## Evaluation and required comparisons

Use the same classifier, source checkpoint, support/query draws and legal information for each comparison:

- SOURCE and always-normalize.
- Concentration-only, entropy-only and displacement-only gates.
- The three-feature depth-two gate.
- A development-selected fixed action and a clearly labeled hindsight action oracle.
- Channel-selective normalization and an imbalance-aware normalization method such as NOTE/DELTA/TRIBE in a later faithful model experiment. Until those comparisons are made, do not claim superiority to imbalance-aware TTA.

Primary outcomes are query accuracy/error, harm relative to SOURCE, action regret, useful normalization gains captured and total inference cost. Report each corruption/prior regime as well as averages. Count the source forward, feature calculations, gate, state operations and any adapted rerun. Report use-normalization frequency: choosing SOURCE everywhere is not evidence of a useful adaptation policy.

The claim succeeds only if the three-feature gate beats the strongest one-feature gate and the development-selected fixed action on untouched regimes by a meaningful margin, without losing its value after cost. The matched-concentration study must independently support the proposed failure mechanism. Improvement against always-normalize alone is inadequate.

## Closest prior work and novelty limits

[NOTE](https://arxiv.org/abs/2208.05117) already addresses normalization under correlated, class-biased streams. [Channel-Selective Normalization](https://proceedings.mlr.press/v274/vianna25a.html) directly studies covariate plus label shifts and selectively adapts channels. MORPHEUS and the [TTA identifiability preprint](https://arxiv.org/abs/2609.11235) already study selecting actions and limits of observable evidence. Thus class imbalance, SOURCE-versus-update selection and a few prediction statistics are established ingredients.

The exact matched-concentration, held-out-dominant-class experiment is a **candidate scope requiring further full-method overlap checks**, not a verified open gap. The user's urgency does not change that evidence requirement.

## Evidence we currently have

The [digit diagnostic](shift-aware-tta-diagnostic-2026-10-23.md) supports investigating action differences. Its post-hoc concentration rule reached 80.52% versus 76.46% SOURCE accuracy on one existing held-out-family split, while costing about 5.8 times as much as direct SOURCE inference in that implementation. Positive cost penalties selected direct SOURCE. That result motivates a cheap baseline, but it does not validate the three-feature tree, fresh generalization, efficiency or a publishable contribution.

## Deliverable and immediate next step

The deliverable would be an empirical paper centered on the limits and usefulness of cheap adaptation decisions, with the gate as a reproducible baseline. A high-quality-conference contribution is not established by the current toy study. Defining a smaller method does not remove the need for stronger external evidence.

Next concrete step, when execution is requested: freeze the exact three-feature gate and matching protocol, check the closest methods' evaluation details, and run a fresh confirmation before treating the post-hoc rule as a research result. Use uv for all Python execution and dependency management.

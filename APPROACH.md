# Historical approach: Cheap Harm Prediction for Test-Time Normalization

Status note, 26 October 2026: preserved from the earlier approach-selection task. The user subsequently authorized a fresh novelty assessment. See the [current review](outputs/shift-aware-tta-deep-review-2026-10-26.md) and [new planned diagnostic](experiments/002-state-conditioned-selection.md). This earlier gate is not presumed novel or the current recommendation.

## Method

Given an unlabeled support batch, run the frozen source classifier and compute:

1. **Predicted-class concentration:** the fraction of examples assigned to the most frequently predicted class.
2. **Mean predictive entropy:** the average uncertainty of the predicted probability distributions.
3. **Feature displacement:** the average absolute difference between support-feature means and stored source-feature means, divided by source-feature standard deviations with a fixed numerical guard.

Feed these three values into a depth-two regression tree that predicts the reduction in classification error from updating normalization statistics.

Apply the normalization update when predicted error reduction exceeds a globally calibrated threshold. Otherwise, use the unchanged source model. Keep classifier weights fixed. Estimate normalization statistics from support inputs and freeze them when predicting on a separate query batch.

## Gate Training

Construct labeled auxiliary-development episodes with varied corruptions and class proportions. Each episode contains disjoint support and query images.

Evaluate both actions from the same source state. Use query error of the unchanged model minus query error after normalization as the tree's training target. Fit the tree using only the three support-derived signals. Select the threshold on separate calibration data using classification error plus measured total computation cost.

Keep original image identities disjoint across training, calibration and final evaluation. Freeze the tree and threshold before final evaluation. Target labels are unavailable during deployment.

## Evaluation

Compare genuinely class-concentrated batches with class-balanced corrupted batches that produce similar predicted-class concentration. Define matching bins or tolerances on development data, without using adaptation outcomes to select matches.

Hold out entire corruption families and dominant-class identities from gate development while retaining all classes in source-classifier training. Measure whether normalization benefits differ at matched concentration and whether entropy and feature displacement improve action selection.

Compare against the unchanged model, always normalizing, each single-feature gate, and established imbalance-aware normalization methods. Report accuracy, harmful-update frequency, action regret and total inference cost, including source passes, feature computation, gating and any adapted rerun.

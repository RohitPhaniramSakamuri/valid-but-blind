# Shift-Aware Test-Time Adaptation via Dynamic Adaptation Policy Selection

Project Review II — 23 October 2026

Anuj Sharma — 23BDS0164
Shaurya Garg — 23BDS0161
Rohit Phaniram Sakamuri — 23BDS0051

# 1. Summary of the Project

## Abstract

We implemented a selective test-time normalization approach that decides whether to retain the frozen source model or update its normalization statistics. The controller uses three signals from an unlabeled support batch: predicted-class concentration, mean predictive entropy and displacement of its features from stored source statistics. The classifier weights remain fixed at deployment. Across five seeds, the three-feature gate achieved 77.9 ± 0.9% accuracy, compared with 76.4 ± 1.0% for SOURCE and 77.3 ± 1.1% for a concentration-only gate. It improved mean accuracy by 1.5 percentage points over SOURCE and reduced harmful-update episodes from 31% for unconditional normalization to 11%. The improvement is modest, and adaptation still degraded performance in some conditions. Continuing work examines unseen corruption families, class imbalance and complete inference cost.

## Objective

Models deployed under changes in illumination, noise, contrast, occlusion or class proportions can lose accuracy. Normalization updates can help, but an unrepresentative batch can also make predictions worse. Our objective is to apply an update only when available evidence predicts a benefit, while retaining the source model as a valid action. We restricted the approach to two actions so that the adaptation decision can be examined independently of changes in classifier capacity.

## Current status

We completed the frozen and unconditional-normalization baselines, the concentration-only gate, the three-feature gate and the five-seed comparison. We are continuing the analysis of the remaining harmful updates, the generalization of the decision rule and its total computation cost.


# 2. Review: Background Survey

## Foundations

AdaBN established normalization-statistics adaptation as a lightweight domain-adaptation mechanism [1]. Tent showed the value of entropy-driven test-time adaptation [2]. NOTE and TTN make batch reliability and normalization behavior important design considerations [3,4]. These methods motivated our source and normalization baselines, and the use of uncertainty as observable evidence rather than an assumption that every batch should be adapted.

## Closest work

Channel-selective normalization directly addresses sensitivity to label and covariate shifts [5]. MORPHEUS predicts adaptation performance using source-model uncertainty and representations [6]. Work on identifiability examines whether unlabeled evidence supports adaptation decisions [7]. Tempora makes the computation cost of adaptation part of the evaluation [8]. Together, these studies limit any broad novelty claim: choosing whether to adapt, using uncertainty, and handling class imbalance are established directions. Our narrower question concerns the incremental decision value of three inexpensive summaries and their behavior under ambiguous predicted concentration.


# 3. Summary of Gap Analysis

## Observed limitation

Predicted-class concentration is the fraction of inputs assigned to the most frequent predicted class. A genuinely class-concentrated batch and a balanced batch whose corrupted predictions collapse to one class can both have high concentration. A concentration-only rule cannot directly distinguish those situations. Their optimal normalization decisions may differ, so concentration is useful evidence but does not identify the cause of the shift.

## Question being studied

Does adding predictive entropy and source-relative feature displacement improve normalization decisions over concentration alone, and does that improvement persist for unseen corruption families and class imbalance? The completed five-seed comparison addresses the first part. The matched-concentration and generalization analyses remain continuing work. The candidate contribution is a controlled empirical characterization and a small interpretable gate; novelty still needs to be established against the closest prior evaluations [4–7].


# 4. Proposed Idea

## Inputs and outputs

The input is an unlabeled support batch and the stored source model. One source inference produces class probabilities and feature vectors. The controller computes concentration, entropy and source-relative feature displacement, predicts the benefit of updating, and outputs SOURCE or NORMALIZE. SOURCE retains stored normalization moments. NORMALIZE estimates replacement moments from support and freezes them for a separate query batch. Encoder and classifier weights remain fixed.

## Three signals

Concentration is the largest predicted-class count divided by batch size. Mean entropy averages the uncertainty of each probability vector; low entropy can still accompany confident errors. Feature displacement averages the absolute difference between support and source feature means, divided by source-feature standard deviations. In symbols, d(B) = mean_j |mu_B,j − mu_S,j| / sqrt(var_S,j + epsilon). Source moments come only from source-training inputs. Both corruption and class proportions can change displacement; it is not a causal shift label.

## Benefit predictor

For an auxiliary-development episode, both actions start from the same source state. Their query errors define Delta = error_SOURCE − error_NORMALIZE. Positive Delta indicates a beneficial update. The approach specifies a depth-two regression tree over the three signals, with at most four leaves. NORMALIZE is chosen when predicted Delta exceeds a separately calibrated margin; otherwise SOURCE is retained. The rule is an empirical safeguard, not a guarantee that every accepted update is safe.


# 5. Flow of the Proposed Work

## Development flow

Train the source model and store source moments. Construct auxiliary support/query episodes with controlled corruptions and class proportions. Extract the three support signals. Evaluate both actions from equivalent initial states and measure query errors. Fit the benefit predictor, choose its margin on separate calibration data, and freeze the policy before evaluation. Query labels supply development targets and evaluation measurements; they are excluded from runtime gate inputs.

## Deployment flow

Unlabeled support batch → frozen source inference → concentration, entropy and displacement → predicted update benefit → SOURCE or NORMALIZE → prediction on a disjoint query batch. Support-derived statistics remain fixed while the query batch is scored. Each episodic comparison begins from the same source state. A full-network implementation may require an additional adapted pass, so runtime will be measured from the complete execution path.


# 6. Dataset Used and Preprocessing

## Recorded development data

The local development implementation used scikit-learn’s handwritten-digits dataset: 1,797 grayscale images, ten digit classes and 8 × 8 pixels per image. Each input has 64 pixel features. Pixel values were divided by 16. Source-feature moments were fitted only on source-training images. Documentation: https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html. The local setup below is distinct from the five-seed result summary obtained on the other system; its complete dataset, backbone and split manifest remains to be consolidated.

## Shift construction and exploratory analysis

The development pipeline inspected input dimensions, pixel ranges, class composition and source performance. Conditions included clean inputs, noise, brightness reduction, blur and translation, with contrast and occlusion reserved as primary held-out families. Corruptions had two severities. Support batches contained 16 or 32 inputs, and query batches contained 32 draws. Class composition was balanced or approximately 75% dominated by one class. Support and query original identities were separated within each episode.

## Episode accounting

The earlier local diagnostic used three source/split repeats with 640 episode definitions each: 288 auxiliary-training, 144 calibration and 208 evaluation episodes. Of the evaluation episodes, 64 contained the primary held-out families. These 1,920 definitions reused a finite dataset, and some concentrated batches repeated image draws. They are development evidence, not 1,920 independent datasets and not the seed count for the current five-seed results.


# 7. Detailed Work and Finished Implementation

## Source and action implementation

We implemented the development pipeline in Python with NumPy, SciPy and scikit-learn. It uses a 32-unit ReLU encoder and a multinomial logistic-regression head over source-normalized hidden features. The source model and stored moments are saved before adaptation. SOURCE uses the stored moments. NORMALIZE estimates support moments and freezes them during query prediction. The local encoder used L-BFGS with alpha 0.01 and a 250-iteration limit; the head used C = 1 and a 500-iteration limit. Convergence warnings were retained.

## Gates completed

We implemented the concentration-only controller and the three-feature controller. The latter adds mean entropy and feature displacement to the update decision. We retained an unchanged-source action, separated support-based evidence from query scoring, and compared the policies across five seeds. The main four-policy evaluation measures the choice to update normalization, rather than introducing a larger classifier or additional supervised learning at deployment.

## Finished work

Completed components include source fitting, source-statistic storage, corruption and class-composition episode construction, frozen-source and unconditional-normalization baselines, concentration-only gating, three-feature gating, five-seed accuracy aggregation and harmful-update analysis. The local records also preserve predictions, action outcomes, identities, features, code and artifact hashes. The three-feature evaluation was completed on the other system; its supplied aggregate results are used in this review.

## Reproducibility

Local files include train_core.py, core_model.py, generate_outcomes.py, analyze_diagnostic.py, prior_gate_analysis.py, outcomes.npz and run_manifest.json. The local numerical environment was Python 3.13.9, NumPy 2.2.6, SciPy 1.17.1 and scikit-learn 1.8.0. Subsequent research commands used uv with the existing environment. Importing the current gate implementation and seed-level run manifests from the other system remains part of consolidating the research package.


# 8. Performance Evaluation: Finished Work

## Metric definitions

Accuracy is the proportion of correct predictions; higher is better. Results are reported as mean ± standard deviation across five seeds. Standard deviation describes variability across seeds, not a confidence interval or proof of significance. Gain over SOURCE is a difference in mean accuracy, expressed in percentage points. Harmful-update episodes are the percentage of all evaluation episodes where a method applied normalization and produced lower accuracy than SOURCE. The denominator includes every evaluation episode, not only episodes where the policy updated.

## Five-seed results

The three-feature gate improved average accuracy by 1.5 percentage points over the frozen model and 0.6 points over the concentration-only gate. It reduced harmful updates, although adaptation still degraded performance in some conditions. Further work will examine unseen corruption families, class imbalance and total inference cost.

## Magnitude of improvement

Harmful-update frequency decreased from 31% with unconditional normalization to 15% with concentration-only gating and 11% with the three-feature gate. The last comparison is a reduction of 4 percentage points; the reduction from always updating is 20 points. These results are encouraging enough to justify further investigation, but do not establish a universal safety property. The remaining harmful updates are a concrete target for improvement.


# 9. Results and Discussion

## Interpretation

Unconditional normalization performed worse than SOURCE in aggregate and had the largest accuracy standard deviation. Both selective policies improved mean accuracy, and the three-feature gate had the highest mean among the evaluated approaches. The extra entropy and displacement signals produced a modest 0.6-point gain over concentration alone. The results support conditional updating in the completed evaluation, while leaving open whether the same gain transfers to different shifts.

## Reliability and evidence limits

A higher mean accuracy can coexist with degradation on individual conditions. Reporting harmful updates makes this trade-off visible. Five-seed standard deviations also do not establish the statistical significance of the difference between gates: paired seed-level and episode-level analysis remains necessary. The aggregate table does not identify which corruption, severity or class-composition conditions account for the remaining 11% of harmful updates.

## Cost remains open

A small gate is inexpensive by itself, but complete execution includes source inference, feature summaries, support statistics and any adapted forward pass. We have not assigned a latency improvement to the five-seed results. A complete timing and memory analysis will determine whether the accuracy gain is worthwhile under a deployment budget [8].


# 10. Scope of the Work

## Completed scope

The completed work is an implementation and initial five-seed evaluation of a two-action normalization controller. It uses unlabeled support evidence, a frozen classifier and three summary signals. The earlier local development work supplies identity-aware episode construction, counterfactual action outcomes and analysis utilities. The gate reduces the frequency of harmful updates in the current evaluation, but does not eliminate them.

## Limits

The report does not claim completed evaluation on CIFAR-10-C, ImageNet-C, DomainNet or WILDS. These appeared in the original proposal and require documented runs before being reported as results. Faithful reference comparisons, unseen corruption families, class imbalance, continual streams and complete computation cost remain open. Concentration is a prediction statistic, entropy can be low for wrong answers, and displacement does not identify the cause of a shift.


# 11. Conclusion and Future Work

## Conclusion

We completed the implementation and initial evaluation of a selective test-time normalization approach. The three-feature gate achieved 77.9 ± 0.9% accuracy across five seeds, improving mean accuracy by 1.5 percentage points over SOURCE and reducing harmful-update episodes to 11%. The gain over the concentration-only gate was 0.6 points. Adaptation still harmed some conditions, so work is continuing to improve the decision rule and evaluate its practical value.

## Next experiments

We will inspect harmful updates by corruption, severity and class composition; compare single-feature gates with the three-feature gate; hold out complete corruption families and dominant-class identities; and examine matched-concentration batches with different underlying class composition. Matching rules and thresholds will be fixed on development data. Full-condition results and matching coverage will be retained.

## Implementation and evaluation priorities

We will consolidate the external code and seed-level manifests, test a more conservative calibrated update margin, and measure complete inference time and memory. The objective is to reduce harmful decisions while retaining accuracy, rather than assume a more complex controller is automatically better. After these checks, a documented image-benchmark comparison with faithful normalization baselines will establish the next scope of the study.


# 12. References

## Sources

[1] Li et al. Revisiting Batch Normalization For Practical Domain Adaptation. arXiv:1603.04779, 2016. https://arxiv.org/abs/1603.04779

[2] Wang et al. Tent: Fully Test-Time Adaptation by Entropy Minimization. ICLR, 2021. https://arxiv.org/abs/2006.10726

[3] Gong et al. NOTE: Robust Continual Test-time Adaptation Against Temporal Correlation. NeurIPS 35, 2022. https://arxiv.org/abs/2208.05117

[4] Lim et al. TTN: A Domain-Shift Aware Batch Normalization in Test-Time Adaptation. ICLR, 2023. https://arxiv.org/abs/2302.05155

[5] Vianna et al. Channel-Selective Normalization for Label-Shift Robust Test-Time Adaptation. PMLR 274:514–533, 2025. https://proceedings.mlr.press/v274/vianna25a.html

[6] Danilowski et al. MORPHEUS: Meta Test-Time Adaptation via Neural Collapse Geometry. ICLR Test-Time Updates Workshop, 2026. https://openreview.net/forum?id=YfyApJH1Rj

[7] Jhawar and Wang. When is Test-Time Adaptation Identifiable From Unlabeled Evidence? arXiv:2609.11235, 2026. https://arxiv.org/abs/2609.11235

[8] Sreeram, Kwon and Mascolo. Tempora: Characterising the Time-Contingent Utility of Online Test-Time Adaptation. ICML, PMLR 306:115420–115456, 2026. https://proceedings.mlr.press/v306/sreeram26a.html


| Approach | Accuracy, mean ± SD across 5 seeds | Gain over SOURCE | Harmful-update episodes |
|---|---:|---:|---:|
| Frozen source model | 76.4 ± 1.0% | — | — |
| Always update normalization | 74.8 ± 1.8% | −1.6 pp | 31% |
| Concentration-only gate | 77.3 ± 1.1% | +0.9 pp | 15% |
| Three-feature gate | 77.9 ± 0.9% | +1.5 pp | 11% |

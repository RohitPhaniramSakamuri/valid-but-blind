# Superseded preparation draft

This preparation draft predates the user's five-seed results. Use [the current review](review-ii-five-seed-progress.md) and the files in `../reports/review-ii/`. The metrics below belong to the earlier local diagnostic and were not used as the five-seed results in the delivered report.

# Shift-Aware Test-Time Adaptation via Dynamic Adaptation Policy Selection

## Project Review II — Progress Report

Anuj Sharma — 23BDS0164  
Shaurya Garg — 23BDS0161  
Rohit Phaniram Sakamuri — 23BDS0051

Report date: 23 October 2026

Working method: Cheap Harm Prediction for Test-Time Normalization

# 1. Summary of the Project

## Abstract

We investigated whether a classifier should update its normalization statistics on every incoming batch or first decide whether the update is likely to help. We implemented a CPU experiment pipeline with a frozen source classifier, support-based feature normalization, an entropy-based affine adaptation baseline, and adaptation-policy selectors. The completed study used 1,797 handwritten-digit images and three source-training and data-split seeds. Across these runs, we constructed 1,920 episode definitions and evaluated three adaptation actions per episode. These episodes reused the same underlying dataset.

The initial results showed that normalization behaved differently under balanced and class-concentrated input batches. On the first split's held-out contrast and occlusion conditions, the frozen source model achieved 76.46% accuracy. A concentration-based gate achieved 80.52% accuracy and reduced the frequency of episodes with increased error from 48.44% for unconditional normalization to 6.25%. However, the gate's average measured route cost increased from 0.069 ms to 0.403 ms. The gate was introduced after examining the initial action breakdown, so its improvement remains exploratory. Our continuing work focuses on a three-feature, depth-two decision tree that predicts the benefit of normalization, followed by fresh evaluation under held-out shifts and class compositions.

## Problem and objective

A model trained on one input distribution may encounter different brightness, contrast, noise, occlusion or class proportions after deployment. Updating normalization statistics can help align its internal features with the incoming data. The same update can also remove useful information or distort features when a batch contains mostly one class. Our objective is to retain the source model when adaptation is likely to increase error and apply a small normalization update when the expected improvement justifies its cost.

We narrowed the broad policy-selection idea to two deployment actions: SOURCE, which retains the source statistics, and NORMALIZE, which estimates new statistics from an unlabeled support batch. This limits the controller's complexity and makes its decisions easier to inspect. Runtime target labels are unavailable. Labeled auxiliary data are used during development to learn which action was beneficial.

## Current progress

We completed the source-model implementation, corruption and episode construction, three-action baseline evaluation, cheap and richer evidence selectors, a concentration-only gate, repeat runs, and result analysis. The current method specification extends the concentration gate with predictive entropy and source-relative feature displacement. Implementation refinement and fresh confirmation of this three-feature gate remain the next stage; the metrics in this report describe the completed baseline and diagnostic implementations.

# 2. Review: Background Survey

We organized the literature around normalization, entropy-based adaptation, class-composition sensitivity, adaptation selection and computation cost. The review catalog contains 48 primary sources with recorded reading scopes. The following eight works directly informed the present approach.

| Work | Main idea relevant to this project | How it informed our work |
| --- | --- | --- |
| Li et al., 2016, AdaBN [1] | Adapt feature-normalization statistics to a different domain. | Motivated a lightweight statistics-only adaptation action. |
| Wang et al., 2021, Tent [2] | Adapt normalization-related parameters by minimizing prediction entropy. | Motivated the support-only entropy-affine baseline. |
| Gong et al., 2022, NOTE [3] | Address unreliable adaptation under temporally correlated inputs. | Established that batch composition and stream structure need explicit consideration. |
| Lim et al., 2023, TTN [4] | Make normalization sensitive to domain shift. | Showed that normalization-policy adaptation is an established direction. |
| Vianna et al., 2025, Channel-Selective Normalization [5] | Improve normalization robustness when label and covariate distributions change. | Provides a close comparator for the planned class-composition evaluation. |
| Danilowski et al., 2026, MORPHEUS [6] | Predict adaptation performance using source-model representation and uncertainty information. | Establishes prior work close to a learned adaptation selector. |
| Jhawar and Wang, 2026 [7] | Study when unlabeled evidence supports adaptation decisions. | Motivated testing ambiguous evidence rather than assuming it identifies the shift cause. |
| Sreeram et al., 2026, Tempora [8] | Evaluate adaptation utility while accounting for time and compute. | Motivated reporting the complete route cost alongside accuracy. |

The entropy baseline in our implementation updates affine parameters above a frozen feature encoder. It is derived from the entropy-minimization idea; it is not a reproduction of native Tent on its original architecture or benchmarks. Similarly, our normalization action operates on a declared hidden-feature normalization step rather than a deep network's complete collection of BatchNorm layers.

The recent selection and normalization papers also constrain the contribution we can claim. Dynamic selection, using uncertainty to predict adaptation quality, and protecting adaptation against class imbalance already have substantial prior work. The current study therefore concentrates on a narrower question about the limitations of predicted-class concentration and the value of two additional inexpensive signals.

# 3. Summary of Gap Analysis

## Candidate research question

Can a small controller distinguish batches where normalization helps from batches where it harms, when genuine class concentration and corruption-induced prediction collapse produce similar predicted-class concentration?

Predicted-class concentration is the proportion of inputs assigned to the most common predicted class. A high value does not reveal the true class distribution. For example, a batch may genuinely contain mostly one digit, or it may contain many digits that the corrupted model incorrectly predicts as one digit. The controller sees model outputs and features, so both situations can look similar through a concentration-only rule.

Our completed experiments established a practical reason to study this decision: unconditional normalization helped some balanced conditions and substantially harmed many concentrated conditions. They did not establish that predicted concentration alone identifies the underlying reason. We are testing whether entropy and feature displacement add decision value once concentration is approximately matched.

## Scope of the proposed contribution

The contribution under investigation is a controlled empirical characterization and a deliberately small decision rule. It is not a claim that detecting shift, choosing an adaptation action, or handling class imbalance is new. The remaining literature check must establish whether the matched-concentration evaluation offers a meaningful distinction from the closest normalization and selection studies [4–7].

# 4. Proposed Idea

## From unconditional adaptation to a benefit gate

An unconditional policy estimates normalization statistics from every support batch and applies them to subsequent queries. Our working policy first runs the frozen source model on the support batch, computes three summary values, and predicts whether the update will reduce query error. It then either retains SOURCE or applies NORMALIZE.

| Component | Unconditional normalization | Current working approach |
| --- | --- | --- |
| Decision before updating | Update every batch | Predict the benefit of updating |
| Runtime evidence | Support features for statistics | Predicted concentration, entropy and feature displacement |
| Available actions | NORMALIZE | SOURCE or NORMALIZE |
| Parameter learning at deployment | No gradient steps required | No gradient steps required |
| Main failure concern | An unrepresentative batch can damage predictions | Evidence may still be ambiguous on unseen shifts |
| Cost accounting | Statistics estimation and query prediction | Source support pass, feature summaries, gate, update and query prediction |

## Three input features

1. Predicted-class concentration, c: the largest predicted-class count divided by support-batch size. This is a property of the model's predictions, not a measurement of the true class proportions.
2. Mean predictive entropy, h: the average uncertainty of the class-probability vectors. High entropy indicates diffuse probabilities, but low entropy does not guarantee that the predictions are correct.
3. Source-relative feature displacement, d: the average absolute difference between support-feature means and stored source means, divided by the corresponding source standard deviations. Both class proportions and corruption can affect this value.

For feature coordinate j, the displacement is d(B) = mean over j of |mu_B,j − mu_S,j| / sqrt(var_S,j + epsilon). Here B is the support batch; mu_B is its feature mean; mu_S and var_S are source-training moments; and epsilon is a fixed numerical guard. Source moments are computed without using calibration or final-test images.

## Gate target and action rule

For each auxiliary-development episode, we evaluate both actions from the same source state. The learning target is Delta = error_SOURCE − error_NORMALIZE on the disjoint query batch. A positive Delta means normalization helped. We fit a regression tree of maximum depth two to predict Delta from c, h and d. Such a tree has at most four leaves.

At deployment, NORMALIZE is selected when the predicted error reduction exceeds one globally calibrated threshold; otherwise SOURCE is selected. Calibration considers classification error and the complete route cost. The threshold may prefer SOURCE for all batches if the measured improvement does not justify adaptation. This decision rule is an empirical safeguard, not a guarantee of safety under arbitrary shifts.

# 5. Flow of the Proposed Work

## Development flow

We first train the source classifier and store its feature moments. We construct auxiliary episodes with controlled corruptions and class proportions, keeping the original image pools separate. Each episode contains support inputs and a disjoint query set. The source model produces the support features used by the gate. Query labels are used only in development to measure the difference between the two actions.

The next gate-development stage fits the depth-two regression tree on auxiliary-training episodes, chooses its threshold on calibration episodes, and freezes both before evaluation. Corruption-family identities, true class proportions and query labels are excluded from runtime gate inputs.

## Deployment flow

Unlabeled support batch → frozen source-model pass → concentration, entropy and feature displacement → predicted normalization benefit → SOURCE or NORMALIZE → prediction on a separate query batch.

If NORMALIZE is selected, support-derived means and variances are frozen while scoring the query batch. The source encoder and classification weights stay fixed. A new episode begins from the same source state, preventing one policy's update from affecting another policy's comparison. A full-network implementation may require an additional adapted forward pass; the method must be timed according to its actual execution path.

# 6. Dataset Used and Preprocessing

## Dataset details

We used the handwritten-digits dataset distributed with scikit-learn. It contains 1,797 grayscale images, ten classes representing digits 0–9, and 8 × 8 pixels per image. Each input therefore has 64 pixel features. Dataset documentation: https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html.

We divided the pixel values by 16, producing inputs in the range [0, 1]. We inspected dimensions, class counts, pixel ranges, source performance and the behavior of corrupted inputs. The feature-normalization moments were estimated only from the source-training partition. We did not fit a preprocessing transform using final-test images.

| Image partition | Images per source split | Purpose |
| --- | --- | --- |
| Source training | 900 | Fit the encoder, classification head and stored source moments |
| Auxiliary training | 400 | Fit action selectors; two disjoint 200-image pools for grouped cross-fitting |
| Calibration | 200 | Choose global policy thresholds and computation trade-offs |
| Final evaluation | 297 | Construct evaluation episodes from unseen original image identities |
| Total | 1,797 | One underlying dataset, repeated with three source/split seeds |

## Distribution-shift construction

Development conditions included clean inputs, pixel noise, brightness reduction, blur and translation. Contrast changes and occlusion were excluded from selector development and used as the primary held-out shift families. We used two severities for each corruption, support batches of 16 or 32 inputs, and query batches of 32 draws.

Class-composition conditions were balanced or approximately 75% dominated by one class. Support and query original image identities were disjoint within each episode. Some concentrated batches required repeated draws from the available image pool. Images were also reused across episodes within a partition, so episode counts do not represent independent datasets or independent trials.

## Episode accounting

Each source/split seed produced 288 auxiliary-training episodes, 144 calibration episodes and 208 final-evaluation episodes. Of the 208 evaluation episodes, 64 contained held-out contrast or occlusion conditions. Across seeds 241023, 241024 and 241025, this produced 1,920 episode definitions and 5,760 evaluations of SOURCE, NORMALIZE and entropy-affine adaptation. Additional selector and control analyses reused these recorded outcomes.

# 7. Detailed Work: Implementation

## Source classifier and environment

We implemented the baseline using Python, NumPy, SciPy and scikit-learn on CPU. The source encoder was a one-hidden-layer MLP with 32 ReLU units. It used L-BFGS, regularization alpha = 0.01 and a 250-iteration limit. We retained its learned encoder, standardized the hidden features using source-training moments, and fitted a multinomial logistic-regression head with C = 1 and a 500-iteration limit.

The recorded environment was Python 3.13.9, NumPy 2.2.6, SciPy 1.17.1 and scikit-learn 1.8.0. The retained analysis and follow-up commands used uv with the existing system environment. No cloud GPU or paid API was required for this study. All three encoder fits reached the fixed iteration limit; their convergence warnings remain in the run records.

## Adaptation actions implemented

SOURCE retained the source feature means and variances. NORMALIZE, recorded as BN in the code, replaced these moments with support-batch moments and froze them for the query batch. The entropy-affine baseline started from support normalization and performed three support-only steps on affine scale and offset, using learning rate 0.05 and a gradient-norm limit of 5. The encoder and classification-head weights remained fixed for all three actions. A numerical variance guard of 0.001 was used in the hidden-feature normalization.

We implemented cheap selectors using 82 source-output and feature-summary values, and richer selectors using 110 values. Richer evidence added two globally fixed subpixel-translated views and charged the additional source passes. Ridge action predictors used alpha = 10. These earlier selectors helped assess whether additional evidence was worth acquiring; the continuing three-feature gate removes that extra-view branch from the main method.

## Initial concentration gate

We implemented a simpler two-action rule that selected NORMALIZE when predicted-class concentration was at or below a calibrated threshold and SOURCE otherwise. The threshold grid was 0.15, 0.20, 0.25, 0.35, 0.50, 0.65 and 0.80. With no computation penalty, calibration selected 0.35 on the first split.

This rule was added after inspecting the initial action-by-class-composition results. Its threshold was calibrated without final-test labels, but the design itself was informed by the earlier evaluation. We therefore use it as an exploratory baseline and reserve a fresh evaluation for the revised three-feature gate.

## Implementation artifacts

| File or record | Implemented responsibility |
| --- | --- |
| train_core.py and source_model.npz | Source fitting and saved model state |
| core_model.py | Frozen prediction, support normalization, entropy-affine updates and support summaries |
| generate_outcomes.py and episodes.csv | Corruption episodes, identity separation and per-action measurements |
| analyze_diagnostic.py | Action selectors, acquisition policies and computation-aware comparisons |
| prior_gate_analysis.py | Calibration and evaluation of the concentration-only gate |
| outcomes.npz and run_manifest.json | Saved predictions, labels, costs, features, identities and artifact hashes |

# 8. Finished Work and Performance Evaluation

## Finished work

We completed an executable end-to-end CPU pipeline, source training on three splits, seven input conditions including clean data, two class-composition settings, three adaptation actions, cheap and richer selectors, a concentration-only gate, computation-aware policy comparisons, and result breakdowns by shift family and class composition. We also completed four additional leave-one-family-out selector analyses and retained the negative outcomes.

The pipeline checks covered separation of source, auxiliary, calibration and evaluation identities; support/query separation; immutable source parameters; finite normalized probabilities; and reconstruction of classification error from saved predictions. Analytic gradients for the entropy-affine action were checked against finite differences. These checks support the correctness of the small implementation; they do not establish generalization to larger image benchmarks.

## Metrics

Accuracy is the proportion of correctly classified query draws; higher is better. Negative log-likelihood (NLL) measures the probability assigned to the correct class and penalizes confident mistakes; lower is better. Harmful-episode frequency is the proportion of evaluation episodes whose classification error is strictly higher than SOURCE. It measures episode-level degradation, not the fraction of individual predictions harmed. Route cost includes the support evidence, gate and selected action where applicable; lower is better.

## Primary held-out results: first source/split seed

The following results average the 64 held-out contrast and occlusion episodes for seed 241023. Each query batch contains 32 draws. NLL and harmful-episode frequency were aggregated from the saved per-episode outcomes and selected actions.

| Implemented policy | Accuracy (%) | NLL | Harmful episodes (%) | Mean route cost (ms) |
| --- | --- | --- | --- | --- |
| Frozen SOURCE | 76.46 | 0.771 | 0.00 | 0.069 |
| Always NORMALIZE | 63.23 | 1.747 | 48.44 | 0.144 |
| Always entropy-affine | 63.62 | 1.742 | 48.44 | 0.485 |
| Initial concentration gate | 80.52 | 0.686 | 6.25 | 0.403 |

The concentration gate improved average accuracy by 4.05 percentage points over SOURCE and chose normalization on 32 of the 64 episodes. Its harmful-episode frequency was lower than unconditional normalization, although four episodes still had higher error than SOURCE. The average route cost was about 5.8 times that of direct SOURCE inference on this small CPU model. The result identifies an accuracy–cost trade-off rather than an efficiency improvement.

## Class-composition breakdown

On all 208 evaluation episodes of the first split, SOURCE accuracy was 78.13% for balanced conditions and 80.41% for concentrated conditions. Unconditional normalization increased balanced-condition accuracy to 82.51% but reduced concentrated-condition accuracy to 40.08%. This breakdown explains why unconditional normalization performed poorly despite helping some conditions.

Even the initial gate was imperfect: on the 64 held-out episodes, its balanced-condition accuracy was 85.06% versus SOURCE's 76.37%, while concentrated-condition accuracy was 75.98% versus SOURCE's 76.56%. That small decline is part of the motivation for a more informative gate and a direct test of ambiguous concentration values.

## Repeat results for the earlier evidence selectors

| Source/split seed | SOURCE accuracy (%) | Cheap selector (%) | Always-rich selector (%) | Rich minus cheap (pp) |
| --- | --- | --- | --- | --- |
| 241023 | 76.46 | 77.34 | 78.66 | +1.32 |
| 241024 | 73.68 | 73.97 | 74.27 | +0.29 |
| 241025 | 74.02 | 74.95 | 78.37 | +3.42 |

The repeats changed source training and original-image partitions while retaining the same underlying dataset. They show variable gains from richer evidence. They do not provide three-seed confirmation of the concentration gate or the proposed three-feature tree. At every positive computation penalty tested, calibration selected zero additional-evidence acquisition in all three runs.

# 9. Results and Discussion

The strongest completed observation is that the usefulness of a normalization update depends on more than the corruption family. Class composition changed the action's behavior substantially. The initial gate retained many of the balanced-condition benefits while avoiding much of the degradation from always updating concentrated batches. However, it still harmed some episodes and was slower than direct inference.

The richer-evidence experiments also produced a useful negative result. Additional views sometimes improved action selection, but the improvement varied across source/split seeds and did not justify the measured cost under the tested positive penalties. Four additional family holdouts gave inconsistent gains. We consequently narrowed the main method to a small gate using information already available from a source support pass.

The current evidence does not establish a high-performing general adaptation method. It supports a concrete next experiment: test whether entropy and source-relative feature displacement improve decisions over concentration alone, particularly when different underlying conditions yield similar concentration. That experiment must keep threshold selection, matching rules and final evaluation separate.

Local timing needs careful interpretation. The source model is tiny, and Python and estimator-wrapper overhead are significant relative to a forward pass. A NumPy implementation of the previously fitted linear selectors reduced selector overhead while preserving their decisions, but complete selection routes still exceeded direct inference cost. Those measurements justify implementation work; they do not predict the cost ratio of a modern vision backbone.

# 10. Scope of the Work

The completed study covers episodic classification with a frozen encoder and head, a declared hidden-feature normalization layer, unlabeled support inputs, separate query inputs, controlled corruption families, and class-composition changes. It establishes an implemented research pipeline and an initial decision-making result on a small dataset.

Important limits remain. The same 1,797-image dataset supports all three repeats. Many episode definitions share original images, and some concentrated query batches include repeated draws. The concentration gate was developed after inspecting an action breakdown. The encoder fits reached their iteration limit. The implementation uses a shallow feature-space surrogate rather than full-network adaptation.

CIFAR-10-C, ImageNet-C, DomainNet and WILDS have not been run in this project. Native Tent, NOTE and channel-selective normalization comparisons remain outstanding. Continual streams, mixed corruption compositions, physical deployment deadlines, energy and memory consumption also remain outside the completed evaluation. We have not claimed benchmark superiority or established novelty.

# 11. Continuing Work and Further Testing

## Three-feature gate

We are continuing the approach by replacing the initial single-threshold rule with a depth-two regression tree over concentration, entropy and feature displacement. The immediate objective is to reduce harmful updates while retaining or improving the measured accuracy gain. The computation objective is to reduce unnecessary support recomputation and gate overhead, without omitting the source pass or adapted execution from the reported cost.

## Fresh evaluation protocol

Before the next execution, we will freeze the feature definitions, tree depth, threshold rule, cost objective and evaluation partitions. We will hold out complete corruption families and dominant-class identities from gate development while retaining every class in source-model training. Original image identities will remain separated between development, calibration and evaluation.

The central analysis will compare genuinely class-concentrated batches with balanced corrupted batches that have similar observed predicted-class concentration. Matching bins or tolerances will be chosen on development data without using the measured action benefits. We will report matching coverage and retain unmatched conditions in the full evaluation so that a favorable subset does not replace the complete result.

## Baselines and ablations

The comparison will include SOURCE, always NORMALIZE, the initial concentration-only gate, entropy-only and displacement-only gates, the three-feature tree, and an auxiliary-development fixed policy. An oracle that retrospectively selects the best action using evaluation labels will serve only as a diagnostic upper bound. Its accuracy will not be reported as a deployable result.

We will measure accuracy, NLL, harmful-episode frequency, action regret relative to the same action menu, and complete route cost. We will separate improvements averaged across all conditions from changes on concentrated batches and unseen shift families. After the small implementation passes a fresh evaluation, we will prioritize CIFAR-10-C with a declared normalization-equipped backbone and faithful reference baselines before attempting larger benchmarks.

# 12. Conclusion and Future Work

We implemented and evaluated the baseline components needed to study selective test-time normalization. The completed work shows that normalization can help balanced inputs while damaging concentrated inputs, and that a simple gate can improve the average accuracy of the frozen source model in the initial held-out conditions. The same experiment also exposed unresolved latency and reliability issues.

The immediate deliverable is a fixed three-feature gate and a fresh evaluation that directly tests the ambiguity of predicted-class concentration. The next deliverable is a stronger image-benchmark comparison with faithful normalization baselines. We will continue to revise the approach based on measured gains and failures rather than assume that a more complex gate will perform better.

| Next milestone | Concrete completion criterion |
| --- | --- |
| Complete the three-feature controller | Fixed feature definitions, fitted depth-two tree and calibration-only threshold |
| Run fresh confirmation | Evaluation identities and shift/class holdouts fixed before inspecting results |
| Analyze reliability and cost | Per-condition accuracy, harm frequency, regret and complete route timings |
| Scale the evaluation | CIFAR-10-C with faithful normalization baselines and a recorded compute budget |
| Consolidate the research claim | Closest-prior-work comparison, reproducible implementation and measured limitations |

# 13. References

[1] Yanghao Li, Naiyan Wang, Jianping Shi, Jiaying Liu, and Xiaodi Hou. Revisiting Batch Normalization For Practical Domain Adaptation. arXiv:1603.04779, 2016. https://arxiv.org/abs/1603.04779

[2] Dequan Wang, Evan Shelhamer, Shaoteng Liu, Bruno Olshausen, and Trevor Darrell. Tent: Fully Test-Time Adaptation by Entropy Minimization. ICLR, 2021. https://arxiv.org/abs/2006.10726

[3] Taesik Gong, Jongheon Jeong, Taewon Kim, Yewon Kim, Jinwoo Shin, and Sung-Ju Lee. NOTE: Robust Continual Test-time Adaptation Against Temporal Correlation. NeurIPS 35, 2022. https://papers.nips.cc/paper_files/paper/2022/hash/ae6c7dbd9429b3a75c41b5fb47e57c9e-Abstract-Conference.html

[4] Hyesu Lim, Byeonggeun Kim, Jaegul Choo, and Sungha Choi. TTN: A Domain-Shift Aware Batch Normalization in Test-Time Adaptation. ICLR, 2023. https://arxiv.org/abs/2302.05155

[5] Pedro Vianna, Muawiz Sajjad Chaudhary, Paria Mehrbod, An Tang, Guy Cloutier, Guy Wolf, Michael Eickenberg, and Eugene Belilovsky. Channel-Selective Normalization for Label-Shift Robust Test-Time Adaptation. Proceedings of the 3rd Conference on Lifelong Learning Agents, PMLR 274:514–533, 2025. https://proceedings.mlr.press/v274/vianna25a.html

[6] Michal Danilowski, Alexander Murphy, Young D. Kwon, and Abhirup Ghosh. MORPHEUS: Meta Test-Time Adaptation via Neural Collapse Geometry. ICLR Test-Time Updates Workshop, 2026. https://openreview.net/forum?id=YfyApJH1Rj

[7] Kartik Jhawar and Lipo Wang. When is Test-Time Adaptation Identifiable From Unlabeled Evidence? arXiv:2609.11235, 2026. https://arxiv.org/abs/2609.11235

[8] Sudarshan Sreeram, Young D. Kwon, and Cecilia Mascolo. Tempora: Characterising the Time-Contingent Utility of Online Test-Time Adaptation. ICML, PMLR 306:115420–115456, 2026. https://proceedings.mlr.press/v306/sreeram26a.html

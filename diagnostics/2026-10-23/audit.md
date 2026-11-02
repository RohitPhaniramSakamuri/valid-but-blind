# Independent audit of the bounded diagnostic

Date: 23 October 2026. Audit started while implementation was being written. The user explicitly authorized running the diagnostic in a 15-minute window. This audit does not establish paper reproduction, novelty or benchmark generalization.

## Declared scope

The available system has NumPy/scikit-learn and no installed PyTorch. The execution team chose a local, alternate-data mechanism study on the bundled 8×8 digit dataset. A source-trained MLP representation, normalized hidden features and a linear classifier support SOURCE, support-statistics normalization and an entropy-driven affine update. That last action is a declared surrogate, not native Tent.

## Protocol checks requested before outcomes

- Source fitting, meta-training, calibration and final evaluation identities remain disjoint.
- The meta-training set is divided into disjoint identity groups; using arbitrary episode IDs would not prevent leakage when underlying images repeat.
- Each support/query pair is disjoint in original image identity.
- Cheap/rich selector features use support observations only, excluding evaluator-only family/severity labels and query outcomes.
- Source state remains immutable across candidate actions and episodes.
- Support-estimated normalization is frozen on query data in the declared entropy action.
- Additional-view evidence and all routing/update costs must be charged, and a SOURCE prediction still carries its base inference cost.
- Reused images, resampled episodes and duplicated draws are dependent; a large row count is not a large independent dataset count.

## Executed mathematical and state checks

Command: `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python audit_checks.py`, from this diagnostic directory (or using its full relative path from the workspace).

- Central finite differences checked all 14 gamma/beta coordinates on an independently generated 17×7 feature example. With epsilon 1e-5, maximum absolute discrepancies were 9.89e-12 for gamma and 2.17e-11 for beta.
- The four original data partitions have sizes 900/400/200/297, cover all 1,797 images, and have zero pairwise identity intersections.
- SOURCE, BN and ENTROPY left every saved source-model array byte-identical during the checked calls.
- All three actions returned finite probabilities summing to one. Evaluating the first query point alone or inside a 32-point query batch changed its prediction probabilities by at most 2.22e-16, consistent with frozen support/source statistics and pointwise query inference.
- The checked entropy intervention lowered support entropy from 0.23553 to 0.22995. That demonstrates agreement with its optimization objective, not improved classification correctness.
- The source MLP fit reached its fixed 250-iteration cap and emitted a convergence warning. It is recorded in `source_manifest.json`; this run must not be described as warning-free.

## Saved-outcome integrity checks

The generator produced 640 episodes: 288 training, 144 calibration and 208 final-pool episodes. The primary previously unseen-family subset contains 64 contrast/occlusion episodes.

- Every episode's support/query identity sets were disjoint.
- Every support/query ID was contained in its declared meta image pool. All six pairs among the two training pools, calibration pool and final pool had zero overlap.
- Contrast and occlusion were absent from training and calibration families.
- Query labels matched the original bundled dataset. Stored error vectors reconstructed exactly from the saved predictions and labels.
- All cheap/rich features were finite; the first 82 rich features exactly equaled the cheap vector. Code inspection confirms family, severity, class labels, original IDs and query outcomes are evaluator fields, not feature inputs.
- Recorded action/evidence durations were finite and positive.

The raw outputs retain support/query IDs and predictions, enabling these checks. Numerical results are in `audit_results.json`.

## Analysis code audit

Inspection of `analyze_diagnostic.py` found that selectors fit training episodes only, their out-of-fold targets use the two disjoint original-ID groups, and gate thresholds/cost scaling use the separate calibration pool. Final labels enter hindsight/oracle diagnostics and result calculation, not fitted runtime models. Ridge regularization and the cost/rate grids are fixed in the analysis configuration.

A cost-accounting correction was requested: an ambiguity trigger must run the cheap selector to compute its action margin even when it later acquires rich evidence, so the acquired ambiguity path needs both selector costs. The lead applied the additional `model_cost0 * acquire` charge; this correction was inspected in the revised script. The learned-value gate uses cheap features directly and need not run the cheap selector on an acquired route under the declared implementation.

## Limits of the evidence

- Half of the 640 episodes contain repeated query draws; the smallest query set has only 15 distinct original images among 32 draws. Across episodes, images are reused. All final-pool episodes together draw from only 297 original images.
- Episode bootstrap intervals are conditional descriptive resampling intervals for this finite pool and construction. They do not establish independent-image population uncertainty or cross-dataset significance.
- The per-episode oracle uses finite observed query outcomes, so its headroom is optimistic and may include sampling variation. It is not a deployable selector.
- Curve points have different measured total costs. Merely assigning equal acquisition fractions is not strict cost matching; any superiority claim needs a budget-frontier comparison.
- Timing includes Python/scikit-learn pipeline overhead, which is large relative to this very small classifier. A measured runtime loss here does not prove that evidence acquisition is intrinsically inefficient on larger models or devices.
- The scalar entropy surrogate, finite-difference check and alternate digit corruptions do not reproduce Tent, CIFAR-C, ImageNet-C, DomainNet, WILDS or a continual-state benchmark.
- A richer selector's observed accuracy improvement alone does not validate selective purchase. The first analysis selects zero acquisition on calibration across all four declared cost weights; that negative finding should remain visible.

## Additional checks of finite-query optimism and dependence

Executed `audit_headroom.py` using `uv run --no-project --no-sync python ...` in the existing environment, with no dependency installation. The CLI warned that `--no-sync` has no effect with `--no-project`; the script completed. Existing policy choices were frozen, and no selector or acquisition model was refit.

First, split each episode's query **identities** into two halves, keeping all repeated occurrences of an identity together. Select the best action using labeled outcomes in one half and score it on the other, reverse the halves, and combine the held-out errors. Repeat that split randomization 300 times. This is a retrospective label-assisted diagnostic, not an executable unlabeled policy. It reduces the optimism of selecting/scoring on the same finite query set but does not recover unlimited-data action risks.

Second, cluster-resample original query identities 4,000 times while preserving every occurrence of an identity across episodes. Compute cheap-minus-rich error reduction with the already frozen choices. These are conditional sensitivity intervals: source fitting, shared support sets and shift constructions remain fixed, so this does not remove every dependence or justify population-level significance.

| Source/split seed | Full-query oracle headroom over SOURCE | Cross-query-identity transfer headroom | Cheap-to-rich error reduction | Query-ID cluster interval |
| --- | --- | --- | --- | --- |
| 241023 | 6.445 pp | 5.401 pp | 1.318 pp | 0.855–1.816 pp |
| 241024 | 7.080 pp | 5.589 pp | 0.293 pp | 0.000–0.639 pp |
| 241025 | 8.301 pp | 7.232 pp | 3.418 pp | 2.472–4.454 pp |

Every source/split repeat also passed the gradient/state/partition/outcome integrity checks. These repeats use the same bundled dataset, not independent datasets. Their variation is a reason to avoid presenting the first seed as a representative universal gain. Raw independent-check outputs are `audit_results.json`, `audit_headroom.json` and `audit_query_identity_gains.csv` in the base and repeat directories.

## Audit conclusion

No remaining blocking numerical, partition, runtime-label-access or support/query-state defect was found in the inspected bounded diagnostic after the ambiguity-route cost correction. The scientific limitations above remain material. The pilot can support a statement of conditional action/evidence headroom and a negative or uncertain purchase-policy result; it cannot establish a successful general TTA controller or original benchmark reproduction.

The subsequently added `prior_gate_analysis.py` was also inspected: its conditional SOURCE/BN concentration gate charges the cheap observation even when it returns SOURCE; only a calibration-selected constant SOURCE policy omits that observation. Threshold selection uses calibration outcomes. Because the gate design followed inspection of final action-by-prior behavior, its evaluation remains explicitly post-hoc exploratory; calibration-only threshold selection does not make that reused final evaluation confirmatory.

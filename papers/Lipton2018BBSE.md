# Detecting and Correcting for Label Shift with Black Box Predictors

Citation key: `Lipton2018BBSE`.
Authors: Zachary Lipton; Yu-Xiang Wang; Alexander Smola.
Publication: 2018; Proceedings of the 35th International Conference on Machine Learning, PMLR 80:3122-3130.
Status: selectively inspected; not a replication.

## Literature refresh — 26 October 2026

Primary source: [Detecting and Correcting for Label Shift with Black Box Predictors](https://proceedings.mlr.press/v80/lipton18a.html).

Reading scope: Official metadata/abstract and visible official PDF introduction on estimator assumptions; partial reading.

Inspected locations: Abstract; Introduction and confusion-matrix condition.

Relevance (our reading): Estimates target class priors from unlabeled predictions and labeled source confusion statistics; detects and corrects pure label shift.

Boundary / reviewer qualification: Requires invariant class-conditionals and invertible confusion matrix; simultaneous nuisance shifts can invalidate its source confusion statistics.

Publication qualification: ICML 2018 proceedings verified

No code or benchmark was run for this refresh. [Current synthesis](../outputs/shift-aware-tta-deep-review-2026-10-26.md). Detailed reading histories and original metadata remain in [catalog](../sources/catalog.json).

# 008: Frozen confirmation of shifted-level alarms, with many architectures (frozen 3 Nov 2026, before any exp008 stream ran)

Status: PLANNED at freeze. Outcomes are appended after the run.

**Why.** exp006 returned NOT CONFIRMED under mis-specified criteria (absolute gaps, unequal false-alarm rates). exp007 found that the twin ranks failures best, and that the twin plus a 3-model agreement-pattern estimator ranked better on both earlier sets. The alarm level transferred unevenly from dev to held shifts. This run tests that on fresh data, with relative criteria at matched false alarms. It also adds broader dev shifts and a range of alarm architectures.

## Data and streams

None of these medical datasets or seeds has been used before.

| | Medical | CIFAR-100-C |
|---|---|---|
| Data | OCTMNIST-224 (4 classes), OrganCMNIST-224 (11 classes, CT), PneumoniaMNIST-224 (2 classes, X-ray); dev images capped at 4,000 | Six RobustBench checkpoints, new seeds (tag exp008) |
| Dev shifts | Gaussian noise, speckle, brightness, gamma, shot noise, posterize, salt-and-pepper, darken | Hendrycks' 4 extra corruptions, plus gamma, posterize, salt-and-pepper, darken applied to clean dev images |
| Held shifts | Blur, JPEG, contrast, pixelate × 3 severities | The 15 standard corruptions × severities 1, 3, 5 |

**Priors:**
- Dev: natural, Dirichlet 1, Dirichlet 0.3 and Dirichlet 0.1.
- Held: natural, Dirichlet 1 and Dirichlet 0.1.

**Streams:** 120 batches of 48.

**Arms:**
- Tent 1e-3 is primary everywhere.
- Tent 5e-3 runs on the medical sets as secondary.

**Definitions** (as in exp004–006):
- **Strict:** mean error ≥ r0 + 0.15 and last-quarter error < 0.85.
- **Safe:** mean error < r0 + 0.10 and last-quarter error < 0.85.

## Detectors

There are 13 signals, each paired with 3 calibrations, plus 2 confidence-sequence monitors. Every level comes from that (dataset, checkpoint, arm)'s dev streams only. Anything fitted is fitted out-of-fold by dev corruption.

**Signals:**
- **Single-model signals:** twin, released proxy, prototype, ATC, DoC, dropout disagreement.
- **Pattern:** a non-negative error estimate from the 3-model agreement × twin-uncertainty cells.
- **Monotone LightGBM:** predicts running excess error.
- **Isolation forests at three levels:**
  - stream (running signal vector);
  - batch (per-batch vector, running mean of anomaly scores);
  - image (per-image signals; running share of images above the 95th percentile of dev-safe images).
- **Rank and martingale signals:**
  - dominance (mean ECDF rank of batch twin-flag rates against dev-safe batches);
  - a conformal test martingale on batch twin-flag p-values.
- **Combinations:**
  - **twin+pattern** (primary): standardised average;
  - **fusion:** twin, ATC and dropout.

**Calibrations:**
- **G:** global split-conformal level, α = 0.05.
- **M:** Mondrian. Two bins by the early class-skew descriptor, the total-variation distance between the twin's predicted-class histogram over the first 11 batches and that on clean natural dev streams. G is used when a bin has fewer than 19 safe dev streams.
- **Z:** the per-checkpoint score standardised by dev-safe median and 10–90 spread, then a conformal level on the maximum.

**Confidence-sequence monitors:**
- the published monitor;
- the exp004 twin bound.

## Frozen verdict (Tent 1e-3, held, pooled over 4 datasets)

**Primary detector:** twin+pattern with calibration G.

| | Condition |
|---|---|
| C1 (ranking) | At a matched 5% false-alarm rate (per-group thresholds set on held safe streams with hindsight), twin+pattern misses at least 40% fewer clear failures than the released proxy (relative) |
| C2 (deployed safety) | Realised false alarms ≤ 10% pooled and ≤ 15% in every dataset |
| C3 (deployed power) | Missed ≤ 20% pooled, and at least 40% fewer misses than the published monitor (relative) |

- **CONFIRMED:** C1, C2 and C3 all hold.
- **PARTIAL:** C1 and C3 hold, but C2 fails in at most one dataset with pooled false alarms ≤ 15%.
- **INCONCLUSIVE:** fewer than 80 strict or 120 safe pooled streams.
- **NOT CONFIRMED:** any other outcome.

**Secondary (reported, not part of the verdict):** twin+pattern counts as non-inferior to ATC if its matched-5% misses are no more than 1.25 times ATC's.

**Descriptive:** every detector × calibration, deployed and matched at 3%, 5% and 7%, per dataset and per arm.

## Compute

- **Instance:** one SageMaker job, ml.g6e.12xlarge (4×L40S), in us-east-1. A duplicate is queued in us-west-2, and a cross-region S3 claim makes the second one exit.
- **Hard limit:** 20 h.
- **Results:** the job runs the analysis itself and copies its reports to `s3://vbb-exp008-286879406788-use1/results/<job>/`.
- **Resources:** logged in `AWS_RESOURCES.md`.

## Partial outcome (3 Nov 2026, 22:00 IST): CIFAR-100-C only, so no verdict

**Status.** The medical half did not run. A `fetch()` loop variable overwrote the class count, so all medical tasks crashed. The job then hung on a bare `wait` until it was stopped (about $45 billed). Both bugs are fixed in code. The frozen verdict pools four datasets, so these CIFAR-only numbers are descriptive.

**Data.** 2,046 streams: six checkpoints, 194 strict and 506 safe held-out streams on Tent 1e-3. Analysed locally with the frozen `analyze8.py`; the log is in `results/analysis_local.log`.

**Criteria computed on CIFAR alone.** All three are met, but they are not the frozen verdict.

| | Condition | Result |
|---|---|---|
| C1 | Matched-5% misses: twin+pattern vs released proxy | 8.8% vs 33.0% (−73%) |
| C2 | Deployed false alarms | 3.2% |
| C3 | Deployed misses vs published monitor | 14.9% vs 44.8% (−67%), with lower false alarms (3.2% vs 4.3%) |
| Secondary | Non-inferior to ATC (matched 5%) | Yes: 8.8% vs 12.4% |

**Matched 5% false-alarm misses, by detector.**

| Detector | Missed |
|---|---|
| Monotone LightGBM | **3.6%** |
| Fusion | 4.1% |
| DoC | 6.7% |
| Dropout disagreement | 7.2% |
| Pattern | 7.7% |
| Twin+pattern | 8.8% |
| Martingale | 9.8% |
| Twin | 10.3% |
| Dominance | 11.3% |
| ATC | 12.4% |
| Isolation forest, batch | 17.5% |
| Isolation forest, stream | 18.6% |
| Prototype | 30.4% |
| Isolation forest, image | 33.0% |
| Released proxy | 33.0% |

**Deployed results worth noting.**

| Detector | Missed | False alarms |
|---|---|---|
| Monotone LightGBM with calibration Z | 17/194 (8.8%) | 12/506 (2.4%) |
| DoC with calibration G | 9/194 | 27/506 (5.3%) |
| Twin+pattern with calibration G | 29/194 | 16/506 |
| Published monitor | 87/194 | 22/506 |

**Reading (exploratory).**
- Isolation forests at every level did not help.
- Mondrian calibration gave no consistent gain.
- Z calibration helped some signals.
- Monotone constraints made the learned detector the best ranker on CIFAR, unlike the unconstrained learned detectors of exp005. This needs the medical data before it means anything.

## Outcome (4 Nov 2026, 01:38 IST): NOT CONFIRMED

**Data.** 3,948 streams in total:
- CIFAR-100-C: 2,046 streams from job d;
- OrganCMNIST and PneumoniaMNIST: 1,268 streams from job `vbb-exp008m-1103-1640`, 10,662 billable s on ml.g6e.8xlarge;
- OCTMNIST: 634 streams from job `vbb-exp008p-1103-1730`, 5,914 billable s on ml.g6e.2xlarge.

On Tent 1e-3, the held-out pool has 351 strict-failure and 637 safe streams, well above the inconclusive floor (80 and 120).

| Dataset | Strict | Safe |
|---|---|---|
| CIFAR-100-C | 194 | 506 |
| OCT | 66 | 42 |
| OrganC | 53 | 49 |
| Pneumonia | 38 | 40 |

The analysis is the frozen `analyze8.py`. Its outputs are in `diagnostics/2026-11-03-exp008-confirm/`:
- `merged/analysis_merged.log`;
- `merged/report8.json`;
- `merged/rows8.json`.

The jobs' own logs are in `job_reports/`, and the raw medical streams in `results_med/`.

**Frozen criteria (primary: twin+pattern with calibration G).**

| | Condition | Result | Met |
|---|---|---|---|
| C1 | Matched-5% misses vs released proxy, at least 40% fewer | 11.1% vs 25.9% (−57%) | yes |
| C2 | Deployed false alarms ≤ 10% pooled and ≤ 15% per dataset | 2.5% pooled (16/637); 3.2% CIFAR, 0% on each medical set | yes |
| C3 | Deployed misses ≤ 20% pooled, and at least 40% fewer than the published monitor | 31.9% (112/351) vs 59.5% (209/351) (−46%) | **no**: the relative part holds, the 20% ceiling does not |
| Secondary | Non-inferior to ATC at matched 5% (≤ 1.25 × ATC) | 11.1% vs 14.5% | yes |

Verdict by the frozen rule: **NOT CONFIRMED**. PARTIAL needs C3, and C3 failed.

**Why C3 failed.** The cause is the same one exp007 found: the dev-calibrated level transfers unevenly. On every medical set, twin+pattern|G raised zero false alarms, so its level sat too high there.

| Dataset | Twin+pattern\|G missed | Published monitor missed |
|---|---|---|
| CIFAR | 29/194 (15%) | 87/194 |
| OCT | 23/66 (35%) | 64/66 |
| OrganC | 22/53 (42%) | 20/53 |
| Pneumonia | **38/38 (100%)** | 38/38 |

On Pneumonia, the only binary task, twin+pattern never alarmed. On OrganC it missed slightly more than the published monitor. Ranking (C1) held; the alarm level did not.

**Matched 5% false-alarm misses, pooled (descriptive).**

| Detector | Missed |
|---|---|
| Monotone LightGBM | **6.3%** |
| DoC | 8.5% |
| Fusion | 10.3% |
| Twin+pattern | 11.1% |
| Dropout disagreement | 12.5% |
| ATC | 14.5% |
| Dominance | 14.8% |
| Pattern | 16.0% |
| Twin | 17.1% |
| Isolation forest, batch | 17.4% |
| Isolation forest, stream | 17.9% |
| Martingale | 17.9% |
| Released proxy | 25.9% |
| Prototype | 26.2% |
| Isolation forest, image | 27.9% |

**Deployed, by dataset (exploratory, not the frozen primary).**

| Detector | CIFAR missed / FA | OCT | OrganC | Pneumonia | Pooled missed | Pooled FA |
|---|---|---|---|---|---|---|
| Monotone LightGBM\|Z | 17/194, 12/506 | 10/66, 0/42 | 13/53, 0/49 | 11/38, 0/40 | 51/351 (14.5%) | 12/637 (1.9%) |
| DoC\|Z | 10/194, 41/506 | 6/66, 3/42 | 0/53, 2/49 | 7/38, 2/40 | 23/351 (6.6%) | 48/637 (7.5%) |
| Fusion\|G | 13/194, 27/506 | 7/66, 4/42 | 1/53, 0/49 | 15/38, 3/40 | 36/351 (10.3%) | 34/637 (5.3%) |
| ATC\|Z | 28/194, 27/506 | 8/66, 3/42 | 0/53, 3/49 | 11/38, 2/40 | 47/351 (13.4%) | 35/637 (5.5%) |
| Published monitor | 87/194, 22/506 | 64/66, 0/42 | 20/53, 0/49 | 38/38, 0/40 | 209/351 (59.5%) | 22/637 (3.5%) |

**Reading.**
- *Frozen result.* Twin+pattern ranks failures well (C1), but its dev-calibrated level does not carry over to the medical tasks. The confirmation failed on deployed power, not on ranking or safety.
- *Exploratory.* Monotone LightGBM with calibration Z would have met all three thresholds if it had been the primary: 14.5% missed, 1.9% false alarms, −76% misses relative to the published monitor. But it was picked after the CIFAR partial results were seen. It is a hypothesis for a new frozen test, not a confirmed result.
- *Exploratory.* DoC, fusion and ATC with Z calibration catch more failures than twin+pattern but raise more false alarms. DoC|Z misses only 6.6%, but at 7.5% false alarms.
- *Negative results, kept.* Isolation forests at every level, Mondrian calibration and the conformal martingale gave no consistent gain.

**Cost and teardown.** The medical rerun cost about $17 on job m plus a few dollars on job p. All exp008 AWS resources were deleted on 4 Nov; see `AWS_RESOURCES.md`.

# 010: Frozen confirmation of the family-validated alarm, and a test of the coupling claim on other objectives (frozen 14 Nov 2026, before any exp010 stream ran)

Status: PLANNED at freeze. Outcomes are appended after the run.

**Why.** [exp009](009-level-transfer-diagnosis.md) located the uneven transfer of the alarm level and chose a fix on streams that had already been scored. This run tests that fix once, on datasets, checkpoints and draws this project has not used, with relative criteria at matched false-alarm rates. It also tests whether the monitor blind spot is specific to Tent's entropy loss or appears for other objectives that reward confident predictions.

## Data and streams

| | Medical | CIFAR-10-C |
|---|---|---|
| Data (new to this project) | TissueMNIST-224 (8 classes, microscopy), OrganSMNIST-224 (11 classes, CT); val and test images each capped at 4,000 by a fixed seed | RobustBench CIFAR-10 common-corruption checkpoints: AugMix WRN-40-2, AugMix ResNeXt-29, PRIME ResNet-18, Addepalli2021Towards WRN-34 |
| Source model | ImageNet ResNet-18 fine-tuned as in exp008 (`prepare10.py`) | published checkpoints |
| Dev shifts | Gaussian noise, speckle, brightness, gamma, shot noise, posterize, salt-and-pepper, darken | Hendrycks' 4 extra corruptions, plus gamma, posterize, salt-and-pepper, darken on clean dev images |
| Held shifts | blur, JPEG, contrast, pixelate × 3 severities | the 15 standard corruptions × severities 1, 3, 5 |
| Images | dev = validation split; held = test split; calibration = 1,000 training images | test set split by seed 20261114: 1,000 calibration, 4,000 dev, 5,000 held |

- Priors: dev natural, Dirichlet 1, 0.3, 0.1; held natural, Dirichlet 1, 0.1. Streams: 120 batches of 48. Seeds tagged `exp010`.
- Definitions as in exp004–008. Strict: mean error ≥ r0 + 0.15 and last-quarter error < 0.85. Safe: mean error < r0 + 0.10 and last-quarter error < 0.85.
- Labels build streams and score outcomes only.

**Arms** (all update BN affine parameters with Adam, learning rate 1e-3, test-batch statistics):
- `tent0.001`: entropy. Primary, on every dataset and checkpoint.
- `pl0.001`: hard pseudo-label cross-entropy.
- `im0.001`: information maximisation (mean entropy minus entropy of the mean prediction).
- `pl` and `im` run on both medical sets and on the two light CIFAR-10 checkpoints (AugMix WRN-40-2, PRIME ResNet-18).
- The entropy-free twin (BN statistics only) and the frozen source are recorded on every stream.

## Primary detector: family-validated alarm (FV)

Fixed in `diagnostics/2026-11-14-exp010-confirm/job/analyze10.py` (sha256 recorded below). For each (dataset, checkpoint, arm), from its dev streams only:

1. Candidates, in tie-break order:
   - **twin|G**: running share of images where the twin is uncertain or disagrees with the adapted model, minus the twin's clean error; one constant level.
   - **doc|Z**: clean source confidence minus the adapted model's running confidence, standardised at each read-out time by the safe dev streams at that time (median, 10–90 spread); level on the maximum.
   - **fus3|G**: the exp008 fusion detector, unchanged (mean of time-standardised twin, ATC and dropout scores).
2. Levels use the split-conformal rank at α = 0.05 on safe dev streams; read-outs every 5 batches from batch 11. The time standardisation and the choice in step 3 use the same dev streams, so **no coverage guarantee is claimed**. Realised false alarms are tested instead (C2, C4).
3. Leave-one-dev-family-out: for each dev family, set levels on the other families and score the left-out family. Deploy the candidate with the smallest (LOFO missed share + LOFO false-alarm share), level reset on all safe dev streams.
4. Audit: a deployment is flagged *weak* when the chosen candidate's LOFO missed share exceeds 0.25 (with at least 10 LOFO failing streams). Flagged deployments stay in every criterion; the flag is only reported.
5. Abstention: a setting with fewer than 19 safe dev streams cannot be calibrated. Every dev-calibrated detector then never alarms on it, and its held streams stay in every count (its failures are misses).

## Frozen verdict (Tent 1e-3, held streams, pooled over TissueMNIST, OrganSMNIST and CIFAR-10-C)

| | Condition |
|---|---|
| C1 (ranking) | At a matched 5% false-alarm rate (per-setting thresholds set on held safe streams with hindsight), FV misses at least 40% fewer clear failures than the released proxy with a dev-set level (relative) |
| C2 (deployed safety) | Realised false alarms ≤ 10% pooled, and ≤ 15% in every dataset with at least 20 safe streams |
| C3 (deployed power) | As exp008's C3, which the earlier rule failed: FV misses ≤ 20% pooled and at least 40% fewer clear failures than the published monitor (relative). In addition, no more misses than the published monitor in any dataset with at least 15 strict streams |
| C4 (level transfer) | FV misses at least 30% fewer than the earlier rule, twin with a constant level (relative, pooled), or at most 5% outright; in every dataset with at least 15 strict streams it misses no more than that rule plus 2 streams; and FV's realised pooled false-alarm rate is at most 7.5% (1.5 times the target), so that fewer misses are not bought with more false alarms |

- **CONFIRMED:** C1–C4 all hold.
- **PARTIAL:** C1, C2 and C3 hold but C4 fails.
- **INCONCLUSIVE:** fewer than 80 strict or 120 safe pooled streams.
- **INCOMPLETE (no verdict):** any planned stream of any setting is missing (200 dev and 141 held per CIFAR-10 setting; 200 and 117 per medical setting).
- **NOT CONFIRMED:** any other outcome.

Why these thresholds:
- Improvement criteria are relative. The only absolute numbers are exp008's own ceilings (20% missed, 10% and 15% false alarms), kept so that the new rule faces the test the earlier rule failed, and the 7.5% false-alarm band.
- The 5% escape in C4 exists because a relative gain is unattainable when the earlier rule already misses almost nothing (it missed 2/86 in exp005).
- C1's hindsight thresholds are set per setting; settings with fewer than 10 held safe streams are left out for both detectors, and achieved false-alarm rates are reported.
- Attainability check, not evidence: `analyze10.py` run on the already-seen exp006 and exp008 streams gives FV 16/307 missed with 36/578 false alarms (earlier rule 40/307, published 149/307) and 22/351 with 31/637 (earlier rule 76/351, published 209/351). The design was chosen on those streams, so all four criteria hold there by construction.

**Secondary (reported, not in the verdict):** FV restricted to twin|G and doc|Z; each candidate alone; monotone LightGBM with calibration Z (the exp008 exploratory lead); matched misses at 3%, 5%, 7%; results split by the audit flag; FV on the `pl` and `im` arms.

## Frozen coupling test (per objective arm)

The paper's claim is that the blind spot comes from adaptation optimising the quantity the monitor reads. If so it should appear for other confidence-rewarding objectives and not for the BN-only twin.

- Monitor: the published sequential bound, applied to each model's own flags (adapted model: recalibrated threshold; source and twin: fixed clean thresholds).
- For each arm, pooled over the settings where it ran: missed share on the arm's strict streams, against the frozen source's missed share on the source's strict streams (same streams, counted once).
- The coupling-specific contrast is against the **BN-only twin**: same normalisation, no objective. Its strict streams are defined from the twin's own error and its own clean error.
- **Blind spot SHOWN** for an arm needs both: (i) its missed share exceeds the twin's, with the lower end of a 95% interval for the difference above 0 (2,000 resamples of (setting, corruption) clusters, seed 0); (ii) it is higher than the twin's in more than half of the settings with at least 5 strict streams on both sides.
- **INCONCLUSIVE** with fewer than 20 strict streams on either side or fewer than 2 eligible settings. **NOT SHOWN** otherwise.
- Secondary, reported with the same interval: the contrast against the frozen source. The source fails on different streams from the adapted model (severe corruption rather than class skew), so this contrast is confounded by which streams fail.
- Why the rule has this form: a first draft required a 1.5-fold ratio against the source. A dry run of `analyze10.py` on the already-seen exp006 and exp008 streams, before any exp010 stream existed, gave Tent 1e-3 a ratio of 1.34–1.48 against the source (interval for the difference −0.01 to 0.30) and 1.8–2.0 against the twin (0.13 to 0.39). The ratio was arbitrary and the source contrast confounded, so the rule was restated as above. Both contrasts are reported for every arm.
- `im` is a mixed objective: its diversity term opposes class-skewed predictions. A negative result for `im` may reflect that term; a negative result for `pl` would limit the claim to entropy.
- **Decay prediction (frozen, secondary).** For each model, the AUROC of its 20-batch window confidence between its own failing and its own safe held streams is computed in six windows, per setting, then averaged. *Decay SHOWN* for an arm if the adapted model's AUROC falls from the first to the last window by at least 0.10 more than the twin's. On exp006 and exp008 (already seen, Tent 1e-3) the falls were 0.52 and 0.56 for Tent against 0.00 for the twin and the source.
- Descriptive: error capture (share of errors flagged) for arm against source per setting.

Every outcome (three arms, both contrasts, the decay read-out) is reported whichever way it falls.

## Compute

- Two SageMaker training jobs in us-east-1, each with a hard runtime limit and no background loops: CIFAR-10-C on ml.g6e.8xlarge, medical on ml.g6e.4xlarge (fall back to another g6e size if there is no capacity).
- The code was smoke-run end to end on CPU (every checkpoint, every arm, the medical preparation) before launch.
- Conventions inherited unchanged from exp004–008, stated here because a pre-run review asked: predictions are the logits of the forward pass used for the update (before the step), while the monitor's threshold is recalibrated every 5 batches with the weights after the step; and the released monitor's confidence-sequence tuning parameter uses the first quarter of the stream, as in the authors' code.
- Jobs write streams only. `analyze10.py` runs locally on the downloaded streams, once. Python via uv (`--python 3.10 --with numpy<2 --with confseq --with scipy --with lightgbm --with scikit-learn`).
- Resources are logged in `AWS_RESOURCES.md`.

## Pre-run review (14 Nov 2026)

A read-only adversarial review by a second agent (Codex session `01a1786b`) before the freeze found no held-label leakage into choices or levels. It asked for, and this record and `analyze10.py` now include: abstention instead of silently dropping uncalibratable settings; a completeness check; a coupling rule that also requires a contrast with the BN-only twin and handles zero or saturated baselines; achieved false-alarm rates and minimum support in the matched comparison; a false-alarm band in C4; and no claim of a conformal guarantee.

## Freeze

Frozen 14 Nov 2026, 01:55 IST, before any exp010 stream ran. First 16 hex digits of sha256:

- `analyze10.py`: `3ddb8d1c4194b250`
- `run10.py`: `a5c441815168324f`
- `prepare10.py`: `676541187ca84ded`
- `corrupt10.py`: `d28a77aa4efbbc0e`
- `launcher10.py`: `dd63e745f2d76d19`
- `job.sh`: `f58f3e358dd2d191`
- `cifar_models.py`: `8e0a04b097e3c27b`

Smoke runs before the freeze (CPU, 4–6 batches per stream, fake medical images, clean CIFAR-10 only) checked that every checkpoint, every arm and the medical preparation run; their outputs were discarded and contain no exp010 stream. Clean calibration errors seen in the smoke run: AugMix WRN-40-2 0.046, AugMix ResNeXt 0.044, PRIME ResNet-18 0.078, Addepalli WRN-34 0.142.

## Run (14 Nov 2026, 08:40–10:50 IST)

- The SageMaker jobs submitted at 02:00 IST produced nothing retrievable: the AWS key was rejected by 08:24 IST and the user reported the account's credits exhausted. AWS was dropped.
- Streams ran on RunPod secure cloud: three pods, each 2 × RTX 4090, torch 2.9.1+cu128, numpy 2.2.6 and torchvision 0.24.1 installed with uv. Cost $9.76. All pods were deleted; `runpodctl pod list` is empty.
- All 4,630 planned streams are in `diagnostics/2026-11-14-exp010-confirm/results/streams/` (14 settings, each complete). The frozen `analyze10.py` (sha256 prefix `3ddb8d1c4194b250`, unchanged) ran once: `results/analysis.log`, `results/report10.json`, `results/rows10.json`.
- Deviations, none in the frozen stream or analysis code:
  - RTX 4090s and RunPod's image instead of L40S and the SageMaker image; `runpod/pod_run.sh` and `runpod/parfetch.sh` replaced `job.sh` (Zenodo throttled single connections, so files were fetched as parallel ranges and md5-checked).
  - Shard counts per setting differed from the SageMaker plan. Shards only decide which process runs which stream.
  - Each medical dataset ran on one pod, so all its objectives share one source model (`results/models/`).
  - On the two medical pods a second launcher was started for the `im` tasks to avoid idle GPUs; a few streams were therefore computed twice and the later file kept.
  - `calibration.json` of `cifar10__Hendrycks2020AugMix_WRN__pl0.001` had one extra closing brace, because two shard processes wrote it at once. The first analysis attempt stopped on it before computing anything. The file was repaired by keeping the first valid object; the original is kept as `.orig`. Calibration values agree across all objectives of every model.
  - Two pods were accidentally started twice and were wiped and restarted before any stream was written.

## Outcome: PARTIAL

Held-out streams, Tent 1e-3, pooled: 272 strict and 399 safe (CIFAR-10-C 151 and 361; OrganSMNIST 66 and 7; TissueMNIST 55 and 31). No setting was flagged weak by the audit, and none abstained.

| | Condition | Result | Met |
|---|---|---|---|
| C1 | Matched-5% misses at least 40% fewer than the released proxy | 5/206 (2.4%) against 31/206 (15.0%), −84%; achieved false alarms 5.6% for both. OrganSMNIST left out of this comparison (7 held safe streams, below the minimum of 10) | yes |
| C2 | False alarms ≤ 10% pooled, ≤ 15% per dataset with at least 20 safe streams | 30/399 (7.5%); CIFAR-10-C 29/361 (8.0%), TissueMNIST 0/31; OrganSMNIST 1/7, too few to judge | yes |
| C3 | Missed ≤ 20% and at least 40% fewer than the published monitor; no dataset worse than it | 22/272 (8.1%) against 171/272 (62.9%), −87%; 1/151 against 76/151, 10/66 against 40/66, 11/55 against 55/55 | yes |
| C4 | At least 30% fewer misses than the twin with a constant level (or ≤ 5%); no dataset worse by more than 2 streams; false alarms ≤ 7.5% | Misses 22/272 against 40/272 (−45%), holds; per dataset 1 against 1, 10 against 28, 11 against 11, holds; false alarms 30/399 = 7.52%, **fails** (29 would have passed) | **no** |

Verdict by the frozen rule: **PARTIAL** (C1, C2 and C3 hold; C4 fails on its false-alarm band).

**What the audit chose.** Twin with a constant level on TissueMNIST and three CIFAR-10 checkpoints; DoC with a time-resolved level on AugMix WRN-40-2; the fusion on OrganSMNIST.

**Reading (ours).**
- The power criteria that the exp008 detector failed were met on unused data: 8.1% missed against a 20% ceiling.
- The level still does not hit its target. Realised false alarms were 7.5% against a nominal 5%, 8.0% on CIFAR-10-C, and the frozen band was missed by a fraction of one stream. The claim "the level now transfers" is not confirmed.
- FV's gain over the earlier rule came from one dataset. It chose the twin on five of six settings, where the two rules are the same detector; on OrganSMNIST it chose the fusion and missed 10 instead of 28.
- On TissueMNIST it still missed 11/55 (20%).
- The 30 false alarms were mostly under class skew (16 at Dirichlet 0.1, 10 at Dirichlet 1) and spread over corruptions (fog 6, impulse noise 4, shot noise 4).

**Deployed, all detectors (Tent 1e-3, pooled; descriptive).**

| Detector | Missed | False alarms | Matched-5% missed |
|---|---|---|---|
| FV | 22/272 | 30/399 | 2.4% |
| Monotone LightGBM, Z | 35/272 | 23/399 | 2.9% |
| DoC, time-resolved level | 36/272 | 27/399 | 15.0% |
| Fusion | 39/272 | 25/399 | 11.2% |
| FV restricted to twin or DoC | 40/272 | 29/399 | 2.4% |
| Twin, constant level (earlier rule) | 40/272 | 31/399 | 2.4% |
| Released proxy, dev level | 60/272 | 13/399 | 15.0% |
| Earlier twin bound | 65/272 | 44/399 | – |
| Published monitor | 171/272 | 4/399 | – |

FV on the other objectives (secondary): pseudo-labels 13/215 missed with 8/181 false alarms (published monitor 132/215); information maximisation 5/303 with 3/130 (published 131/303).

## Coupling test outcome

Published monitor on each model's own flags; missed share on that model's strict streams.

| Objective | Adapted model | BN-only twin | Frozen source | Difference vs twin (95% interval) | Higher than twin in | Verdict |
|---|---|---|---|---|---|---|
| Entropy (Tent) | 171/272 (63%) | 133/358 (37%) | 92/184 (50%) | 0.26 (0.17 to 0.34) | 5 of 6 settings | **SHOWN** |
| Pseudo-labels | 132/215 (61%) | 108/246 (44%) | 81/146 (55%) | 0.17 (0.10 to 0.26) | 3 of 4 | **SHOWN** |
| Information maximisation | 131/303 (43%) | 108/246 (44%) | 81/146 (55%) | −0.01 (−0.07 to 0.05) | 2 of 4 | **NOT SHOWN** |

- Secondary contrast against the frozen source: Tent 0.13 (0.02 to 0.25); pseudo-labels 0.06 (−0.07 to 0.21); information maximisation −0.12 (−0.24 to −0.01).
- Decay prediction (fall in AUROC of window confidence, first to last 20 batches): **SHOWN for all three.** Tent 0.98 to 0.59; pseudo-labels 0.98 to 0.72; information maximisation 0.98 to 0.79. Twin 1.00 to 1.00; source 0.93 to 0.93 (Tent settings) and 0.88 to 0.89 (other settings).
- Reading (ours): the blind spot is not specific to entropy; it appeared for hard pseudo-labels. It did not appear as missed alarms under information maximisation, although that model's confidence also lost separation over the stream. As stated before the run, the diversity term makes that negative result ambiguous.

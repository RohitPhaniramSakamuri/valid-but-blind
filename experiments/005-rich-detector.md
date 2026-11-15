# 005: Can a richer or learned detector beat the twin? (protocol frozen 3 Nov 2026 before any stream ran)

Status: PLANNED at freeze. Outcomes are appended below after the run.

**Earlier exploratory work:** `diagnostics/2026-11-03-exp005-detector/dev_offline.py` used results already seen, so it makes no held-out claim.

**Data.** BloodMNIST-224 (primary, never used in this project) and DermaMNIST-224 (secondary; its results are already known in aggregate). ResNet-18 trained as in exp004, using a fit/select/calibration split of the train set.

**Separation.** Detectors are fit and tuned only on streams from official validation images with dev corruptions (Gaussian noise, speckle, brightness, gamma, saturation). Held-out streams use official test images with blur, JPEG, contrast and pixelate. Test labels only score results. Three severities, three priors (natural, Dirichlet 1, 0.1), clean included; dev two draws, held three. 120 batches of 48. Arms Tent 1e-3 (primary) and 5e-3.

**Clear failure/safe:** as exp004 (strict: mean error >= r0+.15, last-quarter < .85; safe: mean error < r0+.10, last-quarter < .85).

**Signals.** Per image from Tent, the twin and frozen source: confidence, margin, entropy, pairwise agreement, KL, prototype distance, feature norm, penultimate dropout disagreement. Per batch: predicted-class entropy, source BN input shift per block, BN parameter drift, PCA-16 penultimate means.

**Candidates.**
- Unlearned: released, prototype, twin (with sequential bound as in exp004 and with same-margin form), ATC, DoC-style confidence, simplified AETTA-style dropout disagreement (a simplification, not the published method).
- Learned, predicting prefix error: ridge, LightGBM, ridge+LightGBM stack, PCA latent+LightGBM, GRU on batch features, per-image LightGBM averaged per batch, and an average of per-image and stream LightGBM.

**Selection.** One learned detector is chosen on dev only: leave-one-dev-corruption-out within each dataset, pooled, fewest missed with false alarms <= 10%, ties broken by AUROC. Alarm margin: 95th percentile of the out-of-fold maximum score on safe dev streams. Same procedure for every same-margin detector. No selection or tuning uses held streams.

**Verdict (BloodMNIST, Tent 1e-3, held).** BETTER DETECTOR if the selected detector misses <= 20% of strict streams and has false alarms <= 10% with >= 40 safe streams, and misses at least .10 fewer than the same-margin twin with false alarms not more than .05 higher. INCONCLUSIVE with < 20 strict or < 40 safe. Otherwise NOT SHOWN. All other detectors, Tent 5e-3 and DermaMNIST are descriptive.

**Limit.** Dev and held corruptions share a dataset and an image-quality nature. This tests new corruption families, not arbitrary shifts; there is no formal guarantee.

## Outcome (run 3 Nov 2026, 07:28–08:31 IST; H100 pod, about $4.40, deleted after copying results)

**Verdict: NOT SHOWN.**

**What happened during the run.**
- The first launch used 12 processes and ran out of GPU memory during the 1,000-image calibration pass. I relaunched with 8 processes. Code and seeds were unchanged, and finished streams were kept.
- The first analysis stalled from thread contention. I reran it with 4 threads. This was a speed-only change.

**Setup.**
- Source models: BloodMNIST val accuracy .984 (r0 .020); DermaMNIST r0 .172.
- 852 streams in total.
- Raw data: `diagnostics/2026-11-03-exp005-detector/raw/results.tgz`, gitignored, md5 2a14dd75...
- Reports: `report.json`, `selection.json`, `rows.json`.

**Dev selection.** Leave-one-dev-corruption-out, out-of-fold, at 10/181 false alarms.

| Detector | Missed (of 117) |
|---|---|
| image_plus_stream (selected on the AUROC tie-break) | 1 |
| lgbm | 1 |
| latent_lgbm | 2 |
| gru | 3 |
| stack | 4 |
| twin | 4 |
| ridge | 6 |
| prototype | 22 |
| released | 32 |

**Held, BloodMNIST, Tent 1e-3 (primary).**

| Detector | Missed | False alarms |
|---|---|---|
| Selected (image_plus_stream) | 13/45 | 0/65 |
| Same-margin twin | 4/45 | 3/65 |

The selected detector misses 29%, above the 20% limit, and does worse than the twin.

**Held, pooled over 4 settings (two datasets × two Tent learning rates; 165 strict, 185 safe). Descriptive.** Each detector's alarm margin was set on dev streams.

| Detector | Missed | False alarms |
|---|---|---|
| Same-margin twin | 9/165 (5.5%) | 15/185 (8.1%) |
| lgbm | 27/165 (16%) | 14/185 (7.6%) |
| prototype | 35/165 (21%) | 18/185 (9.7%) |
| image_plus_stream | 42/165 (25%) | 4/185 (2.2%) |
| DoC | 49/165 (30%) | 10/185 (5.4%) |
| Dropout disagreement (simplified, not AETTA) | 53/165 (32%) | 11/185 (5.9%) |
| released | 58/165 (35%) | 9/185 (4.9%) |
| Twin with clean-image correction and sequential bound (exp004 form) | 72/165 (44%) | 21/185 (11%) |

**Per setting, same-margin twin.**

| Setting | Missed | False alarms |
|---|---|---|
| Blood 1e-3 | 4/45 | 3/65 |
| Blood 5e-3 | 0/42 | 9/70 (13%) |
| Derma 1e-3 | 5/41 | 1/37 |
| Derma 5e-3 | 0/37 | 2/13 |

The exp004-form twin bound missed 41/41 on Derma 1e-3. The released monitor missed 30/37 on Derma 5e-3.

**Cross-dataset (margin from the other dataset's dev).**

| Direction | Twin missed | Twin false alarms |
|---|---|---|
| Derma → Blood | 1/45 | 4/65 |
| Blood → Derma | 8/41 | 0/37 |

**Interpretation (ours).**
- The learned models fit the dev corruptions and transferred worse than the twin signal.
- The large gain comes from replacing the clean-image correction and confidence bound with an alarm margin calibrated on synthetic dev-corruption streams.
- That twin form was a pre-specified comparator, not the selected primary, so its numbers are held-out but secondary. A new frozen test with it as primary is needed before it can be a headline claim.
- It has no formal guarantee. False alarms exceeded 10% in one of the four settings.
- BloodMNIST is easy for the source model (r0 .02); the released monitor's blind spot there is small (2/45).

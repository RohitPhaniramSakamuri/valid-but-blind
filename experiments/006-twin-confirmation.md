# 006: Frozen confirmation of the dev-calibrated twin alarm (frozen 3 Nov 2026, before any stream ran)

Status: PLANNED at freeze. Outcomes are appended after the run.

**Why.** In exp005, the twin with an alarm margin set on synthetic dev streams did best on held-out data (9/165 missed, 15/185 false alarms). It was a comparator there, not the primary. This experiment tests it as the primary, on data and draws not used before.

**Primary detector (fixed now).**
- Per batch, flag images where the twin is uncertain (twin confidence below its clean max-F1 threshold) or the twin and the adapted model disagree.
- The score is the running mean of the flag rate minus the twin's clean error.
- Alarm at the first checkpoint (batch 11 onward, every 5 batches) where the score exceeds the margin.
- The margin is set separately for each deployed model, adaptation method and dataset, from that setting's dev streams only.
- The margin is the k-th smallest of the per-stream maximum scores on the n safe dev streams, with k = ceil((n+1)(1−0.05)). If k > n there are no alarms. This is the split-conformal construction: if dev and real safe streams are exchangeable, false alarms are at most 0.05 + 1/(n+1).

**Data (none used before in this project).**
- PathMNIST-224 (colour histology, 9 classes).
- OrganAMNIST-224 (grayscale CT, 11 classes).
- CIFAR-100-C on the six RobustBench models used in exp004, with new seeds (tag exp006).

**Separation.**
- Medical:
  - Dev streams use official validation images with Gaussian noise, speckle, brightness, gamma and saturation. For grayscale OrganA, shot noise replaces saturation.
  - Held streams use official test images with blur, JPEG, contrast and pixelate at three severities.
- CIFAR:
  - The test set is split by seed: 1,000 calibration, 4,000 dev and 5,000 held images.
  - Dev uses Hendrycks' four extra corruptions (speckle_noise, gaussian_blur, spatter, saturate).
  - Held uses the 15 standard corruptions at severities 1, 3 and 5.
- All streams:
  - Priors are natural, Dirichlet 1 and Dirichlet 0.1; streams are 120 batches of 48, and clean streams are included.
  - Labels only build streams and score results.
- Source models:
  - Medical: ResNet-18 trained as in exp005 on at most 30,000 training images.
  - CIFAR: the published checkpoints.

**Arms.**
- Tent 1e-3 on everything (primary).
- Tent 5e-3 and SAR (as in exp004) on the medical sets (secondary).
- EATA was not run, because I could not reproduce its filters reliably.

**Definitions (as exp004).**
- Strict failure: mean error ≥ r0 + 0.15 and last-quarter error < 0.85.
- Safe: mean error < r0 + 0.10 and last-quarter error < 0.85.

**Verdict on Tent 1e-3, held streams, pooled over PathMNIST, OrganAMNIST and CIFAR.**
- **CONFIRMED** if all of these hold:
  - the twin misses ≤ 20% of strict streams;
  - false alarms are ≤ 10% of safe streams;
  - it misses at least 0.15 fewer than the released monitor under the same margin rule;
  - it misses at least 0.15 fewer than the exp004 twin bound;
  - each of the three datasets on its own has ≤ 30% missed and ≤ 15% false alarms.
- **PARTIAL** if the pooled conditions hold but a dataset fails.
- **INCONCLUSIVE** with fewer than 40 strict or 60 safe pooled streams.
- **NOT CONFIRMED** otherwise.

**Descriptive only.** Every other detector from exp005 is kept, and LightGBM is fit on each dataset's dev streams. Also reported: the secondary arms, the conformal bound n per setting, first-alarm times and per-corruption misses.

**Compute.** One SageMaker ml.g7e.4xlarge training job in us-east-1 with a hard time limit. Resources are logged in AWS_RESOURCES.md.

## Outcome (run 3 Nov 2026, 09:40–12:20 IST; SageMaker L40S jobs; analysis 12:35 IST)

**Verdict: NOT CONFIRMED.** 2,592 streams.

**Primary, pooled over three datasets, Tent 1e-3, held-out (306 strict, 578 safe).**

| Detector | Missed | False alarms |
|---|---|---|
| Twin, dev-conformal margin | 40/306 (13%) | 14/578 (2.4%) |
| Released monitor, same margin rule | 81/306 (26%) | 31/578 (5.4%) |
| Released monitor as published (sequential bound) | 149/306 (49%) | 12/578 (2.1%) |
| Twin with exp004 sequential bound | 53/306 (17%) | 38/578 (6.6%) |
| Prototype | 86/306 (28%) | 20/578 (3.5%) |
| ATC | 45/306 (15%) | 21/578 (3.6%) |
| DoC | 34/306 (11%) | 31/578 (5.4%) |
| Dropout disagreement | 37/306 (12%) | 32/578 (5.5%) |
| LightGBM | 62/306 (20%) | 15/578 (2.6%) |

**Which conditions held:**
- Met: missed ≤ 20%; false alarms ≤ 10%; every dataset ≤ 30% missed and ≤ 15% false alarms (Path 3/67 and 1/25, OrganA 12/40 and 0/62, CIFAR 25/199 and 13/491).
- Failed: the twin had to miss at least 0.15 fewer than the same-margin released monitor. The gap was 0.13.
- Failed: the twin had to miss at least 0.15 fewer than the exp004 twin bound. The gap was 0.04. That bound misses less on the medical sets, but there its false alarms are 13/25 (Path) and 16/62 (OrganA).

**Secondary (descriptive): twin vs. the published released monitor.**

| Setting | Twin missed | Twin false alarms | Published monitor missed |
|---|---|---|---|
| Path Tent 5e-3 | 27/80 | 0/23 | 70/80 |
| Path SAR | 9/94 | 0/3 | 8/94 |
| OrganA Tent 5e-3 | 9/39 | 0/61 | 22/39 |
| OrganA SAR | 4/52 | 0/52 | 0/52 (but 7/52 false alarms) |

**Per CIFAR model (twin missed and false alarms; published monitor missed):**

| Model | Twin missed | Twin false alarms | Published monitor missed |
|---|---|---|---|
| PARN18 | 3/18 | 1/106 | 18/18 |
| WRN34 | 1/16 | 2/108 | 15/16 |
| WRN-34-10 | 3/22 | 3/103 | 7/22 |
| ResNeXt | 1/35 | 1/77 | 28/35 |
| AugMix WRN | 0/44 | 4/64 | 25/44 |
| PRIME | 17/64 | 2/33 | 0/64 (but 9/33 false alarms) |

**Interpretation (ours).**
- Against the monitor as published, the twin misses far fewer failures (13% vs. 49%) at a similar false-alarm rate (2.4% vs. 2.1%).
- Much of that gain also appears when any confidence signal gets the same dev-calibrated margin. DoC, dropout disagreement and ATC reach 11–15% missed, but with 1.5–2.3 times the twin's false alarms.
- The twin has the lowest false-alarm rate among the detectors that miss about 15% or less. It is not uniquely best on misses.
- The frozen improvement margins over the same-margin released monitor and over the exp004 bound were not met. The claim "the twin is clearly better than the same-margin monitor" is therefore not confirmed on new data.

**Infrastructure notes.**
- The first two jobs eventually also ran 5 CIFAR models with identical code and seeds. Those duplicates are kept for a reproducibility check and are not used in the analysis.
- Addepalli WRN34 needed a BN-hook fix, which affects only descriptive features.
- Clean CIFAR-100 came from the Hugging Face mirror; labels were checked against CIFAR-100-C.

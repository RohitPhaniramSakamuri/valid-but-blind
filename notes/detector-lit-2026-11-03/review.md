# Label-free failure detectors under test-time adaptation

Bounded review, 3 November 2026. Sources below are those opened in the project record; no new experiments or code tests.

## 1. Estimators and monitors

**Status: partial.** This is a targeted map, not a re-read of every named method.

| Method | Signal / estimator; unit | Online or batch; TTA? |
|---|---|---|
| Schirmer et al., *Monitoring Risks in TTA* ([NeurIPS 2025](https://proceedings.neurips.cc/paper_files/paper/2025/hash/746960ad49ddb47248970a0e1404230c-Abstract-Conference.html)) | Source-calibrated unlabeled loss proxies; sequential lower risk bound, proxy informativeness assumption. Experiments include proxy failure and prototype-distance replacement. | Online sequential; specifically TTA. |
| AETTA ([CVPR 2024](https://openaccess.thecvf.com/content/CVPR2024/html/Lee_AETTA_Label-Free_Accuracy_Estimation_for_Test-Time_Adaptation_CVPR_2024_paper.html)) | Dropout disagreement estimates current adapted-model accuracy; supports recovery decisions. | Repeated online estimates; specifically TTA. Extra stochastic forwards. |
| ATC ([Garg et al., ICLR 2022](https://arxiv.org/abs/2201.04234)) | Source-validation-calibrated confidence threshold estimates target accuracy of a fixed classifier. | Target-set/batch estimate; not TTA-tested as an adapting risk alarm. Requires assumptions; arbitrary-shift accuracy is unidentifiable. |
| Flühmann et al. ([2025 preprint](https://arxiv.org/html/2507.22776v1)) | Confidence-derived confusion matrices / CM-ATC, CM-DoC and CBPE estimate clinical metrics. Fixed binary classifiers; labeled source training/validation. | Dataset/batch estimates; not online TTA. Artifact and prevalence experiments are separate. |
| MMC+ ([2024 preprint version read](https://arxiv.org/html/2410.13174v2)) / CheXstray ([2022 abstract](https://arxiv.org/abs/2202.02833)) | Embedding/image appearance, metadata and classifier outputs for medical drift; reference windows. CheXstray abstract-only here. | Windowed drift monitoring, not risk guarantees or TTA. MMC+ uses independent feature channels; drift need not imply error. |
| Named leads not characterized here | AutoEval/meta-models, DoC, ProjNorm, Agreement-on-the-line, COT, GDE, SSL estimators, TRUSTED, MANO, CheXstray successor details, MMC+ 2026 journal version and medical confidence aggregation need source-specific inspection before comparison. | No method-level claims made. Some names denote distinct tasks/settings; do not treat them as interchangeable estimators. |

## 2. Learned estimator architectures

**Status: no report found (bounded search).** In opened records I found no reported comparison showing gradient boosting, stacking, GRU/TCN, or a latent representation layer beating simpler estimators on batch/per-sample statistics for this TTA risk-detection task. Flühmann’s confidence-derived metric estimators and Schirmer’s calibrated proxy/sequential construction are relevant simpler competitors; AETTA uses stochastic disagreement, not evidence here for boosting. This is not a claim that such architectures are absent from all adjacent literature. No performance numbers for those architecture comparisons were verified.

## 3. Adapted-versus-BN/frozen twin signal

**Status: no report found (bounded search) for the exact signal; partial for adjacent signals.** Schirmer et al. directly study proxy failure under adaptation and replace uncertainty with prototype distance; AETTA uses dropout disagreement on the adapted model and recovery. Those anticipate label-free TTA monitoring and model disagreement broadly, but neither source inspected reports confidence/prediction-gap features between entropy-adapted Tent and a same-weight, no-gradient copy using current test-batch BN statistics. Nor did I find an exact adapted-versus-frozen divergence alarm in the opened records. “No report found” is limited to these sources and the project’s targeted review, not an exhaustive literature absence claim.

## 4. Recommendation and expected baselines

**Status: found.** Start with an interpretable, regularized logistic model or shallow gradient-boosted trees only as a secondary comparison; the reviewed evidence does not establish a deep/sequence estimator advantage. Pre-register four feature families: (1) adapted-model confidence/entropy and logit margins; (2) twin-versus-adapted disagreement and confidence gap; (3) source-relative feature/prototype distance; (4) batch temporal summaries and prediction/class histogram. Add image quality only if modality warrants it. Train on labeled source plus synthetic corruption streams, but hold out shift families and prevent target labels/shift IDs entering routing, stopping or tuning. The “error rose above clean +0.10” threshold needs source calibration and fixed false-alarm evaluation; non-alarm cannot certify safety.

Expected baselines: frozen-model ATC/confidence threshold; Schirmer’s proxy monitor and prototype-distance proxy; AETTA dropout disagreement (charge extra forwards); entropy-only and twin-only rules; source/frozen sentinel; simple feature/prototype distance; and a prevalence-aware confidence-derived estimator where task assumptions permit. Compare sensitivity at matched false-alarm rate and report latency/compute, calibration by shift family, and sequential delay. Use whole streams as evaluation units, not shuffled batches alone.

### Sources actually opened

Schirmer, *Monitoring Risks in Test-Time Adaptation* (official NeurIPS record/PDF; selective full-text review, not all proofs): https://proceedings.neurips.cc/paper_files/paper/2025/hash/746960ad49ddb47248970a0e1404230c-Abstract-Conference.html

Lee et al., *AETTA* (CVPR 2024; main methods/results and selected supplement): https://openaccess.thecvf.com/content/CVPR2024/html/Lee_AETTA_Label-Free_Accuracy_Estimation_for_Test-Time_Adaptation_CVPR_2024_paper.html

Garg et al., *Leveraging Unlabeled Data to Predict Out-of-Distribution Performance* (ICLR 2022; selective sections): https://arxiv.org/abs/2201.04234

Flühmann et al., *Label-free estimation of clinically relevant performance metrics under distribution shifts* (2025 preprint; main HTML §§1–6): https://arxiv.org/html/2507.22776v1

Merkow et al., MMC+ (2024 preprint v2 main text; 2026 journal full text inaccessible): https://arxiv.org/html/2410.13174v2

Soin et al., CheXstray (abstract-only screen): https://arxiv.org/abs/2202.02833

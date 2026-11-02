# Final-query candidates: primary-source screen

Date: 2026-11-02. Requested by root after the independent reviewer pass. Primary arXiv metadata, PDFs and extracts are saved in `evidence/tta_causes/`; no experiments or tests performed. These late discoveries are further evidence that the broad citation graph did not reach saturation. None changes the five recommended verdicts.

## Jiang et al., ZAEC, arXiv2608.05945

Verified title: *Respect Your Zero-Shot Uncertainty: Conservative Calibration for Test-Time-Adapted Vision-Language Models*. Jingyan Jiang, Yaru Sun, Xiao Chen, Jiazhen Huang, Caiting Li, Zhijian He, Yin Chen and Pingting Hao; first posted6August2026; no independent venue verified.

Read main diagnostic headings, Table1/Fig2, Method/Props1–2, Experimental Setup, Tables2–4/ablation and conclusion (PDFpp3–7). On prediction-agreement samples, top1/correctness are fixed while adaptation changes confidence/entropy. This is a cleaner existing demonstration of the confidence/accuracy separation underlying C3. ZAEC uses frozen zero-shot entropy as a sample-specific floor, restoring it by the smallest temperature≥1 while preserving class rankings. It is a direct existing **label-free post-hoc calibration repair**, relevant to C5 and any proposed source-entropy anchor. Five VLM methods (TPT/TPS/TDA/DPE/DLAE), CLIPViT-B/16/RN50 and15classification datasets; metrics accuracy/ECE/NLL. No Tent, true-prior Dirichlet setting or sequential risk alarms. Zero-shot underconfidence can make the repair overly conservative (boundary case Fig4; conclusion). The9-page PDF cites AppendicesC/D and proof/implementation appendices that are absent from that downloaded version; they were not read. C3 remains substantially anticipated; C5 remains partially covered.

## Zhang et al., PORTAL, arXiv2610.37658

Verified title: *When Should We Intervene at Test Time?* Jiahao Zhang, Xinling Wen, Liangliang Li and Yu Chen; first posted27October2026;79-page preprint.

Read §§2.1–2.3,4.1–4.3,4.6–4.7 and AppendixX's related-work distinction. PORTAL selects candidate interventions using **sparse target labels**, which score all fixed-before-feedback candidates on the same input. It decides queries/stopping and periodically refreshes labels when past evidence becomes stale. Datasets include CIFAR10/100-C, ImageNet-C, PACS and naturalCLIPsettings; fixed candidates include source/BN/flip/BN+flip. The stale-evidence example in §4.6 changes the label law while candidate predictions remain fixed; it is not adaptation-induced confidence self-masking. It cites Schirmer directly in §4.6 p8 and AppendixX. **Add to forward-citer union if absent.** It is no label-free C5 solution and gives no C1/C2 monitor result. No verdict changes.

## Ren et al., StaR-TTA, arXiv2610.35500

Verified title: *Test-Time Confidence Adaptation under RL-Induced Trajectory Shift*. Zhenzhen Ren, Xiaoqing Zhang, GuoBiao Li, Bowen Fang, Yanxi Wang, Xinpeng Zhang and Ke Han; first posted26October2026; no independent venue verified.

Read §§3.1–3.3,4.1–4.3,5.1–5.2,6 and AppendixA.2/A.4/A.5. Confidence estimators trained on BaseLLM trajectories can lose ranking accuracy after **offline AgenticRL** changes the base model. Controlled tool/answer/trajectory comparisons investigate the transfer loss. StaR-TTA learns source correctness/stability relations with labelled Base trajectories, then fits a linear confidence corrector from target stability rankings and Base–RL agreement without target correctness labels; both LLMs and main scorer stay frozen during this confidence adaptation. QA datasets/LLMfamilies; AUROC/ECE/Brier/NLL; no image corruption/class-prior skew or sequential alarms. This reinforces C4's monitor-staleness vulnerability and C5's existing label-free confidence repair, but does not establish the continual entropy-adaptation mechanism or exact monitor failure. No verdict changes.

## Entropy Enigma extraction correction

The root requested an explicit extraction row for the named seed. It is now in the main agent `report.md` close-work table. Sections4.1–4.4 were reread for this update. Weighted Flips counts changes in predictions of the first1000images over an adaptation trajectory, weighted by each image's initial confidence percentile. Its mapping to dataset accuracy is fit using labelled ImageNet validation and corruption-holdout accuracies. It is a dataset-level estimator of initial/source-model accuracy, not a sequential monitor of the current changing model. Offline labels and adaptation/probing cost must be disclosed. Current reading does not support an assumption-free independent-signal interpretation.

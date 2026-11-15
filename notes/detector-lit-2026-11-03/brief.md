# Literature task: label-free failure detectors for test-time adaptation (hard limit: 20 minutes)

Context: a deployed classifier adapts online with Tent (entropy minimization on BatchNorm parameters). We need a label-free online detector of "true error rose above clean error + 0.10". Existing approach: risk monitor of Schirmer et al. (NeurIPS 2025), blinded by entropy minimization. Our candidate: compare the adapted model with a gradient-free "twin" (same weights, test-batch BN statistics) and feed batch-level features to a learned error estimator trained on synthetic corruptions of labeled source data, optionally gradient-boosted (XGBoost/LightGBM), a stacked ensemble, or a latent representation layer.

Answer, citing only sources you actually opened, with URL, and say abstract-only where that is all you read:

1. Architectures for label-free error/accuracy estimation or failure detection under shift: meta-models / AutoEval, ATC, DoC, ProjNorm, Agreement-on-the-line, COT/optimal transport, GDE, SSL-based estimators, TRUSTED-style, MANO, AETTA, Mahalanobis/feature-based monitors, medical ones (e.g. CheXstray, MMC+, Flühmann 2025). For each: inputs, model family, whether it is online or batch, and whether it was tested under TTA.
2. Any use of gradient boosting, stacking, sequence models (GRU/TCN), or latent/representation layers on batch-level or per-sample statistics for performance estimation. Report what beat what, with numbers if available.
3. Prior use of the specific signal: confidence or prediction gap between an entropy-adapted model and a non-gradient BN-only copy, or adapted-versus-frozen divergence, as an error or failure signal in TTA. Closest matches, and whether any anticipates it exactly.
4. Recommendation: which three to five feature families and which model class are best supported, and which competitors a reviewer would expect as baselines.

Do not invent citations. Write the answer to notes/detector-lit-2026-11-03/review.md, with a one-line status for each question: found / partial / no report found (bounded search). Keep it under 900 words.

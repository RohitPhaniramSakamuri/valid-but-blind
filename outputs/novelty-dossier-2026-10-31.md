# Novelty dossier: does candidate A survive its closest prior work?

Date: **31 October 2026**. Status: literature attack and proposed experiment. **No model was run.** This is a targeted refresh of the 26 October review, not a systematic search. No novelty is verified.

## 1. Verdict

| Part of candidate A | Decision | Reason |
| --- | --- | --- |
| H1: the same batch can favour different actions after different histories | **Keep only as a gate. Not a contribution.** | TTAB, MORPHEUS and the identifiability study already show that history and order change outcomes. |
| H2: deeper state (optimizer, displacement) adds value beyond current-model evidence | **Demote; low expected value.** | See the structural argument in §3. The only state that is truly hidden can often be removed by design. |
| H3: training on the selector's own states fixes a replay-to-autonomous failure | **Keep as a control, not as the method.** | DAgger is the known remedy. A new analogous LLM study found that training on successive states did not consistently help. |
| Refined candidate A′: adaptation corrupts the evidence the selector reads | **New working candidate; unverified.** | §4. It is more specific and can be refuted cheaply, but AETTA and Cygert et al. sit close to it. |

Plain recommendation: stop treating "selector on self-induced states" as the paper. Test A′ with the small experiment in [Experiment 003](../experiments/003-evidence-decay-under-adaptation.md). If A′ fails, a large selector study has little left to justify it, and the project should reconsider B or a new direction.

## 2. The headroom problem

A selector can only win by the gap between the best fixed method and an oracle. Published numbers suggest that gap can be small once a strong fixed method is included.

- **MORPHEUS Table 1** (ViT-B, ImageNet-C severity 5; authors' numbers). The paper's own comparison is 65.1% for its selector against 65.2% for SPA. **Our arithmetic** on that table: a per-corruption oracle over the ten listed methods averages 65.75%, against 65.25% for SPA. SPA is best in 13 of 15 corruptions; ROID wins defocus and contrast. So this per-domain menu has about **0.5 points** of room. This is one table, one model and domain-level choice with reported means. It does not bound batch-level or non-IID settings.
- **Identifiability Table 1** (CIFAR-100-C controlled worlds; authors' numbers, the paper is marked under review at ICLR 2027). Oracle regret is 4.980 pp for SOURCE/KEEP and 0.312 pp for source-only stream-aware evidence (Z3). In that source-reset setting, little regret remains for a better selector to remove. Matched IID/correlated worlds are where these selectors differ.

**Consequence (our interpretation):** an "our selector beats the methods" paper looks hard on IID corruption benchmarks. Any headroom more likely lies in correlated or class-skewed streams and in live, non-source states. Those are exactly the states these two papers did not select from.

## 3. Why H2 and H3 are weak

**H2, structural argument (ours, untested).** Intuition: if two models have the same weights and buffers, they give identical predictions and differ only in hidden update memory. With plain SGD there is no such memory, so nothing hidden remains. If weights differ, the difference is at least partly visible in current logits and features. So "deeper state" has two possible values:

- **Optimizer memory:** real but removable. ASR's released code already restores the optimizer on reset (`self.optimizer.load_state_dict(self.optimizer_state)` in `methods/base.py`, `asr_reset`, read 31 October from the default branch, commit not pinned). A stateless update is a one-line alternative.
- **Parameter displacement not visible in a 64-image batch:** possible, but GALA already acts on layer displacement since an anchor.

This does not prove H2 false, because a small batch may reveal weight differences poorly. It does make H2 a poor primary claim.

**H3.** Harness Learning (LLM agents, not vision) reports: "Training on successive revision contexts with immediate rewards does not consistently improve on training on individual revisions." (§5.4). This does not transfer directly, but it is a warning that the remedy may add nothing. Meanwhile Agentic-TTT Appendix E already names the mismatch ("can introduce exposure bias") and leaves autonomous-stream training to future work. So a measured gap in vision would be an application of a named problem, and would need a large effect to stand as a contribution.

## 4. Refined candidate A′: evidence decay under adaptation

**Intuition.** A thermometer is useless if the act of treating the patient also changes how the thermometer reads. Entropy-based TTA pushes entropy down, and selectors often read entropy. So the update may damage the selector's instrument.

**Example.** A selector learns on source-reset batches that "mean entropy 1.2 means UPDATE helps". After 100 updates, the live model reports entropy 0.4 on an equally hard batch, because lowering entropy is what it was trained to do. The learned mapping now misreads the situation.

**The tension that could make this useful (our hypothesis):**

| Evidence | Sees the live state? | Altered by updates? |
| --- | --- | --- |
| Frozen-source pass | No | No |
| Live quantities the update directly optimizes (entropy, confidence) | Yes | Yes, directly |
| Live quantities not directly optimized (feature geometry) | Yes | Indirectly |
| Source-live disagreement | Partly | Partly |

**Exact claim to test.** In an online, predict-then-update stream with no target labels at runtime, and a pre-action selector fitted on labeled auxiliary streams: the error of a next-block action-value predictor grows with adaptation exposure, more for directly optimized evidence than for other evidence. The growth is not removed by simply fitting on all exposure levels at the same budget.

**Implementation significance.** If true, a selector should be built from a specific evidence type or recalibrated by exposure, and existing selectors' source-reset evaluations would overstate their online value. If false, entropy-style evidence is safe to use across adaptation, which is a modest but usable negative result.

## 5. Closest sources and what they already cover

Passages were read in primary text on 31 October unless stated. Reading was selective, not full-paper.

| Source (key) | Passage inspected | Already covers | Does not cover, in what we read |
| --- | --- | --- | --- |
| **AETTA** (`Lee2024AETTA`) | §3.2; results discussion | **Closest to A′.** "as the expectation function's accuracy drops, the confidence increases" and this "violates" calibration. Softmax-score estimates overestimate accuracy when accuracy drops. Corrects with dropout disagreement and skew. | Estimates current-model accuracy, not the next action's value. No comparison of optimized and unoptimized evidence by exposure. |
| **Cygert et al.** (`Cygert2026RealisticSelection`) | Selection-over-time figure text; §6 | For EATA, selecting by entropy helps at first and then declines; unsupervised selection "may oscillate". | Selects hyperparameters by post-adaptation criteria, not pre-action actions. |
| **Entropy Enigma** (`Press2024EntropyEnigma`, new) | Abstract, §4 | Entropy minimization helps for a few steps, then embeds test data far from training data. Estimates accuracy from prediction flips during adaptation. | Dataset-level accuracy prediction, not stream action selection. |
| **Identifiability** (`Jhawar2026Identifiability`) | §4.1, Table 1, §7 | "Every action starts from the same frozen source state for a target world." Source-only evidence avoids decay by construction. | No selection from live adapted states in the parts read. |
| **MORPHEUS** (`Danilowski2026MORPHEUS`) | §§1–3, Table 1 | Pre-action prediction from source entropy and geometry; regressors fitted by adapting on training domains. | Source model only, one choice per domain (6,400 samples per domain in Table 1). |
| **Agentic-TTT** (`Lu2026AgenticTTT`) | §2.2.2, Appendix E | Same-snapshot counterfactuals; gold-history training; names exposure bias. | LLM skill library over a frozen backbone; does not test it. |
| **ASR** (`Lim2026ASR`) | §§3.3–3.5, appendix; `methods/base.py` | Hand-designed reset timing and scope; source/current inconsistency sets coefficients; about 38% of its resets are detrimental. Hyperparameters set on "5% of a single holdout split". | Add-on to a method; does not choose among methods or fit a learned selector. |
| **GALA** (`Sahoo2025GALA`) | §§2.1–2.3 | Hand-set cosine threshold on displacement since an anchor; rejects "misaligned" updates. | Layer masking, not action selection. |
| **Hybrid-TTA** (`Park2025HybridTTA`) | §4.1, supplement | Hand-set loss-EMA rule switches full/adapter tuning. Values "heuristically selected based on a small subset of the first target domain". | Segmentation, not learned. Its own loss signal is affected by earlier tuning; feedback not analysed in what we read. |
| **RNA** (`Yeo2023RNA`) | arXiv v1, §3 (CVF PDF still returned 403) | **Resolves a handoff question:** "the original weights of f are frozen", and a controller needs only a forward pass. | Not a persistent-weight rollout, so it does not cover training on self-induced states. Needs feedback signals beyond plain unlabeled classification. |
| **TTAB** (`Zhao2023Pitfalls`) | Abstract, §4.1 | Selection is "exceedingly difficult due to online batch dependency", even given labels. **This is H1's predecessor.** | Hyperparameters and model selection, not an evidence-exposure study. |
| **Harness Learning** (`Zhang2026HarnessLearning`, new) | §4.3, §5.4, Appendix F headings | Training on successive states showed no consistent gain. | LLM agent harness; prescribed revision reports. |
| **Reliability-gated anchoring** (`Singh2026ReliabilityGated`, new) | Abstract, limitations heading | Frozen-source evidence can itself become unreliable ("blind anchoring"); entropy gate misses "wrong low-entropy sources". | Gates an anchor inside ROID. **Directly weakens the "source evidence is safe" row in §4.** |
| **OATTA** (`Kim2026OATTA`, new) | Abstract only | Likelihood-ratio gate reverts to the base predictor. | Abstract only; no conclusions about its method detail. |
| **SLRF** (`Su2026SLRF`) | Crossref and Semantic Scholar metadata only | Title verified: "Shift-level regulated continual test-time adaptation framework". | **Full text still closed** (Semantic Scholar: `CLOSED`; Springer redirected to login). Remains an unresolved collision. **Please obtain it through library access if you can.** |

## 6. Remaining difference, and why it matters

Across what we read, no visual TTA paper reports a pre-action action-value predictor measured as a function of adaptation exposure, split by whether the evidence is directly optimized. **This is a statement about the passages and searches above, not a verified gap.** Two web searches on this exact angle (nine overall in this pass) returned nothing direct. That is weak evidence, because the Feynman semantic search was unavailable (`Unknown alpha command: search`) and search coverage of 2026 preprints is uneven.

It matters because source-reset evaluations are the current standard for pre-action selectors, and this would show whether their numbers carry over to continuing deployment.

## 7. What would refute A′

1. **Too little headroom:** best-fixed-to-oracle gap is negligible on live states.
2. **No decay:** predictor error does not grow with exposure.
3. **No difference by evidence type:** optimized and unoptimized evidence decay alike. This would remove the mechanism but leave a general decay finding.
4. **Trivial fix:** fitting across all exposure levels at equal budget removes the decay. Then this is ordinary coverage, and no method paper remains.
5. **Already published:** SLRF's text or a later paper reports it.
6. **Collapse only:** decay appears only in collapsed states, which ASR and AETTA already target.

**Likely counterexample (our expectation):** outcome 4 is the most probable failure. Exposure may simply be a learnable input. Even then, a clear finding that source-reset evaluation misleads may remain, but it would be a diagnostic result rather than a method, and its publishability is unknown.

## 8. Candidate B and C status

Neither was re-attacked in this pass. B partly overlaps A′, because both ask when a label-free signal stops being informative. A′ differs by focusing on signals corrupted by the update itself. C remains deferred.

## 9. Limits of this pass

- Selective reading; quotations were checked against extracted text, but two-column PDF extraction can disorder sentences.
- One search tool only; no citation-graph traversal.
- The 0.5-point figure is our arithmetic on reported means.
- Recent preprints here are unreviewed unless their records state otherwise.

## 10. Next step

Run [Experiment 003](../experiments/003-evidence-decay-under-adaptation.md) once execution is authorized. This machine has 8 CPU threads, 15 GB RAM, no `nvidia-smi`, and no PyTorch in system Python, so a CPU timing probe must come first, or a GPU machine must be named.

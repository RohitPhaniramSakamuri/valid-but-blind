# Final scientific review of the 26 October deep review

Reviewed artifact: [deep review](../../outputs/shift-aware-tta-deep-review-2026-10-26.md). Date: 26 October 2026. Role: critical review, separate from the earlier source-collection pass. No experiment, implementation test, package installation or benchmark execution was performed.

## Verdict

The artifact is an appropriately qualified literature review and proposed research program. It does **not** establish genuine novelty or conference readiness, and it says so explicitly. The original broad proposal is correctly rejected as a novelty claim. The recommended question is a plausible but still narrow and unverified intersection of existing work.

No fatal factual or novelty overclaim was found in the inspected main text. Several protocol details should be pinned before execution, especially the rich current-model baseline and the exact statistics/gradient transitions. The report's linked Experiment 002 file had not yet been saved when this review began; its existence and final contents need confirmation before handoff.

## Scientific strengths

- The review acknowledges direct whole-method selection, shift-level strategy routing and live-state scope switching, rather than manufacturing novelty by treating all TTA as a fixed strategy.
- It fairly distinguishes MORPHEUS's frozen-source observations from live-state heuristics and explicitly treats SLRF's inaccessible full text as an unresolved collision.
- It incorporates the especially close Agentic-TTT precedent, including its persistent adapter state, same-snapshot counterfactual rollouts and acknowledged gold-history/autonomous-history mismatch. Neither exposure bias nor data aggregation is represented as new.
- Current-data matching, complete-state branching, hidden target labels, causal deployment timing, support/query separation, cost accounting and local-versus-dynamic oracle distinctions are all present.
- Negative outcomes have explicit rejection rules. A current-output or cheap-reset explanation would defeat a strong new-method claim.

## Required clarifications before experimental execution

### 1. Strengthen the current-model evidence comparator

Severity: medium, scientifically consequential.

The present hierarchy names a current-model **prediction-summary** baseline, followed by current predictions plus state descriptors. This can be too weak. MORPHEUS uses feature geometry, while the proposed state descriptor may expose much richer information about the current network.

Use an equivalent rich selector over current-model logits, current feature geometry and ordered-window summaries, with the same regressor capacity, training episodes and cost treatment as the source-side counterpart. Then add parameter/buffer/optimizer/history evidence. Otherwise an improvement over a few current scalar summaries can be mistaken for evidence of hidden adaptation-state value.

### 2. Define the UPDATE and NORMALIZE interventions precisely

Severity: medium, an execution blocker until specified.

“ETA-style reliable entropy step” does not determine BatchNorm behavior. Updating BN affine parameters in training mode can also update running buffers and use support statistics; an affine-only step using frozen running statistics is a different action. NORMALIZE also needs exact layer coverage, interpolation/momentum and how multi-layer statistics are collected.

Choose and document those semantics explicitly. An atomic gradient action can freeze the running buffers, while a statistics action changes only declared buffers, or a joint action can be included under a distinct name. The aim is interpretable interventions, not accidental coupling through a library mode flag.

### 3. Include stochastic state and separate bookkeeping from learned state

Severity: medium for stochastic methods; minor for a deterministic first diagnostic.

Teacher augmentation, sampling, dropout and stochastic restoration can make identical clones differ through random-number draws. Preserve or control RNG state and use paired randomness for comparable branches, or report repeated branch randomness. “Complete state” should encompass all state that actually affects future execution.

KEEP should preserve learned state while still advancing external time and elapsed-time/update-age bookkeeping. If counters are included in the state vector, clarify which are clock variables and which affect optimization/reset schedules; otherwise “preserve state” conflicts with the proposed age features.

### 4. Guard against noisy action-ranking flips

Severity: medium.

A finite query can make the empirical best action change even if population risks are practically tied. The review already calls for paired uncertainty and meaningful margins. Operationalize this with predeclared pairwise/tie-aware rules and fresh-query replication where feasible. Never search histories for label-observed flips, then report that selected sample as their prevalence.

Report full effect distributions and non-flips, not just the most illustrative matches. A local empirical oracle is an outcome diagnostic; it is not an unbiased estimator of population-optimal action benefit.

## Main reviewer objections the proposed paper would still face

1. **Known phenomenon, known remedy.** Different parameter states responding differently is elementary; offline-to-online state mismatch and data aggregation are established. The study needs a material visual-TTA failure that remains after strong current-model evidence, sensible hyperparameters and reset controls.
2. **Small-action-menu artifact.** A selector over weak atomic actions can create a problem that a strong fixed ROID/ASR/other legal method removes. The report correctly requires stronger complete-method comparators; retain that requirement.
3. **Offline supervision.** The selector learns from labeled auxiliary query outcomes and many counterfactual action runs. “No labeled target data at deployment” is accurate; “unsupervised controller training” or “source-data-free preparation” would not be.
4. **Collection-budget advantage.** Learner-state aggregation must be compared with equally many scored outcomes, comparable refitting/search effort and broader random/fixed-policy coverage. Otherwise gain can be due to more development supervision.
5. **Generalization versus arbitrary corruption memorization.** Both prefix/history families and present shifts need holdouts; source image identities, dominant classes and relevant model/checkpoint choices need separation. The proposed splits acknowledge this.
6. **Temporal horizon mismatch.** A one-step loss predictor is myopic; a useful whole-stream controller may require delayed rewards. Report results for the objective actually trained. Do not use autonomous accuracy alone to claim optimal long-horizon control.

These are unresolved scientific burdens, not reasons to describe the candidate as already disproven. They determine what Stage 1 and subsequent stages must establish.

## Fresh citation checks during review

The following report URLs were reopened and their titles/authors checked against the relevant ledger or official primary metadata:

- [NOTE, arXiv:2208.05117](https://arxiv.org/abs/2208.05117): correct paper and six authors; linked version history is consistent with the NeurIPS 2022 work.
- [Yu et al., arXiv:2307.03133](https://arxiv.org/abs/2307.03133): correct benchmarking title and authors Yongcan Yu, Lijun Sheng, Ran He and Jian Liang.
- [GALA, arXiv:2404.03784v2](https://arxiv.org/html/2404.03784v2): correct layer-selection paper; the source/anchor-reset distinction is relevant.
- [RNA author project](https://rapid-network-adaptation.epfl.ch/): correct ICCV 2023 project and learned feedback-controller scope. Exact controller-training trajectories remain a required full-method check, as the main report states.
- [POEM, arXiv:2408.07511](https://arxiv.org/abs/2408.07511): correct protected entropy-matching paper.
- [RDumb, arXiv:2306.05401](https://arxiv.org/abs/2306.05401): correct CCC/reset baseline.
- [Zhou et al., PMLR zhou26be](https://proceedings.mlr.press/v306/zhou26be.html): verified ICML 2026 title, six authors and pages 166172–166195.
- [Garg et al., arXiv:2201.04234](https://arxiv.org/abs/2201.04234): correct ATC paper and abstract's explicit identifiability qualification.

No obvious guessed or mismatched URL was found in this bounded check. It is not a link audit of all 103 library records, and fresh abstract checks do not imply full-paper reading.

## Recommendation

Keep the main conclusion conditional. Resolve exact-overlap checks and action semantics, then begin only the specified diagnostic when execution is authorized. Do not write a result-bearing abstract from this review. If richer current-model evidence or cheap reset controls remove the effect, preserve that negative finding and reassess the research direction.

## Disposition after the lead's revisions

The revised main review and the now-saved [Experiment 002](../../experiments/002-state-conditioned-selection.md) were selectively reread. The requested rich current-model comparator, frozen-buffer affine UPDATE primitive, separate NORMALIZE transition, random-number snapshots, advancing external clock, state-pure observations, stronger collection-budget accounting and fresh-query/tie-aware checks are now explicit. The UPDATE primitive is correctly labeled as different from native ETA/Tent. The earlier missing-protocol-link concern is resolved.

The lead is additionally separating prefix identities from support, query and fresh-query identities, while allowing declared prefix repetition. That distinction is appropriate: repeated exposure in the history should not leak the current scoring examples.

One final design choice to pin is the horizon: support size 64 and frozen query size 512 span several future decision blocks if decisions recur every 64 images. Treat that as a fixed-KEEP diagnostic horizon, or use the next declared prediction block as the primary one-decision target. It should not silently become a different objective during autonomous evaluation. This is a protocol clarification, not a newly detected invalid result; no experiment has run.

The additional RNA project inspection reinforces its access qualification. Its classification examples use coarse labels or retrieval from labeled source images; geometric tasks use different feedback. The visible project “Get started” link currently resolves to an unrelated XDEnsembles repository, so it is not verified RNA implementation access. The central RNA source record does not claim that code URL. No additional scholarly record is required for this observation.

**Final disposition:** the revised literature report is suitable to deliver with its conditional novelty assessment. Exact first-in-field originality, source-compatible numerical baselines, action-estimator fidelity and empirical contribution remain unresolved. These limits are represented honestly; the review does not support a result-bearing abstract or authorize execution.

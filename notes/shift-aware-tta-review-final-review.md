# Final internal review of the synthesis

Date: 23 October 2026. Reviewed artifact: `outputs/shift-aware-tta-review.md`, as read after its initial draft. The experiment protocol was being written separately and was not available during this pass. This review does not edit the main synthesis or run experiments.

## Overall judgment

The draft is candid about the broad proposal being occupied, distinguishes proposal from results, and places the acquisition idea alongside the correct neighboring literatures. Candidate A is presented as a hypothesis rather than a verified gap. That framing is appropriate. I would not reject the investigation on novelty grounds before a diagnostic, but the described method is currently an application of familiar value-of-information ideas, not yet a demonstrated algorithmic contribution.

The cross-fitted realized-gain target is scientifically coherent for the **specified episodic support/query decision**, provided its data independence and final-fitting procedure are made explicit. It estimates the benefit of replacing a particular cheap selector with a particular rich selector. It does not estimate an intrinsic causal property of the shift or the value of every possible future observation. Those distinctions matter to the claims.

## Blocking fixes before treating this as an executable protocol

### 1. Make the fitting and validation nesting explicit

The current statement that cross-fitting prevents an overfit richer selector from appearing useful is incomplete: the acquisition gate can still overfit those out-of-fold gain targets, and tuning both selectors on the same evaluation fold defeats the protection.

Specify three levels clearly:

1. Reserve final deployment families and image identities before fitting or selecting any controller component.
2. Inside development data, generate each gate-training target using selector fits that did not use that episode or its correlated family/image group. Selector hyperparameters must be chosen without the target episode as well.
3. Fit/tune the gate on its designated training/validation data, then refit selectors on the allowed development pool and evaluate the complete frozen system on the untouched final split.

The final refitted selectors differ slightly from the fold-trained selectors used to generate gate targets. This is ordinary stacking/cross-fitting distribution mismatch, not invalidity, but it needs a gate-validation check and an explicit limitation. No final test-label choice of gate margin, lambda, probe count or action hyperparameter is permissible.

### 2. A positive observed gain is a noisy training label, not proof of episode benefit

Each `d` uses empirical losses on a finite query set and may be noisy. If near-zero gains are thresholded into a binary label, the controller could learn sampling variation. Prefer regression or a development-fixed indifference region; use query sets large enough for the diagnostic and inspect paired uncertainty. Avoid interpreting 'positive d' as a certified safe intervention. This strengthens the current no-guarantee caveat.

### 3. Explicitly freeze what each selector sees

State that cheap and rich selectors use only support observations available before the terminal action; query features cannot leak into the probe gate unless the protocol deliberately permits transductive access for every baseline. No query labels enter any runtime object. The richer selector's augmented views must be generated from the same allowed support prefix. If it uses future context, that changes latency/access and cannot be costed as an ordinary extra view.

### 4. Keep episodic and continual claims separate

The reset-to-source support/query diagnostic is valid, but is not a demonstration that a learned controller works when a long stream changes both data and model state. Episode-level action-value tables cannot be reused as if they were valid counterfactual outcomes for a different live adaptation state. Keep the headline claim episodic until a separately declared continual experiment resets/clones parameters, BN buffers, optimizer state, teachers, caches and memories consistently.

### 5. Clarify the cost-aware oracle and fixed-action baselines

For the diagnostic, each action outcome is measured from the same source state on the same support/query episode. The oracle chooses the lowest *query loss plus declared cost*, not the maximum same-batch adapted accuracy. It is analysis-only.

Distinguish a development-selected fixed method from the final-test best-fixed method. The former is deployable; the latter is a hindsight diagnostic comparator. Selection headroom should be shown against both and not exaggerated by a weak fixed baseline. Any oracle including probe information should disclose that its budget is a ceiling/diagnostic, not a feasible implementation.

## Important caveats that do not block the review

- **No first-of-kind claim:** MORPHEUS plus SA-TTS/AFA already suggests much of the proposed architecture. The paper would need a specific TTA mechanism result and more than a positive average delta after adding views.
- **CAS as an actual ablation:** it currently appears in reading/background. Implement a same-evidence similarity/uncertainty skip rule with the same available actions as an adaptation where practical; mark that conversion as an adaptation of CAS, since its native system is VLM-specific. Do not imply raw native CAS numbers are comparable to a CNN selector.
- **Fixed adaptation cost is state/data dependent:** Tent/ETA/SAR may skip or vary update work; use measured per-episode cost and latency, rather than one global method constant. Account for any cached/shared operations once, and explain reuse identically for every controller.
- **Rich-selector capacity:** hold regression family and training/tuning budget comparable between cheap and rich selectors. Check whether a larger cheap model closes the gap; otherwise representation/capacity effects can masquerade as information value.
- **Raw versus operational utility:** the linear loss-plus-cost target is one declared utility, not a guarantee for deadlines. Hard deadline results need an explicit event/arrival/scheduling rule and a late-prediction penalty; a lambda sweep cannot silently substitute for it.
- **Whole-family holdouts are small in number:** intervals over images can look falsely precise. Repeat units should reflect independent episodes/streams and folds; report family-wise results even when an aggregate improves.
- **Source preparation:** labeled auxiliary episodes and checkpoint/source-statistics preparation are allowed only when disclosed. 'Unlabeled target deployment' does not imply a fully source-data-free development process.
- **No-update is not human deferral:** selecting SOURCE returns a source prediction. It does not reject the input or obtain supervision. Use those terms consistently.
- **Budget-independent vocabulary:** a mean runtime saving on one device does not establish 'efficient' across architectures or memory limits. Tempora and BoTTA already make this a substantive evaluation issue.

## Metadata and source fixes

- BoTTA has a primary-source discrepancy: the publisher article identifies SenSys 2026, while the older arXiv v2 report-number field states SenSys 2025. The publisher version can be the main citation; retain the discrepancy in provenance rather than silently merging metadata.
- FORGE's arXiv record states TMLR 2026; independent acceptance verification was not completed here. CAS's arXiv record states ECCV 2026. Use those as author-reported venue statuses unless proceedings/acceptance is separately checked.
- The request for a 'FAR video selective' comparison was ambiguous and no reliable primary match was established; do not add a guessed citation. Existing CAS, SEGA and SA-TTS already cover the necessary acquisition/selection neighbors.

## Concrete falsification criterion

Before learning a purchase policy, require a meaningful held-out gain of the always-rich selector over cheap-only using a shared action menu and matched fitting budget. Then require the learned purchase rule to beat random, fixed-schedule and uncertainty purchase at equal total compute. If either step fails, the correct conclusion is that this evidence/action menu does not support the proposed acquisition mechanism, even if post-hoc oracle action diversity exists.

## Recommendation

Complete the protocol with the five blocking clarifications, then perform the small action-headroom diagnostic only after the user authorizes an execution environment and experiment. The literature review is suitable as a map and candidate proposal; it should not be represented as establishing an open gap or a successful method.

# Final adversarial verification of the synthesis

Date: 23 October 2026. Reviewed artifact: `outputs/shift-aware-tta-review.md`. Role: verifier. No experiments or implementation tests run. The experiment-plan file linked by the review was not yet present when this pass started; the items below must also be reflected in that plan.

## Overall judgment

The review's main positioning is supported: the broad proposal has close precedents, the residual acquisition question is labeled a candidate intersection, and existing result claims are correctly removed. Source-free deployment is separated from offline supervision, while transductive/online information budgets and cost matter. No first-in-field assertion or universal safety theorem is warranted, and the draft explicitly recognizes that.

The direct collisions most important to preserve are MORPHEUS, Jhawar2026Identifiability, SA-TTS, CAS, SEGA and FORGE. Tempora already makes operational cost alter method rankings. GALA and ASR prevent an overly broad current-state/reset novelty claim. Source metadata spot checks confirmed the IDs for GALA (AAAI 2025; arXiv v2 dated February 2025), CAS (arXiv September 2026, comments ECCV 2026), FORGE (arXiv September 2026, claims TMLR publication), SEGA (August 2026 preprint under review), and MoASE++ (May 2026 preprint). These checks do not independently certify all claimed proceedings acceptances.

## Corrections required before freezing the protocol

### 1. Make the acquisition equation account for the complete route

The current equation uses `c` defined as adaptation cost and `c_q` as observation acquisition cost. This omits differences between the cheap and rich selectors themselves and can omit extra feature/augmentation preprocessing. Replace those definitions with complete incremental route costs, for example:

`d = [L(g0) + lambda * C0] - [L(g1) + lambda * (C1 + Cq)]`.

Here `C0` includes cheap-selector inference, the selected adaptation and prediction; `C1` includes rich-selector inference, its selected adaptation and prediction; `Cq` includes all extra views, preprocessing, transfers and new feature calculations. Shared source-pass/support-processing costs can cancel **only in this within-episode contrast**. They remain part of all-in deployment cost when comparing the method to SOURCE or a fixed-action baseline that does not need the same support pass. Gate evaluation itself must also appear in reported deployment timing.

An equivalent expression is fine; no need to charge a source pass twice or to count cheap features as an extra forward when they are obtained from an existing pass.

### 2. Specify query normalization and state semantics

The proposed diagnostic adapts on support and scores a subsequent disjoint query batch. Native normalization-based implementations may use the query batch's statistics even without a gradient update. That is additional query-time adaptation/transduction, not automatically a fixed support-only predictor. Before execution, choose one consistent declared protocol:

- Freeze all adapted parameters and mutable buffers after support, then use fixed normalization statistics on query. A Tent implementation may require a clearly named support-conditioned variant; do not silently present altered normalization behavior as an exact native reproduction.
- Or allow a named query-time normalization operation for the applicable methods, disclose the extra information access and cost, and use that same definition during offline outcome generation and final evaluation.

All counterfactual actions must begin from the same source snapshot in this episodic diagnostic. Reset weights, running statistics, optimizer moments, counters and stochastic state as relevant. The current-state branch requires an explicitly separate live-state protocol.

### 3. Nest selector cross-fitting, gate training and calibration

Out-of-fold `g0/g1` targets avoid one overfitting route, but the complete training graph must also prevent gate or threshold leakage. Define outer final-test image/family groups untouched throughout development. Inside development, construct out-of-fold selector predictions and realized query losses for training the gate. Fit gate hyperparameters and acquisition thresholds/cost settings on separate grouped validation episodes or through a nested fold process. Refit final selectors only on allowed development groups, and evaluate the whole gate/selector pipeline once on final hidden-label groups.

Offline oracle action gains are useful upper bounds; they must not replace the realized gains of `g0/g1` when teaching the gate unless that change is explicitly a separate oracle-supervised baseline. The draft uses the appropriate realized-selection target and should retain it.

### 4. Avoid implied formal harm control

The phrase “controlled harmful adaptation relative to SOURCE” in §6 can be read as a guarantee. Use “lower measured harmful-adaptation rate relative to SOURCE” or specify the empirical metric. The development-calibrated trigger is explicitly not guaranteed under arbitrary unseen shifts, so the outcome wording should match.

## Important nonblocking clarifications

- The order-aware selector baseline must receive only temporal context available under the chosen episode protocol. A whole-target summary cannot be imported into a causal support-prefix experiment as a same-information baseline. Mark architecture-inspired adaptations of published selectors clearly.
- For an initial single acquisition decision, call this a one-step evidence-purchase controller. A general sequential acquisition policy is a later extension and has established feature-acquisition antecedents.
- Compare query support distribution relations explicitly: stable-within-episode shift for the first diagnostic; abrupt changes between support and query are a separate stress case. Otherwise selector failure and support representativeness become conflated.
- Match “no update” precisely: frozen SOURCE is different from KEEP of an already adapted model. The episodic main experiment currently uses SOURCE consistently; preserve this distinction when moving to continual experiments.
- The review properly qualifies SLRF to abstract-level evidence and MORPHEUS as a workshop paper. Keep access/read-scope limits in the bibliography and source index.
- Use the published Cygert2026 title in the main bibliography, linking the differently titled 2024 preprint. Use the May 2026 Tempora version/official ICML record when describing its expanded evaluation scope.

## Result

No additional literature-based blocker was identified in this pass. The four protocol/wording corrections above are required for a reviewable empirical proposal. They do not certify novelty or predict successful experiments. The candidate should still be abandoned or reframed if there is little best-action headroom, richer evidence fails out of family, or equal-cost random/simple uncertainty acquisition matches the learned gate.

## Resolution check

The revised main review and newly written `experiments/001-policy-selection-pilot.md` were reread on 23 October 2026. All four requested corrections are incorporated: the target uses full route costs `C0/C1`; common costs remain charged against SOURCE; nested grouped selector/gate/validation stages and final hidden labels are specified; and harm is described empirically. The plan explicitly distinguishes native Tent, a support-update/query-normalization wrapper and a fixed-support-statistics variant, prohibiting query gradients and unintended persistent buffer mutation. Final normalization semantics remain an implementation choice to freeze and record before running, not an unacknowledged equivalence claim.

No remaining blocking error was identified in this reread. Source/development-image provenance, finite-query gain noise, selector-refit mismatch, oracle costs, and the separate continual-state extension are also recorded. This is document-level verification only; no implementation or experiment has been tested, and novelty remains unresolved.

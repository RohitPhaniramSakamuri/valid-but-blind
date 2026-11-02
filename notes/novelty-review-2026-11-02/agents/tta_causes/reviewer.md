# Independent critical review of the root synthesis

Date: 2026-11-02. Reviewed `../../review.md` as present before the final three-query audit was appended. No experiments, model runs, or tests performed. This review checks interpretation and evidence scope; it is not independent reproduction of the underlying experiments.

## Overall assessment

The five verdicts are separated and use exactly one allowed verdict per claim in the opening table. The synthesis correctly treats the experiment record's mechanism/authors-pipeline outcome as pending. It preserves the failed cross-model confidence hypothesis, identifies the conditional-on-violation denominator problem, and does not present missed alarms as a theorem violation. Its recommendation is appropriately narrower than a general new failure mechanism or universal independent-alarm claim.

I do **not** find a decisive unacknowledged source establishing the exact complete C1 or C2 comparison. However, their apparent residual is much narrower than a reader might infer from the first finding alone. The combined evidence from Schirmer's own §5.4, AETTA, Cygert and Han makes a confidence-monitor failure under entropy adaptation unsurprising. The report should be read as “this particular consequential measurement was not located,” not “a reviewer should consider the idea original.” The draft already says this explicitly; preserve that language.

## C1: material distinctions versus obvious specialization

The main material distinction is **not** CIFAR100-C instead of another dataset, Dirichlet instead of another sampler, or six models instead of one. Those are empirical scope changes. The material question is whether Schirmer's *adaptation-aware, source-recalibrated, one-sided risk monitor* loses power relative to its frozen counterpart on matched external draws despite conditions under which users might expect its proxy to remain useful. AETTA and Cygert do not evaluate this monitor; Han has revealed outcomes and a different score process. Therefore their results do not directly entail the measured 147/166 versus44/110 gap.

Against that distinction, Schirmer's own missed alarms and prototype-distance repair sharply weaken originality. A reviewer can plausibly regard the new result as an expected stress test of a known limitation, even if the precise comparison is absent. The draft's request for a source/target error-separation explanation and a useful remedy is justified. Do not strengthen “No report found” into a contribution claim without explaining this point.

The Cygert qualification is now correct. Fig6 is corrupted CIFAR100-C with temporally correlated class exposure and δ∈{10,1,.1,.01}, not proof of the same persistent global prior. Fig6 panels show SAR/EATA/AdaContrast, not Tent. The draft explicitly says both. Alpha/delta equality does not match label support, class dwell time, population marginal or image replacement. No correction needed here.

The local term “noncollapsed” needs to remain operational. A last-quarter error cutoff does not demonstrate multi-class prediction support or lack of representation collapse. Dirichlet's positive population probabilities also do not guarantee every class appears in a finite stream. The draft's operational-collapse warning is correct; avoid shortening it away in later summaries.

## C2: precise claim, no established local result

The pending-record treatment is necessary and correct. A literature absence verdict cannot validate the claimed factorial result. A matched-accuracy BN-only predecessor for conformal coverage could anticipate the causal logic without containing sequential monitoring or label-prior skew; its blocked full text prevents either dismissing or equating it with C2.

Fixing the threshold is a good confound check but makes pure confidence scaling an even more obvious source of missed alarms. The more substantive contrast would be the entropy step versus BN-only under the same monitor, matched risk margins and stated update semantics. A failure of the BN-only prespecified criterion is lack of demonstrated sufficiency, not evidence that BN has no causal role. The draft handles this distinction correctly.

## C3 and AETTA measurement precision

Suggested small clarification: AETTA Fig2's plotted confidence is that of its dropout hypothesis expectation function `h_tilde`, discussed in §3.2, rather than necessarily the same maximum-softmax score used in the local Schirmer port. Its main Fig4 and Table2 additionally evaluate the raw SoftmaxScore estimator and show severe errors under failing Tent/EATA. The qualitative confidence/error-decoupling claim is supported, but a sentence saying AETTA measures the *same confidence signal* would be inaccurate. The current draft does not make that stronger statement; adding this distinction would improve precision.

The draft correctly separates probability calibration from error separation. A common monotone transformation can preserve threshold events after source recalibration; average confidence and ECE alone therefore do not establish the source of Schirmer's power loss. Preserve the failed cross-model confidence prediction in any final summary of C3. The proposed joint-mass decomposition is more specific than the generic over-certainty story, and is explicitly labelled as an interpretation/algebraic reading rather than a theorem contribution.

## C4 and C5

“Already published” is defensible for C4's existence claim. It is not a universal theorem about every confidence-derived monitor. The draft explicitly removes the unsupported universal quantifier and distinguishes threshold/reference adaptation, model updates and adaptive-process-control residual masking. This is scientifically important and should not be compressed into one allegedly common guarantee.

C5 is correctly “Partially covered”: there are many existing ways to form label-free signals, and some already trigger resets/abstention. None inspected proves the desired sequential sensitivity for this exact failure. Do not imply that an adapted-model perturbation score is independent merely because it differs from entropy, or that a frozen sentinel can detect learning-induced harm by itself. The draft's warnings cover both.

## Five reviewer objections and recommendation

1. **False alarms versus power:** answered candidly. The draft cites Schirmer's existing failure discussion, not just generic confidence-sequence conservatism.
2. **Known over-certainty:** answered with the right separation between a predictable broad mechanism and an unproven specific calibration/power effect.
3. **Artificial or already studied skew:** answered. The report does not credit Dirichlet0.1 or combined corruption/skew as a new setting and requests an externally motivated regime before deployment claims.
4. **Unfair source comparison:** answered substantially. Paired external draws rebut “different streams,” while different strict-violation subsets remain a real issue. Shared violations and excess-error bands reduce the concern without establishing causal identification or independent replicates.
5. **Newer TTA solves it:** appropriately unresolved. Published calibration/accuracy improvements are not monitor-power results. The wording “recent work still reports confident errors despite stronger methods” is acceptable only with the stated task/scope boundaries; do not generalize the open-set results or medical binary ROC-AUC results into proof all current methods fail at C1. The draft avoids that stronger claim.

The workshop-style recommendation is conditional on the pending controls and implementation comparison, and is not an acceptance forecast. It also supplies explicit stopping criteria. This is a candid assessment. The order is sensible: implementation fidelity and a mechanistic error-mass explanation are more valuable initially than multiplying near-identical CIFAR runs. The report correctly treats current-method and cross-dataset additions as scope checks rather than automatic originality.

## Remaining documentation weaknesses to resolve before final delivery

- The final audit placeholder must be replaced with the actual three search families, dated result disposition and whether they changed any verdict. Three empty searches are not citation saturation.
- Ensure all central citation keys for the six additions from this arm match the `metadata.json` and canonical bibliography. In particular, COME's local full text is arXivv1 under review, whereas its publication header/title was checked from indexed official ICLR2025 PDF; do not label the saved old text as the final published version.
- Keep root/agent reading scopes distinct. The large number of title-only POEM/S2 or venue-list rows must never be presented as that many full-paper reads.
- Complete absence findings remain limited by blocked Mahdiani/TRUST-ADAPT and uninspected direct citers. The report appropriately acknowledges that the requested global citation saturation was not achieved. The final response should say so plainly rather than calling the review exhaustive.

No blocking scientific misrepresentation identified in the current synthesis. The optional AETTA score clarification above is the main precision improvement from this reviewer pass. The exact C1/C2 differences remain materially testable but potentially incremental; no source-search result here establishes their publishable originality.

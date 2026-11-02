# Researcher track: closest prior art and a fresh decision question

Date: 26 October 2026. This is a fresh primary-source overlap investigation, not an extension that assumes the previous gate or acquisition proposal should survive. No model experiment, test, installation or benchmark reproduction was performed. The [source ledger](researcher-sources.json) has 20 freshly checked records, including 12 keys absent from the inherited catalog. Reading depth varies explicitly by record.

## Assessment

The broad abstract overlaps existing work. Three particularly direct collisions are [SLRF](https://link.springer.com/article/10.1007/s10618-026-01222-x), which chooses adaptation strategies after shift-level detection; [MORPHEUS](https://theyoungkwon.github.io/papers/articles/danilowski_morpheus_iclr-ttu26.pdf), which predicts whole-method performance before executing adaptation; and [AdaTent++](https://www.frontiersin.org/journals/signal-processing/articles/10.3389/frsip.2026.1842851/full), which routes among statistics updates, gradient updates and skipping. These records were independently reopened today. MORPHEUS is explicitly a TTU workshop paper, rather than verified ICLR main track. SLRF's full method remains subscription-only: its abstract establishes broad overlap but cannot establish or exclude exact overlap of a narrower proposal.

The original premise that TTA generally applies a single strategy without conditioning on deployment signals is not a defensible literature claim. Physical shift causes also need not be identifiable from a marginal feature displacement or prediction distribution.

## Existing ingredients that cannot be the main novelty

| Ingredient | Close primary predecessor | Consequence |
| --- | --- | --- |
| Source predictions/geometry predict which full TTA method to use | MORPHEUS, §2 | A lightweight meta-regressor or classifier over adaptation actions is established. |
| Prior/stream/batch-size ambiguity can reverse the best action | [Jhawar and Wang](https://arxiv.org/html/2609.11235v1), §§3–5 | Adding a KEEP action, temporal summaries, or an evidence-insufficiency argument is established. |
| Teacher/student history drives selection of update scope | [Hybrid-TTA](https://arxiv.org/html/2409.08566v2), §4.1 | Current model state and history already enter visual adaptation control. |
| Source/current disagreement controls recovery and update intensity | [ASR](https://arxiv.org/html/2603.03796v1), §3.5 | That disagreement statistic is not a new descriptor. |
| Accumulated gradients/displacements select layers or skip | [GALA](https://arxiv.org/html/2404.03784), §§2.2–2.3 | State-dependent layer selection and trajectory resets already exist. |
| Class mixture changes corrupt normalization | [Channel-selective normalization](https://proceedings.mlr.press/v274/vianna25a.html), [DELTA](https://arxiv.org/abs/2301.13018), [TRIBE](https://ojs.aaai.org/index.php/AAAI/article/view/29435) | A new study needs these controls; comparison only with always-normalize is inadequate. |
| Predicted class composition conditions adaptation/refinement | [Label Shift Adapter](https://arxiv.org/abs/2308.08810), [DART](https://arxiv.org/abs/2411.15204) | Estimating priors and conditioning on them is established. |
| Distinguish reducible and irreducible uncertainty | [EATA-C](https://arxiv.org/abs/2403.11491) | A generic “uncertainty versus repairability” explanation is insufficient. |
| Per-condition harm can be hidden by aggregate accuracy | [Majumdar and Saha](https://arxiv.org/abs/2608.22233) | A CIFAR-C help/harm table alone would be weak novelty. |
| Decision rules for steps and update subspace | [Wakayama](https://proceedings.mlr.press/v306/wakayama26a.html) | A decision-theoretic framing needs a concrete result beyond this literature. |
| Recovery-time/temporal-dependence theory | [Zhou et al.](https://arxiv.org/abs/2605.28057) | “First theory of nonstationary TTA” is unavailable. |
| Attribute interventions at inference | [FACTOR](https://arxiv.org/abs/2605.03294) | Counterfactual input perturbations themselves are known. |

The entry for TRIBE should use its **AAAI 2024** publication, linked to the 2023 preprint; later arXiv revisions do not make it a new 2025 method. EATA-C extends EATA and should be linked to it rather than conflated with the original ICML 2022 loss.

## Strong adjacent control precedent: Agentic-TTT

[Agentic-TTT](https://arxiv.org/html/2610.12002v1), submitted 8 October 2026, already learns whether to adapt, which TTT algorithm to call and which stored adapter to reuse. Its policy conditions on persistent state; training compares trajectories from the same snapshot. Adapters can be warm-started and updated, even though the backbone stays frozen. Thus learned state-conditioned control and counterfactual utility training are established principles.

Its Appendix E explicitly acknowledges that training state histories follow annotated gold actions whereas deployment follows policy decisions, and leaves autonomous-stream credit assignment to future work. This supplies a concrete limitation to investigate; it does not establish an untouched general problem.

## Best remaining candidate intersection

**Question:** On a visual deployment stream, can a selector distinguish a change in the current inputs from a change in the model's ability to adapt caused by its own earlier updates, and remain useful on the states created by its own decisions?

This should be framed around a controlled effect and a measurable failure, not “first state-aware TTA.” The possible contribution has two connected parts:

1. Isolate action-ranking changes caused by adaptation state while holding the present support and query images fixed.
2. Measure and correct the gap between a selector evaluated on externally generated histories and the same selector run autonomously through a full stream.

The inspected MORPHEUS setup starts with a source model. Jhawar and Wang §4.1 explicitly start every action from the same frozen source state per deployment world; their controlled intervention changes whole-stream organization. That does not establish the proposed matched-present-data state study, but it is close conceptual prior art. Hybrid-TTA and ASR already react to evolving state; Agentic-TTT already exposes the training/deployment state mismatch. The exact visual mechanism/evaluation intersection remains **unverified**, particularly until SLRF's full method and more sequential selection literature are available.

## Minimal falsifiable study to decide whether to pursue it

Construct a fixed current support/query pair from a held-out shift. Reach it through independently specified histories that differ in corruption, class mixture and adaptation actions. Start histories from a common source checkpoint. At the matched decision, clone the entire live state, including parameters, normalization buffers, optimizer, teacher and memory when applicable. Execute the same legal action menu on each clone and evaluate on the same disjoint query. Labels score outcomes offline and never reach the deployed selector.

Do not choose matched histories because their labels reveal opposite rankings. Specify histories and query identities first, preserve non-flips and ties, and repeat across source seeds, models, held-out history families and current shifts. If the action menu cannot be transferred meaningfully between states, simplify to explicit atomic operations rather than silently discarding method-specific state.

Three success conditions would be needed before developing a large controller:

- A material fraction of robust ranking reversals at identical present images, beyond finite-query uncertainty and a single collapse pathology.
- A state-conditioned predictor improves on strong source-only and order-aware selectors, ASR/Hybrid-style heuristics and development-selected fixed actions under the same information/cost budget.
- The improvement survives closed-loop deployment, including state trajectories absent from training. An offline-only improvement does not answer this question.

For a proposed correction, collect auxiliary-development states from several fixed policies and from successive frozen versions of the learned policy. At each saved state, score cloned candidate actions on separate development queries. Refit only from development outcomes; hold the final shifts, source images and histories untouched. This resembles established on-policy data aggregation rather than a new general learning principle. Its contribution would have to be the demonstrated TTA failure mechanism, a useful state representation or estimator, and robust unseen-stream results.

A one-step oracle and a full-horizon oracle answer different questions. Report both only when their definitions and costs are explicit; do not call a myopic selector optimal over a stream. KEEP-LIVE, ANSWER-WITH-SOURCE and RESET-STATE are also different operations and need separate semantics.

## Remaining limitations of this track

Searches included whole-method selection, dynamic tuning, layer/step selection, prior-aware normalization, counterfactual evidence, reset/recovery and state-aware meta-control. Searches found many secondary aggregators; claims above use primary papers, proceedings, author PDFs or author code. Some OpenReview/CVF pages returned browser challenges or 403, and one PMLR PDF returned an unsupported content type. Corresponding ledger scopes are narrow; indexed primary snippets do not count as full-paper reading. No search absence is evidence of exhaustive novelty.

No claimed benchmark improvement, conference readiness, universal safety or causal shift identification follows from these findings. The main empirical protocol is still planned.

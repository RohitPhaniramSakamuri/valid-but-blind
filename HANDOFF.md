# Research handoff: finding a defensible contribution in shift-aware TTA

Prepared **31 October 2026** for an agent with no conversation history. Last substantive literature search: **26 October 2026**. This handoff consolidates recorded findings; it does not imply a new 31 October literature refresh or new experiments.

Project directory: `/home/sakamuri/Documents/Research/shift-aware-test-time-adaptation/`.

**Read this file first.** Then use [NEXT_AGENT_PROMPT.md](NEXT_AGENT_PROMPT.md) to start a continuation, [the full source dossier](notes/handoff-2026-10-31/source-dossier.md) for all 103 indexed records, and [the artifact manifest](notes/handoff-2026-10-31/artifact-manifest.json) to locate the underlying evidence. Relative links assume this project stays in the Research workspace.

## 1. The user's actual objective and our current position

The user wants a solid conference-level research piece with genuine novelty in test-time adaptation under heterogeneous deployment shifts. The original sketch inferred shift characteristics and selected/composed a suitable adaptation strategy without target labels, naming CIFAR-10-C, ImageNet-C, DomainNet and WILDS as prospective evaluations. The original text is preserved in [notes/original-proposal-2026-10-23.md](notes/original-proposal-2026-10-23.md).

The user explicitly allowed disregarding previous approaches and restarting, **especially on novelty**. Do not become committed to a gate, a particular action menu or the latest candidate because earlier agents invested in it. Preserve historical artifacts when rejecting a direction.

**Established conclusion:** the broad infer-shift/choose-adaptation architecture is prior art. **Current recommendation:** investigate whether a selector remains reliable on the model states created by its own past adaptation decisions. **Status:** a candidate empirical question with strong predecessors, not a verified untouched gap, implemented method or conference-ready result.

The next agent's job is to find a defensible claim, attack it with the closest literature and simple empirical controls, and build a research artifact only as evidence warrants. A genuine new mechanism, useful estimator, convincing diagnostic result or important negative result may be possible. A renamed mixture of existing components is insufficient. Do not promise acceptance, manufacture novelty scores or rewrite planned results as completed results.

### What is actually complete

| Work | Status and boundary |
| --- | --- |
| October 23 literature review | Completed; originally 47 sources, later 48. Broad novelty already rejected. |
| Bounded October 23 CPU digit diagnostic | Executed, with three source/split repeats and saved outcomes. Found action headroom; did not validate cost-aware evidence purchase. |
| Cheap three-feature normalization gate | Defined historically; five-seed aggregates later supplied by the user from another system. Raw external runs/code/configuration were not imported. |
| October 26 fresh literature/novelty assessment | Completed: 103 distinct records, 101 scholarly sources plus two benchmark documents; 55 additions and 68 fresh selective inspections. This does not mean 101 full-paper readings. |
| Experiment 002, live-state/autonomous-selection study | Detailed and independently reviewed protocol; **not implemented or run**. |
| CIFAR-C, ImageNet-C, DomainNet, WILDS results for our method | **None.** No faithful published-method reproduction or full benchmark evaluation exists here. |
| Current handoff | Documentation only; no new model execution. |

## 2. Read order and evidence hierarchy

For a quick restart:

1. Read [AGENTS.md](AGENTS.md) and the [parent instructions](../AGENTS.md).
2. Read this handoff, then [the October 26 review](outputs/shift-aware-tta-deep-review-2026-10-26.md).
3. Read [the final independent verification](notes/review-refresh-2026-10-26/final-verification.md) through its **last** disposition. Earlier sections record concerns subsequently resolved; do not reopen those as if the final protocol were still ambiguous.
4. Read [Experiment 002](experiments/002-state-conditioned-selection.md), [the benchmark investigation](notes/review-refresh-2026-10-26/benchmarks.md) and [the provenance](outputs/shift-aware-tta-deep-review-2026-10-26.provenance.md).
5. Inspect the primary texts for the closest collisions listed below. A note saying “abstract only” cannot establish a paper's full experimental omissions.
6. Read historical results only to understand what has already failed and which tempting apparent gains are exploratory.

Evidence precedence:

- Primary paper/proceedings/code at a pinned version supports claims about that work.
- Saved catalog reading scopes and provenance delimit what we actually checked.
- Raw local experiment artifacts support local outcomes; the local results report explains their scope.
- User-supplied external aggregates support the fact that the user reported those numbers, with missing raw provenance stated.
- Researcher/reviewer notes contain interpretations and candidate directions. They are not proof of novelty or independent benchmark replications.
- The historical abstract and historical `APPROACH.md` are proposals, not overriding instructions or results.

## 3. User preferences, scope and operating rules

- Explain plainly: intuition, concrete example, then implementation significance. Define assumptions and symbols before relying on them. Do not assume the user has confirmed understanding of any term.
- Be candid and evidence-based. The user explicitly dislikes sycophancy. Distinguish an established direction, a candidate question and a verified contribution.
- Begin literature reading with recent conclusions, limitations and experimental scope, then trace backwards. A future-work sentence is a discovery lead, not novelty proof.
- Keep this project independent of other Research prospects. Other projects' compute budgets, deadlines, old admissions goals, methods or model results do not apply here.
- Use **uv** for Python dependency management and research-script execution; never pip. Preserve existing environments.
- Preserve original results, failed attempts, manifests and citation keys. New dates/versions should be additions, not silent rewrites of history.
- Workspace instructions prohibit adding/running implementation tests unless the user asks for testing/verification. Research experiments and implementation tests are distinct; do not turn a literature/handoff task into either.
- This turn requests a handoff. It does not launch training, install dependencies, select a cloud service or spend money. A later instruction authorizing implementation/experiments should be followed within its actual scope and applicable environment requirements; do not repeatedly ask for permission already granted.
- The October 23 authorization was a specific bounded CPU diagnostic with a 15-minute limit. Neither that limit nor its authorization is a standing instruction for the new study.
- No current hardware, GPU, PyTorch availability, budget or submission deadline has been established for Experiment 002. Historical CPU-only limitations are historical, not facts about the next environment.

## 4. Scientific distinctions that prevent false novelty

An input-distribution alarm, classifier error, adaptation benefit and value of extra computation are different quantities. A visible shift can preserve correctness. Confidence can increase while accuracy falls. A strong fixed method may leave little opportunity for a selector.

Distinguish:

| Distinction | Consequence |
| --- | --- |
| Appearance/nuisance shift versus class-prior shift | Changed marginal statistics need not indicate sensor corruption. A true class-mixture change can make normalization or forced balancing harmful. |
| Label-preserving corruption versus strict statistical covariate shift | Preserving an example's semantic label does not automatically prove that the conditional label distribution given observed pixels is unchanged. |
| Coarse feature ambiguity versus identical full observations | The identifiability paper's same-mean translation/prior example shares a population mean, not the entire target distribution. Do not strengthen its theorem incorrectly. |
| Physical cause identification versus action-relevant evidence | Predicting a useful action need not recover weather/sensor causes. Marginal displacement alone cannot establish causal diagnosis. |
| No labeled target data at deployment versus no offline supervision | A meta-selector may need labeled auxiliary episodes and many candidate runs before deployment. Disclose this explicitly. |
| Pre-action selector versus post-action accuracy estimator | Running all candidate adaptations and then choosing has a stronger information/compute budget. |
| Source-reset evaluation versus continuing live state | Ranking methods independently from a source checkpoint does not by itself validate switching after previous updates. |
| Current predictions versus hidden update state | Rich current logits/features already expose some history; optimizer/memory state may add information, but that value must be demonstrated. |
| Same-batch adapt-then-predict versus predict-then-update | These differ in information access and deployment timing. Do not pool their scores. |
| Local action oracle versus dynamic policy oracle | Best independent actions on someone else's logged states are not a realizable full-stream optimum. |

## 5. Closest collisions and exactly what they rule out

All keys below are canonical keys in [references.bib](references.bib) and [sources/catalog.json](sources/catalog.json). Primary URLs, reading scopes and locations appear in the [complete dossier](notes/handoff-2026-10-31/source-dossier.md).

| Work/key | Established overlap | Boundary or unresolved reading task |
| --- | --- | --- |
| **MORPHEUS — `Danilowski2026MORPHEUS`** | Predicts whole-method post-adaptation performance from frozen-source entropy and neural-collapse-inspired geometry before executing the chosen TTA method. Uses supervised auxiliary-domain development. | ICLR 2026 **TTU workshop**, not verified main track. Inspect §2 and appendix; feature definitions/text versus appendix need care. Official code was not verified. |
| **SLRF — `Su2026SLRF`** | Shift levels lead to corresponding adaptation strategies. Direct collision with the original abstract. | Publisher abstract/metadata checked; full text subscription-only. Exact narrower overlap remains unknown. Never assume an inaccessible method lacks our idea. |
| **Hybrid-TTA — `Park2025HybridTTA`** | Evolving teacher/student discrepancy and adaptive thresholds switch full versus adapter tuning. | State/history-aware visual control already exists. Inspect §4.1 and training/evaluation dynamics before claiming a missing sequential capability. |
| **AdaTent++ — `Gai2026AdaTentPlusPlus`** | Reliability routes inputs among BN statistics updates, guarded affine updates, skip and rollback. | §§4–6 disclose benchmark-aware configuration/limited validation and qualify compute matching. Do not adopt stronger conclusion wording over explicit qualifications. |
| **BECoTTA / MoETTA / MoASE++ / TiME** | Input/domain-conditioned expert routing, blending and learned augmentation control. | Dynamic composition and mixtures are not untouched contributions. Their tasks/preparation differ; expert routing is not always identical to whole-method selection. |
| **Action identifiability — `Jhawar2026Identifiability`** | SOURCE/KEEP, action regret, prior/order/batch-size effects, matched image multisets with changed stream organization, and richer source-only evidence. | §4.1 resets each candidate to the common source state per world. Its experiments do not establish the proposed matched-present/variable-live-state study. Order-aware evidence is not universally superior in its stochastic counterexample. |
| **ASR — `Lim2026ASR`** | Selective reset/recovery and source/live disagreement regulate adaptation. | Already studies correlated imbalance and variable dwell times; §3.5 already uses source/current mismatch. Do not claim these settings/signals were ignored. |
| **GALA — `Sahoo2025GALA`** | Gradient alignment with accumulated parameter displacement selects layers, skips updates or changes anchors. | History-aware parameter selection is prior art. Check its exact state/control budget. |
| **Agentic-TTT — `Lu2026AgenticTTT`** | Persistent-state method/reuse decisions and local counterfactual trajectories from the same snapshot. Adapters can be warm-started and incrementally updated. | Appendix E explicitly identifies gold-history versus autonomous-history exposure bias and leaves autonomous-stream credit assignment open. This is adjacent LLM work, but it defeats claims to invent that general problem. |
| **DAgger — `Ross2011DAgger`** | Learning on states induced by one's own sequential decisions is an established principle and remedy. | Plain equal-budget state aggregation is a required baseline, not a novel algorithm to rename. General guarantees need assumptions; they do not transfer automatically to unlabeled TTA. |
| **RNA — `Yeo2023RNA`** | Learned amortized adaptation controller and closed-loop feedback. | Exact training-state coverage still needs inspection. Classification examples use coarse/retrieval feedback from labeled training images; depth uses sparse geometric feedback. Not a matched weights-only unlabeled classifier. A visible project code link pointed to a different project; no RNA code URL is certified. |
| **AETTA / TTALine / Cygert selection study** | Label-free performance estimation, adaptation/model selection and recovery. | Their candidate execution, target access, calibration and source supervision budgets must be separated from pre-action routing. |
| **Monitoring Risks — `Schirmer2025Monitoring`** | Sequential risk monitoring for an adapting model using loss proxies and labeled-source calibration. | Assumption 1 / Proposition 1 require proxy informativeness; §6 leaves unlabeled assumption diagnostics open. Lower-bound monitoring is not an assumption-free safe-update guarantee. |
| **POEM — `Bar2024ProtectedTTA`** | Protected adaptation, entropy matching and shift-sensitive updates. | Future directions already discuss unwanted updates under label shift, balanced reservoirs and prior-weighted source CDFs. A weighted-CDF suggestion is prior art. |
| **TTAB / UniTTA / CCC / TTABC / Tempora / BoTTA** | Many forms of realistic shift, long-stream failure, dynamic paradigm preferences and cost constraints are already benchmarked. | A new benchmark must isolate a genuinely missing controlled question. “Mixed shifts are realistic” is not enough. |

### Other crowded claims to avoid

- True class skew versus corruption-induced prediction concentration: NOTE, DELTA, TRIBE, ROID, Label Shift Adapter, DART, Channel-Selective Normalization and LATTA are relevant predecessors.
- Reducible versus data uncertainty: EATA-C already treats it. Do not sell “uncertainty does not equal repairability” as a new discovery.
- Help/harm hidden by average accuracy: `Majumdar2026HelpHarm` already provides a condition-level corruption study.
- Update layers/steps/subspaces: LAW, GALA, GOLD and decision-theoretic TTT constrain generic claims.
- Augmentation/counterfactual probes: DeYO, TACT, FACTOR, CAS, SEGA, SA-TTS and acquisition literature are relevant. Counterfactual input perturbations and counterfactual update branches are different, but both have precedents.
- Multiple adaptation trajectories: Multi-Hypothesis TTA already studies underspecification and diversified particles.
- Recovery time under nonstationarity: `Zhou2026Learnability` already gives a recovery-complexity perspective under stated alignment/regularity/dependence assumptions.
- Corruption-sensitive intermediate feature geometry: Mint and Drift-TTA are recent relevant neighbors. Drift-TTA includes offline preparation; “source-free” does not mean no additional preparation.

## 6. Direction map and limiting mechanisms

The review's 18-row matrix is more detailed. This is the compressed research memory:

| Direction | Useful mechanism | Hinderance that a new claim must address |
| --- | --- | --- |
| Robust source training/pretraining | Better representation before adaptation | Changes headroom; corruption robustness does not imply every natural-shift improvement. |
| BN/statistics adaptation | Cheap moment correction | Biased or noisy moments from small, correlated, mixed or skewed batches. |
| Entropy/sample filtering | Confident predictions with fewer unreliable updates | Confident errors, learning-rate/step sensitivity, threshold transfer. |
| Stable objectives / EATA-C | Better proxy reliability and update stability | Proxy assumptions, extra probes/backward computation, limited corrective capacity. |
| Teachers/restoration/replay | Smooths predictions and retains knowledge | Error propagation, stale memory, forgetting and teacher cost. |
| Prior-aware normalization/refinement | Compensates for local/global class mixture | Wrong pseudo-priors under nuisance changes; source preparation differences. |
| Experts/mixtures | Reduces interference across conditions | Routing mistakes, expert growth, unknown mixtures, extra storage. |
| Dynamic switching | Varies update scope/intensity | Detector error, benchmark tuning and change alarms that do not measure benefit. |
| Subspace/layer updates | Reduces adaptation work | Restricted capacity and conditional theoretical results. |
| Method/performance selection | Uses complementarity across actions | Inadequate evidence, candidate-execution budget and development transfer. |
| Monitoring/reset | Detects or limits degradation | Conditional proxy validity and loss of useful state on reset. |
| TTT/reconstruction/multi-view consistency | Label-free auxiliary supervision | Source-stage task setup, invariance assumptions and task/proxy misalignment. |
| Output/prototype/cache refinement | Often avoids backpropagation | Representation/pseudo-label quality, graphs/caches, stronger target-set access. |
| Feature/nuisance correction | Repairs geometry or transformation-sensitive directions | Assumptions about label-preserving transformations and offline training. |
| Multi-hypothesis adaptation | Avoids reliance on one low-entropy solution | Particle cost, selection/weighting and retained underspecification. |
| Budget/evidence scheduling | Matches updates/probes to resources | Actual latency differs from FLOPs/trainable parameters; accounting can remove gains. |
| Open-set adaptation | Separates known and unknown examples/objectives | Partition errors contaminate updates; new detection metrics/task. |
| Theory/identifiability | Exposes what evidence or assumptions are necessary | Restricted model/channel assumptions are not universal runtime guarantees. |

## 7. Current candidate A and why it might still be worth investigating

**Question:** does a selector trained on source-reset or fixed-policy trajectories fail when its own previous actions change the states on which later choices are made?

Illustration: two classifiers see exactly the same current foggy support/query sequence, but one arrives from useful related adaptation and the other from a skewed, unrelated prefix. A source-only descriptor sees identical present data. Rich current-model evidence reveals some state differences. Optimizer or memory state can additionally affect the next update even when present predictions are identical.

Three results would be needed:

1. A material, reproducible residual state-dependent action effect on plausible noncollapsed states, after holding present images/order fixed.
2. Additional state evidence improves beyond a strong current-model baseline with matched logits, feature geometry and ordered summaries.
3. The effect matters during autonomous rollout, and a correction survives strong reset/state-aggregation baselines and resource matching.

Different weights producing different predictions is trivial. An artificially destructive learning rate causing collapse is not a new deployment mechanism. A replay-only selector gain does not establish autonomous reliability. Discovering exposure bias or applying plain DAgger does not establish a new general learning principle.

Possible contribution, conditional on evidence: a controlled visual TTA study separating external shift from action-induced state, an evaluation protocol revealing residual replay-to-autonomous failure, and a useful state representation/estimator/training correction. A generic MDP formulation or three-feature router is insufficient.

### Candidate B and C if A fails

**B: proxy validity.** Can a restricted, observable diagnostic flag when a label-free risk-monitoring proxy stops being informative under combined shifts? Start from Monitoring Risks §6 and POEM's label-shift qualification. ATC/BBSE and conditional prior estimators limit identifiability. A universal unlabeled guarantee is not justified. A narrow empirical warning/abstention mechanism may be worth investigating if it adds beyond known prior correction.

**C: action interaction.** Is there a specific important interference/complementarity mechanism among ordered adaptation actions under compound shifts? BoTTA already evaluates compounds, mixtures already compose experts, and order effects are generally unsurprising. Defer until a concrete unexplained interaction is identified.

These are alternatives, not an obligation to make one of them work. Reject or replace all three if the closest literature or experiments remove their value.

## 8. Experiment 002: exact protocol decisions already resolved

The canonical detailed specification is [experiments/002-state-conditioned-selection.md](experiments/002-state-conditioned-selection.md). It is planned, not executable code. Do not mistake historical digit scripts for its implementation.

### State and action semantics

Immutable source checkpoint is separate from live state. Snapshot parameters, BN buffers, optimizer, any teacher/memory, counters/mode flags and RNG. External stream time is separate and advances even when no learning occurs.

| Primary transition | Exact diagnostic meaning |
| --- | --- |
| KEEP | Use current adapted state; preserve predictive/learning state. Elapsed-time bookkeeping still advances. |
| NORMALIZE | Change only declared support-derived BN statistics, with estimator/interpolation fixed on development; freeze them on query. |
| UPDATE | One reliable entropy step on normalization affine parameters using **frozen live running statistics**; BN buffers unchanged. ETA-inspired diagnostic primitive, **not native ETA/Tent/EATA**. |
| RESET | Restore the specified source parameters, buffers, optimizer/counters and auxiliary state. Weights-only reset is a different action. |

SOURCE is a separate immutable-source baseline policy in the primary study. If later selectable, formalize a joint prediction-choice/state-transition contract: answering with source while retaining live state differs from resetting live state. Never silently add SOURCE as an alias for RESET.

All evidence forwards are state-pure: no BN writes, gradients, teacher updates, memory insertion or RNG/counter changes affecting candidate execution. Query scoring is likewise pure. Restore RNG/common random numbers where stochastic counterfactuals are comparable. Candidate branches at a decision start from the same full snapshot.

The primary shared BN backbone supports the statistics action. A LayerNorm-only backbone requires a different declared menu. When adding complete algorithms, do not silently discard their optimizer/teacher/memory state to make them interchangeable. Some should remain separate faithful autonomous baselines.

### Timing and identity separation

Primary deployment is **predict then update**: predict B_t using the previously selected state; observe B_t without labels; choose/apply the next transition; score its effect on B_(t+1). No future query inputs enter the current controller.

The proposed prediction/support block is 64 examples. The primary one-decision loss target is the **next 64-example block**. A separate 512-example post-action diagnostic window freezes subsequent transitions to KEEP. That 512-window score is not a one-step training target or autonomous rollout score. This distinction was explicitly corrected during review.

Split original image identities before making corruptions. Within a local matched case, prefix IDs, support IDs, query IDs and fresh query-replication IDs are disjoint pools. A sibling corruption of a query image must not appear in its prefix. Matched histories/branches deliberately share the present sequence for paired comparisons. Repetitions in longer autonomous streams are allowed only when declared and grouped appropriately.

Histories/current continuations must be chosen independently of which action wins. Keep all ties, non-flips and failures. Use calibration-fixed practical margins, paired/tie-aware intervals and fresh query repetitions to distinguish ranking differences from finite-query noise. Correlated windows/branches are not independent experiments.

### Proposed data/model regime, not a completed setup

One transparent CIFAR-100 option: train source on 45,000 official training IDs; use 3,000 different training IDs for auxiliary selector fitting and 2,000 for calibration; leave the official 10,000 test IDs untouched. This differs from a standard 50,000-image source model and must be disclosed; competitors must share source preparation. A pretrained checkpoint alternative needs a legitimate auxiliary-data regime, not an implicit change.

Candidate source seeds: 11, 29, 47, 71, 101. Initial support/prediction size 64; sensitivity sizes 16/32/128. Prefix scales 2,048 and 8,192 observations are examples to freeze or amend on development before final evaluation. Hardware, source architecture details, optimizer/LR, exact family lists, practical margins and compute budget are not yet fixed.

Hold out corruption families, history patterns and dominant-class identities from selector fitting. The classifier still learns all source classes. Holding out dominant target classes is not a new-class recognition task. Hold out original images as well as corruption families. Labels may construct/evaluate skewed streams offline; labels and domain/shift IDs never become runtime features.

### Observations, selector and collection comparison

Compare equal-capacity predictors using:

1. Frozen-source global evidence.
2. Frozen-source ordered evidence, reflecting the close identifiability predecessor.
3. Rich current-model logits, geometry and ordered summaries mirroring source evidence.
4. That same evidence plus compact parameter/buffer/optimizer/memory/age descriptors.

Source/live disagreement and displacement are established features, not claimed novel. A source pass can be additional runtime. Observation cost must include parameter scans, memory and copies.

A small action-loss regressor can select the minimum predicted subsequent loss plus a development-fixed compute penalty. This is ordinary decision machinery. Train action-loss targets on cloned actions and disjoint labeled auxiliary queries; final labels stay evaluator-only. One-step training is myopic and does not solve delayed credit assignment.

Compare states collected from fixed policies, broad random policies and successive frozen versions of the learned policy. Match unique labeled development query IDs and reuse, scored action outcomes, candidate update steps, support forwards and state-generation compute. Show frontiers if simultaneous equality is impossible. Include plain DAgger-style aggregation before proposing a special remedy.

### Stage sequence and required controls

1. **Residual headroom/mechanism:** matched present data after predefined realistic prefixes. Include periodic reset, optimizer reset and a stateless-update variant. A paired optimizer-memory ablation fixes weights/buffers while retaining versus resetting momentum; it is an intentional diagnostic, not an independent natural deployment.
2. **Incremental evidence:** test deeper state beyond rich current-model evidence, fixed actions and simple age/entropy/concentration/reset rules.
3. **Replay versus free rollout:** score logged states, then allow each controller to create its own states on the same external stream. Equal-budget collection/aggregation comparisons matter here.
4. **External confirmation:** only after a residual effect exists, move to another architecture and ImageNet-C/DomainNet-126. Add real-shift/other-task evaluation only if it probes the actual mechanism.

Controls include strong frozen SOURCE, every fixed action and best development-fixed action, normalization, faithful strong reliable/stable update methods, ROID/RoTTA, RDumb, compatible ASR/GALA/Hybrid-TTA, MORPHEUS-style selection and a strong ordered source selector. Class-mixture studies additionally require imbalance-aware methods. Different source access/backbone/task comparisons belong in separate qualified tables.

### Measurements and stopping rules

Measure accuracy/error, excess error versus SOURCE and same-state KEEP, harmful-update frequency **and magnitude**, worst-family/group/tail behavior, local same-state action regret, replay-to-autonomous performance and complete latency/memory/forward/backward/state cost. Report source preparation and offline selector collection/fitting separately.

A local hindsight oracle uses evaluator labels to score branches from one state. Independent local optima on another policy's trajectory form a replay diagnostic, not a dynamic upper bound. A sequence oracle must generate its own state transitions and declare its horizon/objective.

Stop or reframe if headroom is negligible, exists only after pathological updates, disappears with simple resets/optimizer reset, is fully captured by rich current evidence, fails autonomously, does not transfer to unseen histories/models, or loses after cost. If plain equal-budget aggregation matches the remedy, do not rename it; assess whether an important new empirical finding remains.

## 9. Benchmark knowledge the next agent must preserve

The full [benchmark companion](notes/review-refresh-2026-10-26/benchmarks.md) contains dataset/source links and qualifications.

- **CIFAR-10-C/100-C:** useful controlled screens, commonly 15 corruptions × five severities. Declare exact list and averaging. New severity is weaker than new family. Small dataset resampling is not independent validation.
- **ImageNet-C:** fix checkpoint, preprocessing, severity aggregation, order, batch size and reset/timing. Raw mean error and original AlexNet-normalized mCE are different metrics.
- **ImageNet-3DCC:** useful geometry-related transfer; estimated geometry and synthetic corruptions remain approximations. Underlying image IDs can overlap ImageNet-C.
- **ImageNet-V2/A/R/Sketch:** resampling, naturally hard examples and representation/style shifts differ; class subsets/mappings matter. These are not extra severity levels.
- **DomainNet:** full dataset has six domains/345 classes. Common DomainNet-126 is a four-domain/126-class TTA subset. Source-free, multi-source, full-target/multi-pass and online causal access are different protocols. Pin the exact source-to-target transfer and implementation.
- **WILDS:** iWildCam macro F1, FMoW worst-region accuracy, Camelyon17 average accuracy; do not replace official metrics with convenient overall accuracy. Correlated patches need slide/patient-aware uncertainty. As inspected October 26, standard rules prohibit test training/model selection and evaluation batch statistics; nonstandard rules retain the test-training/selection prohibition. Historical ARM-BN/test-time BN rows exist, so do not state every inference-only refinement is categorically forbidden. A custom online-updating study must be distinguished from official submissions. WILDS 2.0 designated unlabeled splits provide a different adaptation-before-test regime. Recheck current rules before a submission claim.
- **ACDC/Cityscapes-C:** real adverse conditions versus synthetic segmentation corruption; mIoU and dataset/version definitions matter. A segmentation extension is substantial work, not a cheap way to claim generality.

Existing benchmark programs already include realism: TTAB, Yu's Benchmark-TTA, CCC/RDumb, UniTTA, time-constrained evaluation, Tempora, BoTTA and TTABC. UniTTA defines 36 formal domain/class combinations and evaluates 24 settings in the inspected paper; its released sampler differs from the original. A living TTA leaderboard exists at `test-time.cc/tta-leaderboard/`; its reproduction-code link was TBD when inspected. Do not claim no leaderboard exists, and do not claim independently reproducible current SOTA from that website alone.

TTABC documents CLIP paradigm preferences. Its v3 Table 4 reports SOURCE/Tent/DeYO corruption accuracies 21.46/26.94/34.98%, and natural averages 57.86% for DeYO versus 63.01% for prototype-based TPS. These are **authors' table-specific results**, not ours or a universal ranking. Natural-average prose and tables in that version disagree; always cite the exact table. Do not inherit a numeric summary uncritically.

Cost can change method rankings: Alfarra's time-constrained evaluation, Tempora and BoTTA are direct precedents. Count source/current passes, probes, candidate/shadow execution, teacher work, gradients, copies, resets, memory, throughput and device latency. Few trainable parameters or claimed “one pass” is not adequate. A cached classifier-head shortcut in the old toy architecture does not imply a one-pass deep BN implementation.

## 10. Historical evidence: useful, but not validation of candidate A

### October 23 bounded digit experiment

Canonical result report: [outputs/shift-aware-tta-diagnostic-2026-10-23.md](outputs/shift-aware-tta-diagnostic-2026-10-23.md). Code/results: [diagnostics/2026-10-23/](diagnostics/2026-10-23/). Raw counts in `run_manifest.json`; architecture/action definitions in `CORE_SCOPE.md`.

- Bundled sklearn digits: 1,797 images, ten labels, 8×8. Per split: 900 source / 400 meta / 200 calibration / 297 test images. Meta cross-fitting used two disjoint 200-ID pools.
- MLP encoder: one 32-unit ReLU hidden layer; separate multinomial head fit after source normalization. Three pipelines/splits, six fitted components. Encoder/head stay frozen at adaptation time.
- 640 episode definitions per split, 1,920 total; 5,760 three-action evaluations. Episode resampling and repeated IDs mean these are not independent experiments.
- Development: clean, noise, brightness, blur, translation; held-out contrast/occlusion. Support sizes 16/32, two severities, balanced/dominant-class sampling.
- Actions: SOURCE, hidden-support-statistics normalization, and three entropy-affine steps at LR0.05 **starting from support normalization**. This old action differs from Experiment 002's frozen-live-buffer UPDATE. Neither is native Tent.
- Cheap/rich ridge evidence dimensions: 82/110. Rich evidence used two fixed mild ±0.35-pixel translations plus a charged repeated original pass.

Held-out-family average accuracies (64 episodes per source/split):

| Seed | SOURCE | Cheap selector | Always-rich | Hindsight oracle |
| --- | ---: | ---: | ---: | ---: |
| 241023 | 76.46% | 77.34% | 78.66% | 82.91% |
| 241024 | 73.68% | 73.97% | 74.27% | 80.76% |
| 241025 | 74.02% | 74.95% | 78.37% | 82.32% |

The important negative result: calibration chose **zero extra evidence acquisition at every positive declared cost weight** (0.002, 0.01, 0.03 error per calibration-source-time unit) in all three repeats. Rich evidence sometimes helps; that does not validate buying it selectively or efficiently.

Four additional held-out-family folds had inconsistent transfer; the rich selector's mean error was slightly worse than SOURCE over those folds. A post-hoc concentration gate suggested a simpler action rule but is exploratory, even though its threshold was calibrated without test-label tuning. One recorded original-split figure was 80.52% versus 76.46% SOURCE, with about 5.8× cost in that implementation; do not promote it as fresh confirmation.

Tiny-system timings were dominated partly by wrapper overhead. Compiled linear maps preserved decisions but did not prove efficient acquisition on a modern network. The encoder reached its fixed iteration limit in all three fits; warnings are retained. Gradient/split/immutability audits were conducted under that historical authorization, not repeated for this handoff.

### Externally reported five-seed gate results

Canonical provenance: [reports/review-ii/result_provenance.json](reports/review-ii/result_provenance.json). Report source: [papers/review-ii-five-seed-progress.md](papers/review-ii-five-seed-progress.md).

| Policy | User-reported accuracy | Harmful-update episodes |
| --- | ---: | ---: |
| SOURCE | 76.4 ± 1.0% | — |
| Always normalize | 74.8 ± 1.8% | 31% |
| Concentration-only gate | 77.3 ± 1.1% | 15% |
| Three-feature gate | 77.9 ± 0.9% | 11% |

The ± values describe five-seed variation, not confidence intervals. Harm is the percentage of **all evaluation episodes** where normalization was applied and accuracy was worse than SOURCE. Raw predictions, individual seed outcomes, external code and dataset/backbone/split manifests are missing. Do not infer these are faithful CIFAR-C/ImageNet-C results, reproduce them from local digits, or combine them with the three local seeds.

The historical gate uses predicted concentration, mean entropy and source-relative standardized feature displacement in a depth-two regression tree. It chooses SOURCE versus support normalization and was motivated by true-class-mixture versus corruption-induced collapse at matched predicted concentration. Literature overlap is substantial; these aggregates do not establish novelty or validate candidate A. Some historical prose still says “planned/unvalidated”; interpret it chronologically with the external-results provenance, rather than erasing either record.

## 11. Source library, publication qualifications and access limits

Authoritative working records: [REFERENCES.md](REFERENCES.md), [references.bib](references.bib), [catalog JSON](sources/catalog.json), [catalog CSV](sources/catalog.csv), and [papers/](papers/). The handoff's [source dossier](notes/handoff-2026-10-31/source-dossier.md) expands every indexed record in one place.

As of the saved review: 103 records, 101 scholarly and two official web records; 48 inherited, 55 added, 68 freshly selectively inspected. Remaining records retain earlier reading status. This was targeted deep research, not a complete citation database or exhaustive systematic review. Recheck novelty-critical sources and work since October 26 before making a new claim.

Preserve canonical aliases:

| Alias appearing in research notes | Canonical citation key |
| --- | --- |
| `Schneider2020CovariateAdaptation` | `Schneider2020BNAdapt` |
| `Zhou2026RecoveryComplexity` | `Zhou2026Learnability` |
| `Park2023LabelShiftAdapter` | `Park2023LSA` |

Important metadata/access qualifications:

- MORPHEUS is TTU workshop, not ICLR main track.
- SLRF full text is inaccessible in the saved investigation; broad overlap is supported by publisher abstract only.
- Channel-Selective Normalization / Hybrid-TTN has a 2025 PMLR volume for the 2024 CoLLAs event. Preserve `Vianna2025ChannelSelective`. Its official PDF was selectively inspected: source-labeled per-class sensitivities, prior-dependent rescore, offline batch500 experiments and BN scope.
- TRIBE is AAAI2024 with a 2023 preprint; EATA-C is a later journal extension, not the original EATA result.
- Monitoring Risks is NeurIPS2025 **volume38**, correcting the inherited volume error.
- TTABC's NeurIPS2026 E&D acceptance was author-reported; independent proceedings confirmation was not completed. Several other recent sources likewise remain preprints/author-reported venue status.
- BoTTA's publisher SenSys2026 citation and older preprint report-number year differ; publisher version governs the current citation, discrepancy retained. Its paper-linked code returned404 in an earlier pass.
- RNA code availability was not verified. Source-linked repository existence is not execution/reproduction evidence.
- Official OpenReview/CVF endpoints sometimes returned browser challenges/403. Alternate author/proceedings/arXiv versions were used with access limits recorded; no failed fetch counts as a full read.
- Use exact NOTE identifier `2208.05117` and Yu Benchmark-TTA `2307.03133`; both were checked in the final verification. Do not substitute nearby guessed IDs.

Saved evidence: nine PDFs/text extractions in `sources/pdfs/` and `sources/text/` with original manifest; one additional official Channel-Selective PDF/text under `notes/review-refresh-2026-10-26/verifier-evidence/`; seven HTML snapshots under `primary-snapshots/` in that refresh directory. Hashes/retrieval statuses are in `sources/manifest.json` and `notes/review-refresh-2026-10-26/snapshot-manifest.json`. Downloading a paper is not full-paper reading.

## 12. Tools, environment history and scripts with side effects

The installed Feynman skills were used for literature/deep research, primary-paper exploration, critique and session records. Their skill files are under the workspace `.agents/skills/feynman/`. Use current skill instructions when continuing. The session-log skill calls for a record in `notes/session-logs/`, provided for this handoff.

On October 26, `feynman alpha status` reported authentication but the documented semantic-search command returned `Unknown alpha command: search`. Slash workflows were not directly exposed in the chat. Available research/verifier/reviewer stages and primary-source tools were used; no successful alpha search or hidden workflow run was claimed. Rediscover current capabilities instead of assuming the old CLI problem persists. Do not call the user's stale bare `alpha` binary or silently repair account configuration.

Historical numerical environment: Python3.13.9, NumPy2.2.6, SciPy1.17.1, sklearn1.8.0. PyTorch/torchvision were absent for the October23 diagnostic. These versions/absences are **not freshly verified current setup**. No project PyTorch environment or runnable Experiment002 entrypoint has been created.

| File/tool | Side effect / continuation caution |
| --- | --- |
| `diagnostics/2026-10-23/autoresearch.sh` | Refits/recomputes and runs historical audits in-place; overwrites model, splits, outcomes and timing artifacts. Do not run for a literature/handoff task. Preserve/copy the run directory before any authorized rerun. |
| `notes/build_reference_records.py` | Rebuilds from the **old** review ledgers. Can discard the later reference expansion. Do not run as a current-library update. |
| `notes/review-refresh-2026-10-26/build_library.py` | Reconstructs from the archived 48-source base plus four fixed October26 ledgers; rewrites index/BibTeX/catalog and dated note sections. It is not an append-only importer. Later central-only edits/new sources can be lost on rerun. Inspect/extend it or use a new dated migration preserving current records. |
| `notes/review-refresh-2026-10-26/save_primary_snapshots.py` | Re-fetches and overwrites dated snapshot files/manifest. Save new evidence to a new dated location rather than rewriting historical retrieval provenance. |
| `reports/review-ii/build_report.py` | Historical report/presentation generation, unrelated to implementing the new method. Do not run unless that document task is requested; presentation work requires its skill. |
| Handoff export utility in `notes/handoff-2026-10-31/` | Writes only the source dossier and artifact inventory. It does not run research code or alter the scientific catalog. The inventory excludes itself to avoid a self-hash cycle. |

No Git repository was available at the workspace root in the October26 session. Do not infer current Git state or initialize one as part of a research continuation without a reason. Record code/checkpoint/data hashes or commits when actual implementation begins.

## 13. Continuation plan toward a solid research piece

### Milestone 1: attack the candidate before building it

Refresh the narrow literature since October26 and inspect the exact closest methods. Prioritize SLRF full text if legally available, RNA training rollouts, ASR/GALA/Hybrid state transitions, Agentic-TTT §2.2.2/AppendixE, MORPHEUS and identifiability's evaluation unit. Search beyond the phrase “shift-aware”: whole-method selection, autonomous/meta-control, learner-induced state distribution, state coverage, optimizer memory, policy switching, unsupervised validation and reset/recovery.

For each candidate, write a novelty dossier containing: precise deployment/action/information setting; the failure being claimed; three or more closest sources; exact passages inspected; what they already solve; the remaining difference; why that difference matters; an observation that would refute the gap; and the smallest experiment needed. A difference in benchmark name, feature count or combination of modules is not enough.

If an exact predecessor or a trivial control defeats candidate A, record that and pivot. Do not launch repeated cosmetic gates until a positive number appears. Candidate B/C are starting points, not compulsory fallbacks.

### Milestone 2: freeze a small honest protocol

Choose source checkpoint/data access and the actual execution environment under the next task's authorization. Freeze primary claim, data IDs, holdouts, action contracts, timing/horizon, model/optimizer semantics, resource budget, practical margins, primary comparisons and stopping rules. Preserve current proposals as dated versions if amended.

Implementation should separate: immutable source; live state; pure observation; explicit transition; query evaluator; source/meta/calibration/final identity registry; trajectory logging; deterministic branch snapshots; resource measurement. All evaluator labels and shift metadata stay outside controller inputs. This is an architectural outline, not existing code or a new algorithm.

### Milestone 3: try to falsify the residual mechanism

Implement only Stage1 at first. Show action headroom beyond strong fixed/reset/stateless controls on realistic noncollapsed histories. Use fresh query replication, not noisy argmin flips. If there is no material residual, stop large-controller development and reassess novelty.

### Milestone 4: test the proposed correction fairly

Compare rich current evidence with deeper state; fixed/random state coverage with plain learner-state aggregation; replay with autonomous streams. Match labels/reuse and collection/candidate compute. Require a TTA-specific finding or improvement beyond established aggregation and state heuristics. Keep negative results and compute failures.

### Milestone 5: establish external scope, then write claims

Use another model/normalization family and a large corruption plus natural-domain setting that tests the mechanism. Report clean/source-return, class-mixture, temporal and tail behavior where relevant. Reproduce faithful strong baselines at pinned versions and distinguish original settings from ports. Use a cost frontier, not “efficient” from parameter count.

A strong resulting paper should make a small number of claims with traceable supporting results and explicit limits. Build a claim/evidence table before the abstract: claim, closest prior art, experiment or theorem support, figure/table/output manifest, assumptions and remaining threats. A benchmark-only paper still needs an important missing measurement beyond TTAB/CCC/UniTTA/TTABC and recent identifiability/help-harm studies.

Possible honest outcomes: a useful new mechanism and method; a substantial controlled diagnostic/negative study; a rigorous documented rejection of the direction. A conference outcome remains contingent on actual contribution and evidence.

## 14. What is unresolved—do not silently fill these gaps

- Exact novelty, especially full-text overlap of SLRF and training-state coverage of learned controllers.
- Any literature developments after October26 or changed publication/code/benchmark rules.
- Existence and size of residual live-state effects after simple/current-evidence controls.
- Whether standard dataset aggregation already removes the autonomous failure.
- A valid auxiliary-labeled development regime for a chosen pretrained source.
- Exact source architecture/checkpoint, optimizer/LR, state contract details for added full methods, practical margins and runtime device.
- Hardware, compute/budget/deadline and later execution scope.
- Raw provenance of external five-seed gate results.
- Faithful modern TTA implementation, original benchmark results, final plots or manuscript.

The record-integrity checks on October26 found 103 unique catalog/BibTeX keys, all 103 note files and resolving local links in the delivered documents. The independent verification found no blocking **document** error after amendments. Neither is proof of implementation correctness, empirical validity, exhaustive novelty or a successful method.

## 15. How to leave the project for the next continuation

Update README actual status, CHANGELOG, research-branches, source index/BibTeX/catalog and paper notes when substantive evidence changes. Keep citation aliases and primary-source reading scopes. Record every executed experiment separately with hypotheses, controls, data IDs/splits, environment, commands, seeds, metrics, output manifests and interpretation. Preserve failed/no-benefit results.

Use [NEXT_AGENT_PROMPT.md](NEXT_AGENT_PROMPT.md) as a brief bootstrap, this file as the self-contained research memory, the [complete source dossier](notes/handoff-2026-10-31/source-dossier.md) as the bibliography expansion, and underlying records as the authority for precise outcomes. The user's objective is genuine novelty and a solid research piece; the currently proposed mechanism is allowed to fail.

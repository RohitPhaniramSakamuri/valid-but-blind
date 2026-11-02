# Fifteen minute CPU diagnostic

Authorized by the user on 23 October 2026: run the diagnostic with subagents in 15 minutes. Start 17:48:26 UTC; target finish 18:03:26 UTC. Execution environment: the existing local CPU Python environment, using installed NumPy/scikit-learn/SciPy; no package installation, cloud run or paid API.

## Scope fixed before inspecting outcomes

Run the three diagnostic stages on scikit-learn's bundled 8×8 ten-class digits and declared custom shifts. This is an alternate-data mechanism study. No CIFAR-C, ImageNet-C, DomainNet or WILDS result is implied.

The source classifier will use a source-trained small MLP encoder and source-standardized hidden features with a refit multinomial head. Its normalization-statistics and entropy-affine interventions are explicit adaptations for this architecture, not exact reproductions of native Tent or any cited benchmark.

- Source fit images are disjoint from selector-development, calibration and final-evaluation images.
- Meta-training cross-fitting uses disjoint original-image pools. Episode resampling within a pool is correlated and must be disclosed.
- Support and query identities do not overlap within an episode. True query labels are used only for offline development targets or final evaluation.
- Cheap/rich routing features are computed from support inputs only. Family/severity/prior metadata are evaluator fields, not selector inputs.
- All actions start from equivalent source state per episode; query prediction semantics are declared in code/metadata.
- Cheap and rich selectors use matched low-capacity regression. The acquisition gate uses only out-of-fold realized selection gains, with calibration choices made separately from final evaluation.
- Terminal actions: SOURCE, statistics-only support normalization, and an entropy-based normalization-affine update. Hyperparameters fixed before final outcomes.
- Acquisition controls: never, always, random, fixed schedule, source entropy, selector ambiguity and learned realized-gain purchase. Include a same-view source ensemble control if completed within budget.
- Evaluate accuracy/error, oracle headroom, harmful choices, paired selector/evidence differences and all-in measured/estimated route costs. Timing is descriptive local-CPU evidence, not device-independent efficiency.

## Roles and outputs

- `diagnostic_core`: classifier, mathematical interventions, source fit and frozen split record.
- `diagnostic_outcomes`: declared shift generation and raw action/evidence outcomes.
- Lead: selector and acquisition comparisons, summary, figures and durable records.
- `diagnostic_audit`: numerical gradient, state and split checks; independent interpretation audit.

All results must identify actual executed work and any omitted protocol elements. The larger experiment plan remains separate; this time-boxed pilot cannot establish publication readiness, novelty or general deployment performance.

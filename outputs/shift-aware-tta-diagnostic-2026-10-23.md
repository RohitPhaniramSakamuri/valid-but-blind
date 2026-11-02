# Shift aware adaptation diagnostic results

Run date: 23 October 2026. Status: completed bounded CPU mechanism diagnostic; the full benchmark protocol remains unrun.

## Conclusion

There is action-selection headroom in this small task, and richer observations sometimes improve selection. The tested acquisition controller does not establish a net benefit once local computation is penalized: calibration chose zero acquisition at every positive cost weight in all three source/split repeats. Do not promote this run as a successful adaptation method or a verified research gap.

## What actually ran

- Three source pipelines on the bundled 1,797-image, ten-class, 8×8 handwritten-digits dataset. Each pipeline fits an MLP encoder and a separate multinomial head: six fitted components in total.
- Source/meta-training/calibration/test image counts of 900/400/200/297 per source split. Meta cross-fitting uses two disjoint 200-image pools; support/query original IDs never overlap within an episode.
- 640 defined episodes per source/split repeat: 288 selector-training, 144 calibration and 208 test. Of the test episodes, 64 contain held-out contrast/occlusion families. Total: 1,920 episode definitions and 5,760 three-action evaluations, plus frozen-view ensemble controls. Reruns are not counted as new episodes.
- Five development conditions: clean, pixel noise, brightness reduction, blur and translation. Two previously unavailable test families: contrast and occlusion. Two support sizes (16/32), two corruption severities and balanced versus dominant-class sampling.
- Three terminal actions: frozen SOURCE, support-statistics normalization, and three support-only entropy-affine steps with fixed rate 0.05. Query normalization is frozen from support; encoder and classifier-head weights never adapt.
- Matched ridge selectors with 82 cheap features or 110 richer features; richer evidence uses two globally fixed subpixel translations plus a charged repeated original-view pass. No true target labels or family IDs enter runtime features.
- Grouped out-of-fold acquisition targets, separate calibration thresholds, random/fixed/entropy/ambiguity/value-gate acquisition controls, four cost weights and a frozen three-view source ensemble.
- Four additional leave-one-family-out selector checks, numerical entropy-gradient checks, state/split/outcome audits, query-identity sensitivity checks and an explicitly post-hoc simple concentration gate.

The 1,920 episodes reuse a finite dataset, and some skewed batches repeat image draws. They are not 1,920 independent experiments. This is a source-MLP/normalized-head surrogate, not native Tent, a modern image backbone, or CIFAR-C/ImageNet-C/DomainNet/WILDS replication.

## Primary held-out family results

Accuracy is the average over 64 held-out-family episodes per row. All query batches contain 32 draws; original identities can repeat in skewed conditions. The oracle uses evaluation labels retrospectively and cannot be deployed.

| Source/split seed | SOURCE accuracy | Cheap selector | Always-rich selector | Rich minus cheap | Oracle accuracy |
| --- | --- | --- | --- | --- | --- |
| 241023 | 76.46% | 77.34% | 78.66% | +1.32 pp | 82.91% |
| 241024 | 73.68% | 73.97% | 74.27% | +0.29 pp | 80.76% |
| 241025 | 74.02% | 74.95% | 78.37% | +3.42 pp | 82.32% |

Selection headroom exists across the three repeats. Rich-minus-cheap gains vary from about 0.29 to 3.42 percentage points. These repeats change the source seed and image split but reuse the same underlying dataset; they are not independent external validations.

## Does the learned purchase rule work?

The calibration-selected purchase fraction was zero at each positive declared cost penalty (0.002, 0.01, 0.03 error per calibration-source-time unit) in every repeat. With zero computation penalty, the selected rates and final behavior varied across seeds. Thus a richer selector's accuracy improvement does not establish that a cheap gate can purchase its evidence effectively or profitably.

Random, fixed-schedule, entropy, selector-margin and learned-value purchase policies were evaluated over calibration-fixed rate grids. Their final costs differ because they can choose different terminal actions. The curves describe accuracy versus measured/estimated route cost; they do not establish strict matched-budget superiority of the learned policy. See all rows in the per-run `policy_comparisons.csv` and `policy_by_family.csv` files.

## Cost and implementation sensitivity

For the original run, direct SOURCE query inference averaged 0.069 ms. sklearn pipeline wrappers add substantial overhead around these tiny linear selectors. Compiling the same fitted linear maps into NumPy arithmetic preserved every selected action (maximum prediction differences below 1e-14), but total routes still averaged 0.460 ms for cheap selection and 1.241 ms for always-rich selection.

The sensitivity changes implementation cost, not predictions. It did not refit the acquisition gate under a compiled backend. Local timings are short, device- and implementation-sensitive, and separately measured components are summed; this is not a physical deadline/scheduling benchmark or an inherent impossibility result for acquisition on larger networks.

## A useful mechanism observation

On the original split's test conditions, statistics-only normalization helped balanced batches on average but severely hurt dominant-class batches. This is an established normalization/prior-shift failure mode, not a new discovery. It explains why shift-family averages alone can hide action-selection opportunities.

A simple predicted-class-concentration SOURCE/BN gate was subsequently added. It is explicitly post-hoc, motivated by the observed breakdown, even though its threshold uses calibration labels only. It is an exploratory comparator, not fresh confirmation. Its artifacts record the threshold grid and costs.

## Further generalization and uncertainty checks

Four additional folds removed noise, brightness, blur or translation from selector training before evaluating that family's separate test-image pool. The mean rich-minus-cheap gain was about 0.34 pp; the rich selector's mean error was slightly worse than SOURCE across those four folds. Improvements were inconsistent, reinforcing that the two primary unseen families do not establish general transfer.

For the original split, selecting an action using labels from one query-identity half and evaluating on the other, then reversing halves, retained about 5.40 pp improvement over SOURCE versus 6.45 pp for the optimistic full-query oracle. Across the two repeat splits the cross-query gains were about 5.59 and 7.23 pp. This reduces one source of finite-query oracle optimism, but remains a retrospective label-assisted diagnostic.

Query-identity cluster resampling and episode resampling were also performed with fixed models and policy choices. They retain repeated occurrences of an original query image together where specified. Shared supports, models and family construction still induce dependence. The intervals are conditional sensitivity analyses, not independent population-level confidence or proof of significance.

## Checks, warnings and omissions

Independent checks verified analytic affine entropy gradients against finite differences, immutable source arrays, normalized finite probabilities, disjoint source/meta/calibration/test pools, support/query separation, held-out family exclusion, reconstruction of saved errors from predictions and equal cheap-feature prefixes in richer evidence. The initial ambiguity-trigger cost omitted a required cheap-selector inference on purchased rows; it was corrected before the retained analysis.

Each of the three source encoder fits reached the fixed 250-iteration limit. Those warnings are retained; no final-test tuning or refitting was used to hide them. The entropy action backpropagates analytically through the affine/head calculation only; it never updates the encoder. Its counts must not be described as full-network backward passes.

Not performed: original cited-paper reproduction, large image benchmarks, another dataset or architecture, robust-method menus such as native SAR/ROID/DeYO, composition generalization, continuous live-state controllers, energy measurement or physical deadline testing. These belong to the larger protocol. The current gate did not pass the scaling criterion, so no broad benchmark success is claimed.

## Execution and uv

The user authorized the bounded local CPU diagnostic. Initial source/outcome commands used the already installed Python environment before the subsequent uv instruction. After that instruction, analyses, repeat generation and checks used uv. No pip, dependency installation, cloud GPU or paid API was used. The recorded numerical environment is Python 3.13.9, NumPy 2.2.6, SciPy 1.17.1 and scikit-learn 1.8.0 with bounded numerical threads.

The executable recipe is `autoresearch.sh`. It uses `uv run --no-project --no-python-downloads --python /usr/bin/python python ...` to select the existing system environment without installing packages. Re-running overwrites artifacts in that run directory; copy the directory first to preserve a prior timing run.

## Decision and next step

Keep the action/evidence diagnostic and the negative acquisition result. Do not claim the proposed controller works. Before scaling, compare a simpler low-dimensional selector/gate and stronger faithful adaptation actions on a source model where forward/backward compute dominates Python overhead, with a newly fixed evaluation split. The concentration-gate finding requires fresh confirmation. No automatic expensive follow-up is authorized by this report.

## Artifacts

- [Original run and source code](../diagnostics/2026-10-23/)
- [Original action/evidence outcomes](../diagnostics/2026-10-23/outcomes.npz)
- [Policy comparison table](../diagnostics/2026-10-23/policy_comparisons.csv)
- [Accuracy/cost figure](../diagnostics/2026-10-23/accuracy_cost_frontier.png)
- [Independent audit](../diagnostics/2026-10-23/audit.md)
- [Repeat ledger](../diagnostics/2026-10-23/repeat_summary.json)
- [Original larger experiment plan](../experiments/001-policy-selection-pilot.md)

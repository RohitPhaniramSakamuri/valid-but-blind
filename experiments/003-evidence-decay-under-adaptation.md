# Does a selector's evidence decay as the model adapts?

Experiment ID: **003-evidence-decay-under-adaptation**. Proposed **31 October 2026**.

Status: **Planned; not implemented or run.** No result exists. It reuses the action and timing contract of [Experiment 002](002-state-conditioned-selection.md) and is meant to run before it. Rationale: [novelty dossier](../outputs/novelty-dossier-2026-10-31.md).

## Question and hypotheses

- **H0 (gate):** live states have meaningful action headroom over the best fixed action.
- **H1 (decay):** a next-block action-value predictor fitted on source-reset states loses selection quality as adaptation exposure grows.
- **H2 (mechanism):** decay is larger for evidence the update directly optimizes (entropy, confidence) than for other evidence.
- **H3 (residual):** fitting across all exposure levels, at the same number of scored outcomes, does not remove the decay.

Exposure `k` means the number of adaptation updates applied before the decision.

## Setup (proposed values, to freeze on development data)

**Data.** CIFAR-100-C with a pretrained BN checkpoint from RobustBench (exact model and hash to record).

**Source regime.** This differs from Experiment 002's 45k/3k/2k split because no source model is trained here. Because the checkpoint used all 50,000 training images, auxiliary labels come from corrupted test identities:

- 5,000 development and 5,000 final original IDs, split before any corruption. Confirm first that image order matches across corruption files.
- Within each: 3,000 prefix IDs and 2,000 present IDs, the latter forming 10 disjoint support/query/fresh-query triples of 64 each.

The final-pool labels are used by the evaluator only. Numbers from this regime are not comparable to standard published results.

**Shift holdout.** Fold 1 develops on noise and blur (7 corruptions) and evaluates on weather and digital (8). Fold 2 swaps them. Severities 3 and 5.

**Prefixes.** Chosen without looking at which action wins:

- Exposure `k` in {0, 8, 32, 128} updates, batch 64. `k = 128` needs 8,192 observations, so prefix IDs repeat under different corruptions. This is disclosed and grouped in the analysis.
- Prefix corruption: same family or different family as the present batch.
- Prefix policy: UPDATE-only or uniform random over the menu.

Trajectories are checkpointed at each `k` and shared across triples.

**Actions.** KEEP, NORMALIZE, UPDATE, RESET, as defined in Experiment 002. UPDATE is the modified frozen-BN primitive, not native Tent or ETA. Use SGD without momentum first, so optimizer memory cannot explain the results. Learning rate is fixed on development data and must not collapse the model on development streams.

**Target.** Loss on the next 64-example block, branched from an identical snapshot, with a fresh disjoint query as replication.

**Evidence sets, with equal predictor capacity:**

| Set | Contents |
| --- | --- |
| S | Frozen-source entropy, confidence, class concentration, feature geometry |
| L-opt | The same entropy, confidence and concentration from the live model |
| L-other | Live feature geometry only |
| X | Source-live disagreement |
| All | Union of the above |

**Training regimes.** (a) Fitted on `k = 0` only. (b) Fitted across all `k`, with the number of scored outcomes matched to (a). Exposure `k` itself is an allowed input in a further variant of (b).

**Scale.** About 2,080 final-fold states per fold and stream seed (160 present sequences × 13 age/relation/policy conditions) × 4 branches × 192 images, or roughly **1.6 million image forwards**, plus about 8,192 prefix updates and similar for development. Start with one checkpoint and three stream seeds. A second architecture comes only if the gates pass.

**Metrics.** Explained here because the decisions rest on them:

- **Local regret:** the chosen action's next-block loss minus the best branched action's loss, from the same state. Zero is perfect.
- **Headroom:** the regret of the best development-fixed action.
- **Value error:** absolute error of predicted action loss differences.

Report mean, tail and collapsed/noncollapsed strata (evaluator-only, with the threshold fixed on development data). Use a cluster bootstrap over trajectories and original IDs, because branches sharing a prefix are not independent.

## Decision rules (provisional; freeze on development data before final scoring)

| Check | Provisional rule | If it fails |
| --- | --- | --- |
| H0 | Headroom at least 1.0 pp at `k >= 32` on noncollapsed states | Stop; selector work has little room |
| H1 | Regime (a) regret rises at least 0.5 pp from `k = 0` to `k = 128`, interval excludes 0 | Stop; evidence is stable, report the negative result |
| H2 | L-opt decay exceeds L-other or S decay, interval excludes 0 | Keep decay finding; drop the Goodhart-style mechanism |
| H3 | Regime (b) leaves at least half of the decay | Ordinary coverage suffices; no method claim |

## Steps to run

No code exists yet. Before running:

1. User authorizes execution, dataset and checkpoint downloads, and names the machine.
2. Create a project uv environment (`uv init`, `uv add torch torchvision robustbench` or pinned equivalents). Never pip.
3. Run a timing probe on a handful of branches and record the projected runtime here. Reduce severities or triples by dated amendment if needed.
4. Freeze the manifest on development data, then score the final pool once.

## Amendments, 31 October 2026, before any real data was seen

1. **Random prefixes exclude RESET.** A uniform policy with RESET would reset about every four batches, so `k = 128` would not mean high exposure. Prefix random is uniform over KEEP, NORMALIZE and UPDATE. Update counts are logged per state.
2. **Low-exposure training uses `k <= 8`, not `k = 0`.** At `k = 0` KEEP and RESET are the same state, so a predictor fitted there could never learn to separate them. H1 decay is measured from `k = 8` to `k = 128`.
3. **Headroom is cross-fit.** Choosing and scoring on the same 64 images flatters an oracle. The gate oracle chooses on one block and is scored on the disjoint other block. The naive figure is reported alongside.
4. **"Same family" prefix** means other corruptions from the present batch's family, never the present corruption itself.
5. **Tuning rule.** Severity 5, development data. Alpha from {0.1, 0.3, 1.0} minimizing error at `k = 0`. Learning rate from {1e-4, 1e-3, 1e-2, 1e-1} minimizing error after 128 updates, among rates whose worst corruption is at most 5 pp worse than source. Three development triples are reused for tuning, so development outcomes share these images.
6. **Noncollapsed** means KEEP error at most 5 pp above source and top predicted class share below 50%, using evaluator labels.

Code: [`run.py`](../diagnostics/2026-10-31-exp003/run.py), [`analyze.py`](../diagnostics/2026-10-31-exp003/analyze.py). The architecture is written locally and loads the checkpoint with a key check, because a Git install of RobustBench was blocked by the permission system. Checkpoint SHA-256: `ce86bde2485fbc74ae90186bcb73d294af6c6fe587205b700eb1b4a20e783d78`.

## Runtime estimate, 31 October 2026

Measured here with an untrained ResNeXt-29-like model (4.87M parameters) on random 64-image batches, using 4 CPU threads, a busy machine and uv's CPU PyTorch: forward 1.585 s (n=10), BN-affine update 3.376 s (n=5). A short noisy sample, and the real checkpoint may differ.

Cost per fold and seed, counting 12 forwards plus 1 update per state, and all prefix steps as updates: final about 20.6 h, development about 18 h, so about 39 h on CPU. The full plan (2 folds × 3 seeds) is about 232 h, or roughly 10 days.

GPU figures are **assumptions, not measurements**: forward 15 ms, update 50 ms, about 10 ms of snapshot overhead per branch. That gives about 30 min per fold and seed, and about 3 h in total. AWS has no credentials on this machine. RunPod is reachable; its $0.22/h RTX 3090 figure comes from an earlier exited pod, not a current quote.

## Actual results

**Run, 31 October 2026:** fold 1, development pool only (noise and blur), seed 1, one AugMix ResNeXt-29 checkpoint. RunPod RTX 4090 secure-cloud pod at $0.89/h, torch 2.4.1+cu124, Python 3.11 in a uv venv with system site packages. Command chain: [`pod_job.sh`](../diagnostics/2026-10-31-exp003/pod_job.sh). Outputs: [`results/`](../diagnostics/2026-10-31-exp003/results/). 1,820 state rows; the 70 trajectories finished in under about 7 minutes. **The final pool was not touched.**

Tuning chose alpha 1.0 and learning rate 1e-4. Both sit at the edge of their grids. Rate 1e-3 had mean error 71% with a worst corruption 59 pp above source.

**H0 gate: failed by its rule.** Cross-fit headroom at `k >= 32` on noncollapsed states was **0.45 pp (95% interval -0.44 to 1.67; n = 764)**, against the 1.0 pp threshold. The interval includes 1.0, so the data do not exclude it. The naive same-block figure was 2.20 pp.

| Mean error % by exposure, all states | KEEP | NORMALIZE | UPDATE | RESET |
| --- | --- | --- | --- | --- |
| `k = 8` | 49.68 | 34.76 | 49.66 | 41.43 |
| `k = 32` | 49.66 | 34.75 | 49.61 | 41.43 |
| `k = 128` | 47.37 | 34.71 | 47.35 | 41.43 |

**Exploratory, development only:** low-exposure-trained L-opt excess error over the cross-fit oracle was 1.02 pp at `k = 8` and 1.01 pp at `k = 128`, so there was no growth. Fitting across all exposures did not improve it (1.36 and 1.33 pp).

**Interpretation and limits:**

- NORMALIZE won almost everywhere and is nearly history-independent, because alpha 1.0 replaces the BN statistics with those of the current batch.
- **Exposure was weak in the update-only arm.** At learning rate 1e-4, KEEP error after 128 updates was 41.72%, against 41.42% for RESET on the same noncollapsed states, and UPDATE matched KEEP. So this run is **not a strong test of evidence decay**. It says little about H1 and H2 under stronger adaptation.
- Present batches come from one fixed corruption, so support and query always match. That favours NORMALIZE and excludes corruption changes between decisions.
- Cross-fit headroom understates, and same-block headroom overstates, what perfect per-batch selection could gain.
- One fold, one seed, one checkpoint, development data, reused tuning images.

**Decision under the frozen rule:** stop; folds 2, other seeds and the final pool were not run. Any stronger-adaptation run would be post-hoc and exploratory.

### Exploratory stronger-adaptation check, 31 October 2026

**Post-hoc; cannot pass the gate.** Fold 1 development data, seed 1, 3,640 rows, 737 s. Code: [`run_strong.py`](../diagnostics/2026-10-31-exp003/run_strong.py), [`analyze_strong.py`](../diagnostics/2026-10-31-exp003/analyze_strong.py). Outputs: [`results_strong/`](../diagnostics/2026-10-31-exp003/results_strong/). Alpha 0.1; adapt prefix applies NORMALIZE then UPDATE per batch; change streams score the query on a different corruption. **No learning rate met the safety rule** (worst excess about 35 pp at all three, nearly equal, so the rate is unlikely to be the cause), so the fallback 2e-4 was used.

Adaptation was now substantial: at `k = 128` on the adapt prefix, disagreement with source was 48% and stationary KEEP error 50.49% against 41.43% for source. However, **live entropy rose** from 0.73 to 1.21, the opposite of the proposed mechanism, and a single UPDATE still matched KEEP within about 0.1 pp.

| `k >= 32` | Best fixed | Headroom, all states (95% interval) | Headroom, noncollapsed |
| --- | --- | --- | --- |
| Stationary | RESET | 3.89 pp (0.93 to 7.33) | -0.17 pp |
| Change | RESET | 5.37 pp (2.24 to 8.72) | -0.17 pp |

Selector excess error over the cross-fit oracle, in pp:

| Stream, evidence | Low-exposure fit, `k = 8` | Low-exposure fit, `k = 128` | All-exposure fit, `k = 128` |
| --- | --- | --- | --- |
| Stationary, All | -0.27 | 0.49 | 0.36 |
| Stationary, L-opt | 2.02 | 5.05 | 4.80 |
| Change, All | 3.20 | 11.00 | 7.09 |
| Change, S | 3.84 | 11.05 | 8.33 |
| Change, L-opt | 2.30 | 10.70 | 6.66 |
| Change, L-other | 2.58 | 11.75 | 7.17 |

Within-corruption correlation of live entropy with KEEP error, adapt prefix: stationary 0.21 (`k = 8`) to 0.49 (`k = 128`); change -0.57 to -0.63. Prefix relation may confound this, and it was not separated.

**Interpretation:**

- The optimized-signal mechanism (H2) is **not supported** here: entropy rose, and on change streams L-opt did not decay more than L-other or S.
- Stationary streams show no problem once evidence is combined, even with low-exposure fitting.
- Headroom exists only on degraded states and is mostly a reset decision, which ASR and RDumb already target.
- **New lead, unverified:** after a corruption change, selector error grows strongly with exposure, and all-exposure fitting removes only part of it. This may be partly unavoidable, because the support batch does not reveal the next corruption. No identifiability check was done.
- One fold, one seed, development data, a post-hoc design and a harmful prefix.

### Saved-data follow-up on the change-stream lead, 31 October 2026

Exploratory, no new model runs and no intervals. Code: [`analyze_change.py`](../diagnostics/2026-10-31-exp003/analyze_change.py). Output: `results_strong/analysis_change.json`. Excess error over the cross-fit oracle at `k = 128`, in pp:

| Comparator | Change | Stationary |
| --- | --- | --- |
| Always RESET (also the fixed choice) | 4.58 | 3.78 |
| Always KEEP | 13.48 | 12.27 |
| Disagreement threshold rule | 7.07 | 3.76 |
| Ridge, All evidence plus `k` | 6.81 | 0.26 |
| Random forest, All evidence plus `k` | 5.33 | 0.70 |
| Ridge trained on stationary, tested on change | 11.93 | n/a |
| Table that knows support and next corruption | 0.08 | -0.24 |

**Design flaw found:** the next corruption always came from the other family. Prefix relation therefore reveals whether the prefix matches the next corruption, and evidence may partly do so too. The history table using relation (2.07 pp) is not achievable in deployment and is not reported as a result.

**Conclusions:**

- **The change-stream lead is rejected as a method direction.** No evidence-based selector beat always RESET on change streams, and knowing the next corruption closes almost all the gap, so the excess is largely missing information.
- **The entropy sign flip is retracted.** Split by prefix relation, the -0.63 correlation became 0.075 and 0.017, so it came from mixing prefix types.
- Reset benefit on the stationary query of the same state did not predict benefit on the change query (correlation -0.02 to -0.19), although 64-image noise weakens this.
- **Remaining observation:** on stationary streams, evidence selectors beat always RESET by about 3 to 3.5 pp, but a stationary-trained selector is 7.35 pp worse than always RESET after a change. Whether a stream is stationary is not observable in advance. This was seen on one fold and seed with a harmful prefix, and its novelty has not been checked.
- **A′ status:** not supported in this setup. No further Experiment 003 runs are recommended.

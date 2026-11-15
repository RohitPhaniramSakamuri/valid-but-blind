# 007: Why the dev-calibrated twin alarm failed conditions 3 and 4 (diagnosis, 3 Nov 2026)

**Status: EXPLORATORY.** Every held-out stream used here was already seen in exp005 or exp006, so nothing below is a confirmatory claim.
- Code: `diagnostics/2026-11-03-exp007-alarm-diagnosis/` (`load7.py`, `diag_a.py`, `diag_b.py`, `diag_c.py`).
- Outputs: `diag_a.json`, `diag_b.json`.

## The frozen criteria were mis-specified

**Absolute gap.** Conditions 3 and 4 asked for at least 0.15 fewer misses in absolute terms. From a 17% baseline, that demands a miss rate below 2%. The criterion should have been relative.

**Unequal operating points.** The comparison set the twin's misses at 2.4% false alarms against misses at 5.4% and 6.6%.

## Matched false-alarm comparison (exp006, Tent 1e-3)

Thresholds here are set per group on the held-out safe streams. That makes this an oracle comparison, so it is descriptive only.

| False alarms | Twin missed | Released-monitor signal missed | Relative reduction |
|---|---|---|---|
| About 3% | 11.1% | 33.0% | −66% |
| About 6% | 7.5% | 22.9% | −67% |
| About 7% | 4.9% | 15.4% (exp004 twin bound: 17.3% at 6.6%) | −68% (−72% vs bound) |

Within-group AUROC of the per-stream maximum score:
- **Twin:** 0.992, the highest of any detector.
- **Released monitor signal:** 0.961.
- **DoC:** 0.981.
- **Dropout disagreement and ATC:** 0.987.

## What the alarm level actually is

**What it does.** It is one number per deployed setting: the conformal 95% quantile of the highest score that safe dev streams reach. It never uses a failing stream. Its implicit assumption is that held-out safe streams reach the same score heights as dev safe streams.

**It does not transfer.** The same 5% rule gave:
- 2.4% false alarms on exp006 (too high a level, so misses);
- 5.9% on exp005 Tent 1e-3;
- 7.6% on exp005 with both arms (too low a level).

**Why the level is too high on exp006.** The top safe dev streams combine a Dirichlet-0.1 class mix with saturate, spatter, speckle or shot noise.
- On those streams the twin is 3–24 points worse than Tent. Between 18% and 44% of images are flagged while Tent is correct.
- Example: OrganAMNIST's level is 0.416, while its median safe dev stream scores 0.114. The result was 0 of 62 false alarms and 12 of 40 missed.

**The score cannot separate the missed streams.**
- The estimated error (flag rate) is 0.467 on missed failing streams and 0.473 on quiet safe streams.
- The true errors are 0.345 and 0.298.
- The reason is that false flags (Tent correct but flagged) make up about 19–23% of images and vary more between streams than the true error does.

**A hypothesis that was wrong.** Early sampling noise does not inflate the level. The between-stream SD of the score is flat over time (0.059–0.062), and safe dev streams usually reach their maximum at the last checkpoint, because Tent drifts away from the twin.

**Where errors hide (three-model agreement).** On images where Tent and the twin agree but the frozen source model differs, Tent is wrong 60–78% of the time on failing streams. The twin flag catches these only when the twin is also uncertain.

## Candidate fixes

Each candidate is fitted and calibrated on dev streams only, out-of-fold by dev corruption where anything is fitted.

| Candidate | exp006 T1e-3 missed / FA | exp005 T1e-3 missed / FA | Matched 5% FA miss (exp006 / exp005) |
|---|---|---|---|
| Twin (frozen) | 13.1% / 2.4% | 2.3% / 5.9% | 7.5% / 3.5% |
| Twin, residual calibration | 25.2% / 0.9% | 23.3% / 0.0% | same ranking as twin |
| 3-model pattern estimator (10 non-negative weights) | 19.9% / 2.6% | 40.7% / 0.0% | 6.9% / 4.7% |
| Twin + pattern (standardised average) | 10.8% / 2.6% | 10.5% / 0.0% | **5.9% / 2.3%** |
| Twin + ATC + dropout fusion | 7.8% / 4.5% | 10.5% / 7.8% | 3.6% / 9.3% |

**Reading the table.**
- **Twin + pattern** ranks better than the twin on both sets. Its deployed level still transfers inconsistently: on exp005, false alarms fall to 0% while misses rise.
- **Fusion** helps exp006 but gives 15.4% false alarms on OrganAMNIST and 26.9% misses on DermaMNIST.
- **No candidate dominates on both sets.** The weak part is the transfer of the alarm level from dev corruption families to new ones, not the ranking signal.

## Directions supported by this

1. **Broader dev families.** Use many more synthetic dev families, including several class-mix levels, so that the dev safe distribution covers the deployment one.
2. **Conditional (Mondrian) calibration.** Set the level separately by a label-free stream descriptor, such as class-mix skew estimated from the twin and source predictions, or the source-BN input shift. Rescue-type dev streams then stop setting the level for every stream.
3. **Matched-FA, relative criteria in every frozen protocol.**

## laya (receptron/laya; convaiinnovations/laya)

**What it is.** A ModernBERT-large text decision model with 421M parameters. It takes a text or JSON state and typed questions and returns probabilities.

**What its model card says about it:**
- Base checkpoints are "near chance on typed-decisions zero-shot".
- It "ships over-confident", so users must refit temperatures on their own data.
- The act/escalate head "carries no usable signal yet".
- Fine-tuning is supported.

**Why it does not address conditions 3 or 4:**
- It would see the same numbers we already threshold, serialized as tokens, so it adds no information.
- The ranking is already 0.99 AUROC; the failure is threshold transfer.
- Fine-tuning a 421M-parameter text model on about 1,000 dev streams repeats the exp005 finding that learned detectors overfit dev corruptions.
- Its probabilities are calibrated on its own training data. Using them directly drops the conformal false-alarm statement, and conformalizing them reproduces the same transfer problem.

**The transferable idea.** Laya's per-bucket temperature refit, one temperature per question type and option count, is conditional calibration. That is direction 2 above, and it needs no language model.

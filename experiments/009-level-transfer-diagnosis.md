# 009: Why the dev-calibrated alarm level transfers unevenly, and a candidate fix (diagnosis, 14 Nov 2026)

**Status: EXPLORATORY.** Every held-out stream used here (exp005, exp006, exp008) had already been scored. Nothing below is a confirmatory claim. The fix chosen here is tested on fresh data in [exp010](010-family-validated-alarm-confirmation.md).

- Code and outputs: `diagnostics/2026-11-14-exp009-level-transfer/` (`cache9.py`, `lib9.py`, `diag1.py`–`diag6.py`, `harness.py`; `diag2.json`, `diag3.json`, `harness_rows.json`).
- Inputs: the saved per-image arrays of exp005, exp006 and exp008 (7,392 streams). No model was run. Run with `uv run --no-project --with "numpy<2" --with scipy python <script>` (uv-managed environment, not the system Python).
- Tent 1e-3 only; 19 deployed settings (dataset, checkpoint) with at least 19 safe dev streams.

## The problem being isolated

The level rule of exp006/exp008 is one number per deployed setting: the split-conformal 95% quantile of the highest score that safe development (dev) streams reach. Its realised behaviour on held-out shifts was uneven:

| Setting (twin, constant level) | Missed | False alarms |
|---|---|---|
| exp005 BloodMNIST / DermaMNIST | 1/45, 1/41 | 4/65, 2/37 |
| exp006 OrganAMNIST | 12/40 | 0/62 |
| exp008 OrganCMNIST | 17/53 | 0/49 |
| exp008 PneumoniaMNIST | 29/38 | 2/40 |
| exp008 CIFAR-100-C (six checkpoints) | 24/194 | 22/506 |

## Hypotheses and what the saved streams show

**H1. False alarms on a new family are not forecast by the other dev families.** Consistent with the data; not established.
- Leave-one-dev-family-out (LOFO): set the level on all other dev families, score the left-out family.
- Pooled LOFO false alarms were 2–7% per setting, close to the 5% target. But single families ranged from 0% to 52% (salt-and-pepper, 11/21, on one CIFAR checkpoint; speckle 4/10 on another).
- Across the 19 settings, LOFO false alarms did not predict held-out false alarms (Spearman −0.20 for the twin, 0.12 for the fusion detector).
- Reading (ours): streams within a family are not independent draws, so the bound α + 1/(n+1) with n counted in streams does not apply across families. With only 5–9 families we cannot tell whether families themselves are exchangeable, and 19 settings give a weak test of forecastability.

**H2. The misses are a power problem that is visible on dev before deployment.** Supported.
- LOFO missed share on dev predicted held-out missed share across settings: Spearman 0.73 (twin), 0.60 (fusion).
- PneumoniaMNIST: LOFO missed 27/87 for the twin; held-out missed 29/38. OrganAMNIST: 6/30 against 12/40. OrganCMNIST was the exception (4/61 against 17/53).

**H3. The level is set by a small tail of "rescue" streams.** Supported for both channels.
- On the top 5% of safe dev streams by twin score, the twin's error exceeded Tent's by 9.6 points on average (4 points over all safe dev streams). Tent is right and the twin is not, so the twin flags them.
- Example: OrganAMNIST's level is 0.416; the 95th percentile of held-out safe streams is 0.21 and the 10th percentile of held-out failures is 0.30. A level near 0.25 would have separated most of them, not all.

**H4. A second signal cancels this nuisance (my guess before looking). Rejected.**
- Tent's confidence drop (DoC) and the twin score are strongly correlated on safe dev streams (mean Spearman 0.81). The twin's top-5% safe streams sit at the 94th percentile of DoC as well.
- The tail of the fused score, relative to the safe-to-failing gap, was the same as either channel alone (0.53, 0.52, 0.51).
- So averaging signals does not remove the rescue-stream tail on dev. Any gain from fusion has another cause.

**H5. A constant level is the wrong shape for a signal whose safe distribution changes over the stream.** Supported for DoC under Tent.
- DoC's maximum over the 22 read-outs was in the first quarter of the read-outs on every stream of the six settings inspected (`diag4.py`), safe or failing, and its safe quantiles fall over the stream. This fits Tent raising confidence as it adapts; we did not run a control that separates Tent from the running average itself.
- So a constant level on DoC acts as a test on the earliest read-outs; later read-outs rarely reach it.
- The safe 95th percentile shrinks over the stream (OrganCMNIST: 0.10 at batch 11 to 0.03 at batch 116). Failing streams separate from safe ones only later there (held-out failing 10th percentile 0.04 against safe 95th percentile 0.03 at the end; 0.08 against 0.10 at the start).
- On CIFAR-100-C the opposite happens: failing streams' DoC falls below that of safe streams late in the stream, the masking effect of the paper's Sect. 5 seen in time.
- Standardising the score at each read-out time by the safe dev streams at that time (calibration Z of exp008) lets every read-out count. DoC misses fell from 18/53 to 0/53 on OrganCMNIST and from 11/40 to 2/40 on OrganAMNIST. Its false alarms rose above target on CIFAR (52/491 in exp006).
- The twin's score has no such drift, and Z did not help it.

**H6. No single channel has power everywhere.** Supported.
- Twin with a constant level: best on BloodMNIST and DermaMNIST (2/86 missed), weak on the Organ sets and PneumoniaMNIST.
- DoC with a time-resolved level: best on the Organ sets and PneumoniaMNIST (7/38), worse on DermaMNIST (7/41 missed, 7/37 false alarms) and on CIFAR false alarms.

## Candidate fix: choose the channel per deployment by family-wise validation

For each deployed setting, on its dev streams only:
1. Candidates: the twin with a constant level; DoC with a time-resolved level; the exp008 fusion detector (twin, ATC, dropout; unchanged).
2. For each dev family in turn, set levels on the other families and score the left-out family.
3. Deploy the candidate with the smallest LOFO missed share plus LOFO false-alarm share, with its level reset on all safe dev streams.
4. Report the chosen candidate's LOFO missed share as a blind-spot audit.

Held-out results on the three earlier experiments (all already seen, so descriptive):

| Rule | exp005 missed / FA | exp006 missed / FA | exp008 missed / FA |
|---|---|---|---|
| Twin, constant level (the earlier rule) | 2/86, 6/102 | 40/306, 14/578 | 76/351, 29/637 |
| DoC, time-resolved level | 8/86, 11/102 | 29/306, 52/578 | 23/351, 48/637 |
| Fusion (exp008 definition) | 9/86, 8/102 | 24/306, 26/578 | 36/351, 34/637 |
| Family-validated choice among the three (as frozen for exp010) | 2/86, 6/102 | 16/307, 36/578 | 22/351, 31/637 |
| Family-validated choice, twin or DoC only | 2/86, 6/102 | 21/306, 35/578 | 21/351, 33/637 |
| Published monitor | (exp005 record) | 149/306, 12/578 | 209/351, 22/637 |

- The choice was stable across three selection criteria and five candidate pools (`diag6.py`): missed 2–9%, false alarms 4–6% in every experiment.
- The exp006 and exp008 entries of the frozen row come from `analyze10.py`; the other rows and exp005 come from `harness.py`. `analyze10.py` counts one borderline OrganAMNIST stream as strict that the earlier scripts did not (307 against 306).
- PneumoniaMNIST stayed the weakest set (7/38 missed with DoC chosen).
- The exp008 fusion detector was written into the frozen exp008 analysis before exp008 ran, as a descriptive entry. Its exp008 numbers are therefore out-of-sample for that detector, though it was one of 41 descriptive entries and not the primary.

## What this does and does not establish

- It locates the failure: (a) a constant level on a signal that adaptation moves over time, (b) no single channel with power on every dataset, (c) family-level, not stream-level, exchangeability.
- It does not establish a fix. The family-validated choice was designed on these same held-out streams. Its test is exp010.
- Closest prior art for learned or calibrated label-free risk monitors, per the project library: `Amoukou2024SequentialHarmful`, `Garg2022ATC`, `Guillory2021DoC`, `Lee2024AETTA`. We have not found a family-wise validated choice of monitoring channel under adaptation, but the search was not exhaustive.

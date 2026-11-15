# Does a label-free TTA monitor miss risk under combined corruption and class-prior shift?

Experiment ID: **004-monitor-blind-spots**. Proposed **31 October 2026**.

Status: **Planned; not implemented or run. No result exists.** Rationale: [candidate B dossier](../outputs/candidate-b-dossier-2026-10-31.md).

## Questions

- **Q1 (gate):** on streams combining corruption and class-prior change, does the monitor of Schirmer et al. miss real risk violations on noncollapsed models, or over-alarm on benign prior shift?
- **Q2, only if Q1 passes:** does an independent label-free signal reduce misses at controlled false alarms, beyond accuracy-estimator and prior-correction baselines?

A failed Q1 is informative: it would extend that monitor's evidence to a harder setting, and candidate B′ would stop.

## Setup (proposed; freeze on development data)

**Monitor.** Inspect `github.com/monasch/tta-monitor` and pin a commit. Use its bound and calibration. A port or changed setting must be disclosed. It may assume a different dataset and model.

**Model and data.** The Experiment 003 checkpoint (SHA-256 `ce86bde2…`) and CIFAR-100-C, using the same 5,000 development IDs. Final IDs stay untouched. The monitor needs a labeled clean calibration set, so 2,000 clean development IDs serve as calibration and are excluded from streams. Because the checkpoint trained on all 50,000 training images, its training data cannot be used for this. Confirm that clean test order matches CIFAR-100-C first.

**Adaptation arms.** Source, plus a Tent-style update labelled as such unless the repository's implementation is used directly. A second arm is added only if the code provides one faithfully.

**Streams.** Noise and blur families, severities 3 and 5:

| Type | Purpose |
| --- | --- |
| Corruption, balanced | Reference, comparable to the authors' setting |
| Corruption plus class skew (Dirichlet) | Main test |
| Corruption plus easy-class-heavy skew | Tests masking |
| Clean plus class skew | Benign check: false alarms, unless risk truly rises |

"Easy" classes are defined from source accuracy on development calibration data. Labels build streams and score results offline only.

**Truth.** A violation is running risk above source risk plus the monitor's tolerance, measured with evaluator labels.

**Metrics.**

- **Missed alarm rate:** share of truly violating streams with no alarm.
- **False alarm rate:** share of non-violating streams with an alarm.
- **Delay:** batches between violation and alarm.
- **Assumption margin:** the Assumption 1 margin, computed with evaluator labels, plus false positive and false negative rates over time.
- **Collapse:** report results with and without collapsed streams, using the top predicted class share.

## Provisional gate

Q1 passes if, on noncollapsed streams, at least **20% of violating streams are missed**, or at least **10% of benign clean-skew streams raise a false alarm**, in at least two stream-severity cells with intervals excluding zero. Freeze before scoring anything beyond a code-path check.

## Cost

Roughly 84 streams. Proposed, and to be measured with a timing check: about 20 minutes on a single rented GPU, about $0.30. Recalibrating thresholds on 2,000 images is the main cost, and its frequency may need fixing. Create a new pod only for the run and delete it straight after.

## Amendments, 31 October 2026, after reading the code and before any stream was run

Monitor code inspected at commit `f200f00d4ca79567df0214bdd46150bb729c2227`. It is a research script tied to its own loaders, so the calibration and bound are **ported** into [`run_monitor.py`](../diagnostics/2026-10-31-exp004/run_monitor.py) and [`analyze_monitor.py`](../diagnostics/2026-10-31-exp004/analyze_monitor.py), and this is not a run of their entry point. Settings follow their CIFAR-100 Tent config, including the same ResNeXt architecture: Adam, lr 1e-3, batch 100, calibration 1,000 clean images recalibrated every batch, alpha 0.15, tolerance 0.1.

1. **Calibration is 1,000 images, not 2,000**, the repository default, drawn from development IDs.
2. **Streams:** the other 4,000 development IDs for three epochs, 120 batches. IDs repeat, and skewed streams also sample with replacement. Their confidence-sequence horizon assumption (`T_OPT` as 25% of the stream) is kept.
3. **Stream kinds:** balanced, Dirichlet(0.1) global skew, easy-class-heavy (80% on the 20 most accurate classes on calibration data), and by-class order, the authors' label-shift method. Clean versions use 3 repeats. 136 streams.
4. **The source arm is included** with a fixed threshold, as in their code.
5. **Code differences from the paper, as read:** the code's threshold omits the source finite-sample term, and its `compute_wn` returns `(log 2 - log alpha) / (2n)` with no square root, far narrower than a Hoeffding width. The paper's math was partly lost in text extraction, so this is **not yet confirmed as a bug**. Primary results use the released form. The square-root form is a sensitivity check only and cannot pass the gate.
6. **Truth and gate are fixed in `analyze_monitor.py`.** Violation: running error above `r0 + 0.1` at `t >= 10`. Collapse: last-quarter error at least 0.85.

## Actual results

**Run, 31 October to 1 November 2026:** 136 streams, development IDs only (noise and blur; clean), RTX 4090 RunPod pod, torch 2.4.1+cu124. Analysis in a separate Python 3.10 uv venv with confseq and NumPy below 2, because confseq would not build on 3.11. Outputs: [`results_monitor/`](../diagnostics/2026-10-31-exp004/results_monitor/). One stream, `source/impulse_noise/5/balanced/0`, hit a numerical failure and used the repository's predictable-mixture sequence instead. Calibration: source error `r0` 0.199, alarm threshold 0.299, source false-alarm rate 0.170.

**Q1 gate: passed by its frozen rule** (8 cells released form, 9 square-root form, all from missed alarms). No false alarm occurred on any of the 136 streams, in either form.

**The gate overstates the finding.** Its violation definition counts any running error above threshold at `t >= 10`, so marginal streams count. A stricter check added **after seeing the gate**, final running error at least 0.349 on noncollapsed streams, gives:

| Arm, stream | Mean error | Mean confidence | Strict violations | Missed | Mean PFN | Assumption fail share |
| --- | --- | --- | --- | --- | --- | --- |
| Tent, corrupted, Dirichlet | 0.392 | 0.910 | 9 | **9** | 0.278 | 0.001 |
| Tent, clean, Dirichlet | 0.416 | 0.936 | 3 | **3** | 0.340 | 0.000 |
| Tent, corrupted, balanced | 0.301 | 0.825 | 4 | 3 | 0.077 | 0.045 |
| Tent, corrupted, easy-heavy | 0.245 | 0.895 | 0 | 0 | 0.115 | 0.006 |
| Tent, corrupted, by-class | 0.783 | 0.630 | 13 | 0 | 0.143 | 0.000 |
| Tent, clean, by-class | 0.742 | 0.652 | 3 | 0 | 0.158 | 0.000 |
| Source, corrupted, balanced | 0.419 | 0.789 | 7 | 2 | 0.098 | 0.000 |
| Source, corrupted, Dirichlet | 0.413 | 0.792 | 7 | 2 | 0.099 | 0.071 |

**Interpretation:**

- **Main finding:** under persistent class skew, Tent's error rose while its confidence also rose, and the monitor missed all 12 strict violations. Tent on clean balanced data had 0.221 error; on clean Dirichlet it had 0.416.
- **Not a stream-length problem, in our reading.** Mean positive rate (0.115 to 0.177) sits below the source false-alarm rate (0.170), which is subtracted in the bound, so the bound stays near zero. Final gaps equal most or all of the error.
- **Supports our reading of Assumption 1:** it almost never failed on these streams while the monitor was blind.
- **By-class order, the paper's label-shift style, was caught in all 16 cases.** Persistent skew behaved differently here.
- Easy-heavy "misses" disappeared under the strict definition, so the masking example is not supported.
- Remaining balanced misses look like ordinary looseness close to the threshold, not a prior-shift effect.

**Exploratory signal check, Tent, excluding by-class streams, in-sample, no held-out data:** AUROC for strict violation was 0.441 for uncertainty, 0.791 for top predicted share and 0.836 for source-live disagreement. Source-live disagreement is already used by ASR and others. No threshold or false-alarm rate has been tested, so Q2 is **not answered**.

**Limits:** a port, not the authors' entry point; development IDs and noise/blur only; one checkpoint; one Tent configuration; Dirichlet(0.1) with one draw per stream and images sampled with replacement; 12 strict cases share images; strict definition added post hoc. Literature on Tent under label shift is extensive, so Tent's harm is known; whether the monitor's blindness has been reported is **not checked**. The paper's authors evaluated different settings, and this does not show their results are wrong.

### Confirmation protocol, frozen 1 November 2026 before running

Literature check (four web searches, selective reading): no paper found that reports this exact blind spot. The closest are `Han2026Exchangeability`, which shows adaptation hiding sustained changes from its own monitor in forecasting with revealed outcomes, and TTAB, which shows Tent degrading under Dirichlet label shift. Monitoring Risks §5.3 itself notes that a monitor relying on the model's own outputs "may become unreliable when the model itself fails". This is not a verified gap.

Pass rule and populations are fixed in [`analyze_confirm.py`](../diagnostics/2026-10-31-exp004/analyze_confirm.py), and streams in [`run_confirm.py`](../diagnostics/2026-10-31-exp004/run_confirm.py). Held-out weather and digital families, 4,000 final IDs. **Primary:** Tent, corrupted, Dirichlet 0.1. It is confirmed only if there are at least 10 strict violations; at least 75% are missed with a 95% lower bound above 50%; by-class misses are at most 20%; Assumption 1 failure share is at most 0.05; and Dirichlet error exceeds uniform-with-replacement error by at least 0.03. ETA, clean streams and other alpha values are descriptive. Note: the development data shaped this rule, and calibration reuses the 1,000 development images.

### Confirmation result, 1 November 2026

Run on a RunPod A40, torch 2.4.1+cu124: 285 streams in 7,691 s. Outputs: [`results_confirm/`](../diagnostics/2026-10-31-exp004/results_confirm/). **The frozen rule passed: confirmed for this setup.** Final IDs, held-out weather and digital families, same checkpoint. This pool has now been used once.

| Check | Rule | Result |
| --- | --- | --- |
| Strict violations, Tent, corrupted, Dirichlet 0.1 | at least 10 | 20 of 32 streams |
| Missed | at least 75%, lower bound above 50% | **20 of 20**, lower bound 0.83 |
| By-class control, missed | at most 20% | 0 of 13 |
| Assumption 1 failure share | at most 0.05 | 0.000 |
| Dirichlet minus uniform-with-replacement error | at least 0.03 | 0.096 (0.383 vs 0.287) |

Descriptive, same streams and seeds across arms:

| Corrupted streams | Mean error | Mean confidence | Strict | Missed | Mean final bound |
| --- | --- | --- | --- | --- | --- |
| Tent, Dirichlet 0.1 | 0.383 | 0.915 | 20 | 20 | 0.000 |
| ETA, Dirichlet 0.1 | 0.346 | 0.854 | 14 | 14 | 0.031 |
| Source, Dirichlet 0.1 | 0.371 | 0.760 | 15 | 1 | 0.297 |
| Tent, Dirichlet 0.5 | 0.311 | 0.867 | 1 | 1 | 0.065 |
| Tent, Dirichlet 1.0 | 0.300 | 0.855 | 1 | 1 | 0.085 |
| Tent, by class | 0.802 | 0.644 | 13 | 0 | 0.558 |

**Interpretation:** Tent and the unadapted source have similar error under strong skew, but the monitor catches the source and misses Tent, because adapted confidence is high. The effect is concentrated at strong skew: only 1 strict case at alpha 0.5 or 1.0, where error barely clears the threshold. ETA shows the same pattern, as a descriptive result, with entropy margin 0.4 ln 100 from the config comment; the config value itself reads 0.4.

**Signal check, exploratory:** across Tent streams without by-class, AUROC was 0.828 for top share, 0.702 for disagreement and 0.311 for uncertainty. **Within Tent Dirichlet 0.1 alone, top share falls to 0.537**, so it mainly detects skew, not harm. Disagreement is 0.746 and uncertainty 0.792 there, and across Tent and ETA they are 0.742 and 0.581. Development's 0.836 for disagreement did not hold. No alarm rule has been tested, so Q2 remains open.

**Limits:** one checkpoint and architecture, CIFAR-100-C, 120 batches, ported monitor, sampling with replacement, and a single Tent configuration. Twelve of 285 streams, one in the primary group, used the fallback sequence. The monitor's lower bound is not shown to be wrong: it stays valid but is too loose to alarm. Novelty remains unverified.

### Square-root question, resolved 1 November 2026

The paper's §B.1 gives `w0 = sqrt(log(1/alpha_source) / N_cal)` and a Hoeffding bound for the source false-positive term. The released code at the pinned commit uses `(log 2 - log alpha) / (2n)` with no square root for the `L_1` term, and its threshold is `r0 + tolerance` with no `w0`. So the code differs from the paper as written; both differences make alarms easier. We have not asked the authors, and do not know whether the paper's figures used this code. Since our released-form results already use the more alarm-prone version, it does not explain the misses.

### Second-model protocol, frozen 1 November 2026 before running

Modas2021 PRIME ResNet-18 (SHA-256 `737bf08d…`), loaded with strict keys. Same held-out streams, same seeds and the same frozen rule in `analyze_confirm.py`. Arms: source and Tent. **The final IDs are being reused**, after one earlier use on the first model. ETA is omitted. Files: [`run_second.py`](../diagnostics/2026-10-31-exp004/run_second.py), [`run_authors_check.sh`](../diagnostics/2026-10-31-exp004/run_authors_check.sh).

### Second-model result, 1 November 2026

RTX 4090, torch 2.4.1+cu124, 146 streams in 440 s after downloads. Outputs: [`results_second/`](../diagnostics/2026-10-31-exp004/results_second/). Three streams used the fallback sequence. **The frozen rule failed: the finding did not generalize to this model.**

| Check | Rule | Result |
| --- | --- | --- |
| Strict violations, Tent, corrupted, Dirichlet 0.1 | at least 10 | 24 |
| Missed | at least 75%, lower bound above 50% | **13 of 24 (54%), lower bound 0.33: fail** |
| By-class control | at most 20% | 16 of 16 collapsed, so no usable control cases |
| Assumption 1 failure share | at most 0.05 | **0.109: fail** |
| Dirichlet minus uniform-with-replacement error | at least 0.03 | 0.088 |

| Corrupted, Dirichlet 0.1 | Mean error | Mean confidence | Strict | Missed | Mean final bound |
| --- | --- | --- | --- | --- | --- |
| ResNeXt, Tent | 0.383 | 0.915 | 20 | 20 | 0.000 |
| PRIME ResNet-18, Tent | 0.443 | 0.587 | 24 | 13 | 0.328 |
| PRIME ResNet-18, source | 0.342 | 0.300 | 11 | 0 | 0.311 |

**Interpretation:** the direction remains, since Tent is missed more often than source, and all 3 clean Dirichlet streams were missed. But the near-total blindness did not transfer. This model's confidence is much lower, and mean positive rate under Tent (0.549) stays well above the source false-alarm rate (0.171), so the bound does not fall to zero. **Unverified hypothesis:** the blind spot depends on how confident the adapted model becomes. Two models cannot test that. Uses of the source arm here also showed more Assumption 1 failures and 5 alarms on 21 non-strict Dirichlet streams, some of which sit close to the threshold; these are descriptive.

**Authors' code check: did not run.** `monitor.py` at the pinned commit failed on import, `load_state_dict_from_url` from `torchvision.models.resnet`, with torchvision in the pod's environment. It needs an older torchvision. So the port has **not** been compared with their code. Their environment file was not used.

**Decision under the stated plan:** do not proceed to ImageNet-C.

**Cost:** balance $50.56 to $49.98 for this run; pod deleted automatically after the hash check.

### Confidence-dependence test, frozen 1 November 2026 before running

**Prediction:** across models, on corrupted Dirichlet 0.1 streams, Tent's missed share rises with its mean confidence. New models: Hendrycks2020 AugMix WRN-40-2, Addepalli2021 PARN18, Addepalli2021 WRN-34, Addepalli2022 WRN-34-10, all from the RobustBench CIFAR-100 corruption list. Same streams and monitor. The verdict rule is in [`analyze_models.py`](../diagnostics/2026-11-01-exp004-models/analyze_models.py): needs at least 3 scored new models and a confidence range of at least 0.15, or it is inconclusive; Spearman at least 0.8 on new models, at least 0.7 on all, and fixed miss shares at high and low confidence. **The final IDs are being reused again**, and the two earlier models suggested this prediction, so they are not independent evidence. Four to six models give a coarse check only.

The authors' code runs unmodified at the pinned commit in a separate uv venv, with torch 1.11 and torchvision 0.12 instead of their pinned 1.10 and 0.11.

### Confidence-dependence result, 1 November 2026

Run on an RTX 4090, torch 2.4.1+cu124; 584 streams; outputs in [`2026-11-01-exp004-models/`](../diagnostics/2026-11-01-exp004-models/). Key checks passed. The hash matched and the pod was deleted. Cost about $2.38.

**Frozen verdict: NOT SUPPORTED.** Spearman was 0.00 across new models (needed 0.8) and 0.20 across all six (needed 0.7), and the high/low confidence check failed. Confidence does not explain which models are missed.

| Model, Tent, corrupted, Dirichlet 0.1 | Confidence | Error | Tent missed | Source missed | Mean final bound | Source false-alarm rate |
| --- | --- | --- | --- | --- | --- | --- |
| Addepalli PARN18 | 0.417 | 0.520 | 11/16 | 6/10 | 0.394 | 0.172 |
| Addepalli WRN-34 | 0.582 | 0.503 | 18/18 | 4/9 | 0.143 | 0.259 |
| PRIME ResNet-18 | 0.587 | 0.443 | 13/24 | 0/11 | 0.328 | 0.171 |
| Addepalli WRN-34-10 | 0.605 | 0.478 | 8/17 | 2/10 | 0.357 | 0.147 |
| AugMix WRN-40-2 | 0.834 | 0.426 | 21/22 | 3/13 | 0.124 | 0.118 |
| AugMix ResNeXt | 0.915 | 0.383 | 20/20 | 1/15 | 0.000 | 0.170 |

**Post hoc, not part of any frozen rule:** Tent's missed share exceeds source's in **all six models**, pooled 91 of 117 (78%) against 16 of 68 (24%). Missed share tracks the final bound closely, but the bound is what triggers the alarm, so that is close to circular and is not an explanation of cause. Three of six models meet the original 75% miss threshold. Strict violation sets differ between arms, and the final IDs have been reused repeatedly, so this needs fresh confirmation. By-class control is only usable for the two AugMix models; the others collapsed on all 16 by-class streams.

**Authors' code: still not run.** The torch 1.11 environment worked on the GPU, but `monitor.py` failed on a missing `mpmath` that I left out of the dependency list. Not a problem in their code. Port still unverified.

### Tent-versus-source replication, protocol frozen 1 November 2026 before any stream ran

**Question:** does the post-hoc pattern from the six-model run hold on images not reused in that run? Six models, Dirichlet 0.1, noise and blur, severities 3 and 5, three draws per condition, shared by both arms. Stream images: the 4,000 development IDs. Calibration: the same 1,000 clean development IDs. Files: [`2026-11-01-exp004-replicate/`](../diagnostics/2026-11-01-exp004-replicate/).

**Rule, in [`analyze_replicate.py`](../diagnostics/2026-11-01-exp004-replicate/analyze_replicate.py):** a model is scored with at least 5 strict violations in both arms. Inconclusive with under 5 scored models. Replicated only if Tent's missed share is higher in at least 5 scored models and the pooled gap is at least 25 points. Reported outside the verdict: without AugMix ResNeXt, square-root form, draws where both arms violate, shares by excess error, bootstrap over models.

**Known limits, stated before running:** AugMix ResNeXt saw these images in earlier monitoring, and all models were seen on the final images, so the models themselves are not new. The rule comes from the result it tests. Tent and source can still violate on different draws, and a larger excess error is easier to detect, so a gap would not by itself show adaptation is the cause.

**Result, 1 November 2026: REPLICATED under the frozen rule.** RTX 4090, torch 2.4.1+cu124, 504 streams. Hashes matched and the pod was deleted. Cost $1.77. Tent's missed share was higher in all six models, pooled 147 of 166 (89%) against 44 of 110 (40%), a gap of 49 points. Outputs: `replicate_report.json` and `results_*/` in the folder above.

| Model | Tent confidence | Tent missed | Source missed |
| --- | --- | --- | --- |
| Addepalli PARN18 | 0.419 | 19/19 | 14/17 |
| PRIME ResNet-18 | 0.585 | 20/35 | 2/15 |
| Addepalli WRN-34 | 0.583 | 21/21 | 8/17 |
| Addepalli WRN-34-10 | 0.604 | 22/25 | 5/17 |
| AugMix WRN-40-2 | 0.830 | 33/34 | 6/22 |
| AugMix ResNeXt | 0.910 | 32/32 | 9/22 |

**Frozen side reports, outside the verdict:** without AugMix ResNeXt, 115/134 against 35/88, also replicated. Square-root form, 154/166 against 68/110, also replicated. Bootstrap over models, gap interval 0.32 to 0.62, coarse with six models. On the 97 draws where both arms violate, Tent alone was missed on 49 and source alone on 2; these draws share corruptions and models, so they are not independent. Missed by excess error: 0.15-0.25, Tent 103/111, source 40/67; 0.25-0.35, 38/49 against 4/17; above 0.35, 6/6 against 0/26. Tent's strict violations are not simply smaller, since it is missed more within each band, though Tent's few cases above 0.35 limit that band. 17 of 504 streams used the predictable-mixture fallback.

**Exploratory, after the verdict ([`compare_authors.py`](../diagnostics/2026-11-01-exp004-replicate/compare_authors.py)):** on strict streams, averaged equally over models, Tent and source error were similar (0.51, 0.54), while Tent had higher confidence (0.65, 0.38), a lower flagged rate (0.43, 0.62), and a higher share of wrong predictions unflagged (0.215, 0.097). The monitor can only see the flagged rate, so this is a candidate mechanism. It is not an isolated cause: Tent's threshold is recalibrated each batch and source's is fixed, so adaptation and recalibration are confounded here.

**Authors' code: ran for the first time, with a disclosed change.** At commit `f200f00`, `load_source_dataset` has no `cifar100` branch, although a CIFAR-100 config exists, so it cannot calibrate on this dataset as released. [`cifar100_calibration.patch`](../diagnostics/2026-11-01-exp004-replicate/cifar100_calibration.patch) adds a branch calling their `load_cifar100`. We used torch 1.11 and torchvision 0.12 instead of their pinned 1.10 and 0.11, plus `auto-attack`, `mpmath` and other undeclared installs. ResNeXt, Gaussian noise severity 5, seed 12. Applying our monitor formula to their saved outputs: uniform error 0.383, flagged 0.486, alarm at batch 45 of 100; by-class error 0.973, alarm at batch 7. Our port's development runs on the same corruption: error 0.391, flagged 0.516, alarm at batch 112 of 120; by-class error 0.815, alarm at batch 12. Streams differ (10,000 images once against 4,000 IDs three times) and calibration sets differ, so this shows broad agreement in alarm outcome, not an exact port check. **Their code has no Dirichlet stream option, so the blind spot itself has not been run through their pipeline.**

**Limits:** CIFAR-100-C only; one Tent configuration; six models already used to suggest the pattern; development images and families had shaped the earlier rule; Dirichlet images sampled with replacement; novelty unverified.

### Mechanism and authors'-pipeline test, frozen 1 November 2026 before any stream ran

Novelty check first: [`novelty-check.md`](../notes/novelty-check-2026-11-01/novelty-check.md). No direct report found; candidate gap, not verified.

**Mechanism run** ([`run_factorial.py`](../diagnostics/2026-11-01-exp004-mechanism/run_factorial.py)): six models, final IDs (reused), weather and digital, severities 3 and 5, Dirichlet 0.1, two new draws shared by arms. Arms: source, BN statistics only, Tent at 1e-4 and 1e-3. Each adapted arm is scored with recalibrated and fixed thresholds from the same logits. A frozen model recalibrates to the same threshold, so a recalibrating source arm would be identical and is not run. Calibration passes use autocast; other Tent passes do not.

**Authors' pipeline** ([`authors_stream.py`](../diagnostics/2026-11-01-exp004-mechanism/authors_stream.py)): their `evaluate()` with the disclosed CIFAR-100 patch, AugMix ResNeXt and WRN-40-2, Tent and source. Run-time replacements supply our exact replication draws 0 and 1 and our 1,000 calibration IDs, which also gives a batch-level port check.

**Rules, in [`analyze_all.py`](../diagnostics/2026-11-01-exp004-mechanism/analyze_all.py):** Q1 fixed-threshold Tent against source: gap holds if higher in at least 5 scored models and pooled gap at least 25 points. Q2 Tent against BN, recalibrated: entropy adds if higher in at least 5 and gap at least 15. Q3 BN against source: normalization suffices if higher in at least 5 and gap at least 25. Authors' pipeline: reproduced if at least 10 strict per arm, Tent missed at least 75%, gap at least 25 points and higher in both models. Port agrees if alarms match on at least 90% of streams and median error difference is at most 0.01.

**Result, 2 November 2026 IST (run finished 1 November, 19:21 UTC): all frozen verdicts below.** RTX 4090. 768 factorial streams and 112 authors' streams. Hashes matched and the pod was deleted. Pod spend about $4.30, plus $0.63 for the failed first launch.

| Frozen question | Comparison, missed/strict | Models higher | Pooled gap | Verdict |
| --- | --- | --- | --- | --- |
| Q1 fixed threshold | Tent 1e-3 fixed 109/109; source 18/73 | 6/6 | 0.75 | **FIXED GAP HOLDS** |
| Q2 entropy step | Tent 1e-3 recalibrated 94/109; BN recalibrated 37/154 | 6/6 | 0.62 | **ENTROPY ADDS** |
| Q3 normalization alone | BN recalibrated 37/154; source 18/73 | 2/6 | -0.01 | **NOT SHOWN** |
| Authors' pipeline | Tent 40/40; source 10/28 (per model, Tent 19/19 and 21/21; source 6/14 and 4/14) | 2/2 | 0.64 | **REPRODUCED** |
| Port check | Alarms match on 99.1% of 112 streams; median error difference 0.0003 | | | **PORT AGREES** |

**Frozen descriptive reports:** Tent 1e-3 recalibrated against source, 94/109 and 18/73, gap 0.62. Tent 1e-4 against source: recalibrated 81/140 and 18/73, gap 0.33; fixed 73/140, gap 0.28; each higher in 5 of 6 models. BN fixed against source, 47/154 and 18/73, gap 0.06, higher in 3 of 6. All six models were scored in every comparison. BN alone is uneven across models: recalibrated misses were 36/67 on the three Addepalli models and 1/87 on the others. 31 factorial streams and 4 authors' streams (5 port streams) used the predictable-mixture fallback.

**Execution deviations:** 15 authors' streams in the first attempt ran out of GPU memory beside the factorial. The rerun at 4 processes lost 51 ResNeXt streams to the same cause. Only streams without a row were rerun, at 3 processes then 2; two failed at 3 and succeeded at 2. No row was replaced, and the rule and draws did not change. Logs: `authors_progress*.log`, `authors_err*.log`.

**Exploratory, after all verdicts ([`explore_masses.py`](../diagnostics/2026-11-01-exp004-mechanism/explore_masses.py), `explore_masses.json`). Not frozen; enters no rule.** Strict streams, equal-weight model means; each arm has its own strict set.

| Arm and threshold | Error | Flagged | Flagged wrong | Unflagged wrong | Flagged correct | Missed with flagged − L1 ≤ alarm level |
| --- | --- | --- | --- | --- | --- | --- |
| Source | 0.530 | 0.653 | 0.458 | 0.072 | 0.195 | 6 of 18 |
| BN recalibrated | 0.526 | 0.645 | 0.452 | 0.074 | 0.193 | 16 of 37 |
| Tent 1e-4 recalibrated | 0.514 | 0.556 | 0.397 | 0.117 | 0.158 | 66 of 81 |
| Tent 1e-3 recalibrated | 0.508 | 0.434 | 0.297 | 0.212 | 0.138 | 87 of 94 |
| Tent 1e-3 fixed | 0.508 | 0.239 | 0.180 | 0.328 | 0.058 | 109 of 109 |

Error is similar across arms, but under Tent the flagged rate and the flagged-wrong share fall, and more errors go unflagged. Recalibration recovers part of this (flagged 0.239 to 0.434) but not all. In the recalibrated Tent 1e-3 arm, flagged rate falls from 0.479 in the first half to 0.389 in the second while error stays near 0.51. BN's split matches source's. Most Tent misses have a stream-average flagged rate too low to clear the alarm level, so a narrower confidence sequence alone would rarely rescue them at that rate; this is a stream-average summary, not a population limit. On draws where both arms violate: Tent 1e-3 against BN, Tent alone missed 77, BN alone 1 (108 draws; mean error difference -0.043); Tent against source, 38 and 0 (60 draws; -0.016); BN against source, 11 and 14 (71 draws; +0.026). Draws share models and corruptions, so they are not independent. Tent's misses also exceed BN's within each excess-error band that has enough streams (0.15-0.25, 65/74 and 34/87; 0.25-0.35, 27/31 and 3/57; above 0.35, 2/4 and 0/10).

**Interpretation:** the entropy step lowers the visible flagged rate without a matching fall in error, which reduces the monitor's detection power. These data support that specific mechanism; they do not identify which change in the network causes it, and they were analyzed after the verdicts. The monitor's false-alarm guarantee is not contradicted: non-alarms are not a theorem violation.

**Limits:** CIFAR-100-C only; Tent only; reused final IDs and pre-selected models; Dirichlet 0.1 with replacement sampling; each arm conditions on its own violations; torch 1.11 in the authors' arm, with the disclosed patch and run-time stream replacement. The Mahdiani SSRN preprint, which uses a BN-only control for conformal coverage, is unread beyond its abstract ([review](../notes/novelty-review-2026-11-02/review.md)). Novelty is not established.

### SAR extension, frozen 2 November 2026 before any SAR stream ran

**Why:** the finding is Tent only, and SAR is designed for skewed streams while still minimizing entropy. **Run** ([`run_sar.py`](../diagnostics/2026-11-02-exp004-sar/run_sar.py)): same six models, final IDs, weather and digital families, severities 3 and 5, Dirichlet 0.1 and draws as the factorial, whose source, BN and Tent arms are reused. SAR defaults from Niu et al.: SGD lr 0.00025, momentum 0.9, SAM rho 0.05, margin 0.4 ln(100), reset below EMA 0.2. Disclosed departures: BN models and all BN layers update.

**Rule** ([`analyze_sar.py`](../diagnostics/2026-11-02-exp004-sar/analyze_sar.py)): GAP EXTENDS TO SAR if SAR recalibrated is missed more than source in at least 5 scored models with pooled gap at least 25 points; otherwise NOT SHOWN. INCONCLUSIVE under 5 scored models. If any model lacks all 32 streams when the analysis runs, it is reported only as incomplete and enters no paper claim.

**Amendment before any SAR stream was scored or seen:** the original 10:30 IST cutoff was removed at the user's request, so the run may complete. No comparison, threshold or scoring rule changed. Run on an H100 80GB because RTX 4090s were unavailable; the comparators ran on an RTX 4090.

**Result, 2 November 2026: NOT SHOWN under the frozen rule.** All 192 streams finished; hashes matched and the pod was deleted. SAR recalibrated missed 47/159 against source 18/73, higher in 3 of 6 models, gap 0.05. Per model, SAR against source: AugMix ResNeXt 10/26, 2/17; PRIME 0/32, 3/11; AugMix WRN 1/28, 4/14; PARN18 5/24, 5/11; WRN-34 18/21, 3/11; WRN-34-10 13/28, 1/9.

**Descriptive:** SAR fixed 51/159 (gap 0.07). SAR against BN recalibrated 47/159 and 37/154 (gap 0.06, 3 of 6). No collapsed streams, 159 of 192 strict, 8 resets, 8 fallback streams. On draws where both violated, SAR alone missed 11 and source alone 14 (71 draws).

**Exploratory, after the verdict:** on strict streams SAR is close to BN: error 0.52, flagged 0.62, unflagged wrong 0.08, confidence 0.36 (BN 0.34; Tent 0.65). Share of samples kept by the margin: AugMix ResNeXt 0.69, AugMix WRN 0.72, PRIME 0.04, PARN18 0.06, WRN-34 0.08, WRN-34-10 0.09. On the four low-kept models, SAR may barely adapt, so this is **not evidence of a fix**. SAR's filtering, SGD optimizer and learning rate were not separated. Pod spend about $4.50, plus about $0.60 for an idle pod left by an interrupted launch.

**Exploratory additions, after all verdicts ([`explore_power.py`](../diagnostics/2026-11-01-exp004-mechanism/explore_power.py), `explore_power.json`):** counts reproduce the frozen tallies. Error capture on strict streams: source 0.86, BN 0.86, SAR 0.84, Tent 1e-3 recalibrated 0.57, fixed 0.35; lower for Tent than source on 6 of 6 models in both replication and factorial. Flag precision: 0.70, 0.70, 0.71, 0.68, 0.75. Gap intervals, factorial Tent vs source: corruption-within-model bootstrap 0.51 to 0.72, model bootstrap 0.42 to 0.78. Logistic adjusted miss difference for arm, controlling excess error and model: replication 0.46, factorial 0.60, Tent vs BN 0.59, BN vs source 0.01. Median first alarm among alarming streams: Tent 69, source 28 (factorial). False-alarm rates were not computed in this step.

**False-alarm check, exploratory, definitions written before computing ([`explore_false_alarm.py`](../diagnostics/2026-11-01-exp004-mechanism/explore_false_alarm.py), `explore_false_alarm.json`):** alarms on safe streams (mean error below r0 + 0.10, not collapsed): factorial source 1/81, Tent 1e-3 recalibrated 2/46, fixed 0/46, BN 0/8, SAR 0/7; replication source 0/81, Tent 3/34. Counts are small; BN and SAR have very few safe streams. See `same_three_models` in the JSON for separation on the three models where both arms have enough streams.

### Entropy-free twin monitor, frozen 2 November 2026 before any twin stream ran

**Why:** exploratory results show Tent's entropy step lowers the share of errors flagged, while BN keeps it. **Design** ([`run_twin.py`](../diagnostics/2026-11-02-exp004-twin/run_twin.py)): beside Tent, a no-gradient copy of the checkpoint uses test-batch BN statistics. Where predictions agree, Tent is wrong exactly when the twin is wrong. Statistic: P(twin flagged, agree) + w P(flagged, disagree) + c P(not flagged, disagree). Threshold and false-alarm terms are computed once on clean calibration images. **Tuning** uses noise and blur only, Dirichlet and balanced. **Verdict** ([`analyze_twin.py`](../diagnostics/2026-11-02-exp004-twin/analyze_twin.py)) uses weather and digital, same draws as the factorial, plus balanced and clean streams. FIX WORKS: missed lower in at least 5 of 6 models, pooled fall of at least 0.40, false alarms on all held-out safe streams at most 10%. PARTIAL: fall of at least 0.20, same limit. Otherwise NOT SHOWN.

**Result, 2 November 2026: FIX WORKS under the frozen rule, for the selected uncertified form.** 468 streams, H100; hashes matched and the pod was deleted. Dev selection chose w = 1, c = 1 (flag if the twin is uncertain or the models disagree). Held-out Dirichlet: missed 30/115 against released 94/109, lower in 6 of 6 models, fall 0.60. False alarms on all held-out safe streams 5/121 (Dirichlet 3/46, balanced 2/69, clean 0/6). Per model, fix against released: AugMix ResNeXt 0/21, 20/20; PRIME 0/25, 13/24; AugMix WRN 1/23, 22/22; PARN18 10/13, 12/12; WRN-34 12/16, 15/15; WRN-34-10 7/17, 12/16.

**Correction, found 2 November 2026 during the by-corruption breakdown:** the frozen analysis pooled 30/115 for the twin, but its strict streams included six clean Dirichlet streams that the released comparator (109 strict streams) never ran. All six alarmed. On matching corrupted streams the twin missed 30/109, a fall of 0.59 (model bootstrap 0.30 to 0.81); per model 0/20, 0/24, 1/22, 10/12, 12/15, 7/16. The frozen verdict is unchanged. Certified forms: 109/109 on those streams. See `explore_twin_matched.py`.

**The certified forms failed:** w = 0 missed 115/115 with c = 0 and with c = 1, with no false alarms. They are valid but useless here.

**Exploratory stress checks, after the verdict ([`explore_twin.py`](../diagnostics/2026-11-02-exp004-twin/explore_twin.py), `explore_twin.json`):** the selected statistic is a detector and not a lower bound: its stream-average value minus its correction exceeded Tent's error on 86% of AugMix ResNeXt streams, 26% AugMix WRN, 20% PRIME, 18% WRN-34-10, 2% WRN-34, 0% PARN18. When Tent was safe but the twin was strictly violating, it false-alarmed on 4/13. **No held-out stream had Tent strictly violating with the twin below the alarm level, so failures caused only by adaptation were not tested**; 4 had the twin in the band, none caught; one collapsed stream alarmed. Same draws both strict: fix alone missed 1, released alone 65, both 29, neither 14 (109 draws). Same safe Dirichlet streams: 3/46 against 2/46. Model bootstrap of the fall: 0.33 to 0.82. Same three Addepalli models: AUROC 0.94 against 0.788; 11/46 against 20/43 missed at 5% false alarms. The three Addepalli models remain weak: 29/46 missed. Median first alarm among alarms: batch 34. Same-draw Tent error differed from the factorial by a median of 0.0007 and at most 0.0077 across GPUs. Cost is 100 extra forward images per batch against 1,000 for per-batch recalibration; wall time was not compared.

**Interpretation:** this is a strong practical detector on failures shared by Tent and its entropy-free twin, which are nearly all the failures seen here. It is not a certified bound, and it has not been shown to catch adaptation-caused harm.

### Adaptation-harm test of the twin alarm, frozen 2 November 2026 before any harm stream ran

**Why:** the twin evaluation had no Tent violation with the twin below the alarm level. **Run** ([`run_harm.py`](../diagnostics/2026-11-02-exp004-harm/run_harm.py)): Tent at Adam lr 1e-2 and 5e-2 on clean and severity-1 snow, fog, contrast and JPEG, Dirichlet and balanced; by-class clean at lr 1e-3 and 1e-2. Twin statistic fixed at w = 1, c = 1; released monitor on the same streams. **Rule** ([`analyze_harm.py`](../diagnostics/2026-11-02-exp004-harm/analyze_harm.py)): target streams have Tent error at least r0 + 0.15, including collapse, and twin error below r0 + 0.10. Excluding by-class: INCONCLUSIVE under 20 target streams or 3 models; CATCHES HARM if the alarm fires on at least 75% and false alarms on safe streams are at most 10%; PARTIAL at 50%; otherwise NOT SHOWN.

**Result, 2 November 2026: NOT SHOWN under the frozen rule.** 132 streams; hashes matched and the pod was deleted. Target detection passed the 75% level, 51/61 (84%), but false alarms were 1/6 (17%), above the 10% limit; only 6 safe streams existed. **Descriptive:** released monitor 23/61 on targets and 3/6 false alarms. Certified forms 0/61 and 9/61. 56 of 61 targets collapsed; non-collapsed twin 3/5, released 2/5. By lr: 1e-2 twin 17/27, released 20/27; 5e-2 twin 34/34, released 3/34. 53 balanced and 8 Dirichlet targets. Per model, twin against released: AugMix ResNeXt 8/8, 4/8; PRIME 10/10, 5/10; AugMix WRN 4/5, 4/5; PARN18 7/12, 4/12; WRN-34 10/14, 0/14; WRN-34-10 12/12, 6/12. By-class clean: the twin also fails, so these are shared failures. **Design flaw, recorded after the verdict at the user's challenge:** the false-alarm limit had no minimum number of safe streams, unlike the target count. At n = 6, one alarm fails it and zero passes it; the exact 95% interval for 1/6 is 0.4% to 64%. The frozen verdict stays NOT SHOWN, and this test is read as uninformative on false alarms.

**Paper wording, at the user's direction:** the paper reports detection as passed*, with a footnote giving the frozen combined outcome and the design flaw, plus a future-work item. The record of the frozen verdict stays NOT SHOWN.

**Interpretation:** the alarm sees extreme collapse, but reliable detection of subtler adaptation-caused harm is not shown; at lr 1e-2 the released monitor did slightly better.

**By-corruption breakdown, exploratory (`explore_by_corruption.py`):** released monitor on Tent, missed/strict: brightness 3/3, contrast 10/15, elastic 14/15, fog 13/17, frost 19/20, JPEG 16/16, pixelate 13/14, snow 6/9; replication: defocus 9/11, gaussian 23/28, glass 26/31, impulse 28/31, motion 18/19, shot 19/21, zoom 24/25. Twin on matching streams: brightness 0/3, contrast 7/15, elastic 4/15, fog 1/17, frost 7/20, JPEG 4/16, pixelate 6/14, snow 1/9. Counts per corruption are small and share models.

### DermaMNIST-224 test, frozen 2 November 2026 before any medical stream ran

**Why:** the literature review found no report of this comparison in medical imaging, within its stated limits. **Data:** DermaMNIST-224 (CC BY-NC). One ImageNet-pretrained ResNet-18 trained on 5,507 training images; 1,000 reserved for calibration, 500 for checkpoint selection. Official validation images are a development sanity check; official test images are held out. MedMNIST has no lesion IDs, so patient-level separation cannot be proven; a near-duplicate check is reported. **Shifts:** synthetic corruptions written in this repo, a port rather than MedMNIST-C. Development: Gaussian noise, speckle, brightness. Held out: Gaussian blur, JPEG, contrast, pixelate, each at two severities, plus clean. Priors: natural, Dirichlet 1.0, Dirichlet 0.1. Three draws; 120 batches of 48. **Arms:** source, BN, Tent 1e-3 and 5e-3, SAR. **Monitors:** released, prototype distance (our port) and the twin rule fixed from the CIFAR test. Thresholds recalibrate every 5 batches, a disclosed speed choice. **Rules and code:** [`analyze_derma.py`](../diagnostics/2026-11-02-exp004-derma/analyze_derma.py), [`run_derma.py`](../diagnostics/2026-11-02-exp004-derma/run_derma.py). This is a controlled stress test, not a clinical result.

**Result, 2 November 2026:** 447 streams, H100; hashes matched and the pod was deleted. Source validation accuracy 0.835, r0 0.176. Frozen verdicts: blind spot REPLICATES (Tent 33/33, source 12/44, gap 0.73, corruption-severity bootstrap 0.44 to 1.00). ENTROPY ADDS (33/33 vs BN 12/35). Twin FALSE ALARMS NOT ESTIMABLE: 17/33 vs released 33/33, fall 0.48, but only 28 safe streams, below the frozen 40; all monitors 0/28 (upper 95% limit 12%). BEATS PROTOTYPE (prototype 33/33). SAR NOT SHOWN (14/35 vs 12/44). Adaptation-caused harm INCONCLUSIVE (1 target). Twin on BN missed more than released (20/35 vs 12/35). **Execution note:** Zenodo throttled the download, so it was restarted with parallel ranges and verified by MD5; the frozen code and rules did not change, and this was before any stream ran. **Exploratory (`explore_derma.py`):** both-strict draws, Tent vs source: Tent alone missed 23, source alone 0, both 7 of 30, error difference +0.02, flagged difference -0.28. Twin alone missed 0, released alone 16 of 33. Error capture on strict streams: source 0.67, BN 0.57, Tent 0.29. Streams excluded by the 0.85 limit: released alarmed on Tent 0/16, BN 12/14, source 3/10; twin on Tent 12/16. Twin median first alarm batch 84.5. Near-duplicates: about 1% of test images close to a training image; lesion IDs unavailable. Pod cost about $2.70.

**Confirmation-run cost:** balance fell from $54.99 to $50.56 for this run, including the pod's idle time until results were copied at 08:34 IST. Pod deleted.

**Earlier cost:** balance fell from $62.89 to $54.99 across Experiments 003 and 004, including idle time. The pod was deleted after the results were copied and the stream file's hash matched.

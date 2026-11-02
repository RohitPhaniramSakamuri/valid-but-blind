# Candidate B dossier: can we tell when a label-free risk signal has stopped working?

Date: **31 October 2026**. Status: literature attack, a saved-data look and a planned experiment. **No new model was run.** Selective reading and a targeted search, not a systematic review. No novelty is verified.

## 1. Verdict

| Version of B | Decision | Reason |
| --- | --- | --- |
| A universal unlabeled test that proxies are valid | **Reject** | Impossible without restrictions (§3). |
| A signal that predicts how wrong the proxy is | **Reject as a separate contribution** | That is an unlabeled accuracy estimator, which is crowded (§4). |
| **B′: monitor blind spots.** Does a label-free TTA monitor stay silent when combined corruption and class-prior shift raise risk, and does an independent signal close the gap? | **New working candidate; unverified** | Narrow, measurable and cheap to refute (§5). Monitoring Risks may already handle it. |

## 2. What the closest paper actually leaves open

**Intuition.** A monitor without labels watches a stand-in for error, such as low confidence. It needs that stand-in to keep pointing at real errors.

Schirmer et al. (`Schirmer2025Monitoring`) build a sequential lower bound on the risk of an adapting model, with `1 - max probability` as the proxy. Passages read:

- **§6:** "verifying Assumption 1 for a given loss proxy still requires a labeled test stream" and "developing unsupervised diagnostics to flag potential violations of the assumption remains an important direction for future work."
- **§5.2:** the assumption "is generally satisfied in practice", with one persistent exception, the static source model on ImageNet severity 5.
- **§3.4:** proxy thresholds are recalibrated on a **labeled source calibration set** using the adapted model. So the method needs held labeled data and repeated forward passes.
- **§A.5:** label shift was tested on Yearbook by reordering the stream. This is the only explicit label-shift experiment in what we read.
- **§A.4:** the assumption of the similar Amoukou et al. bound is reported as "violated in nearly every practical setting".

**Assumption 1 in plain terms.** Averaged over time:

`false alarms from the proxy now <= false alarms at source + misses from the proxy now`

**Our reading (not stated by the authors):** misses appear on the right-hand side, so the assumption becomes **easier to satisfy as the proxy misses more errors**. A confidently wrong model can satisfy it. The assumption protects against false alarms, and it does not establish that the monitor will notice a problem. So there are two different failures:

| Failure | Meaning | Covered by Assumption 1? |
| --- | --- | --- |
| Over-alarm | Proxy says "bad" on correct predictions | Yes, this breaks validity |
| Blind spot | Risk rises while the proxy stays quiet | No, the bound stays valid but too loose |

The authors do evaluate detection empirically: alarms within 25 steps on ImageNet-C severity 5, and collapse detection. So the blind spot is a hypothesis about harder settings, not a known defect.

## 3. The limit on any diagnostic

**Concrete example.** Take two deployments with identical images and an identical model, but different true labels for those images. Every label-free signal is identical in both, yet the risk differs. So no unlabeled test can work for all shifts.

Prior statements: Garg et al. (`Garg2022ATC`, already in our library) on the need for assumptions, and Solozobov (`Solozobov2026Governance`), who reports zero change in all proxy metrics under pure concept drift. Any claim here must therefore name its shift family. B′ is limited to label-preserving corruption plus class-prior change, with no new classes.

## 4. Closest sources

| Source | Passage | Already covers | Does not cover, in what we read |
| --- | --- | --- | --- |
| **Monitoring Risks** | §§3.3–3.4, 5.2–5.3, 6, A.4–A.5 | Monitor for adapting models; collapse detection; one label-shift test | Unlabeled diagnostics for its assumption; large-class combined corruption and prior shift |
| **Amoukou et al.** (`Amoukou2024SequentialHarmful`) | Abstract, Assumption 4.1 | Label-free harmful-shift detection with a trained error estimator, including covariate and label shifts | Adapting models |
| **D3M** (`Nguyen2025D3M`) | Abstract, §5 | Disagreement-based deterioration monitoring with false-positive control | TTA; authors note noisy results at small query sizes |
| **AETTA** (`Lee2024AETTA`) | Read earlier | Accuracy estimation under adaptation failure | Sequential alarms |
| **Entropy Enigma** (`Press2024EntropyEnigma`) | Read earlier | Accuracy estimation from flips during adaptation | Sequential alarms |
| **POEM** (`Bar2024ProtectedTTA`) | Future directions | Its monitor might react to label shift and trigger needless adaptation; suggests remedies | An evaluated solution, in what we read |
| **PPRM** (`Zhang2026PPRM`) | Abstract | Semi-supervised monitoring with few true labels | Fully unlabeled operation |
| **Discern** (`Balachandran2026Discern`) | Abstract | Certifies updates from disagreement, labeling only disagreements | Label-free verdicts on harmful updates; continuous TTA |
| **Solozobov** | Abstract | Combined proxy monitors; concept-drift blind spot | TTA; independent preprint on credit data |

**Why predicting proxy error is crowded.** If a signal can say how far confidence is from true error, it can correct the estimate, which makes it an accuracy estimator. ATC, DoC, AETTA, Weighted Flips, GdScore and D3M already occupy that space, so B′ must add something beyond estimation: for example, a sequential alarm with stated false-alarm behaviour in the blind-spot regime.

**Not obtained or not read:** the `monasch/tta-monitor` code; full texts of the newly added papers; SLRF. Web searches found no unlabeled diagnostic for this assumption in TTA, which is weak evidence.

## 5. Candidate B′

**Exact question.** With no target labels at runtime and a labeled source calibration set, as in Schirmer et al.: on streams combining corruption and class-prior change, how often does the monitor miss a real risk violation on noncollapsed models, and how often does it over-alarm on benign prior shift? Does an independent signal reduce misses without breaking false-alarm control, beyond what an accuracy estimator would give?

**Why it might matter.** Skewed class streams are a standard hard case in TTA, and they could affect uncertainty in either direction. Example: a stream of mostly easy classes lifts confidence and may hide corruption damage on rarer classes. The reverse case is a stream of hard classes, which could lower confidence and raise an alarm even though nothing has broken.

**Saved-data hint, weak.** From Experiment 003's rows (balanced classes, one fold and seed, development data, batch-level confidence), `1 - confidence` underestimated error by about 19–21 pp on stationary streams. KEEP error exceeded source by over 5 pp with confidence at or above source in 7–9% of those harmful states. These rows use support-batch confidence, not the monitor, and contain no class-prior shift. They show only that this is worth testing. Change-stream figures are excluded because support and query differ there.

## 6. What would refute B′

1. The real monitor rarely misses violations in these streams.
2. Misses occur only in collapse, where concentration already gives it away, or at thresholds no one would use.
3. Label-free prior correction (BBSE-style) or a simple concentration signal closes the gap, which would make this known prior correction.
4. The added signal only works as an accuracy estimator, with no gain over AETTA-style or disagreement baselines.
5. Later work already reports it.

**Most likely failure (our expectation):** outcome 1. The authors report prompt detection, and the sequential running risk may absorb a lot.

## 7. Next step

[Experiment 004](../experiments/004-monitor-blind-spots.md) tests refutation 1 first, using the authors' released code once inspected.

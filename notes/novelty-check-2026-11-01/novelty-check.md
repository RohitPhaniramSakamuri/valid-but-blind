# Novelty check: monitor blind spot under class skew

Date: 1 November 2026. Scope: web searches, arXiv listing search and targeted reading of the passages below. This is not a full citation audit. No Google Scholar "cited by" list was reviewed.

**Claim checked:** under strong non-collapsing class skew plus corruption, the Schirmer et al. monitor misses Tent's risk violations much more often than a frozen model's, across models.

**Result: no direct report found. The gap is a candidate and is not verified.** Each ingredient is already known:

| Source | Covers | Does not cover, in what we read |
| --- | --- | --- |
| `Schirmer2025Monitoring`, §A.5 | Label shift on Yearbook through class-ordered streams. Reports earlier alarms and says the framework "effectively captures failures of TTA methods caused by label shift". Future work asks for unlabeled diagnostics of Assumption 1. | Non-collapsing skew on a large-class dataset; comparison of missed violations with a frozen model |
| Amin and Kim, "The Over-Certainty Phenomenon", arXiv 2404.16168 (TMLR 2025) | TTA methods become over-certain, with calibration harm and misplaced trust | Effect on a risk monitor |
| Nam et al., "Style Invariance as a Correctness Likelihood", arXiv 2512.07390 | TTA overconfidence and calibration in dynamic streams | Sequential alarms. Its Dirichlet stream correlates corruption types, not class priors |
| `Han2026Exchangeability` | Self-monitoring can hide shifts or give invalid alarms | Forecasting and betting gates, not this monitor or classification under class skew |
| `Lee2024AETTA`, `Press2024EntropyEnigma` | Label-free accuracy estimation under adaptation | Sequential alarm miss rates. A keyword search found no class-skew evaluation in AETTA's stored text; that is weak evidence |
| `Bar2024ProtectedTTA` | Monitor reactions to label shift | The opposite concern: needless adaptation |

**Our interpretation:** the over-certainty mechanism is not new, so the possible contribution is narrow: its measured consequence for label-free sequential monitoring, in a setting where that monitor's own appendix reports good detection on a different label-shift form. Schirmer et al. tested a different dataset and stream, so the result does not contradict their theorem or show their experiments are wrong. Our Assumption 1 failure shares were low, so validity held while detection failed.

**What could overturn this:** an unindexed or very recent paper, or a citing paper that we did not find. Search tools did not return any 2026 paper citing Schirmer et al., which is weak evidence.

Sources are in [`evidence/`](evidence/). These were read only in the passages named, not in full.

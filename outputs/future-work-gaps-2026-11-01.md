# Finding gaps from future-work sections

Date: **1 November 2026**. Status: literature pass only. **No model was run.** Method: keyword extraction of future-work and limitation sentences from 42 arXiv papers from 2024 onward in our library (`notes/future-work-mining-2026-11-01/passages.json`), selective reading of the passages that mattered, and targeted web searches. This is not a systematic review, and some entries rest on search summaries, marked below. No gap is verified.

## 1. Is there an easier way to novelty?

**Yes, with a cost.** Everything we tried so far competed on the same crowded question: how to decide when and how to adapt. The cheaper route is to **ask a well-established question about an outcome that TTA papers rarely measure**. New methods need to beat strong baselines. A measurement study needs a clear question, a controlled comparison and a result that matters.

Costs of this route:

- A study of this kind has a narrower contribution than a new method, and may suit a workshop or a specialist venue better. We cannot promise any outcome.
- A future-work sentence is only a lead. Authors list what they did not do, and others may already have done it.
- Being new is not the same as being useful. The result has to change what someone would do.

## 2. Questions asked of the future-work passages

| # | Question | Source of the question | What already exists | Assessment |
| --- | --- | --- | --- | --- |
| 1 | **Does online adaptation widen error gaps between demographic groups?** | `Launay2026FairTPT` studies **episodic** VLM adaptation and says online is not its focus. TTAB observes worst-group effects on Waterbirds. | FairTPT (episodic CLIP); FairDomain (DA/DG, not TTA; from a search summary); TTAB Waterbirds (spurious correlation, not demographic). Two targeted searches found no direct study. | **Best lead.** Candidate gap. |
| 2 | Is there a label-free signal that tracks correctness when a many-class model is overconfident? | `Rehan2026FORGE` §4.6, `Singh2026ReliabilityGated`, `Huang2026TTABC`, and our Experiment 004 | AETTA, Entropy Enigma, DeYO, style-invariance and more (search summaries for the last) | Important and repeatedly requested, but hard and crowded. |
| 3 | Does a prediction set still cover the truth while the model adapts? | `Kasa2024EACP` raises it | EACP, QTC, CUI/TUI, CPATTA (partly search summaries) | **Crowded.** Already closer than it first looked. |
| 4 | Do condition-level help and harm patterns carry over to other datasets? | `Majumdar2026HelpHarm` §7: CIFAR-100-C and ImageNet-C untested | That study on CIFAR-10-C | Easiest, but low value: an extension. |
| 5 | Does calibration get worse after TTA, and can it be fixed without labels? | Several | EATA-C, ZAEC, ranked entropy (search summaries) | **Crowded.** |
| 6 | Can we monitor without labels when the model is confidently wrong? | `Schirmer2025Monitoring` §6 | Experiment 004 here | Tested; model-dependent. Pause. |

## 3. The recommended candidate

**Question:** when a deployed classifier adapts online without labels, does it widen error gaps between demographic groups, and does the make-up of the incoming stream drive this?

**Intuition.** Batch-norm adaptation learns from whoever is in the batch. If most images come from one group, the adjustment suits that group best.

**Example.** A face-attribute model adapts to a new camera on a stream with 90% of one group. Overall accuracy rises, while the 10% group's accuracy falls. An average-accuracy report would call this a success.

**Why this may be worth doing (our reasoning).**

- It would change a deployment decision: average accuracy could approve an update that harms a group.
- It connects to what we measured: Experiment 004 showed class skew strongly affects adaptation. Group make-up is a similar skew. That analogy is untested.
- It connects to Review II: harmful updates hidden by an average.

**Closest work and the remaining difference:**

| Source | Covers | Difference |
| --- | --- | --- |
| `Launay2026FairTPT` | Episodic prompt tuning on CLIP; reports worsened disparities | Online, persistent-state adaptation on standard classifiers; effect of group make-up |
| `Zhao2023Pitfalls` | Waterbirds worst-group error across TTA methods | Spurious correlation benchmark, not a controlled demographic-mix study |
| `Tian2024FairDomain` | Fairness under domain shift, DA/DG, medical imaging | Not test-time adaptation (search summary only) |
| `Lim2026ASR`, `Weerasinghe2026LATTA`-style imbalance work | Class imbalance | Class imbalance is not group imbalance: group labels are unknown and may not align with classes |

**What would refute it:**

1. Gaps do not change beyond noise.
2. Gaps change only because overall accuracy changes.
3. A simple control removes it, such as frozen BN statistics, or balancing already covered by NOTE or TRIBE.
4. A paper we missed already reports it. A follow-up search on medical imaging and face analysis is still needed.

**Limits to state upfront:**

- Demographic attributes in public datasets are imperfect labels and raise ethical concerns, so they must be used carefully and evaluator-only.
- Corrupted faces are a controlled test, not a real deployment.
- Fairness metrics can disagree with each other. One must be chosen in advance.

## 4. Smallest test (planned only, not authorized)

CelebA with a standard target attribute and group attribute, a source ResNet trained once, Source, BN-statistics, Tent and ETA arms, and corruptions held out. Vary the stream's group mix: natural, 90/10 each way, and balanced. Fix labels and groups as evaluator-only, score on a balanced held-out set, and report worst-group accuracy and the gap. Pass rule to be frozen first. Dataset access and cost are not verified; CelebA's official hosting has had download limits.

## 5. Other things found

- `Majumdar2026HelpHarm`: per-batch reliability modulation is posed but unanswered.
- `Huang2026TTABC`: leveraging shifted label priors as evidence is an open direction for CLIP.
- `Rehan2026FORGE`: its adaptation gate never fires on Tiny-ImageNet-C because the model is overconfident, which matches our concern from Experiment 004 in a different setting.

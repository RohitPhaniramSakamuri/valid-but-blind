# Does online adaptation harm whichever demographic group is the minority in the stream?

Experiment ID: **005-group-gaps-under-online-adaptation**. Protocol frozen **1 November 2026 before any data was processed**.

Status: **Run; rule not met. See Actual results.** Rationale: [gap review](../outputs/future-work-gaps-2026-11-01.md).

## Question

When a binary classifier adapts online without labels, does a demographic group's balanced accuracy fall when that group becomes a small share of the stream, beyond what a frozen model shows on the same sampled images?

**Why balanced accuracy:** the average of accuracy on positive and negative examples within a group. It stops a group's score moving just because its class mix differs.

## Data and ethics

CelebA aligned images via the `flwrlabs/celeba` Hugging Face mirror, an unofficial copy of a dataset released for non-commercial research. Official split sizes (162,770 / 19,867 / 19,962) and identity disjointness are checked by the script. Center-cropped and resized to 96 × 96.

`Male` is a binary annotated attribute, not a measure of anyone's identity. It serves as a research grouping, as in earlier group-robustness work. Group labels are used by the evaluator and to build streams, never by the models or adaptation.

**Targets:** primary `Blond_Hair`; secondary `Smiling`.

## Models

ResNet-18 with ImageNet weights, trained on the train split with plain cross-entropy, no group information: SGD lr 0.01, momentum 0.9, weight decay 1e-4, 5 epochs, batch 256, horizontal flips. **Three seeds per target.**

## Adaptation arms

Frozen source; BN (batch statistics); Tent (Adam, lr 1e-3, batch statistics, BN affine); ETA-style (Tent plus entropy margin 0.4 ln 2, no redundancy filter, because cosine redundancy is uninformative with two classes; not native ETA); BN-blend (descriptive: 50/50 source and batch statistics).

## Streams

**Mix:** share of `Male` in {10%, natural, 50%, 90%}. Within a group, images are drawn uniformly, so P(class | group) stays natural. Sampling is with replacement. 150 batches of 64, 2 repeats. Sampling is identical across arms for pairing. Adaptive state resets per stream.

**Corruptions:** my own ImageNet-C-inspired implementations at one fixed strength, not the official benchmark.

- Development pool (validation split, descriptive only): Gaussian noise, Gaussian blur.
- Final pool (test split, held-out families): contrast, brightness, pixelate, haze.
- Clean also runs in both, descriptive only.

## Metrics and frozen rule

For a model, corruption and arm, the **composition effect** is:

`CE = mean over both groups of [BA of group g when g is 10% of the stream − BA of g in the 50% stream]`

**DiD** is CE for an adaptive arm minus CE for the frozen source. The frozen source's predictions do not depend on the batch, so its CE reflects sampling only.

Intervals: two-way bootstrap over model seeds and corruptions (few clusters, so read cautiously).

**SUPPORTED** for an arm (BN or Tent, final pool, `Blond_Hair`) only if all of these hold:

1. DiD ≤ −2 percentage points, with the 95% interval below 0.
2. DiD is negative in all 3 model seeds.

**GENERALIZES** if the same arm is also SUPPORTED on `Smiling`.

Descriptive: natural-mix gap versus source, worst class-group cell, ETA and BN-blend, per-group effects.

## What would refute it

Rule not met; or an effect only on one target; or BN-blend removing it cheaply. A pass would still leave novelty unverified and is one dataset with a coarse group attribute.

## Files

[`run_fair.py`](../diagnostics/2026-11-01-exp005/run_fair.py), [`analyze_fair.py`](../diagnostics/2026-11-01-exp005/analyze_fair.py), [`pod_fair.sh`](../diagnostics/2026-11-01-exp005/pod_fair.sh).

## Actual results

**Run, 1 November 2026:** RunPod RTX 4090, torch 2.4.1+cu124, uv venv with system site packages, `pyarrow==17.0.0`. 1,920 streams in 2,475 s. Split sizes and identity disjointness passed. Outputs: [`results/`](../diagnostics/2026-11-01-exp005/results/); checkpoints were not retained. Pod deleted after the hash check. Cost about $0.85.

**Frozen rule: not supported for BN or Tent, so it does not generalize.**

| Final pool | DiD (pp) | 95% interval | Seeds negative | Rule |
| --- | --- | --- | --- | --- |
| Blond_Hair, BN | -4.15 | -7.19 to 0.04 | 3 of 3 | Fail, interval touches 0 |
| Blond_Hair, Tent | -3.53 | -6.23 to 0.03 | 3 of 3 | Fail, interval touches 0 |
| Blond_Hair, ETA-style (descriptive) | -5.23 | -8.52 to -1.12 | 3 of 3 | Not a rule arm |
| Smiling, BN | -0.49 | -0.90 to -0.09 | 3 of 3 | Fail, below 2 pp |
| Smiling, Tent | -0.15 | -0.74 to 0.40 | 2 of 3 | Fail |

**Design flaw found on reading the results.** Keeping P(class | group) natural means changing the group mix also changes the stream's class mix, when class and group are correlated. Blond hair is far more common in the non-Male group. So this was not a clean test of group composition.

The data point to class prior, not minority status (our interpretation; no clean test run):

- Under BN on Blond_Hair, **both** groups improve as Male share rises: Male 62.4 / 73.1 / 78.8% and other 84.9 / 89.2 / 91.2% at 10 / 50 / 90% Male. A minority-harm effect would make the groups move in opposite directions.
- Blond recall rises and non-blond recall falls with Male share, which fits batch statistics shifting with class prior.
- Smiling, nearly balanced within groups, shows a very small effect.

**At natural mix (final pool, Blond_Hair):** gap 17.18 pp for source, 18.67 BN, 19.59 Tent, with no intervals computed. Both groups' balanced accuracy rose substantially, and the worst cell improved from 18.3% to 40.1% under BN. So adaptation helped both groups here, and the gap existed before adaptation (clean source: 69.5% vs 90.9%). On Smiling the gap fell slightly or stayed about the same.

**Other limits:** own corruption implementations, one fixed strength, coarse binary group, unofficial data mirror, sampling with replacement with few blond-Male images, and only 3 seeds and 4 corruptions for the bootstrap. Development results were inconsistent: BN +0.95 and Tent -5.54 on Blond_Hair.

**Decision:** the candidate, as stated, is not supported. A rerun holding class mix fixed is possible, but Smiling already approximates that condition and shows little effect, so it is not recommended.

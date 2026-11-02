# The Entropy Enigma: Success and Failure of Entropy Minimization

Citation key: `Press2024EntropyEnigma`
Authors, year, and venue: Ori Press, Ravid Shwartz-Ziv, Yann LeCun, Matthias Bethge; 2024; ICML 2024, PMLR 235.
Authoritative link: https://arxiv.org/abs/2405.05012
Status: Venue from the footer of arXiv v2; PMLR page not separately opened.
Reading progress: 2026-10-31: arXiv PDF abstract, introduction and §4 opening.

## What the inspected passages cover

Explains early success and later failure of entropy minimization; estimates dataset accuracy from weighted prediction flips during adaptation. Locations: Abstract, Section 4.

## Limitations for our use

Dataset-level accuracy estimation, not stream action selection.

## Connection to our research (our interpretation)

Close predecessor for evidence behaviour under adaptation. See the [dossier](../outputs/novelty-dossier-2026-10-31.md).

## Next reading step

Read the remaining sections before relying on this source for any claim beyond the passages above.

## Adversarial review — 2 November 2026

Ori Press, Ravid Shwartz-Ziv, Yann LeCun, Matthias Bethge. 2024. ICML 2024, PMLR 235. [Primary source](https://arxiv.org/abs/2405.05012).

Publication/version qualification: Venue from the footer of arXiv v2; PMLR page not separately opened

**Actual reading:** §§4.1–4.4 selectively reread in final close-work audit; offline fitted weighted-flip estimator and its initial-model dataset-accuracy target checked.

**Locations:** §§4.1–4.4

**Method/evidence and connection:** Prediction-flip accuracy estimation during entropy adaptation is prior art; estimates initial/source dataset accuracy with offline labeled fitting, not current-model sequential risk.

**Limit:** Dataset-level accuracy estimation, not stream action selection.

**Next reading step:** resolve access/version limits and the precise C1–C5 overlap before stronger claims. [Detailed claim review](../notes/novelty-review-2026-11-02/review.md); [source-level reading and extraction](../notes/novelty-review-2026-11-02/review.md). No experiments were run for this reading.

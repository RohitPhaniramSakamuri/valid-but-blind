# Core source model and adaptation semantics

Created and run 23 October 2026 using existing CPU libraries. This is a controlled mechanism demonstration on sklearn's bundled digit images. It does not reproduce native Tent, CIFAR-C, an original paper architecture, or a novel research contribution.

## Source model

- Ten digit labels, 0–9; 1,797 images, each 8 × 8; pixel values divided by 16.
- Stratified source fit: 900 images. Independent meta-training: 400; meta-calibration: 200; final test: 297. `splits.json` stores original dataset row IDs.
- An MLP classifier fits source labels with one 32-unit ReLU layer. Its hidden encoder is retained; source-only hidden mean/variance define a normalization layer. A separate multinomial logistic head is refit using source-normalized hidden activations and source labels.
- Only source-fit labels train the encoder/head. All values used to construct source normalization come from that fit partition.
- Fixed seed 241023. Encoder L-BFGS max iterations 250, alpha 0.01; logistic head C = 1 and max iterations 500. The encoder reached the iteration limit; its warning is recorded. No checkpoint was selected using final outcomes, and no refit was performed to hide the warning.

## Terminal actions

`SOURCE` predicts with source normalization and fixed encoder/head.

`BN` obtains hidden mean and variance from the current support batch, then freezes those values for prediction on a separate query batch. This is a support-statistics normalization adaptation, not a literal full-network BatchNorm reproduction.

`ENTROPY` starts from the same support-statistics normalization. It initializes affine scale gamma = 1 and bias beta = 0, takes three fixed support-only prediction-entropy gradient steps at learning rate 0.05, then scores query inputs with fixed adapted affine values and support statistics. Encoder/head weights never change. This is a Tent-derived affine entropy action, not the native Tent implementation or its original benchmark protocol.

The entropy-gradient direction is analytic. For each logit probability p and sample entropy H, the derivative is `-p * (log(p) + H)`, averaged over the support batch. The independent diagnostic audit checked gamma/beta gradients by finite differences.

Every call creates local normalization/affine state. Query computation never changes support statistics or model arrays. Terminal actions share the identical source state and support/query cases for comparison.

## Evidence

Cheap evidence includes prediction-entropy/confidence/margin summaries, predicted-class frequencies, and normalized hidden-feature means and standard deviations from one frozen-source support pass. No true support labels, corruption identity or severity are features.

Rich evidence adds a globally fixed pair of mild left/right horizontal subpixel translations (0.35 pixel), with linear interpolation and nearest boundary handling. These are not flips and are approximately label-preserving at this small magnitude. The feature extractor recomputes an original-source pass for paired disagreement diagnostics, plus two translated-view passes. All three are included in rich-evidence elapsed time; no free cached-pass assumption is made.

## Cost units

`elapsed_ms` is measured wall time for the complete terminal action, including support feature extraction, affine gradient calculations and query prediction. It excludes the separately measured evidence calls.

`forward_images` is retained as an alias for `encoder_forward_images`: images passed through the learned hidden encoder. It is not a count of every head calculation.

`head_forward_images` separately counts query logits and the three support-head passes of the entropy action. `backward_images` is an alias for `affine_gradient_images`: analytic gamma/beta gradient calculations using the fixed head. There is no encoder backpropagation; `encoder_backward_images` is zero for every action.

These operation counts supplement wall time. They must not be described as ordinary full-network forward/backward costs.

## Reproduce the source stage

From this directory using the recorded existing numerical environment:

```bash
uv run --no-project --no-python-downloads --python /usr/bin/python python train_core.py
```

This refits and overwrites the model/split artifacts deterministically. Source-stage outcomes are saved in `source_manifest.json`; the model is `source_model.npz`.

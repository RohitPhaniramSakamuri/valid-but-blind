# Where this matters in real imaging work (for the 3 Nov faculty demo)

Every number below is from our own runs.
- **Held-out:** test data not used to design or tune anything.
- **Dev:** used for development, not reported as results.
- Experiment 006 is still running, and its numbers will be added once it finishes.

## Setting

A hospital or lab deploys an image classifier: dermoscopy lesion type, histology tissue type, or CT organ. Its images drift away from the training data.
- **Image quality can change:** a new scanner or camera, different staining or contrast settings, compression in the image archive, slides out of focus.
- **The case mix can change:** a referral clinic sees far more melanoma than the training set had.

**Labels:** there are none in deployment. Nobody marks the correct answer for each new image.

**Two tools people use here:**
1. **Test-time adaptation (Tent).** The model updates itself on each batch of unlabeled images to fit the new data. It does this by making its own predictions more confident.
2. **A label-free risk monitor** (Schirmer et al., NeurIPS 2025). It watches the model's confidence and raises an alarm when error has probably risen above the clean level. It is the published safety check for exactly this setting.

**The problem we found:** making predictions more confident is exactly what the monitor reads. Adaptation therefore hides its own failures from the monitor.

## Scenario 1: dermatology clinic with a different case mix (DermaMNIST, held-out)

The images are clean: same camera, same quality as training. The only difference is that the clinic's mix of the 7 lesion types differs from the training data.

**What we measured on one real stream** (Tent learning rate 5e-3, strongly skewed Dirichlet-0.1 case mix, stream `held__clean__0__dir01__2`):

| | Value |
|---|---|
| Error of the adapting model | **81%** |
| Error of the same model with no adaptation | **39%** |
| Average confidence of the adapting model | **97%** |
| Existing monitor | **Never raised an alarm** in 120 batches (5,760 images) |
| Our twin alarm | **Fired at batch 11** (528 images) |

**What this means in practice:**
- Adaptation made the model about twice as wrong as not adapting at all. It also became more confident while doing so.
- The only safety check in place stayed silent.
- With our alarm, someone would have been told after about 500 images, and could switch adaptation off or send the cases for review.

**This was not a one-off.** On held-out dermatology streams at that learning rate:

| Monitor | Missed failures | False alarms |
|---|---|---|
| Existing monitor | **30 of 37** | 0 of 13 |
| Our twin alarm | **0 of 37** | 2 of 13 |

At the gentler learning rate (1e-3), the existing monitor missed 12 of 41 and the twin missed 5 of 41.

## Scenario 2: degraded image quality (contrast, JPEG, blur, pixelation)

**The corruptions:** synthetic stand-ins for real acquisition problems. Reduced contrast and exposure, heavy archive compression, out-of-focus slides, low resolution. These are held-out families: the detector was calibrated only on noise, brightness, gamma and saturation.

**An example stream:** dermatology, contrast reduced to 0.6 of normal, with a Dirichlet-1 case mix (stream `held__contrast__1__dir1__0`, Tent 5e-3).
- **Adapting model:** 82% error at 96.6% average confidence.
- **No adaptation:** 37% error.
- **Monitors:** the existing monitor stayed silent, and the twin alarm fired at batch 11.

**Across both medical datasets (BloodMNIST and DermaMNIST) and both learning rates, held-out:**

| Monitor | Failures missed | False alarms |
|---|---|---|
| Existing monitor | 35% | 4.9% |
| Our twin alarm | **5.5%** | 8.1% |
| The twin as it stood before (clean-image correction) | 44% | 11% |

The pool is 165 clear failures and 185 safe streams. Both monitors here use the same rule for setting the alarm level from development streams.

## Scenario 3: research use in an image-processing lab

**The situation:** a lab builds an enhancement, denoising or compression pipeline in front of a classifier, or runs a trained model on a new unlabeled dataset from another site. The open question is whether the model's outputs can still be trusted there. Today that needs labelling a sample by hand.

**What our method provides:**
- **A label-free trust check:** it costs one extra forward pass per batch, through a copy of the model that never takes a gradient step.
- **It is only needed once:** the alarm level is set from the lab's own labelled validation images, with synthetic corruptions applied.

**What it enables:**
- **Compare pipelines without labels:** if a preprocessing variant triggers the alarm, the model's error has very likely risen on that data.
- **Decide whether adaptation is safe on a new dataset:** test-time adaptation is often used to rescue performance on a new site, and the alarm says when it is doing harm instead.

## Why this is more than "the monitor fails"

1. **Diagnosis (verified on CIFAR-100-C and DermaMNIST):** the published monitor goes blind specifically under entropy-based adaptation.
   - On CIFAR-100-C it missed 147 of 166 clear failures when the model adapted, against 44 of 110 when it did not.
   - On DermaMNIST it missed 33 of 33, against 12 of 44.
2. **Learned detectors are not the answer (verified, experiment 005).** We tested ridge, gradient boosting, stacked models, a latent PCA layer, a GRU and per-image models. They fit the development corruptions and transferred worse to new ones than the simple twin.
3. **A simple fix that works (held-out, experiment 005; frozen confirmation running in experiment 006).** Compare the adapting model with a copy that sees the same batch statistics but takes no gradient step. Flag images where that copy is unsure or the two disagree. Set the alarm level by a conformal rule on development streams.
4. **A false-alarm guarantee.** If the deployment's safe data resemble the development streams, the false-alarm rate is at most 5% + 1/(n+1), where n is the number of safe development streams.

## Limits to state plainly

- **Corruptions:** they are synthetic stand-ins, not a real multi-site shift. Camelyon17 (real hospital-to-hospital shift) is the planned next test.
- **Architecture:** the method needs BatchNorm layers, so a ViT-style model would need a different twin.
- **False alarms:** they exceeded 10% in 1 of 4 settings (BloodMNIST, Tent 5e-3: 9 of 70 safe streams).
- **Confirmation (experiment 006, finished 12:35 IST):** PathMNIST histology, OrganAMNIST CT and CIFAR-100-C with 6 models, 2,592 streams. The verdict rule was frozen in advance.
  - **Verdict: NOT CONFIRMED.**
  - **Against the published monitor** (the realistic comparison), on held-out new data:

    | Monitor | Failures missed | False alarms |
    |---|---|---|
    | Our twin alarm | **13%** (40 of 306) | **2.4%** (14 of 578) |
    | Published monitor | **49%** (149 of 306) | 2.1% (12 of 578) |

  - **Why the frozen test still failed:**
    - It also required the twin to beat the published monitor's own signal, recalibrated the same way, by at least 15 points. The gap was 13 (26% vs 13% missed).
    - It required beating the earlier twin form by 15 points. The gap was 4, but that earlier form had many more false alarms on the medical sets.
  - **Several simple confidence signals help too:** given the same dev-calibrated alarm level, they miss about 11–15%, but with about twice the twin's false alarms.
  - **How to say it:** the twin with a dev-calibrated alarm misses about a quarter as many failures as the published monitor (13% vs 49%) at a similar false-alarm rate, and has the fewest false alarms of the strong detectors. It is not uniquely the best on misses.

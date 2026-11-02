# SA-TTS: Stress-Aware Test-Time Scaling for Vision Models

Citation key: `Yang2026SATTS`.
Authors: Youla Yang.
Year and venue: 2026; Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops, pages 11480–11487.
Publication/version status: CVPR 2026 workshop proceedings; primary CVF metadata verified.
[Authoritative source](https://openaccess.thecvf.com/content/CVPR2026W/Viscale/html/Yang_SA-TTS_Stress-Aware_Test-Time_Scaling_for_Vision_Models_CVPRW_2026_paper.html). [Local PDF](../sources/pdfs/Yang2026SATTS.pdf)
Reading progress: Downloaded official CVF PDF: title/author block, abstract, Algorithm 1, methodology and scope discussion; partial reading.

## Research question and contribution

Staged acquisition: entropy/margin first, augmentation disagreement when needed, then multi-crop inference. Blocks a generic novelty claim about escalating evidence on uncertain inputs.

## Background needed

See the linked review for the decision variable and information regime; clarify prerequisites during reading.

## Reading notes

Inspected locations: Abstract; Methodology; Algorithm 1.

## Method and implementation

Implementation availability not established by this review. The literature-review stage did not execute this paper's code or reproduce its benchmark. The later custom digit diagnostic is a separate surrogate study, described in the project README.

## Evidence and limitations

Inspected terminal actions are inference policies with a fixed backbone rather than selection among parameter-update TTA methods. Detailed experiments were not audited by reviewer.

## Connection to our research

This source constrains the proposed contribution; distinguish its actual decision and evidence access from our acquisition hypothesis. [Review](../outputs/shift-aware-tta-review.md).

## Possible experiment

Compare legal evidence and total cost under the [planned protocol](../experiments/001-policy-selection-pilot.md) where the source's task and method can be matched.

## Next reading step

Inspect remaining method, split and code details before choosing an implementation baseline or claiming the paper omits a specific test.

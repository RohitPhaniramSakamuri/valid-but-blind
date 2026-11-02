# Original user proposal

Received 23 October 2026. Preserved as proposed text. No experiment or result claimed below has been completed for this project.

## Title

Shift-Aware Test-Time Adaptation via Dynamic Adaptation Policy Selection

## Supplied abstract

Modern machine learning models often suffer significant performance degradation when deployed under distribution shifts such as changes in illumination, weather, sensor noise, or viewpoint. Existing test-time adaptation methods typically apply a single adaptation strategy regardless of the underlying cause of the shift, leading to suboptimal robustness across diverse deployment scenarios. We propose a shift-aware test-time adaptation framework that first infers the characteristics of the encountered distribution shift and then dynamically selects or composes an adaptation policy tailored to that shift. By conditioning adaptation on the inferred shift rather than treating all shifts uniformly, the framework aims to improve robustness while remaining computationally efficient and requiring no labeled target data. We evaluate the approach on standard distribution-shift benchmarks, including CIFAR-10-C, ImageNet-C, DomainNet, and WILDS, demonstrating improved generalization across heterogeneous real-world corruptions and unseen deployment environments.

## Assessment requirements

- Check the static-policy premise against direct dynamic-selection and routing predecessors.
- Keep “no target labels at deployment” distinct from labeled offline router development.
- Replace asserted benchmark success with a prospective evaluation protocol until outcomes exist.
- Distinguish constructed corruption benchmarks, natural-domain datasets and the WILDS task suite.

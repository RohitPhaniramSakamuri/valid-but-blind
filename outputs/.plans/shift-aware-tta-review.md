# Shift-aware TTA literature investigation

Date: 23 October 2026. Status: completed literature review and proposed protocol; experiments unrun.

## Objective

Assess direct prior art for the proposed shift-aware adaptation-policy selector, identify a defensible candidate gap, and specify a staged falsification protocol. No experiments are run in this task.

## Work tracks

1. Lead: foundations, benchmark assumptions, review synthesis, proposed protocol and bibliography.
2. Researcher: closest selection/routing/shift-awareness methods, including recent work.
3. Verifier: unlabeled model-selection limits, evaluation leakage, source requirements and evidence audit.
4. Reviewer: novelty collisions and adversarial review of the narrowed candidate.

## Findings that change the plan

- Direct collisions identified: Hybrid-TTA, SLRF and MORPHEUS already implement forms of shift-conditioned strategy or method selection.
- Jhawar and Wang (September 2026 preprint) already analyze evidence insufficiency, order-aware selection, no-update actions, prior/covariate ambiguity and held-out corruptions. Those alone cannot be proposed as a new gap.
- Candidate under scrutiny: acquiring additional unlabeled decision evidence only when its expected selection benefit justifies its measured cost. Compare with always using rich evidence and equal-cost selective baselines.
- State-aware policy switching and rollback are crowded adjacent directions; retain as a branch rather than make a novelty claim.

## Tool and verification status

Primary-source web search is available. The installed Feynman CLI reports alphaXiv authentication but rejects the documented `feynman alpha search` subcommand as unknown. Alpha paper search was therefore unavailable; no authentication or package settings were changed. The slash workflows are not exposed in this session; the skill's researcher/verifier/reviewer stages are being carried out with the available research agents and web tools.

## Completion record

- Completed comparison and metadata index: 47 primary sources, 47 paper notes, 9 downloaded PDFs. Reading scopes are explicit.
- Read selected closest methods, protocols and limitations; no exhaustive/full-paper claim.
- Wrote `outputs/shift-aware-tta-review.md`, matching provenance and `experiments/001-policy-selection-pilot.md`.
- Verifier and reviewer critiqued the actual synthesis. Corrected all-in costs, query normalization, nested validation, query noise, refit mismatch and oracle wording. Verifier re-read corrections and found no remaining blocking document issue.
- Added project to the root directory map and updated local README, research branches and project log.

## Next research step

Choose a source checkpoint and valid auxiliary development split before implementing the action-headroom diagnostic. The narrow acquisition question remains a hypothesis; empirical gains and novelty are unresolved.

# Independent verification of review.md

Date: **2026-11-02 (Asia/Kolkata)**. Reviewed draft lines 1–154 before completion of its final-audit section. No edits to the parent report, model runs, experiments or implementation tests. Read-only record checks used `uv run --no-project`.

## Disposition

The claim verdicts are supported at their stated, access-bounded level. No finding invalidates their overall direction. Two wording corrections below would remove avoidable overgeneralization. The final-audit placeholder and final artifact accounting still need completion by the parent.

## Corrections

1. **Medium — line 71, overgeneralized method-class restriction.** “Conditional conformal martingales require fixed scores” attributes one inspected setup's assumption to the whole method class. The primary sources support the narrower statement: Shaer `2602.13848-full.txt` explicitly says its scoring function is fixed (around line 210); Liu's `martingale-new-full.txt` explicitly says it uses a fixed score and reference (around line 1158). Suggested replacement: **“the inspected Shaer/Liu conditional-conformal methods assume a fixed scoring function.”** This preserves the relevant boundary without ruling out other conformal constructions permitting updated models.

2. **Medium — line 13, sufficient condition for suppressed alarms.** Reducing flagged-error mass alone does not logically suppress the alarm: flagged-correct mass, the source correction, and threshold also matter. The algebra in §3 already gets this right. Suggested replacement: **“Suppressed alarms are conditionally expected when the resulting proxy-positive rate keeps its lower bound below the risk threshold; that causal chain has not been directly established here.”** A simpler acceptable version is “can suppress alarms if it sufficiently reduces the proxy-positive rate relative to calibration.”

3. **Low — lines 25/125, identify the implementation in the headline description.** The local record reports a port with disclosed formula/environment differences; the exact authors'-pipeline comparison remains pending. Line 25 already discloses this, but “reproducible ... observation” in line 125 can be made more precise as **“documented multi-model observation from the port.”** This is a wording improvement, not evidence against the counts.

4. **Low — lines 25–27, optional explicit event definition.** For a self-contained diagnostic description, add that the replication's strict event requires final mean error `r0 + 0.15` or greater and last-quarter error below `0.85` (`analyze_replicate.py:39,47–49`). The monitor's alarm threshold is `r0 + 0.10`. Without this sentence the linked protocol supplies the definition, so the current text is not factually wrong.

5. **Completion item — lines 144–148.** The three fresh disproof attempts and source-to-claim audit are still promised rather than recorded. Replace the placeholder with actual queries/results, and include any unresolved close lead in the limitation statement. Do not describe a completed final audit until that work exists.

## Claim-by-claim verification

| Claim | Audit result |
| --- | --- |
| C1 | “No report found” is explicitly limited to inspected sources; incomplete forward full-text coverage and blocked close sources remain conspicuous. The counts 147/166 and 44/110, paired 97-stream subset and discordant 49/2 counts match the authoritative experiment record. The draft correctly states that each arm conditions on its own strict subset and does not pool streams as independent statistical units. |
| C2 | Correctly left unconfirmed locally. The experiment record's final mechanism/authors'-pipeline section still says “Result: pending.” Earlier author-code runs do not establish the Dirichlet blind spot or exact port agreement. A failed BN-only criterion would not prove BN causally irrelevant; draft line 45 makes that distinction. Mahdiani's abstract-only lead is not used as decisive evidence. |
| C3 | “Substantially anticipated” is supported by the TTA arm's relevant primary passages. The draft explicitly distinguishes raw-confidence bias from Schirmer's calibrated threshold/separability requirement and retains the failed cross-model confidence prediction. Except for correction 2, it does not treat confidence increase as established mediation of this alarm gap. |
| C4 | **Already published is justified for the stated existence-level vulnerability.** Han Appendix L Tables 49–50 directly contrast masked adapted scores with persistent frozen residual signal; Messaoud §4 p6/§5.4 p13 explicitly describes adaptation masking; Duan's methods/repair/limitations show model updates staling frozen activation probes. These are adjacent settings with disclosed differences. Draft lines 14/65 reject the unsupported universal “any” interpretation. No abstract-only source is needed for this verdict. |
| C5 | **Partially covered is justified.** Independent learned error estimators, disagreement checks, source/current signals and label-free alignment repairs are existing methods. None of the fully read sources demonstrates controlled false alarms and useful sensitivity in the exact Tent/Dirichlet/Schirmer setup. The draft correctly flags Han/PPRM/WATCH's outcome requirements and CASTER's poor gate transfer; proposed independence is not treated as a guarantee. |

## Primary-source checks

- **Schirmer §5.4:** the primary passage expressly says the uncertainty lower bound becomes too loose and the alarm fails for last-layer TTA; prototype distance yields tighter bounds for T3A/STAD. The report's characterization is accurate and does not falsely say Tent was the failing arm there.
- **Schirmer Assumption 1/Corollary 1:** the draft's `q = r − FN + FP`, `B = q − FP0`, and `r − B = FN − FP + FP0` match the 0–1-loss population construction. Its FP/FN are joint masses, not conditional error rates. The numerical illustration gives `q=.20`, `B=.03` correctly. Large FN can preserve validity while destroying useful sensitivity; longer sampling cannot repair a fixed population proxy gap. This does not challenge false-alarm control.
- **Han Appendix L:** requires revealed forecasting outcomes. Draft correctly restricts the analogy and does not advertise a label-free fix.
- **CBPE:** source paper's guarantees require calibration; TableShift experiments evaluate eight of 15 available datasets, rather than all 15. The main review does not give the wrong sample count. The claim is correctly separated from Schirmer's weaker failure-ranking requirement.
- **PPRM §3.1/§5.1.2:** positive target-label count is explicit; Fig. 2a's URM miss is under static CIFAR-10 corruption, not the C1 Tent comparison. The draft preserves both distinctions.
- **WATCH:** the outcome-conformity channel needs outcomes; its input-only X-CTM detects input changes, not guaranteed risk harm. The draft is accurate.
- **Duan:** activation alignment repair needs paired unlabeled base/update activations and initial labeled probe training. It is not a universal safety or sequential risk guarantee. The draft cites it only as adjacent monitor-staleness evidence.
- **SSRN/TRUST-ADAPT:** blocked full text is plainly marked. The main conclusions do not rely on assumed omitted methods or results.

## Record/schema inspection

The central CSV files present during inspection were parsed read-only for schema overflow; final row counts remain the parent's responsibility because merging was ongoing. No implementation tests were run. The source/date/query and per-claim overlap schemas are appropriate. Main-report source claims trace to linked primary locations or agent extraction reports, with inaccessible/abstract-only sources labeled.

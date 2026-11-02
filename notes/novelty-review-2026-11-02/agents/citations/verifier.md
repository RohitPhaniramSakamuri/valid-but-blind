# Citation and scope verification of the draft review

Verified on **2 November 2026**, against `review.md` as read in this pass, this arm's raw API/Scholar responses, metadata, source extracts, and follow-up paper reading. No new searches or experiments were performed for this verifier pass.

## Overall disposition

The draft's bounded C1/C2 absence statements are appropriately cautious. It explicitly denies global citation saturation and distinguishes source access from full reading. The positive C3/C4 prior-art assessment is compatible with this arm's findings, subject to preserving the literal-universal caveat for C4. **One material access hole and two precision corrections should be incorporated before finalization.**

## Required corrections or completion

1. **Add ODFD as an unresolved direct citer.** The one-page coverage limit and §8 currently name Mahdiani and TRUST-ADAPT but omit Jia et al.'s *Online Dynamic Fault Diagnosis for Rotating Machinery Under Source-Free Streaming Test-Time Adaptation*, DOI10.1109/JSEN.2026.3741562, IEEE11737673. Direct document/stamp/DOI/PDF requests returned HTTP202 with empty bodies; OpenAlex reports closed/no repository, exact-title Scholar has one record/no alternative version. Methods/results/appendices remain unread. Its abstract's fixed uncertainty thresholds and confidence-weighted adaptation make it a meaningful remaining hole, even though no exact C1 evidence was found. Do not describe the full forward-citer audit as cleared. Parent already indicated this will be added.

2. **Say the six Scholar host versions were enumerated, not all inspected.** §7 currently says tracing “used ... all six listed host versions.” This arm retrieved the *list* of six version URLs; it did not retrieve and read all six host copies independently. Safer text: “enumerated all six host versions in Scholar's cluster, then separately identified arXiv v1/v2 and the ICML PUT workshop version.” The official NeurIPS text was inspected by the parent, but ACM/UvA mirror copies should not gain a reading status by association.

3. **Finish the final-audit placeholder and final source counts.** The final adversarial audit is currently a placeholder. This arm now has138 search/retrieval rows,113 screened titles,12 metadata records and132 saved evidence/derived files. These are *arm-specific counts*, not total distinct papers read. Merge and deduplicate final ledgers before giving review-wide counts. The existence of metadata or a PDF does not upgrade the row to a full reading.

## Numerically verified citation accounting

- Google Scholar cluster **7250704993477156062**: two saved cited-by pages contain **16 entries /15 unique titles**, because the sports-maintenance paper appears on both pages. Displayed totals are inconsistent (13/16); subsequent full/date-sorted/arXiv probes429. Do not claim all16 displayed citations were resolved.
- Semantic Scholar canonical arXiv record **6631660c936a204606798af54c5235d0c729203e**: **12** citation records, no continuation cursor in the saved response. The title list is complete for this record's returned snapshot, not for every possible paper version or index.
- Deduplicating those two sets gives **20 distinct titles**, not27or28. The draft reports this correctly.
- Semantic Scholar returned80 backward records, including one checklist-text artifact. This count must not become “80 valid papers fully read.” The draft avoids that mistake.
- OpenAlex W7197038270 (published) and W6929305892 (arXiv DOI) each report0 citations. A DOI-filter query failed to recover the directly accessible arXiv record. These empty/inconsistent records cannot outweigh the positive Scholar/S2 list. The draft handles this correctly.
- Crossref reports1 citation without an identifiable forward list in the public response. It does not demonstrate that only1citation exists. The draft handles this correctly.

## Exact six Scholar-listed host URLs

The raw list is `evidence/citations/scholar_versions_retry-records.json`:

1. `https://proceedings.neurips.cc/paper_files/paper/2025/hash/746960ad49ddb47248970a0e1404230c-Abstract-Conference.html`
2. `https://pure.uva.nl/ws/files/340219841/085713-2705open.pdf`
3. `https://openreview.net/forum?id=TzHX2RWUdE`
4. `https://papers.neurips.cc/paper_files/paper/2025/file/746960ad49ddb47248970a0e1404230c-Paper-Conference.pdf`
5. `https://dl.acm.org/doi/abs/10.52202/085713-2705`
6. `https://dare.uva.nl/id/6156d96b-db4d-4ac9-ade9-77bd59197db0`

These are six hosts/records of the conference paper, not six independently distinct scientific contributions. arXiv2507.08721v1 (11July2025), v2 (8November2025), and PUT workshop OpenReview`k14ktterKG` are tracked separately. The workshop was paper72, oral18July2025, verified on the official program. Official NeurIPS volume is38 and canonical key/year remains `Schirmer2025Monitoring`; Scholar's2026 date/repository volume39 should not override it. The draft preserves the correct identity.

## Follow-up source distinctions the synthesis should preserve

- **Anatomy/Boundary2609.12136:** now selectively read beyond abstract. §5.5/Fig1c/PDFp14/AppendixJ show a revealed-label log-loss-regret e-process missing most AUC harm during adaptation. This is a substantial adjacent proxy/metric-mismatch precedent, but not a run of Schirmer's label-free monitor, not Tent/BN, and not the same zero-one-risk target. Cite as `Wang2026TemporalBoundary` if added. AppendixJ says the e-process implementation is absent from the deposit.
- **E-valuator2512.03109:** now read §§2–4 and relevant appendices. Schirmer appears in related work; experimental baselines are verifier/threshold variants, not the TTA monitor. It offers independent-verifier sequential testing with labeled trajectory calibration and sampling assumptions. It does not guarantee power after arbitrary changes to an adapting classifier. Cite as `Sadhuka2025EValuator` if added.
- **Atarmla2609.23254:** exact scalar adaptive-*threshold* results, not a fixed-threshold adaptation result. The draft explicitly distinguishes this, correctly.
- **Hong2603.08455:** no online model update specified in the tested protocol. The draft explicitly prevents the misleading claim that it demonstrates weight-update masking, correctly.
- **CASTER2609.00374:** the gate is independent of Tent's optimization but transfers poorly; independence alone does not imply useful C5 power. The draft captures this.
- **ConditionalCTM2602.13848 and parameter-free2610.17343:** require fixed scoring functions. Their power theorems cannot be carried over to adaptive confidence scores without new conditions. The draft captures this.

## Verdict wording caution

The table gives C4 “Already published” after restating it as an existential/general vulnerability, while the request's literal “any confidence-derived...” wording is stronger. The existing caveat is essential: **the positive verdict concerns the general vulnerability, not a theorem quantifying over every confidence-derived monitor.** Keep that sentence in the verdict itself, as currently done, and avoid a final response that drops it. Likewise, C1/C2 “No report found” means the exact comparison was not found in the inspected accessible evidence; it cannot be shortened to “new” or “all prior work excluded.”

No additional citation-accounting blockers were found within this verifier scope. Claims about primary papers handled by other subreviews were not independently reread in this pass; this is not a second full audit of every source in `review.md`.

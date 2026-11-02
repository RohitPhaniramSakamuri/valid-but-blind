"""Finalize review and current project pointers; preserve chronological records."""
from pathlib import Path
BASE=Path(__file__).resolve().parent;PROJECT=BASE.parent.parent
p=BASE/'review.md';s=p.read_text()
s=s.replace('**Coverage limit:** 20 distinct Schirmer forward-citation titles were recovered from Scholar and Semantic Scholar, with separate workshop/preprint/version checks. Several citers received only metadata/abstract screening. Citation expansion did **not** reach global saturation, and full texts of Mahdiani\'s conformal paper and TRUST-ADAPT remain blocked.', '**Coverage limit:** 20 distinct Schirmer forward-citation titles were recovered from Scholar and Semantic Scholar; a final adversarial search identified PORTAL as a further full-text-verified citer, bringing the known set to 21. Separate workshop/preprint/version checks were performed. Several citers received only metadata/abstract screening. Citation expansion did **not** reach global saturation. Mahdiani\'s conformal paper, TRUST-ADAPT, and the direct machinery-TTA citer ODFD remain blocked in full text.')
s=s.replace('reports a frozen replication rule passing on CIFAR-100-C: Tent missed','reports a frozen replication rule passing on CIFAR-100-C using the project\'s monitor port: Tent missed')
s=s.replace('The experiment excludes streams by a last-quarter error cutoff;', 'A strict violation uses final error at least r₀+0.15, while the released-form alarm threshold is r₀+0.10. The experiment excludes streams by a last-quarter error cutoff;')
s=s.replace('AETTA §3.2/Fig. 2 is direct prior evidence that Tent\'s confidence can rise while accuracy falls.', 'AETTA §3.2/Fig. 2 is direct prior evidence that Tent\'s confidence can rise while accuracy falls. Its plotted confidence is an expectation over dropout predictions, not necessarily the port\'s exact maximum-softmax statistic; its separate estimator comparisons also evaluate SoftmaxScore.')
s=s.replace('Schirmer tracing used Google Scholar\'s cluster7250704993477156062, all six listed host versions,', 'Schirmer tracing queried Google Scholar\'s cluster7250704993477156062 and enumerated all six listed host versions,')
s=s.replace('giving a union of 20. OpenAlex', 'giving an index union of 20. The final-query follow-up read PORTAL (27 October2026), verified its Schirmer citation in §4.6 p8 and AppendixX, and expanded the known union to21. Its sparse-target-label controller is not the C1 monitor comparison. [Late-source reading](agents/tta_causes/late-screen.md). OpenAlex')
s=s.replace('Mahdiani\'s SSRN landing/PDF and TRUST-ADAPT\'s publisher/PDF returned403.', 'Mahdiani\'s SSRN landing/PDF and TRUST-ADAPT\'s publisher/PDF returned403. Direct citer ODFD (IEEE Sensors Journal, DOI10.1109/JSEN.2026.3741562) returned empty/challenge202 responses at the article/PDF endpoints; its abstract and bibliographic metadata cannot exclude closer overlap. [Direct-citer follow-up](agents/citations/direct-citers-followup.md).')
s=s.replace('Audit results are appended after the independent verification passes and final three query families.', '''Three independent review passes checked source support, verdict scope, citation accounting, and local outcomes: [citation verifier](agents/citations/verifier.md), [adjacent-source verifier](agents/adjacent_monitors/verifier.md), and [critical reviewer](agents/tta_causes/reviewer.md). Corrections restrict fixed-score claims to the inspected methods, distinguish total proxy-positive mass from flagged errors alone, clarify AETTA's plotted statistic, enumerate rather than imply reading every host copy, and retain all blockers.

Three final adversarial search families were run on2November2026, followed by single-query refinements. Exact strings and raw responses are in `root-search-log.csv` and `evidence/root-search-12.json` through `root-search-15.json` (see CSV for the precise batch/query mapping):

| Attempt to overturn C1 | Exact refined query | What it found and disposition |
| --- | --- | --- |
| Same-paper label-shift search | `"Monitoring Risks in Test-Time Adaptation" "label shift"` | Recovered the paper's AppendixA.5 and workshop version, plus repository/reference lists. Primary figures were checked; no complete C1 comparison was established. |
| Failure phrasing beyond the monitor's name | `"test-time adaptation" "missed" "confidence" "monitor"` | Surfaced late primary candidates ZAEC, PORTAL, and StaR-TTA through discovery indexes. All three received selective methods/results reading; ZAEC supplies prediction-preserving confidence inflation and a label-free calibration repair. PORTAL became a21st verified citer. None reports the exact C1 contrast. |
| Recent Tent/skew/risk combination | `"Tent" "Dirichlet" "risk" "monitoring" after:2025-11-02 before:2026-11-03` | Returned noisy non-TTA and patent/benchmark leads; none established the exact comparison. Date syntax was not reliably enforced by the engine, so no coverage claim is inferred from this query. |

The initial variants also searched `tta-monitor` with false-negative/Dirichlet/fixed-threshold phrases and Schirmer/Tent/frozen terms. The audit **did find new relevant prior work**, rather than merely confirming the draft. Verdicts remain unchanged, but the source set and C3/C5 prior-art coverage were expanded. These findings show why one no-yield keyword search or a zero-count index cannot certify absence.

The merged ledgers contain385 search/retrieval rows and2,818 distinct title/source screens. Most screens are mechanical titles or index snippets; this is **not**2,818 full-paper readings.377 saved evidence files include raw indexes, PDF/text pairs, errors, and figures, not377 independent papers. Counts are reproducible in [review-stats.json](review-stats.json). The central library now contains148 stable-key records,32 added in this review; source notes and dated histories distinguish actual reading from retrieval.

**Traceability disposition:** published-results claims link to primary sources and section/figure/table locations; local numerical claims link to Experiment004; access-limited leads are named as such; algebra and methodological judgments are labeled interpretation. No verdict relies on treating a blocked abstract as a verified method/result. A final document audit checks links, citation-key consistency, CSV structure, and the five verdict assignments; it is not an implementation test or research experiment.''')
insert='''
**Late adversarial-search predecessors.** ZAEC already isolates confidence inflation on examples whose top-1 prediction and correctness stay fixed, then repairs confidence with a frozen-source entropy floor without changing those predictions. It studies VLM calibration, not this sequential alarm. StaR-TTA repairs confidence-estimator staleness after offline RL model updates without target correctness labels; it is not continual entropy TTA. PORTAL instead needs sparse target labels. These strengthen the existing-method objection to a generic C5 proposal. [ZAEC](https://arxiv.org/abs/2608.05945), Table1/Props1–2/pp3–7; [StaR-TTA](https://arxiv.org/abs/2610.35500), §§3–5/AppendixA; [PORTAL](https://arxiv.org/abs/2610.37658), §4.6/AppendixX; [reading/version limits](agents/tta_causes/late-screen.md). ZAEC refers to appendices absent from its downloaded nine-page version; their contents were not assumed.

**The named Entropy Enigma predecessor** uses weighted prediction flips during adaptation to estimate initial/source-model dataset accuracy. Its flip-to-accuracy mapping uses labeled offline data; this is not an assumption-free current-model risk alarm. [Press etal.](https://arxiv.org/abs/2405.05012), §§4.1–4.4; [explicit extraction](agents/tta_causes/report.md).
'''
if '**Late adversarial-search predecessors.**' not in s:s=s.replace('## 3. Why validity can coexist with blindness',insert+'\n## 3. Why validity can coexist with blindness')
p.write_text(s)

updates={
'README.md':'''## Current review — 2 November 2026

The [adversarial novelty review](notes/novelty-review-2026-11-02/review.md) narrows the monitor finding. C1 exact adapted/frozen miss-rate comparison: no matching report found within incomplete coverage. C2 fixed-threshold/entropy-versus-BN contrast: no matching accessible report found, **and locally still pending**. C3 mechanism: substantially anticipated. C4 general self-masking vulnerability: already published; universal wording unsupported. C5 independent label-free remedy: partially covered by existing methods; no exact sensitive fix established.

Known prior art includes Schirmer's own proxy-failure/repair experiment, AETTA, corrupted Dirichlet model-selection experiments, Han's self-masking/frozen-sentinel study, and recent calibration/monitor-staleness work. The library has148 records,32 added. [Queries/screens/evidence](notes/novelty-review-2026-11-02/) preserve reading scope.21 Schirmer citers are known from20 indexed titles plus PORTAL. Citation saturation was not reached; SSRN/TRUST-ADAPT/ODFD full texts remain blocked. No experiments or implementation tests ran.

**Next concrete step:** resolve blocked close predecessors and finish documenting the already frozen implementation/factorial outcomes before strengthening C2 or proposing a fix. Retain only a bounded diagnostic claim; broad confidence failure and independent monitoring are established ideas. Earlier dated statuses below are historical, not the current conclusion.
''',
'notes/research-branches.md':'''## Adversarial review update — 2 November 2026

The [new review](novelty-review-2026-11-02/review.md) rejects broad originality for entropy/confidence failure and adaptation undermining its own monitoring signal. Existing independent estimators, disagreement/conformal methods, and frozen sentinels constrain any remedy.

**Remaining candidate question, not an established gap:** does Schirmer's supported confidence monitor have materially worse sensitivity for Tent than frozen checkpoints under persistent many-class skew and corruption, beyond its already documented proxy failures? The local port replication reports147/166 versus44/110 missed, but the exact literature audit is incomplete. Fixed-threshold/BN cause and authors' Dirichlet-pipeline outcomes remain pending in the authoritative experiment record. Mean-confidence dependence previously failed and is not revived as an explanation.

The review recovered20 indexed Schirmer citers and a21st through full-text follow-up. Mahdiani's conformal/BN-control paper, TRUST-ADAPT, and ODFD remain access blockers. Continue as a narrow diagnostic only after those checks; change direction if ordinary proxy/current-method controls remove the useful residual. No experiments ran for this review.
''',
'CHANGELOG.md':'''## 2 November 2026 — adversarial novelty review of Experiment004

- Created [claim-by-claim review](notes/novelty-review-2026-11-02/review.md), repeatable search/screen ledgers, close-work matrices, primary evidence/manifests, provenance, and independent verification/critique records.
- Recovered20 Schirmer citers from Scholar/S2 plus PORTAL through final adversarial follow-up; traced preprint/workshop/host versions and documented index disagreement/rate limits. Global citation saturation was not reached.
- C1/C2: no exact matching accessible report found, with explicit coverage limits; C2 and authors'-pipeline outcomes remain locally pending. C3 substantially anticipated; C4 general vulnerability already published; C5 partially covered.
- Added32 distinct source records (library148), preserved stable keys and old reading histories, corrected stale publication metadata for SHSD/D3M/PPRM, and added/updated source notes. Central files were backed up before append-only migration.
- No experiments, model runs, implementation tests, package installation, or paid compute. Python retrieval/document work used `uv run --no-project`. SSRN/TRUST-ADAPT/ODFD full texts and parts of the citation graphs remain unresolved.

Next: resolve blocked close work and document the already frozen causal/implementation checks before advancing the diagnostic or a remedy.
'''}
for name,section in updates.items():
    path=PROJECT/name;s=path.read_text();heading=section.splitlines()[0]
    if heading in s:continue
    first=s.find('\n');s=s[:first+1]+'\n'+section+'\n'+s[first+1:];path.write_text(s)
print('Updated review and current project pointers.')

# Code, evidence and reproduction boundaries

Original project material is [all rights reserved](LICENSE). Viewing this public research record is not a grant to run, copy or reuse its original code or documents. Obtain express written permission for uses requiring authorization. Third-party components retain their [own licenses](THIRD_PARTY_NOTICES.md).

## Current scientific status

The original policy-selection proposal evolved into a controlled study of a label-free monitor during adaptation. The completed manuscript, protocols and review presentations retain negative and partial findings.

The latest frozen test of the family-validated alarm ran 4,630 planned streams overall. The primary held-out Tent pool contains 272 clear failures and 399 safe streams. The alarm missed 22/272 at 30/399 false alarms, compared with 171/272 misses for the published monitor and 40/272 for the constant-level twin. Its frozen verdict is **PARTIAL**: ranking, deployed safety and deployed power passed; false alarms of 7.52% exceeded the 7.5% level-transfer band. No general guarantee or established novelty is claimed.

## Source and evidence map

| Component | Code | Saved evidence |
| --- | --- | --- |
| Original monitor diagnostic and mechanism controls | [diagnostics/2026-11-01-exp004-mechanism](diagnostics/2026-11-01-exp004-mechanism) | [Experiment 004](experiments/004-monitor-blind-spots.md) and the corresponding diagnostic summaries |
| Medical stress test | [diagnostics/2026-11-02-exp004-derma](diagnostics/2026-11-02-exp004-derma) | [Experiment 004](experiments/004-monitor-blind-spots.md) and saved JSON/JSONL outcomes |
| Shifted-development detectors | [diagnostics/2026-11-03-exp005-detector](diagnostics/2026-11-03-exp005-detector) | [Experiment 005](experiments/005-rich-detector.md), `report.json` and `rows.json` |
| Twin confirmation | [diagnostics/2026-11-03-exp006-confirm/job](diagnostics/2026-11-03-exp006-confirm/job) | [Experiment 006](experiments/006-twin-confirmation.md), [report6.json](diagnostics/2026-11-03-exp006-confirm/results/report6.json) and [rows6.json](diagnostics/2026-11-03-exp006-confirm/results/rows6.json) |
| Alarm diagnosis (exploratory) | [diagnostics/2026-11-03-exp007-alarm-diagnosis](diagnostics/2026-11-03-exp007-alarm-diagnosis) | [Experiment 007](experiments/007-alarm-diagnosis.md), `diag_a.json` and `diag_b.json` |
| Shifted-level confirmation | [diagnostics/2026-11-03-exp008-confirm/job](diagnostics/2026-11-03-exp008-confirm/job) | [Experiment 008](experiments/008-shifted-level-confirmation.md), [report8.json](diagnostics/2026-11-03-exp008-confirm/merged/report8.json) and [rows8.json](diagnostics/2026-11-03-exp008-confirm/merged/rows8.json) |
| Level-transfer diagnosis (exploratory) | [diagnostics/2026-11-14-exp009-level-transfer](diagnostics/2026-11-14-exp009-level-transfer) | [Experiment 009](experiments/009-level-transfer-diagnosis.md), diagnosis JSON files and `harness_rows.json` |
| Fresh family-validated confirmation | [run10.py](diagnostics/2026-11-14-exp010-confirm/job/run10.py), [prepare10.py](diagnostics/2026-11-14-exp010-confirm/job/prepare10.py), [analyze10.py](diagnostics/2026-11-14-exp010-confirm/job/analyze10.py) | [Experiment 010](experiments/010-family-validated-alarm-confirmation.md), [report10.json](diagnostics/2026-11-14-exp010-confirm/results/report10.json) and [rows10.json](diagnostics/2026-11-14-exp010-confirm/results/rows10.json) |
| Live demonstration | [demo](demo/README.md) | Saved demo comparison results; the demo has disclosed differences from the recorded runs |
| Manuscript | [paper/main.tex](paper/main.tex) and [figures](paper/figures) | [PDF preview](paper/manuscript_preview.pdf) and [Overleaf package](paper/springer_overleaf.zip) |
| Assessment and review documents | [reports/assessment](reports/assessment/README.md) and [reports/reviews](reports/reviews/README.md) | Editable documents, PDFs, poster and delivery ZIP |

## Data, labels and state

Published checkpoints are obtained through RobustBench or the corresponding authors. CIFAR-C and MedMNIST datasets are obtained from their providers, subject to their terms. Datasets, checkpoints, private cloud account records and per-image tensor archives are not distributed here. The public repository contains source code, calibration metadata and compact outcome summaries; it is not a complete archive of the raw runs.

Original clean-calibration identities are excluded from target streams. Development and held-out shift families are separate. Labeled clean calibration and labeled synthetic development streams are allowed offline and are explicit method requirements. Deployment labels are hidden from adaptation, signal selection, alarm levels and stopping decisions. Labels are used to construct controlled research streams and score outcomes externally.

The source checkpoint is immutable. Adaptive states reset at the beginning of each stream and continue updating within the stream. The entropy-free twin uses batch statistics without an entropy gradient. Counterfactual arms use equivalent starting checkpoints and paired draws. Each model's own error defines its strict-violation subset; counts from different model arms do not necessarily share a denominator.

## Execution requirements

Python commands use **uv**. The experiment protocols record their original hardware, dependency versions, stream definitions, freeze hashes, commands and deviations. The fresh confirmation used GPU execution; CPU document generation does not reproduce it. Cloud launcher files are historical execution records and may refer to resources that no longer exist.

The scripts are retained with their original assumptions, relative paths and output behavior. For example, the final analysis entry point is [analyze_local.sh](diagnostics/2026-11-14-exp010-confirm/analyze_local.sh); it expects the separately retained `streams/` tensor files. Running it on a checkout without those arrays will not reproduce the published aggregate report. The exploratory level-transfer diagnosis also needs raw arrays that are not included. Use the saved reports to inspect the existing results without launching experiments.

Source data and checkpoint preparation, adaptation runs, confidence-sequence analysis and document generation have different dependency requirements. Follow the relevant protocol rather than treating the entire repository as a single-install package. Complete deployment latency and memory measurements remain future work.

## Document regeneration

Review and assessment builders use the source catalog in [sources/catalog.json](sources/catalog.json), local research records and the supplied review templates. The review builder uses already installed python-pptx, python-docx, lxml and Pillow through uv. PDF rendering additionally requires LibreOffice, pdftoppm and qpdf. Commands are in [reports/reviews/README.md](reports/reviews/README.md).

The current review delivery has no calendar dates or publication years in the presentation/report text or speaker notes. Historical source records and mandatory upstream copyright notices retain their original dates. Building documents does not execute the research experiments. Generated document hashes and source-report checks are recorded in [build_manifest.json](reports/reviews/build_manifest.json).

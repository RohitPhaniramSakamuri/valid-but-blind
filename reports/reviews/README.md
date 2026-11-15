# Review presentations

Prepared for **Rohit Phaniram Sakamuri — 23BDS0051** using the supplied `Review1.pptx`, `Review2.pptx` and `Review3.pptx` templates. The originals are preserved. The decks retain the templates’ 4:3 page size, section order and section requirements, with completed content, editable diagrams, tables, charts and speaker notes.

| Deck | Slides | Focus |
| --- | --- | --- |
| [Review I](Review_I_Rohit_23BDS0051.pptx) | 8 | Initial policy-selection proposal, literature overlap and refinement to risk monitoring |
| [Review II](Review_II_Rohit_23BDS0051.pptx) | 13 | Implemented monitor study, controlled comparisons and entropy-free twin |
| [Review III](Review_III_Rohit_23BDS0051.pptx) | 16 | Completed study and fresh family-validated-alarm confirmation |

These are reconstructed stage presentations based on the current research records. They do not claim to be historically submitted versions. Calendar dates and publication years are omitted from presentation text, speaker notes and the companion documents. Default date placeholders and Office/PDF date metadata are also removed.

Each deck has a PDF beside it. Review III also includes the companions requested by its template:

- [Word summary](Review_III_Report_Rohit_23BDS0051.docx) and [PDF](Review_III_Report_Rohit_23BDS0051.pdf), following Title, Abstract, Keywords, Introduction, Literature Review, Proposed Work, Performance Evaluation, Results and Discussion, and References.
- [Editable A3 portrait poster](Review_III_A3_Poster_Rohit_23BDS0051.pptx) and [print-ready PDF](Review_III_A3_Poster_Rohit_23BDS0051.pdf). Print at actual size on A3 paper.
- The repository URL from the local checkout’s configured Git origin. GitHub’s API confirms the repository is public; synchronization of every local research file is not claimed.

The [complete delivery bundle](Review_Presentations_Rohit_23BDS0051.zip) contains the three editable decks, their PDFs, the Word/PDF summary, and the editable/printable poster.

Original project material is [all rights reserved](../../LICENSE); reuse requires Rohit Phaniram Sakamuri's prior express written permission, subject to applicable law, GitHub's platform terms and retained third-party rights. The delivery bundle includes the rights notice and upstream license notices. Mandatory historical copyright notices retain their original wording; the presentation and report content remains free of dates.

## Evidence and scope

The source records are the [current manuscript](../../paper/main.tex), experiments [004](../../experiments/004-monitor-blind-spots.md), [006](../../experiments/006-twin-confirmation.md), [007](../../experiments/007-alarm-diagnosis.md), [008](../../experiments/008-shifted-level-confirmation.md), [009](../../experiments/009-level-transfer-diagnosis.md), [010](../../experiments/010-family-validated-alarm-confirmation.md), the saved final analysis report, and the existing source catalog. Source roles, final primary counts and artifact hashes are in [build_manifest.json](build_manifest.json).

The final test is **PARTIAL**: 22/272 failures missed and 30/399 false alarms. The exact false-alarm rate is 7.52%, above the frozen 7.5% band. Ranking, deployed safety and deployed power passed; level transfer did not. Earlier failed confirmations, offline labeled development requirements, runtime label restrictions, uncertified alarms and limitations remain explicit. The broader ideas of confidence failure and independent monitoring are prior art; novelty is not established.

Review II uses matching corrupted-stream twin counts, 30/109 versus 94/109. This differs from the initial frozen output’s 30/115 because six clean violations were absent from the original monitor’s corresponding run. Replication counts, 147/166 versus 44/110, are from another study and have arm-specific violation subsets. The final run’s 4,630 streams include development streams and secondary objectives; its primary held-out Tent pool is 272 strict and 399 safe streams.

This task generated documents from saved evidence. It did not run scientific experiments, implementation tests, new literature searches, training, dependency installation or paid compute. Document preparation used existing Python libraries through uv and LibreOffice for rendering. Layout review covered all slides and the poster, and the final result counts were checked against the saved report.

A submission-readiness pass removed document-preparation commentary from speaker notes, confirmed that the companion files resolve within the bundle, checked the archive and file hashes, and confirmed the repository’s public visibility. Proposal-stage language and future-work sections are intentional; the final PARTIAL verdict describes the scientific outcome rather than an unfinished document.

## Rebuilding

[build_reviews.py](build_reviews.py) generates the editable files. [finalize_reviews.py](finalize_reviews.py) renders, refreshes the embedded poster preview, strips PDF metadata, checks document content and creates the delivery archive. Neither script executes the project’s scientific code.

```bash
uv run --no-project --cache-dir /tmp/rohit-review-uv python reports/reviews/build_reviews.py
uv run --no-project --cache-dir /tmp/rohit-review-uv python reports/reviews/finalize_reviews.py
```

Rendering requires LibreOffice, pdftoppm and qpdf. The generator’s poster preview uses the rendered poster image; the finalizer refreshes that preview before rendering Review III.

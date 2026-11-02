"""Append candidate B records. Append-only and idempotent, like apply_records.py."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATE = "2026-10-31"
LEDGER = "outputs/candidate-b-dossier-2026-10-31.md"
ABS = "Abstract only."
NEW = [
    ("Amoukou2024SequentialHarmful", "Sequential Harmful Shift Detection Without Labels",
     ["Salim I. Amoukou", "Tom Bewley", "Saumitra Mishra", "Freddy Lecue", "Daniele Magazzeni", "Manuela Veloso"], 2024,
     "arXiv preprint 2412.12910", "https://arxiv.org/abs/2412.12910", "arXiv v1, 17 December 2024; venue not verified",
     "Abstract, introduction and Assumption 4.1 passages.",
     "Label-free harmful-shift detection using a trained error estimator, including covariate and label shifts.",
     "Not designed for adapting models; Schirmer et al. report its assumption violated in nearly every practical setting they tried."),
    ("Nguyen2025D3M", "Reliably Detecting Model Failures in Deployment Without Labels",
     ["Viet Nguyen", "Changjian Shui", "Vijay Giri", "Siddharth Arya", "Amol Verma", "Fahad Razak", "Rahul G. Krishnan"], 2025,
     "arXiv preprint 2506.05047", "https://arxiv.org/abs/2506.05047", "arXiv v4, 4 November 2025; venue not verified",
     "Abstract and start of the limitations section.",
     "Disagreement-based deterioration monitoring with false-positive control and sample-complexity bounds.",
     "Not TTA; authors report noisy results at small query sizes."),
    ("Solozobov2026Governance", "Label-Free Detection of Governance Evidence Degradation in Risk Decision Systems",
     ["Oleg Solozobov"], 2026, "arXiv preprint 2604.17836", "https://arxiv.org/abs/2604.17836",
     "arXiv preprint by an independent researcher; venue not verified", ABS,
     "Composite proxy monitoring; reports zero proxy change under pure concept drift.", "Credit-risk data, not TTA; unreplicated."),
    ("Balachandran2026Discern", "Pay Only for Disagreement: Certified No-Regression Verdicts for Model Updates with Matching Label-Complexity Bounds",
     ["Vishnu Bindu Balachandran"], 2026, "arXiv preprint 2609.17560", "https://arxiv.org/abs/2609.17560",
     "arXiv v1; carries a JMLR-style header but acceptance is not verified", ABS,
     "Certifies low-disagreement updates without labels and audits disagreements with labels.", "Discrete model updates, not continuous TTA; needs labels to judge disagreements."),
    ("Zhang2026PPRM", "Prediction-Powered Risk Monitoring of Deployed Models for Detecting Harmful Distribution Shifts",
     ["Guangyi Zhang", "Yunlong Cai", "Guanding Yu", "Osvaldo Simeone"], 2026, "arXiv preprint 2602.02229", "https://arxiv.org/abs/2602.02229",
     "arXiv v2, 10 June 2026; venue not verified", ABS,
     "Semi-supervised anytime-valid risk lower bounds from synthetic plus few true labels.", "Needs some true labels; not TTA in what was read."),
]
HISTORY = {
    "Schirmer2025Monitoring": ("arXiv v2 §§3.3–3.4, 5.2–5.3, 6, A.4–A.5. Released code not yet inspected.", ["Assumption 1", "Sections 3.3–3.4", "Section 5", "Section 6", "Appendix A.4–A.5"]),
    "Bar2024ProtectedTTA": ("arXiv PDF future-direction passage on label shift.", ["Discussion"]),
}

path = ROOT / "sources/catalog.json"
catalog = json.loads(path.read_text())
keys = {r["key"] for r in catalog}
assert set(HISTORY) <= keys
for r in catalog:
    if r["key"] in HISTORY and not any(h.get("source_ledger") == LEDGER for h in r.setdefault("reading_history", [])):
        scope, locs = HISTORY[r["key"]]
        r["reading_history"].append(dict(date=DATE, read_scope=scope, locations=locs, source_ledger=LEDGER))
        r["freshly_verified"] = DATE
added = [n for n in NEW if n[0] not in keys]
for key, title, authors, year, venue, url, status, scope, overlap, limit in added:
    catalog.append(dict(key=key, title=title, authors=authors, year=year, venue=venue, entry_type="misc", url=url, read_scope=scope,
                        locations=[], method_overlap=overlap, limitation=limit, publication_status=status,
                        reading_history=[dict(date=DATE, read_scope=scope, locations=[], source_ledger=LEDGER)],
                        freshly_verified=DATE, source_ledger=LEDGER, accessed=DATE))
    note = ROOT / "papers" / f"{key}.md"
    if not note.exists():
        note.write_text(f"# {title}\n\nCitation key: `{key}`\nAuthors, year, and venue: {', '.join(authors)}; {year}; {venue}.\nAuthoritative link: {url}\nStatus: {status}.\n"
                        f"Reading progress: {DATE}: {scope}\n\n## What the inspected passages cover\n\n{overlap}\n\n## Limitations for our use\n\n{limit}\n\n"
                        f"## Connection to our research\n\nSee the [candidate B dossier](../{LEDGER}).\n")
path.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n")
with (ROOT / "sources/catalog.csv").open("a", newline="") as f:
    w = csv.writer(f)
    for key, title, authors, year, venue, url, status, scope, overlap, limit in added:
        w.writerow([key, title, "; ".join(authors), year, venue, url, "", status, scope, "", overlap, limit, "", DATE, LEDGER])
with (ROOT / "references.bib").open("a") as f:
    for key, title, authors, year, venue, url, status, *_ in added:
        f.write(f"\n@misc{{{key},\n  title = {{{{{title}}}}},\n  author = {{{' and '.join(authors)}}},\n  year = {{{year}}},\n  howpublished = {{{venue}}},\n  url = {{{url}}},\n  note = {{{status}}},\n  urldate = {{{DATE}}},\n}}\n")
refs = ROOT / "REFERENCES.md"
text = refs.read_text().rstrip("\n")
if added:
    text += f"\n\n## Addendum 2026-10-31, candidate B\n\nThe library now has **{len(catalog)} records**. Added by the [candidate B dossier]({LEDGER}).\n\n| Key and source | Publication/status | Last reading scope | Relevance and qualification |\n| --- | --- | --- | --- |\n"
    for key, title, authors, year, venue, url, status, scope, overlap, limit in added:
        text += f"| `{key}` — [{title}]({url}) | {status} | {DATE}: {scope} | {overlap} {limit} |\n"
refs.write_text(text.rstrip("\n") + "\n")
print(len(catalog), len(added))

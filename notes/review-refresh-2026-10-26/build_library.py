"""Merge primary-source research ledgers into the durable reference library.

This is record preparation, not an experiment or implementation test. Original
records are archived, original paper notes remain, and reading histories survive.
Run with uv; no third-party dependencies are needed.
"""
from pathlib import Path
import hashlib
import csv
import json
import re
import shutil
import unicodedata

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent
DATE = "2026-10-26"
ARCHIVE = PROJECT / "sources" / "library-before-refresh-2026-10-26"
ARCHIVE.mkdir(exist_ok=True)
for name, origin in (
    ("catalog.json", PROJECT / "sources" / "catalog.json"),
    ("REFERENCES.md", PROJECT / "REFERENCES.md"),
    ("references.bib", PROJECT / "references.bib"),
):
    if not (ARCHIVE / name).exists():
        shutil.copy2(origin, ARCHIVE / name)


def norm(value):
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", value.lower())


base = json.loads((ARCHIVE / "catalog.json").read_text())
records = {x["key"]: x for x in base}
aliases = {}
ledger_names = ["lead-sources.json", "researcher-sources.json", "benchmarks-sources.json", "verifier-sources.json"]
fresh_keys = set()
for name in ledger_names:
    for raw in json.loads((HERE / name).read_text()):
        source = dict(raw)
        key = source["key"]
        match = key if key in records else next((
            k for k, old in records.items()
            if norm(old["title"]) == norm(source["title"])
            or (source.get("doi") and old.get("doi", "").lower() == source["doi"].lower())
        ), None)
        if match and match != key:
            aliases[key] = match
        canonical = match or key
        if canonical not in records:
            records[canonical] = dict(source, key=canonical)
            records[canonical]["reading_history"] = []
        item = records[canonical]
        if "reading_history" not in item:
            item["reading_history"] = [{
                "date": "2026-10-23", "read_scope": item["read_scope"],
                "locations": item.get("locations", []), "source_ledger": item.get("source_ledger"),
                "limitation": item.get("limitation"),
            }]
        scope = source.get("refresh_read_scope", source["read_scope"])
        locations = source.get("refresh_locations", source.get("locations", []))
        if isinstance(locations, str):
            locations = [locations]
        ledger_path = f"notes/review-refresh-2026-10-26/{name}"
        item["reading_history"].append({
            "date": DATE, "read_scope": scope, "locations": locations,
            "source_ledger": ledger_path,
            "limitation": source.get("refresh_limitation", source.get("limitation")),
        })
        for field, value in source.items():
            if field not in {"key", "source_ledger", "reading_history"} and value is not None:
                item[field] = value
        item["key"] = canonical
        item["read_scope"] = scope
        item["locations"] = locations
        item["freshly_verified"] = DATE
        item["source_ledger"] = ledger_path
        fresh_keys.add(canonical)

# Reconcile publication fields where one track has the fuller primary record.
records["Zhou2026Learnability"].update({
    "url": "https://proceedings.mlr.press/v306/zhou26be.html",
    "arxiv_url": "https://arxiv.org/abs/2605.28057",
    "venue": "ICML 2026, PMLR 306:166172–166195",
    "publication_status": "Official ICML 2026 proceedings verified; linked arXiv is the same work.",
})
records["Schirmer2025Monitoring"]["venue"] = "NeurIPS 2025, Advances in Neural Information Processing Systems 38"
records["Schirmer2025Monitoring"]["url"] = "https://proceedings.neurips.cc/paper_files/paper/2025/hash/746960ad49ddb47248970a0e1404230c-Abstract-Conference.html"
records["Schirmer2025Monitoring"]["html_url"] = "https://arxiv.org/html/2507.08721v2"
records["Vianna2025ChannelSelective"]["publication_status"] = "PMLR volume published 2025 for the 3rd CoLLAs conference held 2024; established citation key preserved. Official PDF selectively read during refresh."
vianna_pdf = HERE / "verifier-evidence" / "Vianna2025ChannelSelective.pdf"
records["Vianna2025ChannelSelective"]["local_pdf"] = str(vianna_pdf.relative_to(PROJECT))
records["Vianna2025ChannelSelective"]["pdf_sha256"] = hashlib.sha256(vianna_pdf.read_bytes()).hexdigest()
records["Vianna2025ChannelSelective"]["local_text"] = str((HERE / "verifier-evidence" / "Vianna2025ChannelSelective.txt").relative_to(PROJECT))
records["Yeo2023RNA"]["read_scope"] = "Indexed official CVF PDF title block/abstract/introduction and author project feedback descriptions; direct CVF fetch returned 403, full training rollouts not audited."

ordered = sorted(records.values(), key=lambda x: (x["year"], x["key"]))
(PROJECT / "sources" / "catalog.json").write_text(json.dumps(ordered, ensure_ascii=False, indent=2) + "\n")
with (PROJECT / "sources" / "catalog.csv").open("w", newline="") as handle:
    fields = ["key", "title", "authors", "year", "venue", "url", "doi", "publication_status", "read_scope", "locations", "method_overlap", "limitation", "code_url", "freshly_verified", "source_ledger"]
    writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    for item in ordered:
        row = {field: item.get(field, "") for field in fields}
        row["authors"] = "; ".join(item["authors"])
        row["locations"] = "; ".join(item.get("locations", []))
        if item.get("publication_year_unknown"):
            row["year"] = ""
        writer.writerow(row)
(HERE / "citation-aliases.json").write_text(json.dumps(aliases, ensure_ascii=False, indent=2) + "\n")
scholarly = sum(x.get("kind") != "benchmark_documentation" for x in ordered)
new_count = len(ordered) - len(base)
summary = {
    "date": DATE, "total_distinct_records": len(ordered), "scholarly_records": scholarly,
    "benchmark_documentation_records": len(ordered)-scholarly,
    "inherited_records": len(base), "added_distinct_records": new_count,
    "freshly_inspected_distinct_records": len(fresh_keys),
    "new_paper_note_count": new_count, "aliases": aliases,
    "historical_primary_pdf_count": 9,
    "additional_primary_pdfs": ["notes/review-refresh-2026-10-26/verifier-evidence/Vianna2025ChannelSelective.pdf"],
    "scope": "Selective reading, primary-source metadata verification, and document critique. No research experiments or implementation tests.",
}
(HERE / "library-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")


def cell(text):
    return str(text).replace("|", "\\|").replace("\n", " ")


index = [
    "# Reference library for shift-aware test-time adaptation", "",
    f"Updated {DATE}. **{len(ordered)} distinct records: {scholarly} scholarly sources and {len(ordered)-scholarly} official benchmark/web records.** "
    f"The refresh adds {new_count} distinct records to the inherited {len(base)} and freshly inspects {len(fresh_keys)} distinct sources. "
    "Reading is selective, not uniformly full-paper reading. Date-specific scopes and limitations are preserved in sources/catalog.json.", "",
    "The user's 26 October request authorizes a fresh novelty assessment. Historical findings do not establish the new proposal. "
    "[Current review](outputs/shift-aware-tta-deep-review-2026-10-26.md), [provenance](outputs/shift-aware-tta-deep-review-2026-10-26.provenance.md), "
    "[deduplication aliases](notes/review-refresh-2026-10-26/citation-aliases.json). "
    "[Original library snapshot](sources/library-before-refresh-2026-10-26/) is retained.", "",
    "Stable citation keys are preserved; linked preprint/proceedings versions count once. "
    "Web documentation has an access date, not an invented publication year. Historical PDF downloads and results retain their original provenance.", "",
    "| Key and source | Publication/status | Last reading scope | Relevance and qualification |",
    "| --- | --- | --- | --- |",
]
bib = [f"% Research library refreshed {DATE}; reading scopes in REFERENCES.md and sources/catalog.json.",
       "% Original keys preserved. Web access dates are not publication dates.", ""]
for item in ordered:
    key = item["key"]
    checked = item.get("freshly_verified", "2026-10-23")
    year = "undated; accessed 2026" if item.get("publication_year_unknown") else item["year"]
    index.append(f"| `{key}` — [{cell(item['title'])}]({item['url']}) | {year}; {cell(item['venue'])} | "
                 f"{checked}: {cell(item['read_scope'])} | {cell(item['method_overlap'])} "
                 f"[Note](papers/{key}.md). |")
    paper_path = PROJECT / "papers" / f"{key}.md"
    refresh = ["", "## Literature refresh — 26 October 2026", "",
               f"Primary source: [{item['title']}]({item['url']}).", "",
               f"Reading scope: {item['read_scope']}", "",
               "Inspected locations: " + "; ".join(item.get("locations", [])) + ".", "",
               "Relevance (our reading): " + item["method_overlap"], "",
               "Boundary / reviewer qualification: " + item["limitation"], "",
               "Publication qualification: " + item["publication_status"], "",
               "No code or benchmark was run for this refresh. [Current synthesis](../outputs/shift-aware-tta-deep-review-2026-10-26.md). "
               "Detailed reading histories and original metadata remain in [catalog](../sources/catalog.json).", ""]
    if item.get("local_pdf"):
        refresh.extend([f"[Preserved primary PDF](../{item['local_pdf']}).", ""])
    if paper_path.exists():
        if key in fresh_keys:
            prior = paper_path.read_text().split("\n## Literature refresh — 26 October 2026")[0]
            paper_path.write_text(prior.rstrip() + "\n" + "\n".join(refresh))
    else:
        header = [f"# {item['title']}", "", f"Citation key: `{key}`.",
                  "Authors: " + "; ".join(item["authors"]) + ".",
                  f"Publication: {year}; {item['venue']}.",
                  "Status: selectively inspected; not a replication.", ""]
        paper_path.write_text("\n".join(header + refresh))
    kind = item.get("entry_type")
    venue = item["venue"].lower()
    if not kind:
        if item.get("kind") == "benchmark_documentation" or venue.startswith("arxiv"):
            kind = "misc"
        elif any(s in venue for s in ("journal", "transactions", "neurocomputing", "frontiers", "data mining")):
            kind = "article"
        else:
            kind = "inproceedings"
    venue_field = {"misc": "howpublished", "article": "journal", "inproceedings": "booktitle"}[kind]
    fields = [("title", "{" + item["title"] + "}"), ("author", " and ".join(item["authors"]))]
    if not item.get("publication_year_unknown"):
        fields.append(("year", str(item["year"])))
    fields.extend([(venue_field, item["venue"]), ("url", item["url"])])
    if item.get("doi"):
        fields.append(("doi", item["doi"]))
    fields.extend([("note", item["publication_status"]), ("urldate", checked)])
    bib.extend([f"@{kind}{{{key},"] + [f"  {field} = {{{value}}}," for field, value in fields] + ["}", ""])
(PROJECT / "REFERENCES.md").write_text("\n".join(index) + "\n")
(PROJECT / "references.bib").write_text("\n".join(bib))
(ARCHIVE / "manifest.json").write_text(json.dumps({
    name: hashlib.sha256((ARCHIVE / name).read_bytes()).hexdigest()
    for name in ("catalog.json", "REFERENCES.md", "references.bib")
}, indent=2) + "\n")
print(json.dumps(summary, indent=2))

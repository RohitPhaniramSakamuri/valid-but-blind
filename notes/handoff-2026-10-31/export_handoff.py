"""Export existing research context without executing or changing research code.

Uses the current catalog, not old source-ledger rebuilds. Writes only the handoff
source dossier and inventory. No network, third-party dependency or model work.
"""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent
DATE = "2026-10-31"
CATALOG = PROJECT / "sources" / "catalog.json"
sources = json.loads(CATALOG.read_text())
scholarly = sum(x.get("kind") != "benchmark_documentation" for x in sources)


def items(value):
    return value if isinstance(value, list) else [value]


def safe(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


out = [
    "# Full source dossier for the continuing research agent", "",
    f"Exported {DATE} from the existing catalog: **{len(sources)} distinct records, {scholarly} scholarly works and {len(sources)-scholarly} benchmark documents**. "
    "Last substantive review: 26 October 2026. This export performs no fresh source verification, full-paper reading or experiment.", "",
    "Read [HANDOFF](../../HANDOFF.md) first. [Current catalog](../../sources/catalog.json) retains machine-readable records; "
    "[BibTeX](../../references.bib) preserves citation keys. A source's presence does not mean its full method was read or its code executed. "
    "Read the per-entry scope/history and primary text before using an absence claim as novelty evidence.", "",
    "## Source index", "", "| Key | Source | Publication/status |", "| --- | --- | --- |",
]
for source in sources:
    out.append(f"| [{source['key']}](#{source['key'].lower()}) | {safe(source['title'])} | {safe(source['venue'])} |")

printed_fields = {
    "key", "title", "authors", "year", "venue", "url", "doi", "publication_status", "read_scope", "locations",
    "method_overlap", "limitation", "code_url", "freshly_verified", "source_ledger", "reading_history", "publication_year_unknown",
    "local_pdf", "local_text",
}
for source in sources:
    key = source["key"]
    year = "Publication year unknown; documentation accessed 2026" if source.get("publication_year_unknown") else str(source["year"])
    out.extend([
        "", f"## {key}", "", f"**{source['title']}**", "",
        "Authors: " + "; ".join(source["authors"]) + ".", "",
        f"Publication: {year}; {source['venue']}.", "",
        f"Primary source: [{source['title']}]({source['url']}). [Project paper note](../../papers/{key}.md).", "",
    ])
    if source.get("doi"):
        out.extend([f"Verified DOI in saved record: `{source['doi']}`.", ""])
    out.extend([
        "Publication qualification: " + source["publication_status"], "",
        "Recorded reading scope: " + source["read_scope"], "",
        "Inspected locations: " + "; ".join(str(x) for x in items(source.get("locations", []))) + ".", "",
        "Relevance / overlap from our reading: " + source["method_overlap"], "",
        "Limitation / reviewer boundary: " + source["limitation"], "",
    ])
    if source.get("freshly_verified"):
        out.extend([f"Fresh inspection date recorded by the earlier review: {source['freshly_verified']}. This is not the handoff-export date.", ""])
    if source.get("code_url"):
        out.extend([f"Recorded implementation/author resource: [link]({source['code_url']}). Availability/role follows the reading qualification; no execution is implied.", ""])
    for field, label in (("local_pdf", "Preserved primary PDF"), ("local_text", "Extracted text"), ("source_ledger", "Source ledger")):
        if source.get(field):
            out.extend([f"[{label}](../../{source[field]}).", ""])
    if source.get("reading_history"):
        out.extend(["### Recorded reading history", ""])
        for history in source["reading_history"]:
            out.append(f"- **{history.get('date', 'date not recorded')}**: {history.get('read_scope', 'scope not recorded')}")
            if history.get("locations"):
                out.append("  Locations: " + "; ".join(str(x) for x in items(history["locations"])) + ".")
            if history.get("limitation"):
                out.append("  Qualification: " + history["limitation"])
            if history.get("source_ledger"):
                out.append(f"  [Dated ledger](../../{history['source_ledger']}).")
            out.append("")
    extra = {k: v for k, v in source.items() if k not in printed_fields}
    if extra:
        out.extend(["### Other stored metadata", "", "```json", json.dumps(extra, ensure_ascii=False, indent=2), "```", ""])
(HERE / "source-dossier.md").write_text("\n".join(out) + "\n")


def role(path):
    if path in {"HANDOFF.md", "NEXT_AGENT_PROMPT.md"} or path.startswith("notes/handoff-2026-10-31/"):
        return "successor context / documentation export"
    if path.startswith("diagnostics/"):
        return "historical executed digit diagnostic; preserve original meaning; scripts may overwrite runs"
    if path.startswith("reports/") or path.startswith("papers/review-ii"):
        return "historical progress reporting; external aggregate provenance differs from local experiments"
    if path.startswith("sources/library-before-refresh"):
        return "preserved earlier bibliography snapshot"
    if path.startswith(("sources/pdfs/", "sources/text/")) or "/primary-snapshots/" in path or "/verifier-evidence/" in path:
        return "primary reading evidence; retention does not imply full reading"
    if path.startswith("sources/") or path in {"REFERENCES.md", "references.bib"}:
        return "bibliography / source catalog / retrieval provenance"
    if path.startswith("papers/"):
        return "source-specific paper note with reading qualification"
    if path.startswith("experiments/"):
        return "planned protocol; linked historical results remain separate"
    if path.startswith("notes/session-logs/"):
        return "durable session record"
    if path.startswith("notes/review-refresh-2026-10-26/"):
        return "fresh-review investigation, verification, ledger or record-preparation utility"
    if path.startswith("outputs/"):
        return "research synthesis / historical result report; consult document status"
    if path in {"README.md", "AGENTS.md", "APPROACH.md", "CHANGELOG.md"}:
        return "project entry point, scope or chronological status"
    return "supporting project research record"


excluded = {".git", ".venv", "node_modules", "__pycache__"}
manifest_path = HERE / "artifact-manifest.json"
files = []
for path in sorted(PROJECT.rglob("*")):
    rel = path.relative_to(PROJECT)
    if any(part in excluded for part in rel.parts) or path == manifest_path:
        continue
    if path.is_symlink():
        files.append({"path": str(rel), "kind": "symlink_not_followed", "role": role(str(rel))})
    elif path.is_file():
        data = path.read_bytes()
        files.append({"path": str(rel), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "role": role(str(rel))})
manifest = {
    "prepared_date": DATE,
    "project_directory": str(PROJECT),
    "last_substantive_literature_review": "2026-10-26",
    "source_records": len(sources),
    "scholarly_records": scholarly,
    "catalog_sha256": hashlib.sha256(CATALOG.read_bytes()).hexdigest(),
    "claim_status": "Broad routing is prior art; residual live-state/autonomous-selection gap is unverified.",
    "experiment_002_status": "planned; not implemented or executed",
    "historical_results": "Executed small-digit surrogate and separately user-reported external gate aggregates; no original image-benchmark results.",
    "entry_points": ["HANDOFF.md", "NEXT_AGENT_PROMPT.md", "README.md", "AGENTS.md"],
    "external_workspace_context": ["../AGENTS.md", "../README.md", "../templates/"],
    "excluded_directory_names": sorted(excluded),
    "self_excluded_to_avoid_hash_cycle": str(manifest_path.relative_to(PROJECT)),
    "file_count": len(files),
    "total_file_bytes": sum(x.get("bytes", 0) for x in files),
    "files": files,
}
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"source_records_exported": len(sources), "artifact_files_recorded": len(files), "source_dossier_words": len((HERE / "source-dossier.md").read_text().split())}, indent=2))

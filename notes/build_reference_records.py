"""Compile the reviewed source ledgers into project-local research records.

Only writes bibliography/index/paper-note records. Does not run experiments or
claim full-paper reading beyond the explicit per-source reading scopes.
"""
from pathlib import Path
import json
import re


PROJECT = Path(__file__).resolve().parent.parent
FILES = [
    "shift-aware-tta-review-lead-sources.json",
    "shift-aware-tta-review-researcher-sources.json",
    "shift-aware-tta-review-verifier-sources.json",
    "shift-aware-tta-review-reviewer-sources.json",
    "shift-aware-tta-review-followup-sources.json",
]
records = {}
titles = {}
for filename in FILES:
    source = json.loads((PROJECT / "notes" / filename).read_text())
    if isinstance(source, dict):
        source = source["sources"]
    for entry in source:
        title = re.sub(r"[^a-z0-9]", "", entry["title"].lower())
        if entry["key"] in records or title in titles:
            raise ValueError(f"Duplicate source key/title requires reconciliation: {entry['key']}")
        entry = dict(entry)
        entry["publication_status"] = entry.pop("publicationstatus", entry.get("publication_status", ""))
        entry["source_ledger"] = f"notes/{filename}"
        if isinstance(entry["locations"], str):
            entry["locations"] = [entry["locations"]]
        records[entry["key"]] = entry
        titles[title] = entry["key"]

records["Su2026SLRF"]["doi"] = "10.1007/s10618-026-01222-x"
records["Gai2026AdaTentPlusPlus"]["doi"] = "10.3389/frsip.2026.1842851"
records["Karimi2026ShiftACT"]["doi"] = "10.1016/j.neucom.2025.132013"
records["Cygert2026RealisticSelection"]["doi"] = "10.5220/0014320100004084"
records["Danilowski2026MORPHEUS"].update({
    "pdf_url": "https://theyoungkwon.github.io/papers/articles/danilowski_morpheus_iclr-ttu26.pdf",
    "read_scope": "Author PDF downloaded; abstract, sections 1–3, meta-training description and selected appendix/table passages read. Workshop status checked against PDF header and author publication page.",
    "locations": ["Section 2, Problem and Methodology", "Section 3", "Appendix split descriptions"],
    "limitation": "Supervised auxiliary-domain development precedes unlabeled selection. Text/table numbers and feature definitions need care; no numerical result is copied as our reproduction. Official code not verified.",
})
records["Doloriel2026SEGA"].update({
    "read_scope": "Abstract, sections 3.2–3.3, Algorithm 1 and selected conclusion passages from downloaded PDF; partial reading.",
    "locations": ["Sections 3.2–3.3", "Algorithm 1", "Conclusion"],
    "limitation": "Algorithm 1 computes N declared erasure levels and gates updates/recovery. This is probe-based adaptation control, rather than the proposed learned net-value acquisition across a whole-method menu. No full code audit.",
})
records["Zhang2026MoASEPlusPlus"].update({
    "read_scope": "Abstract, routing description and section 5.2 including equations 11–16 from downloaded PDF; partial reading.",
    "locations": ["Section 5.2", "Equations 11–16"],
    "limitation": "Learned augmentation strength uses a teacher-distillation/strength reward. That is close prior art for policy-driven augmentation, not an audited costed whole-method evidence selector. No implementation execution.",
})
records["Cygert2026RealisticSelection"]["read_scope"] += "; published PDF downloaded and title/author block checked"
records["Yang2026SATTS"]["read_scope"] = "Downloaded official CVF PDF: title/author block, abstract, Algorithm 1, methodology and scope discussion; partial reading."
records["Jiang2026CAS"]["read_scope"] = "Primary arXiv metadata and full HTML sections 2–3.3, including episodic scope and the CAS decision rule; no code audit."
records["Liang2025TTASurvey"]["publication_status"] += "; publisher metadata checked: online 18 July 2024, volume year 2025"

manifest = json.loads((PROJECT / "sources" / "manifest.json").read_text())
aliases = {"Cygert2026Selection": "Cygert2026RealisticSelection"}
for download in manifest:
    key = aliases.get(download["key"], download["key"])
    if key in records and download["status"] == "downloaded":
        records[key]["local_pdf"] = str(Path("sources/pdfs") / Path(download["pdf"]).name)
        records[key]["pdf_sha256"] = download["sha256"]

ordered = sorted(records.values(), key=lambda source: (source["year"], source["key"]))
(PROJECT / "sources" / "catalog.json").write_text(json.dumps(ordered, indent=2, ensure_ascii=False) + "\n")
(PROJECT / "papers").mkdir(exist_ok=True)


def safe(text):
    return str(text).replace("|", "\\|").replace("\n", " ")


index = ["# Reference library for shift aware test time adaptation", "",
         f"Review date: 23 October 2026. {len(ordered)} distinct primary scholarly sources are indexed. Reading is selective; each entry states the actual scope. A bibliography entry or downloaded PDF does not imply full-paper reading or reproduction.", "",
         "Stable citation keys are used across the review, notes and BibTeX. Journal/conference versions and preprints refer to the same source where linked. Public code links are recorded only where verified in the source/repository review; no code was executed.", "",
         "| Key and source | Year and publication | Reading scope | Relevance and notes |", "| --- | --- | --- | --- |"]
bib = ["% Compiled from primary-source metadata verified during the 2026-10-23 review.",
       "% Reading scopes and version/venue qualifications are in REFERENCES.md and sources/catalog.json.", ""]
for item in ordered:
    key = item["key"]
    index.append(f"| `{key}` — [{safe(item['title'])}]({item['url']}) | {item['year']}; {safe(item['venue'])} | {safe(item['read_scope'])} | {safe(item['method_overlap'])} [Note](papers/{key}.md). |")
    local = f"[Local PDF](../{item['local_pdf']})" if item.get("local_pdf") else "No local PDF in this project."
    code = f"[Public implementation / author resource]({item['code_url']})" if item.get("code_url") else "Implementation availability not established by this review."
    note = [f"# {item['title']}", "", f"Citation key: `{key}`.",
            "Authors: " + "; ".join(item["authors"]) + ".",
            f"Year and venue: {item['year']}; {item['venue']}.",
            f"Publication/version status: {item['publication_status']}.",
            f"[Authoritative source]({item['url']}). {local}",
            f"Reading progress: {item['read_scope']}", "",
            "## Research question and contribution", "", item["method_overlap"], "",
            "## Background needed", "", "See the linked review for the decision variable and information regime; clarify prerequisites during reading.", "",
            "## Reading notes", "", "Inspected locations: " + "; ".join(item["locations"]) + ".", "",
            "## Method and implementation", "", code + " The literature-review stage did not execute this paper's code or reproduce its benchmark. The later custom digit diagnostic is a separate surrogate study, described in the project README.", "",
            "## Evidence and limitations", "", item["limitation"], "",
            "## Connection to our research", "", "This source constrains the proposed contribution; distinguish its actual decision and evidence access from our acquisition hypothesis. [Review](../outputs/shift-aware-tta-review.md).", "",
            "## Possible experiment", "", "Compare legal evidence and total cost under the [planned protocol](../experiments/001-policy-selection-pilot.md) where the source's task and method can be matched.", "",
            "## Next reading step", "", "Inspect remaining method, split and code details before choosing an implementation baseline or claiming the paper omits a specific test.", ""]
    (PROJECT / "papers" / f"{key}.md").write_text("\n".join(note))
    is_preprint = item["venue"].lower().startswith("arxiv") or "arxiv preprint" in item["venue"].lower()
    is_journal = any(word in item["venue"].lower() for word in ("journal", "neurocomputing", "frontiers", "data mining")) and not is_preprint
    kind = "misc" if is_preprint else ("article" if is_journal else "inproceedings")
    venue_field = "howpublished" if kind == "misc" else ("journal" if kind == "article" else "booktitle")
    fields = [("title", "{" + item["title"] + "}"), ("author", " and ".join(item["authors"])),
              ("year", str(item["year"])), (venue_field, item["venue"]), ("url", item["url"])]
    if item.get("doi"):
        fields.append(("doi", item["doi"]))
    fields += [("note", item["publication_status"]), ("urldate", "2026-10-23")]
    bib.append(f"@{kind}{{{key},")
    for field, value in fields:
        bib.append(f"  {field} = {{{value}}},")
    bib += ["}", ""]
(PROJECT / "REFERENCES.md").write_text("\n".join(index) + "\n")
(PROJECT / "references.bib").write_text("\n".join(bib))
print(json.dumps({"distinct_sources": len(ordered), "paper_notes": len(ordered),
                  "local_pdfs": sum(bool(item.get('local_pdf')) for item in ordered)}, indent=2))

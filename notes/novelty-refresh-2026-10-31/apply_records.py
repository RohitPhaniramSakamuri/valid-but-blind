"""Append the 31 October 2026 novelty-refresh records to the current library.

Append-only and idempotent: existing records are never rewritten, only given an
extra reading_history entry. It does not rebuild anything from older ledgers.
Warning: notes/review-refresh-2026-10-26/build_library.py would drop these
additions if rerun, because it reconstructs from a fixed archived base.
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATE = "2026-10-31"
LEDGER = "outputs/novelty-dossier-2026-10-31.md"

NEW = [
    dict(
        key="Zhang2026HarnessLearning",
        title="Harness Learning Enables Generalizable Test-Time Adaptation",
        authors=["Alvin Zhang", "Xuecheng Liu", "Zixuan Wang", "Fahim Tajwar", "Daman Arora",
                 "Ruslan Salakhutdinov", "Daniel Khashabi", "Yuda Song", "Andrea Zanette"],
        year=2026, venue="arXiv preprint 2609.35738", url="https://arxiv.org/abs/2609.35738",
        publication_status="arXiv v1, 28 September 2026; no venue verified",
        read_scope="Selective arXiv HTML: abstract, §4.3, §5.3–5.4, Appendix F opening.",
        locations=["Section 4.3", "Section 5.4", "Appendix F"],
        method_overlap="Trains a proposer on successive self-generated revision states; §5.4 reports no consistent gain over training on individual revisions.",
        limitation="LLM agent harnesses with prescribed revision reports, not visual TTA. A warning about the remedy, not a transferable result.",
        note="Adjacent precedent for training on self-generated states.",
    ),
    dict(
        key="Singh2026ReliabilityGated",
        title="Reliability-Gated Source Anchoring for Continual Test-Time Adaptation",
        authors=["Vikash Singh", "Debargha Ganguly", "Weicong Chen", "Sabyasachi Sahoo", "Sreehari Sankar",
                 "Biyao Zhang", "Mohsen Hariri", "Shouren Wang", "Osama Zafar", "Christian Gagné", "Vipin Chaudhary"],
        year=2026, venue="arXiv preprint 2605.14063", url="https://arxiv.org/abs/2605.14063",
        publication_status="arXiv v2, 19 May 2026; marked preprint; no venue verified",
        read_scope="PDF abstract, introduction opening and limitations section heading text only.",
        locations=["Abstract", "Section 1", "Broader Impact and Limitations"],
        method_overlap="Source-posterior entropy gates source-coupled terms in ROID ('blind anchoring'); frozen-source reliability is itself questioned.",
        limitation="Abstract says the gate detects high-entropy source collapse but not wrong low-entropy sources. Gates an anchor; does not choose among actions. Numerical claims are the authors' and unreplicated.",
        note="Weakens any assumption that frozen-source evidence is safe.",
    ),
    dict(
        key="Press2024EntropyEnigma",
        title="The Entropy Enigma: Success and Failure of Entropy Minimization",
        authors=["Ori Press", "Ravid Shwartz-Ziv", "Yann LeCun", "Matthias Bethge"],
        year=2024, venue="ICML 2024, PMLR 235", url="https://arxiv.org/abs/2405.05012",
        publication_status="Venue from the footer of arXiv v2; PMLR page not separately opened",
        read_scope="arXiv PDF abstract, introduction and §4 opening.",
        locations=["Abstract", "Section 4"],
        method_overlap="Explains early success and later failure of entropy minimization; estimates dataset accuracy from weighted prediction flips during adaptation.",
        limitation="Dataset-level accuracy estimation, not stream action selection.",
        note="Close predecessor for evidence behaviour under adaptation.",
    ),
    dict(
        key="Kim2026OATTA",
        title="Order-Aware Test-Time Adaptation: Leveraging Temporal Dynamics for Robust Streaming Inference",
        authors=["Young Kyung Kim", "Oded Schlesinger", "Qiangqiang Wu", "J. Matías Di Martino", "Guillermo Sapiro"],
        year=2026, venue="arXiv preprint 2601.21012", url="https://arxiv.org/abs/2601.21012",
        publication_status="arXiv v1, 28 January 2026; no venue verified",
        read_scope="Abstract only.",
        locations=["Abstract"],
        method_overlap="Gradient-free recursive Bayesian refinement with a learned transition matrix; likelihood-ratio gate reverts to the base predictor.",
        limitation="Abstract only; supports no claim about the full method or experiments.",
        note="Order-aware gate; lower priority.",
    ),
]

HISTORY = {
    "Lu2026AgenticTTT": ("Fresh text of §2.2.2 and Appendix E; quotations checked.", ["Section 2.2.2", "Appendix E"]),
    "Jhawar2026Identifiability": ("§4.1, Table 1, §5.2 and §7 rechecked; paper marked under review at ICLR 2027.", ["Section 4.1", "Table 1", "Section 7"]),
    "Lim2026ASR": ("§§3.3–3.5 passages and released methods/base.py asr_reset (default branch, commit not pinned): the code restores optimizer state on reset.", ["Sections 3.3–3.5", "methods/base.py"]),
    "Sahoo2025GALA": ("§§2.1–2.3: hand-set cosine threshold on displacement since an anchor.", ["Sections 2.1–2.3"]),
    "Park2025HybridTTA": ("§4.1 and supplement: hand-set loss-EMA rule; values chosen on a subset of the first target domain.", ["Section 4.1", "Supplement"]),
    "Yeo2023RNA": ("arXiv v1 2309.15762 §3: original weights frozen; controller needs only a forward pass. CVF PDF still returned 403.", ["Section 3"]),
    "Danilowski2026MORPHEUS": ("Saved text §§1–3 and Table 1. Our arithmetic: per-corruption oracle 65.75% versus SPA 65.25%.", ["Sections 1–3", "Table 1"]),
    "Zhao2023Pitfalls": ("PMLR PDF abstract and §4.1 on batch dependency.", ["Abstract", "Section 4.1"]),
    "Lee2024AETTA": ("CVF PDF §3.2 and results discussion on calibration violation under adaptation failure.", ["Section 3.2", "Results"]),
    "Cygert2026RealisticSelection": ("Saved text: selection-over-time figure discussion and §6.", ["Selection figure text", "Section 6"]),
    "Su2026SLRF": ("Crossref and Semantic Scholar metadata only; full text closed, Springer redirected to login.", ["Metadata"]),
}


def bib_entry(r):
    return (f"\n@misc{{{r['key']},\n  title = {{{{{r['title']}}}}},\n  author = {{{' and '.join(r['authors'])}}},\n"
            f"  year = {{{r['year']}}},\n  howpublished = {{{r['venue']}}},\n  url = {{{r['url']}}},\n"
            f"  note = {{{r['publication_status']}}},\n  urldate = {{{DATE}}},\n}}\n")


def main():
    path = ROOT / "sources/catalog.json"
    catalog = json.loads(path.read_text())
    keys = {r["key"] for r in catalog}
    missing = set(HISTORY) - keys
    if missing:
        raise SystemExit(f"Unknown keys: {missing}")

    for r in catalog:
        if r["key"] in HISTORY:
            scope, locs = HISTORY[r["key"]]
            history = r.setdefault("reading_history", [])
            if not any(h.get("date") == DATE for h in history):
                history.append(dict(date=DATE, read_scope=scope, locations=locs, source_ledger=LEDGER))
                r["freshly_verified"] = DATE

    added = [r for r in NEW if r["key"] not in keys]
    for r in added:
        catalog.append({
            "key": r["key"], "title": r["title"], "authors": r["authors"], "year": r["year"], "venue": r["venue"],
            "entry_type": "misc", "url": r["url"], "read_scope": r["read_scope"], "locations": r["locations"],
            "method_overlap": r["method_overlap"], "limitation": r["limitation"],
            "publication_status": r["publication_status"],
            "reading_history": [dict(date=DATE, read_scope=r["read_scope"], locations=r["locations"], source_ledger=LEDGER)],
            "freshly_verified": DATE, "source_ledger": LEDGER, "accessed": DATE,
        })
    path.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n")

    with (ROOT / "sources/catalog.csv").open("a", newline="") as f:
        w = csv.writer(f)
        for r in added:
            w.writerow([r["key"], r["title"], "; ".join(r["authors"]), r["year"], r["venue"], r["url"], "",
                        r["publication_status"], r["read_scope"], "; ".join(r["locations"]), r["method_overlap"],
                        r["limitation"], "", DATE, LEDGER])

    with (ROOT / "references.bib").open("a") as f:
        f.writelines(bib_entry(r) for r in added)

    refs = ROOT / "REFERENCES.md"
    text = refs.read_text().rstrip("\n")
    if "Addendum 2026-10-31" not in text:
        text += ("\n\n## Addendum 2026-10-31\n\nThe library now has **107 records: 105 scholarly and 2 official "
                 "benchmark/web records**. The four below were added by the [novelty dossier]"
                 "(outputs/novelty-dossier-2026-10-31.md); eleven existing records gained dated reading history in "
                 "`sources/catalog.json`.\n\n| Key and source | Publication/status | Last reading scope | Relevance and qualification |\n| --- | --- | --- | --- |\n")
        for r in NEW:
            text += f"| `{r['key']}` — [{r['title']}]({r['url']}) | {r['publication_status']} | {DATE}: {r['read_scope']} | {r['method_overlap']} {r['limitation']} |\n"
    refs.write_text(text.rstrip("\n") + "\n")

    for r in NEW:
        note = ROOT / "papers" / f"{r['key']}.md"
        if not note.exists():
            note.write_text(
                f"# {r['title']}\n\nCitation key: `{r['key']}`\nAuthors, year, and venue: {', '.join(r['authors'])}; {r['year']}; {r['venue']}.\n"
                f"Authoritative link: {r['url']}\nStatus: {r['publication_status']}.\nReading progress: {DATE}: {r['read_scope']}\n\n"
                f"## What the inspected passages cover\n\n{r['method_overlap']} Locations: {', '.join(r['locations'])}.\n\n"
                f"## Limitations for our use\n\n{r['limitation']}\n\n## Connection to our research (our interpretation)\n\n{r['note']} See the [dossier](../{LEDGER}).\n\n"
                f"## Next reading step\n\nRead the remaining sections before relying on this source for any claim beyond the passages above.\n")

    for key, (scope, locs) in HISTORY.items():
        note = ROOT / "papers" / f"{key}.md"
        if note.exists() and f"## Reading update {DATE}" not in note.read_text():
            with note.open("a") as f:
                f.write(f"\n## Reading update {DATE}\n\n{scope} Locations: {', '.join(locs)}. See the [dossier](../{LEDGER}).\n")

    print(f"catalog={len(catalog)} added={len(added)} updated_history={len(HISTORY)}")


if __name__ == "__main__":
    main()

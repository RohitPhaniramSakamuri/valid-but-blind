"""Build the assessment DOCX from current project records; no experiment execution.

Run from this directory: uv run --no-project python build_report.py
Uses the already installed python-docx package.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from lxml import etree


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
CONTENT = json.loads((HERE / "report_content.json").read_text())
SOURCES = {r["key"]: r for r in json.loads((PROJECT / "sources/catalog.json").read_text())}
OUTPUT = HERE / "ML_Assessment_Rohit_23BDS0051.docx"
BLACK = RGBColor(0, 0, 0)


def set_font(style, size, bold=False):
    style.font.name = "Arial"
    style.font.size = Pt(size)
    style.font.bold = bold
    style.font.italic = False
    style.font.color.rgb = BLACK
    rpr = style.element.get_or_add_rPr()
    fonts = rpr.find(qn("w:rFonts"))
    if fonts is None:
        fonts = OxmlElement("w:rFonts")
        rpr.insert(0, fonts)
    for attr in ("ascii", "hAnsi", "eastAsia", "cs"):
        fonts.set(qn("w:" + attr), "Arial")
    for attr in ("asciiTheme", "hAnsiTheme", "eastAsiaTheme", "cstheme"):
        fonts.attrib.pop(qn("w:" + attr), None)


def add_table(doc, block):
    caption = doc.add_paragraph(block["caption"], "Caption")
    caption.paragraph_format.keep_with_next = True
    table = doc.add_table(rows=1, cols=len(block["headers"]))
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    table.autofit = False
    for col, width in zip(table.columns, block["widths"]):
        col.width = Inches(width)
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement("w:" + edge)
        for attr, val in (("val", "single"), ("sz", "4"), ("color", "000000")):
            el.set(qn("w:" + attr), val)
        borders.append(el)
    table._tbl.tblPr.append(borders)
    repeat_header = OxmlElement("w:tblHeader")
    table.rows[0]._tr.get_or_add_trPr().append(repeat_header)
    for cell, text in zip(table.rows[0].cells, block["headers"]):
        cell.text = text
    for values in block["rows"]:
        row = table.add_row()
        for cell, text in zip(row.cells, values):
            cell.text = text
    for row_index, row in enumerate(table.rows):
        no_split = OxmlElement("w:cantSplit")
        row._tr.get_or_add_trPr().append(no_split)
        for cell, width in zip(row.cells, block["widths"]):
            cell.width = Inches(width)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            margins = OxmlElement("w:tcMar")
            for side in ("top", "left", "bottom", "right"):
                el = OxmlElement("w:" + side)
                el.set(qn("w:w"), "85")
                el.set(qn("w:type"), "dxa")
                margins.append(el)
            cell._tc.get_or_add_tcPr().append(margins)
            for paragraph in cell.paragraphs:
                paragraph.paragraph_format.space_after = Pt(2)
                paragraph.paragraph_format.space_before = Pt(2)
                paragraph.paragraph_format.line_spacing = 1.0
                for run in paragraph.runs:
                    run.font.name = "Arial"
                    run.font.size = Pt(10.5)
                    run.font.color.rgb = BLACK
                    run.bold = row_index == 0
    after = doc.add_paragraph()
    after.paragraph_format.space_after = Pt(1)
    after.paragraph_format.line_spacing = 0.25
    after.add_run().font.size = Pt(2)


def reference_text(number, key):
    record = SOURCES[key]
    authors = record["authors"]
    author_string = ", ".join(authors) if len(authors) <= 4 else ", ".join(authors[:2]) + ", et al."
    venue = re.sub(r"\s+", " ", record["venue"])
    venue = venue.replace("NeurIPS2025", "NeurIPS 2025").replace("Systems38", "Systems 38")
    venue = re.sub(r"pp\.(?=\d)", "pp. ", venue)
    return f"[{number}] {author_string} ({record['year']}). {record['title']}. {venue}."


def make_document():
    doc = Document()
    section = doc.sections[0]
    section.page_width = Inches(8.2677)
    section.page_height = Inches(11.6929)
    section.top_margin = section.bottom_margin = Inches(0.8)
    section.left_margin = section.right_margin = Inches(1.0)
    section.header_distance = section.footer_distance = Inches(0.35)
    set_font(doc.styles["Normal"], 12)
    normal = doc.styles["Normal"].paragraph_format
    normal.line_spacing = 1.08
    normal.space_after = Pt(7)
    normal.widow_control = True
    set_font(doc.styles["Title"], 20, True)
    set_font(doc.styles["Subtitle"], 14, True)
    set_font(doc.styles["Heading 1"], 18, True)
    set_font(doc.styles["Heading 2"], 13, True)
    for name in ("Heading 1", "Heading 2"):
        pf = doc.styles[name].paragraph_format
        pf.space_before = Pt(12)
        pf.space_after = Pt(6)
        pf.line_spacing = 1.0
        pf.keep_with_next = True
        pf.keep_together = True
    set_font(doc.styles["Caption"], 11, True)
    doc.styles["Caption"].font.italic = False
    set_font(doc.styles["Footer"], 10)
    set_font(doc.styles["List Number"], 12)
    doc.styles["List Number"].paragraph_format.space_after = Pt(4)

    p = doc.add_paragraph(CONTENT["course"], "Title")
    p.paragraph_format.space_after = Pt(12)
    p = doc.add_paragraph(CONTENT["author"], "Subtitle")
    p.paragraph_format.space_after = Pt(3)
    p = doc.add_paragraph(CONTENT["registration"])
    p.paragraph_format.space_after = Pt(8)
    doc.add_heading("Title", 1)
    title = doc.add_paragraph()
    title.paragraph_format.space_after = Pt(8)
    title.paragraph_format.keep_with_next = True
    run = title.add_run(CONTENT["title"])
    run.bold = True
    run.font.size = Pt(18)

    for block in CONTENT["blocks"]:
        kind = block["kind"]
        if kind == "heading":
            heading = doc.add_heading(block["text"], 1)
            if block["text"] == "References":
                heading.paragraph_format.page_break_before = True
        elif kind == "subheading":
            doc.add_heading(block["text"], 2)
        elif kind == "table":
            add_table(doc, block)
        elif kind == "numbered":
            doc.add_paragraph(block["text"], "List Number")
        else:
            p = doc.add_paragraph()
            if block.get("lead"):
                p.add_run(block["lead"]).bold = True
            p.add_run(block["text"])

    for number, key in enumerate(CONTENT["reference_keys"], 1):
        p = doc.add_paragraph(reference_text(number, key))
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_together = True
        for run in p.runs:
            run.font.size = Pt(10.5)

    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    field = OxmlElement("w:fldSimple")
    field.set(qn("w:instr"), "PAGE")
    footer._p.append(field)

    # Use explicit black text and white fills, including inherited Word styles.
    for style in doc.styles:
        if style.type in (1, 2):
            style.font.color.rgb = BLACK
    for part in doc.part.package.parts:
        if str(part.partname).startswith("/word/theme/"):
            root = etree.fromstring(part.blob)
            ans = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
            scheme = root.find("a:themeElements/a:clrScheme", ans)
            if scheme is not None:
                for item in scheme:
                    light = etree.QName(item).localname.startswith("lt")
                    for child in list(item):
                        item.remove(child)
                    rgb = etree.SubElement(item, "{" + ans["a"] + "}srgbClr")
                    rgb.set("val", "FFFFFF" if light else "000000")
            part._blob = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)
    for root in (doc.element, doc.styles.element):
        for border in list(root.iter(qn("w:pBdr"))):
            border.getparent().remove(border)
        for el in root.iter():
            if qn("w:color") in el.attrib:
                el.set(qn("w:color"), "000000")
            if el.tag == qn("w:color"):
                el.set(qn("w:val"), "000000")
                for attr in list(el.attrib):
                    if "theme" in attr.lower():
                        del el.attrib[attr]
            elif el.tag == qn("w:shd"):
                el.set(qn("w:fill"), "FFFFFF")
                for attr in list(el.attrib):
                    if "theme" in attr.lower():
                        del el.attrib[attr]

    props = doc.core_properties
    props.title = CONTENT["title"]
    props.author = CONTENT["author"]
    props.last_modified_by = CONTENT["author"]
    props.subject = "Machine Learning Assessment - " + CONTENT["registration"]
    props.comments = ""
    props.keywords = "test-time adaptation, risk monitoring, CIFAR-100-C"
    props.created = props.modified = datetime.now(timezone.utc)
    doc.save(OUTPUT)

    used_sources = [{"number": n, **SOURCES[key]} for n, key in enumerate(CONTENT["reference_keys"], 1)]
    (HERE / "report_sources.json").write_text(json.dumps(used_sources, indent=2, ensure_ascii=False) + "\n")
    text = "\n".join(p.text for p in doc.paragraphs)
    words = len(text.split()) + sum(len(c.text.split()) for t in doc.tables for row in t.rows for c in row.cells)
    print(json.dumps({"output": str(OUTPUT), "words_including_tables": words, "references": len(used_sources), "tables": len(doc.tables)}, indent=2))


if __name__ == "__main__":
    make_document()

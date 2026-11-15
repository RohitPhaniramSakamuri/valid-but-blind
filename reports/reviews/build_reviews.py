"""Prepare review presentations from supplied templates and saved research records.

Document generation only: this script does not execute scientific experiments.
Use: uv run --no-project --cache-dir /tmp/rohit-review-uv python reports/reviews/build_reviews.py
"""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from copy import deepcopy
from io import BytesIO
import json
import re
import hashlib
import xml.etree.ElementTree as ET
from lxml import etree as LX

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_LEGEND_POSITION
from pptx.chart.data import CategoryChartData
from docx import Document
from docx.shared import Inches as DInches, Pt as DPt, RGBColor as DColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
NAME = 'Rohit Phaniram Sakamuri'
ID = '23BDS0051'
REPO = 'https://github.com/RohitPhaniramSakamuri/valid-but-blind'
INK = '172B3A'
TEAL = '087E83'
GRAY = '55636B'
LIGHT = 'EEF5F5'
WHITE = 'FFFFFF'
LINE = 'D4DFE2'
ORANGE = 'A35A18'
FONT = 'Calibri'

# Bibliographic records are reused from the local library. Publication years are
# deliberately absent from visible citations, as requested for these artifacts.
REFS = {
 'tent': ('Wang et al.', 'Tent: Fully Test-Time Adaptation by Entropy Minimization.', 'ICLR', 'https://github.com/DequanWang/tent'),
 'ttn': ('Lim et al.', 'TTN: A Domain-Shift Aware Batch Normalization in Test-Time Adaptation.', 'ICLR', 'https://github.com/lim-h/TTN'),
 'morpheus': ('Danilowski et al.', 'MORPHEUS: Meta Test-Time Adaptation via Neural Collapse Geometry.', 'ICLR Test-Time Updates Workshop', 'https://openreview.net/forum?id=YfyApJH1Rj'),
 'monitor': ('Schirmer et al.', 'Monitoring Risks in Test-Time Adaptation.', 'NeurIPS', 'https://arxiv.org/abs/2507.08721'),
 'aetta': ('Lee et al.', 'AETTA: Label-Free Accuracy Estimation for Test-Time Adaptation.', 'CVPR', 'https://openaccess.thecvf.com/content/CVPR2024/html/Lee_AETTA_Label-Free_Accuracy_Estimation_for_Test-Time_Adaptation_CVPR_2024_paper.html'),
 'sar': ('Niu et al.', 'Towards Stable Test-Time Adaptation in Dynamic Wild World.', 'ICLR', 'https://github.com/mr-eggplant/SAR'),
 'atc': ('Garg et al.', 'Leveraging Unlabeled Data to Predict Out-of-Distribution Performance.', 'ICLR', 'https://arxiv.org/abs/2201.04234'),
 'doc': ('Guillory et al.', 'Predicting with Confidence on Unseen Distributions.', 'ICCV', 'https://arxiv.org/abs/2107.03315'),
 'cifar': ('Hendrycks and Dietterich.', 'Benchmarking Neural Network Robustness to Common Corruptions and Perturbations.', 'ICLR', 'https://github.com/hendrycks/robustness'),
 'med': ('Yang et al.', 'MedMNIST v2: A large-scale lightweight benchmark for 2D and 3D biomedical image classification.', 'Scientific Data', 'https://medmnist.com/'),
 'han': ('Han et al.', 'The Premise Is the Problem: Exchangeability Failure in Self-Monitored Test-Time Adaptation.', 'Preprint', 'https://arxiv.org/abs/2610.07038'),
}

# Prefer the exact primary-source URLs already verified in the project library.
_catalog = {r['key']:r for r in json.loads((ROOT/'sources/catalog.json').read_text())}
for _short, _key in {'tent':'Wang2021Tent', 'ttn':'Lim2023TTN',
                     'morpheus':'Danilowski2026MORPHEUS', 'monitor':'Schirmer2025Monitoring',
                     'aetta':'Lee2024AETTA', 'sar':'Niu2023SAR', 'atc':'Garg2022ATC',
                     'han':'Han2026Exchangeability'}.items():
    REFS[_short] = (*REFS[_short][:3], _catalog[_key]['url'])


def color(h):
    return RGBColor.from_string(h)


def text(s, x, y, w, h, value, size=20, bold=False, shade=INK, align=None, link=None):
    box = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(.015)
    tf.margin_top = tf.margin_bottom = Inches(.015)
    for i, line in enumerate(value.split('\n')):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.space_after = Pt(4)
        p.line_spacing = 1.05
        if align is not None:
            p.alignment = align
        for run in p.runs:
            run.font.name = FONT
            run.font.size = Pt(size)
            run.font.bold = bold
            run.font.color.rgb = color(shade)
            if link:
                run.hyperlink.address = link
    return box


def rect(s, x, y, w, h, fill=LIGHT, stroke=None, radius=False):
    sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE,
                            Inches(x), Inches(y), Inches(w), Inches(h))
    sh.fill.solid()
    sh.fill.fore_color.rgb = color(fill)
    if stroke:
        sh.line.color.rgb = color(stroke)
        sh.line.width = Pt(.8)
    else:
        sh.line.fill.background()
    effect = sh._element.find('.//{http://schemas.openxmlformats.org/drawingml/2006/main}effectRef')
    if effect is not None:
        effect.set('idx','0')
    if radius:
        sh.adjustments[0] = .08
    return sh


def arrow(s, x, y, w=.42, h=.25, shade=TEAL):
    sh = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.fill.solid()
    sh.fill.fore_color.rgb = color(shade)
    sh.line.fill.background()
    return sh


def callout(s, value, y=6.18, shade=TEAL, size=18):
    rect(s, .55, y, 8.9, .57, LIGHT)
    text(s, .72, y+.08, 8.52, .44, value, size, True, shade)


def paragraph(s, label, value, y, size=20, x=.6, w=8.8, h=.96):
    text(s, x, y, w, .32, label.upper(), 12, True, TEAL)
    text(s, x, y+.39, w, h, value, size)


def cards(s, entries, y=1.75, height=2.6):
    n = len(entries)
    gap = .2
    w = (8.9 - gap*(n-1))/n
    for i, (label, body) in enumerate(entries):
        x = .55+i*(w+gap)
        rect(s, x, y, w, height, LIGHT)
        text(s, x+.18, y+.18, w-.36, .64, label, 20 if height<2.5 else 23, True, TEAL)
        text(s, x+.18, y+.9, w-.36, height-.97, body, 17 if height<2.5 else 20)


def table(s, headers, rows, widths, y=1.75, h=3.9, size=17, x=.55):
    tab = s.shapes.add_table(len(rows)+1, len(headers), Inches(x), Inches(y),
                             Inches(sum(widths)), Inches(h)).table
    for col, width in zip(tab.columns, widths):
        col.width = Inches(width)
    # A modest header and generous body rows prevent accidental multi-line clipping.
    tab.rows[0].height = Inches(.48)
    for row in list(tab.rows)[1:]:
        row.height = Inches((h-.48)/len(rows))
    for i, vals in enumerate([headers]+rows):
        for j, val in enumerate(vals):
            cell = tab.cell(i,j)
            cell.text = str(val)
            cell.margin_left = cell.margin_right = Inches(.10)
            cell.margin_top = cell.margin_bottom = Inches(.06)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            cell.fill.fore_color.rgb = color(INK if i==0 else (LIGHT if i%2 else WHITE))
            for p in cell.text_frame.paragraphs:
                p.space_after = Pt(1)
                p.line_spacing = 1.02
                for r in p.runs:
                    r.font.name = FONT
                    r.font.size = Pt(size if i else size-1)
                    r.font.bold = i==0
                    r.font.color.rgb = color(WHITE if i==0 else INK)
    return tab


def barchart(s, labels, values, x, y, w, h, maxval=100, colors=None, size=14, title=None):
    d = CategoryChartData()
    d.categories = labels
    d.add_series('Rate (%)', values)
    chart = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Inches(x), Inches(y),
                              Inches(w), Inches(h), d).chart
    chart.has_legend = False
    chart.has_title = False
    chart.chart_style = 10
    chart.value_axis.minimum_scale = 0
    chart.value_axis.maximum_scale = maxval
    chart.value_axis.major_unit = maxval/4
    chart.value_axis.tick_labels.font.name = FONT
    chart.value_axis.tick_labels.font.size = Pt(size-2)
    chart.category_axis.tick_labels.font.name = FONT
    chart.category_axis.tick_labels.font.size = Pt(size)
    chart.category_axis.reverse_order = True
    chart.value_axis.has_major_gridlines = True
    chart.value_axis.major_gridlines.format.line.color.rgb = color(LINE)
    chart.category_axis.format.line.fill.background()
    chart.value_axis.format.line.fill.background()
    plot = chart.plots[0]
    plot.gap_width = 70
    plot.has_data_labels = True
    plot.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
    plot.data_labels.number_format = '0.0"%"'
    plot.data_labels.font.name = FONT
    plot.data_labels.font.size = Pt(size)
    plot.data_labels.font.color.rgb = color(INK)
    for i, point in enumerate(chart.series[0].points):
        point.format.fill.solid()
        point.format.fill.fore_color.rgb = color((colors or [GRAY]*len(values))[i])
        point.format.line.fill.background()
    if title:
        text(s, x, y-.3, w, .3, title, 16, True)
    return chart


def notes(s, value):
    s.notes_slide.notes_text_frame.text = value


def prepare(template):
    p = Presentation(ROOT/template)
    for slide in p.slides:
        for sh in list(slide.shapes):
            el = sh._element
            el.getparent().remove(el)
        slide.background.fill.solid()
        slide.background.fill.fore_color.rgb = color(WHITE)
    # Remove date and inherited footer placeholders throughout the template.
    ns = {'p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
    for part in [*p.slide_masters, *p.slide_layouts]:
        for sh in list(part.shapes):
            ph = sh._element.find('.//p:ph', ns)
            if ph is not None and ph.get('type') in ('dt','ftr','sldNum'):
                sh._element.getparent().remove(sh._element)
    return p


def base(p, idx, title, stage, subtitle=None):
    s = p.slides[idx]
    text(s, .55, .28, 8.8, .23, f'SHIFT-AWARE TEST-TIME ADAPTATION  /  {stage.upper()}', 10, True, TEAL)
    text(s, .55, .78, 8.9, .8, title, 29, True)
    rect(s, .55, 1.53, 8.9, .025, LINE)
    if subtitle:
        text(s, .55, 1.65, 8.9, .5, subtitle, 18, False, GRAY)
    rect(s, .55, 7.0, 8.9, .012, LINE)
    text(s, .55, 7.12, 8.2, .19, f'{NAME}  |  {ID}', 9, False, GRAY)
    text(s, 8.73, 7.1, .7, .24, f'{idx+1:02d} / {len(p.slides):02d}', 10, False, GRAY, PP_ALIGN.RIGHT)
    return s


def cover(p, stage, focus, proposal=False):
    s = p.slides[0]
    rect(s, .55, .65, .12, 5.85, TEAL)
    text(s, .95, .74, 8.2, .32, 'SHIFT-AWARE TEST-TIME ADAPTATION', 15, True, TEAL)
    text(s, .95, 1.45, 8.2, .4, stage.upper(), 19, True, GRAY)
    if proposal:
        text(s, .95, 2.12, 8.0, 2.0, 'Shift-Aware Test-Time Adaptation\nvia Dynamic Adaptation\nPolicy Selection', 29, True)
        text(s, .95, 4.25, 7.9, .8, 'Initial proposal and the reliability question\nthat shaped the completed study', 21, False, GRAY)
    else:
        text(s, .95, 2.2, 8.0, .75, 'Valid but Blind', 44, True)
        text(s, .95, 3.18, 7.8, 1.1, 'Test-time adaptation can erode\nthe signal its risk monitor reads', 27)
        text(s, .95, 4.6, 7.8, .65, focus, 19, False, TEAL)
    text(s, .95, 5.7, 8.0, .4, NAME, 23, True)
    text(s, .95, 6.22, 8.0, .35, ID, 19, False, GRAY)
    return s


def refs_slide(p, idx, stage, keys):
    s = base(p, idx, 'References', stage)
    y = 1.78
    pitch = 4.92/len(keys)
    for i, key in enumerate(keys, 1):
        au, title, venue, url = REFS[key]
        text(s, .62, y, .38, .35, f'[{i}]', 14, True, TEAL)
        text(s, 1.06, y, 8.15, pitch-.08, f'{au} {title} {venue}.', 15 if len(keys)<=7 else 14, link=url)
        y += pitch
    notes(s, 'The cited literature covers test-time adaptation, normalization, accuracy estimation and sequential '
             'risk monitoring. Titles link to the corresponding sources. Broad confidence failure and independent '
             'monitoring are established ideas; the contribution is assessed as a bounded empirical case study. '
             'The recorded literature coverage is incomplete and does not establish novelty.')
    return s


def pipeline(s, boxes, y=2.25, height=1.55):
    n = len(boxes)
    gap = .38
    w = (8.9-gap*(n-1))/n
    for i, (label, body) in enumerate(boxes):
        x = .55+i*(w+gap)
        rect(s, x, y, w, height, LIGHT)
        text(s, x+.1, y+.12, w-.2, .32, label, 18, True, TEAL)
        text(s, x+.1, y+.52, w-.2, height-.57, body, 16)
        if i<n-1:
            arrow(s, x+w+.05, y+height/2-.1, .28, .2)


def twin_diagram(s, y=2.0):
    rect(s, .6, y+1.15, 1.5, 1.0, INK)
    text(s, .74, y+1.34, 1.23, .65, 'Unlabeled\nimages', 20, True, WHITE)
    for x1,y1,x2,y2 in [(2.1,y+1.65,2.4,y+1.65), (2.4,y+.72,2.4,y+2.6)]:
        c = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
        c.line.color.rgb=color(TEAL); c.line.width=Pt(1.5)
    arrow(s, 2.4, y+.6, .35, .23)
    arrow(s, 2.4, y+2.48, .35, .23)
    rect(s, 2.85, y, 3.1, 1.45, LIGHT)
    text(s, 3.03, y+.15, 2.75, .4, 'Tent model', 22, True, TEAL)
    text(s, 3.03, y+.68, 2.75, .6, 'Entropy updates\nProduces predictions', 19)
    rect(s, 2.85, y+1.88, 3.1, 1.45, LIGHT)
    text(s, 3.03, y+2.03, 2.75, .4, 'Entropy-free twin', 22, True, TEAL)
    text(s, 3.03, y+2.56, 2.75, .64, 'Batch statistics only\nMonitoring evidence', 18)
    arrow(s, 6.12, y+.65)
    arrow(s, 6.12, y+2.45)
    rect(s, 6.75, y+.45, 2.65, 2.6, INK)
    text(s, 6.95, y+.64, 2.25, .45, 'Risk alarm', 23, True, WHITE)
    text(s, 6.95, y+1.25, 2.25, 1.55, 'Flag when the twin\nis uncertain OR\ndisagrees with Tent.', 19, False, WHITE)


def review_one():
    p = prepare('Review1.pptx'); st = 'Review I'
    s = cover(p, st, '', proposal=True)
    notes(s, 'This deck presents the initial proposal and its refinement. The original policy-selection title is retained '
             'as a proposal, not a demonstrated contribution. Later review decks present the completed diagnostic '
             'study and the family-validated alarm. The project literature already contains whole-method routing, '
             'so a broad claim of first shift-aware policy selection is not defensible.')
    s = base(p, 1, 'Summary of the Project', st)
    cards(s, [('Deployment shift', 'Blur, noise and changing class proportions can reduce accuracy.'),
              ('Adaptation', 'Update a deployed model from unlabeled inputs instead of retraining it.'),
              ('Reliability', 'Decide whether the adaptation evidence can be trusted.')], height=2.8)
    paragraph(s, 'Initial objective', 'Choose among keeping the source model, updating normalization, and applying an entropy update.', 4.9, 21, h=.8)
    callout(s, 'Refinement: study when adaptation hides its own errors from a risk monitor.', 6.24, size=17)
    notes(s, 'Distribution shift means deployment data differ from training data. A shift alarm is not itself an error '
             'alarm, and marginal change does not identify the cause. The initial idea was to choose a whole adaptation '
             'policy from unlabeled evidence. Literature overlap motivated a narrower question about the reliability '
             'of that evidence. All statements here describe motivation and planned scope at the proposal stage.')
    s = base(p, 2, 'Review: Background Survey', st)
    table(s, ['Prior work', 'Established idea', 'Implication for this project'], [
        ['Tent [1]', 'Minimize prediction entropy at test time.', 'Confidence is also changed by adaptation.'],
        ['TTN [2]', 'Use shift-aware normalization.', 'Normalization is an existing action family.'],
        ['MORPHEUS [3]', 'Predict performance and select a TTA method.', 'Whole-method routing already exists.'],
        ['Risk monitoring [4]', 'Detect excess risk with a label-free proxy.', 'A valid bound can still miss a failure.'],
        ['AETTA [5]', 'Estimate adapted-model accuracy without target labels.', 'Confidence and correctness can diverge.'],
    ], [2.0,3.2,3.7], h=4.65, size=17)
    notes(s, 'References are numbered on the final slide. MORPHEUS is a workshop work and uses supervised auxiliary '
             'development. TTN and normalization '
             'routing overlap the initial action menu. Schirmer and AETTA already discuss proxy weakness; this project '
             'does not claim discovery of that general principle. Source reading was selective and recorded locally.')
    s = base(p, 3, 'Summary of Gap Analysis', st)
    paragraph(s, 'Broad idea already covered', 'Inferring shift properties and selecting adaptation is established prior work [2, 3].', 1.82, h=.7)
    paragraph(s, 'Evidence can be ambiguous', 'The same marginal change can reflect image corruption or a change in class proportions.', 3.12, h=.75)
    paragraph(s, 'Narrow empirical question', 'Does entropy adaptation make a released risk monitor miss more failures under persistent class skew?', 4.45, 22, h=.85)
    callout(s, 'A candidate measurement gap; the general confidence-failure mechanism is known [4, 5].', 6.24, size=16)
    notes(s, 'The exact gap must be distinguished from broad overconfidence, label-free accuracy estimation, dynamic '
             'method selection and self-masking. This question calls for adapted/frozen and entropy/normalization '
             'controls, rather than adding features to a generic selector. Absence of an exact report in a bounded '
             'literature search does not establish novelty. No completed experiment is claimed in this deck.')
    s = base(p, 4, 'Proposed Idea', st)
    text(s, .6, 1.8, 8.6, .4, 'Starting proposal: select an adaptation policy', 21, True)
    pipeline(s, [('Observe', 'Unlabeled batch'), ('Select', 'Keep / normalize / update'), ('Predict', 'Use chosen model')], 2.38, 1.1)
    text(s, .6, 3.98, 8.7, .4, 'Refined study: evaluate evidence independently', 21, True)
    pipeline(s, [('Adapt', 'Model makes predictions'), ('Cross-check', 'Separate no-entropy signal'), ('Monitor', 'Measure missed risk alarms')], 4.58, 1.12)
    callout(s, 'Do not equate higher confidence with lower deployment error.', 6.24)
    notes(s, 'This figure records research evolution rather than treating the refined method as the original proposal. '
             'The upper row is an action-selection concept. The lower row is a monitoring study: the alarm informs an '
             'operator and does not automatically reset, reject or route the deployed model. Independence here means '
             'removing the entropy gradient from the twin; the two models still share a checkpoint and inputs.')
    s = base(p, 5, 'Flow of the Proposed Work', st)
    table(s, ['Step', 'Work to perform', 'Control'], [
        ['1', 'Fix source checkpoint and clean calibration set.', 'Keep identities out of target streams.'],
        ['2', 'Create corruption and class-prior shifts.', 'Separate dev and held-out shift families.'],
        ['3', 'Run frozen source, BN-only and Tent.', 'Equivalent starting states; paired input draws.'],
        ['4', 'Log flags and alarms without target labels.', 'Labels remain with an external evaluator.'],
        ['5', 'Compare misses, false alarms and costs.', 'Freeze decision rules before held-out scoring.'],
    ], [.8,4.3,3.8], h=4.65, size=18)
    notes(s, 'BN means batch normalization. Frozen source never updates. BN-only uses test-batch statistics without '
             'a gradient step. Tent continually updates within a stream, then is reset to the source checkpoint for '
             'a new stream. Hidden labels may construct the controlled research streams and score errors; they must '
             'not be available to the router, online monitor, tuning process or stopping rule. '
             'This protocol describes the proposal-stage evaluation design.')
    s = base(p, 6, 'Scope of the Work', st)
    table(s, ['Included in the study design', 'Requirements and boundaries'], [
        ['Image corruptions and class imbalance', 'A changed input marginal does not identify a shift cause.'],
        ['Unlabeled online adaptation and monitoring', 'Labeled source/clean calibration and offline dev data are allowed and disclosed.'],
        ['Frozen, BN-only and continually adapted states', 'Reset between streams; retain the immutable source.'],
        ['Misses, false alarms and computation', 'Count twin passes, threshold recalibration and all candidate work.'],
        ['Held-out-family confirmation', 'No universal safety, clinical or novelty claim.'],
    ], [3.6,5.3], h=4.65, size=18)
    notes(s, 'The initial benchmark ambitions are not results. A small diagnostic can falsify a claim before a large '
             'evaluation. Offline development requires labeled synthetic shifts; runtime target correctness labels '
             'remain unavailable. In reporting overhead, '
             'parameter count alone is insufficient: forward passes, calibration and candidate executions all matter.')
    refs_slide(p, 7, st, ['tent','ttn','morpheus','monitor','aetta'])
    save(p, 'Review_I_Rohit_23BDS0051.pptx')


def review_two():
    p = prepare('Review2.pptx'); st = 'Review II'
    s = cover(p, st, 'Implementation, controlled comparisons and the twin alarm')
    notes(s, 'This review covers the completed monitor-diagnostic stage. The earlier dynamic-policy-selection idea '
             'is motivation; the implemented contribution being assessed is a risk-monitoring diagnostic and an '
             'entropy-free twin alarm. The third review contains the later family-validated confirmation. Earlier '
             'externally supplied gate aggregates are separate evidence and are not pooled with these experiments.')
    s = base(p, 1, 'Summary of the Project', st)
    cards(s, [('Question', 'Can adaptation make a label-free alarm less sensitive?'),
              ('Finding', 'The monitor missed 147/166 Tent failures versus 44/110 frozen-source failures.'),
              ('Remedy', 'An entropy-free twin reduced misses on paired held-out corrupted streams.')], height=3.0)
    paragraph(s, 'Completed work', 'Six-checkpoint replication, controlled mechanism tests, an authors’ code check, and a frozen twin-alarm evaluation.', 5.1, 21, h=.75)
    notes(s, 'A missed failure is a strict violating stream with no alarm at any time. The replication rates are '
             '88.6% for Tent and 40.0% for source. The two arms have different strict-violation subsets; this is not '
             'a same-denominator accuracy comparison. Paired and error-band analyses are in the project record. '
             'The twin result is a different held-out study, detailed on the performance slide.')
    s = base(p, 2, 'Review: Background Survey', st)
    table(s, ['Prior work', 'Role in this implementation', 'Relevant limit'], [
        ['Tent [1]', 'Entropy update on batch-normalization parameters.', 'Confidence need not track correctness.'],
        ['Risk monitoring [2]', 'Released uncertainty-proxy sequential alarm.', 'A lower bound does not guarantee sensitivity.'],
        ['AETTA [3]', 'Close label-free performance-estimation work.', 'Overconfidence is already documented.'],
        ['SAR [4]', 'Stable-adaptation extension/control.', 'A Tent finding need not generalize to SAR.'],
        ['ATC [5]', 'Confidence-threshold performance baseline.', 'Calibration must transfer to new shifts.'],
    ], [1.9,3.8,3.2], h=4.65, size=17)
    notes(s, 'These rows explain the implementation and closest competing interpretations. They do not imply faithful '
             'reproduction of every listed method’s published benchmark. The released monitor was run using its own '
             'evaluation pipeline with a disclosed CIFAR-100 loader patch and supplied class-skew streams. The broad '
             'confidence failure, independent monitoring and proxy replacement principles have predecessors.')
    s = base(p, 3, 'Summary of Gap Analysis', st)
    table(s, ['Question to resolve', 'Comparison implemented'], [
        ['Does Tent reduce alarm power?', 'Same checkpoints and paired draws: Tent versus frozen source.'],
        ['Is threshold recalibration responsible?', 'Tent with a fixed source threshold versus recalibrated threshold.'],
        ['Is normalization sufficient to explain it?', 'BN-only versus source; Tent versus BN-only.'],
        ['Is the result a porting artifact?', 'Released authors’ evaluation pipeline and alarm agreement.'],
        ['Can a separate signal help?', 'No-entropy twin selected on dev; evaluated on held-out families.'],
    ], [3.4,5.5], h=4.65, size=18)
    notes(s, 'The gap being measured is sequential alarm sensitivity under persistent corruption-plus-class-prior shift. '
             'The exact adapted/frozen comparison was not found in the bounded recorded literature search; some close '
             'full texts were unavailable and citation tracing was incomplete. This search outcome does not establish '
             'novelty. Multiple controls help identify the entropy step rather than confidence means alone.')
    s = base(p, 4, 'Proposed Idea: Entropy-Free Twin', st)
    twin_diagram(s, 1.88)
    callout(s, 'The working twin alarm has no formal guarantee; deployment labels are not used.', 6.24, size=16)
    notes(s, 'The twin starts from the same source checkpoint and uses batch-normalization statistics without Tent’s '
             'entropy gradient. Flag an image when the twin has low confidence or the models disagree. The flag '
             'stream enters the alarm calculation. Offline labeled calibration selects thresholds; target correctness '
             'is not an online input. Shared errors can still evade disagreement. A certified form of this earlier '
             'alarm missed every violation, so the effective form is reported as uncertified.')
    s = base(p, 5, 'Flow of the Implemented Work', st)
    table(s, ['Stage', 'Implementation'], [
        ['Prepare', 'Load checkpoint; keep an immutable source and a separate clean calibration set.'],
        ['Construct', 'Generate fixed-prior streams with paired image draws across model arms.'],
        ['Predict and update', 'Log prediction logits; update Tent; keep source fixed and twin gradient-free.'],
        ['Monitor', 'Recalibrate the published proxy; record flags, risk bounds and alarm times.'],
        ['Score externally', 'Use hidden labels only to define violations and calculate misses/false alarms.'],
        ['Confirm', 'Freeze rules on development shifts and score held-out families.'],
    ], [2.1,6.8], h=4.65, size=17)
    notes(s, 'Each stream begins from equivalent source states, and adaptation continues within that stream. Predictions '
             'follow the recorded pre-step-forward convention; threshold recalibration uses post-step weights. '
             'Each arm is scored on its own strict-violation subset. Original identities are separated from clean '
             'calibration, and repeated sampling inside a stream is disclosed.')
    s = base(p, 6, 'Dataset Used and Preprocessing', st)
    table(s, ['Item', 'Recorded setup'], [
        ['Dataset', 'CIFAR-100-C; 100 classes; 32 × 32 images; severities 3 and 5 [6].'],
        ['Checkpoints', 'Six published models: two AugMix, PRIME ResNet-18 and three Addepalli models.'],
        ['Stream construction', 'Dirichlet(0.1) class priors; 120 batches × 100 images; replacement sampling.'],
        ['Calibration and shifts', '1,000 clean images excluded from streams; noise/blur dev, weather/digital tests.'],
        ['Clear failure', 'Mean error ≥ clean error + 15 percentage points; last-quarter error < 85%.'],
    ], [2.15,6.75], h=3.95, size=17)
    text(s, .62, 5.95, 4.2, .35, 'Dataset: github.com/hendrycks/robustness', 15, False, TEAL, link='https://github.com/hendrycks/robustness')
    text(s, .62, 6.4, 7.8, .35, 'Checkpoints: robustbench.github.io', 15, False, TEAL, link='https://robustbench.github.io/')
    notes(s, 'The corruption benchmark applies label-preserving transformations; that does not prove a statistical '
             'covariate-shift assumption. Sampling lasts three epochs over 4,000 original IDs with replacement, so '
             'stream observations are not independent images. The persistent Dirichlet prior makes a few classes '
             'dominate. The collapse exclusion is an operational error cutoff, not a representation-collapse proof. '
             'Only documented runs are claimed; the proposal’s ImageNet and natural-domain ambitions remain separate.')
    s = base(p, 7, 'Detailed Work and Implementation', st)
    table(s, ['Component', 'Implemented behavior'], [
        ['Frozen source', 'Checkpoint parameters and source behavior remain unchanged.'],
        ['BN-only / twin', 'Use test-batch normalization statistics; no entropy gradient.'],
        ['Tent', 'Adam, learning rate 0.001; update batch-normalization affine parameters.'],
        ['Published monitor', 'Low-confidence flags → running lower risk bound → alarm above clean risk + 10 points.'],
        ['State and cost', 'Reset between streams; count twin inference and repeated clean-set recalibration.'],
    ], [2.2,6.7], h=4.05, size=18)
    callout(s, 'Alarm power is evaluated separately from validity of the original risk bound.', 6.24, size=17)
    notes(s, 'A bound can remain valid while lying far below actual risk. That is the central distinction behind '
             'the title. The original monitor uses a sequential confidence sequence and a clean false-positive '
             'correction. Its tuning parameter convention and calibration access follow the recorded code. '
             'The twin adds a model copy and forward pass; the original recalibration also processes clean images '
             'periodically. Complete latency and memory advantages have not been measured and are not claimed.')
    s = base(p, 8, 'Performance Evaluation', st)
    table(s, ['Study / method', 'Missed', 'Rate'], [
        ['Replication: source', '44/110', '40.0%'],
        ['Replication: Tent', '147/166', '88.6%'],
        ['Twin test: original', '94/109', '86.2%'],
        ['Twin test: twin alarm', '30/109', '27.5%'],
    ], [2.45,1.0,.95], y=2.03, h=3.35, size=16)
    barchart(s, ['Source', 'Tent', 'Original', 'Twin alarm'], [40,147/166*100,94/109*100,30/109*100],
             4.85, 2.1, 4.5, 3.3, maxval=110, colors=[GRAY,ORANGE,GRAY,TEAL], size=15)
    text(s, .6, 1.72, 8.8, .25, 'Missed clear failures ↓   |   Results from two separate frozen studies', 16, True, TEAL)
    text(s, .6, 5.7, 8.8, .38, 'Twin false alarms: 5/121 safe streams (4.1%).', 20, True)
    text(s, .6, 6.27, 8.8, .43, 'Replication arms have different violation subsets. Twin comparison uses the same corrupted streams.', 15, False, GRAY)
    notes(s, 'Replication: six checkpoints, Tent missed 147 of 166 strict streams and source 44 of 110. The difference '
             'was higher for Tent in all six models; model-bootstrap gap interval 32 to 62 percentage points. Twin '
             'study: on matching corrupted streams, original missed 94/109 and twin 30/109; the initial frozen output '
             'also included six clean violations, giving twin 30/115. The matching corrupted-stream counts are used '
             'here. False alarms are 5/121 for the twin. Replication and twin-test rates come from separate studies '
             'and do not define one paired effect.')
    s = base(p, 9, 'Results and Discussion', st)
    table(s, ['Control / extension', 'Missed failures', 'Conclusion'], [
        ['Fixed threshold', 'Tent 109/109; source 18/73', 'Gap persists.'],
        ['Entropy step', 'Tent 94/109; BN-only 37/154', 'Entropy adds misses in all six models.'],
        ['BN-only', 'BN 37/154; source 18/73', 'Gap not shown across models.'],
        ['Authors’ code', 'Tent 40/40; source 10/28', 'Pattern reproduced; 99.1% alarm agreement.'],
        ['SAR extension', 'SAR 47/159; source 18/73', 'Generalization to SAR not shown.'],
    ], [2.05,3.6,3.25], h=4.15, size=16)
    callout(s, 'Exploratory: errors captured by flags fell from 86% (source) to 57% (Tent).', 6.24, size=16)
    notes(s, 'The threshold-fixed and entropy-versus-BN tests support the entropy step as a cause in this setup. '
             'BN alone did not satisfy the across-model gap rule, which does not prove BN is harmless. Authors’ '
             'code used its evaluate function with the disclosed loader and stream additions. Exploratory error '
             'capture fell while flag precision was similar, about 70% versus 68%. SAR selected only a small '
             'fraction of samples on several models, so its negative result does not establish a successful remedy.')
    s = base(p, 10, 'Scope of the Work', st)
    paragraph(s, 'Demonstrated in this stage', 'A Tent-specific monitor blind spot, mechanism controls, and fewer misses from the twin on held-out corruptions.', 1.85, h=.95)
    paragraph(s, 'Limits', 'Shared images and checkpoints; arm-specific failure subsets; strong class skew; no universal result across adaptation methods.', 3.35, h=.95)
    paragraph(s, 'Safety and resources', 'The useful twin is uncertified. Its adaptation-caused-failure test was NOT SHOWN. Complete latency and memory remain unmeasured.', 4.88, h=.95)
    notes(s, 'The frozen test on deliberately adaptation-caused failures had too few safe streams for the false-alarm '
             'criterion; combined verdict NOT SHOWN. These findings concern benchmark classification, not clinical '
             'performance or operational safety. The diagnostic cannot identify shift causes from marginal inputs '
             'alone. Broader confidence-failure and independent-monitoring ideas are prior art, and novelty remains '
             'unestablished within the recorded literature coverage.')
    s = base(p, 11, 'Conclusion and Future Work', st)
    cards(s, [('Measure', 'Count missed failures as well as false alarms.'),
              ('Explain', 'Separate entropy updates from normalization and recalibration.'),
              ('Improve', 'Use a separate signal, then test its alarm level on unseen shifts.')], height=2.9)
    paragraph(s, 'Next stage', 'Calibrate on shifted development streams; validate across shift families; confirm once on new datasets and checkpoints.', 5.0, 21, h=.9)
    notes(s, 'The study shows that statistical validity and practical detection power are distinct. The twin helps '
             'under the studied conditions but provides no general guarantee. Later experiments reveal that strong '
             'ranking need not yield a reliable deployed alarm level. Review III reports this continuation, including '
             'failed confirmations and the PARTIAL fresh test of the family-validated alarm. Future natural-shift '
             'and non-BN tests remain proposals, not completed evidence.')
    refs_slide(p, 12, st, ['tent','monitor','aetta','sar','atc','cifar'])
    save(p, 'Review_II_Rohit_23BDS0051.pptx')


def review_three():
    p = prepare('Review3.pptx'); st = 'Review III'
    s = cover(p, st, 'Completed study and a fresh test of the family-validated alarm')
    notes(s, 'This final review covers the completed study recorded in the manuscript and experiment protocols, '
             'including the fresh family-validated test. The verdict is PARTIAL under the rule frozen before the run. '
             'The original title concerned dynamic adaptation-policy selection; the work evolved into assessing '
             'the reliability of adaptation evidence. This deck does not claim a universal repair or established novelty.')
    s = base(p, 1, 'Summary of the Project', st)
    cards(s, [('Observe', 'Tent can become harder for its confidence-based risk monitor to detect.'),
              ('Diagnose', 'Entropy-free evidence helps, but dev-calibrated alarm levels transfer unevenly.'),
              ('Validate', 'A family-validated alarm was tested on 4,630 new streams.')], height=2.95)
    text(s, .65, 5.0, 8.7, .65, 'Fresh test: 22/272 failures missed (8.1%).', 26, True, TEAL)
    text(s, .65, 5.85, 8.7, .7, 'Verdict: PARTIAL — false alarms 30/399 (7.52%),\nabove the frozen 7.5% band around a 5% target.', 21, True, ORANGE)
    notes(s, 'The full fresh run includes development and held-out streams, three objectives and fourteen settings. '
             'The primary held-out Tent pool is 272 strict and 399 safe streams, not all 4,630 streams. The published '
             'monitor missed 171/272; the earlier constant-level twin missed 40/272. False alarms were higher than '
             'the published monitor’s 4/399 and close to the twin’s 31/399. Fewer misses therefore do not imply a '
             'better operating point in every respect. A matched-false-alarm comparison is reported separately.')
    s = base(p, 2, 'Review: Background Survey', st)
    table(s, ['Prior work', 'What it supplies', 'What this study measures'], [
        ['Tent [1]', 'Online entropy adaptation.', 'How its objective affects alarm evidence.'],
        ['Risk monitoring [2]', 'Label-free sequential risk bounds; proxy failures.', 'Missed violations versus frozen and BN-only arms.'],
        ['AETTA [3]', 'Label-free adapted-model accuracy estimation.', 'Sequential alarms rather than accuracy alone.'],
        ['ATC / DoC [4, 5]', 'Confidence-based performance signals.', 'Dev-calibrated and time-resolved levels.'],
        ['Self-monitoring [6]', 'Self-masking with revealed forecasting outcomes.', 'A label-free image-classification worked case.'],
    ], [2.0,3.35,3.55], h=4.55, size=17)
    notes(s, 'The general ideas of overconfidence, proxy failure, independent monitoring and self-masking are prior '
             'art. Some close papers were only partially read or inaccessible. The recorded search did not saturate; '
             'the work is framed as a bounded controlled case study. Runtime target labels are absent, but clean '
             'calibration and labeled synthetic development streams are explicit requirements.')
    s = base(p, 3, 'Summary of Gap Analysis', st)
    table(s, ['Observed problem', 'Evidence', 'Response'], [
        ['Adaptation weakens its own proxy.', 'Tent misses more than BN-only in controlled tests.', 'Keep an entropy-free twin signal.'],
        ['Ranking does not fix alarm levels.', 'Earlier frozen confirmations were NOT CONFIRMED.', 'Validate transfer across dev shift families.'],
        ['No signal works everywhere.', 'An earlier twin+pattern alarm missed 112/351 (31.9%) in a frozen test.', 'Select among three candidates per deployment.'],
    ], [2.85,3.4,2.65], h=3.8, size=18)
    callout(s, 'New question: can a dev-selected signal and level work on entirely unused datasets?', 6.24, size=16)
    notes(s, 'The shifted-level confirmation on PathMNIST, OrganAMNIST and CIFAR missed 13% but failed its frozen '
             'absolute-improvement criteria. The next confirmation, on CIFAR-100-C, OCT, OrganC and Pneumonia, '
             'missed 112/351 at 16/637 false alarms and failed its 20% miss ceiling. Exploratory diagnosis on '
             'already-seen streams shaped the family-validated rule; those diagnosis results are not confirmation '
             'evidence. The final fresh study uses new datasets and a frozen analysis.')
    s = base(p, 4, 'Proposed Idea: Family-Validated Alarm', st)
    cards(s, [('Twin', 'Uncertainty or disagreement, without an entropy update.'),
              ('Time-resolved DoC', 'Confidence change standardized at each read-out time.'),
              ('Fusion', 'Twin, confidence threshold and dropout evidence.')], y=1.9, height=2.2)
    arrow(s, 4.78, 4.14, .42, .25)
    rect(s, .65, 4.62, 8.7, 1.03, INK)
    text(s, .9, 4.77, 8.2, .7, 'Leave one dev shift family out → choose signal\n→ set level on safe dev streams → freeze for deployment', 21, True, WHITE, PP_ALIGN.CENTER)
    callout(s, 'Offline dev labels are required. Online target labels are not used.', 6.24, size=18)
    notes(s, 'Selection is per dataset/checkpoint/objective, before deployment; this is not runtime switching among '
             'adaptation policies. Twin uses a constant level. DoC is time-standardized from safe dev streams. Fusion '
             'is the previous twin/ATC/dropout combination. For each held-out dev family, calibrate on other families '
             'and calculate missed-share plus false-alarm-share. Pick the lowest score with fixed tie-breaking, '
             'then refit its level on all safe dev streams. No theoretical coverage guarantee is claimed.')
    s = base(p, 5, 'Flow of the Final Work', st)
    table(s, ['Stage', 'Information and state contract'], [
        ['1. Prepare', 'Immutable source checkpoint and labeled clean calibration; model copies start identically.'],
        ['2. Develop', 'Labeled synthetic shift streams; separate image IDs and shift families.'],
        ['3. Select', 'Leave-one-family-out candidate comparison; calibrate final level on safe dev streams.'],
        ['4. Freeze', 'Lock data splits, stream code, criteria and analysis before the fresh run.'],
        ['5. Deploy and score', 'Online adaptation/alarms see no target labels; an external evaluator scores outcomes.'],
    ], [2.15,6.75], h=4.45, size=18)
    notes(s, 'Reset state at the beginning of each stream; Tent adapts continuously within it. The source is frozen, '
             'the twin has no entropy gradient, and calibrated detection choices are fixed for each deployment '
             'setting. Development families and held-out families are separate. Held-out labels cannot affect '
             'routing, candidate choice, thresholds or stopping. Matched-false-alarm results use hindsight labels '
             'only for descriptive comparison, not for deployed thresholds.')
    s = base(p, 6, 'Dataset Used: Fresh Confirmation', st)
    table(s, ['Dataset', 'Content / model', 'Held-out pool'], [
        ['CIFAR-10-C [7]', '10 classes; four published checkpoints; 15 corruptions.', '151 strict; 361 safe'],
        ['OrganSMNIST [8]', '11-class CT; fine-tuned ResNet-18; 224-pixel inputs.', '66 strict; 7 safe'],
        ['TissueMNIST [8]', '8-class microscopy; fine-tuned ResNet-18; 224-pixel inputs.', '55 strict; 31 safe'],
    ], [2.0,4.8,2.1], h=2.55, size=17)
    text(s, .62, 4.6, 8.7, .7, '120 batches × 48 images per stream; natural, Dirichlet(1)\nand Dirichlet(0.1) held-out class proportions.', 20)
    text(s, .62, 5.55, 8.7, .7, '4,630 streams overall, across 14 settings and three objectives.\nPrimary Tent analysis: 272 clear failures and 399 safe streams.', 20, True)
    text(s, .62, 6.5, 3.2, .25, 'Data: medmnist.com', 14, False, TEAL, link='https://medmnist.com/')
    text(s, 4.0, 6.5, 5.3, .25, 'Corruptions: github.com/hendrycks/robustness', 14, False, TEAL, link='https://github.com/hendrycks/robustness')
    notes(s, 'CIFAR-10 uses 1,000 clean calibration, 4,000 development and 5,000 held original identities. Medical '
             'calibration uses 1,000 training images; dev and held use validation and test splits capped at 4,000 '
             'images each. Held medical shifts are blur, JPEG, contrast and pixelation at three severities. Dev '
             'includes extra synthetic shift families and an additional Dirichlet prior of 0.3. Labels construct '
             'streams and score results, but are hidden online. OrganSMNIST has only seven safe primary streams, '
             'so its false-alarm estimate is too small for a reliable dataset-specific conclusion.')
    s = base(p, 7, 'Detailed Work: Selection and Calibration', st)
    table(s, ['Rule', 'Frozen implementation'], [
        ['Selection target', 'Minimize leave-one-family-out missed share + false-alarm share.'],
        ['Alarm level', 'Nominal 5% level from safe dev-stream maximum scores; read every five batches after batch 10.'],
        ['Time standardization', 'For DoC, use dev-safe median and 10–90% spread at each read-out time.'],
        ['Low dev support', 'Fewer than 19 safe dev streams → no alarm; retain resulting misses in evaluation.'],
        ['Guarantee and costs', 'No formal coverage claim; account for dev candidate runs, twin inference and fusion/dropout passes.'],
    ], [2.3,6.6], h=4.55, size=18)
    notes(s, 'The same development streams inform standardization, candidate selection and final calibration, which '
             'prevents a general coverage guarantee. Realized false alarms are evaluated explicitly. No final setting '
             'abstained or was flagged weak in the audit. All 4,630 planned streams completed; the frozen analysis '
             'code was unchanged. Actual compute used six RTX 4090 GPUs across three terminated RunPod pods, with '
             'recorded cost $9.76. This experiment cost is not a deployment-latency measurement. Full inference '
             'overhead and memory trade-offs remain open.')
    s = base(p, 8, 'Performance Evaluation: Fresh Test', st)
    table(s, ['Detector', 'Missed / 272 failures', 'False alarms / 399 safe'], [
        ['Published monitor', '171 (62.9%)', '4 (1.0%)'],
        ['Released proxy, dev level', '60 (22.1%)', '13 (3.3%)'],
        ['Twin, constant level', '40 (14.7%)', '31 (7.8%)'],
        ['Family-validated alarm', '22 (8.1%)', '30 (7.52%)'],
    ], [3.55,2.6,2.75], y=1.83, h=2.38, size=16)
    barchart(s, ['Published','Twin','FV'], [171/272*100,40/272*100,22/272*100],
             .72, 4.68, 4.25, 1.95, maxval=80, colors=[GRAY,GRAY,TEAL], size=12, title='Missed clear failures (%) ↓')
    barchart(s, ['Published','Twin','FV'], [4/399*100,31/399*100,30/399*100],
             5.25, 4.68, 4.0, 1.95, maxval=12, colors=[GRAY,GRAY,TEAL], size=12, title='False alarms on safe streams (%) ↓')
    notes(s, 'Primary held-out Tent results pooled over the three new datasets. A strict failure has mean error '
             'at least clean error plus 15 points and last-quarter error below 85%; a safe stream has mean error '
             'below clean error plus 10 points and the same collapse filter. Intermediate streams do not enter '
             'either denominator. The final alarm reduces misses but has more false alarms than the published '
             'monitor. The dev-level proxy comparison helps distinguish the score from its original calibration. '
             'Matched thresholds are a separate hindsight analysis, not a deployed performance guarantee.')
    s = base(p, 9, 'Results and Discussion: PARTIAL', st)
    table(s, ['Frozen criterion', 'Fresh result', 'Met?'], [
        ['C1: ranking at matched false alarms', '5/206 missed vs 31/206; both at 5.6% achieved false alarms.', 'Yes'],
        ['C2: deployed safety', '30/399 false alarms; within the 10% pooled ceiling.', 'Yes'],
        ['C3: deployed power', '22/272 missed (8.1%); 87% fewer than the published monitor.', 'Yes'],
        ['C4: level transfer', '7.52% false alarms exceeds the frozen 7.5% band.', 'No'],
    ], [3.15,4.65,1.1], y=1.85, h=3.6, size=17)
    text(s, .63, 5.75, 8.75, .75, 'Coupling test versus BN-only: SHOWN for Tent and hard pseudo-labels; NOT SHOWN for information maximization.', 20, True, TEAL)
    notes(s, 'C1 excludes OrganSMNIST by the frozen minimum safe-stream support. C2 also requires no more than '
             '15% false alarms per dataset with at least 20 safe streams. C3 includes a 20% miss ceiling and '
             'per-dataset non-inferiority to the published monitor. C4’s miss-reduction and per-dataset conditions '
             'held, but the exact false-alarm rate 30/399 = 7.5188% exceeded 7.5%; 29 alarms would have passed. '
             'Preserve the PARTIAL verdict despite rounding. Against the BN-only twin, the monitor missed '
             '171/272 versus 133/358 for Tent, 132/215 versus 108/246 for pseudo-labels, and 131/303 versus '
             '108/246 for information maximization. These arms have their own strict sets, and the final contrast '
             'does not establish a universal mechanism for every confidence-rewarding objective.')
    s = base(p, 10, 'Scope of the Completed Work', st)
    paragraph(s, 'Supported findings', 'A controlled Tent case study; a pseudo-label extension; a family-validated alarm that meets ranking, safety and power criteria.', 1.85, h=.95)
    paragraph(s, 'Remaining empirical limits', 'TissueMNIST: 11/55 failures still missed. OrganSMNIST: only 7 safe streams. Natural shifts and non-BN models remain open.', 3.4, h=.95)
    paragraph(s, 'Deployment requirements', 'Labeled clean and synthetic dev data; extra model/candidate computation; no runtime target labels and no formal alarm guarantee.', 4.95, h=.95)
    notes(s, 'Most gain over the earlier constant-level twin came from OrganSMNIST, where the selected fusion '
             'missed 10 instead of 28. The twin was selected for TissueMNIST and three CIFAR checkpoints; '
             'DoC for AugMix WRN-40-2, and fusion for OrganSMNIST. Overall calibration still overshoots a nominal 5% false-alarm '
             'target, especially on CIFAR-10-C (29/361, about 8%). Medical datasets here are controlled benchmark '
             'stress tests, not clinical validation. Literature coverage remains bounded and does not prove novelty.')
    s = base(p, 11, 'Conclusion and Future Work', st)
    cards(s, [('Finding', 'Adaptation can weaken the evidence its monitor reads.'),
              ('Practical lesson', 'Evaluate detection power and alarm-level transfer separately.'),
              ('Final verdict', 'Fewer misses on fresh data; full level transfer remains unconfirmed.')], height=2.85)
    paragraph(s, 'Planned extensions', 'Natural shifts, non-BN architectures, disjoint calibration/selection splits, and complete inference-time and memory measurement.', 4.96, 21, h=.9)
    callout(s, 'Completed benchmark study with explicit negative and partial results.', 6.24, size=18)
    notes(s, 'The completed result is a bounded diagnostic and empirical alarm study. The original sequential '
             'monitor’s guarantee is not contradicted by poor sensitivity. Independent evidence helps, but '
             'does not make shared errors identifiable under arbitrary label shift. The frozen verdict is PARTIAL. '
             'Natural shifts, non-BN architectures, disjoint development splits and complete deployment-overhead '
             'evaluation remain future work.')
    refs_slide(p, 12, st, ['tent','monitor','aetta','atc','doc','han','cifar','med'])
    s = base(p, 13, 'Word Summary of the Work', st)
    text(s, .65, 1.87, 8.6, .5, 'Editable companion report included', 25, True, TEAL)
    table(s, ['Report structure', 'Report structure (continued)'], [
        ['Title and Abstract', 'Proposed Work'],
        ['Keywords', 'Performance Evaluation'],
        ['Introduction', 'Results and Discussion'],
        ['Literature Review', 'References'],
    ], [4.45,4.45], y=2.7, h=2.4, size=20)
    text(s, .65, 5.47, 8.6, .8, 'Review_III_Report_Rohit_23BDS0051.docx', 20, True,
         link='Review_III_Report_Rohit_23BDS0051.docx')
    text(s, .65, 6.18, 8.6, .4, 'Uses the final counts and retains the PARTIAL verdict.', 19)
    notes(s, 'The companion report covers the abstract, keywords, introduction, literature review, proposed '
             'work, performance evaluation, results and references. The file is '
             'included beside the presentation and in the delivery bundle, with a PDF copy. It reports the same '
             'primary counts, denominator definitions, limitations and PARTIAL verdict as the presentation.')
    s = base(p, 14, 'A3 Poster of the Work', st)
    poster_png = HERE/'assets'/'poster.png'
    if poster_png.exists():
        s.shapes.add_picture(str(poster_png), Inches(.72), Inches(1.76), height=Inches(4.95))
    else:
        rect(s, .72, 1.9, 3.4, 4.65, LIGHT)
        text(s, .9, 2.12, 3.0, 2, 'Valid but Blind\n\nA3 research poster', 27, True, TEAL)
    text(s, 4.75, 2.0, 4.2, .9, 'Print-ready A3 portrait poster', 26, True, TEAL)
    text(s, 4.75, 3.2, 4.3, 1.4, 'Includes motivation, method, primary results, frozen verdict, limitations and references.', 22)
    text(s, 4.75, 5.05, 4.1, .9, 'Editable PPTX and PDF\nIncluded in the review bundle', 20)
    notes(s, 'The poster is a separate A3 portrait PowerPoint and PDF, measuring 297 by 420 millimetres. This slide '
             'contains a preview. Print the PDF at actual size rather than fitting the slide preview to a page. '
             'The editable poster retains the same scientific qualifications as the final deck.')
    s = base(p, 15, 'Source Code Link', st)
    text(s, .65, 1.95, 8.7, .4, 'Project repository', 17, True, TEAL)
    text(s, .65, 2.55, 8.7, 1.25, 'github.com/RohitPhaniramSakamuri/\nvalid-but-blind', 27, True, link=REPO)
    table(s, ['Project component', 'Location in the repository'], [
        ['Live demonstration', 'demo/'],
        ['Scientific manuscript', 'paper/'],
        ['Protocols and recorded verdicts', 'experiments/'],
        ['Runners, saved analyses and reports', 'diagnostics/'],
    ], [3.7,5.2], y=4.18, h=2.35, size=18)
    notes(s, 'The project repository contains the demonstration, manuscript, experiment records and diagnostic '
             'code. Experiment records and saved analysis reports provide the evidence for the presented counts '
             'and frozen verdicts. Review presentations and companion documents are in reports/reviews.')
    save(p, 'Review_III_Rohit_23BDS0051.pptx')


def save(p, name):
    p.core_properties.author = NAME
    p.core_properties.last_modified_by = NAME
    p.core_properties.title = name.replace('_',' ').removesuffix('.pptx')
    p.core_properties.subject = 'Shift-aware test-time adaptation: review presentation'
    p.core_properties.comments = ''
    p.save(HERE/name)
    scrub_office(HERE/name)


def scrub_office(path):
    # Also clean note masters and chart workbooks, whose defaults carry dates.
    def clean(raw):
        with ZipFile(BytesIO(raw)) as z:
            entries = [(i,z.read(i.filename)) for i in z.infolist()]
        dest=BytesIO()
        with ZipFile(dest,'w',ZIP_DEFLATED) as out:
            for info,data in entries:
                filename=info.filename
                if filename=='docProps/core.xml':
                    node=LX.fromstring(data)
                    for child in list(node):
                        if child.tag.rsplit('}',1)[-1] in ('created','modified','lastPrinted'):
                            node.remove(child)
                    data=LX.tostring(node,encoding='utf-8',xml_declaration=True,standalone=True)
                elif filename.endswith('.xml') and b'type="dt"' in data:
                    node=LX.fromstring(data)
                    for ph in node.xpath('//*[local-name()="ph" and @type="dt"]'):
                        parent=ph
                        while parent is not None and parent.tag.rsplit('}',1)[-1]!='sp':
                            parent=parent.getparent()
                        if parent is not None:
                            parent.getparent().remove(parent)
                    data=LX.tostring(node,encoding='utf-8',xml_declaration=True,standalone=True)
                elif filename.endswith('.xlsx'):
                    data=clean(data)
                out.writestr(info,data)
        return dest.getvalue()
    path.write_bytes(clean(path.read_bytes()))


def make_poster():
    p = Presentation()
    p.slide_width = Inches(297/25.4)
    p.slide_height = Inches(420/25.4)
    s = p.slides.add_slide(p.slide_layouts[6])
    rect(s, 0, 0, 11.6929, 2.72, INK)
    text(s, .48, .32, 10.75, .35, 'SHIFT-AWARE TEST-TIME ADAPTATION  /  RESEARCH POSTER', 15, True, 'A8DDDA')
    text(s, .48, .92, 10.75, .85, 'Valid but Blind', 48, True, WHITE)
    text(s, .48, 1.85, 10.75, .65, 'Test-time adaptation can erode the signal its risk monitor reads', 23, False, WHITE)
    text(s, .48, 2.97, 10.75, .43, f'{NAME}  |  {ID}', 24, True)
    # Upper two columns.
    text(s, .5, 3.7, 5.12, .42, 'WHY THIS MATTERS', 23, True, TEAL)
    text(s, .5, 4.34, 5.1, 1.8, 'Tent lowers entropy while its monitor reads confidence [1, 2].\nConfidence can rise without fewer errors.\nA valid risk bound can still miss a failure.', 20)
    text(s, 6.0, 3.7, 5.15, .42, 'THE CONTROLLED FINDING', 23, True, TEAL)
    text(s, 6.0, 4.34, 5.15, 1.8, 'CIFAR-100-C; six checkpoints; strong skew.\nTent: 147/166 failures missed (89%).\nFrozen source: 44/110 (40%).\nEntropy adds misses beyond BN-only.', 20)
    rect(s, .5, 6.27, 10.65, 2.1, LIGHT)
    text(s, .72, 6.48, 10.1, .44, 'FAMILY-VALIDATED ALARM', 25, True, TEAL)
    text(s, .72, 7.18, 10.1, .95, 'Twin evidence  /  time-resolved confidence  /  fusion\n→ choose by leave-one-dev-family-out validation → freeze for deployment', 23, True)
    text(s, .5, 8.77, 10.65, .43, 'FRESH CONFIRMATION', 25, True, TEAL)
    text(s, .5, 9.39, 10.65, .82, '4,630 streams overall: CIFAR-10-C, TissueMNIST and OrganSMNIST [3, 4].\nPrimary held-out Tent pool: 272 clear failures and 399 safe streams.', 22)
    table(s, ['Detector', 'Failures missed', 'False alarms'], [
        ['Published monitor', '171/272 (62.9%)', '4/399 (1.0%)'],
        ['Twin, constant level', '40/272 (14.7%)', '31/399 (7.8%)'],
        ['Family-validated alarm', '22/272 (8.1%)', '30/399 (7.52%)'],
    ], [4.5,3.15,3.0], x=.5, y=10.55, h=2.0, size=21)
    rect(s, .5, 12.87, 10.65, 1.12, LIGHT)
    text(s, .72, 13.03, 10.1, .8, 'FROZEN VERDICT: PARTIAL\n7.52% false alarms > 7.5% band; ranking, safety and power passed.', 21, True, ORANGE)
    text(s, .5, 14.27, 10.65, .75, 'Limits: offline labeled dev/calibration required; no runtime target labels; no formal alarm guarantee. Natural shifts, non-BN models and complete overhead remain open.', 19)
    text(s, .5, 15.25, 10.65, .8, '[1] Wang et al., Tent. ICLR.  [2] Schirmer et al., Monitoring Risks in Test-Time Adaptation. NeurIPS.\n[3] Hendrycks & Dietterich, Common Corruptions. ICLR.  [4] Yang et al., MedMNIST v2. Scientific Data.\nSource code: github.com/RohitPhaniramSakamuri/valid-but-blind', 13, False, GRAY)
    notes(s, 'A3 portrait poster. The adapted/frozen replication uses arm-specific strict subsets. The fresh '
             'confirmation uses the same Tent primary pool across detectors. Strict means mean error at least '
             'clean error plus 15 points and last-quarter error below 85%; safe means error below clean error '
             'plus 10 points and the same collapse filter. The false-alarm target was 5%; the frozen transfer '
             'band was 7.5%. Broader confidence failure and independent monitoring are established ideas.')
    save(p, 'Review_III_A3_Poster_Rohit_23BDS0051.pptx')


REPORT_SECTIONS = [
 ('Abstract', 'Test-time adaptation updates a deployed model using unlabeled inputs. When adaptation and a risk '
  'monitor read the same predictions, the update can weaken the evidence the monitor needs. In a controlled '
  'CIFAR-100-C replication, a released label-free monitor missed 147 of 166 clear failures under Tent, versus '
  '44 of 110 for frozen checkpoints. Entropy-versus-normalization controls support the entropy step as a cause '
  'in this setup. An entropy-free twin reduced misses, but later confirmations showed uneven transfer of '
  'development-calibrated alarm levels. A family-validated alarm selects among three signals using '
  'leave-one-shift-family-out validation. Its frozen test on unused data contained 4,630 streams overall. '
  'On the primary held-out Tent pool it missed 22/272 failures at 30/399 false alarms, compared with 171/272 '
  'misses for the published monitor. The verdict was PARTIAL: ranking, safety and power criteria held, but '
  'the false-alarm rate of 7.52% exceeded the frozen 7.5% transfer band. These are benchmark findings; no '
  'universal guarantee or established novelty is claimed.'),
 ('Keywords', 'Test-time adaptation; risk monitoring; label shift; entropy minimization; sequential alarms; calibration.'),
 ('Introduction', 'Distribution shift can reduce a classifier’s accuracy after deployment. Tent [1] adapts '
  'normalization parameters by minimizing prediction entropy without using target labels. A label-free '
  'monitor [2] can estimate a lower bound on risk from uncertainty flags and raise an alarm when that bound '
  'crosses a tolerated level. The concern is that adaptation changes the confidence signal itself. Lower '
  'entropy need not mean fewer errors, and a quiet monitor does not certify safety. The project began with '
  'dynamic adaptation-policy selection and narrowed to this measurable reliability question. Marginal input '
  'change alone cannot establish whether a shift is caused by corruption or changed class proportions.'),
 ('Literature Review', 'Tent [1] supplies the entropy-adaptation baseline. Schirmer et al. [2] supply the released '
  'sequential monitor and already report failures of uncertainty proxies in other settings. AETTA [3] '
  'documents the separation of confidence and accuracy during adaptation. ATC [4] and DoC [5] supply '
  'confidence-based performance signals. Han et al. [6] study self-masking with revealed forecasting '
  'outcomes. Thus confidence failure, independent monitoring and self-masking are established ideas. '
  'The project’s recorded literature search found no exact match for its adapted/frozen sequential-miss '
  'comparison, but coverage was incomplete and some full texts were unavailable. This does not prove novelty.'),
 ('Proposed Work', 'The implemented family-validated alarm has three candidates: an entropy-free twin signal, '
  'a time-resolved difference-of-confidence signal, and a fusion of twin, confidence-threshold and dropout '
  'evidence. The twin shares the source checkpoint and uses test-batch normalization statistics without an '
  'entropy gradient. It flags low twin confidence or disagreement with the adapted model. For each deployment '
  'setting, leave-one-development-family-out evaluation selects the candidate with the smallest missed share '
  'plus false-alarm share. Its final level is fitted to safe development-stream maximum scores at a nominal '
  '5% rate. DoC uses the safe-development median and 10–90% spread separately at each read-out time. '
  'Read-outs occur every five batches starting at batch 11. Settings with fewer than 19 safe development '
  'streams do not alarm and remain in evaluation. Selection and calibration use labeled synthetic '
  'development data; online target correctness labels are unavailable. Because development data are reused '
  'for signal choice and calibration, no general coverage guarantee is asserted.\n\n'
  'The source remains immutable. The adaptive model updates continuously within each stream, and all '
  'model states reset between streams. Counterfactual arms start from equivalent checkpoints and use '
  'paired draws. Clean calibration identities, development identities and held-out identities are separated. '
  'Held-out labels are used only by an external evaluator, not for choosing the signal, level or stopping rule.'),
 ('Performance Evaluation', 'The original diagnostic used CIFAR-100-C [7], six published checkpoints and '
  'persistent Dirichlet(0.1) class priors. A clear failure is a stream with mean error at least 15 percentage '
  'points above clean error and last-quarter error below 85%. A missed failure never produces an alarm. '
  'A safe stream has mean error below clean error plus 10 points and the same last-quarter filter. '
  'Intermediate streams enter neither primary denominator. The last-quarter filter is an operational '
  'collapse exclusion, not proof against all forms of collapse.\n\n'
  'The fresh confirmation used CIFAR-10-C, TissueMNIST and OrganSMNIST [7, 8]. CIFAR-10-C used four published '
  'checkpoints; the two medical datasets used fine-tuned ResNet-18 models. Streams contained 120 batches '
  'of 48 images, with natural or Dirichlet-skewed priors. Development and held-out corruption families were '
  'separate. The complete run contained 4,630 streams across fourteen settings and three objectives; the '
  'primary held-out Tent comparison contains 272 strict and 399 safe streams. Miss rate and false-alarm '
  'rate use these distinct denominators. Matched-false-alarm evaluation sets thresholds with hindsight '
  'and measures ranking only; it is not a deployed calibration result.'),
 ('Results and Discussion', 'In the original replication, Tent was missed more than source in all six models '
  '(147/166 versus 44/110). In the factorial study, the gap persisted with a fixed threshold (109/109 '
  'versus source 18/73). Tent also missed more than BN-only (94/109 versus 37/154); normalization alone '
  'did not meet the across-model gap rule. The monitor authors’ pipeline reproduced the pattern '
  '(40/40 versus 10/28) with a disclosed loader patch and supplied streams. On matching corrupted '
  'streams, the early twin reduced misses from 94/109 to 30/109 with 5/121 false alarms. Its useful '
  'form was uncertified. The gap was not shown for SAR, and the adaptation-caused-failure test was NOT SHOWN.\n\n'
  'Later alarm-level confirmations were NOT CONFIRMED, including a study with 112/351 misses '
  '(31.9%) despite 16/637 false alarms. Exploratory diagnosis on already-seen streams motivated '
  'family validation; those streams are development evidence, not fresh confirmation.\n\n'
  'In the final fresh test, the family-validated alarm missed 22/272 (8.1%), versus the published '
  'monitor’s 171/272 (62.9%) and the constant-level twin’s 40/272 (14.7%). False alarms were 30/399 '
  '(7.52%), compared with 4/399 and 31/399. At matched 5.6% achieved false alarms on eligible settings, '
  'it missed 5/206 versus 31/206 for the released proxy. OrganSMNIST was excluded from this matched '
  'comparison by the frozen safe-support rule. C1 ranking, C2 deployed safety and C3 deployed power '
  'passed. C4 failed its false-alarm band: 30/399 exceeds 7.5%, while 29 alarms would have passed. '
  'The frozen verdict is PARTIAL.\n\n'
  'The coupling contrast against the BN-only twin was SHOWN for Tent and hard pseudo-labels, and '
  'NOT SHOWN for information maximization. TissueMNIST still had 11/55 missed failures, and '
  'OrganSMNIST had only seven safe primary streams. These are controlled benchmark stress tests '
  'rather than clinical validation. Full deployment latency and memory remain unmeasured; costs '
  'must include the twin, offline candidate execution, calibration and any dropout/fusion passes. '
  'Natural shifts, non-BN architectures and disjoint selection/calibration development splits '
  'are future work. The original monitor’s mathematical guarantee is not contradicted by poor power.'),
]


def make_report():
    d = Document()
    sec = d.sections[0]
    sec.page_width = DInches(8.2677); sec.page_height = DInches(11.6929)
    sec.top_margin = sec.bottom_margin = DInches(.7)
    sec.left_margin = sec.right_margin = DInches(.78)
    normal = d.styles['Normal']
    normal.font.name = FONT; normal.font.size = DPt(11)
    normal.paragraph_format.space_after = DPt(7)
    normal.paragraph_format.line_spacing = 1.1
    for name in ['Title','Heading 1','Heading 2']:
        d.styles[name].font.name = FONT
        d.styles[name].font.color.rgb = DColor.from_string(INK)
    d.add_heading('Valid but Blind', 0)
    d.add_paragraph('Test-Time Adaptation Can Erode the Signal Its Risk Monitor Reads', style='Subtitle')
    d.add_paragraph(f'{NAME}  |  {ID}')
    d.add_paragraph('Review III — Companion Report')
    for heading, body in REPORT_SECTIONS:
        d.add_heading(heading, 1)
        for para in body.split('\n\n'):
            d.add_paragraph(para)
        if heading=='Performance Evaluation':
            t=d.add_table(rows=1, cols=3); t.style='Light Shading Accent 1'
            for c,v in zip(t.rows[0].cells,['Detector','Missed failures','False alarms']): c.text=v
            for row in [['Published monitor','171/272 (62.9%)','4/399 (1.0%)'],
                        ['Released proxy, dev level','60/272 (22.1%)','13/399 (3.3%)'],
                        ['Twin, constant level','40/272 (14.7%)','31/399 (7.8%)'],
                        ['Family-validated alarm','22/272 (8.1%)','30/399 (7.52%)']]:
                for c,v in zip(t.add_row().cells,row): c.text=v
            for row in t.rows:
                trPr=row._tr.get_or_add_trPr(); trPr.append(OxmlElement('w:cantSplit'))
    d.add_heading('References', 1)
    for i,k in enumerate(['tent','monitor','aetta','atc','doc','han','cifar','med'],1):
        au,ti,venue,url=REFS[k]
        # Display title/venue without calendar fields; full source metadata stays in the project library.
        d.add_paragraph(f'[{i}] {au} {ti} {venue}.')
    d.add_paragraph('Source code: '+REPO)
    foot=sec.footer.paragraphs[0]
    foot.text=f'{NAME}  |  {ID}  |  '
    fld=OxmlElement('w:fldSimple'); fld.set(qn('w:instr'),'PAGE'); foot._p.append(fld)
    for r in foot.runs: r.font.size=DPt(9)
    d.core_properties.author=NAME
    d.core_properties.last_modified_by=NAME
    d.core_properties.title='Valid but Blind — Review III Companion Report'
    path=HERE/'Review_III_Report_Rohit_23BDS0051.docx'
    d.save(path); scrub_office(path)


def main():
    HERE.mkdir(exist_ok=True)
    make_poster()
    review_one()
    review_two()
    review_three()
    make_report()
    manifest = {
      'student':NAME, 'registration':ID,
      'templates':['Review1.pptx','Review2.pptx','Review3.pptx'],
      'slide_counts':{'Review I':8,'Review II':13,'Review III':16},
      'scientific_sources':['paper/main.tex','experiments/004-monitor-blind-spots.md',
                            'experiments/006-twin-confirmation.md','experiments/007-alarm-diagnosis.md',
                            'experiments/008-shifted-level-confirmation.md','experiments/009-level-transfer-diagnosis.md',
                            'experiments/010-family-validated-alarm-confirmation.md','sources/catalog.json'],
      'scope':'Document generation from existing records only. No experiments, implementation tests or new literature search.',
      'final_verdict':'PARTIAL',
      'final_primary_counts':{'strict':272,'safe':399,'fv_missed':22,'fv_false_alarms':30,
                              'published_missed':171,'published_false_alarms':4,
                              'constant_twin_missed':40,'constant_twin_false_alarms':31},
      'original_templates_preserved':True,
      'output_sha256':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in HERE.glob('*') if f.suffix in ('.pptx','.docx')},
    }
    (HERE/'build_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('Created three review decks, an editable A3 poster, and the Word companion report.')


if __name__=='__main__':
    main()

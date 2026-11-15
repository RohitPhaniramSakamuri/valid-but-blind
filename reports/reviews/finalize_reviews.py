"""Render and package the review artifacts, without running research code."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from io import BytesIO
import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
from lxml import etree as ET

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
FILES=[
 'Review_I_Rohit_23BDS0051.pptx',
 'Review_II_Rohit_23BDS0051.pptx',
 'Review_III_Rohit_23BDS0051.pptx',
 'Review_III_A3_Poster_Rohit_23BDS0051.pptx',
 'Review_III_Report_Rohit_23BDS0051.docx',
]
DATE=re.compile(r'\b(?:19|20)\d{2}\b|\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|'
                r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\b')


def run(*args):
    return subprocess.run([str(a) for a in args],check=True,capture_output=True,text=True).stdout


def office_check(raw,label):
    with ZipFile(BytesIO(raw)) as z:
        for n in z.namelist():
            if n.endswith('.xml'):
                rt=ET.fromstring(z.read(n))
                texts=' '.join(rt.xpath('//*[local-name()="t"]/text()'))
                if DATE.search(texts):
                    raise ValueError(f'Calendar text remains: {label}/{n}')
                if n=='docProps/core.xml' and rt.xpath('//*[local-name()="created" or local-name()="modified" or local-name()="lastPrinted"]'):
                    raise ValueError(f'Calendar metadata remains: {label}/{n}')
                if rt.xpath('//*[local-name()="ph" and @type="dt"]'):
                    raise ValueError(f'Date placeholder remains: {label}/{n}')
            elif n.endswith('.xlsx'):
                office_check(z.read(n),label+'/'+n)


def main():
    args=argparse.ArgumentParser()
    args.add_argument('--skip-render',action='store_true',help='Use PDFs already rendered with LibreOffice.')
    opts=args.parse_args()
    if not opts.skip_render:
        lo=['libreoffice','-env:UserInstallation=file:///tmp/rohit-review-final-lo',
            '--headless','--convert-to','pdf','--outdir',str(HERE)]
        run(*lo,HERE/FILES[3])
        run('pdftoppm','-scale-to','1800','-singlefile','-png',
            HERE/Path(FILES[3]).with_suffix('.pdf'),HERE/'assets/poster')
        spec=importlib.util.spec_from_file_location('reviews',HERE/'build_reviews.py')
        builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
        builder.review_three()
        run(*lo,*[HERE/f for f in FILES if f!=FILES[3]])

    report_path=next((ROOT/'diagnostics').glob('*-exp010-confirm/results/report10.json'))
    final_report=json.loads(report_path.read_text())['verdict']
    if final_report['VERDICT']!='PARTIAL' or final_report['counts']!={'strict':272,'safe':399}:
        raise ValueError('Saved source evidence changed; review the presentation counts before packaging.')
    if not (final_report['C1'] and final_report['C2'] and final_report['C3'] and not final_report['C4']):
        raise ValueError('Frozen criterion results differ from the presentation.')

    expected_pages=[8,13,16,1,3]
    audits=[]
    for name,pages in zip(FILES,expected_pages):
        path=HERE/name
        office_check(path.read_bytes(),name)
        pdf=path.with_suffix('.pdf')
        clean=pdf.with_suffix('.clean.pdf')
        run('qpdf','--remove-info','--remove-metadata',pdf,clean)
        clean.replace(pdf)
        info=run('pdfinfo',pdf)
        if re.search(r'^(CreationDate|ModDate):',info,re.M):
            raise ValueError('Date metadata remains in '+pdf.name)
        page_count=int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1))
        if page_count!=pages:
            raise ValueError(f'Unexpected page count in {pdf.name}: {page_count}')
        txt=run('pdftotext','-layout',pdf,'-')
        if DATE.search(txt):
            raise ValueError('Calendar text remains in '+pdf.name)
        if 'Rohit Phaniram Sakamuri' not in txt or '23BDS0051' not in txt:
            raise ValueError('Student identity missing from '+pdf.name)
        audits.append({'file':name,'pdf_pages':page_count,'identity':'present',
                       'calendar_text':'absent','date_placeholders':'absent',
                       'office_and_pdf_date_metadata':'absent'})

    manifest=json.loads((HERE/'build_manifest.json').read_text())
    artifacts=[HERE/f for f in FILES]+[(HERE/f).with_suffix('.pdf') for f in FILES]
    manifest['document_checks']=audits
    manifest['saved_primary_report_sha256']=hashlib.sha256(report_path.read_bytes()).hexdigest()
    manifest['output_sha256']={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in artifacts}
    manifest['rights_notice_sha256']=hashlib.sha256((ROOT/'LICENSE').read_bytes()).hexdigest()
    (HERE/'build_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')

    delivery=HERE/'Review_Presentations_Rohit_23BDS0051.zip'
    with ZipFile(delivery,'w',ZIP_DEFLATED) as z:
        for f in artifacts:
            z.write(f,f.name)
        z.write(ROOT/'LICENSE','LICENSE')
        z.write(ROOT/'THIRD_PARTY_NOTICES.md','THIRD_PARTY_NOTICES.md')
        for notice in sorted((ROOT/'LICENSES').glob('*.txt')):
            z.write(notice,'LICENSES/'+notice.name)
        # Short, portable inventory; the repository README retains provenance/build detail.
        z.writestr('READ_ME.txt',
          'Rohit Phaniram Sakamuri | 23BDS0051\n\n'
          'Review I: proposal and literature (8 slides).\n'
          'Review II: implementation and diagnostic results (13 slides).\n'
          'Review III: completed study and fresh confirmation (16 slides).\n\n'
          'Each presentation has a PDF. The final-review companions are a Word/PDF report '
          'and an editable/printable A3 portrait poster. Print the poster at actual size.\n'
          'Dates are omitted. The final frozen verdict is PARTIAL: 22/272 failures missed; '
          '30/399 false alarms (7.52%), above the 7.5% transfer band.\n'
          'Original project material is all rights reserved. Reuse requires Rohit Phaniram '
          'Sakamuri\'s prior express written permission, subject to the included LICENSE.\n'
          'The three original templates are preserved in the project directory.\n')
    print(json.dumps({'bundle':delivery.name,'documents':len(artifacts),
                      'slide_counts':[8,13,16],'final_verdict':'PARTIAL',
                      'document_checks':'passed','bundle_bytes':delivery.stat().st_size},indent=2))


if __name__=='__main__':
    main()

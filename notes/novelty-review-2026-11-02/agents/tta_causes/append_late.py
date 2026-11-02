from pathlib import Path
import csv,json,hashlib
R=Path(__file__).resolve().parents[2]
A=R/'agents'/'tta_causes'; E=R/'evidence'/'tta_causes'
late=json.loads((A/'late-metadata.json').read_text())
rows=[]; logs=[]
for p in late:
 rows.append(dict(citation_key=p['key'],title=p['title'],year=p['year'],url=p['url'],reading_scope=p['read_scope'],decision='retained adjacent prior' if p['key']!='Zhang2026PORTAL' else 'verified direct Schirmer citer; target-label method',reason=p['method_overlap']+'; '+p['limitation'],C1='no exact report',C2='no exact report',C3='further anticipation' if p['key']=='Jiang2026ZAEC' else 'different mechanism',C4='further support for score-staleness vulnerability' if p['key']=='Ren2026StaRTTA' else 'adjacent',C5='label-free calibration repair' if p['key']!='Zhang2026PORTAL' else 'requires target labels'))
 logs.append(dict(date='2026-11-02',source='arXiv primary-record/fulltext final adversarial follow-up',query=p['url'],result_count='1 primary paper',results_url=p['local_pdf'],relevant_papers=p['key'],blocked_notes='ZAEC referenced appendices absent from downloaded9-pagePDF' if p['key']=='Jiang2026ZAEC' else ''))
for filename,data in [('late-screened-papers.csv',rows),('late-search-log.csv',logs)]:
 with (A/filename).open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
manifest=[]
for p in sorted(E.glob('*')):
 if p.is_file():manifest.append(dict(path=str(p.relative_to(R)),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),recorded_date='2026-11-02'))
(A/'evidence-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Wrote3 late primary-source records and refreshed evidence manifest')

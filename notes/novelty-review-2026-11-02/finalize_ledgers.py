"""Merge provenance ledgers; reading levels remain explicit."""
import csv,hashlib,html,json,re
from pathlib import Path
from urllib.parse import urlparse
BASE=Path(__file__).resolve().parent;PROJECT=BASE.parent.parent
DATE='2026-11-02'
def readcsv(p):
    with p.open(newline='') as f:return list(csv.DictReader(f))
def writecsv(path,rows,fields):
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)
catalog=json.loads((PROJECT/'sources/catalog.json').read_text())
norm=lambda s:re.sub(r'[^a-z0-9]','',s.lower())
def urlid(s):
    m=re.search(r'arxiv.org/(?:abs|pdf|html)/(\d{4}\.\d{4,5})',s)
    return 'arxiv:'+m[1] if m else s.rstrip('/')
titlemap={norm(r['title']):r['key'] for r in catalog};urlmap={urlid(r['url']):r['key'] for r in catalog}
logs=[]
for p in [BASE/'root-search-log.csv',*sorted((BASE/'agents').glob('*/search-log.csv')),*sorted((BASE/'agents').glob('*/late-search-log.csv'))]:
    for row in readcsv(p):
        row['agent_ledger']=str(p.relative_to(BASE));logs.append(row)
for p in sorted(BASE.glob('venue-retrieval*.json')):
    for r in json.loads(p.read_text()):
        logs.append(dict(date=DATE,source=r['source'],query=r['url'],result_count='1 retrieved resource' if r.get('status')==200 else 'not successfully retrieved',results_url=r['url'],relevant_papers='see title-screen CSV or metadata',blocked_notes=r.get('error','') or ('HTTP202 challenge content; not a successful source read' if r.get('status')==202 else ''),status=r.get('status'),file=r.get('evidence',''),agent_ledger=str(p.relative_to(BASE))))
logfields=['date','source','query','result_count','results_url','relevant_papers','blocked_notes','status','file','agent_ledger']
writecsv(BASE/'search-log.csv',logs,logfields)

screens=[]
for p in [*sorted((BASE/'agents').glob('*/screened-papers.csv')),*sorted((BASE/'agents').glob('*/late-screened-papers.csv'))]:
    for row in readcsv(p):
        row['screen_origin']=str(p.relative_to(BASE));screens.append(row)
# A row per title returned by root web search (non-paper hits remain marked as resources).
for p in sorted((BASE/'evidence').glob('root-search-*.json')):
    d=json.loads(p.read_text());r=d.get('result','')
    if isinstance(r,dict):r=r.get('value',r)
    if not isinstance(r,str):r=json.dumps(r)
    for title,url in re.findall(r'^([^\n]+) \((https?://[^\s)]+)\)\s*$',r,re.M):
        key=titlemap.get(norm(title),urlmap.get(urlid(url),''))
        screens.append(dict(citation_key=key,title=title,url=url,year='',reading_scope='Root web-index title/snippet screen only; richer source record retained if separately read',decision='title/snippet screen; not used alone for verdict',reason='Search returned this source; no full-text omission claim inferred',**{c:'Not assessed by this screen' for c in ['C1','C2','C3','C4','C5']},screen_origin=str(p.relative_to(BASE))))
for row in readcsv(BASE/'venue-title-candidates.csv'):
    key=titlemap.get(norm(row['title']),urlmap.get(urlid(row['url']),''))
    screens.append(dict(citation_key=key,title=row['title'],url=row['url'],year='',reading_scope=row['reading_scope'],decision='mechanical title triage only; not used alone for verdict',reason='Declared keyword matched official title; detailed relevance unresolved unless separately read',**{c:'Not assessed by title triage' for c in ['C1','C2','C3','C4','C5']},screen_origin='venue-title-candidates.csv: '+row['source']))
for r in catalog:
    if r.get('source_ledger')!='notes/novelty-review-2026-11-02/review.md':continue
    screens.append(dict(citation_key=r['key'],title=r['title'],url=r['url'],year=r['year'],reading_scope=r['read_scope'],decision='included as source or explicit access-limited lead',reason=r['method_overlap'],**{c:'See claim review and detailed extraction; no unstated overlap inferred' for c in ['C1','C2','C3','C4','C5']},screen_origin='record-update.json'))
def quality(row):
    s=row.get('reading_scope','').lower()
    return (10 if any(x in s for x in ['§','method','appendix','figure','full text']) else 2 if 'abstract' in s else 0)
merged={}
for row in screens:
    key=row.get('citation_key') or titlemap.get(norm(row.get('title','')),urlmap.get(urlid(row.get('url','')),''))
    identity=key or ('title:'+norm(row.get('title','')))
    if not identity or identity=='title:':continue
    row['citation_key']=key or 'screen:'+hashlib.sha256(identity.encode()).hexdigest()[:12]
    # Preserve all origins; select the most informative actually recorded reading.
    if identity in merged:
        previous=merged[identity];origins=previous.get('screen_origin','')+'; '+row.get('screen_origin','')
        selected=row if quality(row)>quality(previous) else previous
        selected=dict(selected,screen_origin=origins);merged[identity]=selected
    else:merged[identity]=row
screenfields=['citation_key','title','year','url','reading_scope','decision','reason','C1','C2','C3','C4','C5','screen_origin']
writecsv(BASE/'screened-papers.csv',list(merged.values()),screenfields)

# Detailed comparison matrices retain their original explicit reading scope.
rows=[]
for p in sorted((BASE/'agents').glob('*/*work*.csv')):
    for row in readcsv(p):rows.append(dict(origin=str(p.relative_to(BASE)),**row))
fields=list(dict.fromkeys(k for row in rows for k in row))
writecsv(BASE/'closest-work.csv',rows,fields)

files=[]
for p in sorted((BASE/'evidence').rglob('*')):
    if p.is_file():files.append(dict(file=str(p.relative_to(BASE)),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),scope='Retrieval is not full reading; consult screened-papers and source notes.'))
(BASE/'evidence-manifest.json').write_text(json.dumps(files,indent=2)+'\n')
stats=dict(date=DATE,search_rows=len(logs),distinct_screen_records=len(merged),screens_with_section_or_method_keywords=sum(quality(r)>=10 for r in merged.values()),mechanical_or_index_only=sum(quality(r)<10 for r in merged.values()),evidence_files=len(files),evidence_bytes=sum(r['bytes'] for r in files),citation_index_union=20,additional_fulltext_discovered_citer='Zhang2026PORTAL',known_distinct_schirmer_citers=21,global_citation_saturation=False)
(BASE/'review-stats.json').write_text(json.dumps(stats,indent=2)+'\n');print(json.dumps(stats,indent=2))

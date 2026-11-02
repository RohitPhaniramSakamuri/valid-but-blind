import csv,hashlib,html,json,pathlib,re,urllib.parse
BASE=pathlib.Path(__file__).resolve().parents[2];E=BASE/'evidence'/'citations';A=BASE/'agents'/'citations'
metadata=json.loads((A/'metadata.json').read_text())
new=[('2609.12136','Wang2026TemporalBoundary','§§2–3,4.1–4.2,5.4–5.6,7; AppendixJ.1; Fig1c visually inspected PDFp14','Revealed-label log-loss-regret monitor misses most AUC harm; metric mismatch, not Schirmer/Tent confidence masking'),('2512.03109','Sadhuka2025EValuator','§§2.1–2.4,3,4.1–4.3,5; Appendices8.1.2,8.1.6 and selected8.2','Independent verifier density-ratio alarm with PAC calibration; no TTA/frozen-classifier comparison')]
for aid,key,scope,overlap in new:
    s=(E/(aid+'-abs.html')).read_text();extract=lambda name:[html.unescape(x) for x in re.findall(r'<meta name="'+name+r'" content="([^"]+)"',s)]
    r=dict(key=key,title=extract('citation_title')[0],authors=extract('citation_author'),year=int(extract('citation_date')[0][:4]),url='https://arxiv.org/abs/'+aid,arxiv_id=aid,entry_type='misc',venue='arXiv preprint; no accepted venue independently verified',publication_status='Primary arXiv metadata verified 2026-11-02',read_scope=scope,locations=scope.split('; '),method_overlap=overlap,limitation='Selective reading; no experiments or independent proof verification',source_files=['evidence/citations/'+aid+'-abs.html','evidence/citations/'+aid+'-full.html'])
    metadata=[x for x in metadata if x['key']!=key];metadata.append(r)
d=json.loads((E/'fault-crossref.json').read_text())['message']['items'][0]
metadata.append(dict(key='Jia2026ODFD',title=d['title'][0],authors=[x['given']+' '+x['family'] for x in d['author']],year=2026,url='https://doi.org/'+d['DOI'],doi=d['DOI'],entry_type='article',venue='IEEE Sensors Journal',publication_status='Publisher Crossref metadata verified 2026-11-02; full text inaccessible',read_scope='Publisher Crossref metadata and Scholar abstract only; IEEE202 empty, no full text read',locations=['Crossref publisher deposit','Scholar abstract'],method_overlap='Unresolved direct citer; dual fixed uncertainty thresholds under source-free streaming TTA indicated in abstract',limitation='Methods/results/appendices inaccessible; cannot exclude direct C1–C3 overlap',source_files=['evidence/citations/fault-crossref.json','evidence/citations/fault-scholar.html']))
(A/'metadata.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
rows=list(csv.DictReader((A/'screened-papers.csv').open()));fields=list(rows[0])
for r in rows:
    if 'The Anatomy and Boundary' in r['title']:
        r.update(citation_key='Wang2026TemporalBoundary',reading_scope=new[0][2],decision='include adjacent evidence',reason=new[0][3],C1='Not Schirmer monitor; log-loss vs AUC, delayed labels, tabular correction',C2='No Tent/BN/fixed-threshold ablation',C3='Different cause: monitored loss improves while ranking worsens',C4='Partially covered: controlled sequential monitor misses adaptation harm under metric mismatch',C5='Monitor the actual deployment metric; not a label-free fix')
    if r['title'].startswith('E-valuator:'):
        r.update(citation_key='Sadhuka2025EValuator',reading_scope=new[1][2],decision='include adjacent evidence',reason=new[1][3],C1='No Schirmer baseline or Tent/frozen comparison in inspected methods/results',C2='No Tent/BN cause test',C3='Separates calibration from alarm control, not entropy-minimization cause',C4='General signal indistinguishability limits, not adaptation-masking study',C5='Independent-verifier sequential wrapper; calibration assumptions, no exact TTA fix')
    if r['title'].startswith('Online Dynamic Fault Diagnosis'):
        r.update(citation_key='Jia2026ODFD',url='https://doi.org/10.1109/JSEN.2026.3741562',reading_scope='Publisher Crossref metadata; Scholar abstract only; IEEE document,stamp,DOI,PDF each202empty; no alternateOA',decision='unresolved: full text blocked',reason='Direct citer remains a concrete access hole; cannot infer full-paper omissions from abstract',C1='Unknown: full text inaccessible',C2='Unknown; abstract mentions fixed thresholds but no result audit possible',C3='Unknown: confidence-weighted adaptation in abstract only',C4='Unknown beyond abstract-level methods',C5='Unknown: full text inaccessible')
with (A/'screened-papers.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
log=A/'search-log.csv';rows=list(csv.DictReader(log.open()));fields=list(rows[0]);known={r['file'] for r in rows}
for file in ['search-direct-citers.json','search-direct-citers2.json']:
    q=E/file
    if str(q.relative_to(BASE)) in known:continue
    d=json.loads(q.read_text());urls=re.findall(r'\((https?://[^ )]+)\)',d['result'])
    for query in d['queries']:
        rows.append(dict(date='2026-11-02',source='Web search (direct-citer follow-up)',query=query['q'],result_count='not separated across batch',results_url='https://www.google.com/search?q='+urllib.parse.quote(query['q']),relevant_papers='; '.join(dict.fromkeys(urls)),blocked_notes='Ranked search; no alternate primary full text found for IEEE11737673',status='returned',file=str(q.relative_to(BASE))))
for r in rows:
    if 'fault-' in r['file'] and r['status']=='202':r['blocked_notes']='HTTP202 zero-byte body: no article text, not successful full-text access'
    if 'fault-ieee' in r['query'] and r['status']=='202':r['blocked_notes']='HTTP202 zero-byte body: no article text'
with log.open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
manifest=[]
for q in E.iterdir():
    if q.is_file() and q.name!='manifest.json':manifest.append(dict(file=str(q.relative_to(BASE)),date='2026-11-02',bytes=q.stat().st_size,sha256=hashlib.sha256(q.read_bytes()).hexdigest()))
(E/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
stats=json.loads((A/'stats.json').read_text());stats.update(search_log_rows=len(rows),evidence_files=len(manifest),metadata_records=len(metadata));(A/'stats.json').write_text(json.dumps(stats,indent=2)+'\n');print(json.dumps(stats))

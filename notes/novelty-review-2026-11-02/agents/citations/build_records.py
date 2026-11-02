import csv,hashlib,html,json,pathlib,re
BASE=pathlib.Path(__file__).resolve().parents[2]
PROJECT=BASE.parents[1]
E=BASE/'evidence'/'citations'; A=BASE/'agents'/'citations'
norm=lambda x:re.sub(r'[^a-z0-9]','',html.unescape(x).lower())
catalog=json.loads((PROJECT/'sources'/'catalog.json').read_text())
existing={norm(x['title']):x['key'] for x in catalog}
new={
'2610.08991':('Tang2026REFIT','§§3.4,4.1,4.5–4.7,5; Table6/Fig5; selected AppendicesC–F','C5 close practical verification; ATC after input/BN correction, not sequential alarms'),
'2605.21783':('Ariq2026CertifyingAdapt','§§2–6; AppendixJ including Tables10–13 and vision protocol','C5 close theoretical certificate; static fixed representation/conditional shift assumptions, vision diagnostic noncertified'),
'2602.13848':('Shaer2026ConditionalCTM','§§1–4,5; AppendixA,B,H; Figures1–4','C4 reference contamination and C5 fixed reference; requires fixed score, measures distribution shift not classifier risk'),
'2609.00374':('Khazem2026CASTER','§§1–4.7,5; Tables1–3; mechanism-transfer discussion','C5 independent geometry gate and its failure to transfer to Tent'),
'2607.02510':('Schirmer2026LLMMonitoring','§§3.1–3.4,4.1–4.3,5; AppendixB headings; Figures1–3','C5 external verifier and sequential risk control; no TTA, calibration exchangeable with deployment'),
'2610.17343':('Liu2026ConditionalCTM','§§1–5; AppendixF table/figure mapping; fixed-score limitation','C5 faster sequential shift detector and power/delay; fixed score, no TTA classifier-risk evidence'),
'2609.23254':('Atarmla2026SelfCalibration','§§1–7 and selected AppendixA; Theorems1,2,4; Proposition4; Figure2 visually inspected','C4 adaptive thresholds manufacture blind sets; scalar synthetic tracker, no Tent or fixed-threshold cause'),
'2603.08455':('Hong2026BoilingFrog','Full main text and AppendicesA–E; Figure5 visually inspected','C4 adjacent internal-signal blindness and collapse before awareness; online model changes not specified'),
'2609.20700':('Wang2026PredictionFragmentation','§§2–6; Table2; selected supplementsS1.3,S4,S9,S10; limitation passages','C5 source/live disagreement geometry controls harmful edits; no sequential risk guarantee'),
}
metadata=[]
for aid,(key,scope,overlap) in new.items():
    stem='martingale-new' if aid=='2610.17343' else aid
    s=(E/(stem+'-abs.html')).read_text()
    extract=lambda name:[html.unescape(x) for x in re.findall(r'<meta name="'+name+r'" content="([^"]+)"',s)]
    title=extract('citation_title')[0]
    key=existing.get(norm(title),key)
    authors=extract('citation_author');date=extract('citation_date')[0]
    rec={'key':key,'title':title,'authors':authors,'year':int(date[:4]),'url':'https://arxiv.org/abs/'+aid,'arxiv_id':aid,'entry_type':'misc','venue':'arXiv preprint; no accepted venue independently verified','publication_status':'Primary arXiv metadata verified 2026-11-02','read_scope':scope,'locations':scope.split('; '),'method_overlap':overlap,'limitation':'No experiments or code execution; claims here summarize paper evidence, not independent verification.','source_files':[str((E/(stem+'-abs.html')).relative_to(BASE)),str((E/(stem+'-full.html')).relative_to(BASE))]}
    if aid=='2602.13848':rec.update(entry_type='inproceedings',venue='Proceedings of the 43rd International Conference on Machine Learning, PMLR306:109447–109469',publication_status='ICML2026 publication verified against official PMLR page',published_url='https://proceedings.mlr.press/v306/shaer26a.html')
    metadata.append(rec)
(A/'metadata.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
byid={x['arxiv_id']:x for x in metadata}
screen={}
def add(title,url,year='',aid='',scope='title/metadata screen only',decision='exclude from close evidence',reason='No direct evidence of the claimed adapted-versus-frozen sequential-monitor comparison established by this screen',edge=''):
    title=html.unescape(title)
    if title.startswith('If the contribution is primarily'):return
    n=norm(title)
    key=existing.get(n,'arxiv:'+aid if aid else '')
    if aid in byid:
        r=byid[aid];key=r['key'];scope=r['read_scope'];decision='include in close evidence';reason=r['method_overlap']
    row={'citation_key':key,'title':title,'year':year,'url':url,'reading_scope':scope,'decision':decision,'reason':reason,'C1':'No same result established by current reading','C2':'No fixed-threshold entropy-versus-BN cause established','C3':'Not established in this screening','C4':'Not established in this screening','C5':'Not established in this screening','citation_edge':edge}
    if n not in screen:screen[n]=row
    elif decision=='include in close evidence':screen[n]=row
    else:screen[n]['citation_edge']+='; '+edge
for file,field,edge in [('s2_citations_retry.json','citingPaper','forward citation of Schirmer'),('s2_refs_round3.json','citedPaper','backward reference of Schirmer')]:
    for x in json.loads((E/file).read_text())['data']:
        r=x[field];aid=(r.get('externalIds') or {}).get('ArXiv','');add(r['title'],'https://arxiv.org/abs/'+aid if aid else r.get('url',''),r.get('year',''),aid,edge=edge)
scholar=[]
for stem in ['scholar_cites_retry','scholar_cites10']:
    scholar.extend(json.loads((E/(stem+'-records.json')).read_text()))
for r in scholar:
    aid=r['url'].split('/abs/')[-1] if '/abs/' in r['url'] else ''
    add(r['title'],r['url'],2026 if '2026' in r['meta'] else 2025 if '2025' in r['meta'] else '',aid,scope='Google Scholar title/snippet screen; primary inaccessible unless separately recorded',edge='Google Scholar forward citation of Schirmer')
for q in E.glob('*-cites.json'):
    d=json.loads(q.read_text())
    for x in d.get('data',[]):
        r=x.get('citingPaper',{});aid=(r.get('externalIds') or {}).get('ArXiv','');add(r.get('title',''), 'https://arxiv.org/abs/'+aid if aid else r.get('url',''),r.get('year',''),aid,edge='forward citation of '+q.stem.removesuffix('-cites'))
for aid,r in byid.items():add(r['title'],r['url'],r['year'],aid,edge='close citation neighbor')
for q in E.glob('*-abs.html'):
    s=q.read_text();aid=re.findall(r'<meta name="citation_arxiv_id" content="([^"]+)"',s);title=re.findall(r'<meta name="citation_title" content="([^"]+)"',s);date=re.findall(r'<meta name="citation_date" content="([^"]+)"',s)
    if aid and title:add(title[0],'https://arxiv.org/abs/'+aid[0],date[0][:4] if date else '',aid[0],scope='Primary arXiv metadata and abstract; no full-paper omission claim',edge='citation neighbor metadata')
for row in screen.values():
    k=row['citation_key']
    if k=='Atarmla2026SelfCalibration':row.update(C4='Substantially anticipates adaptation-induced masking via thresholds; does not prove universal C4',C5='Warns gains/false-alarm guarantees leave blind sets; no fix demonstrated for TTA')
    if k=='Hong2026BoilingFrog':row.update(C4='Partially covers internal-signal blindness; no online model update specified',C5='Calls for external supervisory monitoring, untested as fix')
    if k=='Shaer2026ConditionalCTM':row.update(C4='Partially covers self-normalizing reference contamination',C5='Fixed-reference anytime-valid shift alarm, fixed score required')
    if k=='Liu2026ConditionalCTM':row.update(C5='Fixed-score shift alarm with restart and delay bounds; no risk-monitor TTA validation')
    if k=='Tang2026REFIT':row.update(C5='Post-correction ATC verification and abstention already exist; no sequential error control')
    if k=='Schirmer2026LLMMonitoring':row.update(C5='External verifier risk-calibrated online monitor; different task and exchangeability')
    if k=='Khazem2026CASTER':row.update(C5='Independent geometry gate already exists and poor transfer to Tent is demonstrated')
    if k=='Ariq2026CertifyingAdapt':row.update(C5='Static baseline-relative certificate; assumptions/audit needed, vision vacuous')
    if k=='Wang2026PredictionFragmentation':row.update(C3='Weak confidence/entropy association with adaptation harm in Table2, different metric/task',C5='Offline-calibrated source/live geometry rollback, stopping and routing')
with (A/'screened-papers.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(next(iter(screen.values())).keys()));w.writeheader();w.writerows(screen.values())
log=A/'search-log.csv';rows=list(csv.DictReader(log.open()));fields=list(rows[0])
for q in E.glob('search-round*.json'):
    d=json.loads(q.read_text());urls=re.findall(r'\((https?://[^ )]+)\)',d['result'])
    for query in d['queries']:
        rows.append(dict(date=d['date'],source='Web search (batched; primary evidence checked separately)',query=query['q'],result_count='not separated by tool across batched queries',results_url='https://www.google.com/search?q='+__import__('urllib.parse',fromlist=['quote']).quote(query['q']),relevant_papers='; '.join(dict.fromkeys(urls)),blocked_notes='Ranking-limited results; exact per-query count unavailable; raw output saved',status='returned',file=str(q.relative_to(BASE))))
for stem,url in [('atarmla_fig2','https://arxiv.org/html/2609.23254v1/figA1_trace.png'),('hong_fig5','https://arxiv.org/html/2603.08455v1/fig_pe_fft.png')]:
    rows.append(dict(date='2026-11-02',source='arXiv figure image',query=url,result_count=1,results_url=url,relevant_papers=stem,blocked_notes='Visually inspected against caption; no experiment',status=200,file='evidence/citations/'+stem+'.png'))
with log.open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
manifest=[]
for q in E.iterdir():
    if q.is_file() and q.name!='manifest.json':manifest.append(dict(file=str(q.relative_to(BASE)),date='2026-11-02',bytes=q.stat().st_size,sha256=hashlib.sha256(q.read_bytes()).hexdigest()))
(E/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
scholar_unique={norm(x['title']) for x in scholar};s2_titles={norm(x['citingPaper']['title']) for x in json.loads((E/'s2_citations_retry.json').read_text())['data']}
stats={'scholar_citer_records':len(scholar),'scholar_unique_citers':len(scholar_unique),'s2_citers':len(s2_titles),'unique_scholar_s2_union':len(scholar_unique|s2_titles),'screened_rows':len(screen),'search_log_rows':len(rows),'evidence_files':len(manifest)}
(A/'stats.json').write_text(json.dumps(stats,indent=2)+'\n');print(json.dumps(stats))

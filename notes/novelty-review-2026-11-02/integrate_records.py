"""Append dated literature records without rebuilding historical libraries."""
import csv, hashlib, json, re, shutil, unicodedata
from pathlib import Path
BASE=Path(__file__).resolve().parent
PROJECT=BASE.parent.parent
DATE='2026-11-02'
LEDGER='notes/novelty-review-2026-11-02/review.md'

def norm(s):
    return re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKD',str(s)).encode('ascii','ignore').decode().lower())

def normalize(raw,origin):
    row=dict(raw)
    row['key']=raw['key']
    row['entry_type']=raw.get('entry_type',raw.get('type','misc'))
    row['venue']=raw.get('venue',raw.get('journal',raw.get('booktitle',raw.get('institution','arXiv preprint; venue not independently verified'))))
    row['read_scope']=raw.get('read_scope',raw.get('reading_scope','Metadata only; see source ledger.'))
    row['publication_status']=raw.get('publication_status',raw.get('qualification','Metadata verified against linked primary source; see dated review.'))
    row['method_overlap']=raw.get('method_overlap',raw.get('relevance','See claim-specific extraction in dated review.'))
    row['limitation']=raw.get('limitation',raw.get('qualification','Selective reading; no experiments or independent proof verification.'))
    row['locations']=raw.get('locations',[])
    row['review_origin']=origin
    row['source_ledger']=LEDGER
    row['accessed']=DATE
    row['freshly_verified']=DATE
    return row

raws=[]
for p in sorted((BASE/'agents').glob('*/*metadata.json')):
    for row in json.loads(p.read_text()):raws.append(normalize(row,str(p.relative_to(PROJECT))))
foundation=[
dict(key='Guo2017Calibration',title='On Calibration of Modern Neural Networks',authors=['Chuan Guo','Geoff Pleiss','Yu Sun','Kilian Q. Weinberger'],year=2017,entry_type='inproceedings',venue='Proceedings of the 34th International Conference on Machine Learning, PMLR 70:1321–1330',url='https://proceedings.mlr.press/v70/guo17a.html',read_scope='Selective primary PDF §§2–4, Figures1–3, Table1; temperature-scaling definition. No TTA experiments.',locations=['§§2–4','Figures1–3','Table1'],method_overlap='Calibration and classification accuracy differ; foundation only, not direct evidence of C1–C2.'),
dict(key='Hendrycks2017FailureBaseline',title='A Baseline for Detecting Misclassified and Out-of-Distribution Examples in Neural Networks',authors=['Dan Hendrycks','Kevin Gimpel'],year=2017,entry_type='inproceedings',venue='International Conference on Learning Representations',url='https://arxiv.org/abs/1610.02136',read_scope='Selective §§2–3 softmax baseline and AUROC/AUPR definitions; experimental section mapped, not fully audited.',locations=['§§2–3'],method_overlap='Maximum-softmax error detection foundation; no adaptation or sequential alarm.',publication_status='ICLR2017 header verified; preprint first2016.'),
dict(key='Podkopaev2022RiskMonitoring',title='Tracking the risk of a deployed model and detecting harmful distribution shifts',authors=['Aleksandr Podkopaev','Aaditya Ramdas'],year=2022,entry_type='inproceedings',venue='International Conference on Learning Representations',url='https://arxiv.org/abs/2110.06177',read_scope='Selective §§1–2.2, hypothesis/false-alarm definitions and confidence-sequence construction; experiments/appendix mapped, not full proof audit.',locations=['§§1–2.2'],method_overlap='Foundational supervised risk monitoring; needs target outcomes; false-alarm control does not alone guarantee useful power.',publication_status='ICLR2022 confirmed against DBLP official conference record; preprint first2021.'),
dict(key='Howard2021ConfidenceSequences',title='Time-uniform, nonparametric, nonasymptotic confidence sequences',authors=['Steven R. Howard','Aaditya Ramdas','Jon McAuliffe','Jasjeet Sekhon'],year=2021,entry_type='article',venue='The Annals of Statistics 49(2):1055–1080',journal='The Annals of Statistics',doi='10.1214/20-AOS1991',url='https://arxiv.org/abs/1810.08240',read_scope='Introduction and definition Eq1 read; theorem/appendix structure mapped only. No proof verification.',locations=['Introduction','Eq1'],method_overlap='Confidence-sequence coverage definition; mathematical foundation only, not direct C1 evidence.',publication_status='2021 journal metadata verified; saved arxivv9 is a2022 revision of2018 preprint.')]
raws += [normalize(x,'notes/novelty-review-2026-11-02/evidence/root/') for x in foundation]

# Fresh readings of existing stable-key works; do not fabricate fresh full-paper scope.
existing_updates={
'Garg2022ATC':dict(read_scope='Primary PDF §§3.1–4/Proposition1/Corollary1/Example1, §5 experimental setup; AppendixA proof/example map. Not full proof verification.',locations=['§3.1 Proposition1/Corollary1/Example1','§4','§5'],method_overlap='Target accuracy unidentifiable without assumptions even with source joint and target marginal; ATC calibrates a fixed classifier threshold. Not an adaptation-proof risk alarm.'),
'Park2023LSA':dict(read_scope='Primary arxiv PDF §3 adapter/prior estimation, §4/Tables1–2/§4.4 and §6 conclusion; main text only, referenced supplementary not independently audited.',locations=['§3','§4 Tables1–2','§4.4','§6'],method_overlap='Combines corruption and forward/uniform/backward long-tailed class distributions; source/BN/Tent comparisons and prior-conditioned adapter. Source training can itself be long-tailed; no sequential alarms.'),
'Kim2024TTALine':dict(read_scope='Primary PDF §§3–5.2/Table3/Figure3, §§6–7, appendix algorithm/data-budget map. Relevant methods/results selective, not all theoretical proofs.',locations=['§5.2 Table3/Figure3','§6','§7','AppendixD'],method_overlap='Agreement-based unlabeled performance and TTA-method selection already exist; adaptation can improve those estimators. Needs multiple candidates and sufficient ID data; no sequential risk guarantee or class-prior-skew test established.'),
'Press2024EntropyEnigma':dict(read_scope='§§4.1–4.4 selectively reread in final close-work audit; offline fitted weighted-flip estimator and its initial-model dataset-accuracy target checked.',locations=['§§4.1–4.4'],method_overlap='Prediction-flip accuracy estimation during entropy adaptation is prior art; estimates initial/source dataset accuracy with offline labeled fitting, not current-model sequential risk.'),
'Schirmer2025Monitoring':dict(read_scope='Official NeurIPS PDF §§2–6, AppendicesA.1–A.5/B.1–B.4 and experimental configuration; Fig5 rendered/visually inspected. Cross-read arxivv2. Selective, not all proofs/checklist.',locations=['§§3.2–3.4','§§5.1–5.4','Figure5','AppendicesA.1–A.5,B.1–B.4'],method_overlap='Already documents uncertainty-proxy alarm failure for T3A/STAD and prototype-distance repair; no exact C1 comparison established.',venue='NeurIPS2025, Advances in Neural Information Processing Systems38'),
'Lee2024AETTA':dict(read_scope='Main §§3–5/Figures2–4,6/Tables1–3; supplementA/C/D.1/D.4/F; Fig2 visually inspected by TTA subreview.',locations=['§3.2/Figure2','§3.3','Tables1–2','SupplementC,D.1,D.4'],method_overlap='Confidence/accuracy decoupling and corrected disagreement/recovery are prior art; no same sequential missed-risk comparison.'),
'Cygert2026RealisticSelection':dict(read_scope='Published2026 PDF §§3.1,4,5.1–5.3/Figures6–8; Figure6 visually inspected. Older preprint distinguished.',locations=['§5.2/Figure6 p81','Figures7–8 p82'],method_overlap='Corrupted CIFAR100 Dirichlet-class-correlation proxy selection already studied; no Schirmer alarm comparison.'),
'Bar2024ProtectedTTA':dict(read_scope='§§2–4/Figures1,3/AppendicesF.4,G; S2 all27 citations and110 reference metadata screened.',locations=['§§2–4','AppendicesF.4,G'],method_overlap='Betting/entropy monitoring controls adaptation; label-prior caveats already recognized.'),
'Zhao2023Pitfalls':dict(read_scope='§§4–6/Tables3–5/AppendixF.1; clean label-shift tables distinguished from corruption evaluations.',locations=['§6','Tables3–5','AppendixF.1'],method_overlap='Dirichlet/TTA degradation and BN vulnerabilities established; not a Schirmer missed-alarm test.'),
'Niu2023SAR':dict(read_scope='§§3.1–3.2,4,5/Figure2/Table5 selectively inspected.',locations=['§3.1','Figure2','Table5'],method_overlap='Separates statistics problems and entropy collapse, gives heuristic reset; no sequential power guarantee.'),
'Lee2024DeYO':dict(read_scope='§§3–4/Table5/AppendixM selectively inspected.',locations=['§§3–4','Table5','AppendixM'],method_overlap='Perturbation-derived reliability and stable updates; accuracy improvement is not a monitoring remedy guarantee.'),
'Marsden2024ROID':dict(read_scope='§§3–5/Figure4/Tables3–4/selectedAppendixB.',locations=['§§3–5','Tables3–4'],method_overlap='Prior correction/diversity already address correlated class/corruption streams; no exact monitor-sensitivity evaluation.'),
'Han2026Exchangeability':dict(read_scope='§3,§6 and AppendixL pp45–49/Tables48–51 read in detail; other main/appendix sections selective only.',locations=['AppendixL pp45–49','Tables48–51'],method_overlap='Adapted forecasting residuals self-mask sustained shifts; frozen residual sentinel restores empirical sensitivity. Requires revealed outcomes, not label-free classifier monitoring.'),
'Kasa2024EACP':dict(read_scope='§§2–4/Algorithm1/Tables1–3; AppendixB/C/D map.',locations=['Tables1–3','Algorithm1'],method_overlap='Entropy-scaled conformal correction plus ETA; no anytime risk alarm; nominal undercoverage remains.'),
'Lyu2025CUI':dict(read_scope='Arxivv1 §§3–5/Algorithm1/Table2/Figure2; later OpenReview status blocked/unverified.',locations=['§4.1.2','§4.3.1','Table2'],method_overlap='Source/current-model uncertainty correction already addresses evolving-model proxy drift; no class-prior-risk power result.'),
}

backup=BASE/'record-backups';backup.mkdir(exist_ok=True)
for filename in ['REFERENCES.md','references.bib','sources/catalog.json','sources/catalog.csv','README.md','CHANGELOG.md','notes/research-branches.md']:
    src=PROJECT/filename;dst=backup/filename.replace('/','__')
    if src.exists() and not dst.exists():shutil.copy2(src,dst)
catalog=json.loads((PROJECT/'sources/catalog.json').read_text());by={r['key']:r for r in catalog}
bib=(PROJECT/'references.bib').read_text()
added=[];refreshed=[];aliases=[];records=[]
for row in raws:
    key=row['key'];duplicate=next((old for old in catalog if old['key']!=key and (norm(old['title'])==norm(row['title']) or (old.get('doi') and row.get('doi') and old['doi'].lower()==row['doi'].lower()))),None)
    if duplicate:
        aliases.append(dict(requested=key,canonical=duplicate['key'],reason='same normalized title or DOI'));key=duplicate['key'];row['key']=key
    is_new=key not in by
    if is_new:
        by[key]=row;catalog.append(row);added.append(key)
    else:
        old=by[key]
        for field in ['title','authors','year','entry_type','venue','url','doi','journal','booktitle','volume','number','pages','publication_status','read_scope','locations','method_overlap','limitation','accessed','freshly_verified','source_ledger','review_origin']:
            if field in row:old[field]=row[field]
        row=old;refreshed.append(key)
    history=row.setdefault('reading_history',[])
    if not any(x.get('date')==DATE and x.get('source_ledger')==LEDGER for x in history):history.append(dict(date=DATE,read_scope=row['read_scope'],locations=row.get('locations',[]),source_ledger=LEDGER))
    records.append(row)
for key,update in existing_updates.items():
    row=by[key];row.update(update,accessed=DATE,freshly_verified=DATE,source_ledger=LEDGER);refreshed.append(key)
    history=row.setdefault('reading_history',[])
    if not any(x.get('date')==DATE and x.get('source_ledger')==LEDGER for x in history):history.append(dict(date=DATE,read_scope=row['read_scope'],locations=row['locations'],source_ledger=LEDGER))
    records.append(row)

unique_records={r['key']:r for r in records}
for key in added:
    r=by[key];typ=r.get('entry_type','misc')
    fields={'title':'{'+r['title']+'}','author':' and '.join(r['authors']),'year':str(r['year']),'url':r['url']}
    if typ=='article':fields['journal']=r.get('journal',r['venue'])
    elif typ=='inproceedings':fields['booktitle']=r.get('booktitle',r['venue'])
    elif typ=='techreport':fields['institution']=r.get('institution',r['venue'])
    else:fields['howpublished']=r['venue']
    for k in ['doi','volume','number','pages']:
        if r.get(k):fields[k]=str(r[k])
    fields['note']=r['publication_status'];fields['urldate']=DATE
    bib+='\n@'+typ+'{'+key+',\n'+''.join('  '+k+' = {'+v+'},\n' for k,v in fields.items())+'}\n'

# Update known stale venue status in-place while preserving keys/other fields.
for key in ['Amoukou2024SequentialHarmful','Nguyen2025D3M','Zhang2026PPRM']:
    r=by[key];pattern=r'@\w+\{'+re.escape(key)+r',\n.*?\n\}'
    match=re.search(pattern,bib,re.S)
    if match:
        block=match[0];block=re.sub(r'^@\w+', '@inproceedings',block)
        block=re.sub(r'  howpublished = \{.*?\},\n','  booktitle = {'+r['venue']+'},\n',block)
        block=re.sub(r'  note = \{.*?\},\n','  note = {'+r['publication_status']+'},\n',block)
        block=re.sub(r'  urldate = \{.*?\},','  urldate = {'+DATE+'},',block)
        if r.get('doi') and '  doi =' not in block:block=block[:-1]+'  doi = {'+r['doi']+'},\n}'
        bib=bib[:match.start()]+block+bib[match.end():]
(PROJECT/'references.bib').write_text(bib)
(PROJECT/'sources/catalog.json').write_text(json.dumps(catalog,indent=2,ensure_ascii=False)+'\n')
with (PROJECT/'sources/catalog.csv').open('w') as f:
    fields=list(dict.fromkeys(k for r in catalog for k in r))
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
    for r in catalog:w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in r.items()})

for key,r in unique_records.items():
    path=PROJECT/'papers'/f'{key}.md'
    text=path.read_text() if path.exists() else '# '+r['title']+'\n\nCitation key: `'+key+'`.\n'
    marker='## Adversarial review — 2 November 2026'
    section='\n'+marker+'\n\n'+', '.join(r['authors'])+'. '+str(r['year'])+'. '+r['venue']+'. [Primary source]('+r['url']+').\n\nPublication/version qualification: '+r['publication_status']+'\n\n**Actual reading:** '+r['read_scope']+'\n\n**Locations:** '+('; '.join(r.get('locations',[])) or 'Metadata/abstract only; full text not read.')+'\n\n**Method/evidence and connection:** '+r['method_overlap']+'\n\n**Limit:** '+r.get('limitation','Selective literature inspection, not independent reproduction or a complete proof audit.')+'\n\n**Next reading step:** resolve access/version limits and the precise C1–C5 overlap before stronger claims. [Detailed claim review](../'+LEDGER+'); [source-level reading and extraction](../'+r.get('review_origin',LEDGER)+'). No experiments were run for this reading.\n'
    if marker in text:text=text[:text.index(marker)].rstrip()+'\n'+section
    else:text+=section
    if key=='Schirmer2025Monitoring':
        text=text.replace('Year and venue: 2025; NeurIPS 39.','Year and venue: 2025; NeurIPS2025, Advances in Neural Information Processing Systems38 (39th conference).')
        text=text.replace('No local PDF in this project.','Current primary PDF: [saved NeurIPS version](../notes/novelty-review-2026-11-02/evidence/root/Schirmer2025Monitoring-neurips.pdf); earlier reading history retained below.')
    path.write_text(text)

baseline=json.loads((backup/'sources__catalog.json').read_text())
cumulative_added=[r['key'] for r in catalog if r['key'] not in {x['key'] for x in baseline}]
index=PROJECT/'REFERENCES.md';text=index.read_text()
heading='## Adversarial novelty review — 2 November 2026'
if heading in text:text=text[:text.index(heading)].rstrip()+'\n'
new_table='\n'+heading+'\n\nCurrent library: **'+str(len(catalog))+' records**. This review adds '+str(len(cumulative_added))+' distinct sources and appends dated reading histories; past counts above are historical snapshots. Reading scope varies explicitly; blocked metadata-only sources are not verdict evidence. [Review]('+LEDGER+'); [search/screening ledgers](notes/novelty-review-2026-11-02/).\n\n| Key/source | Publication and reading scope | Overlap/limit |\n| --- | --- | --- |\n'
for key,r in unique_records.items():
    vals=['`'+key+'` — ['+r['title']+']('+r['url']+')',r['venue']+'. '+r['read_scope'],r['method_overlap']+' '+r['limitation']+' [Note](papers/'+key+'.md).']
    new_table+='| '+' | '.join(v.replace('|','/').replace('\n',' ') for v in vals)+' |\n'
text+=new_table
text=text.replace('Updated 2026-10-26. **103 distinct records: 101 scholarly sources and 2 official benchmark/web records.**','Current update: **2026-11-02; '+str(len(catalog))+' records**. The dated addendum below describes the current review. Historical 2026-10-26 snapshot: **103 distinct records: 101 scholarly sources and 2 official benchmark/web records.**',1)
text=re.sub(r'Current update: \*\*2026-11-02; \d+ records\*\*','Current update: **2026-11-02; '+str(len(catalog))+' records**',text,count=1)
index.write_text(text)
stats=dict(date=DATE,catalog_records=len(catalog),added_keys=cumulative_added,new_in_this_invocation=added,refreshed_keys=sorted(set(refreshed)),aliases=aliases,note_keys=list(unique_records))
(BASE/'record-update.json').write_text(json.dumps(stats,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(stats,indent=2,ensure_ascii=False))

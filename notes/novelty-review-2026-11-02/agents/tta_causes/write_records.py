"""Write literature review ledgers from manually inspected documents, without model runs."""
from pathlib import Path
import csv,hashlib,json,re

P=Path(__file__).resolve().parents[4]
R=P/'notes'/'novelty-review-2026-11-02'
A=R/'agents'/'tta_causes'; E=R/'evidence'/'tta_causes'

new=[
dict(key='Amin2025OverCertainty',title='The Over-Certainty Phenomenon in Modern Test-Time Adaptation Algorithms',authors=['Fin Amin','Jung-Eun Kim'],year=2025,venue='Transactions on Machine Learning Research',entry_type='article',url='https://arxiv.org/abs/2404.16168',read_scope='2026-11-02 selective full text: v4 §§3–6, Figs1–3, Tables1–3/7–11, AppendixA.1–A.5 selected; not all proofs/references read',locations=['§3','§3.1','§4','§6.3','Tables1–3/7–11'],publication_status='TMLR07/2025 printed in arXiv2404.16168v4 header; first preprint title used UDA in2024',local_pdf='evidence/tta_causes/2404.16168.pdf'),
dict(key='Nam2026SICL',title='Towards Reliable Test-Time Adaptation: Style Invariance as a Correctness Likelihood',authors=['Gilhyun Nam','Taewon Kim','Joonhyun Jeong','Eunho Yang'],year=2026,venue='Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision',pages='3088--3097',doi='10.1109/WACV61042.2026.00302',entry_type='inproceedings',url='https://openaccess.thecvf.com/content/WACV2026/papers/Nam_Towards_Reliable_Test-Time_Adaptation_Style_Invariance_as_a_Correctness_Likelihood_WACV_2026_paper.pdf',read_scope='2026-11-02 selective full text published §§4–7/Fig2/Table2; preprint AppendixC/D; Fig2 visually checked; not all references read',locations=['§4.2/Fig2 p3090','§6.3','§7.1–7.4','preprint AppendixC.3'],publication_status='WACV2026 official CVF PDF; arXiv2512.07390 is preprint2025',local_pdf='evidence/tta_causes/Nam2026SICL-published.pdf'),
dict(key='Ahmed2026Dashboard',title='The dashboard says “perfect:” a systematic audit of label-free model monitoring and test-time adaptation under temporal distribution shift in network intrusion detection',authors=['Wali Ahmed','Md Azizul Rahaman','Pappu Roy','Parves Alam'],year=2026,venue='Frontiers in Artificial Intelligence',volume='9',pages='1928858',doi='10.3389/frai.2026.1928858',entry_type='article',url='https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2026.1928858/full',read_scope='2026-11-02 publisher full methods §§3.1–3.4, experimental §§4.1–4.6, Props1–2, Tables5–8, discussion/limitations§5.4; not every reference or supplement read',locations=['§3.3.2','§3.4','§4.3 Props1–2/Table6','§4.6/Table8','§5.4'],publication_status='Publisher metadata verifies08October2026 publication; full article saved; claims not independently reproduced',local_pdf='evidence/tta_causes/Ahmed2026Dashboard.pdf'),
dict(key='Zhang2025COME',title='COME: Test-time Adaptation by Conservatively Minimizing Entropy',authors=['Qingyang Zhang','Yatao Bian','Xinke Kong','Peilin Zhao','Changqing Zhang'],year=2025,venue='International Conference on Learning Representations',entry_type='inproceedings',url='https://arxiv.org/abs/2410.10894',read_scope='2026-11-02 arXivv1 selective full text §§3–5, Figs1–2, Theorem1, Tables1–4, AppendixC.1/C.5/C.8/D.2; indexed official published PDF header/authors verified; direct published-PDF fetch403',locations=['§3/Figs1–2','§4.3/Theorem1','§5.1–5.2','AppendixD.2'],publication_status='ICLR2025 header in indexed official OpenReview PDF; local text is older under-review arXivv1 with title adaption',local_pdf='evidence/tta_causes/COME.pdf'),
dict(key='Li2026OpenSetAccuracy',title='A Closer Look at In-Distribution vs. Out-of-Distribution Accuracy for Open-Set Test-time Adaptation',authors=['Zefeng Li','Evan Shelhamer'],year=2026,venue='Transactions on Machine Learning Research',entry_type='article',url='https://arxiv.org/abs/2606.01973',read_scope='2026-11-02 selective full text §§3.1–3.3/4.1–4.9, Tables1/10/11/13, §5 conclusion and relevant appended figures; not all references read',locations=['§3.3','§4.6 p10','Tables1/10/11/13','§5 p13'],publication_status='TMLR05/2026 printed in arXiv2606.01973v1 header; first arXiv posting01June2026',local_pdf='evidence/tta_causes/Li2026OpenSetAccuracy.pdf'),
dict(key='Nielen2026DSBR',title='Entropy Minimization without Model Collapse: Mitigating Prediction Bias in Medical Imaging',authors=['Tim Nielen','Sameer Ambekar','Johannes Kiechle','Daniel M. Lang','Julia A. Schnabel'],year=2026,venue='arXiv preprint2606.02339',entry_type='misc',url='https://arxiv.org/abs/2606.02339',read_scope='2026-11-02 selective full text §§3–5, Figs2/4, Tables1–3, AppendixG; not all proofs/experiments read',locations=['§3.1–3.2 pp4–5','§4 pp5–6','§5.1–5.2','AppendixG p24'],publication_status='Primary arXiv metadata verified; institute reports forthcoming NeurIPS2026 spotlight but independent proceedings confirmation not completed',local_pdf='evidence/tta_causes/Nielen2026DSBR.pdf')]
(A/'metadata.json').write_text(json.dumps(new,indent=2,ensure_ascii=False)+'\n')

# Every directly inspected paper, including abstract-only leads, is named here.
main=[
('Amin2025OverCertainty','retained','Over-certainty and certainty-driven reliability already studied','no exact alarm','no Schirmer factorial','substantially anticipated','vulnerability anticipated','calibration repair prior'),
('Nam2026SICL','retained','TTA calibration worsens; adaptation-aware probe correction','no class-prior skew alarm','no monitor factorial','substantially anticipated','vulnerability anticipated','method predecessor'),
('Ahmed2026Dashboard','retained','Fixed-threshold confidence monitor selects collapsed variant','different monitor/domain/collapse','not entropy-isolated','partially covered','already published existence','abstention alarm prior'),
('Zhang2025COME','retained','Conservative entropy objective plus misclassification detection','no sequential alarm','different objective ablation','substantially anticipated','vulnerability anticipated','newer method comparator'),
('Li2026OpenSetAccuracy','retained','Adaptation confidence worsens unknown-class rejection','open-set different risk target','normalization comparisons not causal factorial','substantially anticipated','already published analogue','partial rejection repair'),
('Nielen2026DSBR','retained','Prediction bias amplification and ROC-AUC limits despite accuracy repair','no sequential alarm','mechanism on GN no Schirmer','partially covered','partially covered','newer method comparator'),
('Lee2024AETTA','retained','Direct confidence/error divergence and disagreement proxy failure','no exact class-prior monitoring comparison','no Schirmer threshold factorial','substantially anticipated','already published existence','label-free recovery predecessor'),
('Cygert2026RealisticSelection','retained','Corruption+Dirichlet class correlation defeats proxy selection','strong ingredient overlap no Schirmer alarm','not monitor causal test','substantially anticipated','already published analogue','alternative selection metrics limited'),
('Press2024EntropyEnigma','retained','EM phases and weighted prediction-flip accuracy estimation','no sequential alarm','not monitor cause','mechanism anticipated','partially covered','estimator predecessor'),
('Bar2024ProtectedTTA','retained','Sequential entropy betting and label-shift false-trigger limitation','different detector target','not miss-gap factorial','partially covered','feedback-aware monitoring','sequential detector prior'),
('Zhao2023Pitfalls','retained','Known class skew/BN/Tent failures and pretrained model sensitivity','shift ingredients known','BN vs Tent rationale','indirect','indirect','benchmark precedent'),
('Niu2023SAR','retained','Separates BN failures and entropy collapse on GN; recovery','not same monitor','general ablation anticipated','indirect','entropy heuristics known','newer method/heuristic baseline'),
('Lee2024DeYO','retained','Independent object-destructive reliability probe','not same monitor','not monitor factorial','indirect','indirect','sample-signal baseline'),
('Marsden2024ROID','retained','Prior-corrected stable adaptation under correlated corruption','shift setting prior','not monitor factorial','indirect','indirect','newer method baseline'),
('Weerasinghe2026LATTA','retained','Entropy-affine drift under partial class imbalance','shift/entropy mechanism known','not monitor factorial','partially covered','indirect','newer class-prior baseline')]
catalog=json.loads((P/'sources/catalog.json').read_text())+new
bykey={p['key']:p for p in catalog}
rows=[]
scopes={
'Lee2024AETTA':'2026-11-02 selective full text §§3–5, Figs2–4/6, Tables1–3, supplementA/C/D.1/D.4/F; Fig2 visually inspected',
'Cygert2026RealisticSelection':'2026-11-02 published PDF §§3.1/4/5.1–5.3, Figs6–8; Fig6 visually inspected',
'Press2024EntropyEnigma':'2026-11-02 selective full text §§2–4/6; AppendixA/B/C/D/E selected',
'Bar2024ProtectedTTA':'2026-11-02 selective full text §§2–4, Figs1/3, AppendixF.4/G',
'Zhao2023Pitfalls':'2026-11-02 selective full text §§4–6, Tables3–5, AppendixF.1',
'Niu2023SAR':'2026-11-02 selective full text §§3.1–3.2/4/5, Fig2/Table5',
'Lee2024DeYO':'2026-11-02 selective full text §§3–4,Table5,AppendixM',
'Marsden2024ROID':'2026-11-02 selective full text §§3–5,Fig4,Tables3–4,AppendixB selected',
'Weerasinghe2026LATTA':'2026-11-02 selective full text §§3–6,Eq4/7/Table1; prior stored supplement derivation not freshly reread'}
for key,decision,reason,*overlap in main:
 p=bykey[key]
 rows.append(dict(citation_key=key,title=p['title'],year=p['year'],url=p['url'],reading_scope=scopes.get(key,p['read_scope']),decision=decision,reason=reason,**dict(zip(['C1','C2','C3','C4','C5'],overlap))))

abstracts=[
('Zhang2026UATTA','Pretrain-then-Adapt: Uncertainty-Aware Test-Time Adaptation for Text-based Person Search',2026,'https://arxiv.org/abs/2604.08598','offline retrieval task; no risk monitor described'),
('Luo2026ProtoDCS','ProtoDCS: Towards Robust and Efficient Open-Set Test-Time Adaptation for Vision-Language Models',2026,'https://arxiv.org/abs/2602.23653','OOD separation and prototype update; no sequential risk described'),
('Kim2025UltraLight','Ultra-Light Test-Time Adaptation for Vision--Language Models',2025,'https://arxiv.org/abs/2511.09101','logit-level accuracy/calibration framework; not a risk monitor in abstract'),
('Wang2026CATE','CATE: Consensus-aware calibration for test-time prompt tuning via energy anchoring',2026,'https://doi.org/10.1016/j.knosys.2026.115517','confidence-selection/entropy feedback loop; full text not audited so not behind verdict'),
('Ma2022MedicalCalibration','Test-Time Adaptation with Calibration of Medical Image Classification Nets for Label Distribution Shift',2022,'https://doi.org/10.1007/978-3-031-16437-8_30','DBLP metadata/title screen only; closed full text not acquired, unresolved adjacent medical calibration'),
('CRETTA_OpenReview_OdWkyqnkiS','CRETTA (title/author metadata unresolved)',2026,'https://openreview.net/forum?id=OdWkyqnkiS','browser challenge and HTTP403; indexed appendix snippets show confidence/ECE but not enough for verdict'),
('Lyu2025CUI','Conformal Uncertainty Indicator for Continual Test-Time Adaptation',2025,'https://arxiv.org/abs/2502.02998','abstract read; full-text assessment delegated to adjacent arm'),
('Wang2021Tent','Tent: Fully Test-Time Adaptation by Entropy Minimization',2021,'https://arxiv.org/abs/2006.10726','existing note and indexed method figures; citation graph attempt429; no new full-paper reread in this arm')]
for key,title,year,url,reason in abstracts:
 rows.append(dict(citation_key=key,title=title,year=year,url=url,reading_scope='2026-11-02 metadata/abstract or named indexed snippets only',decision='screened; not a verdict source',reason=reason,**{f'C{i}':'not determined from this reading' for i in range(1,6)}))

# A returned citation graph is a title-screening input, never a full-text read.
raw=json.loads(json.loads((E/'Bar2024ProtectedTTA-s2-trace.json').read_text())['body'])
normal=lambda s:re.sub(r'[^a-z0-9]','',s.lower())
known={normal(p['title']):p for p in catalog}
seen={normal(r['title']) for r in rows}
for relation in ['citations','references']:
 for p in raw[relation]:
  t=p['title']; norm=normal(t)
  if norm in seen: continue
  seen.add(norm)
  old=known.get(norm)
  key=old['key'] if old else 'S2_'+(p.get('paperId') or hashlib.sha256(t.encode()).hexdigest()[:12])
  close=bool(re.search(r'monitor|risk|shift|adapt|calibr|failure|confidence|uncertainty|conformal',t,re.I))
  rows.append(dict(citation_key=key,title=t,year=p.get('year',''),url=p.get('url',''),reading_scope='2026-11-02 title-only Semantic Scholar POEM '+relation,decision='related title; deferred or covered elsewhere' if close else 'excluded after title screen',reason='Title overlap only; not read for verdict in this arm' if close else 'Title concerns general method/background or unrelated task; no direct TTA monitor-failure claim evident from title',**{f'C{i}':'unknown; title only' for i in range(1,6)}))
with (A/'screened-papers.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

# Closest-work machine-readable matrix, matching the human table in report.md.
close=[]
table=(A/'report.md').read_text().split('## Close-work extraction')[1].split('## Tracing by round')[0]
for line in table.splitlines():
 if line.startswith('|') and not line.startswith('| Work') and not line.startswith('|---'):
  cols=[x.strip() for x in line.strip('|').split('|')]
  if len(cols)==5: close.append(dict(work_and_locations=cols[0],signal_and_adaptation=cols[1],data_and_shift=cols[2],metrics_sequential_frozen_cause=cols[3],labels_and_claim_overlap=cols[4]))
with (A/'closest-work.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(close[0]));w.writeheader();w.writerows(close)

# Append bibliographic API attempts to web queries exactly once.
with (A/'search-log.csv').open() as f: logs=list(csv.DictReader(f))
with (A/'api-search-log.csv').open() as f: logs+=list(csv.DictReader(f))
logs=[dict(t) for t in {tuple(r.items()):r for r in logs}.values()]
for r in logs:
 path=R/r['results_url']
 if 'search-' in path.name and path.exists():
  body=json.loads(path.read_text()); count=body.count('cite') if isinstance(body,str) else 0
  r['result_count']=str(count)+' returned records across batched queries; per-query total unavailable'
with (A/'search-log.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(logs[0]));w.writeheader();w.writerows(logs)

manifest=[]
for p in sorted(E.glob('*')):
 if p.is_file(): manifest.append({'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'recorded_date':'2026-11-02','note':'Downloaded/open-access primary PDF, extracted text, derived figure render or raw retrieval as indicated by filename. Legacy2404.16168 and2512.07390v1 copies retain01Nov retrieval; read afresh02Nov.'})
(A/'evidence-manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'detailed_or_abstract_rows':len(main)+len(abstracts),'total_screened_rows_including_POEM_title_trace':len(rows),'search_rows':len(logs),'new_metadata_records':len(new),'closest_rows':len(close),'evidence_files':len(manifest)}))

import csv,hashlib,json,pathlib,re
BASE=pathlib.Path(__file__).resolve().parent
ROOT=BASE.parents[1]
DATE='2026-11-02'
related={
 '01':'Han2026Exchangeability;Mahdiani2026ConformalTTA;Kivimaki2026CBPE;Lyu2025CUI;Cheng2026RollingCP;Ponduru2025TrustAdapt',
 '02':'Mahdiani2026ConformalTTA;Nguyen2025D3M;Prinster2025WATCH;Liu2026ConditionalMartingales',
 '04':'Stocco2022AdaptiveDrivingMonitor;Ahmed2026Dashboard;Feng2024Performativity',
 '05':'Kasa2024EACP;Rabanser2019FailingLoudly;Ginsberg2023Detectron',
 '06':'Lyu2025CUI;Ahmed2026Dashboard;Kim2025ClinicalMonitoring;Messaoud2004ResidualControl',
 '07':'Messaoud2004ResidualControl;Ong2015Masking',
 '08':'Lyu2025CUI;Amoukou2024SequentialHarmful;Ginsberg2023Detectron',
 '09':'Zhang2026PPRM;Messaoud2004ResidualControl;Kim2025ClinicalMonitoring;Lyu2025CUI',
 '10':'Ginsberg2023Detectron;Kivimaki2026CBPE;Goldwasser2020Rejectron',
 '11':'Amoukou2024SequentialHarmful;Nguyen2025D3M;Zhang2026PPRM;Kim2025ClinicalMonitoring',
 '12':'Lee2024AETTA;Ahmed2026Dashboard;Duan2026MonitorStaleness;Tang2026REFIT;Yuan2026UnderwaterBN',
 '13':'Tang2026REFIT;Yuan2026UnderwaterBN;Yuan2026OpenWorldUATR',
 '14':'Duan2026MonitorStaleness;Ponduru2025TrustAdapt;Liu2026ConditionalMartingales;Cheng2026RollingCP',
}
rows=[]
for path in sorted(BASE.glob('web-search-*.json')):
 data=json.loads(path.read_text());result=data['result'];text=result if isinstance(result,str) else json.dumps(result)
 n=len(re.findall(r'^.{5,200} \(https?://[^)]+\)$',text,re.M));batch=path.stem.rsplit('-',1)[1]
 for query in data['queries']:
  rows.append(dict(date=DATE,source='web.run ranked web-search index',query=query,result_count=f'Per-query total not exposed; {n} ranked source records in batched response',results_url=str(path.relative_to(ROOT)),relevant_papers=related.get(batch,''),blocked_notes='Search results are ranked/truncated; not an exhaustive database list. Primary full-text blocks recorded separately.'))
manual_queries=[
 ('"7602585" pdf Mahdiani','Mahdiani2026ConformalTTA','SSRN indexed primary abstract only; full-text403'),
 ('"Diagnosing and repairing" "conformal" pdf','Mahdiani2026ConformalTTA','No alternate full text located'),
 ('"Mohammad Reza Mahdiani" "test-time" github','Mahdiani2026ConformalTTA','No author-hosted full text located'),
 ('"Performance Estimation in Binary Classification Using Calibrated Confidence"','Kivimaki2026CBPE','Official journal and author institution identified'),
]
for q,keys,note in manual_queries:rows.append(dict(date=DATE,source='web.run ranked web-search index',query=q,result_count='Per-query total not exposed',results_url='https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7602585' if 'Mahdiani' in keys else 'https://link.springer.com/article/10.1007/s10994-025-06970-3',relevant_papers=keys,blocked_notes=note+'; batch03 raw result not saved; query/outcome transcribed from tool call.'))
for record in json.loads((BASE/'retrieval-manifest.json').read_text()):
 rows.append(dict(date=DATE,source='Direct primary-source GET via urllib',query='GET '+record['url'],result_count=str(record.get('status','blocked')),results_url=record.get('path',record['url']),relevant_papers=record['key'],blocked_notes=record.get('error','PDF retrieved and text extracted;download is not full-paper reading.')))
direct=[
 ('https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7602585','Mahdiani2026ConformalTTA','403 Forbidden'),
 ('https://openreview.net/forum?id=ev9OcnAHOI','Lyu2025CUI','Browser challenge;withdrawal/status not verified'),
 ('https://hdl.handle.net/10419/22573','Messaoud2004ResidualControl','Web-tool failed;fullPDFretrieved fromEconStor'),
 ('https://www.econstor.eu/bitstream/10419/22573/1/tr60-04.pdf','Messaoud2004ResidualControl','200;PDFandtext saved'),
 ('https://arxiv.org/pdf/2212.02742','Ginsberg2023Detectron','200;PDFandtext saved'),
 ('https://arxiv.org/pdf/2505.05295','Kivimaki2026CBPE','200;preprintPDFsaved;official2026journal metadata separately checked'),
 ('https://arxiv.org/abs/2606.15980','Duan2026MonitorStaleness','200;v1June14/v2June18,2026;acceptance unverified'),
 ('https://arxiv.org/pdf/2606.15980','Duan2026MonitorStaleness','200;v2PDFandtext saved'),
 ('https://arxiv.org/pdf/2610.08991','Tang2026REFIT','200;detailed reading by citation agent'),
 ('https://nannyml.readthedocs.io/en/stable/how_it_works/performance_estimation.html','NannyML2026CBPEDocs','200;Assumptions/Limitations and multiclass formula read;HTMLsaved'),
 ('https://proceedings.mlr.press/v238/feng24b.html','Feng2024Performativity','Official metadata verified'),
 ('https://proceedings.mlr.press/v267/prinster25a.html','Prinster2025WATCH','Official metadata verified'),
 ('https://proceedings.mlr.press/v306/zhang26g.html','Zhang2026PPRM','Official ICML2026metadata verified'),
 ('https://pmc.ncbi.nlm.nih.gov/articles/PMC12278811/','Kim2025ClinicalMonitoring','Primary methods/results/discussion excerpts;HTMLsaved'),
 ('https://pmc.ncbi.nlm.nih.gov/articles/PMC9786604/','Stocco2022AdaptiveDrivingMonitor','Primary methods/challenges/discussion excerpts;HTMLsaved'),
 ('https://ijsrcseit.com/home/article/view/CSEIT25113445','Ponduru2025TrustAdapt','403 Forbidden;RePEc abstract only'),
 ('https://ijsrcseit.com/home/article/download/CSEIT25113445/CSEIT25113445','Ponduru2025TrustAdapt','403 Forbidden'),
]
for url,key,note in direct:rows.append(dict(date=DATE,source='Primary-source web.open or curl retrieval',query='GET '+url,result_count='Not a search',results_url=url,relevant_papers=key,blocked_notes=note))
with (BASE/'search-log.csv').open('w',newline='') as f:
 writer=csv.DictWriter(f,fieldnames=['date','source','query','result_count','results_url','relevant_papers','blocked_notes']);writer.writeheader();writer.writerows(rows)

fields=['citation_key','title','year','url','reading_scope','decision','reason','C1','C2','C3','C4','C5']
screens=[]
def screen(key,title,year,url,scope,decision,reason,c1='',c2='',c3='',c4='',c5=''):
 screens.append(dict(zip(fields,[key,title,year,url,scope,decision,reason,c1,c2,c3,c4,c5])))
screen('Han2026Exchangeability','The Premise Is the Problem: Exchangeability Failure in Self-Monitored Test-Time Adaptation',2026,'https://arxiv.org/abs/2610.07038','Full relevant methods§3,results§4–6,AppendixLpp45–49Tables48–51;proofs not audited','Include close','Adaptation absorbs sustained shifts;frozen residual sentinel retains signal','No exact classification/Tent/Dirichlet comparison','Different cause:Kalman fitting and dependence','No confidence minimization','Direct general self-masking precedent','Independent frozen sentinel;needs observed outcomes')
screen('Messaoud2004ResidualControl','Monitoring of the BTA Deep Hole Drilling Process Using Residual Control Charts',2004,'https://hdl.handle.net/10419/22573','§§1–5;§4p6;§5.4p13Fig6;appendix mapped','Include foundational','Adaptive parameter estimates absorb changes and mask future residual alarms','','','Not entropy/confidence','Explicit masking/parameter-adaptation problem','Lagged/independent residual design precedent;not model-risk guarantee')
screen('Kivimaki2026CBPE','Performance Estimation in Binary Classification Using Calibrated Confidence',2026,'https://link.springer.com/article/10.1007/s10994-025-06970-3','Published primaryHTML;arxivPDF§§3–6,Theorem1,Table2','Include close','Confidence-to-performance guarantees require calibration','','','Direct calibration dependency;conditional algebra anticipates bias','Does not experiment with adaptation','Mandatory confidence baseline;not independent signal')
screen('NannyML2026CBPEDocs','Estimation of Performance of the Monitored Model','undated','https://nannyml.readthedocs.io/en/stable/how_it_works/performance_estimation.html','Multiclass formula;Assumptions/Limitations;calibration appendix','Include official nonpaper','Explicit calibration/unseen-region/concept-shift limits','','','Uncalibrated confidence invalidates estimate','No TTA study','CBPE/DLE practical baseline definitions')
screen('Amoukou2024SequentialHarmful','Sequential Harmful Shift Detection Without Labels',2024,'https://proceedings.neurips.cc/paper_files/paper/2024/hash/e9721921b799b6ea98d37f9e77f1a7fe-Abstract-Conference.html','§§2–5,Assumption4.1,Theorem4.2,AppendicesA/D/E','Include close','Separately learned error estimator drives sequential alarm','Fixed model;noTTA differential','','Proxy quality affects power','No model-updating mechanism','Existing label-free sequential separate-estimator monitor')
screen('Nguyen2025D3M','Reliably detecting model failures in deployment without labels',2025,'https://proceedings.neurips.cc/paper_files/paper/2025/hash/0bb251eba663f0345c0929f5bbbfb6dc-Abstract-Conference.html','§§2,3,5;AppendixAsetup/TheoremsA3,A5,A6','Include close','Bayesian last-layer disagreement monitor','No TTA or corruption+skew','','Not confidence-means-risk','No changing feature extractor','Useful existing checker;batch test not anytime alarm')
screen('Ginsberg2023Detectron','A Learning Based Hypothesis Test for Harmful Covariate Shift',2023,'https://arxiv.org/abs/2212.02742','§3Algorithm1;§4Table1;§5;AppendixA/C/I map','Include close','Constrained external classifiers test disagreement on unlabeled target','No TTA differential','','','Checker can fail from underspecified class;not adaptation causal','Existing independent checker;source access+retraining;batch test')
screen('Prinster2025WATCH','WATCH: Adaptive Monitoring for AI Deployments via Weighted-Conformal Martingales',2025,'https://proceedings.mlr.press/v267/prinster25a.html','§§2–4,Theorem3.1,Figure3Table1,AppendixC/D6','Include close','Paired risk/conformity and input-shift monitors','No Tent/Dirichlet','','','Adaptive set weighting not classifier-learning failure','Main signal requires outcome labels;X-CTM alone detects input shift')
screen('Lyu2025CUI','Conformal Uncertainty Indicator for Continual Test-Time Adaptation',2025,'https://arxiv.org/abs/2502.02998','Arxivv1§§3–5,Algorithm1,Table2,Figure2;OpenReviewforumblocked','Include close','Source/current joint logits repair unreliable uncertainty','NoDirichlet/sequential missed-risk study','No entropy-vs-BN isolation','Error accumulation undermines raw uncertainty','Explicit changing-model signal unreliability','Existing label-free source-calibration indicator;no alarm-power guarantee')
screen('Kasa2024EACP','Adapting Prediction Sets to Distribution Shifts Without Labels',2024,'https://arxiv.org/abs/2406.01416','§§2–4,Algorithm1,Tables1–3,AppendixB/C/D map','Include close','Entropy-scaled conformal sets plusETA','Noclass-prior/missed-alarm comparison','No isolation','Entropy changes prediction-set scaling','No universal failure claim','Existing label-free uncertainty correction;not risk alarm')
screen('Zhang2026PPRM','Prediction-Powered Risk Monitoring of Deployed Models for Detecting Harmful Distribution Shifts',2026,'https://proceedings.mlr.press/v306/zhang26g.html','§§2–5,Fig2;AppendixB;§3.1nt>0','Include close','True-label residual correction avoids surrogate-quality assumptions','SchirmerURM misses under corruption;static model notTTA/skew','','','NoTTA-self-masking experiment','Semi-supervised alternative;cannot calllabel-free')
screen('Feng2024Performativity','Monitoring machine learning-based risk prediction algorithms in the presence of performativity',2024,'https://proceedings.mlr.press/v238/feng24b.html','§§2–6,Fig2–4;appendixmodel-updateexperiments','Include adjacent','Clinical feedback and model updates interact with CUSUM','NoTTA/image/skew','','','Feedback-aware monitoring prior;different mechanism','Requires clinical outcomes/ignorability')
screen('Mahdiani2026ConformalTTA','Diagnosing and repairing the conformal coverage guarantee of test-time-adapted image classifiers',2026,'https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7602585','Indexedprimaryabstract/referencesonly;landing/PDF403','Unresolved close:blocked','Abstract describes matchedBNcausecontrol+TTAconfidencecorruption','NoDirichletorSchirmercomparisoninabstract','Potentialstrongpredecessor;fulltextrequired','Potentialstrongpredecessor;fulltextrequired','Potentialsameendogenousconfidenceidea','Abstractclaimspredict-before-updatefix;fulltextrequired')
screen('Duan2026MonitorStaleness','Do Activation Monitors Survive Model Updates? Benchmarking, Predicting, and Repairing Activation-Monitor Staleness',2026,'https://arxiv.org/abs/2606.15980','v2methods,Tables3–5,mechanism/repair/discussion/limitations,pp2–7','Include adjacent','FrozenactivationprobesstaleafterLoRA;label-freerealignment','Noimagecorruptions/Tent/skew','Differentmechanism:representationgeometry','Notconfidenceproxy','Directmodel-updates-change-monitorsignal','Existinglabel-freemonitorrepair;notsequentialriskpower')
screen('Rabanser2019FailingLoudly','Failing Loudly: An Empirical Study of Methods for Detecting Dataset Shift',2019,'https://papers.neurips.cc/paper_files/paper/2019/hash/846c260d715e5b854ffad5f70a516c88-Abstract.html','Officialabstract/metadataonly','Screen adjacent','Frozen-featuretwo-samplemonitoringknown;notverdictcritical','','','','','Existinginput-shiftsentinel;harmnotidentical')
screen('Stocco2022AdaptiveDrivingMonitor','Confidence-driven weighted retraining for predicting safety-critical failures in autonomous driving systems',2022,'https://pmc.ncbi.nlm.nih.gov/articles/PMC9786604/','Primarymethods§§3–4anddiscussionexcerpts','Screen adjacent','AdaptiveAE-monitorlearnsnominaldata;couplingwarning','','','','Architecture-levelcouplingwarning','Separatebehaviourmonitorwithuncertainty/lateraldeviation')
screen('Kim2025ClinicalMonitoring','Monitoring strategies for continuous evaluation of deployed clinical prediction models',2025,'https://pmc.ncbi.nlm.nih.gov/articles/PMC12278811/','Primarymethods/results/figures/discussionexcerpts;PubMedmetadata','Screen adjacent','Adherence/samplingweightingrepairfeedbackbiasedmonitoring','','','','Deployment-inducedlabelfeedback,notconfidenceTTA','Requiresoutcomes/treatmentassumptions')
screen('Tang2026REFIT','REFIT: Recognize, Fix, and Test Wearable Sensor Placement Shifts without Labels',2026,'https://arxiv.org/abs/2610.08991','PDFmetadata/introonlyhere;detailedreadingbycitationagent','Refer other agent','ATCverifiesinput/BNcorrection','','','','','Notindependentfromadaptedconfidence;noentropylearning')
screen('Yuan2026UnderwaterBN','Source-Free Domain Adaptation for Underwater Acoustic Target Recognition: A Strong Batch-Normalization Statistics Baseline Under Cross-Water-Area Shift',2026,'https://www.preprints.org/manuscript/202609.1126','Primaryindexedfulltext§§3.6,4.3,4.6;notfullpaperread','Refer TTA agent','Entropy-selectedTentcollapseandBNcontrol','Collapsedtwo-classoffline;noSchirmer','Controlsreportedbutnotalarmcomparison','Confidencecollapsebreaksselection','Adjacentproxyself-optimization','Noindependentalarm')
screen('Ponduru2025TrustAdapt','TRUST-ADAPT: Risk-Gated Reversible Test-Time Learning with Conformal Shift Evidence and Selective Memory',2025,'https://ideas.repec.org/a/jbh/ijsrcs/v11y2025i2id2156.html','RePEcbibliographicabstractonly;publisherpage/PDF403','Unresolved close:blocked','Frozen-sourceconformalHoeffdinggate+rollbackinabstract','','','','Architecturepriorartlead','Potentialfrozensentinelprecedent;fulltextrequired')
screen('Cheng2026RollingCP','Rolling Conformal Prediction in Sequential Model Training',2026,'https://arxiv.org/abs/2609.26951','Primaryarxivabstractonly','Screen adjacent;notverdictbasis','Predict-before-updateCPrequiresobserved(X,Y)stream','','','','Showsmodelupdatescanbehandledunderexchangeability','Notlabel-freeharmmonitor')
screen('Liu2026ConditionalMartingales','Monitoring for Shifts at Unknown Times: Parameter-Free Conditional Conformal Martingales',2026,'https://arxiv.org/abs/2610.17343','Primaryarxivabstractonly','Screen adjacent;notverdictbasis','Fixedreferenceavoidscontamination;portfoliochangepointtest','','','','NoTTAclassifiermechanism','Existingsequentialdetector;detectionrequiresalternativevisibleinsignal')
screen('Goldwasser2020Rejectron','Beyond Perturbations: Learning Guarantees with Arbitrary Adversarial Test Examples',2020,'https://papers.neurips.cc/paper_files/paper/2020/file/b6c8cf4c587f2ead0c08955ee6e2502b-Review.html','Primaryreview+DetectronAppendixAaccount;originalnotfullyread','Screen foundational;notverdictbasis','PQ-learningdisagreementselectiveclassifier','','','','','Abstentionguaranteesunderstrongrealizability/ERMassumptions')
screen('AnnotationEfficientATTA2025','Annotation-Efficient Active Test-Time Adaptation with Conformal Prediction',2025,'https://arxiv.org/abs/2509.25692','Title/abstractsearchresultonly','Exclude directC5fix','Activeannotationuseslabels;notlabel-free','','','','','Excludedstrictlabel-freefix')
screen('Ong2015Masking','A Control Chart Based on Cluster-Regression Adjustment for Retrospective Monitoring of Individual Characteristics',2015,'https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0125835','Primaryabstract/maskingdefinitiononly','Screen foundational','Outliercontaminationmasksoutliers;differentfromonlineTTA','','','','Broadmaskingprecedent','Notadaptationriskfix')
screen('Yuan2026OpenWorldUATR','Open-World Source-Free Domain Adaptation for Underwater Acoustic Target Recognition Under Naturally Contaminated Target Streams: Adaptation Survives, Post-Hoc Rejection Fails',2026,'https://www.preprints.org/manuscript/202609.1683','Primaryindexedmethod/calibrationexcerptsonly','Refer TTA agent','Open-setrejectionconfidencefailsalongsideadaptation','','','Confidenceinversion/rejectionfailure','AdjacentnotSchirmer','Noindependentalarm')
with (BASE/'screened-papers.csv').open('w',newline='') as f:
 writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(screens)
manifest=[]
for p in sorted((ROOT/'evidence'/'adjacent_monitors').glob('*')):
 if p.is_file():manifest.append({'date':DATE,'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'note':'Access/download alone does not mean full reading;see screened-papers.csv. HanPDF/textcopiedfrom2026-11-01evidenceandfreshlyread.'})
(BASE/'evidence-manifest.json').write_text(json.dumps(manifest,indent=2))
report=BASE/'report.md';s=report.read_text();s=s.replace('TableShift15datasets/synthetic','TableShift(eight of15datasets evaluated)/synthetic').replace('one96-step','one 96-step').replace('magnitude1','magnitude 1').replace('magnitude3','magnitude 3').replace('frozen-signal','frozen signal').replace('independent-sentinel','independent sentinel')
report.write_text(s)
print(json.dumps({'search_log_rows':len(rows),'screened_records':len(screens),'evidence_files':len(manifest)}))

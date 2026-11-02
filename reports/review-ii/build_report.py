from pathlib import Path
import json, re, textwrap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from docx import Document
from docx.shared import Inches as DI, Pt as DP, RGBColor as DC
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
ROOT = PROJECT.parent
ASSETS = HERE/'assets'
ASSETS.mkdir(exist_ok=True)
TITLE = 'Shift-Aware Test-Time Adaptation via Dynamic Adaptation Policy Selection'
TEAM = [('Anuj Sharma','23BDS0164'),('Shaurya Garg','23BDS0161'),('Rohit Phaniram Sakamuri','23BDS0051')]
BLACK = RGBColor(0,0,0)
metrics = [
 ['Frozen source model','76.4 ± 1.0%','—','—'],
 ['Always update normalization','74.8 ± 1.8%','−1.6 pp','31%'],
 ['Concentration-only gate','77.3 ± 1.1%','+0.9 pp','15%'],
 ['Three-feature gate','77.9 ± 0.9%','+1.5 pp','11%'],
]
refs = [
 '[1] Li et al. Revisiting Batch Normalization For Practical Domain Adaptation. arXiv:1603.04779, 2016. https://arxiv.org/abs/1603.04779',
 '[2] Wang et al. Tent: Fully Test-Time Adaptation by Entropy Minimization. ICLR, 2021. https://arxiv.org/abs/2006.10726',
 '[3] Gong et al. NOTE: Robust Continual Test-time Adaptation Against Temporal Correlation. NeurIPS 35, 2022. https://arxiv.org/abs/2208.05117',
 '[4] Lim et al. TTN: A Domain-Shift Aware Batch Normalization in Test-Time Adaptation. ICLR, 2023. https://arxiv.org/abs/2302.05155',
 '[5] Vianna et al. Channel-Selective Normalization for Label-Shift Robust Test-Time Adaptation. PMLR 274:514–533, 2025. https://proceedings.mlr.press/v274/vianna25a.html',
 '[6] Danilowski et al. MORPHEUS: Meta Test-Time Adaptation via Neural Collapse Geometry. ICLR Test-Time Updates Workshop, 2026. https://openreview.net/forum?id=YfyApJH1Rj',
 '[7] Jhawar and Wang. When is Test-Time Adaptation Identifiable From Unlabeled Evidence? arXiv:2609.11235, 2026. https://arxiv.org/abs/2609.11235',
 '[8] Sreeram, Kwon and Mascolo. Tempora: Characterising the Time-Contingent Utility of Online Test-Time Adaptation. ICML, PMLR 306:115420–115456, 2026. https://proceedings.mlr.press/v306/sreeram26a.html',
]
survey = [
 ['AdaBN [1]','Source-to-target normalization statistics','Statistics-only update baseline'],
 ['Tent [2]','Entropy-based test-time adaptation','Uncertainty as adaptation evidence'],
 ['NOTE / TTN [3,4]','Batch reliability; shift-aware normalization','Control batch-composition effects'],
 ['Channel-selective norm. [5]','Robustness to label and covariate shifts','Close normalization comparator'],
 ['MORPHEUS / identifiability [6,7]','Predict when adaptation will help','Close action-selection prior work'],
 ['Tempora [8]','Time-contingent adaptation utility','Measure the complete inference route'],
]
splits = [['Source training','900','Fit encoder, head and source moments'],['Auxiliary training','400','Learn selectors; two 200-image pools'],['Calibration','200','Choose policy thresholds'],['Final evaluation','297','Unseen original image identities']]

sections = [
 ('Summary of the Project', [
  ('Abstract', 'We implemented a selective test-time normalization approach that decides whether to retain the frozen source model or update its normalization statistics. The controller uses three signals from an unlabeled support batch: predicted-class concentration, mean predictive entropy and displacement of its features from stored source statistics. The classifier weights remain fixed at deployment. Across five seeds, the three-feature gate achieved 77.9 ± 0.9% accuracy, compared with 76.4 ± 1.0% for SOURCE and 77.3 ± 1.1% for a concentration-only gate. It improved mean accuracy by 1.5 percentage points over SOURCE and reduced harmful-update episodes from 31% for unconditional normalization to 11%. The improvement is modest, and adaptation still degraded performance in some conditions. Continuing work examines unseen corruption families, class imbalance and complete inference cost.'),
  ('Objective', 'Models deployed under changes in illumination, noise, contrast, occlusion or class proportions can lose accuracy. Normalization updates can help, but an unrepresentative batch can also make predictions worse. Our objective is to apply an update only when available evidence predicts a benefit, while retaining the source model as a valid action. We restricted the approach to two actions so that the adaptation decision can be examined independently of changes in classifier capacity.'),
  ('Current status', 'We completed the frozen and unconditional-normalization baselines, the concentration-only gate, the three-feature gate and the five-seed comparison. We are continuing the analysis of the remaining harmful updates, the generalization of the decision rule and its total computation cost.'),
 ]),
 ('Review: Background Survey', [
  ('Foundations', 'AdaBN established normalization-statistics adaptation as a lightweight domain-adaptation mechanism [1]. Tent showed the value of entropy-driven test-time adaptation [2]. NOTE and TTN make batch reliability and normalization behavior important design considerations [3,4]. These methods motivated our source and normalization baselines, and the use of uncertainty as observable evidence rather than an assumption that every batch should be adapted.'),
  ('Closest work', 'Channel-selective normalization directly addresses sensitivity to label and covariate shifts [5]. MORPHEUS predicts adaptation performance using source-model uncertainty and representations [6]. Work on identifiability examines whether unlabeled evidence supports adaptation decisions [7]. Tempora makes the computation cost of adaptation part of the evaluation [8]. Together, these studies limit any broad novelty claim: choosing whether to adapt, using uncertainty, and handling class imbalance are established directions. Our narrower question concerns the incremental decision value of three inexpensive summaries and their behavior under ambiguous predicted concentration.'),
 ]),
 ('Summary of Gap Analysis', [
  ('Observed limitation', 'Predicted-class concentration is the fraction of inputs assigned to the most frequent predicted class. A genuinely class-concentrated batch and a balanced batch whose corrupted predictions collapse to one class can both have high concentration. A concentration-only rule cannot directly distinguish those situations. Their optimal normalization decisions may differ, so concentration is useful evidence but does not identify the cause of the shift.'),
  ('Question being studied', 'Does adding predictive entropy and source-relative feature displacement improve normalization decisions over concentration alone, and does that improvement persist for unseen corruption families and class imbalance? The completed five-seed comparison addresses the first part. The matched-concentration and generalization analyses remain continuing work. The candidate contribution is a controlled empirical characterization and a small interpretable gate; novelty still needs to be established against the closest prior evaluations [4–7].'),
 ]),
 ('Proposed Idea', [
  ('Inputs and outputs', 'The input is an unlabeled support batch and the stored source model. One source inference produces class probabilities and feature vectors. The controller computes concentration, entropy and source-relative feature displacement, predicts the benefit of updating, and outputs SOURCE or NORMALIZE. SOURCE retains stored normalization moments. NORMALIZE estimates replacement moments from support and freezes them for a separate query batch. Encoder and classifier weights remain fixed.'),
  ('Three signals', 'Concentration is the largest predicted-class count divided by batch size. Mean entropy averages the uncertainty of each probability vector; low entropy can still accompany confident errors. Feature displacement averages the absolute difference between support and source feature means, divided by source-feature standard deviations. In symbols, d(B) = mean_j |mu_B,j − mu_S,j| / sqrt(var_S,j + epsilon). Source moments come only from source-training inputs. Both corruption and class proportions can change displacement; it is not a causal shift label.'),
  ('Benefit predictor', 'For an auxiliary-development episode, both actions start from the same source state. Their query errors define Delta = error_SOURCE − error_NORMALIZE. Positive Delta indicates a beneficial update. The approach specifies a depth-two regression tree over the three signals, with at most four leaves. NORMALIZE is chosen when predicted Delta exceeds a separately calibrated margin; otherwise SOURCE is retained. The rule is an empirical safeguard, not a guarantee that every accepted update is safe.'),
 ]),
 ('Flow of the Proposed Work', [
  ('Development flow', 'Train the source model and store source moments. Construct auxiliary support/query episodes with controlled corruptions and class proportions. Extract the three support signals. Evaluate both actions from equivalent initial states and measure query errors. Fit the benefit predictor, choose its margin on separate calibration data, and freeze the policy before evaluation. Query labels supply development targets and evaluation measurements; they are excluded from runtime gate inputs.'),
  ('Deployment flow', 'Unlabeled support batch → frozen source inference → concentration, entropy and displacement → predicted update benefit → SOURCE or NORMALIZE → prediction on a disjoint query batch. Support-derived statistics remain fixed while the query batch is scored. Each episodic comparison begins from the same source state. A full-network implementation may require an additional adapted pass, so runtime will be measured from the complete execution path.'),
 ]),
 ('Dataset Used and Preprocessing', [
  ('Recorded development data', 'The local development implementation used scikit-learn’s handwritten-digits dataset: 1,797 grayscale images, ten digit classes and 8 × 8 pixels per image. Each input has 64 pixel features. Pixel values were divided by 16. Source-feature moments were fitted only on source-training images. Documentation: https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html. The local setup below is distinct from the five-seed result summary obtained on the other system; its complete dataset, backbone and split manifest remains to be consolidated.'),
  ('Shift construction and exploratory analysis', 'The development pipeline inspected input dimensions, pixel ranges, class composition and source performance. Conditions included clean inputs, noise, brightness reduction, blur and translation, with contrast and occlusion reserved as primary held-out families. Corruptions had two severities. Support batches contained 16 or 32 inputs, and query batches contained 32 draws. Class composition was balanced or approximately 75% dominated by one class. Support and query original identities were separated within each episode.'),
  ('Episode accounting', 'The earlier local diagnostic used three source/split repeats with 640 episode definitions each: 288 auxiliary-training, 144 calibration and 208 evaluation episodes. Of the evaluation episodes, 64 contained the primary held-out families. These 1,920 definitions reused a finite dataset, and some concentrated batches repeated image draws. They are development evidence, not 1,920 independent datasets and not the seed count for the current five-seed results.'),
 ]),
 ('Detailed Work and Finished Implementation', [
  ('Source and action implementation', 'We implemented the development pipeline in Python with NumPy, SciPy and scikit-learn. It uses a 32-unit ReLU encoder and a multinomial logistic-regression head over source-normalized hidden features. The source model and stored moments are saved before adaptation. SOURCE uses the stored moments. NORMALIZE estimates support moments and freezes them during query prediction. The local encoder used L-BFGS with alpha 0.01 and a 250-iteration limit; the head used C = 1 and a 500-iteration limit. Convergence warnings were retained.'),
  ('Gates completed', 'We implemented the concentration-only controller and the three-feature controller. The latter adds mean entropy and feature displacement to the update decision. We retained an unchanged-source action, separated support-based evidence from query scoring, and compared the policies across five seeds. The main four-policy evaluation measures the choice to update normalization, rather than introducing a larger classifier or additional supervised learning at deployment.'),
  ('Finished work', 'Completed components include source fitting, source-statistic storage, corruption and class-composition episode construction, frozen-source and unconditional-normalization baselines, concentration-only gating, three-feature gating, five-seed accuracy aggregation and harmful-update analysis. The local records also preserve predictions, action outcomes, identities, features, code and artifact hashes. The three-feature evaluation was completed on the other system; its supplied aggregate results are used in this review.'),
  ('Reproducibility', 'Local files include train_core.py, core_model.py, generate_outcomes.py, analyze_diagnostic.py, prior_gate_analysis.py, outcomes.npz and run_manifest.json. The local numerical environment was Python 3.13.9, NumPy 2.2.6, SciPy 1.17.1 and scikit-learn 1.8.0. Subsequent research commands used uv with the existing environment. Importing the current gate implementation and seed-level run manifests from the other system remains part of consolidating the research package.'),
 ]),
 ('Performance Evaluation: Finished Work', [
  ('Metric definitions', 'Accuracy is the proportion of correct predictions; higher is better. Results are reported as mean ± standard deviation across five seeds. Standard deviation describes variability across seeds, not a confidence interval or proof of significance. Gain over SOURCE is a difference in mean accuracy, expressed in percentage points. Harmful-update episodes are the percentage of all evaluation episodes where a method applied normalization and produced lower accuracy than SOURCE. The denominator includes every evaluation episode, not only episodes where the policy updated.'),
  ('Five-seed results', 'The three-feature gate improved average accuracy by 1.5 percentage points over the frozen model and 0.6 points over the concentration-only gate. It reduced harmful updates, although adaptation still degraded performance in some conditions. Further work will examine unseen corruption families, class imbalance and total inference cost.'),
  ('Magnitude of improvement', 'Harmful-update frequency decreased from 31% with unconditional normalization to 15% with concentration-only gating and 11% with the three-feature gate. The last comparison is a reduction of 4 percentage points; the reduction from always updating is 20 points. These results are encouraging enough to justify further investigation, but do not establish a universal safety property. The remaining harmful updates are a concrete target for improvement.'),
 ]),
 ('Results and Discussion', [
  ('Interpretation', 'Unconditional normalization performed worse than SOURCE in aggregate and had the largest accuracy standard deviation. Both selective policies improved mean accuracy, and the three-feature gate had the highest mean among the evaluated approaches. The extra entropy and displacement signals produced a modest 0.6-point gain over concentration alone. The results support conditional updating in the completed evaluation, while leaving open whether the same gain transfers to different shifts.'),
  ('Reliability and evidence limits', 'A higher mean accuracy can coexist with degradation on individual conditions. Reporting harmful updates makes this trade-off visible. Five-seed standard deviations also do not establish the statistical significance of the difference between gates: paired seed-level and episode-level analysis remains necessary. The aggregate table does not identify which corruption, severity or class-composition conditions account for the remaining 11% of harmful updates.'),
  ('Cost remains open', 'A small gate is inexpensive by itself, but complete execution includes source inference, feature summaries, support statistics and any adapted forward pass. We have not assigned a latency improvement to the five-seed results. A complete timing and memory analysis will determine whether the accuracy gain is worthwhile under a deployment budget [8].'),
 ]),
 ('Scope of the Work', [
  ('Completed scope', 'The completed work is an implementation and initial five-seed evaluation of a two-action normalization controller. It uses unlabeled support evidence, a frozen classifier and three summary signals. The earlier local development work supplies identity-aware episode construction, counterfactual action outcomes and analysis utilities. The gate reduces the frequency of harmful updates in the current evaluation, but does not eliminate them.'),
  ('Limits', 'The report does not claim completed evaluation on CIFAR-10-C, ImageNet-C, DomainNet or WILDS. These appeared in the original proposal and require documented runs before being reported as results. Faithful reference comparisons, unseen corruption families, class imbalance, continual streams and complete computation cost remain open. Concentration is a prediction statistic, entropy can be low for wrong answers, and displacement does not identify the cause of a shift.'),
 ]),
 ('Conclusion and Future Work', [
  ('Conclusion', 'We completed the implementation and initial evaluation of a selective test-time normalization approach. The three-feature gate achieved 77.9 ± 0.9% accuracy across five seeds, improving mean accuracy by 1.5 percentage points over SOURCE and reducing harmful-update episodes to 11%. The gain over the concentration-only gate was 0.6 points. Adaptation still harmed some conditions, so work is continuing to improve the decision rule and evaluate its practical value.'),
  ('Next experiments', 'We will inspect harmful updates by corruption, severity and class composition; compare single-feature gates with the three-feature gate; hold out complete corruption families and dominant-class identities; and examine matched-concentration batches with different underlying class composition. Matching rules and thresholds will be fixed on development data. Full-condition results and matching coverage will be retained.'),
  ('Implementation and evaluation priorities', 'We will consolidate the external code and seed-level manifests, test a more conservative calibrated update margin, and measure complete inference time and memory. The objective is to reduce harmful decisions while retaining accuracy, rather than assume a more complex controller is automatically better. After these checks, a documented image-benchmark comparison with faithful normalization baselines will establish the next scope of the study.'),
 ]),
 ('References', [('Sources', '\n\n'.join(refs))]),
]

# Charts use exactly the user-reported five-seed aggregates.
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'text.color':'black','axes.labelcolor':'black','xtick.color':'black','ytick.color':'black'})
fig, axs = plt.subplots(1,2,figsize=(10,3.2),gridspec_kw={'width_ratios':[1.6,1]})
labels=['SOURCE','Always norm.','Concentration','Three-feature']
means=[76.4,74.8,77.3,77.9]; sd=[1.0,1.8,1.1,0.9]
bars=axs[0].barh(labels,means,xerr=sd,color=['white','.8','.6','.35'],edgecolor='black',capsize=3)
axs[0].set_xlim(0,100);axs[0].set_xlabel('Accuracy (%) — error bars: SD over five seeds');axs[0].invert_yaxis()
for bar,m,s in zip(bars,means,sd): axs[0].text(m+s+1,bar.get_y()+bar.get_height()/2,f'{m:.1f}',va='center',fontsize=9)
axs[1].bar(['Always\nnorm.','Concentration','Three-\nfeature'],[31,15,11],color=['.8','.6','.35'],edgecolor='black')
axs[1].set_ylim(0,40);axs[1].set_ylabel('Harmful-update episodes (%)')
for i,v in enumerate([31,15,11]):axs[1].text(i,v+1,str(v)+'%',ha='center')
for ax in axs:ax.spines[['top','right']].set_visible(False)
fig.tight_layout();fig.savefig(ASSETS/'five_seed_results.png',dpi=200,bbox_inches='tight');plt.close(fig)

# Reuse the supplied presentation's slide size, masters and layouts.
prs=Presentation(ROOT/'Review2.pptx')
for sid in list(prs.slides._sldIdLst):
 prs.part.drop_rel(sid.rId);prs.slides._sldIdLst.remove(sid)
def textbox(slide,x,y,w,h,text,size=19,bold=False,align=None):
 box=slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h));tf=box.text_frame;tf.word_wrap=True
 tf.margin_left=tf.margin_right=Inches(.03);tf.margin_top=tf.margin_bottom=Inches(.02)
 for i,line in enumerate(text.split('\n')):
  p=tf.paragraphs[0] if i==0 else tf.add_paragraph();p.text=line;p.space_after=Pt(8)
  if align is not None:p.alignment=align
  for r in p.runs:r.font.name='Calibri';r.font.size=Pt(size);r.font.bold=bold;r.font.color.rgb=BLACK
 return box
def slide(title,section):
 s=prs.slides.add_slide(prs.slide_layouts[1])
 for sh in list(s.shapes):
  if sh.is_placeholder and sh.placeholder_format.idx!=0:sh._element.getparent().remove(sh._element)
 t=s.shapes.title;t.left=Inches(.5);t.top=Inches(.3);t.width=Inches(9);t.height=Inches(1.1)
 t.text=title
 for p in t.text_frame.paragraphs:
  for r in p.runs:r.font.name='Calibri';r.font.size=Pt(29);r.font.color.rgb=BLACK
 textbox(s,.5,7.08,8.3,.2,'Review II  |  Shift-Aware Test-Time Adaptation',size=9)
 textbox(s,9,7.08,.4,.2,str(len(prs.slides)),size=9,align=PP_ALIGN.RIGHT)
 if section is not None:s.notes_slide.notes_text_frame.text='\n\n'.join(h+'\n'+p for h,p in sections[section][1])
 return s
def bullets(s,items,y=1.6,size=21):
 for item in items:
  lines=max(1,len(textwrap.wrap(item,width=int(76*19/size))))
  h=max(.65,lines*size/72*1.22+.18)
  textbox(s,.65,y,8.75,h,'•  '+item,size=size);y+=h+.17
def table(s,headers,rows,x=.5,y=1.6,w=9,h=3.5,widths=None,size=15):
 tab=s.shapes.add_table(len(rows)+1,len(headers),Inches(x),Inches(y),Inches(w),Inches(h)).table
 if widths:
  for c,v in zip(tab.columns,widths):c.width=Inches(v)
 for i,row in enumerate([headers]+rows):
  for j,v in enumerate(row):
   c=tab.cell(i,j);c.text=str(v);c.margin_left=c.margin_right=Inches(.07);c.margin_top=c.margin_bottom=Inches(.04)
   c.fill.solid();c.fill.fore_color.rgb=RGBColor(235,235,235) if i==0 else RGBColor(255,255,255)
   c.vertical_anchor=MSO_ANCHOR.MIDDLE
   for p in c.text_frame.paragraphs:
    for r in p.runs:r.font.name='Calibri';r.font.size=Pt(size);r.font.bold=i==0;r.font.color.rgb=BLACK
 return tab
def card(s,x,y,w,h,text,size=18):
 sh=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,Inches(x), Inches(y), Inches(w), Inches(h))
 sh.fill.solid();sh.fill.fore_color.rgb=RGBColor(245,245,245);sh.line.color.rgb=BLACK
 textbox(s,x+.12,y+.1,w-.24,h-.2,text,size=size)

s=slide('Project Review II',None)
textbox(s,.7,1.65,8.6,1.65,TITLE,size=29,bold=True,align=PP_ALIGN.CENTER)
textbox(s,1,3.65,8,1.55,'\n'.join(n+' — '+r for n,r in TEAM),size=20,align=PP_ALIGN.CENTER)
textbox(s,1,5.6,8,.8,'Cheap Harm Prediction for Test-Time Normalization\nImplementation and five-seed evaluation',size=17,align=PP_ALIGN.CENTER)

s=slide('Summary of the Project',0)
bullets(s,['Goal: decide when updating normalization helps and when SOURCE should be retained.','Implemented: frozen source, unconditional normalization, concentration-only gate and three-feature gate.','Five-seed result: 77.9 ± 0.9% accuracy; +1.5 percentage points over SOURCE.','Harmful-update episodes reduced to 11%; unseen shifts, imbalance and inference cost remain under study.'],size=21)

s=slide('Review: Background Survey',1)
table(s,['Work','Core idea','Use in this study'],survey,h=4.5,widths=[2.2,3.5,3.3],size=14)
textbox(s,.6,6.3,8.8,.5,'Normalization and adaptation selection are established; the contribution must be narrower.',size=15)

s=slide('Summary of Gap Analysis',2)
bullets(s,['High predicted-class concentration can reflect genuine class imbalance or corruption-induced prediction collapse.','A concentration-only decision can therefore look similar in conditions with different update benefits.','Question: do entropy and feature displacement improve the decision, and does the gain transfer?','Current evidence: +0.6 percentage points over concentration-only gating; generalization remains open.'],size=20)

s=slide('Proposed Idea',3)
card(s,.65,1.7,4.1,3.5,'UNCONDITIONAL NORMALIZATION\n\nEvery batch updates statistics.\n\nNo prediction of whether the update will help.',20)
card(s,5.2,1.7,4.1,3.5,'SELECTIVE NORMALIZATION\n\nThree batch summaries predict update benefit.\n\nChoose SOURCE or NORMALIZE.',20)
textbox(s,.7,5.65,8.6,.9,'Gate inputs: concentration, mean entropy, source-relative feature displacement.\nEncoder and classifier weights remain fixed.',size=18)

s=slide('Flow of the Proposed Work',4)
for y,a,b in [(1.55,'Unlabeled support batch','Frozen source inference'),(3.05,'Concentration + entropy\n+ feature displacement','Benefit predictor\n(depth-two tree)'),(4.55,'SOURCE or NORMALIZE','Separate query prediction')]:
 card(s,.7,y,3.9,1.05,a,18);textbox(s,4.7,y+.22,.5,.5,'→',24);card(s,5.3,y,3.9,1.05,b,18)
textbox(s,.7,6.05,8.6,.65,'Development: action-error difference → fit gate → calibrate margin.\nDeployment uses no target labels; support statistics are frozen for queries.',size=16)

s=slide('Dataset Used and Preprocessing',5)
textbox(s,.6,1.45,8.8,.9,'Local development: handwritten digits; 1,797 grayscale images, 10 classes, 8 × 8 pixels. Pixel values divided by 16.',size=19)
table(s,['Partition','Images','Purpose'],splits,y=2.65,h=2.25,widths=[2.3,1,5.7],size=15)
textbox(s,.6,5.12,8.8,1.15,'Development shifts: noise, brightness, blur, translation; held-out contrast and occlusion. Balanced and 75%-dominant batches.\nFive-seed gate results came from the other system; its full run manifest is being consolidated.',size=16)
textbox(s,.6,6.45,8.8,.25,'Dataset: scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html',size=10)

s=slide('Detailed Work: Finished Implementation',6)
table(s,['Component','Finished work'],[
 ['Source pipeline','Training, stored source moments and frozen prediction'],
 ['Normalization action','Support-only moments; fixed query-time statistics'],
 ['Concentration-only gate','One-signal comparator for conditional updating'],
 ['Three-feature gate','Concentration, entropy and displacement; benefit-based decision'],
 ['Evaluation','Four-policy comparison across five seeds; harmful-update analysis'],
 ['Research records','Saved development code, outcomes and reproducibility artifacts'],
 ],h=4.4,widths=[2.6,6.4],size=16)
textbox(s,.6,6.25,8.8,.45,'Continuing: unseen conditions, feature ablations, harmful-update diagnosis and total inference cost.',size=16)

s=slide('Performance Evaluation',7)
table(s,['Approach','Accuracy\nmean ± SD','Gain vs\nSOURCE','Harmful\nupdates'],metrics,y=1.5,h=2.6,widths=[3.65,1.8,1.75,1.8],size=15)
s.shapes.add_picture(str(ASSETS/'five_seed_results.png'),Inches(.65), Inches(4.25),width=Inches(8.7),height=Inches(2.25))
textbox(s,.65,6.6,8.7,.27,'Five seeds. Harmful updates: % of all episodes with an update and lower accuracy than SOURCE.',size=10)

s=slide('Results and Discussion',8)
bullets(s,['Three-feature gate: +1.5 points over SOURCE and +0.6 points over the concentration-only gate.','Harmful-update episodes: 31% → 15% → 11% as the decision becomes selective.','Improvement is modest. Normalization still harms some conditions; the remaining failures need analysis.','SD describes seed variability. Paired results are needed for significance claims; latency benefits have not been established.'],size=20)

s=slide('Scope of the Work',9)
bullets(s,['Completed: two-action controller, three support signals and initial five-seed comparison.','Runtime inputs are unlabeled; the source classifier weights remain fixed.','Unseen families, class imbalance, continual streams and complete computation cost remain open.','Next benchmark stage: documented image-benchmark evaluation and faithful normalization baselines.'],size=21)

s=slide('Conclusion and Future Work',10)
textbox(s,.65,1.5,8.7,.85,'Finished result: 77.9 ± 0.9% accuracy; +1.5 points over SOURCE; 11% harmful-update episodes.',size=23,bold=True)
table(s,['Continuing task','Next deliverable'],[
 ['Consolidate the external runs','Code, seed-level results and configuration manifests'],
 ['Improve reliability','Diagnose failures; calibrate a more conservative update margin'],
 ['Check generalization','Unseen families, imbalance and matched-concentration analysis'],
 ['Evaluate practical value','Complete inference time, memory and feature ablations'],
 ],y=2.8,h=3.1,widths=[3,6],size=16)
textbox(s,.65,6.2,8.7,.45,'We will retain improvements only when they survive the stronger evaluation.',size=17)

s=slide('References',11)
for i,r in enumerate(refs):
 short=r.rsplit(' https://',1)[0]
 textbox(s,.6,1.45+i*.64,8.8,.6,short,size=12)
textbox(s,.6,6.65,8.8,.2,'Full source links and detailed implementation discussion are included in the Word report.',size=10)
prs.save(HERE/'Shift_Aware_TTA_Review_II.pptx')

# Detailed Word report follows the supplied template's section sequence.
doc=Document();sec=doc.sections[0];sec.top_margin=DI(.7);sec.bottom_margin=DI(.7);sec.left_margin=sec.right_margin=DI(.8)
for name in ['Normal','Title','Subtitle','Heading 1','Heading 2','Heading 3']:
 st=doc.styles[name];st.font.name='Calibri';st.font.color.rgb=DC(0,0,0)
doc.styles['Normal'].font.size=DP(11);doc.styles['Normal'].paragraph_format.space_after=DP(7)
doc.styles['Normal'].paragraph_format.line_spacing=1.08
doc.styles['Heading 1'].font.size=DP(16);doc.styles['Heading 2'].font.size=DP(12)
sec.header.paragraphs[0].text='SHIFT-AWARE TEST-TIME ADAPTATION  |  REVIEW II'
sec.header.paragraphs[0].runs[0].font.size=DP(8)
fp=sec.footer.paragraphs[0];fp.alignment=2
fp.add_run('Page ');f=OxmlElement('w:fldSimple');f.set(qn('w:instr'),'PAGE');fp._p.append(f)
doc.add_paragraph('PROJECT REVIEW II',style='Subtitle')
doc.add_heading(TITLE,0)
doc.add_paragraph('Cheap Harm Prediction for Test-Time Normalization',style='Subtitle')
doc.add_paragraph('Implementation, completed evaluation and continuing work')
for name,reg in TEAM:doc.add_paragraph(name+' — '+reg)
doc.add_paragraph('23 October 2026')
doc.add_page_break()
def dtable(headers,rows):
 t=doc.add_table(rows=1, cols=len(headers));t.style='Table Grid'
 for c,v in zip(t.rows[0].cells,headers):c.text=v
 for row in rows:
  for c,v in zip(t.add_row().cells,row):c.text=str(v)
 for i,row in enumerate(t.rows):
  pr=row._tr.get_or_add_trPr();pr.append(OxmlElement('w:cantSplit'))
  for c in row.cells:
   for p in c.paragraphs:
    for r in p.runs:r.font.size=DP(9);r.font.color.rgb=DC(0,0,0);r.bold=i==0
 return t
md=['# '+TITLE,'','Project Review II — 23 October 2026','']+[n+' — '+r for n,r in TEAM]
for idx,(title,parts) in enumerate(sections,1):
 doc.add_heading(str(idx)+'. '+title,1);md+=['','# '+str(idx)+'. '+title,'']
 for heading,body in parts:
  if heading!='Sources':doc.add_heading(heading,2)
  for para in body.split('\n\n'):doc.add_paragraph(para)
  md+=['## '+heading,'',body,'']
  if idx==2 and heading=='Closest work':dtable(['Work','Relevant idea','Influence'],survey)
  if idx==6 and heading=='Recorded development data':dtable(['Partition','Images','Purpose'],splits)
  if idx==8 and heading=='Five-seed results':
   dtable(['Approach','Accuracy: mean ± SD','Gain vs SOURCE','Harmful-update episodes'],metrics)
   doc.add_paragraph('Accuracy is summarized across five seeds. Harmful-update percentages use all evaluation episodes as the denominator.')
   doc.add_picture(str(ASSETS/'five_seed_results.png'),width=DI(6.55))
   doc.add_paragraph('Figure 1. Mean accuracy with seed SD, and harmful-update episodes for the evaluated adaptation policies.')
md+=['','| Approach | Accuracy, mean ± SD across 5 seeds | Gain over SOURCE | Harmful-update episodes |','|---|---:|---:|---:|']+['| '+' | '.join(row)+' |' for row in metrics]
for p in doc.paragraphs:
 for r in p.runs:r.font.color.rgb=DC(0,0,0)
doc.save(HERE/'Shift_Aware_TTA_Review_II.docx')
(PROJECT/'papers'/'review-ii-five-seed-progress.md').write_text('\n'.join(md)+'\n')
(HERE/'result_provenance.json').write_text(json.dumps({'report_date':'2026-10-23','main_results_source':'User-supplied actual five-seed results from another system, supplied in this conversation','main_results':metrics,'harm_definition':'Percentage of all evaluation episodes where the policy applied normalization and accuracy was lower than SOURCE','sd_definition':'Variation across five seeds; not confidence intervals','external_run_details':'Raw predictions, individual seed results, dataset/backbone/split manifest and external gate code not supplied','development_source':'diagnostics/2026-10-23; recorded local digits development, reported separately','new_experiments_run_for_report':False,'template':'Review2.pptx; original retained; masters, layouts and 4:3 dimensions reused'},indent=2)+'\n')
print(json.dumps({'presentation':str(HERE/'Shift_Aware_TTA_Review_II.pptx'),'slides':len(prs.slides),'word':str(HERE/'Shift_Aware_TTA_Review_II.docx'),'words':sum(len(p.text.split()) for p in doc.paragraphs)},indent=2))

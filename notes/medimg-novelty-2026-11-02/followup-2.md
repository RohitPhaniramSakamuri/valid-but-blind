# Supervisor follow-up 2: exact comparison, BN-twin rule, and medical contribution

**Search/review date: 2 November 2026. No experiments were run.** This extends the existing reviews and preserves their access limits. Only this follow-up document is being added; repository result records are treated as historical evidence, not independently recomputed results.

**Outcome:** I did not find an accessible inspected paper reporting the complete adapted-versus-frozen missed-alarm comparison under joint corruption and class-prior shift. C1 and M6 therefore retain **No report found**, within the coverage below. I also found no explicitly implemented equivalent of the entire BN-twin OR rule plus sequential risk-alarm wrapper. Its ingredients have close predecessors, including a BN-calibrated anchor that the medical review did not discuss. A successful DermaMNIST pilot would primarily contribute a controlled medical measurement and replication.

## 1. Attempt to overturn M6 and C1

### Exact target and result

I searched for the broader falsifier as well as the literal C1: a label-free sequential/anytime **model-risk** monitor evaluated on an entropy-adapted predictor and a frozen comparator, under **joint image corruption and class-prior change**, with missed violations, false-negative alarms, power or equivalent detection-delay evidence. Medical imaging is required for M6, but not for the broader search. A study using a different sequential monitor could substantially anticipate C1 without reproducing its literal Schirmer implementation.

| Claim | Follow-up verdict | Exact boundary and unresolved sources |
|---|---|---|
| **C1** | **No report found** | No inspected accessible report gives the complete Schirmer/Tent-versus-frozen missed-risk comparison under persistent class-prior skew plus corruption. The broader search for another label-free sequential monitor did not produce a verified matching comparison either. Mahdiani, ODFD and TRUST-ADAPT remain unread in full; citation enumeration remains incomplete. |
| **M6** | **No report found** | Same conjunction restricted to medical imaging, including artifact/site change plus prevalence change. New UNSURE leads do not supply verified matching evidence. In addition to the blockers above, *Well-Calibrated but Unusable* is a newly identified **blocked close medical lead** involving prevalence and adaptation. Its full method cannot be excluded. |

**Paper evidence already established, retained rather than rediscovered:** Schirmer §§3.4/5.4 and Fig. 5 explicitly demonstrate poor proxy-induced alarm power and repair it with a prototype proxy; the studied failure is not the requested Tent/frozen joint-shift comparison. The published Cygert study evaluates corrupted Dirichlet streams and proxy-based adaptation/model selection (§5.2/Figs. 6–8), rather than this risk-alarm comparison. Han Appendix L compares adaptive and frozen monitoring signals, but uses revealed forecasting outcomes. PPRM §5.1.2/Fig. 2a shows an uncertainty-risk-monitor non-alarm with a fixed classifier and uses target labels in its alternative. Exact extraction and reading scopes are preserved in the [earlier review](../novelty-review-2026-11-02/review.md) and its [direct-citer follow-up](../novelty-review-2026-11-02/agents/citations/direct-citers-followup.md). These precedents already defeat a broad claim of discovering silent adaptation failure or independent monitoring.

### New evidence or deeper reading in this follow-up

The following are **paper claims** or explicitly qualified abstract claims. The last column is **my assessment**, not a statement by those authors. A selective reading is not represented as a full-paper reading. None of the incomplete screens is counted as a fully cleared source.

| Source and verified metadata | Reading depth and evidence location | Paper states | Assessment against the requested comparison |
|---|---|---|---|
| **Guan, Qiuguo; Ren, Zhiyu. Cross-Domain Robust Dynamic Trust Evaluation for Industrial Internet of Things Edge Nodes.** *Computers, Materials & Continua* 88(2), article 99, published 15 June 2026. [Publisher](https://www.techscience.com/cmc/v88n2/67683/html), DOI 10.32604/cmc.2026.082704. | Full-text methods §§3.3.1–3.3.4 and experiments §§4.1–4.5 read; metadata/abstract and selected introductory/limitation text. Several result tables are images and their cells were **not** independently transcribed. | RaL-TTA uses a forward-only BN-calibrated frozen anchor (Eq. 17), entropy/volatility gating (Eq. 25), and disagreement-related fallback (Eqs. 35–39). §4.3 reports Tent losing attack recall; §4.4.2 counts protection-state batches. | Important additional BN-anchor predecessor. Attack recall/FPR measure the intrusion classifier, not a separate sequential model-risk monitor’s misses. The protection rule differs from the requested OR rule. No matching anytime risk-bound comparison is established. |
| **Adhikary, Souraj; Chabi, Negar; Mastmeyer, Andre. Bound-Aware Per-Organ Recall Risk Control for Multi-Organ CT Segmentation under Clinical Domain Shift.** 2026 arXiv; title also appears in the official UNSURE programme. [Full text](https://arxiv.org/html/2608.18193v1). | Full main text §§1–7 read; equations, Tables 1–2/Figs. 1–4; reference list selective. | Frozen AMOS/RAOS segmentation, labeled local recalibration and WSR/HB/CRC bounds. §3.1 defines FNR as missed **organ voxels**; §§3.3/4 specify cached outputs without model retraining. §5.2 reports failed risk-control transfer. | A tempting false match: a betting bound and false negatives occur, but neither is the requested label-free deployment-alarm comparison. No entropy TTA arm. |
| **Guinea, Alejandro Sanchez; Erokhina, Mariya. Sequential Conformal Safety for Trustworthy Clinical Decision Pathways in Ophthalmology.** UNSURE @ MICCAI 2026, official LNCS 17260 record. [Proceedings page](https://papers.miccai.org/miccai-2026-sat/UNSURE2026_076.html). | Official abstract/metadata only. Main PDF failed on the ordinary and download-query URLs. | Abstract describes stage-wise conformal pruning through a clinical decision tree, including diabetic-retinopathy/OCT pathways. | “Sequential” concerns staged clinical decisions in the accessible description. It does not establish the requested result; full text remains unresolved. |
| **Zhang, Tianyi; Liu, Zixuan. Well-Calibrated but Unusable: Calibration Error Does Not Certify Zero-Shot Chest X-Ray VLMs.** UNSURE @ MICCAI 2026, official LNCS 17260 record. [Proceedings page](https://papers.miccai.org/miccai-2026-sat/UNSURE2026_028.html). | Official abstract/metadata only; main PDF inaccessible on two URL forms; no public alternate full text located. | Abstract combines calibration-prevalence sweeps with a transductive-adaptation stress test, reporting low ECE despite poor discrimination. | A serious new medical overlap lead. The accessible text does not report joint artifact/prevalence **sequential-alarm misses**, but an abstract cannot clear its uninspected experiments. Prioritize this source before any priority claim. |
| **Stöhr, Patricia; Götz, Michael; Ropinski, Timo; Wolf, Daniel Santak. Investigating Test-Time Adaptation of Convolutional Neural Networks for Medical Image Analysis under Distribution Shifts.** CLiMeM @ MICCAI 2026, official LNCS 17263 record. [Official PDF](https://papers.miccai.org/miccai-2026-sat/paper/CLiMeM_005.pdf). | Metadata, §2.2 and §3/Tables 1–2 read; other main passages selective. Full-document search for “monitor” had no match. | WhiCo aligns features using stored source moments; §3 compares frozen/TTT/WhiCo classification on corrupted CT, including simulated low-dose images. TTT uses reconstruction, not entropy minimization. | Additional medical adaptation-harm evidence, with a materially different adaptation loss and evaluation. Inspected results measure accuracy/AUC/F1, not missed sequential risk alarms. |
| **Xu, Ruoshi; Gao, Mingqi; Luo, Shengda; Chen, Jingkun. CIRSeg: Coarse-to-Fine Intensity-Robust Liver Segmentation with Source-Free Continual Test-Time Adaptation.** CARE @ MICCAI 2026, official LNCS 17273 record. [Official PDF](https://papers.miccai.org/miccai-2026-sat/paper/CARE_030.pdf). | §2.4/Eqs. 9–11, §§3.1/3.3–3.4, Table 2 and conclusion read; remaining training methods selective. | Frozen anchor plus entropy/consistency-adapted student, confidence-based update screening and a prior bank. State persists across cases. §3.4 explicitly says paired no-TTA test predictions were unavailable for causal comparison. | Additional medical frozen-reference/entropy-TTA overlap. The gate regulates updating; no corresponding sequential risk alarm is established in the inspected method/results. Its correlation-based “consistency” is not the requested binary live/twin disagreement. |
| **Koziak, Adam; Guo, Yuhong. Reliability-Guided Adaptive Ensembling for Robust Test-Time Adaptation.** arXiv:2606.22351, 21 June 2026. [Primary full text](https://arxiv.org/html/2606.22351v1). | Expanded beyond the earlier abstract screen: §§1/3 and selected §4 results/configuration/ablation text and tables read; not the full supplement. | SAFER pools perturbed views using feature agreement for adversarial-stream TTA; §3.1 includes smoothing/frequency transforms; §4 reports classification accuracy. | Another consistency/remedy precursor, not a verified missed-alarm comparison. A full-text search found no “Monitoring Risks” title; secondary descriptions do **not** establish that it cites Schirmer. It is not added to the verified citer count. |
| **Timans, Alexander; Verma, Rajeev; Nalisnick, Eric; Naesseth, Christian A. On Continuous Monitoring of Risk Violations under Unknown Shift.** UAI 2025 acceptance stated on primary arXiv record. [Full text](https://arxiv.org/html/2506.16416v1). | Primary metadata and §§6.1–6.2/discussion passages read, not full proofs. | §6.1 monitors an outlier classifier’s total error; §6.2 defines miscoverage using true labels. Discussion treats unsupervised monitoring/model updates as extensions. | Another apparent false match for entropy, sequential testing and FNs; the inspected experiments are not label-free entropy-adapted/frozen risk monitoring. |

**Other screened leads, explicitly incomplete:** Yue Li, MengYu Yuan, Yujing Yang, Jia Fu, Yi Xin, Chu Jie Duan and Jun Wang, *An ethics-informed computable audit framework for monitoring misdiagnosis risk in AI-assisted diagnosis*, *Scientific Reports* 16, 16462 (6 April 2026), [primary](https://www.nature.com/articles/s41598-026-46652-1): abstract, “Simulation study: synthetic shift and subgroup imbalance,” and selected sentinel/limitations passages read. It describes synthetic binary diagnostic scores and delayed-label audit metrics; no inspected entropy-TTA comparison. Zayn Andre Zainal et al., *Safety-Relevant Biomedical Machine Learning Should Adopt Stability-First Reporting*, medRxiv DOI 10.64898/2026.09.30.26364447: expanded **indexed primary-text excerpts**, including §3, §4 Objection 4 and reporting targets, are now visible, but direct full-page retrieval still returns 403. This previously known medical citer remains incompletely read; the excerpts concern training/observation-process stress tests, not a verified C1 experiment.

The τ-Guard preprint (Research Square rs-10544123/v1) appeared through an author-uploaded ResearchGate abstract: recalibration-invariant drift scoring and a CUSUM comparison. Its primary full text remained inaccessible. An indexed anonymous ICLR 2026 TCUQ PDF (§5.2, OpenReview `7Rfyx8EZea`) also discusses accuracy-drop detection under corruption; identity and full protocol were not resolved, so it is a discovery-only lead. Neither is used to clear C1. SicTTA, found through CIRSeg’s reference 24, has verified [PubMed metadata/abstract](https://pubmed.ncbi.nlm.nih.gov/41207141/) and an [official author repository](https://github.com/HiLab-git/SicTTA): Jianghao Wu, Xinya Liu, Guotai Wang and Shaoting Zhang, *MedIA* 108, 103859 (2026; online October 2025). Publisher full text failed; it remains an abstract-level uncertainty/normalization precursor, not verified alarm evidence.

### Citation tracing, workshop coverage and blockers

**Fresh citation attempts:** the Semantic Scholar canonical-arXiv lookup and known paper-hash citation endpoint, Google Scholar cited-by cluster `7250704993477156062`, and OpenAlex published-paper citation endpoint were all inaccessible through the web tool. A search-visible secondary mlsanity page listed 12 citing titles, all already in the earlier 21-title union. This is a subset, not a new complete citation audit. No newly verified direct citer is claimed. The previously audited Anatomy, E-valuator, PORTAL and outcome-dependent monitoring papers retain their recorded distinctions; unread citer abstracts are not negative full-text findings.

**Workshop search was strengthened:** I inspected the official [UNSURE 2026 programme](https://unsuremiccai.github.io/) and keyword matches in the [MICCAI satellite index](https://papers.miccai.org/miccai-2026-sat/) for monitoring, sequential safety and TTA, then followed the close UNSURE/CLiMeM/CARE records above. This now independently corroborates TCSR’s UNSURE inclusion; the previous review only had its author-reported acceptance. The index mixes historical event tags such as ADSMI2024 with a 2026 page template, so its template year is not used to redate old work. This was targeted screening, not full reading of every workshop submission.

**Rechecked full-text blockers:** [Mahdiani SSRN 7602585 Delivery PDF](https://papers.ssrn.com/sol3/Delivery.cfm/7602585.pdf?abstractid=7602585&mirid=1), [ODFD IEEE 11737673](https://ieeexplore.ieee.org/document/11737673/), and the [correct TRUST-ADAPT publisher PDF](https://ijsrcseit.com/home/article/download/CSEIT25113445/CSEIT25113445) again failed. Their previously recorded abstract-level claims remain unverified. AdaSwitch3D’s earlier full-text block also remains unresolved; it was not freshly retrieved in this follow-up. Add the two UNSURE PDFs, SicTTA and τ-Guard above to the access limits. These holes prevent an exhaustive absence assertion for C1, M6 or the exact twin rule.

## 2. Closest work to the specific BN-twin OR alarm

Define the **sample flag**, separately from the stream alarm:

\[
Q_t(x)=\mathbf{1}\{U(b_{B_t}(x))>\lambda_b\ \lor\ \arg\max b_{B_t}(x)\ne\arg\max f_t(x)\}.
\]

Here `b` starts from the source checkpoint, takes no gradient steps, and uses **current test-batch BN statistics**. `f_t` is the live adapted classifier. The source-calibrated flag stream is then passed to the project’s confidence-sequence/alarm computation. Its equivalent acceptance predicate is **twin confident AND predictions agree**; I looked for this equivalence as well as “twin” wording. Merely having two models or an OR operator is insufficient to establish equivalence.

| Closest predecessor | Paper evidence / reading scope | Exact overlap and difference: my assessment |
|---|---|---|
| [Schirmer et al., NeurIPS 2025](https://proceedings.neurips.cc/paper_files/paper/2025/file/746960ad49ddb47248970a0e1404230c-Paper-Conference.pdf) | Prior full-text selective reading, §§3.2–3.4/Proposition 1/Eq. 7 and §5.4/Fig. 5. | Supplies the sequential wrapper and explicitly replaceable proxy. No inspected BN-twin OR instantiation. A generic proxy framework accommodating a flag is not evidence that this flag was implemented. |
| **RaL-TTA, above** | §§3.3.1/3.3.4, Eq. 17 and Eqs. 35–39. | Closest newly identified **BN-anchor implementation**: forward-only calibration and live/anchor comparison. Anchor statistics are calibrated once on trusted normal target traffic; fallback is scored/budgeted and gated, not the current-batch twin OR risk alarm. |
| **Cerqueira, Vitor; Gomes, Heitor Murilo; Bifet, Albert; Torgo, Luis. STUDD: A Student–Teacher Method for Unsupervised Concept Drift Detection.** [Primary 2021 preprint](https://arxiv.org/abs/2103.00903). | PDF §§4.1–4.2, pp. 8–10/Figs. 4–5 read; related work and experimental setup selective. Accepted-journal metadata not independently verified here. | Direct architecture precursor: monitor model disagreement without deployment labels through a sequential change detector. Student is trained to mimic teacher; no live entropy-TTA/BN-twin OR, and no equivalent anytime model-risk guarantee is established. |
| [Han et al., 2026](https://arxiv.org/abs/2610.07038) | Inherited full-text selective extraction: Appendix L/Tables 48–51. | Closest independent **frozen-sentinel response to adaptation masking**. Uses revealed forecasting outcomes and a different adapter; not this label-free classification rule. |
| [ReDi-FM, IJCAI 2026](https://ijcai.org/proceedings/2026/140), and **CIRSeg, above** | ReDi-FM §§3.2–3.3 previously read; CIRSeg §2.4 freshly read. | Medical fixed-reference confidence/consistency mechanisms are established. They regulate adaptation or distillation rather than reporting this sequential alarm’s power. |
| [AETTA, CVPR 2024](https://openaccess.thecvf.com/content/CVPR2024/papers/Lee_AETTA_Label-Free_Accuracy_Estimation_for_Test-Time_Adaptation_CVPR_2024_paper.pdf) | Inherited selective main reading, §3.2/Fig. 2 and estimator method. | Disagreement as a label-free correctness signal during TTA is established. Its dropout probes come from the adapted model; no entropy-free BN-reference OR rule. |

**Exact-rule answer:** no accessible inspected paper explicitly specifies the complete rule or an equivalent acceptance/computation rule with the same model states, information access and sequential target. This is bounded by the blockers in §1. The strongest prior-work objection is the combination of Schirmer’s replaceable-proxy alarm with established uncertainty/disagreement monitoring and BN anchors, rather than a verified identical equation.

**Important correction to the question’s wording — my inference, supported by the local record:** the working OR rule is fed into a sequential **alarm computation**, but its selected output is not an established lower bound on live-model risk. [The local manuscript](../../paper/main.tex), “An Entropy-Free Twin Alarm—Design/Results,” says only the `w=0` form has the displayed inequality; the successful `w=1,c=1` OR rule is heuristic. Transferring the twin’s clean error corrections to a shifted stream also needs an assumption. An uncertain wrong twin can disagree with a correct live prediction: the OR flag counts that case without proving a live error. A confidence sequence for the flag rate cannot repair this proxy-to-error gap. Thus an exact-rule priority claim and a certified-risk claim are separate questions; neither follows from a positive pilot.

Also, a no-gradient current-batch BN twin is not a fixed predictor. It changes with batch composition, including prevalence. A fully frozen-source comparator and a BN-only arm are therefore necessary distinctions when describing the result.

## 3. What a successful option-d pilot would contribute

**Conditional assessment:** suppose a prespecified, held-out DermaMNIST-224 study shows the adapted/frozen power gap and a useful twin recovery at comparable empirical false-alarm rates. The additional evidence would be **a controlled medical-classification measurement of sequential alarm sensitivity under joint synthetic shifts**, together with a tested proxy substitution. The proposal supplies neither a new sequential-testing framework nor a new principle of independent reference monitoring.

The following table separates what each paper establishes from the increment the hypothetical result would supply. Reading depths/versions are in [closest-work.csv](closest-work.csv); these five main texts were inspected in the preceding medical review, with ReDi-FM’s equation-extraction limitation retained.

| Relative to | Paper’s established result | Additional evidence from the specified successful pilot — my assessment |
|---|---|---|
| **ECFR**, MICCAI 2026, §3.2/Table 1/Fig. 3. [Primary](https://papers.miccai.org/miccai-2026/paper/0402_paper.pdf) | Medical Tent calibration can worsen; entropy/consistency adaptation can produce undesirable confidence behavior. | Quantified **missed sequential risk violations** relative to the same frozen checkpoint, under explicitly joint corruption/prior sampling, plus the twin’s alarm-power comparison. “Tent damages medical calibration” is already covered. |
| **DSBR**, 2026, §5 and Appendix G/Table 10. [Primary](https://arxiv.org/abs/2606.02339) | Medical entropy-adaptation prediction bias/collapse; explicit label-shift stress tests are on ImageNet-C. | Medical joint-shift **monitor evaluation**, including failure to alarm and normalization-versus-entropy controls. A finding of adaptation collapse alone adds little. |
| **TCSR**, UNSURE 2026, §§3–4/Table 1. [Primary](https://arxiv.org/html/2608.16748v1) | Label-free-at-runtime medical failure alarms combining quality and other features for a fixed segmenter. | Sensitivity loss caused by changing the monitored classifier’s state, and recovery in an adapting classifier’s stream-level alarm. The pilot would not originate medical failure detection, quality features or temporal alerting. |
| **Flühmann et al.**, UNSURE 2025, §4.2/§5.3/Fig. 4. [Primary](https://arxiv.org/html/2507.22776v1) | Static medical metric estimators struggle under prevalence shift; artifact and prevalence experiments are separate. | The **interaction with entropy adaptation and sequential alarm power** under a controlled joint shift, rather than only estimating a static model’s clinical metrics. |
| **ReDi-FM**, IJCAI 2026, §§3.2–3.3. [Primary](https://ijcai.org/proceedings/2026/140) | Frozen reference models and disagreement already guide medical continual adaptation. | Using a cheap BN-only companion as an external alarm signal, keeping the live adaptation policy fixed, and quantifying missed violations/false alarms. Frozen-reference medical safety mechanisms themselves are already covered. |

**Plain assessment:** one positive DermaMNIST result is a useful diagnostic replication. Its weight depends on showing a consequential loss of detection power, rather than moving the alarm threshold or making Tent fail with an extreme learning rate. It has limited standalone method strength. Synthetic blur/JPEG plus resampled lesion labels supports a controlled benchmark claim; it does not establish natural scanner drift, clinical disease-prevalence dynamics, or patient safety.

**Strongest reviewer objection — my inference:** “You have moved an already documented proxy-failure problem to a convenient medical benchmark and combined standard uncertainty, disagreement and a BN reference inside an existing alarm. Where is the residual benefit over the original paper’s prototype proxy and established correctness estimators, at the same false-alarm and compute budget?” A dataset substitution and a positive OR-rule ablation alone do not answer this objection.

To support even the bounded claim, evaluation must separate development and held-out image IDs/shift families, seal evaluation labels from routing/tuning/stopping, use equivalent initial states, and report safe-stream denominators and paired/common-violation comparisons. It must distinguish source/BN/Tent, shared failures from adaptation-only harm, and collapse from subtler failures. These are conditions on interpreting a future result, not experiments performed here. Adequate noncollapsed and safe subsets matter more than adding many correlated resampled streams. The existing CIFAR adaptation-harm combined verdict remains **NOT SHOWN**; a hypothetical medical success must not rewrite it.

**Most defensible single-sentence contribution claim, only if the frozen held-out result supports every clause:**

> On DermaMNIST-224 under prespecified corruption and class-prior shifts, we quantify lower detection power of Schirmer’s label-free sequential monitor for Tent than for its frozen checkpoint, and show that an entropy-free BN-twin uncertainty-or-disagreement proxy recovers sensitivity at comparable empirical false-alarm rates on held-out shift families.

**A claim a reviewer should reject:**

> We introduce the first statistically guaranteed medical safety monitor that detects entropy-adaptation failures under arbitrary scanner and prevalence shifts without labels.

It overstates priority, converts a heuristic proxy into a guarantee, generalizes beyond the tested shifts and modality, and hides the source/development-label requirements. The useful claim concerns measured power within a specified protocol.

## Search ledger for this follow-up

The follow-up used **54 exact search queries in 14 batches**, plus 20 retrieval/find/click batches. Some calls combined searches with primary retrievals. Search results were screened as visible batch unions; the engine did not expose per-query exhaustive hit totals. Irrelevant finance, climate-adaptation and biochemical “label-free” hits were excluded. Full-text access/read depth is stated above. Queries follow; this is a reproducibility record, not a claim of citation saturation.

1. `"Monitoring Risks in Test-Time Adaptation" -"schirmer" "2026"`
2. `"Monitoring Risks in Test-Time Adaptation" "Dirichlet"`
3. `"sequential" "risk" "Tent" "false negative"`
4. `"test-time adaptation" "missed alarms"`
5. `"Monitoring Risks in Test-Time Adaptation" "2026" "medical"`
6. `"Monitoring Risks in Test-Time Adaptation" "false" "alarm"`
7. `"UNSURE" "2026" "monitoring" adaptation`
8. `"MICCAI 2026" workshop "risk" "adaptation"`
9. `"Reliability-Guided Adaptive Ensembling for Robust Test-Time Adaptation"`
10. `"sequential risk" "class" "corruption" adaptation`
11. `"risk monitoring" "label shift" adaptation`
12. `"test-time adaptation" "false negatives" monitor`
13. `"test-time adaptation" "batch norm" "twin" monitor`
14. `"risk monitoring" "disagreement" adaptation`
15. `"test-time adaptation" "uncertain or" disagreement`
16. `"test-time adaptation" "prior shift" "alarm"`
17. `"Sequential Conformal Safety for Trustworthy Clinical Decision Pathways in Ophthalmology"`
18. `"Bound-Aware Per-Organ Recall Risk Control" `
19. `"Well-Calibrated but Unusable" `
20. `"UNSURE 2026" "adaptation" monitoring`
21. `"batch-normalization" "disagreement" "risk" monitoring`
22. `"frozen" "uncertain" "disagree" "test-time adaptation"`
23. `"test-time adaptation" "confidence sequence" "disagreement"`
24. `"entropy-free" "monitor" twin`
25. `"Tent" "risk monitor" "Dirichlet"`
26. `"Schirmer" "monitoring" "Dirichlet"`
27. `"CIFAR-100-C" "missed" "monitor"`
28. `"label-free" "sequential" "entropy" "2026" monitor`
29. `"STUDD" "student" "teacher" drift detection paper`
30. `"test-time adaptation" "uncertainty" "or disagreement" monitor`
31. `"test-time adaptation" "frozen reference" "sequential"`
32. `"Cross-Domain Robust Dynamic Trust Evaluation"`
33. `"Schirmer" "Monitoring Risks" "2026" "alarm" -site:openreview.net -site:proceedings.neurips.cc`
34. `"class-prior" "corruption" "monitoring" adaptation`
35. `"7602585" "Dirichlet"`
36. `"test-time adaptation" "false negative rate" "risk" monitor`
37. `"Schirmer" "monitoring" "label shift"`
38. `"risk monitoring" "TENT" "Dirichlet" 2026`
39. `"unsupervised" "risk monitor" "false negatives" adaptation`
40. `"label-free" "sequential risk" "frozen"`
41. `site:arxiv.org/abs/26 "risk monitoring" "test-time adaptation"`
42. `site:arxiv.org/html/26 "Schirmer" "alarm"`
43. `site:arxiv.org "Tent" "missed" "risk"`
44. `"test-time adaptation" "Dirichlet" "monitoring" "2026"`
45. `"Safety-Relevant Biomedical Machine Learning Should Adopt Stability-First Reporting"`
46. `"Schirmer" "monitoring" "medical" "2026" -site:sotwe.com -site:sciencestack.ai -site:hypepaper.app -site:lacuna.tiptreesystems.com`
47. `"batch-norm" "twin" "alarm"`
48. `"risk" "uncertain" "disagrees" "reference model"`
49. `"Well-Calibrated but Unusable" Zhang Liu pdf`
50. `"Sequential Conformal Safety" arxiv`
51. `"τ-Guard" "test-time adaptation"`
52. `"STUDD" uncertainty confidence`
53. `"SicTTA" "103859"`
54. `"SicTTA" "uncertainty" "frozen"`


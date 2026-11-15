Saved [review.md](/home/sakamuri/Documents/Research/shift-aware-test-time-adaptation/notes/medimg-novelty-2026-11-02/review.md), [search-log.csv](/home/sakamuri/Documents/Research/shift-aware-test-time-adaptation/notes/medimg-novelty-2026-11-02/search-log.csv), [closest-work.csv](/home/sakamuri/Documents/Research/shift-aware-test-time-adaptation/notes/medimg-novelty-2026-11-02/closest-work.csv), and [contribution-options.md](/home/sakamuri/Documents/Research/shift-aware-test-time-adaptation/notes/medimg-novelty-2026-11-02/contribution-options.md). No experiments ran.

| Claim | Verdict |
|---|---|
| M1 | Partially covered |
| M2 | Substantially anticipated |
| M3 | Substantially anticipated |
| M4 | Already published |
| M5 | Partially covered |
| M6 | No report found |

M6’s exact searched conjunction was medical artifact **plus** prevalence shift, entropy adaptation, and missed sequential risk alarms compared with a frozen model. This absence finding remains limited by the inaccessible sources below.

The top three threats are:

1. **[TCSR-Monitor](https://arxiv.org/html/2608.16748v1):** classical image-quality features already contribute to medical failure alarms.
2. **[SICL](https://openaccess.thecvf.com/content/WACV2026/papers/Nam_Towards_Reliable_Test-Time_Adaptation_Style_Invariance_as_a_Correctness_Likelihood_WACV_2026_paper.pdf):** perturbation consistency already estimates correctness during adaptation.
3. **[ECFR](https://papers.miccai.org/miccai-2026/paper/0402_paper.pdf):** Table 1 directly reports worse medical Tent calibration.

**Recommendation:** option **d**, a controlled DermaMNIST-224 pilot. Pursue **b** only if quality improves detection beyond twin-only at comparable false alarms. The proposed three-hour budget is conditional, not measured.

**Could not access fully:** Mahdiani SSRN 7602585, ODFD, TRUST-ADAPT, AdaSwitch3D, CertainTTA, OptTTA, NIQE, and MMC+’s journal version—the earlier MMC+ preprint was read. Fail-CAM remained unidentified; forward-citation tracing remained incomplete.
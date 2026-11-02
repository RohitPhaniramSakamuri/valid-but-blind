# Test-Time Confidence Adaptation under RL-Induced Trajectory Shift

Citation key: `Ren2026StaRTTA`.

## Adversarial review — 2 November 2026

Zhenzhen Ren, Xiaoqing Zhang, GuoBiao Li, Bowen Fang, Yanxi Wang, Xinpeng Zhang, Ke Han. 2026. arXiv preprint2610.35500. [Primary source](https://arxiv.org/abs/2610.35500).

Publication/version qualification: arXivv1 first posted26October2026; primary record/PDF verified; no independent venue verified

**Actual reading:** 2026-11-02 selective full text §§3.1–3.3/4.1–4.3/5.1–5.2/6 and AppendixA.2/A.4/A.5; not all experiments read

**Locations:** §3.1/Table1 p3; §3.2/Table2 p3; §4.3 pp5–6; §5.1–5.2; AppendixA.2/Table13; AppendixA.4/Table15; AppendixA.5 cost

**Method/evidence and connection:** Offline agentic-RL model updates degrade learned confidence estimators; target-label-free confidence corrector uses stability rankings and Base–RL agreement

**Limit:** QA trajectories after offlineRL, not continual entropyTTA/image skew; labelled Base trajectories needed; main LLMs/scorer frozen during confidence adaptation; no sequential alarms

**Next reading step:** resolve access/version limits and the precise C1–C5 overlap before stronger claims. [Detailed claim review](../notes/novelty-review-2026-11-02/review.md); [source-level reading and extraction](../notes/novelty-review-2026-11-02/agents/tta_causes/late-metadata.json). No experiments were run for this reading.

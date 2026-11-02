# Independent verification of the assembled deep review

Date: 26 October 2026. Reviewed artifact: `outputs/shift-aware-tta-deep-review-2026-10-26.md`, as present during this pass. The draft linked Experiment 002 while that file was still being written; this pass therefore does not certify the final experiment file. Scope: scientific/document review and selected live source verification. No implementation, experiment, test, installation or benchmark reproduction was performed.

## Decision

**No blocking scientific error found in the reviewed synthesis.** It appropriately rejects broad novelty, names direct collisions, separates proposed experiments from results, and treats the recommendation as a candidate. The protocol is suitable as a study proposal. A few execution-defining details must be fixed before implementation; they do not invalidate the literature conclusion.

## Confirmed critical points

- The contribution is conditional: action-state coverage and replay-to-autonomous failure must be important beyond current predictions, reset heuristics and standard data aggregation. The text correctly identifies Agentic-TTT and DAgger as general predecessors and does not claim to invent persistent-state control or exposure bias.
- ASR/GALA/Hybrid-TTA are represented as state-aware predecessors. The draft explicitly acknowledges ASR's imbalance and dwell-time experiments, preventing an unfair absence claim.
- KEEP preserves the live model; RESET changes persistent state; answering with SOURCE can preserve live state. These are scientifically distinct, and the action table recognizes the distinction.
- Primary timing is predict-then-update: current predictions precede support adaptation, and a chosen transition affects the next batch. The secondary adapt-then-predict setting is separate. This prevents future-query input leakage.
- Local action regret compares branches from the same state and observed support. It is not described as full-stream optimality. The draft correctly rejects a fictitious dynamic oracle assembled from best local actions on another trajectory.
- A 45k/3k/2k CIFAR training/meta/calibration split is disclosed as a changed source regime, with all methods sharing it. Official test identities remain untouched. Labels for constructing controlled skew are evaluator metadata and are not runtime observations.
- Source training, auxiliary labels, candidate execution and feature costs are explicitly recognized. The report avoids treating no target labels at deployment as absence of offline supervision.
- Historical digit and external aggregate results are not used to validate the fresh proposal. No success on CIFAR-C/ImageNet-C/DomainNet/WILDS is invented.

## Execution details requiring explicit decisions

### 1. Define UPDATE's normalization semantics

The draft says one ETA-style reliable entropy update with a BN backbone. This leaves two materially different primitives: affine optimization using fixed live normalization buffers, or refreshing support normalization statistics and then optimizing affine parameters. A native ETA implementation can use current batch normalization, so the distinction affects the comparison with NORMALIZE and KEEP.

Suggested protocol sentence: “UPDATE uses [specified] statistics on support, changes [specified] buffers/affine parameters, and then scores the subsequent query with all statistics frozen. It is an ETA-inspired primitive; the complete native ETA/EATA comparator is separately implemented and named.” Choose the bracketed semantics before running.

### 2. Require pure feature observation forwards

The draft prohibits query-time buffer writes, but current-model feature extraction can itself mutate BN/teacher state if executed in training mode. That would make an allegedly skipped action adapt anyway.

Suggested protocol sentence: “Every inference pass used for source/current evidence is state-pure; only the declared action transition may change persistent state. Snapshot/restore covers RNG and counters as well as weights, buffers, optimizer, teacher and memory.” State-pure inference is also needed for KEEP and source fallback.

### 3. Formalize or exclude the optional source output choice

The main four-action transition menu is clear. SOURCE fallback is currently optional and separate. For the first experiment, explicitly exclude it from the learned menu and retain immutable SOURCE as a comparator, or encode a joint output-choice/transition action. Merely adding SOURCE to the four transitions without saying what happens to live state would undo the distinction established by the table.

Under predict-then-update, clarify that an output choice made after observing batch t applies to the designated future block. If fallback is allowed to choose the answer to the current batch from its current inputs, label that as a separate output-selection layer with its own costs and timing.

### 4. Match all development resources, not only scored outcomes

Equal numbers of scored action outcomes are necessary but do not alone equate unique labeled query images, reuse of those images, prefix-generation cost, candidate adaptation steps, or total support forward passes. Learning from different policy-generated states is intended; giving one collector more labeled evidence is not.

Suggested reporting: fix the labeled development identity pool and score budget; report per-method unique labels, scored action-state pairs, state-generation steps, candidate steps and total offline compute. Include plain equal-budget dataset aggregation. Separate selector-training/calibration image groups throughout trajectory collection, including prefixes. Generate development corruptions from permitted training identities rather than accidentally consuming official CIFAR-C test identities.

### 5. Specify evaluation identity reuse and prefix/query separation

Matching the present support/query sequence across histories is essential. Also record whether a query identity appeared earlier in a prefix or under another corruption, and prohibit that in the primary mechanism test if claiming an effect of inherited adaptation rather than repeated-example exposure. Repeated identities in later continual stress tests can be allowed explicitly, with dependence-aware uncertainty and all policies sharing the same stream.

These are implementation-free protocol decisions. There is no need to run tests to resolve them during this literature task.

## Selected citation and source verification

The requested links were reopened live:

| Link | Finding |
| --- | --- |
| [NOTE, arXiv 2208.05117](https://arxiv.org/abs/2208.05117) | Correct paper: Gong, Jeong, Kim, Kim, Shin and Lee. NeurIPS 2022 camera-ready version noted by arXiv. The nearby identifier 2208.05115 is an unrelated condensed-matter paper and must not replace it. |
| [NOTE, official proceedings](https://papers.nips.cc/paper_files/paper/2022/hash/ae6c7dbd9429b3a75c41b5fb47e57c9e-Abstract-Conference.html) | Correct title/authors, IABN and prediction-balanced reservoir mechanism; DOI 10.52202/068431-1976. |
| [Yu et al., arXiv 2307.03133](https://arxiv.org/abs/2307.03133) | Correct title, authors Yongcan Yu/Lijun Sheng/Ran He/Jian Liang, July 2023. Abstract confirms 13 methods/variants across CIFAR10/100-C, ImageNet-C, DomainNet and Office-Home and several access regimes. It is not evidence of a current 2026 SOTA. |
| [WILDS submission rules](https://wilds.stanford.edu/submit/) | Standard item 2 and nonstandard item 2 prohibit test-set training/selection; standard item 6 prohibits evaluation batch statistics. Draft wording matches these rules. |
| [WILDS leaderboard](https://wilds.stanford.edu/leaderboard/) | Confirms iWildCam macro F1, FMoW worst-region accuracy, Camelyon17 average accuracy, and historical ARM-BN/Test-time BN rows. Draft appropriately treats historical rows as insufficient authorization for a new test-trained submission. |

Other critical claims were checked against the earlier verifier primary-source passages and the researcher/benchmark ledgers: Agentic-TTT §2.2.2 and Appendix E; identifiability §§3–5; ASR methods/analysis; GALA §§2.2–2.3; Monitoring Risks Assumption 1/Proposition 1/§6; POEM future directions; Hybrid-TTN methods and offline batch setting. Reading scopes remain partial and explicit. SLRF full text remains inaccessible, and no novelty claim assumes it lacks the proposed experiment.

The synthesis cites a canonical merged record using descriptive labels in some places; source-key aliases in `citation-aliases.json` preserve the LSA and recovery-complexity duplicates. No wrong-title citation was found among the links checked in this pass. This is not a network audit of all 103 records or a claim to have read every source in full.

## Remaining novelty boundary

The proposed architecture and learning principle remain established ingredients. The potential contribution is the demonstrated **size, mechanism and residual difficulty** of visual selector failure under policy-generated adaptation states. The study must be abandoned or reframed if ordinary current-output features, optimizer reset, ASR/GALA or standard aggregation remove the supposed problem. The draft states that boundary clearly and does not promise acceptance or genuine novelty before those checks.

## Targeted recheck after revision

The revised report and the now-present `experiments/002-state-conditioned-selection.md` were reread. **No blocking scientific or document error remains in the reviewed definitions.** This is document review only; no implementation behavior is verified.

- UPDATE is now explicitly a frozen-live-BN-statistics affine entropy primitive, not native ETA/Tent; NORMALIZE changes only declared buffers. Their distinction is clear.
- The primary selector menu excludes SOURCE as an answer action. A future fallback must model the output/transition contract separately. KEEP/RESET/source-baseline semantics remain distinct.
- Observation forwards are state-pure, with RNG/counters included in the snapshot contract; query scoring has no gradient, BN or memory mutations.
- Development comparisons now match unique query-label identities and reuse, action scoring, candidate steps, support forwards and state-collection compute, or report a frontier when simultaneous matching is impossible. Separate fixed calibration streams are retained.
- Full Experiment 002 preserves realistic/noncollapsed cases, simple reset and optimizer controls, rich current-model baselines, independent query repetition, tie-aware margins and autonomous rollout evaluation. Its local versus replay versus dynamic oracle distinctions are correct.
- Root reported adding primary prefix/query identity disjointness. That amendment was not yet visible during the last targeted read; it should prohibit current support/query identities in earlier prefixes for the mechanism experiment, while explicitly allowing paired branches to share their fixed present sequence.

One nonblocking run-manifest clarification remains: a proposed support size of 64 and query window of 512 should not be conflated with the actual next stream batch when describing “one-step” loss. State whether 512 is a frozen post-action risk-estimation window with subsequent KEEP, distinct from the actual next-batch score, or use the next batch as the primary one-step target. The protocol already asks that multi-batch continuation transitions be fixed, so the issue is naming and target alignment rather than future-information leakage.

Exact numerical margins, corruption-family membership, architecture/checkpoint, optimizer and compute budget remain legitimately unchosen until the prospective protocol is frozen for authorized execution. Their absence is not an experimental result or a reason to claim the method works.

### Final delivered-paragraph check

The final amendments were read in both delivered artifacts. The primary one-decision target is now explicitly the next 64-example prediction block. The separate 512-example post-action window fixes subsequent transitions to KEEP and is excluded from one-step training/rollout results. Prefix, support, query and fresh query-replication original-ID pools are disjoint in local matched cases; sibling corruptions cannot expose query identities in a prefix. Deliberate matched branches share the same present sequence, with dependence retained, and later autonomous repetition is separately disclosed.

**Final disposition: the earlier clarification requests are resolved. No remaining blocking document error was found in this verification. Experiments remain planned and unexecuted; this finding is not implementation validation or proof of novelty.**

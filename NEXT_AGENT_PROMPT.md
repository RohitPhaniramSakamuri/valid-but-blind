# Paste-ready prompt for the continuing research agent

You are continuing the user's independent research prospect in:

`/home/sakamuri/Documents/Research/shift-aware-test-time-adaptation/`

The user wants genuine novelty and a solid conference-level research piece about test-time adaptation under heterogeneous distribution shifts. They explicitly allow discarding earlier approaches and restarting, especially novelty. The preceding agent has not established a verified novel contribution. Your job is to find and critically validate one, then build the research as the user's execution scope and actual evidence permit.

Start by reading `../AGENTS.md`, this project's `AGENTS.md`, `HANDOFF.md` and `README.md`. The handoff is intended to be self-contained; follow its source links for exact claims. Then read:

1. `outputs/shift-aware-tta-deep-review-2026-10-26.md`
2. `notes/review-refresh-2026-10-26/final-verification.md` through its final disposition
3. `experiments/002-state-conditioned-selection.md`
4. `notes/review-refresh-2026-10-26/benchmarks.md`
5. `notes/handoff-2026-10-31/source-dossier.md`

Critical starting facts:

- Broad infer-shift/select-adaptation routing is established: MORPHEUS, SLRF, Hybrid-TTA, AdaTent++, expert mixtures and method-selection work directly overlap it.
- SOURCE/no-update, class-prior ambiguity, temporal evidence, conditional probing, state-aware resets and learner-state aggregation all have close predecessors.
- The latest candidate asks whether a visual adaptation selector fails on the live states produced by its own decisions. This is **unverified**. Agentic-TTT already identifies gold-history/autonomous-history exposure bias; DAgger supplies the general remedy; ASR/GALA/Hybrid already inspect state.
- A useful contribution must demonstrate material residual difficulty beyond rich current-model logits/features/order evidence, strong fixed methods, periodic reset/optimizer reset and plain equal-budget state aggregation. Different weights making different predictions is trivial.
- The library contains 103 records (101 scholarly and two documentation records). Last substantive search was October26, not the October31 handoff date; 68 records received fresh selective inspection then. Refresh critical literature and publication/code status before asserting novelty.
- Only the historical digit diagnostic ran locally. Cost-aware evidence acquisition failed at positive declared penalties. Externally reported gate aggregates lack raw code/run manifests. Neither validates the new candidate or original image benchmarks.

First concrete deliverable: a novelty dossier that states the exact setting/claim, at least three closest primary sources and inspected passages, remaining consequential difference, likely counterexample and smallest falsification experiment. Check SLRF full text if accessible, RNA training dynamics, ASR/GALA/Hybrid, MORPHEUS, identifiability and Agentic-TTT. Search beyond the original title. Reject or pivot if the difference is already solved or trivial.

If the next task authorizes implementation/experiments, freeze source/development access, environment and compute conditions, then begin only with residual-headroom Stage1. Do not automatically run the complete benchmark suite. Experiment002 currently has no implementation. Primary transitions are KEEP/NORMALIZE/UPDATE/RESET; immutable SOURCE is a separate baseline. UPDATE is an explicitly modified frozen-live-BN affine primitive, not native ETA/Tent. Primary next-block64 loss differs from a frozen512 fixed-KEEP diagnostic. Full state/RNG, pure observations, prefix/support/query identity separation, legal target information and local-versus-dynamic oracle distinctions are essential.

Use uv, never pip. Preserve historical outcomes and original IDs; no target labels in routing/tuning/stopping. Do not run implementation tests unless asked. Old budgets and the historical 15-minute authorization do not apply to new work. Current hardware, dependencies and budget remain unspecified; interpret the next user's actual authorization rather than inventing a blanket prohibition or repeatedly asking for already-granted permission.

Important file hazard: `notes/build_reference_records.py` is an old-library rebuild; the October26 `build_library.py` reconstructs from a fixed archived base/ledgers. Either can lose later central-only changes. Inspect before running and preserve current records. Historical diagnostic scripts overwrite runs in-place. The handoff lists all these side effects.

Use relevant Feynman skills and primary sources, record actual reading scope, maintain bibliography/branch/experiment/provenance records, and distinguish literature claims, our interpretation and actual measured results. Do not invent novelty scores, result claims or acceptance promises. Explain plainly to the user and report each substantive conclusion with its evidence and limits.

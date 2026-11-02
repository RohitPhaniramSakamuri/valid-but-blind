# Handoff package — 31 October 2026

Project: `/home/sakamuri/Documents/Research/shift-aware-test-time-adaptation/`.

Start with [HANDOFF.md](../../HANDOFF.md). It consolidates user intent, scientific findings, prior-art collisions, historical results, current candidate/protocol, limitations, implementation hazards and continuation milestones. [NEXT_AGENT_PROMPT.md](../../NEXT_AGENT_PROMPT.md) is a short prompt to give the next agent.

This directory contains:

- [source-dossier.md](source-dossier.md): a readable export of every one of the 103 source records, including reading histories and remaining metadata.
- [artifact-manifest.json](artifact-manifest.json): relative paths, role descriptions, file sizes and SHA-256 hashes of project artifacts, excluding transient environments/caches and the manifest itself.
- [export_handoff.py](export_handoff.py): standard-library documentation exporter; reads the existing scientific catalog and writes only the dossier and inventory.

The source index, BibTeX, primary evidence and experiment artifacts remain at their established project paths. Nothing is moved or deleted. There is no separate archive to unpack: give the successor this project directory and access to the parent instructions/templates. If copying to another system, preserve relative paths and provide the parent instructions as well.

Last substantive literature investigation: **26 October 2026**. Handoff preparation date: **31 October 2026**. Source scopes and publication/code qualifications are historical records; exporting them does not freshly verify them. The proposed live-state study remains planned and unimplemented.

To regenerate this documentation export after intentional record changes:

```bash
uv run --no-project --no-python-downloads --python /usr/bin/python3 notes/handoff-2026-10-31/export_handoff.py
```

Run from the project root. It overwrites this directory's dossier and inventory, so preserve them first if their exact earlier snapshot matters. It does not launch experiments, invoke old bibliography rebuilders, access the network or install dependencies.

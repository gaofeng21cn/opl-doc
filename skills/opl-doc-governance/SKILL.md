---
name: "opl-doc-governance"
description: "Compatibility entry for OPL Doc. Use when an existing prompt, install, or session still asks for OPL Doc Governance; follow OPL Doc for OPL-family developer documentation lifecycle governance, live-truth README/docs audits, one-document-one-role taxonomy, active plan foldback, tombstones, and opl-doc-doctor workflows."
---

# OPL Doc Governance Compatibility Entry

This skill name is retained for existing prompts and installed workflows. The canonical skill is `opl-doc`.

When this skill triggers, follow `../opl-doc/SKILL.md` as the source of truth. Treat `$opl-doc-governance` exactly like `$opl-doc`; do not create a second workflow, second taxonomy, or second install surface.

Quick routing:

- Use `opl-doc-doctor doctor <repo-root> --format json` only as a preflight risk map.
- For OPL series, multi-repo, long-running, stale-doc cleanup with edits, or worktree/subagent/absorb-back requests, create or resume `/goal`.
- Govern the whole `README*` plus `docs/**/*.md` portfolio against live repo truth.
- Keep one document to one role and route process history to history/tombstone surfaces.
- Retire stale modules, interfaces, tests, docs, workflows, and entrypoints directly when replacement plus no-active-caller evidence exists; do not add compatibility aliases, facades, wrappers, or compatibility prose to governed repos.

---
name: "opl-doc"
description: "Short entry for OPL Doc Governance. Use when governing OPL-family developer documentation lifecycle, auditing README/docs claims against live repo truth, enforcing one-document-one-role taxonomy, folding active plans into canonical docs/history/tombstones, directly retiring stale docs without compatibility surfaces, or running opl-doc-doctor."
---

# OPL Doc

This is the short skill name for OPL Doc Governance.

Follow the canonical workflow in `../opl-doc-governance/SKILL.md`. The short name exists so users can ask for `$opl-doc` or "OPL Doc" on new machines without changing the plugin repository name or breaking existing `$opl-doc-governance` installs.

Operationally, treat this skill exactly as OPL Doc Governance:

- Read the target repo's `AGENTS.md`, `TASTE.md` when present, canonical docs, active truth owner, and live source/contracts/tests/read-model surfaces before editing.
- Use `opl-doc-doctor doctor <repo-root> --format json` only as a preflight risk map.
- For OPL series, multi-repo, long-running, stale-doc cleanup with edits, or worktree/subagent/absorb-back requests, create or resume `/goal`.
- Audit the whole `README*` plus `docs/**/*.md` portfolio, not only active gap docs.
- Keep one document to one role; move process history to history/tombstone surfaces.
- Retire stale modules, interfaces, tests, docs, workflows, and entrypoints directly when replacement plus no-active-caller evidence exists; do not add compatibility aliases, facades, wrappers, or compatibility prose.
- Before closeout, run repo-native verification and confirm active truth, canonical docs, coverage ledger, and next-round prompt reflect only remaining work.

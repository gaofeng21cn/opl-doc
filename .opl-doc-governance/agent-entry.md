# OPL Doc Governance Agent Entry

Owner: `OPL Doc Governance`
Purpose: `repo_native_agent_entry`
State: `active_entry`
Machine boundary: This file is agent-readable guidance; machine truth remains in source, tests, contracts, CLI/API output, runtime ledgers, and receipt refs.

## First agent move

1. Read this file and `.opl-doc-governance/config.json`.
2. Read the target repo `AGENTS.md`.
3. Read `TASTE.md` when present.
4. Read canonical current docs before supporting docs: `README.md`, `docs/README.md`, `docs/project.md`, `docs/status.md`, `docs/architecture.md`, `docs/invariants.md`, `docs/decisions.md`, and active gap references when present.
5. Run the OPL Doc Governance doctor from the installed skill or governance tool checkout, targeting this repo root, then verify important findings by reading files.

## Operating mode

- Repo profile: `codex_plugin`.
- For long-horizon, multi-repo, edit-heavy, worktree/subagent, or absorb-back-to-main requests, create or resume a `/goal` before execution.
- For a short single-repo read-only audit, start with doctor output and direct file reads.
- Treat docs as developer context, not production readiness evidence.

## Lifecycle policy

- Each long-lived document has one owner, one purpose, one state, and one machine boundary.
- Current truth belongs in canonical docs.
- Active work belongs in `docs/active/`.
- Historical process, retired plans, and tombstones belong in `docs/history/`.
- Stale modules, interfaces, tests, aliases, and compatibility wording are retired directly after active callers move.

## Closeout gate

- Canonical docs reflect current truth.
- Active docs contain only current plans, gaps, and baton material.
- History or tombstone files hold necessary provenance.
- Prose does not contradict source, tests, contracts, CLI/API output, runtime ledgers, or receipt refs.
- Final verification ran on the target repo's final main checkout.

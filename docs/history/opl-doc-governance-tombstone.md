# `opl-doc-governance` Tombstone

Owner: `One Person Lab`
Purpose: `retired_entrypoint_provenance`
State: `history_tombstone`
Machine boundary: Human-readable provenance only. Active plugin behavior is defined by `.codex-plugin/plugin.json`, `skills/opl-doc/SKILL.md`, `skills/opl-doc/agents/openai.yaml`, installer checks, and tests.

`opl-doc-governance` was the previous document-governance skill name. The active canonical plugin and skill surface is now `opl-doc`.

Retirement rule:

- Do not expose `opl-doc-governance` as a skill, UI entry, README quick-start entry, or active workflow.
- Do not add aliases, facades, wrappers, or prose that presents the old name as usable.
- Do not restore installer cleanup hooks, marketplace cleanup branches, or tests that keep the old name in an active install path.

Use `opl-doc` for all current documentation lifecycle governance work.

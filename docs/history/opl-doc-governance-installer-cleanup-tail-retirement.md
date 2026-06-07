# `opl-doc-governance` Installer Cleanup Tail Retirement

Owner: `OPL Doc`
Purpose: `retired_installer_cleanup_tail_provenance`
State: `history_tombstone`
Machine boundary: Human-readable provenance only. Active install behavior is defined by `scripts/install_local_plugin.py`, `.codex-plugin/plugin.json`, `skills/opl-doc/SKILL.md`, `skills/opl-doc/agents/openai.yaml`, and tests.

`opl-doc-governance` was already a retired entrypoint. The remaining installer branch that deleted `~/plugins/opl-doc-governance` and removed marketplace entries with that name has now been retired as migration tail cleanup.

Current install behavior is intentionally single-surface:

- install or replace `~/plugins/opl-doc`
- register only `opl-doc` in the personal marketplace
- create the `opl-doc-doctor` command symlink
- verify the canonical `opl-doc` plugin files

Do not restore old-name cleanup hooks, marketplace pruning branches, compatibility aliases, or tests that keep `opl-doc-governance` in the active installer path.

# OPL Doc Governance

<p align="center">
  <a href="./README.md"><strong>English</strong></a> | <a href="./README.zh-CN.md">中文</a>
</p>

<p align="center"><strong>Document lifecycle governance for long-running AI software development</strong></p>
<p align="center">A Codex skill and CLI doctor for keeping developer docs current, layered, and useful for autonomous engineering loops.</p>

## Why This Exists

Long-running AI development fails when documentation becomes a second, stale source of truth. Old plans remain active, historical checklists keep growing, retired interfaces look alive, and agents waste time reconciling contradictory docs.

OPL Doc Governance turns document cleanup into a repeatable workflow. It helps an agent read the current repository truth, classify each document by lifecycle role, retire stale material, fold history into archives or tombstones, and close the loop with verification.

It is OPL-native by design: OpenArc, OpenSpec, Spec Kit, Agent OS, and similar projects are useful references, but this repository does not migrate OPL-family projects into an external file layout.

## What It Provides

- **Codex skill**: a reusable workflow for developer-document lifecycle governance.
- **Automatic goal mode**: for OPL series, multi-repo, long-running, or edit-heavy cleanup, the skill tells the agent to create or resume a `/goal` before execution.
- **Read-only doctor**: a CLI scan that reports canonical doc presence, lifecycle headers, stale active wording, and long incremental-list risks.
- **OPL series workflow**: a generated plan for `one-person-lab`, `med-autoscience`, `med-autogrant`, `redcube-ai`, `opl-meta-agent`, and future OPL-compatible repositories.
- **Change packet templates**: a small active-work packet for non-trivial documentation or engineering changes.

## Quick Start

Install it as a local Codex plugin:

```bash
python3 scripts/install_local_plugin.py
```

Restart Codex, then use one sentence:

```text
Use OPL Doc Governance to govern this repo's developer documentation lifecycle.
```

For the full OPL series:

```text
Use OPL Doc Governance to govern the OPL series developer documentation lifecycle.
```

For OPL series, multi-repo cleanup, long-running autonomous work, or tasks that mention worktrees, subagents, or absorbing back to `main`, the skill should create or resume a `/goal` automatically. Short single-repo read-only audits start with the doctor and do not force goal mode.

## CLI

Run a read-only audit:

```bash
python3 scripts/opl_doc_doctor.py doctor /path/to/repo
python3 scripts/opl_doc_doctor.py doctor /path/to/repo --format json
```

Generate the OPL series workflow:

```bash
python3 scripts/opl_doc_doctor.py family-plan --format markdown
python3 scripts/opl_doc_doctor.py family-plan --format json
```

Use local workspace paths when needed:

```bash
python3 scripts/opl_doc_doctor.py family-plan --workspace-root /path/to/workspace --format json
```

Override or add repositories:

```bash
python3 scripts/opl_doc_doctor.py family-plan --repo award=award-agent --format markdown
```

## Lifecycle Model

Every long-lived developer document should have one job:

| Lifecycle role | Where it belongs |
| --- | --- |
| Current truth | `README*`, `docs/README*`, `docs/project.md`, `docs/status.md`, `docs/architecture.md`, `docs/invariants.md`, `docs/decisions.md` |
| Active work | `docs/active/` |
| Product, runtime, source, and delivery support | `docs/product/`, `docs/runtime/`, `docs/source/`, `docs/delivery/` |
| Stable policies, specs, and references | `docs/policies/`, `docs/specs/`, `docs/references/` |
| Historical process, retired plans, tombstones | `docs/history/` |
| Machine truth | source, tests, contracts, CLI/API output, runtime ledger, receipt refs |

The doctor is intentionally read-only. It can identify risks, but it does not declare a repository production-ready and it does not replace code, tests, contracts, read models, or owner receipts.

## Change Packets

For non-trivial work, use a short packet under `docs/active/changes/<change-id>/`:

```text
intent.md
design.md
tasks.md
verification.md
foldback.md
```

When the change is complete, fold current facts back into canonical docs and move process material to history or tombstone references.

## Technical Notes

<details>
  <summary><strong>Developer and agent details</strong></summary>

### Repository Layout

- `.codex-plugin/plugin.json`: local Codex plugin manifest.
- `skills/opl-doc-governance/SKILL.md`: the skill entry used by Codex.
- `skills/opl-doc-governance/agents/openai.yaml`: UI metadata and default prompt.
- `scripts/opl_doc_doctor.py`: read-only doctor and family-plan generator.
- `scripts/install_local_plugin.py`: local plugin installer.
- `templates/`: goal and change-packet templates.
- `tests/`: pytest coverage for the doctor, goal mode, and installer.

### Verification

```bash
python3 -m pytest -q
python3 scripts/opl_doc_doctor.py doctor .
python3 scripts/opl_doc_doctor.py family-plan --format markdown
bash scripts/verify.sh
```

### Boundaries

- This repository governs developer documentation lifecycle and engineering closeout workflows.
- It does not own OPL series project truth, runtime truth, domain verdicts, artifact authority, or owner receipts.
- It keeps OPL-native taxonomy and does not migrate repositories into OpenArc, OpenSpec, Spec Kit, or Agent OS layouts.
- Public defaults use repository names, not local absolute paths. Use `--workspace-root` or `--repo ID=PATH` for local machines.

### Documentation

- [Documentation index](./docs/README.md)
- [Project overview](./docs/project.md)
- [Current status](./docs/status.md)
- [Architecture](./docs/architecture.md)
- [Invariants](./docs/invariants.md)
- [Decisions](./docs/decisions.md)
- [Usage](./docs/usage.md)

</details>

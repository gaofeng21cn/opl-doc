# OPL Doc Governance

<p align="center">
  <a href="./README.md"><strong>English</strong></a> | <a href="./README.zh-CN.md">中文</a>
</p>

<p align="center"><strong>An OPL-native documentation steward for long-running AI engineering</strong></p>
<p align="center">Keep repo docs current, layered, and useful when Codex or another agent needs to understand the goal and keep developing over time.</p>

<table>
  <tr>
    <td width="33%" valign="top">
      <strong>Who It Serves</strong><br/>
      Developers and AI operators maintaining OPL-family or OPL-compatible repositories
    </td>
    <td width="33%" valign="top">
      <strong>What It Organizes</strong><br/>
      Ideal-state references, Active Truth plans, history/tombstones, and verification evidence
    </td>
    <td width="33%" valign="top">
      <strong>How To Start</strong><br/>
      Ask Codex to use OPL Doc Governance for the repo or the OPL series
    </td>
  </tr>
</table>

## Why OPL Doc Governance

AI agents can keep building only when the repository tells them what is true now. In long-running development, old plans stay in active docs, historical checklists keep growing, retired interfaces look alive, and the next agent has to spend context reconstructing the real state.

OPL Doc Governance turns that cleanup work into a repeatable steward workflow. It helps Codex read the current repository truth, rewrite active docs toward the single best Active Truth, retire stale surfaces, fold process material into archives or tombstones, and finish with fresh verification evidence.

The goal is simple: a user should be able to ask for document governance in one sentence, and the agent should know how to start, when to create a `/goal`, how to avoid stale-doc pollution, and how to close the loop.

## What It Provides

- **A Codex skill for document stewardship**: the agent gets a stable reading order, cleanup policy, and closeout discipline.
- **Repo-native reading**: the doctor reports the target repo's own agent guidance, canonical docs, machine-truth surfaces, and verification commands.
- **Automatic long-horizon mode**: OPL series, multi-repo, or edit-heavy work creates or resumes a `/goal` without the user remembering a long prompt.
- **A read-only doctor**: the CLI reports missing canonical docs, missing lifecycle signals, stale active wording, and long incremental-list risks.
- **An autonomous development loop**: ideal state stays as the durable user input; governance refreshes current completion progress, current-state gaps, and the next-round agent prompt from live repo truth.
- **An Active Truth plan template**: a recommended shape for the single active owner of progress, gaps, executable next-round prompts, routing decisions, and foldback targets.
- **An OPL series workflow**: generated guidance for `one-person-lab`, `med-autoscience`, `med-autogrant`, `redcube-ai`, `opl-meta-agent`, and future OPL-compatible repositories.
- **Change packet templates**: a compact active-work packet for changes that need intent, design, tasks, verification, and foldback.

## One-Sentence Quick Start

Install it as a local Codex plugin:

```bash
python3 scripts/install_local_plugin.py
```

This copies the plugin into `~/plugins/opl-doc-governance`, registers it in the personal marketplace, and creates a user-level `opl-doc-doctor` command under `~/.local/bin`. It does not write anything into the repos being governed.

Restart Codex, then use one sentence:

- "Use OPL Doc Governance to govern this repo's developer documentation lifecycle."
- "Use OPL Doc Governance to govern the OPL series developer documentation lifecycle."
- "Use OPL Doc Governance to clean stale active docs and fold completed plans into history."

For OPL series, multi-repo cleanup, long-running autonomous work, or tasks that mention worktrees, subagents, or absorbing back to `main`, the skill should create or resume a `/goal` automatically. Short single-repo read-only audits start with the doctor and do not force goal mode.

## How It Works

- The agent reads the repository guidance, current docs, and live code or contract surfaces before editing.
- The doctor gives a quick risk map without changing the target repository.
- The skill treats ideal-state references as the user's maintained intent and derives current progress, open gaps, and the next-round agent prompt from live code, contracts, tests, CLI/read-models, and docs.
- If a repo lacks a stable active owner, the agent can use `templates/active-truth-plan.md` as the shape for the single Active Truth plan.
- The skill routes each section by role and checks closeout so closed gaps, process packets, and stale wording do not stay in active paths.
- The skill classifies docs as current truth, active plan, support reference, history, tombstone, or stale pollution.
- Active docs are rewritten to current truth; historical process material moves to history or tombstone references.
- Completed work folds back into canonical docs and ends with repo-native verification.

OPL Doc Governance is OPL-native by design. OpenArc, OpenSpec, Spec Kit, Agent OS, and similar projects are useful references, but this repository does not migrate OPL-family projects into an external file layout.

## CLI

Run a read-only audit:

```bash
opl-doc-doctor doctor /path/to/repo
opl-doc-doctor doctor /path/to/repo --format json
```

Generate the OPL series workflow:

```bash
opl-doc-doctor family-plan --format markdown
opl-doc-doctor family-plan --format json
```

Use local workspace paths when needed:

```bash
opl-doc-doctor family-plan --workspace-root /path/to/workspace --format json
```

Override or add repositories:

```bash
opl-doc-doctor family-plan --repo award=award-agent --format markdown
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

The doctor is intentionally read-only and lightweight. It can identify structural risks, but it does not manage document meaning, declare a repository production-ready, or replace Codex reading code, tests, contracts, read models, or owner receipts.

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
- `templates/`: Active Truth plan, goal, and change-packet templates.
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

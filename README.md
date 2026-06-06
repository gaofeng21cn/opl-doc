# OPL Doc

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
      Ask Codex to use OPL Doc for the repo or the OPL series
    </td>
  </tr>
</table>

## Why OPL Doc

AI agents can keep building only when the repository tells them what is true now. In long-running development, old plans stay in active docs, historical checklists keep growing, retired interfaces look alive, and the next agent has to spend context reconstructing the real state. OPL Doc prevents that documentation drift so every AI engineering handoff can start from current facts, clear entry points, and a verifiable next step.

OPL Doc turns that cleanup work into a repeatable steward workflow. It helps Codex read the current repository truth, audit every README and docs section against that truth, rewrite active docs toward the single best Active Truth, make each document keep one job, retire stale surfaces without compatibility prose, fold process material into archives or tombstones, and finish with fresh verification evidence.

`opl-doc` is the canonical plugin and skill name.

It also helps OPL-family repositories keep one current narrative: user entries explain product value, developer entries explain boundaries and verification, and stale technical wording is folded into history or tombstones. OPL Doc only checks whether those document claims match each repo's current truth; it does not become a second source of truth.

The goal is simple: a user should be able to ask for document governance in one sentence, and the agent should know how to start, when to create a `/goal`, how to avoid stale-doc pollution, and how to close the loop.

## What It Provides

- **A stable document-steward entry**: Codex knows what to read first, how to judge stale content, and how to close out without the user repeating a long prompt.
- **Current-fact reading**: it starts from the target repo's guidance, README, docs, code, contracts, and verification entries before deciding what prose needs to change.
- **README narrative repair**: it checks whether entry pages explain product value, usage scenarios, and how to start, while keeping technical detail in developer sections.
- **Stale-plan cleanup**: completed plans, retired routes, and process material are folded into history or tombstones instead of staying in active docs.
- **Whole-portfolio cleanup**: every `README*` and `docs/**/*.md` file is reviewed so each long-lived document keeps one clear job.
- **OPL series governance**: generated guidance for `one-person-lab`, `med-autoscience`, `med-autogrant`, `redcube-ai`, `opl-meta-agent`, `one-person-lab-app`, and future compatible repositories.
- **Change packet templates**: compact temporary packets for work that needs intent, design, tasks, verification, and foldback.

## One-Sentence Quick Start

For a complete new-machine Codex setup that includes OPL runtime, MAS/MAG/RCA/OMA agent surfaces, OPL Flow, OPL Doc, One Person Lab App, and companion tools, start from the [One Person Lab new-machine Codex bootstrap guide](https://github.com/gaofeng21cn/one-person-lab/blob/main/docs/references/current-support/opl-new-machine-codex-bootstrap.md).

Install it as a local Codex plugin:

```bash
git clone git@github.com:gaofeng21cn/opl-doc.git
cd opl-doc
python3 scripts/install_local_plugin.py
python3 scripts/install_local_plugin.py --verify-only
```

This copies the plugin into `~/plugins/opl-doc`, registers it in the personal marketplace, creates a user-level `opl-doc-doctor` command under `~/.local/bin`, and installs the `opl-doc` skill entry. It also removes stale retired plugin registrations when present. It does not write anything into the repos being governed.

Restart Codex, then use one sentence:

- "Use OPL Doc to govern this repo's developer documentation lifecycle."
- "Use OPL Doc to govern the OPL series developer documentation lifecycle."
- "Use OPL Doc to clean stale active docs and fold completed plans into history."

For OPL series, multi-repo cleanup, long-running autonomous work, or tasks that mention worktrees, subagents, or absorbing back to `main`, the skill should create or resume a `/goal` automatically. The default OPL series is six repos and 12 primary reference documents. Short single-repo read-only audits start with the doctor and do not force goal mode.

## How It Works

- The agent reads repository guidance and current docs before editing. Existing prose is treated as claims to verify against code, contracts, tests, command output, and runtime evidence.
- The doctor gives a quick risk map without changing the target repository; it is not the governance input or task list.
- The skill treats ideal-state references as the user's maintained intent and derives current progress, open gaps, and the next-round agent prompt from the current repository facts; canonical docs are reconciled into those facts rather than trusted as proof by themselves.
- The agent reviews substantive document claims against current repository facts before editing, then rewrites content, merges duplicate responsibilities, and routes stale material.
- The agent audits the whole doc portfolio, not only the gap document: each long-lived document must retain one owner, one purpose, one state, and one machine boundary.
- If a repo lacks a stable active owner, the agent can use `templates/active-truth-plan.md` as the shape for the single Active Truth plan.
- The skill routes each section by role and checks closeout so closed gaps, process packets, and stale wording do not stay in active paths.
- The skill classifies docs as current truth, active plan, support reference, history, tombstone, or stale pollution.
- Active docs are rewritten to current truth; historical process material moves to history or tombstone references.
- Outdated modules, interfaces, tests, docs, workflows, and entrypoints are retired directly after replacement and no-active-caller evidence exists; the governance output must not add compatibility aliases, facades, wrappers, or "legacy still works" prose.
- OPL series governance runs as long-horizon tranches. A verified and absorbed lane is only a tranche closeout; the global `/goal` stays open while the coverage ledger still has unreviewed docs, unresolved stale/retire candidates, or carry-forward gaps.
- Completed work folds back into canonical docs and ends with repo-native verification.

OPL Doc is OPL-native by design. OpenArc, OpenSpec, Spec Kit, Agent OS, and similar projects are useful references, but this repository does not migrate OPL-family projects into an external file layout.

The default OPL series workflow covers the six governed repo set: OPL, MAS, MAG, RCA, OMA, and the App. Support repos such as `opl-doc` and `opl-aion-shell` are explicit extensions for workflow or shell-carrier tasks; they are not default Foundry Agent truth owners.

## CLI

Run a read-only audit:

```bash
opl-doc-doctor doctor /path/to/repo
opl-doc-doctor doctor /path/to/repo --format json
```

Check or write an OPL-native repo profile:

```bash
opl-doc-doctor native-check /path/to/repo
opl-doc-doctor native-sync /path/to/repo
opl-doc-doctor native-sync /path/to/repo --apply
```

`native-sync` defaults to dry-run. With `--apply`, it writes only
`contracts/opl-native-profile.json`. That file is a plugin sync declaration:
it records the repo profile, Active Truth owner, canonical docs, taxonomy dirs,
machine-truth surfaces, repo-owned paths, and verification commands. It is
not a second source of project, runtime, delivery, or quality truth.

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

Every long-lived developer document should have one job. If a document mixes current truth, active plan, support reference, execution log, and history, governance picks the canonical owner for each role, moves useful content there, and archives, tombstones, or deletes the duplicate material.

| Lifecycle role | Where it belongs |
| --- | --- |
| Current truth | `README*`, `docs/README*`, `docs/project.md`, `docs/status.md`, `docs/architecture.md`, `docs/invariants.md`, `docs/decisions.md` |
| Active work | `docs/active/` |
| Product, runtime, source, and delivery support | `docs/product/`, `docs/runtime/`, `docs/source/`, `docs/delivery/` |
| Stable policies, specs, and references | `docs/policies/`, `docs/specs/`, `docs/references/` |
| Historical process, retired plans, tombstones | `docs/history/` |
| Machine truth | source, tests, contracts, CLI/API output, and runtime evidence |

The doctor is intentionally read-only and lightweight. It can identify structural risks, but it does not manage document meaning, provide the governance task list, declare a repository production-ready, or replace Codex reading code, tests, contracts, read models, or runtime evidence.

`family-plan` is likewise a workflow map, not a second source of repository truth. It keeps support repos as extension-only inputs and leaves current truth in each governed repo's own canonical docs, contracts, tests, and runtime evidence.

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
- `skills/opl-doc/SKILL.md`: canonical Codex skill entry.
- `skills/opl-doc/agents/openai.yaml`: UI metadata and default prompt.
- `scripts/opl_doc_doctor.py`: read-only doctor and family-plan generator.
- `scripts/opl_doc_doctor.py native-check|native-sync`: repo-native profile check/sync surface for `contracts/opl-native-profile.json`.
- `scripts/install_local_plugin.py`: local plugin installer.
- `docs/history/opl-doc-governance-tombstone.md`: provenance for the retired `opl-doc-governance` entrypoint.
- `templates/`: Active Truth plan, goal, and change-packet templates.
- `tests/`: pytest coverage for the doctor, goal mode, and installer.

### Verification

```bash
python3 -m pytest -q
python3 scripts/opl_doc_doctor.py doctor .
python3 scripts/opl_doc_doctor.py family-plan --format markdown
python3 scripts/opl_doc_doctor.py native-sync .
bash scripts/verify.sh
```

### Boundaries

- This repository governs developer documentation lifecycle and engineering closeout workflows.
- It does not own OPL series project truth, runtime truth, domain verdicts, artifact authority, quality verdicts, owner receipts, production readiness, or the default Foundry Agent truth set.
- It keeps OPL-native taxonomy and does not migrate repositories into OpenArc, OpenSpec, Spec Kit, or Agent OS layouts.
- Public defaults use repository names, not local absolute paths. Use `--workspace-root` or `--repo ID=PATH` for local machines.
- OPL-family root READMEs are user-facing by default: they should start from problems, value, and usage scenarios. Terms such as `executor-first`, stage, route, receipt, typed blocker, and Tool Affordance Boundary belong in folded Agent / developer / operator sections or canonical technical docs.

### Documentation

- [Documentation index](./docs/README.md)
- [Project overview](./docs/project.md)
- [Current status](./docs/status.md)
- [Architecture](./docs/architecture.md)
- [Invariants](./docs/invariants.md)
- [Decisions](./docs/decisions.md)
- [Usage](./docs/usage.md)

</details>

---
name: opl-doc-governance
description: Use when governing OPL-family developer documentation lifecycle, auditing stale docs, folding active plans into canonical docs/history/tombstones, creating long-horizon change packets, or running the OPL docs doctor across one-person-lab, med-autoscience, med-autogrant, redcube-ai, opl-meta-agent, or adjacent OPL-compatible repositories.
---

# OPL Doc Governance

Use this skill for developer-document governance: helping AI maintain the current single Active Truth from ideal state and live repo truth, derive current completion progress, maintain current-state gaps and next-round agent prompts, retire stale docs, and close the software-engineering loop. Do not use it for domain truth, runtime provider ownership, artifact authority, quality verdicts, or owner receipts.

## First Move

1. Read the target repo's `AGENTS.md`.
2. Read `TASTE.md` when present.
3. Read canonical current docs before touching supporting docs:
   - `README.md`
   - `docs/README.md`
   - `docs/project.md`
   - `docs/status.md`
   - `docs/architecture.md`
   - `docs/invariants.md`
   - `docs/decisions.md`
   - `docs/active/current-state-vs-ideal-gap.md`
4. Run the doctor when available:

```bash
opl-doc-doctor doctor <repo-root> --format json
```

Use doctor output as evidence, then verify important claims by reading files.

## Goal Mode

When the user asks for OPL series governance, multi-repo cleanup, long-running autonomous development, stale-doc cleanup with edits, or anything that mentions worktrees/subagents/absorbing back to `main`, create or resume a `/goal` before execution. The user should not have to remember to ask for `/goal`.

Use this objective shape:

```text
使用 OPL Doc Governance，自动创建或延续 /goal，治理 OPL series 的开发文档生命周期；以各 repo 的 ideal-state reference 和 single Active Truth plan 为主要参考，根据 live code、contracts、tests、CLI/read-model 与 docs 的当前事实，重写维护当前完成进度、现状与理想态差距、下一轮 Agent prompt；逐条评估 README* 与 docs/**/*.md 下其他文档，清理归档过时内容，避免二次污染；保证每个文档只有唯一任务和定位，active docs 不保存执行流水或历史增量日志，过时模块/接口/测试按理想态直接退役且不保留兼容面；可以并行使用 subagent/worktree，每条线完成后验证、提交、吸收回 main 并清理；最终 main checkout 必须重新验证。
```

For a short single-repo read-only audit, run doctor first and do not force `/goal` unless the user asks for cleanup or long-running execution.

## How To Use This Skill

For one repo:

```text
使用 OPL Doc Governance 治理当前 repo 的开发文档生命周期。
```

For the full OPL series:

```text
使用 OPL Doc Governance 治理 OPL series 的开发文档生命周期。
```

If the user asks how this differs from OpenArc/OpenSpec/Spec Kit, read `docs/reference-comparison.md`.

For a repo that lacks a clear active truth owner, use `templates/active-truth-plan.md` from this plugin as the recommended shape. Do not copy it blindly when the target repo already has a canonical active plan; map the same sections into the repo's existing owner document.

## Active Owner Discovery

Find the target repo's active truth owner before creating or rewriting any plan:

1. Read repo guidance for an explicit active plan or docs portfolio pointer.
2. Prefer `docs/active/current-state-vs-ideal-gap.md` when it exists and is current.
3. Otherwise search `docs/active/` for a document that owns current progress, current gaps, and next-round agent prompt together.
4. If multiple active docs claim the same role, choose the one closest to the repo's canonical docs and rewrite/retire the duplicates.
5. If none exists, create or map the bundled `templates/active-truth-plan.md` shape into the repo's normal active docs location.

## Repo-Native Reading

Repo-native means the skill and CLI stay external while the agent works from the target repo's own surfaces: `AGENTS.md`, `TASTE.md`, `README*`, `docs/**`, contracts, source, tests, scripts, package metadata, and repo-local verification commands. Do not install this CLI or generate `.opl-doc-governance/` inside target repos.

The local plugin installer creates the user-level `opl-doc-doctor` command. If it is unavailable, run the bundled script from this plugin checkout instead.

## Lifecycle Model

Every long-lived document needs:

- `Owner`
- `Purpose`
- `State`
- `Machine boundary`

Canonical placement:

- Current truth: `README.md`, `docs/README.md`, `docs/project.md`, `docs/status.md`, `docs/architecture.md`, `docs/invariants.md`, `docs/decisions.md`
- Active work: `docs/active/`
- Public narrative: `docs/public/`
- Product/runtime/source/delivery support: `docs/product/`, `docs/runtime/`, `docs/source/`, `docs/delivery/`
- Stable policies/specs/references: `docs/policies/`, `docs/specs/`, `docs/references/`
- Historical process, retired plans, old specs, tombstones: `docs/history/`
- Machine truth: `contracts/`, source, tests, CLI/API output, runtime ledger, receipt refs

Route section content by role:

| Section role | Destination |
| --- | --- |
| Current truth | Canonical docs |
| Active gap or next step | Single Active Truth plan |
| Support reference | `docs/references/`, `docs/specs/`, or the repo's support layer |
| Process history | `docs/history/` |
| Retired surface | Tombstone/provenance in history |
| Stale pollution | Rewrite, delete, or replace with a compact history pointer |

## Autonomous Development Loop

This skill must support the user's intended operating model: the user maintains the ideal state, while document governance derives and refreshes the development loop from live repo truth.

Required loop inputs:

- Ideal-state / target-state reference: what the repo should become.
- Live repo truth: code, contracts, tests, CLI/read-model output, runtime ledgers, and current docs.

Required loop outputs:

- Current completion progress.
- Current-state vs ideal-state gaps.
- Next-round agent prompt tied to those gaps.

For OPL-family repos, the active ideal-state gap plan is the usual output location. If a repo uses another canonical active plan, map to that document explicitly. Keep functional / structural gaps separate from test / evidence gaps. If no stable shape exists, use the bundled `templates/active-truth-plan.md` sections:

- Ideal-state reference.
- Current completion progress.
- Functional / structural gaps.
- Test / evidence gaps.
- Next-round agent prompt.
- History / tombstone foldback.

Rewrite algorithm:

1. Anchor the ideal state from the user-maintained target-state reference; do not derive the ideal from current implementation.
2. Read live repo truth for each target area: source, contracts, tests, CLI/read-model output, runtime ledgers, and canonical docs.
3. Classify each existing active-plan item as `done`, `open`, `blocked`, `evidence_gap`, `retired`, or `stale_pollution`.
4. Replace the active plan with the best current truth: progress table, current gaps, and the next-round agent prompt. Do not preserve stale rows for chronology.
5. Move only useful provenance into history/tombstone, especially no-resurrection guards for retired surfaces.
6. Run repo-native verification and rewrite the plan again if verification changes the truth.

The next-round agent prompt must be executable as a `/goal` objective or long-running Codex prompt. It must name the write scope, non-goals, live truth inputs, required actions, verification commands, completion gate, and foldback target. Do not leave a bare TODO list as the baton.

## Active Truth Governance

OPL Doc Governance is Active Truth first. It is not primarily a history-management system.

Hard rules:

- Active docs are rewritten toward the best current truth; do not append execution diaries, dated closeout logs, or long historical checklists.
- Each governed repo should have one active truth owner for current progress, current gaps, and the next-round agent prompt.
- The next-round agent prompt must include write scope, non-goals, live truth inputs, verification commands, completion gate, and foldback target.
- Completed work must remove or rewrite the closed gap in the active truth plan; process trace moves to `docs/history/` or tombstone/provenance.
- Before closeout, confirm closed gaps were removed or rewritten, canonical docs gained durable current truth, active paths contain no completed process packet, and the next-round prompt only names remaining work.
- History exists to prevent semantic pollution of Active Truth, not to preserve every intermediate decision in active paths.

## OPL Series Lifecycle Workflow

Use this when the user asks to refresh OPL series docs from ideal state and gap plans.

1. Treat each governed repo's ideal-state reference and single Active Truth plan as primary references.
2. Read current code/contracts/tests/read-model surfaces before editing docs.
3. Rewrite the active plan so it states current completion progress, current-state-vs-ideal gaps, and a next-round agent prompt.
4. Review other `docs/**/*.md` content section by section.
5. Classify each section as current truth, active plan, support reference, process history, retired/tombstone, or stale pollution.
6. Fold historical incremental lists into compact current-state tables plus history/tombstone pointers.
7. Retire stale modules/interfaces/tests directly once active callers have moved; do not preserve compatibility aliases.
8. Update canonical docs and archive/tombstone supporting docs so each document has one job.
9. Run repo-native verification, absorb worktree lanes back to `main`, and clean temporary worktrees/branches.

## Change Packet

For non-trivial work, create a short change packet in conversation or under `docs/active/changes/<change-id>/` when the repo keeps persistent active packets:

- `intent.md`: objective, non-goals, owner boundary
- `design.md`: doc taxonomy impact and machine-boundary impact
- `tasks.md`: implementation lanes and verification
- `verification.md`: commands and evidence
- `foldback.md`: where active material lands after completion

Fold completed packet content into canonical docs or `docs/history/`; do not leave completed process material in active paths.

Templates live under `templates/change-packet/`.

## Hard Rules

- Do not migrate OPL-family repos to OpenArc/OpenSpec/Spec Kit file names.
- Do not treat Markdown completeness as production readiness.
- Do not treat active docs as an execution log; Active Truth is a current-state rewrite surface.
- Do not put runtime truth, domain truth, quality verdicts, artifact authority, or owner receipts in docs.
- Do not keep compatibility aliases or facade docs after retirement gates are met.
- Do not create a second changelog/memory system when the repo already has history/process and receipt ledgers.

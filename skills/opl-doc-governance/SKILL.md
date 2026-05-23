---
name: opl-doc-governance
description: Use when governing OPL-family developer documentation lifecycle, auditing stale docs, folding active plans into canonical docs/history/tombstones, creating long-horizon change packets, or running the OPL docs doctor across one-person-lab, med-autoscience, med-autogrant, redcube-ai, opl-meta-agent, or adjacent OPL-compatible repositories.
---

# OPL Doc Governance

Use this skill for developer-document governance: helping AI understand current goals, maintain long-running plans, retire stale docs, and close the software-engineering loop. Do not use it for domain truth, runtime provider ownership, artifact authority, quality verdicts, or owner receipts.

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
python3 scripts/opl_doc_doctor.py doctor <repo-root> --format json
```

Use doctor output as evidence, then verify important claims by reading files.

## Goal Mode

When the user asks for OPL series governance, multi-repo cleanup, long-running autonomous development, stale-doc cleanup with edits, or anything that mentions worktrees/subagents/absorbing back to `main`, create or resume a `/goal` before execution. The user should not have to remember to ask for `/goal`.

Use this objective shape:

```text
使用 OPL Doc Governance，自动创建或延续 /goal，治理 OPL series 的开发文档生命周期；以各 repo 的 ideal-state reference 和 active gap plan 为主要参考，根据 live code、contracts、tests、CLI/read-model 与 docs 的当前事实，逐条评估 README* 与 docs/**/*.md 下其他文档，清理归档过时内容，避免二次污染；保证每个文档只有唯一任务和定位，折叠历史增量长清单，过时模块/接口/测试按理想态直接退役且不保留兼容面；可以并行使用 subagent/worktree，每条线完成后验证、提交、吸收回 main 并清理；最终 main checkout 必须重新验证。
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

## OPL Series Lifecycle Workflow

Use this when the user asks to refresh OPL series docs from ideal state and gap plans.

1. Treat each governed repo's ideal-state reference and active gap plan as primary references.
2. Read current code/contracts/tests/read-model surfaces before editing docs.
3. Review other `docs/**/*.md` content section by section.
4. Classify each section as current truth, active plan, support reference, process history, retired/tombstone, or stale pollution.
5. Fold historical incremental lists into compact current-state tables plus history pointers.
6. Retire stale modules/interfaces/tests directly once active callers have moved; do not preserve compatibility aliases.
7. Update canonical docs and archive/tombstone supporting docs so each document has one job.
8. Run repo-native verification, absorb worktree lanes back to `main`, and clean temporary worktrees/branches.

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
- Do not put runtime truth, domain truth, quality verdicts, artifact authority, or owner receipts in docs.
- Do not keep compatibility aliases or facade docs after retirement gates are met.
- Do not create a second changelog/memory system when the repo already has history/process and receipt ledgers.

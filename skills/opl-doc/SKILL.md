---
name: "opl-doc"
description: "Use when governing OPL-family developer documentation lifecycle, auditing every README/docs claim against live repo truth, enforcing one-document-one-role taxonomy, folding active plans into canonical docs/history/tombstones, directly retiring stale modules/interfaces/tests/docs without compatibility surfaces, creating long-horizon change packets, or running the OPL docs doctor across one-person-lab, med-autoscience, med-autogrant, redcube-ai, opl-meta-agent, one-person-lab-app, or adjacent OPL-compatible repositories."
---

# OPL Doc

Use this skill for developer-document governance: helping AI maintain the current single Active Truth from ideal state and live repo truth, derive current completion progress, maintain current-state gaps and next-round agent prompts, retire stale docs, and close the software-engineering loop. Do not use it for domain truth, runtime provider ownership, artifact authority, quality verdicts, or owner receipts.

## First Move

1. Read the target repo's `AGENTS.md`.
2. Read `TASTE.md` when present.
3. Read canonical current docs before touching supporting docs. Treat these docs as current-state claims to verify, not as authority by themselves:
   - `README.md`
   - `README.*` when present
   - `docs/README.md`
   - `docs/project.md`
   - `docs/status.md`
   - `docs/architecture.md`
   - `docs/invariants.md`
   - `docs/decisions.md`
   - `docs/active/current-state-vs-ideal-gap.md`
4. Locate the ideal-state reference and single Active Truth plan, then identify the live repo surfaces that can prove or disprove their claims. The live surfaces, not the existing prose, decide the governed current truth.
5. Inventory all `README*` and `docs/**/*.md` files before editing. The audit scope is not only the gap plan: every long-lived doc section must be checked for current role, current truth, and stale pollution risk.
6. Optionally run the doctor as a preflight risk map:

```bash
opl-doc-doctor doctor <repo-root> --format json
```

Use doctor output only as a preflight risk map. It is never the governance input, never the task list, and never proof that docs are current. Its `active_truth_health` output is only a shape signal for missing progress/gap/prompt sections, non-executable next prompts, or active process-log pollution. Important claims must still be verified from live source, contracts, tests, CLI/read-model output, runtime ledgers, receipts, and the actual document text.

For edit work, do not start by fixing doctor findings. Start by building the semantic input set: ideal state, current active truth plan, relevant canonical/support docs, implementation surfaces, verification/read-model surfaces, and stale/retired candidate docs.

## Goal Mode

When the user asks for OPL series governance, multi-repo cleanup, long-running autonomous development, stale-doc cleanup with edits, or anything that mentions worktrees/subagents/absorbing back to `main`, create or resume a `/goal` before execution. The user should not have to remember to ask for `/goal`.

The default OPL series scope is six repos: `one-person-lab`, `med-autoscience`, `med-autogrant`, `redcube-ai`, `opl-meta-agent`, and `one-person-lab-app`. Their ideal-state references plus single Active Truth plans form 12 primary reference documents. Do not shrink this to the older five-repo set unless the user explicitly excludes the App repo.

Use this objective shape:

```text
使用 OPL Doc，自动创建或延续 /goal，治理 OPL series 6 个 repo 的开发文档生命周期；以各 repo 的 ideal-state reference 和 single Active Truth plan 合计 12 个主参考文档为主要参考，根据 live code、contracts、tests、CLI/read-model 与 docs 的当前事实，重写维护当前完成进度、现状与理想态差距、下一轮 Agent prompt；逐条评估 README* 与 docs/**/*.md 下其他所有文档和章节，清理归档过时内容，避免二次污染；保证每个文档只有唯一任务和定位，active docs 不保存执行流水或历史增量日志，过时模块/接口/测试/文档/workflow/入口按理想态直接退役且不保留兼容面、alias、facade 或 wrapper；可以并行使用 subagent/worktree，每条线完成后验证、提交、吸收回 main 并清理；本轮 tranche 完成只表示本轮已验证并折回，不得把全局 /goal 标记 complete，除非 6 个 repo 的 README* 与 docs/**/*.md 已逐段覆盖、未覆盖文档清单为空、未完成 gap 已转入下一轮 Agent prompt；每轮结束必须留下覆盖清单、未覆盖文档、剩余 stale/retire 候选和下一轮写入范围；最终 main checkout 必须重新验证。
```

For a short single-repo read-only audit, run doctor first and do not force `/goal` unless the user asks for cleanup or long-running execution.

## How To Use This Skill

For one repo:

```text
使用 OPL Doc 治理当前 repo 的开发文档生命周期。
```

For the full OPL series:

```text
使用 OPL Doc 治理 OPL series 的开发文档生命周期。
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

Repo-native means the skill and CLI stay external while the agent works from the target repo's own surfaces: `AGENTS.md`, `TASTE.md`, `README*`, `docs/**`, contracts, source, tests, scripts, package metadata, and repo-local verification commands. Do not install this CLI or generate `.opl-doc/` inside target repos.

The local plugin installer creates the user-level `opl-doc-doctor` command. If it is unavailable, run the bundled script from this plugin checkout instead.

## Live Truth Audit

Document governance must start from current repository reality, not from doctor findings.

For every governed repo, perform a semantic audit before editing:

1. Read the ideal-state reference and active truth owner.
2. Read the code, contracts, tests, package/scripts, CLI/read-model surfaces, ledgers, and receipts that can prove or disprove the active plan's and canonical docs' claims.
3. Run repo-native read commands when the docs mention runtime, readiness, App/workbench, generated surfaces, owner receipt, typed blocker, artifact, memory, lifecycle, source, or production evidence.
4. Compare each active-plan claim and each relevant canonical-doc statement against the live truth just read.
5. Review every `README*` and `docs/**/*.md` section that can influence engineering decisions. Classify each section before editing: current truth, active gap, support reference, process history, retired/tombstone, or stale pollution.
6. Review stale/retired candidate docs for content that must be merged, archived, tombstoned, or deleted.
7. Rewrite docs from the comparison result, not from the doctor's structural findings.

Minimum acceptable evidence:

- Completion progress rows need source, contract, test, CLI/read-model, ledger, receipt, or explicit blocker refs.
- Functional / structural gaps need a target-state reference plus the current implementation surface that still differs.
- Test / evidence gaps need the existing implementation state plus the missing proof, receipt, or command.
- Retired surfaces need no-active-caller, replacement owner, tombstone/provenance, or negative guard evidence.
- Document merge/delete/archive decisions need the content role, destination owner, and live evidence that the old text is current support material, process history, retired provenance, or stale pollution.
- One-document-one-role decisions need the current document owner, the unique purpose it will retain, the duplicate or competing purpose to remove, and the destination for any useful content.

If you cannot find live evidence for a claim, write it as unknown, blocked, or evidence gap. Do not keep stale prose because it is already in a document.

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

## Whole-Docs Portfolio Audit

Doc governance is a whole-portfolio semantic audit. It must not stop after fixing the active gap plan.

For every `README*` and `docs/**/*.md` file:

1. Identify the document's single job: current truth, active plan, support reference, policy/spec, public narrative, product/runtime/source/delivery support, history, or tombstone.
2. Check each substantive section against live repo truth and the ideal-state reference.
3. Remove competing roles from the document. Move useful content to the correct owner; delete stale content that no longer has a legitimate role.
4. Fold historical incremental lists into compact current-state tables, current gaps, and history/tombstone pointers. Do not preserve chronology in active docs for its own sake.
5. If a section describes an outdated module, interface, test, doc path, workflow, or entrypoint, prove whether active callers remain. Once replacement and no-active-caller evidence exists, retire it directly and do not add compatibility aliases, facades, wrappers, or "legacy still works" prose.
6. Ensure the remaining document has one owner, one purpose, one state, and one machine boundary. If a document cannot be given one durable role, archive, tombstone, or delete it.

The output should make the current unique truth obvious at first scan. Detailed reasoning belongs in evidence references, history, or tombstones, not in active current-truth docs.

For long-horizon OPL series work, maintain a coverage ledger for each repo: reviewed docs/sections, edited docs, archived/tombstoned/deleted docs, unreviewed docs, unresolved stale/retire candidates, and next tranche write scope. A verified tranche can be absorbed back to `main`, but it does not close the global `/goal` while the coverage ledger still has unreviewed docs or unresolved carry-forward items.

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
2. Read live repo truth for each target area: source, contracts, tests, CLI/read-model output, and runtime ledgers; read canonical docs as claims that must be reconciled against those surfaces.
3. Review the active truth plan, canonical docs, support docs, history/tombstone candidates, and stale/retired candidates section by section, comparing each substantive claim to live truth.
4. Classify each existing active-plan item as `done`, `open`, `blocked`, `evidence_gap`, `retired`, or `stale_pollution`.
5. Replace the active plan with the best current truth: progress table, current gaps, and the next-round agent prompt. Do not preserve stale rows for chronology.
6. Update canonical/support docs so durable current truth has one owner and stale support content is merged, archived, tombstoned, or deleted.
7. Rewrite or retire docs that carry multiple roles. A document should not simultaneously be current truth, active plan, execution log, and historical reference.
8. Move only useful provenance into history/tombstone, especially no-resurrection guards for retired surfaces.
9. Run repo-native verification and rewrite the plan again if verification changes the truth.

The next-round agent prompt must be executable as a `/goal` objective or long-running Codex prompt. It must name the write scope, non-goals, live truth inputs, required actions, verification commands, completion gate, and foldback target. Do not leave a bare TODO list as the baton.

## Active Truth Governance

OPL Doc is Active Truth first. It is not primarily a history-management system.

Hard rules:

- Do not run doctor and then only fix doctor findings. That is a structural cleanup pass, not OPL Doc.
- Do not update docs from the existing prose alone. Every substantive current-state, progress, gap, retirement, and next-step claim must be checked against live repo truth or marked as an evidence gap.
- Active docs are rewritten toward the best current truth; do not append execution diaries, dated closeout logs, or long historical checklists.
- Each governed repo should have one active truth owner for current progress, current gaps, and the next-round agent prompt.
- Each long-lived document should have one durable role. If two documents claim the same role, pick the canonical owner and rewrite, archive, tombstone, or delete the duplicate.
- The next-round agent prompt is the user's intended autonomous-development baton, not a TODO list. It must include objective, write scope, non-goals, live truth inputs, required actions, verification commands, completion gate, and foldback target so it can be pasted into `/goal`.
- Completed work must remove or rewrite the closed gap in the active truth plan; process trace moves to `docs/history/` or tombstone/provenance.
- Before closeout, confirm closed gaps were removed or rewritten, canonical docs gained durable current truth, each edited doc has a single role, active paths contain no completed process packet, and the next-round prompt only names remaining work.
- Do not mark the global `/goal` complete merely because one tranche was verified, committed, and absorbed. Call it a tranche closeout, keep the global goal active, and carry remaining docs/gaps into the next-round Agent prompt.
- Every multi-repo tranche must leave a coverage ledger that names reviewed docs, unreviewed docs, unresolved stale/retire candidates, and the next write scope. If that ledger is missing, the tranche is not complete.
- History exists to prevent semantic pollution of Active Truth, not to preserve every intermediate decision in active paths.

## OPL Series Lifecycle Workflow

Use this when the user asks to refresh OPL series docs from ideal state and gap plans.

1. Treat the default six repos as the governed OPL series unless the user narrows scope: `one-person-lab`, `med-autoscience`, `med-autogrant`, `redcube-ai`, `opl-meta-agent`, and `one-person-lab-app`.
2. Treat each governed repo's ideal-state reference and single Active Truth plan as primary references; the default six-repo run has 12 primary reference documents.
3. Run doctor only as preflight, then set it aside; use `active_truth_health` only to notice shape risks, not as semantic proof.
4. Read current code/contracts/tests/read-model surfaces before editing docs.
5. For each active plan, canonical doc, support doc, history/tombstone candidate, and stale/retired candidate, compare substantive claims against live repo truth section by section.
6. Rewrite the active plan so it states current completion progress, current-state-vs-ideal gaps, and a next-round agent prompt.
7. Review other `README*` and `docs/**/*.md` content section by section.
8. Classify each section as current truth, active plan, support reference, process history, retired/tombstone, or stale pollution.
9. Fold historical incremental lists into compact current-state tables plus history/tombstone pointers.
10. Retire stale modules/interfaces/tests/docs directly once active callers have moved; do not preserve compatibility aliases, facades, wrappers, or compatibility wording.
11. Update canonical docs and archive/tombstone supporting docs so each document has one job.
12. Maintain a repo-by-repo coverage ledger for reviewed docs, edited docs, retired docs, unreviewed docs, unresolved stale/retire candidates, and next tranche write scope.
13. Run repo-native verification, absorb completed worktree lanes back to `main`, and clean only the current tranche's temporary worktrees/branches.
14. Close the tranche, not the global goal, unless the coverage ledger proves no unreviewed docs, unresolved stale/retire candidates, or unfinished gaps remain across all governed repos.

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
- Do not convert a verified tranche into global completion while any governed repo still has unreviewed docs, unresolved stale/retire candidates, or carry-forward gaps.

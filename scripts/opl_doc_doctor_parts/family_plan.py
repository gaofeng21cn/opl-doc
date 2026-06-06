"""OPL series document lifecycle workflow plan generation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .constants import DEFAULT_SERIES_REPO_NAMES, DEFAULT_SUPPORT_REPO_NAMES, OPL_DOC_AUTHORITY_BOUNDARY


def build_primary_reference_docs(repo_paths: dict[str, str]) -> list[str]:
    docs: list[str] = []
    for repo_id in repo_paths:
        label = repo_id.upper()
        docs.append(f"{label} ideal-state / target-state reference")
        docs.append(f"{label} single Active Truth plan")
    return docs


def default_series_repos(workspace_root: str | None = None) -> dict[str, str]:
    if not workspace_root:
        return dict(DEFAULT_SERIES_REPO_NAMES)
    root = Path(workspace_root).expanduser()
    return {
        repo_id: str(root / repo_name)
        for repo_id, repo_name in DEFAULT_SERIES_REPO_NAMES.items()
    }


def build_goal_objective(repo_paths: dict[str, str]) -> str:
    repo_list = ", ".join(repo_paths)
    repo_count = len(repo_paths)
    reference_count = repo_count * 2
    return (
        "使用 OPL Doc，自动创建或延续 /goal，治理 OPL series "
        f"{repo_count} 个 repo（{repo_list}）的开发文档生命周期；以各 repo 的 ideal-state "
        f"reference 和 single Active Truth plan 合计 {reference_count} 个主参考文档为主要参考，根据 live code、"
        "contracts、tests、CLI/read-model 与 docs 的当前事实，重写维护当前"
        "完成进度、现状与理想态差距、下一轮 Agent prompt；逐条评估 "
        "README* 与 docs/**/*.md 下其他所有文档和章节，先按语义主题确定 Single Source of Truth，"
        "再做内容层面的合并、收薄、归档、删除和细节纳入，清理归档过时内容，避免二次污染；"
        "保证每个长期文档只有唯一任务和定位，active docs 不保存执行流水或历史"
        "增量日志，过时模块/接口/测试/文档/workflow/入口按"
        "理想态直接退役且不保留兼容面、alias、facade 或 wrapper；可以并行使用 subagent/worktree，"
        "每条线完成后验证、提交、吸收回 main 并清理；本轮 tranche 完成只表示本轮已验证并折回，"
        "不得把全局 /goal 标记 complete，除非 6 个 repo 的 README* 与 docs/**/*.md 已逐段覆盖、"
        "未覆盖文档清单为空、未完成 gap 已转入下一轮 Agent prompt；每轮结束必须留下覆盖清单、"
        "未覆盖文档、剩余 stale/retire 候选和下一轮写入范围。最终 main checkout 必须重新验证，"
        "且 canonical docs、history/tombstone 与必要的 contracts/read-model references 已同步。"
    )


def family_plan(repo_paths: dict[str, str] | None = None) -> dict[str, Any]:
    paths = repo_paths or default_series_repos()
    primary_reference_docs = build_primary_reference_docs(paths)
    support_repos = dict(DEFAULT_SUPPORT_REPO_NAMES)
    support_repo_policy = {
        "default_included_in_governed_repo_set": False,
        "extension_only": True,
        "not_foundry_agent_truth_set": True,
        "support_repos": support_repos,
        "authority_boundary": OPL_DOC_AUTHORITY_BOUNDARY,
        "include_only_when": [
            "user_explicitly_requests_support_repo_governance",
            "current_task_touches_support_repo_docs_or_scripts",
            "support_repo_is_needed_to_explain_workflow_or_shell_carrier_boundary",
        ],
    }
    governance_prompt_elements = [
        "series_primary_reference_docs",
        "support_repo_extension_boundary",
        "active_owner_discovery",
        "live_truth_semantic_audit",
        "doctor_is_preflight_only",
        "single_active_truth_first",
        "ssot_first_semantic_consolidation",
        "content_level_not_file_level",
        "rewrite_active_truth",
        "active_truth_plan_shape",
        "content_routing_table",
        "next_round_agent_prompt",
        "foldback_closure_check",
        "evaluate_all_docs_item_by_item",
        "cleanup_and_archive_stale_content",
        "unique_task_positioning",
        "fold_long_incremental_lists",
        "directly_retire_outdated_modules_interfaces_tests",
        "allow_parallel_worktrees_and_subagents",
        "absorb_main_and_cleanup_when_complete",
        "long_horizon_tranche_continuation",
        "coverage_ledger_for_unfinished_docs",
    ]
    steps = [
        "Use the OPL series primary reference docs: each governed repo contributes its ideal-state reference plus its single Active Truth plan.",
        "Read each repo's AGENTS.md, TASTE.md when present, status, architecture, invariants, docs portfolio guidance, and the series primary reference docs before editing.",
        "Run doctor only as a preflight risk map; do not turn doctor findings into the governance task list.",
        "Treat doctor, native profile, and family-plan outputs as workflow aids only: they do not own repo truth, runtime truth, domain truth, artifact authority, quality verdicts, owner receipts, production readiness, or the Foundry Agent truth set.",
        "Keep opl-doc and shell repos as support extensions. They are included only when explicitly requested or when the current task touches their docs/scripts; they are not part of the default Foundry Agent truth set.",
        "Build the semantic input set before editing: semantic theme, SSOT owner candidate, ideal-state reference, active truth plan, canonical/support/history docs, source/contracts/tests, read-model commands, runtime ledgers, receipts, blockers, and stale/retired candidate docs.",
        "Discover the active truth owner before editing: prefer repo-declared pointers and docs/active/current-state-vs-ideal-gap.md, then retire or rewrite duplicate active plans that claim the same role.",
        "For each docs lane, determine the Single Source of Truth before editing peer docs. Prefer machine-readable contracts/schemas/source/package scripts/validators/tests/runtime evidence, then canonical owner docs, then active plans, then support/history.",
        "Govern by content theme and section rather than by file path: classify peer sections as covered_by_ssot, more_specific_detail, conflicts_with_ssot, stale_or_superseded, history_or_provenance, or out_of_scope.",
        "Perform a live truth semantic audit: read source, contracts, tests, package scripts, CLI/read-model outputs, runtime ledgers, receipts, and blockers that prove or disprove active-plan and canonical-doc claims.",
        "Treat ideal-state as the user-maintained target and rewrite the active plan to the best current truth from live code, contracts, tests, CLI/read-model, and docs.",
        "If a repo lacks a stable active truth owner, use templates/active-truth-plan.md as the section shape; if one already exists, map the same sections into that canonical active plan instead of creating a second plan.",
        "Active docs must keep current completion progress, current-state-vs-ideal gaps, and the next-round Agent prompt; do not append execution diaries, dated closeout logs, or historical checklists.",
        "Route sections by role: current truth to canonical docs, active gaps to the Active Truth plan, support material to references/specs/support layers, process history to docs/history, retired surfaces to tombstone/provenance, and stale pollution to rewrite/delete.",
        "Review every README* and docs/**/*.md semantic section against live repo truth and the theme SSOT; update content because the code/contracts/tests/read-model or owner doc changed or disproved prose, not because a structural scanner emitted a warning.",
        "For every merge, archive, tombstone, or delete decision, record the SSOT owner, content role, destination owner, and evidence that the old text is covered duplicate, specific support material, process history, retired provenance, or stale pollution.",
        "The next-round Agent prompt must be executable as a /goal or long-running Codex prompt and include write scope, non-goals, live truth inputs, required actions, verification commands, completion gate, and foldback target.",
        "Before closeout, verify closed gaps were removed or rewritten, durable current truth was folded into canonical docs, active paths contain no completed process packet, and the next-round prompt only names remaining work.",
        "逐条评估 docs 下其他所有文档；for each semantic theme, keep one current owner and classify peer sections as covered duplicate, support detail, conflict, stale/superseded, history/provenance, or out of scope.",
        "清理和归档过时内容，避免二次污染；route history to docs/history or tombstone refs instead of active docs.",
        "每个长期文档必须有唯一任务和定位；update canonical docs so every long-lived document has one owner, one purpose, one state, and one machine boundary.",
        "历史增量长清单要折叠 into compact current-state tables plus archive pointers.",
        "过时模块/接口/测试/文档/workflow/入口全部按当前理想态直接退役清理，不保留兼容 alias、facade、wrapper 或 compatibility wording.",
        "可以并行开 worktree/subagent for independent repos or non-overlapping lanes; keep scopes explicit and merge evidence back to the owner lane.",
        "Run repo-native doc/contract/tests verification, absorb completed lanes back to main, and clean temporary branches/worktrees.",
        "Treat each execution as a long-horizon tranche: a tranche can be verified and absorbed, but the global goal must remain open until all governed repos and all README*/docs/**/*.md sections have been covered or explicitly carried forward.",
        "Maintain a coverage ledger for every governed repo: reviewed docs/sections, edited docs, archived/tombstoned/deleted docs, unreviewed docs, unresolved stale/retire candidates, and the next tranche write scope.",
    ]
    return {
        "objective": "OPL series document lifecycle governance and software-engineering closeout",
        "repos": paths,
        "support_repo_policy": support_repo_policy,
        "goal_mode": {
            "recommended": True,
            "agent_action": "create_goal_or_resume_goal_before_multi_repo_or_long_horizon_governance",
            "objective": build_goal_objective(paths),
            "single_repo_exception": "For a short single-repo read-only audit, run doctor first and do not force /goal unless the user asks for cleanup or long-running execution.",
        },
        "primary_reference_doc_count": len(primary_reference_docs),
        "primary_reference_docs_per_repo": primary_reference_docs,
        "governance_prompt_elements": governance_prompt_elements,
        "workflow": steps,
        "completion_gate": [
            "canonical docs reflect current truth",
            "active docs were rewritten to the single best Active Truth",
            "active truth includes current completion progress, current-state gaps, and next-round Agent prompt",
            "stale process material is archived or tombstoned",
            "each governed semantic theme has one documented SSOT owner",
            "peer docs keep only entry summaries, pointers, unique support detail, machine-boundary notes, or history/provenance",
            "no active compatibility-resurrection wording remains",
            "contracts/tests/read-model references are not contradicted by prose",
            "outdated modules/interfaces/tests/docs/workflows/entrypoints are directly retired when their active callers have moved",
            "completed lanes were absorbed back to main and temporary worktrees/branches were cleaned",
            "verification was run on the final main checkout",
            "global goal was not marked complete merely because one tranche finished",
            "coverage ledger records reviewed, edited, archived, tombstoned, deleted, unreviewed, and carry-forward documents for every governed repo",
            "support repos remain explicit extensions and never become the default Foundry Agent truth set",
        ],
    }


def parse_repo_overrides(
    values: list[str],
    base: dict[str, str] | None = None,
) -> dict[str, str]:
    repos = dict(base) if base is not None else default_series_repos()
    for value in values:
        if "=" not in value:
            raise SystemExit(f"--repo must use ID=PATH, got: {value}")
        repo_id, path = value.split("=", 1)
        repo_id = repo_id.strip()
        path = path.strip()
        if not repo_id or not path:
            raise SystemExit(f"--repo must use non-empty ID=PATH, got: {value}")
        repos[repo_id] = path
    return repos

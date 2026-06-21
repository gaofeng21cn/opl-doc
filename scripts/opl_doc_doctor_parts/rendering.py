"""Markdown report rendering for doctor and family-plan payloads."""

from __future__ import annotations

from typing import Any


def print_markdown(payload: dict[str, Any]) -> None:
    print("# OPL Doc Doctor")
    print()
    print(f"Root: `{payload['root']}`")
    print(f"Profile: `{payload['repo_profile']}`")
    print(f"Markdown docs: `{payload['markdown_doc_count']}`")
    surfaces = payload["repo_native_surfaces"]
    print(f"Agent guidance: `{len(surfaces['agent_guidance'])}`")
    print(f"Verification surfaces: `{len(surfaces['verification'])}`")
    print()
    print("## Active Truth Health")
    health = payload["active_truth_health"]
    print(f"- status: `{health['status']}`")
    print(f"- checked owner docs: `{health['checked_doc_count']}`")
    print(f"- missing items: `{health['missing_item_count']}`")
    print(f"- process-log headings: `{health['process_log_heading_count']}`")
    for document in health["documents"]:
        prompt_ready = "yes" if document["next_round_agent_prompt_ready"] else "no"
        print(f"- `{document['path']}` next prompt ready: `{prompt_ready}`")
    print()
    print("## Findings")
    if not payload["findings"]:
        print("- none")
    for finding in payload["findings"]:
        print(
            f"- `{finding['severity']}` `{finding['code']}` `{finding['path']}`: "
            f"{finding['message']} Action: {finding['action']}"
        )
    print()
    print("## Recommendation")
    print(payload["recommendation"])


def print_family_markdown(payload: dict[str, Any]) -> None:
    print("# OPL Series Docs Lifecycle Workflow")
    print()
    print(f"Objective: {payload['objective']}")
    print()
    print("## Goal Mode")
    print("create or resume a /goal before multi-repo or long-horizon governance.")
    print()
    print(payload["goal_mode"]["objective"])
    print()
    print("## Repos")
    for name, path in payload["repos"].items():
        print(f"- `{name}`: `{path}`")
    print()
    print("## Support Repos")
    support_policy = payload["support_repo_policy"]
    print("support repos are explicit extensions, not the default Foundry Agent truth set.")
    for name, path in support_policy["support_repos"].items():
        print(f"- `{name}`: `{path}`")
    print()
    print("## Support Profile Guard")
    support_guard = payload["support_profile_guard"]
    print(
        "materialized support profile guard: "
        f"`{support_guard['guard_id']}` / `{support_guard['state']}`"
    )
    print("support profile remains profile sync / workflow plan / no-resurrection only.")
    print()
    print("## Primary References")
    print(f"{payload['primary_reference_doc_count']} primary reference docs")
    for reference in payload["primary_reference_docs_per_repo"]:
        print(f"- {reference}")
    print()
    print("## Governance Prompt Elements")
    labels = {
        "series_primary_reference_docs": "OPL series primary reference docs",
        "active_owner_discovery": "active truth owner 发现顺序",
        "live_truth_semantic_audit": "live repo truth 语义审计",
        "doctor_is_preflight_only": "doctor 只做预检 guard",
        "single_active_truth_first": "唯一 Active Truth / SSOT 优先",
        "ssot_first_semantic_consolidation": "先定 Single Source of Truth 再内容级合并",
        "content_level_not_file_level": "按语义内容治理，不按文件机械整理",
        "rewrite_active_truth": "重写 active truth 到当前最优真相",
        "active_truth_plan_shape": "Active Truth plan 推荐形状",
        "content_routing_table": "按内容角色路由文档章节",
        "next_round_agent_prompt": "下一轮 Agent prompt",
        "foldback_closure_check": "foldback closeout 闭环检查",
        "evaluate_all_docs_item_by_item": "逐条评估 README/docs 下其他所有文档和章节",
        "cleanup_and_archive_stale_content": "清理和归档过时内容",
        "unique_task_positioning": "每个长期文档必须有唯一任务和定位",
        "fold_long_incremental_lists": "历史增量长清单要折叠",
        "directly_retire_outdated_modules_interfaces_tests": "过时模块/接口/测试/文档/workflow/入口直接退役清理",
        "allow_parallel_worktrees_and_subagents": "允许并行 worktree/subagent",
        "absorb_main_and_cleanup_when_complete": "完成后吸收回 main 并清理",
        "long_horizon_tranche_continuation": "长线 tranche 续跑，不把本轮完成当全局完成",
        "coverage_ledger_for_unfinished_docs": "覆盖清单记录已审/未审文档和下一轮范围",
    }
    for element in payload["governance_prompt_elements"]:
        print(f"- {labels.get(element, element)}")
    print()
    print("## Workflow")
    for index, step in enumerate(payload["workflow"], start=1):
        print(f"{index}. {step}")
    print()
    print("## Completion Gate")
    for gate in payload["completion_gate"]:
        print(f"- {gate}")

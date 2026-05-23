from __future__ import annotations

from io import StringIO
from pathlib import Path
from contextlib import redirect_stdout

from scripts.opl_doc_doctor import (
    default_series_repos,
    doctor,
    family_plan,
    parse_repo_overrides,
    print_family_markdown,
)


def test_doctor_detects_opl_profile_and_core_docs(tmp_path: Path) -> None:
    root = tmp_path / "one-person-lab"
    docs = root / "docs"
    docs.mkdir(parents=True)
    (root / "README.md").write_text("# OPL\n", encoding="utf-8")
    (root / "AGENTS.md").write_text("# Agents\n", encoding="utf-8")
    (root / "TASTE.md").write_text("# Taste\n", encoding="utf-8")
    (docs / "project.md").write_text(
        "# Project\n\nOwner: `OPL`\nPurpose: `project`\nState: `active_truth`\nMachine boundary: contracts\n",
        encoding="utf-8",
    )
    (docs / "status.md").write_text("# Status\n", encoding="utf-8")
    (docs / "architecture.md").write_text("# Architecture\n", encoding="utf-8")
    (docs / "invariants.md").write_text("# Invariants\n", encoding="utf-8")

    payload = doctor(root)

    assert payload["repo_profile"] == "opl_framework"
    assert payload["core_docs"]["docs/project.md"] is True
    assert payload["markdown_doc_count"] == 4
    assert payload["repo_native_surfaces"]["agent_guidance"] == ["AGENTS.md", "TASTE.md"]
    assert payload["repo_native_surfaces"]["canonical_docs"]["present"] == [
        "README.md",
        "AGENTS.md",
        "TASTE.md",
        "docs/project.md",
        "docs/status.md",
        "docs/architecture.md",
        "docs/invariants.md",
    ]


def test_doctor_detects_repo_native_verification_without_writing(tmp_path: Path) -> None:
    root = tmp_path / "redcube-ai"
    scripts = root / "scripts"
    scripts.mkdir(parents=True)
    (root / "README.md").write_text("# RCA\n", encoding="utf-8")
    (root / "AGENTS.md").write_text("# Agents\n", encoding="utf-8")
    (scripts / "verify.sh").write_text("#!/usr/bin/env bash\n", encoding="utf-8")
    (root / "package.json").write_text('{"scripts":{"test":"node --test","build":"tsc"}}\n', encoding="utf-8")

    payload = doctor(root)

    assert payload["repo_native_surfaces"]["agent_guidance"] == ["AGENTS.md"]
    assert payload["repo_native_surfaces"]["verification"] == [
        "scripts/verify.sh",
        "package.json:scripts.test",
        "package.json:scripts.build",
    ]
    assert not (root / ".opl-doc-governance").exists()


def test_doctor_flags_active_legacy_vocabulary(tmp_path: Path) -> None:
    root = tmp_path / "redcube-ai"
    active = root / "docs" / "active"
    active.mkdir(parents=True)
    (root / "README.md").write_text("# RCA\n", encoding="utf-8")
    (root / "AGENTS.md").write_text("# Agents\n", encoding="utf-8")
    (active / "current-state-vs-ideal-gap.md").write_text(
        "# Gap\n\nOwner: `RCA`\nPurpose: `gap`\nState: `active_plan`\nMachine boundary: contracts\n\n"
        "This keeps a compatibility alias for gateway-first behavior.\n",
        encoding="utf-8",
    )

    payload = doctor(root)

    codes = {finding["code"] for finding in payload["findings"]}
    assert "legacy_vocabulary_active_path" in codes
    assert payload["recommendation"].startswith("Run an active-doc retirement pass")


def test_history_legacy_vocabulary_is_not_flagged(tmp_path: Path) -> None:
    root = tmp_path / "one-person-lab"
    history = root / "docs" / "history"
    history.mkdir(parents=True)
    (history / "gateway.md").write_text("gateway-first historical note\n", encoding="utf-8")

    payload = doctor(root)

    assert all(finding["code"] != "legacy_vocabulary_active_path" for finding in payload["findings"])


def test_negative_retirement_policy_is_not_legacy_pollution(tmp_path: Path) -> None:
    root = tmp_path / "one-person-lab"
    active = root / "docs" / "active"
    active.mkdir(parents=True)
    (active / "current-state-vs-ideal-gap.md").write_text(
        "# Gap\n\nOwner: `OPL`\nPurpose: `gap`\nState: `active_plan`\nMachine boundary: contracts\n\n"
        "过时模块退役后不保留任何兼容面，也不新增 compatibility alias。\n",
        encoding="utf-8",
    )

    payload = doctor(root)

    assert all(finding["code"] != "legacy_vocabulary_active_path" for finding in payload["findings"])


def test_doctor_flags_dated_active_heading_incremental_list(tmp_path: Path) -> None:
    root = tmp_path / "one-person-lab"
    active = root / "docs" / "active"
    active.mkdir(parents=True)
    dated_sections = "\n".join(
        f"## 2026-05-{day:02d}\n\n- captured one more update\n"
        for day in range(1, 7)
    )
    (active / "current-state-vs-ideal-gap.md").write_text(
        "# Gap\n\nOwner: `OPL`\nPurpose: `gap`\nState: `active_plan`\nMachine boundary: contracts\n\n"
        f"{dated_sections}",
        encoding="utf-8",
    )

    payload = doctor(root)

    matching = [
        finding
        for finding in payload["findings"]
        if finding["code"] == "long_incremental_list_risk"
    ]
    assert matching
    assert matching[0]["path"] == "docs/active/current-state-vs-ideal-gap.md"
    assert "dated headings" in matching[0]["message"]


def test_doctor_flags_long_checkbox_incremental_list(tmp_path: Path) -> None:
    root = tmp_path / "med-autoscience"
    active = root / "docs" / "active"
    active.mkdir(parents=True)
    checklist = "\n".join(f"- [ ] incremental item {index}" for index in range(1, 13))
    (active / "cleanup.md").write_text(
        "# Cleanup\n\nOwner: `MAS`\nPurpose: `cleanup`\nState: `active_plan`\nMachine boundary: contracts\n\n"
        f"{checklist}\n",
        encoding="utf-8",
    )

    payload = doctor(root)

    assert any(
        finding["code"] == "long_incremental_list_risk"
        and "checkbox items" in finding["message"]
        for finding in payload["findings"]
    )


def test_family_plan_contains_opl_series_workflow() -> None:
    payload = family_plan()

    assert set(payload["repos"]) == {"opl", "mas", "mag", "rca", "oma"}
    assert payload["repos"]["oma"] == "opl-meta-agent"
    assert payload["primary_reference_doc_count"] == 10
    assert "OPL single Active Truth plan" in payload["primary_reference_docs_per_repo"]
    assert payload["goal_mode"]["recommended"] is True
    assert "create_goal" in payload["goal_mode"]["agent_action"]
    assert any("archive" in step or "tombstone" in step for step in payload["workflow"])
    assert "verification was run on the final main checkout" in payload["completion_gate"]


def test_family_plan_json_contains_original_series_governance_prompt_elements() -> None:
    payload = family_plan()

    assert len(payload["primary_reference_docs_per_repo"]) == 10
    assert {
        "evaluate_all_docs_item_by_item",
        "active_owner_discovery",
        "single_active_truth_first",
        "rewrite_active_truth",
        "active_truth_plan_shape",
        "content_routing_table",
        "next_round_agent_prompt",
        "foldback_closure_check",
        "cleanup_and_archive_stale_content",
        "unique_task_positioning",
        "fold_long_incremental_lists",
        "directly_retire_outdated_modules_interfaces_tests",
        "allow_parallel_worktrees_and_subagents",
        "absorb_main_and_cleanup_when_complete",
    }.issubset(set(payload["governance_prompt_elements"]))
    assert "series_primary_reference_docs" in payload["governance_prompt_elements"]
    assert any("active truth owner" in step for step in payload["workflow"])
    assert any("Route sections by role" in step for step in payload["workflow"])
    assert any("Active Truth" in step for step in payload["workflow"])
    assert any("active-truth-plan.md" in step for step in payload["workflow"])
    assert any("Agent prompt" in step and "/goal" in step for step in payload["workflow"])
    assert any("Before closeout" in step for step in payload["workflow"])
    assert any("docs 下其他所有文档" in step for step in payload["workflow"])
    assert any("worktree" in step and "subagent" in step for step in payload["workflow"])


def test_family_plan_markdown_contains_original_series_governance_prompt_elements() -> None:
    payload = family_plan()
    output = StringIO()

    with redirect_stdout(output):
        print_family_markdown(payload)

    markdown = output.getvalue()
    assert "OPL Series Docs Lifecycle Workflow" in markdown
    assert "Goal Mode" in markdown
    assert "create or resume a /goal" in markdown
    assert "10 primary reference docs" in markdown
    assert "single Active Truth plan" in markdown
    assert "active truth owner 发现顺序" in markdown
    assert "唯一 Active Truth / SSOT 优先" in markdown
    assert "Active Truth plan 推荐形状" in markdown
    assert "按内容角色路由文档章节" in markdown
    assert "active-truth-plan.md" in markdown
    assert "下一轮 Agent prompt" in markdown
    assert "foldback closeout 闭环检查" in markdown
    assert "opl-meta-agent" in markdown
    assert "逐条评估 docs 下其他所有文档" in markdown
    assert "清理和归档过时内容" in markdown
    assert "每个文档必须有唯一任务和定位" in markdown
    assert "历史增量长清单要折叠" in markdown
    assert "过时模块/接口/测试" in markdown
    assert "worktree/subagent" in markdown
    assert "吸收回 main 并清理" in markdown


def test_parse_repo_overrides_keeps_default_series_and_adds_extra_repo() -> None:
    repos = parse_repo_overrides(["award=award-agent"])

    assert set(repos) == {"opl", "mas", "mag", "rca", "oma", "award"}
    assert repos["award"] == "award-agent"


def test_default_series_repos_can_expand_from_workspace_root() -> None:
    repos = default_series_repos("/workspace")

    assert repos["opl"] == "/workspace/one-person-lab"
    assert repos["oma"] == "/workspace/opl-meta-agent"


def test_family_plan_goal_prompt_is_self_contained_for_codex_goal() -> None:
    payload = family_plan()

    goal_prompt = payload["goal_mode"]["objective"]
    assert "OPL series" in goal_prompt
    assert "自动创建或延续 /goal" in goal_prompt
    assert "single Active Truth plan" in goal_prompt
    assert "下一轮 Agent prompt" in goal_prompt
    assert "逐条评估" in goal_prompt
    assert "吸收回 main" in goal_prompt
    assert "最终 main checkout" in goal_prompt

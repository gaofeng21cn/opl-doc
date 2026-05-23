from __future__ import annotations

from io import StringIO
from pathlib import Path
from contextlib import redirect_stdout

from scripts.opl_doc_doctor import (
    default_series_repos,
    doctor,
    family_plan,
    init_repo,
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
    assert payload["repo_native"]["present"] is False


def test_init_repo_dry_run_reports_repo_native_files_without_writing(tmp_path: Path) -> None:
    root = tmp_path / "med-autoscience"
    root.mkdir()

    payload = init_repo(root, dry_run=True)

    assert payload["dry_run"] is True
    assert payload["repo_profile"] == "foundry_agent"
    assert payload["created"] == [
        ".opl-doc-governance/config.json",
        ".opl-doc-governance/agent-entry.md",
        ".opl-doc-governance/README.md",
    ]
    assert not (root / ".opl-doc-governance").exists()


def test_init_repo_writes_repo_native_config_and_agent_entry(tmp_path: Path) -> None:
    root = tmp_path / "redcube-ai"
    root.mkdir()

    payload = init_repo(root)

    config_path = root / ".opl-doc-governance" / "config.json"
    entry_path = root / ".opl-doc-governance" / "agent-entry.md"
    readme_path = root / ".opl-doc-governance" / "README.md"
    assert payload["dry_run"] is False
    assert config_path.exists()
    assert entry_path.exists()
    assert readme_path.exists()
    assert "opl-doc-governance" in config_path.read_text(encoding="utf-8")
    assert "First agent move" in entry_path.read_text(encoding="utf-8")
    assert "/path/to" not in entry_path.read_text(encoding="utf-8")


def test_init_repo_refuses_to_overwrite_without_force(tmp_path: Path) -> None:
    root = tmp_path / "one-person-lab"
    native = root / ".opl-doc-governance"
    native.mkdir(parents=True)
    (native / "config.json").write_text("custom\n", encoding="utf-8")

    try:
        init_repo(root)
    except FileExistsError as exc:
        assert ".opl-doc-governance/config.json" in str(exc)
    else:
        raise AssertionError("init_repo should refuse to overwrite existing repo-native files")


def test_init_repo_dry_run_reports_existing_files_without_force(tmp_path: Path) -> None:
    root = tmp_path / "one-person-lab"
    native = root / ".opl-doc-governance"
    native.mkdir(parents=True)
    (native / "config.json").write_text("custom\n", encoding="utf-8")

    payload = init_repo(root, dry_run=True)

    assert payload["dry_run"] is True
    assert payload["skipped_existing"] == [".opl-doc-governance/config.json"]
    assert (native / "config.json").read_text(encoding="utf-8") == "custom\n"


def test_doctor_reports_repo_native_entry_when_present(tmp_path: Path) -> None:
    root = tmp_path / "opl-meta-agent"
    root.mkdir()
    init_repo(root)

    payload = doctor(root)

    assert payload["repo_native"]["present"] is True
    assert payload["repo_native"]["complete"] is True
    assert payload["repo_native"]["agent_entry_path"] == ".opl-doc-governance/agent-entry.md"
    assert payload["repo_native"]["schema_version"] == "opl-doc-governance.repo-native.v1"


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
    assert payload["goal_mode"]["recommended"] is True
    assert "create_goal" in payload["goal_mode"]["agent_action"]
    assert any("archive" in step or "tombstone" in step for step in payload["workflow"])
    assert "verification was run on the final main checkout" in payload["completion_gate"]


def test_family_plan_json_contains_original_series_governance_prompt_elements() -> None:
    payload = family_plan()

    assert len(payload["primary_reference_docs_per_repo"]) == 10
    assert {
        "evaluate_all_docs_item_by_item",
        "cleanup_and_archive_stale_content",
        "unique_task_positioning",
        "fold_long_incremental_lists",
        "directly_retire_outdated_modules_interfaces_tests",
        "allow_parallel_worktrees_and_subagents",
        "absorb_main_and_cleanup_when_complete",
    }.issubset(set(payload["governance_prompt_elements"]))
    assert "series_primary_reference_docs" in payload["governance_prompt_elements"]
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
    assert "逐条评估" in goal_prompt
    assert "吸收回 main" in goal_prompt
    assert "最终 main checkout" in goal_prompt

from __future__ import annotations

import json
import subprocess
import sys
from io import StringIO
from pathlib import Path
from contextlib import redirect_stdout

from scripts.opl_doc_doctor_parts.family_plan import (
    build_support_profile_guard_audit,
    default_series_repos,
    family_plan,
    parse_repo_overrides,
)
from scripts.opl_doc_doctor_parts.constants import (
    build_support_profile_guard,
    build_support_repo_policy,
)
from scripts.opl_doc_doctor_parts.invariant_checks import doctor
from scripts.opl_doc_doctor_parts.plugin_sync import native_check, native_sync
from scripts.opl_doc_doctor_parts.profile_discovery import detect_profile
from scripts.opl_doc_doctor_parts.rendering import print_family_markdown


def test_doctor_entrypoint_is_command_bootstrap_not_api_facade() -> None:
    entrypoint = Path("scripts/opl_doc_doctor.py")
    source = entrypoint.read_text(encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(entrypoint), "doctor", ".", "--format", "json"],
        check=True,
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)

    assert source.count("\n") < 20
    assert "scripts.opl_doc_doctor_parts.cli import main" in source
    assert "from scripts.opl_doc_doctor_parts import (" not in source
    assert "__all__" not in source
    assert "sys.dont_write_bytecode = True" in source
    assert payload["repo_profile"] == "codex_plugin"


def test_doctor_parts_package_root_is_not_api_facade() -> None:
    package_root = Path("scripts/opl_doc_doctor_parts/__init__.py")
    source = package_root.read_text(encoding="utf-8")

    assert "from ." not in source
    assert "__all__" not in source


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
    assert payload["authority_boundary"]["doctor_role"] == "lightweight_risk_map_only"
    assert "repo_truth" in payload["authority_boundary"]["does_not_own"]
    assert "owner_receipts" in payload["authority_boundary"]["does_not_own"]


def test_detect_profile_uses_package_identity_inside_worktree_named_differently(tmp_path: Path) -> None:
    root = tmp_path / "opl-native-profile-pilot"
    root.mkdir()
    (root / "package.json").write_text('{"name":"opl-meta-agent"}\n', encoding="utf-8")

    assert detect_profile(root) == "opl_meta_agent"


def test_native_check_reports_missing_profile_without_writing(tmp_path: Path) -> None:
    root = tmp_path / "opl-meta-agent"
    docs = root / "docs" / "active"
    contracts = root / "contracts"
    docs.mkdir(parents=True)
    contracts.mkdir()
    (root / "README.md").write_text("# OMA\n", encoding="utf-8")
    (root / "AGENTS.md").write_text("# Agents\n", encoding="utf-8")
    (root / "package.json").write_text('{"scripts":{"verify":"scripts/verify.sh","test":"node --test"}}\n', encoding="utf-8")
    (root / "scripts").mkdir()
    (root / "scripts" / "verify.sh").write_text("#!/usr/bin/env bash\n", encoding="utf-8")
    (docs / "opl-meta-agent-ideal-state-gap-plan.md").write_text(
        "# OMA Gap\n\n"
        "Owner: `OMA`\nPurpose: `active_truth_plan`\nState: `active_plan`\n"
        "Machine boundary: contracts\n\n"
        "## Current State Summary\n\nok\n\n"
        "## Current-State vs Ideal-State Gaps\n\nok\n\n"
        "## Next-Round Agent Prompt\n\n"
        "Write scope: docs\n\nNon-goals: runtime\n\nLive truth inputs: contracts\n\n"
        "Verification commands: npm test\n\nCompletion gate: profile checked\n\nFoldback target: docs/status.md\n",
        encoding="utf-8",
    )

    payload = native_check(root)

    assert payload["ok"] is False
    assert payload["profile_path"] == str(root / "contracts" / "opl-native-profile.json")
    assert payload["missing"] == ["contracts/opl-native-profile.json"]
    assert payload["expected_profile"]["repo_id"] == "opl-meta-agent"
    assert payload["expected_profile"]["repo_profile"] == "opl_meta_agent"
    assert payload["expected_profile"]["doc_profile"] == "opl_meta_agent"
    assert payload["expected_profile"]["flow_profile"] == "opl_meta_agent"
    assert payload["expected_profile"]["active_truth_owner"] == "docs/active/opl-meta-agent-ideal-state-gap-plan.md"
    assert payload["expected_profile"]["verification_commands"] == [
        "scripts/verify.sh",
        "package.json:scripts.verify",
        "package.json:scripts.test",
    ]
    assert (
        payload["expected_profile"]["managed_by_plugins"]["opl-doc"]["authority_boundary"]["native_profile_role"]
        == "profile_sync_and_drift_check_only"
    )
    assert "repo_truth" in payload["expected_profile"]["managed_by_plugins"]["opl-doc"]["does_not_own"]
    assert payload["support_repo_policy"] == build_support_repo_policy()
    assert payload["support_profile_guard"] == build_support_profile_guard()
    assert payload["support_profile_guard_audit"]["schema"] == "opl_doc_support_profile_guard_audit.v1"
    assert payload["support_profile_guard_audit"]["state"] == "passed_no_resurrection_guard"
    assert payload["authority_boundary"]["native_check_can_join_default_foundry_agent_truth_set"] is False
    assert payload["false_ready_guard"]["native_check_pass_can_claim_full_goal_complete"] is False
    assert not (contracts / "opl-native-profile.json").exists()


def test_native_sync_cli_explicit_dry_run_does_not_write_profile(tmp_path: Path) -> None:
    root = tmp_path / "opl-meta-agent"
    docs = root / "docs" / "active"
    contracts = root / "contracts"
    docs.mkdir(parents=True)
    contracts.mkdir()
    (root / "README.md").write_text("# OMA\n", encoding="utf-8")
    (root / "AGENTS.md").write_text("# Agents\n", encoding="utf-8")
    (root / "package.json").write_text('{"name":"opl-meta-agent","scripts":{"test":"node --test"}}\n', encoding="utf-8")
    (docs / "opl-meta-agent-ideal-state-gap-plan.md").write_text(
        "# OMA Gap\n\n"
        "Owner: `OMA`\nPurpose: `active_truth_plan`\nState: `active_plan`\n"
        "Machine boundary: contracts\n\n"
        "## Current State Summary\n\nok\n\n"
        "## Current-State vs Ideal-State Gaps\n\nok\n\n"
        "## Next-Round Agent Prompt\n\n"
        "Write scope: docs\n\nNon-goals: runtime\n\nLive truth inputs: contracts\n\n"
        "Verification commands: npm test\n\nCompletion gate: profile checked\n\nFoldback target: docs/status.md\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "scripts/opl_doc_doctor.py",
            "native-sync",
            str(root),
            "--dry-run",
        ],
        check=True,
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
    )

    payload = json.loads(result.stdout)
    assert payload["apply"] is False
    assert payload["applied"] is False
    assert payload["planned_changes"] == [
        {"path": "contracts/opl-native-profile.json", "action": "create"}
    ]
    assert not (contracts / "opl-native-profile.json").exists()


def test_native_sync_apply_writes_profile_and_then_check_passes(tmp_path: Path) -> None:
    root = tmp_path / "med-autoscience"
    (root / "docs" / "active").mkdir(parents=True)
    (root / "contracts").mkdir()
    (root / "src").mkdir()
    (root / "tests").mkdir()
    (root / "pyproject.toml").write_text("[project]\nname='med-autoscience'\n", encoding="utf-8")
    (root / "scripts").mkdir()
    (root / "scripts" / "verify.sh").write_text("#!/usr/bin/env bash\n", encoding="utf-8")
    (root / "docs" / "active" / "mas-ideal-state-gap-plan.md").write_text(
        "# MAS Gap\n\n"
        "Owner: `MAS`\nPurpose: `active_truth_plan`\nState: `active_plan`\n"
        "Machine boundary: contracts\n\n"
        "## Current State Summary\n\nok\n\n"
        "## Current-State vs Ideal-State Gaps\n\nok\n\n"
        "## Next-Round Agent Prompt\n\n"
        "Write scope: docs\n\nNon-goals: domain truth\n\nLive truth inputs: contracts\n\n"
        "Verification commands: scripts/verify.sh\n\nCompletion gate: profile checked\n\nFoldback target: docs/status.md\n",
        encoding="utf-8",
    )

    sync_payload = native_sync(root, apply=True)

    profile_path = root / "contracts" / "opl-native-profile.json"
    assert sync_payload["applied"] is True
    assert profile_path.exists()
    assert native_check(root)["ok"] is True

    profile = __import__("json").loads(profile_path.read_text(encoding="utf-8"))
    assert profile["schema"] == "opl_native_profile.v1"
    assert profile["repo_id"] == "med-autoscience"
    assert profile["plugin_native_status"] == "profile_declared"
    assert profile["owned_by_repo"] == [
        "contracts/**",
        "src/**",
        "tests/**",
        "docs/status.md",
        "docs/active/mas-ideal-state-gap-plan.md",
    ]


def test_native_sync_apply_recomputes_profile_after_creating_contracts_dir(tmp_path: Path) -> None:
    root = tmp_path / "opl-doc"
    (root / "docs" / "active").mkdir(parents=True)
    (root / "docs").mkdir(exist_ok=True)
    (root / "tests").mkdir()
    (root / ".codex-plugin").mkdir()
    (root / "scripts").mkdir()
    (root / ".codex-plugin" / "plugin.json").write_text('{"name":"opl-doc"}\n', encoding="utf-8")
    (root / "README.md").write_text("# OPL Doc\n", encoding="utf-8")
    (root / "AGENTS.md").write_text("# Agents\n", encoding="utf-8")
    (root / "docs" / "README.md").write_text("# Docs\n", encoding="utf-8")
    (root / "docs" / "status.md").write_text("# Status\n", encoding="utf-8")
    (root / "docs" / "project.md").write_text("# Project\n", encoding="utf-8")
    (root / "docs" / "architecture.md").write_text("# Architecture\n", encoding="utf-8")
    (root / "docs" / "invariants.md").write_text("# Invariants\n", encoding="utf-8")
    (root / "docs" / "decisions.md").write_text("# Decisions\n", encoding="utf-8")
    (root / "pyproject.toml").write_text("[project]\nname='opl-doc'\n", encoding="utf-8")
    (root / "scripts" / "verify.sh").write_text("#!/usr/bin/env bash\n", encoding="utf-8")
    (root / "docs" / "active" / "opl-doc-active-truth-plan.md").write_text(
        "# Active Truth\n\n"
        "Owner: `OPL Doc`\nPurpose: `active_truth_plan`\nState: `active_plan`\n"
        "Machine boundary: tests\n\n"
        "## Current State Summary\n\nok\n\n"
        "## Current-State vs Ideal-State Gaps\n\nok\n\n"
        "## Next-Round Agent Prompt\n\n"
        "Write scope: docs\n\nNon-goals: repo truth\n\nLive truth inputs: tests\n\n"
        "Verification commands: scripts/verify.sh\n\nCompletion gate: profile checked\n\n"
        "Foldback target: docs/status.md\n",
        encoding="utf-8",
    )

    sync_payload = native_sync(root, apply=True)

    assert sync_payload["applied"] is True
    assert sync_payload["ok"] is True
    assert sync_payload["drift"] == []
    profile = json.loads((root / "contracts" / "opl-native-profile.json").read_text(encoding="utf-8"))
    assert profile["machine_truth_surfaces"] == ["contracts", "tests", "pyproject.toml"]


def test_support_repo_profile_contract_is_materialized() -> None:
    root = Path(__file__).resolve().parents[1]
    profile_path = root / "contracts" / "opl-native-profile.json"
    support_policy_path = root / "contracts" / "support-repo-policy.json"

    assert profile_path.exists()
    assert support_policy_path.exists()
    payload = native_check(root)
    assert payload["ok"] is True
    assert payload["missing"] == []
    assert payload["drift"] == []

    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    assert profile["schema"] == "opl_native_profile.v1"
    assert profile["repo_id"] == "opl-doc"
    assert profile["repo_profile"] == "codex_plugin"
    assert profile["active_truth_owner"] == "docs/active/opl-doc-active-truth-plan.md"
    assert profile["managed_by_plugins"]["opl-doc"]["authority_boundary"][
        "support_repos_role"
    ] == "extension_only_not_default_foundry_agent_truth_set"
    assert profile["managed_by_plugins"]["opl-doc"]["managed_surfaces"] == [
        "contracts/opl-native-profile.json",
        "contracts/support-repo-policy.json",
    ]
    assert "repo_truth" in profile["managed_by_plugins"]["opl-doc"]["does_not_own"]

    support_policy = json.loads(support_policy_path.read_text(encoding="utf-8"))
    assert support_policy == build_support_repo_policy()
    assert support_policy["contract_ref"] == "contracts/support-repo-policy.json"
    assert support_policy["canonical_contract_ref"] == "contracts/support-repo-policy.json"
    assert support_policy["legacy_contract_ref_alias_allowed"] is False
    assert support_policy["forbidden_legacy_contract_refs"] == [
        "contracts/support_repo_policy.json"
    ]
    assert support_policy["no_resurrection_guard"][
        "support_repos_must_not_enter_default_series_repo_set"
    ] is True
    assert support_policy["no_resurrection_guard"][
        "legacy_underscore_support_policy_ref_must_not_resurrect"
    ] is True
    assert not (root / "contracts" / "support_repo_policy.json").exists()


def test_native_check_cli_materializes_support_profile_guard_readback() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "scripts/opl_doc_doctor.py",
            "native-check",
            ".",
            "--format",
            "json",
        ],
        check=True,
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
    )

    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["support_repo_policy"] == build_support_repo_policy()
    assert payload["support_profile_guard"] == build_support_profile_guard()
    assert payload["support_profile_guard_audit"]["state"] == "passed_no_resurrection_guard"
    assert payload["support_profile_guard_audit"]["check_summary"] == {
        "total": 7,
        "passed": 7,
        "failed": 0,
    }
    assert payload["support_profile_guard_audit"]["source_readback_refs"] == [
        "scripts/opl_doc_doctor.py support-profile-check . --format json",
        "scripts/opl_doc_doctor.py family-plan --format json",
        "scripts/opl_doc_doctor.py native-check .",
    ]
    assert payload["authority_boundary"]["native_check_can_replace_repo_truth"] is False
    assert payload["authority_boundary"]["native_check_can_claim_owner_receipt"] is False
    assert payload["false_ready_guard"]["native_check_pass_can_claim_foundry_agent_truth"] is False


def test_verify_entrypoint_keeps_python_cache_outside_checkout() -> None:
    verify_script = Path("scripts/verify.sh").read_text(encoding="utf-8")
    pyproject = Path("pyproject.toml").read_text(encoding="utf-8")

    assert "OPL_DOC_REPO_TEMP_ROOT" in verify_script
    assert "PYTHONDONTWRITEBYTECODE=1" in verify_script
    assert "PYTHONPYCACHEPREFIX" in verify_script
    assert "PYTEST_ADDOPTS" in verify_script
    assert "cache_dir=$temp_root/pytest-cache" in verify_script
    assert "sys.dont_write_bytecode = True" in Path("scripts/opl_doc_doctor.py").read_text(encoding="utf-8")
    assert 'addopts = "-p no:cacheprovider"' in pyproject


def test_native_sync_preserves_other_plugin_profile_entries(tmp_path: Path) -> None:
    root = tmp_path / "one-person-lab-app"
    (root / "docs" / "active").mkdir(parents=True)
    (root / "contracts").mkdir()
    (root / "tests").mkdir()
    (root / "package.json").write_text('{"name":"one-person-lab-app","scripts":{"test":"node --test"}}\n', encoding="utf-8")
    (root / "docs" / "active" / "app-ideal-state-gap-plan.md").write_text(
        "# App Gap\n\n"
        "Owner: `APP`\nPurpose: `active_truth_plan`\nState: `active_plan`\n"
        "Machine boundary: contracts\n\n"
        "## Current State Summary\n\nok\n\n"
        "## Current-State vs Ideal-State Gaps\n\nok\n\n"
        "## Next-Round Agent Prompt\n\n"
        "Write scope: docs\n\nNon-goals: runtime\n\nLive truth inputs: contracts\n\n"
        "Verification commands: npm test\n\nCompletion gate: profile checked\n\nFoldback target: docs/status.md\n",
        encoding="utf-8",
    )
    existing = {
        "managed_by_plugins": {
            "opl-flow": {
                "version": "0.1.0",
                "management": "workflow_profile_pointer",
                "managed_surfaces": [
                    {"path": "AGENTS.md", "management": "managed_block", "kind": "repo_agent_instructions"}
                ],
            }
        }
    }
    (root / "contracts" / "opl-native-profile.json").write_text(
        __import__("json").dumps(existing, indent=2) + "\n",
        encoding="utf-8",
    )

    native_sync(root, apply=True)

    profile = __import__("json").loads((root / "contracts" / "opl-native-profile.json").read_text(encoding="utf-8"))
    assert profile["managed_by_plugins"]["opl-flow"] == existing["managed_by_plugins"]["opl-flow"]
    assert profile["managed_by_plugins"]["opl-doc"]["management"] == "profile_check_and_sync"


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
    assert not (root / ".opl-doc").exists()


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


def test_zero_residue_policy_is_not_legacy_pollution(tmp_path: Path) -> None:
    root = tmp_path / "redcube-ai"
    docs = root / "docs"
    docs.mkdir(parents=True)
    (docs / "architecture.md").write_text(
        "# Architecture\n\nOwner: `RCA`\nPurpose: `architecture`\nState: `current`\n"
        "Machine boundary: contracts\n\n"
        "这些能力及其 compatibility alias 在 active source 中必须为零。\n",
        encoding="utf-8",
    )

    payload = doctor(root)

    assert all(finding["code"] != "legacy_vocabulary_active_path" for finding in payload["findings"])


def test_history_provenance_guard_line_is_not_legacy_pollution(tmp_path: Path) -> None:
    root = tmp_path / "one-person-lab"
    active = root / "docs" / "active"
    active.mkdir(parents=True)
    (active / "current-state-vs-ideal-gap.md").write_text(
        "# Gap\n\nOwner: `OPL`\nPurpose: `gap`\nState: `active_plan`\nMachine boundary: contracts\n\n"
        "旧 gateway/frontdoor/Hermes-first wording 只作为 history/provenance/negative guard 阅读，不恢复为 active route。\n",
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


def test_doctor_detects_repo_native_active_truth_plan_names(tmp_path: Path) -> None:
    root = tmp_path / "redcube-ai"
    active = root / "docs" / "active"
    active.mkdir(parents=True)
    (root / "README.md").write_text("# RCA\n", encoding="utf-8")
    (root / "AGENTS.md").write_text("# Agents\n", encoding="utf-8")
    (active / "rca-ideal-state-gap-plan.md").write_text(
        "# RCA Gap\n\nOwner: `RCA`\nPurpose: `ideal_state_gap_plan`\nState: `active_plan`\nMachine boundary: contracts\n",
        encoding="utf-8",
    )

    payload = doctor(root)

    assert payload["active_gap_reference_docs"] == ["docs/active/rca-ideal-state-gap-plan.md"]
    assert payload["recommendation"] != "Add or map the active ideal-state gap document before long-horizon autonomous development."


def test_doctor_prefers_explicit_active_truth_purpose_outside_active_dir(tmp_path: Path) -> None:
    root = tmp_path / "opl-health-platform"
    docs = root / "docs"
    docs.mkdir(parents=True)
    (root / "README.md").write_text("# OPL Health\n", encoding="utf-8")
    (root / "AGENTS.md").write_text("# Agents\n", encoding="utf-8")
    (docs / "roadmap.md").write_text(
        "# Roadmap\n\n"
        "Owner: `OPL Health`\nPurpose: `single_active_truth_plan`\nState: `active_planning`\n"
        "Machine boundary: docs only\n\n"
        "## Current State Summary\n\nDocs-only planning.\n\n"
        "## 当前差距\n\nA specialty is not selected.\n\n"
        "## Next-Round Agent Prompt\n\n"
        "Write scope:\n- docs/scenarios/\n\n"
        "Non-goals:\n- runtime\n\n"
        "Live truth inputs:\n- owner brief\n\n"
        "Verification commands:\n- git diff --check\n\n"
        "Completion gate:\n- one scenario selected\n\n"
        "Foldback target:\n- docs/roadmap.md\n",
        encoding="utf-8",
    )

    payload = doctor(root)

    assert payload["active_gap_reference_docs"] == ["docs/roadmap.md"]
    assert payload["active_truth_health"]["owner_docs"] == ["docs/roadmap.md"]
    assert payload["active_truth_health"]["status"] == "pass"


def test_doctor_reports_multiple_explicit_active_truth_owners(tmp_path: Path) -> None:
    root = tmp_path / "opl-health-platform"
    docs = root / "docs"
    docs.mkdir(parents=True)
    (root / "README.md").write_text("# OPL Health\n", encoding="utf-8")
    (root / "AGENTS.md").write_text("# Agents\n", encoding="utf-8")
    active_truth = (
        "Owner: `OPL Health`\nPurpose: `single_active_truth_plan`\nState: `active_planning`\n"
        "Machine boundary: docs only\n\n"
        "## Current State Summary\n\nDocs-only planning.\n\n"
        "## Current Gaps\n\nOne scenario remains.\n\n"
        "## Next-Round Agent Prompt\n\n"
        "Write scope: docs\n\nNon-goals: runtime\n\nLive truth inputs: owner brief\n\n"
        "Verification commands: git diff --check\n\nCompletion gate: one owner\n\n"
        "Foldback target: docs/roadmap.md\n"
    )
    (docs / "roadmap.md").write_text("# Roadmap\n\n" + active_truth, encoding="utf-8")
    (docs / "status-plan.md").write_text("# Status Plan\n\n" + active_truth, encoding="utf-8")

    payload = doctor(root)

    assert payload["active_truth_health"]["status"] == "attention_required"
    assert payload["active_truth_health"]["owner_conflict_count"] == 1
    assert any(finding["code"] == "multiple_active_truth_owners" for finding in payload["findings"])


def test_doctor_reports_active_truth_health_for_executable_plan(tmp_path: Path) -> None:
    root = tmp_path / "one-person-lab"
    active = root / "docs" / "active"
    active.mkdir(parents=True)
    (active / "current-state-vs-ideal-gap.md").write_text(
        "# Current State vs Ideal Gap\n\n"
        "Owner: `OPL`\nPurpose: `active_truth_plan`\nState: `active_plan`\n"
        "Machine boundary: contracts\n\n"
        "## Current State Summary\n\n"
        "| Area | Current status | Live evidence |\n| --- | --- | --- |\n"
        "| runtime | partial | src/runtime.ts |\n\n"
        "## Current-State vs Ideal-State Gaps\n\n"
        "### Functional / Structural Gaps\n\n"
        "| Gap | Ideal state | Current state |\n| --- | --- | --- |\n"
        "| provider | Temporal | local proof only |\n\n"
        "### Test / Evidence Gaps\n\n"
        "| Gap | Existing implementation state | Missing evidence |\n| --- | --- | --- |\n"
        "| soak | implemented | long-soak receipt |\n\n"
        "## Next-Round Agent Prompt\n\n"
        "Write scope:\n- docs and runtime tests\n\n"
        "Non-goals:\n- domain verdicts\n\n"
        "Live truth inputs:\n- source/contracts/tests\n\n"
        "Verification commands:\n```bash\n./scripts/verify.sh\n```\n\n"
        "Completion / foldback gate:\n- active plan rewritten\n\n"
        "Foldback target:\n- docs/status.md\n",
        encoding="utf-8",
    )

    payload = doctor(root)

    health = payload["active_truth_health"]
    assert health["status"] == "pass"
    assert health["checked_doc_count"] == 1
    assert health["missing_item_count"] == 0
    assert health["documents"][0]["next_round_agent_prompt_ready"] is True
    assert all(finding["code"] != "active_truth_plan_incomplete" for finding in payload["findings"])


def test_doctor_accepts_active_goal_agent_prompt_heading(tmp_path: Path) -> None:
    root = tmp_path / "one-person-lab"
    active = root / "docs" / "active"
    active.mkdir(parents=True)
    (active / "current-state-vs-ideal-gap.md").write_text(
        "# Current State vs Ideal Gap\n\n"
        "Owner: `OPL`\nPurpose: `active_truth_plan`\nState: `active_plan`\n"
        "Machine boundary: contracts\n\n"
        "## Current State Summary\n\n"
        "| Area | Current status | Live evidence |\n| --- | --- | --- |\n"
        "| runtime | partial | src/runtime.ts |\n\n"
        "## Current-State vs Ideal-State Gaps\n\n"
        "### Functional / Structural Gaps\n\n"
        "| Gap | Ideal state | Current state |\n| --- | --- | --- |\n"
        "| provider | Temporal | local proof only |\n\n"
        "### Test / Evidence Gaps\n\n"
        "| Gap | Existing implementation state | Missing evidence |\n| --- | --- | --- |\n"
        "| soak | implemented | long-soak receipt |\n\n"
        "## Active-Goal Agent Prompt\n\n"
        "Write scope:\n- docs and runtime tests\n\n"
        "Non-goals:\n- domain verdicts\n\n"
        "Live truth inputs:\n- source/contracts/tests\n\n"
        "Verification commands:\n```bash\n./scripts/verify.sh\n```\n\n"
        "Completion / foldback gate:\n- active plan rewritten\n\n"
        "Foldback target:\n- docs/status.md\n",
        encoding="utf-8",
    )

    payload = doctor(root)

    health = payload["active_truth_health"]
    assert health["status"] == "pass"
    assert health["documents"][0]["next_round_agent_prompt_ready"] is True
    assert all(finding["code"] != "active_truth_plan_incomplete" for finding in payload["findings"])


def test_doctor_flags_active_truth_plan_without_agent_prompt_fields(tmp_path: Path) -> None:
    root = tmp_path / "med-autogrant"
    active = root / "docs" / "active"
    active.mkdir(parents=True)
    (active / "mag-ideal-state-gap-plan.md").write_text(
        "# MAG Ideal State Gap Plan\n\n"
        "Owner: `MAG`\nPurpose: `active_truth_plan`\nState: `active_plan`\n"
        "Machine boundary: contracts\n\n"
        "## Current State Summary\n\n"
        "Current state summary exists.\n\n"
        "## Current-State vs Ideal-State Gaps\n\n"
        "Functional / Structural Gaps exist.\n\n"
        "## Next-Round Agent Prompt\n\n"
        "- Fix the remaining things.\n",
        encoding="utf-8",
    )

    payload = doctor(root)

    codes = {finding["code"] for finding in payload["findings"]}
    assert payload["active_truth_health"]["status"] == "attention_required"
    assert "active_next_prompt_not_executable" in codes
    document = payload["active_truth_health"]["documents"][0]
    assert document["next_round_agent_prompt_ready"] is False
    assert "write_scope" in document["missing_next_prompt_fields"]
    assert "verification_commands" in document["missing_next_prompt_fields"]


def test_doctor_flags_process_log_headings_in_active_truth_owner(tmp_path: Path) -> None:
    root = tmp_path / "redcube-ai"
    active = root / "docs" / "active"
    active.mkdir(parents=True)
    (active / "rca-ideal-state-gap-plan.md").write_text(
        "# RCA Ideal State Gap Plan\n\n"
        "Owner: `RCA`\nPurpose: `active_truth_plan`\nState: `active_plan`\n"
        "Machine boundary: contracts\n\n"
        "## Current State Summary\n\n"
        "Current state summary exists.\n\n"
        "## Current-State vs Ideal-State Gaps\n\n"
        "Functional / Structural Gaps exist.\n\n"
        "## Next-Round Agent Prompt\n\n"
        "Write scope:\n- docs\n\n"
        "Non-goals:\n- runtime\n\n"
        "Live truth inputs:\n- contracts\n\n"
        "Verification commands:\n```bash\n./scripts/verify.sh\n```\n\n"
        "Completion / foldback gate:\n- done\n\n"
        "Foldback target:\n- docs/status.md\n\n"
        "## 执行记录\n\n"
        "- 2026-05-23 completed a lane.\n",
        encoding="utf-8",
    )

    payload = doctor(root)

    assert payload["active_truth_health"]["process_log_heading_count"] == 1
    assert any(finding["code"] == "active_process_log_in_active_doc" for finding in payload["findings"])


def test_family_plan_contains_opl_series_workflow() -> None:
    payload = family_plan()

    assert set(payload["repos"]) == {
        "opl",
        "app",
        "native_workbench",
        "flow",
        "opl_doc",
        "mas",
        "mag",
        "rca",
        "oma",
        "bookforge",
        "scholarskills",
    }
    assert payload["repos"]["oma"] == "opl-meta-agent"
    assert payload["repos"]["bookforge"] == "opl-bookforge"
    assert payload["repos"]["app"] == "one-person-lab-app"
    assert payload["repos"]["native_workbench"] == "opl-native-workbench"
    assert payload["repos"]["flow"] == "opl-flow"
    assert payload["repos"]["opl_doc"] == "opl-doc"
    assert payload["repos"]["scholarskills"] == "mas-scholar-skills"
    assert payload["support_repo_policy"]["default_included_in_governed_repo_set"] is False
    assert payload["support_repo_policy"]["extension_only"] is True
    assert payload["support_repo_policy"]["not_foundry_agent_truth_set"] is True
    assert payload["support_profile_guard"] == build_support_profile_guard()
    assert payload["support_repo_policy"]["canonical_contract_ref"] == (
        "contracts/support-repo-policy.json"
    )
    assert payload["support_repo_policy"]["legacy_contract_ref_alias_allowed"] is False
    assert payload["support_repo_policy"]["forbidden_legacy_contract_refs"] == [
        "contracts/support_repo_policy.json"
    ]
    assert (
        payload["support_profile_guard"]["state"]
        == "materialized_extension_only_support_profile_guard"
    )
    assert (
        payload["support_profile_guard"]["authority_boundary"][
            "can_join_default_foundry_agent_truth_set"
        ]
        is False
    )
    assert payload["support_repo_policy"]["support_repos"] == {"shell": "opl-aion-shell"}
    assert payload["support_profile_guard"]["canonical_support_policy_ref"] == (
        "contracts/support-repo-policy.json"
    )
    assert payload["support_profile_guard"]["legacy_contract_ref_alias_allowed"] is False
    assert payload["primary_reference_doc_count"] == 22
    assert "OPL single Active Truth plan" in payload["primary_reference_docs_per_repo"]
    assert "BOOKFORGE single Active Truth plan" in payload["primary_reference_docs_per_repo"]
    assert "APP single Active Truth plan" in payload["primary_reference_docs_per_repo"]
    assert payload["goal_mode"]["recommended"] is True
    assert "create_goal" in payload["goal_mode"]["agent_action"]
    assert any("archive" in step or "tombstone" in step for step in payload["workflow"])
    assert "verification was run on the final main checkout" in payload["completion_gate"]
    assert "global goal was not marked complete merely because one tranche finished" in payload["completion_gate"]


def test_family_plan_json_contains_original_series_governance_prompt_elements() -> None:
    payload = family_plan()

    assert len(payload["primary_reference_docs_per_repo"]) == 22
    assert {
        "evaluate_all_docs_item_by_item",
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
        "cleanup_and_archive_stale_content",
        "unique_task_positioning",
        "fold_long_incremental_lists",
        "directly_retire_outdated_modules_interfaces_tests",
        "allow_parallel_worktrees_and_subagents",
        "absorb_main_and_cleanup_when_complete",
        "long_horizon_tranche_continuation",
        "coverage_ledger_for_unfinished_docs",
    }.issubset(set(payload["governance_prompt_elements"]))
    assert "series_primary_reference_docs" in payload["governance_prompt_elements"]
    assert any("preflight risk map" in step and "governance task list" in step for step in payload["workflow"])
    assert any("workflow aids only" in step and "repo truth" in step for step in payload["workflow"])
    assert any("support extensions" in step and "Foundry Agent truth set" in step for step in payload["workflow"])
    assert any("semantic input set" in step and "SSOT owner" in step for step in payload["workflow"])
    assert any("Single Source of Truth" in step and "peer docs" in step for step in payload["workflow"])
    assert any("content theme and section" in step and "covered_by_ssot" in step for step in payload["workflow"])
    assert any("source, contracts, tests" in step and "CLI/read-model" in step for step in payload["workflow"])
    assert any("every README*" in step and "docs/**/*.md" in step for step in payload["workflow"])
    assert any("merge, archive, tombstone, or delete decision" in step and "SSOT owner" in step for step in payload["workflow"])
    assert any("active truth owner" in step for step in payload["workflow"])
    assert any("Route sections by role" in step for step in payload["workflow"])
    assert any("Active Truth" in step for step in payload["workflow"])
    assert any("active-truth-plan.md" in step for step in payload["workflow"])
    assert any("Agent prompt" in step and "/goal" in step for step in payload["workflow"])
    assert any("Before closeout" in step for step in payload["workflow"])
    assert any("docs 下其他所有文档" in step for step in payload["workflow"])
    assert any("worktree" in step and "subagent" in step for step in payload["workflow"])
    assert any("tranche" in step and "global goal" in step for step in payload["workflow"])
    assert any("coverage ledger" in step and "unreviewed" in step for step in payload["workflow"])


def test_family_plan_markdown_contains_original_series_governance_prompt_elements() -> None:
    payload = family_plan()
    output = StringIO()

    with redirect_stdout(output):
        print_family_markdown(payload)

    markdown = output.getvalue()
    assert "OPL Series Docs Lifecycle Workflow" in markdown
    assert "Goal Mode" in markdown
    assert "create or resume a /goal" in markdown
    assert "Repo Map (Workflow Baseline / Candidate Input)" in markdown
    assert "fresh owned-repo discovery required: `true`" in markdown
    assert "22 conceptual primary reference slots" in markdown
    assert "actual owners come from the frozen governed scope" in markdown
    assert "Support Repos" in markdown
    assert "Support Profile Guard" in markdown
    assert "opl-doc.support-profile.no-resurrection.v1" in markdown
    assert "profile sync / workflow plan / no-resurrection only" in markdown
    assert "explicit extensions" in markdown
    assert "not the default Foundry Agent truth set" in markdown
    assert "opl-doc" in markdown
    assert "opl-aion-shell" in markdown
    assert "single Active Truth plan" in markdown
    assert "active truth owner 发现顺序" in markdown
    assert "live repo truth 语义审计" in markdown
    assert "doctor 只做预检 guard" in markdown
    assert "唯一 Active Truth / SSOT 优先" in markdown
    assert "先定 Single Source of Truth 再内容级合并" in markdown
    assert "按语义内容治理，不按文件机械整理" in markdown
    assert "Single Source of Truth" in markdown
    assert "covered_by_ssot" in markdown
    assert "Active Truth plan 推荐形状" in markdown
    assert "按内容角色路由文档章节" in markdown
    assert "active-truth-plan.md" in markdown
    assert "下一轮 Agent prompt" in markdown
    assert "foldback closeout 闭环检查" in markdown
    assert "opl-meta-agent" in markdown
    assert "opl-bookforge" in markdown
    assert "逐条评估 README/docs 下其他所有文档和章节" in markdown
    assert "清理和归档过时内容" in markdown
    assert "每个长期文档必须有唯一任务和定位" in markdown
    assert "历史增量长清单要折叠" in markdown
    assert "过时模块/接口/测试/文档/workflow/入口" in markdown
    assert "worktree/subagent" in markdown
    assert "吸收回 main 并清理" in markdown
    assert "governance_worklist / authority-aware matrix" in markdown
    assert "fresh currentness / owner write-set gate" in markdown
    assert "逐仓验证、提交、push 和远端 ref 回读" in markdown
    assert "阻断项保留 owner、合法入口和停止条件" in markdown
    assert "fresh evidence 不越级声明 readiness" in markdown
    assert "semantic input set" in markdown
    assert "preflight risk map" in markdown
    assert "every README* and docs/**/*.md" in markdown
    assert "SSOT owner" in markdown
    assert "merge, archive, tombstone, or delete decision" in markdown
    assert "peer docs keep only entry summaries" in markdown
    assert "tranche" in markdown
    assert "coverage ledger" in markdown


def test_parse_repo_overrides_keeps_default_series_and_adds_extra_repo() -> None:
    repos = parse_repo_overrides(["award=award-agent"])

    assert set(repos) == {
        "opl",
        "app",
        "native_workbench",
        "flow",
        "opl_doc",
        "mas",
        "mag",
        "rca",
        "oma",
        "bookforge",
        "scholarskills",
        "award",
    }
    assert repos["award"] == "award-agent"


def test_default_series_repos_can_expand_from_workspace_root() -> None:
    repos = default_series_repos("/workspace")

    assert repos["opl"] == "/workspace/one-person-lab"
    assert repos["oma"] == "/workspace/opl-meta-agent"
    assert repos["bookforge"] == "/workspace/opl-bookforge"
    assert repos["app"] == "/workspace/one-person-lab-app"
    assert repos["native_workbench"] == "/workspace/opl-native-workbench"
    assert repos["flow"] == "/workspace/opl-flow"
    assert repos["opl_doc"] == "/workspace/opl-doc"
    assert repos["scholarskills"] == "/workspace/mas-scholar-skills"


def test_family_plan_goal_prompt_is_self_contained_for_codex_goal() -> None:
    payload = family_plan()

    goal_prompt = payload["goal_mode"]["objective"]
    assert "OPL series" in goal_prompt
    assert "自动创建或延续 /goal" in goal_prompt
    assert "single Active Truth plan" in goal_prompt
    assert "下一轮 Agent prompt" in goal_prompt
    assert "逐条评估" in goal_prompt
    assert "其他所有文档和章节" in goal_prompt
    assert "11 个 repo" in goal_prompt
    assert "22 个概念主参考" in goal_prompt
    assert "workflow baseline" in goal_prompt
    assert "actual governed scope" in goal_prompt
    assert "已退役或不存在的 repo 不形成 backlog" in goal_prompt
    assert "governance_worklist" in goal_prompt
    assert "authority-aware matrix" in goal_prompt
    assert "ahead/behind" in goal_prompt
    assert "远端 ref 回读" in goal_prompt
    assert "本轮 tranche" in goal_prompt
    assert "未覆盖文档" in goal_prompt
    assert "alias、facade 或 wrapper" in goal_prompt
    assert "吸收回 main" in goal_prompt
    assert "最终 main checkout" in goal_prompt

    assert payload["scope_policy"] == {
        "repo_map_role": "workflow_baseline_or_explicit_candidate_input",
        "requires_fresh_owned_repo_discovery": True,
        "actual_governed_scope_must_be_frozen_before_mutation": True,
        "retired_or_absent_repo_creates_backlog": False,
        "upstream_fork_body_write_allowed": False,
        "discovery_inputs": [
            "workspace_inventory",
            "repo_local_agent_guidance",
            "repo_local_docs_and_contracts",
            "repo_owner_markers",
            "user_scope",
        ],
    }
    assert payload["primary_reference_doc_role"] == (
        "conceptual_baseline_only_until_actual_scope_is_frozen"
    )
    assert "dynamic_owned_repo_discovery" in payload["governance_prompt_elements"]
    assert (
        "governance_worklist_and_authority_aware_matrix"
        in payload["governance_prompt_elements"]
    )
    assert (
        "per_repo_verify_commit_push_and_remote_ref_readback"
        in payload["governance_prompt_elements"]
    )
    assert any(
        "actual governed scope was fresh-discovered" in item
        for item in payload["completion_gate"]
    )
    assert any(
        "successful push by themselves to establish" in item
        for item in payload["workflow"]
    )


def test_family_plan_support_repos_are_extension_only() -> None:
    payload = family_plan()
    contract_policy = json.loads(
        Path("contracts/support-repo-policy.json").read_text(encoding="utf-8")
    )

    assert set(payload["repos"]) == {
        "opl",
        "app",
        "native_workbench",
        "flow",
        "opl_doc",
        "mas",
        "mag",
        "rca",
        "oma",
        "bookforge",
        "scholarskills",
    }
    assert "shell" not in payload["repos"]
    policy = payload["support_repo_policy"]
    profile_guard = payload["support_profile_guard"]
    profile_guard_audit = payload["support_profile_guard_audit"]
    assert policy == contract_policy == build_support_repo_policy()
    assert profile_guard == build_support_profile_guard()
    assert profile_guard_audit["schema"] == "opl_doc_support_profile_guard_audit.v1"
    assert profile_guard_audit["state"] == "passed_no_resurrection_guard"
    assert profile_guard_audit["check_summary"] == {
        "total": 7,
        "passed": 7,
        "failed": 0,
    }
    assert profile_guard_audit["source_contract_refs"] == [
        "contracts/opl-native-profile.json",
        "contracts/support-repo-policy.json",
    ]
    assert profile_guard_audit["source_readback_refs"] == [
        "scripts/opl_doc_doctor.py support-profile-check . --format json",
        "scripts/opl_doc_doctor.py family-plan --format json",
        "scripts/opl_doc_doctor.py native-check .",
    ]
    assert profile_guard_audit["default_governed_repo_ids"] == [
        "app",
        "bookforge",
        "flow",
        "mag",
        "mas",
        "native_workbench",
        "oma",
        "opl",
        "opl_doc",
        "rca",
        "scholarskills",
    ]
    assert profile_guard_audit["support_repo_ids"] == ["shell"]
    assert profile_guard_audit["support_repo_names"] == ["opl-aion-shell"]
    assert profile_guard_audit["forbidden_legacy_contract_refs_present"] == []
    assert {
        check["check_id"]: check["status"]
        for check in profile_guard_audit["checks"]
    } == {
        "support_policy_contract_matches_generated_policy": "passed",
        "native_profile_declares_support_extension_only": "passed",
        "default_governed_repo_ids_exclude_support_repo_ids": "passed",
        "default_governed_repo_names_exclude_support_repo_names": "passed",
        "legacy_support_repo_policy_ref_absent": "passed",
        "support_guard_derived_from_canonical_policy": "passed",
        "support_guard_false_ready_flags_fail_closed": "passed",
    }
    assert profile_guard_audit["authority_boundary"]["audit_can_join_default_foundry_agent_truth_set"] is False
    assert profile_guard_audit["false_ready_guard"]["audit_pass_can_claim_full_goal_complete"] is False
    assert profile_guard["source_contract_refs"] == [
        "contracts/opl-native-profile.json",
        "contracts/support-repo-policy.json",
    ]
    assert profile_guard["canonical_support_policy_ref"] == "contracts/support-repo-policy.json"
    assert profile_guard["legacy_contract_ref_alias_allowed"] is False
    assert profile_guard["forbidden_legacy_contract_refs"] == [
        "contracts/support_repo_policy.json"
    ]
    assert profile_guard["derived_from_support_repo_policy"] is True
    assert profile_guard["native_profile_must_declare_extension_only"] is True
    assert profile_guard["family_plan_must_emit_this_guard"] is True
    assert profile_guard["support_repo_names"] == ["opl-aion-shell"]
    assert (
        profile_guard["false_ready_guard"][
            "support_profile_materialized_can_claim_foundry_agent_truth"
        ]
        is False
    )
    assert (
        profile_guard["false_ready_guard"][
            "support_profile_materialized_can_claim_production_ready"
        ]
        is False
    )
    assert (
        profile_guard["authority_boundary"]["can_create_second_active_backlog"]
        is False
    )
    assert (
        profile_guard["no_resurrection_guard"]
        == policy["no_resurrection_guard"]
    )
    assert policy["authority_boundary"]["family_plan_role"] == "workflow_plan_only"
    assert policy["authority_boundary"]["support_repos_role"] == "extension_only_not_default_foundry_agent_truth_set"
    assert "foundry_agent_truth_set" in policy["authority_boundary"]["does_not_own"]
    assert "owner_receipts" in policy["authority_boundary"]["does_not_own"]
    assert "user_explicitly_requests_support_repo_governance" in policy["include_only_when"]
    guard = policy["no_resurrection_guard"]
    assert guard["default_series_repo_ids_must_exclude_support_repo_ids"] == ["shell"]
    assert guard["default_series_repo_names_must_exclude_support_repo_names"] == [
        "opl-aion-shell",
    ]
    assert guard["legacy_underscore_support_policy_ref_must_not_resurrect"] is True
    assert guard["legacy_contract_ref_alias_allowed"] is False


def test_support_profile_check_cli_is_direct_strict_readback() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "scripts/opl_doc_doctor.py",
            "support-profile-check",
            ".",
            "--format",
            "json",
        ],
        check=True,
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
    )

    payload = json.loads(result.stdout)
    assert payload["schema"] == "opl_doc_support_profile_guard_audit.v1"
    assert payload["state"] == "passed_no_resurrection_guard"
    assert payload["check_summary"] == {
        "total": 7,
        "passed": 7,
        "failed": 0,
    }
    assert payload["authority_boundary"]["audit_can_replace_repo_truth"] is False
    assert payload["authority_boundary"]["audit_can_claim_owner_receipt"] is False
    assert payload["false_ready_guard"]["audit_pass_can_claim_production_ready"] is False


def test_support_profile_check_accepts_json_alias_without_new_contract_path() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "scripts/opl_doc_doctor.py",
            "support-profile-check",
            ".",
            "--json",
        ],
        check=True,
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
    )

    payload = json.loads(result.stdout)
    assert payload["schema"] == "opl_doc_support_profile_guard_audit.v1"
    assert payload["state"] == "passed_no_resurrection_guard"
    assert payload["source_readback_refs"] == [
        "scripts/opl_doc_doctor.py support-profile-check . --format json",
        "scripts/opl_doc_doctor.py family-plan --format json",
        "scripts/opl_doc_doctor.py native-check .",
    ]
    assert payload["authority_boundary"]["audit_can_join_default_foundry_agent_truth_set"] is False
    assert payload["false_ready_guard"]["audit_pass_can_claim_full_goal_complete"] is False


def test_support_profile_guard_audit_fails_when_support_repo_or_legacy_ref_resurrects(tmp_path: Path) -> None:
    root = tmp_path / "opl-doc"
    (root / "contracts").mkdir(parents=True)
    (root / "contracts" / "opl-native-profile.json").write_text(
        json.dumps(
            {
                "managed_by_plugins": {
                    "opl-doc": {
                        "authority_boundary": {
                            "support_repos_role": "extension_only_not_default_foundry_agent_truth_set"
                        }
                    }
                }
            }
        ),
        encoding="utf-8",
    )
    (root / "contracts" / "support-repo-policy.json").write_text(
        json.dumps(build_support_repo_policy()),
        encoding="utf-8",
    )
    (root / "contracts" / "support_repo_policy.json").write_text("{}", encoding="utf-8")

    audit = build_support_profile_guard_audit(
        {"shell": "opl-aion-shell", "opl": "one-person-lab"},
        repo_root=root,
    )

    checks = {
        check["check_id"]: check["status"]
        for check in audit["checks"]
    }
    assert audit["state"] == "failed"
    assert checks["default_governed_repo_ids_exclude_support_repo_ids"] == "failed"
    assert checks["default_governed_repo_names_exclude_support_repo_names"] == "failed"
    assert checks["legacy_support_repo_policy_ref_absent"] == "failed"
    assert audit["forbidden_legacy_contract_refs_present"] == [
        "contracts/support_repo_policy.json"
    ]
    assert audit["authority_boundary"]["audit_can_claim_production_readiness"] is False
    assert audit["false_ready_guard"]["audit_pass_can_claim_foundry_agent_truth"] is False


def test_support_profile_check_cli_fails_closed_for_legacy_policy_ref(tmp_path: Path) -> None:
    root = tmp_path / "opl-doc"
    (root / "contracts").mkdir(parents=True)
    (root / "contracts" / "opl-native-profile.json").write_text(
        json.dumps(
            {
                "managed_by_plugins": {
                    "opl-doc": {
                        "authority_boundary": {
                            "support_repos_role": "extension_only_not_default_foundry_agent_truth_set"
                        }
                    }
                }
            }
        ),
        encoding="utf-8",
    )
    (root / "contracts" / "support-repo-policy.json").write_text(
        json.dumps(build_support_repo_policy()),
        encoding="utf-8",
    )
    (root / "contracts" / "support_repo_policy.json").write_text("{}", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/opl_doc_doctor.py",
            "support-profile-check",
            str(root),
            "--format",
            "json",
        ],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)

    assert result.returncode == 1
    assert payload["state"] == "failed"
    assert payload["check_summary"]["failed"] >= 1
    assert payload["forbidden_legacy_contract_refs_present"] == [
        "contracts/support_repo_policy.json"
    ]


def test_verify_script_exposes_support_profile_strict_lane() -> None:
    verify_script = Path("scripts/verify.sh").read_text(encoding="utf-8")

    assert "support-profile|support-profile-strict|support-profile:strict" in verify_script
    assert "support-profile-check . --format json" in verify_script
    assert "opl-doc-support-profile-check.json" in verify_script

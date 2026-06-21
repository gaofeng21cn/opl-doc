"""Shared constants for the OPL document lifecycle doctor."""

from __future__ import annotations

import re


CORE_DOCS = [
    "README.md",
    "AGENTS.md",
    "TASTE.md",
    "docs/README.md",
    "docs/project.md",
    "docs/status.md",
    "docs/architecture.md",
    "docs/invariants.md",
    "docs/decisions.md",
]

FAMILY_REFERENCE_DOCS = [
    "docs/active/current-state-vs-ideal-gap.md",
    "docs/active/production-framework-closure-gap-matrix.md",
]

ACTIVE_TRUTH_DOC_NAME_RE = re.compile(
    r"(?:current-state.*ideal.*gap|ideal.*(?:state)?.*gap.*plan|active.*truth.*plan)",
    re.IGNORECASE,
)

CANONICAL_DOC_DIRS = [
    "docs/active",
    "docs/public",
    "docs/product",
    "docs/runtime",
    "docs/delivery",
    "docs/source",
    "docs/policies",
    "docs/specs",
    "docs/references",
    "docs/history",
]

NATIVE_PROFILE_REL_PATH = "contracts/opl-native-profile.json"
SUPPORT_REPO_POLICY_REL_PATH = "contracts/support-repo-policy.json"

HEADER_FIELDS = ("Owner:", "Purpose:", "State:", "Machine boundary:")

LEGACY_ACTIVE_TOKENS = (
    "frontdoor",
    "gateway-first",
    "federation-first",
    "Hermes-first",
    "compatibility alias",
    "兼容入口",
    "兼容面",
)

RETIREMENT_NEGATION_MARKERS = (
    "不保留",
    "不得保留",
    "不新增",
    "不得新增",
    "不恢复",
    "不得恢复",
    "不再",
    "只作为",
    "只作",
    "只保留",
    "只允许",
    "历史",
    "退役",
    "已退役",
    "保留为",
    "superseded",
    "history",
    "historical",
    "provenance",
    "diagnostic",
    "fixture",
    "negative guard",
    "tombstone",
    "direct retirement",
    "no compatibility",
)

DEFAULT_SERIES_REPO_NAMES = {
    "opl": "one-person-lab",
    "mas": "med-autoscience",
    "mag": "med-autogrant",
    "rca": "redcube-ai",
    "oma": "opl-meta-agent",
    "bookforge": "opl-bookforge",
    "app": "one-person-lab-app",
}

DEFAULT_SUPPORT_REPO_NAMES = {
    "opl_doc": "opl-doc",
    "shell": "opl-aion-shell",
}

SUPPORT_REPO_INCLUDE_ONLY_WHEN = [
    "user_explicitly_requests_support_repo_governance",
    "current_task_touches_support_repo_docs_or_scripts",
    "support_repo_is_needed_to_explain_workflow_or_shell_carrier_boundary",
]

OPL_DOC_AUTHORITY_BOUNDARY = {
    "doctor_role": "lightweight_risk_map_only",
    "native_profile_role": "profile_sync_and_drift_check_only",
    "family_plan_role": "workflow_plan_only",
    "support_repos_role": "extension_only_not_default_foundry_agent_truth_set",
    "does_not_own": [
        "repo_truth",
        "runtime_truth",
        "domain_truth",
        "artifact_authority",
        "quality_verdicts",
        "owner_receipts",
        "production_readiness",
        "foundry_agent_truth_set",
    ],
}


def build_support_repo_policy() -> dict[str, object]:
    return {
        "schema": "opl_doc_support_repo_policy.v1",
        "policy_id": "opl-doc.support-repo-policy.v1",
        "state": "extension_only_not_default_foundry_agent_truth_set",
        "default_included_in_governed_repo_set": False,
        "extension_only": True,
        "not_foundry_agent_truth_set": True,
        "support_repos": dict(DEFAULT_SUPPORT_REPO_NAMES),
        "authority_boundary": OPL_DOC_AUTHORITY_BOUNDARY,
        "include_only_when": list(SUPPORT_REPO_INCLUDE_ONLY_WHEN),
        "contract_ref": SUPPORT_REPO_POLICY_REL_PATH,
        "no_resurrection_guard": {
            "support_repos_must_not_enter_default_series_repo_set": True,
            "family_plan_must_derive_support_policy_from_this_source": True,
            "native_profile_must_keep_support_repo_role_extension_only": True,
            "default_series_repo_ids_must_exclude_support_repo_ids": sorted(
                DEFAULT_SUPPORT_REPO_NAMES
            ),
            "default_series_repo_names_must_exclude_support_repo_names": sorted(
                DEFAULT_SUPPORT_REPO_NAMES.values()
            ),
        },
    }

DATED_HEADING_RISK_THRESHOLD = 5
CHECKBOX_LIST_RISK_THRESHOLD = 10

AGENT_GUIDANCE_DOCS = (
    "AGENTS.md",
    "TASTE.md",
    "CLAUDE.md",
    "GEMINI.md",
    ".github/copilot-instructions.md",
)

MACHINE_TRUTH_SURFACES = (
    "contracts",
    "schemas",
    "src",
    "tests",
    "package.json",
    "pyproject.toml",
)

PACKAGE_SCRIPT_VERIFICATION_ORDER = (
    "verify",
    "test",
    "test:fast",
    "test:meta",
    "test:full",
    "build",
    "lint",
    "typecheck",
)

DATED_HEADING_RE = re.compile(
    r"^#{1,6}\s+"
    r"(?:\d{4}[-/.]\d{1,2}(?:[-/.]\d{1,2})?|\d{1,2}[-/.]\d{1,2}[-/.]\d{2,4})"
    r"(?:\b|[：:\s-])"
)
CHECKBOX_ITEM_RE = re.compile(r"^\s*[-*+]\s+\[[ xX]\]\s+")
PROCESS_LOG_HEADING_RE = re.compile(
    r"^#{1,6}\s+"
    r"(?:execution log|process log|closeout log|timeline|changelog|"
    r"执行记录|执行流水|过程记录|完成记录|变更记录|历史增量)"
    r"(?:\b|[：:\s-])",
    re.IGNORECASE,
)

ACTIVE_PROGRESS_MARKERS = (
    "Current Completion Progress",
    "Current progress",
    "当前完成进度",
    "完成进度",
)

ACTIVE_GAP_MARKERS = (
    "Current-State vs Ideal-State Gaps",
    "Functional / Structural Gaps",
    "Test / Evidence Gaps",
    "现状与理想",
    "功能/结构差距",
    "测试/证据差距",
)

NEXT_AGENT_PROMPT_MARKERS = (
    "Active-Goal Agent Prompt",
    "Active Goal Agent Prompt",
    "Next-Round Agent Prompt",
    "Next-round Agent Prompt",
    "Active-Goal Agent prompt",
    "Active Goal Agent prompt",
    "下一轮 Agent prompt",
    "下一轮 Agent Prompt",
    "下一轮提示词",
)

NEXT_AGENT_PROMPT_REQUIRED_MARKERS = {
    "write_scope": ("Write scope", "写入范围", "变更范围", "写入边界"),
    "non_goals": ("Non-goals", "Non-goals:", "禁止范围", "非目标", "不改范围"),
    "live_truth_inputs": (
        "Live truth inputs",
        "live truth 输入",
        "live repo truth",
        "当前事实输入",
        "读取面",
    ),
    "verification_commands": ("Verification commands", "验证命令", "验证入口"),
    "completion_gate": ("Completion", "completion gate", "完成口径", "完成门槛"),
    "foldback_target": ("Foldback", "foldback", "折回", "归档目标", "foldback target"),
}

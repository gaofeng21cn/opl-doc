#!/usr/bin/env python3
"""OPL-native document lifecycle doctor."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


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
    "app": "one-person-lab-app",
}

DEFAULT_SUPPORT_REPO_NAMES = {
    "opl_doc": "opl-doc",
    "shell": "opl-aion-shell",
}

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
    "Next-Round Agent Prompt",
    "Next-round Agent Prompt",
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


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    path: str
    message: str
    action: str

    def to_json(self) -> dict[str, str]:
        return {
            "severity": self.severity,
            "code": self.code,
            "path": self.path,
            "message": self.message,
            "action": self.action,
        }


def rel_exists(root: Path, rel_path: str) -> bool:
    return (root / rel_path).exists()


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(errors="ignore")


def package_json_scripts(root: Path) -> dict[str, str]:
    package_json = root / "package.json"
    if not package_json.exists():
        return {}
    try:
        payload = json.loads(read_text(package_json))
    except json.JSONDecodeError:
        return {}
    scripts = payload.get("scripts")
    return scripts if isinstance(scripts, dict) else {}


def package_json_name(root: Path) -> str | None:
    package_json = root / "package.json"
    if not package_json.exists():
        return None
    try:
        payload = json.loads(read_text(package_json))
    except json.JSONDecodeError:
        return None
    name = payload.get("name")
    return name if isinstance(name, str) and name else None


def pyproject_name(root: Path) -> str | None:
    pyproject = root / "pyproject.toml"
    if not pyproject.exists():
        return None
    for line in read_text(pyproject).splitlines():
        match = re.match(r'\s*name\s*=\s*["\']([^"\']+)["\']', line)
        if match:
            return match.group(1)
    return None


def repo_identity(root: Path) -> str:
    package_name = package_json_name(root)
    if package_name == "opl-framework-shared":
        return "one-person-lab"
    if package_name == "redcube-ai-mono":
        return "redcube-ai"
    return package_name or pyproject_name(root) or root.name


def detect_profile(root: Path) -> str:
    name = repo_identity(root)
    if name == "one-person-lab":
        return "opl_framework"
    if name == "one-person-lab-app":
        return "opl_app"
    if name in {"med-autoscience", "med-autogrant", "redcube-ai"}:
        return "foundry_agent"
    if name == "opl-meta-agent":
        return "opl_meta_agent"
    if rel_exists(root, ".codex-plugin/plugin.json") or rel_exists(root, "skills"):
        return "codex_plugin"
    if rel_exists(root, "pyproject.toml") or rel_exists(root, "package.json"):
        return "tooling_repo"
    return "generic_repo"


def inspect_repo_native_surfaces(root: Path, core_status: dict[str, bool]) -> dict[str, Any]:
    package_scripts = package_json_scripts(root)
    verification = []
    if rel_exists(root, "scripts/verify.sh"):
        verification.append("scripts/verify.sh")
    for script_name in PACKAGE_SCRIPT_VERIFICATION_ORDER:
        if script_name in package_scripts:
            verification.append(f"package.json:scripts.{script_name}")
    if rel_exists(root, "pyproject.toml") and rel_exists(root, "tests"):
        verification.append("python -m pytest")

    return {
        "agent_guidance": [
            path for path in AGENT_GUIDANCE_DOCS if rel_exists(root, path)
        ],
        "canonical_docs": {
            "present": [path for path, exists in core_status.items() if exists],
            "missing": [path for path, exists in core_status.items() if not exists],
        },
        "machine_truth": [
            path for path in MACHINE_TRUTH_SURFACES if rel_exists(root, path)
        ],
        "verification": verification,
    }


def inspect_header(path: Path) -> dict[str, bool]:
    if not path.exists() or not path.is_file():
        return {field: False for field in HEADER_FIELDS}
    head = "\n".join(read_text(path).splitlines()[:12])
    return {field: field in head for field in HEADER_FIELDS}


def list_markdown_docs(root: Path) -> list[Path]:
    docs_root = root / "docs"
    if not docs_root.exists():
        return []
    return sorted(path for path in docs_root.rglob("*.md") if path.is_file())


def is_history_path(path: Path) -> bool:
    return "docs/history/" in path.as_posix()


def is_active_rel_path(rel_path: str) -> bool:
    return rel_path.startswith("docs/active/")


def has_legacy_resurrection(text: str, token: str) -> bool:
    for line in text.splitlines():
        if token not in line:
            continue
        if any(marker in line for marker in RETIREMENT_NEGATION_MARKERS):
            continue
        return True
    return False


def incremental_list_risk_details(text: str) -> list[str]:
    lines = text.splitlines()
    dated_headings = sum(1 for line in lines if DATED_HEADING_RE.match(line))
    checkbox_items = sum(1 for line in lines if CHECKBOX_ITEM_RE.match(line))

    details: list[str] = []
    if dated_headings >= DATED_HEADING_RISK_THRESHOLD:
        details.append(f"{dated_headings} dated headings")
    if checkbox_items >= CHECKBOX_LIST_RISK_THRESHOLD:
        details.append(f"{checkbox_items} checkbox items")
    return details


def active_truth_reference_docs(root: Path) -> list[str]:
    refs = [
        path
        for path in FAMILY_REFERENCE_DOCS
        if rel_exists(root, path)
    ]
    active_root = root / "docs" / "active"
    if not active_root.exists():
        return refs
    for doc in sorted(active_root.glob("*.md")):
        rel = doc.relative_to(root).as_posix()
        if rel in refs:
            continue
        if ACTIVE_TRUTH_DOC_NAME_RE.search(doc.name):
            refs.append(rel)
    return refs


def active_truth_owner_docs(root: Path, active_gap_docs: list[str]) -> list[str]:
    owner_docs = [
        rel
        for rel in active_gap_docs
        if ACTIVE_TRUTH_DOC_NAME_RE.search(Path(rel).name)
    ]
    return owner_docs or active_gap_docs


def contains_marker(text: str, markers: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(marker.lower() in lowered for marker in markers)


def missing_next_prompt_marker_groups(text: str) -> list[str]:
    return [
        group
        for group, markers in NEXT_AGENT_PROMPT_REQUIRED_MARKERS.items()
        if not contains_marker(text, markers)
    ]


def process_log_headings(text: str) -> list[str]:
    return [
        line.strip()
        for line in text.splitlines()
        if PROCESS_LOG_HEADING_RE.match(line)
    ]


def inspect_active_truth_health(root: Path, active_gap_docs: list[str]) -> dict[str, Any]:
    owner_docs = active_truth_owner_docs(root, active_gap_docs)
    documents = []
    missing_total = 0
    process_log_total = 0
    prompt_not_ready_total = 0

    for rel in owner_docs:
        path = root / rel
        text = read_text(path) if path.exists() else ""
        has_progress = contains_marker(text, ACTIVE_PROGRESS_MARKERS)
        has_gaps = contains_marker(text, ACTIVE_GAP_MARKERS)
        has_next_prompt = contains_marker(text, NEXT_AGENT_PROMPT_MARKERS)
        missing_prompt_groups = (
            missing_next_prompt_marker_groups(text) if has_next_prompt else list(NEXT_AGENT_PROMPT_REQUIRED_MARKERS)
        )
        headings = process_log_headings(text)
        missing_items = []
        if not has_progress:
            missing_items.append("current_completion_progress")
        if not has_gaps:
            missing_items.append("current_state_vs_ideal_gaps")
        if not has_next_prompt:
            missing_items.append("next_round_agent_prompt")
        if missing_prompt_groups:
            missing_items.append("next_round_agent_prompt_executable_fields")

        missing_total += len(missing_items)
        process_log_total += len(headings)
        if missing_prompt_groups:
            prompt_not_ready_total += 1

        documents.append(
            {
                "path": rel,
                "has_current_completion_progress": has_progress,
                "has_current_state_vs_ideal_gaps": has_gaps,
                "has_next_round_agent_prompt": has_next_prompt,
                "next_round_agent_prompt_ready": has_next_prompt and not missing_prompt_groups,
                "missing_next_prompt_fields": missing_prompt_groups,
                "process_log_headings": headings,
                "missing_items": missing_items,
            }
        )

    status = "pass"
    if not owner_docs:
        status = "missing_active_truth_owner"
    elif missing_total or process_log_total:
        status = "attention_required"

    return {
        "status": status,
        "owner_docs": owner_docs,
        "checked_doc_count": len(owner_docs),
        "missing_item_count": missing_total,
        "process_log_heading_count": process_log_total,
        "next_round_agent_prompt_not_ready_count": prompt_not_ready_total,
        "documents": documents,
    }


def doctor(root: Path) -> dict[str, Any]:
    root = root.resolve()
    profile = detect_profile(root)
    docs = list_markdown_docs(root)
    findings: list[Finding] = []

    core_status = {path: rel_exists(root, path) for path in CORE_DOCS}
    repo_native_surfaces = inspect_repo_native_surfaces(root, core_status)
    dir_status = {path: rel_exists(root, path) for path in CANONICAL_DOC_DIRS}

    for path, exists in core_status.items():
        if not exists and path not in {"TASTE.md", "docs/decisions.md"}:
            findings.append(
                Finding(
                    "warning",
                    "missing_canonical_doc",
                    path,
                    "canonical OPL governance document is absent",
                    "create, map to an existing canonical doc, or document why this repo profile does not need it",
                )
            )

    for doc in docs:
        rel = doc.relative_to(root).as_posix()
        if is_history_path(doc):
            continue
        header = inspect_header(doc)
        missing = [field for field, present in header.items() if not present]
        if missing:
            findings.append(
                Finding(
                    "info",
                    "missing_lifecycle_header",
                    rel,
                    f"missing lifecycle header fields: {', '.join(missing)}",
                    "add Owner/Purpose/State/Machine boundary if this is a long-lived governance doc",
                )
            )

        text = read_text(doc)
        legacy_hits = [
            token
            for token in LEGACY_ACTIVE_TOKENS
            if has_legacy_resurrection(text, token)
        ]
        if legacy_hits and not is_history_path(doc):
            findings.append(
                Finding(
                    "warning",
                    "legacy_vocabulary_active_path",
                    rel,
                    f"active doc contains legacy or compatibility vocabulary: {', '.join(legacy_hits[:3])}",
                    "move historical wording to docs/history or rewrite as tombstone/provenance with current owner truth",
                )
            )

        incremental_risks = incremental_list_risk_details(text) if is_active_rel_path(rel) else []
        if incremental_risks:
            findings.append(
                Finding(
                    "warning",
                    "long_incremental_list_risk",
                    rel,
                    f"active doc has long incremental-list shape: {', '.join(incremental_risks)}",
                    "fold into compact current-state tables, preserve necessary provenance under docs/history, and keep the active doc focused on current tasks",
                )
            )

    active_gap_docs = active_truth_reference_docs(root)
    active_truth_health = inspect_active_truth_health(root, active_gap_docs)

    if not active_truth_health["owner_docs"] and profile in {"opl_framework", "foundry_agent", "opl_meta_agent"}:
        findings.append(
            Finding(
                "warning",
                "active_truth_owner_missing",
                "docs/active",
                "repo has no detected single Active Truth owner for current progress, gaps, and next-round prompt",
                "map or create one active truth owner before autonomous long-horizon development",
            )
        )
    for document in active_truth_health["documents"]:
        path = document["path"]
        missing_items = document["missing_items"]
        if any(
            item in missing_items
            for item in (
                "current_completion_progress",
                "current_state_vs_ideal_gaps",
                "next_round_agent_prompt",
            )
        ):
            findings.append(
                Finding(
                    "warning",
                    "active_truth_plan_incomplete",
                    path,
                    f"active truth owner is missing: {', '.join(missing_items)}",
                    "rewrite the active owner to current progress, current gaps, and an executable next-round Agent prompt",
                )
            )
        elif "next_round_agent_prompt_executable_fields" in missing_items:
            findings.append(
                Finding(
                    "warning",
                    "active_next_prompt_not_executable",
                    path,
                    "next-round Agent prompt exists but lacks executable fields",
                    "include write scope, non-goals, live truth inputs, verification commands, completion gate, and foldback target",
                )
            )
        if document["process_log_headings"]:
            findings.append(
                Finding(
                    "warning",
                    "active_process_log_in_active_doc",
                    path,
                    "active truth owner contains process-log headings: "
                    + ", ".join(document["process_log_headings"][:3]),
                    "move execution diaries, closeout logs, and historical timelines to docs/history or tombstone/provenance",
                )
            )

    return {
        "root": str(root),
        "repo_profile": profile,
        "repo_native_surfaces": repo_native_surfaces,
        "core_docs": core_status,
        "canonical_dirs": dir_status,
        "markdown_doc_count": len(docs),
        "active_gap_reference_docs": active_gap_docs,
        "active_truth_health": active_truth_health,
        "authority_boundary": OPL_DOC_AUTHORITY_BOUNDARY,
        "finding_count": len(findings),
        "findings": [finding.to_json() for finding in findings],
        "recommendation": recommend(profile, findings, active_gap_docs, active_truth_health),
    }


def _profile_doc_role(path: str) -> str:
    roles = {
        "README.md": "root_entry",
        "AGENTS.md": "repo_agent_working_rules",
        "TASTE.md": "maintenance_preferences",
        "docs/README.md": "docs_entry",
        "docs/project.md": "project_positioning",
        "docs/status.md": "current_status",
        "docs/architecture.md": "architecture_boundary",
        "docs/invariants.md": "hard_constraints",
        "docs/decisions.md": "active_decision_record",
    }
    return roles.get(path, "canonical_doc")


def _owned_by_repo(active_truth_owner: str | None) -> list[str]:
    owned = ["contracts/**", "src/**", "tests/**", "docs/status.md"]
    if active_truth_owner:
        owned.append(active_truth_owner)
    return owned


def expected_native_profile(root: Path, current: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = doctor(root)
    surfaces = payload["repo_native_surfaces"]
    active_truth_owner = next(iter(payload["active_truth_health"]["owner_docs"]), None)
    canonical_docs = [
        {"path": path, "role": _profile_doc_role(path)}
        for path in surfaces["canonical_docs"]["present"]
    ]
    taxonomy_dirs = [
        path
        for path, exists in payload["canonical_dirs"].items()
        if exists
    ]
    repo_profile = payload["repo_profile"]
    managed_by_plugins = dict((current or {}).get("managed_by_plugins") or {})
    managed_by_plugins["opl-doc"] = {
        "management": "profile_check_and_sync",
        "managed_surfaces": [NATIVE_PROFILE_REL_PATH],
        "authority_boundary": OPL_DOC_AUTHORITY_BOUNDARY,
        "does_not_own": [
            "repo_truth",
            "domain_truth",
            "runtime_truth",
            "artifact_authority",
            "owner_receipts",
            "quality_verdicts",
            "production_readiness",
        ],
    }
    return {
        "schema": "opl_native_profile.v1",
        "repo_id": repo_identity(root),
        "repo_profile": repo_profile,
        "flow_profile": repo_profile,
        "doc_profile": repo_profile,
        "active_truth_owner": active_truth_owner,
        "canonical_docs": canonical_docs,
        "taxonomy_dirs": taxonomy_dirs,
        "machine_truth_surfaces": surfaces["machine_truth"],
        "verification_commands": surfaces["verification"],
        "owned_by_repo": _owned_by_repo(active_truth_owner),
        "managed_by_plugins": managed_by_plugins,
        "plugin_native_status": "profile_declared",
    }


def _native_profile_text(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def _load_native_profile(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    if not path.exists():
        return None, None
    try:
        payload = json.loads(read_text(path))
    except json.JSONDecodeError as exc:
        return None, f"{NATIVE_PROFILE_REL_PATH} is not valid JSON: {exc}"
    if not isinstance(payload, dict):
        return None, f"{NATIVE_PROFILE_REL_PATH} must contain a JSON object"
    return payload, None


def native_check(root: Path) -> dict[str, Any]:
    root = root.resolve()
    profile_path = root / NATIVE_PROFILE_REL_PATH
    current, load_error = _load_native_profile(profile_path)
    expected = expected_native_profile(root, current)
    missing = [] if profile_path.exists() else [NATIVE_PROFILE_REL_PATH]
    errors = [load_error] if load_error else []
    drift: list[str] = []
    if current is not None:
        for key, expected_value in expected.items():
            if current.get(key) != expected_value:
                drift.append(key)
    ok = not missing and not errors and not drift
    return {
        "ok": ok,
        "mode": "native-check",
        "apply": False,
        "repo_root": str(root),
        "profile_path": str(profile_path),
        "missing": missing,
        "errors": errors,
        "drift": drift,
        "expected_profile": expected,
    }


def native_sync(root: Path, apply: bool = False) -> dict[str, Any]:
    root = root.resolve()
    profile_path = root / NATIVE_PROFILE_REL_PATH
    current, _load_error = _load_native_profile(profile_path)
    expected = expected_native_profile(root, current)
    expected_text = _native_profile_text(expected)
    current_text = read_text(profile_path) if profile_path.exists() else None
    planned_changes = []
    if current_text != expected_text:
        planned_changes.append(
            {
                "path": NATIVE_PROFILE_REL_PATH,
                "action": "create" if current_text is None else "update",
            }
        )
    if apply and planned_changes:
        profile_path.parent.mkdir(parents=True, exist_ok=True)
        profile_path.write_text(expected_text, encoding="utf-8")
    check = native_check(root)
    return {
        **check,
        "mode": "native-sync",
        "apply": apply,
        "applied": bool(apply and planned_changes),
        "planned_changes": planned_changes,
    }


def recommend(
    profile: str,
    findings: list[Finding],
    active_gap_docs: list[str],
    active_truth_health: dict[str, Any],
) -> str:
    if any(finding.code == "legacy_vocabulary_active_path" for finding in findings):
        return "Run an active-doc retirement pass: rewrite current truth, then archive or tombstone stale historical wording."
    if active_truth_health["status"] == "attention_required":
        return "Refresh the Active Truth owner from live repo truth before autonomous development."
    if not active_gap_docs and profile in {"opl_framework", "foundry_agent"}:
        return "Add or map the active ideal-state gap document before long-horizon autonomous development."
    if findings:
        return "Patch lifecycle headers and canonical doc mappings before adding new governance documents."
    return "Governance baseline is readable; use change packets for non-trivial development work."


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="OPL document governance doctor")
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor_parser = subparsers.add_parser("doctor")
    doctor_parser.add_argument("repo_root", nargs="?", default=".")
    doctor_parser.add_argument("--format", choices=["markdown", "json"], default="markdown")

    family_parser = subparsers.add_parser("family-plan")
    family_parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    family_parser.add_argument(
        "--repo",
        action="append",
        default=[],
        metavar="ID=PATH",
        help="Add or override an OPL series repo, for example oma=/path/to/opl-meta-agent.",
    )
    family_parser.add_argument(
        "--workspace-root",
        help="Optional local workspace root used to expand default public repo names into local paths.",
    )

    native_check_parser = subparsers.add_parser("native-check")
    native_check_parser.add_argument("repo_root", nargs="?", default=".")
    native_check_parser.add_argument("--format", choices=["json"], default="json")

    native_sync_parser = subparsers.add_parser("native-sync")
    native_sync_parser.add_argument("repo_root", nargs="?", default=".")
    native_sync_parser.add_argument("--apply", action="store_true")
    native_sync_parser.add_argument("--format", choices=["json"], default="json")

    return parser.parse_args()


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


def main() -> int:
    args = parse_args()
    if args.command == "doctor":
        payload = doctor(Path(args.repo_root))
        if args.format == "json":
            print(json.dumps(payload, indent=2, sort_keys=True))
        else:
            print_markdown(payload)
        return 0
    if args.command == "family-plan":
        repos = default_series_repos(args.workspace_root) if args.workspace_root else None
        if args.repo:
            repos = repos or default_series_repos()
            repos = parse_repo_overrides(args.repo, repos)
        payload = family_plan(repos)
        if args.format == "json":
            print(json.dumps(payload, indent=2, sort_keys=True))
        else:
            print_family_markdown(payload)
        return 0
    if args.command == "native-check":
        payload = native_check(Path(args.repo_root))
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0 if payload["ok"] else 1
    if args.command == "native-sync":
        payload = native_sync(Path(args.repo_root), apply=args.apply)
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0 if payload["ok"] or (not args.apply and payload["planned_changes"]) else 1
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())

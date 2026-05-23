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
    "退役",
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
}

DATED_HEADING_RISK_THRESHOLD = 5
CHECKBOX_LIST_RISK_THRESHOLD = 10

REPO_NATIVE_DIR = ".opl-doc-governance"
REPO_NATIVE_CONFIG_PATH = f"{REPO_NATIVE_DIR}/config.json"
REPO_NATIVE_AGENT_ENTRY_PATH = f"{REPO_NATIVE_DIR}/agent-entry.md"
REPO_NATIVE_README_PATH = f"{REPO_NATIVE_DIR}/README.md"
REPO_NATIVE_SCHEMA_VERSION = "opl-doc-governance.repo-native.v1"
REPO_NATIVE_FILES = (
    REPO_NATIVE_CONFIG_PATH,
    REPO_NATIVE_AGENT_ENTRY_PATH,
    REPO_NATIVE_README_PATH,
)

DATED_HEADING_RE = re.compile(
    r"^#{1,6}\s+"
    r"(?:\d{4}[-/.]\d{1,2}(?:[-/.]\d{1,2})?|\d{1,2}[-/.]\d{1,2}[-/.]\d{2,4})"
    r"(?:\b|[：:\s-])"
)
CHECKBOX_ITEM_RE = re.compile(r"^\s*[-*+]\s+\[[ xX]\]\s+")


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


def detect_profile(root: Path) -> str:
    name = root.name
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


def build_repo_native_config(root: Path) -> dict[str, Any]:
    profile = detect_profile(root)
    return {
        "schema_version": REPO_NATIVE_SCHEMA_VERSION,
        "governance_skill": "opl-doc-governance",
        "repo_profile": profile,
        "goal_mode": {
            "auto_create_for_long_horizon_or_editing": True,
            "single_repo_read_only_audit_starts_with_doctor": True,
        },
        "agent_entry": REPO_NATIVE_AGENT_ENTRY_PATH,
        "canonical_docs": CORE_DOCS,
        "canonical_doc_dirs": CANONICAL_DOC_DIRS,
        "primary_reference_docs": FAMILY_REFERENCE_DOCS
        if profile in {"opl_framework", "foundry_agent", "opl_meta_agent"}
        else [],
        "lifecycle_fields": list(HEADER_FIELDS),
        "machine_truth_boundaries": [
            "source",
            "tests",
            "contracts",
            "CLI/API output",
            "runtime ledger",
            "receipt refs",
        ],
        "verification": {
            "doctor_json": "python3 <opl-doc-governance-checkout>/scripts/opl_doc_doctor.py doctor <repo-root> --format json",
            "repo_native": "run the target repository's own documented verification before closeout",
        },
        "owner_boundary": (
            "Developer-document lifecycle governance only; domain truth, runtime truth, "
            "artifact authority, quality verdicts, and owner receipts stay with their owning surfaces."
        ),
    }


def repo_native_agent_entry_text(config: dict[str, Any]) -> str:
    profile = config["repo_profile"]
    return f"""# OPL Doc Governance Agent Entry

Owner: `OPL Doc Governance`
Purpose: `repo_native_agent_entry`
State: `active_entry`
Machine boundary: This file is agent-readable guidance; machine truth remains in source, tests, contracts, CLI/API output, runtime ledgers, and receipt refs.

## First agent move

1. Read this file and `{REPO_NATIVE_CONFIG_PATH}`.
2. Read the target repo `AGENTS.md`.
3. Read `TASTE.md` when present.
4. Read canonical current docs before supporting docs: `README.md`, `docs/README.md`, `docs/project.md`, `docs/status.md`, `docs/architecture.md`, `docs/invariants.md`, `docs/decisions.md`, and active gap references when present.
5. Run the OPL Doc Governance doctor from the installed skill or governance tool checkout, targeting this repo root, then verify important findings by reading files.

## Operating mode

- Repo profile: `{profile}`.
- For long-horizon, multi-repo, edit-heavy, worktree/subagent, or absorb-back-to-main requests, create or resume a `/goal` before execution.
- For a short single-repo read-only audit, start with doctor output and direct file reads.
- Treat docs as developer context, not production readiness evidence.

## Lifecycle policy

- Each long-lived document has one owner, one purpose, one state, and one machine boundary.
- Current truth belongs in canonical docs.
- Active work belongs in `docs/active/`.
- Historical process, retired plans, and tombstones belong in `docs/history/`.
- Stale modules, interfaces, tests, aliases, and compatibility wording are retired directly after active callers move.

## Closeout gate

- Canonical docs reflect current truth.
- Active docs contain only current plans, gaps, and baton material.
- History or tombstone files hold necessary provenance.
- Prose does not contradict source, tests, contracts, CLI/API output, runtime ledgers, or receipt refs.
- Final verification ran on the target repo's final main checkout.
"""


def repo_native_readme_text(config: dict[str, Any]) -> str:
    profile = config["repo_profile"]
    return f"""# Repo-Native OPL Doc Governance

Owner: `OPL Doc Governance`
Purpose: `repo_native_config`
State: `active_reference`
Machine boundary: This directory stores agent-readable governance configuration only.

This repo carries a local OPL Doc Governance entry so future agents can discover the document lifecycle rules without relying on a long prompt.

- Profile: `{profile}`
- Config: `{REPO_NATIVE_CONFIG_PATH}`
- Agent entry: `{REPO_NATIVE_AGENT_ENTRY_PATH}`

The local entry preserves this repo's own documentation taxonomy. It does not migrate the repo to OpenArc, OpenSpec, Spec Kit, or Agent OS file layouts.
"""


def build_repo_native_files(root: Path) -> dict[str, str]:
    config = build_repo_native_config(root)
    return {
        REPO_NATIVE_CONFIG_PATH: json.dumps(config, indent=2, sort_keys=True) + "\n",
        REPO_NATIVE_AGENT_ENTRY_PATH: repo_native_agent_entry_text(config),
        REPO_NATIVE_README_PATH: repo_native_readme_text(config),
    }


def inspect_repo_native(root: Path) -> dict[str, Any]:
    config_path = root / REPO_NATIVE_CONFIG_PATH
    entry_path = root / REPO_NATIVE_AGENT_ENTRY_PATH
    readme_path = root / REPO_NATIVE_README_PATH
    present_files = [path for path in REPO_NATIVE_FILES if rel_exists(root, path)]
    missing_files = [path for path in REPO_NATIVE_FILES if not rel_exists(root, path)]
    schema_version = None
    repo_profile = None
    if config_path.exists():
        try:
            config = json.loads(read_text(config_path))
            schema_version = config.get("schema_version")
            repo_profile = config.get("repo_profile")
        except json.JSONDecodeError:
            schema_version = "invalid_json"
    return {
        "present": bool(present_files),
        "complete": not missing_files and schema_version == REPO_NATIVE_SCHEMA_VERSION,
        "config_path": REPO_NATIVE_CONFIG_PATH if config_path.exists() else None,
        "agent_entry_path": REPO_NATIVE_AGENT_ENTRY_PATH if entry_path.exists() else None,
        "readme_path": REPO_NATIVE_README_PATH if readme_path.exists() else None,
        "schema_version": schema_version,
        "repo_profile": repo_profile,
        "present_files": present_files,
        "missing_files": missing_files,
    }


def init_repo(root: Path, *, dry_run: bool = False, force: bool = False) -> dict[str, Any]:
    root = root.resolve()
    files = build_repo_native_files(root)
    existing = [rel_path for rel_path in files if (root / rel_path).exists()]
    if existing and not dry_run and not force:
        raise FileExistsError(
            "repo-native governance file already exists; use force to overwrite: "
            + ", ".join(existing)
        )

    if not dry_run:
        for rel_path, text in files.items():
            path = root / rel_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")

    return {
        "root": str(root),
        "repo_profile": detect_profile(root),
        "schema_version": REPO_NATIVE_SCHEMA_VERSION,
        "dry_run": dry_run,
        "force": force,
        "created": list(files),
        "skipped_existing": existing if dry_run else [],
        "agent_entry_path": REPO_NATIVE_AGENT_ENTRY_PATH,
        "config_path": REPO_NATIVE_CONFIG_PATH,
        "next_step": f"Read {REPO_NATIVE_AGENT_ENTRY_PATH}, then run doctor and repo-native verification.",
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


def doctor(root: Path) -> dict[str, Any]:
    root = root.resolve()
    profile = detect_profile(root)
    repo_native = inspect_repo_native(root)
    docs = list_markdown_docs(root)
    findings: list[Finding] = []

    core_status = {path: rel_exists(root, path) for path in CORE_DOCS}
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

    active_gap_docs = [
        path
        for path in FAMILY_REFERENCE_DOCS
        if rel_exists(root, path)
    ]

    return {
        "root": str(root),
        "repo_profile": profile,
        "repo_native": repo_native,
        "core_docs": core_status,
        "canonical_dirs": dir_status,
        "markdown_doc_count": len(docs),
        "active_gap_reference_docs": active_gap_docs,
        "finding_count": len(findings),
        "findings": [finding.to_json() for finding in findings],
        "recommendation": recommend(profile, findings, active_gap_docs),
    }


def recommend(profile: str, findings: list[Finding], active_gap_docs: list[str]) -> str:
    if any(finding.code == "legacy_vocabulary_active_path" for finding in findings):
        return "Run an active-doc retirement pass: rewrite current truth, then archive or tombstone stale historical wording."
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
        docs.append(f"{label} active gap and improvement plan")
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
    return (
        "使用 OPL Doc Governance，自动创建或延续 /goal，治理 OPL series "
        f"repo（{repo_list}）的开发文档生命周期；以各 repo 的 ideal-state "
        "reference 和 active gap plan 为主要参考，根据 live code、contracts、"
        "tests、CLI/read-model 与 docs 的当前事实，逐条评估 README* 与 "
        "docs/**/*.md 下其他文档，清理归档过时内容，避免二次污染；保证每个"
        "文档只有唯一任务和定位，折叠历史增量长清单，过时模块/接口/测试按"
        "理想态直接退役且不保留兼容面；可以并行使用 subagent/worktree，"
        "每条线完成后验证、提交、吸收回 main 并清理；最终 main checkout "
        "必须重新验证，且 canonical docs、history/tombstone 与必要的 "
        "contracts/read-model references 已同步。"
    )


def family_plan(repo_paths: dict[str, str] | None = None) -> dict[str, Any]:
    paths = repo_paths or default_series_repos()
    primary_reference_docs = build_primary_reference_docs(paths)
    governance_prompt_elements = [
        "series_primary_reference_docs",
        "evaluate_all_docs_item_by_item",
        "cleanup_and_archive_stale_content",
        "unique_task_positioning",
        "fold_long_incremental_lists",
        "directly_retire_outdated_modules_interfaces_tests",
        "allow_parallel_worktrees_and_subagents",
        "absorb_main_and_cleanup_when_complete",
    ]
    steps = [
        "Use the OPL series primary reference docs: each governed repo contributes its ideal-state reference plus its active gap and improvement plan.",
        "Read each repo's AGENTS.md, TASTE.md when present, status, architecture, invariants, docs portfolio guidance, and the series primary reference docs before editing.",
        "逐条评估 docs 下其他所有文档；classify each section as current truth, active gap, support reference, process history, retired/tombstone, or stale pollution.",
        "清理和归档过时内容，避免二次污染；route history to docs/history or tombstone refs instead of active docs.",
        "每个文档必须有唯一任务和定位；update canonical docs so every long-lived document has one owner, one purpose, one state, and one machine boundary.",
        "历史增量长清单要折叠 into compact current-state tables plus archive pointers.",
        "过时模块/接口/测试全部按当前理想态直接退役清理，不保留兼容 alias、facade 或 compatibility wording.",
        "可以并行开 worktree/subagent for independent repos or non-overlapping lanes; keep scopes explicit and merge evidence back to the owner lane.",
        "Run repo-native doc/contract/tests verification, absorb completed lanes back to main, and clean temporary branches/worktrees.",
    ]
    return {
        "objective": "OPL series document lifecycle governance and software-engineering closeout",
        "repos": paths,
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
            "stale process material is archived or tombstoned",
            "no active compatibility-resurrection wording remains",
            "contracts/tests/read-model references are not contradicted by prose",
            "outdated modules/interfaces/tests are directly retired when their active callers have moved",
            "completed lanes were absorbed back to main and temporary worktrees/branches were cleaned",
            "verification was run on the final main checkout",
        ],
    }


def print_markdown(payload: dict[str, Any]) -> None:
    print("# OPL Doc Doctor")
    print()
    print(f"Root: `{payload['root']}`")
    print(f"Profile: `{payload['repo_profile']}`")
    print(f"Markdown docs: `{payload['markdown_doc_count']}`")
    repo_native = payload["repo_native"]
    if repo_native["present"]:
        state = "complete" if repo_native["complete"] else "incomplete"
        print(f"Repo-native governance: `{state}`")
        if repo_native["agent_entry_path"]:
            print(f"Agent entry: `{repo_native['agent_entry_path']}`")
    else:
        print("Repo-native governance: `absent`")
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
    print("## Primary References")
    print(f"{payload['primary_reference_doc_count']} primary reference docs")
    for reference in payload["primary_reference_docs_per_repo"]:
        print(f"- {reference}")
    print()
    print("## Governance Prompt Elements")
    labels = {
        "series_primary_reference_docs": "OPL series primary reference docs",
        "evaluate_all_docs_item_by_item": "逐条评估 docs 下其他所有文档",
        "cleanup_and_archive_stale_content": "清理和归档过时内容",
        "unique_task_positioning": "每个文档必须有唯一任务和定位",
        "fold_long_incremental_lists": "历史增量长清单要折叠",
        "directly_retire_outdated_modules_interfaces_tests": "过时模块/接口/测试直接退役清理",
        "allow_parallel_worktrees_and_subagents": "允许并行 worktree/subagent",
        "absorb_main_and_cleanup_when_complete": "完成后吸收回 main 并清理",
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


def print_init_repo_markdown(payload: dict[str, Any]) -> None:
    print("# OPL Repo-Native Governance Init")
    print()
    print(f"Root: `{payload['root']}`")
    print(f"Profile: `{payload['repo_profile']}`")
    print(f"Schema: `{payload['schema_version']}`")
    print(f"Dry run: `{payload['dry_run']}`")
    print()
    print("## Files")
    for path in payload["created"]:
        print(f"- `{path}`")
    if payload["skipped_existing"]:
        print()
        print("## Existing Files")
        for path in payload["skipped_existing"]:
            print(f"- `{path}`")
    print()
    print("## Next Step")
    print(payload["next_step"])


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

    init_parser = subparsers.add_parser("init-repo")
    init_parser.add_argument("repo_root", nargs="?", default=".")
    init_parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    init_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report repo-native governance files without writing them.",
    )
    init_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing repo-native governance files.",
    )

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
    if args.command == "init-repo":
        try:
            payload = init_repo(Path(args.repo_root), dry_run=args.dry_run, force=args.force)
        except FileExistsError as exc:
            print(str(exc))
            return 2
        if args.format == "json":
            print(json.dumps(payload, indent=2, sort_keys=True))
        else:
            print_init_repo_markdown(payload)
        return 0
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())

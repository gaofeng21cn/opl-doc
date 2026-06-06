"""Read-only document lifecycle and active-truth invariant checks."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .common import Finding, read_text, rel_exists
from .constants import (
    ACTIVE_GAP_MARKERS,
    ACTIVE_PROGRESS_MARKERS,
    ACTIVE_TRUTH_DOC_NAME_RE,
    CANONICAL_DOC_DIRS,
    CHECKBOX_ITEM_RE,
    CHECKBOX_LIST_RISK_THRESHOLD,
    CORE_DOCS,
    DATED_HEADING_RE,
    DATED_HEADING_RISK_THRESHOLD,
    FAMILY_REFERENCE_DOCS,
    HEADER_FIELDS,
    LEGACY_ACTIVE_TOKENS,
    NEXT_AGENT_PROMPT_MARKERS,
    NEXT_AGENT_PROMPT_REQUIRED_MARKERS,
    OPL_DOC_AUTHORITY_BOUNDARY,
    PROCESS_LOG_HEADING_RE,
    RETIREMENT_NEGATION_MARKERS,
)
from .profile_discovery import detect_profile, inspect_repo_native_surfaces


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

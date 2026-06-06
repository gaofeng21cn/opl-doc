#!/usr/bin/env python3
"""Compatibility entrypoint for the OPL-native document lifecycle doctor."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.opl_doc_doctor_parts import (
    Finding,
    build_goal_objective,
    build_primary_reference_docs,
    default_series_repos,
    detect_profile,
    doctor,
    expected_native_profile,
    family_plan,
    inspect_repo_native_surfaces,
    main,
    native_check,
    native_sync,
    parse_args,
    parse_repo_overrides,
    print_family_markdown,
    print_markdown,
    recommend,
    repo_identity,
)

__all__ = [
    "Finding",
    "build_goal_objective",
    "build_primary_reference_docs",
    "default_series_repos",
    "detect_profile",
    "doctor",
    "expected_native_profile",
    "family_plan",
    "inspect_repo_native_surfaces",
    "main",
    "native_check",
    "native_sync",
    "parse_args",
    "parse_repo_overrides",
    "print_family_markdown",
    "print_markdown",
    "recommend",
    "repo_identity",
]


if __name__ == "__main__":
    raise SystemExit(main())

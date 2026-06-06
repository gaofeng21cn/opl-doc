"""Internal modules for the OPL document lifecycle doctor."""

from __future__ import annotations

from .cli import main, parse_args
from .common import Finding
from .family_plan import (
    build_goal_objective,
    build_primary_reference_docs,
    default_series_repos,
    family_plan,
    parse_repo_overrides,
)
from .invariant_checks import doctor, recommend
from .plugin_sync import expected_native_profile, native_check, native_sync
from .profile_discovery import detect_profile, inspect_repo_native_surfaces, repo_identity
from .rendering import print_family_markdown, print_markdown

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

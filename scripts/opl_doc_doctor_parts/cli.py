"""Command-line interface for the OPL document lifecycle doctor."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .family_plan import (
    build_support_profile_guard_audit,
    default_series_repos,
    family_plan,
    parse_repo_overrides,
)
from .invariant_checks import doctor
from .plugin_sync import native_check, native_sync
from .rendering import print_family_markdown, print_markdown


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="OPL document governance doctor")
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor_parser = subparsers.add_parser("doctor")
    doctor_parser.add_argument("repo_root", nargs="?", default=".")
    doctor_parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    doctor_parser.add_argument(
        "--json",
        action="store_const",
        const="json",
        dest="format",
        help="Alias for --format json; kept as a CLI readback convenience, not a new contract path.",
    )

    family_parser = subparsers.add_parser("family-plan")
    family_parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    family_parser.add_argument(
        "--json",
        action="store_const",
        const="json",
        dest="format",
        help="Alias for --format json; kept as a CLI readback convenience, not a new contract path.",
    )
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

    support_profile_parser = subparsers.add_parser("support-profile-check")
    support_profile_parser.add_argument("repo_root", nargs="?", default=".")
    support_profile_parser.add_argument("--format", choices=["json"], default="json")
    support_profile_parser.add_argument(
        "--json",
        action="store_const",
        const="json",
        dest="format",
        help="Alias for --format json; kept as a CLI readback convenience, not a new contract path.",
    )
    support_profile_parser.add_argument(
        "--repo",
        action="append",
        default=[],
        metavar="ID=PATH",
        help="Add or override an OPL series repo before running the support profile guard.",
    )
    support_profile_parser.add_argument(
        "--workspace-root",
        help="Optional local workspace root used to expand default public repo names into local paths.",
    )

    native_check_parser = subparsers.add_parser("native-check")
    native_check_parser.add_argument("repo_root", nargs="?", default=".")
    native_check_parser.add_argument("--format", choices=["json"], default="json")
    native_check_parser.add_argument(
        "--json",
        action="store_const",
        const="json",
        dest="format",
        help="Alias for --format json; kept as a CLI readback convenience, not a new contract path.",
    )

    native_sync_parser = subparsers.add_parser("native-sync")
    native_sync_parser.add_argument("repo_root", nargs="?", default=".")
    native_sync_apply = native_sync_parser.add_mutually_exclusive_group()
    native_sync_apply.add_argument("--apply", action="store_true", dest="apply")
    native_sync_apply.add_argument("--dry-run", action="store_false", dest="apply")
    native_sync_parser.set_defaults(apply=False)
    native_sync_parser.add_argument("--format", choices=["json"], default="json")
    native_sync_parser.add_argument(
        "--json",
        action="store_const",
        const="json",
        dest="format",
        help="Alias for --format json; kept as a CLI readback convenience, not a new contract path.",
    )

    return parser.parse_args()


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
    if args.command == "support-profile-check":
        repos = default_series_repos(args.workspace_root) if args.workspace_root else None
        if args.repo:
            repos = repos or default_series_repos()
            repos = parse_repo_overrides(args.repo, repos)
        payload = build_support_profile_guard_audit(
            repos or default_series_repos(),
            repo_root=Path(args.repo_root),
        )
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0 if payload["state"] == "passed_no_resurrection_guard" else 1
    if args.command == "native-check":
        payload = native_check(Path(args.repo_root))
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0 if payload["ok"] else 1
    if args.command == "native-sync":
        payload = native_sync(Path(args.repo_root), apply=args.apply)
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0 if payload["ok"] or (not args.apply and payload["planned_changes"]) else 1
    raise AssertionError(args.command)

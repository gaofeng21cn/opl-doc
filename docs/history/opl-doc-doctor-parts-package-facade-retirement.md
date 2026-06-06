# OPL Doc doctor parts package facade retirement

Owner: `One Person Lab`
Purpose: `opl_doc_doctor_parts_package_facade_retirement_provenance`
State: `history_provenance`
Machine boundary: This document records a support-repo governance closeout. Current behavior is owned by concrete modules under `scripts/opl_doc_doctor_parts/`, `scripts/opl_doc_doctor.py`, tests, and repo-native verification output.

## Closeout

The package-root import facade in `scripts/opl_doc_doctor_parts/__init__.py` is retired. The package root remains only as a Python package marker; it no longer imports concrete implementation modules or declares `__all__`.

Current owner split:

- `scripts/opl_doc_doctor.py`: command bootstrap for `doctor`, `family-plan`, `native-check`, and `native-sync`.
- `scripts/opl_doc_doctor_parts/cli.py`: CLI parser and command dispatch.
- `scripts/opl_doc_doctor_parts/invariant_checks.py`: doctor and recommendation logic.
- `scripts/opl_doc_doctor_parts/family_plan.py`: OPL series workflow plan generation.
- `scripts/opl_doc_doctor_parts/plugin_sync.py`: native profile check/sync.
- `scripts/opl_doc_doctor_parts/profile_discovery.py`: repo profile and surface discovery.
- `scripts/opl_doc_doctor_parts/rendering.py`: markdown rendering helpers.
- `tests/test_opl_doc_doctor.py`: concrete-module import coverage and package-root no-facade guard.

## Retired Surface

- Retired: importing doctor APIs from `scripts.opl_doc_doctor_parts`.
- Replacement: import from the concrete owner module under `scripts.opl_doc_doctor_parts.*`.
- No-resurrection rule: do not restore package-root implementation imports or a broad `__all__` facade in `scripts/opl_doc_doctor_parts/__init__.py`.

## Verification

Verification run on `2026-06-07`:

- `python3 -m pytest tests/test_opl_doc_doctor.py -q`: passed with `25 passed`.
- `python3 -m pytest -q`: passed with `30 passed`.
- `python3 scripts/opl_doc_doctor.py doctor . --format json`: exited `0` with `finding_count=0`.
- `python3 scripts/opl_doc_doctor.py family-plan --format markdown`: exited `0`.
- `python3 scripts/opl_doc_doctor.py native-sync .`: exited `0` in dry-run mode and reported missing `contracts/opl-native-profile.json`; no file was written because profile creation is outside this package-facade retirement lane.
- `bash scripts/verify.sh`: passed with `30 passed`.
- `git diff --check`: passed.
- Active package-root facade scan: no active `from scripts.opl_doc_doctor_parts import ...` or package-root `__all__` remains outside no-resurrection tests and history provenance.

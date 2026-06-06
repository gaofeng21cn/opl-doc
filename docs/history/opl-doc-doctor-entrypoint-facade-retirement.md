# OPL Doc doctor entrypoint facade retirement

Owner: `One Person Lab`
Purpose: `opl_doc_doctor_entrypoint_facade_retirement_provenance`
State: `history_provenance`
Machine boundary: This document records a support-repo governance closeout. Current behavior is owned by `scripts/opl_doc_doctor.py`, `scripts/opl_doc_doctor_parts/`, installer tests, doctor tests, and repo-native verification output.

## Closeout

The old `scripts/opl_doc_doctor.py` import-compatibility facade role is retired. The file remains as the repo-local command bootstrap and installed `opl-doc-doctor` symlink target, but it no longer re-exports the doctor API surface.

Current owner split:

- `scripts/opl_doc_doctor.py`: command bootstrap for `doctor`, `family-plan`, `native-check`, and `native-sync`.
- `scripts/opl_doc_doctor_parts/`: implementation and import API owner.
- `scripts/install_local_plugin.py`: installed command symlink owner.
- `tests/test_opl_doc_doctor.py`: no-facade regression guard for the command bootstrap.
- `tests/test_install_local_plugin.py`: installed command target guard.

## Retired Surface

- Retired: importing public API from `scripts.opl_doc_doctor`.
- Replacement: import from `scripts.opl_doc_doctor_parts` or its concrete modules.
- No-resurrection rule: do not restore a broad `__all__` re-export facade in `scripts/opl_doc_doctor.py`.

## Verification

Expected verification for this closeout:

- `python3 -m pytest -q`
- `python3 scripts/opl_doc_doctor.py doctor . --format json`
- `python3 scripts/opl_doc_doctor.py family-plan --format markdown`
- `python3 scripts/opl_doc_doctor.py native-sync .`
- `bash scripts/verify.sh`
- `git diff --check`

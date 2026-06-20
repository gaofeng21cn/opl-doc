#!/usr/bin/env python3
"""Repo-local command bootstrap for the OPL document lifecycle doctor."""

from __future__ import annotations

import sys
from pathlib import Path

sys.dont_write_bytecode = True

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.opl_doc_doctor_parts.cli import main


if __name__ == "__main__":
    raise SystemExit(main())

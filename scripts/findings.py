"""Typed result subclasses for audit checks."""
from __future__ import annotations

from dataclasses import dataclass

from scripts.report import CheckResult


@dataclass
class StructuralFinding(CheckResult):
    """A check result that points to a specific file in the audited repo.

    v0.1.1 introduces this subclass to carry the file path that the check
    examined or expected. The CLI report and JSON output render `file_path`
    when present; semantic checks (text-based) don't have a file path and
    keep returning plain `CheckResult`.
    """

    file_path: str | None = None

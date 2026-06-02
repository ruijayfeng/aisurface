"""Render GEO audit reports as Markdown."""
from __future__ import annotations

from dataclasses import dataclass, field

SUB_SCORE_MAX = 100
MAX_MUST_FIX = 5
MAX_SHOULD_FIX = 5

# Map CheckResult.category to user-facing sub-score labels
CATEGORY_LABELS = {
    "structural": "Structure",
    "semantic": "Readability",
}


@dataclass
class CheckResult:
    id: int | str
    name: str
    category: str  # "structural" or "semantic"
    score: float
    max_score: float
    passed: bool
    impact: int  # 1-25, used to weight must-fix ordering
    skipped: bool = False
    error: str | None = None


@dataclass
class AuditReport:
    project_name: str
    results: list[CheckResult] = field(default_factory=list)
    skipped: list[CheckResult] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


# Lazy re-export: a top-level `from scripts.findings import ...` would
# create a circular import (findings.py imports CheckResult from this
# module, so this module can't import from findings at load time).
# PEP 562 module __getattr__ defers the import until an external caller
# actually asks for `scripts.report.StructuralFinding`.
def __getattr__(name: str):
    if name == "StructuralFinding":
        from scripts.findings import StructuralFinding
        return StructuralFinding
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def _compute_health_score(results: list[CheckResult]) -> int:
    if not results:
        return 0
    total = sum(r.score for r in results)
    total_max = sum(r.max_score for r in results)
    if total_max == 0:
        return 0
    return round(total / total_max * SUB_SCORE_MAX)


def _compute_sub_scores(results: list[CheckResult]) -> list[tuple[str, int]]:
    """Aggregate scores per category, mapped to user-friendly labels."""
    if not results:
        return []
    by_category: dict[str, list[CheckResult]] = {}
    for r in results:
        by_category.setdefault(r.category, []).append(r)
    sub_scores: list[tuple[str, int]] = []
    for category, items in by_category.items():
        total = sum(r.score for r in items)
        total_max = sum(r.max_score for r in items)
        if total_max == 0:
            continue
        label = CATEGORY_LABELS.get(category, category.title())
        sub_scores.append((label, round(total / total_max * SUB_SCORE_MAX)))
    return sorted(sub_scores, key=lambda x: x[0])


def _bucket_results(results: list[CheckResult]) -> tuple[list, list, list, int]:
    """Sort into 🔴 must-fix, 🟡 should-fix, 🟢 nice-to-have, and a deferred count."""
    failed = sorted(
        [r for r in results if not r.passed],
        key=lambda r: -r.impact,
    )
    must_fix = failed[:MAX_MUST_FIX]
    should_fix = failed[MAX_MUST_FIX:MAX_MUST_FIX + MAX_SHOULD_FIX]
    nice = [r for r in results if r.passed and r.score < r.max_score]
    deferred_count = len(failed) - len(must_fix) - len(should_fix)
    return must_fix, should_fix, nice, deferred_count


def _format_check_line(r: CheckResult, teacher_mode: bool = False) -> str:
    """Format a check bullet line; optionally append a teacher-mode primer."""
    # Must-fix style includes impact; should-fix / nice-to-have don't.
    # We always emit the canonical "name + optional impact" form for consistency,
    # then optionally add the primer on the next line.
    base = f"- **{r.name}** (impact +{r.impact}%)"
    # StructuralFindings carry a file_path; show it inline so the user
    # knows which file the check examined. Avoids a forward reference to
    # StructuralFinding (this module re-exports it lazily via __getattr__).
    file_path = getattr(r, "file_path", None)
    if file_path:
        base = f"{base} (`{file_path}`)"
    if not teacher_mode:
        return base
    # Local import to avoid a hard dependency at module import time and to keep
    # report.py usable in contexts where concepts.py isn't on the path.
    from scripts.concepts import get_primer
    primer = get_primer(r.id)
    if not primer:
        return base
    return f"{base}\n  - _Why this matters: {primer}_"


def render_report(report: AuditReport, teacher_mode: bool = False) -> str:
    """Render the audit report as Markdown.

    Args:
        report: The audit report to render.
        teacher_mode: When True, inject a short educational primer after each
            check's name. Used by `python -m scripts.cli --learn`.
    """
    score = _compute_health_score(report.results)
    sub_scores = _compute_sub_scores(report.results)
    must_fix, should_fix, nice, deferred_count = _bucket_results(report.results)

    lines: list[str] = [
        f"# GEO Audit Report: {report.project_name}",
        "",
        f"**Health score**: {score} / 100",
        "",
    ]

    # Sub-scores section
    if sub_scores:
        lines.append("## Sub-scores")
        lines.append("")
        for label, sub in sub_scores:
            lines.append(f"- **{label}**: {sub} / {SUB_SCORE_MAX}")
        lines.append("")

    # Must-fix section
    if must_fix:
        lines.append("## 🔴 Must-fix")
        lines.append("")
        for r in must_fix:
            lines.append(_format_check_line(r, teacher_mode=teacher_mode))
        lines.append("")

    # Should-fix section
    if should_fix:
        lines.append("## 🟡 Should-fix")
        lines.append("")
        for r in should_fix:
            lines.append(_format_check_line(r, teacher_mode=teacher_mode))
        lines.append("")

    # Nice-to-have
    if nice:
        lines.append("## 🟢 Nice-to-have")
        lines.append("")
        for r in nice:
            lines.append(_format_check_line(r, teacher_mode=teacher_mode))
        lines.append("")

    # Deferred checks footer
    if deferred_count > 0:
        lines.append(f"_...and {deferred_count} more failed checks not shown._")
        lines.append("")

    # Skipped checks
    if report.skipped:
        lines.append("## ⏭️ Skipped checks")
        lines.append("")
        for s in report.skipped:
            lines.append(f"- {s.name}: {s.error or '(no message)'}")
        lines.append("")

    # Errors
    if report.errors:
        lines.append("## ❌ Errors")
        lines.append("")
        for err in report.errors:
            lines.append(f"- {err}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"

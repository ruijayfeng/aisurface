"""Render GEO audit reports as Markdown."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

SUB_SCORE_MAX = 100
MAX_MUST_FIX = 5
MAX_SHOULD_FIX = 5

# Weighted health score: 40/30/20/10. The 4 categories reflect which gaps
# hurt AI citation most (citation-friendliness outweighs raw distribution).
CATEGORY_WEIGHTS: dict[str, int] = {
    "citation_friendliness": 40,
    "structure": 30,
    "readability": 20,
    "distribution": 10,
}

# Map each check id to one of the 4 weighted categories.
CATEGORY_CHECK_IDS: dict[str, tuple[int, ...]] = {
    "citation_friendliness": (4, 8, 9, 10),
    "structure": (5, 6, 7),
    "readability": (1, 2, 3),
    "distribution": (11, 12),
}

# Map the 4 category keys to user-facing sub-score labels.
CATEGORY_LABELS = {
    "citation_friendliness": "Citation-Friendliness (引用友好度)",
    "structure": "Structure (结构)",
    "readability": "Readability (可读性)",
    "distribution": "Distribution (覆盖)",
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
    health_score: int = 0
    max_score: int = 100
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


def _compute_health_score(categories: dict[str, list[CheckResult]]) -> tuple[int, int]:
    """Compute the weighted health score.

    Args:
        categories: dict mapping category name to list of CheckResults.
                    Each category's contribution is (sum_score / sum_max) * weight.
                    Total is the sum of category contributions, capped at 100.

    Returns:
        (score, max_score) where max_score is always 100.

    Categories:
        - citation_friendliness (40): checks #4, #8, #9, #10
        - structure (30): checks #5, #6, #7
        - readability (20): checks #1, #2, #3
        - distribution (10): checks #11, #12
    """
    total = 0.0
    for cat, results in categories.items():
        if not results:
            continue
        cat_score = sum(r.score for r in results)
        cat_max = sum(r.max_score for r in results)
        if cat_max == 0:
            continue
        weight = CATEGORY_WEIGHTS.get(cat, 0)
        total += (cat_score / cat_max) * weight
    return round(total), 100


def _compute_sub_scores(results: list[CheckResult]) -> list[tuple[str, int]]:
    """Aggregate scores per category, mapped to user-friendly labels.

    Buckets are determined by CATEGORY_CHECK_IDS (not r.category), so the
    4 sub-scores line up with the weighted health score.
    """
    if not results:
        return []
    sub_scores: list[tuple[str, int]] = []
    for cat_key, check_ids in CATEGORY_CHECK_IDS.items():
        cat_results = [r for r in results if r.id in check_ids]
        if not cat_results:
            continue
        total = sum(r.score for r in cat_results)
        total_max = sum(r.max_score for r in cat_results)
        if total_max == 0:
            continue
        label = CATEGORY_LABELS.get(cat_key, cat_key.title())
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


def _format_check_line(
    r: CheckResult,
    teacher_mode: bool = False,
    wrap: Callable[[str, str], str] | None = None,
    name_color: str = "gray",
) -> str:
    """Format a check bullet line; optionally append a teacher-mode primer.

    Args:
        r: The check result to format.
        teacher_mode: When True, append a primer explaining why the check matters.
        wrap: Optional colorize function `(text, color) -> str` that wraps text
            with ANSI codes. When None (default), no color is applied — useful
            for tests and non-TTY callers.
        name_color: The color name passed to `wrap` for `r.name`.
    """
    w = wrap or (lambda text, _color: text)
    # Must-fix style includes impact; should-fix / nice-to-have don't.
    # We always emit the canonical "name + optional impact" form for consistency,
    # then optionally add the primer on the next line.
    base = f"- **{w(r.name, name_color)}** (impact +{r.impact}%)"
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


def render_report(
    report: AuditReport,
    teacher_mode: bool = False,
    wrap: Callable[[str, str], str] | None = None,
) -> str:
    """Render the audit report as Markdown.

    Args:
        report: The audit report to render.
        teacher_mode: When True, inject a short educational primer after each
            check's name. Used by `python -m scripts.cli --learn`.
        wrap: Optional colorize function `(text, color) -> str` that wraps text
            with ANSI codes. When None (default), no color is applied — useful
            for tests and non-TTY callers. The CLI passes `scripts.colors.colorize`
            so check names and section headers get colored.
    """
    w = wrap or (lambda text, _color: text)
    score = report.health_score
    sub_scores = _compute_sub_scores(report.results)
    must_fix, should_fix, nice, deferred_count = _bucket_results(report.results)

    lines: list[str] = [
        f"# GEO Audit Report: {w(report.project_name, 'bold')}",
        "",
        f"**Health score**: {w(str(score), 'bold')} / {report.max_score}",
        "",
    ]

    # Sub-scores section
    if sub_scores:
        lines.append(w("## Sub-scores", "gray"))
        lines.append("")
        for label, sub in sub_scores:
            lines.append(f"- **{w(label, 'blue')}**: {sub} / {SUB_SCORE_MAX}")
        lines.append("")

    # Must-fix section
    if must_fix:
        lines.append(w("## 🔴 Must-fix", "red"))
        lines.append("")
        for r in must_fix:
            lines.append(_format_check_line(r, teacher_mode=teacher_mode, wrap=w, name_color="red"))
        lines.append("")

    # Should-fix section
    if should_fix:
        lines.append(w("## 🟡 Should-fix", "yellow"))
        lines.append("")
        for r in should_fix:
            lines.append(_format_check_line(r, teacher_mode=teacher_mode, wrap=w, name_color="yellow"))
        lines.append("")

    # Nice-to-have
    if nice:
        lines.append(w("## 🟢 Nice-to-have", "green"))
        lines.append("")
        for r in nice:
            lines.append(_format_check_line(r, teacher_mode=teacher_mode, wrap=w, name_color="green"))
        lines.append("")

    # Deferred checks footer
    if deferred_count > 0:
        lines.append(f"_...and {deferred_count} more failed checks not shown._")
        lines.append("")

    # Skipped checks
    if report.skipped:
        lines.append(w("## ⏭️ Skipped checks", "gray"))
        lines.append("")
        for s in report.skipped:
            lines.append(f"- {s.name}: {s.error or '(no message)'}")
        lines.append("")

    # Errors
    if report.errors:
        lines.append(w("## ❌ Errors", "red"))
        lines.append("")
        for err in report.errors:
            lines.append(f"- {w(err, 'red')}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"

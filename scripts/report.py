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
    id: int
    name: str
    category: str  # "structural" or "semantic"
    score: float
    max_score: float
    passed: bool
    impact: int  # 1-25, used to weight must-fix ordering


@dataclass
class AuditReport:
    project_name: str
    results: list[CheckResult] = field(default_factory=list)
    skipped: list[tuple[str, str]] = field(default_factory=list)  # (check_name, reason)
    errors: list[tuple[str, str]] = field(default_factory=list)


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


def render_report(report: AuditReport) -> str:
    """Render the audit report as Markdown."""
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
            lines.append(f"- **{r.name}** (impact +{r.impact}%)")
        lines.append("")

    # Should-fix section
    if should_fix:
        lines.append("## 🟡 Should-fix")
        lines.append("")
        for r in should_fix:
            lines.append(f"- {r.name}")
        lines.append("")

    # Nice-to-have
    if nice:
        lines.append("## 🟢 Nice-to-have")
        lines.append("")
        for r in nice:
            lines.append(f"- {r.name}")
        lines.append("")

    # Deferred checks footer
    if deferred_count > 0:
        lines.append(f"_...and {deferred_count} more failed checks not shown._")
        lines.append("")

    # Skipped checks
    if report.skipped:
        lines.append("## ⏭️ Skipped checks")
        lines.append("")
        for name, reason in report.skipped:
            lines.append(f"- {name}: {reason}")
        lines.append("")

    # Errors
    if report.errors:
        lines.append("## ❌ Errors")
        lines.append("")
        for name, err in report.errors:
            lines.append(f"- {name}: {err}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"

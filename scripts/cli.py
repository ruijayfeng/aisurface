"""CLI entry point for aisurface audit."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from scripts import critic, distribution, github_meta, report, scanner
from scripts.report import AuditReport, CheckResult
from scripts.scanner import RepoAssets

# AI search platforms tracked in references/ai-search-platforms.md.
# Used by the platform_coverage heuristic (check #12) to score how
# many platforms the README explicitly names.
AI_PLATFORMS = [
    "ChatGPT", "Perplexity", "Claude", "Gemini",
    "豆包", "DeepSeek", "文心一言", "通义千问", "Kimi", "智谱", "GLM",
]


def _read_readme(assets: RepoAssets) -> str:
    if assets.readme is None:
        return ""
    return assets.readme.read_text(encoding="utf-8", errors="ignore")


def _check_faq_section(readme: str) -> tuple[int, bool]:
    """Score 10 if a FAQ / Frequently Asked / 常见问题 heading exists, else 0."""
    if re.search(
        r"^#{1,4}\s*(faq|frequently\s+asked|常见问题)",
        readme, re.MULTILINE | re.IGNORECASE,
    ):
        return 10, True
    return 0, False


def _check_when_to_use(readme: str) -> tuple[int, bool]:
    """Score 10 if both 'When to use' AND 'When NOT to use' sections present,
    5 if only one is present, 0 if neither."""
    has_use = bool(re.search(
        r"^#{1,4}\s*(when\s+to\s+use|适用场景|use\s+cases)",
        readme, re.MULTILINE | re.IGNORECASE,
    ))
    has_not_use = bool(re.search(
        r"^#{1,4}\s*(when\s+not\s+to\s+use|不适用|not\s+for|when\s+to\s+avoid)",
        readme, re.MULTILINE | re.IGNORECASE,
    ))
    if has_use and has_not_use:
        return 10, True
    if has_use or has_not_use:
        return 5, False
    return 0, False


def _check_citation_worthy_content(readme: str) -> tuple[int, bool]:
    """Count sections containing concrete numbers, fenced code blocks, or
    named entities (multi-word capitalized phrases). Score 2 points per
    such section, capped at 10. Pass threshold is 7 (>=4 signal sections)."""
    # Split on heading lines; first chunk is the pre-first-heading text.
    sections = re.split(r"^#{1,4}\s+", readme, flags=re.MULTILINE)
    signal_sections = 0
    for section in sections:
        if not section.strip():
            continue
        # Concrete numbers (e.g. 3 commands, 100%, $5, 2026)
        if re.search(r"\b\d+(?:[\.,]\d+)?%?\b", section):
            signal_sections += 1
            continue
        # Fenced code blocks
        if "```" in section:
            signal_sections += 1
            continue
        # Named entities: 2+ consecutive Capitalized words
        if re.search(r"\b[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)+\b", section):
            signal_sections += 1
    score = min(10, signal_sections * 2)
    return score, score >= 7


def _check_platform_coverage(readme: str) -> tuple[int, bool]:
    """Score how many AI search platforms (from references/ai-search-platforms.md)
    the README mentions by name. 10 if 3+, 5 if 1-2, 0 if 0."""
    count = sum(1 for p in AI_PLATFORMS if p in readme)
    if count >= 3:
        return 10, True
    if count >= 1:
        return 5, False
    return 0, False


def _structural_checks(assets: RepoAssets) -> list[CheckResult]:
    """Run the 4 structural checks (#5, #6, #7, #11)."""
    results: list[CheckResult] = []

    # #5 Schema.org
    results.append(
        CheckResult(
            id=5,
            name="Schema.org markup on website",
            category="structural",
            score=10 if assets.has_schema_org else 0,
            max_score=10,
            passed=assets.has_schema_org,
            impact=20,
        )
    )
    # #6 llms.txt
    results.append(
        CheckResult(
            id=6,
            name=".well-known/llms.txt present",
            category="structural",
            score=10 if assets.has_llms_txt else 0,
            max_score=10,
            passed=assets.has_llms_txt,
            impact=15,
        )
    )
    # #7 GitHub topics — use suggest_topics to count candidates from readme
    readme_text = _read_readme(assets)
    suggested_count = len(github_meta.suggest_topics(readme_text, existing=[]))
    topics_passed = suggested_count >= 8
    results.append(
        CheckResult(
            id=7,
            name="GitHub topics complete (8-12)",
            category="structural",
            score=10 if topics_passed else (5 if suggested_count >= 4 else 0),
            max_score=10,
            passed=topics_passed,
            impact=5,
        )
    )
    # #11 Distribution signals — use real local-signal detection.
    # github_stars stays 0 until v0.3 wires real GitHub API (per CHANGELOG).
    # The pass threshold is 5, the max achievable from locally-observable
    # signals (registries max 3 + description max 2). v0.3 can raise it to 6
    # once stars become real data.
    sig = distribution.check_signals(
        project_name=assets.root.name,
        description=readme_text[:200] if readme_text else "",
        github_stars=0,
        has_npm=assets.has_npm,
        has_pypi=assets.has_pypi,
    )
    dist_passed = sig["score"] >= 5
    results.append(
        CheckResult(
            id=11,
            name="Distribution signals (awesome / npm / PyPI)",
            category="structural",
            score=sig["score"],
            max_score=10,
            passed=dist_passed,
            impact=5,
        )
    )
    return results


def _semantic_checks(assets: RepoAssets) -> list[CheckResult]:
    """Run the 8 LLM-critic checks via offline_critique fallback."""
    readme = _read_readme(assets)
    if not readme:
        return [
            CheckResult(
                id=i,
                name=f"Semantic check #{i}",
                category="semantic",
                score=0,
                max_score=10,
                passed=False,
                impact=10,
            )
            for i in (1, 2, 3, 4, 8, 9, 10, 12)
        ]

    critique = critic.offline_critique(readme, topic=assets.project_type)
    faq_score, faq_passed = _check_faq_section(readme)
    wtu_score, wtu_passed = _check_when_to_use(readme)
    cwc_score, cwc_passed = _check_citation_worthy_content(readme)
    pc_score, pc_passed = _check_platform_coverage(readme)
    return [
        CheckResult(id=1, name="README problem statement", category="semantic",
                    score=critique["problem_clarity"], max_score=10,
                    passed=critique["problem_clarity"] >= 7, impact=20),
        CheckResult(id=2, name="README has FAQ section", category="semantic",
                    score=critique["has_faq"], max_score=10,
                    passed=critique["has_faq"] >= 7, impact=15),
        CheckResult(id=3, name="README when to use / not to use", category="semantic",
                    score=critique["has_when_to_use"], max_score=10,
                    passed=critique["has_when_to_use"] >= 7, impact=10),
        CheckResult(id=4, name="README has runnable code examples", category="semantic",
                    score=critique["has_code_examples"], max_score=10,
                    passed=critique["has_code_examples"] >= 7, impact=15),
        CheckResult(id=8, name="FAQ section in README", category="semantic",
                    score=faq_score, max_score=10, passed=faq_passed, impact=5),
        CheckResult(id=9, name="When to use / not to use in README", category="semantic",
                    score=wtu_score, max_score=10, passed=wtu_passed, impact=8),
        CheckResult(id=10, name="Citation-worthy content", category="semantic",
                    score=cwc_score, max_score=10, passed=cwc_passed, impact=8),
        CheckResult(id=12, name="AI platform coverage in README", category="semantic",
                    score=pc_score, max_score=10, passed=pc_passed, impact=10),
    ]


def run_audit(repo_root: Path) -> AuditReport:
    """Run the 12-check audit on `repo_root` and return the report."""
    assets = scanner.scan_repo(repo_root)
    results = _structural_checks(assets) + _semantic_checks(assets)
    return AuditReport(project_name=repo_root.name, results=results)


def main(argv: list[str] | None = None) -> int:
    # Reconfigure stdout to UTF-8 for Windows compatibility (emoji glyphs in reports)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        prog="aisurface",
        description="Audit a repo for AI-search citation readiness.",
    )
    parser.add_argument("path", nargs="?", default=".", help="Repo root (default: cwd)")
    parser.add_argument("--learn", action="store_true", help="Enable teacher mode")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of Markdown")
    args = parser.parse_args(argv)

    repo_root = Path(args.path).resolve()
    if not repo_root.exists():
        print(f"Error: {repo_root} does not exist", file=sys.stderr)
        return 1

    report_obj = run_audit(repo_root)
    if args.json:
        import json
        print(json.dumps({
            "project_name": report_obj.project_name,
            "results": [
                {"id": r.id, "name": r.name, "score": r.score, "max_score": r.max_score, "passed": r.passed, "impact": r.impact}
                for r in report_obj.results
            ],
            "skipped": report_obj.skipped,
            "errors": report_obj.errors,
        }, indent=2, ensure_ascii=False))
    else:
        print(report.render_report(report_obj, teacher_mode=args.learn))
    return 0


if __name__ == "__main__":
    sys.exit(main())

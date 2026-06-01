"""CLI entry point for aisurface audit."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from scripts import critic, distribution, github_meta, report, scanner
from scripts.report import AuditReport, CheckResult
from scripts.scanner import RepoAssets


def _read_readme(assets: RepoAssets) -> str:
    if assets.readme is None:
        return ""
    return assets.readme.read_text(encoding="utf-8", errors="ignore")


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
    # #11 Distribution signals — use check_signals with placeholder inputs
    sig = distribution.check_signals(
        project_name=assets.root.name,
        description=readme_text[:200] if readme_text else "",
        github_stars=0,
        has_npm=False,
        has_pypi=False,
    )
    dist_passed = sig["score"] >= 6
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
        CheckResult(id=8, name="GitHub description clarity", category="semantic",
                    score=5, max_score=10, passed=False, impact=5),  # Heuristic
        CheckResult(id=9, name="docs/ has FAQ page", category="semantic",
                    score=5, max_score=10, passed=False, impact=8),
        CheckResult(id=10, name="docs/ has comparison/alternatives", category="semantic",
                    score=5, max_score=10, passed=False, impact=8),
        CheckResult(id=12, name="Original citable content", category="semantic",
                    score=5, max_score=10, passed=False, impact=10),
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

from scripts.report import AuditReport, CheckResult, render_report


def _sample_check_results():
    return [
        CheckResult(id=1, name="README problem statement", category="semantic", score=8, max_score=10, passed=True, impact=15),
        CheckResult(id=5, name="Schema.org markup", category="structural", score=0, max_score=10, passed=False, impact=20),
        CheckResult(id=6, name="llms.txt present", category="structural", score=10, max_score=10, passed=True, impact=10),
    ]


def test_render_report_contains_health_score():
    report = AuditReport(project_name="my-proj", results=_sample_check_results())
    output = render_report(report)
    assert "my-proj" in output
    assert "Health score" in output


def test_render_report_contains_must_fix_section():
    report = AuditReport(project_name="p", results=_sample_check_results())
    output = render_report(report)
    assert "Must-fix" in output or "\U0001f534" in output
    assert "Schema.org" in output


def test_render_report_contains_sub_scores():
    report = AuditReport(project_name="p", results=_sample_check_results())
    output = render_report(report)
    # Should mention at least one sub-score
    assert "Readability" in output
    assert "Structure" in output


def test_render_report_handles_empty_results():
    report = AuditReport(project_name="empty", results=[])
    output = render_report(report)
    assert "empty" in output


def test_render_report_shows_structural_finding_file_path():
    """StructuralFinding results should include their file_path in the rendered output."""
    from scripts.findings import StructuralFinding

    results = [
        StructuralFinding(id=5, name="Schema.org markup on website", category="structural",
                          score=5, max_score=10, passed=True, impact=20,
                          file_path="index.schema.json"),
        CheckResult(id=1, name="README problem statement", category="semantic",
                    score=8, max_score=10, passed=True, impact=15),
    ]
    report = AuditReport(project_name="p", results=results)
    output = render_report(report)
    assert "`index.schema.json`" in output
    # Plain CheckResults have no file_path; ensure we didn't accidentally render one.
    assert "None" not in output


def test_compute_health_score_weighted():
    """_compute_health_score takes a categories dict and returns (score, max_score=100)."""
    from scripts.report import _compute_health_score

    all_pass = {
        "citation_friendliness": [
            CheckResult(id=4, name="a", category="semantic", score=10, max_score=10, passed=True, impact=10),
            CheckResult(id=8, name="b", category="semantic", score=10, max_score=10, passed=True, impact=5),
            CheckResult(id=9, name="c", category="semantic", score=10, max_score=10, passed=True, impact=8),
            CheckResult(id=10, name="d", category="semantic", score=10, max_score=10, passed=True, impact=8),
        ],
        "structure": [
            CheckResult(id=5, name="e", category="structural", score=10, max_score=10, passed=True, impact=20),
            CheckResult(id=6, name="f", category="structural", score=10, max_score=10, passed=True, impact=15),
            CheckResult(id=7, name="g", category="structural", score=10, max_score=10, passed=True, impact=5),
        ],
        "readability": [
            CheckResult(id=1, name="h", category="semantic", score=10, max_score=10, passed=True, impact=20),
            CheckResult(id=2, name="i", category="semantic", score=10, max_score=10, passed=True, impact=15),
            CheckResult(id=3, name="j", category="semantic", score=10, max_score=10, passed=True, impact=10),
        ],
        "distribution": [
            CheckResult(id=11, name="k", category="structural", score=10, max_score=10, passed=True, impact=5),
            CheckResult(id=12, name="l", category="semantic", score=10, max_score=10, passed=True, impact=10),
        ],
    }

    # All pass → 100
    score, max_score = _compute_health_score(all_pass)
    assert max_score == 100
    assert score == 100

    # All zero → 0
    all_fail = {
        cat: [CheckResult(id=r.id, name=r.name, category=r.category,
                           score=0, max_score=10, passed=False, impact=5)
              for r in results]
        for cat, results in all_pass.items()
    }
    score, max_score = _compute_health_score(all_fail)
    assert max_score == 100
    assert score == 0

    # Half in citation_friendliness (50%) → 20 (citation) + 30 (structure) + 20 (readability) + 10 (distribution) = 80
    half = {cat: list(results) for cat, results in all_pass.items()}
    half["citation_friendliness"] = [
        CheckResult(id=4, name="a", category="semantic", score=5, max_score=10, passed=True, impact=10),
        CheckResult(id=8, name="b", category="semantic", score=5, max_score=10, passed=True, impact=5),
        CheckResult(id=9, name="c", category="semantic", score=5, max_score=10, passed=True, impact=8),
        CheckResult(id=10, name="d", category="semantic", score=5, max_score=10, passed=True, impact=8),
    ]
    score, max_score = _compute_health_score(half)
    assert max_score == 100
    assert score == 80

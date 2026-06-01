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

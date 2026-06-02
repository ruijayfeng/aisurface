"""Unit tests for the safe_check decorator."""
from __future__ import annotations

from scripts.report import CheckResult
from scripts.safe_check import safe_check


def test_safe_check_catches_exception():
    """safe_check catches an exception and returns a CheckResult with skipped=True."""

    @safe_check
    def throwing_check():
        raise RuntimeError("network timeout")

    result = throwing_check()
    assert isinstance(result, CheckResult)
    assert result.passed is False
    assert result.skipped is True
    assert "network timeout" in result.error


def test_safe_check_passes_through_on_success():
    """safe_check returns the underlying result unchanged when no exception."""

    @safe_check
    def passing_check():
        return CheckResult(
            id="x",
            name="x",
            category="semantic",
            score=10,
            max_score=10,
            passed=True,
            impact=5,
        )

    result = passing_check()
    assert isinstance(result, CheckResult)
    assert result.passed is True
    assert result.skipped is False
    assert result.error is None


def test_safe_check_preserves_check_metadata():
    """When the wrapped function returns a CheckResult, safe_check returns it as-is."""
    original = CheckResult(
        id=42,
        name="custom check",
        category="structural",
        score=7,
        max_score=10,
        passed=True,
        impact=3,
    )

    @safe_check
    def metadata_check():
        return original

    result = metadata_check()
    assert result.id == 42
    assert result.name == "custom check"
    assert result.category == "structural"
    assert result.score == 7
    assert result.max_score == 10
    assert result.passed is True
    assert result.impact == 3

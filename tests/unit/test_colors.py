"""Unit tests for the color helper module."""
from __future__ import annotations


def test_should_colorize_false_when_no_color_env(monkeypatch):
    """should_colorize() returns False when NO_COLOR is set."""
    from scripts.colors import should_colorize

    monkeypatch.setenv("NO_COLOR", "1")
    monkeypatch.setattr("sys.stdout.isatty", lambda: True)
    assert should_colorize() is False


def test_colorize_returns_plain_when_disabled(monkeypatch):
    """colorize() returns text unchanged when should_colorize() is False."""
    from scripts.colors import colorize, should_colorize

    monkeypatch.setenv("NO_COLOR", "1")
    assert should_colorize() is False
    result = colorize("hello", "red")
    assert result == "hello"


def test_colorize_wraps_when_enabled(monkeypatch):
    """colorize() wraps text with ANSI codes when should_colorize() is True."""
    from scripts.colors import colorize, should_colorize

    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.setattr("sys.stdout.isatty", lambda: True)
    assert should_colorize() is True
    result = colorize("hello", "red")
    assert "\x1b[" in result  # ANSI escape
    assert "hello" in result

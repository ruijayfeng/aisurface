"""Unit tests for the safe_dispatch decorator."""
from __future__ import annotations

from types import SimpleNamespace

import pytest

from scripts.safe_dispatch import safe_dispatch


def test_catches_module_not_found_for_scripts(capsys):
    """safe_dispatch catches ModuleNotFoundError when the missing module is in scripts.*"""

    @safe_dispatch
    def handler(args):
        raise ModuleNotFoundError("No module named 'scripts.foo'")

    result = handler(SimpleNamespace())
    captured = capsys.readouterr()
    assert result == 1
    assert "✗" in captured.err


def test_catches_file_not_found_and_includes_path(capsys):
    """safe_dispatch catches FileNotFoundError and includes args.path in the hint"""

    @safe_dispatch
    def handler(args):
        with open(args.path) as f:  # noqa: F841
            return 0

    args = SimpleNamespace(path="/nope")
    result = handler(args)
    captured = capsys.readouterr()
    assert result == 1
    assert "/nope" in captured.err
    assert "路径不存在" in captured.err


def test_catches_unicode_encode_error(capsys):
    """safe_dispatch catches UnicodeEncodeError and hints at PYTHONUTF8"""

    @safe_dispatch
    def handler(args):
        raise UnicodeEncodeError("utf-8", "x", 0, 1, "reason")

    result = handler(SimpleNamespace())
    captured = capsys.readouterr()
    assert result == 1
    assert "PYTHONUTF8" in captured.err


def test_catches_permission_error_on_cache_dir(capsys, monkeypatch):
    """safe_dispatch catches PermissionError on the cache dir and hints at AISURFACE_CACHE_DIR"""
    monkeypatch.setenv("AISURFACE_CACHE_DIR", "/var/cache/aisurface")

    @safe_dispatch
    def handler(args):
        raise PermissionError(13, "Permission denied", "/var/cache/aisurface/foo.json")

    result = handler(SimpleNamespace())
    captured = capsys.readouterr()
    assert result == 1
    assert "/var/cache/aisurface" in captured.err
    assert "AISURFACE_CACHE_DIR" in captured.err


def test_does_not_catch_keyboard_interrupt():
    """safe_dispatch must NOT catch KeyboardInterrupt; it must re-raise"""

    @safe_dispatch
    def handler(args):
        raise KeyboardInterrupt()

    with pytest.raises(KeyboardInterrupt):
        handler(SimpleNamespace())


def test_does_not_catch_value_error():
    """safe_dispatch must NOT catch unrelated ValueError; it must re-raise"""

    @safe_dispatch
    def handler(args):
        raise ValueError("not for us")

    with pytest.raises(ValueError, match="not for us"):
        handler(SimpleNamespace())

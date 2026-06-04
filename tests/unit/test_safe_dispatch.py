"""Unit tests for the safe_dispatch decorator.

Bilingual coverage: the decorator accepts a `lang` keyword (defaults to
inference from LANG env) and emits hints in either Chinese or English.
"""
from __future__ import annotations

from types import SimpleNamespace

import pytest

from scripts.safe_dispatch import _infer_lang, safe_dispatch

# -- Catch tests, parametrized over language --------------------------------

@pytest.mark.parametrize(
    "lang, expected_fragment",
    [
        ("zh", "没装"),
        ("en", "is not installed"),
    ],
)
def test_catches_module_not_found(lang, expected_fragment, capsys):
    """safe_dispatch with `lang` produces a bilingual hint for ModuleNotFoundError on scripts.*"""

    @safe_dispatch(lang=lang)
    def handler(args):
        raise ModuleNotFoundError("No module named 'scripts.foo'")

    result = handler(SimpleNamespace())
    captured = capsys.readouterr()
    assert result == 1
    assert "✗" in captured.err
    assert expected_fragment in captured.err


@pytest.mark.parametrize(
    "lang, expected_fragment",
    [
        ("zh", "路径不存在"),
        ("en", "path not found"),
    ],
)
def test_catches_file_not_found(lang, expected_fragment, capsys):
    """safe_dispatch with `lang` produces a bilingual hint for FileNotFoundError, includes args.path"""

    @safe_dispatch(lang=lang)
    def handler(args):
        with open(args.path) as f:  # noqa: F841
            return 0

    args = SimpleNamespace(path="/nope")
    result = handler(args)
    captured = capsys.readouterr()
    assert result == 1
    assert "/nope" in captured.err
    assert expected_fragment in captured.err


@pytest.mark.parametrize(
    "lang, expected_fragment",
    [
        ("zh", "控制台编码"),
        ("en", "console encoding"),
    ],
)
def test_catches_unicode_error(lang, expected_fragment, capsys):
    """safe_dispatch with `lang` produces a bilingual hint for UnicodeEncodeError"""

    @safe_dispatch(lang=lang)
    def handler(args):
        raise UnicodeEncodeError("utf-8", "x", 0, 1, "reason")

    result = handler(SimpleNamespace())
    captured = capsys.readouterr()
    assert result == 1
    assert "PYTHONUTF8" in captured.err
    assert expected_fragment in captured.err


@pytest.mark.parametrize(
    "lang, expected_fragment",
    [
        ("zh", "写不进"),
        ("en", "cannot write"),
    ],
)
def test_catches_permission_error(lang, expected_fragment, capsys, monkeypatch):
    """safe_dispatch with `lang` produces a bilingual hint for PermissionError on cache dir"""
    monkeypatch.setenv("AISURFACE_CACHE_DIR", "/var/cache/aisurface")

    @safe_dispatch(lang=lang)
    def handler(args):
        raise PermissionError(13, "Permission denied", "/var/cache/aisurface/foo.json")

    result = handler(SimpleNamespace())
    captured = capsys.readouterr()
    assert result == 1
    assert "/var/cache/aisurface" in captured.err
    assert "AISURFACE_CACHE_DIR" in captured.err
    assert expected_fragment in captured.err


# -- Re-raise tests (language-independent) ----------------------------------

def test_does_not_catch_keyboard_interrupt():
    """safe_dispatch must NOT catch KeyboardInterrupt; it must re-raise"""

    @safe_dispatch(lang="en")
    def handler(args):
        raise KeyboardInterrupt()

    with pytest.raises(KeyboardInterrupt):
        handler(SimpleNamespace())


def test_does_not_catch_value_error():
    """safe_dispatch must NOT catch unrelated ValueError; it must re-raise"""

    @safe_dispatch(lang="en")
    def handler(args):
        raise ValueError("not for us")

    with pytest.raises(ValueError, match="not for us"):
        handler(SimpleNamespace())


def test_does_not_catch_module_not_found_for_unrelated_module():
    """safe_dispatch must NOT catch ModuleNotFoundError for non-scripts.* modules; re-raise"""

    @safe_dispatch(lang="en")
    def handler(args):
        raise ModuleNotFoundError("No module named 'pandas'")

    with pytest.raises(ModuleNotFoundError):
        handler(SimpleNamespace())


def test_does_not_catch_permission_error_on_unrelated_path():
    """safe_dispatch must NOT catch PermissionError for non-cache paths; re-raise"""

    @safe_dispatch(lang="en")
    def handler(args):
        raise PermissionError(13, "Permission denied", "/etc/passwd")

    with pytest.raises(PermissionError):
        handler(SimpleNamespace())


# -- Language inference ------------------------------------------------------

def test_infer_lang_zh_simplified(monkeypatch):
    """_infer_lang returns 'zh' when LANG starts with zh_* (Simplified)"""
    monkeypatch.setenv("LANG", "zh_CN.UTF-8")
    assert _infer_lang() == "zh"


def test_infer_lang_zh_traditional(monkeypatch):
    """_infer_lang returns 'zh' when LANG starts with zh_* (Traditional / Big5)"""
    monkeypatch.setenv("LANG", "zh_TW.Big5")
    assert _infer_lang() == "zh"


def test_infer_lang_en(monkeypatch):
    """_infer_lang returns 'en' when LANG is en_*"""
    monkeypatch.setenv("LANG", "en_US.UTF-8")
    assert _infer_lang() == "en"


def test_infer_lang_default_english_when_unset(monkeypatch):
    """_infer_lang returns 'en' when LANG is unset (default fallback)"""
    monkeypatch.delenv("LANG", raising=False)
    assert _infer_lang() == "en"


# -- Explicit lang override --------------------------------------------------

def test_explicit_lang_overrides_env(monkeypatch, capsys):
    """Explicit lang='en' overrides LANG=zh_* to produce English hints"""
    monkeypatch.setenv("LANG", "zh_CN.UTF-8")

    @safe_dispatch(lang="en")
    def handler(args):
        raise ModuleNotFoundError("No module named 'scripts.foo'")

    result = handler(SimpleNamespace())
    captured = capsys.readouterr()
    assert result == 1
    assert "is not installed" in captured.err
    assert "没装" not in captured.err


def test_default_lang_infers_from_env(monkeypatch, capsys):
    """When lang is None, the wrapper infers from LANG at call time"""
    monkeypatch.setenv("LANG", "zh_CN.UTF-8")

    @safe_dispatch
    def handler(args):
        raise ModuleNotFoundError("No module named 'scripts.foo'")

    result = handler(SimpleNamespace())
    captured = capsys.readouterr()
    assert result == 1
    assert "没装" in captured.err

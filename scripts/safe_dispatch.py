"""
 * [INPUT]: Depends on stdlib `functools`/`os`/`sys` and `scripts.colors.colorize`.
 * [OUTPUT]: Provides `@safe_dispatch` decorator that catches a curated set of user-facing exceptions in CLI subcommand handlers — `ModuleNotFoundError` (only when the missing module is in `scripts.*`), `FileNotFoundError`, `UnicodeEncodeError`, `PermissionError` on the cache dir — printing a red `✗` hint to stderr and returning exit 1. The hint is bilingual: `lang='zh'` or `lang='en'`. When `lang` is omitted the language is inferred from the LANG env var (LANG starts with `zh` → Chinese, anything else including unset → English). Re-raises `KeyboardInterrupt` and any other exception unchanged.
 * [POS]: CLI error-message wrapper. Applied to `cmd_audit`/`cmd_fix`/`cmd_verify`/`cmd_doctor` in `cli.py`. Sits at the dispatcher boundary, one layer above `safe_check` (which wraps individual audit checks).
 * [PROTOCOL]: Update this header when changed, then check CLAUDE.md

safe_dispatch decorator: catch user-facing errors in CLI subcommand handlers
and print actionable hints to stderr before returning exit 1.

Why only these four exception types?
  - ModuleNotFoundError: "aisurface: command not found" is unactionable;
    we hint at a reinstall when the missing module is in our own namespace.
  - FileNotFoundError: the user typed a path that doesn't exist; tell them
    which path we tried, in their language.
  - UnicodeEncodeError: Windows console (cp936/cp1252) blows up on
    emoji/CJK; the fix is `set PYTHONUTF8=1`.
  - PermissionError on the cache dir: surface the env var so the user
    knows which directory is misconfigured.

Bilingual hints: language is selected per-call so tests can monkeypatch
LANG. The default fallback is English because the user base is global and
English error messages are the lowest-common-denominator for support;
Chinese speakers on zh_* locales still see Chinese.

Anything else (KeyboardInterrupt, ValueError, real bugs) re-raises so we
never mask a real bug as a user-friendly error.
"""
from __future__ import annotations

import functools
import os
import sys
from collections.abc import Callable
from typing import Any

from scripts import colors

_HINTS: dict[str, dict[str, str]] = {
    "zh": {
        "module_not_found": "✗ aisurface 没装(或装错环境). 跑: pip install aisurface",
        "path_not_found": "✗ 路径不存在: {path}. 检查下路径再试",
        "unicode_error": "✗ 控制台编码有问题. 设 PYTHONUTF8=1 和 PYTHONIOENCODING=utf-8",
        "permission_error": "✗ 写不进 {cache_str}. 看权限,或设 AISURFACE_CACHE_DIR 改路径",
    },
    "en": {
        "module_not_found": "✗ aisurface is not installed (or installed in the wrong env). Run: pip install aisurface",
        "path_not_found": "✗ path not found: {path}. Check the path and try again",
        "unicode_error": "✗ console encoding problem. Set PYTHONUTF8=1 and PYTHONIOENCODING=utf-8",
        "permission_error": "✗ cannot write to {cache_str}. Check permissions, or set AISURFACE_CACHE_DIR to a writable path",
    },
}


def _infer_lang() -> str:
    """Infer display language from LANG env. LANG starts with 'zh' → 'zh', else 'en'."""
    return "zh" if os.environ.get("LANG", "").lower().startswith("zh") else "en"


def _hint(msg: str) -> None:
    """Print a red hint line to stderr (msg may include a leading ✗)."""
    print(f"  {colors.colorize(msg, 'red')}", file=sys.stderr)


def safe_dispatch(
    handler: Callable[..., int] | None = None, *, lang: str | None = None
) -> Callable[..., int]:
    """Wrap a CLI subcommand handler to catch user-facing errors.

    The handler is expected to take the argparse `args` namespace as its
    only positional argument and return an int exit code.

    `lang` selects the hint language ('zh' or 'en'). When None, the
    language is inferred from the LANG env var on each call: LANG=zh_*
    → Chinese, anything else (including unset) → English.

    Two call forms:
        @safe_dispatch                       # default — infer from LANG
        @safe_dispatch(lang="en")            # explicit override
    """
    def make_wrapper(fn: Callable[..., int]) -> Callable[..., int]:
        @functools.wraps(fn)
        def wrapper(args: Any) -> int:
            effective_lang = lang if lang is not None else _infer_lang()
            hints = _HINTS[effective_lang]
            try:
                return fn(args)
            except ModuleNotFoundError as e:
                # Only catch if the missing module is ours; pandas/httpx/etc.
                # errors are real bugs, not user-install problems.
                if "scripts." not in str(e):
                    raise
                _hint(hints["module_not_found"])
                return 1
            except FileNotFoundError:
                path = getattr(args, "path", "<unknown>")
                _hint(hints["path_not_found"].format(path=path))
                return 1
            except UnicodeEncodeError:
                _hint(hints["unicode_error"])
                return 1
            except PermissionError as e:
                cache_env = os.environ.get("AISURFACE_CACHE_DIR")
                default_cache = "~/.aisurface"
                cache_str = cache_env or default_cache
                if cache_str in str(e) or default_cache in str(e):
                    _hint(hints["permission_error"].format(cache_str=cache_str))
                    return 1
                raise
        return wrapper

    if handler is None:
        # Called as @safe_dispatch(lang='en') or @safe_dispatch() — return a decorator.
        return make_wrapper
    # Called as @safe_dispatch — apply directly.
    return make_wrapper(handler)

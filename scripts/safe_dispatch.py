"""
 * [INPUT]: Depends on stdlib `functools`/`os`/`sys` and `scripts.colors.colorize`.
 * [OUTPUT]: Provides `@safe_dispatch` decorator that catches a curated set of user-facing exceptions in CLI subcommand handlers — `ModuleNotFoundError` (only when the missing module is in `scripts.*`), `FileNotFoundError`, `UnicodeEncodeError`, `PermissionError` on the cache dir — printing a red `✗` hint to stderr and returning exit 1. Re-raises `KeyboardInterrupt` and any other exception unchanged.
 * [POS]: CLI error-message wrapper. Applied to `cmd_audit`/`cmd_fix`/`cmd_verify` in `cli.py` (Task 2). Sits at the dispatcher boundary, one layer above `safe_check` (which wraps individual audit checks).
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

Anything else (KeyboardInterrupt, ValueError, real bugs) re-raises so we
never mask a real bug as a user-friendly error.
"""
from __future__ import annotations

import functools
import os
import sys
from collections.abc import Callable

from scripts import colors


def _hint(msg: str) -> None:
    """Print a red ✗ hint line to stderr."""
    print(f"  {colors.colorize('✗', 'red')} {msg}", file=sys.stderr)


def safe_dispatch(handler: Callable[..., int]) -> Callable[..., int]:
    """Wrap a CLI subcommand handler to catch user-facing errors.

    The handler is expected to take the argparse `args` namespace as its
    first positional argument and return an int exit code.
    """
    @functools.wraps(handler)
    def wrapper(*args, **kwargs) -> int:
        try:
            return handler(*args, **kwargs)
        except ModuleNotFoundError as e:
            # Only catch if the missing module is ours; pandas/httpx/etc.
            # errors are real bugs, not user-install problems.
            if "scripts." not in str(e):
                raise
            _hint(
                f"Internal module not found: {e}. "
                f"Try `pip install -e .` or reinstall the skill."
            )
            return 1
        except FileNotFoundError as e:
            path = getattr(args[0], "path", "<unknown>") if args else "<unknown>"
            _hint(f"路径不存在: {path} ({e})")
            return 1
        except UnicodeEncodeError as e:
            _hint(
                f"Console encoding error: {e}. "
                f"Hint: set PYTHONUTF8=1 (or `chcp 65001` on Windows)."
            )
            return 1
        except PermissionError as e:
            cache = os.environ.get("AISURFACE_CACHE_DIR", "<unset>")
            _hint(
                f"Permission denied on cache dir {cache}: {e}. "
                f"Hint: check AISURFACE_CACHE_DIR or directory permissions."
            )
            return 1
    return wrapper

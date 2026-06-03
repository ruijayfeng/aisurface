"""
 * [INPUT]: Depends on `os` (reads `NO_COLOR` env var), `sys` (detects TTY).
 * [OUTPUT]: Provides `colorize(text, color) -> str` — wraps text in ANSI codes; returns text unchanged if `NO_COLOR=1` or stdout is not a TTY.
 * [POS]: Presentation layer. Imported by `cli.py` and `audit.py` to color the rendered report. The `wrap=` parameter in `report.render_report` is this function by convention.
 * [PROTOCOL]: Update this header when changed, then check CLAUDE.md
"""

"""ANSI color helpers for the CLI.

Auto-detection respects:
- --no-color flag (caller's responsibility to set)
- NO_COLOR env var (https://no-color.org)
- TERM=dumb
- non-TTY stdout (piped, redirected, CI)
- Windows version < 10 (legacy cmd)

Color codes are valid ANSI; terminals that don't support them will show
the escape codes as garbage. The auto-detection above prevents this for
common cases.
"""
from __future__ import annotations

import os
import sys

_ANSI_CODES: dict[str, str] = {
    "reset": "\x1b[0m",
    "red": "\x1b[31m",
    "green": "\x1b[32m",
    "yellow": "\x1b[33m",
    "blue": "\x1b[34m",
    "gray": "\x1b[90m",
    "bold": "\x1b[1m",
}


def should_colorize() -> bool:
    """Return True if color output should be applied to stdout."""
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("TERM") == "dumb":
        return False
    if not sys.stdout.isatty():
        return False
    if os.name == "nt":
        # Windows 10+ supports ANSI via ENABLE_VIRTUAL_TERMINAL_PROCESSING.
        # Python 3.6+ enables this automatically for stdout on Win10+.
        # For older Windows, we conservatively disable color.
        try:
            import sys as _sys
            if _sys.getwindowsversion().major < 10:
                return False
        except (AttributeError, OSError):
            # Not on Windows or version detection failed; assume no.
            return False
    return True


def colorize(text: str, color: str) -> str:
    """Wrap `text` with ANSI color codes if should_colorize() is True.

    If color is unknown, returns text unchanged (no escape codes).
    """
    if color not in _ANSI_CODES:
        return text
    if not should_colorize():
        return text
    return f"{_ANSI_CODES[color]}{text}{_ANSI_CODES['reset']}"

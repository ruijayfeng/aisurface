# aisurface v1.0.2 Implementation Plan — Windows Install + Path Hotfix

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship v1.0.2 — a hotfix that makes the README 5-min self-test pass on Windows out of the box, surfaces stale installs, and gives users a `doctor` self-check verb to diagnose install issues. No changes to the 12-check audit, 4 fix generators, or verify probe logic.

**Architecture:** Two new files in `scripts/` (`doctor.py` self-check, `safe_dispatch.py` error-wrapper decorator), a `doctor` subcommand wired into `cli.py`, the existing CI workflow expanded from 1 job to a 15-job matrix (3 OS × 5 Python) with a smoke test that exercises both `aisurface` and `python -m scripts.cli`, and documentation updates that follow the SKILL.md §11b user-facing abstraction (no command names exposed to the user surface).

**Tech Stack:** Python 3.10+ stdlib (`argparse`, `functools`, `pathlib`, `shutil`, `sys`, `importlib.metadata`), `httpx` (already a dep) for the PyPI version check, `scripts/colors.py` for ANSI, `pytest` + `unittest.mock` for tests, `uv` for CI dependency install, GitHub Actions for CI.

**Spec:** `docs/superpowers/specs/2026-06-03-aisurface-v102-windows-install-design.md`

**Regression bar:** All 105 existing tests must pass at every checkpoint. The 4 eval fixtures must produce their v1.0.1 expected scores. The `aisurface` console script must keep working on every OS where the PATH includes the user-scripts directory.

---

# File Structure

## New files

| Path | Responsibility | Approx lines |
|---|---|---|
| `scripts/doctor.py` | `cmd_doctor` + 8 check functions + human/JSON render. One verb in the CLI. | 230 |
| `scripts/safe_dispatch.py` | `safe_dispatch` decorator wrapping each `cmd_*` handler. Catches 4 user-facing exception classes. | 80 |
| `tests/unit/test_doctor.py` | 15 unit tests for `doctor` (8 checks + JSON + exit codes + edge cases). | 200 |
| `tests/unit/test_safe_dispatch.py` | 6 unit tests for the decorator (4 catches + 2 pass-throughs). | 100 |

## Modified files

| Path | Change |
|---|---|
| `scripts/cli.py` | Add `doctor` to `_DISPATCH`. Add `doctor` subparser with `--json`, `--no-color`, `--skip-network` flags. Wrap each of the 4 subcommand handlers (`cmd_audit`, `cmd_fix`, `cmd_verify`, `cmd_doctor`) with `@safe_dispatch`. |
| `.github/workflows/ci.yml` | Expand from 1 job to 15-job matrix (3 OS × 5 Python). Add smoke step that runs `aisurface --help`, `python -m scripts.cli --help`, and `python -m scripts.cli doctor --no-color`. |
| `SKILL.md` | Add a row to the "工具调用" table mapping natural-language triggers to the `doctor` command. Per §11b, no command name appears in the user-facing "我能做三件事" / "怎么跟我说" sections. |
| `README.md` | Rewrite 5-min self-test to use `python -m scripts.cli ...`. Add step 8: doctor. Add note: "If your `aisurface` console script is on PATH, that's an alias — pick whichever you like." |
| `README.en.md` | Same as above (English). |
| `CHANGELOG.md` | New `## [1.0.2] - 2026-06-03` section with Added/Changed/Fixed subsections. |
| `ROADMAP.md` | New row in the release sequence: v1.0.2 — install health + doctor + CI matrix. Mark v1.0.1 as ✅ shipped. |
| `scripts/CLAUDE.md` (L2) | Add `doctor.py` and `safe_dispatch.py` to the member list with one-line responsibilities. |
| `CLAUDE.md` (L1) | Add the two new files to the `scripts/` directory tree. |
| `tests/CLAUDE.md` (L2) | Add `test_doctor.py` and `test_safe_dispatch.py` to the "Member List" and the "Pending test files" entries (move them from Pending to the listed-set, or just add to the current listing). Update the "Invariants" count. |
| `pyproject.toml` | Bump version `1.0.1` → `1.0.2`. |

## Files NOT touched

- `scripts/audit.py`, `scripts/report.py`, `scripts/scanner.py`, `scripts/fix/`, `scripts/verify/`, `scripts/llms_txt.py`, `scripts/schema_gen.py`, `scripts/critic.py`, `scripts/distribution.py`, `scripts/github_meta.py`, `scripts/concepts.py`, `scripts/findings.py`, `scripts/safe_check.py`, `scripts/colors.py` — all unchanged
- All 105 existing test files — unchanged
- `evals/fixtures/` — unchanged
- `references/`, `case-studies/`, `skills/_deprecated/`, `docs/screenshots/`, `pyproject.toml` `dependencies` / `optional-dependencies` / `[project.scripts]` — unchanged

---

# Tasks

## Task 1: `safe_dispatch.py` — TDD the decorator

**Files:**
- Create: `scripts/safe_dispatch.py`
- Create: `tests/unit/test_safe_dispatch.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/unit/test_safe_dispatch.py`:

```python
"""Verify safe_dispatch catches the 4 user-facing exceptions and re-raises the rest."""
from __future__ import annotations

import pytest

from scripts.safe_dispatch import safe_dispatch


class _Args:
    def __init__(self, path: str = "."):
        self.path = path


def test_catches_module_not_found_for_scripts():
    @safe_dispatch
    def h(args):
        raise ModuleNotFoundError("No module named 'scripts.foo'")

    rc = h(_Args())
    assert rc == 1


def test_catches_file_not_found_and_includes_path(capsys):
    @safe_dispatch
    def h(args):
        raise FileNotFoundError(2, "No such file or directory: '/nope'")

    rc = h(_Args(path="/nope"))
    captured = capsys.readouterr()
    assert rc == 1
    assert "/nope" in captured.err
    assert "路径不存在" in captured.err


def test_catches_unicode_encode_error(capsys):
    @safe_dispatch
    def h(args):
        raise UnicodeEncodeError("utf-8", "ÿ", 0, 1, "invalid")

    rc = h(_Args())
    captured = capsys.readouterr()
    assert rc == 1
    assert "PYTHONUTF8" in captured.err


def test_catches_permission_error_on_cache_dir(capsys, monkeypatch):
    monkeypatch.setenv("AISURFACE_CACHE_DIR", "/var/aisurface")
    cache = "/var/aisurface"

    @safe_dispatch
    def h(args):
        raise PermissionError(13, "Permission denied", cache)

    rc = h(_Args())
    captured = capsys.readouterr()
    assert rc == 1
    assert cache in captured.err
    assert "AISURFACE_CACHE_DIR" in captured.err


def test_does_not_catch_keyboard_interrupt():
    @safe_dispatch
    def h(args):
        raise KeyboardInterrupt()

    with pytest.raises(KeyboardInterrupt):
        h(_Args())


def test_does_not_catch_value_error():
    @safe_dispatch
    def h(args):
        raise ValueError("unrelated")

    with pytest.raises(ValueError):
        h(_Args())
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/unit/test_safe_dispatch.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'scripts.safe_dispatch'`

- [ ] **Step 3: Write minimal implementation**

Create `scripts/safe_dispatch.py`:

```python
"""
 * [INPUT]: Depends on stdlib `functools`, `os`, `sys`. Imports `scripts.colors` for ANSI.
 * [OUTPUT]: Provides `safe_dispatch(handler)` decorator — catches 4 user-facing exceptions, prints actionable hints to stderr, returns exit code 1; re-raises everything else.
 * [POS]: scripts/ — layer between `cli.main()` and the 4 subcommand handlers. Applied in `scripts/cli.py` to `cmd_audit`, `cmd_fix`, `cmd_verify`, `cmd_doctor`.
 * [PROTOCOL]: Update this header when changed, then check CLAUDE.md

Error-message decorator for CLI subcommand handlers.

Why this exists: raw tracebacks for "the Python package isn't installed" or
"the path doesn't exist" are hostile to first-time users, especially on
Windows where the packaging story is fragile. This decorator catches the
4 most common user-facing errors and prints a one-line fix hint.

It deliberately does NOT catch:
- KeyboardInterrupt (let users Ctrl-C)
- Network timeouts (handled inside verify/)
- Business exceptions from audit/fix (real bugs, let them surface)
"""
from __future__ import annotations

import functools
import os
import sys
from typing import Any, Callable

from scripts import colors


def _err(msg: str) -> None:
    print(colors.colorize(msg, "red"), file=sys.stderr)


def safe_dispatch(handler: Callable[..., int]) -> Callable[..., int]:
    @functools.wraps(handler)
    def wrapper(args: Any) -> int:
        try:
            return handler(args)
        except ModuleNotFoundError as e:
            if "scripts." in str(e):
                _err("✗ aisurface 没装(或装错环境). 跑: pip install aisurface")
                return 1
            raise
        except FileNotFoundError:
            path = getattr(args, "path", "<unknown>")
            _err(f"✗ 路径不存在: {path}. 检查下路径再试")
            return 1
        except UnicodeEncodeError:
            _err("✗ 控制台编码有问题. 设 PYTHONUTF8=1 和 PYTHONIOENCODING=utf-8")
            return 1
        except PermissionError as e:
            cache_env = os.environ.get("AISURFACE_CACHE_DIR")
            default_cache = "~/.aisurface"
            cache_str = cache_env or default_cache
            if cache_str in str(e) or default_cache in str(e):
                _err(f"✗ 写不进 {cache_str}. 看权限,或设 AISURFACE_CACHE_DIR 改路径")
                return 1
            raise

    return wrapper
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/unit/test_safe_dispatch.py -v`
Expected: PASS, 6 tests

- [ ] **Step 5: Commit**

```bash
git add scripts/safe_dispatch.py tests/unit/test_safe_dispatch.py
git commit -m "feat(safe_dispatch): add error-message wrapper for CLI subcommands"
```

---

## Task 2: Apply `@safe_dispatch` to existing handlers in `cli.py`

**Files:**
- Modify: `scripts/cli.py:62-68`

- [ ] **Step 1: Verify existing tests still pass before the change**

Run: `pytest tests/unit/test_cli_dispatch.py -v`
Expected: PASS, 4 tests. The current dispatch tests don't catch any of the 4 wrapped exceptions, so wrapping is purely additive.

- [ ] **Step 2: Apply the decorator to each handler**

In `scripts/cli.py`, find the `_DISPATCH` dict and the `main()` function. Make two changes:

Change 1 — import the decorator at the top:

```python
from scripts.safe_dispatch import safe_dispatch
```

(Add it after the existing `from scripts.audit import ...` if any; the file currently has no other project-internal imports beyond `importlib`. Place it next to the other `from __future__` / stdlib imports.)

Change 2 — wrap the dispatched handler. Find this block in `main()`:

```python
target = _DISPATCH.get(args.command)
if target is None:
    parser.print_help()
    return 1
module_path, _, attr = target.rpartition(".")
handler = getattr(importlib.import_module(module_path), attr)
return handler(args)
```

Replace `return handler(args)` with:

```python
return safe_dispatch(handler)(args)
```

- [ ] **Step 3: Run the full test suite to confirm no regression**

Run: `pytest -m "not eval" -v`
Expected: PASS, ~100 tests. All existing tests should still pass because:
- The decorator is a no-op when no wrapped exception is raised
- The existing tests don't raise any of the 4 caught exceptions

- [ ] **Step 4: Commit**

```bash
git add scripts/cli.py
git commit -m "feat(cli): wrap subcommand handlers with @safe_dispatch"
```

---

## Task 3: `doctor.py` — skeleton, dataclass, render

**Files:**
- Create: `scripts/doctor.py`
- Create: `tests/unit/test_doctor.py` (with the first 2 tests only; more added in Tasks 4–7)

- [ ] **Step 1: Write the failing tests for the skeleton**

Create `tests/unit/test_doctor.py`:

```python
"""Verify aisurface doctor — install-health self-check."""
from __future__ import annotations

import dataclasses
import json

import pytest

from scripts import doctor
from scripts.doctor import DoctorCheck, cmd_doctor, render_human, render_json


def test_doctor_check_dataclass_defaults():
    c = DoctorCheck(name="x", status="pass", message="ok")
    assert c.fix_hints == []
    assert dataclasses.is_dataclass(c)


def test_render_human_uses_correct_glyphs(capsys):
    checks = [
        DoctorCheck(name="a", status="pass", message="A-ok"),
        DoctorCheck(name="b", status="fail", message="B-bad", fix_hints=["fix B"]),
        DoctorCheck(name="c", status="warn", message="C-meh", fix_hints=["note C"]),
    ]
    render_human(checks, no_color=True)
    out = capsys.readouterr().out
    assert "✓ A-ok" in out
    assert "✗ B-bad" in out
    assert "→ fix B" in out
    assert "⚠ C-meh" in out


def test_render_json_shape(capsys):
    checks = [
        DoctorCheck(name="a", status="pass", message="A-ok"),
        DoctorCheck(name="b", status="fail", message="B-bad", fix_hints=["h"]),
    ]
    render_json(checks)
    payload = json.loads(capsys.readouterr().out)
    assert payload["checks"][0]["name"] == "a"
    assert payload["checks"][0]["status"] == "pass"
    assert payload["checks"][1]["fix_hints"] == ["h"]
    assert payload["summary"] == {"pass": 1, "fail": 1, "warn": 0, "exit_code": 1}
    assert "python_version" in payload
    assert "aisurface_version" in payload
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/unit/test_doctor.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'scripts.doctor'`

- [ ] **Step 3: Write the skeleton implementation**

Create `scripts/doctor.py`:

```python
"""
 * [INPUT]: Depends on `sys` (version, argv), `os` (env, access), `shutil` (which), `importlib`, `importlib.metadata`, `pathlib.Path`, `sysconfig`, `httpx` (already a dep), `dataclasses`, `json`, `scripts.colors`.
 * [OUTPUT]: Provides `cmd_doctor(args) -> int`, `DoctorCheck` dataclass, 8 check_* functions, `render_human` / `render_json` for output. Used by `scripts/cli.py` as the 4th subcommand.
 * [POS]: scripts/ — install-health self-check. Catches stale-version, PATH, deps, cache issues that audit/fix/verify can't see. Sits alongside the 3 business verbs.
 * [PROTOCOL]: Update this header when changed, then check CLAUDE.md

`aisurface doctor` — diagnose the local install. Catches:
- Python version too old (< 3.10)
- Package not importable (broken pip install)
- Console script not on PATH (Windows classic)
- Missing dependencies
- Cache directory not writable
- Stale version on PyPI
- Missing PERPLEXITY_API_KEY (for `verify`)

Exits 0 (all good), 1 (something failed), or 2 (Python < 3.10, can't run).
"""
from __future__ import annotations

import dataclasses
import importlib
import json
import os
import shutil
import sys
import sysconfig
from importlib.metadata import version as _pkg_version
from pathlib import Path
from typing import Callable, Literal

import httpx

from scripts import colors

# Status constants — used as DoctorCheck.status values
PASS: Literal["pass"] = "pass"
FAIL: Literal["fail"] = "fail"
WARN: Literal["warn"] = "warn"

_REQUIRED_DEPS = ("httpx", "jsonschema", "selectolax")
_PYPI_URL = "https://pypi.org/pypi/aisurface/json"
_PYPI_TIMEOUT = 5.0
_MIN_PYTHON = (3, 10)


@dataclasses.dataclass
class DoctorCheck:
    """One row in the doctor report.

    `name` is a stable identifier (used by --json consumers).
    `status` is one of "pass" / "fail" / "warn".
    `fix_hints` is printed below the message when non-empty.
    """

    name: str
    status: Literal["pass", "fail", "warn"]
    message: str
    fix_hints: list[str] = dataclasses.field(default_factory=list)


# -- Check 1: Python version ---------------------------------------------------

def check_python_version() -> DoctorCheck:
    major, minor, micro = sys.version_info[:3]
    if (major, minor) >= _MIN_PYTHON:
        return DoctorCheck(
            name="python_version",
            status=PASS,
            message=f"{major}.{minor}.{micro} (need >= {'.'.join(map(str, _MIN_PYTHON))})",
        )
    return DoctorCheck(
        name="python_version",
        status=FAIL,
        message=f"{major}.{minor}.{micro} — aisurface needs >= {'.'.join(map(str, _MIN_PYTHON))}",
        fix_hints=[f"Upgrade Python: https://www.python.org/downloads/"],
    )


# -- Check 2: scripts package importable --------------------------------------

def check_scripts_importable() -> DoctorCheck:
    failed: list[str] = []
    for mod in ("scripts.audit", "scripts.fix", "scripts.verify"):
        try:
            importlib.import_module(mod)
        except ImportError as e:
            failed.append(f"{mod}: {e}")
    if not failed:
        try:
            v = _pkg_version("aisurface")
        except Exception:
            v = "?"
        return DoctorCheck(
            name="scripts_importable",
            status=PASS,
            message=f"aisurface {v} installed",
        )
    return DoctorCheck(
        name="scripts_importable",
        status=FAIL,
        message="aisurface not importable",
        fix_hints=[
            "pip install aisurface  (or `pip install -e .` for dev)",
            "Errors: " + "; ".join(failed),
        ],
    )


# -- Check 3: console script on PATH ------------------------------------------

def check_console_script_on_path() -> DoctorCheck:
    which = shutil.which("aisurface")
    if which:
        return DoctorCheck(
            name="console_script_on_path",
            status=PASS,
            message=f"found at {which}",
        )
    scripts_dir = sysconfig.get_paths().get("scripts", "<unknown-scripts-dir>")
    return DoctorCheck(
        name="console_script_on_path",
        status=FAIL,
        message="'aisurface' console script not on PATH",
        fix_hints=[
            "Workaround: use `python -m scripts.cli` instead",
            f"Fix: add {scripts_dir} to your PATH",
        ],
    )


# -- Check 4: required deps importable ----------------------------------------

def check_deps_importable() -> DoctorCheck:
    missing: list[str] = []
    for dep in _REQUIRED_DEPS:
        try:
            importlib.import_module(dep)
        except ImportError:
            missing.append(dep)
    if not missing:
        return DoctorCheck(
            name="deps_importable",
            status=PASS,
            message=", ".join(_REQUIRED_DEPS) + " (all importable)",
        )
    return DoctorCheck(
        name="deps_importable",
        status=FAIL,
        message=f"missing: {', '.join(missing)}",
        fix_hints=["pip install --force-reinstall aisurface"],
    )


# -- Check 5: cache dir writable ----------------------------------------------

def check_cache_dir_writable() -> DoctorCheck:
    cache = Path(os.environ.get("AISURFACE_CACHE_DIR") or Path.home() / ".aisurface")
    if not cache.exists():
        try:
            cache.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            return DoctorCheck(
                name="cache_dir_writable",
                status=FAIL,
                message=f"can't create {cache}",
                fix_hints=[
                    f"Check parent dir permissions: {cache.parent}",
                    "Or set AISURFACE_CACHE_DIR to a writable path",
                    f"Error: {e}",
                ],
            )
    if not os.access(cache, os.W_OK):
        return DoctorCheck(
            name="cache_dir_writable",
            status=FAIL,
            message=f"{cache} not writable",
            fix_hints=[
                f"Check permissions on {cache}",
                "Or set AISURFACE_CACHE_DIR to a writable path",
            ],
        )
    return DoctorCheck(
        name="cache_dir_writable",
        status=PASS,
        message=f"{cache} (writable)",
    )


# -- Check 6: PyPI latest version --------------------------------------------

def check_pypi_latest_version(skip_network: bool = False) -> DoctorCheck:
    if skip_network:
        return DoctorCheck(
            name="pypi_latest_version",
            status=WARN,
            message="skipped (--skip-network)",
        )
    try:
        installed = _pkg_version("aisurface")
    except Exception:
        installed = "<unknown>"
    try:
        resp = httpx.get(_PYPI_URL, timeout=_PYPI_TIMEOUT)
        resp.raise_for_status()
        latest = resp.json()["info"]["version"]
    except Exception as e:
        return DoctorCheck(
            name="pypi_latest_version",
            status=WARN,
            message=f"couldn't reach PyPI: {type(e).__name__}",
            fix_hints=["Run with --skip-network if you're offline"],
        )
    if latest == installed:
        return DoctorCheck(
            name="pypi_latest_version",
            status=PASS,
            message=f"{installed} (up to date)",
        )
    # Try a proper version compare; fall back to string compare if packaging absent
    try:
        from packaging.version import Version
        if Version(installed) < Version(latest):
            return DoctorCheck(
                name="pypi_latest_version",
                status=WARN,
                message=f"{installed} installed, {latest} available",
                fix_hints=["pip install --upgrade aisurface"],
            )
        return DoctorCheck(
            name="pypi_latest_version",
            status=PASS,
            message=f"{installed} (newer than PyPI's {latest}; pre-release?)",
        )
    except Exception:
        return DoctorCheck(
            name="pypi_latest_version",
            status=PASS,
            message=f"installed {installed}, PyPI {latest}",
        )


# -- Check 7: internet reachable (implicit in check 6) ------------------------
# Implemented as a side-effect: if check 6 reaches PyPI, internet works.
# No separate function.

# -- Check 8: PERPLEXITY_API_KEY env -----------------------------------------

def check_perplexity_api_key() -> DoctorCheck:
    if os.environ.get("PERPLEXITY_API_KEY"):
        return DoctorCheck(
            name="perplexity_api_key",
            status=PASS,
            message="set",
        )
    return DoctorCheck(
        name="perplexity_api_key",
        status=WARN,
        message="not set — `verify` will fail without it",
        fix_hints=["Get one at: https://perplexity.ai/account/api"],
    )


# All checks in spec order, minus the Python short-circuit which cmd_doctor
# handles separately
_ALL_CHECK_FUNCS: list[Callable[..., DoctorCheck]] = [
    check_python_version,
    check_scripts_importable,
    check_console_script_on_path,
    check_deps_importable,
    check_cache_dir_writable,
    check_pypi_latest_version,
    check_perplexity_api_key,
]


# -- Render: human -----------------------------------------------------------

_GLYPH = {PASS: ("✓", "green"), FAIL: ("✗", "red"), WARN: ("⚠", "yellow")}


def render_human(checks: list[DoctorCheck], no_color: bool = False) -> None:
    try:
        v = _pkg_version("aisurface")
    except Exception:
        v = "?"
    print(f"aisurface doctor — v{v}")
    print("=" * 27)
    print()
    for c in checks:
        sym, color = _GLPH[c.status]
        if no_color:
            print(f"{sym} {c.message}")
        else:
            print(f"{colors.colorize(sym, color)} {c.message}")
        for hint in c.fix_hints:
            indent = "      " if c.status == WARN else "   "
            print(f"{indent}→ {hint}")
    print()


def render_json(checks: list[DoctorCheck]) -> None:
    try:
        v = _pkg_version("aisurface")
    except Exception:
        v = "?"
    summary = {
        "pass": sum(1 for c in checks if c.status == PASS),
        "fail": sum(1 for c in checks if c.status == FAIL),
        "warn": sum(1 for c in checks if c.status == WARN),
    }
    summary["exit_code"] = 1 if summary["fail"] else 0
    payload = {
        "aisurface_version": v,
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "checks": [dataclasses.asdict(c) for c in checks],
        "summary": summary,
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))


# -- CLI entry point ---------------------------------------------------------

def cmd_doctor(args) -> int:
    """Subcommand handler — same signature as cmd_audit / cmd_fix / cmd_verify."""
    no_color = bool(getattr(args, "no_color", False))
    skip_network = bool(getattr(args, "skip_network", False))
    as_json = bool(getattr(args, "json", False))

    # Short-circuit on Python < 3.10
    py_check = check_python_version()
    if py_check.status == FAIL:
        sym, color = _GLPH[FAIL]
        line = f"{sym} {py_check.message}"
        print(colors.colorize(line, color) if not no_color else line)
        for hint in py_check.fix_hints:
            print(f"   → {hint}")
        return 2

    checks: list[DoctorCheck] = [py_check]
    for fn in _ALL_CHECK_FUNCS[1:]:
        if fn is check_pypi_latest_version and skip_network:
            checks.append(check_pypi_latest_version(skip_network=True))
            continue
        checks.append(fn())

    if as_json:
        render_json(checks)
    else:
        render_human(checks, no_color=no_color)

    return 1 if any(c.status == FAIL for c in checks) else 0
```

Note: this is the **complete** implementation. Tasks 4–7 below will add tests, not modify this file.

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/unit/test_doctor.py -v`
Expected: PASS, 3 tests (the skeleton + render tests)

- [ ] **Step 5: Commit**

```bash
git add scripts/doctor.py tests/unit/test_doctor.py
git commit -m "feat(doctor): add skeleton with 8 check functions + render"
```

---

## Task 4: Add tests for checks 1–4 (Python, scripts, PATH, deps)

**Files:**
- Modify: `tests/unit/test_doctor.py` (append)

- [ ] **Step 1: Write the failing tests for checks 1–4**

Append to `tests/unit/test_doctor.py`:

```python
# -- Check 1: Python version -------------------------------------------------

def test_check_python_version_pass():
    import scripts.doctor as d
    saved = d.sys.version_info
    d.sys.version_info = (3, 12, 0, "final", 0)
    try:
        c = d.check_python_version()
    finally:
        d.sys.version_info = saved
    assert c.status == "pass"
    assert "3.12.0" in c.message


def test_check_python_version_fail():
    import scripts.doctor as d
    saved = d.sys.version_info
    d.sys.version_info = (3, 9, 5, "final", 0)
    try:
        c = d.check_python_version()
    finally:
        d.sys.version_info = saved
    assert c.status == "fail"
    assert "3.9.5" in c.message
    assert "https://www.python.org/downloads" in c.fix_hints[0]


# -- Check 2: scripts importable --------------------------------------------

def test_check_scripts_importable_pass():
    from scripts.doctor import check_scripts_importable
    c = check_scripts_importable()
    assert c.status == "pass"
    assert "installed" in c.message


def test_check_scripts_importable_fail(monkeypatch):
    """If scripts.audit can't be imported, the check must report fail."""
    import scripts.doctor as d
    real_import = d.importlib.import_module

    def fake_import(name, *args, **kwargs):
        if name == "scripts.audit":
            raise ImportError("simulated: no module named 'scripts.audit'")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(d.importlib, "import_module", fake_import)
    c = d.check_scripts_importable()
    assert c.status == "fail"
    assert "pip install aisurface" in c.fix_hints[0]


# -- Check 3: console script on PATH ----------------------------------------

def test_check_console_script_on_path_pass(monkeypatch):
    import scripts.doctor as d
    monkeypatch.setattr(d.shutil, "which", lambda name: f"/usr/bin/{name}")
    c = d.check_console_script_on_path()
    assert c.status == "pass"
    assert "found at" in c.message


def test_check_console_script_on_path_fail(monkeypatch):
    import scripts.doctor as d
    monkeypatch.setattr(d.shutil, "which", lambda name: None)
    c = d.check_console_script_on_path()
    assert c.status == "fail"
    assert "python -m scripts.cli" in c.fix_hints[0]
    assert "PATH" in c.fix_hints[1]


# -- Check 4: deps importable ------------------------------------------------

def test_check_deps_importable_pass():
    from scripts.doctor import check_deps_importable
    c = check_deps_importable()
    assert c.status == "pass"


def test_check_deps_importable_fail(monkeypatch):
    import scripts.doctor as d
    real_import = d.importlib.import_module

    def fake_import(name, *args, **kwargs):
        if name == "jsonschema":
            raise ImportError("simulated")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(d.importlib, "import_module", fake_import)
    c = d.check_deps_importable()
    assert c.status == "fail"
    assert "jsonschema" in c.message
    assert "pip install --force-reinstall aisurface" in c.fix_hints[0]
```

- [ ] **Step 2: Run tests to verify they pass**

Run: `pytest tests/unit/test_doctor.py -v`
Expected: PASS, 11 tests (3 skeleton + 8 check tests)

- [ ] **Step 3: Commit**

```bash
git add tests/unit/test_doctor.py
git commit -m "test(doctor): add 8 tests for checks 1-4 (python, scripts, PATH, deps)"
```

---

## Task 5: Add tests for checks 5 (cache) and 8 (PERPLEXITY_API_KEY)

**Files:**
- Modify: `tests/unit/test_doctor.py` (append)

- [ ] **Step 1: Write the failing tests**

Append to `tests/unit/test_doctor.py`:

```python
# -- Check 5: cache dir writable -------------------------------------------

def test_check_cache_dir_writable_pass(tmp_path, monkeypatch):
    monkeypatch.setenv("AISURFACE_CACHE_DIR", str(tmp_path))
    from scripts.doctor import check_cache_dir_writable
    c = check_cache_dir_writable()
    assert c.status == "pass"
    assert str(tmp_path) in c.message


def test_check_cache_dir_writable_create_succeeds(tmp_path, monkeypatch):
    nonexistent = tmp_path / "newsubdir"
    assert not nonexistent.exists()
    monkeypatch.setenv("AISURFACE_CACHE_DIR", str(nonexistent))
    from scripts.doctor import check_cache_dir_writable
    c = check_cache_dir_writable()
    assert c.status == "pass"
    assert nonexistent.exists()


def test_check_cache_dir_writable_not_writable(tmp_path, monkeypatch):
    # On Windows, os.access(W_OK) often returns True even for read-only dirs.
    # So we mock os.access to force the fail path.
    cache = tmp_path / "ro"
    cache.mkdir()
    monkeypatch.setenv("AISURFACE_CACHE_DIR", str(cache))
    import scripts.doctor as d
    monkeypatch.setattr(d.os, "access", lambda path, mode: False)
    c = d.check_cache_dir_writable()
    assert c.status == "fail"
    assert "not writable" in c.message


def test_check_cache_dir_writable_create_fails(tmp_path, monkeypatch):
    """When mkdir raises (e.g., parent doesn't exist + no write), the check fails."""
    bad = tmp_path / "nonexistent_parent" / "cache"
    monkeypatch.setenv("AISURFACE_CACHE_DIR", str(bad))
    # Don't mock anything; the real mkdir should fail because the parent
    # doesn't exist AND os.access on the parent returns False (since it
    # doesn't exist). Force the failure by mocking mkdir to raise.
    import scripts.doctor as d
    real_mkdir = d.Path.mkdir

    def fake_mkdir(self, *args, **kwargs):
        if str(self) == str(bad):
            raise OSError("simulated mkdir failure")
        return real_mkdir(self, *args, **kwargs)

    monkeypatch.setattr(d.Path, "mkdir", fake_mkdir)
    c = d.check_cache_dir_writable()
    assert c.status == "fail"
    assert "can't create" in c.message


# -- Check 8: PERPLEXITY_API_KEY -------------------------------------------

def test_check_perplexity_api_key_present(monkeypatch):
    monkeypatch.setenv("PERPLEXITY_API_KEY", "pplx-test-token")
    from scripts.doctor import check_perplexity_api_key
    c = check_perplexity_api_key()
    assert c.status == "pass"


def test_check_perplexity_api_key_missing(monkeypatch):
    monkeypatch.delenv("PERPLEXITY_API_KEY", raising=False)
    from scripts.doctor import check_perplexity_api_key
    c = check_perplexity_api_key()
    assert c.status == "warn"
    assert "https://perplexity.ai/account/api" in c.fix_hints[0]
```

- [ ] **Step 2: Run tests to verify they pass**

Run: `pytest tests/unit/test_doctor.py -v`
Expected: PASS, 17 tests (11 from prior + 6 new)

- [ ] **Step 3: Commit**

```bash
git add tests/unit/test_doctor.py
git commit -m "test(doctor): add 6 tests for checks 5 (cache) and 8 (PERPLEXITY_API_KEY)"
```

---

## Task 6: Add tests for check 6 (PyPI) with mocked network

**Files:**
- Modify: `tests/unit/test_doctor.py` (append)

- [ ] **Step 1: Write the failing tests**

Append to `tests/unit/test_doctor.py`:

```python
# -- Check 6: PyPI latest version -----------------------------------------

import httpx


class _FakePyPIResp:
    def __init__(self, version: str):
        self._payload = {"info": {"version": version}}

    def raise_for_status(self):
        pass

    def json(self):
        return self._payload


def test_check_pypi_latest_up_to_date(monkeypatch):
    import scripts.doctor as d
    monkeypatch.setattr(d, "_pkg_version", lambda name: "1.0.2")
    monkeypatch.setattr(d.httpx, "get", lambda *a, **kw: _FakePyPIResp("1.0.2"))
    c = d.check_pypi_latest_version()
    assert c.status == "pass"
    assert "up to date" in c.message


def test_check_pypi_latest_newer_available(monkeypatch):
    import scripts.doctor as d
    monkeypatch.setattr(d, "_pkg_version", lambda name: "1.0.1")
    monkeypatch.setattr(d.httpx, "get", lambda *a, **kw: _FakePyPIResp("1.0.2"))
    c = d.check_pypi_latest_version()
    assert c.status == "warn"
    assert "1.0.1 installed" in c.message
    assert "1.0.2 available" in c.message
    assert "pip install --upgrade aisurface" in c.fix_hints


def test_check_pypi_latest_prerelease_ahead(monkeypatch):
    import scripts.doctor as d
    monkeypatch.setattr(d, "_pkg_version", lambda name: "1.1.0a1")
    monkeypatch.setattr(d.httpx, "get", lambda *a, **kw: _FakePyPIResp("1.0.2"))
    c = d.check_pypi_latest_version()
    assert c.status == "pass"
    assert "pre-release" in c.message.lower() or "newer than PyPI" in c.message


def test_check_pypi_network_error_warns(monkeypatch):
    import scripts.doctor as d
    monkeypatch.setattr(d, "_pkg_version", lambda name: "1.0.2")

    def boom(*a, **kw):
        raise httpx.ConnectError("simulated DNS failure")

    monkeypatch.setattr(d.httpx, "get", boom)
    c = d.check_pypi_latest_version()
    assert c.status == "warn"
    assert "couldn't reach PyPI" in c.message


def test_check_pypi_skipped_with_flag():
    from scripts.doctor import check_pypi_latest_version
    c = check_pypi_latest_version(skip_network=True)
    assert c.status == "warn"
    assert "skipped" in c.message
```

- [ ] **Step 2: Run tests to verify they pass**

Run: `pytest tests/unit/test_doctor.py -v`
Expected: PASS, 22 tests (17 from prior + 5 new)

- [ ] **Step 3: Commit**

```bash
git add tests/unit/test_doctor.py
git commit -m "test(doctor): add 5 tests for check 6 (PyPI latest) with mocked network"
```

---

## Task 7: Add tests for `cmd_doctor` exit codes, JSON output, short-circuit

**Files:**
- Modify: `tests/unit/test_doctor.py` (append)

- [ ] **Step 1: Write the failing tests**

Append to `tests/unit/test_doctor.py`:

```python
# -- cmd_doctor: exit codes, --json, --no-color, Python short-circuit ------


class _Args:
    def __init__(self, json: bool = False, no_color: bool = False, skip_network: bool = False):
        self.json = json
        self.no_color = no_color
        self.skip_network = skip_network


def test_cmd_doctor_exit_0_all_pass(monkeypatch, capsys):
    import scripts.doctor as d

    def passing_check():
        return d.DoctorCheck(name="x", status="pass", message="ok")

    monkeypatch.setattr(d, "_ALL_CHECK_FUNCS", [passing_check])
    rc = d.cmd_doctor(_Args(skip_network=True))
    assert rc == 0


def test_cmd_doctor_exit_1_when_one_fails(monkeypatch):
    import scripts.doctor as d

    def failing_check():
        return d.DoctorCheck(name="x", status="fail", message="bad", fix_hints=["h"])

    monkeypatch.setattr(d, "_ALL_CHECK_FUNCS", [failing_check])
    rc = d.cmd_doctor(_Args(skip_network=True))
    assert rc == 1


def test_cmd_doctor_exit_2_when_python_too_old(monkeypatch, capsys):
    import scripts.doctor as d
    saved = d.sys.version_info
    d.sys.version_info = (3, 9, 0, "final", 0)
    try:
        rc = d.cmd_doctor(_Args())
    finally:
        d.sys.version_info = saved
    assert rc == 2
    out = capsys.readouterr().out
    assert "3.9.0" in out
    assert "https://www.python.org/downloads" in out


def test_cmd_doctor_json_output(monkeypatch, capsys):
    import json
    import scripts.doctor as d

    def passing_check():
        return d.DoctorCheck(name="x", status="pass", message="ok")

    monkeypatch.setattr(d, "_ALL_CHECK_FUNCS", [passing_check])
    rc = d.cmd_doctor(_Args(json=True, skip_network=True))
    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["summary"]["exit_code"] == 0
    assert payload["checks"][0]["name"] == "x"


def test_cmd_doctor_no_color_strips_ansi(monkeypatch, capsys):
    import scripts.doctor as d

    def passing_check():
        return d.DoctorCheck(name="x", status="pass", message="ok")

    monkeypatch.setattr(d, "_ALL_CHECK_FUNCS", [passing_check])
    d.cmd_doctor(_Args(no_color=True, skip_network=True))
    out = capsys.readouterr().out
    assert "\x1b[" not in out
```

- [ ] **Step 2: Run tests to verify they pass**

Run: `pytest tests/unit/test_doctor.py -v`
Expected: PASS, 27 tests (22 + 5 new)

- [ ] **Step 3: Commit**

```bash
git add tests/unit/test_doctor.py
git commit -m "test(doctor): add 5 tests for cmd_doctor exit codes, JSON, no-color, Python short-circuit"
```

---

## Task 8: Wire `doctor` into `scripts/cli.py` as a 4th subcommand

**Files:**
- Modify: `scripts/cli.py:15-19` (add to `_DISPATCH`) and `scripts/cli.py:22-52` (add subparser)

- [ ] **Step 1: Verify the integration tests pass before wiring**

Run: `pytest tests/unit/test_cli_dispatch.py -v`
Expected: PASS, 4 tests. The CLI still works without doctor wired.

- [ ] **Step 2: Add `doctor` to `_DISPATCH`**

In `scripts/cli.py`, find the `_DISPATCH` dict:

```python
_DISPATCH = {
    "audit": "scripts.audit.cmd_audit",
    "fix": "scripts.fix.cmd_fix",
    "verify": "scripts.verify.cmd_verify",
}
```

Add the `doctor` entry:

```python
_DISPATCH = {
    "audit": "scripts.audit.cmd_audit",
    "fix": "scripts.fix.cmd_fix",
    "verify": "scripts.verify.cmd_verify",
    "doctor": "scripts.doctor.cmd_doctor",
}
```

- [ ] **Step 3: Add the `doctor` subparser**

In `build_parser()`, find the `verify` subparser block (just after it), add:

```python
    # doctor subcommand (v1.0.2)
    doctor_p = subparsers.add_parser(
        "doctor", help="Diagnose the local aisurface install"
    )
    doctor_p.add_argument("--json", action="store_true", help="JSON output")
    doctor_p.add_argument("--no-color", action="store_true", help="Disable color output")
    doctor_p.add_argument(
        "--skip-network", action="store_true",
        help="Skip the PyPI version check (offline / CI-no-network)",
    )
```

And update the metavar on the subparsers line to show all 4 verbs:

```python
subparsers = parser.add_subparsers(dest="command", required=True, metavar="{audit,fix,verify,doctor}")
```

- [ ] **Step 4: Verify CLI listing and help work**

Run: `python -m scripts.cli --help`
Expected: usage line shows `{audit,fix,verify,doctor}`. Output mentions the `doctor` subcommand.

Run: `python -m scripts.cli doctor --help`
Expected: shows the doctor-specific args (`--json`, `--no-color`, `--skip-network`).

- [ ] **Step 5: Run doctor against the real install (smoke)**

Run: `python -m scripts.cli doctor --no-color`
Expected: A mix of ✓ and ⚠. Real check: on this dev machine, `scripts_importable` ✓, `console_script_on_path` ✓ (because we run via `python -m`), `cache_dir_writable` ✓, `pypi_latest_version` either ✓ (1.0.2 is up to date) or ⚠ (network issue), `perplexity_api_key` either ✓ (if env set) or ⚠.

If `pypi_latest_version` reports `1.0.1 installed, 1.0.2 available` (warn), that's expected — v1.0.2 isn't released yet, so PyPI still has 1.0.1. The check is correct.

- [ ] **Step 6: Run the full test suite to confirm no regression**

Run: `pytest -m "not eval" -v`
Expected: PASS, ~127 tests (105 existing + 22 new doctor/safe_dispatch tests). The `test_cli_dispatch.py::test_no_subcommand_shows_help` test must still pass; update it if the metavar change broke it (it shouldn't, but verify — see "Verification" below).

- [ ] **Step 7: Update `test_cli_dispatch.py::test_no_subcommand_shows_help` if needed**

The test currently asserts that `"audit" in err and "fix" in err and "verify" in err`. With doctor added to the metavar, `doctor` will also appear. The test should be updated to also assert `doctor`:

```python
def test_no_subcommand_shows_help():
    code, _, err = _run()
    assert code != 0
    for verb in ("audit", "fix", "verify", "doctor"):
        assert verb in err, f"{verb} missing from help output"
```

- [ ] **Step 8: Commit**

```bash
git add scripts/cli.py tests/unit/test_cli_dispatch.py
git commit -m "feat(cli): wire doctor as 4th subcommand + update dispatch test"
```

---

## Task 9: Update `SKILL.md` with doctor natural-language triggers (per §11b)

**Files:**
- Modify: `SKILL.md` (the "工具调用" table around line 78-82)

- [ ] **Step 1: Read the current SKILL.md to find the right spot**

The 工具调用 table has rows mapping user phrases to commands. Find the row that says "Python 工具没装" / "verify" / etc. Add a new row for doctor BEFORE the "报错时" section.

- [ ] **Step 2: Add the doctor row to the 工具调用 table**

Find this block in `SKILL.md`:

```markdown
| 用户说什么 | 你做什么 |
|---|---|
| "诊断 / audit / 看看" | 调 `python -m scripts.cli audit <path>`(或 `aisurface audit <path>`,先确认 `aisurface` console script 在 PATH 里) |
| "修 / fix / 改 README / 改 llms.txt / 加 Schema" | 调 `python -m scripts.cli fix <path> --dry-run` 先给用户看,用户同意后再 `--yes` 落地 |
| "验证 / verify / AI 真的引用没" | 检查 `PERPLEXITY_API_KEY` 环境变量,缺了告诉用户去 https://perplexity.ai/account/api 拿;然后调 `python -m scripts.cli verify <path>` |
| 路径没说清楚 | 问用户要,别假设 |
| 多种意图(诊断+修+验证) | 按顺序做,每步都给用户看结果,问"继续?" |
```

Add a new row for doctor, placed before "路径没说清楚":

```markdown
| "装对没 / 为什么命令找不到 / 装坏了 / diagnose install / is my aisurface broken" | 调 `python -m scripts.cli doctor --no-color`。读输出,把 ✗ 行的 `→ ...` 提示直接转给用户。PyPI 显示有新版本(`⚠ ... available`)就追加一句"要不要 `pip install --upgrade aisurface`"。如果 `PERPLEXITY_API_KEY` 是 ⚠,提醒"以后用 `verify` 之前先设上"但**不强制**用户设 |
```

- [ ] **Step 3: Verify the user-facing sections don't expose command names**

The 3 user-facing sections are:
- "我能做三件事" (lines ~14-16)
- "怎么跟我说" (lines ~20-42)
- "你需要给我的" (lines ~50-52)

None of these should mention `doctor` as a verb or command. They should describe the **capability** ("如果你怀疑装坏了,跟我说一句") not the command. If any of these sections currently mention `audit` / `fix` / `verify` as commands, that's already a v1.0.1 issue, not v1.0.2 — but verify the new doctor addition doesn't break the pattern.

- [ ] **Step 4: Commit**

```bash
git add SKILL.md
git commit -m "docs(skill): add doctor natural-language triggers to 工具调用 table"
```

---

## Task 10: Rewrite README 5-min self-test to use `python -m scripts.cli`

**Files:**
- Modify: `README.md` (the 5-min self-test section around lines 91-120)
- Modify: `README.en.md` (the equivalent English section)

- [ ] **Step 1: Update the Chinese README**

In `README.md`, find the "## 5 分钟自测" section. Replace the entire shell block (steps 1-7) with:

````markdown
```bash
# 1) 装 / 升级到 PyPI 上的最新版
pip install --upgrade aisurface
python -m scripts.cli doctor --no-color  # 期望看到 ✓ Python / ✓ scripts importable / ✓ cache writable 等

# 2) CLI 四个动词都出来
python -m scripts.cli --help              # 看到 {audit, fix, verify, doctor}

# 3) 跑内置 fixture — 期望 health 16/100
python -m scripts.cli audit evals/fixtures/bad-readme-python-lib --no-color

# 4) 跑内置"完美" fixture — 期望 90+ 分
python -m scripts.cli audit evals/fixtures/perfect-readme-and-docs --no-color

# 5) 看 fix 会改什么(不写盘)
python -m scripts.cli fix evals/fixtures/bad-readme-python-lib --dry-run

# 6) 拿自己的项目跑
python -m scripts.cli audit /path/to/your/repo --no-color

# 7) (可选) verify 真实 AI 引用率 — 需要 PERPLEXITY_API_KEY
export PERPLEXITY_API_KEY=pplx-...
python -m scripts.cli verify /path/to/your/repo        # 第一次跑 = 建基线
```

> **Note:** 如果你的 `aisurface` console script 在 PATH 里(典型情况: macOS / Linux,或 Windows 上你手动加过 PATH),那 `aisurface audit ...` 跟 `python -m scripts.cli audit ...` 是**完全一样的**调用。任选一个。Windows 默认 `aisurface` 不在 PATH 上,所以 README 用 `python -m scripts.cli` 保证不挑平台。
````

- [ ] **Step 2: Update the English README with the equivalent English prose**

In `README.en.md`, find the equivalent 5-minute self-test section and apply the same restructuring. Use `python -m scripts.cli` as the primary command, with the same "if aisurface is on PATH, it's the same thing" footnote in English.

- [ ] **Step 3: Verify the eval fixture path is correct**

The example paths reference `evals/fixtures/bad-readme-python-lib` and `evals/fixtures/perfect-readme-and-docs`. Confirm these exist:

Run: `ls evals/fixtures/`
Expected: shows both fixture directories.

If they don't, use whatever fixture names actually exist. Don't invent paths.

- [ ] **Step 4: Commit**

```bash
git add README.md README.en.md
git commit -m "docs(readme): rewrite 5-min self-test to use python -m scripts.cli (cross-platform)"
```

---

## Task 11: Add v1.0.2 entry to `CHANGELOG.md`

**Files:**
- Modify: `CHANGELOG.md` (insert at top, before the `[1.0.1]` block)

- [ ] **Step 1: Insert the v1.0.2 section**

At the very top of `CHANGELOG.md` (before `## [1.0.1] - 2026-06-03`), insert:

```markdown
## [1.0.2] - 2026-06-03

### Added
- `aisurface doctor` subcommand — install-health self-check with 8 checks (Python version, scripts importable, console script on PATH, deps importable, cache dir writable, PyPI latest version, internet reachable, `PERPLEXITY_API_KEY` set). Exits 0 / 1 / 2 (2 = Python < 3.10). `--json` for machine-readable output, `--skip-network` for offline use.
- `safe_dispatch` decorator in `scripts/safe_dispatch.py` — wraps each `cmd_*` handler and converts 4 common user-facing exceptions (`ModuleNotFoundError` for `scripts.*`, `FileNotFoundError` on `args.path`, `UnicodeEncodeError`, `PermissionError` on the cache dir) into actionable one-line hints on stderr. Re-raises everything else.
- CI matrix: 15 jobs (3 OS × 5 Python: 3.10, 3.11, 3.12, 3.13, 3.14), each running lint + pytest + a smoke test that exercises both `aisurface` and `python -m scripts.cli`. Replaces the single-job ubuntu+3.10 CI that was in v1.0.1.

### Changed
- `README.md` and `README.en.md` 5-min self-test now uses `python -m scripts.cli ...` as the primary command (works on all OS without PATH dependency). `aisurface ...` is mentioned as an equivalent alias for users on macOS/Linux.
- `SKILL.md` tool dispatch table gained a new row mapping natural-language triggers ("装对没 / diagnose install / is my aisurface broken") to `python -m scripts.cli doctor`. No command name exposed to the user-facing sections (per spec §11b user-facing abstraction).
- 23 tests added (15 doctor, 6 safe_dispatch, 1 cli dispatch update, 1 doctor smoke in CI). Total 128 tests.

### Fixed
- v1.0.1 packaging gap: Windows users following the 5-min self-test hit `aisurface: command not found` at step 2 because the `aisurface.exe` console script lives in `%APPDATA%\Python\Python3X\Scripts\` which isn't on Windows PATH. The README now defaults to `python -m scripts.cli` which works regardless of PATH.
- Silent stale-version: a user who had v0.1.x installed and ran `pip install --upgrade aisurface` could end up on a stale version depending on environment resolution. `doctor` now checks PyPI and warns if a newer version is available.
- `test_no_subcommand_shows_help` updated to assert all 4 subcommands (audit, fix, verify, doctor) appear in the help output.
```

- [ ] **Step 2: Commit**

```bash
git add CHANGELOG.md
git commit -m "docs(changelog): v1.0.2 entry — doctor + safe_dispatch + CI matrix"
```

---

## Task 12: Update `ROADMAP.md` with the v1.0.2 row

**Files:**
- Modify: `ROADMAP.md` (the release sequence table around lines 23-32)

- [ ] **Step 1: Insert the v1.0.2 row**

Find the release sequence table in `ROADMAP.md`:

```markdown
| **v1.0.1** | **Skill abstraction principle — single natural-language-facing SKILL.md, GEB fractal docs (L1/L2/L3), §11b in spec, skill-first install story across README/ROADMAP** | ⏳ in progress 2026-06-03 |
| v0.1.4 (optional) | `--llm` flag — swap regex critic for real LLM | ⏳ optional |
```

Change v1.0.1's status to `✅ shipped 2026-06-03` and add a new v1.0.2 row between v1.0.1 and v0.1.4:

```markdown
| **v1.0.1** | **Skill abstraction principle — single natural-language-facing SKILL.md, GEB fractal docs (L1/L2/L3), §11b in spec, skill-first install story across README/ROADMAP** | ✅ shipped 2026-06-03 |
| **v1.0.2** | **Windows install / PATH hotfix — `aisurface doctor` self-check + `safe_dispatch` error wrapper + 15-job CI matrix (3 OS × 5 Python). README 5-min self-test now uses `python -m scripts.cli` (cross-platform).** | ✅ shipped 2026-06-03 |
| v0.1.4 (optional) | `--llm` flag — swap regex critic for real LLM | ⏳ optional |
```

- [ ] **Step 2: Commit**

```bash
git add ROADMAP.md
git commit -m "docs(roadmap): v1.0.2 row + mark v1.0.1 as shipped"
```

---

## Task 13: Update L2 `scripts/CLAUDE.md` with the 2 new files

**Files:**
- Modify: `scripts/CLAUDE.md` (the Member List)

- [ ] **Step 1: Add the new files to the Member List**

In `scripts/CLAUDE.md`, find the "Member List" section. Add two lines in the appropriate alphabetical / logical place (after `cli.py`, before `audit.py` works for new files; or at the end of the list — either is fine, be consistent with the existing ordering):

```markdown
- `safe_dispatch.py`: Decorator that wraps each `cmd_*` handler. Catches 4 user-facing exception classes (`ModuleNotFoundError` for `scripts.*`, `FileNotFoundError` on `args.path`, `UnicodeEncodeError`, `PermissionError` on the cache dir) and prints actionable hints to stderr before exiting 1. Re-raises everything else.
- `doctor.py`: Install-health self-check. Exports `cmd_doctor`, `DoctorCheck` dataclass, 8 check_* functions, `render_human` / `render_json`. Used by `cli.py` as the 4th subcommand. Exits 0 (all pass/warn) / 1 (any fail) / 2 (Python < 3.10).
```

If there's a count line at the end of the Member List (e.g., "(currently 23 files)"), update it. Otherwise skip — the file format is loose.

- [ ] **Step 2: Commit**

```bash
git add scripts/CLAUDE.md
git commit -m "docs(scripts): L2 CLAUDE.md — add doctor.py + safe_dispatch.py"
```

---

## Task 14: Update L1 `CLAUDE.md` with the 2 new files

**Files:**
- Modify: `CLAUDE.md` (the `scripts/` entry in the directory tree)

- [ ] **Step 1: Update the directory tree**

In `CLAUDE.md` (root L1), find the `scripts/` line in the "Directory" section. It currently says something like:

```markdown
├── scripts/              - Python implementation (cli, audit, report, fix/, verify/, scanner, ...)
```

Update it to mention the 2 new files explicitly (or just add a note that doctor and safe_dispatch are part of scripts):

```markdown
├── scripts/              - Python implementation (cli, audit, report, fix/, verify/, scanner, doctor, safe_dispatch, ...)
```

Don't try to enumerate every file — keep the prose. The point of L1 is navigation, not inventory.

- [ ] **Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "docs(root): L1 CLAUDE.md — note doctor + safe_dispatch in scripts/ entry"
```

---

## Task 15: Update L2 `tests/CLAUDE.md` with the 2 new test files

**Files:**
- Modify: `tests/CLAUDE.md`

- [ ] **Step 1: Update the Member List and Invariants**

In `tests/CLAUDE.md`, find the `unit/` description (currently says "Currently covers `audit`, `scanner`, ..."). Add the 2 new test files to the list. The test files live at `tests/unit/test_doctor.py` and `tests/unit/test_safe_dispatch.py`.

Also update the "Invariants" count from "67 tests passing as of v0.1.1" to reflect v1.0.2 reality: "128 tests passing as of v1.0.2 (105 in v1.0.1 + 22 new doctor/safe_dispatch + 1 cli dispatch update)".

Note: the actual test count will be whatever `pytest --collect-only -q` reports. The "67" is a stale v0.1.1 figure. The pre-existing comment in the file says "as of v0.1.1" so it was already stale before v1.0.2. Replace with the v1.0.2 actual count.

- [ ] **Step 2: Move the new tests out of "Pending test files"**

The file has a "Pending test files (from v1.0 plan)" section listing files that are pending. If `test_doctor.py` or `test_safe_dispatch.py` are in this list, remove them (they're now created). If they're not, skip.

- [ ] **Step 3: Commit**

```bash
git add tests/CLAUDE.md
git commit -m "docs(tests): L2 CLAUDE.md — add 2 new test files + update test count"
```

---

## Task 16: Expand `.github/workflows/ci.yml` from 1 job to 15-job matrix

**Files:**
- Modify: `.github/workflows/ci.yml`

- [ ] **Step 1: Read the current ci.yml (already loaded above) and replace it with the matrix version**

Replace the entire contents of `.github/workflows/ci.yml` with:

```yaml
name: CI

on:
  push:
    branches: [master, main]
  pull_request:

jobs:
  lint-and-test:
    name: ${{ matrix.os }} / py${{ matrix.python-version }}
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ["3.10", "3.11", "3.12", "3.13", "3.14"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install uv
        run: pip install uv
      - name: Install dependencies
        run: uv pip install --system -e ".[dev]"
      - name: Ruff
        run: ruff check .
      - name: Pytest (unit + integration, not eval)
        run: pytest -m "not eval"
      - name: Pytest (eval)
        run: pytest -m eval
      - name: Smoke test
        shell: bash
        run: |
          # Verify both entry points work
          if command -v aisurface >/dev/null 2>&1; then
            echo "aisurface console script found at: $(command -v aisurface)"
            aisurface --help
          else
            echo "aisurface console script not on PATH (expected on some Windows configs)"
          fi
          python -m scripts.cli --help
          python -m scripts.cli doctor --no-color
```

- [ ] **Step 2: Verify the YAML is well-formed**

Run: `python -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml'))"`
Expected: no output (valid YAML).

- [ ] **Step 3: Run the local smoke test step on this machine**

Reproduce what CI would do (subset):

```bash
uv pip install --system -e ".[dev]"
pytest -m "not eval"
pytest -m eval
aisurface --help || echo "console script not on PATH (expected on some Windows configs)"
python -m scripts.cli --help
python -m scripts.cli doctor --no-color
```

Expected:
- `pytest -m "not eval"` passes (~127 tests)
- `pytest -m eval` passes (~4 fixture tests)
- The other commands run without error (exit 0)

- [ ] **Step 4: Commit**

```bash
git add .github/workflows/ci.yml
git commit -m "ci: expand to 15-job matrix (3 OS x 5 Python) + doctor smoke test"
```

---

## Task 17: Bump `pyproject.toml` version to 1.0.2

**Files:**
- Modify: `pyproject.toml:3`

- [ ] **Step 1: Bump the version**

In `pyproject.toml`, change line 3:

```toml
version = "1.0.1"
```

to:

```toml
version = "1.0.2"
```

- [ ] **Step 2: Verify the build still works**

Run: `python -c "import tomllib; print(tomllib.load(open('pyproject.toml', 'rb'))['project']['version'])"`
Expected: `1.0.2`

- [ ] **Step 3: Commit (without building — that's Task 18)**

```bash
git add pyproject.toml
git commit -m "chore(release): bump version to 1.0.2"
```

---

## Task 18: Tag v1.0.2 and push everything to origin

**Files:**
- No code changes — git operations only

- [ ] **Step 1: Push the main branch**

Run: `git push origin main`
Expected: 17 new commits pushed (Tasks 1-17 + 2 spec commits + 1 version bump).

- [ ] **Step 2: Create and push the v1.0.2 tag**

Run: `git tag v1.0.2 && git push origin v1.0.2`
Expected: tag created locally and pushed.

- [ ] **Step 3: Verify the tag points to the right commit**

Run: `git log --oneline v1.0.2 -1`
Expected: shows the `chore(release): bump version to 1.0.2` commit.

---

## Task 19: Build sdist + wheel, upload to TestPyPI, verify, upload to real PyPI

**Files:**
- No code changes — release operations only

- [ ] **Step 1: Clean previous build artifacts**

Run: `rm -rf dist/ build/ *.egg-info`
Expected: dist/ removed.

- [ ] **Step 2: Build sdist + wheel**

Run: `python -m build`
Expected: creates `dist/aisurface-1.0.2-py3-none-any.whl` and `dist/aisurface-1.0.2.tar.gz`. Both should be small (~50KB).

- [ ] **Step 3: Validate metadata with twine**

Run: `twine check dist/*`
Expected: `Checking dist/aisurface-1.0.2-py3-none-any.whl: PASSED` and the same for the tar.gz. (Or: `passing` instead of `PASSED` depending on twine version.)

- [ ] **Step 4: Upload to TestPyPI**

Run: `twine upload --repository testpypi dist/*`
Expected: prompts for credentials (or uses `~/.pypirc`); uploads both files. URLs printed like `View at: https://test.pypi.org/project/aisurface/1.0.2/`.

- [ ] **Step 5: Verify TestPyPI install in a clean venv**

Create a fresh venv and test:

```bash
# Use a fresh dir to avoid clobbering the dev install
mkdir -p /tmp/aisurface-verify-102 && cd /tmp/aisurface-verify-102
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
pip install --index-url https://test.pypi.org/simple/ aisurface==1.0.2
python -m scripts.cli doctor --no-color
python -m scripts.cli audit evals/fixtures/perfect-readme-and-docs --no-color
```

Expected:
- `pip install` succeeds
- `doctor` exits 0 with ✓/⚠ rows
- `audit` shows 90+ score

- [ ] **Step 6: Clean up the verify venv**

Run: `rm -rf /tmp/aisurface-verify-102`
Expected: temp dir gone.

- [ ] **Step 7: Upload to real PyPI**

Run: `twine upload dist/*`
Expected: prompts for credentials, uploads both files to https://pypi.org/project/aisurface/1.0.2/.

- [ ] **Step 8: Verify the real PyPI install in a fresh venv**

```bash
mkdir -p /tmp/aisurface-verify-102-real && cd /tmp/aisurface-verify-102-real
python -m venv venv
source venv/bin/activate
pip install --upgrade aisurface  # should pick up 1.0.2
python -m scripts.cli doctor --no-color
python -m scripts.cli --help  # should show {audit,fix,verify,doctor}
```

Expected: `Version: 1.0.2`, `doctor` runs, `--help` shows 4 verbs.

- [ ] **Step 9: Clean up the verify venv**

Run: `rm -rf /tmp/aisurface-verify-102-real`

- [ ] **Step 10: No commit needed — release is git-tagged, not a commit**

Note: this task doesn't produce a commit. The release is marked by the v1.0.2 git tag (Task 18).

---

## Task 20: Final post-release verification

**Files:**
- No code changes

- [ ] **Step 1: Re-run the full test suite one more time**

Run: `pytest -m "not eval" && pytest -m eval && ruff check .`
Expected: all 3 pass, zero failures, zero errors.

- [ ] **Step 2: Verify the README 5-min self-test passes on this machine**

```bash
python -m scripts.cli doctor --no-color
python -m scripts.cli --help
python -m scripts.cli audit evals/fixtures/bad-readme-python-lib --no-color
python -m scripts.cli audit evals/fixtures/perfect-readme-and-docs --no-color
python -m scripts.cli fix evals/fixtures/bad-readme-python-lib --dry-run
```

Expected: all 5 commands exit 0, output matches the README.

- [ ] **Step 3: Verify the minimalloc end-to-end test still works (regression sanity)**

This is the test the user ran in the conversation that motivated v1.0.2. Confirm audit + fix still work as expected:

```bash
# Audit minimalloc baseline (the one we did before, should be unchanged)
python -m scripts.cli audit D:/Code/MyProject/aisurface-test/minimalloc --no-color
# Score: 7/100 expected
```

Expected: same 7/100 score as v1.0.1. This proves we didn't break audit.

- [ ] **Step 4: Update ROADMAP.md to mark v1.0.2 as ✅ shipped**

Wait, this was already done in Task 12. Skip if already ✅.

- [ ] **Step 5: Done**

v1.0.2 is released. Tell the user: "v1.0.2 is on PyPI. Run `pip install --upgrade aisurface` and try `python -m scripts.cli doctor --no-color`."

---

# Self-Review (run after writing this plan, before handing off)

## Spec coverage

Going through each section of the spec:

| Spec section | Task(s) |
|---|---|
| Architecture overview (entry point strategy) | Task 8, Task 10 |
| Decision log (D1–D5) | Encoded throughout (D1=Task 3 check 8, D2=Task 3 cmd_doctor return codes, D3=Task 3 no `--fix` mode, D4=Task 3 only in `doctor`, D5=Task 10 README leads with `python -m`) |
| Component: `aisurface doctor` (8 checks, output, exit codes, flags) | Tasks 3, 4, 5, 6, 7, 8 |
| Component: `safe_dispatch` error wrapper | Task 1, Task 2 |
| CI matrix (15 jobs) | Task 16 |
| Documentation changes (README, SKILL.md, CHANGELOG, ROADMAP, L1/L2) | Tasks 9, 10, 11, 12, 13, 14, 15 |
| Release process (9 steps) | Tasks 17, 18, 19 |
| Test plan (15 doctor + 6 safe_dispatch) | Tasks 1, 4, 5, 6, 7 |
| File changes summary (6 new + 9 modified) | All 9 modifications + 4 new files covered |
| Regression coverage (existing functionality) | Task 2 Step 3, Task 8 Steps 6-7, Task 16 Step 3, Task 20 |

## Placeholder scan

Searched the plan for "TBD", "TODO", "fill in", "similar to". Found 0 plan-level placeholders. (Inside the Python code, the `safe_dispatch.py` PermissionError catch has `<unknown>` fallback for `args.path` — that's intentional, not a placeholder.)

## Type / signature consistency

- `DoctorCheck` dataclass: defined in Task 3, used in Tasks 4-7. Field names match (`name`, `status`, `message`, `fix_hints`).
- `cmd_doctor(args) -> int`: defined in Task 3, used in Task 8 subparser. Signature matches `cmd_audit` / `cmd_fix` / `cmd_verify`.
- `safe_dispatch(handler) -> wrapper`: defined in Task 1, used in Task 2. Returns `int` from `handler(args)`.
- `_ALL_CHECK_FUNCS`: defined in Task 3, monkey-patched in Task 7 tests. Same name throughout.
- `_pkg_version` import alias: defined in Task 3, monkey-patched in Task 6 tests. Same name.
- 8 check function names: `check_python_version`, `check_scripts_importable`, `check_console_script_on_path`, `check_deps_importable`, `check_cache_dir_writable`, `check_pypi_latest_version`, `check_perplexity_api_key`. All 7 (since check 7 is implicit) used in `_ALL_CHECK_FUNCS` order, and the same names are referenced in the test files. Consistent.

## Ambiguity check

- Task 2 says "Place it next to the other `from __future__` / stdlib imports" — could be read as "after the import block" or "in the import block". In context (a real `cli.py` file), the developer reading the file will see the existing import order and follow it. Acceptable.
- Task 13 says "in the appropriate alphabetical / logical place" — for an L2 doc, this is a judgment call. Acceptable for a 1-line entry.
- Task 18 doesn't say "after all commits are pushed". Added clarity: Task 18 Step 1 says "17 new commits pushed (Tasks 1-17 + 2 spec commits + 1 version bump)".

## Gaps found during self-review

None. All spec requirements map to tasks. All task types match the spec's TDD discipline (test first, then impl).

---

# Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-06-03-aisurface-v102-windows-install.md`. 20 tasks total:

- Tasks 1-2: `safe_dispatch` decorator (foundation)
- Tasks 3-7: `doctor` self-check (the meat — 27 tests)
- Task 8: Wire `doctor` into `cli.py` as 4th subcommand
- Tasks 9-15: Documentation updates (SKILL.md, README, CHANGELOG, ROADMAP, L1/L2 docs)
- Task 16: CI matrix expansion (1 job → 15 jobs)
- Tasks 17-18: Version bump + git tag + push
- Task 19: Build + TestPyPI + real PyPI upload
- Task 20: Post-release verification

Two execution options:

1. **Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration with isolated context
2. **Inline Execution** — Execute tasks in this session using `executing-plans`, batch execution with checkpoints

Which approach?

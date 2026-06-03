"""
 * [INPUT]: Depends on `sys` (version, argv), `os` (env, access), `shutil` (which), `importlib`, `importlib.metadata`, `pathlib.Path`, `sysconfig`, `httpx` (already a dep), `dataclasses`, `json`, `scripts.colors`.
 * [OUTPUT]: Provides `cmd_doctor(args) -> int`, `DoctorCheck` dataclass, 7 check_* functions (internet reachability is implicit in check_pypi_latest_version), `render_human` / `render_json` for output. Used by `scripts/cli.py` as the 4th subcommand.
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
        fix_hints=["Upgrade Python: https://www.python.org/downloads/"],
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
        sym, color = _GLYPH[c.status]
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
        sym, color = _GLYPH[FAIL]
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

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

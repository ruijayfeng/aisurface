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

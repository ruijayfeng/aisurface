"""Verify CLI dispatches to the right subcommand."""
import subprocess
import sys


def _run(*args) -> tuple[int, str, str]:
    r = subprocess.run(
        [sys.executable, "-m", "scripts.cli", *args],
        capture_output=True, text=True, encoding="utf-8",
    )
    return r.returncode, r.stdout, r.stderr


def test_audit_subcommand_runs():
    code, out, _ = _run("audit", "evals/fixtures/minimal-cli-tool")
    assert code == 0
    assert "Health score" in out


def test_no_subcommand_shows_help():
    code, _, err = _run()
    assert code != 0
    assert "audit" in err and "fix" in err and "verify" in err


def test_fix_subcommand_registered():
    code, _, err = _run("fix", "--help")
    assert code == 0


def test_verify_subcommand_registered():
    code, _, err = _run("verify", "--help")
    assert code == 0

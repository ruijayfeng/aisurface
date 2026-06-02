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


def test_fix_subcommand_dispatches_to_handler():
    # perfect-readme-and-docs fixture has all 4 patch targets, so the dispatcher
    # reports "Nothing to fix" (instead of generating 4 patches).
    code, out, _ = _run("fix", "evals/fixtures/perfect-readme-and-docs", "--dry-run")
    assert code == 0
    assert "Nothing to fix" in out


def test_verify_subcommand_dispatches_to_stub():
    code, _, err = _run("verify", "evals/fixtures/minimal-cli-tool")
    assert code == 1
    assert "not fully wired" in err

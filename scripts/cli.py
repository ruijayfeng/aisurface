"""CLI entry point. Dispatches to audit/fix/verify subcommands."""
from __future__ import annotations

import argparse
import importlib
import sys

_DISPATCH = {
    "audit": "scripts.audit.cmd_audit",
    "fix": "scripts.fix.cmd_fix",
    "verify": "scripts.verify.cmd_verify",
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="aisurface",
        description="AI-search citation readiness for OSS projects.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True, metavar="{audit,fix,verify}")

    # audit subcommand
    audit_p = subparsers.add_parser("audit", help="Run 12-check GEO audit")
    audit_p.add_argument("path", nargs="?", default=".", help="Repo root (default: cwd)")
    audit_p.add_argument("--learn", action="store_true", help="Teacher mode")
    audit_p.add_argument("--json", action="store_true", help="JSON output")
    audit_p.add_argument("--no-color", action="store_true", help="Disable color output")

    # fix subcommand (Task 6 wires the handler)
    fix_p = subparsers.add_parser("fix", help="Generate and apply patches for must-fix items")
    fix_p.add_argument("path", nargs="?", default=".", help="Repo root (default: cwd)")
    fix_p.add_argument("--dry-run", action="store_true", help="Print patches, don't apply")
    fix_p.add_argument("--yes", action="store_true", help="Apply all without confirmation")
    fix_p.add_argument("--only", help="Comma-separated patch types (faq,when_to_use,llms_txt,schema_org)")
    fix_p.add_argument("--no-color", action="store_true", help="Disable color output")

    # verify subcommand (Task 13 wires the handler)
    verify_p = subparsers.add_parser("verify", help="Probe AI platforms for citation rate")
    verify_p.add_argument("path", nargs="?", default=".", help="Repo root (default: cwd)")
    verify_p.add_argument("--platforms", default="perplexity",
                          help="Comma-separated platform names (perplexity,deepseek)")
    verify_p.add_argument("--baseline", action="store_true", help="Establish/reset baseline")
    verify_p.add_argument("--queries-file", help="Custom queries file (1 query per line)")

    return parser


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = build_parser()
    args = parser.parse_args(argv)

    target = _DISPATCH.get(args.command)
    if target is None:
        parser.print_help()
        return 1
    module_path, _, attr = target.rpartition(".")
    handler = getattr(importlib.import_module(module_path), attr)
    return handler(args)


if __name__ == "__main__":
    sys.exit(main())

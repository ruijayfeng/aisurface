"""
 * [INPUT]: Depends on `scripts.scanner.scan_repo`, the four patch generators in this package (`fix.faq`, `fix.when_to_use`, `fix.llms_txt`, `fix.schema_org`), and `argparse` args (`--path`, `--only`, `--dry-run`, `--yes`).
 * [OUTPUT]: Provides `Patch` dataclass (patch_type, target_file, new_content, is_new_file, description) and `cmd_fix(args) -> int` (CLI dispatch target for the `fix` subcommand). Iterates generators, prints summary, prompts for apply (or skips on `--yes`/`--dry-run`).
 * [POS]: Fix subcommand core. Imported by `cli.py`. Dispatcher layer that sits above the four single-purpose patch generators.
 * [PROTOCOL]: Update this header when changed, then check CLAUDE.md
"""

"""Fix subcommand: generate and apply patches."""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Patch:
    patch_type: str
    target_file: Path
    new_content: str
    is_new_file: bool
    description: str


def cmd_fix(args) -> int:
    from scripts.fix.faq import generate_faq_patch
    from scripts.fix.llms_txt import generate_llms_txt_patch
    from scripts.fix.schema_org import generate_schema_org_patch
    from scripts.fix.when_to_use import generate_when_to_use_patch
    from scripts.scanner import scan_repo

    repo_root = Path(args.path).resolve()
    if not repo_root.exists():
        print(f"Error: {repo_root} does not exist", file=sys.stderr)
        return 1

    assets = scan_repo(repo_root)
    only = set(args.only.split(",")) if args.only else None

    generators = [
        ("faq", lambda: generate_faq_patch(repo_root, project_type=assets.project_type or "generic")),
        ("when_to_use", lambda: generate_when_to_use_patch(repo_root)),
        ("llms_txt", lambda: generate_llms_txt_patch(repo_root)),
        ("schema_org", lambda: generate_schema_org_patch(repo_root)),
    ]

    patches: list[Patch] = []
    for ptype, gen in generators:
        if only and ptype not in only:
            continue
        patch = gen()
        if patch is not None:
            patches.append(patch)

    if not patches:
        print("Nothing to fix. Either everything passes or all targets already exist.")
        return 0

    print(f"Generated {len(patches)} patch(es):\n")
    for p in patches:
        relpath = p.target_file.relative_to(repo_root) if p.target_file.is_relative_to(repo_root) else p.target_file
        kind = "NEW " if p.is_new_file else "EDIT"
        print(f"  [{p.patch_type}] {kind} {relpath} — {p.description}")

    if args.dry_run:
        print("\n--dry-run: no files written.")
        return 0

    if not args.yes:
        try:
            answer = input("\nApply all? [Y/n]: ").strip().lower()
        except EOFError:
            answer = ""
        if answer in {"n", "no"}:
            print("Aborted.")
            return 0

    # Re-run each generator at apply time so multiple edit patches on the
    # same file compose correctly. The earlier `patches` list is what we
    # showed the user; the actual write uses fresh state (each generator
    # reads the current file, so a later edit builds on an earlier one).
    for ptype, gen in generators:
        if only and ptype not in only:
            continue
        patch = gen()
        if patch is None:
            continue
        patch.target_file.parent.mkdir(parents=True, exist_ok=True)
        patch.target_file.write_text(patch.new_content, encoding="utf-8")
        print(f"✓ Applied [{ptype}] to {patch.target_file}")

    return 0

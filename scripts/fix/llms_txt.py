"""
 * [INPUT]: Depends on `pathlib.Path`, `scripts.scanner.scan_repo`, `scripts.llms_txt.build_llms_txt` (shared builder).
 * [OUTPUT]: Provides `generate_llms_txt_patch(repo_root) -> Patch | None`. If `.well-known/llms.txt` already exists, returns None. Otherwise returns a `Patch` writing a valid llms.txt body to that path, with project name + description + a single "Docs" section.
 * [POS]: One of the four `fix` patch generators. Imported lazily by `fix.cmd_fix`. Targets check #6 (llms.txt presence) in the audit. Composes with `scripts/llms_txt.py` (the audit-side reader and shared builder).
 * [PROTOCOL]: Update this header when changed, then check CLAUDE.md
"""

"""llms.txt patch: generates a valid .well-known/llms.txt file."""
from __future__ import annotations

import re
from pathlib import Path

from scripts.fix import Patch
from scripts.llms_txt import render_llms_txt


def generate_llms_txt_patch(repo_root: Path) -> Patch | None:
    """Generate a new .well-known/llms.txt file.

    Returns None if the file already exists.
    """
    target = repo_root / ".well-known" / "llms.txt"
    if target.exists():
        return None

    name = _extract_project_name(repo_root)
    description = _extract_description(repo_root)

    content = render_llms_txt(
        project_name=name,
        description=description,
        sections=[
            {"title": "Docs", "links": [{"url": "/README.md", "title": "Project README"}]},
        ],
        details={"License": "<TODO: e.g. MIT>", "Language": "<TODO: e.g. Python>"},
    )

    return Patch(
        patch_type="llms_txt",
        target_file=target,
        new_content=content,
        is_new_file=True,
        description=f".well-known/llms.txt (per llmstxt.org spec, {len(content.splitlines())} lines)",
    )


def _extract_description(repo_root: Path) -> str:
    """Pull a 1-line description from README's first paragraph after the H1."""
    readme = repo_root / "README.md"
    if not readme.exists():
        return f"{repo_root.name} project"
    text = readme.read_text(encoding="utf-8")
    match = re.search(r"^#\s+\S.*?\n+([^\n#].+?)(?:\n|$)", text, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return f"{repo_root.name} project"


def _extract_project_name(repo_root: Path) -> str:
    """Pull project name from README's H1, falling back to directory name."""
    readme = repo_root / "README.md"
    if readme.exists():
        text = readme.read_text(encoding="utf-8")
        match = re.search(r"^#\s+(\S.*?)$", text, re.MULTILINE)
        if match:
            return match.group(1).strip()
    return repo_root.name

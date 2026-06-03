"""
 * [INPUT]: Depends on `pathlib.Path`, `scripts.scanner.scan_repo`, the README file at the repo root.
 * [OUTPUT]: Provides `generate_when_to_use_patch(repo_root) -> Patch | None`. If both `## When to use` and `## When NOT to use` already exist, returns None. Otherwise returns a `Patch` adding both sections with templated bullet placeholders for the user to fill in.
 * [POS]: One of the four `fix` patch generators. Imported lazily by `fix.cmd_fix`. Targets check #3 (when-to-use) and check #9 (when-NOT-to-use) in the audit.
 * [PROTOCOL]: Update this header when changed, then check CLAUDE.md
"""

"""When-to-use stub patch: adds 'When to use' + 'When NOT to use' sections."""
from __future__ import annotations

import re
from pathlib import Path

from scripts.fix import Patch

_WHEN_TO_USE_STUB = """## When to use

- <TODO: scenario 1 where this project is the right choice>
- <TODO: scenario 2>
- <TODO: scenario 3>
"""

_WHEN_NOT_TO_USE_STUB = """## When NOT to use

- <TODO: scenario 1 where users should pick something else>
- <TODO: scenario 2>
- <TODO: pointer to the recommended alternative for those cases>
"""


def generate_when_to_use_patch(repo_root: Path) -> Patch | None:
    """Insert missing When-to-use / When-NOT-to-use sections.

    Returns None if README is missing OR both sections already exist.
    """
    readme = repo_root / "README.md"
    if not readme.exists():
        return None

    existing = readme.read_text(encoding="utf-8")
    has_use = bool(re.search(
        r"^#{1,4}\s*(when\s+to\s+use|适用场景|use\s+cases)",
        existing, re.MULTILINE | re.IGNORECASE,
    ))
    has_not_use = bool(re.search(
        r"^#{1,4}\s*(when\s+not\s+to\s+use|不适用|not\s+for|when\s+to\s+avoid)",
        existing, re.MULTILINE | re.IGNORECASE,
    ))

    if has_use and has_not_use:
        return None

    parts: list[str] = []
    if not has_use:
        parts.append(_WHEN_TO_USE_STUB)
    if not has_not_use:
        parts.append(_WHEN_NOT_TO_USE_STUB)
    to_insert = "\n".join(parts)

    new_content = _insert_after_first_h1(existing, to_insert)
    return Patch(
        patch_type="when_to_use",
        target_file=readme,
        new_content=new_content,
        is_new_file=False,
        description=f"When-to-use sections ({'both' if not (has_use or has_not_use) else 'missing half'})",
    )


def _insert_after_first_h1(content: str, section: str) -> str:
    """Insert after the first H1 + its immediate paragraph block, else at end."""
    h1_match = re.search(r"^#\s+\S.*$", content, re.MULTILINE)
    if not h1_match:
        sep = "" if content.endswith("\n") else "\n"
        return content + sep + "\n" + section
    rest_start = h1_match.end()
    next_h2 = re.search(r"^##\s+", content[rest_start:], re.MULTILINE)
    idx = rest_start + next_h2.start() if next_h2 else len(content)
    return content[:idx] + section + "\n" + content[idx:]

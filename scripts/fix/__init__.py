"""Fix subcommand: generate and apply patches."""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Patch:
    """A single patch the user can apply or skip."""
    patch_type: str       # "faq" | "when_to_use" | "llms_txt" | "schema_org"
    target_file: Path     # File to write or modify
    new_content: str      # Full new file content (for new files) or post-edit content (for edits)
    is_new_file: bool     # True if target_file doesn't exist yet
    description: str      # Human-readable summary, e.g. "FAQ section (8 Q&A)"


def cmd_fix(args) -> int:
    """Stub - wired in Task 6."""
    print("fix command not fully wired yet", file=sys.stderr)
    return 1

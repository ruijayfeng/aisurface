"""Schema.org patch: generates index.schema.json with SoftwareApplication + FAQPage."""
from __future__ import annotations

import json
from pathlib import Path

from scripts.fix import Patch
from scripts.schema_gen import build_faq_page, build_software_application


def generate_schema_org_patch(repo_root: Path) -> Patch | None:
    """Generate a new index.schema.json file with SoftwareApplication + FAQPage stubs.

    Returns None if the file already exists.
    """
    target = repo_root / "index.schema.json"
    if target.exists():
        return None

    sw = build_software_application(
        name=repo_root.name,
        description=f"<TODO: 1-sentence description of {repo_root.name}>",
        url=f"<TODO: project URL, e.g. https://github.com/owner/{repo_root.name}>",
    )
    faq = build_faq_page(questions=[
        {"q": "<TODO: Q1>", "a": "<TODO: A1>"},
        {"q": "<TODO: Q2>", "a": "<TODO: A2>"},
    ])

    content = json.dumps([sw, faq], indent=2, ensure_ascii=False)
    return Patch(
        patch_type="schema_org",
        target_file=target,
        new_content=content,
        is_new_file=True,
        description="index.schema.json (SoftwareApplication + FAQPage)",
    )

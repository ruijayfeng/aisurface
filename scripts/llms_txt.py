"""
 * [INPUT]: Depends on `pathlib`, `typing.TypedDict` (stdlib).
 * [OUTPUT]: Provides `Link`, `Section` TypedDicts; `build_llms_txt(project_name, description, sections, details) -> str`; `write_llms_txt(repo_root, project_name, description, sections, details) -> Path`.
 * [POS]: llms.txt generation per https://llmstxt.org. Used by the audit verb's check #6 (to test if file exists) and by `fix/llms_txt.py` to generate the file.
 * [PROTOCOL]: Update this header when changed, then check CLAUDE.md

Generate and validate .well-known/llms.txt per the llms.txt spec.
"""
from __future__ import annotations

from pathlib import Path
from typing import TypedDict


class Link(TypedDict):
    url: str
    title: str


class Section(TypedDict):
    title: str
    links: list[Link]


def render_llms_txt(
    project_name: str,
    description: str,
    sections: list[Section],
    details: dict[str, str] | None = None,
) -> str:
    """Render an llms.txt file body per https://llmstxt.org.

    Pure function: takes structured inputs, returns a string.

    Args:
        project_name: Used as the H1.
        description: Single-line blockquote summary.
        sections: Optional list of `{title, links}` sections.
        details: Optional `{key: value}` for the "Project details" section.

    Returns:
        The full llms.txt content as a string.
    """
    lines = [f"# {project_name}", "", f"> {description}", ""]

    if details:
        lines.append("## Project details")
        lines.append("")
        for key, value in details.items():
            lines.append(f"- {key}: {value}")
        lines.append("")

    for section in sections:
        lines.append(f"## {section['title']}")
        lines.append("")
        for link in section["links"]:
            lines.append(f"- [{link['title']}]({link['url']})")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


# Backward-compat alias (existing callers/tests use this name).
build_llms_txt = render_llms_txt


def validate_llms_txt(content: str) -> list[str]:
    """Return a list of validation errors. Empty list = valid."""
    errors: list[str] = []
    lines = content.splitlines()
    if not lines or not lines[0].startswith("# "):
        errors.append("Missing H1 title (first line must be '# <name>')")
    if len(lines) < 3 or not lines[2].startswith("> "):
        errors.append("Missing blockquote description (third line must be '> <desc>')")
    return errors


def write_llms_txt(
    repo_root: Path,
    project_name: str,
    description: str,
    sections: list[Section],
    details: dict[str, str] | None = None,
) -> Path:
    """Write llms.txt to `<repo_root>/.well-known/llms.txt`.

    Creates `.well-known/` if it does not exist.
    """
    target_dir = repo_root / ".well-known"
    target_dir.mkdir(exist_ok=True)
    target = target_dir / "llms.txt"
    target.write_text(
        render_llms_txt(project_name, description, sections, details),
        encoding="utf-8",
    )
    return target

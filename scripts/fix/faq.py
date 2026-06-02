"""FAQ injection patch: adds 8 Q&A stubs to README."""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from scripts.fix import Patch


@dataclass
class FAQTemplate:
    """A project-type-specific FAQ template."""
    name: str
    questions: list[tuple[str, str]]  # (question, stub_answer)

    @classmethod
    def for_project_type(cls, project_type: str) -> FAQTemplate:
        """Return a template for the given project type, falling back to 'generic'."""
        if project_type in _TEMPLATES:
            return _TEMPLATES[project_type]
        return _TEMPLATES["generic"]


_GENERIC_QA = [
    ("What does this project do?", "<TODO: 1-sentence summary of the core capability>"),
    ("Who is this for?", "<TODO: target user profile, e.g. 'Python backend developers building APIs'>"),
    ("How is this different from <alternative>?", "<TODO: 1-2 specific differentiators>"),
    ("What are the system requirements?", "<TODO: language version, OS, hardware>"),
    ("How do I install it?", "<TODO: one-line install command + verification>"),
    ("Where do I find examples?", "<TODO: link to examples/ folder or docs section>"),
    ("How do I report a bug or request a feature?", "<TODO: link to issue tracker + template>"),
    ("What's the license?", "<TODO: MIT/Apache/GPL + 1 sentence on commercial use>"),
]

_PYTHON_LIB_QA = [
    ("What does this library do?", "<TODO: 1-sentence summary>"),
    ("Which Python versions are supported?", "<TODO: e.g. 'Python 3.10+'>"),
    ("How do I install it?", "<TODO: `pip install ...` or `uv add ...`>"),
    ("How is this different from <competing library>?", "<TODO: 1-2 specific differentiators>"),
    ("Does it work with async code?", "<TODO: yes/no + 1-line example>"),
    ("How do I run the tests?", "<TODO: `pytest` invocation + any setup>"),
    ("How do I report a bug?", "<TODO: link to GitHub issues>"),
    ("What's the license?", "<TODO: MIT/Apache/GPL>"),
]

_TEMPLATES: dict[str, FAQTemplate] = {
    "generic": FAQTemplate("generic", _GENERIC_QA),
    "python-library": FAQTemplate("python-library", _PYTHON_LIB_QA),
    # Add more types in v0.1.4+: "cli-tool", "web-framework", "docs-site"
}


def generate_faq_patch(repo_root: Path, project_type: str = "generic") -> Patch | None:
    """Generate a patch that injects a FAQ section into README.

    Returns None if README is missing OR an FAQ section already exists.
    """
    readme = repo_root / "README.md"
    if not readme.exists():
        return None

    existing = readme.read_text(encoding="utf-8")
    if re.search(r"^#{1,4}\s*(faq|frequently\s+asked|常见问题)", existing, re.MULTILINE | re.IGNORECASE):
        return None

    template = FAQTemplate.for_project_type(project_type)
    faq_section = _render_faq_section(template)
    new_content = _insert_before_license(existing, faq_section)

    return Patch(
        patch_type="faq",
        target_file=readme,
        new_content=new_content,
        is_new_file=False,
        description=f"FAQ section ({len(template.questions)} Q&A, template: {template.name})",
    )


def _render_faq_section(template: FAQTemplate) -> str:
    lines = ["## FAQ", ""]
    for q, a in template.questions:
        lines.append(f"### {q}")
        lines.append("")
        lines.append(a)
        lines.append("")
    return "\n".join(lines)


def _insert_before_license(content: str, faq_section: str) -> str:
    """Insert faq_section before '## License' if present, else at end."""
    license_match = re.search(r"^#{1,4}\s*license", content, re.MULTILINE | re.IGNORECASE)
    if license_match:
        idx = license_match.start()
        return content[:idx] + faq_section + "\n" + content[idx:]
    sep = "" if content.endswith("\n") else "\n"
    return content + sep + "\n" + faq_section + "\n"

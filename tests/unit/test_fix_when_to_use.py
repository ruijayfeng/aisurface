"""When-to-use stub patch generator."""
from pathlib import Path

from scripts.fix.when_to_use import generate_when_to_use_patch


def test_inserts_both_sections(tmp_path: Path):
    readme = tmp_path / "README.md"
    readme.write_text("# my-lib\n\nA tool.\n", encoding="utf-8")
    patch = generate_when_to_use_patch(tmp_path)
    assert "## When to use" in patch.new_content
    assert "## When NOT to use" in patch.new_content


def test_skips_if_both_present(tmp_path: Path):
    readme = tmp_path / "README.md"
    readme.write_text(
        "# x\n\n## When to use\n\nfoo\n\n## When NOT to use\n\nbar\n", encoding="utf-8"
    )
    patch = generate_when_to_use_patch(tmp_path)
    assert patch is None


def test_adds_missing_half_if_only_when_to_use_exists(tmp_path: Path):
    readme = tmp_path / "README.md"
    readme.write_text("# x\n\n## When to use\n\nfoo\n", encoding="utf-8")
    patch = generate_when_to_use_patch(tmp_path)
    assert patch is not None
    assert "## When NOT to use" in patch.new_content
    assert patch.new_content.count("## When to use") == 1  # don't duplicate


def test_missing_readme_returns_none(tmp_path: Path):
    assert generate_when_to_use_patch(tmp_path) is None

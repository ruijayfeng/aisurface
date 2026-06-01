from pathlib import Path

from scripts.llms_txt import build_llms_txt, validate_llms_txt


def test_build_llms_txt_basic():
    content = build_llms_txt(
        project_name="my-proj",
        description="A test project",
        sections=[
            {"title": "Docs", "links": [{"url": "/docs/", "title": "Documentation"}]},
        ],
    )
    assert "# my-proj" in content
    assert "> A test project" in content
    assert "## Docs" in content
    assert "- [Documentation](/docs/)" in content


def test_build_llms_txt_with_optional_fields():
    content = build_llms_txt(
        project_name="my-proj",
        description="desc",
        sections=[],
        details={"Language": "Python", "License": "MIT"},
    )
    assert "## Project details" in content
    assert "- Language: Python" in content
    assert "- License: MIT" in content


def test_validate_llms_txt_accepts_valid():
    valid = build_llms_txt(
        project_name="p", description="d", sections=[{"title": "S", "links": []}]
    )
    assert validate_llms_txt(valid) == []


def test_validate_llms_txt_flags_missing_h1():
    errors = validate_llms_txt("no h1 here")
    assert any("H1" in e or "title" in e.lower() for e in errors)


def test_validate_llms_txt_flags_missing_quote():
    errors = validate_llms_txt("# Title\nNo quote line\n")
    assert any("quote" in e.lower() or "description" in e.lower() for e in errors)


def test_write_llms_txt_to_dotfile(tmp_path: Path):
    from scripts.llms_txt import write_llms_txt
    target = write_llms_txt(
        tmp_path,
        project_name="p",
        description="d",
        sections=[],
    )
    assert target == tmp_path / ".well-known" / "llms.txt"
    assert target.exists()
    assert target.read_text().startswith("# p")

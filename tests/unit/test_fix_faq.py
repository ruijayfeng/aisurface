"""FAQ injection patch generator."""
from pathlib import Path

from scripts.fix.faq import FAQTemplate, generate_faq_patch


def test_generates_8_qa_pairs_for_python_library(tmp_path: Path):
    readme = tmp_path / "README.md"
    readme.write_text("# my-lib\n\nA Python library.\n", encoding="utf-8")
    patch = generate_faq_patch(tmp_path, project_type="python-library")
    assert patch.target_file == readme
    assert "## FAQ" in patch.new_content
    assert patch.new_content.count("\n### ") == 8


def test_skips_if_faq_already_present(tmp_path: Path):
    readme = tmp_path / "README.md"
    readme.write_text("# my-lib\n\n## FAQ\n\nExisting content.\n", encoding="utf-8")
    patch = generate_faq_patch(tmp_path, project_type="python-library")
    assert patch is None  # Nothing to do


def test_inserts_before_license_section(tmp_path: Path):
    readme = tmp_path / "README.md"
    readme.write_text(
        "# my-lib\n\n## Install\n\npip install\n\n## License\n\nMIT\n",
        encoding="utf-8",
    )
    patch = generate_faq_patch(tmp_path, project_type="python-library")
    install_idx = patch.new_content.find("## Install")
    faq_idx = patch.new_content.find("## FAQ")
    license_idx = patch.new_content.find("## License")
    assert install_idx < faq_idx < license_idx


def test_missing_readme_returns_none(tmp_path: Path):
    patch = generate_faq_patch(tmp_path, project_type="python-library")
    assert patch is None


def test_unknown_project_type_uses_generic_template():
    template = FAQTemplate.for_project_type("never-heard-of-it")
    assert len(template.questions) == 8
    assert template.name == "generic"

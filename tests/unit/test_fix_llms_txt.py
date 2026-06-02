"""llms.txt patch generator."""
from pathlib import Path

from scripts.fix.llms_txt import generate_llms_txt_patch


def test_generates_new_file_patch(tmp_path: Path):
    (tmp_path / "README.md").write_text("# my-lib\n\nA Python library.\n", encoding="utf-8")
    patch = generate_llms_txt_patch(tmp_path)
    assert patch is not None
    assert patch.is_new_file is True
    assert patch.target_file == tmp_path / ".well-known" / "llms.txt"
    assert "my-lib" in patch.new_content
    assert "# my-lib" in patch.new_content  # H1 per llmstxt.org spec


def test_skips_if_already_present(tmp_path: Path):
    well_known = tmp_path / ".well-known"
    well_known.mkdir()
    (well_known / "llms.txt").write_text("# existing\n", encoding="utf-8")
    patch = generate_llms_txt_patch(tmp_path)
    assert patch is None


def test_uses_project_name_from_directory(tmp_path: Path):
    project = tmp_path / "cool-tool"
    project.mkdir()
    (project / "README.md").write_text("# cool-tool\n", encoding="utf-8")
    patch = generate_llms_txt_patch(project)
    assert "cool-tool" in patch.new_content

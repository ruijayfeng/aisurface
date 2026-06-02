"""Schema.org patch generator."""
import json
from pathlib import Path

from scripts.fix.schema_org import generate_schema_org_patch


def test_generates_new_file_with_software_application(tmp_path: Path):
    (tmp_path / "README.md").write_text("# my-lib\n\nA tool.\n", encoding="utf-8")
    patch = generate_schema_org_patch(tmp_path)
    assert patch is not None
    assert patch.is_new_file is True
    assert patch.target_file == tmp_path / "index.schema.json"
    parsed = json.loads(patch.new_content)
    types = [item.get("@type") for item in parsed] if isinstance(parsed, list) else [parsed.get("@type")]
    assert "SoftwareApplication" in types


def test_skips_if_already_present(tmp_path: Path):
    (tmp_path / "index.schema.json").write_text('{"@context": "https://schema.org"}', encoding="utf-8")
    assert generate_schema_org_patch(tmp_path) is None

"""Detect and inventory GEO-relevant files in a project repository."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

PROJECT_MARKERS = {
    "node": ["package.json"],
    "python": ["pyproject.toml", "setup.py", "requirements.txt"],
    "go": ["go.mod"],
    "rust": ["Cargo.toml"],
    "nextjs": ["next.config.js", "next.config.ts", "next.config.mjs"],
    "vite": ["vite.config.js", "vite.config.ts"],
}


@dataclass
class RepoAssets:
    """Inventory of files in a project relevant to GEO."""

    root: Path
    readme: Path | None = None
    project_type: str = "unknown"
    docs_files: list[Path] = field(default_factory=list)
    has_well_known_dir: bool = False
    has_llms_txt: bool = False
    has_schema_org: bool = False
    schema_files: list[Path] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "root": str(self.root),
            "readme": str(self.readme) if self.readme else None,
            "project_type": self.project_type,
            "docs_files": [str(p) for p in self.docs_files],
            "has_well_known_dir": self.has_well_known_dir,
            "has_llms_txt": self.has_llms_txt,
            "has_schema_org": self.has_schema_org,
            "schema_files": [str(p) for p in self.schema_files],
        }


def _detect_project_type(root: Path) -> str:
    """Return the most specific project type marker found in root."""
    for ptype, markers in PROJECT_MARKERS.items():
        for marker in markers:
            if (root / marker).exists():
                return ptype
    return "unknown"


def scan_repo(root: Path) -> RepoAssets:
    """Walk `root` and build a RepoAssets inventory.

    Args:
        root: Path to the repository root (must exist).

    Returns:
        A populated RepoAssets instance. Empty/missing repo returns
        a RepoAssets with mostly-None/empty fields (no exception).
    """
    root = root.resolve()
    if not root.exists():
        return RepoAssets(root=root)

    assets = RepoAssets(
        root=root,
        readme=(root / "README.md") if (root / "README.md").exists() else None,
        project_type=_detect_project_type(root),
    )

    docs_dir = root / "docs"
    if docs_dir.is_dir():
        assets.docs_files = sorted(docs_dir.rglob("*.md"))

    wk_dir = root / ".well-known"
    if wk_dir.is_dir():
        assets.has_well_known_dir = True
        assets.has_llms_txt = (wk_dir / "llms.txt").exists()

    for pattern in ("*.schema.json", "*.schema.jsonld"):
        assets.schema_files.extend(root.rglob(pattern))
    assets.has_schema_org = len(assets.schema_files) > 0

    return assets

"""Detect and inventory GEO-relevant files in a project repository."""
from __future__ import annotations

import fnmatch
import os
from dataclasses import dataclass, field
from pathlib import Path

PROJECT_MARKERS = {
    "nextjs": ["next.config.js", "next.config.ts", "next.config.mjs"],
    "vite": ["vite.config.js", "vite.config.ts"],
    "rust": ["Cargo.toml"],
    "go": ["go.mod"],
    "python": ["pyproject.toml", "setup.py", "requirements.txt"],
    "node": ["package.json"],
}

IGNORE_DIRS = {
    "node_modules", ".git", ".venv", "venv", "env",
    "__pycache__", "dist", "build", ".next", ".nuxt",
    "target", ".pytest_cache", ".ruff_cache", ".mypy_cache",
    "coverage", "htmlcov", ".tox",
}


def _iter_relevant_files(root: Path, pattern: str):
    """Yield files matching `pattern` under `root`, pruning IGNORE_DIRS at walk time."""
    root = Path(root)
    if not root.is_dir():
        return
    for dirpath, dirs, files in os.walk(root):
        # Prune in-place: modify dirs list to skip ignored directories
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for filename in files:
            if fnmatch.fnmatch(filename, pattern):
                yield Path(dirpath) / filename


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
        assets.docs_files = sorted(_iter_relevant_files(docs_dir, "*.md"))

    wk_dir = root / ".well-known"
    if wk_dir.is_dir():
        assets.has_well_known_dir = True
        assets.has_llms_txt = (wk_dir / "llms.txt").exists()

    for pattern in ("*.schema.json", "*.schema.jsonld"):
        assets.schema_files.extend(_iter_relevant_files(root, pattern))
    assets.has_schema_org = len(assets.schema_files) > 0

    return assets

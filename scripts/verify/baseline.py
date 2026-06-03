"""
 * [INPUT]: Depends on `pathlib.Path` (file I/O at `~/.aisurface/baselines/<project-hash>/<platform>.json`), `json` (serialize `ProbeResult` lists), `hashlib` (stable project hash from repo path).
 * [OUTPUT]: Provides `BaselineStore` class with `save(platform, results)`, `load(platform) -> list[ProbeResult] | None`, and a module-level `diff_summary(baseline, current) -> str` helper that prints "baseline cited X/N → current cited Y/N, delta +Z".
 * [POS]: Persistence layer for `verify`. Imported by `verify.cmd_verify`. First run with `--baseline` is the baseline; subsequent runs diff against it. If no baseline exists, the current run becomes the baseline.
 * [PROTOCOL]: Update this header when changed, then check CLAUDE.md

Baseline store for verify command. Stores per-project, per-platform citation results.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from pathlib import Path

from scripts.verify import ProbeResult


class BaselineStore:
    """File-backed store at <cache_root>/baselines/<project_hash>/<platform>.json."""

    def __init__(self, cache_root: Path | None = None):
        if cache_root is None:
            cache_root = Path.home() / ".aisurface"
        self.cache_root = cache_root

    def save(self, project_root: Path, platform: str, results: list[ProbeResult]) -> None:
        path = self._path_for(project_root, platform)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps([asdict(r) for r in results], indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def load(self, project_root: Path, platform: str) -> list[ProbeResult] | None:
        path = self._path_for(project_root, platform)
        if not path.exists():
            return None
        raw = json.loads(path.read_text(encoding="utf-8"))
        return [ProbeResult(**item) for item in raw]

    def _path_for(self, project_root: Path, platform: str) -> Path:
        key = hashlib.sha256(str(project_root.resolve()).encode()).hexdigest()[:16]
        return self.cache_root / "baselines" / key / f"{platform}.json"


def diff_summary(baseline: list[ProbeResult], current: list[ProbeResult]) -> dict:
    """Return a dict with citation counts and delta."""
    b_cited = sum(1 for r in baseline if r.cited)
    c_cited = sum(1 for r in current if r.cited)
    return {
        "baseline_cited": b_cited,
        "baseline_total": len(baseline),
        "current_cited": c_cited,
        "current_total": len(current),
        "delta": c_cited - b_cited,
    }

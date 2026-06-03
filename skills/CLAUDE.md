# skills/
> L2 | Parent: /CLAUDE.md

## Member List
- (root `SKILL.md` lives at /SKILL.md, not in this directory — single unified `aisurface` skill)
- `_deprecated/aisurface-readme/SKILL.md`: DEPRECATED in v1.0. Was the README-optimization sub-skill. Capability now in `aisurface fix .`.
- `_deprecated/aisurface-llms-txt/SKILL.md`: DEPRECATED in v1.0. Was the llms.txt-generation sub-skill. Capability now in `aisurface fix . --only=llms_txt`.

## Invariants
- Exactly ONE user-facing skill in this project: the root `/SKILL.md` (name: `aisurface`).
- Deprecated sub-skill files are kept for one release (v1.0) and removed in v1.1.
- No new sub-skills will be added — the v1.0 design §4 explicitly kills the "skill collection" model.

## Rule
Do not create new entries under `skills/` without updating the v1.0 spec. All new skill-shaped functionality must fold into the unified `/SKILL.md`.

[PROTOCOL]: Update this header when the unified SKILL.md is rewritten or a deprecated sub-skill is removed.

# evals/
> L2 | Parent: /CLAUDE.md

## Member List
- `fixtures/`: 4 hand-crafted OSS-project fixtures used by integration tests + the audit verb.
  - `minimal-cli-tool/`: Bare-minimum CLI in TypeScript. Used to verify "no false positives" on an already-clean project.
  - `bad-readme-python-lib/`: Python lib with intentional GEO gaps. Used to verify the audit catches all must-fix items + the v0.1.2 `fix` verb improves the score.
  - 2 other fixtures (see `fixtures/`).
- `expected_patches/`: (Pending v0.1.2) Snapshot directory of expected `fix` patch outputs per fixture, used by `test_full_fix.py::test_patches_match_snapshot`.
- `trigger_evals.json`: 18 labeled trigger queries (10 should-trigger, 8 should-not-trigger) for `skill-creator` description optimization. Used by the v1.0-onwards SKILL.md description loop.

## Invariants
- Fixture count is stable (4) — adding/removing a fixture is an L1 architecture change.
- `trigger_evals.json` is the single source of truth for "should this skill trigger" evaluation. Update it whenever the SKILL.md description changes meaningfully.

## Rule
Hand-craft fixtures to cover both happy-path (clean) and adversarial (intentionally bad) cases. Avoid auto-generated fixtures — they hide bugs.

[PROTOCOL]: Update this header when a fixture is added/removed or `trigger_evals.json` structure changes.

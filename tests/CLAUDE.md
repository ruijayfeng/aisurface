# tests/
> L2 | Parent: /CLAUDE.md

## Member List
- `unit/`: Pure unit tests (each script's logic in isolation). Currently covers `audit`, `scanner`, `report`, `colors`, `safe_check`, `safe_dispatch`, `llms_txt`, `schema_gen`, `critic`, `distribution`, `github_meta`, `doctor`, `cli_dispatch`, `fix_faq`, `fix_when_to_use`, `fix_llms_txt`, `fix_schema_org`, `smoke`, `verify_baseline`, `verify_perplexity`, `verify_protocol`, and `verify_queries`.
- `integration/`: End-to-end tests that run the CLI as a subprocess. Currently `test_full_audit.py` exercises `python -m scripts.cli audit <fixture> --json` against the 4 eval fixtures.
- `evals/` (NOTE: this is a different directory — the eval fixtures live at `/evals/`, not under tests).

## Invariants
- 145 non-eval + 12 eval = 157 tests passing as of v1.0.3.
- Marker `eval` is defined in `pyproject.toml`; deselect with `pytest -m "not eval"`.
- Every new `scripts/*.py` file must have a corresponding `tests/unit/test_<name>.py`.

## Rule
No fix without a failing test first. TDD is mandatory for new functionality in `scripts/`.

[PROTOCOL]: Update this header when a new test file is added, a test category is introduced, or the marker system changes.

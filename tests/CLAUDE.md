# tests/
> L2 | Parent: /CLAUDE.md

## Member List
- `unit/`: Pure unit tests (each script's logic in isolation). Currently covers `audit`, `scanner`, `report`, `colors`, `concepts`, `safe_check`, `llms_txt`, `schema_gen`, `critic`, `findings`, `distribution`, `github_meta`.
- `integration/`: End-to-end tests that run the CLI as a subprocess. Currently `test_full_audit.py` exercises `python -m scripts.cli audit <fixture> --json` against the 4 eval fixtures.
- `evals/` (NOTE: this is a different directory — the eval fixtures live at `/evals/`, not under tests).

## Invariants
- 67 tests passing as of v0.1.1.
- Marker `eval` is defined in `pyproject.toml`; deselect with `pytest -m "not eval"`.
- Every new `scripts/*.py` file must have a corresponding `tests/unit/test_<name>.py`.

## Pending test files (from v1.0 plan)
- `unit/test_cli_dispatch.py`, `test_fix_faq.py`, `test_fix_when_to_use.py`, `test_fix_llms_txt.py`, `test_fix_schema_org.py`, `test_verify_protocol.py`, `test_verify_perplexity.py`, `test_verify_queries.py`, `test_verify_baseline.py`
- `integration/test_full_fix.py`, `test_full_verify.py`

## Rule
No fix without a failing test first. TDD is mandatory for new functionality in `scripts/`.

[PROTOCOL]: Update this header when a new test file is added, a test category is introduced, or the marker system changes.

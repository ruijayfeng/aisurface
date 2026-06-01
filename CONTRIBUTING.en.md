# Contributing

Welcome to contribute to aisurface!

## Issues

- **Bug**: use the `Bug report` template
- **Feature request**: use the `Feature request` template
- **Question**: use the `Question` template

## Pull Requests

1. Fork → change → PR
2. One PR per change
3. All PRs must pass CI (ruff + pytest)
4. Add tests covering your change

## Dev environment

```bash
git clone https://github.com/ruijayfeng/aisurface.git
cd aisurface
pip install -e ".[dev]"
pytest
```

## Adding a new GEO check

`scripts/scanner.py` + `scripts/cli.py` are the main extension points.

Each check must:
- Run without crashing on 2 eval fixtures
- Add a fixture in `tests/integration/test_full_audit.py`
- Update `references/readme-checklist.md`

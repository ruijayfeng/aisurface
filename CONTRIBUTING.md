# 贡献指南

欢迎为 aisurface 贡献！

## 提 issue

- **Bug**: 用 `Bug report` 模板
- **功能建议**: 用 `Feature request` 模板
- **问题咨询**: 用 `Question` 模板

## 提 PR

1. Fork → 改 → PR
2. 一个 PR 一个改动
3. 所有 PR 必须过 CI（ruff + pytest）
4. 添加测试覆盖你的改动

## 开发环境

```bash
git clone https://github.com/ruijayfeng/aisurface.git
cd aisurface
pip install -e ".[dev]"
pytest
```

## 添加新的 GEO 检查

`scripts/scanner.py` + `scripts/cli.py` 是主要扩展点。

每个检查必须：
- 跑在 2 个 eval fixture 上不 crash
- 在 `tests/integration/test_full_audit.py` 添加 fixture
- 更新 `references/readme-checklist.md`

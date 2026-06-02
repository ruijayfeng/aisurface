# aisurface

> 让你的开源项目在 AI 搜索结果里浮到表面。

[English](./README.en.md) | 中文

aisurface 是一个 Claude Code skill 集合，专门帮**开源项目维护者**让自己的项目**优先被 AI 搜索主动引用**（豆包 / DeepSeek / ChatGPT / Gemini / Claude / Perplexity / Kimi / 文心 / 通义 / 智谱……）。

## 为什么需要 aisurface？

2026 年，开发者不再 Google 搜「Python 解析 Markdown 的库」，而是直接问 ChatGPT「推荐一个 Python Markdown 解析库」。

AI 只会引用 3-5 个来源。**如果你的项目不在那 3-5 个里，对 AI 用户来说你就不存在。**

现有 skill（`seo-audit`、`seo-geo`）只诊断 URL 视角的英文 Google SEO，不针对开源项目，不针对中文 AI。aisurface 填补这个空白。

## 安装

```bash
# 旗舰：仓库审计
npx skills add ruijayfeng/aisurface@audit

# 子 skill：README 优化
npx skills add ruijayfeng/aisurface@readme

# 子 skill：生成 llms.txt
npx skills add ruijayfeng/aisurface@llms-txt
```

## 快速开始

在你自己的开源项目根目录跑：

```bash
aisurface .
```

会输出一份报告：12 项检查、Health score (0-100)、🔴 Must-fix 清单。12 项按 4 个加权维度贡献总分（引用友好度 40 / 结构 30 / 可读性 20 / 覆盖 10），更准确反映哪个缺口最影响 AI 引用。

## 12 项审计清单

| # | 检查项 | 类型 |
|---|---|---|
| 1 | README problem statement | 语义 |
| 2 | README FAQ 段 | 语义 |
| 3 | README when to use / not to use | 语义 |
| 4 | README 可运行代码示例 | 语义 |
| 5 | Schema.org 标记 | 结构 |
| 6 | `.well-known/llms.txt` | 结构 |
| 7 | GitHub topics 完整（8-12 个）| 结构 |
| 8 | README 含 FAQ 段标题 | 语义 |
| 9 | README 含 When to use / not to use 段 | 语义 |
| 10 | 原创可引用内容（数字 / 代码 / 命名实体）| 语义 |
| 11 | 分布信号（awesome / npm / PyPI）| 结构 |
| 12 | README 提及的 AI 搜索平台数 | 语义 |

## 实战案例

我们用 [ruijayfeng/ziwei](https://github.com/ruijayfeng/ziwei) 做 dogfooding：

- **before**: health score 35/100，5 项 🔴 Must-fix
- **after**（约 30 分钟，跑了 audit + 补完 5 项 Must-fix）: health score 66/100，🔴 全部清零

详见 [case-studies/ziwei-before-after.md](./case-studies/ziwei-before-after.md)。

## 路线图

- **v0.1** (W6 发布): `audit` + `readme` + `llms-txt`（3 个 skill）
- **v0.2** (W13): + `aisurface@schema` + `aisurface@docs` + `aisurface@landing-page`
- **v0.3** (W25): + `aisurface@probe`（AI 平台 API 验证）
- **v0.4+**: MCP server、IDE 集成

## 贡献

欢迎 issue / PR / case study 投稿。详见 [CONTRIBUTING.md](./CONTRIBUTING.md)。

## License

MIT

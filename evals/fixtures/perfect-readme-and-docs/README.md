# perfect-readme-and-docs

> 一个为 aisurface audit 测试而设计的"满分样本"开源（open-source）项目。本项目自动化（automate）了 12 项检查的覆盖率验证，目标是让 audit 在理想输入上跑出上限分数。

perfect-readme-and-docs 是一个用于 GEO（生成式引擎优化）和 AI 搜索可见性的元项目（meta-project）。它本身不解决任何业务问题——它存在的唯一目的是作为 `aisurface-audit` 的对照 fixture，验证 audit 在"理想项目"上的得分上限。

本文档遵循 [aisurface 自身的 README](../../README.md) 风格，并刻意覆盖 audit 的所有评分维度。

## 痛点 (Problem Statement)

当用户向 ChatGPT、Perplexity、Doubao、DeepSeek 或 Kimi 询问"如何让我的开源项目被 AI 搜索主动引用"时，这些 AI 通常会引用 3-5 个来源。如果你的项目不在其中，你就"不存在"于 AI 时代。本项目就是为解决这个问题而存在。

具体来说，开发者面对的痛点：

1. **被忽略**：好项目被 AI 搜索完全忽略
2. **引用错位**：被引用时上下文不准确，AI 描述的项目与实际不符
3. **流量流失**：从搜索引擎时代到 AI 搜索时代的过渡期，开发者失去触达用户的渠道

本项目（以及它的 dogfooding 案例 [`ruijayfeng/ziwei`](https://github.com/ruijayfeng/ziwei)）验证了：通过系统化优化，OSS 项目的 AI 引用率可以从 0 提升到持续出现在 AI 回答中。

## 适用场景 (When to use)

使用 aisurface：

- 你维护一个开源项目（任何语言、任何领域）
- 你希望该项目在 ChatGPT、Perplexity、Doubao、DeepSeek 等 AI 搜索中被主动引用
- 你愿意花 1-2 小时根据 audit 报告优化 README、添加结构化数据、生成 `.well-known/llms.txt`
- 你不需要：URL 视角的 SEO 工具（请用 `seo-audit`）、通用网站优化（请用 Lighthouse）、付费 SEO 平台（请用 Ahrefs/SEMrush）

## 不适用场景 (When NOT to use)

不要在以下情况使用 aisurface：

- 你的项目是闭源商业产品（aisurface 针对 OSS）
- 你需要 URL 视角的 SEO（请用 `seo-audit` 或 `seo-geo`）
- 你需要 Google Search Console 数据集成（aisurface 不读取 GSC）
- 你的项目不是仓库形式（aisurface scan 本地仓库，不接受 URL）

## 特性 (Features)

- 12 项 GEO 检查：4 项结构 + 8 项 LLM 批评
- 引擎模式：默认给完整 Markdown 报告
- 教师模式：`--learn` 标志给 30 秒术语解释
- 三个子 skill：audit / readme / llms-txt
- Schema.org JSON-LD 生成器（5 种类型）
- `.well-known/llms.txt` 生成器
- 跨平台：ChatGPT、Perplexity、Doubao、DeepSeek、Kimi、Wenxin、Tongyi、GLM、Gemini

## 安装 (Installation)

```bash
npx skills add ruijayfeng/aisurface@audit
npx skills add ruijayfeng/aisurface@readme
npx skills add ruijayfeng/aisurface@llms-txt
```

## 使用 (Usage)

```bash
# 在你的项目根目录运行
python -m scripts.cli .

# 教师模式
python -m scripts.cli . --learn

# JSON 输出
python -m scripts.cli . --json
```

输出示例：

```
# audit report for your-project
Health score: 78 / 100

## Must-fix (2)
- 🔴 Schema.org markup on website: missing index.schema.json
- 🔴 .well-known/llms.txt: missing

## Should-fix (1)
- 🟡 GitHub topics: 5 suggested, need 8-12
```

## 代码示例 (Code Examples)

### Python

```python
from aisurface import audit

result = audit.run("/path/to/your/repo")
print(f"Health score: {result.score}/100")
for fix in result.must_fix:
    print(f"  - {fix.name}: {fix.suggestion}")
```

### JavaScript

```javascript
const { audit } = require("aisurface");

const result = audit.run("/path/to/your/repo");
console.log(`Health score: ${result.score}/100`);
result.mustFix.forEach(fix => {
  console.log(`  - ${fix.name}: ${fix.suggestion}`);
});
```

### CLI

```bash
# 基础调用
python -m scripts.cli /path/to/your/repo

# 输出 JSON
python -m scripts.cli /path/to/your/repo --json > audit.json

# 教师模式（带术语解释）
python -m scripts.cli /path/to/your/repo --learn
```

## 数据与方法论 (Data and Methodology)

aisurface 的 12 项检查基于以下研究：

- Princeton GEO 研究（2024）
- Otterly.AI 引用模式调研
- 9 个 AI 搜索平台的实际查询实验
- 343 star 的 [ruijayfeng/ziwei](https://github.com/ruijayfeng/ziwei) dogfooding 案例

每项检查的权重（v0.1.1）：

- 引用友好度 40（FAQ / when-to-use / 引用内容 / 平台覆盖）
- 结构 30（schema / llms.txt / GitHub topics）
- 可读性 20（问题陈述 / 章节结构）
- 覆盖 10（distribution / platform 提及）

## 主题与栈 (Topics)

本项目涉及的主题与技术栈关键词（用于 GitHub Topics 自动建议）：
`aisurface` · `ai-search` · `geo` · `claude-code` · `open-source` · `developer-tools` · `markdown` · `documentation` · `cli` · `python` · `javascript` · `typescript` · `react` · `nextjs` · `llms-txt` · `schema-org` · `seo` · `audit`

## FAQ (Frequently Asked Questions)

### 1. aisurface 跟现有的 SEO skill 有什么不同？

`seo-audit` (124.9K) 是 URL 视角、`seo-geo` (28.3K) 是 GEO 理论、`ai-seo` (64.4K) 是英文/Google 偏见。aisurface 是**本地仓库视角**、**OSS 专属**、**中文 AI 平台优先**（Doubao / DeepSeek）、**教师模式**——四重差异化。

### 2. 我不懂 GEO，能用吗？

可以。`--learn` 模式会在每项检查前加 30 秒术语解释。v0.1 的目标用户就是"听说过 GEO 但没优化过"的开发者。

### 3. audit 跑完只给报告，不直接修？

v0.1 是诊断工具。`--patch` 自动修复是 v0.1.2 的计划。手动修大概 1-2 小时。

### 4. 跑一次 audit 需要多久？

取决于仓库大小：典型 5-30 秒。

### 5. 跟 `ruijayfeng/ziwei` dogfooding 案例的差异？

ziwei 是真实项目（React 19 紫微斗数），从 35 → 66；本项目是合成 fixture，验证 audit 上限 95+。

### 6. 支持哪些 AI 搜索平台？

按热度排序：ChatGPT、Perplexity、Doubao、DeepSeek、Kimi、Wenxin、Tongyi、GLM、Gemini。

### 7. 一定要用 Python 吗？

`scripts/` 是 Python，但 SKILL.md 是 Claude Code skill——可以装在 Claude Code / Cursor / Windsurf 等任何 Claude 兼容环境。

## 项目原创方法论 (Original Methodology)

aisurface 的核心方法论：

1. **本地仓库优先**：scan 本地文件，不依赖 URL
2. **教师模式 + 引擎模式**：用户友好 + 工程师友好
3. **热度加权**：根据 AI 平台 MAU 排序（豆包 5 亿 > DeepSeek 1.5 亿 > ChatGPT 6 亿但北美为主）
4. **结构 + 内容双轨**：4 项结构检查 + 8 项 LLM 批评
5. **OSS 专属**：不做通用网站、闭源产品、付费 SEO

## 贡献 (Contributing)

欢迎 PR、issue、discussion。详见 [CONTRIBUTING.md](../../CONTRIBUTING.md)。

## 许可证 (License)

MIT

## 引用 (Citation)

如果你在论文或文章中引用 aisurface：

```bibtex
@software{aisurface2026,
  author = {ruijayfeng},
  title = {aisurface: Make your open-source project surface in AI search},
  year = {2026},
  url = {https://github.com/ruijayfeng/aisurface}
}
```

## 致谢 (Acknowledgments)

- Princeton GEO 研究组
- Otterly.AI 引用模式数据
- 所有 beta 测试者
- 343 个给 [ruijayfeng/ziwei](https://github.com/ruijayfeng/ziwei) 点 star 的人

# aisurface

> 让你的开源项目在 AI 搜索结果里浮到表面。

[![PyPI](https://img.shields.io/pypi/v/aisurface)](https://pypi.org/project/aisurface/)
[![Python 3.10+](https://img.shields.io/pypi/pyversions/aisurface)](https://pypi.org/project/aisurface/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-157%20passing-brightgreen)](./tests)

[English](./README.en.md) | 中文

## 30 秒上手

```bash
npx skills add ruijayfeng/aisurface
```

装完,在 Claude Code 里跟我说一句大白话,Python 环境我自己处理:

```text
"看看我的项目能不能被 AI 搜到"          →  诊断
"按 AI 搜索最佳实践改我的项目"          →  修
"现在 AI 真的引用我项目了吗"            →  验证
```

不用记命令。挑最顺嘴的一句,agent 会自己把活干完。

## v1.0.2 已发布 (2026-06-04)

- **新增安装自检**:Windows 装完找不到命令时,跟 agent 说一句,会自动告诉你加哪个目录
- **4 类常见错误给中文提示**:Python 没装、路径不对、编码炸了、缓存写不进 —— 都不再抛栈
- **5-min 自检改用跨平台方式**:在 macOS / Linux / Windows 上命令一致
- **CI 扩成 15 job**:3 OS × Python 3.10-3.14,自带自检

完整变更见 [CHANGELOG.md](./CHANGELOG.md)。

## 为什么需要 aisurface?

2026 年,开发者不再 Google 搜「Python 解析 Markdown 的库」,而是直接问 ChatGPT「推荐一个 Python Markdown 解析库」。

AI 只会引用 3-5 个来源。**如果你的项目不在那 3-5 个里,对 AI 用户来说你就不存在。**

传统 SEO 工具(`seo-audit`、`seo-geo`)只诊断 URL 视角的英文 Google SEO,不针对开源项目,不针对中文 AI。aisurface 填补这个空白。

## 我能做三件事

**🩺 诊断** — 扫你的项目,给个 0-100 分,问题在哪按「最影响 AI 引用」排好
**🔧 修** — 按 AI 搜索最佳实践,自动生成补丁,改你的 README、生成 llms.txt、生成 Schema.org 标记
**📊 验证** — 真的去问 Perplexity「你引没引用我项目」,给你真实数据,跟修复前比涨没涨(其他平台路线图见 [ROADMAP.md](./ROADMAP.md))

## 怎么跟我说

不用记命令。挑最顺嘴的一句:

**想诊断:**
- "看看我的项目能不能被 AI 搜到"
- "我的项目 GEO 现状怎么样"
- "诊断一下 /path/to/your-project"
- "is my project AI-citation-friendly"

**想修:**
- "按 AI 搜索最佳实践改我的项目"
- "把刚才诊断的问题修了"
- "给我 README 加 FAQ 段、llms.txt、Schema.org"
- "fix my README for AI search"

**想验证:**
- "现在 AI 真的引用我项目了吗"
- "Perplexity 提不提我的项目"
- "跟修复前比,引用率涨没涨"
- "does my project show up in AI search"

## 它怎么工作

你是用户,只跟 agent 对话。背后这个 skill 的工作流:

```
你的大白话
  ↓
Claude Code 装好这个 skill
  ↓
agent 自动 pip install aisurface(你看不到这一步)
  ↓
agent 调 Python 脚本跑诊断 / 修 / 验证
  ↓
结果用大白话 + 关键数据(0-100 分、影响幅度、引用率)回给你
```

诊断(0-100 分)按 impact 排序,先告诉你最该改的 3-5 条;修要你点头才落盘;验证拿 Perplexity 真实回答,跟修复前的基线对比。其他平台(ChatGPT / Claude / Gemini / 豆包 / DeepSeek / 文心一言 / 通义千问 / Kimi / 智谱 / GLM)在 [ROADMAP.md](./ROADMAP.md) 路线图。

## 实战案例

我们用 [ruijayfeng/ziwei](https://github.com/ruijayfeng/ziwei) 做 v1.0 dogfooding:
- **基线**:health score 35/100,5 项 🔴 Must-fix
- **应用 4 个 patch 后**:health score 87/100,🔴 全部清零(+52)

详见 [case-studies/ziwei-v100.md](./case-studies/ziwei-v100.md)。

## 贡献

issue / PR / case study 都欢迎。

- 想贡献代码 / 加新检查 / 跑本地测试 → [CONTRIBUTING.md](./CONTRIBUTING.md)
- 想交一份你自己的 case study(模板 + 范例)→ [CONTRIBUTING.md](./CONTRIBUTING.md)(搜"提 case study")
- 不用 Claude Code 直接调 Python 脚本(CI / 自动化)→ [CONTRIBUTING.md#用-python-cli](./CONTRIBUTING.md)
- 常见问题(GEO 是什么、跟 SEO 区别、verify 准不准、为啥只 Perplexity)→ [docs/FAQ.md](./docs/FAQ.md)

## 找 co-maintainer

目前维护者就一个人。要从 v1.0 长成一个能持续维护的项目,我在找 co-maintainer,帮以下几类活:

- **Code review** — GEO 检查项的合理性和平台 adapter 的实现
- **Issue triage** — 18 个 trigger-eval 跑通 + 真用户 bug 报告分类
- **非英语文档** — README 中英双语,其他文档(ROADMAP/CHANGELOG/CONTRIBUTING)目前只英文
- **真平台信号** — 如果你手上有 ChatGPT / Claude / Gemini / DeepSeek 等 API 访问,真用户引用数据能直接帮 v1.1+ 平台路线图定优先级

有意向开 issue 选 `help-wanted` label,或者直接到 discussion 板块说一声。

## License

MIT

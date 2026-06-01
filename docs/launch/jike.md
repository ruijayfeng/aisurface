<!--
[INPUT]: none (standalone content draft)
[OUTPUT]: 即刻 (Jike) post draft (Chinese, short-form)
[POS]: docs/launch/'s 即刻 draft, consumed by manual posting to okjk.co
[PROTOCOL]: Update this header when changed
-->

---
task: 26
target: 即刻 (Jike)
status: draft
date: 2026-06-02
notes: 即刻 short-form post, 200-500 字; use real case-study numbers (35→66, not 42→92)
---

# 即刻 Post — aisurface v0.1.0

## 标题 (可选)

```
做了个 Claude Code skill 集合：让开源项目在 AI 搜索里被主动引用
```

## 正文 (复制即可，~290 字)

```
做了个 Claude Code skill 集合，叫 aisurface，让开源项目在 AI 搜索里被主动引用。

起因是发现：开发者现在不再 Google 搜「Python Markdown 解析库」，而是直接问 ChatGPT「推荐一个 Python Markdown 解析库」。AI 只会引用 3-5 个来源。如果你的项目不在那 3-5 个里，对 AI 用户来说你就不存在。

而现有 skill（seo-audit、seo-geo）只诊断 URL 视角的英文 Google SEO，不针对开源项目，不针对中文 AI（豆包、DeepSeek、Kimi、文心、通义、智谱）。aisurface 填补这个空白。

3 个核心能力：
- 12 项 GEO 审计（4 项结构 + 8 项语义）
- 教师模式（--learn），不懂 GEO 也能用
- 一键生成 .well-known/llms.txt

我用它 dogfood 自己的 343 star 项目 ruijayfeng/ziwei（紫微斗数 web app，React 19 + TS）：跑完审计 + 应用 5 个 🔴 Must-fix，health score 从 35/100 涨到 66/100，耗时约 30 分钟。

仓库：github.com/ruijayfeng/aisurface
安装：npx skills add ruijayfeng/aisurface@audit

求试用反馈，欢迎把 before/after 案例投稿到 README。
```

## 发帖节奏建议

- **最佳时段**：工作日早高峰 8:30-10:00，或晚高峰 21:00-23:00。即刻的活跃高峰在通勤和睡前。
- **避免时段**：周末凌晨、工作日下午 14:00-16:00（午睡档）、国家法定假日。
- **建议日期**：发布日选在工作日（周二到周四效果最好），和 HN 帖错开 12 小时（先发即即刻，第二天再发 HN）。

## 评论互动

- **响应时限**：2 小时内必须回复每一条评论。即刻的推荐算法对「24 小时内评论密度」非常敏感，沉默 = 沉帖。
- **回复风格**：用对话口吻，不要复制 README 的营销话术。即刻用户最反感「官方账号腔」。
- **争议处理**：如果有人质疑「这不是 SEO 吗」，直接说：「是 SEO 进化版。Google 看关键词 + 链接，AI 看问题匹配 + 来源权威。我们 12 项检查里有一半是 AI 引用特有的（llms.txt、原创可引用内容、Schema.org 语义标记等）。」
- **如果有人问「为什么不做成 URL 视角」**：直接说「URL 视角有 seo-audit、seo-geo 做得很好。aisurface 只做 OSS 仓库视角，做深不做广。」

## 不要做的事

- **不要堆 emoji**：即刻读者普遍反感动辄 🎉🚀✨ 开头，正文里偶尔一个就够了。
- **不要用 markdown 标题**：即刻的 markdown 渲染会破，前面用纯文字 + 短横线列表就行。
- **不要@大 V 求转发**：会被降权，社区里口碑差。
- **不要贴代码块超过 5 行**：即刻不是技术博客，超出部分用「详见 README」引导到 GitHub。

## 发帖前自检

- [ ] 字数在 200-500 之间（当前正文 ~290 字）
- [ ] 链接是 `github.com/ruijayfeng/aisurface` 短格式，不是 `https://github.com/...`
- [ ] 真实数字 35→66 与 `case-studies/ziwei-before-after.md` 一致
- [ ] 没有点名竞品 skill（seo-audit、seo-geo 提了名，但仅作「已存在」语境，不是攻击）
- [ ] 没有承诺 4 hours / 92 分这种计划里的虚高数字

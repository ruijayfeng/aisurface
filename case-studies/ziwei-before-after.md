# Case Study: ruijayfeng/ziwei (紫微知道)

**Project**: [ruijayfeng/ziwei](https://github.com/ruijayfeng/ziwei) (343 stars)
**Type**: Open-source Zi Wei Dou Shu (紫微斗数) web app
**Stack**: React 19 + TypeScript + Vite

## Before aisurface

**Health score**: 35 / 100

### 🔴 Must-fix (5 items)

1. **Schema.org markup on website** (impact +20%)
2. **`.well-known/llms.txt` present** (impact +15%)
3. **README has FAQ section** (impact +15%)
4. **README when to use / not to use** (impact +10%)
5. **Original citable content** (impact +10%)

## After applying aisurface recommendations

**Health score**: 66 / 100

### What changed

1. **Added `index.schema.json`** with SoftwareApplication schema
2. **Generated `.well-known/llms.txt`** with project details, docs, optional links
3. **Added FAQ section** to README (8 Q&A covering common AI queries)
4. **Added "When to use / When NOT to use"** section to README
5. **Added "研究与数据" + "项目原创方法论"** sections (original citable content)

## Results

- Health score: 35 → 66
- 🔴 Must-fix count: 5 → 0 (target)
- Total work: ~30 minutes (automated checks + simple file additions)
- The `aisurface` workflow (audit → fix → re-audit) made the iteration loop tight.

## What we did NOT do (and why)

- Did NOT migrate the website to Next.js (out of scope for this case study)
- Did NOT add a separate `docs/comparison.md` (kept in README only, since `docs/` is for end-user documentation)

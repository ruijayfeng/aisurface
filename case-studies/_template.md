# Case study: [YOUR-PROJECT-NAME]

> Copy this file to `case-studies/<your-project-slug>.md`, fill in the brackets, and
> open a PR. Keep it concrete: real numbers, real diffs, real timelines. A 2-paragraph
> case study with `+20 → 78` and a "what I changed" list is more useful than 10 paragraphs
> of theory.
>
> See [ziwei-v100.md](./ziwei-v100.md) for a complete worked example.

**Date**: YYYY-MM-DD
**Project**: [github-user/repo](https://github.com/...) — one-line description, star count
**Stack**: e.g. Python 3.12 + Click + httpx
**aisurface version**: e.g. v1.0.2

## Baseline

```bash
$ python -m scripts.cli audit . --no-color
```

- `aisurface audit .` score: **N / 100**
- Sub-scores (if reported by your version):
  - Citation-Friendliness: NN / 100
  - Distribution: NN / 100
  - Readability: NN / 100
  - Structure: NN / 100
- Top 🔴 Must-fix items (paste the audit output's top 3-5):
  1. ...
  2. ...
  3. ...

## Applied patches

What `aisurface fix .` actually wrote (or what you manually applied):

1. **<patch name>** — `<file>` (e.g. "FAQ section in README" / "new `.well-known/llms.txt`")
2. ...
3. ...
4. ...

Wall-clock time: ~Ns (the `fix` command is local + deterministic; only `verify` hits the network)

## After

Re-run audit:

```bash
$ python -m scripts.cli audit . --no-color
```

- `aisurface audit .` score: **N / 100**  (delta: +N)
- Sub-scores: ...
- 🔴 Must-fix items remaining: 0 (or list any that need manual work)

## (Optional) Real citation lift

If you have a `PERPLEXITY_API_KEY` and want to measure the actual citation-rate change:

```bash
export PERPLEXITY_API_KEY=pplx-...
python -m scripts.cli verify .       # first run: stores baseline in ~/.aisurface/baselines/
# ... apply patches ...
python -m scripts.cli verify .       # second run: diffs against baseline
```

Paste the `[perplexity] baseline cited X/Y → current cited A/B (delta +N)` line.

## What surprised me

One paragraph: what you expected vs what you got, or what was easier / harder than
you thought. (E.g. "I assumed the FAQ template would be too generic, but the
project-type detection in `fix/faq.py` actually picked up on the words 'CLI' and
'parser' and produced usable Q&A." Or: "The 5-line lift was all from `llms.txt` —
everything else was a wash.")

## What I'd improve in aisurface

Honest feedback welcome. If a check fired that didn't actually help, or a patch
generated something you had to rewrite, say so — that's the most valuable signal
for the rubric. Open an issue with `case-study-feedback` label, or just append
a paragraph here.

---

**Template version**: 2026-06-04. Used for [ziwei-v100.md](./ziwei-v100.md).

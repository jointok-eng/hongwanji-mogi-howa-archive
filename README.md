# Hongwanji Mogi — Howa Archive / 法話アーカイブ

Multilingual Buddhist sermon texts (Jodo Shinshu) published by **Honpa Hongwanji Mogi das Cruzes**, Brazil.

| | |
|---|---|
| **Author** | Josuke Inoue (釋 穣信) — Kaikyoshi / Resident Minister |
| **Organization** | Honpa Hongwanji Mogi das Cruzes |
| **Languages** | Japanese (ja), Portuguese (pt), English (en), Spanish (es) |
| **Period** | June 2023 – August 2026 |
| **Canonical site** | https://hongwanjimogi.org.br/howa.php |
| **License** | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |

## About / 概要

This repository mirrors the temple's monthly dharma talks (*howa* / *pequena conversa sobre budismo*) in plain Markdown for open access, research, and AI-readable archiving.

Each file includes YAML front matter with title, date, author, language, and a canonical URL on the official website.

## Directory structure

```
howa-archive/
  README.md
  2023/
  2024/
  2025/
  2026/
```

File naming: `YYYY-MM-{ja|pt|en|es}.md` (e.g. `2026-08-pt.md`). Duplicate months use a suffix: `2025-03-2-ja.md`.

## Medium / Substack mirror (pt + en)

Ready-to-publish mirror posts for [Medium](https://medium.com) and [Substack](https://substack.com) are in [`mirror/`](mirror/README.md) (78 articles). Each ends with *Originally published at https://hongwanjimogi.org.br/...*

## Citation

> Inoue, Josuke (釋 穣信). *[Sermon title]*. Honpa Hongwanji Mogi das Cruzes, YYYY-MM. https://hongwanjimogi.org.br/howa.php

## Mirror platforms

When republishing on Medium, Substack, or elsewhere, please link back:

> Originally published at https://hongwanjimogi.org.br/howa.php?id=…

## Regeneration

From the parent `howa/` folder:

```bash
python Github/generate_markdown_archive.py
```

#!/usr/bin/env python3
"""Generate Medium / Substack mirror posts (Portuguese and English)."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

MIRROR_ROOT = Path(__file__).resolve().parent
GITHUB_ROOT = MIRROR_ROOT.parent
HOWA_ROOT = GITHUB_ROOT.parent
ARCHIVE_SCRIPT = GITHUB_ROOT / "generate_markdown_archive.py"

MIRROR_LANGS = ["pt", "en"]
POSTS_DIR = MIRROR_ROOT / "posts"
MANIFEST_PATH = MIRROR_ROOT / "manifest.json"

sys.path.insert(0, str(GITHUB_ROOT))
spec = importlib.util.spec_from_file_location("archive_gen", ARCHIVE_SCRIPT)
archive = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(archive)


def build_footer(canonical_url: str, lang: str) -> str:
    if lang == "pt":
        org = "Honpa Hongwanji Mogi das Cruzes"
        byline = "Rev. Josuke Inoue (釋 穣信) — Monge responsável do Templo Honpa Hongwanji de Mogi das Cruzes"
    else:
        org = "Honpa Hongwanji Mogi das Cruzes"
        byline = "Rev. Josuke Inoue (釋 穣信) — Resident Minister, Honpa Hongwanji Mogi das Cruzes"

    return (
        "\n\n---\n\n"
        f"*Originally published at [{canonical_url}]({canonical_url})*\n\n"
        f"{byline}\n\n"
        f"{org} · https://hongwanjimogi.org.br/\n"
    )


def build_post_markdown(title: str, body: str, canonical_url: str, lang: str) -> str:
    subtitle = (
        "Pequena conversa sobre budismo — Honpa Hongwanji Mogi das Cruzes"
        if lang == "pt"
        else "A Brief Talk on Buddhism — Honpa Hongwanji Mogi das Cruzes"
    )
    return f"# {title}\n\n*{subtitle}*\n\n{body}{build_footer(canonical_url, lang)}"


def main() -> None:
    manifest: list[dict] = []

    for lang in MIRROR_LANGS:
        lang_dir = POSTS_DIR / lang
        lang_dir.mkdir(parents=True, exist_ok=True)
        for old in lang_dir.glob("*.md"):
            old.unlink()

    for year, items in archive.REGISTRY.items():
        for filename, m_id in items:
            path = HOWA_ROOT / filename
            meta = archive.parse_m_id(m_id)
            if meta is None:
                continue
            langs = archive.parse_sermon_php(path)
            if not langs:
                continue

            for lang in MIRROR_LANGS:
                block = langs.get(lang)
                if not block:
                    continue
                hreflang = archive.HREFLANG[lang]
                canonical = archive.build_url(meta["sermon_id"], lang)
                slug = f"{meta['file_slug']}-{hreflang}"
                body = archive.html_to_markdown_body(block["content"])
                content = build_post_markdown(block["title"], body, canonical, lang)
                out_path = POSTS_DIR / lang / f"{slug}.md"
                out_path.write_text(content, encoding="utf-8")

                manifest.append(
                    {
                        "slug": slug,
                        "year": year,
                        "language": hreflang,
                        "title": block["title"],
                        "date": meta["published"],
                        "canonical_url": canonical,
                        "file": str(out_path.relative_to(MIRROR_ROOT)).replace("\\", "/"),
                        "medium_tags": [
                            "Buddhism",
                            "Jodo Shinshu",
                            "Dharma Talk",
                            "Brazil",
                            "Honpa Hongwanji",
                        ],
                    }
                )

    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Created {len(manifest)} mirror posts in {POSTS_DIR}")


if __name__ == "__main__":
    main()

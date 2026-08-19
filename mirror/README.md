# Medium / Substack Mirror — Howa Archive

Portuguese and English sermon texts mirrored from [hongwanjimogi.org.br](https://hongwanjimogi.org.br/howa.php) for SEO and AI discoverability on high-authority platforms.

## Generated files

```
posts/
  pt/   ← Portuguese articles (39)
  en/   ← English articles (39)
manifest.json
published_medium.json   ← created after Medium publish
```

Each article ends with:

> *Originally published at https://hongwanjimogi.org.br/howa.php?id=…*

## 1. Regenerate mirror posts

After updating sermons on the website:

```bash
python howa/Github/mirror/generate_mirror_posts.py
```

## 2. Medium (automated)

1. Log in to Medium → **Settings → Security → Integration tokens**
2. Create a token
3. Copy `.env.example` to `.env` and paste the token
4. Publish:

```bash
cd howa/Github/mirror
python publish_medium.py --latest      # newest sermon only (monthly workflow)
python publish_medium.py --slug 2026-08-pt
python publish_medium.py --all         # first-time bulk publish (78 posts)
```

Posts are published as **public** with `canonicalUrl` pointing to the official site.

## 3. Substack (manual paste)

Substack has no public write API. For each new sermon:

1. Open Substack dashboard → **New post**
2. Open `posts/pt/YYYY-MM-pt.md` or `posts/en/YYYY-MM-en.md`
3. Paste the Markdown into the editor
4. Confirm the footer link to hongwanjimogi.org.br is present
5. Publish

Recommended: create two sections or newsletters — **Português** and **English**.

## Monthly workflow (recommended)

When a new sermon is added to the site:

```bash
python howa/Github/generate_markdown_archive.py
python howa/Github/mirror/generate_mirror_posts.py
cd howa/Github/mirror && python publish_medium.py --latest
# Then paste the same file into Substack (pt + en)
```

## License

Same as canonical site content. Link back to the original URL on every mirror.

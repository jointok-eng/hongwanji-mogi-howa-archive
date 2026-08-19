#!/usr/bin/env python3
"""
Publish mirror posts to Medium via Integration Token.

Setup:
  1. https://medium.com/me/settings/security → Integration tokens
  2. Copy .env.example to .env and set MEDIUM_INTEGRATION_TOKEN

Usage:
  python publish_medium.py --all
  python publish_medium.py --slug 2026-08-pt
  python publish_medium.py --latest
"""

from __future__ import annotations

import argparse
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

MIRROR_ROOT = Path(__file__).resolve().parent
MANIFEST_PATH = MIRROR_ROOT / "manifest.json"
LOG_PATH = MIRROR_ROOT / "published_medium.json"
ENV_PATH = MIRROR_ROOT / ".env"


def load_env() -> None:
    if not ENV_PATH.exists():
        return
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def api_request(token: str, method: str, url: str, payload: dict | None = None) -> dict:
    data = None
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Medium API error {exc.code}: {body}") from exc


def get_user_id(token: str) -> str:
    data = api_request(token, "GET", "https://api.medium.com/v1/me")
    return data["data"]["id"]


def load_log() -> dict:
    if LOG_PATH.exists():
        return json.loads(LOG_PATH.read_text(encoding="utf-8"))
    return {}


def save_log(log: dict) -> None:
    LOG_PATH.write_text(json.dumps(log, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def publish_one(token: str, user_id: str, entry: dict) -> str:
    post_path = MIRROR_ROOT / entry["file"]
    content = post_path.read_text(encoding="utf-8")
    payload = {
        "title": entry["title"],
        "contentFormat": "markdown",
        "content": content,
        "tags": entry.get("medium_tags", ["Buddhism"]),
        "publishStatus": "public",
        "canonicalUrl": entry["canonical_url"],
        "license": "all-rights-reserved",
    }
    data = api_request(token, "POST", f"https://api.medium.com/v1/users/{user_id}/posts", payload)
    return data["data"]["url"]


def main() -> None:
    load_env()
    token = os.environ.get("MEDIUM_INTEGRATION_TOKEN", "").strip()
    if not token:
        raise SystemExit(
            "MEDIUM_INTEGRATION_TOKEN is not set.\n"
            "Create howa/Github/mirror/.env from .env.example and add your Medium token."
        )

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    log = load_log()

    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true", help="Publish all posts not yet published")
    parser.add_argument("--slug", help="Publish one slug, e.g. 2026-08-pt")
    parser.add_argument("--latest", action="store_true", help="Publish newest post only")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.slug:
        selected = [e for e in manifest if e["slug"] == args.slug]
    elif args.latest:
        selected = [max(manifest, key=lambda e: (e["date"], e["slug"]))]
    elif args.all:
        selected = manifest
    else:
        parser.error("Use --all, --latest, or --slug")

    if not selected:
        raise SystemExit("No posts matched.")

    if args.dry_run:
        for entry in selected:
            print(f"Would publish: {entry['slug']} -> {entry['title']}")
        return

    user_id = get_user_id(token)
    published = 0
    for entry in selected:
        slug = entry["slug"]
        if slug in log:
            print(f"Skip (already published): {slug} -> {log[slug]}")
            continue
        print(f"Publishing: {slug} ...")
        url = publish_one(token, user_id, entry)
        log[slug] = url
        save_log(log)
        published += 1
        print(f"  -> {url}")
        time.sleep(2)

    print(f"Done. Published {published} new Medium post(s).")


if __name__ == "__main__":
    main()

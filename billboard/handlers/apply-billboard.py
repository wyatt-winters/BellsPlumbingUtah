#!/usr/bin/env python3
"""Replace visible page content with Saddle Up AI billboard while preserving SEO <head>."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "_archive-original"
BODY = (ROOT / "partials/billboard-body.html").read_text()
BILLBOARD_CSS = '<link rel="stylesheet" href="/css/billboard.css">'
INTER_FONT = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">'
)


def extract_head(html: str) -> str | None:
    match = re.search(r"<head\b[^>]*>.*?</head>", html, re.IGNORECASE | re.DOTALL)
    return match.group(0) if match else None


def transform_head(head: str) -> str:
    head = re.sub(
        r'\s*<link[^>]+href="/css/site\.css[^"]*"[^>]*>\s*',
        "\n",
        head,
        flags=re.IGNORECASE,
    )
    head = re.sub(
        r'<link[^>]+fonts\.googleapis\.com/css2\?family=Fraunces[^>]+>\s*',
        "",
        head,
        flags=re.IGNORECASE,
    )
    head = re.sub(
        r'<meta name="theme-color" content="[^"]*">',
        '<meta name="theme-color" content="#0B0B0F">',
        head,
        flags=re.IGNORECASE,
    )
    if "billboard.css" not in head:
        head = head.replace("</head>", f"  {BILLBOARD_CSS}\n</head>")
    if "family=Inter" not in head:
        head = head.replace("</head>", f"  {INTER_FONT}\n</head>")
    return head


def transform_file(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    head = extract_head(original)
    if not head:
        print(f"skip (no head): {path.relative_to(ROOT)}")
        return False

    archive_path = ARCHIVE / path.relative_to(ROOT)
    if not archive_path.exists():
        archive_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, archive_path)

    new_html = (
        "<!DOCTYPE html>\n"
        '<html lang="en">\n'
        f"{transform_head(head)}\n"
        f"{BODY}\n"
        "</html>\n"
    )
    path.write_text(new_html, encoding="utf-8")
    print(f"updated: {path.relative_to(ROOT)}")
    return True


def main() -> None:
    html_files = sorted(ROOT.rglob("*.html"))
    updated = 0
    for path in html_files:
        if "_archive-original" in path.parts:
            continue
        if transform_file(path):
            updated += 1
    print(f"\nDone. Updated {updated} HTML files.")
    print(f"Originals backed up under: {ARCHIVE}")


if __name__ == "__main__":
    main()

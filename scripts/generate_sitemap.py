#!/usr/bin/env python3
"""
Regenerates sitemap.xml and the "## Pages" section of llms.txt from the
canonical URL, <title>, and <meta name="description"> already present in
each *.html file at the project root. Run this after adding or removing a
page, before deploying:

    python3 scripts/generate_sitemap.py

No dependencies beyond the standard library.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://wagereality.com"


def extract(html, pattern, group=1):
    m = re.search(pattern, html, re.S)
    return m.group(group).strip() if m else None


def scan_pages():
    pages = []
    for path in sorted(ROOT.glob("*.html")):
        html = path.read_text(encoding="utf-8")
        canonical = extract(html, r'<link rel="canonical" href="([^"]+)">')
        title = extract(html, r"<title>([^<]*)</title>")
        description = extract(html, r'<meta name="description" content="([^"]*)">')
        if not canonical:
            print(f"warning: {path.name} has no <link rel=\"canonical\">, skipping", file=sys.stderr)
            continue
        pages.append({
            "file": path.name,
            "url": canonical,
            "title": title or path.name,
            "description": description or "",
            "is_home": canonical.rstrip("/") == SITE,
        })
    # homepage first, then everything else alphabetically by URL
    pages.sort(key=lambda p: (not p["is_home"], p["url"]))
    return pages


def render_sitemap(pages):
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for p in pages:
        priority = "1.0" if p["is_home"] else "0.8"
        lines.append("  <url>")
        lines.append(f"    <loc>{p['url']}</loc>")
        lines.append("    <changefreq>monthly</changefreq>")
        lines.append(f"    <priority>{priority}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def render_llms_pages_section(pages):
    lines = ["## Pages"]
    for p in pages:
        title = p["title"].split(" — ")[0].split(" | ")[0].strip()
        desc = p["description"] or "No description available."
        lines.append(f"- [{title}]({p['url']}): {desc}")
    return "\n".join(lines) + "\n"


def update_llms_txt(pages):
    llms_path = ROOT / "llms.txt"
    existing = llms_path.read_text(encoding="utf-8") if llms_path.exists() else ""
    marker = "## Pages"
    head = existing.split(marker)[0].rstrip() if marker in existing else existing.rstrip()
    new_content = head + "\n\n" + render_llms_pages_section(pages)
    llms_path.write_text(new_content, encoding="utf-8")


def main():
    pages = scan_pages()
    if not pages:
        print("No pages with a canonical URL found — nothing written.", file=sys.stderr)
        sys.exit(1)

    (ROOT / "sitemap.xml").write_text(render_sitemap(pages), encoding="utf-8")
    update_llms_txt(pages)

    print(f"Wrote sitemap.xml and llms.txt from {len(pages)} page(s):")
    for p in pages:
        print(f"  {p['file']:<28} -> {p['url']}")


if __name__ == "__main__":
    main()

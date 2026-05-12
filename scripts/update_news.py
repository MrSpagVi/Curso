#!/usr/bin/env python3
"""Update docs/actualidad.md with latest items from RSS feeds.

Run manually:
    pip install feedparser
    python scripts/update_news.py

Or via GitHub Actions (see .github/workflows/news.yml).
"""

import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import feedparser
except ImportError:
    print("Install feedparser: pip install feedparser", file=sys.stderr)
    sys.exit(1)

# Edit this list to add/remove sources. Format: (Display name, RSS URL)
FEEDS = [
    ("Real Instituto Elcano", "https://www.realinstitutoelcano.org/feed/"),
    ("BBC News Mundo", "https://feeds.bbci.co.uk/mundo/rss.xml"),
    ("El País — Internacional", "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/internacional/portada"),
    ("Le Monde Diplomatique (Cono Sur)", "https://www.eldiplo.org/feed/"),
    ("The Conversation — Global", "https://theconversation.com/articles.atom"),
    ("Nueva Sociedad", "https://nuso.org/articulo/feed/"),
]

MAX_ITEMS_PER_FEED = 5
SUMMARY_MAX_LEN = 240
OUTPUT_FILE = Path(__file__).resolve().parent.parent / "docs" / "actualidad.md"


def fetch_feed(url, name):
    """Fetch and parse a single RSS feed. Returns parsed feed or None."""
    try:
        feed = feedparser.parse(url)
        if feed.bozo and not feed.entries:
            print(f"[WARN] {name}: feed invalido o vacio ({url})", file=sys.stderr)
            return None
        if not feed.entries:
            print(f"[WARN] {name}: sin entradas ({url})", file=sys.stderr)
            return None
        return feed
    except Exception as e:
        print(f"[WARN] {name}: error ({e})", file=sys.stderr)
        return None


def fmt_date(entry):
    """Extract a YYYY-MM-DD date string from an entry."""
    for attr in ("published_parsed", "updated_parsed"):
        t = entry.get(attr)
        if t:
            try:
                return datetime(*t[:6]).strftime("%Y-%m-%d")
            except (ValueError, TypeError):
                continue
    return ""


def clean_summary(text):
    """Strip HTML tags and truncate."""
    if not text:
        return ""
    # Basic HTML strip (no need for full parser for RSS summaries)
    import re
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > SUMMARY_MAX_LEN:
        text = text[:SUMMARY_MAX_LEN].rsplit(" ", 1)[0] + "…"
    return text


def render_markdown():
    """Build the markdown content for actualidad.md."""
    lines = [
        "---",
        "title: Actualidad",
        "---",
        "",
        "# Actualidad",
        "",
        "Últimos titulares de fuentes que dictan agenda en ciencia política y geopolítica. "
        "Actualizado automáticamente cada día (vía GitHub Actions).",
        "",
        f"_Última actualización: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}_",
        "",
    ]

    for name, url in FEEDS:
        feed = fetch_feed(url, name)
        lines.append(f"## {name}")
        lines.append("")

        if not feed or not feed.entries:
            lines.append(f"_Sin datos en esta ejecución. Visitar fuente: [{url}]({url})_")
            lines.append("")
            continue

        for entry in feed.entries[:MAX_ITEMS_PER_FEED]:
            title = (entry.get("title") or "Sin título").strip()
            link = entry.get("link") or "#"
            date_str = fmt_date(entry)
            summary = clean_summary(entry.get("summary") or entry.get("description") or "")

            date_suffix = f" · *{date_str}*" if date_str else ""
            lines.append(f"- **[{title}]({link})**{date_suffix}")
            if summary:
                lines.append(f"  - {summary}")
        lines.append("")

    return "\n".join(lines)


def main():
    print(f"Updating {OUTPUT_FILE}...")
    content = render_markdown()
    OUTPUT_FILE.write_text(content, encoding="utf-8")
    print(f"[OK] Wrote {len(content)} chars to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

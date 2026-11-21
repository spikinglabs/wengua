"""Generate llms.txt and llms-full.txt for the built docs site.

llms.txt (https://llmstxt.org) gives AI assistants and answer engines a
clean map of the site; llms-full.txt has every page's Markdown in one file.
Run after `zensical build`: python scripts/llms_txt.py
"""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SITE = ROOT / "site"


def flatten(nav, section=None):
    """Yield (section, title, path) for every page in the Zensical nav."""
    for item in nav:
        if isinstance(item, str):
            yield section, None, item
            continue
        for title, value in item.items():
            if isinstance(value, list):
                yield from flatten(value, title)
            else:
                yield section, title, value


def page_title(md: str, fallback: str) -> str:
    m = re.search(r"^#\s+(.+)$", md, flags=re.M)
    return m.group(1).strip() if m else fallback


def page_summary(md: str) -> str:
    """The page's front-matter description, else its first plain paragraph."""
    m = re.match(r"^---\n(.*?)\n---\n", md, flags=re.S)
    if m:
        d = re.search(r"^description:\s*(.+)$", m.group(1), flags=re.M)
        if d:
            return d.group(1).strip().strip("\"")
    body = re.sub(r"^---\n.*?\n---\n", "", md, flags=re.S)
    for block in re.split(r"\n\s*\n", body):
        block = block.strip()
        if block and not block.startswith(("#", "!!!", ">", "|", "```", "-", "<")):
            return re.sub(r"\s+", " ", re.sub(r"\*\*|\*|`", "", block))
    return ""


def page_url(site_url: str, path: str) -> str:
    slug = path.removesuffix(".md")
    if slug == "index":
        return site_url
    slug = slug.removesuffix("/index")
    return f"{site_url}{slug}/"


def main() -> None:
    config = tomllib.loads((ROOT / "zensical.toml").read_text())["project"]
    site_url = config["site_url"].rstrip("/") + "/"
    pages = list(flatten(config["nav"]))

    lines = [f"# {config['site_name']}", "", f"> {config['site_description']}", ""]
    full = list(lines)
    groups: dict[str, list[str]] = {}
    for section, title, path in pages:
        md = (DOCS / path).read_text()
        title = title or page_title(md, path)
        summary = page_summary(md)
        entry = f"- [{title}]({page_url(site_url, path)})" + (f": {summary}" if summary else "")
        groups.setdefault(section or "Docs", []).append(entry)
        body = re.sub(r"^---\n.*?\n---\n", "", md, flags=re.S).strip()
        full += ["", "---", "", f"Source: {page_url(site_url, path)}", "", body]
    for section, entries in groups.items():
        lines += ["", f"## {section}", "", *entries]

    SITE.mkdir(exist_ok=True)
    (SITE / "llms.txt").write_text("\n".join(lines).strip() + "\n")
    (SITE / "llms-full.txt").write_text("\n".join(full).strip() + "\n")
    print(f"llms.txt: {len(pages)} pages")


if __name__ == "__main__":
    main()

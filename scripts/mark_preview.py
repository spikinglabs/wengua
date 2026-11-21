"""Mark a built site as a PR preview so search engines never index it.

Adds <meta name="robots" content="noindex, nofollow"> and a visible banner to
every page, a Disallow-all robots.txt, and an X-Robots-Tag header (_headers is
read by Cloudflare Pages). Canonical links still point at the production site.
Usage: python scripts/mark_preview.py <pr-number>
"""

from __future__ import annotations

import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"


def main() -> None:
    pr = sys.argv[1] if len(sys.argv) > 1 else "?"
    meta = '<meta name="robots" content="noindex, nofollow">'
    banner = (
        '<div style="background:#b45309;color:#fff;text-align:center;'
        'padding:.4rem;font:600 .8rem/1.4 system-ui,sans-serif">'
        f"Preview of pull request #{pr}. Not the published site.</div>"
    )
    count = 0
    for page in SITE.rglob("*.html"):
        html = page.read_text()
        if meta in html:
            continue
        html = html.replace("<head>", f"<head>\n{meta}", 1)
        body_end = html.find(">", html.find("<body")) + 1
        html = html[:body_end] + banner + html[body_end:]
        page.write_text(html)
        count += 1
    (SITE / "robots.txt").write_text("User-agent: *\nDisallow: /\n")
    (SITE / "_headers").write_text("/*\n  X-Robots-Tag: noindex, nofollow\n")
    (SITE / "sitemap.xml").unlink(missing_ok=True)
    print(f"Marked {count} pages as preview #{pr}")


if __name__ == "__main__":
    main()

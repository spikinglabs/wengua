"""Turn the built site into redirects to the canonical domain, for the old
GitHub Pages address (spikinglabs.github.io/wengua). Each page keeps its path,
points its canonical link at wengua.allo.land and refreshes there at once."""

from __future__ import annotations

import html
import shutil
import sys
from pathlib import Path

SITE = Path(sys.argv[1] if len(sys.argv) > 1 else "site")
OUT = Path(sys.argv[2] if len(sys.argv) > 2 else "site-redirect")
TARGET = "https://wengua.allo.land/"

if OUT.exists():
    shutil.rmtree(OUT)
for page in SITE.rglob("*.html"):
    rel = page.relative_to(SITE).as_posix()
    path = rel[: -len("index.html")] if rel.endswith("index.html") else rel
    url = html.escape(TARGET + path)
    dest = OUT / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(
        f'<!doctype html><html><head><meta charset="utf-8"><title>Moved to wengua.allo.land</title>'
        f'<link rel="canonical" href="{url}"><meta http-equiv="refresh" content="0; url={url}">'
        f'<meta name="robots" content="noindex"></head>'
        f'<body><p>Wengua has moved to <a href="{url}">{url}</a>.</p></body></html>\n',
        encoding="utf-8",
    )
(OUT / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")
print(f"Wrote redirects for {sum(1 for _ in OUT.rglob('*.html'))} pages to {OUT}")

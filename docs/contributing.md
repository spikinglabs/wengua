---
description: "How to work on the Wengua docs with Zensical and keep them current."
---

# Contributing

## Working on the docs

The site is built with [Zensical](https://zensical.org). Pages live in `docs/` and the navigation is in `zensical.toml`.

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-docs.txt
zensical serve        # live preview at http://localhost:8000
zensical build --clean
```

Every pull request builds the site. Every push to `main` deploys it to <https://wengua.allo.land>, the only canonical copy. One Cloudflare Worker (`worker/`) serves the site as static assets and the hosted MCP server at `/mcp`. The old address, `spikinglabs.github.io/wengua`, now redirects every page there.

### Pull request previews

Each pull request from this repository gets a preview at `https://pr-<number>.wengua-docs-preview.pages.dev`, linked in a bot comment. Previews live on a separate Cloudflare Pages domain and are never indexed: every page carries `noindex`, the server sends `X-Robots-Tag: noindex`, `robots.txt` disallows everything, there is no sitemap, and canonical links point at the production site.

Previews and production use two repository secrets: `CLOUDFLARE_API_TOKEN` (with *Cloudflare Pages: Edit*, *Workers Scripts: Edit*, and *Workers Routes: Edit* and *DNS: Edit* on allo.land) and `CLOUDFLARE_ACCOUNT_ID`. Without them, the preview job is skipped.

### Search and AI visibility (SEO and GEO)

- Give every page a `description` in its front matter. It becomes the meta description and the summary in `llms.txt`.
- `scripts/llms_txt.py` writes [`llms.txt`](https://llmstxt.org) and `llms-full.txt` after each build, so AI assistants and answer engines can read the docs cleanly.
- `docs/robots.txt` allows all crawlers, including AI crawlers, and points at the sitemap.
- Only the production site is canonical. Never publish copies of the docs elsewhere without `noindex`.

**Keep the docs current:** a pull request that changes behavior, adds a tool or finishes a milestone should update the matching page and the [Roadmap](roadmap.md) in the same PR.

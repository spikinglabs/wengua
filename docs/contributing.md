# Contributing

## Working on the docs

The site is built with [Zensical](https://zensical.org). Pages live in `docs/` and the navigation is in `zensical.toml`.

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-docs.txt
zensical serve        # live preview at http://localhost:8000
zensical build --clean
```

Every pull request builds the site, and every push to `main` deploys it to GitHub Pages.

**Keep the docs current:** a pull request that changes behavior, adds a tool or finishes a milestone should update the matching page and the [Roadmap](roadmap.md) in the same PR.

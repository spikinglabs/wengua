# Wengua 问卦

The accurate, open I Ching (易经 / 周易) for every AI. Code casts, the model reads. 排卦归程序，解卦归模型。

- **Sourced Chinese text** in traditional and simplified script, collated character by character with a Song edition ([data/SOURCES.md](data/SOURCES.md)).
- **Fair casting** with three coins or the full yarrow-stalk method, exact classical odds, a secure random source, and a record of every coin and stalk.
- **Zhu Xi's rules** decide which texts to read, so the model never has to guess.
- **Works everywhere:** an MCP server, a CLI and libraries for Python and TypeScript.

```bash
npx -y wengua cast -q "What should I understand about this move?"
uvx wengua lookup 水雷屯
```

As an MCP server (Claude Desktop, Claude Code, Cursor, VS Code…):

```json
{ "mcpServers": { "wengua": { "command": "npx", "args": ["-y", "wengua"] } } }
```

| Path | What |
|---|---|
| `data/` | The dataset (`wengua-data`), sources and collation. CC BY-SA 4.0 |
| `python/` | `pip install wengua`: library, CLI, MCP server. MIT |
| `js/` | `npm install wengua`: library, CLI, MCP server. MIT |
| `spec/` | Shared test vectors and MCP tool definitions |
| `docs/` | The documentation site: <https://wengua.allo.land/> |
| `worker/` | The Cloudflare Worker serving the site and the hosted MCP server at <https://wengua.allo.land/mcp> |

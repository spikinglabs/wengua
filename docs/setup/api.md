---
description: "Use Wengua 问卦 from your own app: the hosted MCP server with the Claude API and OpenAI API, or the Python and TypeScript libraries."
---

# APIs and libraries

## Claude API

The Messages API can call a remote MCP server directly. It needs both `mcp_servers` and a matching `mcp_toolset` tool, plus the MCP client beta:

```python
import anthropic

client = anthropic.Anthropic()

response = client.beta.messages.create(
    model="claude-opus-5-5",
    max_tokens=16000,
    betas=["mcp-client-2025-11-20"],
    mcp_servers=[{"type": "url", "url": "https://wengua.allo.land/mcp", "name": "wengua"}],
    tools=[{"type": "mcp_toolset", "mcp_server_name": "wengua"}],
    messages=[{"role": "user", "content": "Cast an I Ching hexagram. My question: what should I focus on this year?"}],
)
print(response.content)
```

With curl, send the header `anthropic-beta: mcp-client-2025-11-20` and the same `mcp_servers` and `tools` fields in the body.

## OpenAI API

The Responses API takes a remote MCP server as a tool:

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-5",
    tools=[{
        "type": "mcp",
        "server_label": "wengua",
        "server_url": "https://wengua.allo.land/mcp",
        "require_approval": "never",
    }],
    input="Cast an I Ching hexagram. My question: what should I focus on this year?",
)
print(response.output_text)
```

## Agent frameworks

Any framework with an MCP client can use the hosted URL (Streamable HTTP) or start `uvx wengua` over stdio. To skip the network entirely, call the library from your own tool.

## Python and TypeScript libraries

```bash
pip install wengua
```

```python
import wengua

reading = wengua.cast(question="What should I understand about this move?")
print(reading["primary"]["name"]["zh_hant"])
for text in reading["selection"]["texts"]:
    print(text["role"], text["text"]["zh_hant"])
```

The same API is in the npm package `wengua` (Node.js 20 or later). See [Core library](../ecosystem/core.md) for the full API, and give your model the texts in `selection.texts` rather than letting it recall them.

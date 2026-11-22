---
description: "在你自己的应用中使用问卦 Wengua：通过 Claude API 和 OpenAI API 调用托管 MCP 服务，或使用 Python 与 TypeScript 库。"
---

# API 与程序库

## Claude API

Messages API 可以直接调用远程 MCP 服务。需要同时提供 `mcp_servers` 和对应的 `mcp_toolset` 工具，并开启 MCP client beta：

```python
import anthropic

client = anthropic.Anthropic()

response = client.beta.messages.create(
    model="claude-opus-5-5",
    max_tokens=16000,
    betas=["mcp-client-2025-11-20"],
    mcp_servers=[{"type": "url", "url": "https://wengua.allo.land/mcp", "name": "wengua"}],
    tools=[{"type": "mcp_toolset", "mcp_server_name": "wengua"}],
    messages=[{"role": "user", "content": "帮我起一卦：今年我应当把重心放在哪里？"}],
)
print(response.content)
```

用 curl 时，发送请求头 `anthropic-beta: mcp-client-2025-11-20`，并在请求体里带上同样的 `mcp_servers` 和 `tools` 字段。

## OpenAI API

Responses API 可以把远程 MCP 服务当作工具：

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
    input="帮我起一卦：今年我应当把重心放在哪里？",
)
print(response.output_text)
```

## 智能体框架

任何带 MCP 客户端的框架都可以使用托管网址（Streamable HTTP），或通过 stdio 启动 `uvx wengua`。想完全不联网，就在你自己的工具里调用程序库。

## Python 与 TypeScript 库

```bash
pip install wengua
```

```python
import wengua

reading = wengua.cast(question="这次搬家我应当明白什么？")
print(reading["primary"]["name"]["zh_hans"])
for text in reading["selection"]["texts"]:
    print(text["role"], text["text"]["zh_hans"])
```

npm 包 `wengua`（Node.js 20 或更高版本）提供同样的 API。完整 API 见 [核心库](../ecosystem/core.md)。请把 `selection.texts` 里的原文交给模型，而不是让它凭记忆背诵。

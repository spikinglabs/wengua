---
description: "How the Wengua dataset, core library, Agent Skill, MCP server, reading card and CLI fit together, and which one to use."
---

# Ecosystem overview

Every Wengua surface is a thin layer over the same dataset and core, so a reading is identical whether it comes from a skill, the CLI or the hosted server.

```mermaid
flowchart TD
  D[Dataset<br/>wengua-data] --> C[Core library<br/>TypeScript + Python]
  C --> S[Agent Skill]
  C --> L[Local MCP<br/>npx / uvx]
  C --> R[Hosted MCP<br/>Cloudflare Workers]
  C --> X[CLI]
  R --> A[Reading card<br/>MCP App]
  L --> A
  S --> U[Claude · ChatGPT · Codex · Cursor · Copilot]
  L --> U
  R --> U
```

## Which one should I use?

| You are… | Use |
|---|---|
| Chatting in Claude.ai or ChatGPT | The hosted MCP server (paste a URL) |
| Using Claude Code, Codex, Cursor or Copilot | The Agent Skill, or the local MCP server |
| In a terminal or scripting | The CLI |
| Building your own app | The core library or the dataset |

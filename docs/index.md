---
description: "Wengua 问卦 lets Claude, ChatGPT, Codex, Cursor and any MCP client consult the I Ching (易经) with the authentic Chinese text in traditional and simplified script, and fair, verifiable casting."
---

# Wengua 问卦

**The accurate, open I Ching (易经) for every AI.**

Wengua lets people consult the *Book of Changes* from Claude, ChatGPT, Codex, Cursor or any MCP client. The program casts the hexagram and retrieves the texts. The AI only interprets.

> 排卦归程序，解卦归模型。

## Try it

- **In Claude.ai or ChatGPT:** add a custom connector with the URL `https://wengua.allo.land/mcp`.
- **In Claude Code:** `claude mcp add --transport http wengua https://wengua.allo.land/mcp`
- **In any MCP client:** `npx -y wengua` or `uvx wengua` ([setup](ecosystem/mcp.md)).
- **As an Agent Skill:** drop [`skills/wengua`](ecosystem/skill.md) into your agent.

## Why Wengua

- **Authentic texts.** The received Chinese text (卦辭, 爻辭 and the Ten Wings 彖/象/文言) in traditional and simplified script, collated character by character with a Song edition. Every hexagram cites its sources and records each editorial change.
- **Fair casting you can verify.** Three coins or the full yarrow-stalk method with the exact classical odds, a secure random generator, a record of every coin and stalk, and statistical tests in CI.
- **The right texts, every time.** Zhu Xi's rules pick which lines to read, so the AI never has to guess or invent a line.
- **Works everywhere.** One core behind an Agent Skill, a local MCP server, a free hosted MCP server, a reading card and a CLI.
- **Reflection, not prediction.** Readings are framed as prompts for thought, never as verdicts.

## The ecosystem

| Piece | What it is | Status |
|---|---|---|
| [Dataset](ecosystem/dataset.md) | All 64 hexagrams, every classical text in 繁 and 简, with sources | ✅ Chinese done; English planned |
| [Core library](ecosystem/core.md) | Casting, derivations, text selection and lookup in TypeScript and Python | ✅ Done |
| [Agent Skill](ecosystem/skill.md) | Drop-in skill for Claude and other agents | ✅ Done |
| [MCP server](ecosystem/mcp.md) | Local (`npx`/`uvx`) and hosted at `wengua.allo.land/mcp` | ✅ Done |
| [Reading card](ecosystem/card.md) | Inline hexagram card in Claude and ChatGPT | ✅ Done |
| [CLI](ecosystem/cli.md) | `wengua cast --json` for terminals and coding agents | ✅ Done |

Packages on npm and PyPI are coming soon. See the [Roadmap](roadmap.md).

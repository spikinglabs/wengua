---
description: "Wengua 问卦 lets Claude, ChatGPT, Codex, Cursor and any MCP client consult the I Ching (易经) with authentic Chinese texts, Legge's English and fair, verifiable casting."
---

# Wengua 问卦

**The accurate, open I Ching (易经) for every AI.**

Wengua lets people consult the *Book of Changes* from Claude, ChatGPT, Codex, Cursor or any MCP client. The program casts the hexagram and retrieves the texts. The AI only interprets.

> 排卦归程序，解卦归模型。

!!! warning "Status: design phase"
    Nothing is published yet. This site tracks the design and will be kept up to date as each piece ships. See the [Roadmap](roadmap.md).

## Why Wengua

- **Authentic texts.** The original Chinese (卦辞, 爻辞 and the Ten Wings 彖/象/文言), in traditional and simplified characters, with James Legge's public-domain English. Every line cites its source.
- **Plain-language notes.** Our own modern notes in 白话 and English, free to reuse under CC BY 4.0.
- **Fair casting you can verify.** Three coins or yarrow stalks with the traditional probabilities, a secure random generator, and statistical tests in CI.
- **Works everywhere.** One core behind an Agent Skill, a local MCP server, a free hosted MCP server and a bilingual reading card.
- **Reflection, not prediction.** Readings are framed as prompts for thought, never as verdicts.

## The ecosystem

| Piece | What it is | Status |
|---|---|---|
| [Dataset](ecosystem/dataset.md) | Sourced bilingual texts of all 64 hexagrams | Planned (M0) |
| [Core library](ecosystem/core.md) | Casting, derivations and lookup in TypeScript and Python | Planned (M1) |
| [Agent Skill](ecosystem/skill.md) | Drop-in skill for 70+ AI platforms | Planned (M2) |
| [MCP server](ecosystem/mcp.md) | Local (`npx`/`uvx`) and hosted | Planned (M2–M3) |
| [Reading card](ecosystem/card.md) | Interactive hexagram card in Claude and ChatGPT | Planned (M3) |
| [CLI](ecosystem/cli.md) | `wengua cast --json` for terminals and coding agents | Planned (M2) |

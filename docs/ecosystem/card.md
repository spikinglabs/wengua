---
description: "The Wengua reading card: an MCP Apps view that draws the cast hexagrams, changing lines and selected texts inline in Claude and ChatGPT."
---

# Reading card

An [MCP Apps](https://github.com/modelcontextprotocol/ext-apps) view, `ui://wengua/reading`, linked from the `cast` and `read_cast` tools. Clients that support MCP Apps show it inline under the answer. Others simply get the reading as text.

The card:

- draws the primary hexagram with its changing lines marked (○ old yang, ✕ old yin) and the relating hexagram beside it,
- lists the selected texts with their roles (主 leads, 輔 supports, 貞 and 悔 for three changing lines) and the rule that chose them,
- has a 繁體 / 简体 toggle, and starts in simplified script when the reading's `locale` asks for it,
- follows the host's theme colours and fonts, and marks seeded test readings.

It is a single HTML file with no external requests (`spec/reading-card.html`). It speaks the MCP Apps postMessage protocol directly, with no SDK.

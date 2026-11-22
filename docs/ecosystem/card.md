---
description: "The Wengua reading card: an MCP Apps view that draws the cast hexagrams, changing lines and selected texts inline in Claude and ChatGPT."
---

# Reading card

An [MCP Apps](https://github.com/modelcontextprotocol/ext-apps) view, `ui://wengua/reading/<hash>`, linked from the `cast` and `read_cast` tools. Clients that support MCP Apps show it inline under the answer. Others simply get the reading as text.

The card:

- draws the primary hexagram with its changing lines marked (○ old yang, ✕ old yin) and the relating hexagram beside it,
- lists the selected texts with their roles (主 leads, 輔 supports, 貞 and 悔 for three changing lines) and the rule that chose them,
- has a 繁體 / 简体 toggle, and starts in simplified script when the reading's `locale` asks for it,
- follows the host's theme colours and fonts, and marks seeded test readings.

It is a single HTML file with no external requests (`spec/reading-card.html`). It speaks the MCP Apps postMessage protocol directly, with no SDK.

How it talks to the host:

1. It sends `ui/initialize` (with `appInfo` and `appCapabilities`), then `ui/notifications/initialized`. It sends `initialized` even when the host rejects or never answers the request, after at most 1.5 seconds, because hosts hold back the tool data until they see it.
2. It draws the reading from `ui/notifications/tool-result`, using `structuredContent` or, failing that, the JSON in the text content.
3. It opens in the reader's script. In order, it uses the reader's own 繁/简 choice (remembered where the host allows storage), the `locale` the model passed to the tool, the host's locale (zh-CN, zh-SG and zh-MY mean simplified, zh-TW, zh-HK and zh-MO mean traditional), and otherwise traditional. When the reader switches script and the host supports `ui/update-model-context`, the card tells the model, so its later replies and casts use the same script.
4. It acknowledges host requests such as `ui/resource-teardown`, and follows `ui/notifications/host-context-changed`.
5. If no result arrives within 12 seconds, it says the reading is in the reply instead of showing "Casting…" forever. Some mobile apps render the card but don't deliver the result yet.

The `cast` and `read_cast` results also carry the card link in `_meta.ui.resourceUri`, for hosts that look for it there.

The card's URI ends in a hash of its HTML, so a client that caches UI resources picks up a new card as soon as it changes. The placeholder shows a small version label (such as "card 4"), which tells you which card a client is running.

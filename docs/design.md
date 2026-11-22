---
description: "The design of Wengua 问卦: positioning, dataset, core library, AI integrations, quality and build order."
---

# Wengua 问卦: design

Status: draft for review · 2026-11-22

Wengua lets people consult the I Ching (易经 / 周易) from any AI assistant or agent. The program casts the hexagram and retrieves the texts. The model only interprets. (排卦归程序，解卦归模型。)

This document sets out what Wengua stands for, how each part works, and the order we build it in.

---

## 1. Positioning

> **Wengua 问卦: the accurate, open I Ching for every AI.**
> The authentic Chinese text, faithful English, and modern plain-language notes in both languages. Fair casting you can verify. Works in Claude, ChatGPT, Codex, Cursor and any MCP client, with or without installing anything.

Principles:

- **Code casts, the model reads.** All randomness, hexagram relationships and text selection are done by code and returned with audit metadata. The model never invents a hexagram or a line text.
- **Sources first.** Every text unit carries its source, edition and any variant readings.
- **Reflection, not prediction.** The skill frames readings as reflection. It declines medical, legal and financial verdicts, and it never claims supernatural accuracy.
- **Bilingual by default.** Chinese is the canonical text. The response language follows the user.
- **Free to run.** No accounts and no server-side LLM. The hosted endpoint is stateless and cheap.

---

## 2. Feature design

### 2.1 Dataset (`data/`), published separately as `wengua-data`

One JSON file per hexagram, plus `trigrams.json`. They are generated into a single `iching.json` bundle and versioned with SemVer.

Each hexagram has:

- `number` (King Wen 文王序), `unicode` (䷀ U+4DC0…), `binary` (bottom to top, `"111111"`), `upper` / `lower` trigrams
- `name`: `{ zh_hant: "乾", zh_hans: "乾", pinyin: "qián", en: "The Creative / Force" }`
- `judgment` (卦辞), `tuan` (彖传), `image` (大象), `wenyan` (文言, only for 乾 and 坤)
- `lines[1..6]`: `{ position, label: "初九", text (爻辞), xiao_xiang (小象) }`. Hexagrams 1 and 2 also get `use_nine` / `use_six` (用九 / 用六).
- Every text unit has `zh_hant`, `zh_hans`, `en_legge`, `zh_plain` (our 白话), `en_plain` (our plain English) and `source` (`{ edition, ref, variants[] }`).

Sources:
- Chinese: the 通行本 based on the 武英殿本《周易正義》 edition, cross-checked against 四部叢刊 and Wikisource. Public domain.
- English: James Legge, *The Yi King* (Sacred Books of the East vol. XVI, 1882). Public domain.
- `zh_plain` and `en_plain`: written by us and reviewed by a human, released with the dataset under CC BY-SA 4.0.
- **Not used:** any modern translation or commentary that is still under copyright.

License: the dataset is CC BY-SA 4.0, because the digital transcriptions we build on are share-alike. The classical text itself is public domain. The code is MIT.

Validation (in CI): 64 hexagrams, 384 lines plus 用九/用六, binary ↔ number ↔ Unicode consistency, each line label (九/六, 初…上) matching its bit, simplified text matching an OpenCC conversion of the traditional text (with a reviewed list of exceptions), and no empty fields.

### 2.2 Core library (`wengua-core`, TypeScript and Python)

The same logic in two languages, verified against **one shared file of test vectors** so the implementations can't drift apart.

- **Casting methods**
  - `coins`: three coins, P(6, 7, 8, 9) = 1/8, 3/8, 3/8, 1/8. Records each coin flip.
  - `yarrow`: 大衍筮法, P(6, 7, 8, 9) = 1/16, 5/16, 7/16, 3/16. Simulates the actual stalk division, not just the final probabilities, so the steps can be replayed.
  - `manual`: the user enters six values from a physical cast (6/7/8/9, bottom to top), or coin faces.
  - Later: `meihua` (梅花易数 from time or numbers), clearly labeled as a different school.
- **Randomness**: a secure RNG (`crypto.getRandomValues` / `secrets`). `seed` is allowed only when the caller sets `mode: "test"`, and the output then says so. A chi-square test in CI checks the distributions.
- **Derivations**: 本卦, 动爻, 之卦, 互卦, 错卦, 综卦.
- **Text selection (取辞)**: 朱熹《易学启蒙》 rules by number of changing lines (0 to 6, including 用九/用六) is the default. Other conventions are opt-in and named, so the model knows which school it is applying.
- **Lookup**: by number, Chinese name (traditional or simplified), pinyin with or without tones, English name, Unicode symbol, binary, or trigram pair ("坎上震下").
- **Output**: a `Reading` object with `primary`, `changing_lines`, `relating`, `nuclear`, `selected_texts`, `method`, `audit` ({rng, per-coin or per-stalk record, timestamp, library and dataset versions}) and `locale`.

### 2.3 Integrations, all thin layers over the core

| Surface | Package | Who it's for | Notes |
|---|---|---|---|
| Agent Skill | `skills/wengua/` | Claude, ChatGPT, Codex, Cursor, Copilot (70+ platforms) | A `SKILL.md` plus a bundled script and data, with no server. It teaches the reading flow (§2.4). |
| Local MCP | `npx wengua` / `uvx wengua` | Claude Desktop/Code, Cursor, VS Code, Goose | stdio. Supports MCP 2026-07-28 (stateless) and earlier versions. |
| Remote MCP | `https://mcp.wengua.<domain>/mcp` | Claude.ai, ChatGPT and mobile users who can't install anything | Cloudflare Workers, stateless, no auth, rate-limited by IP, no logs of questions. |
| MCP App | `ui://wengua/reading/<hash>` | Claude and ChatGPT (both support MCP Apps) | An inline card that draws 本卦 → 之卦, highlights changing lines, has a 中/EN and 繁/简 toggle, and an optional coin or stalk replay animation. |
| CLI | `wengua cast --json` | Coding agents, terminal users | Comes free with the packages. |
| Data and docs | `wengua-data`, `llms.txt`, static site | Anyone building their own tool | The dataset on npm and PyPI, plus a static site with all 64 hexagrams, bilingual. |
| Directory listings | MCP Registry, Claude connectors, ChatGPT plugins, Smithery | Discovery | — |

MCP tools (kept small and task-shaped):

| Tool | Input | Returns |
|---|---|---|
| `cast` | `question` (optional but encouraged), `method` (coins/yarrow), `locale` | A `Reading`, plus the MCP App card when supported |
| `read_cast` | six line values or coin faces from a physical cast, `question` | A `Reading` |
| `lookup` | any identifier (number, name, pinyin, ䷀, binary, trigrams) | The hexagram with all its text layers |
| `relations` | hexagram, optional changing lines | 之/互/错/综 with their texts |

Resources: `wengua://hexagram/{n}`, `wengua://trigram/{name}`. Prompt: `reading`, a guided reading template.

### 2.4 Reading craft (the skill and prompt)

1. Help the user turn a vague worry into one clear, open question (e.g. "What should I understand about…" rather than yes/no).
2. Call `cast` (or `read_cast` for a physical cast). **Never invent or "re-roll" a result.** Suggest not recasting the same question soon (不再三), but don't enforce it in v1.
3. Present the hexagram: the symbol, its name in both languages, the line drawing and the changing lines.
4. Quote the selected Chinese text with its translation, and say which rule chose it.
5. Interpret by connecting the text and imagery to the user's situation. Keep the classical text clearly separate from our interpretation.
6. Close with one or two reflective prompts, not a verdict.
7. Boundaries: no medical, legal or financial verdicts, no predictions about third parties, and point people to real help when distress shows up.

### 2.5 Quality and trust

- Shared test vectors (TS ↔ Python), data validation and RNG distribution tests in CI.
- An **agent eval set**: about 30 scripted conversations checking that the model calls the tool, doesn't invent texts, quotes the right lines, answers in the user's language and respects the boundaries. Run on Claude and GPT models before each release.
- `SOURCES.md` documents editions, variant readings and every editorial choice.
- Privacy: the hosted server never stores questions; logs keep only counts.

---

## 3. Build order

| Milestone | Scope | Done when |
|---|---|---|
| **M0 Dataset** | 64 hexagrams × all classical layers + Legge; `SOURCES.md`; validators | CI checks pass and 10 hexagrams have been spot-checked by hand |
| **M1 Core** | TS + Python core, shared test vectors, RNG tests | Both implementations pass the same test vectors |
| **M2 Skill + local MCP + CLI** | `skills/wengua`, `npx wengua`, `uvx wengua`, `wengua` CLI | Works in Claude Code, Claude Desktop, Codex and Cursor; eval set v1 passes |
| **M3 Remote MCP + MCP App** | Cloudflare Worker, reading card | Works in Claude.ai and ChatGPT by pasting a URL |
| **M4 Plain-language notes** | `zh_plain` / `en_plain` for 64 hexagrams + 386 lines | Reviewed by a human |
| **M5 Distribution** | Publish to npm/PyPI, MCP Registry, Claude directory, ChatGPT plugins, static site + `llms.txt` | Listed and installable |
| Later | 梅花易数, an optional local-only reading journal, more languages (日本語, 한국어) | — |

M4 can run alongside M1 to M3. The tools work without the plain notes and simply leave those fields out.

## 4. Open questions

1. A domain for the hosted endpoint and the site (e.g. `wengua.dev` / `wengua.app`)?
2. Who reviews the Chinese plain-language notes?
3. Should the default English name style follow Legge ("Khien") or modern pinyin ("Qian")? Proposal: pinyin names, with Legge's text unchanged.

---
description: "The wengua command line for casting and looking up I Ching hexagrams, with traditional and simplified Chinese and JSON output for coding agents."
---

# CLI

Comes with both packages (`npx wengua …` or `uvx wengua …`, or `wengua …` once installed).

```bash
wengua cast -q "What should I understand about this move?" -m yarrow
wengua cast --json            # the full Reading as JSON, for coding agents
wengua read 9 8 7 7 8 6       # a physical cast, bottom line first
wengua lookup 乾為天
wengua                        # no arguments: run the MCP server over stdio
```

Output shows the hexagram drawn top to bottom, the changing lines, and the selected texts in traditional and simplified Chinese:

```text
䷶ 55 豐 / 丰 fēng · Abundance  →  ䷷ 56 旅 lǚ · The Wanderer
  ━━━   ━━━ ✕ 6
  ━━━   ━━━   8
  ━━━━━━━━━   7
  ━━━━━━━━━   7
  ━━━   ━━━   8
  ━━━━━━━━━ ○ 9

二爻變：以本卦二變爻之辭占，以上爻為主。
二爻变：以本卦二变爻之辞占，以上爻为主。
Two changing lines: read both lines of the primary hexagram; the upper one leads.
  [55 上六] (principal)
    豐其屋，蔀其家，闚其戶，闃其无人，三歲不覿，凶。
    丰其屋，蔀其家，闚其户，阒其无人，三岁不觌，凶。
  ...
```

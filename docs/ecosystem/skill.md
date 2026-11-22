---
description: "The Wengua Agent Skill for Claude, ChatGPT, Codex, Cursor and Copilot, and how it guides an I Ching reading."
---

# Agent Skill

A `SKILL.md` folder that follows the open [Agent Skills](https://agentskills.io) standard, so it works in Claude, ChatGPT, Codex, Cursor, GitHub Copilot and other platforms. It bundles the Python package and dataset (about 360 KB) and needs no server, no network and no install: only Python 3.10 or later.

The skill lives in [`skills/wengua/`](https://github.com/spikinglabs/wengua/tree/main/skills/wengua).

## Install

[Download wengua-skill.zip](https://wengua.allo.land/wengua-skill.zip){ .md-button .md-button--primary }

The zip is rebuilt from `main` on every deploy. Step-by-step instructions for each AI are in [Get started](../setup/index.md):

- **Claude.ai and the Claude apps:** Customize → Skills → + → Create skill → Upload a skill ([guide](../setup/claude.md#agent-skill)).
- **Claude Code:** unzip into `~/.claude/skills` ([guide](../setup/claude.md#claude-code)).
- **Codex:** `~/.agents/skills` · **Gemini CLI:** `~/.gemini/skills` · **GitHub Copilot:** `~/.copilot/skills` · **Cursor:** `~/.cursor/skills`.

The script inside is the same `wengua` CLI:

```bash
python3 scripts/run.py cast --json -q "What should I understand about this move?"
python3 scripts/run.py read --json 7 8 9 7 6 8
python3 scripts/run.py lookup --json 水雷屯
```

## How the skill guides a reading

1. Help the user frame one clear, open question.
2. Cast with the bundled script, or read a physical cast. Never invent or re-roll a result.
3. Show the hexagram, its names and the changing lines.
4. Quote the selected Chinese text, in traditional or simplified script to match the user, with a translation, and name the rule that selected it.
5. Interpret by connecting the text to the user's situation, keeping the classical text separate from interpretation.
6. Close with one or two reflective questions, not a verdict.

Boundaries: no medical, legal or financial verdicts, and no predictions about other people.

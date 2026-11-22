---
description: "适用于 Claude、ChatGPT、Codex、Cursor 和 Copilot 的问卦 Wengua Agent Skill，以及它如何引导一次占卦。"
---

# Agent Skill

一个带 `SKILL.md` 的文件夹，遵循开放的 [Agent Skills](https://agentskills.io) 标准，因此可用于 Claude、ChatGPT、Codex、Cursor、GitHub Copilot 等平台。它内含 Python 包和数据集（约 360 KB），不需要服务器、不联网、不用安装，只要 Python 3.10 或更高版本。

技能位于 [`skills/wengua/`](https://github.com/spikinglabs/wengua/tree/main/skills/wengua)。

## 安装

[下载 wengua-skill.zip](https://wengua.allo.land/wengua-skill.zip){ .md-button .md-button--primary }

每次部署都会从 `main` 重新打包。各家 AI 的详细步骤见 [快速上手](../setup/index.md)：

- **Claude.ai 和 Claude 应用：** Customize → Skills → + → Create skill → Upload a skill（[指南](../setup/claude.md#agent-skill)）。
- **Claude Code：** 解压到 `~/.claude/skills`（[指南](../setup/claude.md#claude-code)）。
- **Codex：** `~/.agents/skills` · **Gemini CLI：** `~/.gemini/skills` · **GitHub Copilot：** `~/.copilot/skills` · **Cursor：** `~/.cursor/skills`。

里面的脚本就是 `wengua` 命令行：

```bash
python3 scripts/run.py cast --json -q "这次搬家我应当明白什么？"
python3 scripts/run.py read --json 7 8 9 7 6 8
python3 scripts/run.py lookup --json 水雷屯
```

## 技能如何引导占卦

1. 帮用户把心事整理成一个清楚、开放的问题。
2. 用内置脚本起卦，或读取实物起卦的结果。绝不编造，也不重新起卦。
3. 显示卦象、卦名和变爻。
4. 按用户使用的字体（繁体或简体）引用选出的原文并附上翻译，说明是哪条规则选出的。
5. 把原文和用户的处境联系起来解读，并把经文与解读分开。
6. 以一两个引人反思的问题结尾，而不是下定论。

界限：不对医疗、法律或财务问题下结论，也不预测他人。

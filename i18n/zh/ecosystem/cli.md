---
description: "问卦 Wengua 命令行：起卦、查卦，输出繁简两体中文，并为编程智能体提供 JSON 输出。"
---

# 命令行

两个包都自带（`uvx wengua …` 或 `npx wengua …`，安装后直接用 `wengua …`）。

```bash
wengua cast -q "这次搬家我应当明白什么？" -m yarrow
wengua cast --json            # 完整结果的 JSON，供编程智能体使用
wengua read 9 8 7 7 8 6       # 实物起卦的结果，自下而上
wengua lookup 乾為天
wengua                        # 不带参数：通过 stdio 运行 MCP 服务
```

输出自上而下画出卦象，列出变爻，以及选出的繁简两体原文：

<!-- no-convert -->
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

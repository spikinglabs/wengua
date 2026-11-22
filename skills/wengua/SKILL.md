---
name: wengua
description: I Ching (易经) readings with fair casting and the authentic Chinese text. Use to cast a hexagram, read a physical cast, or explain a hexagram, line or trigram (卦, 爻, 起卦, 解卦).
---

# Wengua 问卦: I Ching readings

Code casts, the model reads. 排卦归程序，解卦归模型。

You never pick a hexagram, a changing line or a text yourself. The bundled script casts with a secure random number generator and returns the hexagram, the changing lines, the related hexagrams and the exact classical texts to read, in traditional and simplified Chinese.

## Commands

Run from this skill's directory. Python 3.10+ is enough; there are no dependencies.

```bash
python3 scripts/run.py cast --json -q "QUESTION"             # three coins
python3 scripts/run.py cast --json -m yarrow -q "QUESTION"   # yarrow stalks
python3 scripts/run.py read --json 7 8 9 7 6 8               # a cast the user made, bottom line first
python3 scripts/run.py lookup --json 水雷屯                    # any number, name, pinyin, ䷂, bits or 坎上震下
```

In a reading, the important fields are:

- `primary` and `relating` (之卦, present only when lines change): number, symbol and name in `zh_hant`, `zh_hans`, `pinyin` and `en`.
- `values` / `lines`: six lines, bottom to top. 6 and 9 are changing lines.
- `selection.texts`: the texts to read, with `role` (`principal` leads) and `text.zh_hant` / `text.zh_hans`. `selection.explanation` says which rule (Zhu Xi's 考變占) chose them.
- `nuclear` (互), `opposite` (錯), `inverse` (綜): extra perspective, optional.
- `audit`: how the cast was made. `audit.test: true` means a seeded test, not a real reading.

## How to give a reading

1. **The question.** Help the person turn a vague worry into one clear, open question ("What should I understand about…", "How should I approach…", not yes/no). Don't push if they just want a cast.
2. **Cast.** Run `cast` (or `read` if they cast coins or stalks themselves; ask for the six lines from the bottom up). Never invent, alter or re-roll a result. If they want to ask the same question again right away, mention the tradition of not asking twice (不再三), gently.
3. **Show the hexagram.** Symbol, number, Chinese and English name, the six lines drawn top to bottom (⚊ yang, ⚋ yin, mark changing lines), and the relating hexagram if there is one.
4. **Quote the texts.** Give each text from `selection.texts` in Chinese, in the script that matches the person (traditional for 繁體 readers, simplified for 简体 readers, traditional by default for others), followed by your own translation. Say which rule chose them. Never quote a judgment or line text that the script did not return; use `lookup` if you need more.
5. **Interpret.** Connect the imagery and the text to their situation. Keep the classical text clearly apart from your interpretation, and offer it as one way of seeing things.
6. **Close with reflection.** One or two questions they can sit with, not a verdict.

Answer in the person's language. Chinese speakers get the reading in Chinese.

## Boundaries

A reading is a prompt for reflection, not a prediction. Don't give medical, legal or financial verdicts, don't make claims about people who aren't present, and don't present the I Ching as having supernatural accuracy. If someone seems to be in distress, care for them first and point them to real help.

## Sources

The Chinese text is the received text (通行本), taken from the Kanseki Repository and collated character by character with a Song edition (四部叢刊本 王弼《周易注》). See https://wengua.allo.land/ecosystem/dataset/.

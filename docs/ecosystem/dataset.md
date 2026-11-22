---
description: "The open, sourced bilingual dataset of all 64 I Ching hexagrams: 卦辞, 爻辞, the Ten Wings and James Legge's English."
---

# Dataset

`wengua-data` is the foundation: one JSON record per hexagram plus the eight trigrams, published on npm and PyPI.

## Contents per hexagram

- King Wen number, Unicode symbol (䷀…䷿), six-bit binary (bottom to top), upper and lower trigrams
- Names in traditional and simplified Chinese, pinyin and English
- 卦辞 judgment, 彖传, 大象, 文言 (乾 and 坤 only)
- Six lines, each with its label (初九…上六), 爻辞 and 小象, plus 用九 / 用六
- For every text unit: `zh_hant` and `zh_hans` now, with `en_legge`, `zh_plain` and `en_plain` to follow
- `variants` (differences from the cross-check edition) and `source` links to the exact source files

## Sources

| Layer | Source | Status |
|---|---|---|
| Chinese (繁/简) | Kanseki Repository KR1a0001 《周易》 (received text), cross-checked character by character against Chinese Wikisource | ✅ Done |
| English | James Legge, *The Yî King* (1882), public domain | Planned |
| Plain notes | Written by Wengua contributors | Planned |

Every difference between the two Chinese editions is recorded in the hexagram's `variants` field and in `data/cross-check.json`. The editions, snapshots and editorial choices are documented in [`data/SOURCES.md`](https://github.com/spikinglabs/wengua/blob/main/data/SOURCES.md).

The dataset is licensed **CC BY-SA 4.0**. The classical text is in the public domain; the license covers the digital transcriptions it builds on and our structure and glosses.

We do **not** use any modern translation or commentary that is still under copyright.

## Validation

CI rebuilds the data from the committed source snapshots and fails if the result differs from what is committed. It then checks that there are 64 hexagrams and 384 lines plus 用九/用六, that binary, number, Unicode and trigrams agree, that each line label (九/六) matches its bit, that no field is empty, and that 乾 never turns into 干 in the simplified text.

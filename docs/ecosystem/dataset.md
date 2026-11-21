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
- For every text unit: `zh_hant`, `zh_hans`, `en_legge`, `zh_plain`, `en_plain` and a `source`

## Sources

| Layer | Source | License |
|---|---|---|
| Chinese | 通行本, 武英殿本《周易正義》, cross-checked with 四部叢刊 and Wikisource | Public domain (CC0) |
| English | James Legge, *The Yi King* (1882) | Public domain |
| Plain notes | Written by Wengua contributors | CC BY 4.0 |

We do **not** use Wilhelm-Baynes or any modern copyrighted translation or commentary.

## Validation

CI checks that there are 64 hexagrams and 384 lines plus 用九/用六, that binary, number and Unicode agree, that each line label matches its bit, and that the simplified text matches the traditional text through OpenCC (with a reviewed list of exceptions).

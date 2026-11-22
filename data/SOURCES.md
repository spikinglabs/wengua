# Sources and editorial choices

## Witnesses

| Role | Edition | Where |
|---|---|---|
| Base text | **Kanseki Repository (漢籍リポジトリ) KR1a0001 《周易》**, TLS edition: punctuated, standard characters | `sources/kanripo/` |
| Collation witness | **四部叢刊本 王弼《周易注》**, a photo-reprint of a Song edition, transcribed in Kanseki Repository KR1a0006 (branch `SBCK`) | `sources/witnesses/sbck/` |
| Cross-check | **Chinese Wikisource 《周易》**, one page per hexagram, pinned by revision id | `sources/wikisource/` |

Kanripo's `WYG` branch of KR1a0006 (四庫全書本) turned out to be the same transcription as `SBCK`, so it is kept in `sources/witnesses/wyg/` but does not count as a separate witness.

## How the text was checked

1. **Collation with the Song edition** (`scripts/data/collate.py`, output `collation-sbck.json`). The commentary is removed from the witness, then every text unit (卦辭, 彖, 大象, 爻辭, 小象, 用九/用六 and 文言) is aligned character by character inside the witness's text for that hexagram, ignoring punctuation. Differences in glyph only (異體字 such as 爲/為, 旣/既, 乗/乘) are listed in `sources/witnesses/orthographic-variants.tsv` and counted, not reported. About 12,500 characters are compared.
2. **Cross-check with Wikisource** (in `build.py`, output `cross-check.json` and each hexagram's `variants`).
3. **Two-against-one rule.** Where the Song edition and Wikisource agree against the base text, the received reading is restored. Each change is listed in `sources/emendations.tsv` and in the hexagram's `emendations` field, with the base reading kept. There are 23. Most are places where the TLS edition had adopted a later scholar's emendation, for example 比's 彖 (an inserted 比吉 and brackets), 隨's 彖 (隨之 for 隨時), 井's 彖 (往來井井), 震's 彖 (不喪匕鬯), 苞 for 包 in 蒙, 泰 and 否, and 利己 for 利已 in 大畜.

## What is left, and why

After the emendations, 11 differences with the Song edition remain. None meets the two-against-one rule.

- **Transcription errors in the witness** (kept as in the base text): 大過 九二 小象 天 for 夫; 中孚 九五 寜 for 攣; 中孚 上九 青/昔 for 音 and 聲 for 登; 小過 judgment 昔 for 音.
- **Readings where only one witness differs** (kept as in the base text by decision of the maintainer on 2026-11-22; to be revisited with a further witness, such as the 阮元 edition of 《周易正義》):
  - 賁 彖 剛柔交錯: the base and Wikisource have it, the Song edition does not.
  - 坎 九五 衹: the Song edition has 祇, Wikisource has 禔.
  - 大壯 九三 小象 final 也.
  - 乾 文言 乾元亨者 (Song edition 乾元者), and 坤 文言 無成 (Song edition 无成). Wikisource's 文言 is not compared, so these two have only two witnesses.
- **Gaps in the witness transcription:** part of 臨 (彖, 大象 and lines 1 to 3) is missing from the Kanripo transcription of the Song edition, so those units are checked against Wikisource only.

Wikisource still differs in 104 fields after the emendations. Almost all are glyph variants or readings found only in Wikisource.

## Editorial choices

- **Structure:** 卦辞, then 彖, 大象, the six lines each with its 小象, then 用九/用六 and 文言 for 乾 and 坤.
- **Hexagram names in the judgment:** for 履, 否, 同人 and 艮 the name is part of the first sentence (履虎尾, 否之匪人, 同人于野, 艮其背), so the judgment text includes it. 坎's judgment opens with 習坎.
- **乾's commentary:** the source gives 大象 and all 小象 as one block, which we split by sentence.
- **Punctuation:** we keep the source's punctuation, but remove the TLS citation marks 「」 inside 彖 and 象, and the 《》 around hexagram names. Quotation marks in 文言 are kept.
- **Simplified text:** generated with OpenCC (`t2s`), except that 乾 is never converted to 干, because in the Yijing it is always qián.
- **English names:** short glosses written for Wengua (CC BY-SA 4.0).

## English: Legge

Every judgment, Tuan, Image, line text, small image, 用九 and 用六 has `en_legge`: James Legge's translation from *The Yî King* (Sacred Books of the East XVI, 1882), public domain. It was rebuilt from three Internet Archive scans of the book and the proofread pages on English Wikisource, then corrected by hand. The witnesses and method are in [`sources/legge/README.md`](sources/legge/README.md). Legge's translation of the Wenyan (文言, his Appendix IV) is not included yet.

## Not used

No modern translation or commentary that is still under copyright.

## Planned

- Legge's translation of the Wenyan (文言), from Appendix IV of the same volume.
- Plain-language notes in modern Chinese and English, written for Wengua.

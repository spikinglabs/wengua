# Sources and editorial choices

## Primary text

**Kanseki Repository (漢籍リポジトリ), KR1a0001 《周易》**, base edition TLS. Snapshot of the 64 hexagram files from
<https://github.com/kanripo/KR1a0001>, stored in `sources/kanripo/`. This edition follows the standard received text (通行本) of the 王弼 and 孔穎達 tradition.

## Cross-check

**Chinese Wikisource, 《周易》**, one page per hexagram, stored in `sources/wikisource/` with the revision id on the first line. Each source URL in the data points at that exact revision.

Every judgment, line text, 彖, 大象, 小象 and 用九/用六 is compared character by character with punctuation ignored. Differences are listed in each hexagram's `variants` field and collected in `cross-check.json`. In the first build, 126 fields differed. Most are variant forms (群/羣, 无/無, 床/牀); a few are real readings (for example 剝 上九 得輿 against 德車, 困 九四 徐徐 against 荼荼), where the primary text keeps the received reading.

We chose Kanripo over Wikisource as primary because the Wikisource pages mix in readings from other editions without marking all of them.

## Editorial choices

- **Structure:** 卦辞, then 彖, 大象, the six lines each with its 小象, then 用九/用六 and 文言 for 乾 and 坤.
- **Hexagram names in the judgment:** for 履, 否, 同人 and 艮 the name is part of the first sentence (履虎尾, 否之匪人, 同人于野, 艮其背), so the judgment text includes it. 坎's judgment opens with 習坎.
- **乾's commentary:** the source gives 大象 and all 小象 as one block, which we split by sentence.
- **Punctuation:** we keep the source's punctuation, but remove the TLS citation marks 「」 inside 彖 and 象, and the 《》 around hexagram names. Quotation marks in 文言 are kept.
- **Simplified text:** generated with OpenCC (`t2s`), except that 乾 is never converted to 干, because in the Yijing it is always qián.
- **English names:** short glosses written for Wengua (CC BY-SA 4.0).

## Not used

No modern translation or commentary that is still under copyright.

## Planned

- James Legge, *The Yî King* (Sacred Books of the East XVI, 1882), public domain, as the English layer.
- Plain-language notes in modern Chinese and English, written for Wengua.

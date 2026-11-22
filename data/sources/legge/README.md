# Legge's English

`text.json` holds James Legge's English translation for every hexagram, keyed by King Wen number: the judgment (卦辭), the six line texts (爻辭) and 用九/用六 from his Text, the Tuan (彖) from his Appendix I, the Great Image (大象) and the small images of the lines (小象) from his Appendix II, and the 文言 of 乾 and 坤 from his Appendix IV. `scripts/data/build.py` adds each one to the dataset as `en_legge`.

**Work:** James Legge, *The Yî King*, The Sacred Books of the East, vol. XVI (Oxford: Clarendon Press, 1882; 2nd edition 1899). Public domain.

## How the text was made

No clean digital edition was available, so the text was rebuilt from three scans of the printed book on the Internet Archive and the proofread pages on English Wikisource:

| Witness | What it is |
|---|---|
| [`iching00jame`](https://archive.org/details/iching00jame) | Dover reprint of the 2nd edition (1899). Best OCR; the main witness. |
| [`sacredbooksofchi16conf`](https://archive.org/details/sacredbooksofchi16conf) | 1882 edition (Princeton copy). Second OCR witness. |
| [`sacredbooksofeas0016fmax`](https://archive.org/details/sacredbooksofeas0016fmax) | 1899 printing. Consulted where the first two disagree. |
| [Wikisource, *Sacred Books of the East - Volume 16*](https://en.wikisource.org/wiki/Index:Sacred_Books_of_the_East_-_Volume_16.djvu) | Proofread transcription. Used for hexagrams 1–19 where it matches the OCR text (pages for later hexagrams were not yet proofread). |

1. Each OCR text was split into the paragraphs of each hexagram, leaving out Legge's notes, page headers and paragraph numbers. In the appendices each hexagram starts with its Roman numeral; where a numeral was garbled, the hexagrams were aligned in order across the whole appendix.
2. The two main OCR witnesses were merged word by word; where they differ, the reading made of real English words wins.
3. For the judgments and lines of hexagrams 1–19 the proofread Wikisource text replaces the merge wherever the two agree closely (similarity of 0.9 or more), as a check that the merge is right.
4. Spelling was normalised to plain ASCII: Legge's diacritics in romanised names were dropped, hyphens broken across lines were joined, and quotation marks made straight. Legge's em dashes and his parentheses, which mark words he added to the Chinese, are kept.
5. Remaining OCR errors were corrected by hand against the scans (for example the end of 坤's judgment, which a page header had replaced, "mount Khi" in 升, "white mao grass" in 大過, garbled romanised names such as "Kieh" and "Kia Zan", missing quotation marks, and notes or verse renderings from Legge's notes that had run into the text).

`scripts/data/validate.py` checks that every judgment, Tuan, Image, line, small image and 文言 paragraph has an `en_legge` text with no stray characters or spacing errors. Corrections are welcome: compare with the scans above and open a pull request that edits `text.json`.

Legge's cross-references such as "(See Appendix III, i, 48.)" are kept as he printed them. His romanisation of hexagram names (Khien, Khwan, Kun…) is kept inside his text. The dataset's own `name.en` field holds Wengua's short English names instead.

## 文言 (Appendix IV)

Appendix IV is short (eight pages), so it was transcribed by hand from the 1882 scan and then compared word by word with both OCR witnesses; the only differences were OCR garbles of romanised names. Legge numbers its paragraphs 1–36 for 乾 and 1–10 for 坤. The dataset follows the paragraphs of the Chinese text instead, so his paragraphs are joined like this:

| 文言 paragraph | Legge, Appendix IV |
|---|---|
| 乾 1 | Section I, 1–3 |
| 乾 2–7 | 4–9 (one per line) |
| 乾 8 | 10–16 |
| 乾 9 | 17–23 |
| 乾 10 | 24–26 |
| 乾 11 | 27–29 and the first half of 30 |
| 乾 12 | the rest of 30, and 31–36 |
| 坤 1 | Section II, 1–4 and 5 up to "early discrimination." |
| 坤 2 | the rest of 5, and 6–10 |

Two of his paragraphs straddle a break in the Chinese. Section I, 30 is split at its semicolon (君子以成德為行，日可見之行也 ends 乾 11), so the first half ends with a full stop and the second starts "But the force of that phrase". Section II, 5 is split between two sentences (《易》曰、「履霜、堅冰至」 starts 坤 2) and needs no change.

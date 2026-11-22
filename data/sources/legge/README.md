# Legge's English

`text.json` holds James Legge's English translation of the judgment (卦辭) and the six line texts (爻辭) of every hexagram, plus 用九 and 用六, keyed by King Wen number. `scripts/data/build.py` adds each one to the dataset as `en_legge`.

**Work:** James Legge, *The Yî King*, The Sacred Books of the East, vol. XVI (Oxford: Clarendon Press, 1882; 2nd edition 1899). Public domain.

## How the text was made

No clean digital edition of Legge's text section was available, so it was rebuilt from three scans of the printed book on the Internet Archive and the proofread pages on English Wikisource:

| Witness | What it is |
|---|---|
| [`iching00jame`](https://archive.org/details/iching00jame) | Dover reprint of the 2nd edition (1899). Best OCR; the main witness. |
| [`sacredbooksofchi16conf`](https://archive.org/details/sacredbooksofchi16conf) | 1882 edition (Princeton copy). Second OCR witness. |
| [`sacredbooksofeas0016fmax`](https://archive.org/details/sacredbooksofeas0016fmax) | 1899 printing. Consulted where the first two disagree. |
| [Wikisource, *Sacred Books of the East - Volume 16*](https://en.wikisource.org/wiki/Index:Sacred_Books_of_the_East_-_Volume_16.djvu) | Proofread transcription. Used for hexagrams 1–19 where it matches the OCR text (pages for later hexagrams were not yet proofread). |

1. Each OCR text was split into the judgment and line paragraphs of each hexagram, leaving out Legge's notes, page headers and line numbers.
2. The two main OCR witnesses were merged word by word; where they differ, the reading made of real English words wins.
3. For hexagrams 1–19 the proofread Wikisource text replaces the merge wherever the two agree closely (similarity of 0.9 or more), as a check that the merge is right.
4. Spelling was normalised to plain ASCII: Legge's diacritics in romanised names were dropped, hyphens broken across lines were joined, and quotation marks made straight. Legge's em dashes and his parentheses, which mark words he added to the Chinese, are kept.
5. Remaining OCR errors were corrected by hand against the scans (for example "mount Khi" in 升, "white mao grass" in 大過, and notes that had run into the text in 无妄).

`scripts/data/validate.py` checks that every judgment and line has an `en_legge` text with no stray characters or spacing errors. Corrections are welcome: compare with the scans above and open a pull request that edits `text.json`.

Legge's romanisation of hexagram names (Khien, Khwan, Kun…) is kept inside his text. The dataset's own `name.en` field holds Wengua's short English names instead.

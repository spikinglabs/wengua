---
description: "Wengua's core library in TypeScript and Python: fair three-coin and yarrow-stalk casting, changing lines, related hexagrams, Zhu Xi's text selection and lookup."
---

# Core library

The same logic in TypeScript (`npm install wengua`) and Python (`pip install wengua`). Both packages must reproduce one shared file of test vectors (`spec/vectors.json`), so they cannot drift apart: the same seed gives the same cast in both, coin for coin.

=== "Python"

    ```python
    import wengua

    r = wengua.cast("What should I understand about this move?", method="yarrow")
    r["primary"]["name"]          # {'zh_hant': '豐', 'zh_hans': '丰', 'pinyin': 'fēng', 'en': 'Abundance'}
    r["selection"]["texts"]       # the texts to read, chosen by Zhu Xi's rules, in 繁 and 简

    wengua.read_cast([9, 8, 7, 7, 8, 6])   # a physical cast, bottom line first
    wengua.get("水雷屯")                     # full record of hexagram 3
    ```

=== "TypeScript"

    ```ts
    import { cast, readCast, get } from "wengua";

    const r = cast({ question: "What should I understand about this move?", method: "yarrow" });
    r.primary.name;            // { zh_hant: "豐", zh_hans: "丰", pinyin: "fēng", en: "Abundance" }
    r.selection.texts;         // the texts to read, in 繁 and 简

    readCast([9, 8, 7, 7, 8, 6]);
    get("水雷屯");
    ```

## Casting methods

| Method | P(6) old yin | P(7) young yang | P(8) young yin | P(9) old yang |
|---|---|---|---|---|
| Three coins | 1/8 | 3/8 | 3/8 | 1/8 |
| Yarrow stalks (大衍筮法) | 1/16 | 5/16 | 7/16 | 3/16 |
| Manual | from a physical cast | | | |

- **Coins:** three fair coins per line, heads 3 and tails 2. Each coin is recorded.
- **Yarrow:** a full simulation of the 大衍筮法 with 49 stalks and three changes per line: divide (分二), hang one (掛一), count by fours (揲四), set aside the remainders (歸奇). Every division is recorded. The left heap is drawn uniformly from 1 to the largest multiple of four that leaves the right heap a stalk, so each remainder is equally likely. The odds then come out exactly 1/16, 5/16, 7/16, 3/16. A naive uniform split would make old yin about 4.8% instead of 6.25%.
- **Randomness** comes from the operating system (`secrets` in Python, `crypto.getRandomValues` in JavaScript), with rejection sampling so there is no modulo bias. A `seed` is accepted only with `mode="test"`, and such readings carry `audit.test: true`.
- CI runs a chi-square test on both methods with both random sources.

## Derivations

本卦 (primary), 動爻 (changing lines), 之卦 (relating), 互卦 (nuclear), 錯卦 (opposite, every line inverted), 綜卦 (inverse, turned upside down).

## Text selection (取辭)

The default rule is Zhu Xi's, from《易學啓蒙·考變占》:

| Changing lines | Read |
|---|---|
| 0 | the judgment of the primary hexagram |
| 1 | that line of the primary hexagram |
| 2 | both lines of the primary hexagram; the upper one leads |
| 3 | the judgments of the primary (貞) and relating (悔) hexagrams |
| 4 | the two unchanging lines of the relating hexagram; the lower one leads |
| 5 | the one unchanging line of the relating hexagram |
| 6 | the judgment of the relating hexagram; for 乾 and 坤, 用九 or 用六 |

Each selected text has a `role` (`principal`, `supporting`, `zhen`, `hui`), and the reading includes the rule's explanation in 繁, 简 and English. `rule="all"` returns every relevant text instead.

## Lookup

`find()` returns every match and `get()` exactly one. Both accept a number, a Chinese name in either script (訟 or 讼), a full name (水雷屯, 乾為天), pinyin with or without tones (`xiǎo chù`, `xiaochu`), the English name, the symbol (䷂), six bits bottom to top (`100010`) or a trigram pair (坎上震下, 上坎下震, `water over thunder`). Ambiguous pinyin such as `kun` (坤 and 困) returns both.

## The Reading object

`question`, `locale`, `method`, `values` (six numbers, bottom to top), `lines`, `primary`, `changing_lines`, `relating`, `nuclear`, `opposite`, `inverse`, `selection` (`rule`, `explanation`, `source`, `texts`) and `audit` (`rng`, `test`, `seed`, `record`, `timestamp`, `library`, `dataset`).

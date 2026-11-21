# Core library

The same logic in TypeScript and Python, kept in sync by one shared file of test vectors.

## Casting methods

| Method | P(6) old yin | P(7) young yang | P(8) young yin | P(9) old yang |
|---|---|---|---|---|
| Three coins | 1/8 | 3/8 | 3/8 | 1/8 |
| Yarrow stalks (大衍筮法) | 1/16 | 5/16 | 7/16 | 3/16 |
| Manual | from a physical cast | | | |

- Randomness comes from a secure generator. A `seed` is accepted only in test mode, and the output says so.
- Every reading carries an `audit` record: the method, each coin or stalk division, and the library and dataset versions.

## Derivations

本卦 (primary), 动爻 (changing lines), 之卦 (relating), 互卦 (nuclear), 错卦 (inverse), 综卦 (reversed).

## Text selection (取辞)

By default, Zhu Xi's rules from《易学启蒙》 decide which texts to read for 0 to 6 changing lines. Other conventions are opt-in and named.

## Lookup

By number, Chinese name, pinyin, English name, Unicode symbol, binary or trigram pair (e.g. 坎上震下).

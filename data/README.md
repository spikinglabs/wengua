# wengua-data

The text of the *Zhouyi* (周易) as structured, bilingual-ready JSON: all 64 hexagrams with 卦辞, 彖传, 大象, six 爻辞 with their 小象, 用九 and 用六, and 文言, in traditional and simplified Chinese.

- `hexagrams/01.json` … `hexagrams/64.json`: one file per hexagram, in King Wen order
- `trigrams.json`: the eight trigrams
- `iching.json`: everything in one file
- `cross-check.json`: every place where the primary edition and the cross-check edition differ
- `sources/`: the exact source snapshots the data was built from

Rebuild with `python scripts/data/build.py` and check with `python scripts/data/validate.py`. See [SOURCES.md](SOURCES.md) for editions and editorial choices.

License: [CC BY-SA 4.0](LICENSE). The classical text itself is in the public domain; the license covers the digital transcriptions we build on and our structure and glosses.

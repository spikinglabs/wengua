"""Collate the dataset against a printed witness edition, character by character.

For every text unit (卦辭, 彖, 大象, 爻辭, 小象, 用九/用六, 文言) the unit is aligned
inside the witness's text for that hexagram (semi-global edit distance:
punctuation removed, free start and end in the witness). Each difference is
classified as either an orthographic variant (異體字, the same word written
another way, listed in data/sources/witnesses/orthographic-variants.tsv) or a
reading that differs, which is reported for review.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import witness  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
VARIANTS_FILE = ROOT / "data" / "sources" / "witnesses" / "orthographic-variants.tsv"
PUNCT = re.compile(r"[，。、；：？！「」『』《》（）〈〉·\s]")


def orthographic() -> set[frozenset]:
    pairs = set()
    if VARIANTS_FILE.exists():
        for line in VARIANTS_FILE.read_text(encoding="utf-8").splitlines():
            if line.strip() and not line.startswith("#"):
                chars = line.split("\t")[0].split()
                for a in chars:
                    for b in chars:
                        if a != b:
                            pairs.add(frozenset((a, b)))
    return pairs


def align(unit: str, hay: str, same=lambda a, b: a == b) -> tuple[int, int, int, list[tuple[str, str]]]:
    """Best match of `unit` inside `hay`: (cost, start, end, ops). ops are (ours, theirs) differences."""
    n, m = len(unit), len(hay)
    INF = 10**9
    prev = [0] * (m + 1)  # free start anywhere in hay
    back = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        cur = [INF] * (m + 1)
        cur[0] = i
        back[i][0] = 1  # up: deletion (ours has extra)
        ui = unit[i - 1]
        bi = back[i]
        for j in range(1, m + 1):
            d = prev[j - 1] + (0 if same(ui, hay[j - 1]) else 1)
            u = prev[j] + 1
            left = cur[j - 1] + 1
            if d <= u and d <= left:
                cur[j], bi[j] = d, 0
            elif u <= left:
                cur[j], bi[j] = u, 1
            else:
                cur[j], bi[j] = left, 2
        prev = cur
    end = min(range(m + 1), key=lambda j: prev[j])
    cost = prev[end]
    i, j, ops = n, end, []
    while i > 0:
        b = back[i][j]
        if b == 0:
            if unit[i - 1] != hay[j - 1]:
                ops.append((unit[i - 1], hay[j - 1]))
            i, j = i - 1, j - 1
        elif b == 1:
            ops.append((unit[i - 1], ""))
            i -= 1
        else:
            ops.append(("", hay[j - 1]))
            j -= 1
    ops.reverse()
    return cost, j, end, _merge(ops)


def _merge(ops):
    """Join runs of single-character insertions/deletions into one difference."""
    out = []
    for a, b in ops:
        if out and ((a == "" and out[-1][0] == "") or (b == "" and out[-1][1] == "")) and (a == "" or b == ""):
            pa, pb = out[-1]
            out[-1] = (pa + a, pb + b)
        else:
            out.append((a, b))
    return out


def units(h: dict):
    yield "judgment", h["judgment"]["zh_hant"]
    yield "tuan", h["tuan"]["zh_hant"]
    yield "image", h["image"]["zh_hant"]
    for line in h["lines"]:
        yield f"line {line['position']}", line["text"]["zh_hant"]
        yield f"xiao_xiang {line['position']}", line["xiao_xiang"]["zh_hant"]
    if h.get("use_line"):
        yield "use_line", h["use_line"]["text"]["zh_hant"]
        yield "use_line xiao_xiang", h["use_line"]["xiao_xiang"]["zh_hant"]
    for k, p in enumerate(h.get("wenyan") or [], 1):
        yield f"wenyan {k}", p["zh_hant"]


def collate(edition: str) -> dict:
    bundle = json.loads((ROOT / "data" / "iching.json").read_text(encoding="utf-8"))
    chunks = witness.chunks(edition)
    ortho = orthographic()
    readings, orth_count, chars, lacunae = [], {}, 0, []

    def same(a, b):
        return a == b or b == "〓" or frozenset((a, b)) in ortho
    for h in bundle["hexagrams"]:
        hay = chunks[h["number"] - 1]
        for field, text in units(h):
            plain = PUNCT.sub("", text)
            chars += len(plain)
            cost, _, _, ops = align(plain, hay, same)
            if cost >= 2 and cost * 3 > len(plain):
                lacunae.append({"hexagram": h["number"], "name": h["name"]["zh_hant"], "field": field})
                continue
            for ours, theirs in ops:
                if len(ours) == 1 and len(theirs) == 1 and frozenset((ours, theirs)) in ortho:
                    orth_count[f"{ours}/{theirs}"] = orth_count.get(f"{ours}/{theirs}", 0) + 1
                else:
                    readings.append({"hexagram": h["number"], "name": h["name"]["zh_hant"], "field": field,
                                     "ours": ours, "witness": theirs})
    return {"witness": witness.WITNESSES[edition], "characters_compared": chars,
            "orthographic_variants": dict(sorted(orth_count.items(), key=lambda kv: -kv[1])),
            "differing_readings": readings,
            "not_found_in_witness": lacunae}


def main() -> None:
    out = collate("sbck")
    path = ROOT / "data" / "collation-sbck.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"Compared {out['characters_compared']} characters with {out['witness']}: "
          f"{sum(out['orthographic_variants'].values())} orthographic variants, "
          f"{len(out['differing_readings'])} differing readings, "
          f"{len(out['not_found_in_witness'])} units missing from the witness transcription")


if __name__ == "__main__":
    main()

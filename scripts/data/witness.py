"""Parse the printed witness editions (王弼《周易注》 in Kanripo KR1a0006) into
64 plain-text chunks, one per hexagram, with the commentary removed.

Witnesses:
  sbck: 四部叢刊 photo-reprint of a Song edition
  wyg:  四庫全書 文淵閣本
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WITNESS_DIR = ROOT / "data" / "sources" / "witnesses"
WITNESSES = {
    "sbck": "四部叢刊本 王弼《周易注》 (Kanripo KR1a0006, branch SBCK)",
    "wyg": "四庫全書文淵閣本 王弼《周易注》 (Kanripo KR1a0006, branch WYG)",
}


def gaiji() -> dict[str, str]:
    out = {}
    for line in (WITNESS_DIR / "gaiji.tsv").read_text(encoding="utf-8").splitlines():
        if line.startswith("#") or not line.strip():
            continue
        code, exact, normal = (line.split("\t") + ["", ""])[:3]
        out[code] = exact or normal or "〓"  # 〓: a character we cannot read
    return out


TRIGRAM_BITS = {"乾": "111", "兌": "110", "兊": "110", "離": "101", "震": "100", "巽": "011",
                "坎": "010", "艮": "001", "坤": "000",
                "良": "001"}  # 良: a transcription typo for 艮 in the 小過 header


def _hex(symbol: str, lower: str, upper: str) -> int:
    """Trust the trigram note; fall back to the symbol if a note is unreadable."""
    if lower not in TRIGRAM_BITS or upper not in TRIGRAM_BITS:
        return ord(symbol) - 0x4DC0 + 1
    import json
    global _BY_BINARY
    try:
        table = _BY_BINARY
    except NameError:
        bundle = json.loads((ROOT / "data" / "iching.json").read_text(encoding="utf-8"))
        table = _BY_BINARY = {h["binary"]: h["number"] for h in bundle["hexagrams"]}
    return table[TRIGRAM_BITS[lower] + TRIGRAM_BITS[upper]]


def chunks(edition: str) -> list[str]:
    """64 strings of classic text (經 and 傳 as printed with Wang Bi), commentary removed."""
    table = gaiji()
    text = ""
    for f in sorted((WITNESS_DIR / edition).glob("KR1a0006_00*.txt")):
        lines = []
        for l in f.read_text(encoding="utf-8").splitlines():
            l = re.sub(r"<(?:pb|md):[^>]+>", "", l).replace("¶", "").strip("\u3000 ")
            if l.startswith("#") or re.fullmatch(r"周易[上下]經.*第[一二三四五六七八九十]+|王弼注|.*卷[一二三四五六七八九十]+", l):
                continue
            lines.append(l)
        text += "".join(lines)
    # The hexagram is identified by its printed trigram note, e.g. ䷂(震下/坎上): a few
    # symbols in the transcription are wrong, the notes are not.
    text = re.sub(r"([\u4DC0-\u4DFF])\((\S)下/(\S)上\)", lambda m: f"\uE000{_hex(*m.groups())}\uE001", text)
    text = re.sub(r"([\u4DC0-\u4DFF])\((\S)上/(\S)下\)", lambda m: f"\uE000{_hex(m.group(1), m.group(3), m.group(2))}\uE001", text)
    text = re.sub(r"\([^)]*\)", "", text)  # interlinear commentary
    text = re.sub(r"&(KR\d+);", lambda m: table.get(m.group(1), "〓"), text)
    text = re.sub(r"[\s\u3000]+", "", text)
    text = re.sub(r"周易卷第[一二三四五六七八九十]+", "", text)
    parts = re.split("\uE000(\\d+)\uE001", text)
    out = {}
    for i in range(1, len(parts), 2):
        out[int(parts[i])] = parts[i + 1]
    if sorted(out) != list(range(1, 65)):
        raise ValueError(f"{edition}: expected 64 hexagrams, found {len(out)}")
    return [out[n] for n in range(1, 65)]

"""Hexagram relationships. Binary strings run bottom to top, 1 = yang."""

from __future__ import annotations


def primary_bits(values: list[int]) -> str:
    return "".join("1" if v in (7, 9) else "0" for v in values)


def relating_bits(values: list[int]) -> str:
    """之卦: the changing lines (6 and 9) turn into their opposite."""
    return "".join("1" if v in (6, 7) else "0" for v in values)


def changing_positions(values: list[int]) -> list[int]:
    return [i + 1 for i, v in enumerate(values) if v in (6, 9)]


def nuclear(bits: str) -> str:
    """互卦: lines 2-4 form the lower trigram, lines 3-5 the upper."""
    return bits[1:4] + bits[2:5]


def opposite(bits: str) -> str:
    """錯卦: every line inverted."""
    return "".join("0" if b == "1" else "1" for b in bits)


def inverse(bits: str) -> str:
    """綜卦: the hexagram turned upside down."""
    return bits[::-1]

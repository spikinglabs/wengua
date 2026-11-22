"""The bundled dataset (wengua-data): 64 hexagrams and 8 trigrams."""

from __future__ import annotations

import json
from functools import lru_cache
from importlib import resources


@lru_cache(maxsize=1)
def bundle() -> dict:
    with resources.files(__package__).joinpath("data/iching.json").open(encoding="utf-8") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def _by_binary() -> dict[str, dict]:
    return {h["binary"]: h for h in bundle()["hexagrams"]}


@lru_cache(maxsize=1)
def _trigrams() -> dict[str, dict]:
    return {t["key"]: t for t in bundle()["trigrams"]}


def hexagram(number: int) -> dict:
    """The full record of hexagram `number` (1 to 64, King Wen order)."""
    n = int(number)
    if not 1 <= n <= 64:
        raise ValueError("hexagram number must be 1 to 64")
    return bundle()["hexagrams"][n - 1]


def hexagram_by_binary(binary: str) -> dict:
    """Six bits, bottom to top, 1 = yang."""
    try:
        return _by_binary()[binary]
    except KeyError:
        raise ValueError(f"not a six-bit hexagram: {binary!r}") from None


def trigram(key: str) -> dict:
    return _trigrams()[key]


def trigrams() -> list[dict]:
    return list(bundle()["trigrams"])

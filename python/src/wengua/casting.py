"""Casting methods. Each returns six line values, bottom to top, and a record of
every coin or stalk so the cast can be audited and replayed.

Line values: 6 old yin (changing), 7 young yang, 8 young yin, 9 old yang (changing).
"""

from __future__ import annotations

from .rng import randbelow

VALID_VALUES = (6, 7, 8, 9)


def cast_coins(rng) -> tuple[list[int], list[dict]]:
    """Three coins per line. Heads count 3, tails 2.

    P(6, 7, 8, 9) = 1/8, 3/8, 3/8, 1/8.
    """
    values, record = [], []
    for _ in range(6):
        coins = [3 if randbelow(rng, 2) else 2 for _ in range(3)]
        value = sum(coins)
        values.append(value)
        record.append({"coins": coins, "value": value})
    return values, record


def _remainder(n: int) -> int:
    """Count a heap off by fours: the remainder is 1 to 4 (4 when it divides evenly)."""
    return 0 if n == 0 else (n - 1) % 4 + 1


def cast_yarrow(rng) -> tuple[list[int], list[dict]]:
    """The 大衍筮法: 50 stalks, one set aside, three changes per line.

    Each change divides the stalks into two heaps at random, hangs one stalk
    from the right heap (掛一), and counts both heaps off by fours (揲四), setting
    the remainders aside (歸奇). After three changes the remaining stalks divided
    by four give the line value.

    The left heap is drawn uniformly from 1 to the largest multiple of four
    that still leaves the right heap a stalk after hanging one. Every remainder
    is then equally likely, both heaps are never empty, and the line values come
    out with exactly the classical odds P(6, 7, 8, 9) = 1/16, 5/16, 7/16, 3/16.
    """
    values, record = [], []
    for _ in range(6):
        stalks = 49
        changes = []
        for _ in range(3):
            left = randbelow(rng, 4 * ((stalks - 2) // 4)) + 1
            right = stalks - left - 1  # one stalk hung between the fingers
            rl, rr = _remainder(left), _remainder(right)
            removed = 1 + rl + rr
            changes.append({"stalks": stalks, "left": left, "right": right + 1,
                            "left_remainder": rl, "right_remainder": rr, "removed": removed})
            stalks -= removed
        value = stalks // 4
        values.append(value)
        record.append({"changes": changes, "remaining": stalks, "value": value})
    return values, record


def parse_manual(values) -> tuple[list[int], list[dict]]:
    """Six values from a physical cast, bottom to top.

    Each item is a line value (6, 7, 8, 9) or the three coin faces of that line,
    given as numbers (2 or 3) or as "h"/"t" (heads 3, tails 2).
    """
    if len(values) != 6:
        raise ValueError("a cast has exactly six lines, bottom to top")
    out, record = [], []
    for v in values:
        if isinstance(v, (list, tuple)):
            coins = [_coin(c) for c in v]
            if len(coins) != 3:
                raise ValueError("each line needs three coins")
            out.append(sum(coins))
            record.append({"coins": coins, "value": sum(coins)})
        else:
            n = int(v)
            if n not in VALID_VALUES:
                raise ValueError(f"line value must be 6, 7, 8 or 9, got {v!r}")
            out.append(n)
            record.append({"value": n})
    return out, record


def _coin(c) -> int:
    if isinstance(c, str):
        c = c.strip().lower()
        if c in ("h", "heads", "3"):
            return 3
        if c in ("t", "tails", "2"):
            return 2
    elif c in (2, 3):
        return int(c)
    raise ValueError(f"a coin is heads (3) or tails (2), got {c!r}")

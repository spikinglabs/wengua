"""Random sources. Real readings use the operating system's secure RNG.

A seeded generator (Mulberry32) exists only for tests and replays. It is the
same algorithm in the Python and TypeScript packages, so a seed gives the same
cast in both, and every reading made with it is labelled as a test.
"""

from __future__ import annotations

import secrets

_M32 = 0xFFFFFFFF


class SecureRng:
    name = "secure"

    def next_u32(self) -> int:
        return secrets.randbits(32)


class SeededRng:
    """Mulberry32. Not for real readings."""

    name = "seeded-test"

    def __init__(self, seed: int) -> None:
        if not isinstance(seed, int) or isinstance(seed, bool):
            raise TypeError("seed must be an integer")
        self.seed = seed & _M32
        self._state = self.seed

    def next_u32(self) -> int:
        a = (self._state + 0x6D2B79F5) & _M32
        self._state = a
        t = ((a ^ (a >> 15)) * (1 | a)) & _M32
        t = ((t + (((t ^ (t >> 7)) * (61 | t)) & _M32)) & _M32) ^ t
        return (t ^ (t >> 14)) & _M32


def randbelow(rng, n: int) -> int:
    """A uniform integer in [0, n), by rejection sampling (no modulo bias)."""
    if n <= 0:
        raise ValueError("n must be positive")
    limit = (1 << 32) - ((1 << 32) % n)
    while True:
        x = rng.next_u32()
        if x < limit:
            return x % n

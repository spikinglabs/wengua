"""Build a Reading: the full, auditable result of a cast."""

from __future__ import annotations

from datetime import datetime, timezone

from . import __version__
from .casting import cast_coins, cast_yarrow, parse_manual
from .data import bundle, hexagram_by_binary
from .derive import changing_positions, inverse, nuclear, opposite, primary_bits, relating_bits
from .rng import SecureRng, SeededRng
from .selection import select

METHODS = ("coins", "yarrow")


def summary(h: dict) -> dict:
    return {"number": h["number"], "unicode": h["unicode"], "binary": h["binary"],
            "name": h["name"], "trigrams": h["trigrams"]}


def build_reading(values, *, method: str, record=None, rng: str = "none", seed=None,
                  question=None, rule: str = "zhuxi", locale=None, timestamp=None) -> dict:
    values = list(values)
    primary = hexagram_by_binary(primary_bits(values))
    changing = changing_positions(values)
    relating = hexagram_by_binary(relating_bits(values))
    pb = primary["binary"]
    meta = bundle()
    return {
        "question": question,
        "locale": locale,
        "method": method,
        "values": values,
        "lines": [{"position": i + 1, "value": v, "yang": v in (7, 9), "changing": v in (6, 9)}
                  for i, v in enumerate(values)],
        "primary": summary(primary),
        "changing_lines": changing,
        "relating": summary(relating) if changing else None,
        "nuclear": summary(hexagram_by_binary(nuclear(pb))),
        "opposite": summary(hexagram_by_binary(opposite(pb))),
        "inverse": summary(hexagram_by_binary(inverse(pb))),
        "selection": select(primary, relating, changing, rule),
        "audit": {
            "rng": rng,
            "test": rng == "seeded-test",
            "seed": seed,
            "record": record,
            "timestamp": timestamp or datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "library": f"wengua-py {__version__}",
            "dataset": f"{meta['dataset']} {meta.get('version', '')}".strip(),
        },
    }


def cast(question=None, method: str = "coins", *, rule: str = "zhuxi", locale=None,
         seed=None, mode=None) -> dict:
    """Cast a hexagram with a secure RNG and return a Reading.

    `seed` is accepted only with mode="test"; such readings say so in `audit`.
    """
    if method not in METHODS:
        raise ValueError(f"unknown method {method!r}; choose one of {', '.join(METHODS)}")
    if seed is not None and mode != "test":
        raise ValueError('a seed is only allowed with mode="test"')
    rng = SeededRng(seed) if seed is not None else SecureRng()
    values, record = (cast_coins if method == "coins" else cast_yarrow)(rng)
    return build_reading(values, method=method, record=record, rng=rng.name,
                         seed=rng.seed if seed is not None else None,
                         question=question, rule=rule, locale=locale)


def read_cast(values, question=None, *, rule: str = "zhuxi", locale=None) -> dict:
    """Make a Reading from a physical cast: six line values or coin faces, bottom to top."""
    vals, record = parse_manual(values)
    return build_reading(vals, method="manual", record=record, rng="none",
                         question=question, rule=rule, locale=locale)

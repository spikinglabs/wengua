"""Wengua 问卦: the accurate, open I Ching for every AI.

Code casts, the model reads. 排卦归程序，解卦归模型。
"""

__version__ = "0.1.0"

from .data import hexagram, trigram, trigrams  # noqa: E402
from .lookup import find, get  # noqa: E402
from .reading import cast, read_cast  # noqa: E402
from .selection import RULES  # noqa: E402

__all__ = ["__version__", "cast", "read_cast", "find", "get", "hexagram", "trigram", "trigrams", "RULES"]

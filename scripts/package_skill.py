"""Zip the Agent Skill for download.

Usage: python scripts/package_skill.py OUT.zip

The docs build puts the zip at the site root (wengua.allo.land/wengua-skill.zip)
so people can download it straight from the docs. The zip holds one top-level
folder, wengua/, which is the layout Claude's skill upload expects.
"""

from __future__ import annotations

import sys
import zipfile
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent / "skills" / "wengua"


def main(out: str) -> None:
    dest = Path(out)
    dest.parent.mkdir(parents=True, exist_ok=True)
    files = sorted(
        p for p in SKILL.rglob("*")
        if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"
    )
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as z:
        for p in files:
            # Fixed timestamps keep the zip identical between builds.
            info = zipfile.ZipInfo(str(Path("wengua") / p.relative_to(SKILL)), (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o755 if p.suffix == ".py" and p.name == "run.py" else 0o644) << 16
            z.writestr(info, p.read_bytes())
    print(f"{dest}: {len(files)} files, {dest.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "wengua-skill.zip")

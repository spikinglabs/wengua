"""Copy the dataset bundle and licenses into the Python and TypeScript packages.

CI runs this and fails if anything changed, so the packages never ship stale data.
"""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COPIES = {
    ROOT / "data" / "iching.json": [ROOT / "python/src/wengua/data/iching.json", ROOT / "js/src/iching.json"],
    ROOT / "spec" / "mcp.json": [ROOT / "python/src/wengua/data/mcp.json", ROOT / "js/src/mcp.json"],
    ROOT / "README.md": [],  # packages carry an edited copy; see python/README.md and js/README.md
    ROOT / "LICENSE": [ROOT / "python/LICENSE", ROOT / "js/LICENSE", ROOT / "skills/wengua/LICENSE"],
    ROOT / "data" / "LICENSE": [ROOT / "python/DATA_LICENSE", ROOT / "js/DATA_LICENSE", ROOT / "skills/wengua/DATA_LICENSE"],
}

for src, dests in COPIES.items():
    for dest in dests:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)
        print(f"{src.relative_to(ROOT)} -> {dest.relative_to(ROOT)}")

# The Agent Skill bundles a copy of the Python package so it runs with no install.
SKILL_PKG = ROOT / "skills/wengua/scripts/wengua"
if SKILL_PKG.exists():
    shutil.rmtree(SKILL_PKG)
shutil.copytree(ROOT / "python/src/wengua", SKILL_PKG, ignore=shutil.ignore_patterns("__pycache__"))
print("python/src/wengua -> skills/wengua/scripts/wengua")

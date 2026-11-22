"""Entry point for the Wengua skill: runs the bundled copy of the wengua package."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from wengua.cli import main  # noqa: E402

sys.exit(main())

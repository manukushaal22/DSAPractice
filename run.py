"""Entry point: `py run.py [selector ...]`. See `py run.py --help`.

Note: deliberately no shebang line - the Windows `py` launcher honours
`#!/usr/bin/env python` and would resolve to the WindowsApps stub.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from dsakit.runner import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

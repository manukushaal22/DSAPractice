"""Launcher for the solver app.

    solverapp\\.venv\\Scripts\\python.exe solverapp\\serve.py

Serves the API and, if `web/dist` exists, the built frontend too - so this one
command is the whole app. During frontend development run `npm run dev` in
`solverapp/web` alongside this and use the Vite URL instead.
"""

from __future__ import annotations

import sys
import webbrowser
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(APP_DIR))

HOST = "127.0.0.1"
PORT = 8000


def main() -> int:
    try:
        import uvicorn
    except ImportError:
        print("uvicorn is not installed. Create the venv and install requirements:")
        print("  py -m venv solverapp\\.venv")
        print("  solverapp\\.venv\\Scripts\\python.exe -m pip install -r solverapp\\requirements.txt")
        return 1

    dist = APP_DIR / "web" / "dist"
    url = f"http://{HOST}:{PORT}"
    if dist.is_dir():
        print(f"Solver app: {url}")
        if "--no-browser" not in sys.argv:
            webbrowser.open(url)
    else:
        print(f"API only: {url}/api/problems  (frontend not built)")
        print("Build it with:  cd solverapp\\web  &&  npm install  &&  npm run build")
        print("Or run the Vite dev server:  npm run dev")

    uvicorn.run(
        "server.app:app",
        host=HOST,
        port=PORT,
        reload="--reload" in sys.argv,
        log_level="info",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

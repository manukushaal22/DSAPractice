# Solver app

A local, browser-based way to work through the problems in `problems/` — a list screen
and a LeetCode-style split screen with the statement on the left and a code editor on
the right.

It reads `problems/` as its only data source. Add a new problem folder in the usual
shape and it shows up on the next page refresh; nothing to register, no restart.

```
solverapp/
  serve.py            launcher (API + built frontend)
  requirements.txt    fastapi, uvicorn
  server/
    app.py            FastAPI routes
    catalog.py        problem discovery + README/PROGRESS.md parsing
    child_runner.py   runs a test suite against submitted code (see below)
    execute.py        subprocess spawn, NDJSON relay, cancellation
    state.py          last-run badges (solverapp/.data/state.json)
  web/                Vite + React + TypeScript + Monaco
```

## Setup (once)

```powershell
py -m venv solverapp\.venv
solverapp\.venv\Scripts\python.exe -m pip install -r solverapp\requirements.txt

cd solverapp\web
npm install
npm run build
```

## Run

```powershell
solverapp\.venv\Scripts\python.exe solverapp\serve.py
```

Opens <http://127.0.0.1:8000>. There is also a **Start solver app** VS Code task.

### Frontend development

Leave `serve.py` running for the API, and in a second terminal:

```powershell
cd solverapp\web
npm run dev          # http://localhost:5173, proxies /api to port 8000
```

## How it works

**Run** never touches your files. The editor buffer is written to a throwaway temp file
and `child_runner.py` registers it in `sys.modules` under the name `solution` *before*
importing the problem's `tests.py`. The test suite's `from solution import <fn>` then
resolves to your buffer, and `problems/pNNN-slug/solution.py` is never read.

**Save** is the only thing that writes to a problem folder, and it writes `solution.py`
only. It preserves the file's existing line endings and refuses to clobber a file that
changed on disk since the tab was opened (you get an *Overwrite* / *Reload* choice).

Cases run through `dsakit.limits.call_with_limits`, the same guard the CLI uses, so the
TLE/MLE budgets declared in each `tests.py` apply identically. `dsakit/` is used as a
library and is not modified — `py run.py` behaves exactly as before.

Results stream case by case as they finish, so a slow perf case doesn't hold up the
verdicts before it. Anything your code `print`s is captured per case and shown in the
result detail.

## Keyboard

| Key | Action |
| --- | --- |
| `Ctrl` + `Enter` | Run all cases |
| `Ctrl` + `S` | Save the buffer to `solution.py` |
| `Esc` | Stop a running suite (kills the subprocess) |

Editor suggestions are **off by default**, matching this workspace's deliberate
no-autocomplete stance for practice. There is a toggle above the editor.

## API

| Method | Path | |
| --- | --- | --- |
| `GET` | `/api/problems` | list with metadata and last-run badges |
| `GET` | `/api/problems/{id}` | README, current `solution.py`, mtime |
| `POST` | `/api/problems/{id}/run` | NDJSON stream: `start` → `case`×N → `done` |
| `PUT` | `/api/problems/{id}/solution` | save; `409` if changed on disk |

`id` accepts `p009`, `9`, or the full folder slug. Interactive docs at `/docs`.

## Notes

- `solverapp/.data/` (last-run badges), `web/node_modules/` and `web/dist/` are gitignored.
- Nothing is ever written into a problem folder except `solution.py` on Save, so
  `dsakit.runner`'s "unexpected files" check stays quiet.
- Node 18 is what this was built against, hence Vite 6 rather than 7.
- Monaco is bundled locally rather than loaded from a CDN, so the app works offline.

# DSA Practice

A self-contained, dependency-free workspace for practising data structures and algorithms
in Python, with an AI coach that hands out problems and reviews solutions.

## How it works

There are two tracks:

- **`learn/`: the learning path.** Topics in prerequisite order. Each has a lesson and
  a ladder of exercises from easy to hard. See [`learn/README.md`](learn/README.md).
- **`problems/`: the interview drill.** Mixed problems where the technique is not
  announced. It doubles as spaced review for completed learn topics.

Either way:

1. Ask the agent for a problem (or the next topic / next rung). It creates a folder with
   a statement, a test suite, and a `solution.py` containing an empty function.
2. You implement the function. Nothing else.
3. Run the tests. Iterate until green.
4. Ask the agent to review. It runs the tests, critiques correctness, complexity, and
   style, and suggests better approaches — in chat. Reviews are not written to disk;
   the durable record is a one-line summary in `PROGRESS.md`.

## Running tests

Python is invoked with the `py` launcher on this machine.

```powershell
py run.py            # run everything (both tracks)
py run.py 1          # run problem p001
py run.py 1 3        # run p001 and p003
py run.py two-sum    # run by folder-name substring
py run.py L1.3       # run learn exercise 01.3
py run.py L1         # run every exercise in learn topic 01
py run.py learn      # run the whole learn track (or: problems)
py run.py --list     # list both tracks and status
py run.py --help
```

Each problem also runs standalone:

```powershell
py problems\p001-best-time-to-buy-and-sell-stock\tests.py
```

## Time and memory limits

Every case runs under a budget, so a runaway solution is **aborted and reported**
instead of being waited on. Defaults are **5000 ms** and **512 MB** per case; perf
cases usually tighten these (p001 uses 1000 ms / 64 MB).

```
TLE   case 14 (perf: 100k sawtooth)
    exceeded the 1000 ms budget - aborted after 1037 ms
    Too slow for this input size. Re-read 'Target complexity' in README.md.
```

An O(n²) attempt at p001 takes **68 s** unguarded; guarded it reports in **2.7 s**.

Override the budgets when you want to:

```powershell
py run.py 1 --time-limit 200      # tighter, in milliseconds
py run.py 1 --memory-limit 32     # in megabytes
py run.py 1 --no-limits           # let a slow solution finish
```

`--time-limit 0` / `--memory-limit 0` also disable a single limit. Passing solutions
print their own time, and memory whenever it exceeds 1 MB, so you can see the cost of
your approach even when it's within budget.

<details>
<summary>How the abort works</summary>

Each case runs on a worker thread while the main thread watches elapsed time and the
process's private committed bytes. On a breach, the watchdog injects a `BaseException`
into the worker via `PyThreadState_SetAsyncExc`. The exception lands at the next bytecode
boundary, so a thread parked inside one long C-level call (a single huge `sorted()`, say)
can outlive the abort — the harness prints a note when that happens and abandons the
thread, which dies with the process. Memory sampling uses `GetProcessMemoryInfo` on
Windows and `/proc/self/statm` on Linux; if neither is available the memory limit is
silently skipped.

</details>


## Layout

```
run.py                       entry point
dsakit/                      test harness (stdlib only), incl. ListNode / TreeNode helpers
problems/
  p001-.../
    README.md                statement, examples, constraints, collapsed hints
    solution.py              <- you edit this file only
    tests.py                 test cases
learn/
  README.md                  roadmap: curriculum, ladder rules, planned ladders
  01-arrays-and-hashing/
    README.md                the lesson
    01.3-.../                an exercise: same three files as a problem
PROGRESS.md                  scoreboard / cross-session memory
AGENTS.md                    instructions the agent reads every session
solverapp/                   optional local web UI (see below)
```

Each problem or exercise folder holds exactly those three files — reviews and notes stay
in chat.

## Solve in a browser (optional)

[`solverapp/`](solverapp/README.md) is a local web app: a problem list, and a
LeetCode-style split screen with the statement on the left and a Monaco editor on the
right. **Run** executes the real test suite and streams every case verdict; your
`solution.py` is only written when you press **Save**.

```powershell
solverapp\.venv\Scripts\python.exe solverapp\serve.py   # http://127.0.0.1:8000
```

It reads `problems/` and `learn/` directly, so a new folder appears on refresh. The
**Learn** tab shows the roadmap with per-topic progress, and each topic's lesson next to
its ladder. Setup and details are in [`solverapp/README.md`](solverapp/README.md). The CLI
above is unaffected and still works with no install step.

## Prompts that work

- *"Start the next topic"* / *"teach me sliding window"* — writes the lesson and the
  first exercise of the learning path.
- *"Next rung"* — the next exercise in the current topic, adapted to your last review.
- *"Give me a new problem"* — medium by default; add "easy"/"hard" or a topic
  ("sliding window", "graphs", "DP") to steer it.
- *"Review my solution for p001"* / *"review L1.3"* — runs tests, then critiques.
- *"Hint for p002"* — escalating nudges, no spoilers.
- *"Show me the optimal solution for p001"* — only reveals when you ask.

## Requirements

Python 3.10+. No third-party packages, no virtualenv, nothing to install.

## AI autocomplete is disabled here

[`.vscode/settings.json`](.vscode/settings.json) turns off Copilot ghost-text, next-edit
suggestions, and inline suggestions for this workspace — otherwise autocomplete just fills
in the answer and you learn nothing. **Copilot Chat still works**, which is how you get
problems, hints, and reviews.

To temporarily re-enable (e.g. you're done practising and want to refactor quickly), flip
the values in `github.copilot.enable` to `true` and reload the window
(`Ctrl+Shift+P` → *Developer: Reload Window*).

## VS Code tasks

- **Test current problem** — `Ctrl+Shift+B` while a file inside a problem folder is open
- **Test all problems** / **List problems** — `Ctrl+Shift+P` → *Tasks: Run Task*
- **Start solver app** — launches the browser UI on <http://127.0.0.1:8000>

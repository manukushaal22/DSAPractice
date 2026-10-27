# Copilot instructions

This is a DSA practice repo. The full workflow — how to create a new problem, the exact
file template, and how to review the human's solution — lives in [`AGENTS.md`](../AGENTS.md)
at the repo root.

**Read `AGENTS.md` before doing anything in this repo.** Key rules:

- Never solve a problem for the human unless they explicitly ask.
- New problems go in `problems/pNNN-slug/` with `README.md`, `solution.py` (stub), `tests.py`.
  **Exactly those three files — never add a fourth.**
- The learning path lives in `learn/` (roadmap: `learn/README.md`). Each topic folder
  `learn/NN-slug/` holds a lesson `README.md` plus exercise folders `NN.K-slug/`, which
  follow the same three-file rule. Exercises are created one rung at a time (AGENTS.md
  Task C).
- Reviews are delivered in chat only. Never write `REVIEW.md` or any other notes file.
- Tests run with `py run.py N` (problems) or `py run.py L1.3` (learn exercises) — `py`,
  not `python`. Standard library only.
- Keep `PROGRESS.md` up to date; it is the cross-session memory.

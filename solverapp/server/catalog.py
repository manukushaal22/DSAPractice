"""Problem discovery and metadata parsing.

The catalog is derived entirely from files already in the repo:

* ``problems/pNNN-slug/README.md``  -> title, difficulty, topics
* ``problems/pNNN-slug/solution.py`` -> stub detection
* ``PROGRESS.md``                    -> status (todo / solved / revisit)

Nothing is written here. A new problem folder is picked up on the next request
because the cache key includes the directory listing and the mtimes of every
file it reads.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[2]
PROBLEMS_DIR = ROOT / "problems"
PROGRESS_FILE = ROOT / "PROGRESS.md"

# `# P009 — Largest Container` (em dash in practice, hyphen tolerated)
_TITLE_RE = re.compile(r"^#\s*(P\d+)\s*[\u2014\u2013-]\s*(.+?)\s*$", re.M)
_DIFFICULTY_RE = re.compile(r"^\*\*Difficulty:\*\*\s*(.+?)\s*$", re.M)
_TOPICS_RE = re.compile(r"^\*\*Topics:\*\*\s*(.+?)\s*$", re.M)
_STUB_RE = re.compile(r"^\s*raise NotImplementedError", re.M)
_FOLDER_RE = re.compile(r"^(p\d+)-(.+)$")

VALID_STATUSES = {"todo", "solved", "revisit"}


@dataclass
class ProgressRow:
    status: str = "todo"
    detail: str = ""
    complexity: str = ""
    solved_on: str = ""


@dataclass
class Problem:
    """Everything the list screen needs about one problem."""

    id: str  # "p009"
    slug: str  # "p009-largest-container"
    number: int  # 9
    title: str  # "Largest Container"
    difficulty: str  # "Medium"
    topics: list[str] = field(default_factory=list)
    status: str = "todo"  # from PROGRESS.md
    status_detail: str = ""
    complexity: str = ""
    solved_on: str = ""
    is_stub: bool = True  # solution.py still raises NotImplementedError


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def _strip_cell(cell: str) -> str:
    return cell.strip()


def parse_progress(text: str) -> dict[str, ProgressRow]:
    """Parse the PROGRESS.md table into ``{"p009": ProgressRow, ...}``.

    Malformed or missing rows are simply absent; callers fall back to defaults.
    """
    rows: dict[str, ProgressRow] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [_strip_cell(c) for c in line.strip("|").split("|")]
        if len(cells) < 5:
            continue
        key = cells[0].lower()
        if not re.fullmatch(r"p\d+", key):
            continue

        raw_status = cells[4]
        status, detail = "todo", ""
        bold = re.match(r"\*\*(\w+)\*\*\s*(?:[\u2014\u2013-]\s*(.*))?", raw_status)
        if bold:
            status = bold.group(1).lower()
            detail = (bold.group(2) or "").strip()
        elif raw_status:
            status = raw_status.split()[0].lower()
        if status not in VALID_STATUSES:
            status = "todo"

        rows[key] = ProgressRow(
            status=status,
            detail=detail,
            complexity=cells[5] if len(cells) > 5 else "",
            solved_on=cells[6] if len(cells) > 6 else "",
        )
    return rows


def parse_readme(text: str, fallback_title: str) -> tuple[str, str, list[str]]:
    """Return ``(title, difficulty, topics)`` from a problem README."""
    title_match = _TITLE_RE.search(text)
    title = title_match.group(2) if title_match else fallback_title

    difficulty_match = _DIFFICULTY_RE.search(text)
    difficulty = difficulty_match.group(1).strip() if difficulty_match else "Unknown"

    topics_match = _TOPICS_RE.search(text)
    topics: list[str] = []
    if topics_match:
        topics = [t.strip() for t in topics_match.group(1).split(",") if t.strip()]

    return title, difficulty, topics


def _titleise(slug_tail: str) -> str:
    return slug_tail.replace("-", " ").title()


def problem_dirs() -> list[Path]:
    """Folders under ``problems/`` that carry a test suite. Mirrors dsakit.runner."""
    if not PROBLEMS_DIR.is_dir():
        return []
    return sorted(
        p for p in PROBLEMS_DIR.iterdir() if p.is_dir() and (p / "tests.py").is_file()
    )


def _signature() -> tuple:
    """Cheap change-detector: folder set plus mtimes of every file we parse."""
    parts: list = []
    try:
        parts.append(PROGRESS_FILE.stat().st_mtime_ns)
    except OSError:
        parts.append(0)
    for directory in problem_dirs():
        entry = [directory.name]
        for name in ("README.md", "solution.py"):
            try:
                entry.append((directory / name).stat().st_mtime_ns)
            except OSError:
                entry.append(0)
        parts.append(tuple(entry))
    return tuple(parts)


_cache: dict = {"signature": None, "problems": []}


def load_problems(force: bool = False) -> list[Problem]:
    """All problems, newest folder contents included. Cached on an mtime signature."""
    signature = _signature()
    if not force and _cache["signature"] == signature:
        return _cache["problems"]

    progress = parse_progress(_read(PROGRESS_FILE))
    problems: list[Problem] = []

    for directory in problem_dirs():
        folder = _FOLDER_RE.match(directory.name)
        if not folder:
            continue
        pid, tail = folder.group(1).lower(), folder.group(2)

        title, difficulty, topics = parse_readme(
            _read(directory / "README.md"), _titleise(tail)
        )
        row = progress.get(pid, ProgressRow())
        solution_text = _read(directory / "solution.py")

        problems.append(
            Problem(
                id=pid,
                slug=directory.name,
                number=int(pid[1:]),
                title=title,
                difficulty=difficulty,
                topics=topics,
                status=row.status,
                status_detail=row.detail,
                complexity=row.complexity,
                solved_on=row.solved_on,
                is_stub=bool(_STUB_RE.search(solution_text)) or not solution_text,
            )
        )

    problems.sort(key=lambda p: p.number)
    _cache["signature"] = signature
    _cache["problems"] = problems
    return problems


def find_problem(problem_id: str) -> Optional[Problem]:
    """Look up by id (``p009``), bare number (``9``), or full slug."""
    token = (problem_id or "").strip().lower()
    if not token:
        return None
    if token.isdigit():
        token = f"p{int(token):03d}"

    problems = load_problems()
    for problem in problems:
        if token in (problem.id, problem.slug):
            return problem
    return None


def problem_dir(problem: Problem) -> Path:
    return PROBLEMS_DIR / problem.slug


def as_dict(problem: Problem) -> dict:
    """camelCase for the TypeScript client."""
    raw = asdict(problem)
    renames = {
        "status_detail": "statusDetail",
        "solved_on": "solvedOn",
        "is_stub": "isStub",
    }
    return {renames.get(key, key): value for key, value in raw.items()}

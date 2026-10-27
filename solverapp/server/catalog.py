"""Problem discovery and metadata parsing.

The catalog is derived entirely from files already in the repo:

* ``problems/pNNN-slug/README.md``           -> title, difficulty, topics
* ``problems/pNNN-slug/solution.py``          -> stub detection
* ``learn/README.md``                         -> curriculum (topics, phases, start rungs)
* ``learn/NN-topic/README.md``                -> the topic's lesson
* ``learn/NN-topic/NN.K-slug/{README,solution}`` -> same as a problem
* ``PROGRESS.md``                             -> status (todo / solved / revisit)

Nothing is written here. A new folder is picked up on the next request because
the cache key includes the directory listings and the mtimes of every file it reads.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[2]
PROBLEMS_DIR = ROOT / "problems"
LEARN_DIR = ROOT / "learn"
LEARN_ROADMAP = LEARN_DIR / "README.md"
PROGRESS_FILE = ROOT / "PROGRESS.md"

# `# P009 — Largest Container` / `# L01.3 — Group Rearranged Words`
# (em dash in practice, hyphen tolerated)
_TITLE_RE = re.compile(r"^#\s*(P\d+|L\d+\.\d+[a-z]?)\s*[\u2014\u2013-]\s*(.+?)\s*$", re.M)
_DIFFICULTY_RE = re.compile(r"^\*\*Difficulty:\*\*\s*(.+?)\s*$", re.M)
_TOPICS_RE = re.compile(r"^\*\*Topics:\*\*\s*(.+?)\s*$", re.M)
_STUB_RE = re.compile(r"^\s*raise NotImplementedError", re.M)
_FOLDER_RE = re.compile(r"^(p\d+)-(.+)$")

# Mirrors dsakit.runner.
_TOPIC_FOLDER_RE = re.compile(r"^(\d{2})-[a-z0-9-]+$")
_EXERCISE_FOLDER_RE = re.compile(r"^(\d{2})\.(\d+)([a-z]?)-(.+)$")
_LEARN_ID_RE = re.compile(r"^l(\d{1,2})\.(\d+)([a-z]?)$")
_PROGRESS_KEY_RE = re.compile(r"p\d+|l\d+\.\d+[a-z]?")
_LESSON_TITLE_RE = re.compile(r"^#\s*\d+\s*[\u2014\u2013-]\s*(.+?)\s*$", re.M)
_CURRENT_TOPIC_RE = re.compile(r"\*\*Current topic:\*\*\s*(\d{1,2})\b")
_MD_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]*\)")

VALID_STATUSES = {"todo", "solved", "revisit"}
FINAL_REQUIRED_RUNG = 5  # .6 is optional


@dataclass
class ProgressRow:
    status: str = "todo"
    detail: str = ""
    complexity: str = ""
    solved_on: str = ""


@dataclass
class Problem:
    """Everything the list screen needs about one problem or learn exercise."""

    id: str  # "p009" / "L01.3"
    slug: str  # "p009-largest-container" / "01.3-group-rearranged-words"
    number: int  # 9 / rung 3
    title: str  # "Largest Container"
    difficulty: str  # "Medium"
    topics: list[str] = field(default_factory=list)
    status: str = "todo"  # from PROGRESS.md
    status_detail: str = ""
    complexity: str = ""
    solved_on: str = ""
    is_stub: bool = True  # solution.py still raises NotImplementedError
    track: str = "problems"  # "problems" | "learn"
    topic: str = ""  # learn only: "01"
    rung: str = ""  # learn only: "3", "3b"
    rel_dir: str = ""  # "problems/p009-..." / "learn/01-.../01.3-..."


@dataclass
class Topic:
    """One row of the learn/ curriculum, merged with what exists on disk."""

    id: str  # "01"
    number: int
    title: str
    folder: str  # "01-arrays-and-hashing"
    phase: str = ""
    needs: list[str] = field(default_factory=list)
    start_rung: int = 1
    related: list[str] = field(default_factory=list)  # ["p001", "p009"]
    has_lesson: bool = False
    status: str = "upcoming"  # "upcoming" | "in-progress" | "complete"
    required: int = 0  # rungs from start_rung to .5
    required_solved: int = 0
    is_current: bool = False
    exercises: list[Problem] = field(default_factory=list)


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
        if not _PROGRESS_KEY_RE.fullmatch(key):
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


def topic_dirs() -> list[Path]:
    if not LEARN_DIR.is_dir():
        return []
    return sorted(
        p for p in LEARN_DIR.iterdir() if p.is_dir() and _TOPIC_FOLDER_RE.match(p.name)
    )


def exercise_dirs(topic: Path) -> list[Path]:
    """Exercise folders of one topic in rung order. Mirrors dsakit.runner."""
    found = []
    for p in topic.iterdir():
        match = _EXERCISE_FOLDER_RE.match(p.name)
        if p.is_dir() and match and (p / "tests.py").is_file():
            found.append((int(match.group(2)), match.group(3), p.name, p))
    return [entry[-1] for entry in sorted(found)]


def _mtime(path: Path) -> int:
    try:
        return path.stat().st_mtime_ns
    except OSError:
        return 0


def _signature() -> tuple:
    """Cheap change-detector: folder sets plus mtimes of every file we parse."""
    parts: list = [_mtime(PROGRESS_FILE), _mtime(LEARN_ROADMAP)]
    for directory in problem_dirs():
        parts.append(
            (directory.name, _mtime(directory / "README.md"), _mtime(directory / "solution.py"))
        )
    for topic in topic_dirs():
        parts.append((topic.name, _mtime(topic / "README.md")))
        for directory in exercise_dirs(topic):
            parts.append(
                (directory.name, _mtime(directory / "README.md"), _mtime(directory / "solution.py"))
            )
    return tuple(parts)


_cache: dict = {"signature": None, "problems": [], "topics": []}


def _make_problem(directory: Path, progress: dict[str, ProgressRow], **fields) -> Problem:
    """Shared by both tracks: README metadata, PROGRESS.md status, stub detection."""
    title, difficulty, topics = parse_readme(
        _read(directory / "README.md"), fields.pop("fallback_title")
    )
    row = progress.get(fields["id"].lower(), ProgressRow())
    solution_text = _read(directory / "solution.py")
    return Problem(
        slug=directory.name,
        title=title,
        difficulty=difficulty,
        topics=topics,
        status=row.status,
        status_detail=row.detail,
        complexity=row.complexity,
        solved_on=row.solved_on,
        is_stub=bool(_STUB_RE.search(solution_text)) or not solution_text,
        rel_dir=directory.relative_to(ROOT).as_posix(),
        **fields,
    )


def _plain(cell: str) -> str:
    """Strip markdown links and code ticks from a table cell."""
    return _MD_LINK_RE.sub(r"\1", cell).replace("`", "").strip()


def parse_curriculum(text: str) -> list[Topic]:
    """Rows of the curriculum table in learn/README.md.

    ``| 01 | [Arrays & Hashing](...) | `01-arrays-and-hashing` | Linear basics | — | .3 | p001 |``
    """
    topics: list[Topic] = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 7 or not re.fullmatch(r"\d{2}", cells[0]):
            continue
        start = re.search(r"\d+", cells[5])
        topics.append(
            Topic(
                id=cells[0],
                number=int(cells[0]),
                title=_plain(cells[1]),
                folder=_plain(cells[2]),
                phase=_plain(cells[3]),
                needs=re.findall(r"\d{2}", cells[4]),
                start_rung=int(start.group()) if start else 1,
                related=re.findall(r"p\d{3}", cells[6].lower()),
            )
        )
    return topics


def _finish_topic(topic: Topic, current: Optional[str]) -> None:
    """Derive status/progress. A rung counts as solved if it or a sibling (3b) is."""
    solved_rungs = {
        int(re.match(r"\d+", ex.rung).group()) for ex in topic.exercises if ex.status == "solved"
    }
    required = range(topic.start_rung, FINAL_REQUIRED_RUNG + 1)
    topic.required = len(required)
    topic.required_solved = sum(1 for rung in required if rung in solved_rungs)
    topic.is_current = topic.id == current
    if topic.required and topic.required_solved == topic.required:
        topic.status = "complete"
    elif topic.exercises or topic.has_lesson:
        topic.status = "in-progress"
    else:
        topic.status = "upcoming"


def _load(force: bool = False) -> dict:
    signature = _signature()
    if not force and _cache["signature"] == signature:
        return _cache

    progress_text = _read(PROGRESS_FILE)
    progress = parse_progress(progress_text)

    problems: list[Problem] = []
    for directory in problem_dirs():
        folder = _FOLDER_RE.match(directory.name)
        if not folder:
            continue
        pid, tail = folder.group(1).lower(), folder.group(2)
        problems.append(
            _make_problem(
                directory, progress, id=pid, number=int(pid[1:]), fallback_title=_titleise(tail)
            )
        )
    problems.sort(key=lambda p: p.number)

    topics = parse_curriculum(_read(LEARN_ROADMAP))
    by_folder = {topic.folder: topic for topic in topics}
    for topic_dir in topic_dirs():
        topic = by_folder.get(topic_dir.name)
        lesson = _read(topic_dir / "README.md")
        if topic is None:  # on disk but missing from the roadmap table
            number = int(_TOPIC_FOLDER_RE.match(topic_dir.name).group(1))
            heading = _LESSON_TITLE_RE.search(lesson)
            topic = Topic(
                id=f"{number:02d}",
                number=number,
                title=heading.group(1) if heading else _titleise(topic_dir.name[3:]),
                folder=topic_dir.name,
            )
            topics.append(topic)
            by_folder[topic.folder] = topic
        topic.has_lesson = bool(lesson)
        for directory in exercise_dirs(topic_dir):
            match = _EXERCISE_FOLDER_RE.match(directory.name)
            rung = f"{int(match.group(2))}{match.group(3)}"
            topic.exercises.append(
                _make_problem(
                    directory,
                    progress,
                    id=f"L{match.group(1)}.{rung}",
                    number=int(match.group(2)),
                    fallback_title=_titleise(match.group(4)),
                    track="learn",
                    topic=match.group(1),
                    rung=rung,
                )
            )

    current_match = _CURRENT_TOPIC_RE.search(progress_text)
    current = f"{int(current_match.group(1)):02d}" if current_match else None
    for topic in topics:
        _finish_topic(topic, current)
    topics.sort(key=lambda t: t.number)

    _cache.update(signature=signature, problems=problems, topics=topics)
    return _cache


def load_problems(force: bool = False) -> list[Problem]:
    """All problems/ entries, newest folder contents included. Cached on an mtime signature."""
    return _load(force)["problems"]


def load_topics(force: bool = False) -> list[Topic]:
    """The learn/ curriculum with each topic's exercises and derived progress."""
    return _load(force)["topics"]


def find_topic(topic_id: str) -> Optional[Topic]:
    """Look up by number (``1`` / ``01``) or folder name."""
    token = (topic_id or "").strip().lower()
    if token.isdigit():
        token = f"{int(token):02d}"
    for topic in load_topics():
        if token in (topic.id, topic.folder):
            return topic
    return None


def find_problem(problem_id: str) -> Optional[Problem]:
    """Look up by id (``p009`` / ``L01.3`` / ``L1.3``), bare number (``9``), or slug."""
    token = (problem_id or "").strip().lower()
    if not token:
        return None
    if token.isdigit():
        token = f"p{int(token):03d}"
    learn_id = _LEARN_ID_RE.match(token)
    if learn_id:
        token = f"l{int(learn_id.group(1)):02d}.{int(learn_id.group(2))}{learn_id.group(3)}"

    data = _load()
    candidates = data["problems"] + [ex for topic in data["topics"] for ex in topic.exercises]
    for problem in candidates:
        if token in (problem.id.lower(), problem.slug.lower()):
            return problem
    return None


def problem_dir(problem: Problem) -> Path:
    return ROOT / problem.rel_dir


def lesson_text(topic: Topic) -> str:
    return _read(LEARN_DIR / topic.folder / "README.md")


_RENAMES = {
    "status_detail": "statusDetail",
    "solved_on": "solvedOn",
    "is_stub": "isStub",
    "rel_dir": "relDir",
    "start_rung": "startRung",
    "has_lesson": "hasLesson",
    "required_solved": "requiredSolved",
    "is_current": "isCurrent",
}


def as_dict(problem: Problem) -> dict:
    """camelCase for the TypeScript client."""
    return {_RENAMES.get(key, key): value for key, value in asdict(problem).items()}


def topic_dict(topic: Topic, last_runs: dict) -> dict:
    """camelCase topic with its exercises (and their last-run badges) inlined."""
    raw = {_RENAMES.get(k, k): v for k, v in asdict(topic).items() if k != "exercises"}
    raw["exercises"] = [
        {**as_dict(ex), "lastRun": last_runs.get(ex.id)} for ex in topic.exercises
    ]
    return raw

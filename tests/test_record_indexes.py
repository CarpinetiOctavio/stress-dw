"""Index checks of the decision log, the method lessons and the concept homes.

What is checked is set by LOG-004 and LOG-010 of the decision log
(docs/decisions/log/):

* Every log entry and every lesson file has an index row, and every row a
  file; index titles equal the files' first headings; index statuses equal
  the frontmatter. The decision-record index of docs/decisions/README.md is
  checked against its records in the same way.
* Every LOG- identifier cited by a lesson resolves to a log entry.
* Every home cited in docs/concept-homes.md resolves, file and anchor; a row
  whose home reads "open" is a declared gap.
* Once the documentation-currency register is versioned, every finding
  identifier cited by a log entry resolves to a finding row of the register,
  and every LSN- identifier cited by the register resolves to a lesson. Until
  then these two checks are skipped.

Every check takes the repository root as a parameter.
"""

import re
from pathlib import Path

import pytest

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent

LOG = Path("docs/decisions/log")
LESSONS = Path("docs/audit/lessons")
DECISIONS = Path("docs/decisions")
CONCEPT_HOMES = Path("docs/concept-homes.md")
REGISTER = Path("docs/audit/documentation-currency.md")

LINKED_ROW = re.compile(
    r"^\|\s*\[(?P<id>[^\]]+)\]\((?P<file>[^)]+)\)\s*\|\s*(?P<title>.*?)\s*\|"
    r"\s*(?P<status>[^|]*?)\s*\|\s*$"
)
LESSON_ROW = re.compile(
    r"^\|\s*(?P<theme>[^|]+?)\s*\|\s*\[`[^`]+`\]\((?P<file>[^)]+)\)\s*\|"
    r"\s*(?P<lessons>LSN-[^|]*?)\s*\|\s*$"
)
HEADING = re.compile(r"^(#{1,6})\s+(?P<text>.+?)\s*$")
LESSON_HEADING = re.compile(r"^## (LSN-\d{3})\b", re.MULTILINE)
LINK = re.compile(r"\]\((?P<target>[^)\s]+)\)")
LOG_ID = re.compile(r"\bLOG-\d{3}\b")
LSN_ID = re.compile(r"\bLSN-\d{3}\b")
DC_ID = re.compile(r"\bDC-\d{2,3}\b")
REGISTER_ROW = re.compile(r"^\| (DC-\d{2,3}) ", re.MULTILINE)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _first_heading(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def _frontmatter_status(text: str) -> str:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return ""
    for line in lines[1:]:
        if line == "---":
            break
        if line.startswith("status:"):
            return line.split(":", 1)[1].strip().strip("\"'")
    return ""


def _linked_rows(index: Path) -> dict[str, tuple[str, str]]:
    rows: dict[str, tuple[str, str]] = {}
    for line in _read(index).splitlines():
        match = LINKED_ROW.match(line)
        if match:
            rows[match.group("file")] = (match.group("title"), match.group("status"))
    return rows


def _indexed_files_problems(
    folder: Path, pattern: str, rows: dict[str, tuple[str, str]]
) -> list[str]:
    files = {path.name for path in folder.glob(pattern)}
    problems = [f"no index row: {name}" for name in sorted(files - set(rows))]
    problems += [f"no file: {name}" for name in sorted(set(rows) - files)]
    return problems


def _title_problems(folder: Path, rows: dict[str, tuple[str, str]]) -> list[str]:
    problems: list[str] = []
    for name, (title, _) in sorted(rows.items()):
        path = folder / name
        if path.is_file() and _first_heading(_read(path)) != title:
            problems.append(f"title differs from first heading: {name}")
    return problems


def _status_problems(folder: Path, rows: dict[str, tuple[str, str]]) -> list[str]:
    problems: list[str] = []
    for name, (_, status) in sorted(rows.items()):
        path = folder / name
        if path.is_file() and _frontmatter_status(_read(path)) != status:
            problems.append(f"status differs from frontmatter: {name}")
    return problems


def log_index_problems(root: Path) -> list[str]:
    """Compares the decision-log index with the log entries.

    Args:
        root: The repository root.

    Returns:
        One line per entry without a row, row without an entry, or row whose
        title or status differs from its entry.
    """
    folder = root / LOG
    rows = _linked_rows(folder / "README.md")
    return (
        _indexed_files_problems(folder, "LOG-[0-9][0-9][0-9]-*.md", rows)
        + _title_problems(folder, rows)
        + _status_problems(folder, rows)
    )


def decision_index_problems(root: Path) -> list[str]:
    """Compares the decision-record index with the decision records.

    Args:
        root: The repository root.

    Returns:
        One line per record without a row, row without a record, or row whose
        title or status differs from its record.
    """
    folder = root / DECISIONS
    rows = _linked_rows(folder / "README.md")
    rows = {name: row for name, row in rows.items() if "/" not in name}
    return (
        _indexed_files_problems(folder, "[0-9][0-9][0-9][0-9]-*.md", rows)
        + _title_problems(folder, rows)
        + _status_problems(folder, rows)
    )


def lesson_index_problems(root: Path) -> list[str]:
    """Compares the lesson index with the lesson files.

    Args:
        root: The repository root.

    Returns:
        One line per theme file without a row, row without a file, or row
        whose theme or lesson list differs from its file.
    """
    folder = root / LESSONS
    rows: dict[str, tuple[str, list[str]]] = {}
    for line in _read(folder / "README.md").splitlines():
        match = LESSON_ROW.match(line)
        if match:
            lessons = [item.strip() for item in match.group("lessons").split(",")]
            rows[match.group("file")] = (match.group("theme"), lessons)
    files = {path.name for path in folder.glob("*.md")} - {"README.md"}
    problems = [f"no index row: {name}" for name in sorted(files - set(rows))]
    problems += [f"no file: {name}" for name in sorted(set(rows) - files)]
    for name, (theme, lessons) in sorted(rows.items()):
        path = folder / name
        if not path.is_file():
            continue
        text = _read(path)
        if _first_heading(text) != theme:
            problems.append(f"theme differs from first heading: {name}")
        if LESSON_HEADING.findall(text) != lessons:
            problems.append(f"lesson list differs from lesson headings: {name}")
    return problems


def _log_ids(root: Path) -> set[str]:
    return {path.name[:7] for path in (root / LOG).glob("LOG-[0-9][0-9][0-9]-*.md")}


def _lesson_ids(root: Path) -> set[str]:
    ids: set[str] = set()
    for path in (root / LESSONS).glob("*.md"):
        ids.update(LESSON_HEADING.findall(_read(path)))
    return ids


def lesson_log_citation_problems(root: Path) -> list[str]:
    """Lists LOG- identifiers cited by lessons that match no log entry.

    Args:
        root: The repository root.

    Returns:
        One line per unresolved identifier, with the lesson file citing it.
    """
    known = _log_ids(root)
    problems: list[str] = []
    for path in sorted((root / LESSONS).glob("*.md")):
        for cited in sorted(set(LOG_ID.findall(_read(path))) - known):
            problems.append(f"{path.name}: {cited}")
    return problems


def _anchors(text: str) -> set[str]:
    anchors: set[str] = set()
    seen: dict[str, int] = {}
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        match = None if in_fence else HEADING.match(line)
        if match:
            text_ = match.group("text").lower()
            slug = "".join(c for c in text_ if c.isalnum() or c in " -_")
            slug = slug.replace(" ", "-")
            count = seen.get(slug, 0)
            seen[slug] = count + 1
            anchors.add(slug if count == 0 else f"{slug}-{count}")
    return anchors


def concept_home_problems(root: Path) -> list[str]:
    """Lists homes in docs/concept-homes.md that do not resolve.

    A row whose home reads "open" is a declared gap and is not checked.

    Args:
        root: The repository root.

    Returns:
        One line per row whose home has no link, or whose link names a
        missing file or a missing anchor.
    """
    path = root / CONCEPT_HOMES
    problems: list[str] = []
    for line in _read(path).splitlines():
        cells = [cell.strip() for cell in line.split("|")]
        if len(cells) < 6 or not cells[1].isdigit():
            continue
        number, home = cells[1], cells[3]
        if home.startswith("open"):
            continue
        targets = [match.group("target") for match in LINK.finditer(home)]
        if not targets:
            problems.append(f"row {number}: no link")
        for target in targets:
            file_part, _, anchor = target.partition("#")
            resolved = (path.parent / file_part).resolve()
            if not resolved.is_file():
                problems.append(f"row {number}: no file {file_part}")
            elif anchor and anchor not in _anchors(_read(resolved)):
                problems.append(f"row {number}: no anchor {target}")
    return problems


def log_finding_citation_problems(root: Path) -> list[str]:
    """Lists finding identifiers cited by log entries that match no register row.

    Args:
        root: The repository root; its versioned register must exist.

    Returns:
        One line per unresolved identifier, with the log entry citing it.
    """
    known = set(REGISTER_ROW.findall(_read(root / REGISTER)))
    problems: list[str] = []
    for path in sorted((root / LOG).glob("LOG-[0-9][0-9][0-9]-*.md")):
        for cited in sorted(set(DC_ID.findall(_read(path))) - known):
            problems.append(f"{path.name}: {cited}")
    return problems


def register_lesson_citation_problems(root: Path) -> list[str]:
    """Lists LSN- identifiers cited by the register that match no lesson.

    Args:
        root: The repository root; its versioned register must exist.

    Returns:
        One line per unresolved identifier.
    """
    cited = set(LSN_ID.findall(_read(root / REGISTER)))
    return sorted(cited - _lesson_ids(root))


def test_the_log_index_matches_the_log_entries() -> None:
    assert log_index_problems(REPOSITORY_ROOT) == []


def test_the_decision_record_index_matches_the_decision_records() -> None:
    assert decision_index_problems(REPOSITORY_ROOT) == []


def test_the_lesson_index_matches_the_lesson_files() -> None:
    assert lesson_index_problems(REPOSITORY_ROOT) == []


def test_every_log_identifier_cited_by_a_lesson_resolves_to_an_entry() -> None:
    assert lesson_log_citation_problems(REPOSITORY_ROOT) == []


def test_every_concept_home_resolves_or_is_declared_open() -> None:
    assert concept_home_problems(REPOSITORY_ROOT) == []


def test_every_finding_cited_by_a_log_entry_resolves_to_a_register_row() -> None:
    if not (REPOSITORY_ROOT / REGISTER).is_file():
        pytest.skip("the documentation-currency register is not versioned yet")
    assert log_finding_citation_problems(REPOSITORY_ROOT) == []


def test_every_lesson_cited_by_the_register_resolves_to_a_lesson() -> None:
    if not (REPOSITORY_ROOT / REGISTER).is_file():
        pytest.skip("the documentation-currency register is not versioned yet")
    assert register_lesson_citation_problems(REPOSITORY_ROOT) == []


def test_a_log_entry_without_an_index_row_is_reported(tmp_path: Path) -> None:
    folder = tmp_path / LOG
    folder.mkdir(parents=True)
    (folder / "README.md").write_text("# Decision log\n", encoding="utf-8")
    (folder / "LOG-001-placeholder.md").write_text(
        "---\nid: LOG-001\nstatus: recorded\n---\n\n# Placeholder\n", encoding="utf-8"
    )

    assert log_index_problems(tmp_path) == ["no index row: LOG-001-placeholder.md"]

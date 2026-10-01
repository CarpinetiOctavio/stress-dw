"""Mechanical check of the voice rule, docs/writing-conventions.md section 2.

The scan covers the files git tracks and the untracked files it does not
ignore, so a new document is checked before it is staged. It reads text
files only: images, binaries and the lock file are out of scope.

Three things are checked:

* Personal names. They are derived from the ``decision-makers`` lines of
  the decision records, so no name is written here. A whole-word match
  fails unless it is on a ``decision-makers`` line, inside a URL, or in
  ``LICENSE``. A name joined to another word by a slash is still a whole
  word and fails; an identifier in which the name runs into other word
  characters is not a whole-word match.
* Attribution of an act to a person, role or tool: a listed role or tool
  followed by a listed verb, or "according to", "per" or "as agreed with"
  (and similar) followed by a listed role or tool.
* First and second person, in Markdown prose; in Python comments,
  docstrings, test names and assertion messages; and in SQL comments.
  Fenced code, inline code and text in quotation marks are skipped in
  Markdown. The root README is exempt from this check only.

What the scan cannot detect: an attribution phrased freely, without a
name, a listed role or a listed tool, passes; so does a pronoun inside a
quotation that is not verbatim; so does prose in a Python string that
is neither a docstring nor an assertion message. Commit messages and
pull-request text are outside the repository tree and are covered by
the rule, not by this check.
"""

import ast
import io
import re
import subprocess
import tokenize
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent

TEXT_SUFFIXES = {".md", ".py", ".sql", ".toml", ".properties"}
TEXT_NAMES = {".gitignore", ".python-version", "LICENSE"}
PROSE_SUFFIXES = {".md", ".py", ".sql"}

URL = re.compile(r"https?://\S+")
INLINE_CODE = re.compile(r"`[^`]*`")
QUOTATION = re.compile(r"\"[^\"]*\"|“[^”]*”")

SUBJECT = (
    r"(?:(?i:the\s+(?:author|owner|user|developer|professor|reviewer"
    r"|assistant|chat))|Code|Claude)"
)
VERB = (
    r"(?:think|thinks|thought|believe[sd]?|decide[sd]?|chose|chooses?"
    r"|want(?:s|ed)?|prefer(?:s|red)?|ask(?:s|ed)?|request(?:s|ed)?"
    r"|notice[sd]?|found|discover(?:s|ed)?|report(?:s|ed)?"
    r"|recommend(?:s|ed)?|suggest(?:s|ed)?|propose[sd]?|confirm(?:s|ed)?"
    r"|approve[sd]?|agree[sd]?)"
)
ATTRIBUTION = (
    re.compile(rf"\b{SUBJECT}\s+(?:(?i:has|had|have|will|did|does)\s+)?(?i:{VERB})\b"),
    re.compile(
        r"(?i:\baccording\s+to|\bper|\bas\s+(?:agreed|discussed|requested|decided"
        rf"|suggested|proposed)\s+(?:with|by))\s+{SUBJECT}\b"
    ),
)
# The pronoun's letter followed by a period is an author's initial in a reference list.
PERSON = re.compile(r"\bI\b(?!\.)|\b(?i:we|my|our|you|your)\b|\b(?:us|Us)\b")
PROPER_NOUNS = ("Our World in Data",)


def _scanned_files(root: Path) -> list[Path]:
    listing = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    paths = [root / name for name in listing.split("\0") if name]
    return sorted(
        path
        for path in paths
        if path.is_file() and (path.suffix in TEXT_SUFFIXES or path.name in TEXT_NAMES)
    )


def _decision_maker_names(root: Path) -> set[str]:
    names: set[str] = set()
    for record in sorted((root / "docs" / "decisions").glob("[0-9]*.md")):
        for line in record.read_text(encoding="utf-8").splitlines():
            if line.startswith("decision-makers:"):
                for person in line.split(":", 1)[1].split(","):
                    names.update(person.split())
    return names


def _markdown_prose(text: str) -> list[tuple[int, str]]:
    prose: list[tuple[int, str]] = []
    in_fence = False
    for number, line in enumerate(text.splitlines(), start=1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            line = QUOTATION.sub(" ", INLINE_CODE.sub(" ", line))
            prose.append((number, line))
    return prose


def _python_prose(text: str) -> list[tuple[int, str]]:
    prose: list[tuple[int, str]] = [
        (token.start[0], token.string)
        for token in tokenize.generate_tokens(io.StringIO(text).readline)
        if token.type == tokenize.COMMENT
    ]
    tree = ast.parse(text)
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.ClassDef | ast.FunctionDef):
            body = node.body
            if (
                body
                and isinstance(body[0], ast.Expr)
                and isinstance(body[0].value, ast.Constant)
                and isinstance(body[0].value.value, str)
            ):
                for offset, line in enumerate(body[0].value.value.splitlines()):
                    prose.append((body[0].lineno + offset, line))
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
            prose.append((node.lineno, node.name.replace("_", " ")))
        if (
            isinstance(node, ast.Assert)
            and isinstance(node.msg, ast.Constant)
            and isinstance(node.msg.value, str)
        ):
            prose.append((node.lineno, node.msg.value))
    return prose


def _sql_prose(text: str) -> list[tuple[int, str]]:
    return [
        (number, line.split("--", 1)[1])
        for number, line in enumerate(text.splitlines(), start=1)
        if "--" in line
    ]


def _prose(path: Path) -> list[tuple[int, str]]:
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".py":
        prose = _python_prose(text)
    elif path.suffix == ".sql":
        prose = _sql_prose(text)
    else:
        prose = _markdown_prose(text)
    return [(number, URL.sub(" ", line)) for number, line in prose]


def _name_hits(root: Path) -> list[str]:
    names = _decision_maker_names(root)
    pattern = re.compile(rf"\b(?:{'|'.join(map(re.escape, sorted(names)))})\b", re.I)
    hits: list[str] = []
    for path in _scanned_files(root):
        if path.name == "LICENSE":
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        for number, line in enumerate(lines, start=1):
            if line.startswith("decision-makers:"):
                continue
            for match in pattern.finditer(URL.sub(" ", line)):
                hits.append(f"{path.relative_to(root)}:{number}: {match.group(0)}")
    return hits


def _attribution_hits(root: Path) -> list[str]:
    hits: list[str] = []
    for path in _scanned_files(root):
        if path.suffix not in PROSE_SUFFIXES:
            continue
        for number, line in _prose(path):
            for pattern in ATTRIBUTION:
                for match in pattern.finditer(line):
                    hits.append(f"{path.relative_to(root)}:{number}: {match.group(0)}")
    return hits


def _person_hits(root: Path) -> list[str]:
    hits: list[str] = []
    for path in _scanned_files(root):
        if path.suffix not in PROSE_SUFFIXES or path == root / "README.md":
            continue
        for number, line in _prose(path):
            for proper_noun in PROPER_NOUNS:
                line = line.replace(proper_noun, " ")
            for match in PERSON.finditer(line):
                hits.append(f"{path.relative_to(root)}:{number}: {match.group(0)}")
    return hits


def test_decision_makers_fields_yield_at_least_one_name() -> None:
    assert _decision_maker_names(REPOSITORY_ROOT)


def test_no_personal_name_appears_outside_decision_makers_urls_and_license() -> None:
    assert _name_hits(REPOSITORY_ROOT) == []


def test_no_act_is_attributed_to_a_person_role_or_tool() -> None:
    assert _attribution_hits(REPOSITORY_ROOT) == []


def test_no_first_or_second_person_appears_outside_the_readme() -> None:
    assert _person_hits(REPOSITORY_ROOT) == []


def _scratch_repository(root: Path) -> None:
    # A scratch repository, so the check never writes into this one.
    subprocess.run(["git", "init", "--quiet"], cwd=root, check=True)
    record = root / "docs" / "decisions" / "0000-placeholder.md"
    record.parent.mkdir(parents=True)
    record.write_text(
        "---\ndecision-makers: Placeholder Person\n---\n", encoding="utf-8"
    )
    subprocess.run(["git", "add", str(record)], cwd=root, check=True)


def test_an_untracked_document_that_git_does_not_ignore_is_scanned(
    tmp_path: Path,
) -> None:
    _scratch_repository(tmp_path)
    (tmp_path / "draft.md").write_text("Drafted by Placeholder.\n", encoding="utf-8")

    assert _name_hits(tmp_path) == ["draft.md:1: Placeholder"]


def test_a_name_joined_to_another_word_by_a_slash_is_flagged(tmp_path: Path) -> None:
    _scratch_repository(tmp_path)
    (tmp_path / "draft.md").write_text(
        "Placeholder/Code decided this.\n", encoding="utf-8"
    )

    assert _name_hits(tmp_path) == ["draft.md:1: Placeholder"]
    assert _attribution_hits(tmp_path) == ["draft.md:1: Code decided"]

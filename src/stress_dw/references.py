"""Check the verification register of published sources against copies of them.

The register is `docs/references/verification.toml`; the rule it implements is
LOG-048. For each source, a copy is looked for in a given directory under the
file name the register gives, and, for a source whose copy is stored in the
repository, in `docs/references/`. The copy must match the registered SHA-256,
unless the register marks the source's hash as not reproducible because its
provider stamps each download, and each registered quotation must occur on its
printed page. Page text and
quotation are compared after Unicode NFKC normalization with all whitespace and
all hyphens (ASCII and soft) removed, so that line breaks, words broken across
lines and ligatures in the PDF do not decide the result.

Run from the repository root, with a directory holding the copies:

    uv run python -m stress_dw.references <directory>
"""

import argparse
import hashlib
import logging
import re
import sys
import tomllib
import unicodedata
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from pypdf import PdfReader
from pypdf.errors import PdfReadError

REGISTER_PATH = Path("docs/references/verification.toml")
STORED_COPIES = Path("docs/references")

# Whitespace, the ASCII hyphen and the soft hyphen: a PDF may keep the hyphen of
# a word broken across lines, so hyphens are dropped from page and quotation alike.
IGNORED = re.compile(r"[\s\-\u00ad]+")
# pypdf returns "/NNN" character codes for a font without a Unicode map.
CHARACTER_CODE = re.compile(r"/(\d{1,3})")


@dataclass(frozen=True)
class Claim:
    """One claim, the printed page that supports it and a verbatim quotation."""

    claim: str
    page: int
    quote: str
    cited_in: tuple[str, ...]
    pdf_page: int | None = None


@dataclass(frozen=True)
class Source:
    """One published source of the register and its claims."""

    id: str
    citation: str
    doi: str
    retrieved_from: str
    retrieved_on: date
    file: str
    sha256: str
    first_page: int
    licence: str
    stored: bool
    claims: tuple[Claim, ...]
    version: str = "published"
    leading_pages: int = 0
    reproducible_hash: bool = True


@dataclass(frozen=True)
class CheckResult:
    """What checking one copy found: problems fail the check, notes do not."""

    problems: list[str]
    notes: list[str]


def _field(entry: dict[str, Any], name: str, kind: type, where: str) -> Any:
    value = entry.get(name)
    # A TOML boolean is a Python int too; it is accepted only where a bool is due.
    if not isinstance(value, kind) or isinstance(value, bool) != (kind is bool):
        raise ValueError(f"{where}: field '{name}' missing or not {kind.__name__}")
    return value


def _optional(
    entry: dict[str, Any], name: str, kind: type, default: Any, where: str
) -> Any:
    return _field(entry, name, kind, where) if name in entry else default


def _claim(entry: dict[str, Any], where: str) -> Claim:
    cited_in = _field(entry, "cited_in", list, where)
    if not all(isinstance(item, str) for item in cited_in):
        raise ValueError(f"{where}: field 'cited_in' holds a non-string item")
    return Claim(
        claim=_field(entry, "claim", str, where),
        page=_field(entry, "page", int, where),
        quote=_field(entry, "quote", str, where),
        cited_in=tuple(cited_in),
        pdf_page=_optional(entry, "pdf_page", int, None, where),
    )


def load_register(path: Path = REGISTER_PATH) -> list[Source]:
    """Read the register at `path`, raising `ValueError` on any malformed entry."""
    with path.open("rb") as handle:
        entries = tomllib.load(handle).get("source", [])
    sources = []
    for number, entry in enumerate(entries, start=1):
        where = f"source {entry.get('id', number)}"
        claims = _field(entry, "claim", list, where)
        sources.append(
            Source(
                id=_field(entry, "id", str, where),
                citation=_field(entry, "citation", str, where),
                doi=_field(entry, "doi", str, where),
                retrieved_from=_field(entry, "retrieved_from", str, where),
                retrieved_on=_field(entry, "retrieved_on", date, where),
                file=_field(entry, "file", str, where),
                sha256=_field(entry, "sha256", str, where),
                first_page=_field(entry, "first_page", int, where),
                licence=_field(entry, "licence", str, where),
                stored=_field(entry, "stored", bool, where),
                claims=tuple(
                    _claim(claim, f"{where}, claim {index}")
                    for index, claim in enumerate(claims, start=1)
                ),
                version=_optional(entry, "version", str, "published", where),
                leading_pages=_optional(entry, "leading_pages", int, 0, where),
                reproducible_hash=_optional(
                    entry, "reproducible_hash", bool, True, where
                ),
            )
        )
    return sources


def normalize(text: str) -> str:
    """Return `text` in Unicode NFKC form with whitespace and hyphens removed."""
    return IGNORED.sub("", unicodedata.normalize("NFKC", text))


def page_text(raw: str) -> str:
    """Return `raw` with pypdf's character codes decoded, where it consists of them.

    A page whose non-whitespace text is mostly "/NNN" codes comes from a font
    without a Unicode map; each code is the character's number. Any other page
    is returned unchanged, so a slash followed by digits in ordinary text is kept.
    """
    coded = sum(len(match[0]) for match in CHARACTER_CODE.finditer(raw))
    if coded > len("".join(raw.split())) / 2:
        return CHARACTER_CODE.sub(lambda match: chr(int(match[1])), raw)
    return raw


def sha256_of(path: Path) -> str:
    """Return the hexadecimal SHA-256 of the file at `path`."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_source(source: Source, copy: Path) -> CheckResult:
    """Check `copy` against `source`.

    A differing hash is a problem, and the quotations are not read, since they
    would be checked against a different document; for a source whose hash is
    not reproducible it is a note, and the quotations are read. The PDF page of
    a printed page skips the source's `leading_pages`, unless the claim gives
    its own `pdf_page`, as a scan whose page offset varies requires.
    """
    actual = sha256_of(copy)
    notes = []
    if actual != source.sha256:
        mismatch = f"{source.id}: SHA-256 of {copy} is {actual}, not {source.sha256}"
        if source.reproducible_hash:
            return CheckResult(problems=[mismatch], notes=[])
        notes.append(f"{mismatch}; the provider stamps each download")
    try:
        reader = PdfReader(copy)
        pages = [normalize(page_text(page.extract_text())) for page in reader.pages]
    except PdfReadError as error:
        problem = f"{source.id}: {copy} could not be read as a PDF: {error}"
        return CheckResult(problems=[problem], notes=notes)
    problems = []
    for claim in source.claims:
        if claim.pdf_page is not None:
            index, lowest = claim.pdf_page - 1, 0
        else:
            index = claim.page - source.first_page + source.leading_pages
            lowest = source.leading_pages
        if not lowest <= index < len(pages):
            problems.append(f"{source.id}: p. {claim.page} is not in {copy}")
        elif normalize(claim.quote) not in pages[index]:
            problems.append(
                f"{source.id}: quotation not found on p. {claim.page}: {claim.quote!r}"
            )
    return CheckResult(problems=problems, notes=notes)


def find_copy(source: Source, directory: Path) -> Path | None:
    """Return the copy of `source` in `directory`, else its stored copy, else None."""
    candidate = directory / source.file
    if candidate.is_file():
        return candidate
    stored = STORED_COPIES / source.file
    if source.stored and stored.is_file():
        return stored
    return None


def main(argv: list[str] | None = None) -> int:
    """Check every source of the register; return 0 only if all copies pass."""
    parser = argparse.ArgumentParser(
        description="Check the verification register against copies of its sources."
    )
    parser.add_argument("directory", type=Path, help="directory holding the copies")
    arguments = parser.parse_args(argv)
    # pypdf warns about fonts it cannot fully decode; the text checked is unaffected.
    logging.getLogger("pypdf").setLevel(logging.ERROR)
    failed = False
    for source in load_register():
        copy = find_copy(source, arguments.directory)
        if copy is None:
            failed = True
            print(f"missing {source.id}: {source.file}, from {source.retrieved_from}")
            continue
        result = check_source(source, copy)
        failed = failed or bool(result.problems)
        for note in result.notes:
            print(f"note    {note}")
        for problem in result.problems:
            print(f"FAILED {problem}")
        if not result.problems:
            print(f"ok      {source.id}: {len(source.claims)} quotations on {copy}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

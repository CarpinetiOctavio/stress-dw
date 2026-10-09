import re
from dataclasses import replace
from pathlib import Path

import pytest

from stress_dw.references import (
    Source,
    check_source,
    find_copy,
    load_register,
    main,
    page_text,
)

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
REGISTER = REPOSITORY_ROOT / "docs/references/verification.toml"
STORED = REPOSITORY_ROOT / "docs/references"
HEADING = re.compile(r"^#{1,6}\s+(?P<text>.+?)\s*$", re.MULTILINE)


def _slug(heading: str) -> str:
    """GitHub's anchor for a Markdown heading."""
    return re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")


def _stored_source() -> Source:
    return next(source for source in load_register(REGISTER) if source.stored)


def test_the_register_is_well_formed() -> None:
    sources = load_register(REGISTER)
    assert sources, "the register lists no source"
    assert len({source.id for source in sources}) == len(sources), "duplicate id"
    for source in sources:
        assert re.fullmatch(r"[0-9a-f]{64}", source.sha256), source.id
        assert source.claims, f"{source.id} has no claim"


def test_a_malformed_entry_is_rejected(tmp_path: Path) -> None:
    register = tmp_path / "verification.toml"
    register.write_text('[[source]]\nid = "x"\nfirst_page = true\n', encoding="utf-8")
    with pytest.raises(ValueError, match="source x"):
        load_register(register)


def test_every_place_a_claim_is_cited_resolves_to_a_heading() -> None:
    for source in load_register(REGISTER):
        for claim in source.claims:
            for place in claim.cited_in:
                path, _, anchor = place.partition("#")
                document = REPOSITORY_ROOT / path
                assert document.is_file(), f"{source.id}: {path} does not exist"
                text = document.read_text(encoding="utf-8")
                anchors = {_slug(match["text"]) for match in HEADING.finditer(text)}
                assert anchor in anchors, f"{source.id}: no heading for {place}"


def test_every_stored_source_has_its_copy_in_the_repository() -> None:
    for source in load_register(REGISTER):
        if source.stored:
            assert (STORED / source.file).is_file(), source.id


def test_the_stored_copy_passes_every_check() -> None:
    source = _stored_source()
    result = check_source(source, STORED / source.file)
    assert (result.problems, result.notes) == ([], [])


def test_a_quotation_on_the_wrong_page_is_reported() -> None:
    source = _stored_source()
    moved = replace(source.claims[1], page=source.claims[1].page + 1)
    altered = replace(source, claims=(moved,))
    assert len(check_source(altered, STORED / source.file).problems) == 1


def test_an_altered_quotation_is_reported() -> None:
    source = _stored_source()
    changed = replace(source.claims[1], quote=source.claims[1].quote + " not in it")
    altered = replace(source, claims=(changed,))
    assert len(check_source(altered, STORED / source.file).problems) == 1


def test_a_page_outside_the_copy_is_reported() -> None:
    source = _stored_source()
    beyond = replace(source.claims[0], page=source.first_page + 1000)
    altered = replace(source, claims=(beyond,))
    assert "is not in" in check_source(altered, STORED / source.file).problems[0]


def test_a_copy_with_another_hash_is_reported(tmp_path: Path) -> None:
    source = _stored_source()
    copy = tmp_path / source.file
    copy.write_bytes((STORED / source.file).read_bytes() + b"\n")
    assert "SHA-256" in check_source(source, copy).problems[0]


def test_a_stamped_copy_is_noted_and_its_quotations_still_checked(
    tmp_path: Path,
) -> None:
    source = replace(_stored_source(), reproducible_hash=False)
    copy = tmp_path / source.file
    copy.write_bytes((STORED / source.file).read_bytes() + b"\n")
    result = check_source(source, copy)
    assert result.problems == []
    assert "stamps each download" in result.notes[0]


def _with_first_pdf_page_as_leading(source: Source) -> Source:
    """The stored copy read as if its first PDF page were a leading page."""
    return replace(source, first_page=source.first_page + 1, leading_pages=1)


def test_leading_pages_shift_printed_pages_to_later_pdf_pages() -> None:
    source = _stored_source()
    later = tuple(c for c in source.claims if c.page > source.first_page)
    shifted = replace(_with_first_pdf_page_as_leading(source), claims=later)
    assert check_source(shifted, STORED / source.file).problems == []


def test_a_quotation_placed_on_a_leading_page_is_reported() -> None:
    source = _stored_source()
    first = tuple(c for c in source.claims if c.page == source.first_page)
    shifted = replace(_with_first_pdf_page_as_leading(source), claims=first[:1])
    assert "is not in" in check_source(shifted, STORED / source.file).problems[0]


def test_a_source_without_a_copy_is_not_found(tmp_path: Path) -> None:
    unstored = next(s for s in load_register(REGISTER) if not s.stored)
    assert find_copy(unstored, tmp_path) is None


def test_the_command_fails_while_any_copy_is_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(REPOSITORY_ROOT)
    assert main([str(tmp_path)]) == 1


def test_character_codes_are_decoded_on_a_page_made_of_them() -> None:
    assert page_text("/80/117/98 /114/101/112/108/121") == "Pub reply"


def test_a_slash_and_digits_in_ordinary_text_are_kept() -> None:
    text = "Received 10/12/2012, accepted for volume 45."
    assert page_text(text) == text


def test_a_claim_with_its_own_pdf_page_is_read_from_that_page() -> None:
    source = _stored_source()
    claim = source.claims[1]
    own_page = claim.page - source.first_page + 1
    pinned = replace(claim, page=claim.page + 40, pdf_page=own_page)
    altered = replace(source, claims=(pinned,))
    assert check_source(altered, STORED / source.file).problems == []


def test_a_wrong_pdf_page_is_reported() -> None:
    source = _stored_source()
    claim = source.claims[1]
    next_page = claim.page - source.first_page + 2
    pinned = replace(claim, pdf_page=next_page)
    altered = replace(source, claims=(pinned,))
    assert len(check_source(altered, STORED / source.file).problems) == 1

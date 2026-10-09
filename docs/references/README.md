# References

Published works on which a claim of this repository rests are checked against a copy of them, under [LOG-048](../decisions/log/LOG-048-verifiable-source-checks.md), which holds the rule and its reasoning. Each work is still cited by its bibliographic data where the claim is made ([ADR-0012](../decisions/0012-cite-only-frozen-and-versioned-sources-as-evidence.md), addendum of 2026-09-30).

## Register

[`verification.toml`](verification.toml) is the register. For each source it gives the citation, the DOI, the URL and date the copy was obtained, the copy's SHA-256, its licence and, where it is not the published version, which version it is; for each claim, the printed page, a verbatim quotation and the documents that make the claim. Its header comment defines each field.

## The check

`stress_dw.references` reads the register and, for each source, checks that a copy has the registered SHA-256 and that each quotation occurs on its printed page. Page text and quotation are compared after Unicode NFKC normalization with all whitespace and all hyphens (ASCII and soft) removed, so that line breaks, words broken across lines and ligatures do not decide the result. Where a PDF's font has no Unicode map, the extracted page consists of character codes; those are decoded first. A claim may give its own PDF page, for a scan whose offset between printed and PDF pages varies. The check runs from the repository root, given a directory that holds the copies under the file names the register gives:

```sh
uv run python -m stress_dw.references <directory>
```

A copy stored in this folder is used when the directory has none. The command prints one line per source: `ok`, `missing` with the URL the copy was obtained from, or `FAILED` with the claim that did not pass. It exits with status 0 only if every source passes.

Some providers stamp each download, for example with its date, and a scan is a unique copy, so that no other copy has the hash of the copy consulted. The register marks such a source (`reproducible_hash = false`); for it, a differing hash is printed as a `note` and the quotations are still checked. For every other source a differing hash fails the check and the quotations are not read, since they would be checked against a different file. The test suite runs the same checks on the stored copy (`tests/test_references.py`).

The check shows that the registered passage is on that page of that file. Whether a claim reads the passage correctly is a reading, open to review against the quotation shown beside it in the register.

## Stored copies

A copy is stored here only when its licence permits redistribution (LOG-048). Each is the publisher's file, unmodified, under its own licence, not under the repository's MIT license.

| File | Register entry | Licence |
|------|----------------|---------|
| [`kim-2017-chi-squared-test-and-fishers-exact-test.pdf`](kim-2017-chi-squared-test-and-fishers-exact-test.pdf) | `kim-2017` | [CC BY-NC 3.0](https://creativecommons.org/licenses/by-nc/3.0/), as printed on its first page |

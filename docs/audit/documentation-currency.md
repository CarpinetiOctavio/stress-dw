# Documentation currency register

Register of the documentation-currency sweep (method: section 2), run at commit `286c53d` before the correspondence phase. It records statements made untrue by a later decision, statements that are false or out of date, and content written in more than one place. The corrections were made in the pull requests of stage 3, listed in section 13; line numbers in this register are locators at the start commit only (sweep rule 6, section 2.3).

## 1. Header

* Start commit: `286c53d` (origin/main, PR #46 merge), on a detached HEAD; tree `45f9506` equals the tree of the reviewed commit `62f79d2`.
* Run on 2026-10-02. Line numbers are locators at `286c53d` only (sweep rule 6, section 2.3).
* Gates before the run: `ruff check` clean; `ruff format --check` clean (16 files); `mypy` clean (16 files); `pytest --ignore=tests/test_acceptance.py` 107 passed; voice test 6 passed. `pytest --collect-only` (collection only, nothing executed): 201 tests, 94 of them in `tests/test_acceptance.py`.
* Not done: the pipeline, any indicator, any database query, any read of the CSV, any edit to a repository file.

## 2. Method

### 2.1 Purpose

The sweep looks for statements that a later decision made untrue, statements that are false or out of date, and content written in more than one place, before the correspondence phase ([ADR-0011](../decisions/0011-preregister-correspondence-criteria-before-exposing-indicator-values.md)) starts from the documentation. It checks internal consistency only. It produces this register; corrections come afterwards, in pull requests.

### 2.2 Stages

1. **Sweep.** The probes of section 2.6 are run read-only and this register is written.
2. **Decisions.** Every DECIDE item of section 8 is answered or assigned to the correspondence phase; each answer is recorded in the [decision log](../decisions/log/README.md).
3. **Corrections.** Pull requests by group (`PR-` prefixes, section 5), each with a plan approved before it is written. PR-e versions this register at `docs/audit/documentation-currency.md`, rewrites its links from draft to final paths (sections 7, 11 and 12) and adds the links from log entries to findings; it is merged before stage 4.
4. **Re-check.** Probes 1–3 are re-run after the corrections, and a closure statement is added.
5. **Redundancy.** Probe 8 pull requests by home concept, after the corrections, each replacement with a table of the claims it preserves.
6. **Final re-run** of probes 1–3.

The sweep started from a list of known incongruences compiled before stage 1. Every item of that list that this register uses is recorded here (findings, or section 5.8); nothing in the register depends on the list itself.

### 2.3 Sweep rules

1. The repository stays read-only until this register is approved; during the sweep pytest runs only with `--ignore=tests/test_acceptance.py`, so no acceptance test is run; the pipeline is not run; working scripts live outside the repository tree.
2. Figures derived from the source file follow the reading rule of section 2.5.
3. Consistency is checked between documents and against code and tests, never against the source file.
4. Accepted decision records are not rewritten; a finding that grounded a decision gets a dated addendum, and only operational descriptions are corrected in place.
5. DECIDE items are never resolved in this register.
6. Findings cite file and section or anchor; line numbers are locators valid at the start commit only.
7. Each finding is tagged `[verified in text]` or `[interpretation]`.
8. The scope is not widened, no model change is proposed, and the legacy repository is not touched.

### 2.4 Rules with a versioned home

These apply to the sweep and are not restated here:

* Exposure of indicator values and declared prior knowledge: [ADR-0011](../decisions/0011-preregister-correspondence-criteria-before-exposing-indicator-values.md), rules 1, 2 and 4.
* Evidence: [ADR-0012](../decisions/0012-cite-only-frozen-and-versioned-sources-as-evidence.md), rules 1–4, and its constraint on values readable in a capture.
* Voice, glosses, one home per concept, names: [writing conventions](../writing-conventions.md).
* The legacy repository: [ADR-0000](../decisions/0000-rebuild-from-scratch-instead-of-continuing-legacy.md), Decision Outcome, and `CLAUDE.md`, whose wordings differ (finding DC-44, item N4).

The convention that accepted decision records are not rewritten and receive dated addenda (sweep rule 4) was stated in no versioned document at the start commit (finding DC-90, item N17); its home is now [`docs/decisions/README.md`, Addenda to accepted decision records](../decisions/README.md#addenda-to-accepted-decision-records).

### 2.5 Reading rule (for this sweep)

The repository is read normally. Figures derived from the source file that already sit in the repository are read only where a check needs them, and are listed in section 4 by file and category, never restated. No new value is produced before the criteria commit of ADR-0011: no indicator value or output, no dump, no exploration of the source file or the database, and no result of A5, A6, A10 or A7.

No versioned document states this rule as a whole. ADR-0011 covers the exposure of indicator values (rule 1) and the declaration of prior knowledge (rule 2), and orders A5, A6 and A10 after the criteria commit (rule 4); ADR-0012 covers values readable in a capture. Neither states that the repository is read normally, the listing by file and category, or the ban on exploring the source file and the database. The rule is stated here for this sweep only; its general home is pending for the correspondence phase (finding DC-91).

### 2.6 Probes

* **Probe 1, temporal drift.** Terms such as "not yet", "pending", "will", "currently", "once", "until", "proposed"; each hit classed still true, now false, HIST or NORM (section 6).
* **Probe 2, counts.** Decision records and addenda, dimensions, columns, questions, indicators, checks, invariants, files named in lists.
* **Probe 3, cross-references.** Links and anchors (GitHub anchor rules), decision-record numbers, finding codes, section numbers, the decision-record index against files and frontmatter; `file:line` citations in living documents.
* **Probe 4, decision lineage.** Each decision record's outcome and consequences against later records, the specification and the code; order and consistency of addendum dates (section 5.3).
* **Probe 5, specification against code and tests,** structure only.
* **Probe 6, conventions.** Voice, glosses, one home per concept, vocabulary; what the voice test cannot catch.
* **Probe 7, evidence discipline.** Claims about external pages or legacy artifacts without a capture or the frozen source; capture values restated elsewhere.
* **Probe 8, redundancy.** A concept-to-home map, confirmed before any replacement (section 7); a duplicate scan over paragraphs, list items and table rows (5-word shingles: Jaccard ≥ 0.50 probable, 0.30–0.50 candidate, containment ≥ 0.60; then exact 8-grams); classes KEEP, REF, CONDENSE, MERGE, REPORT-ONLY.

The probes are named "probe 1" to "probe 8"; ADR-0013's findings M1–M8 keep their names and are cited as "ADR-0013 probe 1" and so on.

### 2.7 Classes

FIX, ADD, HIST, NORM, EXT, CODE, REF, CONDENSE, KEEP, MERGE, REPORT-ONLY, DECIDE, and NONE (sub-reason: clean, still true, open obligation, or correspondence phase) for a finding that requires no action. Bookkeeping conventions: [LOG-005](../decisions/log/LOG-005-register-bookkeeping-conventions.md).

### 2.8 Roles of documents

* Living documents: `README.md` (truth check only; no probe 8 change), `CLAUDE.md` (KEEP; any change is a decision), `docs/*.md`, `docs/specification/*`, `docs/audit/*.md`, and `docs/decisions/README.md` (an index, KEEP in probe 8).
* `docs/decisions/adr-template.md`: normative; in probe 3 and probe 6, out of probe 8.
* Accepted decision records: historical; sources in probe 8, REPORT-ONLY on their side.
* `docs/audit/evidence/**`: evidence, read only as link targets.
* Configuration files `.gitignore`, `.sonarcloud.properties`, `pyproject.toml`: comments only.

### 2.9 Procedure

* **Start.** A detached HEAD at the start commit (section 1).
* **Reading.** Every in-scope Markdown file read in full; the 7 `src` modules and the 16 indicator queries read in full; the 20 other SQL files read for their header comments; `tests/test_acceptance.py` and the `EXPECTED_COLUMNS` block of `tests/test_schema.py` read in full; the other seven test modules read through their comments, docstrings, test names and assertion messages; the three configuration files read for their comments.
* **Scripts** (working files outside the repository, not versioned; the register records their method and results): `m1.py` (temporal terms with context, 175 hits), `m3.py` (link targets, GitHub anchors, bare paths, decision-record numbers, `file:line` locators), shell checks for the decision-record index, the "Fase N" gloss per document, Spanish legacy terms, finding codes and section references, `m8.py` (shingles and 8-grams).
* **Frozen legacy source.** Read with `git show legacy-original:"Informe DW/DW - Estrés y Salud Mental.pdf"` outside the repository tree and `pdftotext` (default mode), without changing the clone: first the question list (text lines 155–200) and the occurrences of "entrevista" (English: "interview") and "diagn" (stem of "diagnóstico", English: "diagnosis"); later a per-page search for further terms and eight rasterized pages (41, 42, 78–79, 98–100, 113), with the page list recorded before reading (section 5.6.1).
* **Tags.** `[verified in text]`: checked by a command or a read, cited; `[interpretation]`: otherwise.

## 3. Scope

90 files at `286c53d`:

| Kind | Files | Note |
|------|-------|------|
| Markdown | 35 | 2,564 lines; `CLAUDE.md`, `README.md`, `docs/*.md`, `docs/specification/*`, `docs/audit/*.md`, 14 ADRs, `docs/decisions/README.md`, `docs/decisions/adr-template.md` |
| Python | 16 | `src` 7, `tests` 9 |
| SQL, in full | 16 | `src/stress_dw/sql/indicators/` |
| SQL, header comments | 20 | dimensions, fact, schema, staging |
| Configuration, comments only | 3 | `.gitignore`, `.sonarcloud.properties`, `pyproject.toml` |

Roles of the documents: section 2.8. `docs/audit/evidence/**` holds 22 files.

## 4. Encountered figures

Figures derived from the source file, or from captures of it, that sit in the repository and were read during the sweep. Listed by file and category; not restated (reading rule, section 2.5).

| File | Category |
|------|----------|
| `CLAUDE.md:33`; `docs/specification.md:26`; `docs/specification/staging.md:28`; `docs/specification/acceptance.md:17` | raw and staged row counts |
| `docs/specification/sources.md:36,47`; `docs/specification/dimensions.md:11,15`; `docs/specification/country-region-mapping.md:24` | distinct country and month counts (A8); `Timestamp` range from the Data Card; A12 parse result |
| `docs/audit/legacy-audit.md:9–21,25–26` | A1 hash; A4 duplicate and profile counts; A8 coverage and missing months; A12 result; A13 distribution figures by country and group size; legacy ETL log counts |
| `docs/conceptual-framework.md:63` | A13 figures by country |
| `docs/audit/phase4-closure.md:15–43,61` | pipeline row counts; dimension row counts; missing months; test names carrying counts |
| `docs/dataset-provenance.md:64` | legacy ETL log counts; Data Card counts |
| ADR-0000 `:11,20,23,35,37` | legacy log counts; legacy report figures; export row count and width |
| ADR-0001 `:23,26,27` (P5, P8, P9) | Data Card range, marginal distributions, counts |
| ADR-0007 `:11,66`; ADR-0010 `:47` | legacy fact rows; staged count |
| ADR-0008 `:11,19–21,26,33–35,42,55` | A4, A13 and G1 figures; counts |
| ADR-0012 `:26`; ADR-0013 `:22` | export row count |
| `tests/test_acceptance.py` | expected counts in assertions and test names |
| Captures `openml-osmi-2014-description-2026-10-01.png`, `openml-osmi-2014-properties-2-2026-10-01.png` (viewed in the preliminary check before stage 1) | qualities of a third-party deposit (instances, features) |

No indicator value, no output, no CSV content and no database content was read.

## 5. Findings

Classes as in section 2.7. Each finding has one primary class; a secondary class, where one applies, follows in parentheses. NONE (sub-reason: clean / still true / open obligation / correspondence phase) marks a finding that requires no action; it is counted in the totals. "PR" is the correction group of stage 3 (PR-a1, PR-a2, PR-b, PR-c, PR-d, PR-e, and the isolated PR-N1 and PR-N2) or stage 5 (probe 8). "Dec." holds decision letters (a–l) only, or the permanent IDs N1, N2, … of the DECIDE items found in stage 1. "corr." marks an item assigned to the correspondence phase. A clean result of a whole probe (for example probe 3) carries a DC ID with class NONE (clean), because the sweep's closure depends on that probe re-running clean. A point verification of a single item carries no ID and goes to the 'Verified, no finding' list (section 5.10). Reconciliation by class: section 10.

### 5.1 Status of Fase 4 and of the A-series checks

| ID | Location | Statement | Why | Class | Disposition | PR | Dec. | Tag |
|----|----------|-----------|-----|-------|-------------|----|------|-----|
| DC-01 | `docs/specification.md:22` | "Fase 4, is not yet specified for this rebuild, so the items below stay open." | `:26` of the same file, `staging.md:3` and `phase4-closure.md:5` state Fase 4 specified and closed | FIX | correct the sentence | PR-a1 | — | verified in text |
| DC-02 | `docs/specification.md:24–26` | Heading "Open items and dependencies" lists "Fase 4" as an open item | its content says it is specified in `staging.md`; it is not open | FIX | move or relabel with DC-01 | PR-a1 | — | verified in text |
| DC-03 | `docs/specification/sources.md:53` | load rule "belongs to … Fase 4 … which is not yet specified …; it moves there when that phase is specified" | Fase 4 is specified; the rule did not move: `staging.md:44` names `sources.md#load-rule` as its home | FIX | drop the temporal clause; state the home | PR-a1 | — | verified in text |
| DC-04 | ADR-0008 `:11` | `specification.md` "leaves open" Fase 4 | was true on 2026-09-25; accepted ADR | REPORT-ONLY (HIST) | REPORT-ONLY | — | — | verified in text |
| DC-05 | `docs/conceptual-framework.md:106` | "checks … that have not run yet (A1–A10, all `Pending`); it will be finalized once they close" | A1, A4, A8, A12, A13 are Established (`legacy-audit.md:9,12,16,20,21`) | FIX | restate against the audit table, by link | PR-a1 | — | verified in text |
| DC-06 | `docs/conceptual-framework.md:111` | "H1 and H3, pending (A1, A4, A5, A6, A10)" | A1 and A4 are Established; A13 is also tagged H1 (`legacy-audit.md:21`) | FIX | restate the list | PR-a1 | — | verified in text |
| DC-07 | `docs/conceptual-framework.md:111` | "plausibly RHMCD-20 (ADR-0001 addendum, H3)" | H3 is in ADR-0001's Hypotheses section ("added 2026-09-22", `:33`); ADR-0001's only addendum (2026-10-01) is about OSMI pages | FIX | correct the pointer | PR-a1 | — | verified in text |
| DC-08 | `docs/conceptual-framework.md:113` | "Fan-out in `Dim_Sintomas` (F1, A2, pending). If uncarried into the new pipeline's design, …" | the design exists (ADR-0007) and C1, C2 pass (`phase4-closure.md:51–52`); A2 stays pending as a legacy audit only (`phase4-closure.md:79`) | FIX | restate; `Dim_Sintomas` glossed (DC-46) | PR-a2 | — | interpretation |
| DC-09 | `docs/specification/country-region-mapping.md:18`, `docs/specification.md:27`, `docs/audit/phase4-closure.md:86` | 33 entries pending A11 | consistent with `legacy-audit.md:19` | NONE (still true) | still true; no action | — | — | verified in text |
| DC-10 | `docs/audit/legacy-audit.md:21` (A13) | result labels its sub-steps "C1", "C2", "C3", "C4" | the same codes are the acceptance checks C1–C11 (`acceptance.md`); the method column numbers them (1)–(4) | FIX | relabel to the method's numbering | PR-a1 | — | verified in text |
| DC-11 | `docs/audit/legacy-audit.md:21` (A13) | "Staging grain for Phase 4 is decided independently of this check (see `conceptual-framework.md` §5 addendum)" | the framework's §5 addendum (`:61–63`) reports A13 and says nothing of the staging grain; ADR-0008 decides it | FIX | point to ADR-0008 | PR-a1 | — | verified in text |
| DC-12 | `docs/audit/legacy-audit.md:14` (A6) | A6 compares `Timestamp` only | H1's test names five variables (ADR-0001 `:31`) | DECIDE | Decided (i): A6 aligned with the five variables of H1's test (LOG-019) | — | i | verified in text |
| DC-13 | `docs/audit/legacy-audit.md:15` (A7), `docs/audit/phase4-closure.md:83` | A7 wording | A7 and its rewording are assigned to the correspondence phase | NONE (correspondence phase) | carried forward | corr. | — | verified in text |
| DC-14 | `docs/audit/phase4-closure.md:81–82` | A5 and A6 "the two checks of hypothesis H1" | A13 is also tagged H1 (`legacy-audit.md:21`); ADR-0001 `:86` speaks of "the tests for H1" | FIX | restate without the count, or by link | PR-a1 | — | verified in text |
| DC-15 | `docs/audit/phase4-closure.md:54` (C4 row) | "Every table has exactly the specified columns and types" | C4 in `acceptance.md:10` is "`fact_response` has exactly the columns … and no column in any table stores a ratio, a percentage, a count, or a derived condition" | FIX | align the "Verifies" cell with `acceptance.md` | PR-a1 | — | verified in text |
| DC-16 | `docs/audit/phase4-closure.md:16,19` | "195 passed with the source file present"; "101 passed and 94 skipped" | at `286c53d` collection gives 201 tests (107 outside the acceptance module, 94 in it); `:21` dates the statement to `9f31ab0` | HIST | KEEP (dated); optional ADD of the date beside the counts; resolved by N1 (the count becomes a dated statement) | PR-N1 | — | verified in text |
| DC-17 | `README.md:14` | "Specification and audit in progress. There is no runnable pipeline yet." | the pipeline exists and runs (`src/stress_dw/pipeline.py`; `phase4-closure.md:5,15`) | DECIDE (FIX) | README.md:14 corrected ahead of its planned rewrite, by reference to phase4-closure.md §1; the Status section is otherwise left to that rewrite. | PR-N2 (isolated, after PR-N1) | N2 | verified in text |
| DC-18 | ADR-0001 `:27` (P9) | "Byte-level identity pending SHA-256 comparison" | resolved: A1 Established, hashes in `dataset-provenance.md` | ADD | dated addendum noting A1 | PR-b | — | verified in text |
| DC-19 | ADR-0000 `:68` (Confirmation) | "`legacy-audit.md` holds the queries and counts quantifying F1–F4" | A2 (F1), A3 (F4) and A7 (F2) are Pending | NONE (open obligation) | open obligation; REPORT-ONLY | — | — | verified in text |
| DC-20 | ADR-0008 `:55` (Confirmation) | acceptance criteria "once specified in `staging.md`" add the staged-row-count check | the check exists as C11 in `acceptance.md`; `staging.md:72` links it | REPORT-ONLY (HIST) | REPORT-ONLY | — | — | verified in text |
| DC-21 | ADR-0007 `:66` | query-time cost "is an assumption to check once the pipeline exists" | the pipeline exists; no measurement is recorded anywhere in the repository (search for "negligible", "query-time cost", "seconds", "benchmark", "timing") | NONE (open obligation) | open obligation; REPORT-ONLY | — | — | verified in text |
| DC-92 | `docs/dataset-provenance.md:81` | "The legacy repository (`stress-dw-legacy`, archived, unmodified)" | since commit `3cf77ce` (2026-09-20, superseded notice, README only) the repository's `main` differs from the tag; "unmodified" holds at the tag `legacy-original` only (DC-44, LOG-006) | FIX | "unmodified at the tag `legacy-original`" | PR-a1 | — | verified in text |

### 5.2 Cross-references, IDs and indexes (probe 3)

| ID | Location | Statement | Why | Class | Disposition | PR | Dec. | Tag |
|----|----------|-----------|-----|-------|-------------|----|------|-----|
| DC-22 | all 35 Markdown files | links, anchors, ADR numbers, section references | every relative link and anchor resolves (GitHub slug rules); no ADR number above 0013; no finding code outside its defined range; every `§N` and "section N" exists | NONE (clean) | clean | — | — | verified in text |
| DC-23 | `docs/decisions/README.md` | index rows | the 14 rows match the files, their H1 titles and their frontmatter status | NONE (clean) | clean | — | — | verified in text |
| DC-24 | `docs/decisions/README.md:28–36` | "Finding and hypothesis IDs": `F`, `P`, `H`, and checks `A` | the repository also uses `E` (ADR-0009), `G` (ADR-0008), `K` (ADR-0011), `S` (ADR-0012), `M` (ADR-0013), and the specification's `C` and `I`; `writing-conventions.md:45` makes this section the home of IDs | ADD | list every letter in use, by link to its record | PR-a1 | — | verified in text |
| DC-25 | ADR-0008 `:11,:28` | "no respondent identifier ([`specification.md`], Open items)" | `specification.md`'s Open items (`:24–28`) do not state it; no living document states it | ADD (REPORT-ONLY) | REPORT-ONLY on the ADR; state the fact in a living home (`fact-table.md#grain` or `sources.md`) | PR-a1 | — | verified in text |
| DC-26 | ADR-0008 `:29,:50` | "A1 already established that the legacy's own … exact-duplicate count on all 17 columns matches this project's extraction"; "A1 shows the legacy project already made the same call" | A1 is the hash comparison (`legacy-audit.md:9`); the 17-column count match is recorded in A4's result (`legacy-audit.md:12`) | ADD | dated addendum pointing to A4 | PR-b | — | verified in text |
| DC-27 | ADR-0002 `:11,:68` | "private until ADR-0001's confirmation made it public" (`:11`); "ADR-0001, which made the repository public" (`:68`) | ADR-0001's Confirmation (`:82–86`) has no item about visibility | REPORT-ONLY | REPORT-ONLY | — | — | verified in text |
| DC-28 | ADR-0009 `:62` | "no post-load updates ([ADR-0007])" | ADR-0007 does not state that; its constraints are on dimension attributes and measures (`:68–69`) | REPORT-ONLY | REPORT-ONLY | — | — | verified in text |
| DC-29 | ADR-0009 `:19` (E1) | evidence "fetched 2026-09-26" | the record is dated 2026-09-25 (frontmatter) | REPORT-ONLY | REPORT-ONLY (the 2026-10-02 addendum supersedes E1's evidence) | — | — | verified in text |
| DC-30 | `docs/methodology.md:7` | "the dimension grain decisions formalized in `docs/specification.md`" | since the split, the rule is in `specification/definitions.md#dimension-grain-rule` and the grains in `specification/dimensions.md` | FIX | point to the parts | PR-a1 | — | verified in text |
| DC-31 | `docs/specification.md:9–18` | Parts table | it lists eight parts and omits `staging.md`, which `:26` cites | ADD | add the row | PR-a1 | — | verified in text |
| DC-32 | `docs/specification.md:28` | "set in a separate document" | no link to `code-conventions.md` | ADD | add the link | PR-a1 | — | verified in text |
| DC-33 | `docs/specification/staging.md:34` | "the hash every check in legacy-audit.md, and this ADR sequence's own findings (A1, G1, E1), were computed against" | `staging.md` is not an ADR; A1 is a check, not an ADR finding; E1 rests on documentation pages, not on a computation (ADR-0009 addendum) | FIX | restate; also link `legacy-audit.md` | PR-a1 | — | verified in text |
| DC-34 | `docs/specification/staging.md:34` | "whether part of the file is CC BY-SA rather than the CC BY its uploader declares" | narrower than `dataset-provenance.md:79`, which records three license statements and no single license | FIX (REF) | REF to `dataset-provenance.md`; REF part confirmed: pointer to `dataset-provenance.md#how-to-obtain-the-file`, written with DC-33 (LOG-007) | PR-a1 | — | verified in text |
| DC-35 | `docs/dataset-provenance.md:77` | "Place it in `data/raw/`" | the pipeline expects `data/raw/mental_health.csv` (`staging.md:34`, `pipeline.py:16`), while the download is named `Mental Health Dataset.csv` (`:8`) | ADD | state the expected name, or REF to `staging.md#extraction` | PR-a1 | — | verified in text |
| DC-36 | `docs/specification/indicators.md:94` | indicator 16: "Uses `symptom_cluster`; see its validity caveat." | its population is that of 15, which also uses `explicit_recognition` (`:84` names both) | ADD | name both | PR-a1 | — | verified in text |

### 5.3 Decision lineage (probe 4)

| ID | Location | Statement | Why | Class | Disposition | PR | Dec. | Tag |
|----|----------|-----------|-----|-------|-------------|----|------|-----|
| DC-37 | ADR-0005 `:21` (F7) | quotes "cómo varía dicha proporción... según el género" as Q4's text | in the frozen report the phrase is in Q2 (report text lines 169–170); Q4 reads "segmentado por género y presencia de estrés creciente" | ADD | dated addendum | PR-b | — | verified in text |
| DC-38 | ADR-0004 `:26,:118` | Q3 "already matches what its indicators (5, 6) compute"; "every question's text now matches exactly" | Q3 asks "region or continent" (`indicators.md:27`); nothing implements continent | DECIDE | Decided (d): Q3 text and objective of the starting option, by an ADR-0004 addendum (LOG-015) | PR-b | d | verified in text |
| DC-39 | ADR-0004 `:58,:85,:103,:114` | objectives of Q2, Q6, Q7.1, Q7.2 | Q2 "co-occurrence" within a population conditioned on family history; Q6 omits the recognition cut its question names; Q7.1 "measure the gap" against `patterns.md:45`; Q7.2 "persists", "non-uptake", "fullest context" | DECIDE | Decided (e): objectives of Q2 and Q7.1 adopted; Q6 and Q7.2 written in the plan of PR-b under conditions (LOG-016) | PR-a2 / PR-b | e | verified in text |
| DC-40 | ADR-0006 `:51–52` vs `indicators.md:31–32` | rows 5–6: population = the condition; cut = occupation × country × region | `indicators.md`: population all rows; grouping sets {occupation, country} and {occupation, region} | DECIDE | Decided (j): a dated addendum to ADR-0006 states that `indicators.md` is the current definition and records how rows 5–6 differ; the table is not changed (LOG-008) | PR-b | j | verified in text |
| DC-41 | ADR-0005 `:52` | indicator 9 renamed "explicit stress-recognition rate by isolation level" | ADR-0006, `indicators.md`, `indicators.py` and `indicator_09.sql` all read "… by isolation" (names checked equal across those four for all 16 indicators) | REPORT-ONLY | REPORT-ONLY (ADR-0006 is the record of the final state) | — | — | verified in text |
| DC-42 | ADR-0003 `:64,:76` | the minimum-count rule "is set in `docs/specification.md`" | `patterns.md:41` sets a `low_n` flag; "No row is suppressed in SQL"; no minimum count is set before a rate is reported | DECIDE | Decided (N3): dated addendum to ADR-0003 recording that the specification implements the minimum-count consideration as a flag (`low_n`, a query-layer parameter; no row suppressed; display left to the reporting layer), not as a rule; the rule for reading flagged cells is set in the correspondence criteria. The addendum corrects "is set in docs/specification.md" and decides no rule | PR-b | N3 | interpretation |
| DC-43 | ADR-0003 `:77` | the filter `care_options IN ('Yes','Not sure')` is "the literal scope of Q7.2 ('...and who report having care options available')" | Q7.2's text (`indicators.md:88`) says "having care options available" while the population keeps "Not sure" | DECIDE | Decided (b): neutral wording; the meaning of the OSMI text stated as a candidate premise; Q7.2's text goes to e (LOG-013) | PR-b | b | interpretation |
| DC-44 | ADR-0000 `:57` | "the only addition permitted [to the legacy] is a superseded notice" | `CLAUDE.md:17`: the legacy is never modified, with no exception | DECIDE | Decided (N4): the one permitted addition was made (`3cf77ce`, 2026-09-20, README only) and no versioned document records it, so a dated addendum to ADR-0000 records it, states the exception exhausted, and states that the notice reflects 2026-09-20 and that `stress-dw` is the current record; `CLAUDE.md:17` is aligned and points to the addendum, in the same pull request | PR-b | N4 | verified in text |
| DC-45 | ADR-0010 `:19`; ADR-0013 `:56,:100`; ADR-0009 parts listed in its addendum (`:53`) | E1 "insert-only"; foreign-key enforcement "which ADR-0009 evidences (E1)" | ADR-0009's addendum restates E1; enforcement on insert is from the captures, on delete from E3; C5 tests it | ADD (DECIDE) | Decided (N5): addenda to ADR-0010 and ADR-0013; ADR-0009's dependent parts not weighed again (LOG-022) | PR-b | N5 | verified in text |
| DC-90 | `docs/decisions/README.md`; `docs/decisions/adr-template.md`; `docs/writing-conventions.md` | convention that accepted decision records are not rewritten and receive dated addenda | applied throughout the decision records (addenda in ADR-0000, ADR-0001, ADR-0003, ADR-0007, ADR-0009, ADR-0012), stated in no versioned document (search for "not rewritten" and "addend" in the three files and `CLAUDE.md`: no hit) | DECIDE | Decided (N17): stated in `docs/decisions/README.md`, in a section beside "Deviations from base MADR", with DC-24 (LOG-009) | PR-a1 | N17 | verified in text |

Lineage table (statement → later change → addendum present):

| ADR | Statement | Superseded or qualified by | Addendum present |
|-----|-----------|----------------------------|------------------|
| 0000 | F2 "without numerators or denominators" | own addendum 2026-09-29 | yes |
| 0000 | F3, `mental_health_interview` reading | own addendum 2026-09-23 | yes |
| 0000 | "only addition permitted is a superseded notice" | `CLAUDE.md:17` (no exception) | no (DC-44) |
| 0001 | P7 | own addendum 2026-10-01 | yes |
| 0001 | P9 "pending SHA-256" | A1 Established | no (DC-18) |
| 0002 | "No CI pipeline exists yet" | still true (no workflow files tracked) | n/a |
| 0003 | tagged inclusion-path design | own addendum 2026-09-23 | yes |
| 0003 | minimum-count rule "set in the specification" | `patterns.md:41` (flag only) | no (DC-42) |
| 0004 | Q7.1 wording | amended in place 2026-09-23 | yes |
| 0004 | Q3 "matches exactly" | `indicators.md:27` (continent) | no (DC-38) |
| 0005 | F7 Q4 quotation | frozen report (Q2) | no (DC-37) |
| 0005 | indicator 9 name | ADR-0006 | no (DC-41) |
| 0006 | rows 5–6 | `indicators.md` grouping sets | no (DC-40) |
| 0007 | "person grain" | ADR-0008 (staged record, no respondent identifier) | no (f) |
| 0007 | consumption layer "not yet specified" | ADR-0013 (direction decided, not specified) | n/a (ADR-0013 records it) |
| 0007 | F2 citation | own addendum 2026-09-29 | yes |
| 0008 | "A1 established …" | A4 | no (DC-26) |
| 0009 | E1, E2, "write-once" | own addendum 2026-10-02 | yes |
| 0010 | E1 "insert-only" | ADR-0009 addendum | no (DC-45) |
| 0013 | foreign-key evidence "(E1)" | ADR-0009 addendum | no (DC-45) |

Order of dates: every addendum is dated on or after its record's date; ADR-0001's H3 (2026-09-22) precedes its addendum (2026-10-01); the framework's addenda are 2026-09-23, 2026-09-25, 2026-09-25. Only anomaly: DC-29.

### 5.4 Specification against code and tests (probe 5)

| ID | Location | Statement | Why | Class | Disposition | PR | Dec. | Tag |
|----|----------|-----------|-----|-------|-------------|----|------|-----|
| DC-47 | `docs/specification/patterns.md:7` | output columns: cut values, `level`, `numerator`, `denominator`, `rate`, `low_n` | the code adds `grouping_set` (indicators 5, 6) and `headline_rate` (10) (`indicators.py:9–11`; `indicator_05.sql`, `indicator_06.sql`, `indicator_10.sql`) | ADD | add both to the output-column contract | PR-c | — | verified in text |
| DC-48 | `indicators.md:52,94`; ADR-0003 `:54,:76` | "headline" names a column for 10 and a designated cell for 16 | two meanings, no home; 16's output does not mark its headline cell | ADD | one home in `patterns.md` | PR-c | — | verified in text |
| DC-49 | `src/stress_dw/schema.py:16` | "the load rule the Python load step will enforce" | it is enforced by `staging.enforce_load_rule` (`staging.py:139`) | CODE | present tense | PR-c | — | verified in text |
| DC-50 | ADR-0007 `:65` | "the cluster's threshold is written in one definition" | the three literals of `symptom_cluster` are repeated in `indicator_14.sql:13–16`, `indicator_15.sql:9–12,21–24` and `indicator_16.sql:9–12,22–25`; the acceptance tests repeat them as an independent oracle (`test_acceptance.py:330–333,337–339,387–389`). Separately, `indicator_10.sql:15` repeats the `mood_swings` literal as indicator 10's headline threshold (`definitions.md:22`), not as part of `symptom_cluster`. Every location: section 5.4.1 | DECIDE | Decided (h): ADR-0007 addendum; no refactor (LOG-018) | PR-b | h | verified in text |
| DC-51 | `docs/specification/dimensions.md`, `staging.md:7–22` | types `VARCHAR(n)`, `CHAR(7)` | DuckDB stores them as `VARCHAR` (`tests/test_schema.py:8–10`); the lengths are not enforced and the specification does not say so | ADD | state it once (dimensions or model conventions) | PR-c | — | verified in text |
| DC-52 | `tests/test_acceptance.py:175` | `FACT_JOINED_TO_DIMENSIONS` | the fragment joins `staging_response` to the dimensions, not `fact_response` | CODE | rename | PR-c | — | verified in text |
| DC-53 | `src/stress_dw/__init__.py:1` | "(Fase 4)" | not glossed; whether the gloss rule applies to docstrings is undecided | CODE (DECIDE) | Decided (N7): glossed (LOG-024) | PR-c | N7 | verified in text |
| DC-54 | `docs/specification/patterns.md:43` | outputs using `symptom_cluster` "are accompanied by the caveat written in its definition" | `indicators.py:24–27` attaches a pointer to the definition, not the caveat's text | DECIDE | Decided (N15): reworded to a link (LOG-031) | PR-c | N15 | interpretation |

#### 5.4.1 Locations of the cluster literals (revision 1)

Search over the 36 SQL files, the 16 Python files and the 35 Markdown files at `286c53d`. Regular expressions: `'Medium', ?'High'`; `'15-30 days', ?'31-60 days', ?'More than 2 months'` (and `'15-30 days'` alone, no other hit); `[Cc]oping_[Ss]truggles ?= ?'Yes'`.

| Literal | Code: role `symptom_cluster` | Code: other role | Tests (oracle) | Documents |
|---------|------------------------------|------------------|----------------|-----------|
| `mood_swings IN ('Medium', 'High')` | `indicator_14.sql:13`; `indicator_15.sql:9,21`; `indicator_16.sql:9,22` | `indicator_10.sql:15`, `FILTER (WHERE level IN ('Medium', 'High'))` on the alias `level` = `dim_symptoms.mood_swings`: indicator 10's headline threshold | `test_acceptance.py:330,337,387` | `definitions.md:22` (indicator 10), `:51` (cluster); `legacy-audit.md:17` (legacy formula, A9); ADR-0003 `:50`; ADR-0005 `:29,:54` (indicator 10); ADR-0006 `:64` |
| `days_indoors IN ('15-30 days', '31-60 days', 'More than 2 months')` | `indicator_14.sql:16`; `indicator_15.sql:12,24`; `indicator_16.sql:12,25` | — | `test_acceptance.py:333,339,389` | `definitions.md:53`; `legacy-audit.md:17`; ADR-0003 `:50`; ADR-0006 `:64` |
| `coping_struggles = 'Yes'` | `indicator_14.sql:14`; `indicator_15.sql:10,22`; `indicator_16.sql:10,23` | `indicator_05.sql:13,15`, `indicator_06.sql:13,15`: condition C of indicators 5–6 | `test_acceptance.py:331,338,388` (cluster); `:403` (`CO_OCCURRENCE_IN_STAGING`, condition C) | `definitions.md:21,52`; `indicators.md:31` |

No `src/stress_dw/*.py` module and no test module other than `test_acceptance.py` contains any of the three. The dimension and fact SQL files name the columns only.

### 5.5 Conventions (probe 6)

| ID | Location | Statement | Why | Class | Disposition | PR | Dec. | Tag |
|----|----------|-----------|-----|-------|-------------|----|------|-----|
| DC-55 | `docs/conceptual-framework.md:40` | "Rows marked "no source description" or "reinterpreted here" carry an assumption, not an established fact; the specification in Chat 1 should treat them accordingly." | attribution to a working session; future-directed; the specification exists | FIX | restate impersonally, by link to the specification | PR-a2 | — | verified in text |
| DC-56 | `docs/conceptual-framework.md:70` | "This section settles what construct each indicator's variables can honestly support, given the corrections in §4. It does not fix SQL-level formulas, numerators, or denominators — that belongs to the specification in Chat 1, per ADR-0000's confirmation that "each indicator definition names a construct its variables can support."" | as DC-55 | FIX | as DC-55 | PR-a2 | — | verified in text |
| DC-57 | `docs/conceptual-framework.md:72,80,88` | headings "(currently "% with …")" | the names are the legacy's; ADR-0003 and ADR-0006 replaced them; the `:100` addendum keeps the section for traceability | FIX | "legacy name" for "currently" | PR-a2 | — | verified in text |
| DC-58 | `docs/conceptual-framework.md:38` | `mental_health_interview` "Reinterpreted here as disclosure willingness / anticipated stigma … not yet confirmed — flagged for review before §6's Indicator 16 direction is finalized" | ADR-0000's addendum (`:30`) states that the pipeline operates on the corrected reading; ADR-0003 and ADR-0004 adopt it; "anticipated stigma" against `:51` ("no stigma items of any kind") | FIX (DECIDE) | Decided (N6): temporal part FIX; "anticipated stigma" dropped (LOG-023) | PR-a2 | N6 | verified in text |
| DC-59 | `docs/conceptual-framework.md:35,112` | `Indicador_Inferido_Estrés` | the legacy flag; the specification has no such object (`symptom_cluster`, `explicit_recognition`); Spanish identifier unglossed; `:112` restates the validity caveat whose home is `definitions.md#symptom_cluster` | FIX (REF) | refer to the legacy flag as such and to `symptom_cluster`; caveat by link; REF part confirmed: `:112` points to the caveat at `definitions.md#symptom_cluster`, `:35` names `symptom_cluster` as the legacy flag's successor (LOG-007) | PR-a2 / stage 5 | — | verified in text |
| DC-60 | `docs/conceptual-framework.md:92` | "a treatment-seeking gap despite resource availability" | `patterns.md:45`: no output is stated as a treatment gap | FIX | with e (LOG-016) | PR-a2 | e | verified in text |
| DC-61 | `docs/conceptual-framework.md:30` | "Later revisions of Andersen's model add a contextual layer beyond the individual-level triad" | no reference in §8 supports it | ADD | cite, or mark as this document's interpretation | PR-a2 | — | verified in text |
| DC-62 | `docs/audit/legacy-audit.md:17` | "the Fase 2 formula" | no gloss anywhere in the file (one use) | FIX | gloss | PR-a1 | — | verified in text |
| DC-46 | `legacy-audit.md:10,16,17,25,34,35`; `conceptual-framework.md:35,112,113`; ADR-0000 `:11,21,23`; ADR-0003; ADR-0006 `:64`; ADR-0012 `:25,26,28,76,78`; ADR-0013 `:22` | legacy identifiers and file names (`Dim_Sintomas`, `Dim_Acceso`, `Dim_Pais`, `Dim_Tiempo`, `indicador_inferido_estres`, `porcentaje_*`, `genero`, `01_limpiar_datos.py`, `06_exportar_powerbi.py`, `CSV procesado`, "Base de Datos II") without a gloss | rule 3 says "any Spanish term"; practice is mixed: some are glossed (`phase4-closure.md:79,84`; ADR-0007 `:11`; ADR-0000 `:35,45`) | DECIDE (FIX) | Decided (N7): identifiers and paths in code format need no gloss (LOG-024) | PR-a1 | N7 | verified in text |
| DC-63 | `CLAUDE.md:11,13,21` (four uses) | "Fase 4" | not glossed | DECIDE | Decided (N8): one CLAUDE.md change (LOG-025) | PR-b | N8 | verified in text |
| DC-64 | `docs/decisions/README.md:11,13` | "Fase 1" in two titles | not glossed in the index | FIX (DECIDE) | Decided (N7): index titles exempt (LOG-024) | PR-a1 | N7 | verified in text |
| DC-65 | ADR-0003 `:11` and two more; ADR-0004 `:7` (title, before the gloss at `:11`); ADR-0006 `:7` | "Fase N" not glossed at first use | accepted ADRs | REPORT-ONLY | REPORT-ONLY | — | — | verified in text |
| DC-66 | ADR-0006 `:15,:16,:81` | "as Code needs to build them"; "produced across a long, exploratory conversation"; "what did we end up with" | rule 2 (attribution to a tool, to a conversation; first person); the voice test does not catch them (the last is in quotation marks) | DECIDE | Decided (N9): left as written (LOG-026) | — | N9 | verified in text |
| DC-67 | `docs/dataset-provenance.md:39,77` | "do not replace or edit them"; "Download it …, verify …, Place it …" | instructions addressed to a reader (rule 2) | FIX | impersonal | PR-a2 | — | verified in text |
| DC-68 | `docs/decisions/README.md:3,25` | "To add one, copy `adr-template.md` and fill it in."; "Use it only when … omit it otherwise." | as DC-67 | FIX | impersonal | PR-a2 | — | verified in text |
| DC-69 | 19 Markdown files, about 40 uses | sentence-initial "See …" | instruction to a reader, or a cross-reference convention: undecided | DECIDE | Decided (N10): allowed; one line in rule 2 (LOG-027) | — | N10 | interpretation |
| DC-70 | `docs/writing-conventions.md:3` | "These rules apply to every document in this repository: `docs/`, the ADRs, and the README." | narrower than rule 2 (`:13`: comments, docstrings, commit messages, PR text, test names) and `CLAUDE.md:23` | FIX | widen the scope sentence, by reference to rule 2 | PR-a1 | — | verified in text |
| DC-71 | `docs/decisions/adr-template.md:4` | `decision-makers` holds the repository owner's real name; the other two fields are placeholders | the template is not a decision record | FIX | low severity | PR-a1 | — | verified in text |
| DC-93 | `docs/writing-conventions.md:7` | "The legacy repository stays in Spanish, unmodified." | true at the tag `legacy-original` only: since commit `3cf77ce` the repository's `main` holds a superseded notice written in English (DC-44, LOG-006) | FIX | wording along the lines of "in Spanish and unmodified at the tag `legacy-original`; its superseded notice is the one later addition (ADR-0000)" | PR-a1 | — | verified in text |
| DC-72 | `docs/writing-conventions.md:11,18` | rule 2 forbids saying whose a decision was and allows `decision-makers` without a reason | — | DECIDE | Decided (N11): kept as written (LOG-028) | — | N11 | verified in text |
| DC-73 | `.gitignore` (GitHub Python template comments, e.g. `:86`, `:188`, `:200–201`) | second person ("you might want", "you can uncomment") | third-party template text inside a versioned file | DECIDE | Decided (N12): left as they are (LOG-029) | — | N12 | verified in text |
| DC-74 | `CLAUDE.md:3`; ADR-0002 `:15` | "SCU" | acronym used without introduction (rule 4) | DECIDE (REPORT-ONLY) | Decided (N8): CLAUDE.md, one change (LOG-025); ADR-0002: REPORT-ONLY | PR-b | N8 | interpretation |
| DC-75 | vocabulary: "conversion" (`indicators.md:82`, `indicators.py:95`, `indicator_15.sql:1`, framework `:84,86`); "isolation" (names 9–11; `dimensions.md:71`); "resource-access" (names 12–13); "non-uptake", "full context" (16); "fullest context", "persists" (ADR-0004 `:114`) | names and wording against rule 5 | decision c (and b, e) | DECIDE | b decided (LOG-013); c decided (LOG-014); e decided (LOG-016) | PR-c | c | verified in text |
| DC-76 | ADR-0003 `:29` "predict"; ADR-0004 `:94` "describing a relationship" | two framings of Q7 / indicator 14 | rule 5 and the ADR-0004 checklist | REPORT-ONLY | REPORT-ONLY (LOG-016) | — | e | verified in text |
| DC-77 | `CLAUDE.md:29`; `docs/decisions/README.md:14` (title of ADR-0007) | "person grain" | `fact-table.md:22`: one row per staged record; ADR-0008: no respondent identifier | DECIDE | Decided (f): response grain by an ADR-0007 addendum; title kept (LOG-017) | PR-c | f | verified in text |

What the voice test cannot catch, as observed: attribution to a working session written as "Chat N" (DC-55, DC-56); a tool named as "Code" (DC-66); "conversation" (DC-66); first person inside quotation marks that are not a quotation from a source (DC-66); imperative instructions to a reader (DC-67, DC-68); third-party template comments (DC-73).

### 5.6 Evidence discipline (probe 7)

| ID | Location | Statement | Why | Class | Disposition | PR | Dec. | Tag |
|----|----------|-----------|-----|-------|-------------|----|------|-----|
| DC-78 | ADR-0005 `:23` (F9); `country-region-mapping.md:3,18`; `phase4-closure.md:86`; `legacy-audit.md:19` | UNSD M49: the region level and the placement of Mexico and Georgia, "consulted 2026-09-23" | a web page; no capture under `docs/audit/evidence/` (ADR-0012 rule 2) | EXT | capture, or moderate the wording | PR-d | — | verified in text |
| DC-79 | ADR-0001 `:33` (H3); `legacy-audit.md:18`; `conceptual-framework.md:111` | RHMCD-20: columns "match, verbatim"; published 2023-12-18; COVID-era framing | a dataset deposit with a DOI: whether the ADR-0012 addendum treats it as a published work or as a page is undecided; no capture | EXT (DECIDE) | Decided (N13): published work, no capture (LOG-030) | PR-d | N13 | interpretation |
| DC-80 | ADR-0002 `:11,:36,:67`; ADR-0009 `:64`; `.sonarcloud.properties:1–3` | GitHub plan and ruleset behavior; a course "taught through DuckDB via Marimo notebooks"; SonarCloud's handling of `*.sql` | claims about third-party services or institutions; no capture | EXT | REPORT-ONLY on ADRs; config comment low | PR-d | — | interpretation |
| DC-81 | ADR-0011 `:35` (K3) | counts "published in pull-request descriptions (#33 and #34)" | PR text on GitHub is a changeable object (ADR-0012 rule 2); no capture | EXT | capture, or record as declared prior knowledge only | PR-d | — | interpretation |
| DC-82 | ADR-0000 `:30`; ADR-0003 `:15` | "At the time the legacy model was designed, the field was treated as indicating whether a person had gone through an interview that determined they were mentally unwell — a diagnostic or assessment event" | search result, method in section 5.6.1: the frozen report reads `mental_health_interview` as participation in an interview and as exposure or contact with the mental-health system; no passage found, in the text layer or on the eight rasterized pages, that describes an interview determining that a person was unwell, or a diagnostic or assessment event; ADR-0012 rule 2: a claim about the legacy project is carried by the frozen source alone | ADD | dated addendum: the participation and exposure/contact reading is carried by the frozen source; the "diagnostic or assessment" qualifier was not found in it; wording is a decision. Candidate for the declaration of prior knowledge (correspondence phase). [interpretation; disposition wording pending a decision] The error lies in how ADR-0000:30 and ADR-0003:15 describe the legacy reading, not in finding F3. The source describes mental_health_interview as willingness to raise a mental-health issue with a potential employer in an interview; the frozen report reads it as participation in an interview and as exposure or contact with the mental-health system (pp. 41-42, 79, 100, 113). Both readings differ from the source, so F3's conclusion stands. The addendum corrects the characterization of the legacy reading only; ADD is the right class. Source description verified in `docs/dataset-provenance.md:34` (Column documentation table, Data Card text "Would you bring up a mental health issue with a potential employer in an interview?"; capture listed at `:50`, `kaggle-datacard-columns-4-2026-09-19.png`) | PR-b / corr. | — | verified in text |
| DC-83 | ADR-0008 `:21` (G1) | "Computed against the SHA-256-verified extraction" | no versioned query or script records the computation | REPORT-ONLY | REPORT-ONLY | — | — | interpretation |
| DC-84 | `docs/audit/phase4-closure.md:90` | "a read-only review of the public repository re-ran the lint, type, and test tooling without the dataset, reproduced the merge conflicts noted during PR sequencing, and cross-checked …" | no versioned record of that review; "PR sequencing" not documented in the repository | ADD | cite a record, or moderate | PR-d | — | interpretation |
| DC-85 | `sources.md:47`; `legacy-audit.md:20`; `dataset-provenance.md:64`; ADR-0001 P5, P8, P9 | values readable in the Data Card captures restated | ADR-0012 `:79`: such values "are not restated in any other document"; the ADR restatements predate the rule | DECIDE | Decided (N14): option (i) with two readings of ADR-0012 `:79` (its scope is values about the data, not descriptions of what a capture shows; a check's own computed result has its own provenance), formalized by a dated addendum to ADR-0012 (PR-b); `dataset-provenance.md:64` points to the capture and keeps the rounding qualifier, `sources.md:47` points to A12's row, `legacy-audit.md:20` keeps A12's result and points to the capture for the match; all three in PR-d, stage 3 (LOG-011) | PR-d / PR-b | N14 | verified in text |
| DC-94 | `CLAUDE.md:25` | "outside material only as dated corroboration" | ADR-0012 rule 2 (`:57`) carries a claim about an object outside the repository, such as a third-party page, by a dated capture; rule 3 (`:58`) admits as corroboration only material about the legacy project | DECIDE | Decided (N8): one CLAUDE.md change (LOG-025) | PR-b | N8 | verified in text |

#### 5.6.1 DC-82: search of the frozen report (revision 1)

* Source: `git show legacy-original:"Informe DW/DW - Estrés y Salud Mental.pdf"` into a working folder outside the repository; SHA-256 `039e4385…dc81`, equal to the frozen report's hash in `evidence/report-versions-comparison-2026-09-29.md`; 127 pages. The clone was not changed.
* Text layer: `pdftotext` (default mode), searched per page, case-insensitive. Pages with hits: "dim_acceso" 2–4, 41–43, 47, 64, 78–79, 98–99, 113; "corrección" 2, 4, 42, 64, 78, 113, 126; "mental_health_interview" 7, 16, 24, 30, 42, 47, 78–80, 98, 100, 113; "contacto" 42, 79, 100, 113; "exposición" 42; "sistema" 1, 5, 42, 68, 100, 113; "entrevista" 7, 16, 19, 41, 42, 79; "evalu" 6; "diagn" 5; "atención", "atencion", "correccion", "exposicion": none. ("interview" matches only as part of `mental_health_interview`.)
* Raster pages, chosen by the text search and recorded before reading (a working file outside the repository, 2026-10-02T19:54:21Z): 41 (Dim_Acceso, design), 42 (Dim_Acceso: Corrección), 78–79 (ETL: Dim_Acceso), 98–100 (ETL: Dim_Acceso, second occurrence, with treatment in the dimension), 113 (Nota sobre corrección de Dim_Acceso). Excluded: 2–4 (table of contents), 43 and 47 (fact table and keys), 64 (fact-load script). Rendered with `pdftoppm -r 80`; only these eight pages were read.
* Passages, quoted exactly:
  * p. 41 and p. 42, field description of `mental_health_interview`: "Ha participado en entrevista de salud mental (Yes, No, Maybe)" (English: "Has participated in a mental-health interview (Yes, No, Maybe)").
  * p. 42, "Justificación de la corrección": "mental_health_interview: Contexto de exposición - ¿tuvo contacto con el sistema?" (English: "mental_health_interview: Exposure context - did they have contact with the system?").
  * p. 79, "Combinaciones coherentes": "care_options='Yes' + mental_health_interview='Yes' → Tiene recursos y ya tuvo contacto (escenario ideal)" (English: "… Has resources and has already had contact (ideal scenario)"); and, under "Validación 3": "¿La mayoría ha tenido entrevistas de salud mental?" (English: "Have most had mental-health interviews?").
  * p. 100, "Justificación conceptual": "mental_health_interview: ¿Ha habido contacto inicial con el sistema de salud mental?" (English: "mental_health_interview: Has there been initial contact with the mental-health system?").
  * p. 113: "care_options y mental_health_interview describen el contexto de acceso a recursos (¿tiene recursos disponibles? ¿ha tenido contacto con el sistema?)" (English: "care_options and mental_health_interview describe the context of access to resources (are resources available? has there been contact with the system?)").
* Not found: any passage describing an interview that determined a person was mentally unwell, or a diagnostic or assessment event for this field. "diagn" occurs once (p. 5, "fundamentar diagnósticos", about the project's general motivation) and "evalu" once (p. 6, "Evaluar la brecha…", the objective of Q4); neither concerns the field.
* Limit: a negative result over the text layer and the eight rasterized pages only. Text inside images on other pages is not covered.
* The 140-page continuation was not read; it is not versioned and is not citable (ADR-0012 rule 3).
* [interpretation; disposition wording pending a decision] The error lies in how ADR-0000:30 and ADR-0003:15 describe the legacy reading, not in finding F3. The source describes mental_health_interview as willingness to raise a mental-health issue with a potential employer in an interview; the frozen report reads it as participation in an interview and as exposure or contact with the mental-health system (pp. 41-42, 79, 100, 113). Both readings differ from the source, so F3's conclusion stands. The addendum corrects the characterization of the legacy reading only; ADD is the right class.
  * Verification of the source description: `docs/dataset-provenance.md:34` gives the Data Card's description of `mental_health_interview` as "Would you bring up a mental health issue with a potential employer in an interview?"; the same file lists the capture that carries it at `:50` (`audit/evidence/kaggle-datacard-columns-4-2026-09-19.png`). The capture was not opened in this revision (it also shows the column's distribution). The same text is quoted in ADR-0000 `:22,:30`, ADR-0003 `:15`, ADR-0004 `:112` and `conceptual-framework.md:38`.
* Side observation, for the starting-list item on `dim_access` (section 5.8): pp. 98–100 hold the legacy's own rationale for keeping `care_options`, `treatment` and `mental_health_interview` in one dimension ("Justificación conceptual: ¿Por qué combinar acceso y tratamiento en una sola dimensión?", English: "Conceptual justification: why combine access and treatment in a single dimension?"), resting on the contact reading; p. 113 keeps `care_options` and `mental_health_interview` together as "contexto de acceso" (English: "access context") after `treatment` is removed. The repository records no rationale after F3's reading.

### 5.7 Execution rules in living documents

| ID | Location | Statement | Why | Class | Disposition | PR | Dec. | Tag |
|----|----------|-----------|-----|-------|-------------|----|------|-----|
| DC-86 | `README.md:24`; `docs/audit/phase4-closure.md:16` | `uv run pytest` | with the source file present this runs C8–C10 without the restricted command `CLAUDE.md:24` requires until the criteria commit | DECIDE | Decided (N1, final): commands A (`uv run pytest -k "not (test_c8_ or test_c9_ or test_c10_)"`) and B (`CLAUDE.md:24`'s restricted command, verbatim) are written once, in `docs/audit/phase4-closure.md` §2 "Reproducing this", with the lapse condition ("until ADR-0011 allows exposure: after the criteria commit, after A5 has been run, and after A6 and A10 have been run or recorded as not obtainable (rule 4).") and the C1–C7/C11 failure sentence; `README.md:24`'s `uv run pytest` line is replaced by a one-line reference to that section, with the ADR-0011 link; no command is repeated in the README. README.md changed ahead of its planned rewrite, for execution safety only; the condition lapses when ADR-0011 allows exposure | PR-N1 (isolated, first PR of stage 3) | N1 | verified in text |
| DC-87 | `CLAUDE.md:24` | "the acceptance tests that execute the indicators (C8, C9 and C10)" | C10's tests do not call `run_indicator` (`test_acceptance.py:346,363`); a failing C10 assertion would display derived-condition counts, the K3 category (ADR-0011 `:35,:58`) | DECIDE | Decided (N8): one CLAUDE.md change (LOG-025) | PR-b | N8 | verified in text |
| DC-88 | `CLAUDE.md:21` | "The only work executed so far against the legacy repo is the read-only checks in `docs/audit/legacy-audit.md`." | other read-only work on the legacy is recorded: ADR-0012 S1–S3, ADR-0000's 2026-09-29 addendum, ADR-0013 M1–M2 | DECIDE | Decided (N8): one CLAUDE.md change (LOG-025) | PR-b | N8 | verified in text |
| DC-89 | `CLAUDE.md:30`; ADR-0013 `:68,:76` | "the correspondence evidence document" | defined nowhere (name, path, contents) | DECIDE | Assigned to the correspondence phase (l, LOG-021) | — | l | verified in text |
| DC-91 | section 2.5 | the reading rule (repository read normally; figures derived from the source file listed by file and category, never restated; no new values before the criteria commit) | no versioned general home: ADR-0011 rules 1, 2 and 4 and ADR-0012 `:79` cover parts only; stated in this register for the sweep only | NONE (correspondence phase) | general home pending for the correspondence phase | corr. | — | verified in text |

### 5.8 Items of the starting list not listed above

* `docs/specification/patterns.md:44` leaves `Occupation` and `care_options` in neither column group: pending g, correspondence phase. [verified in text]
* No post-F3 rationale for bundling care_options with mental_health_interview in dim_access. The only recorded rationale is the legacy's (frozen report pp. 98-100 for the three-field version, p. 113 after treatment was removed), and it rests on reading mental_health_interview as contact with the mental-health system, the reading F3 rejected. The bundle outlived its own justification. [For the correspondence phase; not a sweep finding.] Search basis: `dimensions.md`, ADR-0007 and ADR-0013 read in full; `docs/` searched for lines with `dim_access` and "why", "bundl", "because" or "reason"; frozen report, section 5.6.1.
* Design and sufficiency items of the starting list: not findings of this sweep; carried forward.

### 5.9 Findings that rest on a search by term (revision 1)

A negative result below holds only for the terms and files listed. "Scope" is the 70 files of the scope list (a working file outside the repository: 35 Markdown, 16 Python, 16 indicator SQL, 3 configuration) plus the 20 SQL headers.

| Search for | Kind | Terms or pattern | Files |
|---------|------|------------------|-------|
| probe 1 (section 6) | presence | `not yet`, `pending`, `will`, `to be`, `future`, `later`, `currently`, `provisional`, `planned`, `once`, `until`, `if confirmed`, `proposed`, `TODO`, `yet` (word-bounded, case-insensitive) | scope |
| search for DC-21 | absence | `negligible`, `query-time cost`, `seconds`, `benchmark`, `timing` | `docs/`, `src/`, `tests/`, `README.md`, `CLAUDE.md` |
| search for DC-22 | presence and resolution | Markdown links `[..](..)`; GitHub anchors from headings; backticked `docs/`, `src/`, `tests/` paths; `ADR-\d{4}`; finding codes `[FPHACIEGKSM]\d{1,2}`; `§N`, "section N" | 35 Markdown files (codes: scope) |
| search for DC-24 | presence | finding codes as above | scope |
| search for DC-25 | absence | `identifier` (case-insensitive), plus full reading | living documents |
| search for DC-46 | presence | `Dim_Sintomas`, `Dim_Acceso`, `Dim_Pais`, `Dim_Tiempo`, `Dim_Genero`, `indicador_inferido_estres`, `Indicador_Inferido_Estrés`, `porcentaje_`, `cantidad_`, `Hechos_Estres`, `genero`, `Base de Datos`, `Informe DW`, `CSV procesado`, `columnas`, `limpiar_datos`, `exportar_powerbi`, `cargar_hechos`, `crear_tablas`, `id_historial`, `Corrección`; gloss = `English:` on the same line | 35 Markdown files |
| search for DC-50 | presence | section 5.4.1 | 36 SQL, 16 Python, 35 Markdown |
| search for DC-53, DC-62, DC-63, DC-64, DC-65 | presence | `Fase`; gloss = `English: "Phase` | 35 Markdown files (DC-53 by reading of `src/`) |
| search for DC-66, DC-73 | presence | `Chat`, `Chat N`, `Code`, `conversation`, `the chat`, `assistant`, `we`, `We`, `our`, `us`, `you`, `your`, `I`, `my` | scope, without `tests/test_writing_conventions.py` |
| search for DC-67, DC-68 | presence | sentence-initial `Use`, `Do not`, `Don't`, `Download`, `Place`, `Copy`, `See`, `Read`, `Run`, `Note`, `Verify`, `Check`, `Add`, `Omit`, `Include`, `State`, `Keep`, `Never`; `do not replace`, `do not edit` | 35 Markdown files |
| search for DC-69 | count | sentence-initial `See` / `see` after `.`, `;`, `(` or `—` | 35 Markdown files |
| search for DC-74 | presence | `SCU` (word) | all tracked files (`git grep`) |
| search for DC-75, DC-77, DC-60, DC-76 | presence | `conversion`, `isolation`, `gap`, `persist`, `predict`, `develop`, `deteriorat`, `postpone`, `diagnos`, `symptom`, `severity`, `access`, `non-uptake`, `full context`, `fullest context`, `person grain`, `person-grain`, `respondent` | scope |
| search for DC-82 | presence and absence | section 5.6.1 | frozen report: text layer, 8 rasterized pages |
| search for DC-87 | absence | `run_indicator` | `tests/test_acceptance.py` |
| search for DC-90 | absence | `not rewritten`, `addend` (case-insensitive) | `docs/decisions/README.md`, `docs/decisions/adr-template.md`, `docs/writing-conventions.md`, `CLAUDE.md` |
| Starting list: `dim_access` rationale (section 5.8) | absence | lines with `dim_access` and `why`, `bundl`, `because`, `reason`; plus full reading | `docs/` |

Findings not listed here rest on a full reading of the cited lines, or on a script that compares two texts (question wording, indicator names, index rows, ADR-0012's prescribed wording).


### 5.10 Verified, no finding

Point verifications of single items that found the item consistent. No class, no ID; not counted in the totals (criterion in the section 5 legend).

| From section | Location | Verified | Result | Tag |
|---|---|---|---|---|
| 5.3 | ADR-0012 `:76–77` | constraints on ADR-0000's F2 cell and Context | applied: the three prescribed cell texts and the Context sentence occur verbatim in ADR-0000 | verified in text |
| 5.3 | ADR-0004 `:125` | Confirmation: corrected wording used verbatim as headers | all nine headers of `indicators.md` occur verbatim in ADR-0006; the eight revised ones also in ADR-0004 | verified in text |
| 5.3 | ADR-0009 `:85–86` | Constraints on `fact-table.md` (InnoDB) and `code-conventions.md` (`mysql.connector`) | both applied (`fact-table.md:18`; `code-conventions.md:9`) | verified in text |
| 5.4 | `indicator_05/06.sql`, `indicator_12/13.sql` | 5 and 6, and 12 and 13, are identical but for the header line | by design: a count and its rate are the same cell (`definitions.md:34`) | verified in text |
| 5.4 | indicator names | `indicators.md`, ADR-0006, `Indicator.name`, SQL headers | equal for all 16 | verified in text |
| 5.4 | ADR-0011 `:61` (rule 5) | explicit `ORDER BY` in every indicator query; surrogate keys in natural-key order | holds in all 16 queries and the 8 dimension loads (`ROW_NUMBER() OVER (ORDER BY …)`) | verified in text |
| 5.4 | ADR-0010 `:54` (Confirmation) | tests for a second run and a forced failure | `tests/test_warehouse.py:156,170` | verified in text |
| 5.5 | `docs/decisions/adr-template.md` | placeholder instructions ("State the question …") | normative template text | verified in text |
| 5.6 | ADR-0012 `:85` (Confirmation, rule 4) | every linked evidence file has a row in the evidence table of the document that owns its subject | holds for all 22 files (`dataset-provenance.md` for Kaggle, OWID, OpenML, figshare; `legacy-audit.md` for Looker and the report comparison; ADR-0009's addendum table for DuckDB and SQLite) | verified in text |
| 5.6 | ADR-0012 `:80` | P7 debts | closed by ADR-0001's 2026-10-01 addendum | verified in text |

## 6. Probe 1 classification of temporal hits

175 hits. Now false: DC-01, DC-03, DC-05, DC-06, DC-08, DC-17, DC-18, DC-49, DC-55, DC-56, DC-57, DC-58. HIST (true when written, dated by context or record date): ADR-0003 `:138`, ADR-0006 `:27`, ADR-0008 `:11,:55`, ADR-0009 `:11`, ADR-0010 `:11,:67`, `phase4-closure.md:16,19`. Still true: the Pending rows of `legacy-audit.md`; `specification.md:27`; `country-region-mapping.md:18`; ADR-0005 `:23`; ADR-0002's "no CI" lines (no workflow file is tracked; SonarCloud automatic analysis is configured by `.sonarcloud.properties`, which is not a required status check — interpretation); ADR-0007 `:66,:67`; ADR-0012 `:28`; ADR-0013 `:53,:55,:70`; `dataset-provenance.md:79`; `staging.md:38,44`; `conceptual-framework.md:63` (an expectation, interpretation). NORM or false positive ("has to be", "once" meaning a single time, "until then" in a rule): the remainder, including `CLAUDE.md:19,24,30`, the template, `writing-conventions.md`, ADR-0011, ADR-0012 rules, `schema.py:63,74`, and the test regexes.

## 7. Probe 8: concept-to-home map (confirmed in stage 2, 2026-10-03; LOG-010)

The map was confirmed in stage 2, before any correction pull request ([LOG-010](../decisions/log/LOG-010-concept-home-map.md)). Concepts, homes and reasons live in [`docs/concept-homes.md`](../concept-homes.md); this section keeps the sweep's dispositions. Each row names one concept, its proposed home, every other place it is stated, and a proposed class per place. "Verbatim" means the same wording as the home; "reworded" means the same claim in other words; "pointer" means a link or a reference without restatement. A place marked **S3** is also touched by a correction of stage 3 (finding in brackets); there the pointer is written in stage 3, in the same pull request, and stage 5 keeps only the rows without that mark. Accepted decision records are REPORT-ONLY on their side throughout and are listed only where they bear on the choice of home.

Search basis: the key terms of each concept (script `homemap.py`, a working file outside the repository; terms listed in section 7.3) over the living documents, the accepted decision records, the draft log and lessons, and this register, at commit `286c53d`. The duplicate scan of section 7.1 is the second source.

| # | Concept | Proposed home | Other places (kind) | Proposed class per place | Reason for the home |
|---|---------|---------------|---------------------|--------------------------|---------------------|
| 1 | Status of each A-series check | `docs/audit/legacy-audit.md#checks` | `conceptual-framework.md:106,111,113` (reworded, stale) **S3** [DC-05, DC-06, DC-08]; `specification.md:27` (reworded); `country-region-mapping.md:18` (reworded, A11); `phase4-closure.md` §6 table (reworded, with each check's effect; its status already drifted once, DC-14) **S3** [DC-14] | framework: REF; `specification.md:27`: REF; mapping `:18`: KEEP (the mapping needs to say which entries are unchecked, with a link to A11); `phase4-closure.md` §6: CONDENSE in stage 3 (keeps the effect column, takes each status by link to the audit table) | The audit table records each check's method and result; a status can change only there. |
| 2 | Status of Fase 4 (English: "Phase 4") | `docs/audit/phase4-closure.md#1-status` | `specification.md:22,26` (reworded, stale) **S3** [DC-01, DC-02]; `sources.md:53` (reworded, stale) **S3** [DC-03]; `methodology.md:11` (pointer to `staging.md`); `staging.md:3` (scope sentence); `CLAUDE.md:13,21` (summary); `README.md:14` **S3** [DC-17, N2: by reference] | `specification.md`, `sources.md`: REF; `methodology.md`: KEEP (phase map); `staging.md:3`: KEEP (defines what the part specifies, not the status); `CLAUDE.md`: KEEP (operational summary, links its home); `README.md`: as decided (LOG-002) | The closure record is dated and tied to a commit; status statements elsewhere drift (DC-01 to DC-03). |
| 3 | `explicit_recognition` and `symptom_cluster` | `docs/specification/definitions.md` (both anchors) | `indicators.md:31,68,78,88` (question texts, reworded: "convergent symptom profile"); indicator SQL 14–16 (literal, code); `tests/test_acceptance.py` (literal, independent oracle); `conceptual-framework.md:35,112` (legacy flag `Indicador_Inferido_Estrés`) **S3** [DC-59]; `CLAUDE.md:31` (summary); ADR-0003, ADR-0006 (REPORT-ONLY) | question texts: KEEP (verbatim question wording, ADR-0004 Confirmation); SQL: decision h (DC-50); tests: KEEP (an oracle written independently by design); framework: REF; `CLAUDE.md`: KEEP | The specification's definitions are the contract the code implements. |
| 4 | Validity caveat of `symptom_cluster` | `definitions.md#symptom_cluster` (the caveat block) | `conceptual-framework.md:112` (reworded, on the legacy flag) **S3** [DC-59]; `conceptual-framework.md:35` (reworded, table cell) **S3** [DC-59]; `indicators.md:74,84,94` (pointer); `patterns.md:31,43` (pointer); `indicators.py` caveat string (pointer, code); ADR-0005 (REPORT-ONLY, already a pointer) | framework: REF (DC-59, decided as FIX with REF); pointers: KEEP | Writing conventions, rule 4: a caveat travels by link from one home. |
| 5 | Population filter of indicators 15 and 16 | `definitions.md#multi-level-self-report-rule` (the filter as a non-fold) and `indicators.md` (the population) | `indicators.md:84` (pointer); ADR-0003 addendum, ADR-0006 (REPORT-ONLY) | KEEP | Two concepts in two homes: the rule (definitions) and the population (indicators); each points to the other. |
| 6 | Exposure rule | ADR-0011, rule 1 (with rules 2 and 4) | `CLAUDE.md:24` (operational summary, with command B verbatim); register §2.4 (pointer); `LOG-001` (pointer) | `CLAUDE.md`: KEEP (operational summary; its C10 wording is N8); others: KEEP | The rule is a decision; its record is its home. |
| 7 | Source columns: 17 in the file, 13 modeled, 4 not | `docs/specification/sources.md#column-map` | `specification.md:12` (parts table, reworded); `staging.md:24,32,38,40,44` (reworded, with pointers); `CLAUDE.md:33` (summary); ADR-0013 M7 (REPORT-ONLY) | `specification.md`: KEEP (rule: an index row states what the indexed part holds, `specification.md:5`); `staging.md`: KEEP (each mention carries a pointer and states what staging does with the columns); `CLAUDE.md`: KEEP | The column map is the only table that lists the 17 columns with their destination. |
| 8 | Column documentation: 7 of 17 columns described by the source | `docs/dataset-provenance.md#column-documentation` | `README.md:5` ("most of its columns have no description", reworded); `conceptual-framework.md` §4 "Basis" column (per column, reworded); ADR-0001 P6 (REPORT-ONLY) | `README.md`: KEEP (planned README rewrite); framework: KEEP (it maps each variable and needs its basis in the row; the column is a per-row attribute, not a restatement of the count) | The provenance record holds the source's text and its captures. |
| 9 | Fact grain | `docs/specification/fact-table.md#grain` | `CLAUDE.md:29` ("person grain", reworded) [f]; `docs/decisions/README.md:14` (title of ADR-0007); `staging.md:71` (pointer); ADR-0007, ADR-0008, ADR-0013 (REPORT-ONLY) | `CLAUDE.md`: KEEP, wording by decision f; index title: KEEP (mirrors the record's title) | The specification states the grain the load implements, "one row per staged record". |
| 10 | Dimension list | `docs/specification/dimensions.md#row-set` | `fact-table.md` columns (foreign keys, pointer); `acceptance.md` C1, C2, C5 (pointer); `specification.md:13` (parts table); `phase4-closure.md` §3 (result); `staging.md:57–59,65` (load order, reworded); `CLAUDE.md:29` (summary) | KEEP throughout, each for a named use: foreign keys (`fact-table.md`), checks (`acceptance.md`), a dated run result (`phase4-closure.md` §3), load order (`staging.md`), index (`specification.md:13`), operational summary (`CLAUDE.md`) | One table declares every dimension and its natural key. |
| 11 | Voice rule | `docs/writing-conventions.md#2-voice` | `CLAUDE.md:9,23` (summary with link); `tests/test_writing_conventions.py` docstring (scope of the check) | KEEP | The convention is the rule; the test implements part of it. |
| 12 | Licenses: the uploader's, the OSMI pages' | `docs/dataset-provenance.md` (Source; How to obtain the file) | `staging.md:34` (reworded, narrower) **S3** [DC-34]; `README.md:5` (reworded, short); `README.md:31` (the repository's own license, a different concept); ADR-0001 P1, P7 and addendum (REPORT-ONLY) | `staging.md`: REF; `README.md:5`: KEEP (planned README rewrite); `README.md:31`: not this concept | The provenance record holds the captures and the quotations. |
| 13 | Evidence conventions (captures dated, immutable, one row each) | ADR-0012, rules 1–4 | `dataset-provenance.md:39,52` (reworded; `:39` also an imperative) **S3** at `:39` [DC-67]; `legacy-audit.md:30` (pointer to rule 4); `CLAUDE.md:25` (pointer) | `dataset-provenance.md:39`: REF; `:52`: KEEP (it states the subject of a group of captures, which rule 4 asks the owning document to state); others: KEEP | The rule is a decision record. |
| 14 | Load rule | `docs/specification/sources.md#load-rule` | `staging.md:44` (reworded, with pointer); `code-conventions.md:20,36` (reworded, with pointer); `country-region-mapping.md:23` (a mapping-specific abort, a different rule) | `staging.md:44`: CONDENSE to the pointer and what staging adds (enforced on every load); `code-conventions.md:36`: REF; `:20`: KEEP (pointer only); mapping: not this concept | One home per rule; `staging.md:44` already names `sources.md` as its home. |
| 15 | Deduplication rule | `docs/specification/staging.md#deduplication` | `specification.md:26` (reworded) **S3** [DC-02]; `acceptance.md:17` (C11, the check's statement); `phase4-closure.md:28,61` (results); `docs/decisions/README.md:15` (title of ADR-0008); `CLAUDE.md:33` (summary); ADR-0008 (REPORT-ONLY) | `specification.md`: REF; C11: KEEP (a check states what it checks); results: KEEP; index: KEEP; `CLAUDE.md`: KEEP | The staging part specifies the rule the code implements; ADR-0008 holds its reasoning. |
| 16 | Staged and raw row counts | `docs/specification/staging.md#row-set` | `specification.md:26` (verbatim) **S3** [DC-02]; `acceptance.md:17` (C11 needs the number); `phase4-closure.md` §3 (result of a run); `legacy-audit.md:25–26` (legacy log facts, a different subject); `CLAUDE.md:33` (summary) | `specification.md`: REF; C11: KEEP; `phase4-closure.md`: KEEP (dated result); `legacy-audit.md`: KEEP (legacy evidence); `CLAUDE.md`: KEEP | The staging part fixes the count; the others check it, report it, or record the legacy's own count. |
| 17 | Results of check A13 | `docs/audit/legacy-audit.md` (A13 row) | `conceptual-framework.md:63` (reworded, with figures); ADR-0008 A13 row (REPORT-ONLY) | framework `:63`: CONDENSE, stage 5 (keeps the consequence for H1 with links to A13 and ADR-0001; the A13 figures leave) | Results live with the check; the framework needs only their consequence for H1. |
| 18 | The source's description of `mental_health_interview` | `docs/dataset-provenance.md#column-documentation` | `conceptual-framework.md:38` (verbatim quotation) **S3** for its other wording [DC-58]; ADR-0000, ADR-0001 addendum, ADR-0003, ADR-0004 (REPORT-ONLY) | framework: KEEP (an attributed verbatim quotation, the evidence its row interprets) | The provenance record carries the Data Card's text and its capture. |
| 19 | Wording of the business questions | ADR-0006, final questions (with ADR-0004 for the revisions) | `indicators.md` headers (verbatim) | KEEP (ADR-0004 Confirmation requires the verbatim header) | The decision records fix the wording; the specification repeats it by rule. |
| 20 | Default of `low_n_threshold` | `docs/specification/patterns.md#reporting-rules` | `indicators.py:21–22` (code, cites its home); `LOG-003` (describes the flag, no value); `phase4-closure.md:73` (restates the display rule, with a link) | KEEP (the closure record states what it leaves out, with the link) | The query layer's parameter is part of the reporting rules. |
| 21 | Country-to-region mapping and value domains | `country-region-mapping.md`; `sources.md#value-domains` | `domains.py` (code, names its homes); `legacy-audit.md:16,19` (checks; A8's result says the legacy's "36" was inaccurate); `sources.md:36` and `country-region-mapping.md:24` (restate A8's result, reworded); `acceptance.md` C6 "at most 35" and `dimensions.md:15` (the number, for a check and a ceiling); `phase4-closure.md:86` (A11 status, reworded) | `sources.md:36`, `country-region-mapping.md:24`: REF to A8, stage 5; others: KEEP | The specification holds the fixed tables; the code transcribes them and says so. |
| 22 | Test commands while ADR-0011's exposure order holds | `docs/audit/phase4-closure.md#2-reproducing-this` (after PR-N1) | `README.md:24` (command) **S3** [DC-86, N1: by reference]; `phase4-closure.md:16,19` (dated counts) **S3** [DC-16, DC-86]; `CLAUDE.md:24` (command B verbatim) | `README.md`: REF (LOG-001); `CLAUDE.md:24`: KEEP, a declared duplicate of command B (the operational summary must carry the command a working session runs; its wording is N8) | Decided in LOG-001. |
| 23 | The legacy repository is not modified beyond the superseded notice | ADR-0000, Decision Outcome, with its planned addendum (LOG-006) | `CLAUDE.md:17` **S3** [DC-44, PR-b]; `dataset-provenance.md:81` ("unmodified") **S3** [DC-92]; `methodology.md:13` ("at tag `legacy-original` … unmodified", correct as stated); `writing-conventions.md:7` ("stays in Spanish, unmodified") **S3** [DC-93]; `legacy-audit.md:3` (read-only checks); register §2.4 (pointer) | `CLAUDE.md`: REF to the addendum (LOG-006); `dataset-provenance.md:81`: FIX (DC-92); `methodology.md:13`: KEEP; `writing-conventions.md:7`: FIX (DC-93), keeping rule 1's statement about language; `legacy-audit.md:3`: KEEP | The decision record permits the one change; its addendum records it. |
| 24 | Outputs are test-bench outputs, not findings about a population | ADR-0001, Constraint | `patterns.md:45` (reworded, a reporting rule); `README.md:5` (reworded); `conceptual-framework.md:5` (reworded); `CLAUDE.md:3` (summary); ADR-0011 Consequences (REPORT-ONLY) | `patterns.md:45`: KEEP (the reporting layer needs the rule where it applies, with the link it has); `README.md:5`: KEEP (ADR-0001's own Confirmation requires the README to state it); framework `:5`: KEEP (it states the document's own scope, with the link); `CLAUDE.md`: KEEP | The decision record is the source; two places are required by it. |
| 25 | SHA-256 of the source file | `docs/dataset-provenance.md#identity-of-the-file` | `staging.md:34` (the value the extraction checks); `phase4-closure.md:9` (reworded, reproduction); `legacy-audit.md:9` (A1 result); `staging.py` constant (code) | `staging.md:34`: KEEP (the contract states the value the pipeline enforces); `phase4-closure.md:9`: REF; A1: KEEP (check result); code: KEEP | The identity record holds both hashes and how they were computed. |
| 26 | Hypotheses H1 and H3 and their tests | ADR-0001, Hypotheses | `legacy-audit.md` A5, A6, A10, A13 (tests, pointer); `conceptual-framework.md:56,63,111` (reworded); `phase4-closure.md:81–85` (status of tests) **S3** at `:81–82` [DC-14]; `dataset-provenance.md:79` (reworded, for the license argument); `staging.md:34` (pointer) **S3** [DC-33] | framework `:111`: REF **S3** [DC-06, DC-07]; `:56`: KEEP (the framework's threat analysis needs the claim, with the link); `:63`: CONDENSE, stage 5 (as row 17); others: KEEP | The hypotheses are stated where they were raised. ADR-0001's Hypotheses section is a findings-type section, not the decision itself; it is the home by necessity, since no living document explains H1 and H3, and corrections to them go by addendum. Tests and statuses live in the audit. |
| 27 | Reading of `mental_health_interview` as disclosure willingness | `conceptual-framework.md` §4 (variable mapping) | `conceptual-framework.md:92,94` (uses); `indicators.md:88` (question text); ADR-0000 addendum, ADR-0003, ADR-0004 (REPORT-ONLY) | KEEP (uses and question text); framework `:38` wording by decision N6 | The framework maps each variable; the specification and the decision records use the mapping. |
| 28 | `treatment` read as lifetime | `conceptual-framework.md` §4 (variable mapping) | `fact-table.md:16` (column meaning); `indicators.md`, `patterns.md:27,29` (names); ADR-0003 to ADR-0006 (REPORT-ONLY) | KEEP (each use names the measure; none restates the argument) | As row 27. |
| 29 | Identifier scheme for findings, hypotheses, checks, log entries and lessons | `docs/decisions/README.md#finding-and-hypothesis-ids` | `writing-conventions.md:45` (pointer); each ADR's "new letter" sentence (REPORT-ONLY); draft log and lessons (`LOG-`, `LSN-`) | home: ADD (DC-24; `LOG-` and `LSN-` per LOG-004) **S3**; pointers: KEEP | Writing conventions, rule 7, already names the README as the home. |
| 30 | Convention: accepted decision records are not rewritten and receive dated addenda | `docs/decisions/README.md` (new section; decided, N17, LOG-009) **S3** [DC-90, PR-a1] | register §2.3 rule 4 and §2.4 (sweep statement); `LOG-003`, `LOG-006`, `LOG-008` (uses) | register: REF once versioned; uses: KEEP | The README holds the conventions of decision records. |
| 31 | Reading rule | open (DC-91): general home pending for the correspondence phase | register §2.5 (stated for the sweep only) | register: KEEP until a general home exists | ADR-0011 and ADR-0012 hold parts; no document holds the whole. |
| 32 | Recording standard for decisions; format of lessons | [`docs/decisions/log/README.md`](../decisions/log/README.md#recording-standard); [`docs/audit/lessons/README.md`](lessons/README.md#format) | register §11, §12 (pointers) | KEEP | Decided in LOG-004. |
| 33 | Correspondence evidence document | undefined (decision l) | `CLAUDE.md:30`; ADR-0013 `:68,:76` (REPORT-ONLY) | — | Decision l defines it. |
| 34 | Corrections of the legacy region mapping (Mexico, Georgia) | `country-region-mapping.md#differences-from-the-legacy-mapping` | `phase4-closure.md:86` (reworded, A11 status); ADR-0005 F9 (REPORT-ONLY) | `phase4-closure.md:86`: KEEP (A11's status, with the link) | The mapping states its own differences. |
| 35 | Values about the data readable in a capture | each capture's evidence row (`dataset-provenance.md#evidence`), which states what the capture shows and links it; the value stays in the capture. Scope ([ADR-0012](../decisions/0012-cite-only-frozen-and-versioned-sources-as-evidence.md) `:79`, as read by LOG-011): values about the data (counts, ranges, distributions); descriptions of what a capture shows stay in its evidence row, and a check's own computed result has its own provenance | `dataset-provenance.md:64` (Data Card counts) **S3** [DC-85]; `sources.md:47` (Data Card range) **S3** [DC-85]; `legacy-audit.md:20` (A12's own range, with a clause "matching the Data Card") **S3** [DC-85]; ADR-0001 P5, P8, P9 (REPORT-ONLY) | `:64`: REF to the capture, keeping the rounding qualifier; `sources.md:47`: REF to A12's row; `legacy-audit.md:20`: KEEP the result as A12's own, the clause becomes a pointer to the capture; all PR-d, stage 3 | Decided in LOG-011. |
| 36 | Indicator names (wording depends on decision c) | `docs/specification/indicators.md` | `patterns.md:42` (pointer: outputs carry these names); `Indicator.name` in `indicators.py` and the SQL header comments (code transcriptions, equal for all 16); ADR-0006 (REPORT-ONLY); ADR-0003, ADR-0005 (REPORT-ONLY, earlier names) | KEEP (code transcribes the contract; a rename changes all places in one change) | The specification is the contract the code and outputs follow. |
| 37 | Reading of `care_options` (wording depends on decision b) | `conceptual-framework.md` §4 (variable mapping, "semantics assumed") | `indicators.md` question texts (verbatim, KEEP by ADR-0004 Confirmation); `dataset-provenance.md:35` (legacy-reading column, a different claim: how the legacy read it); ADR-0003 `:77` (REPORT-ONLY) | KEEP | The framework maps each variable; the specification uses the mapping in question wording fixed by decision records. |

Note (a), resolved: `writing-conventions.md:7` is finding DC-93 (FIX, PR-a1).

### 7.1 Decisions of home type: recommendations

* **j (ADR-0006 table, DC-40).** Decided: (ii), LOG-008. Options: (i) correct rows 5 and 6 in place; (ii) a dated addendum to ADR-0006 stating that `indicators.md` is the current definition of every indicator and recording how rows 5 and 6 differ (population and grouping sets); (iii) REPORT-ONLY. Recommended: (ii). ADR-0006 calls itself a snapshot that needs a manual update when the underlying records change (its own Consequences); an in-place change rewrites an accepted record (sweep rule 4); an addendum keeps the snapshot as history and points one way to the contract. Class ADD, PR-b.
* **N14 (capture values restated, DC-85).** Decided: option (i) with two readings of ADR-0012 `:79`, formalized by a dated addendum to ADR-0012 (LOG-011); all three places PR-d, stage 3. Options: (i) treat every restatement as a debt and remove it; (ii) apply ADR-0012's constraint to text written after it, keep a value where a document uses it as its own evidence, and point to that document elsewhere; (iii) no change. Recommended: (ii). `dataset-provenance.md:64` (identity evidence for P9 and A1) and `legacy-audit.md:20` (A12's own comparison) use the values as evidence: KEEP. `sources.md:47` restates the `Timestamp` range from the Data Card: REF to A12's row. ADR-0001 P5, P8, P9: REPORT-ONLY (they predate the constraint). The values stay declared prior knowledge for the correspondence phase (ADR-0011, rule 2). PR-d for all three places.
* **N17 (where the addendum convention is stated, DC-90).** Decided: (i), LOG-009. Options: (i) `docs/decisions/README.md`; (ii) the template; (iii) the writing conventions. Recommended: (i), a short section beside "Deviations from base MADR". The README already holds the conventions of decision records (format, Findings section, identifiers); the writing conventions govern prose, not the lifecycle of records; a template restating the rule would be a second home (a placeholder heading "Addendum (YYYY-MM-DD)" pointing to the README is optional). PR-a1, together with DC-24.
* **DC-34, REF part.** Decided, as below. `staging.md:34`'s license clause becomes a pointer to `dataset-provenance.md#how-to-obtain-the-file`, written with DC-33's correction of the same sentence. Stage 3, PR-a1.
* **DC-59, REF part.** Decided, as below. `conceptual-framework.md:112` points to the validity caveat at `definitions.md#symptom_cluster` instead of restating it, and `:35` names `symptom_cluster` as the successor of the legacy flag with the same link. Stage 3, PR-a2.

### 7.2 Stage 3 overlaps and what stays for stage 5

Written in stage 3 (pointer in the same pull request as the correction): rows 1 (framework `:106,111,113`; `phase4-closure.md:81–82`), 2 (`specification.md:22,26`; `sources.md:53`; `README.md:14`), 3 and 4 (framework `:35,112`), 12 (`staging.md:34`), 13 (`dataset-provenance.md:39`), 15 and 16 (`specification.md:26`), 18 (framework `:38`, wording only), 22 (`README.md:24`; `phase4-closure.md:16,19`), 23 (`CLAUDE.md:17`; `dataset-provenance.md:81`; `writing-conventions.md:7`), 26 (framework `:111`), 29 and 30 (`docs/decisions/README.md`), 35 (`dataset-provenance.md:64`, `sources.md:47`, `legacy-audit.md:20`; PR-d); 1 also `phase4-closure.md` §6 (CONDENSE).

Left for stage 5 (no overlap): row 1 `specification.md:27`; row 14 `staging.md:44` (CONDENSE) and `code-conventions.md:36` (REF); rows 17 and 26 framework `:63` (CONDENSE); row 21 `sources.md:36` and `country-region-mapping.md:24` (REF); row 25 `phase4-closure.md:9`.

A REF or CONDENSE written in stage 3 needs its claim-preservation table in the same pull request (probe 8, section 2.6), so those tables are drafted with the stage-3 plans, not after.

Stage-3 plan notes for `docs/concept-homes.md` (created in the records pull request): PR-a1 adds the anchor of the new section on addenda in `docs/decisions/README.md` to row 30; PR-b adds the link to ADR-0000's addendum on the superseded notice to row 23 (LOG-010).

### 7.3 Search terms of the concept pass

| Concept rows | Terms (regular expressions, case-sensitive unless marked) |
|--------------|-----------------------------------------------------------|
| 1 | `A(1[0-3]\|[1-9])` near "Pending", "pending", "Established", "established", "not run", "have run", "has run", "run yet" |
| 2 | "Fase 4", "Phase 4", "data-integration phase"; "closed" near "9f31ab0" or "rebuild" |
| 3 | `growing_stress = 'Yes'`; `mood_swings IN ('Medium', 'High')`; "three-symptom cluster", "convergent symptom profile" |
| 4 | "no external (clinical) validation"; "declared heuristic" |
| 5 | `care_options IN ('Yes', 'Not sure')`; "declared population filter" |
| 6 | "exposed"/"exposure" near "value"/"indicator"; "criteria commit" |
| 7, 8 | "17 (source) columns", "seventeen"; "13/Thirteen modeled"; "four unmodeled/not modeled/excluded", "Four of the 17"; "7 of (the) 17", "seven of (the) 17", "7 of its 17", "Only 7 of" |
| 9, 10 | "one row per staged record/survey response"; "person grain", "person-grain"; "grain" near "fact"; "eight dimensions" |
| 11 | "impersonal"; "first and/or second person" |
| 12 | "CC BY", "CC-BY"; "license", "licence" |
| 13 | "capture(d/s)" near "dated", "immutable", "never replaced", "not replace"; "never replaced or edited", "do not replace or edit", "immutable" |
| 14 | "aborts the load", "abort the load"; "outside its/their documented domain" |
| 15, 16 | "on all 17", "all 17 source columns", "17-column"; the staged count in its three spellings |
| 17 | "A13" |
| 18 | "Would you bring up a mental health issue" |
| 19 | Markdown block quotes; question rows of ADR-0006's table |
| 20 | "low_n"; "30" near "default"/"threshold" |
| 21, 34 | "Northern America", "Latin America and the Caribbean"; "35 countries/entries"; "Mexico" near "Georgia" (within 40 characters, which misses `country-region-mapping.md:18`; that line was found by reading) |
| 22 | "uv run pytest"; the restricted `-k` expression; "--ignore=tests/test_acceptance.py" |
| 23 | "never modified", "unmodified", "not modified", "superseded notice", "read-only" near "legacy" |
| 24 | "test bench"; "finding about any population", "findings about a/any population", "as prevalence" |
| 25 | "083f44e9", "SHA-256" |
| 26 | "H1", "H3" |
| 27, 28 | "disclosure willingness", "disclosure-willingness", "willingness to disclose"; "lifetime" |
| 29 | "Finding ID(s)", "finding ID(s)", "new letter", "letters in use" |
| 30 | "not rewritten", "dated addendum", "addendum, original" |
| 31 | "by file and category", "read normally" |
| 32, 33 | "recording standard"; "correspondence evidence document", "correspondence-criteria.md" |

Files: every tracked Markdown file outside `docs/audit/evidence/`, the ten draft files, and this register.

### 7.4 Step B results (duplicate scan)

881 units (paragraphs, list items and table rows of at least 12 words after normalization); living documents pairwise and within each document, and each ADR against each living document. Table rows are included as units, in addition to paragraphs and list items, because the specification's content sits mostly in tables. ADR-against-ADR pairs were not compared (both sides REPORT-ONLY).

* Probable (Jaccard ≥ 0.50): 10 hits, all question wording between ADR-0004 or ADR-0006 and `indicators.md`. KEEP (ADR-0004 Confirmation).
* Candidate (0.30–0.50): 10 hits: the rest of the question wording (KEEP); ADR-0008's identity rule against `staging.md:48` (the specification restating its decision record by reference: KEEP); ADR-0010 against `staging.md:61` (KEEP).
* Containment ≥ 0.60: 11 hits: the `mental_health_interview` and `treatment` quotations (KEEP); ADR-0008's A4 row against `legacy-audit.md:12` (REPORT-ONLY); ADR-0001's title in the decisions index (KEEP); ADR-0008's count against `specification.md:26` (REF, staged row count).
* Exact 8-grams below those thresholds: 60 hits, reviewed. Retained as REF candidates: `specification.md:26` (deduplication rule, counts); `staging.md:44` and `code-conventions.md:36` (load rule); `conceptual-framework.md:112` (validity caveat); `conceptual-framework.md:63` (A13 results). The rest are quotations, intra-document references, or ADR text citing its own contract.

### 7.5 Claim-preservation tables

Not drafted. The redundancy method (section 2.6, probe 8) requires one per REF or CONDENSE replacement once the home map is confirmed. For a REF written in stage 3 the table goes with that stage's pull request (section 7.2). The places listed in the map are the input those tables need.

### 7.6 N14: what ADR-0012 allows

Decided on 2026-10-03: option (i) with the two readings below, formalized by a dated addendum to ADR-0012 ([LOG-011](../decisions/log/LOG-011-adr-0012-scope-of-capture-values.md)). The analysis that led to it follows.

* [ADR-0012](../decisions/0012-cite-only-frozen-and-versioned-sources-as-evidence.md) `:79` (Constraint): "values readable in a capture are prior knowledge under rule 2 of ADR-0011 and are declared in the criteria document; they are not restated in any other document." The text has no exception for a document that uses the values as its own evidence, and it does not limit itself to text written after it.
* `:80` (Constraint) treats existing citations that do not meet rule 2 as debts, "recorded as debts and … not rewritten here"; it concerns citations of pages without a capture, not restated values.
* Rule 4 (`:59`) keeps the account of an artifact's origin in one evidence row, and "Every citation points to the row and does not restate it"; it concerns provenance, not values.
* The three places predate ADR-0012 (added 2026-09-29): `dataset-provenance.md:64`, `sources.md:47` and `legacy-audit.md:20` were all written on 2026-09-25 (`git blame` at `286c53d`).
* Result: ADR-0012's text does not allow keeping capture values where a document uses them as evidence. Keeping them would be a deliberate deviation. Its reason, for decision:
  * `dataset-provenance.md:64`: the identity argument (P9, A1) compares the legacy log's counts with the Data Card's; removing the Data Card side leaves a comparison with one side.
  * `legacy-audit.md:20`: A12's range is its own result, computed from the source file; "matching the Data Card" adds the comparison. The values are A12's, so this place may not restate a capture at all; only the comparison clause refers to it.
  * `sources.md:47`: restates the Data Card's range ("range per the Data Card"); no deviation is needed, since a pointer to A12's row carries the same fact.
* Options for decision: (i) remove every capture value outside the criteria document, by pointers; (ii) keep `dataset-provenance.md:64` as a declared deviation recorded by an addendum to ADR-0012, and keep `legacy-audit.md:20` as A12's own result, with `sources.md:47` becoming a pointer; (iii) treat the pre-existing places as debts by analogy with `:80`, recorded and not rewritten.

## 8. DECIDE items

| Item | Findings | Letter |
|------|----------|--------|
| Growing_Stress label — decided, LOG-012 (PR-a2) | — (starting list) | a |
| `care_options` wording; Q7.2 "available" vs 'Not sure' — decided, LOG-013 (PR-b) | DC-43, DC-75 | b |
| Renames 9–13, 15, 16 — decided, LOG-014 (PR-c) | DC-75 | c |
| Q3 text and objective — decided, LOG-015 (PR-b) | DC-38 | d |
| Objectives Q2, Q6, Q7.1, Q7.2; "gap" — decided, LOG-016 (PR-a2, PR-b) | DC-39, DC-60, DC-76 | e |
| "Person grain" — decided, LOG-017 (PR-c) | DC-77 | f |
| H1 partition | `patterns.md:44` | g (correspondence phase) |
| "One definition" of the cluster — decided, LOG-018 (PR-b) | DC-50 | h |
| A6 scope — decided, LOG-019 | DC-12 | i |
| ADR-0006 table — decided, LOG-008 | DC-40 | j |
| `file:line` citations in living documents — decided, LOG-020 | none found in living documents; ADR-0000 `:35` cites legacy script lines at the frozen tag (stable) | k |
| Correspondence evidence document — assigned to the correspondence phase, LOG-021 | DC-89 | l |
| Documented test command (`uv run pytest`); first DECIDE item of stage 2 — decided, LOG-001 | DC-86, DC-16 | N1 |
| README status sentence before the planned README rewrite — decided, LOG-002 | DC-17 | N2 |
| Minimum-count rule of ADR-0003 — decided, LOG-003 | DC-42 | N3 |
| Legacy "superseded notice" vs never modified — decided, LOG-006 | DC-44 | N4 |
| Weight of ADR-0009 items resting on E1, E2; addenda to ADR-0010, ADR-0013 — decided, LOG-022 (PR-b) | DC-45 | N5 |
| "Anticipated stigma" reading — decided, LOG-023 (PR-a2) | DC-58 | N6 |
| Gloss policy for Spanish identifiers and paths; docstrings; index titles — decided, LOG-024 (PR-a1, PR-c) | DC-46, DC-53, DC-64 | N7 |
| CLAUDE.md wording (Fase gloss; C10; legacy work; SCU; corroboration) — decided, LOG-025 (PR-b) | DC-63, DC-74, DC-87, DC-88, DC-94 | N8 |
| Voice in accepted ADRs — decided, LOG-026 | DC-66 | N9 |
| "See …" as instruction to a reader — decided, LOG-027 | DC-69 | N10 |
| `decision-makers` exception without a reason — decided, LOG-028 | DC-72 | N11 |
| Third-party template comments — decided, LOG-029 | DC-73 | N12 |
| RHMCD-20 deposit: published work or page — decided, LOG-030 (PR-d) | DC-79 | N13 |
| Capture values restated before ADR-0012 — decided, LOG-011 | DC-85 | N14 |
| Caveat text vs pointer in outputs — decided, LOG-031 (PR-c) | DC-54 | N15 |
| Whether sections 11 and 12 enter the versioned register in full — resolved by LOG-004 | — | N16 |
| General home of the reading rule (section 2.5) | DC-91 | NONE, correspondence phase |
| Versioned statement of the convention that accepted decision records receive addenda (section 2.4) — decided, LOG-009 | DC-90 | N17 |

### 8.1 Starting options

Options carried from before stage 1 for the letter items. None is decided; each is tagged [proposed; starting options]. Proposed texts are quoted verbatim.

* **b** [proposed; starting options]: neutral wording for `care_options`, with the meaning of the OSMI text stated as a candidate premise (match by column name only; the Data Card is silent). Alternatives: "awareness", or keeping "availability". Decided: option (b1), LOG-013.
* **c** [proposed; starting options]: renames: 9 "Explicit stress-recognition rate by time indoors"; 10 "Elevated mood-swings rate by time indoors"; 11 "Social-weakness rate by time indoors"; 12 "Care-options response rate"; 13 "Care-options response (count)"; 15 "Lifetime treatment-seeking rate by care-options response"; 16 "Lifetime no-treatment rate by stated disclosure willingness". The identifiers `dim_isolation`, `isolation_id` and `duration_band` stay and are declared residual: renaming them touches the DDL, the loads, queries 9–11 and 14–16 and tests C1, C2, C4, C5, C7 and C10, and requires repeating E3 (ADR-0013, constraint). Indicator names are not in `run_indicator`'s row output, so a hash over rows does not depend on them. Decided: LOG-014; the E3 reason is not carried (no versioned text states it).
* **d** [proposed; starting options]: Q3 text "Among respondents, what proportion report both growing stress (Growing_Stress = 'Yes') and coping difficulties (Coping_Struggles = 'Yes'), broken down by occupation and country, and how does that proportion differ when countries are grouped by region?"; objective "Describe how the proportion of respondents reporting both growing stress and coping difficulties differs by occupation (the dataset's five categories, which include Student and Housewife alongside employment categories), by country, and by region, without attributing any difference to a work environment or to resilience." Both by an ADR-0004 addendum; its Confirmation clause makes `indicators.md:27` and ADR-0006 `:35` move with it. Decided: LOG-015.
* **e** [proposed; starting options]: objectives. Q2: "describe how explicit stress recognition differs by gender and across the surveyed period within the subpopulation reporting a family history; no comparison group without family history, so it does not describe a relationship between family history and recognition". Q6: adds the recognition cut and uses "care-options responses". Q7.1: "describe lifetime treatment-seeking among respondents who report 'Yes' or 'Not sure' for care options, by recognition level and inclusion condition, without implying an active decision process or a shortfall against any expected level; 'No' is outside scope". Q7.2: "describe the proportion who do not report lifetime treatment-seeking within the context this dataset can express most favorably for it ..., without asserting persistence over time or postponement, since no time-to-treatment variable exists" (elided in its source as shown). Plus a documentary verdict "does not correspond to the original purpose" for Q2 and Q7.1. Decided: LOG-016 (objectives of Q2 and Q7.1 adopted; Q6 and Q7.2 written in the plan of PR-b under conditions; the documentary verdict assigned to the correspondence phase).
* **f** [proposed; starting options]: "person grain" -> "response grain", by an ADR-0007 addendum and in the living documents; the accepted ADR text stays; the Master Doc, outside the repository, is updated separately. Decided: LOG-017.
* **g** (correspondence phase) [proposed; starting options]: H1 partition for the criteria document: ADR-0001 P6 (documented vs undocumented by the Data Card), marked as preferred since it needs no new evidence; vs by names present in the OSMI schema; vs three-way. Under P6, 8 of 9 questions mix both groups; only Q5 does not. Both reading branches apply to the rest.
* **h** [proposed; starting options]: ADR-0007 `:65` "one definition": correct the text, no refactor. Decided: LOG-018, by an addendum (accepted text is not rewritten).
* **i**, **k**, **l**: no options were proposed. Decided: i, LOG-019; k, LOG-020; l assigned to the correspondence phase, LOG-021.

Options for the N items are developed when each item opens.

## 9. Not swept

* The legacy repository, except the frozen report's text layer (searched by term, sections 2 and 5.6.1) and its pages 41, 42, 78–79, 98–100 and 113 (rasterized and read). Those pages hold no figure derived from the source file: their counts are domain products (9, 18) and their example rows are illustrative combinations.
* `docs/audit/evidence/**` content, except the two OpenML captures viewed in the preliminary check before stage 1.
* The Master Doc, the Project instructions, pull-request descriptions, and git history (except checks that commits `9f31ab0`, `03c9aad` and `af4996e` exist on `main`).
* Truth against the source file (sweep rule 3); external truth of any third-party claim (EXT items are listed, not judged).
* `.python-version`, `LICENSE`, `uv.lock`, `src/stress_dw/py.typed` (out of scope by count).
* Seven test modules line by line: read through comments, docstrings, test names and assertion messages only.
* ADR-against-ADR duplication (probe 8).

## 10. Reconciliation by primary class

Every finding has exactly one primary class; the secondary class, where one applies, is in parentheses. The counts sum to 94.

| Primary class | Count | Findings |
|---------------|-------|----------|
| FIX | 28 | DC-01, DC-02, DC-03, DC-05, DC-06, DC-07, DC-08, DC-10, DC-11, DC-14, DC-15, DC-30, DC-33, DC-34 (REF), DC-55, DC-56, DC-57, DC-58 (DECIDE), DC-59 (REF), DC-60, DC-62, DC-64 (DECIDE), DC-67, DC-68, DC-70, DC-71, DC-92, DC-93 |
| DECIDE | 26 | DC-12, DC-17 (FIX), DC-38, DC-39, DC-40, DC-42, DC-43, DC-44, DC-46 (FIX), DC-50, DC-54, DC-63, DC-66, DC-69, DC-72, DC-73, DC-74 (REPORT-ONLY), DC-75, DC-77, DC-85, DC-86, DC-87, DC-88, DC-89, DC-90, DC-94 |
| ADD | 16 | DC-18, DC-24, DC-25 (REPORT-ONLY), DC-26, DC-31, DC-32, DC-35, DC-36, DC-37, DC-45 (DECIDE), DC-47, DC-48, DC-51, DC-61, DC-82, DC-84 |
| REPORT-ONLY | 9 | DC-04 (HIST), DC-20 (HIST), DC-27, DC-28, DC-29, DC-41, DC-65, DC-76, DC-83 |
| NONE | 7 | DC-09 (still true), DC-13 (correspondence phase), DC-19 (open obligation), DC-21 (open obligation), DC-22 (clean), DC-23 (clean), DC-91 (correspondence phase) |
| EXT | 4 | DC-78, DC-79 (DECIDE), DC-80, DC-81 |
| CODE | 3 | DC-49, DC-52, DC-53 (DECIDE) |
| HIST | 1 | DC-16 |
| Total | 94 | |

Rule applied: a finding on an accepted ADR that needs no change has REPORT-ONLY as primary class, with its nature (HIST) as secondary; one that needs a dated addendum has ADD; one whose action waits on a decision has DECIDE as primary unless the action itself is clear and only its wording is decided (then FIX or CODE, with DECIDE secondary).

## 11. Decisions

Decision records are kept in the decision log, one file per decision ([recording standard](../decisions/log/README.md#recording-standard)). This section only points to them.

| Item | Findings | Log entry |
|------|----------|-----------|
| N1 | DC-86, DC-16 | [LOG-001](../decisions/log/LOG-001-safe-test-commands.md) |
| N2 | DC-17 | [LOG-002](../decisions/log/LOG-002-readme-status-sentence.md) |
| N3 | DC-42 | [LOG-003](../decisions/log/LOG-003-minimum-count-addendum.md) |
| N16 | whether this section and section 12 enter the versioned register in full: resolved, they do not | [LOG-004](../decisions/log/LOG-004-decision-log-and-lessons.md) |
| N4 | DC-44 | [LOG-006](../decisions/log/LOG-006-legacy-superseded-notice.md) |
| j | DC-40 | [LOG-008](../decisions/log/LOG-008-adr-0006-addendum.md) |
| N17 | DC-90 | [LOG-009](../decisions/log/LOG-009-addendum-convention-home.md) |
| Home-map timing | section 7.2 | [LOG-007](../decisions/log/LOG-007-home-map-timing.md) |
| Concept-to-home map confirmed | section 7 | [LOG-010](../decisions/log/LOG-010-concept-home-map.md) |
| N14 | DC-85 | [LOG-011](../decisions/log/LOG-011-adr-0012-scope-of-capture-values.md) |
| b | DC-43; DC-75 (wording of `care_options`) | [LOG-013](../decisions/log/LOG-013-care-options-neutral-wording.md) |
| c | DC-75 (indicator names) | [LOG-014](../decisions/log/LOG-014-indicator-renames-and-residual-identifiers.md) |
| d | DC-38 | [LOG-015](../decisions/log/LOG-015-rewrite-q3-text-and-add-objective.md) |
| e | DC-39, DC-60, DC-76 | [LOG-016](../decisions/log/LOG-016-objectives-q2-q6-q71-q72.md) |
| f | DC-77 | [LOG-017](../decisions/log/LOG-017-response-grain.md) |
| h | DC-50 | [LOG-018](../decisions/log/LOG-018-cluster-literals-addendum.md) |
| i | DC-12 | [LOG-019](../decisions/log/LOG-019-a6-scope.md) |
| k | — | [LOG-020](../decisions/log/LOG-020-no-file-line-convention.md) |
| l | DC-89 | [LOG-021](../decisions/log/LOG-021-evidence-document-to-correspondence-phase.md) |
| N5 | DC-45 | [LOG-022](../decisions/log/LOG-022-adr-0010-0013-addenda.md) |
| N6 | DC-58 | [LOG-023](../decisions/log/LOG-023-disclosure-willingness-reading.md) |
| N7 | DC-46, DC-53, DC-64 | [LOG-024](../decisions/log/LOG-024-gloss-scope.md) |
| N8 | DC-63, DC-74, DC-87, DC-88, DC-94 | [LOG-025](../decisions/log/LOG-025-claude-md-wording.md) |
| N9 | DC-66 | [LOG-026](../decisions/log/LOG-026-voice-of-accepted-records.md) |
| N10 | DC-69 | [LOG-027](../decisions/log/LOG-027-see-as-cross-reference.md) |
| N11 | DC-72 | [LOG-028](../decisions/log/LOG-028-decision-makers-exception.md) |
| N12 | DC-73 | [LOG-029](../decisions/log/LOG-029-template-comments.md) |
| N13 | DC-79 | [LOG-030](../decisions/log/LOG-030-rhmcd-20-published-work.md) |
| N15 | DC-54 | [LOG-031](../decisions/log/LOG-031-cluster-caveat-by-link.md) |
| N8 (SCU item) | DC-74 | [LOG-033](../decisions/log/LOG-033-portfolio-destination-without-scu.md) |
| Citation of unversioned records during stage 3 | — | [LOG-032](../decisions/log/LOG-032-citing-unversioned-records.md) |
| a | no finding carries the letter; `definitions.md#explicit_recognition` gains one sentence (PR-a2) | [LOG-012](../decisions/log/LOG-012-explicit-recognition-premise.md) |
| Register conventions | legend of section 5; section 10 | [LOG-005](../decisions/log/LOG-005-register-bookkeeping-conventions.md) |

Conventions of this register itself (one primary class per finding, the class NONE, the `PR-` prefixes, the N identifiers, the "Verified, no finding" list) are applied in the legend of section 5 and in section 10; their reasoning is in LOG-005.

The working revisions of this register during stages 1 and 2 are not versioned; this file is the version that entered the repository at the end of stage 3.

## 12. Method lessons

Method lessons are kept by theme in the lesson files ([format](lessons/README.md#format)).

| Lesson | Theme file |
|--------|-----------|
| LSN-001, LSN-002, LSN-003, LSN-004 | [evidence and the limits of search](lessons/evidence-and-search-limits.md) |
| LSN-005, LSN-006, LSN-007, LSN-011, LSN-012 | [verification of commands, counts and locators](lessons/verification-of-commands-counts-and-locators.md) |
| LSN-008, LSN-009, LSN-010 | [bookkeeping and namespaces](lessons/bookkeeping-and-namespaces.md) |

## 13. Stage 3 pull requests

| Group | Pull requests |
|-------|---------------|
| PR-N1 | #47 |
| PR-N2 | #48 |
| Records (log, lessons, concept homes, index check) | #49 |
| PR-a1 | #50, #51 |
| PR-b | #52, #53, #54 |
| PR-a2 | #55 |
| PR-c | #56 |
| PR-d | #57 |
| PR-e | the pull request that adds this file |

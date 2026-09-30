---
status: "accepted"
date: 2026-09-29
decision-makers: Octavio Carpineti
---

# Cite only the frozen legacy source and versioned artifacts, and admit outside material only as declared corroboration

## Context and Problem Statement

Every finding in this repository has to be checkable against something that is in the repository or in a frozen source, never against anyone's memory or against a conversation. The question underneath is how the repository manages the information its claims rest on: which sources a claim may cite, what may accompany a claim from outside those sources, and where the account of an artifact's origin is written.

The rule has been applied without a name, and it works. [`dataset-provenance.md`](../dataset-provenance.md#evidence) has an Evidence section with eight captures dated 2026-09-19 under `docs/audit/evidence/`, one table row per capture, none to be replaced or edited. The claims about what the dataset's source declares ([ADR-0001](0001-position-as-portfolio-project.md), P1–P3 and P5–P8) cite those captures. That section is the precedent; this ADR points to it and does not duplicate it.

F2 of [ADR-0000](0000-rebuild-from-scratch-instead-of-continuing-legacy.md) shows what happens when the rule is not applied. F2 cited a "Looker Studio report configuration" as evidence. The chart had been built and inspected but never captured, so the claim rested on memory until 2026-09-28, below the standard every other finding meets. The account of where the chart came from existed in three places that did not refer to one another: F2's evidence cell, a section planned for the portfolio README, and discussion outside the repository. And the source itself is in no frozen source: the frozen legacy project never used Looker Studio (S1). The case illustrates the problem; the decision is the rule.

Which sources may a claim in this repository cite, under what conditions may material from outside them accompany a claim, and where does the account of an artifact's provenance live?

## Findings

Finding IDs use a new letter, `S` (sources): this ADR concerns where evidence may come from, which none of the letters in use (`F`, `P`, `E`, `G`, `K`) covers.

| ID | Finding | Evidence | Status |
|----|---------|----------|--------|
| S1 | **The frozen legacy source never used Looker Studio.** In `legacy-original` the PDF report (127 pages) has no mention of Looker and mentions Power BI on five lines; the export script is `python/06_exportar_powerbi.py`; no text file mentions Looker. | [`stress-dw-legacy@legacy-original`](https://github.com/CarpinetiOctavio/stress-dw-legacy/tree/legacy-original): `git grep -i looker` over non-binary files; `pdftotext` (default mode) on `Informe DW/DW - Estrés y Salud Mental.pdf`, then a case-insensitive count | Established |
| S2 | **The design-level claim of F2 is in the frozen source.** Page 49 of the PDF report holds the sample query `AVG(h.porcentaje_estres)` over the fact table joined to gender and time, as an embedded image (its text is not extractable). The flat export at `legacy-original` has 350,699 rows and the `porcentaje_*` columns. | Page 49 of the PDF report rendered with `pdftoppm`; header and row count of `CSV procesado /dw_salud_mental.csv` at `legacy-original` | Established |
| S3 | **The 140-page version of the report (the continuation), which is not versioned, is the frozen report in substance: no element that the model, the formulas or F1–F4 rely on differs.** The differences found are editorial and presentational, plus added technical description. Over the whole text the similarity is 0.9632 with 52 differences, of these kinds: the BI tool named (Power BI becomes tool-agnostic wording plus Looker Studio); code that is an image in the frozen report and text in the continuation; reordered tables; added technical content (library table, project tree, password read from an environment variable); the cover; a deleted draft sentence; and editorial wording corrections, such as one word in the objective of the fourth question ("las"). | Method: `pdftotext` (poppler 26.08.0, default mode) on both PDFs; U+200B and `<br>` removed, lines holding only a page number dropped, whitespace collapsed to one space; word-level comparison with `difflib`; sections taken between their titles, using each title's occurrence in the body (after the table of contents), and hashed with SHA-256. Method, hashes of both PDFs and the list of differences: [comparison record](../audit/evidence/report-versions-comparison-2026-09-29.md) (rule 3) | Established for the frozen report; the continuation is not versioned, so the record is the only trace of what was compared |
| S4 | **The chart captured on 2026-09-28 belongs to the Looker Studio report of the continuation, which is not part of the frozen source; its relation to the frozen source is verified in design and in structure, not in content.** The continuation names Looker Studio as its BI tool and is the frozen report in substance (S3). The captures, taken from the existing Looker Studio report, show a bar chart with data source labeled `Stress (csv)`, dimension `genero`, metrics `AVG(porcentaje_tratamiento)` and `AVG(porcentaje_no_tratamiento)`, no filter and no date range dimension. The frozen export has those three fields under the same names. Whether the report's data source is that file is not verified. | [`looker-studio-treatment-by-gender-metrics-2026-09-28.png`](../audit/evidence/looker-studio-treatment-by-gender-metrics-2026-09-28.png), [`looker-studio-treatment-by-gender-filters-2026-09-28.png`](../audit/evidence/looker-studio-treatment-by-gender-filters-2026-09-28.png); header of the frozen export; [comparison record of S3](../audit/evidence/report-versions-comparison-2026-09-29.md) | Configuration: Established as captured. Design relation: Established through S3, given the declared provenance. Content relation: Pending, closed by the unweighted `AVG` half of A7 |

## Decision Drivers

* A claim has to be checkable by someone who has only the repository and the frozen source.
* The rule has to resolve the next case (another capture, another outside source) by applying it, without a new decision record.
* The rule must not invalidate what already works: the dataset captures are evidence about an object outside the repository, and no frozen source can carry them.
* Evidence outside the frozen source cannot be held to the same standard: there is no hash of the object and it can change. A finding that depends on it inherits that weakness.
* The account of an artifact's origin has to be written once and cited from every use, not rebuilt at each citation.
* The frozen source is not modified ([ADR-0000](0000-rebuild-from-scratch-instead-of-continuing-legacy.md)); anything about it that the frozen source cannot say has to be stated as outside it.

## Considered Options

* A single source, no exceptions: nothing from outside the frozen source enters as evidence.
* A single source, with outside material only as corroboration: findings rest on the frozen source and versioned artifacts alone, and outside material may accompany a finding under conditions but no finding depends on it.
* Outside evidence admitted under conditions: captured as a versioned dated artifact, with declared provenance and a verified relation to the frozen source, and then usable as primary evidence.

## Decision Outcome

Chosen option: "A single source, with outside material only as declared corroboration", because it is the only option under which every finding's evidence is complete inside sources that anyone can check, while still telling the next case what to do with material that is not one of them.

1. **Citable sources.** A claim cites (a) `stress-dw-legacy` at `legacy-original`, or (b) a versioned artifact of this repository: a document, code, or a capture taken on a stated date and stored under `docs/audit/evidence/`, never replaced or edited.
2. **The subject decides the source.** A claim about the legacy project is carried by (a) alone. A claim about an object outside the repository (a web page, the state of a third-party tool) is carried by a capture of it under (b), dated when taken. Nothing else carries a claim: not memory, not a conversation, not a live link.
3. **Outside material as corroboration.** Material about the legacy project that is not in (a), such as a chart built in another tool, an unversioned version of the report, or a reproduction, may accompany a claim as corroboration. No finding depends on it: the finding's evidence is complete without it. It is admitted only if (i) it is captured as a dated artifact under `docs/audit/evidence/`; (ii) its provenance is declared where it is cited, in one sentence, with the account itself written once (rule 4); (iii) its relation to (a) is stated as verified, with the check that verified it, or as unverified, with the check that would. An analysis over an unversioned input, such as the comparison in S3, is captured the same way, recording its method and the SHA-256 of each input.
4. **One home for provenance.** The account of an artifact's origin is a row in an evidence table in the document that owns the subject: file, date taken, what it shows and, for corroboration, its provenance and its relation to (a). Every citation points to the row and does not restate it. The Evidence table of `dataset-provenance.md` is the model; artifacts about the legacy audit have their table in [`legacy-audit.md`](../audit/legacy-audit.md).

### Applied to F2

F2 rests on the frozen source (S2): the fact-table structure of the report, the sample query on page 49 and the flat export. The captured chart is corroboration under rule 3: (i) captured on 2026-09-28 from the existing Looker Studio report of the continuation; (ii) provenance declared in its evidence-table row: an original artifact of that report, which is not versioned, built in a tool the frozen source does not use (S1); (iii) relation verified in design through S3 (the continuation is the frozen report in substance) and in structure through S4 (the fields), unverified in content, the check being the unweighted `AVG` half of A7.

The chart is not redundant. The query on page 49 shows the defect at design level, in the report's own example. The chart shows the same aggregation configured in a BI tool and applied to treatment by gender, the comparison whose figure A7 examines. Those are two different claims. The second is a claim about the chart, not about the legacy design, and it cannot be checked against the frozen source except through the continuation's design (S3) and the flat export (S4). What F2 grounds (the rebuild, the person grain, additive measures) follows from the design defect alone. Once A7 reproduces the chart's aggregation from the frozen export, the relation moves from unverified to verified; what carries F2 does not change.

The last sentence of F2's finding cell, "The Looker Studio chart on treatment by gender applies `AVG` to these columns.", is removed from the finding. It is a claim about an artifact outside the frozen source, which the frozen source cannot carry (rule 2); it is not withdrawn, and it stays as corroboration in the evidence cell (rule 3), where its captures and its evidence-table row support it. F2 is edited in place instead of receiving an addendum because that sentence did not support what F2 grounds, and an addendum would leave the unsupported attribution standing in the finding; the removal is recorded here.

### Consequences

* Good, because every finding can be verified by anyone with the repository and the frozen tag, and the check is mechanical (see Confirmation).
* Good, because the next case is resolved by rules 1–4: a new capture of an outside page carries claims about that page; a derived artifact about the legacy accompanies a finding and never carries it.
* Good, because the dataset precedent stays valid without change.
* Bad, because an artifact that matters for the narrative, such as a chart as a user would see it, cannot carry any claim about the legacy project, however faithful it is.
* Bad, because findings have to be scoped by subject, which is more discipline than citing whatever supports the claim.
* Constraint: the evidence cell of F2 in ADR-0000 is rewritten once, by the pull request that adopts this ADR, as follows. The finding cell drops its last sentence (quoted in "Applied to F2") and reads: "**Pre-aggregated ratios without numerators or denominators.** The fact table stores percentages; the report's sample query averages them (`AVG(porcentaje_estres)`), an unweighted mean of ratios." The evidence cell reads: "Report, Phase 3 (fact table) and sample query (page 49 of the PDF at `legacy-original`, an embedded image); flat export `CSV procesado /dw_salud_mental.csv` at `legacy-original` (`porcentaje_*` columns). Corroboration outside the frozen source, not required by the finding: Looker Studio chart on treatment by gender, captured 2026-09-28 ([metrics](../audit/evidence/looker-studio-treatment-by-gender-metrics-2026-09-28.png), [filters](../audit/evidence/looker-studio-treatment-by-gender-filters-2026-09-28.png)); provenance and relation to the frozen source in the [Evidence table of `legacy-audit.md`](../audit/legacy-audit.md#evidence); rule in [ADR-0012](0012-cite-only-frozen-and-versioned-sources-as-evidence.md)." The status cell reads: "Established against the report and the export at `legacy-original`. The chart capture corroborates and is not required by the finding."
* Constraint: the sentence of ADR-0000's Context that lists "a Looker Studio report" among what the legacy project implements is replaced in the same pull request by "a flat CSV export for a BI tool (Power BI, in the frozen source)", since it attributes to the legacy project an artifact that the frozen source does not contain (S1).
* Constraint: when A7 closes it reads: compute the treatment rate by gender from staging with explicit numerator and denominator; compute the unweighted `AVG` of `porcentaje_tratamiento` by `genero` over the flat export at `legacy-original`, the aggregation the report's sample query applies; compare the two, and compare the second with the captured chart, which verifies or refutes the relation stated in S4. Both sides are treatment-by-gender values, so the check is run after the criteria commit of [ADR-0011](0011-preregister-correspondence-criteria-before-exposing-indicator-values.md). The row does not mention Looker Studio except through its evidence-table row.
* Constraint: values readable in a capture are prior knowledge under rule 2 of ADR-0011 and are declared in the criteria document; they are not restated in any other document.
* Constraint: existing citations that do not meet rule 2 are recorded as debts and are not rewritten here. [ADR-0001](0001-position-as-portfolio-project.md), P7 cites the OpenML page, a published analysis and a figshare deposit by URL for the OSMI figures, and `docs/audit/evidence/` holds no capture of them. Each is closed by a new capture dated when taken.
* Constraint: all other citations to the report keep pointing to `legacy-original`, unchanged.

### Confirmation

* Every file under `docs/audit/evidence/` that a document links has a row in the evidence table of the document that owns its subject, with the fields of rule 4. Checked by searching `docs/` for links to that directory.
* No Findings row has an Evidence cell made only of corroboration: removing the corroboration items leaves the row evidenced. Checked by review of each row that cites an outside artifact.
* The comparison record of S3 exists under `docs/audit/evidence/`, with the method, the SHA-256 of both PDFs and the list of differences.
* ADR-0000 carries the wording of the two constraints above for F2 and for its Context, verified by diff against this ADR.

## Pros and Cons of the Options

### A single source, no exceptions

* Good, because it is the simplest rule and the easiest to check.
* Bad, because as a rule it is too narrow: the claims about what the dataset's source declares can only be carried by captures of outside pages, so a rule admitting nothing from outside the frozen source would remove the precedent that works. Saving that precedent requires scoping by subject, which is the chosen rule.
* Bad, because it gives no guidance for the next outside artifact beyond refusing it.

### A single source, with outside material only as corroboration

* Good, because each finding's evidence can be verified byte for byte or by hash: the frozen tag, the repository, the captures.
* Good, because F2 loses nothing it needs: the design defect is complete in S2, and every decision F2 grounds follows from it.
* Good, because the conditions for corroboration (dated capture, declared provenance, stated relation) keep useful outside material in the repository, verifiable as an artifact, without letting it carry a claim.
* Bad, because the chart, the only artifact about the treatment-by-gender aggregation, is demoted to corroboration despite being real work.

### Outside evidence admitted under conditions

* Good, because it keeps the chart as primary evidence and matches how the work was done: the chart is an original artifact of the continuation, not a reproduction, and its design relation to the frozen report is established (S3).
* Bad, because the conditions make an artifact checkable as an artifact, not able to carry a claim about the legacy: the relation runs through an unversioned document (the continuation) and through a data source not verified to be the frozen export (S4), and the report lives in a third-party tool whose state a capture fixes on one date only.
* Bad, because the claim the chart adds (the aggregation as configured in a BI tool) supports no decision that the design defect does not already support, so the option would admit primary evidence where none is needed, and each later case would have to argue again what its artifact adds.

## More Information

* Related: [ADR-0000](0000-rebuild-from-scratch-instead-of-continuing-legacy.md) (F2, Context), [ADR-0001](0001-position-as-portfolio-project.md) (P-findings, the dataset captures), [ADR-0011](0011-preregister-correspondence-criteria-before-exposing-indicator-values.md) (prior knowledge, check ordering).
* Precedent: the Evidence section of [`dataset-provenance.md`](../dataset-provenance.md#evidence).
* Frozen source: [`stress-dw-legacy@legacy-original`](https://github.com/CarpinetiOctavio/stress-dw-legacy/tree/legacy-original) (`f2308d29217c8130a14875d7dad7070272b92d28`).
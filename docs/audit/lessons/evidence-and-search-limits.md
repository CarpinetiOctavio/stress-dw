# Evidence and the limits of search

Format: [lessons index](README.md#format).

## LSN-001 — A term search cannot prove absence

* **What happened.** The documentation-currency sweep searched the text of the frozen legacy report for two terms, "entrevista" (English: "interview") and "diagn" (the stem of "diagnóstico", English: "diagnosis"), and reported that the report did not support a reading of `mental_health_interview`. The passages that describe that reading use other words: "contacto" (English: "contact"), "exposición" (English: "exposure"), "sistema" (English: "system").
* **How it was detected.** On review, by naming other wording the source might use for the same idea.
* **Rule.** An absence claim lists the terms and the files searched and is stated as a search result, not as a fact about the source. Where text may sit inside images, the pages to rasterize are chosen by a text search and recorded before they are read.
* **Pointers.** Finding DC-82 of the documentation-currency register.

## LSN-002 — A literal search must cover uses through an alias

* **What happened.** A finding listed the places where the literal `mood_swings IN ('Medium', 'High')` is repeated and omitted `indicator_10.sql`, where the same literal is applied to an alias of the column.
* **How it was detected.** On review, against an earlier reading of the same line.
* **Rule.** A search for a repeated literal lists every location, with the role of each use, including uses through aliases.
* **Pointers.** Finding DC-50 of the documentation-currency register.

## LSN-003 — A starting claim is verified before it is used

* **What happened.** The list of known incongruences the documentation-currency sweep started from placed the exposure rule in `acceptance.md`. A search found no mention of it there.
* **How it was detected.** By the search that built the sweep's concept-to-home map.
* **Rule.** Every claim in a starting list is verified against the repository before it is used.
* **Pointers.** Concept-to-home map of the documentation-currency register.

## LSN-004 — A condition that cites a rule is checked against it item by item

* **What happened.** A first wording of a lapse condition allowed A5, A6 and A10 to be recorded as not obtainable. [ADR-0011](../../decisions/0011-preregister-correspondence-criteria-before-exposing-indicator-values.md), rule 4, gives that allowance only to A6 and A10, which need external datasets; A5 is computed on the source file.
* **How it was detected.** By reading the condition against rule 4, item by item.
* **Rule.** A condition that cites a rule of a decision record is checked against the rule's text, item by item, before it is recorded.
* **Pointers.** [LOG-001](../../decisions/log/LOG-001-safe-test-commands.md).

---
id: LOG-050
alias: correspondence criteria, interpretability bound, harmonization and α
date: 2026-10-09
status: recorded
formalization: none
---

# Fix the interpretability bound of A5 and A6, the harmonization of values, and the α of A10's guard, by the scheme of LOG-047

## Decision

Three elements of the rule that maps checks A5, A6 and A10 to a reading branch are fixed by the scheme of [LOG-047](LOG-047-a5-threshold-procedure.md): a published, consultable source first, verified against its text and entered in the [verification register](../../references/verification.toml) ([LOG-048](LOG-048-verifiable-source-checks.md)), with the search recorded; failing such a source, a declared convention of this project, marked as interpretation ([writing conventions, rule 7](../../writing-conventions.md#7-evidence-discipline)), with its reasoning. Their values, and the list of equivalences of item 2, are fixed in the criteria document, before A5, A6 and A10 run.

1. **Interpretability bound.** Each pair of A5 and each column of A6 carries a noise floor b, the expected size of its measure under no association. For A5, b = √(u/(n − 1)) with u = (r − 1)(c − 1), from the expectation of φ̂² under independence in Bergsma (2013), equation (1), p. 324. For A6, compared as two samples of sizes n₁ and n₂ over k categories, b = √(u · (1/n₁ + 1/n₂)) with u = k − 1, the same expectation for the measure that does not depend on the ratio of the sample sizes, obtained by algebra on the expectation of Bergsma (2013), equation (1), p. 324, and on Cohen (1988), formula (7.2.1), p. 216, and (7.2.2), p. 221; the algebra is this project's interpretation. A measure is interpretable only when b is below half of the threshold for a small effect. This bound is a declared convention: no published source was found.
2. **Harmonization of values.** Before A5, A6 and A10 run, the four unmodeled source columns, the OSMI 2014 data and the RHMCD-20 data are trimmed and case-folded. In the four unmodeled columns, which have no [documented domain](../../specification/sources.md#value-domains), values that differ only in case are merged under their most frequent form. In A6, the values of OSMI 2014 in a column with a documented domain are mapped to the file's domain labels by a closed list of equivalences, written from those labels only and without reading the values of OSMI 2014; every value the list does not match goes to one category, reported with its count and its values. A column with no documented domain (`self_employed` in A6) has no list: both sides are trimmed and case-folded only. In A10 no list is applied: both sides are trimmed and case-folded only. A null is a category of its own in A5 and A6; in A10, a profile with a null in any of its eight columns is left out of the containment test, and the number left out is reported. The same rule applies to both sides of every comparison.
3. **α of A10's guard.** The significance criterion that Cohen (1988), p. 12, describes as conventional.

## Linked findings

None.

## Options considered

* (a) Each element by LOG-047's scheme: a published source first, failing it a declared convention.
* (b) Each element as a declared convention, without a search.
* (c) Each element fixed after the checks run.

## Option chosen

(a).

## Reasons

* Search, 2026-10-09:
  * The sources of the verification register that concern association measures, Cohen (1988), Bergsma (2013) and Kim (2017), were searched in their text layers for conventions, significance criteria, interpretation, negligible values, bias, expected frequencies, rules of thumb and minimums.
  * Two web searches were run, on a bias or sample-size bound for Cramér's V and on the expected value of φ² under independence as a noise floor. They returned tutorials and software documentation, none of them a published, consultable source in the sense of LOG-047.
* Interpretability bound:
  * Bergsma (2013) gives the expectation of φ̂² under independence and a bias-corrected estimator, but no bound.
  * Kim (2017), p. 153, gives a rule on expected frequencies for the chi-squared approximation of a significance test. A5 and A6 read the size of a measure, not a test, so the rule does not apply to them.
  * The bound is therefore a convention. b is the size the measure takes with no association at all. A bound of half the small-effect threshold keeps a measure from reaching that threshold through sampling noise alone. A measure with b at or above the threshold would reach it with no association, and would read as association.
* Harmonization:
  * The file's marginal distributions are already known ([ADR-0001](../0001-position-as-portfolio-project.md), P8). A list of equivalences built from the observed values of OSMI 2014 would therefore show A6's result before A6 runs, which is why the list is written from the file's domain labels only.
  * A list for a column with no documented domain would have to be written from the file's values, which would mean reading the source file before the check's turn ([LOG-049](LOG-049-reading-rule-by-repository-access.md), item 3).
  * A10 applies no list. H3 states that the eight columns match those of RHMCD-20 "verbatim" ([ADR-0001](../0001-position-as-portfolio-project.md), H3), and A10 tests exact or near-exact row matches ([`legacy-audit.md`](../../audit/legacy-audit.md#checks), A10). Mapping RHMCD-20's values to the file's labels could create matches that the values do not hold. That would bias A10 toward "confirms", the outcome that overrides A5.
  * A single category for unmatched values keeps u small. A difference of domain then shows as a category present on one side and absent on the other, instead of making the column uninterpretable under item 1.
  * Applying the same normalization to both sides keeps a difference of format from blocking an exact match in A10.
  * A null records no value whose source can be compared, so a profile with a null cannot show whether the file's values come from RHMCD-20.
  * No published source was searched for this item: it is a procedure on the datasets compared, not a threshold.
* α: Cohen (1988), p. 12, states the significance criterion that "has come to serve as a convention", so a published source exists and no convention is declared.
* Each element rests on algebra, on the specification or on the design of the checks, and on no result of A5, A6 or A10, which do not exist before the criteria commit ([LOG-049](LOG-049-reading-rule-by-repository-access.md), item 3).

## Reasons for each rejected option

* (b): LOG-047 requires a published source first.
* (c): a threshold chosen after the result is known depends on the data ([ADR-0011](../0011-preregister-correspondence-criteria-before-exposing-indicator-values.md), Context; LOG-047).

## Open, and where it goes

* The values of items 1 and 3, the list of equivalences of item 2, and the limitation of the chance model of A10's guard: the criteria document, section 3.
* The prior knowledge of the OSMI 2014 values, declared beside the list: the criteria document, section 1.

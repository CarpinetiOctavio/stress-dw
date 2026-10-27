# Correspondence criteria

Before any indicator value is seen, this document states, for each question, what the output must allow for the warehouse to answer that question. It does not state the answers. A question **corresponds** when its output meets every criterion able to fail, among them the one that states whether the comparison or description named by its objective can be made (section 2).

This document fixes the correspondence criteria. For each business question, they are statements about the observable shapes of the indicator output that let the determination named by the question's objective be made, with the rule that maps checks A5, A6 and A10 to a reading branch. Under [ADR-0011](../decisions/0011-preregister-correspondence-criteria-before-exposing-indicator-values.md), it is committed to `main` before any indicator value is exposed (rule 1), and its commit contains both reading branches (rule 4). The order is: this commit; then A5, A6 and A10; then the exposure and reading of the indicator output. The verdicts are reported in the [correspondence evidence document](../decisions/log/LOG-045-correspondence-evidence-document.md) ([LOG-045](../decisions/log/LOG-045-correspondence-evidence-document.md)).

## 0. Scope

* **"Does not correspond"** means that the output does not let the determination named by the question's objective be made, to the degree the objective claims it ([LOG-046](../decisions/log/LOG-046-user-of-the-outputs.md)). It is a statement about the output, not about respondents.
* **Test bench.** Every output, criterion and verdict is an output of a methodological test bench. None is a finding about any population ([ADR-0001](../decisions/0001-position-as-portfolio-project.md), Constraint).
* **H1 and the reading branches.** H1 ([ADR-0001](../decisions/0001-position-as-portfolio-project.md), Hypotheses) states that the file may join columns from two unrelated surveys. The columns fall into two groups ([LOG-040](../decisions/log/LOG-040-h1-column-groups.md)): the **OSMI group**, named for a match of column names with the OSMI 2014 schema (the name does not state where the columns come from), and the **other group**. A result that crosses the two groups is read under a **branch**:
  * "H1 holds": read as if the two column groups came from different people;
  * "H1 does not hold": read as if each row is one respondent.
  This document decides neither; checks A5, A6 and A10 do, by the rule in section 3.4. Where the rule does not decide, both branches are read (section 2).
* **What no verdict states.** No verdict:
  * is a finding about people or any population (Test bench);
  * states that the data are valid or reliable;
  * states that the file is, or is not, a single survey;
  * gives a direction (section 2, Reading note on direction);
  * covers anything beyond its question's objective ([LOG-046](../decisions/log/LOG-046-user-of-the-outputs.md)).
* **Two-reader test.** Before this commit, fresh readers with no other context applied the text to symbolic boundary cases, with no verdicts attached, and explained each verdict in their own words, so that two readers applying a criterion to the same output reach the same verdict ([ADR-0011](../decisions/0011-preregister-correspondence-criteria-before-exposing-indicator-values.md), rule 3). A frame test covered sections 0 to 5, the section 6 template, and the entries of Q4 and Q7.2; a final test covers the whole document.
  The readers' verdicts were compared with a key written by a party that co-drafted these criteria, so the test shows whether the text alone brings an outside reader to its authors' verdicts, not whether two readers without that intent agree. The cases of Q1 went to both readers, which gives one reader-to-reader comparison.
  Before round 1, the documentary verdict of Q2 and Q7.1 was removed under a stopping rule set in advance ([LOG-051](../decisions/log/LOG-051-stopping-rule-documentary-audit-readings.md)): its rule had been changed each time readings it left open were found, while the key was written, when it was reviewed, and by pre-test audit readings, and the last such reading still found one. The documentary layer gives no verdict.
  The key was withheld from the party that drafts fixes to the text, which did not write it, so that a fix could not encode the key's reading. On 2026-10-17, before either report existed and before the tested draft was frozen, key content reached that party twice: first, the questions whose verdict differs by reading branch and the documentary elements judged open to two readings; then, the statuses of four documentary elements and both documentary verdicts, under an earlier version of the documentary rule. The clarified rule and the quotes of the documentary elements of Q2 and Q7.1 were drafted afterwards by that party; that rule was later removed and the documentary layer was not part of the test ([LOG-051](../decisions/log/LOG-051-stopping-rule-documentary-audit-readings.md)), so the test says nothing about an effect on it. Drafting sessions opened later started without that content until both reports were saved and hashed.
  * Final test: one round, on 2026-10-26, with two fresh readers of the same model and settings, each in its own session with no tool and no search. Both readers gave the key's verdict, criterion status and cause loci for every one of their 46 cases (80 cases in all), and their verdicts on the twelve Q1 cases agree with each other. No divergence was found, the key was not fixed, and the text was not changed after the round. The declaration of the two relays (above) was added after the round and was not independently tested. Both readers are of the same model family as the models that drafted and checked the criteria: their agreement shows that the text leads to one verdict for readers of that family, not for every reader.
  * Dates of the changes line 23 lists:
    - clarified while the key was written (2026-10-17);
    - rewritten on one principle after the key review, which partly reversed that clarification (2026-10-19);
    - amended after the first and second pre-test audit readings (2026-10-23; 2026-10-23);
    - amended once more after the third, under the stopping rule (2026-10-25).
    One pre-test audit reading preceded the rewrite (2026-10-18). A reading by a model of another family was discarded, and none of its answers was used, because the document reached it truncated (2026-10-19).
  * Stopping rule ([LOG-051](../decisions/log/LOG-051-stopping-rule-documentary-audit-readings.md)): gaps found by each audit reading of the rewritten rule, with the item of the rule each arose in.
    - First reading: two, both in "Elements".
    - Second reading: two, both in step 1; one of them rested on a sentence a fix had added.
    - Third reading: three, none fix-induced (one in "Elements", two in step 1).
    - Fourth reading: one, in "Elements".
    The one fix after the third reading was stated on one principle, did not lengthen the rule and changed no checked rule case. The fourth reading still found a gap, so the outcome was counterproductive, and the documentary verdict was removed on 2026-10-25. The documentary layer gives no verdict and was not part of the test.
* **Amendments.** After its commit, this document is not rewritten. A later change is a dated amendment, on the terms of [ADR-0011, Constraint](../decisions/0011-preregister-correspondence-criteria-before-exposing-indicator-values.md#consequences) (section 7).

## 1. Declaration of prior knowledge

What was known when these criteria were fixed is declared by access ([LOG-049](../decisions/log/LOG-049-reading-rule-by-repository-access.md), item 2): everything in this repository at the parent of this document's commit counts as known. The declaration covers what was known to any party that drafted or checked these criteria. It includes the four items of [ADR-0011](../decisions/0011-preregister-correspondence-criteria-before-exposing-indicator-values.md), rule 2:

1. the marginal distributions published in [ADR-0001](../decisions/0001-position-as-portfolio-project.md), P8 (K1);
2. the counts of the derived conditions reported by check C10 (K3);
3. the cell structure of the indicators, that is, how many of the possible cells exist (K3);
4. knowledge of the data from having carried out the original project (listed under "Known from outside the repository").

Items 2 and 3 were published in the descriptions of pull requests #33 and #34, and no repository file records them (ADR-0011, K3). They are declared here as known from outside the repository.

Covered by access, and named because they bear on the criteria:

* The legacy report's reading of `mental_health_interview` as participation in an interview and as exposure to the mental-health system ([documentation-currency register](documentation-currency.md), DC-82), against the source's description, which Q7.2 uses.
* Values about the data readable in the dated captures of the dataset's pages ([LOG-011](../decisions/log/LOG-011-adr-0012-scope-of-capture-values.md)), declared by location only.
* The documentary layer of Q2 and Q7.1 (section 6) rests only on versioned text: the original questions, the legacy report's objectives, the current question and objective, and the versioned records cited beside them. It gives no verdict ([LOG-051](../decisions/log/LOG-051-stopping-rule-documentary-audit-readings.md)) and reads no indicator output.

Known from outside the repository:

* The descriptions of pull requests #33 and #34 (items 2 and 3).
* Copies of the legacy report, identical to the report at the tag `legacy-original` (same SHA-256), and of an unversioned continuation of it (140 pages; its SHA-256 and its comparison with the frozen report are in the [report-versions comparison](evidence/report-versions-comparison-2026-09-29.md)) were held outside both repositories while these criteria were drafted. Their content, including the original project's results, counts as known. The continuation is not cited (item 4).
* A suggestion on aggregating A5, made by a party that had read check A13's result, existed before section 3.4 was drafted.
* The results of the original project are known by access to the legacy repository: they are in the legacy report at the tag `legacy-original`, identified by its SHA-256 ([report-versions comparison](evidence/report-versions-comparison-2026-09-29.md), Inputs), and in the material listed under "Known from outside the repository". They were also available when the original questions were written (item 4).
* The legacy report at the tag `legacy-original` holds, in its text, figures of these categories: row counts of the source file (pp. 52, 61, 62, 110) and of the legacy fact table (pp. 64, 108, 115); the period range covered (pp. 8, 22, 26, 52, 63, 75, 108) and the number of countries covered (pp. 8, 17, 22, 26, 37, 63, 87, 88, 90); dimension cardinalities (pp. 33–42, 63, 76, 79, 81–92, 95, 99); and design and procedure constants (pp. 49, 56, 62, 66, 84, 111, 116, 124–127). It also holds 77 embedded images on 52 pages, not inspected for these criteria, whose content counts as known by access, including any result of the original project.
* An earlier, informal comparison with OSMI 2014 covered its schema only: column names and descriptions. In that comparison, no values, distributions or charts were seen.
* The `Gender` column of OSMI 2014 is free text.
* Language models were used in drafting and checking these criteria. Such models recall value categories of OSMI 2014 columns, among them the variants of `Gender` and the categories of `care_options`. That recall was not used to write section 3.5, whose rule is identity.
* Such models may also retain published analyses of OSMI 2014, including proportions, which cannot be enumerated.

Values added under [LOG-049](../decisions/log/LOG-049-reading-rule-by-repository-access.md), item 4 (displayed in breach of its item 3): none.

### 1.1 Positionality statement

This section declares where the gender cut came from, so that its influence can be judged. It states no finding, and no criterion depends on it.

* The gender cut of Q4 originates in a conviction, held when the questions were written, that seeking treatment for a mental-health condition carries stigma, more so among men.
* The legacy report at the tag `legacy-original` states the purpose, "identificar brechas en la búsqueda de ayuda profesional (especialmente diferencias de género)" (English: "identify gaps in professional help-seeking (especially gender differences)") (p. 5), and states no reason for it.
* Two sources of the [conceptual framework, section 3](../conceptual-framework.md#3-literature-basis-for-the-mechanism) report differences by gender. These are those studies' own findings, about their own samples, not about this file:
  * Clement et al. (2015): men are among the groups disproportionately deterred by stigma (p. 11), and stigma ranked lower as a barrier among studies that included only women (p. 17);
  * Andrade et al. (2014): women with disorders were more likely to recognize a need for treatment (p. 2), and low perceived need was more common among men (p. 7).
* The conviction's "more so among men" is consistent with Clement et al.'s finding (p. 11).
* The framework's text does not state these differences.
* The framework's synthesis reads stigma as "a real but modest and partial channel" ([conceptual framework, section 3](../conceptual-framework.md#3-literature-basis-for-the-mechanism), Synthesis).
* No criterion carries a direction by gender. A direction bears on no correspondence verdict (section 2, Reading note on direction).

## 2. Verdict scale

* **Criterion.** A statement about an observable shape of an indicator output, with the shape that meets it and the shape that does not. It is derived from the objective of its question, never from an expectation about the data; it carries no directional expectation (Reading note on direction, below); and it is specific enough that two readers applying it to the same output reach the same verdict ([ADR-0011](../decisions/0011-preregister-correspondence-criteria-before-exposing-indicator-values.md), rule 3). It is committed before any indicator value is exposed (rule 1).
* **Independence from results.** Every criterion rests on an argument that does not depend on any result ([ADR-0011](../decisions/0011-preregister-correspondence-criteria-before-exposing-indicator-values.md), rule 3).
* **Reading note on direction.** Where the conceptual framework supports a direction, the direction is stated in the question's entry as a reading note, with its source cited, and not as a criterion. It bears on no verdict. A direction is what the data show, and an output that comes out contrary to an expected direction still lets the comparison be made, so it does not touch "does not correspond" ([LOG-046](../decisions/log/LOG-046-user-of-the-outputs.md)). ADR-0011, rule 3, permits a directional expectation ("may appear") and does not require one.
* **Able or unable to fail.** Each criterion is marked as one or the other. A criterion is unable to fail when the shape that does not meet it cannot occur, for whatever reason; this includes a criterion whose meeting shape the specification or checks C8 and C9 guarantee ([LOG-046](../decisions/log/LOG-046-user-of-the-outputs.md)). It is reported and does not count toward "corresponds" (LOG-046); since it is met by construction, it changes no verdict. In plain terms: reported; never decides a verdict.
* **Determination criterion.** Each question has exactly one, marked as such, except as stated at the end of this item: the criterion that states whether the output lets the determination named by the question's objective be made, to the degree the objective claims it (LOG-046). It must be able to fail. A question for which no determination criterion able to fail can be stated receives no verdict, and the document states why.
* **Verdict on a criterion:** met or not met, under the branch applied (section 3), or with the branch marked not applicable where the question crosses no column groups ([LOG-040](../decisions/log/LOG-040-h1-column-groups.md) for the groups; [LOG-045](../decisions/log/LOG-045-correspondence-evidence-document.md) for the not-applicable case).
* **Verdict on a question**, from its criteria able to fail:
  * corresponds: every one is met;
  * partially corresponds: the determination criterion is met and at least one other is not;
  * does not correspond: the determination criterion is not met.

  | Verdict | Plain meaning | What it does not mean |
  |---|---|---|
  | corresponds | the output lets the determination named by the objective be made, and every other criterion able to fail is met | that the output shows a difference, its absence or a direction; that the data are valid; anything about people |
  | partially corresponds | the determination can be made, but at least one other criterion able to fail is not met | that the result is partly true |
  | does not correspond | the output does not let the determination be made; its cause is stated (section 4) | that the figures are wrong; anything about people |

* **Both branches.** Where a result is read under both branches without resolving between them (section 3; LOG-040 for `Occupation`; section 3.1 for `care_options`), each criterion and the question receive one verdict per branch. If the verdicts differ, both are reported and neither is chosen.
* **Citation.** Each verdict cites the criterion it applies and, where one exists, its dated amendment (ADR-0011, Constraint; section 7).

## 3. Reading branches

### 3.1 Column groups

* The two column groups are those of [LOG-040](../decisions/log/LOG-040-h1-column-groups.md): the OSMI group and the other group. A result crosses the groups when it involves at least one column of each ([`patterns.md`, Cross-column-group results](../specification/patterns.md#reporting-rules)). A result within one group is read the same way under both branches.
* `Occupation`: every result that involves it is read under both branches, without resolving between them (LOG-040). In A5, its pairs are computed and reported, and are left out of the aggregation of section 3.4.
* `care_options`: its placement in the OSMI group is a premise that A6 tests (LOG-040; [LOG-041](../decisions/log/LOG-041-a6-osmi-group.md)). The premise holds only if `care_options`' own A6 result is concordant on both units (section 3.4, Units and A6). Otherwise:
  * every indicator result that crosses `care_options` is read under both branches;
  * its A5 pairs are computed and reported, as `Occupation`'s are, and are left out of the aggregation.
  This rule is fixed before any result exists and changes no group membership, so the partition stays as LOG-040 freezes it.

### 3.2 Branch: H1 holds

* Under this branch, a result that crosses the two groups cross-tabulates columns from two unrelated sources. Any association or difference it shows is an artifact of how the sources were combined, not a relationship among respondents.
* A criterion whose determination needs such a relationship is not met under this branch, because the output does not let the determination be made ([LOG-046](../decisions/log/LOG-046-user-of-the-outputs.md)). Its locus is set in section 4.
* A criterion whose determination needs no such relationship is unaffected by the branch.

### 3.3 Branch: H1 does not hold

* A result that crosses the two groups is read as a cross-tabulation within respondents. Every other caveat that applies to it still applies:
  * the test-bench framing ([ADR-0001](../decisions/0001-position-as-portfolio-project.md));
  * the premises of the [conceptual framework, section 4](../conceptual-framework.md#4-variable-mapping-to-andersens-behavioral-model);
  * the reading of flagged cells (section 5);
  * the limitation on denominators (section 5, Limitation).
* "H1 does not hold" means that the mapping of section 3.4 did not establish the merge reading. It does not mean that a single source is shown.
* The checks are not symmetric:
  * A10's "confirms" is direct evidence of a second source; its "does not confirm" is not evidence of a single one.
  * A6's "concordant" places the OSMI group close to OSMI 2014, and says nothing on where the other group comes from.

For `Occupation` and `care_options`, see section 3.1.

### 3.4 Mapping of A5, A6 and A10 to a branch

Every element of this section rests on an argument that does not depend on any result of A5, A6 or A10. None exists before this document is committed ([ADR-0011](../decisions/0011-preregister-correspondence-criteria-before-exposing-indicator-values.md), rule 4; [LOG-049](../decisions/log/LOG-049-reading-rule-by-repository-access.md), item 3).

**Units (H2).**
* **Records unit.** The source rows after the cleaning and deduplication of staging ([ADR-0008](../decisions/0008-staging-deduplication-grain.md); [`staging.md`, Deduplication](../specification/staging.md#deduplication)), with all 17 source columns, read before the four unmodeled columns are discarded.
* **Profile unit.** The distinct profiles on the 16 columns other than `Timestamp` ([ADR-0001](../decisions/0001-position-as-portfolio-project.md), H2).
* A5 and A6 are computed on both units. When both give the same outcome, that is the check's outcome; when they differ, the outcome is indeterminate.
* `Timestamp` enters A5 and A6 at year and month (the grain of [`dim_time`](../specification/dimensions.md#dim_time)). It exists only in the records unit. Its A5 pairs and its A6 column are evaluated once, on the records unit, and enter the outcome of both units.
* A10's row tests use the distinct 8-column symptom profiles, which are the same from either unit, so the two-unit rule does not apply to them. A10's marginal comparisons are reported for both units and do not enter the mapping.
* Values are harmonized before any check runs, by [LOG-050](../decisions/log/LOG-050-a5-a6-a10-reading-thresholds.md), item 2. The list of equivalences for A6 is in section 3.5.
* Where two case forms of a value in the four unmodeled columns are equally frequent (LOG-050, item 2), the form that sorts first by Unicode code point is kept.

**A5: measure and thresholds.**
* **Measure.** A5 reports Cramér's V, with divisor min(r − 1, c − 1) (Cohen 1988, (7.2.6), p. 223; Bergsma 2013, p. 323).
* **Thresholds.** The thresholds are those of Cohen (1988), Table 7.2.3, p. 222, indexed by r − 1 of the smaller dimension (pp. 221, 223).
  * They are the φ' equivalents, by (7.2.6), of the conventions for w (pp. 224–225). This document reads them as thresholds for V, an interpretation ([writing conventions, rule 7](../writing-conventions.md#7-evidence-discipline)).
  * Beyond r − 1 = 5, the threshold is computed by (7.2.6), which Cohen states for any r not greater than k (p. 223).
* **Operative criterion.** "Below Small" is equivalent to √(χ²/n) < 0.10 for any table size (algebra on (7.2.6); interpretation).
* **Kim (2017).** Table 2 (p. 154) is a derived form of Table 7.2.3. Three discrepancies are declared:
  * its "Degree of freedom" is defined in its text as (r − 1)(c − 1) (p. 153), which equals Cohen's r − 1 only for a 2 × 2 table;
  * it cites Cohen pp. 79–80, which give the conventions for r, not for w;
  * its d = 5 Small cell is .04, against Cohen's .045 (rounding).
* **Limitation.** Cohen's own cautions apply: w varies with the smaller dimension of the table (p. 221); the conventions are arbitrary and "a general frame of reference" (pp. 12, 224); an investigator who thinks of association in terms of φ' "cannot use the operational definitions suggested above, or any other pegged to a constant w" (pp. 226–227).

**Interpretability ([LOG-050](../decisions/log/LOG-050-a5-a6-a10-reading-thresholds.md), item 1).**
* Each A5 pair carries the noise floor b = √(u/(n − 1)), with u = (r − 1)(c − 1) (Cohen (7.2.2), p. 221; Bergsma (1), p. 324). It is computed after this document is committed.
* A pair is interpretable only if b < 0.05, half of the Small threshold for w.
* An uninterpretable pair counts neither as structure nor as contradiction.

**A5: outcome within one unit.**
* The aggregation uses two kinds of pair:
  * **cross pairs:** one column of the OSMI group and one symptom column;
  * **within-OSMI pairs:** two columns of the OSMI group.
* The pairs of `Occupation`, and those of `care_options` when section 3.1 excludes them, are reported and left out of the aggregation. Pairs within the other group are reported and are not aggregated: H1 asks for structure inside the OSMI group only (ADR-0001, H1).
* The outcome is one of three, and exactly one applies:
  * **contradicts:** at least one interpretable cross pair is at or above Small;
  * **supports:** every cross pair is interpretable and below Small, and at least one interpretable within-OSMI pair is at or above Small;
  * **indeterminate:** every other case.

**A6.**
* **Scope.** The columns of the OSMI group (LOG-041), with `Timestamp` at year and month.
* **Measure.** Each column is compared with OSMI 2014 as two samples, in a 2 × k table of source by category. The measure is w_d = V/√(π(1 − π)), with π the share of OSMI 2014 in the table, that is, w_d² = Σᵢ (p₁ᵢ − p₂ᵢ)²/Pᵢ with Pᵢ the pooled share.
  * w_d does not depend on the ratio of the two sample sizes; the V of the same table shrinks with that ratio.
  * w_d is algebra on Cohen (7.2.1), p. 216, and the threshold Small = .10 applied to it is an extension. Both are interpretation.
  * The noise floor is b = √(u · (1/n₁ + 1/n₂)), with u = k − 1 (LOG-050, item 1), with the same bound as in A5.
* **Column result.**
  * concordant: interpretable and below Small;
  * discordant: interpretable and at or above Small;
  * indeterminate: uninterpretable.
* **Outcome within one unit.**
  * discordant, if at least one interpretable column is at or above Small;
  * concordant, if every interpretable column is below Small and at least one column is interpretable;
  * indeterminate, if no column is interpretable.
  Uninterpretable columns are named and reported.
* **Limitation.** With the sizes of the two samples, only a column of few categories can be interpretable ([LOG-050](../decisions/log/LOG-050-a5-a6-a10-reading-thresholds.md), item 1). A6's concordance therefore rests on the interpretable columns, which are by construction those of few categories and discriminate between sources less than `Country` or `Timestamp`. R3 also requires A5 to support H1, so A6 never decides the branch alone.
* **Not obtainable** when the OSMI 2014 data cannot be obtained (ADR-0011, rule 4).
* In the mapping rule of this section, "indeterminate" is read as "discordant".

**A10.**
* **Sets.** F is the set of distinct 8-column profiles of the file. R is the set of distinct profiles of RHMCD-20. Both are harmonized by LOG-050, item 2: trimmed and case-folded, with no list of equivalences.
  * Profiles with a null in any of the eight columns are left out of F, and their number is reported.
* **Observed.** c = |F ∩ R| / |F|. The near-exact share c₁ (within one column of a profile in R; [legacy audit](legacy-audit.md), A10) and the record-weighted shares are reported, and stay out of the rule.
* **Chance model.** The eight columns are drawn independently, each from the file's own marginal. Q is the probability that one draw falls in R, Q = Σ_{p∈R} Πⱼ fⱼ(pⱼ). The guard is G = Q^|F|, the probability that |F| independent draws all fall in R. Both are computed after this document is committed.
* **Outcome.**
  * **confirms:** c = 1 and G < α. α is the significance criterion of LOG-050, item 3: .05 (Cohen 1988, p. 12).
  * **does not confirm:** every other case in which RHMCD-20 is obtained.
  * **not obtainable:** the RHMCD-20 data cannot be obtained.
* **Limitation.** The chance model assumes that the eight columns are independent. If both sources share the usual correlation among symptoms, Q and G understate chance coincidence, and both bias A10 toward "confirms". The strict rule c = 1 is kept for that reason.

**Mapping rule.** The rules are applied in this order, and the first that applies decides the branch.

| Rule | Condition | Branch |
|---|---|---|
| R0 | A6 or A10 not obtainable | both, without resolving (ADR-0011, rule 4) |
| R1 | A10 confirms | H1 holds |
| R2 | A10 does not confirm, and A5 contradicts | H1 does not hold |
| R3 | A10 does not confirm, A5 supports, and A6 concordant | H1 holds |
| R4 | A10 does not confirm, A5 supports, and A6 discordant | both, without resolving |
| R5 | A10 does not confirm, and A5 indeterminate | both, without resolving |

* **Grounds of R1.** Full containment of the file's symptom profiles in RHMCD-20, beyond the chance guard, would be direct evidence, if it occurs, of the second source that H1 hypothesizes ([ADR-0001](../decisions/0001-position-as-portfolio-project.md), H3). An association across the groups is then explained by how the sources were combined, so R1 precedes A5.
* The branch set by this rule applies to every result that crosses the groups, except those that section 3.1 reads under both branches (`Occupation`; `care_options` where its premise does not hold). These are read under both branches, whatever the rule gives.

### 3.5 List of equivalences for A6

* The closed list of [LOG-050](../decisions/log/LOG-050-a5-a6-a10-reading-thresholds.md), item 2, is identity: a value of OSMI 2014, after trimming and case-folding, is equivalent to a domain label of the file ([`sources.md`, Value domains](../specification/sources.md#value-domains)) only when it equals that label after the same trimming and case-folding. Every other value goes to the single "unmatched" category, reported with its count and its values.
* **Declared bias.** A value that another list would have mapped to a label goes to "unmatched", where the file has no counterpart. The rule therefore biases A6 toward "discordant", which, where R3 or R4 is reached, leads to R4 (both branches), and the premise of `care_options` toward not holding (section 3.1). Both are the conservative side.

## 4. Locus of a mismatch

The locus says where a criterion that is not met fails. It is descriptive: it changes no verdict (section 2). Each "not met" verdict names every locus set by a rule that causes it, each locus once:

* **Provenance.** A "not met" under "H1 holds" that section 3.2 causes: the criterion crosses the groups, and its determination needs a relationship among respondents. Plain cause: "under the reading that the file joins two sources, this cross says nothing about respondents".
* **Data volume.** A "not met" that section 5, item 3, causes (a comparison the criterion requires involves a cell flagged by `low_n`), or that a cell missing where the entry requires it causes (within an existing stratum, for an entry that defines strata). A stratum that does not exist is not a missing cell. Plain cause: "too few responses, or none, in a cell to read the comparison".
* **Reasoning or design.** A "not met" that neither causes. Plain cause: "the question or its indicator does not let the determination be made".

Each "does not correspond" is reported with the plain cause of every locus of its determination criterion.

Where both branches apply, each verdict carries its own loci.

## 5. Reading of cells flagged by `low_n`

1. The flag, its threshold and its caveat are those of [`patterns.md`, Reporting rules](../specification/patterns.md#reporting-rules). The criteria are read with the threshold's default value; a change of the threshold after any indicator value is exposed is an amendment (section 7).
2. Each criterion names the cells its shape is read from (section 6).
3. Under the low-count caveat ([`patterns.md`, Reporting rules](../specification/patterns.md#reporting-rules)), a comparison that involves a flagged cell is not read as showing a difference or its absence. A criterion whose shape requires such a comparison is not met, because the output does not let that comparison be made ([LOG-046](../decisions/log/LOG-046-user-of-the-outputs.md)).
4. A criterion whose shape is read only from unflagged cells is read from them.
5. A level that occurs in no row of a cell has numerator 0 there, and a level that occurs in no row of the population has no row in any cell ([`patterns.md`, pattern A](../specification/patterns.md#pattern-a--level-distribution)); the criteria read its rate or share as 0, and neither is a missing cell.
6. Flagged cells are shown, marked, and never omitted from the evidence document ([LOG-045](../decisions/log/LOG-045-correspondence-evidence-document.md)); their display in the reporting layer stays with [LOG-003](../decisions/log/LOG-003-minimum-count-addendum.md).
7. **Limitation.** Denominators count staged records, and only exact duplicates on all 17 source columns are removed ([`staging.md`, Deduplication](../specification/staging.md#deduplication)). Rows that check A4 groups as replicated profiles (H2; [legacy audit](legacy-audit.md)) are therefore counted separately, so the flag does not reflect replication: a cell above the threshold may rest on fewer distinct profiles than its denominator. This rule does not correct for it, because the indicator output does not carry distinct-profile counts. The verdicts read under this rule carry this limitation.

## 6. Criteria per question

Each entry is read together with sections 2 to 5, not alone: it applies them and does not restate them. Q4 and Q7.2 come first, as the entries of the frame test (section 0). Each entry states:

* **Question and objective**, by link, with each premise cited at its first use.
* **Outputs and cells:** the indicators, and the cells the criteria read (section 5). An entry adds the population, levels or grain its criteria read, where the outputs leave them open.
* **Documentary layer:** the original question and the legacy purpose, as the original purpose ([LOG-046](../decisions/log/LOG-046-user-of-the-outputs.md), option a). For Q2 and Q7.1, the entry sets them beside the current question and objective, element by element, with the records on each element's columns, and gives no verdict (Documentary layer, below).
* **Criteria:** for each, the shape that meets it and the shape that does not; its ground; whether it is able to fail; which is the determination criterion (section 2); whether it crosses the groups (section 3.1); and whether its determination needs a relationship among respondents (section 3.2); then its criteria unable to fail (section 2).
* **Reading list**, where the entry defines strata: beside the verdict, each stratum is listed as readable or not readable, in the order the entry states. Readable records presence and flags only, and the list is the same under every branch: provenance is reported by the verdict, not by the list. The list changes no verdict and is not a "partially corresponds".
* **What "corresponds" means here:** what the verdict states and does not state, with the loci through which each criterion able to fail can fail under "H1 does not hold" (section 4). An entry with one criterion able to fail is "corresponds" or "does not correspond".
* **Branches:** the reading under each branch; where both branches apply, a two-row table of branch, verdict and plain cause (section 4), after the reading under each branch (section 3).
* **Reading note on direction**, with its source, or "none" (section 2).
* **Premises** involved.
* **In plain terms**, last: what each possible verdict means for the question and what it does not mean. Plain wording states neither less nor more than the criteria, and uses no name that [writing conventions, rule 5](../writing-conventions.md#5-names-claim-only-what-the-data-supports) excludes.

With the source file fixed, the cell structure is known (section 1, item 3). The required cells of each entry follow from the question and its objective, not from that structure.

**Documentary layer** (Q2 and Q7.1 only; [LOG-016](../decisions/log/LOG-016-objectives-q2-q6-q71-q72.md); [LOG-051](../decisions/log/LOG-051-stopping-rule-documentary-audit-readings.md)). It sets the original question and the objective the legacy report states for it beside the current question and objective, element by element, with the versioned records on each element's columns. It gives no status and no verdict, and reads no indicator output.

* Reference: the original question ([ADR-0004](../decisions/0004-revise-business-questions.md), "originally") and the legacy objective (legacy report, pp. 6–7). Other passages of the legacy report are cited as context, not split into elements.
* Elements: the entry splits the reference into the determinations it names: what is measured, among whom, which relationship, which breakdown, and which reading over time. An element is the smallest part of the reference that states a determination on its own, so that the records on its columns can be set beside it:
  * A quantity (a share, a count) belongs to the element that states what it measures, and is never an element of its own, since a quantity determines nothing apart from what it measures. A comparison (a difference, a gap, "versus …"), between groups or between two things measured, is the relationship it determines, an element of its own, since stating each thing compared does not state the comparison.
  * Conditions on who is counted that each restrict the population, joined by "and" or stated one after another, are separate elements; alternatives joined by "or" form one element, since neither alone states who is counted.
  * An element may quote, beside its own words, words of another element that it measures within, relates or qualifies, so that its quote reads in context; it adds its own determination to them, and rests on every column its quote names (Records, below). Parts of the reference that state the same kind of determination on the same content, in one passage or in two, are one element, which quotes each of them. The entry marks the words an element quotes for context, with the element they belong to; every other word of its quote is its own, whatever it states.
  How a column is coded is not an element.
* The end uses the legacy report names (p. 5) are not elements: no question of this repository can serve them ([ADR-0001](../decisions/0001-position-as-portfolio-project.md); [LOG-046](../decisions/log/LOG-046-user-of-the-outputs.md), Reasons, (a)).
* Records: an element rests on a column when its quote names the column or one of its levels, by code or in words, or refers back to words that do. Beside each element, the entry lists those columns and the versioned records (a decision record with its addenda, or a decision-log entry) that state or change what a level of any of them is read to mean, since only such records revise a reading.
* Current text: after the elements, the entry quotes once the current question ([indicators](../specification/indicators.md)) and the current objective ([ADR-0004](../decisions/0004-revise-business-questions.md), with its addenda).

### Q4

* **Question and objective.** The question is in [`indicators.md`, Q4](../specification/indicators.md#q4--indicators-7-8). Its objective is "compare lifetime treatment-seeking against explicit stress recognition, by gender" ([ADR-0004, Q4](../decisions/0004-revise-business-questions.md#q4--originally)). "Explicit stress recognition" is a premise: `growing_stress = 'Yes'` is read as explicit recognition ([`definitions.md`, `explicit_recognition`](../specification/definitions.md#explicit_recognition)).
* **Outputs and cells.** Indicator 7 (the rate, at both levels of `treatment`) and indicator 8 (the count of the `Yes` level), by `gender` × `growing_stress`: six cells, the two `Gender` labels, `Male` and `Female`, by the three `Growing_Stress` labels ([`sources.md`, Value domains](../specification/sources.md#value-domains)).
* **Three levels.** The criteria read all three levels of `growing_stress`, not `Yes` against the rest, because the question asks for "all three levels" (`indicators.md`, Q4).
* **Documentary layer.** The original question ([ADR-0004, Q4](../decisions/0004-revise-business-questions.md#q4--originally), as originally written) and the legacy purpose (section 1.1). No documentary elements ([LOG-016](../decisions/log/LOG-016-objectives-q2-q6-q71-q72.md)).
* **Criteria.**
  * **C1. Every required cell present and unflagged.** Able to fail; the determination criterion, and the only criterion able to fail.
    * Cells read: indicator 7's `Yes` rate, in the six cells.
    * Meets: all six cells are present, and none is flagged by `low_n`. The three levels can then be compared within each gender, and the pattern compared between genders.
    * Does not meet: a required cell is missing, or flagged (section 5, item 3). Cause: data volume (section 4).
    * Ground: the objective compares lifetime treatment-seeking against explicit stress recognition by gender ([ADR-0004, Q4](../decisions/0004-revise-business-questions.md#q4--originally)), and the question asks for all three levels of `Growing_Stress` (`indicators.md`, Q4); the comparison needs the `Yes` rate at every level within each gender, so all six cells are required.
    * Crosses the groups (`gender` and `treatment` in the OSMI group, `growing_stress` in the other; [LOG-040](../decisions/log/LOG-040-h1-column-groups.md)). Its determination needs a relationship among respondents.
  * Unable to fail (section 2): the two levels' rates sum to 1 by pattern C and check C8; indicator 8 equals indicator 7's `Yes` numerator (`indicators.md`, Q4; check C9).
* **What "corresponds" means here.** "Corresponds" means only that the comparison the objective names can be read from the output, not what the comparison shows. Under "H1 does not hold", C1 fails only through data volume (section 4).
* **Branches.**
  * H1 holds: C1 is not met (section 3.2), with the locus provenance (section 4).
  * H1 does not hold: C1 is read as stated (section 3.3).
  * Q4 involves neither `Occupation` nor `care_options` (section 3.1).
  * Where the mapping of section 3.4 applies both branches, Q4 receives one verdict per branch (section 2):

    | Branch | Verdict | Cause |
    |---|---|---|
    | H1 holds | does not correspond | under the reading that the file joins two sources, this cross says nothing about respondents; and, where a required cell is missing or flagged, also too few responses, or none, in a cell to read the comparison |
    | H1 does not hold | corresponds if every required cell is present and unflagged; otherwise does not correspond | where it does not correspond: too few responses, or none, in a cell to read the comparison |

* **Reading note on direction** (section 2).
  * By `growing_stress`: the conceptual framework supports a direction between perceived need and care-seeking ([conceptual framework, section 3](../conceptual-framework.md#3-literature-basis-for-the-mechanism)). It does not transfer here: treatment is lifetime ([conceptual framework, section 4](../conceptual-framework.md#4-variable-mapping-to-andersens-behavioral-model)), the data hold no sequence ([conceptual framework, section 5](../conceptual-framework.md#5-what-this-dataset-cannot-measure)), and `Growing_Stress` is read as perceived need by assumption (section 4 of the framework). No direction is stated.
  * By gender: none (section 1.1).
* **Premises.**
  * Explicit recognition (Question and objective).
  * `Maybe` is reported as its own level ([multi-level self-report rule](../specification/definitions.md#multi-level-self-report-rule)).
  * The limitation on denominators (section 5, Limitation).
* **In plain terms.**
  * "Corresponds": within each gender, and between the two genders, the share that reports lifetime treatment-seeking can be compared across the three answers to `Growing_Stress`. It does not mean that the shares differ, or that they do not, nor anything listed in section 0, What no verdict states.
  * "Does not correspond": the cause is stated with the verdict, as one or both of: "under the reading that the file joins two sources, this cross says nothing about respondents"; "too few responses, or none, in a cell to read the comparison". It does not mean that the figures are wrong.

### Q7.2

* **Question and objective.** The question is in [`indicators.md`, Q7.2](../specification/indicators.md#q72--indicator-16). Its objective is “describe the proportion who do not report lifetime treatment-seeking among respondents with explicit stress recognition, a convergent symptom profile, or both, who report "Yes" or "Not sure" for care options, by stated willingness to disclose a mental health issue to a potential employer, without asserting persistence over time or postponement, since no time-to-treatment variable exists in the data” ([ADR-0004, Addendum (2026-10-04)](../decisions/0004-revise-business-questions.md#addendum-2026-10-04)). Its terms rest on premises and interpretations:
  * explicit stress recognition: `growing_stress = 'Yes'` read as explicit recognition ([`definitions.md`, `explicit_recognition`](../specification/definitions.md#explicit_recognition));
  * a convergent symptom profile: `symptom_cluster`, with its [validity caveat](../specification/definitions.md#symptom_cluster);
  * care options: the `care_options` response, in neutral wording ([LOG-013](../decisions/log/LOG-013-care-options-neutral-wording.md)), placed in the OSMI group as a premise (section 3.1);
  * stated willingness to disclose: `mental_health_interview` read as disclosure willingness, an interpretation of the source's question text ([conceptual framework, section 4](../conceptual-framework.md#4-variable-mapping-to-andersens-behavioral-model)).
* **Outputs and cells.** Indicator 16, pattern C, on the population `(explicit_recognition OR symptom_cluster) AND care_options IN ('Yes','Not sure')`, by `growing_stress` (3 levels) × `symptom_cluster` × `care_options` (`Yes`, `Not sure`) × `mental_health_interview` (3 levels): up to 24 cells (`indicators.md`, Q7.2).
  * A **stratum** is one combination of `growing_stress`, `symptom_cluster` and `care_options` that the population admits: up to eight. Each stratum holds three cells, one per level of `mental_health_interview`. A stratum exists when the output reports at least one of its cells.
  * The quantity of interest is the `No` level of `treatment` (`indicators.md`, Q7.2).
  * The **headline stratum** is that of the headline cell: `growing_stress = 'Yes'`, `symptom_cluster` true, `care_options = 'Yes'` (`indicators.md`, Q7.2; [`patterns.md`, Output columns](../specification/patterns.md#output-columns)).
* **Grain.** The criteria read cell by cell, within each stratum. No sum across strata is formed: it would merge `Not sure` with `Yes` and the levels of `growing_stress`, which the [multi-level self-report rule](../specification/definitions.md#multi-level-self-report-rule) and [ADR-0006](../decisions/0006-final-questions-and-indicators.md) keep apart.
* **Documentary layer.** The original question ([ADR-0004, Q7.2](../decisions/0004-revise-business-questions.md#q72--originally), as originally written) and the legacy purpose (section 1.1). No documentary elements ([LOG-016](../decisions/log/LOG-016-objectives-q2-q6-q71-q72.md)).
* **Criteria.**
  * **C1. Every required cell present and unflagged.** Able to fail; the determination criterion, and the only criterion able to fail.
    * Cells read: indicator 16's `No` rate, in the three `mental_health_interview` cells of every stratum that exists.
    * Meets: in every stratum that exists, the three cells are present, and none is flagged by `low_n`. The `No` rate can then be compared across the three levels of `mental_health_interview` within every stratum.
    * Does not meet: in at least one stratum that exists, a cell is missing, or flagged (section 5, item 3). Cause: data volume (section 4).
    * Ground: the objective names the whole population, so every stratum that exists is required ([LOG-046](../decisions/log/LOG-046-user-of-the-outputs.md)).
    * Crosses the groups (`treatment`, `care_options` and `mental_health_interview` in the OSMI group; `growing_stress` and the columns of `symptom_cluster` in the other; [LOG-040](../decisions/log/LOG-040-h1-column-groups.md)). Its determination needs a relationship among respondents.
  * Unable to fail (section 2): the two levels' rates sum to 1 by pattern C and check C8; indicator 16, summed over `mental_health_interview`, equals indicator 15 cell by cell by check C9 ([`patterns.md`, Cross-indicator consistency](../specification/patterns.md#cross-indicator-consistency)).
* **Reading list.** Beside the verdict, each stratum that exists is listed as readable (its three cells present and unflagged) or not readable. The headline stratum comes first; the others follow by `growing_stress` (`Yes`, `Maybe`, `No`), then `symptom_cluster` (true, false), then `care_options` (`Yes`, `Not sure`). Admitted strata that do not exist are listed last, as absent.
* **What "corresponds" means here.** "Corresponds" means only that the comparison by `mental_health_interview` can be read in every stratum that exists, not what it shows. Under "H1 does not hold", C1 fails only through data volume (section 4).
* **Branches.**
  * H1 holds: C1 is not met (section 3.2), with the locus provenance (section 4).
  * H1 does not hold: C1 is read as stated (section 3.3).
  * `care_options`: every result of Q7.2 crosses `care_options`, as a cut and in the population. Where its premise does not hold (section 3.1), every result of Q7.2 is read under both branches.
  * Q7.2 involves no `Occupation` (section 3.1).
  * Where both branches apply, Q7.2 receives one verdict per branch (section 2):

    | Branch | Verdict | Cause |
    |---|---|---|
    | H1 holds | does not correspond | under the reading that the file joins two sources, this cross says nothing about respondents; and, where a required cell is missing or flagged, also too few responses, or none, in a cell to read the comparison |
    | H1 does not hold | corresponds if every required cell is present and unflagged; otherwise does not correspond | where it does not correspond: too few responses, or none, in a cell to read the comparison |

* **Reading note on direction** (section 2).
  * By `mental_health_interview`: the conceptual framework supports a direction between disclosure concerns and help-seeking: disclosure concerns were the most commonly reported stigma barrier ([conceptual framework, section 3](../conceptual-framework.md#3-literature-basis-for-the-mechanism), Clement et al. 2015). It does not transfer here: treatment is lifetime ([conceptual framework, section 4](../conceptual-framework.md#4-variable-mapping-to-andersens-behavioral-model)), the data hold no sequence ([conceptual framework, section 5](../conceptual-framework.md#5-what-this-dataset-cannot-measure)), and `mental_health_interview` is read as disclosure willingness by interpretation (section 4 of the framework). No direction is stated.
  * By `growing_stress`: as in Q4.
* **Premises.**
  * The four premises and interpretations of Question and objective.
  * `Maybe` and `Not sure` are reported as their own levels ([multi-level self-report rule](../specification/definitions.md#multi-level-self-report-rule)).
  * The limitation on denominators (section 5, Limitation).
* **In plain terms.**
  * "Corresponds": in every group of respondents that the output forms (by answer to `Growing_Stress`, by presence of the symptom profile, and by answer to `care_options`), the share that reports no lifetime treatment-seeking can be compared across the three answers on disclosure to a potential employer. It does not mean that the shares differ, or that they do not. It gives no single figure for all respondents. It says nothing about time between stress and treatment, since the data hold none, nor anything listed in section 0, What no verdict states.
  * "Does not correspond": the cause is stated with the verdict, as one or both of: "under the reading that the file joins two sources, this cross says nothing about respondents"; "too few responses, or none, in a cell to read the comparison". It does not mean that the figures are wrong.
  * The reading list says which groups have their three cells present and unflagged. It changes no verdict.

### Q1

* **Question and objective.** The question is in [`indicators.md`, Q1](../specification/indicators.md#q1--indicators-1-2). Its objective is "compare explicit stress recognition across genders and across the surveyed period — not to trace change within a followed population, since the dataset has no panel structure" ([ADR-0004, Q1](../decisions/0004-revise-business-questions.md#q1--originally)). "Explicit stress recognition" is a premise: `growing_stress = 'Yes'` is read as explicit recognition ([`definitions.md`, `explicit_recognition`](../specification/definitions.md#explicit_recognition)).
* **Outputs and cells.** Indicator 1 (the count of each level of `growing_stress`, with no cut) and indicator 2 (the rate of each level, pattern A, by `period` × `gender`). A `period` is the (`year`, `month`) pair of `dim_time` ([`definitions.md`, Period](../specification/definitions.md#query-vocabulary)). A cell of indicator 2 is one (`period`, `gender`) combination that occurs in the population ([`definitions.md`, Cell](../specification/definitions.md#query-vocabulary)). Strata and required cells: C1.
* **Three levels.** The criteria read the three level rates of each cell, not `Yes` against the rest, because the question asks for "all three levels" (`indicators.md`, Q1).
* **Documentary layer.** The original question ([ADR-0004, Q1](../decisions/0004-revise-business-questions.md#q1--originally), as originally written) and the legacy purpose (section 1.1). No documentary elements ([LOG-016](../decisions/log/LOG-016-objectives-q2-q6-q71-q72.md)).
* **Criteria.**
  * **C1. At least two strata, and every required cell present and unflagged.** Able to fail; the determination criterion, and the only criterion able to fail.
    * Strata: the periods. A stratum exists when the output reports at least one of its cells. A period with no rows is not a stratum, and its absence is not a missing cell (section 4).
    * Required cells: at least two strata exist; in every stratum, the two `Gender` cells, `Male` and `Female` ([`sources.md`, Value domains](../specification/sources.md#value-domains)).
    * Cells read: indicator 2's three level rates in each required cell.
    * Meets: at least two strata exist, and in every stratum both cells are present and neither is flagged by `low_n`. The three levels can then be compared across periods within each gender, and between the genders within each period.
    * Does not meet: in at least one stratum, a required cell is missing or flagged (section 5, item 3); cause: data volume (section 4). Or fewer than two strata exist, so no comparison across periods can be made; cause: reasoning or design (section 4).
    * Ground: the objective names the whole surveyed period, so every stratum that exists is required ([LOG-046](../decisions/log/LOG-046-user-of-the-outputs.md)).
    * Crosses the groups (`period`, from `Timestamp`, and `gender` in the OSMI group, `growing_stress` in the other; [LOG-040](../decisions/log/LOG-040-h1-column-groups.md)). Its determination needs a relationship among respondents.
  * Unable to fail (section 2): indicator 1 equals indicator 2's numerators summed per level ([`patterns.md`, Cross-indicator consistency](../specification/patterns.md#cross-indicator-consistency); check C9); within each cell the level numerators sum to the denominator, so the level rates sum to 1 (pattern A; check C8).
* **Reading list.** Beside the verdict, each stratum is listed in period order as readable (both cells present and unflagged) or not readable.
* **What "corresponds" means here.** "Corresponds" means only that the comparisons the objective names can be read from the output, not what they show. Under "H1 does not hold", C1 fails through data volume or, where fewer than two strata exist, through reasoning or design (section 4).
* **Branches.**
  * H1 holds: C1 is not met (section 3.2), with the locus provenance (section 4).
  * H1 does not hold: C1 is read as stated (section 3.3).
  * Q1 involves neither `Occupation` nor `care_options` (section 3.1).
  * Where the mapping of section 3.4 applies both branches, Q1 receives one verdict per branch (section 2):

    | Branch | Verdict | Cause |
    |---|---|---|
    | H1 holds | does not correspond | under the reading that the file joins two sources, this cross says nothing about respondents; and, where a required cell is missing or flagged, also too few responses, or none, in a cell to read the comparison; and, where fewer than two strata exist, also the question or its indicator does not let the determination be made |
    | H1 does not hold | corresponds if at least two strata exist and every required cell is present and unflagged; otherwise does not correspond | where it does not correspond: too few responses, or none, in a cell to read the comparison; or, where fewer than two strata exist, the question or its indicator does not let the determination be made |

* **Reading note on direction** (section 2).
  * By period: none. The data hold one timestamp per respondent, with no panel structure ([conceptual framework, section 5](../conceptual-framework.md#5-what-this-dataset-cannot-measure)), and no temporal claim is possible from them ([conceptual framework, section 7](../conceptual-framework.md#7-threats-to-validity)).
  * By gender: none (section 1.1).
* **Premises.**
  * Explicit recognition (Question and objective).
  * `Maybe` is reported as its own level ([multi-level self-report rule](../specification/definitions.md#multi-level-self-report-rule)).
  * The limitation on denominators (section 5, Limitation).
  * Each period holds different respondents, not a followed population ([ADR-0004, Q1](../decisions/0004-revise-business-questions.md#q1--originally)).
* **In plain terms.**
  * "Corresponds": within each gender, the share of respondents giving each of the three answers to `Growing_Stress` can be compared across the months in the data, and, within each month, between the two genders. It does not mean that the shares change or stay the same, nor that any change happened in the same people, since each month holds different respondents; nor anything listed in section 0, What no verdict states.
  * "Does not correspond": the cause is stated with the verdict, as one or more of: "under the reading that the file joins two sources, this cross says nothing about respondents"; "too few responses, or none, in a cell to read the comparison"; "the question or its indicator does not let the determination be made". It does not mean that the figures are wrong.
  * The reading list says which months have both cells present and unflagged. It changes no verdict.

### Q2

* **Question and objective.** The question is in [`indicators.md`, Q2](../specification/indicators.md#q2--indicators-3-4). Its objective is "describe how explicit stress recognition differs by gender and across the surveyed period within the subpopulation reporting a family history; no comparison group without family history, so it does not describe a relationship between family history and recognition" ([ADR-0004, addendum of 2026-10-04, Q2](../decisions/0004-revise-business-questions.md#addendum-2026-10-04)). "Explicit stress recognition" is a premise: `growing_stress = 'Yes'` is read as explicit recognition ([`definitions.md`, `explicit_recognition`](../specification/definitions.md#explicit_recognition)).
* **Outputs and cells.** Indicator 3 (the count of each level of `growing_stress`, with no cut) and indicator 4 (the rate of each level, pattern A, by `gender` × `period`), on the rows where `family_history = 'Yes'` (`indicators.md`, Q2). A `period` is the (`year`, `month`) pair of `dim_time` ([`definitions.md`, Period](../specification/definitions.md#query-vocabulary)). A cell of indicator 4 is one (`period`, `gender`) combination that occurs in the population ([`definitions.md`, Cell](../specification/definitions.md#query-vocabulary)). Strata and required cells: C1.
* **Population.** The respondents who report a family history of mental illness (`family_history = 'Yes'`, a source-described column; [conceptual framework, section 4](../conceptual-framework.md#4-variable-mapping-to-andersens-behavioral-model)). The population has no comparison group without family history.
* **Three levels.** The criteria read the three level rates of each cell, not `Yes` against the rest, because the question asks for "all three levels" (`indicators.md`, Q2).
* **Documentary layer.** The original question ([ADR-0004, Q2](../decisions/0004-revise-business-questions.md#q2--originally), as originally written) and the legacy purpose (section 1.1). The legacy objective is "Examinar la relación entre la predisposición familiar y la evolución del estrés, considerando posibles diferencias de tendencia entre géneros." (English: "Examine the relationship between family predisposition and the evolution of stress, considering possible differences in trend between genders.") (legacy report, p. 6). The elements (section 6, Documentary layer):
  * E1. A relationship between family history and stress: "la relación entre la predisposición familiar y la evolución del estrés" (English: "the relationship between family predisposition and the evolution of stress") (objective). Quoted for context: "la evolución del estrés" (E2). Rests on: `family_history`, `Growing_Stress`. Records: [LOG-012](../decisions/log/LOG-012-explicit-recognition-premise.md).
  * E2. A reading of stress over time: "la evolución del estrés" (English: "the evolution of stress") (objective); "a lo largo del tiempo" (English: "over time") (question). Rests on: `Growing_Stress`, `Timestamp`. Records: [LOG-012](../decisions/log/LOG-012-explicit-recognition-premise.md).
  * E3. Differences between genders: "diferencias de tendencia entre géneros" (English: "differences in trend between genders") (objective); "según el género (Gender)" (English: "by gender (Gender)") (question). Rests on: `Gender`. Records: none.
  * E4. Among people with a family history: "personas con historial familiar de problemas de salud mental (family_history = Yes)" (English: "people with a family history of mental health problems (family_history = Yes)") (question). Rests on: `family_history`. Records: none.
  * E5. The proportion who present growing stress: "Qué porcentaje de personas con historial familiar […] presenta estrés creciente (Growing_Stress = Yes)" (English: "What percentage of people with a family history […] present growing stress (Growing_Stress = Yes)") (question). Quoted for context: "personas con historial familiar" (E4). Rests on: `family_history`, `Growing_Stress`. Records: [LOG-012](../decisions/log/LOG-012-explicit-recognition-premise.md).
  * Current question: "Among respondents with a family history of mental illness (`family_history = 'Yes'`), how does explicit stress recognition (`Growing_Stress`, all three levels) differ by gender and across the months represented in the dataset?" ([indicators](../specification/indicators.md)). Current objective: "describe how explicit stress recognition differs by gender and across the surveyed period within the subpopulation reporting a family history; no comparison group without family history, so it does not describe a relationship between family history and recognition" ([ADR-0004](../decisions/0004-revise-business-questions.md), set by [LOG-016](../decisions/log/LOG-016-objectives-q2-q6-q71-q72.md)).
  * Context: legacy report, p. 84.
* **Criteria.**
  * **C1. At least two strata, and every required cell present and unflagged.** Able to fail; the determination criterion, and the only criterion able to fail.
    * Strata: the periods. A stratum exists when the output reports at least one of its cells. A period with no rows in the population is not a stratum, and its absence is not a missing cell (section 4).
    * Required cells: at least two strata exist; in every stratum, the two `Gender` cells, `Male` and `Female` ([`sources.md`, Value domains](../specification/sources.md#value-domains)).
    * Cells read: indicator 4's three level rates in each required cell.
    * Meets: at least two strata exist, and in every stratum both cells are present and neither is flagged by `low_n`. The three levels can then be compared across periods within each gender, and between the genders within each period.
    * Does not meet: in at least one stratum, a required cell is missing or flagged (section 5, item 3); cause: data volume (section 4). Or fewer than two strata exist, so no comparison across periods can be made; cause: reasoning or design (section 4).
    * Ground: the objective names gender and the whole surveyed period ([ADR-0004, addendum of 2026-10-04, Q2](../decisions/0004-revise-business-questions.md#addendum-2026-10-04)), so every stratum that exists is required ([LOG-046](../decisions/log/LOG-046-user-of-the-outputs.md)).
    * Crosses the groups (`family_history`, `period`, from `Timestamp`, and `gender` in the OSMI group; `growing_stress` in the other; [LOG-040](../decisions/log/LOG-040-h1-column-groups.md)). Its determination needs a relationship among respondents.
  * Unable to fail (section 2): indicator 3 equals indicator 4's numerators summed per level ([`patterns.md`, Cross-indicator consistency](../specification/patterns.md#cross-indicator-consistency); check C9); within each cell the level numerators sum to the denominator (pattern A; check C8).
* **Reading list.** Beside the verdict, each stratum is listed in period order as readable (both cells present and unflagged) or not readable.
* **What "corresponds" means here.** "Corresponds" means only that the comparisons the objective names can be read from the output, not what they show. Under "H1 does not hold", C1 fails through data volume or, where fewer than two strata exist, through reasoning or design (section 4).
* **Branches.**
  * H1 holds: C1 is not met (section 3.2), with the locus provenance (section 4).
  * H1 does not hold: C1 is read as stated (section 3.3).
  * Q2 involves neither `Occupation` nor `care_options` (section 3.1).
  * Where the mapping of section 3.4 applies both branches, Q2 receives one verdict per branch (section 2):

    | Branch | Verdict | Cause |
    |---|---|---|
    | H1 holds | does not correspond | under the reading that the file joins two sources, this cross says nothing about respondents; and, where a required cell is missing or flagged, also too few responses, or none, in a cell to read the comparison; and, where fewer than two strata exist, also the question or its indicator does not let the determination be made |
    | H1 does not hold | corresponds if at least two strata exist and every required cell is present and unflagged; otherwise does not correspond | where it does not correspond: too few responses, or none, in a cell to read the comparison; or, where fewer than two strata exist, the question or its indicator does not let the determination be made |

* **Reading note on direction** (section 2).
  * By period and by gender: as in Q1.
  * By family history: not applicable. The population holds no respondents without a family history, and the objective states that Q2 "does not describe a relationship between family history and recognition" ([ADR-0004, addendum of 2026-10-04, Q2](../decisions/0004-revise-business-questions.md#addendum-2026-10-04)).
* **Premises.**
  * Explicit recognition (Question and objective).
  * `Maybe` is reported as its own level ([multi-level self-report rule](../specification/definitions.md#multi-level-self-report-rule)).
  * The limitation on denominators (section 5, Limitation).
  * Each period holds different respondents, not a followed population ([ADR-0004, Q2](../decisions/0004-revise-business-questions.md#q2--originally)).
* **In plain terms.**
  * "Corresponds": among respondents who report a family history of mental illness, the share of respondents giving each of the three answers to `Growing_Stress` can be compared across the months in the data within each gender, and between the two genders within each month. It does not mean that the shares change or stay the same, nor that any change happened in the same people, since each month holds different respondents. It also does not mean that family history and recognition are related, since no respondents without a family history are compared ("no comparison group without family history", objective). Nor does it mean anything listed in section 0, What no verdict states.
  * "Does not correspond": the cause is stated with the verdict, as one or more of: "under the reading that the file joins two sources, this cross says nothing about respondents"; "too few responses, or none, in a cell to read the comparison"; "the question or its indicator does not let the determination be made". It does not mean that the figures are wrong.
  * The reading list says which months have both cells present and unflagged. It changes no verdict.

### Q3

* **Question and objective.** The question is in [`indicators.md`, Q3](../specification/indicators.md#q3--indicators-5-6). Its objective is "Describe how the proportion of respondents reporting both growing stress and coping difficulties differs by occupation (the dataset's five categories, which include Student and Housewife alongside employment categories), by country, and by region, without attributing any difference to a work environment or to resilience" ([ADR-0004, addendum of 2026-10-04, Q3](../decisions/0004-revise-business-questions.md#addendum-2026-10-04)). Growing stress and coping difficulties are read as `growing_stress = 'Yes'` and `coping_struggles = 'Yes'`, as the question states; neither column has a source description ([conceptual framework, section 4](../conceptual-framework.md#4-variable-mapping-to-andersens-behavioral-model)).
* **Outputs and cells.** Indicator 5 (the count of rows that satisfy the condition) and indicator 6 (its rate), pattern B, over all rows, in two grouping sets, {`occupation`, `country`} and {`occupation`, `region`} (`indicators.md`, Q3). `region` is assigned to each country by the fixed mapping ([`country-region-mapping.md`](../specification/country-region-mapping.md)). The denominator is every row in the cell. A cell is one combination of a grouping set's values that occurs in the population ([`definitions.md`, Cell](../specification/definitions.md#query-vocabulary)). Strata and required cells: C1.
* **The condition.** The criteria read one rate per cell: the share of respondents with `growing_stress = 'Yes'` and `coping_struggles = 'Yes'`. `Growing_Stress` is part of the counted condition, not a lens, so its levels are not read separately ([multi-level self-report rule](../specification/definitions.md#multi-level-self-report-rule), the documented exception). Any other answer to either column is outside the condition.
* **Documentary layer.** The original question ([ADR-0006, Final business questions](../decisions/0006-final-questions-and-indicators.md#final-business-questions), Q3, in the legacy wording) and the legacy purpose (section 1.1). No documentary elements ([LOG-016](../decisions/log/LOG-016-objectives-q2-q6-q71-q72.md)).
* **Criteria.**
  * **C1. At least two regions, and every required cell present and unflagged.** Able to fail; the determination criterion, and the only criterion able to fail.
    * Strata: the countries, in the grouping set {`occupation`, `country`}; the regions, in {`occupation`, `region`}. A stratum exists when the output reports at least one of its cells. A country or region with no rows is not a stratum, and its absence is not a missing cell (section 4).
    * Required cells: at least two regions exist, and so at least two countries; in every stratum of each grouping set, the five `Occupation` cells ([`sources.md`, Value domains](../specification/sources.md#value-domains)).
    * Cells read: indicator 6's rate in each required cell.
    * Meets: at least two regions exist, and in every stratum the five cells are present and none is flagged by `low_n`. The rate can then be compared across occupations within each country and each region, and across countries and across regions within each occupation.
    * Does not meet: in at least one stratum, a required cell is missing or flagged (section 5, item 3); cause: data volume (section 4). Or fewer than two regions exist, so no comparison across regions can be made; cause: reasoning or design (section 4).
    * Note: when every country cell is present and unflagged, every region cell is too (Unable to fail, below); the number of regions does not follow, since several countries can fall in one region.
    * Ground: the objective names the breakdowns by occupation, by country and by region, each in full ([ADR-0004, addendum of 2026-10-04, Q3](../decisions/0004-revise-business-questions.md#addendum-2026-10-04)), so every stratum of each grouping set that exists is required ([LOG-046](../decisions/log/LOG-046-user-of-the-outputs.md)).
    * Crosses the groups (`country`, and `region`, from `Country`, in the OSMI group; `occupation`, `growing_stress` and `coping_struggles` in the other; [LOG-040](../decisions/log/LOG-040-h1-column-groups.md)). Its determination needs a relationship among respondents.
  * Unable to fail (section 2): indicator 5 equals indicator 6's numerators ([`patterns.md`, Cross-indicator consistency](../specification/patterns.md#cross-indicator-consistency); check C9); region numerators and denominators are sums over their countries ([`patterns.md`, Pattern B](../specification/patterns.md#pattern-b--conjunction-share); check C8).
* **Reading list.** Beside the verdict, each stratum of each grouping set is listed, countries first, then regions, each in alphabetical order, as readable (five cells present and unflagged) or not readable.
* **What "corresponds" means here.** "Corresponds" means only that the breakdowns the objective names can be read from the output, not what they show. Under "H1 does not hold", C1 fails through data volume or, where fewer than two regions exist, through reasoning or design (section 4).
* **Branches.**
  * H1 holds: C1 is not met (section 3.2), with the locus provenance (section 4).
  * H1 does not hold: C1 is read as stated (section 3.3).
  * Q3 involves `Occupation`, so every result is read under both branches (section 3.1); it does not involve `care_options`. Q3 receives one verdict per branch (section 2):

    | Branch | Verdict | Cause |
    |---|---|---|
    | H1 holds | does not correspond | under the reading that the file joins two sources, this cross says nothing about respondents; and, where a required cell is missing or flagged, also too few responses, or none, in a cell to read the comparison; and, where fewer than two regions exist, also the question or its indicator does not let the determination be made |
    | H1 does not hold | corresponds if at least two regions exist and every required cell is present and unflagged; otherwise does not correspond | where it does not correspond: too few responses, or none, in a cell to read the comparison; or, where fewer than two regions exist, the question or its indicator does not let the determination be made |

* **Reading note on direction** (section 2). By occupation: none; the objective excludes attributing any difference to a work environment or to resilience ([ADR-0004, addendum of 2026-10-04, Q3](../decisions/0004-revise-business-questions.md#addendum-2026-10-04)). By country and by region: none.
* **Premises.**
  * The condition, with `Growing_Stress` counted, not used as a lens (The condition).
  * Coping difficulties read as `coping_struggles = 'Yes'` (`indicators.md`, Q3; no source description, [conceptual framework, section 4](../conceptual-framework.md#4-variable-mapping-to-andersens-behavioral-model)).
  * The occupation categories include Student and Housewife alongside employment categories (objective).
  * The fixed country-to-region mapping ([`country-region-mapping.md`](../specification/country-region-mapping.md)).
  * The limitation on denominators (section 5, Limitation).
* **In plain terms.**
  * "Corresponds": the share of respondents who answer `Yes` to both `Growing_Stress` and `Coping_Struggles` can be compared across the five occupations within each country and each region, and across countries and across regions within each occupation. It does not mean that the shares differ, or that they do not, and it attributes no difference to a work environment or to resilience: the occupations include Student and Housewife alongside employment categories. Nor does it mean anything listed in section 0, What no verdict states.
  * "Does not correspond": the cause is stated with the verdict, as one or more of: "under the reading that the file joins two sources, this cross says nothing about respondents"; "too few responses, or none, in a cell to read the comparison"; "the question or its indicator does not let the determination be made". It does not mean that the figures are wrong.
  * The reading list says which countries and which regions have their five cells present and unflagged. It changes no verdict.

### Q5

* **Question and objective.** The question is in [`indicators.md`, Q5](../specification/indicators.md#q5--indicators-9-10-11). Its objective is "describe how these self-reported measures co-occur with different levels of indoor time, without asserting that indoor time causes or influences them" ([ADR-0004, Q5](../decisions/0004-revise-business-questions.md#q5--originally)). The four columns have no source description; their readings are premises ([conceptual framework, section 4](../conceptual-framework.md#4-variable-mapping-to-andersens-behavioral-model)).
* **Outputs and cells.** Indicators 9, 10 and 11, pattern A, over all rows: the level rates of `growing_stress`, `mood_swings` and `social_weakness`, each by `days_indoors`, whose five levels are ordered by `sort_order` (`indicators.md`, Q5). Indicator 10 also reports a headline rate. Required cells: C1.
* **Levels read.** For indicators 9 and 11, every level of `growing_stress` and of `social_weakness`; for indicator 10, the three levels of `mood_swings`. Indicator 10's headline rate (`Medium` plus `High`) is computed from those levels ([`patterns.md`, Output columns](../specification/patterns.md#output-columns)) and is not read separately.
* **Documentary layer.** The original question ([ADR-0004, Q5](../decisions/0004-revise-business-questions.md#q5--originally), as originally written) and the legacy purpose (section 1.1). No documentary elements ([LOG-016](../decisions/log/LOG-016-objectives-q2-q6-q71-q72.md)).
* **Criteria.**
  * **C1. Every required cell present and unflagged.** Able to fail; the determination criterion, and the only criterion able to fail.
    * Required cells: the five `days_indoors` cells ([`sources.md`, Value domains](../specification/sources.md#value-domains)). Indicators 9, 10 and 11 share them: the population is all rows and the cut is the same, so each cell has one denominator and one flag across the three indicators.
    * Cells read: the level rates of indicators 9, 10 and 11 in each required cell.
    * Meets: the five cells are present and none is flagged by `low_n`. The levels of each measure can then be compared across the five levels of time indoors, in their order.
    * Does not meet: a required cell is missing or flagged (section 5, item 3). Cause: data volume (section 4).
    * Ground: the question asks how the three measures differ "across levels of time spent indoors" (`indicators.md`, Q5), and the cut has five levels, so all five are required.
    * Does not cross the groups: `days_indoors`, `growing_stress`, `mood_swings` and `social_weakness` are all in the other group ([LOG-040](../decisions/log/LOG-040-h1-column-groups.md)).
  * Unable to fail (section 2): within each cell the level numerators of each indicator sum to the denominator (pattern A; check C8).
* **What "corresponds" means here.** "Corresponds" means only that the comparisons the objective names can be read from the output, not what they show. C1 fails only through data volume (section 4).
* **Branches.** Not applicable: Q5 crosses no groups and involves neither `Occupation` nor `care_options` (section 3.1), so it receives one verdict ([LOG-045](../decisions/log/LOG-045-correspondence-evidence-document.md)).
* **Reading note on direction** (section 2). By `days_indoors`: none. The objective excludes "asserting that indoor time causes or influences them" ([ADR-0004, Q5](../decisions/0004-revise-business-questions.md#q5--originally)), and no temporal claim is possible from the data ([conceptual framework, section 7](../conceptual-framework.md#7-threats-to-validity)).
* **Premises.**
  * Explicit recognition ([`definitions.md`, `explicit_recognition`](../specification/definitions.md#explicit_recognition)).
  * The readings of `growing_stress`, `mood_swings`, `social_weakness` and `days_indoors`, which have no source description ([conceptual framework, section 4](../conceptual-framework.md#4-variable-mapping-to-andersens-behavioral-model)).
  * `Maybe` is reported as its own level ([multi-level self-report rule](../specification/definitions.md#multi-level-self-report-rule)).
  * The levels of `days_indoors` are ordered by `sort_order` (`indicators.md`, Q5).
  * Elevated mood swings means `Medium` or `High`, for the headline rate only, which is not read.
  * The limitation on denominators (section 5, Limitation).
* **In plain terms.**
  * "Corresponds": for each of the three measures, the share of respondents at each answer level can be compared across the five levels of time spent indoors. It does not mean that the shares differ, or that they do not, nor that time indoors "causes or influences" any of these measures (objective); nor anything listed in section 0, What no verdict states.
  * "Does not correspond": the cause is stated with the verdict: "too few responses, or none, in a cell to read the comparison". It does not mean that the figures are wrong.

### Q6

* **Question and objective.** The question is in [`indicators.md`, Q6](../specification/indicators.md#q6--indicators-12-13). Its objective is "describe how care-options responses differ by explicit stress recognition, country, occupation and gender, without treating a response as a measure of the care options available to the respondent" ([ADR-0004, addendum of 2026-10-04, Q6](../decisions/0004-revise-business-questions.md#addendum-2026-10-04)). Its terms rest on premises:
  * explicit stress recognition: `growing_stress = 'Yes'` read as explicit recognition ([`definitions.md`, `explicit_recognition`](../specification/definitions.md#explicit_recognition));
  * care-options responses: the `care_options` response, in neutral wording ([LOG-013](../decisions/log/LOG-013-care-options-neutral-wording.md)), placed in the OSMI group as a premise (section 3.1).
* **Outputs and cells.** Indicator 12 (the rate of each `care_options` level) and indicator 13 (the count of each level), pattern A, over all rows, by one cross of `growing_stress` (3 levels) × `country` × `occupation` × `gender` (`indicators.md`, Q6). The denominator is the cell's full respondent count. A cell is one combination of the four cuts that occurs in the population ([`definitions.md`, Cell](../specification/definitions.md#query-vocabulary)). Strata and required cells: C1.
* **Levels read.** The three levels of `care_options`, `Yes`, `Not sure` and `No`, each read separately ([multi-level self-report rule](../specification/definitions.md#multi-level-self-report-rule)); the three levels of `growing_stress` as a cut, not `Yes` against the rest (`indicators.md`, Q6).
* **Documentary layer.** The original question ([ADR-0004, Q6](../decisions/0004-revise-business-questions.md#q6--originally), as originally written) and the legacy purpose (section 1.1). No documentary elements ([LOG-016](../decisions/log/LOG-016-objectives-q2-q6-q71-q72.md)).
* **Criteria.**
  * **C1. At least two strata, and every required cell present and unflagged.** Able to fail; the determination criterion, and the only criterion able to fail.
    * Strata: the countries. A stratum exists when the output reports at least one of its cells. A country with no rows is not a stratum, and its absence is not a missing cell (section 4).
    * Required cells: at least two strata exist; in every stratum, the thirty cells of the three `Growing_Stress` labels by the five `Occupation` labels by the two `Gender` labels ([`sources.md`, Value domains](../specification/sources.md#value-domains)).
    * Cells read: indicator 12's three level rates in each required cell.
    * Meets: at least two strata exist, and in every stratum the thirty cells are present and none is flagged by `low_n`. The responses can then be compared across each cut, with the others held fixed.
    * Does not meet: in at least one stratum, a required cell is missing or flagged (section 5, item 3); cause: data volume (section 4). Or fewer than two strata exist, so no comparison across countries can be made; cause: reasoning or design (section 4).
    * Ground: the objective names differences by explicit stress recognition, country, occupation and gender ([ADR-0004, addendum of 2026-10-04, Q6](../decisions/0004-revise-business-questions.md#addendum-2026-10-04)). The indicator reports them only as one cross, so each difference is read within it, with the other cuts held fixed, and every stratum that exists is required ([LOG-046](../decisions/log/LOG-046-user-of-the-outputs.md)).
    * Crosses the groups (`care_options`, `country` and `gender` in the OSMI group; `growing_stress` and `occupation` in the other; [LOG-040](../decisions/log/LOG-040-h1-column-groups.md)). Its determination needs a relationship among respondents.
  * Unable to fail (section 2): indicator 13 equals indicator 12's numerators ([`patterns.md`, Cross-indicator consistency](../specification/patterns.md#cross-indicator-consistency); check C9); within each cell the three level numerators sum to the denominator (pattern A; check C8).
* **Reading list.** Beside the verdict, each stratum is listed in alphabetical order as readable (its thirty cells present and unflagged) or not readable.
* **What "corresponds" means here.** "Corresponds" means only that the comparisons the objective names can be read from the output, not what they show. Under "H1 does not hold", C1 fails through data volume or, where fewer than two strata exist, through reasoning or design (section 4).
* **Branches.**
  * H1 holds: C1 is not met (section 3.2), with the locus provenance (section 4).
  * H1 does not hold: C1 is read as stated (section 3.3).
  * Q6 involves `Occupation`, so every result is read under both branches; its measure rests on the `care_options` premise tested by A6 (section 3.1). Where that premise does not hold, every result of Q6 is read under both branches (section 3.1), as it already is through `Occupation`, so the table below does not change. Q6 receives one verdict per branch (section 2):

    | Branch | Verdict | Cause |
    |---|---|---|
    | H1 holds | does not correspond | under the reading that the file joins two sources, this cross says nothing about respondents; and, where a required cell is missing or flagged, also too few responses, or none, in a cell to read the comparison; and, where fewer than two strata exist, also the question or its indicator does not let the determination be made |
    | H1 does not hold | corresponds if at least two strata exist and every required cell is present and unflagged; otherwise does not correspond | where it does not correspond: too few responses, or none, in a cell to read the comparison; or, where fewer than two strata exist, the question or its indicator does not let the determination be made |

* **Reading note on direction** (section 2). By `growing_stress`: none. The framework places `Growing_Stress` as perceived need and `care_options` as an enabling resource ([conceptual framework, section 4](../conceptual-framework.md#4-variable-mapping-to-andersens-behavioral-model)); the direction it supports concerns perceived need and care-seeking ([conceptual framework, section 3](../conceptual-framework.md#3-literature-basis-for-the-mechanism)), not perceived need and enabling resources. By gender: none (section 1.1). By country and by occupation: none.
* **Premises.**
  * Explicit recognition (Question and objective).
  * `Yes` and `Not sure` are reported separately ([multi-level self-report rule](../specification/definitions.md#multi-level-self-report-rule)).
  * A response to the care-options item is not a measure of the care options available to the respondent (objective).
  * The `care_options` premise (section 3.1; A6).
  * The limitation on denominators (section 5, Limitation).
* **In plain terms.**
  * "Corresponds": the shares answering `Yes`, `Not sure` and `No` to the care-options item can be compared across the three answers to `Growing_Stress`, across countries, across occupations and across genders, each with the others held fixed. It does not mean that the shares differ, or that they do not, nor that they measure the care options available to respondents; nor anything listed in section 0, What no verdict states.
  * "Does not correspond": the cause is stated with the verdict, as one or more of: "under the reading that the file joins two sources, this cross says nothing about respondents"; "too few responses, or none, in a cell to read the comparison"; "the question or its indicator does not let the determination be made". It does not mean that the figures are wrong.
  * The reading list says which countries have their thirty cells present and unflagged. It changes no verdict.

### Q7

* **Question and objective.** The question is in [`indicators.md`, Q7](../specification/indicators.md#q7--indicator-14). Its objective is "compare lifetime treatment-seeking across levels of explicit recognition within the same symptom profile — describing a relationship between self-reported recognition and treatment-seeking, not a level of psychological awareness or a degree of mental deterioration" ([ADR-0004, Q7](../decisions/0004-revise-business-questions.md#q7--originally)). Its terms rest on premises:
  * explicit recognition: `growing_stress = 'Yes'` read as explicit recognition ([`definitions.md`, `explicit_recognition`](../specification/definitions.md#explicit_recognition));
  * the convergent symptom profile: `symptom_cluster` ([`definitions.md`, `symptom_cluster`](../specification/definitions.md#symptom_cluster)), with its [validity caveat](../specification/definitions.md#symptom_cluster); "elevated" `Mood_Swings` is `Medium` or `High`, `Coping_Struggles` is `Yes`, and "elevated" `Days_Indoors` is `15-30 days`, `31-60 days` or `More than 2 months`.
* **Outputs and cells.** Indicator 14, pattern C (the rate at both levels of `treatment`), on the rows where `symptom_cluster` holds, by `growing_stress` (3 levels): three cells (`indicators.md`, Q7).
* **Population.** The rows where `symptom_cluster` holds (Question and objective).
* **Three levels.** The criteria read all three levels of `growing_stress`, not `Yes` against the rest, because the question asks for "all three levels" (`indicators.md`, Q7).
* **Documentary layer.** The original question ([ADR-0004, Q7](../decisions/0004-revise-business-questions.md#q7--originally), as originally written) and the legacy purpose (section 1.1). No documentary elements ([LOG-016](../decisions/log/LOG-016-objectives-q2-q6-q71-q72.md)).
* **Criteria.**
  * **C1. Every required cell present and unflagged.** Able to fail; the determination criterion, and the only criterion able to fail.
    * Required cells: the three `Growing_Stress` cells ([`sources.md`, Value domains](../specification/sources.md#value-domains)).
    * Cells read: indicator 14's `Yes` rate in the three cells.
    * Meets: the three cells are present and none is flagged by `low_n`. The share that reports lifetime treatment-seeking can then be compared across the three levels.
    * Does not meet: a required cell is missing or flagged (section 5, item 3). Cause: data volume (section 4).
    * Ground: the objective compares lifetime treatment-seeking "across levels of explicit recognition", and the question names all three levels.
    * Crosses the groups (`treatment` in the OSMI group; `symptom_cluster`'s columns and `growing_stress` in the other; [LOG-040](../decisions/log/LOG-040-h1-column-groups.md)). Its determination needs a relationship among respondents.
  * Unable to fail (section 2): the two levels' rates sum to 1 (pattern C; check C8); the three cells' denominators sum to the rows where `symptom_cluster` holds (`indicators.md`, Q7; check C8).
* **What "corresponds" means here.** "Corresponds" means only that the comparison the objective names can be read from the output, not what the comparison shows. Under "H1 does not hold", C1 fails only through data volume (section 4).
* **Branches.**
  * H1 holds: C1 is not met (section 3.2), with the locus provenance (section 4).
  * H1 does not hold: C1 is read as stated (section 3.3).
  * Q7 involves neither `Occupation` nor `care_options` (section 3.1).
  * Where the mapping of section 3.4 applies both branches, Q7 receives one verdict per branch (section 2):

    | Branch | Verdict | Cause |
    |---|---|---|
    | H1 holds | does not correspond | under the reading that the file joins two sources, this cross says nothing about respondents; and, where a required cell is missing or flagged, also too few responses, or none, in a cell to read the comparison |
    | H1 does not hold | corresponds if every required cell is present and unflagged; otherwise does not correspond | where it does not correspond: too few responses, or none, in a cell to read the comparison |

* **Reading note on direction** (section 2). By `growing_stress`: as in Q4.
* **Premises.**
  * Explicit recognition (Question and objective).
  * `Maybe` is reported as its own level ([multi-level self-report rule](../specification/definitions.md#multi-level-self-report-rule)).
  * The `symptom_cluster` definition and its validity caveat; "elevated" as defined there.
  * The limitation on denominators (section 5, Limitation).
* **In plain terms.**
  * "Corresponds": among respondents with the convergent symptom profile, the share that reports lifetime treatment-seeking can be compared across the three answers to `Growing_Stress`. It does not mean that the shares differ, or that they do not; it does not describe "a level of psychological awareness or a degree of mental deterioration" ([ADR-0004, Q7](../decisions/0004-revise-business-questions.md#q7--originally)), and it does not validate the profile ([`symptom_cluster`, validity caveat](../specification/definitions.md#symptom_cluster)); nor anything listed in section 0, What no verdict states.
  * "Does not correspond": the cause is stated with the verdict, as one or both of: "under the reading that the file joins two sources, this cross says nothing about respondents"; "too few responses, or none, in a cell to read the comparison". It does not mean that the figures are wrong.

### Q7.1

* **Question and objective.** The question is in [`indicators.md`, Q7.1](../specification/indicators.md#q71--indicator-15). Its objective is "describe lifetime treatment-seeking among respondents who report 'Yes' or 'Not sure' for care options, by recognition level and inclusion condition, without implying an active decision process or a shortfall against any expected level; 'No' is outside scope" ([ADR-0004, addendum of 2026-10-04, Q7.1](../decisions/0004-revise-business-questions.md#addendum-2026-10-04)). Its terms rest on premises:
  * explicit stress recognition: `growing_stress = 'Yes'` read as explicit recognition ([`definitions.md`, `explicit_recognition`](../specification/definitions.md#explicit_recognition));
  * a convergent symptom profile: `symptom_cluster`, with its [validity caveat](../specification/definitions.md#symptom_cluster);
  * care options: the `care_options` response, in neutral wording ([LOG-013](../decisions/log/LOG-013-care-options-neutral-wording.md)), placed in the OSMI group as a premise (section 3.1).
* **Outputs and cells.** Indicator 15, pattern C (the rate at both levels of `treatment`), on the population `(explicit_recognition OR symptom_cluster) AND care_options IN ('Yes','Not sure')`, by `growing_stress` (3 levels) × `symptom_cluster` × `care_options` (`Yes`, `Not sure`) (`indicators.md`, Q7.1). Required cells: C1.
* **Population.** The rows where explicit recognition or the convergent symptom profile holds, and the care-options response is `Yes` or `Not sure` (Question and objective). Respondents answering `No` are outside its scope, by a declared population filter ([multi-level self-report rule](../specification/definitions.md#multi-level-self-report-rule)).
* **Cells.** By construction, the population admits four (`growing_stress`, `symptom_cluster`) combinations: (`Yes`, true), (`Yes`, false), (`Maybe`, true), (`No`, true). With the two `care_options` levels, the indicator has up to eight cells (`indicators.md`, Q7.1); C1 requires all eight. The two other combinations are outside the population, not missing cells. Unlike the strata of Q7.2, each of the eight is required whether or not it occurs (Ground).
* **Inclusion condition.** The objective's "inclusion condition" is read through the two cuts that replaced it, `growing_stress` and `symptom_cluster` ([ADR-0004, amendment of 2026-09-23, Q7.1](../decisions/0004-revise-business-questions.md#q71--originally)). It is not the earlier three-way tag, which grouped `Maybe` with `No`.
* **Documentary layer.** The original question ([ADR-0004, Q7.1](../decisions/0004-revise-business-questions.md#q71--originally), as originally written) and the legacy purpose (section 1.1). The legacy objective is "Medir la brecha entre disponibilidad de recursos y su utilización efectiva." (English: "Measure the gap between the availability of resources and their effective use.") (legacy report, p. 7). The elements (section 6, Documentary layer):
  * E1. A gap between available resources and their use: "la brecha entre disponibilidad de recursos y su utilización efectiva" (English: "the gap between the availability of resources and their effective use") (objective). Quoted for context: "disponibilidad de recursos" (E2); "utilización efectiva" (E3). Rests on: `care_options`, `treatment`. Records: [ADR-0004](../decisions/0004-revise-business-questions.md), [LOG-013](../decisions/log/LOG-013-care-options-neutral-wording.md).
  * E2. Resources available to the respondent: "disponibilidad de recursos" (English: "availability of resources") (objective). Rests on: `care_options`. Records: [ADR-0004](../decisions/0004-revise-business-questions.md), [LOG-013](../decisions/log/LOG-013-care-options-neutral-wording.md).
  * E3. Use of treatment: "utilización efectiva" (English: "effective use") (objective); "¿Cuál es la proporción de personas […] buscar tratamiento (treatment = Yes)" (English: "What is the proportion of people […] seek treatment (treatment = Yes)") (question). Quoted for context: "personas" (E5). Rests on: `treatment`. Records: [ADR-0004](../decisions/0004-revise-business-questions.md).
  * E4. A decision to seek treatment: "deciden buscar tratamiento (treatment = Yes)" (English: "decide to seek treatment (treatment = Yes)") (question). Quoted for context: "buscar tratamiento (treatment = Yes)" (E3). Rests on: `treatment`. Records: [ADR-0004](../decisions/0004-revise-business-questions.md).
  * E5. Among people with stress or associated symptoms: "personas con estrés o síntomas asociados" (English: "people with stress or associated symptoms") (question). Rests on: `Growing_Stress`. Records: [LOG-012](../decisions/log/LOG-012-explicit-recognition-premise.md).
  * E6. Among those who have care or coverage options: "teniendo opciones de cuidado o cobertura (care_options ≠ 'No')" (English: "having care or coverage options (care_options ≠ 'No')") (question). Rests on: `care_options`. Records: [ADR-0004](../decisions/0004-revise-business-questions.md), [LOG-013](../decisions/log/LOG-013-care-options-neutral-wording.md).
  * E7. Those who seek treatment against those who do not: "frente a quienes no lo hacen" (English: "versus those who do not") (question). Rests on: `treatment`. Records: [ADR-0004](../decisions/0004-revise-business-questions.md).
  * Current question: "Among respondents with explicit stress recognition, a convergent symptom profile, or both, what proportion report having ever sought treatment (`treatment`, lifetime), broken down by care-options response (`care_options`, "Yes" and "Not sure" reported separately; respondents reporting "No" are outside this question's scope), by explicit stress recognition (`Growing_Stress`, all three levels), and by whether a convergent symptom profile is present?" ([indicators](../specification/indicators.md)). Current objective: "describe lifetime treatment-seeking among respondents who report 'Yes' or 'Not sure' for care options, by recognition level and inclusion condition, without implying an active decision process or a shortfall against any expected level; 'No' is outside scope" ([ADR-0004](../decisions/0004-revise-business-questions.md), set by [LOG-016](../decisions/log/LOG-016-objectives-q2-q6-q71-q72.md)).
  * Context: legacy report, pp. 80, 96, 99 and 100. The closing clause of p. 100 states an expected outcome and is not an element.
* **Criteria.**
  * **C1. Every required cell present and unflagged.** Able to fail; the determination criterion, and the only criterion able to fail.
    * Required cells: the eight cells.
    * Cells read: indicator 15's `Yes` rate in each required cell.
    * Meets: the eight cells are present and none is flagged by `low_n`. Lifetime treatment-seeking can then be compared across the three recognition levels among respondents with the convergent profile; between respondents with and without the profile among those answering `Yes` to `Growing_Stress`; and between the `Yes` and `Not sure` care-options responses in each of those.
    * Does not meet: a required cell is missing or flagged (section 5, item 3). Cause: data volume (section 4).
    * Ground: the objective names recognition level and inclusion condition ([ADR-0004, addendum of 2026-10-04, Q7.1](../decisions/0004-revise-business-questions.md#addendum-2026-10-04)). The question also names the care-options response, with `Yes` and `Not sure` reported separately, and reading them together would re-create a fold the specification removed ([multi-level self-report rule](../specification/definitions.md#multi-level-self-report-rule); [ADR-0006, row 15](../decisions/0006-final-questions-and-indicators.md#final-indicator-definitions)). All eight cells are therefore required.
    * Crosses the groups (`treatment` and `care_options` in the OSMI group; `growing_stress` and `symptom_cluster`'s columns in the other; [LOG-040](../decisions/log/LOG-040-h1-column-groups.md)). Its determination needs a relationship among respondents.
  * Unable to fail (section 2): the two levels' rates sum to 1 (pattern C; check C8).
* **What "corresponds" means here.** "Corresponds" means only that the comparisons the objective names can be read from the output, not what they show. Under "H1 does not hold", C1 fails only through data volume (section 4).
* **Branches.**
  * H1 holds: C1 is not met (section 3.2), with the locus provenance (section 4).
  * H1 does not hold: C1 is read as stated (section 3.3).
  * Q7.1 does not involve `Occupation`. Its population and a cut rest on the `care_options` premise tested by A6 (section 3.1). Every result of Q7.1 crosses `care_options`, as a cut and in the population; where its premise does not hold (section 3.1), every result of Q7.1 is read under both branches.
  * Where both branches apply, Q7.1 receives one verdict per branch (section 2):

    | Branch | Verdict | Cause |
    |---|---|---|
    | H1 holds | does not correspond | under the reading that the file joins two sources, this cross says nothing about respondents; and, where a required cell is missing or flagged, also too few responses, or none, in a cell to read the comparison |
    | H1 does not hold | corresponds if every required cell is present and unflagged; otherwise does not correspond | where it does not correspond: too few responses, or none, in a cell to read the comparison |

* **Reading note on direction** (section 2).
  * By `growing_stress`: as in Q4.
  * By care-options response and by profile presence: none. The framework places `care_options` as an enabling resource and the symptom columns as correlates adjacent to perceived need ([conceptual framework, section 4](../conceptual-framework.md#4-variable-mapping-to-andersens-behavioral-model)); the direction it supports concerns perceived need and care-seeking ([conceptual framework, section 3](../conceptual-framework.md#3-literature-basis-for-the-mechanism)), and it states none for either cut. The objective excludes "implying an active decision process or a shortfall against any expected level" ([ADR-0004, addendum of 2026-10-04, Q7.1](../decisions/0004-revise-business-questions.md#addendum-2026-10-04)).
* **Premises.**
  * Explicit recognition (Question and objective).
  * The `symptom_cluster` definition and its validity caveat.
  * `Yes` and `Not sure` are reported separately, and `No` is outside scope (declared filter).
  * The `care_options` premise (section 3.1; A6).
  * The limitation on denominators (section 5, Limitation).
* **In plain terms.**
  * "Corresponds": the share that reports lifetime treatment-seeking can be compared across the three answers to `Growing_Stress` among respondents with the convergent symptom profile; between respondents with and without the profile among those answering `Yes` to `Growing_Stress`; and between the `Yes` and `Not sure` care-options responses in each of those. No other comparison is claimed. It does not mean that the shares differ, or that they do not. It does not describe "an active decision process or a shortfall against any expected level" (objective), nor the care options available to respondents ([LOG-013](../decisions/log/LOG-013-care-options-neutral-wording.md)). It says nothing about respondents who answered `No` to the care-options item, and it does not validate the profile ([`symptom_cluster`, validity caveat](../specification/definitions.md#symptom_cluster)). Nor does it mean anything listed in section 0, What no verdict states.
  * "Does not correspond": the cause is stated with the verdict, as one or both of: "under the reading that the file joins two sources, this cross says nothing about respondents"; "too few responses, or none, in a cell to read the comparison". It does not mean that the figures are wrong.

## 7. Amendments

[PENDING: empty until any change after this document's commit; a change after exposure is marked as post-exposure (ADR-0011, Constraint)]

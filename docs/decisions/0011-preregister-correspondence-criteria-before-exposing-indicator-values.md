---
status: "accepted"
date: 2026-09-28
decision-makers: Octavio Carpineti
---

# Fix the correspondence criteria in a commit before any indicator value is exposed, and declare what was already known about the data

## Context and Problem Statement

After the pipeline was built, a further step examines, question by question, whether what the Hefesto phases ("Fase N", English: "Phase N"; see [`methodology.md`](../methodology.md)) planned (questions, objectives, indicators, design) corresponds to what the built system produces on the real file. The step rests on **correspondence criteria**: for each business question, a statement of what shape of indicator output would count as serving the question's objective and what shape would not. A verdict of "corresponds", "partially corresponds" or "does not correspond" is informative only if the criterion behind it could have gone the other way.

That property is lost when information about the output reaches the person writing a criterion before the criterion is fixed. A marginal distribution, a count, the set of cells an indicator produces, or familiarity with the data from earlier work can each shape a criterion without its author noticing, and the result can read as objective while being fitted to what is already known. No one has to act in bad faith for this to happen; it is automatic. The risk is present here: part of what is known about the file is published in the repository (K1), and part is published only in pull-request descriptions (K3).

How should the correspondence criteria be fixed so that the verdicts they produce can be trusted, given that some information about the data is already known?

### The same problem in other fields

Empirical research has named this problem and established a remedy. HARKing (Kerr, 1998) is the practice of presenting a hypothesis formed after the results are known as if it had been fixed beforehand; a criterion chosen after the output and presented as prior is the same act applied to a different object. Gelman and Loken (2014; the argument first circulated as a working paper, Gelman and Loken, 2013) show that the resulting bias needs neither a search nor bad faith: when analysis choices depend on the data, the number of comparisons that could have been made exceeds the number performed, even if a single analysis is run. Nosek et al. (2018) identify hindsight bias as the reason unaided vigilance fails, and propose the remedy: fix the analysis plan before observing the data, which separates prediction from postdiction. That literature concerns significance testing, and this exercise computes no p-values; what transfers is the structure, a decision contingent on the data, not the statistic.

The problem also has the structure of leakage in predictive modeling. There, information about the evaluation target that should not be available to the modeling process reaches modeling decisions, and the evaluation comes out optimistic with no one cheating (Kaufman et al., 2012). The remedy is a separation between what is decided and what is evaluated, enforced through how the data are managed rather than by assurance. The correspondence exercise has the same two roles: the criteria are decisions, and the indicator values are the evaluation. When information about the values reaches the criteria, correspondence comes out favorable by the same mechanism. The remedy is analogous: keep the values away from the criteria until the criteria are fixed, and make that order checkable from the record instead of asserted.

Two limits from the literature bear on this project. The remedy is cleanest when no one has observed the data. For existing data, Nosek et al. (2018) state that what can be tested depends on whether analysis-plan decisions are blind to the data, ask who has observed the data and which summaries have been communicated, and describe partial blinding as a gray area between prediction and postdiction; Mertens and Krypotos (2019) provide a template in which the analyst states which parts of preexisting data were already used. Gelman and Loken (2014) judge preregistration of limited meaning where the analyst already knows the data well. The file used here is partly known, so blindness cannot be promised.

The three cases share one principle: an evaluation is informative only if what is evaluated was fixed without access to what evaluates it. A hypothesis and its results, a model and its held-out data, a correspondence criterion and the indicator values are instances of the same relation. The analogy with predictive modeling also marks where the remedy must differ. There, isolation is physical: a held-out set that no one has seen is set aside before modeling. Here that is not available, because part of the data is already known. The mechanism below therefore replaces isolation with two substitutes: an order of exposure that the repository history makes verifiable, and a declaration of what was known when the criteria were fixed.

## Findings

Finding IDs use a new letter, `K` (prior knowledge): this ADR concerns what was available about the data before criteria are fixed, which neither ADR-0000 nor ADR-0001 covers.

| ID | Finding | Evidence | Status |
|----|---------|----------|--------|
| K1 | **The marginal distributions of the source-described columns and of the symptom columns are published in the repository.** | [ADR-0001](0001-position-as-portfolio-project.md), P8 | Established |
| K2 | **The acceptance checks C8 and C9 execute all sixteen indicators on every run with the source file and assert only equalities between results; no test writes a value anywhere. A failing assertion prints the values that differ.** | `tests/test_acceptance.py` (fixture `indicators`, tests `test_c8_*` and `test_c9_*`); [`acceptance.md`](../specification/acceptance.md). Printing on failure reproduced with `pandas.testing.assert_series_equal` (used by C9) and with a plain `assert` under pytest (most of C8's tests; one, `test_c8_region_cells_are_sums_over_their_countries`, uses `pandas.testing.assert_frame_equal`) | Established at commit `03c9aad` |
| K3 | **The counts of `explicit_recognition` and `symptom_cluster` on the real file, and the number of cells each indicator produces, were published in pull-request descriptions (#33 and #34) before any criterion was written; no repository file records them.** Under rule 1's definition, these are prior exposures, and rule 2 declares them. | PR #33 and PR #34 descriptions on GitHub; search of `docs/`, `src/`, `tests/` and of commit messages on `main` at commit `03c9aad` | Established |

## Decision Drivers

* A verdict is informative only if its criterion could have failed; a criterion fitted to known output cannot.
* The contamination needs no intent, so the remedy cannot rest on assurance from the author of the criteria.
* Some information about the data is already known (K1, K3), so the remedy must not promise blindness; it can promise an ordered exposure and an inspectable statement of what was known.
* The order must be verifiable by a third party from the record, not by the author's word. `main` is protected and changes only through pull requests ([ADR-0002](0002-protect-main-with-required-pull-requests.md)), so its history is such a record.
* The analysis has a single author, so the remedy must work without a second analyst.
* The rules for reading results that cross column groups depend on checks whose outcomes are themselves information about the data ([`legacy-audit.md`](../audit/legacy-audit.md), A5, A6 and A10), so those rules need protection too.
* The values cited in the final report must be reproducible by anyone with the source file.

## Considered Options

* No protocol: rely on the criteria having been written first.
* Pre-registration by commit: commit the criteria before any value is exposed and declare prior knowledge in the criteria document.
* Blind analysis ([MacCoun and Perlmutter, 2015](#references)): a party other than the analyst runs the indicators and hands over output with masked labels.

## Decision Outcome

Chosen option: "Pre-registration by commit", because it is the option that fits a single-author analysis on partly known data: it fixes the order of exposure, makes that order checkable from the repository history, and turns the prior knowledge that cannot be removed into a declared, inspectable list. It does not deliver blindness and does not claim to. The mechanism has five rules.

1. **Exposure order.** The correspondence criteria are committed to `main` before any indicator value is exposed. An indicator value (a numerator, a denominator, a rate, or the number of cells) is exposed when it is displayed or reported in any form: printed output, a dump, a document, pull-request text, or a message. The restriction is on exposure, not on execution: C8 and C9 already execute the sixteen indicators on every run with the source file and report only pass or fail (K2). The commit and its hash are the verifiable evidence of the order; the order is not merely asserted. If a failing assertion displays values before the criteria commit, those values are added to the declaration of rule 2.
2. **Declared prior knowledge.** What was already known about the data when the criteria were fixed is listed in the criteria document itself, `docs/audit/correspondence-criteria.md`, so that anyone can judge whether a criterion bent to it. The list includes at least: the marginal distributions published in ADR-0001, P8 (K1); the counts of the derived conditions reported by check C10 (K3); the cell structure of the indicators, that is, how many of the possible cells exist (K3); and knowledge of the data from having carried out the original project.
3. **Criteria written from objectives.** Each criterion is derived from the objective of its question, never from an expectation about the data. A criterion of the form "this shape of output would serve deciding X" does not depend on the data. One of the form "the output is expected to come out flat" already contains the data, and is not admitted. A directional expectation may appear only where the [conceptual framework](../conceptual-framework.md) supports it, with its source cited. Each criterion is stated as an observable shape of the output, specific enough that two readers applying it to the same output reach the same verdict.
4. **Reading branches fixed first.** Two branches for reading results that cross the two column groups, one for the case in which H1 ([ADR-0001](0001-position-as-portfolio-project.md)) holds and one for the case in which it does not, are written and committed before checks A5, A6 and A10 are run. Being before the reading of the indicator output is not enough: a branch drafted after a check result is known tends to end up poorer for whichever branch the result leaves unapplied, with no one intending it. That is the contamination this ADR prevents, one level further in. The full order is: commit of the criteria and both branches, then A5, A6 and A10, then exposure and reading of the indicator output. A6 and A10 need external datasets (the OSMI 2014 survey and RHMCD-20). If one cannot be obtained, results that cross column groups are read under both branches without resolving between them, and the criteria document says so.
5. **Reproducible reading.** The indicator dump is produced twice and the two are compared, as a confirmation. The pipeline is deterministic by construction (every indicator query carries an explicit `ORDER BY`, and each dimension's surrogate keys are assigned in the order of its natural key; see `src/stress_dw/sql/`), so the comparison confirms this; it does not answer a detected risk. The final report cites one hash per indicator over a canonical serialization (fixed column order, row order and numeric format), so anyone with the source file can reproduce it. This ADR fixes the principle; the concrete format belongs to the implementation plan.

### Consequences

* Good, because every criterion can fail: it is fixed before the values it will be applied to, so a "does not correspond" verdict remains possible and a "corresponds" verdict carries information.
* Good, because the cost is one commit and a declared list; the mechanism needs no second analyst and no new tooling.
* Good, because a reader of the final report can reproduce each cited value from the source file, its SHA-256 and the commit (rule 5; see [`phase4-closure.md`](../audit/phase4-closure.md#2-reproducing-this)).
* Bad, because the mechanism records the order of publication, not the order of observation: history cannot show what was displayed outside the repository. The declaration of rule 2 covers that gap by stating what was known, not by proving what was not.
* Bad, because prior knowledge can be declared but not removed: the criteria are written by someone who partly knows the data (K1, K3), so whether a criterion bent to that knowledge is left to the reader's judgment of the declared list. This is the gray area the literature describes for preexisting data; the mechanism narrows it and does not close it.
* Bad, because the two reading branches double the interpretive text to be written before the checks run.
* Constraint: after the criteria commit, the criteria document is not rewritten. A criterion changed after any value has been exposed is recorded as a dated amendment beside the original, marked as post-exposure, the original left unchanged. Each verdict cites the criterion it applies and, where one exists, its amendment.
* Constraint: results are reported as outputs of a methodological test bench, as [ADR-0001](0001-position-as-portfolio-project.md) requires, and the criteria document uses no name that [writing conventions, rule 5](../writing-conventions.md#5-names-claim-only-what-the-data-supports) excludes.

### Confirmation

* In the history of `main`, the commit of the criteria document precedes every commit that contains an indicator value, whether in a report, a dump, a decision record or another document. Checked with `git log` over the paths concerned; the final report cites the criteria commit's hash.
* The criteria document contains the declaration of rule 2 with at least the four items listed there.
* The commit that records the results of A5, A6 and A10 in [`legacy-audit.md`](../audit/legacy-audit.md) is later than the commit that contains the two reading branches.
* The final report carries one hash per indicator over the canonical serialization, the reproduction recipe (repository commit, SHA-256 of the source file, the indicator number passed to `run_indicator`), and the result of comparing the two runs.

## Pros and Cons of the Options

### No protocol

* Good, because it costs nothing.
* Bad, because it offers no way to tell a criterion fixed before the values from one fitted after them; the contamination needs no bad faith, so an assurance from the author does not help.

### Pre-registration by commit

* Good, because the order of commits is checkable in the history of a protected branch.
* Good, because it needs no second person and works on data already partly known, provided the prior knowledge is declared.
* Bad, because it evidences the order of publication, not of observation.
* Bad, because it does not restore blindness (limits in Context).

### Blind analysis

* Good, because it acts directly on the analyst's ability to steer analysis choices toward a result.
* Bad, because it requires separating the person who runs and masks from the person who analyzes; with a single author the separation does not exist, and a second party holding the same information adds no independence.
* Bad, because masking has little to hide here: the marginal distributions are already public (K1), and masking variable labels would defeat criteria stated over named variables.
* Not adopted, neither in place of the chosen option nor alongside it: once the criteria are fixed by commit, the reading step applies criteria already written, which leaves less to steer; what remains is the discretion of applying a criterion, which rule 3 reduces by requiring criteria stated as observable shapes of output. It would become relevant if writing the criteria and reading the output were split between two people.

## More Information

* Related: [ADR-0001](0001-position-as-portfolio-project.md) (test-bench constraint; P8; H1 and H3; checks A5, A6, A10), [ADR-0002](0002-protect-main-with-required-pull-requests.md) (protected `main`), [ADR-0004](0004-revise-business-questions.md) (checklist for names and questions), [ADR-0006](0006-final-questions-and-indicators.md) (the questions and indicators the criteria refer to).
* Definitions of C8, C9 and C10: [`acceptance.md`](../specification/acceptance.md). Reporting status of results: [`patterns.md`](../specification/patterns.md#reporting-rules).

### References

* Gelman, A., & Loken, E. (2013). *The garden of forking paths: Why multiple comparisons can be a problem, even when there is no "fishing expedition" or "p-hacking" and the research hypothesis was posited ahead of time.* Unpublished working paper, Department of Statistics, Columbia University, 14 November 2013. https://sites.stat.columbia.edu/gelman/research/unpublished/p_hacking.pdf
* Gelman, A., & Loken, E. (2014). The Statistical Crisis in Science. *American Scientist*, 102(6), 460–465. https://doi.org/10.1511/2014.111.460
* Kaufman, S., Rosset, S., Perlich, C., & Stitelman, O. (2012). Leakage in data mining: Formulation, detection, and avoidance. *ACM Transactions on Knowledge Discovery from Data*, 6(4), Article 15. https://doi.org/10.1145/2382577.2382579
* Kerr, N. L. (1998). HARKing: Hypothesizing after the results are known. *Personality and Social Psychology Review*, 2(3), 196–217. https://doi.org/10.1207/s15327957pspr0203_4
* MacCoun, R., & Perlmutter, S. (2015). Blind analysis: Hide results to seek the truth. *Nature*, 526, 187–189. https://doi.org/10.1038/526187a
* Mertens, G., & Krypotos, A.-M. (2019). Preregistration of analyses of preexisting data. *Psychologica Belgica*, 59(1), 338–352. https://doi.org/10.5334/pb.493
* Nosek, B. A., Ebersole, C. R., DeHaven, A. C., & Mellor, D. T. (2018). The preregistration revolution. *Proceedings of the National Academy of Sciences*, 115(11), 2600–2606. https://doi.org/10.1073/pnas.1708274114

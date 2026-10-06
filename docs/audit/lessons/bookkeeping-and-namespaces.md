# Bookkeeping and namespaces

Format: [lessons index](README.md#format).

## LSN-008 — Totals are computed from one primary class per finding

* **What happened.** The first totals of the documentation-currency register did not match its rows. They were counted from the Class column as written: rows with a dash in that column and the disposition in another were missed, and findings with two classes were counted under the first only.
* **How it was detected.** On review, by counting rows against the totals.
* **Rule.** See [LOG-005](../../decisions/log/LOG-005-register-bookkeeping-conventions.md).
* **Pointers.** Reconciliation section of the documentation-currency register.

## LSN-009 — Every finding identifier appears in a summary of the register

* **What happened.** A report that summarized the documentation-currency register folded two findings into a sentence about clean checks without their identifiers, so they seemed to be missing.
* **How it was detected.** On review, by looking for every identifier in the report.
* **Rule.** See [LOG-005](../../decisions/log/LOG-005-register-bookkeeping-conventions.md).
* **Pointers.** Findings DC-22 and DC-23 of the documentation-currency register.

## LSN-010 — Each namespace has its own prefix

* **What happened.** In the documentation-currency register, the names of the correction groups (a1, a2, b, c, d, e) shared their letters with the decision letters (a–l), so "b" could mean either.
* **How it was detected.** On review.
* **Rule.** See [LOG-005](../../decisions/log/LOG-005-register-bookkeeping-conventions.md) (`PR-` prefixes, N identifiers) and [LOG-004](../../decisions/log/LOG-004-decision-log-and-lessons.md) (`LOG-` and `LSN-` prefixes).
* **Pointers.** Legend of the findings section of the documentation-currency register.

## LSN-013 — Closure lists are built from every disposition

* **What happened.** The "Still open" lists of the stage-4 re-check and of the closure of the documentation-currency sweep were built from the PR column of the register. They left out two findings decided and never placed in a pull request, whose PR column reads "—" (DC-12, DC-69), and items assigned to the correspondence phase only in a disposition or in a pull-request description (DC-81, DC-82, decision e). The sweep was declared closed with those items open. Probe 1's term list did not include state phrases such as "in progress", so a status sentence of the README made stale by the closure was not caught (DC-96).
* **How it was detected.** By a read-only audit after the closure that checked every decision of the log, every disposition and every open item of the log against the repository.
* **Rule.** A closure list is built from the disposition of every finding and every open item of the decision log, never from the PR column, and a probe for temporal drift includes state phrases ("in progress", "ongoing", "next step", "will be", "to be written", "planned").
* **Pointers.** DC-12, DC-69, DC-81, DC-82, DC-96; [LOG-019](../../decisions/log/LOG-019-a6-scope.md), [LOG-027](../../decisions/log/LOG-027-see-as-cross-reference.md); documentation-currency register, sections 14 to 16.

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

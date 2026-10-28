# Boundary cases: where two readings of one rule part

## The concept

A ticket office posts a sign: "free entry for children under 12". One clerk reads it as age < 12, another as age ≤ 12.

![Top: two overlapping sets, reading A and reading B. Both and neither are agreement; only A and only B are gaps. Bottom: ages 9 to 14 under two readings of 'under 12': A lets 9 to 11 in free, B lets 9 to 12. The difference is age 12, at the border.](figures/two-readings-and-the-border.svg)

Software testing calls cases like 11, 12 and 13 **boundary values**: tests placed where a rule changes its answer, because that is where two readings of it part.

## The transfer

The criteria document is the sign. Two fresh readers are the clerks, and the answer key, written by a party that co-drafted the criteria, is the owner's own reading.

* **Cases at the border, not typical ones.** Before the commit, fresh readers with no other context applied the text to symbolic boundary cases, with no verdicts attached, and explained each verdict in their own words ([criteria document, section 0](../audit/correspondence-criteria.md#0-scope), Two-reader test).
* **A gap is a case in "only A" or "only B".** In the criteria, as on the sign, it is a case one reader lets in and the other does not.
* **The owner's sheet stays with the owner.** The key was withheld from the party that rewrote the text, so that the sign could not be written to give the owner's answer. That rule is the subject of [pre-registration](preregistration-and-data-leakage.md).
* **Result.** In the final round both readers gave the key's verdict on every case they read, and the text was not changed afterwards ([criteria document, section 0](../audit/correspondence-criteria.md#0-scope), Two-reader test).

## Where it breaks

* Ages form a line with one border. The cases of a criterion combine several conditions, so its borders are many and the cases test a chosen few.
* Finitely many cases can find a difference between two readings; finding none does not prove the readings equal. Agreement holds on the borders tested.
* Both readers were models of the same family as those that drafted the criteria, so their agreement shows one reading for that family, not for every reader ([criteria document, section 0](../audit/correspondence-criteria.md#0-scope)).

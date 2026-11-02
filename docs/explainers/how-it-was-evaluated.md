# How it was evaluated

How the evaluation was fixed before its results were seen, and where the method overreached.

## Fixed in advance

* **Criteria before results.** What each question's output had to allow was committed before the indicator output was exposed ([correspondence criteria](../audit/correspondence-criteria.md); [ADR-0011](../decisions/0011-preregister-correspondence-criteria-before-exposing-indicator-values.md)). Values of the same quantities already in the repository before that commit are listed and declared, so the commit did not precede every value ([evidence, section 3](../audit/correspondence-evidence.md#3-post-commit-exposures)). Analogy: [pre-registration](../concept-transfers/preregistration-and-data-leakage.md).
* **Boundary-case readers.** Fresh language-model sessions applied the criteria to boundary cases against a key and, in the final round, gave the key's verdict on every case; they are of the same family as the models that drafted the criteria, so the agreement shows one reading for readers of that family, not for every reader, and key content on which questions differ by reading branch reached the party that drafts fixes before the text was frozen ([criteria, section 0](../audit/correspondence-criteria.md#0-scope)). Analogy: [boundary cases](../concept-transfers/boundary-cases.md).
* **Stopping rule.** A rule set before the third audit reading stopped the fixes to the documentary rule of the criteria (section 6); the documentary verdict was removed, and no correspondence verdict changed ([LOG-051](../decisions/log/LOG-051-stopping-rule-documentary-audit-readings.md)). Analogy: [overfitting](../concept-transfers/overfitting.md).

## Where the method overreached

A rule whose verdict changed no correspondence verdict was revised after every audit reading, and the whole phase took effort out of proportion to the one document it fixed ([scope and proportion](../audit/lessons/scope-and-proportion.md); LSN-014, LSN-015). Analogy: [parsimony](../concept-transfers/parsimony.md).

## In the first person

<!-- first-person:start -->
> 
> The overreach was mine. I wrote strict rules, and they were applied to the letter, in my work with language models too, even where a decision needed the direct path. Taking the ingredients at hand to their best expression is half of cooking; the other half is serving the dish while it can still be enjoyed. Parts of this one arrived late.
> 
> What I value most is what I learned along the way. When the criteria had to be fixed before any result, I asked whether it was because of data leakage, which I knew from machine learning. It was not exactly that, but it was close, and stating where a borrowed concept stops holding became how I explain the method. I also learned that the how is what sustains the why; I used to stress only the why. This section was itself going to grow into a review of my premises against the literature, and it was cut back.
> 
> What went wrong is recorded because I learn from what I do wrong. Claiming that everything went right would mean either hiding a mistake or not having noticed it, and both lose. I would rather show than claim: what I state, I try to back with a record, and where I could not, the gap is recorded too. An accurate record leaves no story to maintain.
> 
> — @CarpinetiOctavio
<!-- first-person:end -->

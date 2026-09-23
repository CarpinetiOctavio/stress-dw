---
status: "accepted"
date: 2026-09-22
decision-makers: Octavio Carpineti
---

# Protect `main` with required pull requests

## Context and Problem Statement

`stress-dw` was private until ADR-0001's confirmation made it public. Branch protection is not available on private repositories under a GitHub Free plan, so none was configured while it was private. Two pull requests (#1, #2) were already merged into `main` before any protection existed, following a review-before-merge habit informally. Now that the repository is public and part of a professional portfolio, should `main` be protected, and with what rules?

## Decision Drivers

* The repository is part of a professional portfolio for SCU; a visible pull-request history is itself a signal of engineering discipline to anyone reviewing it, independent of team size.
* There is currently a single contributor, so protections that assume a multi-reviewer team (a required approving review from a second person, code owners) have no practical effect yet.
* PRs #1 and #2 already show the habit is adopted in practice — formalizing it is enforcement, not a behavior change.
* No CI pipeline exists yet, so requiring passing status checks before merge isn't enforceable today.
* Overprotecting now, in a way that blocks the sole contributor's own merges entirely, would add friction to a solo project without a corresponding benefit.

## Considered Options

* No protection on `main` — keep pushing directly.
* Protect `main`: require a pull request before merging; disallow force-pushes and branch deletion; no required status checks.
* Protect `main` with required status checks, once CI exists.
* Protect `main` and require signed commits.

## Decision Outcome

Chosen option: "Protect `main`: require a pull request before merging; disallow force-pushes and branch deletion; no required status checks", because it formalizes what PRs #1 and #2 already did in practice, keeps the engineering-discipline signal visible for the portfolio, and does not depend on a CI pipeline that does not exist yet.

### Consequences

* Good, because it matches the workflow already in use, at no added cost.
* Good, because it prevents an accidental force-push or deletion on the repository's main branch.
* Neutral, because with one contributor, "required review" has no enforcement teeth unless self-approval is explicitly allowed, which GitHub's setting permits.
* Bad, because it adds one extra step — open a pull request, then merge it — to every change, however small.

### Confirmation

Settings → Branches → branch protection rule on `main`, visible in the repository's own settings; a direct push to `main` failing is the fitness function.

## Pros and Cons of the Options

### No protection

* Good, because it is the fastest path, with no added friction.
* Bad, because it does not match what a reviewer would expect from a portfolio repository, and does not prevent an accidental direct push from overwriting history.

### Require pull requests, no status checks

* Good, because it matches the existing habit (PRs #1, #2) and needs no CI to be meaningful.
* Bad, because it does not catch anything a status check would catch — none exist yet.

### Require pull requests and status checks

* Good, because it would catch lint or test failures before merge, once they exist.
* Bad, because there is no CI pipeline yet; the rule would either block every merge or need to be added later regardless.

### Require pull requests and signed commits

* Good, because it adds a verifiable authorship signal.
* Bad, because it requires a one-time GPG/SSH signing setup with no clear benefit for a single-author academic project.

## More Information

* Branch protection was not available while `stress-dw` was private, under GitHub Free.
* Related: [ADR-0001](0001-position-as-portfolio-project.md), which made the repository public.
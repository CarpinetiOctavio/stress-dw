# Parsimony: the fewest parameters that explain the data

## The concept

The normal distribution has two parameters. Newer distributions have three or more, and can follow a sample more closely; that does not make them better. With fewer parameters to estimate, a small sample pins the normal down better, and it is the most studied of all.

![Twenty-five synthetic annual maxima, fitted by a 2-parameter and a 3-parameter distribution. The two curves agree within the record and separate beyond it.](figures/two-fits-one-sample.svg)

*Twenty-five synthetic annual maxima, drawn from a 2-parameter distribution and fitted with 2 and with 3 parameters. Within the record the fits are hard to tell apart; beyond it they diverge.*

In hydrology the difference matters: design values are read at return periods longer than the record, where the extra parameter has the least data behind it. The standard error of fit used to compare fits divides the squared error by n − mp, where mp is the number of parameters, so each parameter costs a degree of freedom; when two fits come out close, the one with fewer parameters is chosen (Ganancias Martínez, 2010, pp. 83 and 85; applied on pp. 167 and 302).

## The transfer

* **Applied before this repository.** The statistical engine of METIS ranks distribution fits by that standard error, with mp in the denominator ([`eea.py`](https://github.com/CarpinetiOctavio/PI_METIS/blob/cae2f4b57a37e968c030848ceee1b5c89355a838/backend/metis/core/etapa2/eea.py), at commit `cae2f4b`).
* **Applied to a rule.** The documentary rule was rewritten on one principle instead of a clause per gap: fewer parameters for the same gaps. See [overfitting](overfitting.md).
* **Applied to a layer.** When fixing that rule stopped converging, the documentary verdict was removed rather than extended; no correspondence verdict depended on it ([LOG-051](../decisions/log/LOG-051-stopping-rule-documentary-audit-readings.md#decision)).
* **Applied to the method.** A rule, check or document that changes no verdict or result is not added ([LSN-015](../audit/lessons/scope-and-proportion.md#lsn-015--the-process-outgrew-the-object)).

## Where it breaks

* A text has no likelihood and no parameter count; "fewer parameters" for a rule means fewer clauses that can each open a reading, an informal measure.
* Parsimony breaks ties; it does not excuse a poor fit. The thesis applies it only when the errors are close.
* The figure's sample was drawn from a 2-parameter distribution, so it favors that fit by construction. A sample from a 3-parameter one would show the opposite risk: too few parameters.

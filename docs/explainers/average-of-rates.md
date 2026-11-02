# Average of rates

The second of two errors that the audit of the course version found ([ADR-0000](../decisions/0000-rebuild-from-scratch-instead-of-continuing-legacy.md)).

## What happened

The course version stored a percentage in each aggregated row and averaged those percentages for a coarser cut. An average of rates gives each row the same weight, so a row behind a few records weighed as much as a row behind many ([legacy audit, A7](../audit/legacy-audit.md#checks)).

![Top: the legacy query averages porcentaje_tratamiento over two aggregated rows, 90.0 from 9 treated of 10 records and 50.0 from 500 of 1,000, and gets 70.0: each row weighs the same, whatever the number of records behind it. Bottom: the rebuild stores no rate; a coarser cut sums the numerators and the denominators of the finer cells, 509 over 1,010, and gets 0.504 (50.4%): each record weighs the same. Illustrative rows.](../specification/figures/average-of-rates.svg)

*An average of rates weighs each row the same; summed numerators and denominators weigh each record the same. Illustrative rows.*

## How the rebuild prevents it

No rate is stored. A rate is a numerator over a denominator, and a coarser cut sums the numerators and the denominators of the finer cells ([roll-up rule](../specification/definitions.md#roll-up-rule)).

## How it is tested

Check C4 confirms that no table stores a ratio, a percentage or a count, and C8 that the cell denominators sum to an independent count ([`acceptance.md`](../specification/acceptance.md)); the test suite runs them when the source file is present ([Phase 4 closure, section 4](../audit/phase4-closure.md#4-acceptance-checks-c1c11)).

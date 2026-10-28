# Sets and multisets: when two rows are the same row

## The concept

A guest list can name two different guests with the same name. As a **multiset**, the list keeps both; as a **set**, it keeps one. Which rows count as the same depends on which columns are compared, and dropping a column first can make different rows identical.

![Three source rows, two of which differ only in an unmodeled column. Deduplicated on all columns, three rows remain; with that column dropped first, the two rows merge and two remain.](figures/dedup-before-or-after-projection.svg)

*Illustrative rows. Deduplicating after dropping a column merges rows that the source kept apart.*

## The transfer

The source file holds exact duplicate rows, and staging must decide what counts as one record.

* **Same record only if every column agrees.** Two raw rows are one staged record only if they agree on all 17 source columns, `Timestamp` included; the first occurrence is kept and the unmodeled columns are dropped afterwards ([ADR-0008](../decisions/0008-staging-deduplication-grain.md#decision-outcome)).
* **Dropping first would merge distinct rows.** Deduplicating on the 13 modeled columns instead would collapse 290,051 records to 259,490, merging rows that differ only in columns the model does not keep ([ADR-0008](../decisions/0008-staging-deduplication-grain.md#findings), G1). The row count would then depend on the model's scope rather than on the source.
* **Dropping `Timestamp` would merge the most.** Deduplicating on the other 16 columns leaves 97,723 profiles; it was rejected because no mechanism was found that would make every repeated profile one respondent ([ADR-0008](../decisions/0008-staging-deduplication-grain.md#deduplicate-on-the-16-non-timestamp-columns-collapse-to-97723-profiles)).

## Where it breaks

* The guest list knows the guests are different people. The source file has no respondent identifier, so rows equal on all 17 columns may still be two people, and unequal rows may be one. Deduplicating on all columns is the choice that discards the least, not a proof of identity ([ADR-0008](../decisions/0008-staging-deduplication-grain.md#decision-outcome), Scope).
* Grain is the companion question: what one row stands for. See [grain](grain-and-cross-sections.md).

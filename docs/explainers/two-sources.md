# Two sources in one file

Why the warehouse passes its checks and still answers only one of its questions.

## What the checks show

The file's columns fall into two groups ([LOG-040](../decisions/log/LOG-040-h1-column-groups.md)), and its symptom columns match a separately published dataset, RHMCD-20 ([legacy audit, A10](../audit/legacy-audit.md#checks)). Read as two sources joined ([legacy audit, Reading branch](../audit/legacy-audit.md#reading-branch)), a question that relates the two groups tabulates columns from different sources, so any difference it shows is an artifact of how the sources were combined, not a relationship among respondents ([criteria, section 3.2](../audit/correspondence-criteria.md#32-branch-h1-holds)).

![A matrix of the nine business questions against the 17 source columns, split into two column groups: group 1, the eight columns whose names are in the OSMI 2014 schema, and group 2, the eight symptom columns and Occupation, matched to RHMCD-20. Eight questions use columns from both groups; only Q5, on time spent indoors, uses columns from group 2 alone.](../audit/figures/one-question-of-nine.svg)

*Only the question on time spent indoors stays within one column group ([evidence, section 4](../audit/correspondence-evidence.md#4-questions)).*

## What it means for the questions

Q5, on time spent indoors, stays within one group and can be answered. Q7, the help-seeking question, relates `treatment`, in one group, to stress recognition and the self-reported symptom profile, in the other, so it cannot be answered with this file ([evidence, section 4](../audit/correspondence-evidence.md#4-questions)). Some questions also have too few responses, or none, in some cells (same section). The computation is not what fails: the outputs reproduce exactly ([evidence, section 1](../audit/correspondence-evidence.md#1-reproduction)).

## What a working resource would need

A resource that could answer the questions that relate the two sources would record symptoms and treatment from the same respondent ([criteria, section 3.2](../audit/correspondence-criteria.md#32-branch-h1-holds)), with a documented provenance ([ADR-0001](../decisions/0001-position-as-portfolio-project.md)), and with the measures this file lacks, such as stigma, a need assessed rather than self-reported, and more than one observation of the same respondent over time ([conceptual framework, section 5](../conceptual-framework.md#5-what-this-dataset-cannot-measure)). What the outputs cannot serve under ADR-0001 is in [LOG-046](../decisions/log/LOG-046-user-of-the-outputs.md).

# Conceptual framework

## 1. Purpose and scope

This document is not, and does not aim to become, an academic publication. Per [ADR-0001](decisions/0001-position-as-portfolio-project.md), this project does not pursue academic publication: the dataset's provenance is undocumented by its source, so no claim here can be read as a finding about any population. That constraint does not lower the bar for how the argument is built — it changes what the argument is allowed to claim, not how carefully it has to be made. Every statement below follows the same evidence discipline used in the ADRs and in `docs/audit/legacy-audit.md`: a claim is either backed by a cited source, marked as this document's own interpretation (not yet confirmed), or marked as pending a check that has not run yet. Nothing is asserted past what its source actually supports.

## 2. Levels of evidence

The project's argument rests on three levels, and they are not interchangeable:

1. **Mechanism.** A general claim about why people do or don't seek help for mental health problems, supported by the literature in §3, independent of this dataset.
2. **Test case.** This dataset, used to demonstrate a methodology — dimensional modeling, ETL, indicator design — not as evidence about a real population, given its undocumented provenance (ADR-0001, P1–P3, P6).
3. **Extrapolation to the present.** Not attempted here. It would require literature published after 2014 that explicitly connects the mechanism in §3 to current populations, which is outside what this document sets out to do.

## 3. Literature basis for the mechanism

- **Clement et al. 2015.** *Psychological Medicine* 45(1):11–27. Meta-analysis of 144 studies. Stigma is associated with reduced help-seeking at a modest median effect size (d = -0.27). Among specific barriers assessed, concern about disclosure was the most frequently reported, while stigma overall ranked fourth among the barriers studied — i.e., a real but partial channel, not the dominant one.
- **Corrigan 2004.** *American Psychologist* 59(7):614–625. Label avoidance: people avoid the label of "mentally ill," which reduces engagement with services through a mechanism distinct from stigma toward others.
- **Andersen 1995.** *Journal of Health and Social Behavior* 36(1):1–10. Behavioral model of health services use: predisposing, enabling, and need (perceived vs. evaluated) components. Perceived need is often a stronger driver of care-seeking than professionally evaluated need. This is the framework used for the variable mapping in §4.
- **Andrade et al. 2014.** *Psychological Medicine* 44(6):1303–1317. WHO World Mental Health surveys, n=63,678 with a 12-month DSM-IV disorder across 24 countries. Low perceived need is the most common reason for not initiating treatment. Attitudinal barriers outweigh structural barriers overall — but this reverses by severity: attitudinal barriers dominate mild-to-moderate cases, structural barriers dominate severe cases. A desire to handle the problem on one's own was the most common attitudinal barrier (63.8% among respondents who did perceive a need).
- **Schnyder et al. 2017.** *British Journal of Psychiatry* 210:261–268. Meta-analysis, 27 studies. Personal negative attitudes toward help-seeking (OR=0.80, 95% CI 0.73–0.88) and personal stigma toward people with a mental illness (OR=0.82, 95% CI 0.69–0.98) are associated with less active help-seeking. Self-stigma is not significant (OR=0.88, 95% CI 0.76–1.03); perceived public stigma shows no association at all. The authors conclude that campaigns should target personal attitudes, not broad public opinion.

**Synthesis.** Across this literature, stigma is a real but modest and partial channel. Low perceived need and personal attitudes toward help-seeking are stronger, more consistent predictors of not seeking treatment than public or perceived stigma is. This is the mechanism the project's motivating idea sits inside — but the literature does not support a simple "stigma is the reason people don't seek treatment" story, and this document does not flatten it into one.

## 4. Variable mapping to Andersen's Behavioral Model

| Variable | Andersen component | Basis | Note |
|---|---|---|---|
| `Gender` | Predisposing — demographic | Source-described | — |
| `Country` | Contextual / external environment | Source-described | A contextual layer beyond the individual-level triad; this placement is this document's own interpretation, with no reference in §8 cited for it |
| `Occupation` | Predisposing — social structure | No source description (ADR-0001, P6) | Semantics assumed from how the report uses it |
| `family_history` | Predisposing — health beliefs | Source-described: "family history of mental illness" | — |
| `Growing_Stress` | Perceived need | No source description | Semantics assumed; the closest thing to a direct perceived-need self-report item in this dataset |
| `Days_Indoors`, `Mood_Swings`, `Coping_Struggles`, `Social_Weakness` | Self-reported correlates adjacent to perceived need | No source description | **Not** evaluated need — evaluated need requires professional or clinical assessment, which this dataset does not have |
| `Indicador_Inferido_Estrés` (legacy derived flag; replaced by [`symptom_cluster`](specification/definitions.md#symptom_cluster) and [`explicit_recognition`](specification/definitions.md#explicit_recognition)) | An alternate perceived-need proxy | Heuristic; see the [validity caveat](specification/definitions.md#symptom_cluster) of `symptom_cluster` | Not evaluated need, despite what the name suggests |
| `care_options` | Enabling — community resources | No source description. The OpenML deposit of the OSMI 2014 survey gives a question text for a column of the same name ([evidence](dataset-provenance.md#evidence)); it is a candidate premise for this column's meaning, matched by name only | Semantics assumed |
| `treatment` | Use | Source-described: "Have you sought treatment for a mental health condition?" (lifetime) | The legacy report reads this as "currently in treatment" — the two readings are not interchangeable, and matter for §6 |
| `mental_health_interview` | Reinterpreted here as disclosure willingness (attitudinal), not exposure | Source-described: "Would you bring up a mental health issue with a potential employer in an interview?" | The legacy report reads this as "participated in a mental-health interview." The reading here is this document's interpretation of the source's question text, adopted by [ADR-0003](decisions/0003-redefine-indicators-14-to-16.md) and [ADR-0004](decisions/0004-revise-business-questions.md) |

Rows marked "no source description" or "reinterpreted here" carry an assumption, not an established fact, into the [specification](specification.md).

---

### Addendum (2026-09-23)
The reading of mental_health_interview above corrects the legacy's original treatment of the field. See ADR-0000, Findings (F3 addendum), for what was originally considered when the legacy model was designed and why the project now operates on the corrected reading.

---

## 5. What this dataset cannot measure

- **Stigma itself.** No stigma scale, no perceived/personal/self-stigma items of any kind.
- **Courage**, the project's own motivating construct — nothing in the dataset measures it.
- **Evaluated need.** Only self-report exists; no clinical or professional assessment.
- **Causality or sequence.** One timestamp per respondent, cross-sectional; no panel structure.
- **Postponement or delay.** No time-to-treatment variable exists anywhere in the file.
- **Representativeness of any population.** Provenance is undocumented by the source (ADR-0001, P1–P3, P6); the marginal skew in the source-described columns versus the near-uniform symptom columns (P8) is consistent with — though not proof of — a file that combines sources with different sampling designs (H1, H3; see §7).


---

### Addendum (2026-09-25)

A13 ([legacy audit](audit/legacy-audit.md#checks)) tested the duplication found by A4 directly. Its result, recorded there, rules out a complete combinatorial grid and simple batch loading, and shows the structure non-uniform across the file, concentrated in the United States and the United Kingdom. This sharpens, without resolving, the H1 concern above ([ADR-0001, Hypotheses](decisions/0001-position-as-portfolio-project.md#hypotheses-not-findings)): a construction artifact concentrated in the two countries an OSMI-type source would skew toward is a more specific pattern than an even cross-file association, and is consistent with — though still not proof of — the same source-mixing hypothesis. A5, A6 and A10 test this with external comparison data; A13's mechanism remains unidentified.

---


## 6. Indicators 14–16: what they can support

This section settles what construct each indicator's variables can honestly support, given the corrections in §4. It does not fix SQL-level formulas, numerators, or denominators — that belongs to the [specification](specification/indicators.md), per ADR-0000's confirmation that "each indicator definition names a construct its variables can support."

### Indicator 14 (legacy name "% with unrecognized symptoms who seek treatment")

**Problems (F3):** no comparison group; "Maybe" is folded into "No" against the report's own granularity section, which treats them as distinct; and now that `treatment` reads as lifetime rather than current, someone who sought treatment in the past without reporting stress now may reflect resolved treatment, not unrecognized symptoms.

**What the variables can support:** a comparison of lifetime treatment-seeking between the implicit three-symptom cluster (no explicit stress report) and an explicit-stress comparison group. Not a measure of "recognition" as a psychological state — that requires something this dataset doesn't have.

**Direction:** something on the order of "lifetime treatment-seeking rate, implicit-cluster group vs. explicit-stress group," with both groups defined and reported.

### Indicator 15 (legacy name "% with resources available who don't seek treatment")

**Problems (F3):** counts "Not sure" as available; filters on a derived flag that already includes explicit self-reporters, blurring the line it's meant to draw.

**What the variables can support:** a lifetime treatment-seeking rate by care-options response, with "Yes" and "Not sure" reported and analyzed separately rather than merged.

**Direction:** "care-options-to-treatment conversion rate" (renamed "Lifetime treatment-seeking rate by care-options response", [LOG-014](decisions/log/LOG-014-indicator-renames-and-residual-identifiers.md)), split by "Yes" and "Not sure" responses.

### Indicator 16 (legacy name "% postponing treatment despite having resources")

**Problems (F3):** no time dimension anywhere in its formula — it cannot measure postponement by definition.

**Reframed by §4:** if `mental_health_interview` is a disclosure-willingness item rather than an exposure event, this indicator was never about postponement — it is closer to whether disclosure willingness co-occurs with not reporting lifetime treatment-seeking among respondents who report "Yes" or "Not sure" for care options.

**Direction:** something like "disclosure willingness and care-options availability, relative to lifetime treatment-seeking" — explicitly not "postponement," since nothing in the file carries a delay or time-to-treatment measure.

---

### Addendum (2026-09-25)

Indicators 14–16 were finalized in [ADR-0003](decisions/0003-redefine-indicators-14-to-16.md) and consolidated in [ADR-0006](decisions/0006-final-questions-and-indicators.md); those are now the source of record for what each indicator measures, and `docs/specification/indicators.md` is the implementation contract this section fed into. This section is kept for traceability of the reasoning that led there, with one correction: indicator 14's **Direction** above ("implicit-cluster group vs. explicit-stress group, with both groups defined and reported") describes what ADR-0003 calls Design B, which was considered and not chosen. The accepted design (Design A) restricts the population to the three-symptom cluster only and partitions it by `growing_stress`'s three levels, so the comparison groups differ only in explicit recognition, not in symptom profile — Design B's explicit group carried no such restriction, which is exactly why ADR-0003 rejected it (it would confound recognition with severity). Indicators 15 and 16's directions above are consistent with the final design.

---

## 7. Threats to validity

This section is provisional while checks it depends on are pending; the status of each check is in the [audit table](audit/legacy-audit.md#checks).

- **Self-report only**, across every variable used here — common-method bias, no independent verification of any item.
- **Cross-sectional.** No causal or temporal claim is possible from this data.
- **Undocumented provenance.** No population can be named or assumed (ADR-0001, P1–P3, P6).
- **H1 and H3** (stated in [ADR-0001, Hypotheses](decisions/0001-position-as-portfolio-project.md#hypotheses-not-findings); their checks and the status of each in the [audit table](audit/legacy-audit.md#checks)). If the file combines an OSMI-type source with a second source — plausibly RHMCD-20 (H3) — any association between the source-described columns and the symptom columns would be an artifact of merging two unrelated files, not a real relationship. This would undermine any cross-tabulation the new pipeline computes across those [two column groups](decisions/log/LOG-040-h1-column-groups.md), not just the indicators already flagged.
- **The convergence threshold** of the legacy flag `Indicador_Inferido_Estrés`, carried into `symptom_cluster`: see the [validity caveat](specification/definitions.md#symptom_cluster).
- **Fan-out in `Dim_Sintomas` (F1).** The rebuild's dimensions follow the [dimension grain rule](specification/definitions.md#dimension-grain-rule), and checks C1 and C2 pass ([closure record](audit/phase4-closure.md#4-acceptance-checks-c1c11)). The legacy's own fan-out is still unquantified (A2, status in the [audit table](audit/legacy-audit.md#checks)), so a legacy indicator compared with a newly computed one may carry it.

## 8. References

- Clement, S., Schauman, O., Graham, T., Maggioni, F., Evans-Lacko, S., Bezborodovs, N., Morgan, C., Rüsch, N., Brown, J. S. L., & Thornicroft, G. (2015). What is the impact of mental health-related stigma on help-seeking? A systematic review of quantitative and qualitative studies. *Psychological Medicine*, 45(1), 11–27.
- Corrigan, P. (2004). How stigma interferes with mental health care. *American Psychologist*, 59(7), 614–625.
- Andersen, R. M. (1995). Revisiting the behavioral model and access to medical care: does it matter? *Journal of Health and Social Behavior*, 36(1), 1–10.
- Andrade, L. H., Alonso, J., Mneimneh, Z., Wells, J. E., Al-Hamzawi, A., Borges, G., Bromet, E., Bruffaerts, R., de Girolamo, G., de Graaf, R., Florescu, S., Gureje, O., Hinkov, H. R., Hu, C., Huang, Y., Hwang, I., Jin, R., Karam, E. G., Kovess-Masfety, V., Levinson, D., Matschinger, H., O'Neill, S., Posada-Villa, J., Sagar, R., Sampson, N. A., Sasu, C., Stein, D. J., Takeshima, T., Viana, M. C., Xavier, M., & Kessler, R. C. (2014). Barriers to mental health treatment: results from the WHO World Mental Health surveys. *Psychological Medicine*, 44(6), 1303–1317.
- Schnyder, N., Panczak, R., Groth, N., & Schultze-Lutter, F. (2017). Association between mental health-related stigma and active help-seeking: systematic review and meta-analysis. *British Journal of Psychiatry*, 210, 261–268.


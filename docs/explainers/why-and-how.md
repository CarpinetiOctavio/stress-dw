# Why and how

Why a warehouse was built, and rebuilt, on a file whose outputs cannot be used as findings.

## The original objective

The course project, preserved at [`stress-dw-legacy`](https://github.com/CarpinetiOctavio/stress-dw-legacy), states its main objective in its report ([report at `legacy-original`](https://github.com/CarpinetiOctavio/stress-dw-legacy/blob/legacy-original/Informe%20DW/DW%20-%20Estr%C3%A9s%20y%20Salud%20Mental.pdf), p. 5):

"Objetivo estratégico principal: Proporcionar evidencia estadística que permita sensibilizar sobre el impacto del estrés en la salud mental, identificar brechas en la búsqueda de ayuda profesional (especialmente diferencias de género), y contribuir a la desestigmatización de los problemas de salud mental."
→ English: "Main strategic objective: to provide statistical evidence that raises awareness of the impact of stress on mental health, identifies gaps in seeking professional help (especially gender differences), and contributes to the destigmatization of mental-health problems."

Its questions follow that aim in order: stress by gender over time (Q1), the gender gap in seeking treatment (Q4), access to mental-health resources by country, occupation and gender (Q6), and the postponement of treatment despite recognition and available resources, linked to the cultural normalization of stress (Q7.2) (same report, pp. 6–7). The rebuild rewords several of these questions, Q7.2 among them, which no longer speaks of postponement, since no time-to-treatment variable exists ([ADR-0004](../decisions/0004-revise-business-questions.md)). That original purpose is recorded as documentary only; no criterion is built on it ([LOG-046](../decisions/log/LOG-046-user-of-the-outputs.md)).

## Why the result cannot answer it

The motivating question, help-seeking by gender, is the one this file cannot answer: Q4 and Q7 relate columns that come from two different sources ([two sources](two-sources.md); [evidence, section 4](../audit/correspondence-evidence.md#4-questions)). The audit of the course version first found the errors that led to rebuilding from scratch instead of continuing ([ADR-0000](../decisions/0000-rebuild-from-scratch-instead-of-continuing-legacy.md)) and the provenance gaps under which no output is read as a finding about any population ([ADR-0001](../decisions/0001-position-as-portfolio-project.md)). The checks that later found the two sources are recorded in the same audit document ([legacy audit, A10](../audit/legacy-audit.md#checks); [Reading branch](../audit/legacy-audit.md#reading-branch)). The literature that motivates the question is in the [conceptual framework, section 3](../conceptual-framework.md#3-literature-basis-for-the-mechanism); it motivates the work and is not supported or contradicted by any output here.

## In the first person

<!-- first-person:start -->
> 
> I start from a declared bias. My focus is on men’s mental health, without taking anything from women’s; it is not about blaming anyone, and it is also self-criticism. Men die by suicide more often than women in every country with comparable data, and in some, such as the United States, about four times as often ([Our World in Data](../conceptual-framework.md#motivating-statistic), from the WHO Mortality Database). It has been close to me for years, in the town in Córdoba where I grew up, and therapy is where I began to grasp its size. The traditional image of the man who provides, who is strong and does not show what he feels, makes it harder to say that something is wrong, and I believe that talking about it well helps more than silence.
>
> The objective of providing statistical evidence came from there: evidence that informs decisions, read from the context a person starts from. That is why the questions slice by country and occupation as well as by sex: a result that matches one’s own country, occupation and age informs more than a global average. I thought of it as more representative; it is a disaggregation, more specific, and each slice holds only if the sample behind it does.
>
> Once the file was known not to support findings, I kept going. Saying that I would contribute to this field given reliable data proves nothing; a project that shows what I would do with it does. The best cook is not the one with the best ingredients, but the one who takes what is at hand to its best expression.
>
> — @CarpinetiOctavio
<!-- first-person:end -->

Help is available: [findahelpline.com](https://findahelpline.com).

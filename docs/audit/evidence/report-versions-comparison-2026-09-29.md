# Comparison of the two versions of the legacy report

Taken on 2026-09-29. This is the record that [ADR-0012](../../decisions/0012-cite-only-frozen-and-versioned-sources-as-evidence.md) requires for its finding S3 (rule 3): an analysis over an unversioned input, recorded with its method and the SHA-256 of each input. It contains no indicator value.

## Inputs

| Version | File | Pages | SHA-256 | Where |
|---------|------|-------|---------|-------|
| Frozen report | `Informe DW/DW - Estrés y Salud Mental.pdf` | 127 | `039e43859a5c5dddec8eaefe12f5dde5507c23bf2a63d29d774d8dd99c69dc81` | `stress-dw-legacy` at `legacy-original` (`f2308d29217c8130a14875d7dad7070272b92d28`) |
| Continuation | `DW - Stress & Mental Health - DW-LEGACY.pdf` | 140 | `545f080ad16f23c6eedd8fa80cc3604b726e20f989e019429fc75ab9127547c6` | Not versioned; this record is the only trace of its text |

## Method

1. Text extraction with `pdftotext` (poppler 26.08.0), default mode, on both PDFs.
2. Normalization: U+200B (zero-width space) and `<br>` removed; lines holding only a page number dropped; all whitespace collapsed to one space.
3. Whole document: word-level comparison with Python's `difflib.SequenceMatcher` (`autojunk=False`), once over the full normalized text and once over the text from the heading "Contexto del Proyecto" onwards, which excludes the cover and the table of contents.
4. Sections: each section is taken from its title to the next section's title. Every title used occurs exactly twice in each version, once in the table of contents and once in the body; the body occurrence is used. Taking the first occurrence after "Contexto del Proyecto" gives the same text, and so the same hashes. Each section is hashed with SHA-256 over its normalized text (UTF-8).

Text that is an embedded image in a PDF is not extracted. Where the frozen report shows code or a table as an image and the continuation shows it as text, the difference appears as an insertion in the continuation; it is a difference of form, not of content.

## Whole document

| Scope | Similarity | Differences |
|-------|-----------|-------------|
| Full text | 0.9632 | 52 |
| From "Contexto del Proyecto" (cover and table of contents excluded) | 0.9626 | 50 |

## Sections

| Section | SHA-256, frozen report | SHA-256, continuation | Identical |
|---------|------------------------|-----------------------|-----------|
| Phase 1 (a): questions | `e35dea6331d74731750a7f7a117df3b64a7d5251024ae65abc4340cdb40ed870` | `4e627a22b484d6a5d80119f67c17b89fddeae934c43f6d49247e4e5573758cf8` | no |
| Phase 1 (b): indicators and perspectives | `d57c545fb56daca0a855bcc5a4be9abf8d669a08c4b847e23633be51b504088a` | `d57c545fb56daca0a855bcc5a4be9abf8d669a08c4b847e23633be51b504088a` | yes |
| Phase 2: derived variable | `314719754d57142069fdf3ef6d5f3de8d5c9e93b8cd76ff505d3033c56cbde91` | `314719754d57142069fdf3ef6d5f3de8d5c9e93b8cd76ff505d3033c56cbde91` | yes |
| Phase 2 (a): indicator formulas | `5071a26c0142e2accfda6ff73546dd6d2a8550b908999961ceef91a03e323888` | `5071a26c0142e2accfda6ff73546dd6d2a8550b908999961ceef91a03e323888` | yes |
| Phase 2 (c): granularity | `927d8ffed8e877493897d27abd86ac6ed0cfe2dede9ae3c0b7c1e18ba8ea12c1` | `a8b11fc3256f900c453bd7a74e692fd575ff378adc3ad2ec7a7d7de7739eee1b` | no |

Where the two differ:

* **Phase 1 (a): questions.** One word: the objective of the fourth question reads "considerando diferencias de género" in the frozen report and "considerando las diferencias de género" in the continuation.
* **Phase 2 (c): granularity.** Table layout only: the extraction orders the cells of the granularity table differently (the header "Nivel de Granularidad" split as "Granularida d" in the frozen report; the position of "Mensual"). No word of content differs.

## Differences by kind

All 52 differences over the full text, classified. None changes the model, an indicator formula, or any element that F1–F4 of [ADR-0000](../../decisions/0000-rebuild-from-scratch-instead-of-continuing-legacy.md) rely on.

| Kind | Count |
|------|-------|
| code or table that is an image in the frozen report and text in the continuation | 18 |
| BI tool named | 11 |
| table layout (extraction order) | 7 |
| technical content added | 7 |
| editorial wording | 4 |
| draft sentence deleted (aligned against table text that is an image in the frozen report) | 3 |
| cover | 2 |

### Full list

Excerpts are cut at 90 characters. Word counts refer to the normalized text.

| # | Kind | Operation | Frozen report (words) | Continuation (words) |
|---|------|-----------|-----------------------|----------------------|
| 1 | cover | replace | 5: Materia: Base de datos aplicada | 6: Subject: Applied database - Database II |
| 2 | cover | replace | 8: Integrantes: [names omitted] | 2: Done by: |
| 3 | BI tool named | replace | 2: Power BI. | 10: herramientas de Business Intelligence (en este proyecto, Google Looker Studio). |
| 4 | editorial wording | insert | 0: — | 1: las |
| 5 | table layout (extraction order) | delete | 3: Campos OLTP Involucrados | 0: — |
| 6 | table layout (extraction order) | delete | 2: por aislamiento | 0: — |
| 7 | table layout (extraction order) | insert | 0: — | 5: Campos OLTP Involucrados por aislamiento |
| 8 | table layout (extraction order) | delete | 5: Nivel de Granularida d Comentario | 0: — |
| 9 | table layout (extraction order) | insert | 0: — | 1: Mensual |
| 10 | table layout (extraction order) | replace | 3: (Enero-Diciembre ) Mensual | 1: (Enero-Diciembre) |
| 11 | table layout (extraction order) | insert | 0: — | 4: Nivel de Granularidad Comentario |
| 12 | BI tool named | insert | 0: — | 2: herramientas como |
| 13 | BI tool named | replace | 1: BI | 4: BI, Looker Studio, Tableau |
| 14 | BI tool named | replace | 4: otras herramientas de análisis | 1: similares |
| 15 | code or table that is an image in the frozen report and text in the continuation | insert | 0: — | 13: id_tiempo anio mes nombre_mes periodo trimestre semestre 2014 Agosto 2014-08 2014 Septiemb… |
| 16 | code or table that is an image in the frozen report and text in the continuation | insert | 0: — | 7: id_genero género descripción Male Masculino Female Femenino |
| 17 | code or table that is an image in the frozen report and text in the continuation | insert | 0: — | 17: id_ género descripción Yes Con antecedentes familiares de salud mental No Sin antecedentes… |
| 18 | code or table that is an image in the frozen report and text in the continuation | insert | 0: — | 18: id_ocupacion occupation descripcion Corporate Empleado corporativo Student Estudiante Busi… |
| 19 | draft sentence deleted (aligned against table text that is an image in the frozen report) | replace | 2: El objetivo | 7: id_pais country region codigo_iso United States America |
| 20 | draft sentence deleted (aligned against table text that is an image in the frozen report) | replace | 11: DW es para El objetivo de mi proyecto es la construccion | 8: Norte USA United Kindom Europa GBR Canada America |
| 21 | draft sentence deleted (aligned against table text that is an image in the frozen report) | replace | 7: DW para ser empleado como recurso fundamentado | 9: Norte CAN Australia Oceania AUS Brazil America Latina BRA |
| 22 | code or table that is an image in the frozen report and text in the continuation | insert | 0: — | 29: id_aislamiento days_indoors orden categoria Go out Every day Bajo 1 - 14 days Bajo 15 - 30… |
| 23 | code or table that is an image in the frozen report and text in the continuation | insert | 0: — | 18: id_acceso care_options treatment mental_health_inte rview Yes Yes Yes Yes No Yes No No No … |
| 24 | code or table that is an image in the frozen report and text in the continuation | insert | 0: — | 24: id_acceso care_options mental_health_interview Yes Yes Yes No Yes Maybe No Yes No No No Ma… |
| 25 | code or table that is an image in the frozen report and text in the continuation | insert | 0: — | 26: Dim_Genero (id=1, genero=’Male’) → Puede estar relacionado con: - - - Hechos (id_hecho=1, … |
| 26 | code or table that is an image in the frozen report and text in the continuation | insert | 0: — | 39: SELECT g.genero, t.mes, t.nombre_mes, AVG(h.porcentaje_estres) AS promedio_estres FROM Hec… |
| 27 | code or table that is an image in the frozen report and text in the continuation | insert | 0: — | 36: -- Verificar que todos los id_tiempo en hechos existen en Dim_Tiempo SELECT COUNT(*) FROM … |
| 28 | code or table that is an image in the frozen report and text in the continuation | insert | 0: — | 38: -- Contar cuántos hechos referencian cada género SELECT g.genero, COUNT(h.id_hecho) AS can… |
| 29 | code or table that is an image in the frozen report and text in the continuation | insert | 0: — | 63: -- Verificar que todas las dimensiones están siendo utilizadas SELECT 'Dim_Tiempo' AS dime… |
| 30 | BI tool named | replace | 4: analizados en Power BI. | 8: consumidos por cualquier herramienta de visualización de datos. |
| 31 | code or table that is an image in the frozen report and text in the continuation | insert | 0: — | 93: CREATE TABLE mental_health_staging ( id INT AUTO_INCREMENT PRIMARY KEY, -- Campos exactame… |
| 32 | code or table that is an image in the frozen report and text in the continuation | insert | 0: — | 15: def insertar_datos_batch(conn, df, batch_size=1000): for start_idx in range(0, total_regis… |
| 33 | code or table that is an image in the frozen report and text in the continuation | insert | 0: — | 9: SELECT COUNT(*) FROM mental_health_staging; -- Resultado esperado: 290,051 registros |
| 34 | code or table that is an image in the frozen report and text in the continuation | insert | 0: — | 25: SELECT COUNT(*) FROM mental_health_staging WHERE Gender IS NULL OR Country IS NULL OR Grow… |
| 35 | code or table that is an image in the frozen report and text in the continuation | insert | 0: — | 18: SELECT Gender, COUNT(*) as cantidad FROM mental_health_staging GROUP BY Gender; -- Verific… |
| 36 | code or table that is an image in the frozen report and text in the continuation | insert | 0: — | 17: SELECT MIN(STR_TO_DATE(Timestamp, '%m/%d/%Y')) as fecha_min, MAX(STR_TO_DATE(Timestamp, '%… |
| 37 | editorial wording | insert | 0: — | 1: su |
| 38 | BI tool named | replace | 2: Power BI. | 6: una herramienta de visualización de datos. |
| 39 | technical content added | insert | 0: — | 223: Librerias externas (Instaladas vía pip) Libreria Script Rol pandas 01, 02, 06 Lee el CSV c… |
| 40 | technical content added | insert | 0: — | 130: ProyectoDB2/ ├── config/ │ └── config.py ├── data/ │ ├── raw/ │ │ └── mental_health.csv │ … |
| 41 | technical content added | replace | 3: Centraliza la configuración | 4: config/config.py centraliza los parámetros |
| 42 | technical content added | replace | 3: MySQL: Justificación: Centralizar | 9: MySQL, las rutas de los archivos de entrada/salida y |
| 43 | technical content added | replace | 5: configuración facilita el mantenimiento y | 24: ruta del log. La contraseña de base de datos no está hardcodeada: se lee desde la variable… |
| 44 | technical content added | replace | 1: hardcodear | 1: exponer |
| 45 | technical content added | replace | 2: múltiples archivos. | 72: el código fuente. """ Archivo de configuración para conexión a MySQL """ import os # Confi… |
| 46 | BI tool named | replace | 1: 06_exportar_powerbi.py | 1: 06_exportar.py |
| 47 | BI tool named | insert | 0: — | 6: con todos los datos del DW |
| 48 | BI tool named | replace | 1: importar | 2: su análisis |
| 49 | BI tool named | replace | 2: Power BI. | 5: herramientas de visualización de datos. |
| 50 | BI tool named | replace | 2: Power BI | 6: La herramienta de visualización de datos |
| 51 | editorial wording | insert | 0: — | 1: los |
| 52 | editorial wording | replace | 1: actualizados | 1: actualizados. |

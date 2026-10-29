-- Check A7 (F2), second part: the unweighted AVG of porcentaje_tratamiento by
-- genero, the aggregation of the Looker Studio chart, over the flat export at
-- legacy-original ("CSV procesado /dw_salud_mental.csv"). The single parameter
-- is the path of a copy of that file.
SELECT
    genero,
    AVG(porcentaje_tratamiento) AS average_porcentaje_tratamiento,
    COUNT(*) AS export_rows
FROM read_csv(?)
GROUP BY genero
ORDER BY genero;

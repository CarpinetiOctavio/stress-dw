-- Check A7 (F2), first part: the treatment rate by gender over the rebuilt
-- staging_response, with explicit numerator and denominator.
SELECT
    gender,
    COUNT(*) FILTER (WHERE treatment = 'Yes') AS numerator,
    COUNT(*) AS denominator,
    COUNT(*) FILTER (WHERE treatment = 'Yes') / COUNT(*) AS rate
FROM staging_response
GROUP BY gender
ORDER BY gender;

CREATE TEMP TABLE summary AS
    SELECT
        (SELECT count(*) as total
        FROM vrm_data
        WHERE aprobo = 0) AS rechazados,
        (SELECT count(*) as total
        FROM vrm_data
        WHERE aprobo = 1) AS aprobados;

-- select the table and show the results
SELECT rechazados, aprobados, CAST(aprobados AS float) / (rechazados + aprobados) as ratio
FROM summary;
SELECT DISTINCT company, id_opec, salary
FROM job_data
WHERE job_tenure = 'NO REQUIERE EXPERIENCIA'
     AND academic_background LIKE '%ECONOMIA%'
     AND process_type = 'CONCURSO_ABIERTO'
ORDER BY salary DESC


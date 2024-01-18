-- Select the country origins and rank them by the number of non-unique fans
SELECT origin, COUNT(DISTINCT fan_id) AS nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;

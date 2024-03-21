-- script that ranks country origins of bands
SELECT origin, SUM(fans) as bands
FROM metal_bands
GROUP BY origin
ORDER BY bands DESC;

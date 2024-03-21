-- script that ranks country origins of bands
SELECT origin, SUM(fans) as band
FROM metal_bands
GROUP BY origin
ORDER BY band DESC;
